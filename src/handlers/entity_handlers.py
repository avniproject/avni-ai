"""
Entity validation and correction handlers.
Replaces Dify code nodes: Ambiguity Checker + Entities Corrector.

Endpoints:
  POST /store-entities       — cache entities by conversation_id (TTL 6h)
  POST /validate-entities    — structural validation of extracted entities
  POST /apply-entity-corrections — apply LLM-generated corrections to entities
"""

from __future__ import annotations

import os
import logging
import time
from typing import Any

from starlette.requests import Request
from starlette.responses import JSONResponse

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# In-memory entity store keyed by conversation_id (TTL = 6 hours)
# Allows agent tool calls to pass only conversation_id instead of full entities
# ---------------------------------------------------------------------------
_ENTITY_STORE_TTL = int(os.getenv("ENTITY_STORE_TTL_HOURS", "6")) * 3600  # seconds


class _EntityStore:
    def __init__(self) -> None:
        self._store: dict[str, tuple[dict, float]] = {}  # id -> (entities, expiry)

    def put(self, conversation_id: str, entities: dict) -> None:
        self._store[conversation_id] = (entities, time.time() + _ENTITY_STORE_TTL)

    def get(self, conversation_id: str) -> dict | None:
        entry = self._store.get(conversation_id)
        if entry is None:
            return None
        entities, expiry = entry
        if time.time() > expiry:
            del self._store[conversation_id]
            return None
        return entities

    def cleanup(self) -> int:
        now = time.time()
        expired = [k for k, (_, exp) in self._store.items() if now > exp]
        for k in expired:
            del self._store[k]
        return len(expired)


_entity_store = _EntityStore()


def get_entity_store() -> _EntityStore:
    """Return the global entity store (used by bundle_handlers for generate_bundle)."""
    return _entity_store


# ---------------------------------------------------------------------------
# SRS text store — keeps raw extracted SRS text server-side so the Dify
# workflow never needs to pass large document blobs through the agent query.
# ---------------------------------------------------------------------------
_SRS_TEXT_STORE_TTL = int(os.getenv("ENTITY_STORE_TTL_HOURS", "6")) * 3600


class _SrsTextStore:
    def __init__(self) -> None:
        self._store: dict[str, tuple[str, float]] = {}

    def put(self, conversation_id: str, text: str) -> None:
        self._store[conversation_id] = (text, time.time() + _SRS_TEXT_STORE_TTL)

    def get(self, conversation_id: str) -> str | None:
        entry = self._store.get(conversation_id)
        if entry is None:
            return None
        text, expiry = entry
        if time.time() > expiry:
            del self._store[conversation_id]
            return None
        return text


_srs_text_store = _SrsTextStore()


async def handle_store_srs_text(request: Request) -> JSONResponse:
    """
    POST /store-srs-text
    Body: { "conversation_id": "...", "srs_text": "..." }
    Caches extracted SRS document text server-side to avoid passing large blobs
    through the agent query field.
    Returns: { "ok": true, "char_count": N }
    """
    try:
        body = await request.json()
    except Exception:
        return JSONResponse({"error": "Invalid JSON body"}, status_code=400)

    conversation_id = body.get("conversation_id")
    srs_text = body.get("srs_text", "")

    if not conversation_id:
        return JSONResponse({"error": "Missing 'conversation_id'"}, status_code=400)
    if not isinstance(srs_text, str):
        return JSONResponse({"error": "'srs_text' must be a string"}, status_code=400)

    _srs_text_store.put(conversation_id, srs_text)
    logger.info(
        "store-srs-text: stored %d chars for conversation_id=%s",
        len(srs_text),
        conversation_id,
    )
    return JSONResponse({"ok": True, "char_count": len(srs_text)})


async def handle_get_srs_text(request: Request) -> JSONResponse:
    """
    GET /get-srs-text?conversation_id=...
    Returns the stored SRS document text for the given conversation.
    Returns: { "srs_text": "...", "char_count": N }
    """
    conversation_id = request.query_params.get("conversation_id")
    if not conversation_id:
        return JSONResponse(
            {"error": "Missing 'conversation_id' query param"}, status_code=400
        )

    # If entities were already stored via parse_srs_file (Excel upload path),
    # signal the agent to skip LLM extraction and go straight to validate_entities.
    if _entity_store.get(conversation_id) is not None:
        return JSONResponse({"already_parsed": True, "text": None})

    text = _srs_text_store.get(conversation_id)
    if text is None:
        return JSONResponse(
            {
                "error": f"No SRS text found for conversation_id={conversation_id}. It may have expired (TTL 6h)."
            },
            status_code=404,
        )
    return JSONResponse({"srs_text": text, "char_count": len(text)})


