import logging
import os

from fastmcp import FastMCP
from starlette.requests import Request
from starlette.responses import JSONResponse
from .handlers import (
    process_config_async_request,
    get_task_status,
)
from .handlers.dspy_handlers import (
    analyze_form_request,
    batch_analyze_forms_request,
    predict_field_type_request,
    validate_form_structure_request,
    get_dspy_service_status_request,
    retrain_avni_analyzer_request,
)
from .services.dspy_service import get_dspy_service
from .tools.admin.addressleveltypes import register_address_level_type_tools
from .tools.admin.catchments import register_catchment_tools
from .tools.admin.locations import register_location_tools
from .tools.admin.users import register_user_tools
from .tools.app_designer.encounters import register_encounter_tools
from .tools.app_designer.programs import register_program_tools
from .tools.app_designer.subject_types import register_subject_type_tools
from .tools.implementation.implementations import register_implementation_tools
from .http import create_cors_middleware

from .utils.env import OPENAI_API_KEY

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def create_server():
    server = FastMCP(name="Avni AI Server", stateless_http=True)

    register_address_level_type_tools()
    register_catchment_tools()
    register_location_tools()
    register_user_tools()
    register_encounter_tools()
    register_program_tools()
    register_subject_type_tools()
    register_implementation_tools()

    # Initialize DSPy service with MIPROv2 training at startup
    logger.info("🚀 Initializing DSPy service with MIPROv2 training...")
    try:
        # This will trigger MIPROv2 training
        dspy_service = await get_dspy_service()
        logger.info("✅ DSPy service initialized successfully with MIPROv2")
    except Exception as e:
        logger.error(f"❌ DSPy initialization failed: {e}")
        # Continue startup even if DSPy fails

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

    # DSPy Smart Form Builder endpoints
    @server.custom_route("/dspy/analyze-form", methods=["POST"])
    async def analyze_form_endpoint(request: Request):
        """Analyze a single form using DSPy AI for improvements and suggestions."""
        return await analyze_form_request(request)

    @server.custom_route("/dspy/batch-analyze", methods=["POST"])
    async def batch_analyze_endpoint(request: Request):
        """Analyze multiple forms concurrently using DSPy AI."""
        return await batch_analyze_forms_request(request)

    @server.custom_route("/dspy/predict-field-type", methods=["POST"])
    async def predict_field_type_endpoint(request: Request):
        """Predict optimal field type for a form question using DSPy AI."""
        return await predict_field_type_request(request)

    @server.custom_route("/dspy/validate-form", methods=["POST"])
    async def validate_form_endpoint(request: Request):
        """Validate form structure and identify issues using DSPy AI."""
        return await validate_form_structure_request(request)


    @server.custom_route("/dspy/status", methods=["GET"])
    async def dspy_status_endpoint(request: Request):
        """Get DSPy service status and health information."""
        return await get_dspy_service_status_request(request)

    return server


if not OPENAI_API_KEY:
    logger.error(
        "OpenAI API key not found. Please set OPENAI_API_KEY environment variable."
    )
    raise ValueError("OpenAI API key is required")

logger.info("Initializing Avni MCP Server...")

import asyncio

# Initialize server with DSPy training
async def initialize_server():
    return await create_server()

ai_server = asyncio.run(initialize_server())

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
