"""
spec_handlers.py — HTTP handlers for the spec stage

Endpoints:
  POST /generate-spec        entities dict → YAML spec string (stores server-side when conversation_id given)
  GET  /get-spec             retrieve stored spec YAML by conversation_id
  GET  /spec-section         fetch one top-level YAML section from stored spec
  PUT  /spec-section         replace one top-level YAML section in stored spec
  POST /validate-spec        YAML spec string → validation result
  POST /spec-to-entities     YAML spec string → full entities dict
  POST /bundle-to-spec       existing bundle JSON → YAML spec string
"""

from __future__ import annotations

import logging
import os
import time

import yaml
from starlette.requests import Request
from starlette.responses import JSONResponse

from ..bundle.spec_generator import entities_to_spec
from ..bundle.spec_parser import spec_to_entities
from ..bundle.spec_validator import validate_spec
from .entity_handlers import _entity_store

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# In-memory spec store keyed by conversation_id (TTL configurable via env)
# generate_spec stores the full YAML here and returns only a compact summary,
# keeping large YAML off the LLM context window entirely.
# ---------------------------------------------------------------------------
_SPEC_STORE_TTL = int(os.getenv("SPEC_STORE_TTL_HOURS", "6")) * 3600
_MAX_SPEC_RESPONSE_CHARS = int(os.getenv("MAX_SPEC_RESPONSE_CHARS", "8000"))


class _SpecStore:
    def __init__(self) -> None:
        self._store: dict[str, tuple[str, float]] = {}  # id -> (spec_yaml, expiry)

    def put(self, conversation_id: str, spec_yaml: str) -> None:
        self._store[conversation_id] = (spec_yaml, time.time() + _SPEC_STORE_TTL)

    def get(self, conversation_id: str) -> str | None:
        entry = self._store.get(conversation_id)
        if entry is None:
            return None
        spec_yaml, expiry = entry
        if time.time() > expiry:
            del self._store[conversation_id]
            return None
        return spec_yaml

    def put_section(self, conversation_id: str, section: str, value: object) -> bool:
        """Replace one top-level key in the stored YAML. Returns False if not found."""
        spec_yaml = self.get(conversation_id)
        if spec_yaml is None:
            return False
        try:
            data = yaml.safe_load(spec_yaml) or {}
        except Exception:
            return False
        data[section] = value
        new_yaml = yaml.dump(
            data, allow_unicode=True, default_flow_style=False, sort_keys=False
        )
        self._store[conversation_id] = (new_yaml, time.time() + _SPEC_STORE_TTL)
        return True

    def cleanup(self) -> int:
        now = time.time()
        expired = [k for k, (_, exp) in self._store.items() if now > exp]
        for k in expired:
            del self._store[k]
        return len(expired)


_spec_store = _SpecStore()


def get_spec_store() -> _SpecStore:
    """Return the global spec store."""
    return _spec_store