SECTION_MAP = {
    "subject_type": "subject_types",
    "program": "programs",
    "encounter_type": "encounter_types",
    "address_level": "address_levels",
}


def _fuzzy_match(name: str, known_names: set[str]) -> bool:
    lower = name.strip().lower()
    for known in known_names:
        if lower == known.lower() or lower in known.lower() or known.lower() in lower:
            return True
    return False


def _validate(entities: dict) -> dict:
    """
    Deterministic structural validation of extracted entities.
    Returns {issues, error_count, warning_count, issues_summary, has_errors, has_warnings}.
    """
    st_rows = entities.get("subject_types", [])
    prog_rows = entities.get("programs", [])
    enc_rows = entities.get("encounter_types", [])
    addr_rows = entities.get("address_levels", [])

    subject_type_names = {r["name"] for r in st_rows if r.get("name")}
    program_names = {r["name"] for r in prog_rows if r.get("name")}

    issues: list[dict[str, str]] = []

    # Duplicate subject types
    seen: dict[str, str] = {}
    for r in st_rows:
        key = r.get("name", "").strip().lower()
        if not key:
            continue
        if key in seen:
            issues.append(
                {
                    "severity": "error",
                    "entity_type": "subject_type",
                    "message": f"Duplicate subject type: '{r['name']}'",
                }
            )
        else:
            seen[key] = r["name"]

    # Subject type missing 'type' field
    for r in st_rows:
        if not r.get("type"):
            issues.append(
                {
                    "severity": "warning",
                    "entity_type": "subject_type",
                    "message": f"Subject type '{r.get('name', '?')}' is missing 'type'",
                }
            )

    # Duplicate programs
    seen = {}
    for r in prog_rows:
        key = r.get("name", "").strip().lower()
        if not key:
            continue
        if key in seen:
            issues.append(
                {
                    "severity": "error",
                    "entity_type": "program",
                    "message": f"Duplicate program: '{r['name']}'",
                }
            )
        else:
            seen[key] = r["name"]

    # Program missing or unknown target subject type
    for r in prog_rows:
        target = r.get("target_subject_type", "")
        if not target:
            issues.append(
                {
                    "severity": "warning",
                    "entity_type": "program",
                    "message": f"Program '{r['name']}' is missing target subject type",
                }
            )
        elif not _fuzzy_match(target, subject_type_names):
            issues.append(
                {
                    "severity": "warning",
                    "entity_type": "program",
                    "message": (
                        f"Program '{r['name']}' references subject type "
                        f"'{target}' which doesn't match any defined subject type"
                    ),
                }
            )

    # Duplicate encounter types
    seen = {}
    for r in enc_rows:
        key = r.get("name", "").strip().lower()
        if not key:
            continue
        if key in seen:
            issues.append(
                {
                    "severity": "error",
                    "entity_type": "encounter_type",
                    "message": f"Duplicate encounter type: '{r['name']}'",
                }
            )
        else:
            seen[key] = r["name"]

    # Encounter cross-reference checks
    for r in enc_rows:
        subject = r.get("subject_type", "")
        if not subject:
            issues.append(
                {
                    "severity": "error",
                    "entity_type": "encounter",
                    "message": (
                        f"Encounter '{r['name']}' has no subject_type — "
                        f"every encounter must be linked to a subject type"
                    ),
                }
            )
        elif not _fuzzy_match(subject, subject_type_names):
            issues.append(
                {
                    "severity": "warning",
                    "entity_type": "encounter",
                    "message": (
                        f"Encounter '{r['name']}' references subject type "
                        f"'{subject}' which doesn't match any defined subject type"
                    ),
                }
            )

        if r.get("is_program_encounter"):
            program = r.get("program_name", "")
            if not program:
                issues.append(
                    {
                        "severity": "error",
                        "entity_type": "program_encounter",
                        "message": (
                            f"Program encounter '{r['name']}' has no program_name — "
                            f"which program does this encounter belong to?"
                        ),
                    }
                )
            elif not _fuzzy_match(program, program_names):
                issues.append(
                    {
                        "severity": "warning",
                        "entity_type": "program_encounter",
                        "message": (
                            f"Program encounter '{r['name']}' references "
                            f"program '{program}' which doesn't match any defined program"
                        ),
                    }
                )

    # Address levels
    if not addr_rows:
        issues.append(
            {
                "severity": "warning",
                "entity_type": "location_hierarchy",
                "message": "No location hierarchy found. A default hierarchy will be generated.",
            }
        )

    # Forms cross-reference checks (Phase 5: when forms are explicitly extracted)
    form_rows = entities.get("forms", [])
    if form_rows:
        valid_form_types = {
            "IndividualProfile",
            "ProgramEnrolment",
            "ProgramExit",
            "ProgramEncounter",
            "Encounter",
            "ProgramEncounterCancellation",
        }
        valid_data_types = {
            "Text",
            "Numeric",
            "Coded",
            "Date",
            "DateTime",
            "Duration",
            "PhoneNumber",
            "Audio",
            "Image",
            "Video",
            "File",
            "Location",
            "Subject",
            "GroupAffiliation",
        }
        for form in form_rows:
            if not isinstance(form, dict):
                continue
            ft = form.get("formType", "")
            if ft and ft not in valid_form_types:
                issues.append(
                    {
                        "severity": "warning",
                        "entity_type": "form",
                        "message": f"Form '{form.get('name', '?')}' has unrecognised formType '{ft}'",
                    }
                )
            st_ref = form.get("subjectType", "")
            if st_ref and not _fuzzy_match(st_ref, subject_type_names):
                issues.append(
                    {
                        "severity": "warning",
                        "entity_type": "form",
                        "message": f"Form '{form.get('name', '?')}' references unknown subjectType '{st_ref}'",
                    }
                )
            prog_ref = form.get("program", "")
            prog_names = {r["name"] for r in prog_rows if r.get("name")}
            if prog_ref and not _fuzzy_match(prog_ref, prog_names):
                issues.append(
                    {
                        "severity": "warning",
                        "entity_type": "form",
                        "message": f"Form '{form.get('name', '?')}' references unknown program '{prog_ref}'",
                    }
                )
            for field in form.get("fields", []):
                if not isinstance(field, dict):
                    continue
                dt = field.get("dataType", "")
                if dt and dt not in valid_data_types:
                    issues.append(
                        {
                            "severity": "warning",
                            "entity_type": "form_field",
                            "message": f"Field '{field.get('name', '?')}' in form '{form.get('name', '?')}' has unrecognised dataType '{dt}'",
                        }
                    )
                if dt == "Coded" and not field.get("options"):
                    issues.append(
                        {
                            "severity": "warning",
                            "entity_type": "form_field",
                            "message": f"Coded field '{field.get('name', '?')}' in form '{form.get('name', '?')}' has no options",
                        }
                    )

    error_count = sum(1 for i in issues if i["severity"] == "error")
    warning_count = sum(1 for i in issues if i["severity"] == "warning")

    if not issues:
        issues_summary = "No issues found. All entities look good."
    else:
        lines = []
        errors = [i for i in issues if i["severity"] == "error"]
        warnings = [i for i in issues if i["severity"] == "warning"]
        if errors:
            lines.append(f"{len(errors)} error(s):")
            for e in errors:
                lines.append(f"  [ERROR] {e['message']}")
        if warnings:
            lines.append(f"{len(warnings)} warning(s):")
            for w in warnings:
                lines.append(f"  [WARNING] {w['message']}")
        issues_summary = "\n".join(lines)

    return {
        "issues": issues,
        "error_count": error_count,
        "warning_count": warning_count,
        "issues_summary": issues_summary,
        "has_errors": error_count > 0,
        "has_warnings": warning_count > 0,
    }


