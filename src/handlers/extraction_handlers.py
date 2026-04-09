"""
Extraction handlers — server-side Excel SRS parsing.

Endpoint:
  POST /parse-srs-file  — decode base64 Excel, parse via scoping_parser, store entities
"""

from __future__ import annotations

import base64
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
    POST /parse-srs-file
    Body: { "conversation_id": "...", "file_b64": "...", "filename": "..." }
    Decodes the base64-encoded Excel file, runs scoping_parser, stores the resulting
    entities in the entity store under conversation_id.
    Returns:
      { ok: true, summary: {forms, encounter_types, subject_types, programs, address_levels} }
      { ok: false, error: "..." }  on parse failure (HTTP 200 so Dify can inspect ok flag)
    """
    try:
        body = await request.json()
    except Exception:
        return JSONResponse(
            {"ok": False, "error": "Invalid JSON body"}, status_code=400
        )

    conversation_id = body.get("conversation_id")
    file_b64 = body.get("file_b64", "")
    filename = body.get("filename", "document.xlsx")

    if not conversation_id:
        return JSONResponse(
            {"ok": False, "error": "Missing 'conversation_id'"}, status_code=400
        )
    if not file_b64:
        return JSONResponse(
            {"ok": False, "error": "Missing 'file_b64'"}, status_code=400
        )

    tmp_path = None
    try:
        raw = base64.b64decode(file_b64)
    except Exception as exc:
        return JSONResponse({"ok": False, "error": f"base64 decode failed: {exc}"})

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
        return JSONResponse({
            "ok": True,
            "summary": audit["entity_counts"],
            "warnings": audit["warnings"],
            "errors": audit["errors"],
            "coverage": audit["coverage"],
        })

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
