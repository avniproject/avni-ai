import logging
import os
from typing import Dict, Any, Optional
from dataclasses import dataclass
from starlette.requests import Request
from starlette.responses import JSONResponse

from ..services.task_manager import task_manager
from ..services.enums import TaskStatus

logger = logging.getLogger(__name__)


@dataclass
class ConfigRequestValidation:
    config_data: Optional[Dict[str, Any]] = None
    auth_token: Optional[str] = None
    base_url: Optional[str] = None
    error_message: Optional[str] = None

    @property
    def is_valid(self) -> bool:
        return self.error_message is None


async def validate_config_request(
    request: Request,
) -> ConfigRequestValidation:
    try:
        body = await request.json()
        config_data = body.get("config")
        if not config_data:
            return ConfigRequestValidation(error_message="config object is required")

        org_type = body.get("org_type", "")
        if org_type in ["Production", "UAT"]:
            return ConfigRequestValidation(
                error_message=f"Configuration creation is not supported for {org_type} organization type. Automated configuration creation is only available for Non Prod/UAT organizations."
            )

        config_data["org_type"] = org_type

        if not any(op in config_data for op in ["create", "update", "delete"]):
            return ConfigRequestValidation(
                error_message="config must contain at least one of: create, update, delete"
            )

        auth_token = request.headers.get("avni-auth-token")
        if not auth_token:
            return ConfigRequestValidation(
                error_message="avni-auth-token header is required"
            )

        base_url = os.getenv("AVNI_BASE_URL")

        return ConfigRequestValidation(
            config_data=config_data, auth_token=auth_token, base_url=base_url
        )

    except Exception as e:
        return ConfigRequestValidation(
            error_message=f"Request validation error: {str(e)}"
        )


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
        validation = await validate_config_request(request)
        if not validation.is_valid:
            status_code = 401 if "auth-token" in validation.error_message else 400
            return create_error_response(validation.error_message, status_code)

        logger.info("Starting async CRUD config processing")
        logger.info(f"Operations requested: {list(validation.config_data.keys())}")

        task = task_manager.create_task(
            config_data=validation.config_data, auth_token=validation.auth_token
        )

        task_manager.start_background_task(task.task_id)

        return create_success_response(
            {
                "task_id": task.task_id,
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
    try:
        task = task_manager.get_task(task_id)

        if not task:
            return create_error_response(f"Task {task_id} not found or expired", 404)

        return create_success_response(task.to_dict())

    except Exception as e:
        logger.error(f"Task status error: {e}")
        return create_error_response("Internal server error", 500)
