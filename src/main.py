import asyncio
import logging
import os

from fastmcp import FastMCP
from starlette.requests import Request
from starlette.responses import JSONResponse

from .handlers.admin_handlers import (
    handle_create_location_type,
    handle_update_location_type,
    handle_delete_location_type,
    handle_get_locations,
    handle_create_location,
    handle_update_location,
    handle_delete_location,
    handle_get_catchments,
    handle_create_catchment,
    handle_update_catchment,
    handle_delete_catchment,
    handle_find_user,
    handle_update_user,
    handle_delete_implementation,
)
from .handlers.bundle_handlers import (
    handle_generate_bundle,
    handle_validate_bundle,
    handle_download_bundle,
    handle_download_bundle_b64,
    handle_patch_bundle,
    handle_get_bundle_files,
    handle_get_bundle_file,
    handle_put_bundle_file,
)
from .handlers.upload_handlers import handle_upload_bundle, handle_upload_status
from .handlers.config_handlers import handle_get_existing_config
from .handlers.entity_handlers import (
    handle_store_entities,
    handle_validate_entities,
    handle_apply_entity_corrections,
    handle_get_entities_section,
    handle_put_entities_section,
    handle_store_srs_text,
    handle_get_srs_text,
)
from .handlers.extraction_handlers import handle_parse_srs_file, handle_parse_srs_files
from .auth_store import handle_store_auth_token
from .handlers.spec_handlers import (
    handle_generate_spec,
    handle_get_spec,
    handle_get_spec_section,
    handle_put_spec_section,
    handle_validate_spec,
    handle_spec_to_entities,
    handle_bundle_to_spec,
)
from .handlers.sandbox_handlers import handle_execute_python
from .handlers.debug_handlers import (
    handle_debug_conversation,
    handle_debug_list_conversations,
    handle_debug_clear_conversation,
)
from .playground.executor import PlaygroundExecutor
from .http import create_cors_middleware

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

_playground_executor = PlaygroundExecutor()


def _create_fastmcp_server() -> FastMCP:
    """Support both FastMCP v2 (constructor kwarg) and v3 (removed kwarg)."""
    try:
        return FastMCP(name="Avni AI Server", stateless_http=True)
    except TypeError as exc:
        if "stateless_http" not in str(exc):
            raise
        return FastMCP(name="Avni AI Server")


def _create_http_app(server: FastMCP):
    """Keep stateless HTTP behavior across FastMCP versions."""
    middleware = [create_cors_middleware()]
    try:
        return server.http_app(middleware=middleware, stateless_http=True)
    except TypeError as exc:
        if "stateless_http" not in str(exc):
            raise
        return server.http_app(middleware=middleware)


def _run_http_server(server: FastMCP, host: str, port: int):
    run_kwargs = {
        "transport": "http",
        "host": host,
        "port": port,
        "middleware": [create_cors_middleware()],
    }
    try:
        server.run(**run_kwargs, stateless_http=True)
    except TypeError as exc:
        if "stateless_http" not in str(exc):
            raise
        server.run(**run_kwargs)


