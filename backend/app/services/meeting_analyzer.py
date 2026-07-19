from __future__ import annotations

from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from pydantic import ValidationError
import re
from app.core.config import PROJECT_ROOT, AppSettings
from app.schemas.meeting_schema import (
    MeetingAnalysisResult,
    Participant,
    TaskMetrics,
)
from app.services.gemini_client import GeminiClient
from app.services.task_metrics import TaskMetricsCalculator


SYSTEM_PROMPT_PATH = PROJECT_ROOT / "app" / "prompts" / "meeting_analysis_system.txt"
USER_PROMPT_PATH = PROJECT_ROOT / "app" / "prompts" / "meeting_analysis_user.txt"


WEEKDAY_NAMES_TR = {
    0: "Pazartesi",
    1: "Salı",
    2: "Çarşamba",
    3: "Perşembe",
    4: "Cuma",
    5: "Cumartesi",
    6: "Pazar",
}


class MeetingAnalyzerError(RuntimeError):
    """Raised when meeting analysis fails."""


def read_text_file(path: Path) -> str:
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    content = path.read_text(encoding="utf-8").strip()

    if not content:
        raise ValueError(f"File is empty: {path}")

    return content


def get_reference_date_context(timezone: str) -> tuple[str, str, str]:
    try:
        now = datetime.now(ZoneInfo(timezone))
    except Exception as exc:
        raise MeetingAnalyzerError(f"Invalid timezone: {timezone}") from exc

    reference_date = now.date().isoformat()
    reference_weekday = WEEKDAY_NAMES_TR[now.weekday()]

    return reference_date, reference_weekday, timezone


UNRESOLVED_PERSON_PATTERN = re.compile(
    r"^(?:SPEAKER_\d+|UNKNOWN(?:_\d+)?)$",
    flags=re.IGNORECASE,
)


def normalize_person_name(value: str | None) -> str | None:
    if value is None:
        return None

    normalized = " ".join(str(value).strip().split())

    if not normalized:
        return None

    if normalized.casefold() in {"none", "null", "-"}:
        return None

    return normalized


def is_unresolved_person(value: str | None) -> bool:
    normalized = normalize_person_name(value)

    if normalized is None:
        return False

    return bool(UNRESOLVED_PERSON_PATTERN.fullmatch(normalized))


def reconcile_participants(
    result: MeetingAnalysisResult,
    expected_participant_count: int | None,
) -> MeetingAnalysisResult:
    """
    Katılımcı sayısını kullanıcı tarafından girilen sayıya kesin olarak eşitler.

    Kurallar:
    - Gerçek isimler tekilleştirilir.
    - SPEAKER_XX ve UNKNOWN_XX gerçek isim olarak sayılmaz.
    - Eksik kişi sayısı kadar UNKNOWN_XX oluşturulur.
    - Aynı çözülemeyen konuşmacıya ait görevler aynı UNKNOWN'a atanır.
    - Fazladan çözülemeyen speaker etiketi varsa son UNKNOWN'a birleştirilir.
    """
    if expected_participant_count is None:
        return result

    if expected_participant_count < 1:
        raise ValueError(
            "expected_participant_count must be at least 1."
        )

    known_participants: dict[str, Participant] = {}
    unresolved_roles: list[str] = []

    def add_known_participant(
        name: str | None,
        role: str | None = None,
    ) -> None:
        normalized_name = normalize_person_name(name)

        if normalized_name is None:
            return

        if is_unresolved_person(normalized_name):
            if role and role not in unresolved_roles:
                unresolved_roles.append(role)
            return

        key = normalized_name.casefold()

        if key not in known_participants:
            known_participants[key] = Participant(
                name=normalized_name,
                role=role,
            )
            return

        existing_participant = known_participants[key]

        if not existing_participant.role and role:
            known_participants[key] = existing_participant.model_copy(
                update={"role": role}
            )

    # Birinci kaynak: Gemini participant çıktısı.
    for participant in result.participants:
        add_known_participant(
            name=participant.name,
            role=participant.role,
        )

    # Participant listesinde unutulmuş gerçek görev sahiplerini de al.
    for action_item in result.action_items:
        add_known_participant(action_item.owner)

    # Gerçek katılımcılar.
    resolved_participants = list(known_participants.values())

    if len(resolved_participants) > expected_participant_count:
        print(
            "[WARN] More real participant names were resolved than expected. "
            f"resolved={len(resolved_participants)}, "
            f"expected={expected_participant_count}"
        )

        resolved_participants = resolved_participants[
            :expected_participant_count
        ]

    missing_participant_count = (
        expected_participant_count - len(resolved_participants)
    )

    unknown_names = [
        f"UNKNOWN_{index:02d}"
        for index in range(1, missing_participant_count + 1)
    ]

    unknown_participants: list[Participant] = []

    for index, unknown_name in enumerate(unknown_names):
        role = (
            unresolved_roles[index]
            if index < len(unresolved_roles)
            else None
        )

        unknown_participants.append(
            Participant(
                name=unknown_name,
                role=role,
            )
        )

    final_participants = (
        resolved_participants + unknown_participants
    )

    # Görev sahiplerinde kullanılacak kanonik isimler.
    canonical_names = {
        participant.name.casefold(): participant.name
        for participant in final_participants
        if not is_unresolved_person(participant.name)
    }

    unresolved_owner_map: dict[str, str] = {}

    def reconcile_owner(owner: str | None) -> str | None:
        normalized_owner = normalize_person_name(owner)

        if normalized_owner is None:
            return None

        # Gerçek bir kişi adıysa kanonik yazımını kullan.
        if not is_unresolved_person(normalized_owner):
            return canonical_names.get(
                normalized_owner.casefold()
            )

        # Tüm katılımcı isimleri bulunduysa UNKNOWN üretme.
        if not unknown_names:
            return None

        raw_owner_key = normalized_owner.upper()

        if raw_owner_key not in unresolved_owner_map:
            # İlk çözülemeyen speaker UNKNOWN_01,
            # ikincisi UNKNOWN_02 şeklinde eşlenir.
            # Speaker sayısı UNKNOWN slotundan fazlaysa son UNKNOWN'a birleşir.
            unknown_index = min(
                len(unresolved_owner_map),
                len(unknown_names) - 1,
            )

            unresolved_owner_map[raw_owner_key] = (
                unknown_names[unknown_index]
            )

        return unresolved_owner_map[raw_owner_key]

    updated_action_items = [
        action_item.model_copy(
            update={
                "owner": reconcile_owner(action_item.owner)
            }
        )
        for action_item in result.action_items
    ]

    updated_decisions = [
        decision.model_copy(
            update={
                "owner": reconcile_owner(decision.owner)
            }
        )
        for decision in result.decisions
    ]

    updated_open_questions = [
        question.model_copy(
            update={
                "owner": reconcile_owner(question.owner)
            }
        )
        for question in result.open_questions
    ]

    reconciled_result = result.model_copy(
        update={
            "participants": final_participants,
            "action_items": updated_action_items,
            "decisions": updated_decisions,
            "open_questions": updated_open_questions,
        }
    )

    # Hard invariant: Backend hiçbir koşulda farklı sayıda kişi döndürmesin.
    actual_count = len(reconciled_result.participants)

    if actual_count != expected_participant_count:
        raise MeetingAnalyzerError(
            "Participant reconciliation failed. "
            f"expected={expected_participant_count}, "
            f"actual={actual_count}"
        )

    return reconciled_result

