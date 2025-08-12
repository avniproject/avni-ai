"""Context management for API key."""

from contextvars import ContextVar
from typing import Optional

# Context variable to store API key for current request
api_key_context: ContextVar[Optional[str]] = ContextVar("api_key", default=None)


def get_api_key() -> Optional[str]:
    """Get API key from current context."""
    return api_key_context.get()


def set_api_key(api_key: str) -> None:
    """Set API key in current context."""
    api_key_context.set(api_key)
