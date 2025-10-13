import logging
from starlette.requests import Request
from starlette.responses import JSONResponse

from ..clients import create_openai_client
from ..core import tool_registry, create_config_processor
from ..core.task_manager import task_manager, TaskStatus
from ..utils import create_error_response, create_success_response
from ..utils.request_utils import extract_base_url

logger = logging.getLogger(__name__)


async def process_chat_request(
    request: Request, openai_api_key: str, server_instructions: str
) -> JSONResponse:
    """Process a complete chat request using direct function calling.

    Args:
        request: The incoming request object
        openai_api_key: OpenAI API key for making requests
        server_instructions: System instructions for the AI assistant

    Returns:
        JSONResponse with the chat result or error
    """
    try:
        body = await request.json()
        message = body.get("message")

        if not message:
            return create_error_response("Message is required", 400)

        auth_token = request.headers.get("AUTH-TOKEN")
        if not auth_token:
            return create_error_response("AUTH-TOKEN header is required", 401)

        # Get available tools from the registry
        available_tools = tool_registry.get_openai_tools()

        # Create messages for the conversation
        messages = [
            {"role": "system", "content": server_instructions},
            {"role": "user", "content": message},
        ]

        openai_client = create_openai_client(openai_api_key, timeout=180.0)
        async with openai_client as client:
            # First API call to get the assistant's response and potential function calls
            response = await client.create_chat_completion(
                messages=messages, tools=available_tools, model="gpt-4o"
            )

            # Check if the assistant wants to call functions
            choice = response["choices"][0]
            assistant_message = choice["message"]

            # Add the assistant's message to the conversation
            messages.append(assistant_message)

            # Process any function calls
            if assistant_message.get("tool_calls"):
                function_results = await client.process_function_calls(
                    response, tool_registry, auth_token
                )

                # Add function results to the conversation
                messages.extend(function_results)

                # Make another API call to get the final response
                final_response = await client.create_chat_completion(
                    messages=messages, tools=available_tools, model="gpt-4o"
                )

                final_message = final_response["choices"][0]["message"]
                output_text = final_message.get("content", "No response generated")
            else:
                # No function calls, use the assistant's direct response
                output_text = assistant_message.get("content", "No response generated")

        return create_success_response({"response": output_text})

    except Exception as e:
        logger.error(f"Chat request processing error: {e}")
        import traceback

        logger.error(f"Full traceback: {traceback.format_exc()}")
        return create_error_response("Internal server error", 500)


async def process_config_request(request: Request) -> JSONResponse:
    """
    Process Avni configuration using LLM with CRUD operations (create, update, delete).

    Expected headers:
    - avni-auth-token: Required authentication token for Avni API
    - avni-base-url: Optional base URL for Avni API

    Expected query parameters:
    - base_url: Optional base URL for Avni API (overrides header)

    Expected body:
    {
        "config": {
            "create": {
                "addressLevelTypes": [...],
                "locations": [...],
                "catchments": [...],
                "subjectTypes": [...],
                "programs": [...],
                "encounterTypes": [...]
            },
            "update": {
                "addressLevelTypes": [...],
                "locations": [...],
                "catchments": [...],
                "subjectTypes": [...],
                "programs": [...],
                "encounterTypes": [...]
            },
            "delete": {
                "addressLevelTypes": [...],
                "locations": [...],
                "catchments": [...],
                "subjectTypes": [...],
                "programs": [...],
                "encounterTypes": [...]
            }
        }
    }

    Args:
        request: The incoming request object
        openai_api_key: OpenAI API key for making requests

    Returns:
        JSONResponse with the config processing result or error
    """
    try:
        body = await request.json()
        config_data = body.get("config")

        if not config_data:
            return create_error_response("config object is required", 400)

        # Validate that config has at least one operation
        if not any(op in config_data for op in ["create", "update", "delete"]):
            return create_error_response(
                "config must contain at least one of: create, update, delete", 400
            )

        # Get auth token from header
        auth_token = request.headers.get("avni-auth-token")
        if not auth_token:
            return create_error_response("avni-auth-token header is required", 401)

        # Extract base URL with priority: query > header > env > default
        base_url = extract_base_url(request)

        logger.info(f"Processing CRUD config with Avni base URL: {base_url}")
        logger.info(f"Operations requested: {list(config_data.keys())}")

        # Create config processor and process the config
        processor = create_config_processor()
        result = await processor.process_config(
            config=config_data, auth_token=auth_token, base_url=base_url
        )

        return create_success_response(result)

    except Exception as e:
        logger.error(f"Config processing error: {e}")
        import traceback

        logger.error(f"Full traceback: {traceback.format_exc()}")
        return create_error_response("Internal server error", 500)


async def process_config_async_request(request: Request) -> JSONResponse:
    """
    Start async configuration processing and return task ID immediately.
    
    Same request format as /process-config but returns immediately with task ID.
    Use /process-config-status/{task_id} to check progress.
    """
    try:
        body = await request.json()
        config_data = body.get("config")

        if not config_data:
            return create_error_response("config object is required", 400)

        # Validate that config has at least one operation
        if not any(op in config_data for op in ["create", "update", "delete"]):
            return create_error_response(
                "config must contain at least one of: create, update, delete", 400
            )

        # Get auth token from header
        auth_token = request.headers.get("avni-auth-token")
        if not auth_token:
            return create_error_response("avni-auth-token header is required", 401)

        # Extract base URL with priority: query > header > env > default
        base_url = extract_base_url(request)

        logger.info(f"Starting async CRUD config processing with Avni base URL: {base_url}")
        logger.info(f"Operations requested: {list(config_data.keys())}")

        # Create task
        task_id = task_manager.create_task(
            config_data=config_data,
            auth_token=auth_token,
            base_url=base_url
        )

        # Start background processing
        processor = create_config_processor()
        task_manager.start_background_task(task_id, processor, None)  # API key handled internally

        # Return task ID immediately
        return create_success_response({
            "task_id": task_id,
            "status": "processing",
            "message": "Configuration processing started. Use /process-config-status/{task_id} to check progress."
        })

    except Exception as e:
        logger.error(f"Async config processing error: {e}")
        import traceback
        logger.error(f"Full traceback: {traceback.format_exc()}")
        return create_error_response("Internal server error", 500)


async def get_task_status(task_id: str) -> JSONResponse:
    """
    Get status and result of a configuration processing task.
    """
    try:
        task = task_manager.get_task(task_id)
        
        if not task:
            return create_error_response(f"Task {task_id} not found or expired", 404)

        return create_success_response(task.to_dict())

    except Exception as e:
        logger.error(f"Task status error: {e}")
        return create_error_response("Internal server error", 500)
