"""
spec_handlers.py — HTTP handlers for the spec stage

Endpoints:
  POST /generate-spec      entities dict → YAML spec string
  POST /validate-spec      YAML spec string → validation result
  POST /spec-to-entities   YAML spec string → full entities dict
  POST /bundle-to-spec     existing bundle JSON → YAML spec string
"""

from __future__ import annotations

import logging

from starlette.requests import Request
from starlette.responses import JSONResponse

from ..bundle.spec_generator import entities_to_spec
from ..bundle.spec_parser import spec_to_entities
from ..bundle.spec_validator import validate_spec

logger = logging.getLogger(__name__)


async def handle_generate_spec(request: Request) -> JSONResponse:
    """
    POST /generate-spec
    Body: { "entities": {...}, "org_name": "..." }
    Returns: { "spec_yaml": "..." }
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

    org_name = body.get("org_name", "")
    try:
        spec_yaml = entities_to_spec(entities, org_name=org_name)
    except Exception as exc:
        logger.exception("generate-spec error")
        return JSONResponse({"error": str(exc)}, status_code=500)

    logger.info("generate-spec: produced spec for org='%s'", org_name)
    return JSONResponse({"spec_yaml": spec_yaml})


async def handle_validate_spec(request: Request) -> JSONResponse:
    """
    POST /validate-spec
    Body: { "spec_yaml": "..." }
    Returns: { "valid": bool, "errors": [...], "warnings": [...], "suggestions": [...] }
    """
    try:
        body = await request.json()
    except Exception:
        return JSONResponse({"error": "Invalid JSON body"}, status_code=400)

    spec_yaml = body.get("spec_yaml")
    if spec_yaml is None:
        return JSONResponse({"error": "Missing 'spec_yaml' key"}, status_code=400)
    if not isinstance(spec_yaml, str):
        return JSONResponse({"error": "'spec_yaml' must be a string"}, status_code=400)

    try:
        result = validate_spec(spec_yaml)
    except Exception as exc:
        logger.exception("validate-spec error")
        return JSONResponse({"error": str(exc)}, status_code=500)

    logger.info(
        "validate-spec: valid=%s errors=%d warnings=%d",
        result["valid"],
        len(result["errors"]),
        len(result["warnings"]),
    )
    return JSONResponse(result)


async def handle_spec_to_entities(request: Request) -> JSONResponse:
    """
    POST /spec-to-entities
    Body: { "spec_yaml": "..." }
    Returns: { "entities": {...}, "org_name": "..." }
    """
    try:
        body = await request.json()
    except Exception:
        return JSONResponse({"error": "Invalid JSON body"}, status_code=400)

    spec_yaml = body.get("spec_yaml")
    if spec_yaml is None:
        return JSONResponse({"error": "Missing 'spec_yaml' key"}, status_code=400)
    if not isinstance(spec_yaml, str):
        return JSONResponse({"error": "'spec_yaml' must be a string"}, status_code=400)

    try:
        result = spec_to_entities(spec_yaml)
    except ValueError as exc:
        return JSONResponse({"error": str(exc)}, status_code=400)
    except Exception as exc:
        logger.exception("spec-to-entities error")
        return JSONResponse({"error": str(exc)}, status_code=500)

    org_name = result.pop("org_name", "")
    logger.info(
        "spec-to-entities: %d subject types, %d programs, %d encounter types, %d forms",
        len(result.get("subject_types", [])),
        len(result.get("programs", [])),
        len(result.get("encounter_types", [])),
        len(result.get("forms", [])),
    )
    return JSONResponse({"entities": result, "org_name": org_name})


async def handle_bundle_to_spec(request: Request) -> JSONResponse:
    """
    POST /bundle-to-spec
    Body: { "bundle": {...} }
    Returns: { "spec_yaml": "..." }

    Inverts a generated bundle back to a human-readable YAML spec.
    Strips UUIDs, reconstructs hierarchy.
    """
    try:
        body = await request.json()
    except Exception:
        return JSONResponse({"error": "Invalid JSON body"}, status_code=400)

    bundle = body.get("bundle")
    if bundle is None:
        return JSONResponse({"error": "Missing 'bundle' key"}, status_code=400)
    if not isinstance(bundle, dict):
        return JSONResponse({"error": "'bundle' must be an object"}, status_code=400)

    try:
        entities = _bundle_to_entities(bundle)
        org_name = body.get("org_name", "")
        spec_yaml = entities_to_spec(entities, org_name=org_name)
    except Exception as exc:
        logger.exception("bundle-to-spec error")
        return JSONResponse({"error": str(exc)}, status_code=500)

    logger.info("bundle-to-spec: converted bundle to spec")
    return JSONResponse({"spec_yaml": spec_yaml})


def _bundle_to_entities(bundle: dict) -> dict:
    """
    Convert a generated bundle dict back to an entities dict suitable for spec generation.
    Strips all UUIDs and id fields.
    """
    entities: dict = {
        "subject_types": [],
        "programs": [],
        "encounter_types": [],
        "address_levels": [],
        "groups": [],
        "forms": [],
    }

    # Address level types → address_levels
    for alt in bundle.get("addressLevelTypes", []):
        entities["address_levels"].append({
            "name": alt.get("name", ""),
            "level": alt.get("level", 1),
            "parent": alt.get("parent", {}).get("name") if isinstance(alt.get("parent"), dict) else alt.get("parent"),
        })

    # Subject types
    for st in bundle.get("subjectTypes", []):
        entities["subject_types"].append({
            "name": st.get("name", ""),
            "type": st.get("type", "Person"),
            "allowProfilePicture": st.get("allowProfilePicture", False),
            "uniqueName": st.get("uniqueName", False),
        })

    # Programs
    for prog in bundle.get("programs", []):
        entities["programs"].append({
            "name": prog.get("name", ""),
            "target_subject_type": prog.get("operationalPrograms", {}).get("subjectType", ""),
            "colour": prog.get("colour", "#4A148C"),
            "allow_multiple_enrolments": prog.get("allowMultipleEnrolments", False),
        })

    # Encounter types — derive from operational encounter types for cross-refs
    op_enc = bundle.get("operationalEncounterTypes", {}).get("operationalEncounterTypes", [])
    op_enc_by_uuid = {e.get("encounterTypeUUID"): e for e in op_enc}
    for enc in bundle.get("encounterTypes", []):
        op = op_enc_by_uuid.get(enc.get("uuid"), {})
        entities["encounter_types"].append({
            "name": enc.get("name", ""),
            "program_name": op.get("programName", ""),
            "subject_type": op.get("subjectTypeName", ""),
            "is_program_encounter": bool(op.get("programName")),
            "is_scheduled": True,
        })

    # Forms — iterate forms subdirectory contents
    for form in bundle.get("forms", []):
        if isinstance(form, dict):
            entities["forms"].append(form)

    # Groups
    for grp in bundle.get("groups", []):
        entities["groups"].append({
            "name": grp.get("name", ""),
            "has_all_privileges": grp.get("hasAllPrivileges", False),
        })

    return entities
