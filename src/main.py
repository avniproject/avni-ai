import asyncio
import logging
import os

from fastmcp import FastMCP
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

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
from .handlers.extraction_handlers import handle_parse_srs_file
from .auth_store import handle_store_auth_token
from .handlers.spec_handlers import (
    handle_generate_spec,
    handle_get_spec,
    handle_get_spec_section,
    handle_put_spec_section,
    handle_validate_spec,
    handle_spec_to_entities,
    handle_bundle_to_spec,
    handle_get_spec_format,
)
from .handlers.sandbox_handlers import handle_execute_python, handle_read_silo_file
from .handlers.log_handlers import handle_append_agent_log, handle_get_agent_logs
from .handlers.ambiguity_handlers import (
    handle_resolve_ambiguities,
    handle_get_ambiguities,
)
from .handlers.chat_srs_handlers import (
    handle_init_session,
    handle_update_section,
    handle_build_entities,
)
from .handlers.knowledge_handlers import handle_knowledge_search
from .handlers.form_designer_handlers import (
    handle_generate_form,
    handle_suggest_form_fields,
    handle_generate_skip_logic,
)
from .handlers.rules_handlers import (
    handle_generate_rule,
    handle_validate_rule,
)
from .handlers.reports_handlers import (
    handle_generate_report_cards,
    handle_suggest_dashboard,
)
from .handlers.inspector_handlers import (
    handle_compile_requirements,
    handle_inspect_config,
)
from .handlers.bulk_admin_handlers import (
    handle_bulk_locations,
    handle_bulk_users,
)
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


class _RequestLoggingMiddleware:
    """Logs every non-health API request with conversation_id, method, path, and status."""

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        path = scope.get("path", "")
        method = scope.get("method", "?")

        # Skip health checks and static files
        if path in ("/health", "/favicon.ico") or path.startswith("/sse"):
            await self.app(scope, receive, send)
            return

        # Extract conversation_id from query string
        qs = scope.get("query_string", b"").decode()
        cid = ""
        for part in qs.split("&"):
            if part.startswith("conversation_id="):
                cid = part.split("=", 1)[1][:12]
                break

        status_code = 0

        async def send_wrapper(message):
            nonlocal status_code
            if message["type"] == "http.response.start":
                status_code = message.get("status", 0)
            await send(message)

        try:
            await self.app(scope, receive, send_wrapper)
        finally:
            if status_code >= 400:
                logger.warning(
                    "API %s %s [cid=%s] → %d",
                    method,
                    path,
                    cid or "?",
                    status_code,
                )
            else:
                logger.info(
                    "API %s %s [cid=%s] → %d",
                    method,
                    path,
                    cid or "body",
                    status_code,
                )


class _SafeErrorMiddleware:
    """Catch-all ASGI middleware that ensures every request gets a complete HTTP response.

    Without this, unhandled async exceptions can cause the server to close the TCP
    connection mid-response, producing Dify's 'incomplete chunked read' error.
    """

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        response_started = False

        async def send_wrapper(message):
            nonlocal response_started
            if message["type"] == "http.response.start":
                response_started = True
            await send(message)

        try:
            await self.app(scope, receive, send_wrapper)
        except asyncio.CancelledError:
            # Client disconnected — nothing to send, just let it go silently
            pass
        except Exception as exc:
            logger.exception("Unhandled exception in ASGI app: %s", exc)
            if not response_started:
                # Safe to send a fresh 500 response
                body = b'{"error":"internal server error"}'
                await send(
                    {
                        "type": "http.response.start",
                        "status": 500,
                        "headers": [
                            (b"content-type", b"application/json"),
                            (b"content-length", str(len(body)).encode()),
                        ],
                    }
                )
                await send(
                    {"type": "http.response.body", "body": body, "more_body": False}
                )
            # If response already started, we can't fix the stream — log and swallow


