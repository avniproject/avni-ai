"""
Configuration inspector handlers.

Provides endpoints for compiling requirements against entity definitions
and performing gap analysis on an AVNI configuration bundle.

Endpoints:
  POST /inspector/compile-requirements  — check requirements against entities
  POST /inspector/inspect-config        — gap analysis with completeness score
"""

from __future__ import annotations

import logging
from typing import Any

from starlette.requests import Request
from starlette.responses import JSONResponse

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Requirement checking
# ---------------------------------------------------------------------------


def _check_requirements(requirements: list[dict], entities: dict) -> list[dict]:
    """
    Check a list of requirements against the entities dict.

    Each requirement has:
      - description: human-readable requirement text
      - entity_type: "subject_type" | "program" | "encounter_type" | "address_level" | "form"
      - name: expected entity name (optional)
      - field: expected field name within a form (optional)

    Returns a list of result dicts with status "met" | "not_met" | "partial".
    """
    results: list[dict] = []

    entity_section_map = {
        "subject_type": "subject_types",
        "program": "programs",
        "encounter_type": "encounter_types",
        "address_level": "address_levels",
        "form": "forms",
    }

    for req in requirements:
        if not isinstance(req, dict):
            continue

        description = req.get("description", "")
        entity_type = req.get("entity_type", "")
        name = req.get("name", "")
        field_name = req.get("field", "")

        section_key = entity_section_map.get(entity_type, "")
        section_items = entities.get(section_key, []) if section_key else []

        result: dict[str, Any] = {
            "description": description,
            "entity_type": entity_type,
            "name": name,
        }

        if not section_key:
            result["status"] = "not_met"
            result["reason"] = f"Unknown entity type: {entity_type}"
            results.append(result)
            continue

        if not name:
            # Just check that the section has at least one entry
            if section_items:
                result["status"] = "met"
                result["reason"] = f"Found {len(section_items)} {entity_type}(s)"
            else:
                result["status"] = "not_met"
                result["reason"] = f"No {entity_type}s defined"
            results.append(result)
            continue

        # Find the named entity
        matched = None
        for item in section_items:
            if isinstance(item, dict) and item.get("name", "").lower() == name.lower():
                matched = item
                break

        if matched is None:
            result["status"] = "not_met"
            result["reason"] = f"{entity_type} '{name}' not found"
            results.append(result)
            continue

        # If a specific field is required, check for it in form fields
        if field_name and entity_type == "form":
            fields = matched.get("fields", [])
            field_found = any(
                isinstance(f, dict) and f.get("name", "").lower() == field_name.lower()
                for f in fields
            )
            if field_found:
                result["status"] = "met"
                result["reason"] = f"Field '{field_name}' found in form '{name}'"
            else:
                result["status"] = "partial"
                result["reason"] = (
                    f"Form '{name}' exists but field '{field_name}' not found"
                )
        else:
            result["status"] = "met"
            result["reason"] = f"{entity_type} '{name}' found"

        results.append(result)

    return results


# ---------------------------------------------------------------------------
# Gap analysis
# ---------------------------------------------------------------------------


