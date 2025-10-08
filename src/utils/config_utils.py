"""Configuration processing utilities for Avni MCP Server."""

import json
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)


def build_system_instructions(
    operational_context: Dict[str, Any], 
    context: Optional[Dict[str, Any]] = None
) -> str:
    """Build system instructions for the LLM.
    
    Args:
        operational_context: Context from Avni operational modules
        context: Additional context (optional)
        
    Returns:
        Complete system instructions string
    """
    instructions = """You are an AI assistant that processes Avni platform configurations.

Your task is to analyze the provided config and operational context, then create the necessary items using available tools.

CRITICAL PARENT-CHILD RELATIONSHIP RULES:
1. NEVER create child items and parent items simultaneously in the same response
2. ALWAYS create parent items first, wait for their creation results, then use the ACTUAL database IDs
3. For location types: if parentId is specified in config, it refers to array index - you must resolve to actual database ID
4. CREATE ITEMS SEQUENTIALLY, not all at once

EXAMPLE for addressLevelTypes:
- Config has: [{"name":"County","parentId":null}, {"name":"SubCounty","parentId":1}]
- Step 1: Create County first → get real database ID (e.g., 1688)
- Step 2: Create SubCounty with parent_id: 1688 (NOT parent_id: 1)

IMPORTANT: You must respond in JSON format with these fields:
{
  "done": boolean,  // true only when ALL config items are successfully created
  "status": "processing|completed|error",
  "results": {
    "created": [...],  // items successfully created this iteration
    "existing": [...], // items that already exist  
    "errors": [...]    // any errors encountered
  },
  "next_action": "description of what you plan to do next"
}

Only set done=true when you have successfully processed the entire config and all items are created or already exist.

Available tools will help you:
- Get existing location types, locations, programs, subject types, encounter types
- Create new items as needed
- Check what already exists to avoid duplicates

Processing order should be:
1. Location types (address level types) - CREATE PARENTS FIRST, then children with actual IDs
2. Locations - CREATE PARENTS FIRST, then children with actual IDs
3. Subject types
4. Programs
5. Encounter types

SEQUENTIAL CREATION WORKFLOW:
- Create one item at a time if there are dependencies
- Wait for creation result to get the actual database ID
- Use that actual ID for dependent items
- Do NOT create multiple dependent items in the same function call batch

Operational Context from Avni:
""" + json.dumps(operational_context, indent=2)
    
    if context:
        instructions += f"\n\nAdditional Context:\n{json.dumps(context, indent=2)}"
        
    return instructions


def build_initial_input(config: Dict[str, Any]) -> str:
    """Build initial input for the LLM.
    
    Args:
        config: Configuration object to process
        
    Returns:
        Initial input string for the LLM
    """
    return f"""Please process this configuration:

{json.dumps(config, indent=2)}

Start by checking what already exists using the available tools, then create missing items in the correct order (location types, locations, subject types, programs, encounter types).

Remember to respond in JSON format with the required fields."""


def parse_llm_response(response_content: str) -> Dict[str, Any]:
    """Parse JSON response from LLM.
    
    Args:
        response_content: Raw response content from LLM
        
    Returns:
        Parsed response dictionary with fallback structure
    """
    try:
        # Extract JSON from response (LLM might include extra text)
        json_start = response_content.find("{")
        json_end = response_content.rfind("}") + 1
        if json_start >= 0 and json_end > json_start:
            json_str = response_content[json_start:json_end]
            return json.loads(json_str)
        else:
            # Fallback if no JSON found
            return _create_fallback_response("Continue processing")
    except json.JSONDecodeError:
        logger.warning(f"Could not parse LLM JSON response: {response_content}")
        return _create_fallback_response("Continue processing")


def extract_text_content(response) -> str:
    """Extract text content from OpenAI response.
    
    Args:
        response: OpenAI response object
        
    Returns:
        Extracted text content or empty string
    """
    # Use OpenAI response object method
    if hasattr(response, 'output_text'):
        return response.output_text or ""
    
    return ""


def _create_fallback_response(next_action: str) -> Dict[str, Any]:
    """Create fallback response structure when parsing fails.
    
    Args:
        next_action: Description of next action
        
    Returns:
        Fallback response dictionary
    """
    return {
        "done": False,
        "status": "processing", 
        "results": {"created": [], "existing": [], "errors": []},
        "next_action": next_action
    }