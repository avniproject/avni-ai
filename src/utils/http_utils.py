"""HTTP response utilities for Avni MCP Server."""

import os
from starlette.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware import Middleware


def create_error_response(message: str, status_code: int = 400) -> JSONResponse:
    """Create a standardized error response.

    Args:
        message: The error message to return
        status_code: HTTP status code (default: 400)

    Returns:
        JSONResponse with error format
    """
    return JSONResponse({"error": message}, status_code=status_code)


def create_success_response(data: dict) -> JSONResponse:
    """Create a standardized success response.

    Args:
        data: The response data

    Returns:
        JSONResponse with the data
    """
    return JSONResponse(data)


def create_cors_middleware() -> Middleware:
    """Create CORS middleware configuration for the server."""
    allowed_origins = []
    avni_base_url = os.getenv("AVNI_BASE_URL")

    if avni_base_url:
        allowed_origins.append(avni_base_url)
    # Allow localhost for development
    allowed_origins.extend(["http://localhost:6010"])

    return Middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "OPTIONS"],
        allow_headers=["*"],
    )