def _apply_corrections(entities: dict, corrections: list[dict]) -> dict:
    """
    Apply a list of corrections to entities dict.
    Each correction has: entity_type, name, _delete?, ...fields
    Returns updated entities dict.
    """
    result: dict[str, Any] = dict(entities)

    for correction in corrections:
        if not isinstance(correction, dict):
            continue

        entity_type = correction.get("entity_type", "").lower()
        section_key = SECTION_MAP.get(entity_type, entity_type)
        if not section_key or section_key not in result:
            continue

        c_name = correction.get("name", "")

        if correction.get("_delete"):
            result[section_key] = [
                e for e in result[section_key] if e.get("name") != c_name
            ]
            continue

        payload = {
            k: v for k, v in correction.items() if k not in ("entity_type", "_delete")
        }
        matched_idx = next(
            (i for i, e in enumerate(result[section_key]) if e.get("name") == c_name),
            None,
        )
        if matched_idx is not None:
            result[section_key][matched_idx].update(payload)
        else:
            result[section_key].append(payload)

    return result


async def handle_store_entities(request: Request) -> JSONResponse:
    """
    POST /store-entities
    Body: { "conversation_id": "...", "entities": {...} }
    Caches entities server-side so agent tools can pass only conversation_id.
    Returns: { "ok": true }
    """
    try:
        body = await request.json()
    except Exception:
        return JSONResponse({"error": "Invalid JSON body"}, status_code=400)

    conversation_id = body.get("conversation_id")
    entities = body.get("entities")

    if not conversation_id:
        return JSONResponse({"error": "Missing 'conversation_id'"}, status_code=400)
    if not isinstance(entities, dict):
        return JSONResponse({"error": "'entities' must be an object"}, status_code=400)

    _entity_store.put(conversation_id, entities)
    logger.info(
        "store-entities: cached entities for conversation_id=%s", conversation_id
    )
    return JSONResponse({"ok": True})


