"""API result handling utilities for Avni MCP Server."""

from typing import Any, Optional
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