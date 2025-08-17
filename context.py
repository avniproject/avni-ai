"""Context management for auth token."""

from contextvars import ContextVar
from typing import Optional

# Context variable to store auth token for current request
auth_token_context: ContextVar[Optional[str]] = ContextVar("auth_token", default=None)


def get_auth_token() -> Optional[str]:
    """Get auth token from current context."""
    return auth_token_context.get()


def set_auth_token(auth_token: str) -> None:
    """Set auth token in current context."""
    auth_token_context.set(auth_token)
