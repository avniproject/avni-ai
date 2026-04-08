"""HTTP handler for the Python Playground endpoint."""

import logging
import os
from starlette.requests import Request
from starlette.responses import JSONResponse

from ..playground.executor import PlaygroundExecutor

logger = logging.getLogger(__name__)

_executor = PlaygroundExecutor()


async def handle_execute_python(request: Request) -> JSONResponse:
    """POST /execute-python — run an LLM-generated Python script in a conversation silo."""
    try:
        body = await request.json()
    except Exception:
        return JSONResponse({"error": "Invalid JSON body"}, status_code=400)

    from ..auth_store import resolve_auth_token

    auth_token = resolve_auth_token(request, body)
    if not auth_token:
        return JSONResponse(
            {
                "error": "Missing auth: provide avni-auth-token header or conversation_id"
            },
            status_code=401,
        )

    conversation_id = body.get("conversation_id")
    code = body.get("code")

    if not conversation_id:
        return JSONResponse({"error": "'conversation_id' is required"}, status_code=400)
    if not code:
        return JSONResponse({"error": "'code' is required"}, status_code=400)

    input_files = body.get("input_files")
    timeout = body.get("timeout")
    avni_base_url = os.getenv("AVNI_BASE_URL")

    result = _executor.execute(
        conversation_id=conversation_id,
        code=code,
        input_files=input_files,
        timeout=timeout,
        auth_token=auth_token,
        avni_base_url=avni_base_url,
    )

    status_code = 200 if result["success"] else 422
    return JSONResponse(result, status_code=status_code)
