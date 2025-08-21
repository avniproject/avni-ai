"""
Avni MCP Server for OpenAI Integration

This server implements the Model Context Protocol (MCP) with Avni health platform
operations designed to work with OpenAI's chat and tool calling features.
"""

import logging
import os

from dotenv import load_dotenv
from fastmcp import FastMCP
from openai import OpenAI
from openai.types.responses.tool_param import Mcp
from starlette.requests import Request
from starlette.responses import JSONResponse

from utils import create_error_response, create_success_response, create_cors_middleware

from tools.location import register_location_tools
from tools.organization import register_organization_tools
from tools.program import register_program_tools
from tools.user import register_user_tools

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# OpenAI configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
base_url = os.getenv("AVNI_MCP_SERVER_URL")
AVNI_MCP_SERVER_URL = base_url + "/mcp"
AVNI_BASE_URL = os.getenv("AVNI_BASE_URL")

# Initialize OpenAI client
openai_client = OpenAI()

# Server instructions for OpenAI
server_instructions = """
You are an AI assistant that helps users interact with the Avni platform for health data management.

You have access to various tools to:
- Create organizations, users, and user groups  
- Manage locations and catchments
- Create programs, subject types, and encounter types
- List and retrieve information about these entities

When users ask to perform operations, use the appropriate tools. Be helpful and explain what you're doing.
Provide clear, concise responses about the operations performed.

Important: All operations require the user to have provided their Avni API key which will be available to the tools automatically.
"""


def create_server():
    """Create and configure the MCP server with Avni tools."""
    mcp = FastMCP(
        name="Avni_MCP_Server", instructions=server_instructions, stateless_http=True
    )

    # Register all Avni tool modules
    register_organization_tools(mcp)
    register_location_tools(mcp)
    register_user_tools(mcp)
    register_program_tools(mcp)

    @mcp.custom_route("/health", methods=["GET"])
    async def health_check(request: Request):
        """Health check endpoint for monitoring."""
        return JSONResponse({"status": "healthy", "service": "Avni MCP Server"})

    @mcp.custom_route("/chat", methods=["OPTIONS"])
    async def chat_options(request: Request):
        """Handle CORS preflight requests for /chat endpoint."""
        return JSONResponse({"status": "ok"})

    @mcp.custom_route("/chat", methods=["POST"])
    async def chat_endpoint(request: Request):
        """Chat endpoint that integrates with OpenAI Responses API."""
        return await process_chat_request(request)

    return mcp


async def process_chat_request(request: Request) -> JSONResponse:
    """Process a complete chat request from parsing to response.

    Args:
        request: The incoming HTTP request

    Returns:
        JSONResponse with the chat result or error
    """
    try:
        # Parse and validate request
        body = await request.json()
        message = body.get("message")

        if not message:
            return create_error_response("Message is required", 400)

        # Validate authentication
        auth_token = request.headers.get("AUTH-TOKEN")
        if not auth_token:
            return create_error_response("AUTH-TOKEN header is required", 401)

        # Validate environment configuration
        if not AVNI_MCP_SERVER_URL:
            return create_error_response(
                "AVNI_MCP_SERVER_URL environment variable not set", 500
            )

        # Configure and call OpenAI Responses API with MCP integration
        mcp_tool: Mcp = {
            "type": "mcp",
            "server_label": "Avni_MCP_Server",
            "server_url": AVNI_MCP_SERVER_URL,
            "require_approval": "never",
        }

        response = openai_client.responses.create(
            model="gpt-4o",
            tools=[mcp_tool],
            input=message,
            instructions=f"Use this auth token when calling MCP tools: {auth_token}",
        )

        return create_success_response({"response": response.output_text})

    except Exception as e:
        logger.error(f"Chat request processing error: {e}")
        return create_error_response("Internal server error", 500)


# Verify OpenAI client is initialized
if not openai_client:
    logger.error(
        "OpenAI API key not found. Please set OPENAI_API_KEY environment variable."
    )
    raise ValueError("OpenAI API key is required")

logger.info("Initializing Avni MCP Server for production deployment...")

# Create the MCP server
mcp_server = create_server()

# Create ASGI application with proper HTTP middleware
app = mcp_server.http_app(middleware=[create_cors_middleware()])

logger.info("ASGI application created successfully")
logger.info("Deploy with: uvicorn main:app --host 0.0.0.0 --port 8023")


def main():
    """Main function for direct execution (development mode)."""
    port = int(os.getenv("PORT", 8023))
    logger.info(f"Starting Avni MCP server on 0.0.0.0:{port}")
    logger.info("Server will be accessible via HTTP transport")

    try:
        # Use modern HTTP transport with proper CORS middleware
        mcp_server.run(
            transport="http",
            host="0.0.0.0",
            port=port,
            middleware=[create_cors_middleware()],
        )
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Server error: {e}")
        raise


if __name__ == "__main__":
    main()
