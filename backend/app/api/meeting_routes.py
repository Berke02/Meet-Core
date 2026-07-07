from __future__ import annotations

from pydantic import BaseModel, Field
import tempfile
from pathlib import Path

from fastapi import APIRouter, File, HTTPException, UploadFile
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

class AudioMeetingAnalysisResponse(BaseModel):
    transcript_text: str = Field(
        ...,
        description="Transcript generated from the uploaded audio file.",
    )
    analysis: MeetingAnalysisResult = Field(
        ...,
        description="Structured meeting analysis generated from transcript.",
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
    
@router.post("/analyze-audio", response_model=AudioMeetingAnalysisResponse)
async def analyze_audio_meeting(
    file: UploadFile = File(...),
) -> AudioMeetingAnalysisResponse:
    allowed_extensions = {".wav", ".mp3", ".m4a", ".mp4", ".webm"}

    original_filename = file.filename or "uploaded_audio"
    suffix = Path(original_filename).suffix.lower()

    if suffix not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported audio file extension: {suffix}",
        )

    try:
        settings = get_settings()

        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
            temp_path = Path(temp_file.name)
            temp_file.write(await file.read())

        from app.services.transcription_service import WhisperXTranscriptionService

        transcription_service = WhisperXTranscriptionService(settings=settings)
        transcript_text = transcription_service.transcribe(temp_path)

        analyzer = MeetingAnalyzer(settings=settings)
        analysis = analyzer.analyze(transcript_text)

        return AudioMeetingAnalysisResponse(
            transcript_text=transcript_text,
            analysis=analysis,
        )

    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Audio meeting analysis failed: {exc}",
        ) from exc

    finally:
        if "temp_path" in locals() and temp_path.exists():
            temp_path.unlink(missing_ok=True)
            