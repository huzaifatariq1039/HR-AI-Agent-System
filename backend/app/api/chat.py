"""
Chat API — REST & WebSocket Endpoints
=======================================
Provides two interfaces for interacting with the HR AI Agent:
1. POST /api/chat      — synchronous single-response endpoint (fallback)
2. WS   /ws/chat       — streaming WebSocket for real-time token & tool events
"""

import json
import traceback
import uuid

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from langchain_core.messages import AIMessageChunk, HumanMessage, ToolMessage

from app.agent.graph import hr_agent_graph
from app.models.schemas import ChatRequest, ChatResponse, StreamEvent

router = APIRouter()


# ---------------------------------------------------------------------------
# REST endpoint — synchronous chat (fallback)
# ---------------------------------------------------------------------------

@router.post("/chat", response_model=ChatResponse, tags=["chat"])
async def chat_sync(request: ChatRequest):
    """
    Synchronous chat endpoint.

    Sends the user message through the LangGraph agent and returns the
    complete response once all tool calls and LLM reasoning are finished.
    Useful as a fallback when WebSocket is not available.
    """
    config = {"configurable": {"thread_id": request.session_id}}

    # Invoke the graph (blocks until complete)
    result = await hr_agent_graph.ainvoke(
        {"messages": [HumanMessage(content=request.message)]},
        config=config,
    )

    # Extract the final AI message
    final_message = result["messages"][-1]

    # Collect tool calls that occurred during this turn
    tool_calls_summary = []
    for msg in result["messages"]:
        if hasattr(msg, "tool_calls") and msg.tool_calls:
            for tc in msg.tool_calls:
                tool_calls_summary.append(
                    {"name": tc["name"], "args": tc["args"]}
                )

    return ChatResponse(
        reply=final_message.content,
        session_id=request.session_id,
        tool_calls=tool_calls_summary,
    )


# ---------------------------------------------------------------------------
# WebSocket endpoint — streaming chat
# ---------------------------------------------------------------------------

@router.websocket("/ws/chat")
async def chat_stream(websocket: WebSocket):
    """
    WebSocket endpoint for streaming agent responses.

    Protocol:
    ---------
    Client sends JSON:  { "message": "...", "session_id": "..." }
    Server streams JSON frames:
        { "type": "token",      "data": "chunk of text" }
        { "type": "tool_start", "data": "tool description", "tool_name": "..." }
        { "type": "tool_end",   "data": "result summary",   "tool_name": "..." }
        { "type": "error",      "data": "error message" }
        { "type": "done",       "data": "" }
    """
    await websocket.accept()

    try:
        while True:
            # Wait for a message from the client
            raw = await websocket.receive_text()
            data = json.loads(raw)

            message = data.get("message", "")
            session_id = data.get("session_id", str(uuid.uuid4()))

            if not message.strip():
                await _send_event(websocket, "error", "Empty message received.")
                await _send_event(websocket, "done")
                continue

            config = {"configurable": {"thread_id": session_id}}

            try:
                # Stream events from the LangGraph agent
                async for event in hr_agent_graph.astream_events(
                    {"messages": [HumanMessage(content=message)]},
                    config=config,
                    version="v2",
                ):
                    kind = event["event"]

                    # ── LLM is streaming tokens ──────────────────────────
                    if kind == "on_chat_model_stream":
                        chunk = event["data"]["chunk"]
                        if isinstance(chunk, AIMessageChunk) and chunk.content:
                            # Only stream content tokens (not tool-call JSON)
                            if isinstance(chunk.content, str) and chunk.content:
                                await _send_event(websocket, "token", chunk.content)

                    # ── Tool execution starting ──────────────────────────
                    elif kind == "on_tool_start":
                        tool_name = event.get("name", "unknown_tool")
                        tool_input = event["data"].get("input", {})
                        await _send_event(
                            websocket,
                            "tool_start",
                            f"Invoking {tool_name}...",
                            tool_name=tool_name,
                            metadata={"input": _safe_serialize(tool_input)},
                        )

                    # ── Tool execution finished ──────────────────────────
                    elif kind == "on_tool_end":
                        tool_name = event.get("name", "unknown_tool")
                        output = event["data"].get("output", "")
                        # The output might be a ToolMessage or raw string
                        if hasattr(output, "content"):
                            output_text = str(output.content)
                        else:
                            output_text = str(output)

                        # Truncate very long outputs for the status event
                        preview = output_text[:200] + "..." if len(output_text) > 200 else output_text

                        await _send_event(
                            websocket,
                            "tool_end",
                            preview,
                            tool_name=tool_name,
                        )

                # Signal completion
                await _send_event(websocket, "done")

            except Exception as e:
                traceback.print_exc()
                await _send_event(websocket, "error", f"Agent error: {str(e)}")
                await _send_event(websocket, "done")

    except WebSocketDisconnect:
        print(f"WebSocket client disconnected")
    except Exception as e:
        traceback.print_exc()
        try:
            await _send_event(websocket, "error", f"Connection error: {str(e)}")
        except Exception:
            pass


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

async def _send_event(
    websocket: WebSocket,
    event_type: str,
    data: str = "",
    tool_name: str | None = None,
    metadata: dict | None = None,
):
    """Send a StreamEvent JSON frame over the WebSocket."""
    event = StreamEvent(
        type=event_type,
        data=data,
        tool_name=tool_name,
        metadata=metadata,
    )
    await websocket.send_text(event.model_dump_json())


def _safe_serialize(obj) -> dict:
    """Safely convert tool input to a JSON-serializable dict."""
    if isinstance(obj, dict):
        return {k: str(v) for k, v in obj.items()}
    return {"value": str(obj)}
