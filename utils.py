"""Utility functions for common operations."""

import os
from typing import Any, Dict, List, Optional
from dataclasses import dataclass
from starlette.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware import Middleware


# For Tool responses
@dataclass
class ApiResult:
    """Result wrapper for API responses."""

    success: bool
    data: Any = None
    error: Optional[str] = None

    @classmethod
    def success_result(cls, data: Any) -> "ApiResult":
        """Create a successful result."""
        return cls(success=True, data=data)

    @classmethod
    def error_result(cls, error: str) -> "ApiResult":
        """Create an error result."""
        return cls(success=False, error=error)

    def format_error(self, operation: str) -> str:
        """Format error message for tool response."""
        return f"Failed to {operation}: {self.error}"

    @classmethod
    def format_empty(cls, resource: str) -> str:
        """Format empty result message."""
        return f"No {resource} found."


def format_list_response(
    items: List[Dict[str, Any]],
    id_key: str = "id",
    name_key: str = "name",
    extra_key: Optional[str] = None,
) -> str:
    """Format a list of items into a readable string response.

    Args:
        items: List of dictionary items
        id_key: Key for ID field
        name_key: Key for name field
        extra_key: Optional extra field to include
    """
    if not items:
        return ""

    result = []
    for item in items:
        line = f"ID: {item.get(id_key)}, Name: {item.get(name_key)}"
        if extra_key and extra_key in item:
            value = item.get(extra_key)
            if isinstance(value, float):
                line += f", {extra_key.title()}: {value:.1f}"
            else:
                line += f", {extra_key.title()}: {value}"
        result.append(line)

    return "\n".join(result)


def format_creation_response(
    resource: str, name: str, id_field: str, response_data: Dict[str, Any]
) -> str:
    """Format creation success response.

    Args:
        resource: Type of resource created (e.g., "Organization", "User")
        name: Name of the created resource
        id_field: Field name for the ID (e.g., "id", "uuid")
        response_data: API response data
    """
    id_value = response_data.get(id_field)
    return (
        f"{resource} '{name}' created successfully with {id_field.upper()} {id_value}"
    )


# HTTP Response utilities
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


# CORS middleware utilities
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
