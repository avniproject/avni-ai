import logging
from starlette.requests import Request
from starlette.responses import JSONResponse

from ..core import create_config_processor
from ..core.task_manager import task_manager
from ..core.enums import TaskStatus
from ..utils import create_error_response, create_success_response
from ..utils.request_validation import validate_config_request

logger = logging.getLogger(__name__)


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

        logger.info(
            f"Starting async CRUD config processing with Avni base URL: {base_url}"
        )
        logger.info(f"Operations requested: {list(config_data.keys())}")

        # Create a task
        task_id = task_manager.create_task(
            config_data=config_data, auth_token=auth_token, base_url=base_url
        )

        # Start background processing
        processor = create_config_processor()
        task_manager.start_background_task(task_id, processor)

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
