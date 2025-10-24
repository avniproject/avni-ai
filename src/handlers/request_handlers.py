import logging
import os
from typing import Dict, Any, Optional, Tuple
from starlette.requests import Request
from starlette.responses import JSONResponse

from ..core.task_manager import task_manager
from ..core.enums import TaskStatus

logger = logging.getLogger(__name__)


async def validate_config_request(
    request: Request,
) -> Tuple[Optional[Dict[str, Any]], Optional[str], Optional[str], Optional[str]]:
    """
    Validate the config request and extract required data.

    Args:
        request: The incoming request object

    Returns:
        Tuple of (config_data, auth_token, base_url, error_message)
        - Success: (config_data, auth_token, base_url, None)
        - Error: (None, None, None, error_message)
    """
    try:
        # Parse request body
        body = await request.json()
        config_data = body.get("config")
        if not config_data:
            return None, None, None, "config object is required"

        # Validate that config has at least one operation
        if not any(op in config_data for op in ["create", "update", "delete"]):
            return (
                None,
                None,
                None,
                "config must contain at least one of: create, update, delete",
            )

        # Get auth token from header
        auth_token = request.headers.get("avni-auth-token")
        if not auth_token:
            return None, None, None, "avni-auth-token header is required"

        # Extract base URL with priority: query > header > env > default
        base_url = os.getenv("AVNI_BASE_URL").rstrip("/")

        return config_data, auth_token, base_url, None

    except Exception as e:
        return None, None, None, f"Request validation error: {str(e)}"


def create_error_response(message: str, status_code: int = 400) -> JSONResponse:
    return JSONResponse({"error": message}, status_code=status_code)


def create_success_response(data: dict) -> JSONResponse:
    return JSONResponse(data)


async def process_config_async_request(request: Request) -> JSONResponse:
    """
    Start async configuration processing and return task ID immediately.

     Expected headers:
    - avni-auth-token: Required authentication token for Avni API

    Expected body:
    {
        "config": {
            "create": {
                "addressLevelTypes": [...],
                "locations": [...],
                "catchments": [...],
                "subjectTypes": [...],
                "programs": [...],
                "encounterTypes": [...]
            },
            "update": {
                "addressLevelTypes": [...],
                "locations": [...],
                "catchments": [...],
                "subjectTypes": [...],
                "programs": [...],
                "encounterTypes": [...]
            },
            "delete": {
                "addressLevelTypes": [...],
                "locations": [...],
                "catchments": [...],
                "subjectTypes": [...],
                "programs": [...],
                "encounterTypes": [...]
            }
        }
    }


    Use /process-config-status/{task_id} to check progress.
    """
    try:
        # Validate request and extract data
        config_data, auth_token, base_url, error = await validate_config_request(
            request
        )
        if error:
            status_code = 401 if "auth-token" in error else 400
            return create_error_response(error, status_code)

        logger.info("Starting async CRUD config processing")
        logger.info(f"Operations requested: {list(config_data.keys())}")

        # Create a task
        task_id = task_manager.create_task(
            config_data=config_data, auth_token=auth_token
        )

        # Start background processing
        task_manager.start_background_task(task_id)

        return create_success_response(
            {
                "task_id": task_id,
                "status": TaskStatus.PROCESSING.value,
                "message": "Configuration processing started. Use /process-config-status/{task_id} to check progress.",
            }
        )

    except Exception as e:
        logger.error(f"Async config processing error: {e}")
        import traceback

        logger.error(f"Full traceback: {traceback.format_exc()}")
        return create_error_response("Internal server error", 500)


async def get_task_status(task_id: str) -> JSONResponse:
    """
    Get the status and result of a configuration processing task.
    """
    try:
        task = task_manager.get_task(task_id)

        if not task:
            return create_error_response(f"Task {task_id} not found or expired", 404)

        return create_success_response(task.to_dict())

    except Exception as e:
        logger.error(f"Task status error: {e}")
        return create_error_response("Internal server error", 500)
