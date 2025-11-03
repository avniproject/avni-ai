import logging
import os

from fastmcp import FastMCP
from starlette.requests import Request
from starlette.responses import JSONResponse
from .handlers import (
    process_config_async_request,
    get_task_status,
)
from .tools.admin.addressleveltypes import register_address_level_type_tools
from .tools.admin.catchments import register_catchment_tools
from .tools.admin.locations import register_location_tools
from .tools.admin.users import register_user_tools
from .tools.app_designer.encounters import register_encounter_tools
from .tools.app_designer.programs import register_program_tools
from .tools.app_designer.subject_types import register_subject_type_tools
from .http import create_cors_middleware

from .utils.env import OPENAI_API_KEY

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_server():
    server = FastMCP(name="Avni AI Server", stateless_http=True)

    register_address_level_type_tools()
    register_catchment_tools()
    register_location_tools()
    register_user_tools()
    register_encounter_tools()
    register_program_tools()
    register_subject_type_tools()

    @server.custom_route("/health", methods=["GET"])
    async def health_check(request: Request):
        return JSONResponse({"status": "healthy", "service": "Avni MCP Server"})

    @server.custom_route("/process-config-async", methods=["POST"])
    async def process_config_async_endpoint(request: Request):
        return await process_config_async_request(request)

    @server.custom_route("/process-config-status/{task_id}", methods=["GET"])
    async def get_config_task_status(request: Request):
        task_id = request.path_params["task_id"]
        return await get_task_status(task_id)

    return server


if not OPENAI_API_KEY:
    logger.error(
        "OpenAI API key not found. Please set OPENAI_API_KEY environment variable."
    )
    raise ValueError("OpenAI API key is required")

logger.info("Initializing Avni MCP Server...")

ai_server = create_server()

app = ai_server.http_app(middleware=[create_cors_middleware()])

logger.info("ASGI application created successfully")


def main():
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
