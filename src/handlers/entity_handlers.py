"""
Entity validation and correction handlers.
Replaces Dify code nodes: Ambiguity Checker + Entities Corrector.

Endpoints:
  POST /validate-entities   — structural validation of extracted entities
  POST /apply-entity-corrections — apply LLM-generated corrections to entities
"""

from __future__ import annotations

import logging
from typing import Any

from starlette.requests import Request
from starlette.responses import JSONResponse

logger = logging.getLogger(__name__)

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
        if r.get("is_program_encounter"):
            program = r.get("program_name", "")
            if program and not _fuzzy_match(program, program_names):
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
        else:
            subject = r.get("subject_type", "")
            if subject and not _fuzzy_match(subject, subject_type_names):
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


async def handle_validate_entities(request: Request) -> JSONResponse:
    """
    POST /validate-entities
    Body: { "entities": { subject_types, programs, encounter_types, address_levels } }
    Returns: { entities, issues, error_count, warning_count, issues_summary, has_errors, has_warnings }
    """
    try:
        body = await request.json()
    except Exception:
        return JSONResponse({"error": "Invalid JSON body"}, status_code=400)

    entities = body.get("entities")
    if entities is None:
        return JSONResponse({"error": "Missing 'entities' key"}, status_code=400)

    if not isinstance(entities, dict):
        return JSONResponse({"error": "'entities' must be an object"}, status_code=400)

    result = _validate(entities)
    result["entities"] = entities

    logger.info(
        "validate-entities: %d errors, %d warnings",
        result["error_count"],
        result["warning_count"],
    )
    return JSONResponse(result)


async def handle_apply_entity_corrections(request: Request) -> JSONResponse:
    """
    POST /apply-entity-corrections
    Body: { "entities": {...}, "corrections": [{entity_type, name, ...fields, _delete?}] }
    Returns: { "result": updated_entities }
    """
    try:
        body = await request.json()
    except Exception:
        return JSONResponse({"error": "Invalid JSON body"}, status_code=400)

    entities = body.get("entities")
    corrections = body.get("corrections", [])

    if entities is None:
        return JSONResponse({"error": "Missing 'entities' key"}, status_code=400)
    if not isinstance(entities, dict):
        return JSONResponse({"error": "'entities' must be an object"}, status_code=400)
    if not isinstance(corrections, list):
        return JSONResponse(
            {"error": "'corrections' must be an array"}, status_code=400
        )

    updated = _apply_corrections(entities, corrections)

    logger.info("apply-entity-corrections: applied %d corrections", len(corrections))
    return JSONResponse({"result": updated})