class MeetingAnalyzer:
    """Analyzes meeting transcripts using an LLM."""

    def __init__(self, settings: AppSettings) -> None:
        self._settings = settings
        self._llm_client = GeminiClient(
            api_key=settings.gemini_api_key,
            model_name=settings.llm_model,
        )

    def analyze(
        self,
        meeting_text: str,
        expected_participant_count: int | None = None,
    ) -> MeetingAnalysisResult:
        if not meeting_text.strip():
            raise ValueError("meeting_text must not be empty.")

        prompt = self._build_prompt(
            meeting_text=meeting_text,
            expected_participant_count=expected_participant_count,
        )
        raw_result = self._llm_client.generate_structured_response(
            prompt=prompt,
            response_schema=MeetingAnalysisResult,
            temperature=0.0,
        )

        try:
            result = MeetingAnalysisResult.model_validate(raw_result)
        except ValidationError as exc:
            raise MeetingAnalyzerError(
                "LLM response is valid JSON but does not match MeetingAnalysisResult schema."
            ) from exc
        result = reconcile_participants(
            result=result,
            expected_participant_count=expected_participant_count,
        )
        # Metrik hesaplamaları
        metrics_calculator = TaskMetricsCalculator()
        for item in result.action_items:
            # İşlem metni olarak source_sentence'ı önceliklendir, yoksa task'ı kullan
            task_text = item.source_sentence if item.source_sentence else item.task
            has_date = bool(item.due_date)
            
            metrics_dict = metrics_calculator.get_all_metrics(
                task_sentence=task_text,
                has_date_entity=has_date,
                verb_count=1
            )
            item.metrics = TaskMetrics(**metrics_dict)

        return result

    def _build_prompt(
        self,
        meeting_text: str,
        expected_participant_count: int | None = None,
    ) -> str:
        system_prompt = read_text_file(SYSTEM_PROMPT_PATH)
        user_prompt_template = read_text_file(USER_PROMPT_PATH)

        reference_date, reference_weekday, timezone = (
            get_reference_date_context(
                self._settings.app_timezone
            )
        )

        participant_count_text = (
            str(expected_participant_count)
            if expected_participant_count is not None
            else "Bilinmiyor"
        )

        user_prompt = user_prompt_template.format(
            meeting_text=meeting_text,
            reference_date=reference_date,
            reference_weekday=reference_weekday,
            timezone=timezone,
            expected_participant_count=participant_count_text,
        )

        return f"{system_prompt}\n\n{user_prompt}"