"""
Pydantic schemas for the HR AI Agent System API.
=================================================
Defines request/response models for the REST and WebSocket interfaces.
"""

from typing import Any, Literal, Optional

from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Chat — REST request/response
# ---------------------------------------------------------------------------

class ChatRequest(BaseModel):
    """Payload sent by the frontend for a chat interaction."""

    message: str = Field(..., min_length=1, description="The user's message text.")
    session_id: str = Field(
        ...,
        description="Unique session identifier for multi-turn conversation memory.",
    )


class ChatResponse(BaseModel):
    """Response returned by the synchronous REST chat endpoint."""

    reply: str = Field(..., description="The agent's full reply text.")
    session_id: str
    tool_calls: list[dict[str, Any]] = Field(
        default_factory=list,
        description="List of tools that were invoked during this turn.",
    )


# ---------------------------------------------------------------------------
# WebSocket streaming frames
# ---------------------------------------------------------------------------

class StreamEvent(BaseModel):
    """
    A single frame streamed over WebSocket to the frontend.

    Types:
    - ``token``       — a chunk of the agent's text response
    - ``tool_start``  — the agent is invoking a specific tool
    - ``tool_end``    — the tool has finished executing (includes result summary)
    - ``error``       — an error occurred during processing
    - ``done``        — the agent has finished its response
    """

    type: Literal["token", "tool_start", "tool_end", "error", "done"] = Field(
        ..., description="The event type."
    )
    data: str = Field(default="", description="Event payload (text chunk, tool name, error message, etc.).")
    tool_name: Optional[str] = Field(default=None, description="Name of the tool (for tool_start/tool_end events).")
    metadata: Optional[dict[str, Any]] = Field(default=None, description="Additional event metadata.")
