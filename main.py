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
    mcp = FastMCP(name="Avni MCP Server", instructions=server_instructions)

    # Register all Avni tool modules
    register_organization_tools(mcp)
    register_location_tools(mcp)
    register_user_tools(mcp)
    register_program_tools(mcp)

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