async def handle_generate_spec(request: Request) -> JSONResponse:
    """
    POST /generate-spec
    Body: { "conversation_id": "...", "org_name": "..." }  — preferred
      OR: { "entities": {...}, "org_name": "..." }           — legacy

    When conversation_id is provided:
      - Entities are fetched from the entity store.
      - Generated spec is stored server-side in _spec_store.
      - Returns a compact summary only — spec_yaml never reaches the LLM.
      - Call GET /get-spec to retrieve the full YAML for display.
    Legacy (no conversation_id): returns spec_yaml directly.
    """
    try:
        body = await request.json()
    except Exception:
        return JSONResponse({"error": "Invalid JSON body"}, status_code=400)

    entities = body.get("entities") or None
    conversation_id = body.get("conversation_id") or None

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

    org_name = body.get("org_name", "")
    try:
        spec_yaml = entities_to_spec(entities, org_name=org_name)
    except Exception as exc:
        logger.exception("generate-spec error")
        return JSONResponse({"error": str(exc)}, status_code=500)

    if conversation_id:
        # Store spec server-side; return compact summary only — no large YAML to LLM
        _spec_store.put(conversation_id, spec_yaml)
        try:
            parsed = yaml.safe_load(spec_yaml) or {}
        except Exception:
            parsed = {}
        summary = {
            k: (len(v) if isinstance(v, list) else ("present" if v else "empty"))
            for k, v in parsed.items()
            if k not in ("org", "settings")
        }
        logger.info(
            "generate-spec: stored spec for conversation_id=%s char_count=%d summary=%s",
            conversation_id,
            len(spec_yaml),
            summary,
        )
        return JSONResponse(
            {
                "stored": True,
                "char_count": len(spec_yaml),
                "summary": summary,
                "next_step": "Call get_spec(conversation_id) to retrieve and show the full spec to the user.",
            }
        )

    # Legacy: return spec_yaml directly (no conversation_id)
    logger.info("generate-spec: produced spec for org='%s' (legacy mode)", org_name)
    return JSONResponse({"spec_yaml": spec_yaml})


async def handle_get_spec(request: Request) -> JSONResponse:
    """
    GET /get-spec?conversation_id=...
    Returns the full stored spec YAML for display to the user.
    Agent calls this after generate_spec confirms stored=true.
    Response is capped at MAX_SPEC_RESPONSE_CHARS as a safety fallback.
    """
    conversation_id = request.query_params.get("conversation_id")
    if not conversation_id:
        return JSONResponse(
            {"error": "Missing 'conversation_id' query param"}, status_code=400
        )

    spec_yaml = _spec_store.get(conversation_id)
    if spec_yaml is None:
        return JSONResponse(
            {
                "error": f"No stored spec for conversation_id={conversation_id!r}. Call generate_spec first."
            },
            status_code=404,
        )

    full_len = len(spec_yaml)
    truncated = full_len > _MAX_SPEC_RESPONSE_CHARS
    if truncated:
        spec_yaml = spec_yaml[:_MAX_SPEC_RESPONSE_CHARS]
        logger.warning(
            "get-spec: truncating spec for conversation_id=%s from %d to %d chars (set MAX_SPEC_RESPONSE_CHARS env var to increase)",
            conversation_id,
            full_len,
            _MAX_SPEC_RESPONSE_CHARS,
        )
    else:
        logger.info(
            "get-spec: returning spec for conversation_id=%s char_count=%d",
            conversation_id,
            full_len,
        )
    return JSONResponse({"spec_yaml": spec_yaml, "truncated": truncated})


async def handle_get_spec_section(request: Request) -> JSONResponse:
    """
    GET /spec-section?conversation_id=...&section=encounterTypes
    Returns one top-level YAML key from the stored spec.
    Valid sections: subjectTypes, programs, encounterTypes, addressLevels, groups, settings, org
    """
    conversation_id = request.query_params.get("conversation_id")
    section = request.query_params.get("section")
    if not conversation_id or not section:
        return JSONResponse(
            {"error": "Missing 'conversation_id' or 'section' query param"},
            status_code=400,
        )

    spec_yaml = _spec_store.get(conversation_id)
    if spec_yaml is None:
        return JSONResponse(
            {
                "error": f"No stored spec for conversation_id={conversation_id!r}. Call generate_spec first."
            },
            status_code=404,
        )

    try:
        data = yaml.safe_load(spec_yaml) or {}
    except Exception as exc:
        return JSONResponse(
            {"error": f"Failed to parse stored spec: {exc}"}, status_code=500
        )

    if section not in data:
        return JSONResponse(
            {"error": f"Section '{section}' not found. Available: {list(data.keys())}"},
            status_code=404,
        )

    section_value = data[section]
    section_yaml = yaml.dump(
        {section: section_value},
        allow_unicode=True,
        default_flow_style=False,
        sort_keys=False,
    )
    logger.info(
        "get-spec-section: conversation_id=%s section=%s", conversation_id, section
    )
    return JSONResponse(
        {"section": section, "value": section_value, "yaml": section_yaml}
    )


