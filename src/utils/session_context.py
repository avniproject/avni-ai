"""Session context management for passing session logger to tools."""

import logging
from contextvars import ContextVar
from typing import Optional, Any

# Context variable to store the session logger
_session_logger: ContextVar[Optional[logging.Logger]] = ContextVar(
    "session_logger", default=None
)


def get_session_logger() -> Optional[logging.Logger]:
    return _session_logger.get()


def set_session_logger(logger: logging.Logger) -> None:
    _session_logger.set(logger)


def log_payload(message: str, payload: Any = None) -> None:
    """Log payload to both standard logger and session logger if available."""
    import json

    # If payload is provided, show both Python repr and JSON serialization
    if payload is not None:
        try:
            json_str = json.dumps(payload, indent=2, default=str)
            full_message = (
                f"{message}\n   Python repr: {payload}\n   JSON payload: {json_str}"
            )
        except Exception:
            full_message = f"{message}\n   Python repr: {payload}"
    else:
        full_message = message

    # Always log to standard logger
    logger = logging.getLogger(__name__)
    logger.info(full_message)

    # Also log to session logger if available
    session_logger = get_session_logger()
    if session_logger:
        session_logger.info(full_message)
