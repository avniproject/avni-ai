"""Request validation utilities for common request validation patterns."""

from typing import Dict, Any, Optional, Tuple
from starlette.requests import Request
import os


async def validate_config_request(
    request: Request,
) -> Tuple[Optional[Dict[str, Any]], Optional[str], Optional[str], Optional[str]]:
    """
    Validate the config request and extract required data.

    Args:
        request: The incoming request object

    Returns:
        Tuple of (config_data, auth_token, base_url, error_message)
        - Success: (config_data, auth_token, base_url, None)
        - Error: (None, None, None, error_message)
    """
    try:
        # Parse request body
        body = await request.json()
        config_data = body.get("config")
        if not config_data:
            return None, None, None, "config object is required"

        # Validate that config has at least one operation
        if not any(op in config_data for op in ["create", "update", "delete"]):
            return (
                None,
                None,
                None,
                "config must contain at least one of: create, update, delete",
            )

        # Get auth token from header
        auth_token = request.headers.get("avni-auth-token")
        if not auth_token:
            return None, None, None, "avni-auth-token header is required"

        # Extract base URL with priority: query > header > env > default
        base_url = os.getenv("AVNI_BASE_URL").rstrip("/")

        return config_data, auth_token, base_url, None

    except Exception as e:
        return None, None, None, f"Request validation error: {str(e)}"
