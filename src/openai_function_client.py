"""OpenAI client for direct function calling."""

import json
import logging
from typing import Dict, List, Any, Optional
import httpx

logger = logging.getLogger(__name__)


class OpenAIFunctionClient:
    """Client for OpenAI Chat Completions API with function calling support."""
    
    BASE_URL = "https://api.openai.com/v1"
    
    def __init__(self, api_key: str, timeout: float = 120.0):
        """Initialize the OpenAI function calling client."""
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
    
    async def create_chat_completion(
        self,
        messages: List[Dict[str, str]],
        tools: List[Dict[str, Any]],
        model: str = "gpt-4o",
        tool_choice: str = "auto"
    ) -> Dict[str, Any]:
        """Create a chat completion with function calling."""
        
        payload = {
            "model": model,
            "messages": messages,
            "tools": tools,
            "tool_choice": tool_choice
        }
        
        logger.info(f"Making OpenAI API call with {len(tools)} tools available")
        
        response = await self._client.post(
            f"{self.BASE_URL}/chat/completions",
            json=payload,
            headers=self._get_headers(),
        )
        
        response.raise_for_status()
        return response.json()
    
    async def process_function_calls(
        self,
        response: Dict[str, Any],
        tool_registry,
        auth_token: str
    ) -> List[Dict[str, Any]]:
        """Process function calls from OpenAI response and execute them."""
        
        function_results = []
        
        if "choices" not in response:
            return function_results
        
        choice = response["choices"][0]
        message = choice.get("message", {})
        tool_calls = message.get("tool_calls", [])
        
        for tool_call in tool_calls:
            if tool_call["type"] == "function":
                function_name = tool_call["function"]["name"]
                function_args = json.loads(tool_call["function"]["arguments"])
                
                # Add auth_token to function arguments
                function_args["auth_token"] = auth_token
                
                logger.info(f"Executing function: {function_name} with args: {function_args}")
                
                try:
                    result = await tool_registry.call_tool(function_name, function_args)
                    function_results.append({
                        "tool_call_id": tool_call["id"],
                        "role": "tool",
                        "name": function_name,
                        "content": str(result)
                    })
                except Exception as e:
                    logger.error(f"Error executing function {function_name}: {e}")
                    function_results.append({
                        "tool_call_id": tool_call["id"],
                        "role": "tool",
                        "name": function_name,
                        "content": f"Error: {str(e)}"
                    })
        
        return function_results


def create_openai_function_client(api_key: str, timeout: float = 120.0) -> OpenAIFunctionClient:
    """
    Factory function to create an OpenAI function calling client.
    
    Args:
        api_key: OpenAI API key
        timeout: Request timeout in seconds (default: 120.0)
    
    Returns:
        Configured OpenAI function calling client
    """
    return OpenAIFunctionClient(api_key, timeout)
