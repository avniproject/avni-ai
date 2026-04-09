"""
Extraction handlers — server-side Excel SRS parsing.

Endpoint:
  POST /parse-srs-file  — JSON body: {conversation_id, file_infos: [{url, filename}]}
  The Dify Code node passes pre-signed file URLs. The backend downloads and parses them.
"""

from __future__ import annotations

import logging
import os
import tempfile

import httpx
from starlette.requests import Request
from starlette.responses import JSONResponse

from ..bundle.scoping_parser import consolidate_and_audit
from .entity_handlers import get_entity_store

logger = logging.getLogger(__name__)


async def handle_parse_srs_file(request: Request) -> JSONResponse:
    """
    POST /parse-srs-file
    Body: { "conversation_id": "...", "file_infos": [{"url": "...", "filename": "..."}] }
    Downloads each file from its pre-signed Dify storage URL and runs scoping_parser.
    Returns:
      { ok: true, summary: {...}, warnings: [...], errors: [...], coverage: {...} }
      { ok: false, error: "..." }  on parse failure (HTTP 200 so Dify can inspect ok flag)
    """
    try:
        body = await request.json()
    except Exception:
        return JSONResponse(
            {"ok": False, "error": "Invalid JSON body"}, status_code=400
        )

    conversation_id = body.get("conversation_id")
    file_infos = body.get("file_infos", [])

    if not conversation_id:
        return JSONResponse(
            {"ok": False, "error": "Missing 'conversation_id'"}, status_code=400
        )
    if not file_infos:
        return JSONResponse(
            {"ok": False, "error": "Missing 'file_infos'"}, status_code=400
        )

    tmp_paths: list[str] = []
    try:
        async with httpx.AsyncClient(verify=False, timeout=30) as client:
            for info in file_infos:
                url = info.get("url", "")
                filename = info.get("filename", "document.xlsx")
                if not url:
                    continue
                # URLs are pre-signed — no auth header needed
                resp = await client.get(url)
                resp.raise_for_status()
                suffix = os.path.splitext(filename)[1] or ".xlsx"
                with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
                    tmp.write(resp.content)
                    tmp_paths.append(tmp.name)

        if not tmp_paths:
            return JSONResponse(
                {"ok": False, "error": "No valid file URLs in file_infos"}
            )

        result = consolidate_and_audit(tmp_paths)
        entities = result["entities"]
        audit = result["audit"]
        get_entity_store().put(conversation_id, entities)

        logger.info(
            "parse-srs-file: stored entities for conversation_id=%s, files=%d, counts=%s",
            conversation_id,
            len(tmp_paths),
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
            "parse-srs-file: failed for conversation_id=%s: %s",
            conversation_id,
            exc,
        )
        return JSONResponse({"ok": False, "error": str(exc)})

    finally:
        for path in tmp_paths:
            try:
                os.unlink(path)
            except OSError:
                pass
