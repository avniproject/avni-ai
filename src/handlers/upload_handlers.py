"""
HTTP handlers for bundle upload to Avni server.
Endpoints: POST /upload-bundle, GET /upload-status/{task_id}
"""

from __future__ import annotations

import asyncio
import base64
import logging
from typing import Any, Dict

from starlette.requests import Request
from starlette.responses import JSONResponse

from ..services.task_manager import task_manager
from ..utils.env import AVNI_BASE_URL

logger = logging.getLogger(__name__)

# Spring Batch statuses that indicate the job is still running
_AVNI_IN_PROGRESS_STATUSES = {"STARTING", "STARTED", "STOPPING"}


async def _upload_processor(
    config_data: Dict[str, Any],
    auth_token: str,
    task_id: str,
    progress_callback,
) -> Dict[str, Any]:
    """Async processor that uploads a bundle ZIP to Avni server and polls job status.

    Avni's POST /import/new returns `true` immediately; the actual bundle import
    runs as an async Spring Batch job.  We poll GET /import/status until the job
    completes, then fetch GET /import/errorfile if errors are reported.
    """
    import httpx

    zip_bytes = config_data["zip_bytes"]
    base_url = config_data.get("base_url", AVNI_BASE_URL).rstrip("/")
    headers = {"AUTH-TOKEN": auth_token}

    progress_callback("Uploading bundle to Avni server...")

    async with httpx.AsyncClient(timeout=120.0) as client:
        response = await client.post(
            f"{base_url}/import/new",
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
        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as e:
            raise RuntimeError(
                f"Avni upload rejected: HTTP {e.response.status_code} — {e.response.text[:500]}"
            ) from e

    progress_callback("Bundle accepted by server, waiting for import to complete...")

    # Poll GET /import/status (most-recent first) until our job finishes.
    # The server returns a Spring Batch Page<JobStatus>; we take the most recent
    # metadataZip job (type field may be "metaDataZip" on the server).
    job_uuid: str | None = None
    job_status: str = ""
    exit_status: str = ""
    skipped: int = 0

    for attempt in range(40):  # up to ~120 s (40 × 3 s)
        await asyncio.sleep(3)
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                status_resp = await client.get(
                    f"{base_url}/import/status",
                    headers=headers,
                    params={"page": 0, "size": 5, "sort": "createTime,desc"},
                )
            if status_resp.status_code != 200:
                logger.warning("import/status returned %s", status_resp.status_code)
                continue
            page = status_resp.json()
            jobs = page.get("content", [])
        except Exception as exc:
            logger.warning("import/status poll failed (attempt %d): %s", attempt, exc)
            continue

        # Find the most-recent metadataZip job
        our_job = next(
            (
                j
                for j in jobs
                if j.get("type") in ("metaDataZip", "metadataZip")
                or j.get("fileName", "").endswith(".zip")
            ),
            jobs[0] if jobs else None,
        )
        if not our_job:
            continue

        job_uuid = our_job.get("uuid")
        job_status = our_job.get("status", "")
        exit_status = our_job.get("exitStatus", "")
        skipped = our_job.get("skipped", 0)

        if job_status not in _AVNI_IN_PROGRESS_STATUSES:
            break  # Job finished (COMPLETED, FAILED, STOPPED, etc.)

    # Determine if the completed job had errors
    combined = (job_status + " " + exit_status).lower()
    has_errors = "error" in combined or job_status == "FAILED" or skipped != 0

    if has_errors:
        error_content = ""
        if job_uuid:
            try:
                async with httpx.AsyncClient(timeout=30.0) as client:
                    err_resp = await client.get(
                        f"{base_url}/import/errorfile",
                        headers=headers,
                        params={"jobUuid": job_uuid},
                    )
                    if err_resp.status_code == 200:
                        error_content = err_resp.text[:15000]
                        logger.info(
                            "Fetched error file for job %s (%d chars)",
                            job_uuid,
                            len(error_content),
                        )
            except Exception as exc:
                logger.warning(
                    "Failed to fetch error file for job %s: %s", job_uuid, exc
                )

        raise RuntimeError(
            f"Avni import completed with errors "
            f"(jobUuid={job_uuid}, status={job_status}, exitStatus={exit_status}, skipped={skipped}):\n"
            f"{error_content}"
        )

    progress_callback("Bundle uploaded successfully")
    return {
        "upload_response": True,
        "job_uuid": job_uuid,
        "job_status": job_status,
        "exit_status": exit_status,
    }


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
    GET /upload-status/{task_id}?wait=true
    Returns task status dict.

    When wait=true (default): polls until the task completes or fails (max 60s).
    This ensures the agent gets a definitive result in a single call instead of
    having to poll repeatedly.
    When wait=false: returns current status immediately (legacy behaviour).
    """
    import asyncio

    task_id = request.path_params.get("task_id", "")
    task = task_manager.get_task(task_id)
    if not task:
        return JSONResponse({"error": f"Task {task_id} not found"}, status_code=404)

    wait = request.query_params.get("wait", "true").lower() != "false"
    if wait and task.status in ("pending", "processing"):
        # Poll until complete or timeout (5 min)
        for _ in range(20):
            await asyncio.sleep(15)
            task = task_manager.get_task(task_id)
            if not task or task.status not in ("pending", "processing"):
                break

    if not task:
        return JSONResponse({"error": f"Task {task_id} not found"}, status_code=404)
    return JSONResponse(task.to_dict())
