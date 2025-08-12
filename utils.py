"""Utility functions for common operations."""

from typing import Any, Dict, List, Optional
from dataclasses import dataclass


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
