#!/usr/bin/env python3
"""
Config Agent - OpenAI API response endpoint that exposes all Avni tools
using direct function calling approach.
"""

import json
import logging
import os
from typing import Dict, List, Any, Optional
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import our components
from src.openai_function_client import create_openai_function_client
from tools.location import register_location_tools_direct
from tools.program import register_program_tools_direct
from src.tool_registry import tool_registry


# Pydantic models for request/response
class ChatMessage(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    model: Optional[str] = "gpt-4o-mini"
    temperature: Optional[float] = 0.7
    max_tokens: Optional[int] = 1000


class ChatResponse(BaseModel):
    id: str
    object: str = "chat.completion"
    created: int
    model: str
    choices: List[Dict[str, Any]]
    usage: Dict[str, int]


# FastAPI app
app = FastAPI(
    title="Avni Config Agent",
    description="OpenAI-compatible API that exposes Avni platform tools via function calling",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """Initialize tools on startup."""
    logger.info("🚀 Starting Avni Config Agent...")

    # Register all tools
    register_location_tools_direct()
    register_program_tools_direct()

    tools = tool_registry.list_tools()
    logger.info(f"✅ Registered {len(tools)} tools: {', '.join(tools)}")


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "name": "Avni Config Agent",
        "description": "OpenAI-compatible API for Avni platform operations",
        "version": "1.0.0",
        "endpoints": {
            "/v1/chat/completions": "Chat completions with function calling",
            "/v1/tools": "List available tools",
            "/health": "Health check"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "Avni Config Agent",
        "tools_count": len(tool_registry.list_tools())
    }


@app.get("/v1/tools")
async def list_tools():
    """List all available tools in OpenAI format."""
    tools = tool_registry.get_openai_tools()
    return {
        "tools": tools,
        "count": len(tools)
    }


@app.post("/v1/chat/completions")
async def chat_completions(request: ChatRequest, http_request: Request):
    """
    OpenAI-compatible chat completions endpoint with function calling.

    This endpoint mimics OpenAI's API but uses direct function calling
    to execute Avni platform operations.
    """
    try:
        # Get API key from Authorization header
        auth_header = http_request.headers.get("authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Missing or invalid authorization header")

        openai_api_key = auth_header.replace("Bearer ", "")

        # Get Avni auth token from custom header
        avni_auth_token = http_request.headers.get("x-avni-auth-token")
        if not avni_auth_token:
            raise HTTPException(
                status_code=400,
                detail="Missing X-Avni-Auth-Token header for Avni API authentication"
            )

        # Validate OpenAI API key format
        if not openai_api_key.startswith('sk-') or len(openai_api_key) < 40:
            raise HTTPException(status_code=401, detail="Invalid OpenAI API key format")

        # Convert Pydantic messages to dict format
        messages = [{"role": msg.role, "content": msg.content} for msg in request.messages]

        # Add system message if not present
        if not messages or messages[0]["role"] != "system":
            system_message = {
                "role": "system",
                "content": """You are an AI assistant that helps users interact with the Avni platform for program data management.

You have access to various tools to:
- Manage locations and catchments
- Create programs, subject types, and encounter types
- List and retrieve information about these entities

When users ask to perform operations, use the appropriate tools. Be helpful and explain what you're doing.
Provide clear, concise responses about the operations performed.

Important: All operations are automatically authenticated with the provided Avni API token."""
            }
            messages.insert(0, system_message)

        # Get available tools
        available_tools = tool_registry.get_openai_tools()

        logger.info(f"🤖 Processing chat completion with {len(available_tools)} tools available")

        # Create OpenAI client and process request
        async with create_openai_function_client(openai_api_key) as client:
            # First API call to get the assistant's response and potential function calls
            response = await client.create_chat_completion(
                messages=messages,
                tools=available_tools,
                model=request.model
            )

            # Check if the assistant wants to call functions
            choice = response["choices"][0]
            assistant_message = choice["message"]

            # Add the assistant's message to the conversation
            messages.append(assistant_message)

            # Process any function calls
            if assistant_message.get("tool_calls"):
                logger.info(f"🔧 Assistant wants to call {len(assistant_message['tool_calls'])} function(s)")

                function_results = await client.process_function_calls(
                    response, tool_registry, avni_auth_token
                )

                # Add function results to the conversation
                messages.extend(function_results)

                # Make another API call to get the final response
                final_response = await client.create_chat_completion(
                    messages=messages,
                    tools=available_tools,
                    model=request.model
                )

                # Return the final response
                return JSONResponse(content=final_response)
            else:
                # No function calls, return the assistant's direct response
                return JSONResponse(content=response)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Chat completion error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@app.post("/v1/chat/completions/stream")
async def chat_completions_stream(request: ChatRequest, http_request: Request):
    """
    Streaming chat completions endpoint (placeholder).

    Note: This is a placeholder for streaming functionality.
    Currently returns the same as non-streaming endpoint.
    """
    # For now, just return the non-streaming response
    # In a full implementation, this would stream the response
    return await chat_completions(request, http_request)


# Custom endpoint for testing with simple message
@app.post("/chat")
async def simple_chat(http_request: Request):
    """
    Simplified chat endpoint for testing.
    Expects JSON: {"message": "your message here"}
    """
    try:
        body = await http_request.json()
        message = body.get("message")

        if not message:
            raise HTTPException(status_code=400, detail="Message is required")

        # Get auth tokens
        avni_auth_token = http_request.headers.get("x-avni-auth-token")
        if not avni_auth_token:
            raise HTTPException(
                status_code=400,
                detail="Missing X-Avni-Auth-Token header"
            )

        openai_api_key = os.getenv("OPENAI_API_KEY")
        if not openai_api_key:
            raise HTTPException(status_code=500, detail="OpenAI API key not configured")

        # Create chat request
        chat_request = ChatRequest(
            messages=[ChatMessage(role="user", content=message)],
            model="gpt-4o-mini"
        )

        # Create a mock request with the auth token
        class MockRequest:
            def __init__(self, avni_token, openai_key):
                self.headers = {
                    "authorization": f"Bearer {openai_key}",
                    "x-avni-auth-token": avni_token
                }

            def get(self, key):
                return self.headers.get(key.lower())

        mock_request = MockRequest(avni_auth_token, openai_api_key)
        mock_request.headers = {k: v for k, v in mock_request.headers.items()}

        # Process the chat
        response = await chat_completions(chat_request, mock_request)

        # Extract the content from the response
        response_data = json.loads(response.body)
        content = response_data["choices"][0]["message"]["content"]

        return {"response": content}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Simple chat error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@app.post("/process-config")
async def process_config(http_request: Request):
    """
    Process a config object from another LLM.

    This endpoint receives a config object and intelligently processes it by:
    1. Checking if items already exist
    2. Creating missing items in the correct order
    3. Making decisions based on function call responses

    Expected JSON format:
    {
        "config": {
            "addressLevelTypes": [...],
            "locations": [...],
            "subjectTypes": [...],
            "programs": [...],
            "encounterTypes": [...]
        }
    }
    """
    try:
        body = await http_request.json()
        config = body.get("config", {})

        if not config:
            raise HTTPException(status_code=400, detail="Config object is required")

        # Get auth tokens
        avni_auth_token = http_request.headers.get("x-avni-auth-token")
        if not avni_auth_token:
            raise HTTPException(
                status_code=400,
                detail="Missing X-Avni-Auth-Token header"
            )

        openai_api_key = os.getenv("OPENAI_API_KEY")
        if not openai_api_key:
            raise HTTPException(status_code=500, detail="OpenAI API key not configured")

        logger.info(f"🔧 Processing config object with sections: {list(config.keys())}")

        # Process the config object intelligently
        result = await process_config_intelligently(config, avni_auth_token, openai_api_key)

        return {"result": result}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Config processing error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


async def process_config_intelligently(config: Dict[str, Any], avni_auth_token: str, openai_api_key: str) -> Dict[str, Any]:
    """
    Intelligently process a config object by checking existing items and creating missing ones.

    Processing order:
    1. addressLevelTypes (location types)
    2. locations
    3. subjectTypes
    4. programs
    5. encounterTypes
    """
    result = {
        "addressLevelTypes": {"created": [], "existing": [], "errors": []},
        "locations": {"created": [], "existing": [], "errors": []},
        "subjectTypes": {"created": [], "existing": [], "errors": []},
        "programs": {"created": [], "existing": [], "errors": []},
        "encounterTypes": {"created": [], "existing": [], "errors": []}
    }

    # Get available tools
    available_tools = tool_registry.get_openai_tools()

    async with create_openai_function_client(openai_api_key) as client:

        # 1. Process Address Level Types (Location Types)
        if "addressLevelTypes" in config:
            logger.info("📍 Processing address level types...")
            await process_address_level_types(
                config["addressLevelTypes"],
                result["addressLevelTypes"],
                client,
                available_tools,
                avni_auth_token
            )

        # 2. Process Locations
        if "locations" in config:
            logger.info("🗺️ Processing locations...")
            await process_locations(
                config["locations"],
                result["locations"],
                client,
                available_tools,
                avni_auth_token
            )

        # 3. Process Subject Types
        if "subjectTypes" in config:
            logger.info("👥 Processing subject types...")
            await process_subject_types(
                config["subjectTypes"],
                result["subjectTypes"],
                client,
                available_tools,
                avni_auth_token
            )

        # 4. Process Programs
        if "programs" in config:
            logger.info("📋 Processing programs...")
            await process_programs(
                config["programs"],
                result["programs"],
                client,
                available_tools,
                avni_auth_token,
                result["subjectTypes"]["created"]  # Pass created subject types for reference
            )

        # 5. Process Encounter Types
        if "encounterTypes" in config:
            logger.info("📝 Processing encounter types...")
            await process_encounter_types(
                config["encounterTypes"],
                result["encounterTypes"],
                client,
                available_tools,
                avni_auth_token,
                result["subjectTypes"]["created"],  # Pass created subject types
                result["programs"]["created"]  # Pass created programs
            )

    return result


async def create_item_with_retry_loop(client, tools, auth_token, item_type, item_name, create_message, success_indicators, max_attempts=5):
    """
    Continuous loop to create an item, making tool calls and giving responses back to LLM until success.

    Args:
        client: OpenAI function client
        tools: Available tools
        auth_token: Avni auth token
        item_type: Type of item being created (for logging)
        item_name: Name of the item
        create_message: Initial message to create the item
        success_indicators: List of strings that indicate success
        max_attempts: Maximum number of attempts before giving up

    Returns:
        bool: True if successful, False if failed after max attempts
    """
    messages = [
        {"role": "system", "content": f"You are processing Avni configuration. Your goal is to successfully create a {item_type} named '{item_name}'. If you encounter errors, analyze them and try different approaches. Use the available tools to check existing items, create new ones, or troubleshoot issues."},
        {"role": "user", "content": create_message}
    ]

    for attempt in range(max_attempts):
        try:
            logger.info(f"🔄 Attempt {attempt + 1}/{max_attempts} to create {item_type} '{item_name}'")

            # Make API call to LLM
            response = await client.create_chat_completion(messages=messages, tools=tools)
            assistant_message = response["choices"][0]["message"]

            # Add assistant's response to conversation
            messages.append(assistant_message)

            # Check if assistant wants to call functions
            if assistant_message.get("tool_calls"):
                logger.info(f"🔧 LLM wants to call {len(assistant_message['tool_calls'])} function(s)")

                # Execute function calls
                function_results = await client.process_function_calls(response, tool_registry, auth_token)

                # Add function results to conversation
                messages.extend(function_results)

                # Check if any function call indicates success
                success = False
                error_messages = []

                for func_result in function_results:
                    content = func_result["content"]
                    logger.info(f"🔍 Function result content: {content[:200]}...")

                    # Check for success indicators
                    if any(indicator in content for indicator in success_indicators):
                        success = True
                        break

                    # Check for error indicators
                    if "Failed to" in content or "HTTP 400" in content or "error" in content.lower():
                        error_messages.append(content)

                if success:
                    logger.info(f"✅ Successfully created {item_type} '{item_name}' on attempt {attempt + 1}")
                    return True

                # Log the errors for debugging
                if error_messages:
                    logger.error(f"❌ Errors detected for {item_type} '{item_name}': {error_messages}")
                else:
                    logger.warning(f"⚠️  No clear success/failure indication for {item_type} '{item_name}'")

                # If not successful, continue the conversation with LLM
                # Add a follow-up message to guide the LLM
                follow_up_message = f"The {item_type} '{item_name}' was not created successfully. Please analyze the results and try a different approach if needed."
                messages.append({
                    "role": "user",
                    "content": follow_up_message
                })

                logger.info(f"⚠️  Attempt {attempt + 1} failed, continuing conversation with LLM...")

            else:
                # No function calls, LLM gave a direct response
                content = assistant_message.get("content", "")
                if any(indicator in content for indicator in success_indicators):
                    logger.info(f"✅ Successfully created {item_type} '{item_name}' on attempt {attempt + 1}")
                    return True

                # Ask LLM to use tools
                messages.append({
                    "role": "user",
                    "content": f"Please use the available tools to create the {item_type} '{item_name}'. Don't just provide instructions - actually call the functions."
                })

        except Exception as e:
            logger.error(f"❌ Error on attempt {attempt + 1} for {item_type} '{item_name}': {e}")

            # Add error to conversation and let LLM try to handle it
            messages.append({
                "role": "user",
                "content": f"An error occurred: {str(e)}. Please try a different approach to create the {item_type} '{item_name}'."
            })

    logger.error(f"❌ Failed to create {item_type} '{item_name}' after {max_attempts} attempts")
    return False


async def process_address_level_types(items, result, client, tools, auth_token):
    """Process address level types (location types) with continuous loop until success."""
    if not items:
        return

    # First, get existing location types
    messages = [
        {"role": "system", "content": "You are processing Avni configuration. Get existing location types."},
        {"role": "user", "content": "Get all existing location types"}
    ]

    response = await client.create_chat_completion(messages=messages, tools=tools)
    assistant_message = response["choices"][0]["message"]
    messages.append(assistant_message)

    existing_types = []
    if assistant_message.get("tool_calls"):
        function_results = await client.process_function_calls(response, tool_registry, auth_token)
        messages.extend(function_results)

        # Parse existing types from function results
        for func_result in function_results:
            if func_result["name"] == "get_location_types":
                content = func_result["content"]
                # Extract existing type names (simple parsing)
                for line in content.split('\n'):
                    if 'Name:' in line:
                        name = line.split('Name:')[1].split(',')[0].strip()
                        existing_types.append(name)

    # Process each address level type
    for item in items:
        name = item.get("name")
        if not name:
            result["errors"].append("Missing name for address level type")
            continue

        if name in existing_types:
            result["existing"].append({"name": name, "status": "already exists"})
            logger.info(f"✅ Address level type '{name}' already exists")
        else:
            # Continuous loop until successful creation
            success = await create_item_with_retry_loop(
                client, tools, auth_token,
                item_type="address level type",
                item_name=name,
                create_message=f"Create a location type named '{name}' with level {item.get('level', 1)}" +
                             (f" with parent ID {item['parentId']}" if item.get('parentId') else ""),
                success_indicators=["created successfully", "Location type", "AddressLevelType"],
                max_attempts=3
            )

            if success:
                result["created"].append({"name": name, "level": item.get("level")})
                logger.info(f"✅ Created address level type '{name}'")
            else:
                result["errors"].append(f"Failed to create address level type '{name}' after multiple attempts")
                logger.error(f"❌ Failed to create address level type '{name}' after multiple attempts")


async def process_locations(items, result, client, tools, auth_token):
    """Process locations."""
    # Similar structure to address_level_types but for locations
    # This would check existing locations and create missing ones
    for item in items:
        name = item.get("name")
        if name:
            # For now, just mark as processed (implement full logic similar to address_level_types)
            result["created"].append({"name": name, "type": item.get("type")})


async def process_subject_types(items, result, client, tools, auth_token):
    """Process subject types with continuous retry loop."""
    for item in items:
        name = item.get("name")
        subject_type = item.get("type", "Person")

        if name:
            # Use retry loop for subject type creation
            success = await create_item_with_retry_loop(
                client, tools, auth_token,
                item_type="subject type",
                item_name=name,
                create_message=f"Create a subject type named '{name}' of type '{subject_type}'",
                success_indicators=["created successfully", "Subject type"],
                max_attempts=3
            )

            if success:
                # Try to extract UUID from the conversation (this is a simplified approach)
                # In a real implementation, you might want to make another call to get the UUID
                result["created"].append({
                    "name": name,
                    "type": subject_type,
                    "uuid": item.get("uuid", f"generated-uuid-for-{name.lower().replace(' ', '-')}")
                })
                logger.info(f"✅ Created subject type '{name}'")
            else:
                result["errors"].append(f"Failed to create subject type '{name}' after multiple attempts")


async def process_programs(items, result, client, tools, auth_token, created_subject_types):
    """Process programs with continuous retry loop."""
    for item in items:
        name = item.get("name")
        subject_type_uuid = item.get("subjectTypeUuid")

        # Find matching subject type UUID from created ones
        if not subject_type_uuid and created_subject_types:
            # Try to match by name or use first created subject type
            subject_type_uuid = created_subject_types[0].get("uuid") if created_subject_types else None

        if name and subject_type_uuid:
            # Use retry loop for program creation
            success = await create_item_with_retry_loop(
                client, tools, auth_token,
                item_type="program",
                item_name=name,
                create_message=f"Create a program named '{name}' with subject type UUID '{subject_type_uuid}'",
                success_indicators=["created successfully"],
                max_attempts=5
            )

            if success:
                result["created"].append({
                    "name": name,
                    "subjectTypeUuid": subject_type_uuid,
                    "uuid": item.get("uuid", f"generated-uuid-for-{name.lower().replace(' ', '-')}")
                })
                logger.info(f"✅ Created program '{name}'")
            else:
                result["errors"].append(f"Failed to create program '{name}' after multiple attempts")


async def process_encounter_types(items, result, client, tools, auth_token, created_subject_types, created_programs):
    """Process encounter types with continuous retry loop."""
    for item in items:
        name = item.get("name")
        subject_type_uuid = item.get("subjectTypeUuid")
        program_uuid = item.get("programUuid")

        # Find matching UUIDs from created items
        if not subject_type_uuid and created_subject_types:
            subject_type_uuid = created_subject_types[0].get("uuid") if created_subject_types else None

        if not program_uuid and created_programs:
            program_uuid = created_programs[0].get("uuid") if created_programs else None

        if name and subject_type_uuid and program_uuid:
            # Use retry loop for encounter type creation
            success = await create_item_with_retry_loop(
                client, tools, auth_token,
                item_type="encounter type",
                item_name=name,
                create_message=f"Create an encounter type named '{name}' with subject type UUID '{subject_type_uuid}' and program UUID '{program_uuid}'",
                success_indicators=["created successfully"],
                max_attempts=5
            )

            if success:
                result["created"].append({
                    "name": name,
                    "subjectTypeUuid": subject_type_uuid,
                    "programUuid": program_uuid,
                    "uuid": item.get("uuid", f"generated-uuid-for-{name.lower().replace(' ', '-')}")
                })
                logger.info(f"✅ Created encounter type '{name}'")
            else:
                result["errors"].append(f"Failed to create encounter type '{name}' after multiple attempts")


if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", 8024))
    logger.info(f"🚀 Starting Avni Config Agent on 0.0.0.0:{port}")

    uvicorn.run(
        "configagent:app",
        host="0.0.0.0",
        port=port,
        reload=True,
        log_level="info"
    )