def _inspect_config(entities: dict) -> dict[str, Any]:
    """
    Perform gap analysis on entities and compute a completeness score.

    Checks:
    - Subject types defined
    - Programs defined with target subject types
    - Encounter types defined with valid cross-references
    - Address levels with proper hierarchy
    - Forms with fields
    - Groups defined
    """
    gaps: list[dict[str, str]] = []
    checks_passed = 0
    checks_total = 0

    # Check subject types
    checks_total += 1
    st_rows = entities.get("subject_types", [])
    if st_rows:
        checks_passed += 1
    else:
        gaps.append({
            "area": "subject_types",
            "severity": "error",
            "message": "No subject types defined",
        })

    # Check programs
    checks_total += 1
    prog_rows = entities.get("programs", [])
    if prog_rows:
        checks_passed += 1
        # Check target subject types
        st_names = {s.get("name", "").lower() for s in st_rows if isinstance(s, dict)}
        for prog in prog_rows:
            if not isinstance(prog, dict):
                continue
            target = (prog.get("target_subject_type") or "").lower()
            if target and target not in st_names:
                gaps.append({
                    "area": "programs",
                    "severity": "warning",
                    "message": (
                        f"Program '{prog.get('name')}' targets "
                        f"'{prog.get('target_subject_type')}' which is not defined"
                    ),
                })
    else:
        gaps.append({
            "area": "programs",
            "severity": "warning",
            "message": "No programs defined (not required for general encounters)",
        })

    # Check encounter types
    checks_total += 1
    enc_rows = entities.get("encounter_types", [])
    if enc_rows:
        checks_passed += 1
    else:
        gaps.append({
            "area": "encounter_types",
            "severity": "error",
            "message": "No encounter types defined",
        })

    # Check address levels
    checks_total += 1
    addr_rows = entities.get("address_levels", [])
    if addr_rows:
        checks_passed += 1
        # Check hierarchy
        names = {a.get("name", "") for a in addr_rows if isinstance(a, dict)}
        for addr in addr_rows:
            if not isinstance(addr, dict):
                continue
            parent = addr.get("parent", "")
            if parent and parent not in names:
                gaps.append({
                    "area": "address_levels",
                    "severity": "warning",
                    "message": (
                        f"Address level '{addr.get('name')}' references parent "
                        f"'{parent}' which is not defined"
                    ),
                })
    else:
        gaps.append({
            "area": "address_levels",
            "severity": "warning",
            "message": "No address levels defined. A default hierarchy will be generated.",
        })

    # Check forms
    checks_total += 1
    form_rows = entities.get("forms", [])
    if form_rows:
        checks_passed += 1
        forms_without_fields = [
            f.get("name", "?")
            for f in form_rows
            if isinstance(f, dict) and not f.get("fields")
        ]
        if forms_without_fields:
            gaps.append({
                "area": "forms",
                "severity": "warning",
                "message": (
                    f"{len(forms_without_fields)} form(s) have no fields: "
                    f"{', '.join(forms_without_fields[:5])}"
                ),
            })
    else:
        gaps.append({
            "area": "forms",
            "severity": "info",
            "message": "No explicit forms defined. Forms will be auto-derived from encounter types.",
        })

    # Check groups
    checks_total += 1
    group_rows = entities.get("groups", [])
    if group_rows:
        checks_passed += 1
    else:
        gaps.append({
            "area": "groups",
            "severity": "info",
            "message": "No groups defined. Default groups will be generated.",
        })

    # Compute completeness score
    completeness = round(checks_passed / checks_total, 2) if checks_total > 0 else 0.0

    return {
        "completeness_score": completeness,
        "checks_passed": checks_passed,
        "checks_total": checks_total,
        "gaps": gaps,
        "gap_count": len(gaps),
        "entity_counts": {
            "subject_types": len(st_rows),
            "programs": len(prog_rows),
            "encounter_types": len(enc_rows),
            "address_levels": len(addr_rows),
            "forms": len(form_rows),
            "groups": len(group_rows),
        },
    }


# ---------------------------------------------------------------------------
# Handlers
# ---------------------------------------------------------------------------


async def handle_compile_requirements(request: Request) -> JSONResponse:
    """
    POST /inspector/compile-requirements
    Body: {
        "requirements": [
            {"description": "Must have ANC encounter", "entity_type": "encounter_type", "name": "ANC"}
        ],
        "entities": { "subject_types": [...], "programs": [...], ... }
    }
    Checks each requirement against the entities and returns status for each.
    """
    try:
        body = await request.json()
    except Exception:
        return JSONResponse({"error": "Invalid JSON body"}, status_code=400)

    requirements = body.get("requirements", [])
    entities = body.get("entities", {})

    if not isinstance(requirements, list):
        return JSONResponse(
            {"error": "'requirements' must be an array"}, status_code=400
        )
    if not isinstance(entities, dict):
        return JSONResponse(
            {"error": "'entities' must be an object"}, status_code=400
        )

    results = _check_requirements(requirements, entities)

    met_count = sum(1 for r in results if r.get("status") == "met")
    not_met_count = sum(1 for r in results if r.get("status") == "not_met")
    partial_count = sum(1 for r in results if r.get("status") == "partial")

    logger.info(
        "inspector/compile-requirements: %d met, %d not_met, %d partial of %d total",
        met_count,
        not_met_count,
        partial_count,
        len(results),
    )
    return JSONResponse(
        {
            "ok": True,
            "results": results,
            "total": len(results),
            "met_count": met_count,
            "not_met_count": not_met_count,
            "partial_count": partial_count,
            "all_met": not_met_count == 0 and partial_count == 0,
        }
    )


async def handle_inspect_config(request: Request) -> JSONResponse:
    """
    POST /inspector/inspect-config
    Body: { "entities": { "subject_types": [...], "programs": [...], ... } }
    Performs gap analysis on the entity configuration and returns a completeness score.
    """
    try:
        body = await request.json()
    except Exception:
        return JSONResponse({"error": "Invalid JSON body"}, status_code=400)

    entities = body.get("entities", {})
    if not isinstance(entities, dict):
        return JSONResponse(
            {"error": "'entities' must be an object"}, status_code=400
        )

    result = _inspect_config(entities)

    logger.info(
        "inspector/inspect-config: completeness=%.0f%% gaps=%d",
        result["completeness_score"] * 100,
        result["gap_count"],
    )
    return JSONResponse({"ok": True, **result})
