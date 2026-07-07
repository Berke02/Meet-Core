from __future__ import annotations

import gc
from pathlib import Path
from typing import Any

from app.core.config import AppSettings


class TranscriptionServiceError(RuntimeError):
    """Raised when audio transcription fails."""


class WhisperXTranscriptionService:
    """Speech-to-text service based on WhisperX.

    This service converts an audio file into transcript text.
    The transcript is then consumed by MeetingAnalyzer as normal meeting text.
    """

    def __init__(self, settings: AppSettings) -> None:
        self._settings = settings

    def transcribe(self, audio_path: Path) -> str:
        if not audio_path.exists():
            raise FileNotFoundError(f"Audio file not found: {audio_path}")

        if audio_path.stat().st_size == 0:
            raise ValueError(f"Audio file is empty: {audio_path}")

        try:
            return self._transcribe_with_whisperx(audio_path)
        except ImportError as exc:
            raise TranscriptionServiceError(
                "WhisperX dependencies are not installed. "
                "Install them with: pip install -r requirements-audio.txt"
            ) from exc
        except Exception as exc:
            raise TranscriptionServiceError(
                f"Audio transcription failed: {exc}"
            ) from exc

    def _transcribe_with_whisperx(self, audio_path: Path) -> str:
        import torch
        import whisperx

        device = self._settings.audio_device
        compute_type = "float16" if device == "cuda" else "int8"

        model = whisperx.load_model(
            self._settings.whisperx_model,
            device=device,
            compute_type=compute_type,
            language="tr",
        )

        audio = whisperx.load_audio(str(audio_path))
        result = model.transcribe(
            audio,
            batch_size=16,
            language="tr",
        )

        model = None
        self._cleanup_torch(torch)

        aligned_result = self._align_words(
            whisperx=whisperx,
            torch=torch,
            result=result,
            audio=audio,
            device=device,
        )

        if self._settings.hf_token:
            try:
                aligned_result = self._diarize_speakers(
                    whisperx=whisperx,
                    torch=torch,
                    result=aligned_result,
                    audio_path=audio_path,
                    device=device,
                )
            except Exception as exc:
                # Diarization is useful but should not break the MVP audio flow.
                # If it fails, we continue with SPEAKER_00 fallback.
                print(f"[WARN] Speaker diarization failed. Falling back to SPEAKER_00. Error: {exc}")

        return self._format_transcript(aligned_result)

    def _align_words(
        self,
        whisperx: Any,
        torch: Any,
        result: dict[str, Any],
        audio: Any,
        device: str,
    ) -> dict[str, Any]:
        model_a, metadata = whisperx.load_align_model(
            language_code=result["language"],
            device=device,
        )

        aligned_result = whisperx.align(
            result["segments"],
            model_a,
            metadata,
            audio,
            device,
            return_char_alignments=False,
        )

        model_a = None
        self._cleanup_torch(torch)

        return aligned_result

    def _diarize_speakers(
        self,
        whisperx: Any,
        torch: Any,
        result: dict[str, Any],
        audio_path: Path,
        device: str,
    ) -> dict[str, Any]:
        import pandas as pd
        from pyannote.audio import Pipeline

        if not self._settings.hf_token:
            raise TranscriptionServiceError(
                "HF_TOKEN is required for speaker diarization."
            )

        try:
            pipeline = Pipeline.from_pretrained(
                "pyannote/speaker-diarization-3.1",
                token=self._settings.hf_token,
            )
        except TypeError:
            pipeline = Pipeline.from_pretrained(
                "pyannote/speaker-diarization-3.1",
                use_auth_token=self._settings.hf_token,
            )

        pipeline.to(torch.device(device))

        diarization = pipeline(str(audio_path))

        diarize_segments: list[dict[str, Any]] = []

        for segment, _, speaker in diarization.itertracks(yield_label=True):
            diarize_segments.append(
                {
                    "start": segment.start,
                    "end": segment.end,
                    "speaker": speaker,
                }
            )

        if not diarize_segments:
            raise TranscriptionServiceError(
                "Speaker diarization did not return any speaker segments."
            )

        diarize_df = pd.DataFrame(diarize_segments)

        diarized_result = whisperx.assign_word_speakers(
            diarize_df,
            result,
        )

        self._cleanup_torch(torch)

        return diarized_result

    @staticmethod
    def _format_transcript(result: dict[str, Any]) -> str:
        transcript_lines: list[str] = []

        for segment in result.get("segments", []):
            text = str(segment.get("text", "")).strip()

            if not text:
                continue

            start = float(segment.get("start", 0.0))
            minute = int(start // 60)
            second = int(start % 60)
            timestamp = f"{minute:02}:{second:02}"

            speaker = str(segment.get("speaker") or "SPEAKER_00").strip()

            transcript_lines.append(f"[{timestamp}] {speaker}: {text}")

        transcript = "\n".join(transcript_lines).strip()

        if not transcript:
            raise TranscriptionServiceError("Transcript is empty.")

        return transcript

    @staticmethod
    def _cleanup_torch(torch: Any) -> None:
        gc.collect()

        if torch.cuda.is_available():
            torch.cuda.empty_cache()