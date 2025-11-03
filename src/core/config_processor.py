import json
import logging
import os
from typing import Dict, Any, Callable, Optional
from dataclasses import dataclass

from ..clients import AvniClient, OpenAIResponsesClient
from .tool_registry import tool_registry
from ..utils.env import OPENAI_API_KEY
from .config_llm_helper import (
    build_system_instructions,
    build_initial_input,
    parse_llm_response,
    extract_text_content,
    log_input_list,
    log_openai_response_summary,
)

logger = logging.getLogger(__name__)


def setup_file_logging(task_id: str) -> logging.Logger:
    logs_dir = "logs"
    os.makedirs(logs_dir, exist_ok=True)

    task_logger = logging.getLogger(f"config_session_{task_id}")
    task_logger.setLevel(logging.INFO)

    for handler in task_logger.handlers[:]:
        task_logger.removeHandler(handler)

    log_file = os.path.join(logs_dir, f"config_session_{task_id}.log")
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.INFO)

    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)

    task_logger.addHandler(file_handler)

    return task_logger


@dataclass
class ConfigProcessResult:
    done: bool
    status: str
    results: Dict[str, Any]
    end_user_result: str
    iterations: Optional[int] = None
    function_calls_made: int = 0
    message: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        result = {
            "done": self.done,
            "status": self.status,
            "results": self.results,
            "endUserResult": self.end_user_result,
            "function_calls_made": self.function_calls_made,
        }

        if self.iterations is not None:
            result["iterations"] = self.iterations
        if self.message is not None:
            result["message"] = self.message

        return result


def create_success_result(
    llm_result: Dict[str, Any], iterations: int
) -> ConfigProcessResult:
    results = llm_result.get("results", {})
    end_user_result = llm_result.get("endUserResult", "")

    return ConfigProcessResult(
        done=True,
        status="completed",
        results=results,
        end_user_result=end_user_result,
        iterations=iterations,
        function_calls_made=0,  # Not tracking individual function calls anymore
    )


def create_error_result(
    error_message: str, additional_errors: list = None
) -> ConfigProcessResult:
    errors = [error_message]
    if additional_errors:
        errors.extend(additional_errors)

    return ConfigProcessResult(
        done=False,
        status="error",
        results={
            "deleted_address_level_types": [],
            "deleted_locations": [],
            "deleted_catchments": [],
            "deleted_subject_types": [],
            "deleted_programs": [],
            "deleted_encounter_types": [],
            "updated_address_level_types": [],
            "updated_locations": [],
            "updated_catchments": [],
            "updated_subject_types": [],
            "updated_programs": [],
            "updated_encounter_types": [],
            "created_address_level_types": [],
            "created_locations": [],
            "created_catchments": [],
            "created_subject_types": [],
            "created_programs": [],
            "created_encounter_types": [],
            "existing_address_level_types": [],
            "existing_locations": [],
            "existing_catchments": [],
            "existing_subject_types": [],
            "existing_programs": [],
            "existing_encounter_types": [],
            "errors": errors,
        },
        end_user_result=f"Configuration processing failed: {error_message}",
        message=error_message,
    )


def create_max_iterations_result(max_iterations: int) -> ConfigProcessResult:
    error_message = "Processing incomplete - reached maximum iterations"

    return ConfigProcessResult(
        done=False,
        status="error",
        results={
            "deleted_address_level_types": [],
            "deleted_locations": [],
            "deleted_catchments": [],
            "deleted_subject_types": [],
            "deleted_programs": [],
            "deleted_encounter_types": [],
            "updated_address_level_types": [],
            "updated_locations": [],
            "updated_catchments": [],
            "updated_subject_types": [],
            "updated_programs": [],
            "updated_encounter_types": [],
            "created_address_level_types": [],
            "created_locations": [],
            "created_catchments": [],
            "created_subject_types": [],
            "created_programs": [],
            "created_encounter_types": [],
            "existing_address_level_types": [],
            "existing_locations": [],
            "existing_catchments": [],
            "existing_subject_types": [],
            "existing_programs": [],
            "existing_encounter_types": [],
            "errors": ["Maximum iterations reached"],
        },
        end_user_result=f"❌ {error_message}",
        iterations=max_iterations,
        message=error_message,
    )


class ConfigProcessor:
    @staticmethod
    async def process_config(
        config: Dict[str, Any],
        auth_token: str,
        task_id: str,
        progress_callback: Callable[[str], None],
    ) -> ConfigProcessResult:
        session_logger = setup_file_logging(task_id)

        session_logger.info("=" * 80)
        session_logger.info(f"NEW CONFIG PROCESSING SESSION: {task_id}")
        session_logger.info(f"Config: {json.dumps(config, indent=2)}")
        session_logger.info("=" * 80)

        try:
            session_logger.info("STEP 1: Fetching complete existing configuration")
            avni_client = AvniClient()
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

            async with OpenAIResponsesClient(OPENAI_API_KEY, 120.0) as client:
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

                    log_openai_response_summary(response, session_logger)
                    response_content = extract_text_content(response)
                    session_logger.info(f"LLM raw response: {response_content}")

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

                    # TODO (One possible way to avoid parse_llm_response is to tell the LLM to respond in a particular format?)
                    llm_result = parse_llm_response(final_response_content)
                    session_logger.info(
                        f"Parsed LLM result: {json.dumps(llm_result, indent=2)}"
                    )

                    if llm_result.get("endUserResult"):
                        progress_callback(llm_result["endUserResult"])

                    if llm_result.get("done", False):
                        logger.info("LLM indicates processing is complete")
                        session_logger.info("✅ LLM indicates processing is COMPLETE!")
                        final_result = create_success_result(llm_result, iteration + 1)
                        session_logger.info(
                            f"Final result: {json.dumps(final_result.to_dict(), indent=2)}"
                        )
                        return final_result

                    if hasattr(current_response, "_input_list"):
                        input_list = getattr(current_response, "_input_list")
                        session_logger.info(
                            f"Conversation will continue with input_list length: {len(input_list)}"
                        )

                logger.warning(f"Reached maximum iterations ({max_iterations})")
                session_logger.error(
                    f"❌ REACHED MAXIMUM ITERATIONS ({max_iterations}) WITHOUT COMPLETION"
                )
                session_logger.error(
                    "The LLM never set done=true. Check the conversation above for issues."
                )
                max_iter_result = create_max_iterations_result(max_iterations)
                session_logger.info(
                    f"Max iterations result: {json.dumps(max_iter_result.to_dict(), indent=2)}"
                )
                return max_iter_result

        except Exception as e:
            logger.error(f"Config processing error: {e}")
            session_logger.error(f"❌ EXCEPTION OCCURRED: {str(e)}")
            session_logger.error(f"Exception type: {type(e).__name__}")
            import traceback

            session_logger.error(f"Traceback: {traceback.format_exc()}")
            error_result = create_error_result(f"Processing failed: {str(e)}")
            session_logger.info(
                f"Error result: {json.dumps(error_result.to_dict(), indent=2)}"
            )
            return error_result
