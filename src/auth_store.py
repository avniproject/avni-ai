"""
Conversation-scoped auth token store.

Allows a Dify workflow to store an auth token once at the start,
then all subsequent tool calls just pass conversation_id and
the server resolves the token automatically.
"""

import logging
import time

from starlette.requests import Request
from starlette.responses import JSONResponse

logger = logging.getLogger(__name__)

_AUTH_STORE_TTL = 6 * 3600  # 6 hours, same as entity store


class _AuthTokenStore:
    def __init__(self) -> None:
        self._store: dict[
            str, tuple[str, float]
        ] = {}  # conversation_id -> (token, expiry)

    def put(self, conversation_id: str, token: str) -> None:
        self._store[conversation_id] = (token, time.time() + _AUTH_STORE_TTL)

    def get(self, conversation_id: str) -> str | None:
        entry = self._store.get(conversation_id)
        if entry is None:
            return None
        token, expiry = entry
        if time.time() > expiry:
            del self._store[conversation_id]
            return None
        return token

    def cleanup(self) -> int:
        now = time.time()
        expired = [k for k, (_, exp) in self._store.items() if now > exp]
        for k in expired:
            del self._store[k]
        return len(expired)


_auth_store = _AuthTokenStore()


def resolve_auth_token(request: Request, body: dict | None = None) -> str | None:
    """Resolve auth token from header or conversation_id lookup.

    Priority:
      1. ``avni-auth-token`` header (explicit, always wins)
      2. ``conversation_id`` in *body* dict → look up stored token
      3. ``conversation_id`` query parameter → look up stored token
    """
    token = request.headers.get("avni-auth-token")
    if token:
        return token

    conversation_id = None
    if body and isinstance(body, dict):
        conversation_id = body.get("conversation_id")
    if not conversation_id:
        conversation_id = request.query_params.get("conversation_id")
    if conversation_id:
        token = _auth_store.get(conversation_id)
        if token:
            logger.debug(
                "Resolved auth token from store for conversation %s", conversation_id
            )
    return token


async def handle_store_auth_token(request: Request) -> JSONResponse:
    """POST /store-auth-token — cache an auth token by conversation_id."""
    try:
        body = await request.json()
    except Exception:
        return JSONResponse({"error": "Invalid JSON body"}, status_code=400)

    conversation_id = body.get("conversation_id")
    auth_token = body.get("auth_token")

    if not conversation_id:
        return JSONResponse({"error": "Missing 'conversation_id'"}, status_code=400)
    if not auth_token:
        return JSONResponse({"error": "Missing 'auth_token'"}, status_code=400)

    _auth_store.put(conversation_id, auth_token)
    logger.info("Stored auth token for conversation %s", conversation_id)
    return JSONResponse({"ok": True, "conversation_id": conversation_id})
