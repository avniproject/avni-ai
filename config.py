"""Configuration module for Avni MCP Server."""

import os

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration from environment variables
BASE_URL = os.getenv("AVNI_BASE_URL", "https://staging.avniproject.org")


def get_headers(api_key: str) -> dict:
    """Get headers for API requests with provided API key."""
    return {
        "auth-token": api_key,
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
