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
  GET  /spec-format          returns the comprehensive YAML spec reference schema
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


def _resolve_entity_references(entities: dict) -> list[dict]:
    """
    Fall-forward: auto-resolve broken cross-references in entities.
    Mutates entities in place. Returns a list of flags describing what was changed.
    """
    flags: list[dict] = []

    st_names = {s["name"] for s in entities.get("subject_types", []) if s.get("name")}
    prog_names = {p["name"] for p in entities.get("programs", []) if p.get("name")}

    first_st = (
        entities["subject_types"][0]["name"] if entities.get("subject_types") else None
    )
    first_prog = entities["programs"][0]["name"] if entities.get("programs") else None

    # Build program → target subject type lookup
    prog_to_st: dict[str, str] = {}
    for p in entities.get("programs", []):
        target = p.get("target_subject_type") or p.get("targetSubjectType", "")
        if target:
            prog_to_st[p["name"]] = target

    for enc in entities.get("encounter_types", []):
        name = enc.get("name", "")
        subject = enc.get("subject_type", "")
        program = enc.get("program_name", "")
        is_program_enc = enc.get("is_program_encounter", False)

        # Unknown subject type → default to first
        if subject and subject not in st_names and first_st:
            flags.append(
                {
                    "type": "defaulted",
                    "entity": "encounter_type",
                    "name": name,
                    "field": "subject_type",
                    "original": subject,
                    "resolved_to": first_st,
                    "reason": (
                        f"Encounter '{name}' references unknown subject type '{subject}'. "
                        f"Available: {sorted(st_names)}. Defaulted to '{first_st}'. "
                        f"Void if not needed."
                    ),
                }
            )
            enc["subject_type"] = first_st

        # Missing subject type → default to first
        if not subject and first_st:
            flags.append(
                {
                    "type": "defaulted",
                    "entity": "encounter_type",
                    "name": name,
                    "field": "subject_type",
                    "original": "",
                    "resolved_to": first_st,
                    "reason": (
                        f"Encounter '{name}' has no subject type. "
                        f"Available: {sorted(st_names)}. Defaulted to '{first_st}'. "
                        f"Void if not needed."
                    ),
                }
            )
            enc["subject_type"] = first_st

        # Program encounter missing program → default
        if is_program_enc and not program and first_prog:
            # Try matching by subject type first
            resolved_prog = first_prog
            enc_st = enc.get("subject_type", "")
            for pname, pst in prog_to_st.items():
                if pst == enc_st:
                    resolved_prog = pname
                    break
            flags.append(
                {
                    "type": "defaulted",
                    "entity": "encounter_type",
                    "name": name,
                    "field": "program_name",
                    "original": "",
                    "resolved_to": resolved_prog,
                    "reason": (
                        f"Program encounter '{name}' has no program. "
                        f"Available: {sorted(prog_names)}. Defaulted to '{resolved_prog}'. "
                        f"Void if not needed."
                    ),
                }
            )
            enc["program_name"] = resolved_prog

        # Program encounter with unknown program → default
        if is_program_enc and program and program not in prog_names and first_prog:
            flags.append(
                {
                    "type": "defaulted",
                    "entity": "encounter_type",
                    "name": name,
                    "field": "program_name",
                    "original": program,
                    "resolved_to": first_prog,
                    "reason": (
                        f"Program encounter '{name}' references unknown program '{program}'. "
                        f"Available: {sorted(prog_names)}. Defaulted to '{first_prog}'. "
                        f"Void if not needed."
                    ),
                }
            )
            enc["program_name"] = first_prog

    if flags:
        logger.info("resolve-entity-references: auto-resolved %d issues", len(flags))
    return flags


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

    # Fall-forward: auto-resolve broken references in entities before generating spec.
    # This ensures generate_spec always succeeds. Flags are returned to the caller.
    flags = _resolve_entity_references(entities)
    if flags and conversation_id:
        # Persist the fixed entities back so downstream consumers see them
        _entity_store.put(conversation_id, entities)

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
        resp: dict = {
            "stored": True,
            "char_count": len(spec_yaml),
            "summary": summary,
            "next_step": "Call get_spec(conversation_id) to retrieve and show the full spec to the user.",
        }
        if flags:
            resp["flags"] = [f["reason"] for f in flags]
        return JSONResponse(resp)

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
    Strips all UUIDs and id fields. Filters voided entities.

    Comprehensive: captures all real-world patterns found across 21+ org bundles.
    """
    entities: dict = {
        "subject_types": [],
        "programs": [],
        "encounter_types": [],
        "address_levels": [],
        "groups": [],
        "forms": [],
    }

    # ── Build UUID lookup maps for cross-references ────────────────────────
    st_uuid_to_name: dict[str, str] = {}
    for st in bundle.get("subjectTypes", []):
        if st.get("uuid"):
            st_uuid_to_name[st["uuid"]] = st.get("name", "")

    prog_uuid_to_name: dict[str, str] = {}
    for prog in bundle.get("programs", []):
        if prog.get("uuid"):
            prog_uuid_to_name[prog["uuid"]] = prog.get("name", "")
    # Also from operationalPrograms
    op_progs = bundle.get("operationalPrograms", {})
    if isinstance(op_progs, dict):
        op_progs = op_progs.get("operationalPrograms", [])
    if isinstance(op_progs, list):
        for op in op_progs:
            prog_ref = op.get("program", {})
            if isinstance(prog_ref, dict) and prog_ref.get("uuid"):
                prog_uuid_to_name[prog_ref["uuid"]] = op.get("name", "")

    enc_uuid_to_name: dict[str, str] = {}
    for enc in bundle.get("encounterTypes", []):
        if enc.get("uuid"):
            enc_uuid_to_name[enc["uuid"]] = enc.get("name", "")

    # formMappings: build encounter→program and program→subjectType links
    enc_uuid_to_prog: dict[str, str] = {}
    enc_uuid_to_st: dict[str, str] = {}
    prog_uuid_to_st: dict[str, str] = {}
    for fm in bundle.get("formMappings", []):
        if fm.get("voided"):
            continue
        enc_uuid = fm.get("encounterTypeUUID")
        prog_uuid = fm.get("programUUID")
        st_uuid = fm.get("subjectTypeUUID")
        if enc_uuid and prog_uuid:
            enc_uuid_to_prog[enc_uuid] = prog_uuid_to_name.get(prog_uuid, "")
        if enc_uuid and st_uuid:
            enc_uuid_to_st[enc_uuid] = st_uuid_to_name.get(st_uuid, "")
        if prog_uuid and st_uuid and fm.get("formType") == "ProgramEnrolment":
            prog_uuid_to_st[prog_uuid] = st_uuid_to_name.get(st_uuid, "")

    # Address level UUID→name for parent resolution
    addr_uuid_to_name: dict[str, str] = {}
    for alt in bundle.get("addressLevelTypes", []):
        if alt.get("uuid") and not alt.get("voided"):
            addr_uuid_to_name[alt["uuid"]] = alt.get("name", "")

    # ── Address level types → address_levels ───────────────────────────────
    for alt in bundle.get("addressLevelTypes", []):
        if alt.get("voided"):
            continue
        parent = alt.get("parent")
        parent_name = None
        if isinstance(parent, dict):
            parent_name = parent.get("name") or addr_uuid_to_name.get(
                parent.get("uuid", "")
            )
        elif isinstance(parent, str) and parent:
            parent_name = parent
        entry = {
            "name": alt.get("name", ""),
            "level": alt.get("level", 1),
        }
        if parent_name:
            entry["parent"] = parent_name
        entities["address_levels"].append(entry)

    # ── Subject types ──────────────────────────────────────────────────────
    for st in bundle.get("subjectTypes", []):
        if st.get("voided"):
            continue
        st_entry: dict = {
            "name": st.get("name", ""),
            "type": st.get("type", "Person"),
        }
        # Comprehensive fields
        for key in [
            "group",
            "household",
            "allowProfilePicture",
            "uniqueName",
            "allowEmptyLocation",
            "allowMiddleName",
        ]:
            if st.get(key):
                st_entry[key] = True
        if st.get("lastNameOptional") is False:
            st_entry["lastNameOptional"] = False
        for key in [
            "validFirstNameFormat",
            "iconFileS3Key",
            "subjectSummaryRule",
            "programEligibilityCheckRule",
            "syncRegistrationConcept1",
            "syncRegistrationConcept1Usable",
            "memberAdditionEligibilityCheckRule",
        ]:
            if st.get(key):
                st_entry[key] = st[key]
        if isinstance(st.get("settings"), dict) and st["settings"]:
            st_entry["settings"] = st["settings"]
        entities["subject_types"].append(st_entry)

    # ── Programs ───────────────────────────────────────────────────────────
    for prog in bundle.get("programs", []):
        if prog.get("voided"):
            continue
        prog_uuid = prog.get("uuid", "")
        prog_entry: dict = {
            "name": prog.get("name", ""),
            "target_subject_type": prog_uuid_to_st.get(prog_uuid, ""),
            "colour": prog.get("colour", "#4A148C"),
        }
        if prog.get("allowMultipleEnrolments"):
            prog_entry["allow_multiple_enrolments"] = True
        if prog.get("showGrowthChart"):
            prog_entry["showGrowthChart"] = True
        for key in [
            "programSubjectLabel",
            "enrolmentSummaryRule",
            "enrolmentEligibilityCheckRule",
            "manualEnrolmentEligibilityCheckRule",
            "enrolmentEligibilityCheckDeclarativeRule",
        ]:
            if prog.get(key):
                prog_entry[key] = prog[key]
        entities["programs"].append(prog_entry)

    # ── Encounter types ────────────────────────────────────────────────────
    for enc in bundle.get("encounterTypes", []):
        if enc.get("voided"):
            continue
        enc_uuid = enc.get("uuid", "")
        prog_name = enc_uuid_to_prog.get(enc_uuid, "")
        st_name = enc_uuid_to_st.get(enc_uuid, "")
        enc_entry: dict = {
            "name": enc.get("name", ""),
            "program_name": prog_name,
            "subject_type": st_name,
            "is_program_encounter": bool(prog_name),
            "is_scheduled": True,
        }
        elig_rule = enc.get("encounterEligibilityCheckRule") or enc.get(
            "entityEligibilityCheckRule"
        )
        if elig_rule:
            enc_entry["encounterEligibilityCheckRule"] = elig_rule
        if enc.get("entityEligibilityCheckDeclarativeRule"):
            enc_entry["entityEligibilityCheckDeclarativeRule"] = enc[
                "entityEligibilityCheckDeclarativeRule"
            ]
        if enc.get("immutable"):
            enc_entry["immutable"] = True
        entities["encounter_types"].append(enc_entry)

    # ── Forms (enriched with entity links from formMappings) ─────────────
    # Build formName → formMapping lookup for cross-ref enrichment
    fm_by_form_name: dict[str, dict] = {}
    fm_by_form_uuid: dict[str, dict] = {}
    for fm in bundle.get("formMappings", []):
        if fm.get("voided"):
            continue
        if fm.get("formName"):
            fm_by_form_name[fm["formName"]] = fm
        if fm.get("formUUID"):
            fm_by_form_uuid[fm["formUUID"]] = fm

    for form in bundle.get("forms", []):
        if not isinstance(form, dict):
            continue
        # Find the matching formMapping to get entity cross-refs
        fm = fm_by_form_name.get(form.get("name", "")) or fm_by_form_uuid.get(
            form.get("uuid", "")
        )
        if fm:
            # Enrich form with entity names resolved from UUIDs
            form_type = fm.get("formType", form.get("formType", ""))
            if form_type:
                form["formType"] = form_type
            st_uuid = fm.get("subjectTypeUUID")
            if st_uuid:
                form["subjectType"] = st_uuid_to_name.get(st_uuid, "")
            prog_uuid_val = fm.get("programUUID")
            if prog_uuid_val:
                form["program"] = prog_uuid_to_name.get(prog_uuid_val, "")
            enc_uuid_val = fm.get("encounterTypeUUID")
            if enc_uuid_val:
                form["encounterType"] = enc_uuid_to_name.get(enc_uuid_val, "")
        entities["forms"].append(form)

    # ── Groups ─────────────────────────────────────────────────────────────
    for grp in bundle.get("groups", []):
        if grp.get("voided"):
            continue
        entities["groups"].append(
            {
                "name": grp.get("name", ""),
                "has_all_privileges": grp.get("hasAllPrivileges", False),
            }
        )

    # ── Settings from organisationConfig ───────────────────────────────────
    org_config = bundle.get("organisationConfig", {})
    if isinstance(org_config, list) and org_config:
        org_config = org_config[0]
    if isinstance(org_config, dict):
        config_settings = org_config.get(
            "settings", org_config.get("organisationConfig", {})
        )
        if isinstance(config_settings, dict) and config_settings:
            settings: dict = {}
            languages = config_settings.get("languages", ["en"])
            settings["languages"] = languages if languages else ["en"]
            for key in [
                "enableComments",
                "enableMessaging",
                "saveDrafts",
                "skipRuleExecution",
                "enableRuleDesigner",
                "metabaseSetupEnabled",
                "showHierarchicalLocation",
                "searchFilters",
                "myDashboardFilters",
                "customRegistrationLocations",
                "searchResultFields",
                "worklistUpdationRule",
            ]:
                if config_settings.get(key) is not None:
                    settings[key] = config_settings[key]
            entities["settings"] = settings

    # ── Group roles ────────────────────────────────────────────────────────
    group_roles = bundle.get("groupRole", bundle.get("groupRoles", []))
    if group_roles:
        active_roles = [r for r in group_roles if not r.get("voided", False)]
        if active_roles:
            entities["group_roles"] = [
                {
                    "role": r.get("role", ""),
                    **(
                        {
                            "groupSubjectType": st_uuid_to_name.get(
                                r.get("groupSubjectTypeUUID", ""), ""
                            )
                        }
                        if r.get("groupSubjectTypeUUID")
                        else {}
                    ),
                    **(
                        {
                            "memberSubjectType": st_uuid_to_name.get(
                                r.get("memberSubjectTypeUUID", ""), ""
                            )
                        }
                        if r.get("memberSubjectTypeUUID")
                        else {}
                    ),
                    **(
                        {"maximumNumberOfMembers": r["maximumNumberOfMembers"]}
                        if r.get("maximumNumberOfMembers")
                        else {}
                    ),
                }
                for r in active_roles
            ]

    # ── Identifier sources ─────────────────────────────────────────────────
    id_sources = bundle.get("identifierSource", [])
    if id_sources:
        active_ids = [s for s in id_sources if not s.get("voided", False)]
        if active_ids:
            entities["identifier_sources"] = [
                {
                    "name": s.get("name", ""),
                    "type": s.get("type", ""),
                    **({"prefix": s["prefix"]} if s.get("prefix") else {}),
                    **({"minLength": s["minLength"]} if s.get("minLength") else {}),
                    **({"maxLength": s["maxLength"]} if s.get("maxLength") else {}),
                    **(
                        {"batchGenerationSize": s["batchGenerationSize"]}
                        if s.get("batchGenerationSize")
                        else {}
                    ),
                }
                for s in active_ids
            ]

    # ── Relationship types ─────────────────────────────────────────────────
    rel_types = bundle.get("relationshipType", [])
    if rel_types:
        active_rels = [r for r in rel_types if not r.get("voided", False)]
        if active_rels:
            entities["relationship_types"] = []
            for rel in active_rels:
                rel_entry: dict = {}
                ind_a = rel.get("individualAIsToBRelation", {})
                ind_b = rel.get("individualBIsToARelation", {})
                if isinstance(ind_a, dict):
                    rel_entry["aIsToB"] = ind_a.get("name", "")
                if isinstance(ind_b, dict):
                    rel_entry["bIsToA"] = ind_b.get("name", "")
                entities["relationship_types"].append(rel_entry)

    # ── Checklists ─────────────────────────────────────────────────────────
    checklists = bundle.get("checklist", [])
    if checklists:
        active_cl = [c for c in checklists if not c.get("voided", False)]
        if active_cl:
            entities["checklists"] = []
            for cl in active_cl:
                cl_entry: dict = {"name": cl.get("name", "")}
                items = cl.get("items", [])
                if items:
                    cl_items = []
                    for item in items:
                        if item.get("voided"):
                            continue
                        concept = item.get("concept", {})
                        item_entry: dict = {
                            "name": concept.get("name", "")
                            if isinstance(concept, dict)
                            else "",
                        }
                        status = item.get("status")
                        if isinstance(status, list):
                            states = [
                                s.get("state", "")
                                for s in status
                                if isinstance(s, dict) and s.get("state")
                            ]
                            if states:
                                item_entry["states"] = states
                        cl_items.append(item_entry)
                    if cl_items:
                        cl_entry["items"] = cl_items
                entities["checklists"].append(cl_entry)

    # ── Videos ─────────────────────────────────────────────────────────────
    videos = bundle.get("video", [])
    if videos:
        active_vids = [v for v in videos if not v.get("voided", False)]
        if active_vids:
            entities["videos"] = [
                {"title": v.get("title", ""), "filePath": v.get("filePath", "")}
                for v in active_vids
            ]

    # ── Documentations ─────────────────────────────────────────────────────
    docs = bundle.get("documentations", [])
    if docs:
        active_docs = [d for d in docs if not d.get("voided", False)]
        if active_docs:
            entities["documentations"] = [
                {"name": d.get("name", ""), "content": d.get("content", "")}
                for d in active_docs[:20]
            ]

    # ── Report cards ───────────────────────────────────────────────────────
    report_cards = bundle.get("reportCard", [])
    if report_cards:
        active_cards = [c for c in report_cards if not c.get("voided", False)]
        if active_cards:
            entities["report_cards"] = [
                {
                    "name": c.get("name", ""),
                    "colour": c.get("colour", c.get("color", "")),
                    "description": c.get("description", ""),
                }
                for c in active_cards
            ]

    # ── Report dashboards ──────────────────────────────────────────────────
    report_dashboards = bundle.get("reportDashboard", [])
    if report_dashboards:
        active_dashes = [d for d in report_dashboards if not d.get("voided", False)]
        if active_dashes:
            entities["report_dashboards"] = [
                {"name": d.get("name", ""), "description": d.get("description", "")}
                for d in active_dashes
            ]

    # ── Menu items ─────────────────────────────────────────────────────────
    menu_items = bundle.get("menuItem", [])
    if menu_items:
        active_mi = [m for m in menu_items if not m.get("voided", False)]
        if active_mi:
            entities["menu_items"] = [
                {
                    "displayKey": m.get("displayKey", ""),
                    "type": m.get("type", ""),
                    **({"icon": m["icon"]} if m.get("icon") else {}),
                    **({"group": m["group"]} if m.get("group") else {}),
                    **(
                        {"linkFunction": m["linkFunction"]}
                        if m.get("linkFunction")
                        else {}
                    ),
                }
                for m in active_mi
            ]

    # ── Message rules ──────────────────────────────────────────────────────
    message_rules = bundle.get("messageRule", [])
    if message_rules:
        active_mr = [m for m in message_rules if not m.get("voided", False)]
        if active_mr:
            entities["message_rules"] = []
            for mr in active_mr:
                mr_entry: dict = {"name": mr.get("name", "")}
                for key in (
                    "entityType",
                    "messageRule",
                    "scheduleRule",
                    "messageTemplateId",
                    "receiverType",
                ):
                    if mr.get(key):
                        mr_entry[key] = mr[key]
                entity_uuid = mr.get("entityTypeUuid")
                if entity_uuid:
                    resolved = (
                        st_uuid_to_name.get(entity_uuid)
                        or prog_uuid_to_name.get(entity_uuid)
                        or enc_uuid_to_name.get(entity_uuid)
                    )
                    if resolved:
                        mr_entry["entityTypeName"] = resolved
                entities["message_rules"].append(mr_entry)

    # ── Group privileges ───────────────────────────────────────────────────
    group_privs = bundle.get("groupPrivilege", [])
    if group_privs:
        grp_uuid_to_name: dict[str, str] = {
            g["uuid"]: g.get("name", "")
            for g in bundle.get("groups", [])
            if g.get("uuid")
        }
        active_gp = [
            g
            for g in group_privs
            if not g.get("voided", False) and g.get("allow", True)
        ]
        if active_gp:
            priv_by_group: dict[str, list] = {}
            for gp in active_gp:
                group_name = gp.get("groupName", "") or grp_uuid_to_name.get(
                    gp.get("groupUUID", ""), "Unknown"
                )
                priv_by_group.setdefault(group_name, []).append(gp)
            entities["group_privileges"] = []
            for group_name, privs in sorted(priv_by_group.items()):
                gp_entry: dict = {"group": group_name, "privileges": []}
                for gp in privs:
                    p: dict = {"type": gp.get("privilegeType", "")}
                    st_name = st_uuid_to_name.get(gp.get("subjectTypeUUID", ""), "")
                    if st_name:
                        p["subjectType"] = st_name
                    prog_name = prog_uuid_to_name.get(gp.get("programUUID", ""), "")
                    if prog_name:
                        p["program"] = prog_name
                    enc_name = enc_uuid_to_name.get(gp.get("encounterTypeUUID", ""), "")
                    if enc_name:
                        p["encounterType"] = enc_name
                    gp_entry["privileges"].append(p)
                entities["group_privileges"].append(gp_entry)

    # ── Group dashboards ───────────────────────────────────────────────────
    group_dashes = bundle.get("groupDashboards", [])
    if group_dashes:
        active_gd = [g for g in group_dashes if not g.get("voided", False)]
        if active_gd:
            entities["group_dashboards"] = [
                {
                    "groupName": gd.get("groupName", ""),
                    "dashboardName": gd.get("dashboardName", ""),
                    **(
                        {"primaryDashboard": True} if gd.get("primaryDashboard") else {}
                    ),
                    **(
                        {"secondaryDashboard": True}
                        if gd.get("secondaryDashboard")
                        else {}
                    ),
                }
                for gd in active_gd
            ]

    # ── Individual relations ───────────────────────────────────────────────
    ind_relations = bundle.get("individualRelation", [])
    if ind_relations:
        active_ir = [r for r in ind_relations if not r.get("voided", False)]
        if active_ir:
            entities["individual_relations"] = []
            for ir in active_ir:
                ir_entry: dict = {"name": ir.get("name", "")}
                genders = ir.get("genders", [])
                if genders:
                    ir_entry["genders"] = [
                        g.get("name", "")
                        for g in genders
                        if isinstance(g, dict) and not g.get("voided", False)
                    ]
                entities["individual_relations"].append(ir_entry)

    # ── Catchments ─────────────────────────────────────────────────────────
    catchments_raw = bundle.get("catchments", [])
    if isinstance(catchments_raw, dict):
        catchments_raw = catchments_raw.get("catchments", [])
    if isinstance(catchments_raw, list) and catchments_raw:
        active_catch = [
            c
            for c in catchments_raw
            if isinstance(c, dict) and not c.get("voided", False)
        ]
        if active_catch:
            entities["catchments"] = [
                {
                    "name": c.get("name", ""),
                    **(
                        {"locationCount": len(c["locations"])}
                        if c.get("locations")
                        else {}
                    ),
                }
                for c in active_catch
            ]

    # ── Locations (summary) ────────────────────────────────────────────────
    locations_raw = bundle.get("locations", [])
    if locations_raw:
        type_counts: dict[str, int] = {}
        for loc in locations_raw:
            loc_type = loc.get("type", "Unknown")
            type_counts[loc_type] = type_counts.get(loc_type, 0) + 1
        entities["locations"] = {
            "totalCount": len(locations_raw),
            "byType": type_counts,
        }

    # ── Concepts (full detail) ─────────────────────────────────────────────
    concepts_raw = bundle.get("concepts", [])
    if concepts_raw:
        active_concepts = [
            c
            for c in concepts_raw
            if c.get("active", True) and not c.get("voided", False)
        ]
        concepts_list = []
        for c in active_concepts:
            dt = c.get("dataType", "NA")
            if dt == "NA" and not c.get("keyValues") and not c.get("answers"):
                continue
            c_entry: dict = {"name": c.get("name", ""), "dataType": dt}
            if c.get("answers"):
                c_entry["answers"] = [
                    a["name"] if isinstance(a, dict) else str(a)
                    for a in c["answers"]
                    if not (isinstance(a, dict) and a.get("voided"))
                ]
            for key in (
                "lowAbsolute",
                "highAbsolute",
                "lowNormal",
                "highNormal",
                "unit",
            ):
                if c.get(key) is not None:
                    c_entry[key] = c[key]
            concepts_list.append(c_entry)
        if concepts_list:
            entities["concepts_detail"] = concepts_list

    # ── Rule dependency ────────────────────────────────────────────────────
    rule_dep = bundle.get("ruleDependency", {})
    if isinstance(rule_dep, dict) and rule_dep.get("code"):
        entities["rule_dependency"] = {
            "hasCode": True,
            "codeLength": len(rule_dep["code"]),
        }

    return entities


# ---------------------------------------------------------------------------
# Spec format reference
# ---------------------------------------------------------------------------

_SPEC_FORMAT_CACHE: dict | None = None


def _load_spec_format() -> dict:
    """Load and parse the comprehensive spec format YAML. Cached after first call."""
    global _SPEC_FORMAT_CACHE
    if _SPEC_FORMAT_CACHE is None:
        from pathlib import Path

        fmt_path = (
            Path(__file__).resolve().parents[2] / "avni-comprehensive-spec-format.yaml"
        )
        if fmt_path.exists():
            _SPEC_FORMAT_CACHE = yaml.safe_load(fmt_path.read_text()) or {}
        else:
            _SPEC_FORMAT_CACHE = {}
    return _SPEC_FORMAT_CACHE


def enrich_spec_with_defaults(spec_yaml: str, sector: str = "") -> dict:
    """
    Enrich a generated spec with smart defaults from the comprehensive format.

    Reads the spec, compares each section against the comprehensive format,
    applies sensible defaults for missing fields, and flags ambiguities that
    need user input.

    Returns:
        {
            "enriched_spec_yaml": str,    # spec with defaults applied
            "defaults_applied": [...],     # what was auto-filled
            "ambiguities": [...],          # questions for the user
        }
    """
    schema = _load_spec_format()
    if not schema:
        return {
            "enriched_spec_yaml": spec_yaml,
            "defaults_applied": [],
            "ambiguities": [],
        }

    try:
        spec = yaml.safe_load(spec_yaml) or {}
    except Exception:
        return {
            "enriched_spec_yaml": spec_yaml,
            "defaults_applied": [],
            "ambiguities": [],
        }

    defaults_applied: list[str] = []
    ambiguities: list[dict] = []
    sector_lower = (sector or "").lower()

    # ── Settings defaults ─────────────────────────────────────────────
    if "settings" not in spec or not spec["settings"]:
        spec["settings"] = {
            "languages": ["en"],
            "enableComments": True,
            "saveDrafts": True,
        }
        defaults_applied.append(
            "Added default settings (languages=en, enableComments, saveDrafts)"
        )

    # ── Subject type defaults ─────────────────────────────────────────
    for st in spec.get("subjectTypes") or []:
        if "lastNameOptional" not in st:
            st["lastNameOptional"] = True
            defaults_applied.append(
                f"subjectType '{st['name']}': set lastNameOptional=true"
            )
        if st.get("type") in ("Group", "Household") and "group" not in st:
            st["group"] = True
            defaults_applied.append(
                f"subjectType '{st['name']}': set group=true (type={st['type']})"
            )
        if st.get("type") == "Household" and "household" not in st:
            st["household"] = True
            defaults_applied.append(f"subjectType '{st['name']}': set household=true")

    # ── Program defaults ──────────────────────────────────────────────
    for prog in spec.get("programs") or []:
        if not prog.get("colour"):
            prog["colour"] = "#4A148C"
            defaults_applied.append(
                f"program '{prog['name']}': set default colour=#4A148C"
            )
        # MCH/Nutrition sector: suggest showGrowthChart
        if (
            sector_lower in ("mch", "nutrition", "child health")
            and "showGrowthChart" not in prog
        ):
            prog_id = prog["name"].lower().replace(" ", "_").replace("-", "_")[:30]
            ambiguities.append(
                {
                    "id": f"prog_{prog_id}_showGrowthChart",
                    "section": "programs",
                    "entity": prog["name"],
                    "field": "showGrowthChart",
                    "question": f"Should program '{prog['name']}' show growth charts? (common for {sector} programs)",
                    "options": ["Yes", "No"],
                    "default": "Yes",
                }
            )

    # ── Encounter type defaults ───────────────────────────────────────
    for enc in spec.get("encounterTypes") or []:
        if "scheduled" not in enc:
            enc["scheduled"] = True
            defaults_applied.append(
                f"encounterType '{enc['name']}': set scheduled=true"
            )
        # Ambiguity: encounter without subject type
        if not enc.get("subjectType") and not enc.get("program"):
            st_names = [s["name"] for s in spec.get("subjectTypes") or []]
            if st_names:
                enc_id = enc["name"].lower().replace(" ", "_").replace("-", "_")[:30]
                ambiguities.append(
                    {
                        "id": f"spec_enc_{enc_id}_subjectType",
                        "section": "encounterTypes",
                        "entity": enc["name"],
                        "field": "subjectType",
                        "question": f"Which subject type does encounter '{enc['name']}' belong to?",
                        "options": st_names,
                        "default": st_names[0],
                    }
                )
        # Ambiguity: program encounter without program
        if enc.get("program") == "" or (
            not enc.get("program") and enc.get("scheduled")
        ):
            prog_names = [p["name"] for p in spec.get("programs") or []]
            if prog_names and not enc.get("subjectType"):
                enc_id = enc["name"].lower().replace(" ", "_").replace("-", "_")[:30]
                ambiguities.append(
                    {
                        "id": f"spec_enc_{enc_id}_program",
                        "section": "encounterTypes",
                        "entity": enc["name"],
                        "field": "program",
                        "question": f"Does encounter '{enc['name']}' belong to a program? If yes, which one?",
                        "options": ["No program (general encounter)"] + prog_names,
                        "default": "No program (general encounter)",
                    }
                )

    # ── Groups default ────────────────────────────────────────────────
    if not spec.get("groups"):
        spec["groups"] = [{"name": "Everyone"}]
        defaults_applied.append("Added default group 'Everyone'")

    enriched_yaml = yaml.dump(
        spec, allow_unicode=True, default_flow_style=False, sort_keys=False
    )
    return {
        "enriched_spec_yaml": enriched_yaml,
        "defaults_applied": defaults_applied,
        "ambiguities": ambiguities,
    }


async def handle_enrich_spec(request: Request) -> JSONResponse:
    """
    POST /enrich-spec
    Body: { "conversation_id": "...", "sector": "MCH" }

    Reads the stored spec, applies smart defaults from the comprehensive format,
    and returns a list of defaults applied + ambiguities needing user input.
    The enriched spec is stored back (replaces the original).
    """
    try:
        body = await request.json()
    except Exception:
        return JSONResponse({"error": "Invalid JSON body"}, status_code=400)

    conversation_id = body.get("conversation_id")
    if not conversation_id:
        return JSONResponse({"error": "Missing conversation_id"}, status_code=400)

    spec_yaml = _spec_store.get(conversation_id)
    if spec_yaml is None:
        return JSONResponse(
            {"error": f"No stored spec for conversation_id={conversation_id}"},
            status_code=404,
        )

    sector = body.get("sector", "")
    result = enrich_spec_with_defaults(spec_yaml, sector)

    # Store enriched spec back
    _spec_store.put(conversation_id, result["enriched_spec_yaml"])
    logger.info(
        "enrich-spec: conversation_id=%s defaults=%d ambiguities=%d",
        conversation_id,
        len(result["defaults_applied"]),
        len(result["ambiguities"]),
    )

    return JSONResponse(
        {
            "enriched": True,
            "defaults_applied": result["defaults_applied"],
            "ambiguities": result["ambiguities"],
            "has_ambiguities": len(result["ambiguities"]) > 0,
        }
    )


async def handle_get_spec_format(request: Request) -> JSONResponse:
    """
    GET /spec-format?section=subjectTypes
    Returns the comprehensive YAML spec reference schema.

    Without section param: returns all top-level section names + the full schema.
    With section param: returns just that section's reference (e.g. subjectTypes
    with all valid fields, or 'fields' for the field-level reference).
    """
    spec_format = _load_spec_format()
    if not spec_format:
        return JSONResponse(
            {"error": "avni-comprehensive-spec-format.yaml not found"},
            status_code=404,
        )

    section = request.query_params.get("section")
    if not section:
        return JSONResponse(
            {
                "sections": list(spec_format.keys()),
                "spec_format": yaml.dump(
                    spec_format,
                    allow_unicode=True,
                    default_flow_style=False,
                    sort_keys=False,
                ),
            }
        )

    # Special case: 'fields' returns the field-level reference from within
    # subjectTypes → registrationForm → sections → fields
    if section == "fields":
        st_list = spec_format.get("subjectTypes", [])
        if st_list and isinstance(st_list, list):
            reg_form = st_list[0].get("registrationForm", {})
            sections = reg_form.get("sections", [])
            if sections:
                field_ref = sections[0].get("fields", [])
                if field_ref:
                    return JSONResponse(
                        {
                            "section": "fields",
                            "reference": yaml.dump(
                                {"fields": field_ref},
                                allow_unicode=True,
                                default_flow_style=False,
                                sort_keys=False,
                            ),
                        }
                    )
        return JSONResponse({"error": "No field reference found"}, status_code=404)

    if section not in spec_format:
        return JSONResponse(
            {
                "error": f"Unknown section '{section}'",
                "valid_sections": list(spec_format.keys()) + ["fields"],
            },
            status_code=404,
        )

    return JSONResponse(
        {
            "section": section,
            "reference": yaml.dump(
                {section: spec_format[section]},
                allow_unicode=True,
                default_flow_style=False,
                sort_keys=False,
            ),
        }
    )
