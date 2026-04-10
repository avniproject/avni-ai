"""
Agent activity log handlers.
Endpoints: POST /agent-log, GET /agent-logs/{conversation_id}

Stores a bounded, time-stamped trace of every step the Dify agent takes
so failures can be diagnosed with full context.
"""

from __future__ import annotations

import logging
import os
import time
from datetime import datetime, timezone
from typing import Any

from starlette.requests import Request
from starlette.responses import JSONResponse

logger = logging.getLogger(__name__)

_LOG_STORE_TTL = int(os.getenv("AGENT_LOG_TTL_HOURS", "24")) * 3600  # default 24 h
_MAX_ENTRIES_PER_CONVERSATION = int(os.getenv("AGENT_LOG_MAX_ENTRIES", "500"))


class _AgentLogStore:
    def __init__(self) -> None:
        # conversation_id -> {"entries": [...], "expiry": float}
        self._store: dict[str, dict[str, Any]] = {}

    def append(self, conversation_id: str, entry: dict[str, Any]) -> int:
        """Append a log entry. Returns the new total entry count."""
        now = time.time()
        if conversation_id not in self._store:
            self._store[conversation_id] = {
                "entries": [],
                "expiry": now + _LOG_STORE_TTL,
            }
        bucket = self._store[conversation_id]
        bucket["expiry"] = now + _LOG_STORE_TTL  # refresh TTL on each write
        entries = bucket["entries"]
        if len(entries) >= _MAX_ENTRIES_PER_CONVERSATION:
            entries.pop(0)  # drop oldest to stay within bound
        entries.append(entry)
        return len(entries)

    def get(self, conversation_id: str) -> list[dict[str, Any]]:
        now = time.time()
        bucket = self._store.get(conversation_id)
        if not bucket or now > bucket["expiry"]:
            return []
        return bucket["entries"]

    def cleanup_expired(self) -> int:
        now = time.time()
        expired = [k for k, v in self._store.items() if now > v["expiry"]]
        for k in expired:
            del self._store[k]
        return len(expired)


_log_store = _AgentLogStore()


def get_log_store() -> _AgentLogStore:
    return _log_store


async def handle_append_agent_log(request: Request) -> JSONResponse:
    """
    POST /agent-log
    Body: {
      "conversation_id": "...",
      "step": 1,
      "phase": "entity_extraction|spec_generation|bundle_generation|bundle_fix|upload|done",
      "action": "Called generate_bundle",
      "tool": "generate_bundle",        // optional
      "status": "success|error|info",
      "summary": "stored=true, concepts=45, forms=8",   // optional
      "error": "...",                   // optional, when status=error
      "tokens_used": 1234,              // optional, cumulative tokens from Dify
      "model": "claude-sonnet-4-6"      // optional
    }
    """
    try:
        body = await request.json()
    except Exception:
        return JSONResponse({"error": "Invalid JSON body"}, status_code=400)

    conversation_id = body.get("conversation_id")
    if not conversation_id:
        return JSONResponse({"error": "Missing 'conversation_id'"}, status_code=400)

    action = body.get("action", "")
    if not action:
        return JSONResponse({"error": "Missing 'action'"}, status_code=400)

    entry: dict[str, Any] = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "step": body.get("step"),
        "phase": body.get("phase", ""),
        "action": action,
        "tool": body.get("tool", ""),
        "status": body.get("status", "info"),
        "summary": body.get("summary", ""),
        "error": body.get("error", ""),
        "tokens_used": body.get("tokens_used"),
        "model": body.get("model", ""),
    }

    count = _log_store.append(conversation_id, entry)
    logger.info(
        "agent-log [%s] step=%s phase=%s status=%s action=%s",
        conversation_id[:8],
        entry["step"],
        entry["phase"],
        entry["status"],
        action[:120],
    )
    return JSONResponse({"ok": True, "entry_count": count})


async def handle_get_agent_logs(request: Request) -> JSONResponse:
    """
    GET /agent-logs/{conversation_id}
    Returns all log entries for the conversation (for human debugging).
    """
    conversation_id = request.path_params.get("conversation_id", "")
    if not conversation_id:
        return JSONResponse({"error": "Missing conversation_id"}, status_code=400)

    entries = _log_store.get(conversation_id)
    if not entries:
        return JSONResponse(
            {"conversation_id": conversation_id, "found": False, "entries": []},
            status_code=404,
        )

    return JSONResponse(
        {
            "conversation_id": conversation_id,
            "found": True,
            "entry_count": len(entries),
            "entries": entries,
        }
    )
