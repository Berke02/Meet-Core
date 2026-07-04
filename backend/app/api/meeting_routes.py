from __future__ import annotations

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.core.config import get_settings
from app.schemas.meeting_schema import MeetingAnalysisResult
from app.services.meeting_analyzer import MeetingAnalyzer, MeetingAnalyzerError


router = APIRouter(prefix="/api/meetings", tags=["meetings"])


class MeetingAnalysisRequest(BaseModel):
    meeting_text: str = Field(
        ...,
        min_length=10,
        description="Meeting transcript or meeting notes to analyze.",
    )


@router.post("/analyze", response_model=MeetingAnalysisResult)
def analyze_meeting(request: MeetingAnalysisRequest) -> MeetingAnalysisResult:
    try:
        settings = get_settings()
        analyzer = MeetingAnalyzer(settings=settings)

        return analyzer.analyze(request.meeting_text)

    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    except MeetingAnalyzerError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="Unexpected error occurred while analyzing the meeting.",
        ) from exc