def _create_http_app(server: FastMCP):
    """Keep stateless HTTP behavior across FastMCP versions."""
    middleware = [create_cors_middleware()]
    try:
        base_app = server.http_app(middleware=middleware, stateless_http=True)
    except TypeError as exc:
        if "stateless_http" not in str(exc):
            raise
        base_app = server.http_app(middleware=middleware)
    return _RequestLoggingMiddleware(_SafeErrorMiddleware(base_app))


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

    # --- SRS File Parse ---
    @server.custom_route("/parse-srs-file", methods=["POST"])
    async def parse_srs_file_endpoint(request: Request):
        return await handle_parse_srs_file(request)

    # --- SRS Text Store ---
    @server.custom_route("/store-srs-text", methods=["POST"])
    async def store_srs_text_endpoint(request: Request):
        return await handle_store_srs_text(request)

    @server.custom_route("/get-srs-text", methods=["GET"])
    async def get_srs_text_endpoint(request: Request):
        return await handle_get_srs_text(request)

    # --- Scoping Parser ---
    @server.custom_route("/parse-scoping-docs", methods=["POST"])
    async def parse_scoping_docs_endpoint(request: Request):
        try:
            body = await request.json()
        except Exception:
            return JSONResponse({"error": "Invalid JSON body"}, status_code=400)
        file_paths = body.get("file_paths", [])
        org_name = body.get("org_name", "")
        if not file_paths:
            return JSONResponse({"error": "No file_paths provided"}, status_code=400)
        try:
            from .bundle.scoping_parser import consolidate_and_audit

            result = consolidate_and_audit(file_paths, org_name=org_name)
            return JSONResponse(result)
        except FileNotFoundError as e:
            return JSONResponse({"error": str(e)}, status_code=404)
        except Exception as e:
            logger.exception("parse-scoping-docs failed")
            return JSONResponse({"error": str(e)}, status_code=500)

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

    @server.custom_route("/spec-format", methods=["GET"])
    async def get_spec_format_endpoint(request: Request):
        return await handle_get_spec_format(request)

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

    # --- Bundle ZIP Download (for debugger UI) ---
    @server.custom_route("/download-bundle-zip", methods=["GET"])
    async def download_bundle_zip_endpoint(request: Request):
        import base64
        from .handlers.bundle_handlers import get_bundle_store

        cid = request.query_params.get("conversation_id")
        if not cid:
            return JSONResponse({"error": "Missing conversation_id"}, status_code=400)
        stored = get_bundle_store().get(cid)
        if not stored:
            return JSONResponse({"error": "No stored bundle"}, status_code=404)
        zip_bytes = base64.b64decode(stored["zip_b64"])
        return Response(
            content=zip_bytes,
            status_code=200,
            media_type="application/zip",
            headers={"Content-Disposition": "attachment; filename=bundle.zip"},
        )

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

    @server.custom_route("/silo-file", methods=["GET"])
    async def read_silo_file_endpoint(request: Request):
        return await handle_read_silo_file(request)

    # --- Agent Activity Log ---
    @server.custom_route("/agent-log", methods=["POST"])
    async def append_agent_log_endpoint(request: Request):
        return await handle_append_agent_log(request)

    @server.custom_route("/agent-logs/{conversation_id}", methods=["GET"])
    async def get_agent_logs_endpoint(request: Request):
        return await handle_get_agent_logs(request)

    # --- Knowledge Search ---
    @server.custom_route("/knowledge-search", methods=["POST"])
    async def knowledge_search_endpoint(request: Request):
        return await handle_knowledge_search(request)

    # --- Ambiguity Resolution ---
    @server.custom_route("/resolve-ambiguities", methods=["POST"])
    async def resolve_ambiguities_endpoint(request: Request):
        return await handle_resolve_ambiguities(request)

    @server.custom_route("/get-ambiguities", methods=["GET"])
    async def get_ambiguities_endpoint(request: Request):
        return await handle_get_ambiguities(request)

    # --- Chat SRS Creation ---
    @server.custom_route("/chat-srs/init-session", methods=["POST"])
    async def chat_srs_init_session(request: Request):
        return await handle_init_session(request)

    @server.custom_route("/chat-srs/update-section", methods=["POST"])
    async def chat_srs_update_section(request: Request):
        return await handle_update_section(request)

    @server.custom_route("/chat-srs/build-entities", methods=["POST"])
    async def chat_srs_build_entities(request: Request):
        return await handle_build_entities(request)

    # --- Form Designer ---
    @server.custom_route("/generate-form", methods=["POST"])
    async def generate_form_endpoint(request: Request):
        return await handle_generate_form(request)

    @server.custom_route("/suggest-form-fields", methods=["POST"])
    async def suggest_form_fields_endpoint(request: Request):
        return await handle_suggest_form_fields(request)

    @server.custom_route("/generate-skip-logic", methods=["POST"])
    async def generate_skip_logic_endpoint(request: Request):
        return await handle_generate_skip_logic(request)

    # --- Rules Generation ---
    @server.custom_route("/generate-rule", methods=["POST"])
    async def generate_rule_endpoint(request: Request):
        return await handle_generate_rule(request)

    @server.custom_route("/validate-rule", methods=["POST"])
    async def validate_rule_endpoint(request: Request):
        return await handle_validate_rule(request)

    # --- Reports & Dashboards ---
    @server.custom_route("/generate-report-cards", methods=["POST"])
    async def generate_report_cards_endpoint(request: Request):
        return await handle_generate_report_cards(request)

    @server.custom_route("/suggest-dashboard", methods=["POST"])
    async def suggest_dashboard_endpoint(request: Request):
        return await handle_suggest_dashboard(request)

    # --- Config Inspector ---
    @server.custom_route("/compile-requirements", methods=["POST"])
    async def compile_requirements_endpoint(request: Request):
        return await handle_compile_requirements(request)

    @server.custom_route("/inspect-config", methods=["POST"])
    async def inspect_config_endpoint(request: Request):
        return await handle_inspect_config(request)

    # --- Bulk Admin ---
    @server.custom_route("/api/bulk-locations", methods=["POST"])
    async def bulk_locations_endpoint(request: Request):
        return await handle_bulk_locations(request)

    @server.custom_route("/api/bulk-users", methods=["POST"])
    async def bulk_users_endpoint(request: Request):
        return await handle_bulk_users(request)

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
