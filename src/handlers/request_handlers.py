import logging
from starlette.requests import Request
from starlette.responses import JSONResponse

from ..clients import create_openai_client
from ..core import tool_registry, create_config_processor
from ..utils import create_error_response, create_success_response
from ..utils.request_utils import extract_base_url

logger = logging.getLogger(__name__)

async def process_chat_request(request: Request, openai_api_key: str, server_instructions: str) -> JSONResponse:
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
            {
                "role": "system",
                "content": server_instructions
            },
            {
                "role": "user",
                "content": message
            }
        ]

        openai_client = create_openai_client(openai_api_key, timeout=180.0)
        async with openai_client as client:
            # First API call to get the assistant's response and potential function calls
            response = await client.create_chat_completion(
                messages=messages,
                tools=available_tools,
                model="gpt-4o"
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
                    messages=messages,
                    tools=available_tools,
                    model="gpt-4o"
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


async def process_config_request(request: Request, openai_api_key: str) -> JSONResponse:
    """
    Process Avni configuration using LLM with continuous loop until completion.
    
    Expected headers:
    - avni-auth-token: Required authentication token for Avni API
    - avni-base-url: Optional base URL for Avni API
    
    Expected query parameters:
    - base_url: Optional base URL for Avni API (overrides header)
    
    Expected body:
    {
        "config": {...},
        "context": {...}  // optional
    }
    
    Args:
        request: The incoming request object
        openai_api_key: OpenAI API key for making requests
        
    Returns:
        JSONResponse with the config processing result or error
    """
    try:
        body = await request.json()
        config = body.get("config")
        context = body.get("context")
        
        if not config:
            return create_error_response("Config object is required", 400)
        
        # Get auth token from header
        auth_token = request.headers.get("avni-auth-token")
        if not auth_token:
            return create_error_response("avni-auth-token header is required", 401)
        
        # Extract base URL with priority: query > header > env > default
        base_url = extract_base_url(request)
        
        logger.info(f"Processing config with Avni base URL: {base_url}")
        
        # Create config processor and process the config
        processor = create_config_processor(openai_api_key)
        result = await processor.process_config(
            config=config,
            auth_token=auth_token,
            base_url=base_url,
            context=context
        )
        
        return create_success_response(result)
        
    except Exception as e:
        logger.error(f"Config processing error: {e}")
        import traceback
        logger.error(f"Full traceback: {traceback.format_exc()}")
        return create_error_response("Internal server error", 500)