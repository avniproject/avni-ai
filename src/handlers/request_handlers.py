import logging
from starlette.requests import Request
from starlette.responses import JSONResponse

from ..core import create_config_processor
from ..core.task_manager import task_manager
from ..core.enums import TaskStatus
from ..utils import create_error_response, create_success_response
from ..utils.request_validation import validate_config_request

logger = logging.getLogger(__name__)


async def process_config_request(request: Request) -> JSONResponse:
    """
    Process Avni configuration using LLM with CRUD operations (create, update, delete).

    Expected headers:
    - avni-auth-token: Required authentication token for Avni API
    - avni-base-url: Optional base URL for Avni API

    Expected query parameters:
    - base_url: Optional base URL for Avni API (overrides header)

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

    Args:
        request: The incoming request object
        openai_api_key: OpenAI API key for making requests

    Returns:
        JSONResponse with the config processing result or error
    """
    try:
        config_data, auth_token, base_url, error = await validate_config_request(
            request
        )
        if error:
            status_code = 401 if "auth-token" in error else 400
            return create_error_response(error, status_code)

        logger.info(f"Processing CRUD config with Avni base URL: {base_url}")
        logger.info(f"Operations requested: {list(config_data.keys())}")

        processor = create_config_processor()
        result = await processor.process_config(
            config=config_data, auth_token=auth_token, base_url=base_url
        )

        return create_success_response(result)

    except Exception as e:
        logger.error(f"Config processing error: {e}")
        import traceback

        logger.error(f"Full traceback: {traceback.format_exc()}")
        return create_error_response("Internal server error", 500)


async def process_config_async_request(request: Request) -> JSONResponse:
    """
    Start async configuration processing and return task ID immediately.

    Same request format as /process-config but returns immediately with task ID.
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
    Get status and result of a configuration processing task.
    """
    try:
        task = task_manager.get_task(task_id)

        if not task:
            return create_error_response(f"Task {task_id} not found or expired", 404)

        return create_success_response(task.to_dict())

    except Exception as e:
        logger.error(f"Task status error: {e}")
        return create_error_response("Internal server error", 500)