async def handle_validate_entities(request: Request) -> JSONResponse:
    """
    POST /validate-entities
    Body: { "entities": {...} }  OR  { "conversation_id": "..." }
    Optional: "verbose": true  — include full issues list and issues_summary.

    Default (used in the agent loop):
      {
        "issues":        [{"severity","entity_type","message"}, ...] capped at
                         top-20 errors + top-10 warnings (errors first),
        "error_count":   int  # actual total (may exceed 20)
        "warning_count": int  # actual total (may exceed 10)
        "has_errors":    bool,
        "has_warnings":  bool,
        "issues_truncated": bool,   # true if capped
        "entity_counts": {...}      # when conversation_id used
      }

    Verbose (verbose=true, for debugging):
      adds full untruncated issues list and issues_summary text.

    Rationale: the previous response embedded every issue (up to 6-8KB of
    text) on every call. That payload then stayed in the LLM's context for
    every subsequent tool-using round, consuming most of the token budget.
    Capping at 30 items keeps the response under ~2KB without hiding the
    useful signal (agents can ask for verbose when they need it).
    """
    try:
        body = await request.json()
    except Exception:
        return JSONResponse({"error": "Invalid JSON body"}, status_code=400)

    entities = body.get("entities") or None
    conversation_id = body.get("conversation_id") or None
    verbose = bool(body.get("verbose", False))

    if entities is None and conversation_id:
        entities = _entity_store.get(conversation_id)
        if entities is None:
            return JSONResponse(
                {
                    "error": f"No entities found for conversation_id={conversation_id}. Call /store-entities first."
                },
                status_code=404,
            )
    elif entities is None:
        return JSONResponse(
            {"error": "Provide 'entities' or 'conversation_id'"}, status_code=400
        )

    if not isinstance(entities, dict):
        return JSONResponse({"error": "'entities' must be an object"}, status_code=400)

    full = _validate(entities)
    all_issues = full.get("issues", []) or []
    errors = [i for i in all_issues if i.get("severity") == "error"]
    warnings = [i for i in all_issues if i.get("severity") == "warning"]

    MAX_ERRORS = 20
    MAX_WARNINGS = 10

    if verbose:
        capped_issues = all_issues
    else:
        capped_issues = errors[:MAX_ERRORS] + warnings[:MAX_WARNINGS]

    result = {
        "issues": capped_issues,
        "error_count": len(errors),
        "warning_count": len(warnings),
        "has_errors": len(errors) > 0,
        "has_warnings": len(warnings) > 0,
        "issues_truncated": (len(errors) > MAX_ERRORS or len(warnings) > MAX_WARNINGS)
        if not verbose
        else False,
    }

    if verbose:
        result["issues_summary"] = full.get("issues_summary", "")

    if conversation_id:
        result["entity_counts"] = {
            k: len(v) if isinstance(v, list) else 1 for k, v in entities.items()
        }
    else:
        result["entities"] = entities

    logger.info(
        "validate-entities: %d errors, %d warnings (verbose=%s, returned=%d issues)",
        len(errors),
        len(warnings),
        verbose,
        len(capped_issues),
    )
    return JSONResponse(result)


