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

from context import set_auth_token

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
AVNI_MCP_SERVER_URL = os.getenv("AVNI_MCP_SERVER_URL")

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

    # Initialize the FastMCP server
    mcp = FastMCP(name="Avni_MCP_Server", instructions=server_instructions)

    # Register all Avni tool modules
    register_organization_tools(mcp)
    register_location_tools(mcp)
    register_user_tools(mcp)
    register_program_tools(mcp)

    # Add health check endpoint
    @mcp.custom_route("/health", methods=["GET"])
    async def health_check(request: Request):
        """Health check endpoint for monitoring."""
        return JSONResponse({"status": "healthy", "service": "Avni MCP Server"})

    # Add chat endpoint for OpenAI Responses API integration
    @mcp.custom_route("/chat", methods=["POST"])
    async def chat_endpoint(request: Request):
        """Chat endpoint that integrates with OpenAI Responses API."""
        try:
            # Parse request body
            body = await request.json()
            message = body.get("message", "")
            
            if not message:
                return JSONResponse(
                    {"error": "Message is required"}, 
                    status_code=400
                )

            # Extract auth-token from request headers
            auth_token = request.headers.get("auth-token")
            if not auth_token:
                return JSONResponse(
                    {"error": "auth-token header is required"}, 
                    status_code=401
                )

            # Set the auth token in context for tools to use
            set_auth_token(auth_token)

            # Get MCP server URL from environment variable
            if not AVNI_MCP_SERVER_URL:
                return JSONResponse(
                    {"error": "AVNI_MCP_SERVER_URL environment variable not set"}, 
                    status_code=500
                )

            # Call OpenAI Responses API with MCP integration
            mcp_tool: Mcp = {
                "type": "mcp",
                "server_label": "Avni_MCP_Server",
                "server_url": AVNI_MCP_SERVER_URL,
                "require_approval": "never"
            }
            
            response = openai_client.responses.create(
                model="gpt-4o",
                tools=[mcp_tool],
                input=message
            )

            return JSONResponse({
                "response": response.output_text
            })

        except Exception as e:
            logger.error(f"Chat endpoint error: {e}")
            return JSONResponse(
                {"error": "Internal server error"},
                status_code=500
            )

    return mcp


def main():
    """Main function to start the MCP server."""
    # Verify OpenAI client is initialized
    if not openai_client:
        logger.error(
            "OpenAI API key not found. Please set OPENAI_API_KEY environment variable."
        )
        raise ValueError("OpenAI API key is required")

    logger.info("Initializing Avni MCP Server...")

    # Create the MCP server
    server = create_server()

    # Configure and start the server
    port = int(os.getenv("PORT", 8023))
    logger.info(f"Starting Avni MCP server on 0.0.0.0:{port}")
    logger.info("Server will be accessible via SSE transport")

    try:
        # Use FastMCP's built-in run method with SSE transport
        server.run(transport="sse", host="0.0.0.0", port=port)
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Server error: {e}")
        raise


if __name__ == "__main__":
    main()
