import logging
from typing import Dict, List, Any, Optional
from openai import AsyncOpenAI

from ..utils.function_call_utils import (
    parse_function_arguments,
    add_function_output,
    format_tools_for_continuation,
    extract_function_calls,
    execute_function_call,
)

logger = logging.getLogger(__name__)


class OpenAIResponsesClient:
    def __init__(self, api_key: str, timeout: float = 120.0):
        if not api_key:
            raise ValueError("OpenAI API key is required")

        self.api_key = api_key
        self._client = AsyncOpenAI(api_key=api_key, timeout=timeout)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._client.close()

    async def close(self):
        """Close the OpenAI client."""
        await self._client.close()

    async def create_response(
        self,
        input_text: str,
        tools: List[Dict[str, Any]],
        model: str = "gpt-4o",
        instructions: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Create a response using OpenAI's Responses API with conversation flow."""

        # Convert tools to format expected by OpenAI library
        formatted_tools = []
        if tools:
            for tool in tools:
                if tool.get("type") == "function":
                    formatted_tools.append(
                        {
                            "type": "function",
                            "name": tool["function"]["name"],
                            "description": tool["function"]["description"],
                            "parameters": tool["function"]["parameters"],
                        }
                    )

        input_list = [{"role": "user", "content": input_text}]

        logger.info(
            f"📞 Making initial OpenAI API call with {len(formatted_tools)} tools"
        )
        logger.info(f"📝 Initial input_list length: {len(input_list)}")

        try:
            response = await self._client.responses.create(
                model=model,
                input=input_list,
                tools=formatted_tools,
                tool_choice="auto",
                instructions=instructions,
            )

            logger.info(f"✅ Got response with {len(response.output)} output items")

            # Log what we got
            for i, item in enumerate(response.output):
                logger.info(f"  Item {i}: type={item.type}")
                if hasattr(item, "name"):
                    logger.info(f"    name={item.name}")
                if hasattr(item, "call_id"):
                    logger.info(f"    call_id={item.call_id}")
                if hasattr(item, "arguments"):
                    logger.info(f"    arguments={item.arguments}")
                if hasattr(item, "content"):
                    logger.info(f"    content={getattr(item, 'content', None)}")

            # Store the input list in the response object for continuation
            # Keep the OpenAI response object to preserve methods like .output_text
            setattr(response, "_input_list", input_list)

            return response
        except Exception as e:
            logger.error(f"OpenAI Responses API error: {e}")
            raise

    async def _make_continuation_call(
        self,
        input_list: List,
        formatted_tools: List[Dict[str, Any]],
        model: str,
        instructions: Optional[str],
    ) -> Any:
        """Make the continuation API call after function execution."""
        logger.info("📞 Making continuation API call after function execution...")
        logger.info(
            f"📝 Final input list length before continuation: {len(input_list)}"
        )

        continue_response = await self._client.responses.create(
            model=model,
            instructions=instructions,
            tools=formatted_tools,
            input=input_list,
        )

        logger.info(
            f"✅ Got continuation response with {len(continue_response.output)} output items"
        )
        logger.info(f"🎉 Final output text: {continue_response.output_text}")

        return continue_response

    async def process_function_calls_and_continue(
        self,
        response: Dict[str, Any],
        tool_registry,
        auth_token: str,
        model: str = "gpt-4o",
        instructions: Optional[str] = None,
        available_tools: List[Dict[str, Any]] = None,
        session_logger: Optional[logging.Logger] = None,
    ) -> Dict[str, Any]:
        input_list = getattr(response, "_input_list", [])

        input_list += response.output

        function_calls = extract_function_calls(response)

        if not function_calls:
            logger.info("ℹ️  No function calls made, returning original response")
            setattr(response, "_input_list", input_list)
            return response

        function_calls_processed = 0
        for func_call in function_calls:
            function_name = func_call["name"]
            call_id = func_call["call_id"]
            arguments_str = func_call["arguments"]

            logger.info(f"🔧 Processing function call: {function_name}")
            logger.info(f"   Arguments: {arguments_str}")
            logger.info(f"   Call ID: {call_id}")

            function_args = parse_function_arguments(arguments_str, call_id)
            if function_args is None:
                # Add error for invalid JSON
                add_function_output(
                    input_list, call_id, f"Invalid JSON: {arguments_str}", is_error=True
                )
                continue

            try:
                result = await execute_function_call(
                    function_name,
                    function_args,
                    tool_registry,
                    auth_token,
                    session_logger,
                )

                add_function_output(input_list, call_id, result, is_error=False)
                function_calls_processed += 1

            except Exception as e:
                logger.error(f"❌ Error executing function {function_name}: {e}")
                add_function_output(input_list, call_id, str(e), is_error=True)

        logger.info(f"📊 Processed {function_calls_processed} function calls")

        try:
            formatted_tools = format_tools_for_continuation(
                available_tools, tool_registry
            )

            continue_response = await self._make_continuation_call(
                input_list, formatted_tools, model, instructions
            )

            setattr(continue_response, "_input_list", input_list)
            return continue_response

        except Exception as e:
            logger.error(f"OpenAI conversation continuation error: {e}")
            raise