async def handle_apply_entity_corrections(request: Request) -> JSONResponse:
    """
    POST /apply-entity-corrections
    Body: { "entities": {...}, "corrections": [...] }
      OR: { "conversation_id": "...", "corrections": [...] }  — looks up + updates store
    Returns: { "result": updated_entities }
    """
    try:
        body = await request.json()
    except Exception:
        return JSONResponse({"error": "Invalid JSON body"}, status_code=400)

    entities = body.get("entities") or None
    conversation_id = body.get("conversation_id") or None
    corrections = body.get("corrections", [])

    if entities is None and conversation_id:
        entities = _entity_store.get(conversation_id)
        if entities is None:
            return JSONResponse(
                {
                    "error": f"No entities found for conversation_id={conversation_id}. Call /store-entities first."
                },
                status_code=404,
            )
    elif entities is None:
        return JSONResponse(
            {"error": "Provide 'entities' or 'conversation_id'"}, status_code=400
        )

    if not isinstance(entities, dict):
        return JSONResponse({"error": "'entities' must be an object"}, status_code=400)
    if not isinstance(corrections, list):
        return JSONResponse(
            {"error": "'corrections' must be an array"}, status_code=400
        )

    updated = _apply_corrections(entities, corrections)

    # Write back to store so subsequent calls see the updated entities
    if conversation_id:
        _entity_store.put(conversation_id, updated)

    logger.info("apply-entity-corrections: applied %d corrections", len(corrections))

    # When using conversation_id, return compact summary instead of full entities
    if conversation_id:
        return JSONResponse(
            {
                "ok": True,
                "corrections_applied": len(corrections),
                "entity_counts": {
                    k: len(v) if isinstance(v, list) else 1 for k, v in updated.items()
                },
            }
        )

    # Legacy: return full entities
    return JSONResponse({"result": updated})


_VALID_ENTITY_SECTIONS = {
    "subject_types",
    "programs",
    "encounter_types",
    "address_levels",
    "forms",
    "misc_sheets",
}


async def handle_get_entities_section(request: Request) -> JSONResponse:
    """
    GET /entities-section?conversation_id=...&section=encounter_types
    Returns one section array from the stored entities dict.
    Valid sections: subject_types, programs, encounter_types, address_levels, forms
    """
    conversation_id = request.query_params.get("conversation_id")
    section = request.query_params.get("section")
    if not conversation_id or not section:
        return JSONResponse(
            {"error": "Missing 'conversation_id' or 'section' query param"},
            status_code=400,
        )

    if section not in _VALID_ENTITY_SECTIONS:
        return JSONResponse(
            {
                "error": f"Invalid section '{section}'. Valid: {sorted(_VALID_ENTITY_SECTIONS)}"
            },
            status_code=400,
        )

    entities = _entity_store.get(conversation_id)
    if entities is None:
        return JSONResponse(
            {
                "error": f"No entities found for conversation_id={conversation_id!r}. Call /store-entities first."
            },
            status_code=404,
        )

    items = entities.get(section, [])
    logger.info(
        "get-entities-section: conversation_id=%s section=%s count=%d",
        conversation_id,
        section,
        len(items),
    )
    return JSONResponse({"section": section, "items": items, "count": len(items)})


async def handle_put_entities_section(request: Request) -> JSONResponse:
    """
    PUT /entities-section
    Body: { "conversation_id": "...", "section": "encounter_types", "items": [...] }
    Replaces one section in the stored entities dict and re-stores it.
    """
    try:
        body = await request.json()
    except Exception:
        return JSONResponse({"error": "Invalid JSON body"}, status_code=400)

    conversation_id = body.get("conversation_id")
    section = body.get("section")
    items = body.get("items")

    if not conversation_id or not section:
        return JSONResponse(
            {"error": "Missing 'conversation_id' or 'section'"}, status_code=400
        )
    if section not in _VALID_ENTITY_SECTIONS:
        return JSONResponse(
            {
                "error": f"Invalid section '{section}'. Valid: {sorted(_VALID_ENTITY_SECTIONS)}"
            },
            status_code=400,
        )
    if not isinstance(items, list):
        return JSONResponse({"error": "'items' must be an array"}, status_code=400)

    entities = _entity_store.get(conversation_id)
    if entities is None:
        return JSONResponse(
            {
                "error": f"No entities found for conversation_id={conversation_id!r}. Call /store-entities first."
            },
            status_code=404,
        )

    entities[section] = items
    _entity_store.put(conversation_id, entities)
    logger.info(
        "put-entities-section: updated section=%s count=%d for conversation_id=%s",
        section,
        len(items),
        conversation_id,
    )
    return JSONResponse({"updated": True, "section": section, "count": len(items)})
