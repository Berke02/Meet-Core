from __future__ import annotations

from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


PROJECT_ROOT = Path(__file__).resolve().parents[2]
ENV_PATH = PROJECT_ROOT / ".env"


class AppSettings(BaseSettings):
    """Application settings loaded from environment variables."""

    gemini_api_key: str = Field(..., alias="GEMINI_API_KEY")
    llm_provider: str = Field(default="gemini", alias="LLM_PROVIDER")
    llm_model: str = Field(default="gemini-2.5-flash", alias="LLM_MODEL")
    app_timezone: str = Field(default="Europe/Istanbul", alias="APP_TIMEZONE")

    model_config = SettingsConfigDict(
        env_file=ENV_PATH,
        env_file_encoding="utf-8",
        extra="ignore",
    )


def get_settings() -> AppSettings:
    return AppSettings()