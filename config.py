"""Configuration module for Avni MCP Server."""

import os

from dotenv import load_dotenv
from context import get_auth_token

# Load environment variables
load_dotenv()

# Configuration from environment variables
BASE_URL = os.getenv("AVNI_BASE_URL")


def get_headers() -> dict:
    """Get headers for API requests using auth token from context."""
    auth_token = get_auth_token()
    if not auth_token:
        raise ValueError("No auth token found in context")

    return {
        "AUTH-TOKEN": auth_token,
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
