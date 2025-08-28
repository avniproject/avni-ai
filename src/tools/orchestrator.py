"""Orchestrator tools for request classification and routing."""

from enum import Enum
from typing import Dict, Callable, Optional, Any, List
from fastmcp import FastMCP
import logging

logger = logging.getLogger(__name__)

class RequestType(str, Enum):
    """Enum representing different types of requests."""
    RAG = "rag"          # For document-based queries
    TEMPLATE = "template" # For structured, predefined workflows
    ASSISTANT = "assistant" # For general conversational queries

class RequestOrchestrator:
    """Handles request classification and routing."""
    
    def __init__(self, fast_llm_client: Any):
        """Initialize with a fast LLM client for request classification."""
        self.fast_llm = fast_llm_client
        self.handlers: Dict[RequestType, Callable] = {}
    
    async def classify_request(self, user_input: str) -> RequestType:
        """Classify the user request using the fast LLM."""
        try:
            # TODO: Implement actual LLM classification
            # This is a placeholder - replace with actual LLM call
            classification = await self._classify_with_llm(user_input)
            return RequestType(classification.lower())
        except Exception as e:
            logger.error(f"Error classifying request: {e}")
            return RequestType.ASSISTANT  # Default to assistant on error
    
    async def _classify_with_llm(self, user_input: str) -> str:
        """Classify the request using the fast LLM."""
        # TODO: Implement actual LLM call to gpt-40-mini
        # This is a simplified example - implement proper prompt engineering
        prompt = f"""
        Classify the following user request into one of these categories:
        - 'rag': For document-based queries that require retrieval
        - 'template': For structured, predefined workflows
        - 'assistant': For general conversational queries
        
        User request: {user_input}
        
        Respond with only one of: rag, template, assistant
        """
        
        # Simulated response - replace with actual LLM call
        # response = await self.fast_llm.complete(prompt)
        # return response.strip().lower()
        
        # Temporary implementation - always returns 'assistant' until LLM is integrated
        return "assistant"
    
    def register_handler(self, request_type: RequestType, handler: Callable) -> None:
        """Register a handler for a specific request type."""
        self.handlers[request_type] = handler
    
    async def handle_request(self, user_input: str, *args, **kwargs) -> Any:
        """Route the request to the appropriate handler based on classification."""
        request_type = await self.classify_request(user_input)
        logger.info(f"Request classified as: {request_type.value}")
        
        handler = self.handlers.get(request_type)
        if handler:
            return await handler(user_input, *args, **kwargs)
        
        # Fallback to assistant if no specific handler found
        assistant_handler = self.handlers.get(RequestType.ASSISTANT)
        if assistant_handler:
            return await assistant_handler(user_input, *args, **kwargs)
            
        raise ValueError(f"No handler registered for request type: {request_type}")


def register_orchestrator_tools(mcp: FastMCP, fast_llm_client: Any) -> RequestOrchestrator:
    """Register orchestrator tools with the MCP server and return the orchestrator instance."""
    orchestrator = RequestOrchestrator(fast_llm_client)
    
    @mcp.tool()
    async def route_request(user_input: str) -> str:
        """Route the user request to the appropriate handler based on classification."""
        try:
            result = await orchestrator.handle_request(user_input)
            return str(result)
        except Exception as e:
            logger.error(f"Error handling request: {e}")
            return f"Error processing your request: {str(e)}"
    
    return orchestrator