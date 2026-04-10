"""HTTP handler for the Python Playground endpoint."""

import json
import logging
import os
from pathlib import Path
from starlette.requests import Request
from starlette.responses import JSONResponse

from ..playground.executor import PlaygroundExecutor

logger = logging.getLogger(__name__)

_executor = PlaygroundExecutor()

_MAX_INLINE = (
    2000  # chars of stdout/stderr returned inline; rest readable via read_silo_file
)


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

    # Build input_files dict
    input_files: dict = body.get("input_files") or {}

    # context dict -> _context.json in silo
    context = body.get("context")
    if context and isinstance(context, dict):
        input_files["_context.json"] = json.dumps(context)

    # input_bundle_files: copy named files from the stored bundle ZIP into the silo
    # before execution so scripts can open them as local files without token cost.
    input_bundle_files: list = body.get("input_bundle_files") or []
    if input_bundle_files:
        from ..handlers.bundle_handlers import get_bundle_store
        import base64
        import io
        import zipfile

        store = get_bundle_store()
        entry = store.get(conversation_id)
        if entry and entry.get("zip_b64"):
            zip_bytes = base64.b64decode(entry["zip_b64"])
            with zipfile.ZipFile(io.BytesIO(zip_bytes)) as zf:
                names_in_zip = zf.namelist()
                for fname in input_bundle_files:
                    # Support "concepts.json" or "forms/MyForm.json"
                    match = next(
                        (
                            n
                            for n in names_in_zip
                            if n == fname or n.endswith("/" + fname)
                        ),
                        None,
                    )
                    if match:
                        input_files[Path(fname).name] = zf.read(match).decode("utf-8")
                    else:
                        logger.warning(
                            "input_bundle_files: %s not found in bundle", fname
                        )
        else:
            logger.warning(
                "input_bundle_files requested but no bundle found for %s",
                conversation_id,
            )

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

    # Truncate stdout/stderr inline to protect agent context window.
    # Full content is in silo files; use read_silo_file to page through them.
    stdout = result.get("stdout", "")
    stderr = result.get("stderr", "")
    if len(stdout) > _MAX_INLINE:
        result["stdout"] = (
            stdout[:_MAX_INLINE]
            + "\n...[truncated — use read_silo_file to read full output]"
        )
        result["stdout_total_chars"] = len(stdout)
    if len(stderr) > _MAX_INLINE:
        result["stderr"] = stderr[:_MAX_INLINE] + "\n...[truncated]"

    status_code = 200 if result["success"] else 422
    return JSONResponse(result, status_code=status_code)


async def handle_read_silo_file(request: Request) -> JSONResponse:
    """GET /silo-file — read a file written by execute_python, in chunks."""
    conversation_id = request.query_params.get("conversation_id")
    filename = request.query_params.get("filename")
    if not conversation_id:
        return JSONResponse({"error": "'conversation_id' is required"}, status_code=400)
    if not filename:
        return JSONResponse({"error": "'filename' is required"}, status_code=400)

    try:
        offset = int(request.query_params.get("offset", 0))
        limit = int(request.query_params.get("limit", 4000))
    except ValueError:
        return JSONResponse(
            {"error": "offset and limit must be integers"}, status_code=400
        )

    limit = min(limit, 8000)  # cap to protect context window

    silo = _executor.get_or_create_silo(conversation_id)
    safe_name = Path(filename).name  # prevent path traversal
    fpath = silo / safe_name

    if not fpath.exists():
        return JSONResponse(
            {"error": f"File '{safe_name}' not found in silo"}, status_code=404
        )

    try:
        content = fpath.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return JSONResponse(
            {"error": f"File '{safe_name}' is binary — not readable as text"},
            status_code=422,
        )

    total = len(content)
    chunk = content[offset : offset + limit]
    return JSONResponse(
        {
            "filename": safe_name,
            "content": chunk,
            "offset": offset,
            "limit": limit,
            "chars_returned": len(chunk),
            "total_chars": total,
            "has_more": (offset + limit) < total,
        }
    )
