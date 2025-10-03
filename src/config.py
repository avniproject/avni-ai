"""Configuration module for Avni MCP Server."""

import os

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration from environment variables
BASE_URL = os.getenv("AVNI_BASE_URL")


def get_headers() -> dict:
    """Get base headers for API requests."""
    return {
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
