"""Request processing utilities for Avni MCP Server."""

import os
from starlette.requests import Request


def extract_base_url(request: Request) -> str:
    """Extract Avni base URL from query param, header, or environment.

    Priority: Query param > Header > Environment variable > Default

    Args:
        request: The incoming request object

    Returns:
        The base URL string with trailing slash removed
    """
    # Priority: Query param > Header > Environment variable > Default
    query_params = dict(request.query_params)
    if "base_url" in query_params:
        return query_params["base_url"].rstrip("/")

    header_base_url = request.headers.get("avni-base-url")
    if header_base_url:
        return header_base_url.rstrip("/")

    avni_base_url = os.getenv("AVNI_BASE_URL")
    if avni_base_url:
        return avni_base_url.rstrip("/")

    # Default fallback
    return "https://staging.avniproject.org"
