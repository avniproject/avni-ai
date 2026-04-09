"""
Extraction handlers — server-side Excel SRS parsing.

Endpoint:
  POST /parse-srs-file  — multipart/form-data with conversation_id + file field
"""

from __future__ import annotations

import logging
import os
import tempfile

from starlette.requests import Request
from starlette.responses import JSONResponse

from ..bundle.scoping_parser import consolidate_and_audit
from .entity_handlers import get_entity_store

logger = logging.getLogger(__name__)


async def handle_parse_srs_file(request: Request) -> JSONResponse:
    """
    POST /parse-srs-file  (multipart/form-data)
    Fields: conversation_id (text), file (file upload)
    Runs scoping_parser on the uploaded file, stores entities under conversation_id.
    Returns:
      { ok: true, summary: {...}, warnings: [...], errors: [...], coverage: {...} }
      { ok: false, error: "..." }  on parse failure (HTTP 200 so Dify can inspect ok flag)
    """
    try:
        form = await request.form()
    except Exception:
        return JSONResponse(
            {"ok": False, "error": "Expected multipart/form-data"}, status_code=400
        )

    conversation_id = form.get("conversation_id")
    upload = form.get("file")

    if not conversation_id:
        return JSONResponse(
            {"ok": False, "error": "Missing 'conversation_id' form field"},
            status_code=400,
        )
    if upload is None:
        return JSONResponse(
            {"ok": False, "error": "Missing 'file' form field"}, status_code=400
        )

    filename = getattr(upload, "filename", None) or "document.xlsx"
    raw = await upload.read()

    tmp_path = None
    try:
        suffix = os.path.splitext(filename)[1] or ".xlsx"
        with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
            tmp.write(raw)
            tmp_path = tmp.name

        result = consolidate_and_audit([tmp_path])
        entities = result["entities"]
        audit = result["audit"]
        get_entity_store().put(conversation_id, entities)

        logger.info(
            "parse-srs-file: stored entities for conversation_id=%s, counts=%s",
            conversation_id,
            audit["entity_counts"],
        )
        return JSONResponse(
            {
                "ok": True,
                "summary": audit["entity_counts"],
                "warnings": audit["warnings"],
                "errors": audit["errors"],
                "coverage": audit["coverage"],
            }
        )

    except Exception as exc:
        logger.warning(
            "parse-srs-file: parse failed for conversation_id=%s: %s",
            conversation_id,
            exc,
        )
        return JSONResponse({"ok": False, "error": str(exc)})

    finally:
        if tmp_path and os.path.exists(tmp_path):
            try:
                os.unlink(tmp_path)
            except OSError:
                pass
