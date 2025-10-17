import json
import logging
import os
from typing import Dict, Any

from ..clients import create_openai_client, create_avni_client
from .tool_registry import tool_registry
from ..utils.logging_utils import setup_file_logging
from ..utils.config_utils import (
    build_system_instructions,
    build_initial_input,
    parse_llm_response,
    extract_text_content,
    log_input_list,
    log_openai_response_summary,
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
        self.openai_api_key = openai_api_key

    async def process_config(
        self, config: Dict[str, Any], auth_token: str, task_id: str
    ) -> Dict[str, Any]:
        """
        Process a config object using LLM with continuous loop until done=true.

        Args:
            config: Configuration object to process
            auth_token: Avni API authentication token
            task_id: Task ID to use for logging session

        Returns:
            Dict with done flag, status, results, etc.
        """
        # Use task_id for logging session
        session_logger = setup_file_logging(task_id)

        session_logger.info("=" * 80)
        session_logger.info(f"NEW CONFIG PROCESSING SESSION: {task_id}")
        session_logger.info(f"Config: {json.dumps(config, indent=2)}")
        session_logger.info("=" * 80)

        try:
            # Fetch complete existing configuration context
            logger.info("Fetching complete existing configuration")
            session_logger.info("STEP 1: Fetching complete existing configuration")
            avni_client = create_avni_client()

            # Get complete configuration using the new method
            complete_existing_config = await avni_client.fetch_complete_config(
                auth_token
            )
            if "error" in complete_existing_config:
                session_logger.error(
                    f"Failed to fetch complete configuration: {complete_existing_config['error']}"
                )
                return create_error_result(
                    "Failed to fetch complete configuration",
                    [complete_existing_config["error"]],
                )

            session_logger.info("Successfully fetched complete existing config")

            system_instructions = build_system_instructions()
            session_logger.info("STEP 2: Built system instructions")
            config_input = build_initial_input(config, complete_existing_config)
            session_logger.info("STEP 3: Built initial input for LLM")

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
                    logger.info(f"LLM iteration {iteration + 1}")
                    session_logger.info("=" * 50)
                    session_logger.info(f"LLM ITERATION {iteration + 1}")
                    session_logger.info("=" * 50)

                    if iteration == 0:
                        session_logger.info(f"Input to LLM: {config_input}")
                        response = await client.create_response(
                            input_text=config_input,
                            tools=available_tools,
                            model="gpt-4o",
                            instructions=system_instructions,
                        )
                    else:
                        if current_response and hasattr(
                            current_response, "_input_list"
                        ):
                            input_list = getattr(current_response, "_input_list")
                            session_logger.info(
                                f"Continuing conversation with input_list length: {len(input_list)}"
                            )

                            # Make continuation calls with the input list
                            # noinspection PyProtectedMember
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
                            setattr(response, "_input_list", input_list)
                        else:
                            session_logger.error(
                                "No previous response or input list found!"
                            )
                            break

                    # Log response summary
                    log_openai_response_summary(response, session_logger)

                    # Extract response content - check if it has text output
                    response_content = extract_text_content(response)
                    session_logger.info(f"LLM raw response: {response_content}")

                    # Log the input list for debugging
                    if hasattr(response, "_input_list"):
                        input_list = getattr(response, "_input_list")
                        log_input_list(input_list, session_logger)

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

                    final_response_content = extract_text_content(current_response)
                    session_logger.info(
                        f"Final LLM response after tools: {final_response_content}"
                    )

                    # Parse JSON response from final LLM response
                    # TODO (One possible way to avoid this is to tell the LLM to respond in a particular format)
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


def create_config_processor() -> ConfigProcessor:
    """Factory function to create a config processor."""
    return ConfigProcessor(os.getenv("OPENAI_API_KEY"))
