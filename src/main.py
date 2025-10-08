"""
Avni MCP Server for OpenAI Integration

This server implements the Model Context Protocol (MCP) with Avni health platform
operations designed to work with OpenAI's chat and tool calling features.
"""

import logging
import os

from dotenv import load_dotenv
from fastmcp import FastMCP
from starlette.requests import Request
from starlette.responses import JSONResponse

from .auth import SimpleTokenVerifier
from .handlers import process_chat_request, process_config_request
from src.tools.admin.addressleveltypes import  register_address_level_type_tools
from src.tools.admin.catchments import  register_catchment_tools
from src.tools.admin.locations import  register_location_tools
from src.tools.app_designer.encounters import register_encounter_tools
from src.tools.app_designer.programs import register_program_tools
from src.tools.app_designer.subject_types import register_subject_type_tools
from .utils import create_cors_middleware

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
base_url = os.getenv("AVNI_MCP_SERVER_URL")
AVNI_MCP_SERVER_URL = base_url + "/mcp"

server_instructions = """
You are an AI assistant that helps users (usually management personals of NGOs) interact with the Avni platform for their program data management.

You have access to various tools to:
- Manage locations and catchments
- Create programs, subject types, and encounter types
- List and retrieve information about these entities

When users ask to perform operations, use the appropriate tools. Be helpful and explain what you're doing.
Provide clear, concise responses about the operations performed.

Important: All operations require the user to have provided their Avni API key which will be available to the tools automatically.
"""


def create_server():
    """Starts an mcp server, though we have removed the mcp server tools as we do direct function calling now """

    mcp = FastMCP(
        name="Avni AI Server",
        instructions=server_instructions,
        stateless_http=True,
        auth=SimpleTokenVerifier(),
    )

    register_address_level_type_tools()
    register_catchment_tools()
    register_location_tools()
    register_encounter_tools()
    register_program_tools()
    register_subject_type_tools()

    @mcp.custom_route("/health", methods=["GET"])
    async def health_check(request: Request):
        """
        Health check endpoint for monitoring.
        """
        return JSONResponse({"status": "healthy", "service": "Avni MCP Server"})

    """ /chat endpoint was being used initially when we were not using Dify , we can get rid of this endpoint"""
    @mcp.custom_route("/chat", methods=["OPTIONS"])
    async def chat_options(request: Request):
        """Handle CORS preflight requests for /chat endpoint."""
        return JSONResponse({"status": "ok"})

    @mcp.custom_route("/chat", methods=["POST"])
    async def chat_endpoint(request: Request):
        """Chat endpoint that integrates with OpenAI Responses API."""
        return await process_chat_request(request, OPENAI_API_KEY, server_instructions)

    @mcp.custom_route("/process-config", methods=["POST"])
    async def process_config_endpoint(request: Request):
        return await process_config_request(request, OPENAI_API_KEY)

    return mcp


if not OPENAI_API_KEY:
    logger.error(
        "OpenAI API key not found. Please set OPENAI_API_KEY environment variable."
    )
    raise ValueError("OpenAI API key is required")

logger.info("Initializing Avni MCP Server for production deployment...")

ai_server = create_server()

# Create ASGI application with proper HTTP middleware
app = ai_server.http_app(middleware=[create_cors_middleware()])

logger.info("ASGI application created successfully")
logger.info("Deploy with: uvicorn main:app --host 0.0.0.0 --port 8023")


def main():
    """Main function for direct execution (development mode)."""
    port = int(os.getenv("PORT", 8023))
    logger.info(f"Starting Avni MCP server on 0.0.0.0:{port}")

    try:
        ai_server.run(
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