async def create_server():
    server = _create_fastmcp_server()

    # --- Health ---
    @server.custom_route("/health", methods=["GET"])
    async def health_check(request: Request):
        return JSONResponse({"status": "healthy", "service": "Avni AI Server"})

    # --- Location Types ---
    @server.custom_route("/api/location-types", methods=["POST"])
    async def create_location_type_endpoint(request: Request):
        return await handle_create_location_type(request)

    @server.custom_route("/api/location-types/{id}", methods=["PUT"])
    async def update_location_type_endpoint(request: Request):
        return await handle_update_location_type(request)

    @server.custom_route("/api/location-types/{id}", methods=["DELETE"])
    async def delete_location_type_endpoint(request: Request):
        return await handle_delete_location_type(request)

    # --- Locations ---
    @server.custom_route("/api/locations", methods=["GET"])
    async def get_locations_endpoint(request: Request):
        return await handle_get_locations(request)

    @server.custom_route("/api/locations", methods=["POST"])
    async def create_location_endpoint(request: Request):
        return await handle_create_location(request)

    @server.custom_route("/api/locations/{id}", methods=["PUT"])
    async def update_location_endpoint(request: Request):
        return await handle_update_location(request)

    @server.custom_route("/api/locations/{id}", methods=["DELETE"])
    async def delete_location_endpoint(request: Request):
        return await handle_delete_location(request)

    # --- Catchments ---
    @server.custom_route("/api/catchments", methods=["GET"])
    async def get_catchments_endpoint(request: Request):
        return await handle_get_catchments(request)

    @server.custom_route("/api/catchments", methods=["POST"])
    async def create_catchment_endpoint(request: Request):
        return await handle_create_catchment(request)

    @server.custom_route("/api/catchments/{id}", methods=["PUT"])
    async def update_catchment_endpoint(request: Request):
        return await handle_update_catchment(request)

    @server.custom_route("/api/catchments/{id}", methods=["DELETE"])
    async def delete_catchment_endpoint(request: Request):
        return await handle_delete_catchment(request)

    # --- Users ---
    @server.custom_route("/api/users", methods=["GET"])
    async def find_user_endpoint(request: Request):
        return await handle_find_user(request)

    @server.custom_route("/api/users/{id}", methods=["PUT"])
    async def update_user_endpoint(request: Request):
        return await handle_update_user(request)

    # --- Implementation ---
    @server.custom_route("/api/implementation", methods=["DELETE"])
    async def delete_implementation_endpoint(request: Request):
        return await handle_delete_implementation(request)

    # --- Config Fetch ---
    @server.custom_route("/api/existing-config", methods=["GET"])
    async def get_existing_config_endpoint(request: Request):
        return await handle_get_existing_config(request)

    # --- Auth Token Store ---
    @server.custom_route("/store-auth-token", methods=["POST"])
    async def store_auth_token_endpoint(request: Request):
        return await handle_store_auth_token(request)

    # --- SRS Text Store ---
    @server.custom_route("/store-srs-text", methods=["POST"])
    async def store_srs_text_endpoint(request: Request):
        return await handle_store_srs_text(request)

    @server.custom_route("/get-srs-text", methods=["GET"])
    async def get_srs_text_endpoint(request: Request):
        return await handle_get_srs_text(request)

    # --- SRS File Parser ---
    @server.custom_route("/parse-srs-file", methods=["POST"])
    async def parse_srs_file_endpoint(request: Request):
        return await handle_parse_srs_file(request)

    @server.custom_route("/parse-srs-files", methods=["POST"])
    async def parse_srs_files_endpoint(request: Request):
        return await handle_parse_srs_files(request)

    # --- Entity Validation ---
    @server.custom_route("/store-entities", methods=["POST"])
    async def store_entities_endpoint(request: Request):
        return await handle_store_entities(request)

    @server.custom_route("/validate-entities", methods=["POST"])
    async def validate_entities_endpoint(request: Request):
        return await handle_validate_entities(request)

    @server.custom_route("/apply-entity-corrections", methods=["POST"])
    async def apply_entity_corrections_endpoint(request: Request):
        return await handle_apply_entity_corrections(request)

    # --- Spec Stage ---
    @server.custom_route("/generate-spec", methods=["POST"])
    async def generate_spec_endpoint(request: Request):
        return await handle_generate_spec(request)

    @server.custom_route("/get-spec", methods=["GET"])
    async def get_spec_endpoint(request: Request):
        return await handle_get_spec(request)

    @server.custom_route("/spec-section", methods=["GET"])
    async def get_spec_section_endpoint(request: Request):
        return await handle_get_spec_section(request)

    @server.custom_route("/spec-section", methods=["PUT"])
    async def put_spec_section_endpoint(request: Request):
        return await handle_put_spec_section(request)

    @server.custom_route("/validate-spec", methods=["POST"])
    async def validate_spec_endpoint(request: Request):
        return await handle_validate_spec(request)

    @server.custom_route("/spec-to-entities", methods=["POST"])
    async def spec_to_entities_endpoint(request: Request):
        return await handle_spec_to_entities(request)

    @server.custom_route("/bundle-to-spec", methods=["POST"])
    async def bundle_to_spec_endpoint(request: Request):
        return await handle_bundle_to_spec(request)

    # --- Bundle Generation ---
    @server.custom_route("/generate-bundle", methods=["POST"])
    async def generate_bundle_endpoint(request: Request):
        return await handle_generate_bundle(request)

    @server.custom_route("/validate-bundle", methods=["POST"])
    async def validate_bundle_endpoint(request: Request):
        return await handle_validate_bundle(request)

    @server.custom_route("/download-bundle", methods=["GET"])
    async def download_bundle_endpoint(request: Request):
        return await handle_download_bundle(request)

    @server.custom_route("/download-bundle-b64", methods=["GET"])
    async def download_bundle_b64_endpoint(request: Request):
        return await handle_download_bundle_b64(request)

    @server.custom_route("/patch-bundle", methods=["POST"])
    async def patch_bundle_endpoint(request: Request):
        return await handle_patch_bundle(request)

    # --- Entity Section Access ---
    @server.custom_route("/entities-section", methods=["GET"])
    async def get_entities_section_endpoint(request: Request):
        return await handle_get_entities_section(request)

    @server.custom_route("/entities-section", methods=["PUT"])
    async def put_entities_section_endpoint(request: Request):
        return await handle_put_entities_section(request)

    # --- Bundle File Inspection ---
    @server.custom_route("/bundle-files", methods=["GET"])
    async def get_bundle_files_endpoint(request: Request):
        return await handle_get_bundle_files(request)

    @server.custom_route("/bundle-file", methods=["GET"])
    async def get_bundle_file_endpoint(request: Request):
        return await handle_get_bundle_file(request)

    @server.custom_route("/bundle-file", methods=["PUT"])
    async def put_bundle_file_endpoint(request: Request):
        return await handle_put_bundle_file(request)

    # --- Bundle Upload ---
    @server.custom_route("/upload-bundle", methods=["POST"])
    async def upload_bundle_endpoint(request: Request):
        return await handle_upload_bundle(request)

    @server.custom_route("/upload-status/{task_id}", methods=["GET"])
    async def upload_status_endpoint(request: Request):
        return await handle_upload_status(request)

    # --- Python Playground ---
    @server.custom_route("/execute-python", methods=["POST"])
    async def execute_python_endpoint(request: Request):
        return await handle_execute_python(request)

    # --- Debug Endpoints ---
    @server.custom_route("/debug/conversation/{conversation_id}", methods=["GET"])
    async def debug_conversation_endpoint(request: Request):
        return await handle_debug_conversation(request)

    @server.custom_route("/debug/conversations", methods=["GET"])
    async def debug_list_conversations_endpoint(request: Request):
        return await handle_debug_list_conversations(request)

    @server.custom_route("/debug/conversation/{conversation_id}", methods=["DELETE"])
    async def debug_clear_conversation_endpoint(request: Request):
        return await handle_debug_clear_conversation(request)

    # Start periodic silo cleanup (every 6 hours)
    asyncio.create_task(_periodic_silo_cleanup())

    return server


async def _periodic_silo_cleanup():
    """Delete playground conversation silos older than TTL."""
    while True:
        try:
            await asyncio.sleep(6 * 3600)
            removed = _playground_executor.cleanup_stale_silos()
            if removed > 0:
                logger.info(f"Silo cleanup removed {removed} stale silo(s)")
        except Exception as e:
            logger.error(f"Silo cleanup error: {e}")


logger.info("Initializing Avni AI Server...")


async def initialize_server():
    return await create_server()


ai_server = asyncio.run(initialize_server())

app = _create_http_app(ai_server)

logger.info("ASGI application created successfully")


def main():
    port = int(os.getenv("PORT", 8023))
    logger.info(f"Starting Avni AI server on 0.0.0.0:{port}")

    try:
        _run_http_server(ai_server, host="0.0.0.0", port=port)
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Server error: {e}")
        raise


if __name__ == "__main__":
    main()
