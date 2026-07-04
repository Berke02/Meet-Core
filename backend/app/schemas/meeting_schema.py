from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


PriorityLevel = Literal["low", "medium", "high"]
RiskLevel = Literal["low", "medium", "high"]


class Participant(BaseModel):
    """Meeting participant extracted from the transcript."""

    name: str = Field(
        ...,
        description="Participant name as mentioned in the meeting text.",
    )
    role: str | None = Field(
        default=None,
        description="Participant role if explicitly mentioned. Otherwise null.",
    )


class Decision(BaseModel):
    """Decision extracted from the meeting."""

    decision: str = Field(
        ...,
        description="Clear decision made during the meeting.",
    )
    owner: str | None = Field(
        default=None,
        description="Owner of the decision if explicitly mentioned. Otherwise null.",
    )
    confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Confidence score between 0 and 1.",
    )
    source_sentence: str | None = Field(
        default=None,
        description="Original sentence or excerpt supporting this decision.",
    )


class ActionItem(BaseModel):
    """Action item extracted from the meeting."""

    task: str = Field(
        ...,
        description="Concrete task assigned or implied in the meeting.",
    )
    owner: str | None = Field(
        default=None,
        description="Responsible person if explicitly mentioned. Otherwise null.",
    )
    due_date: str | None = Field(
        default=None,
        description="Due date in YYYY-MM-DD format if available. Otherwise null.",
    )
    priority: PriorityLevel = Field(
        default="medium",
        description="Estimated priority of the task.",
    )
    risk_level: RiskLevel = Field(
        default="medium",
        description="Estimated risk level of the task.",
    )
    confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Confidence score between 0 and 1.",
    )
    source_sentence: str | None = Field(
        default=None,
        description="Original sentence or excerpt supporting this action item.",
    )


class OpenQuestion(BaseModel):
    """Unresolved question or ambiguity from the meeting."""

    question: str = Field(
        ...,
        description="Question or unresolved topic.",
    )
    owner: str | None = Field(
        default=None,
        description="Person expected to clarify the question if mentioned.",
    )


class MeetingAnalysisResult(BaseModel):
    """Structured LLM output for meeting analysis."""

    summary: str = Field(
        ...,
        description="Concise meeting summary in Turkish.",
    )
    key_topics: list[str] = Field(
        default_factory=list,
        description="Main topics discussed in the meeting.",
    )
    participants: list[Participant] = Field(
        default_factory=list,
        description="Participants detected from the meeting text.",
    )
    decisions: list[Decision] = Field(
        default_factory=list,
        description="Decisions extracted from the meeting.",
    )
    action_items: list[ActionItem] = Field(
        default_factory=list,
        description="Tasks and follow-up actions extracted from the meeting.",
    )
    open_questions: list[OpenQuestion] = Field(
        default_factory=list,
        description="Open questions or unresolved topics.",
    )