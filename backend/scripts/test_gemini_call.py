from __future__ import annotations

import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from app.core.config import get_settings  # noqa: E402
from app.services.meeting_analyzer import MeetingAnalyzer, read_text_file  # noqa: E402


SAMPLE_MEETING_PATH = PROJECT_ROOT / "data" / "samples" / "sample_meeting_01.txt"


def main() -> None:
    try:
        settings = get_settings()
        meeting_text = read_text_file(SAMPLE_MEETING_PATH)

        analyzer = MeetingAnalyzer(settings=settings)
        result = analyzer.analyze(meeting_text)

    except Exception as exc:
        print("\nERROR")
        print("-" * 80)
        print(str(exc))
        raise SystemExit(1) from exc

    print("\nMEETING ANALYSIS RESULT")
    print("-" * 80)
    print(result.model_dump_json(indent=2))


if __name__ == "__main__":
    main()