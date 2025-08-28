"""Custom OpenAI Responses API Client"""

import httpx
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum


class MCPRequireApproval(str, Enum):
    """MCP tool approval requirements."""

    ALWAYS = "always"
    NEVER = "never"
    ONCE = "once"


@dataclass
class MCPTool:
    """MCP tool configuration for OpenAI Responses API."""

    server_label: str
    server_url: str
    require_approval: MCPRequireApproval = MCPRequireApproval.NEVER
    headers: Optional[Dict[str, str]] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary format expected by OpenAI API."""
        tool_dict = {
            "type": "mcp",
            "server_label": self.server_label,
            "server_url": self.server_url,
            "require_approval": self.require_approval.value,
        }

        if self.headers:
            tool_dict["headers"] = self.headers

        return tool_dict


@dataclass
class ResponsesRequest:
    """Request payload for OpenAI Responses API."""

    input: str
    model: str
    tools: List[MCPTool]
    instructions: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary format expected by OpenAI API."""
        request_dict = {
            "input": self.input,
            "model": self.model,
            "tools": [tool.to_dict() for tool in self.tools],
        }

        if self.instructions:
            request_dict["instructions"] = self.instructions

        return request_dict


class OpenAIResponsesClient:
    """Client for OpenAI Responses API with MCP support."""

    BASE_URL = "https://api.openai.com/v1"

    def __init__(self, api_key: str, timeout: float = 120.0):
        """Initialize the OpenAI Responses API client."""
        self.api_key = api_key
        self._client = httpx.AsyncClient(timeout=timeout)

    async def __aenter__(self):
        """Async context manager entry."""
        await self._client.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self._client.__aexit__(exc_type, exc_val, exc_tb)

    async def close(self):
        """Close the HTTP client."""
        await self._client.aclose()

    def _get_headers(self) -> Dict[str, str]:
        """Get default headers for API requests."""
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    async def create_response(self, request: ResponsesRequest) -> Dict[str, Any]:
        """Create a response using OpenAI's Responses API."""

        response = await self._client.post(
            f"{self.BASE_URL}/responses",
            json=request.to_dict(),
            headers=self._get_headers(),
        )

        response.raise_for_status()
        return response.json()

    async def create_mcp_response(
        self,
        input_text: str,
        server_label: str,
        server_url: str,
        auth_token: str,
        model: str = "gpt-4o",
        instructions: Optional[str] = None,
    ) -> Dict[str, Any]:
        mcp_tool = MCPTool(
            server_label=server_label,
            server_url=server_url,
            headers={"Authorization": f"Bearer {auth_token}"},
        )

        request = ResponsesRequest(
            input=input_text,
            model=model,
            tools=[mcp_tool],
            instructions=instructions,
        )

        return await self.create_response(request)


# Factory function for easier usage
def create_openai_client(api_key: str, timeout: float = 120.0) -> OpenAIResponsesClient:
    """
    Factory function to create an OpenAI Responses client.

    Args:
        api_key: OpenAI API key
        timeout: Request timeout in seconds (default: 120.0)

    Returns:
        Configured OpenAI client
    """
    return OpenAIResponsesClient(api_key, timeout)
