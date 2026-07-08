from __future__ import annotations

from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from pydantic import ValidationError

from app.core.config import PROJECT_ROOT, AppSettings
from app.schemas.meeting_schema import MeetingAnalysisResult, TaskMetrics
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


class MeetingAnalyzer:
    """Analyzes meeting transcripts using an LLM."""

    def __init__(self, settings: AppSettings) -> None:
        self._settings = settings
        self._llm_client = GeminiClient(
            api_key=settings.gemini_api_key,
            model_name=settings.llm_model,
        )

    def analyze(self, meeting_text: str) -> MeetingAnalysisResult:
        if not meeting_text.strip():
            raise ValueError("meeting_text must not be empty.")

        prompt = self._build_prompt(meeting_text)

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

    def _build_prompt(self, meeting_text: str) -> str:
        system_prompt = read_text_file(SYSTEM_PROMPT_PATH)
        user_prompt_template = read_text_file(USER_PROMPT_PATH)

        reference_date, reference_weekday, timezone = get_reference_date_context(
            self._settings.app_timezone
        )

        user_prompt = user_prompt_template.format(
            meeting_text=meeting_text,
            reference_date=reference_date,
            reference_weekday=reference_weekday,
            timezone=timezone,
        )

        return f"{system_prompt}\n\n{user_prompt}"
    