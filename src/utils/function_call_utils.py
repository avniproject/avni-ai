"""Function call processing utilities for OpenAI Responses API."""

import json
import logging
from typing import Dict, List, Any, Optional
from src.utils.session_context import set_session_logger

logger = logging.getLogger(__name__)


def parse_function_arguments(
    arguments_str: str, call_id: str
) -> Optional[Dict[str, Any]]:
    """Parse function arguments from string, handling JSON errors.

    Args:
        arguments_str: The arguments string from OpenAI function call
        call_id: The call ID for error logging

    Returns:
        Parsed arguments dict or None on error
    """
    try:
        if isinstance(arguments_str, str):
            return json.loads(arguments_str)
        else:
            return arguments_str
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in function arguments for call {call_id}: {e}")
        return None


def add_function_output(
    input_list: List, call_id: str, result: Any, is_error: bool = False
) -> None:
    """Add function call result or error to the input list.

    Args:
        input_list: The conversation input list to modify
        call_id: The function call ID
        result: The function result or error message
        is_error: Whether this is an error result
    """
    if is_error:
        output_data = {"error": str(result)}
        logger.info(f"   Added error output to input_list")
    else:
        output_data = result  # Direct result, not wrapped in {"result": ...}
        logger.info(f"   Added function output to input_list")

    function_output = {
        "type": "function_call_output",
        "call_id": call_id,
        "output": json.dumps(output_data),
    }
    input_list.append(function_output)


def format_tools_for_continuation(
    available_tools: Optional[List[Dict[str, Any]]], tool_registry
) -> List[Dict[str, Any]]:
    """Format tools for continuation API call.

    Args:
        available_tools: Optional list of available tools
        tool_registry: The tool registry to get tools from if available_tools is None

    Returns:
        List of formatted tools for OpenAI API
    """
    formatted_tools = []
    tools_to_use = (
        available_tools if available_tools else tool_registry.get_openai_tools()
    )

    for tool in tools_to_use:
        if tool.get("type") == "function":
            formatted_tools.append(
                {
                    "type": "function",
                    "name": tool["function"]["name"],
                    "description": tool["function"]["description"],
                    "parameters": tool["function"]["parameters"],
                }
            )

    return formatted_tools


def extract_function_calls(response) -> List[Dict[str, Any]]:
    """Extract and log function calls from the response output.

    Args:
        response: OpenAI response object with output attribute

    Returns:
        List of function call dictionaries with name, call_id, and arguments
    """
    function_calls = []

    logger.info("📋 Checking for function calls in response...")
    for i, item in enumerate(response.output):
        logger.info(f"  Checking item {i}: type={item.type}")
        if item.type == "function_call":
            logger.info(f"  ✅ Found function call: {item.name}")
            function_calls.append(
                {
                    "name": item.name,
                    "call_id": item.call_id,
                    "arguments": item.arguments,
                }
            )
        else:
            logger.info(f"  ℹ️  Non-function item: {item.type}")

    return function_calls


async def execute_function_call(
    function_name: str,
    function_args: Dict[str, Any],
    tool_registry,
    auth_token: str,
    session_logger: Optional[logging.Logger] = None,
) -> Any:
    """Execute a single function call and return the result.

    Args:
        function_name: Name of the function to call
        function_args: Arguments for the function
        tool_registry: The tool registry to execute functions
        auth_token: Authentication token to inject
        session_logger: Optional session logger for detailed logging

    Returns:
        The function execution result
    """
    # Inject auth_token for all function calls
    function_args["auth_token"] = auth_token

    logger.info(f"🔧 Executing function: {function_name}")

    # Always log to session logger during config processing
    if session_logger:
        session_logger.info(f"🔧 EXECUTING FUNCTION: {function_name}")
        session_logger.info(f"   Arguments: {json.dumps(function_args, indent=2)}")
        # Set session logger context for tools to use
        set_session_logger(session_logger)

    result = await tool_registry.call_tool(function_name, function_args)
    logger.info(f"   Function result: {str(result)[:200]}...")

    # Always log result to session logger
    if session_logger:
        session_logger.info(f"   Function result: {str(result)}")
        session_logger.info(f"   ---")

    return result
