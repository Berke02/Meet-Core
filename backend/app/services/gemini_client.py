from __future__ import annotations

import json
import random
import time
from typing import Any, Type

from google import genai
from google.genai import types
from pydantic import BaseModel


class GeminiClientError(RuntimeError):
    """Raised when Gemini client fails."""


class GeminiClient:
    """Thin wrapper around Gemini API with retry support."""

    def __init__(
        self,
        api_key: str,
        model_name: str,
        max_retries: int = 3,
        initial_retry_delay_seconds: float = 2.0,
        max_retry_delay_seconds: float = 20.0,
    ) -> None:
        if not api_key:
            raise ValueError("api_key must not be empty.")

        if not model_name:
            raise ValueError("model_name must not be empty.")

        if max_retries < 0:
            raise ValueError("max_retries must be greater than or equal to 0.")

        self._model_name = model_name
        self._client = genai.Client(api_key=api_key)
        self._max_retries = max_retries
        self._initial_retry_delay_seconds = initial_retry_delay_seconds
        self._max_retry_delay_seconds = max_retry_delay_seconds

    def generate_structured_response(
        self,
        prompt: str,
        response_schema: Type[BaseModel],
        temperature: float = 0.2,
    ) -> dict[str, Any]:
        if not prompt.strip():
            raise ValueError("prompt must not be empty.")

        raw_text = self._generate_content_with_retry(
            prompt=prompt,
            response_schema=response_schema,
            temperature=temperature,
        )

        try:
            parsed_response = json.loads(raw_text)
        except json.JSONDecodeError as exc:
            raise GeminiClientError(
                "Gemini response is not valid JSON.\n"
                f"Raw response:\n{raw_text}"
            ) from exc

        if not isinstance(parsed_response, dict):
            raise GeminiClientError(
                f"Expected JSON object, got {type(parsed_response).__name__}."
            )

        return parsed_response

    def _generate_content_with_retry(
        self,
        prompt: str,
        response_schema: Type[BaseModel],
        temperature: float,
    ) -> str:
        last_exception: Exception | None = None

        for attempt in range(self._max_retries + 1):
            try:
                response = self._client.models.generate_content(
                    model=self._model_name,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        response_mime_type="application/json",
                        response_schema=response_schema,
                        temperature=temperature,
                    ),
                )

                raw_text = response.text

                if not raw_text:
                    raise GeminiClientError("Gemini returned an empty response.")

                return raw_text

            except Exception as exc:
                last_exception = exc

                if not self._is_retryable_error(exc):
                    raise

                if attempt >= self._max_retries:
                    break

                delay_seconds = self._calculate_retry_delay(attempt)

                print(
                    f"[Gemini retry] attempt={attempt + 1}/"
                    f"{self._max_retries}, "
                    f"reason={self._short_error_message(exc)}, "
                    f"sleep={delay_seconds:.1f}s"
                )

                time.sleep(delay_seconds)

        raise GeminiClientError(
            "Gemini request failed after retries.\n"
            f"Last error: {last_exception}"
        ) from last_exception

    def _calculate_retry_delay(self, attempt: int) -> float:
        exponential_delay = self._initial_retry_delay_seconds * (2**attempt)
        jitter = random.uniform(0.0, 1.0)

        return min(
            exponential_delay + jitter,
            self._max_retry_delay_seconds,
        )

    @staticmethod
    def _is_retryable_error(exc: Exception) -> bool:
        message = str(exc).upper()

        retryable_markers = (
            "503",
            "UNAVAILABLE",
            "504",
            "DEADLINE_EXCEEDED",
            "429",
            "RESOURCE_EXHAUSTED",
        )

        return any(marker in message for marker in retryable_markers)

    @staticmethod
    def _short_error_message(exc: Exception, max_length: int = 160) -> str:
        message = str(exc).replace("\n", " ").strip()

        if len(message) <= max_length:
            return message

        return f"{message[:max_length]}..."