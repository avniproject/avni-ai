"""
Extraction handlers — server-side SRS parsing.

Endpoints:
  POST /parse-srs-file   — decode base64 Excel, parse via scoping_parser, store entities
  POST /parse-srs-files  — accept multiple base64 files, consolidate, audit, store entities
"""

from __future__ import annotations

import base64
import logging
import os
import tempfile

from starlette.requests import Request
from starlette.responses import JSONResponse

from ..bundle.scoping_parser import parse_scoping_doc, parse_scoping_docs, consolidate_and_audit
from .entity_handlers import get_entity_store

logger = logging.getLogger(__name__)


async def handle_parse_srs_file(request: Request) -> JSONResponse:
    """
    POST /parse-srs-file
    Body: { "conversation_id": "...", "file_b64": "...", "filename": "..." }
    Decodes a single base64-encoded Excel file, parses via scoping_parser,
    stores entities under conversation_id.
    Returns:
      { ok: true, summary: {...} }
      { ok: false, error: "..." }
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

        entity_spec = parse_scoping_doc(tmp_path)
        entities = entity_spec.to_entities_dict()
        get_entity_store().put(conversation_id, entities)

        summary = {
            "forms": len(entities.get("forms", [])),
            "encounter_types": len(entities.get("encounter_types", [])),
            "subject_types": len(entities.get("subject_types", [])),
            "programs": len(entities.get("programs", [])),
            "address_levels": len(entities.get("address_levels", [])),
        }
        logger.info(
            "parse-srs-file: stored entities for conversation_id=%s, summary=%s",
            conversation_id,
            summary,
        )
        return JSONResponse({"ok": True, "summary": summary})

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


async def handle_parse_srs_files(request: Request) -> JSONResponse:
    """
    POST /parse-srs-files
    Body: { "conversation_id": "...", "org_name": "...",
            "files": [{"file_b64": "...", "filename": "..."}, ...] }
       OR: { "conversation_id": "...", "org_name": "...",
            "file_paths": ["/path/to/file1.xlsx", ...] }

    Multi-file version: accepts multiple base64 files or server-side file paths.
    Consolidates all files, runs audit, stores entities and returns spec YAML.

    Returns:
      { ok: true, spec_yaml: "...", audit: {...}, entities: {...} }
      { ok: false, error: "..." }
    """
    try:
        body = await request.json()
    except Exception:
        return JSONResponse(
            {"ok": False, "error": "Invalid JSON body"}, status_code=400
        )

    conversation_id = body.get("conversation_id")
    org_name = body.get("org_name", "")
    files = body.get("files", [])
    file_paths = body.get("file_paths", [])

    if not conversation_id:
        return JSONResponse(
            {"ok": False, "error": "Missing 'conversation_id'"}, status_code=400
        )
    if not files and not file_paths:
        return JSONResponse(
            {"ok": False, "error": "Provide 'files' (base64) or 'file_paths' (server paths)"},
            status_code=400,
        )

    tmp_paths: list[str] = []
    try:
        # Decode base64 files to temp files
        for f in files:
            file_b64 = f.get("file_b64", "")
            filename = f.get("filename", "document.xlsx")
            if not file_b64:
                continue
            try:
                raw = base64.b64decode(file_b64)
            except Exception as exc:
                return JSONResponse(
                    {"ok": False, "error": f"base64 decode failed for {filename}: {exc}"}
                )
            suffix = os.path.splitext(filename)[1] or ".xlsx"
            with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
                tmp.write(raw)
                tmp_paths.append(tmp.name)

        # Combine temp paths with any server-side file paths
        all_paths = tmp_paths + list(file_paths)

        if not all_paths:
            return JSONResponse(
                {"ok": False, "error": "No valid files to parse"}, status_code=400
            )

        result = consolidate_and_audit(all_paths, org_name=org_name)

        # Store entities for subsequent pipeline calls
        get_entity_store().put(conversation_id, result["entities"])

        logger.info(
            "parse-srs-files: stored entities for conversation_id=%s, counts=%s",
            conversation_id,
            result["audit"]["entity_counts"],
        )

        return JSONResponse({
            "ok": True,
            "spec_yaml": result["spec_yaml"],
            "audit": result["audit"],
            "entities": result["entities"],
        })

    except FileNotFoundError as exc:
        return JSONResponse({"ok": False, "error": str(exc)}, status_code=404)

    except Exception as exc:
        logger.exception(
            "parse-srs-files: failed for conversation_id=%s", conversation_id
        )
        return JSONResponse({"ok": False, "error": str(exc)})

    finally:
        for p in tmp_paths:
            try:
                os.unlink(p)
            except OSError:
                pass
