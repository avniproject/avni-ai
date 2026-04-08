"""
HTTP handlers for bundle upload to Avni server.
Endpoints: POST /upload-bundle, GET /upload-status/{task_id}
"""

from __future__ import annotations

import base64
import logging
from typing import Any, Dict

from starlette.requests import Request
from starlette.responses import JSONResponse

from ..services.task_manager import task_manager
from ..utils.env import AVNI_BASE_URL

logger = logging.getLogger(__name__)


async def _upload_processor(
    config_data: Dict[str, Any],
    auth_token: str,
    task_id: str,
    progress_callback,
) -> Dict[str, Any]:
    """Async processor that uploads a bundle ZIP to Avni server."""
    import httpx

    zip_bytes = config_data["zip_bytes"]
    base_url = config_data.get("base_url", AVNI_BASE_URL)

    progress_callback("Uploading bundle to Avni server...")

    url = f"{base_url.rstrip('/')}/import/new"
    headers = {"AUTH-TOKEN": auth_token}

    async with httpx.AsyncClient(timeout=120.0) as client:
        response = await client.post(
            url,
            headers=headers,
            files={"file": ("bundle.zip", zip_bytes, "application/zip")},
            data={
                "type": "metadataZip",
                "autoApprove": "true",
                "locationUploadMode": "usingParentLocation",
                "locationHierarchy": "",
                "encounterUploadMode": "CREATE_AND_UPDATE",
            },
        )
        response.raise_for_status()
        result = response.json() if response.content else {}

    progress_callback("Bundle uploaded successfully")
    return {"upload_response": result, "status_code": response.status_code}


async def handle_upload_bundle(request: Request) -> JSONResponse:
    """
    POST /upload-bundle
    Headers: avni-auth-token
    Body: { "bundle_zip_b64": "base64-encoded-zip" }
    Returns: { "task_id": "...", "status": "pending" }
    """
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

    zip_b64 = body.get("bundle_zip_b64")
    if not zip_b64:
        # Try to resolve from server-side bundle store using conversation_id
        conversation_id = body.get("conversation_id")
        if conversation_id:
            from ..handlers.bundle_handlers import get_bundle_store

            stored = get_bundle_store().get(conversation_id)
            if stored:
                zip_b64 = stored["zip_b64"]
                logger.info(
                    "upload-bundle: resolved bundle_zip_b64 from store for conversation_id=%s",
                    conversation_id,
                )
    if not zip_b64:
        return JSONResponse(
            {
                "error": "Missing 'bundle_zip_b64' — pass either bundle_zip_b64 directly or conversation_id after calling generate_bundle"
            },
            status_code=400,
        )

    logger.info(
        "upload-bundle: b64 len=%d first30=%r last10=%r",
        len(zip_b64),
        zip_b64[:30],
        zip_b64[-10:],
    )
    try:
        zip_b64_clean = zip_b64.strip().replace(" ", "+")
        try:
            zip_bytes = base64.b64decode(zip_b64_clean, validate=True)
        except Exception:
            zip_bytes = base64.urlsafe_b64decode(zip_b64_clean + "==")
    except Exception:
        return JSONResponse({"error": "Invalid base64 encoding"}, status_code=400)

    base_url = body.get("base_url", AVNI_BASE_URL)

    # Create task using existing TaskManager
    config_data = {"zip_bytes": zip_bytes, "base_url": base_url}
    task = task_manager.create_task(config_data=config_data, auth_token=auth_token)

    # Start background upload
    task_manager.start_background_task(task.task_id, _upload_processor)

    return JSONResponse({"task_id": task.task_id, "status": "pending"})


async def handle_upload_status(request: Request) -> JSONResponse:
    """
    GET /upload-status/{task_id}
    Returns task status dict.
    """
    task_id = request.path_params.get("task_id", "")
    task = task_manager.get_task(task_id)
    if not task:
        return JSONResponse({"error": f"Task {task_id} not found"}, status_code=404)
    return JSONResponse(task.to_dict())
