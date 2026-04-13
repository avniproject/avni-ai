"""
Ambiguity resolution handlers.

Manages a store of ambiguities raised during entity extraction or
config generation, and provides endpoints to submit user resolutions.

Endpoints:
  POST /resolve-ambiguities   — submit answers for pending ambiguities
  GET  /get-ambiguities       — retrieve pending ambiguities for a conversation
"""

from __future__ import annotations

import logging
import os
import time
from typing import Any

from starlette.requests import Request
from starlette.responses import JSONResponse

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# In-memory ambiguity store keyed by conversation_id (TTL = 6 hours)
# ---------------------------------------------------------------------------
_AMBIGUITY_STORE_TTL = int(os.getenv("ENTITY_STORE_TTL_HOURS", "6")) * 3600


class _AmbiguityStore:
    def __init__(self) -> None:
        self._store: dict[str, tuple[list[dict], float]] = {}  # id -> (items, expiry)

    def put(self, conversation_id: str, ambiguities: list[dict]) -> None:
        self._store[conversation_id] = (
            ambiguities,
            time.time() + _AMBIGUITY_STORE_TTL,
        )

    def get(self, conversation_id: str) -> list[dict] | None:
        entry = self._store.get(conversation_id)
        if entry is None:
            return None
        items, expiry = entry
        if time.time() > expiry:
            del self._store[conversation_id]
            return None
        return items

    def cleanup(self) -> int:
        now = time.time()
        expired = [k for k, (_, exp) in self._store.items() if now > exp]
        for k in expired:
            del self._store[k]
        return len(expired)


_ambiguity_store = _AmbiguityStore()


def get_ambiguity_store() -> _AmbiguityStore:
    """Return the global ambiguity store."""
    return _ambiguity_store


# ---------------------------------------------------------------------------
# Handlers
# ---------------------------------------------------------------------------


async def handle_resolve_ambiguities(request: Request) -> JSONResponse:
    """
    POST /resolve-ambiguities
    Body: { "conversation_id": "...", "resolutions": [{"id": "...", "answer": "..."}] }
    Applies user-provided answers to the stored ambiguity list and returns
    the updated list with resolved flags.
    """
    try:
        body = await request.json()
    except Exception:
        return JSONResponse({"error": "Invalid JSON body"}, status_code=400)

    conversation_id = body.get("conversation_id")
    resolutions = body.get("resolutions", [])

    if not conversation_id:
        return JSONResponse({"error": "Missing 'conversation_id'"}, status_code=400)
    if not isinstance(resolutions, list):
        return JSONResponse(
            {"error": "'resolutions' must be an array"}, status_code=400
        )

    ambiguities = _ambiguity_store.get(conversation_id)
    if ambiguities is None:
        return JSONResponse(
            {
                "error": f"No ambiguities found for conversation_id={conversation_id}. "
                "They may have expired (TTL 6h) or were never stored."
            },
            status_code=404,
        )

    # Build a lookup of resolutions by id
    resolution_map: dict[str, Any] = {}
    for res in resolutions:
        if isinstance(res, dict) and res.get("id"):
            resolution_map[res["id"]] = res.get("answer")

    resolved_count = 0
    for amb in ambiguities:
        amb_id = amb.get("id", "")
        if amb_id in resolution_map:
            amb["resolved"] = True
            amb["answer"] = resolution_map[amb_id]
            resolved_count += 1

    # Write back
    _ambiguity_store.put(conversation_id, ambiguities)

    pending = [a for a in ambiguities if not a.get("resolved")]
    logger.info(
        "resolve-ambiguities: resolved %d, %d still pending for conversation_id=%s",
        resolved_count,
        len(pending),
        conversation_id,
    )
    return JSONResponse(
        {
            "ok": True,
            "resolved_count": resolved_count,
            "pending_count": len(pending),
            "all_resolved": len(pending) == 0,
        }
    )


async def handle_get_ambiguities(request: Request) -> JSONResponse:
    """
    GET /get-ambiguities?conversation_id=...
    Returns the stored ambiguity list for the given conversation.
    """
    conversation_id = request.query_params.get("conversation_id")
    if not conversation_id:
        return JSONResponse(
            {"error": "Missing 'conversation_id' query param"}, status_code=400
        )

    ambiguities = _ambiguity_store.get(conversation_id)
    if ambiguities is None:
        return JSONResponse(
            {
                "error": f"No ambiguities found for conversation_id={conversation_id}. "
                "They may have expired (TTL 6h) or were never stored."
            },
            status_code=404,
        )

    pending = [a for a in ambiguities if not a.get("resolved")]
    resolved = [a for a in ambiguities if a.get("resolved")]

    logger.info(
        "get-ambiguities: conversation_id=%s total=%d pending=%d resolved=%d",
        conversation_id,
        len(ambiguities),
        len(pending),
        len(resolved),
    )
    return JSONResponse(
        {
            "ambiguities": ambiguities,
            "total": len(ambiguities),
            "pending_count": len(pending),
            "resolved_count": len(resolved),
            "all_resolved": len(pending) == 0,
        }
    )
