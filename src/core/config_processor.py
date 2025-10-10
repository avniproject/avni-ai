import json
import logging
from typing import Dict, Any

from ..clients import create_openai_client, create_avni_client
from .tool_registry import tool_registry
from ..utils.logging_utils import setup_file_logging, create_session_id
from ..utils.config_utils import (
    build_system_instructions,
    build_initial_input,
    parse_llm_response,
    extract_text_content,
)
from ..utils.response_utils import (
    create_success_result,
    create_error_result,
    create_max_iterations_result,
)

logger = logging.getLogger(__name__)


class ConfigProcessor:
    """Processes Avni configurations using LLM with continuous loop until completion."""

    def __init__(self, openai_api_key: str):
        """
        Initialize config processor.

        Args:
            openai_api_key: OpenAI API key for LLM calls
        """
        if not openai_api_key:
            raise ValueError("OpenAI API key is required")
        self.openai_api_key = openai_api_key

    async def process_config(
        self, config: Dict[str, Any], auth_token: str, base_url: str
    ) -> Dict[str, Any]:
        """
        Process a config object using LLM with continuous loop until done=true.

        Args:
            config: Configuration object to process
            auth_token: Avni API authentication token
            base_url: Avni API base URL

        Returns:
            Dict with done flag, status, results, etc.
        """
        # Create session ID for logging
        session_id = create_session_id()
        session_logger = setup_file_logging(session_id)

        session_logger.info("=" * 80)
        session_logger.info(f"NEW CONFIG PROCESSING SESSION: {session_id}")
        session_logger.info(f"Base URL: {base_url}")
        session_logger.info(f"Config: {json.dumps(config, indent=2)}")
        session_logger.info("=" * 80)

        try:
            # Fetch complete existing configuration context
            logger.info(f"Fetching complete existing configuration from {base_url}")
            session_logger.info("STEP 1: Fetching complete existing configuration")
            avni_client = create_avni_client(base_url)

            # Get operational modules (contains subject types, programs, encounter types, address level types)
            operational_context = await avni_client.fetch_operational_modules(
                auth_token
            )
            if "error" in operational_context:
                session_logger.error(
                    f"Failed to fetch operational modules: {operational_context['error']}"
                )
                return create_error_result(
                    "Failed to fetch operational modules context",
                    [operational_context["error"]],
                )

            # Get locations (not included in operational modules)
            logger.info("Fetching existing locations")
            session_logger.info("   Fetching existing locations...")
            locations_result = await avni_client.make_request(
                "GET", "/locations", auth_token
            )
            if not locations_result.success:
                session_logger.error(
                    f"Failed to fetch locations: {locations_result.error}"
                )
                return create_error_result(
                    "Failed to fetch existing locations", [locations_result.error]
                )

            # Get catchments (not included in operational modules)
            logger.info("Fetching existing catchments")
            session_logger.info("   Fetching existing catchments...")
            catchments_result = await avni_client.make_request(
                "GET", "/catchment", auth_token
            )
            if not catchments_result.success:
                session_logger.error(
                    f"Failed to fetch catchments: {catchments_result.error}"
                )
                return create_error_result(
                    "Failed to fetch existing catchments", [catchments_result.error]
                )

            # Combine all existing configuration data
            complete_existing_config = operational_context.copy()
            complete_existing_config["locations"] = locations_result.data or []
            complete_existing_config["catchments"] = catchments_result.data or []

            session_logger.info(
                f"Successfully fetched complete existing config with {len(complete_existing_config.get('locations', []))} locations and {len(complete_existing_config.get('catchments', []))} catchments"
            )

            # Build system instructions
            system_instructions = build_system_instructions(complete_existing_config)
            session_logger.info("STEP 2: Built system instructions")
            session_logger.info(f"System instructions: {system_instructions}")

            # Initial input for LLM (includes complete existing config in message body)
            config_input = build_initial_input(config, complete_existing_config)
            session_logger.info("STEP 3: Built initial input for LLM")
            session_logger.info(f"Initial input: {config_input}")

            # Get available tools
            available_tools = tool_registry.get_openai_tools()
            session_logger.info(f"STEP 4: Got {len(available_tools)} available tools")
            for i, tool in enumerate(available_tools, 1):
                tool_name = tool.get("function", {}).get("name", "unknown")
                session_logger.info(f"  Tool {i}: {tool_name}")

            max_iterations = 30  # Prevent infinite loops
            session_logger.info(
                f"STEP 5: Starting LLM iteration loop (max {max_iterations} iterations)"
            )

            async with create_openai_client(
                self.openai_api_key, timeout=180.0
            ) as client:
                # Initialize conversation input list once
                current_response = None

                for iteration in range(max_iterations):
                    logger.info(f"LLM iteration {iteration + 1}/{max_iterations}")
                    session_logger.info("=" * 50)
                    session_logger.info(
                        f"LLM ITERATION {iteration + 1}/{max_iterations}"
                    )
                    session_logger.info("=" * 50)

                    if iteration == 0:
                        # First iteration - use initial config input
                        session_logger.info(f"Input to LLM: {config_input}")
                        response = await client.create_response(
                            input_text=config_input,
                            tools=available_tools,
                            model="gpt-4o",
                            instructions=system_instructions,
                        )
                    else:
                        # Continue conversation using stored input list from previous response
                        if current_response and hasattr(
                            current_response, "_input_list"
                        ):
                            input_list = getattr(current_response, "_input_list")
                            session_logger.info(
                                f"Continuing conversation with input_list length: {len(input_list)}"
                            )

                            # Make continuation call directly with input list
                            response = await client._client.responses.create(
                                model="gpt-4o",
                                instructions=system_instructions,
                                tools=[
                                    {
                                        "type": "function",
                                        "name": tool["function"]["name"],
                                        "description": tool["function"]["description"],
                                        "parameters": tool["function"]["parameters"],
                                    }
                                    for tool in available_tools
                                ],
                                input=input_list,
                            )
                            # Store input list in response
                            setattr(response, "_input_list", input_list)
                        else:
                            session_logger.error(
                                "No previous response or input list found!"
                            )
                            break

                    # DEBUG: Log the complete response structure
                    session_logger.info(
                        f"COMPLETE OpenAI Response: {response.model_dump_json(indent=2)}"
                    )

                    # Extract response content - check if it has text output
                    response_content = extract_text_content(response)
                    session_logger.info(f"LLM raw response: {response_content}")

                    # Log the input list for debugging
                    if hasattr(response, "_input_list"):
                        input_list = getattr(response, "_input_list")
                        session_logger.info("Current input list:")
                        for i, item in enumerate(input_list):
                            if isinstance(item, dict):
                                session_logger.info(
                                    f"  {i}: {item.get('type', item.get('role', 'unknown'))} - {str(item)[:100]}..."
                                )
                            else:
                                session_logger.info(
                                    f"  {i}: {type(item)} - {str(item)[:100]}..."
                                )

                    # Process any function calls and continue the conversation (with filtered tools)
                    current_response = await client.process_function_calls_and_continue(
                        response,
                        tool_registry,
                        auth_token,
                        model="gpt-4o",
                        instructions=system_instructions,
                        available_tools=available_tools,
                        session_logger=session_logger,
                    )

                    # Extract final response content
                    final_response_content = extract_text_content(current_response)
                    session_logger.info(
                        f"Final LLM response after tools: {final_response_content}"
                    )

                    # Parse JSON response from final LLM response
                    llm_result = parse_llm_response(final_response_content)
                    session_logger.info(
                        f"Parsed LLM result: {json.dumps(llm_result, indent=2)}"
                    )

                    # Check if LLM says it's done
                    if llm_result.get("done", False):
                        logger.info("LLM indicates processing is complete")
                        session_logger.info("✅ LLM indicates processing is COMPLETE!")
                        final_result = create_success_result(llm_result, iteration + 1)
                        session_logger.info(
                            f"Final result: {json.dumps(final_result, indent=2)}"
                        )
                        return final_result

                    # Log current conversation state for next iteration
                    if hasattr(current_response, "_input_list"):
                        input_list = getattr(current_response, "_input_list")
                        session_logger.info(
                            f"Conversation will continue with input_list length: {len(input_list)}"
                        )
                        for i, item in enumerate(input_list):
                            if isinstance(item, dict):
                                session_logger.info(
                                    f"  {i}: {item.get('type', item.get('role', 'unknown'))} - {str(item)[:100]}..."
                                )
                            else:
                                session_logger.info(
                                    f"  {i}: {type(item)} - {str(item)[:100]}..."
                                )

                # Max iterations reached
                logger.warning(f"Reached maximum iterations ({max_iterations})")
                session_logger.error(
                    f"❌ REACHED MAXIMUM ITERATIONS ({max_iterations}) WITHOUT COMPLETION"
                )
                session_logger.error(
                    "The LLM never set done=true. Check the conversation above for issues."
                )
                max_iter_result = create_max_iterations_result(max_iterations)
                session_logger.info(
                    f"Max iterations result: {json.dumps(max_iter_result, indent=2)}"
                )
                return max_iter_result

        except Exception as e:
            logger.error(f"Config processing error: {e}")
            session_logger.error(f"❌ EXCEPTION OCCURRED: {str(e)}")
            session_logger.error(f"Exception type: {type(e).__name__}")
            import traceback

            session_logger.error(f"Traceback: {traceback.format_exc()}")
            error_result = create_error_result(f"Processing failed: {str(e)}")
            session_logger.info(f"Error result: {json.dumps(error_result, indent=2)}")
            return error_result


def create_config_processor(openai_api_key: str) -> ConfigProcessor:
    """
    Factory function to create a config processor.

    Args:
        openai_api_key: OpenAI API key

    Returns:
        Configured config processor
    """
    return ConfigProcessor(openai_api_key)