async def handle_put_spec_section(request: Request) -> JSONResponse:
    """
    PUT /spec-section
    Body: { "conversation_id": "...", "section": "encounterTypes", "value": [...] }
      OR: { "conversation_id": "...", "section": "encounterTypes", "yaml_fragment": "encounterTypes:\n  - ..." }
    Replaces one top-level key in the stored spec and re-stores it.
    """
    try:
        body = await request.json()
    except Exception:
        return JSONResponse({"error": "Invalid JSON body"}, status_code=400)

    conversation_id = body.get("conversation_id")
    section = body.get("section")
    if not conversation_id or not section:
        return JSONResponse(
            {"error": "Missing 'conversation_id' or 'section'"}, status_code=400
        )

    # Accept either a parsed value or a YAML fragment string
    if "value" in body:
        new_value = body["value"]
    elif "yaml_fragment" in body:
        try:
            fragment = yaml.safe_load(body["yaml_fragment"]) or {}
            new_value = fragment.get(section, fragment)  # unwrap if keyed
        except Exception as exc:
            return JSONResponse(
                {"error": f"Invalid yaml_fragment: {exc}"}, status_code=400
            )
    else:
        return JSONResponse(
            {"error": "Provide 'value' or 'yaml_fragment'"}, status_code=400
        )

    if not _spec_store.put_section(conversation_id, section, new_value):
        return JSONResponse(
            {
                "error": f"No stored spec for conversation_id={conversation_id!r}. Call generate_spec first."
            },
            status_code=404,
        )

    logger.info(
        "put-spec-section: updated section=%s for conversation_id=%s",
        section,
        conversation_id,
    )
    return JSONResponse({"updated": True, "section": section})


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
        entities["address_levels"].append(
            {
                "name": alt.get("name", ""),
                "level": alt.get("level", 1),
                "parent": alt.get("parent", {}).get("name")
                if isinstance(alt.get("parent"), dict)
                else alt.get("parent"),
            }
        )

    # Subject types
    for st in bundle.get("subjectTypes", []):
        entities["subject_types"].append(
            {
                "name": st.get("name", ""),
                "type": st.get("type", "Person"),
                "allowProfilePicture": st.get("allowProfilePicture", False),
                "uniqueName": st.get("uniqueName", False),
            }
        )

    # Programs
    for prog in bundle.get("programs", []):
        entities["programs"].append(
            {
                "name": prog.get("name", ""),
                "target_subject_type": prog.get("operationalPrograms", {}).get(
                    "subjectType", ""
                ),
                "colour": prog.get("colour", "#4A148C"),
                "allow_multiple_enrolments": prog.get("allowMultipleEnrolments", False),
            }
        )

    # Encounter types — derive from operational encounter types for cross-refs
    op_enc = bundle.get("operationalEncounterTypes", {}).get(
        "operationalEncounterTypes", []
    )
    op_enc_by_uuid = {e.get("encounterTypeUUID"): e for e in op_enc}
    for enc in bundle.get("encounterTypes", []):
        op = op_enc_by_uuid.get(enc.get("uuid"), {})
        entities["encounter_types"].append(
            {
                "name": enc.get("name", ""),
                "program_name": op.get("programName", ""),
                "subject_type": op.get("subjectTypeName", ""),
                "is_program_encounter": bool(op.get("programName")),
                "is_scheduled": True,
            }
        )

    # Forms — iterate forms subdirectory contents
    for form in bundle.get("forms", []):
        if isinstance(form, dict):
            entities["forms"].append(form)

    # Groups
    for grp in bundle.get("groups", []):
        entities["groups"].append(
            {
                "name": grp.get("name", ""),
                "has_all_privileges": grp.get("hasAllPrivileges", False),
            }
        )

    return entities
