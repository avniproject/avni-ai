"""
spec_generator.py — entities dict → YAML spec

Converts the internal entities representation (as extracted by the LLM)
into the human-readable YAML spec format defined in avni-ai-iterative-dev-plan.md.
"""

from __future__ import annotations

import logging
from typing import Any

import yaml

from ..schemas.bundle_models import EntitySpec

logger = logging.getLogger(__name__)


def entities_to_spec(entities: dict[str, Any], org_name: str = "") -> str:
    """
    Convert entities dict to YAML spec string.

    entities keys: subject_types, programs, encounter_types, address_levels,
                   groups, forms (optional)
    """
    # Validate through EntitySpec — catches duplicates and cross-ref errors before YAML generation
    try:
        EntitySpec(
            subject_types=entities.get("subject_types", []),
            programs=entities.get("programs", []),
            encounter_types=entities.get("encounter_types", []),
            address_levels=entities.get("address_levels", []),
            groups=entities.get("groups", []),
        )
    except ValueError as exc:
        logger.warning("entities_to_spec: EntitySpec validation failed: %s", exc)
        raise

    spec: dict[str, Any] = {}

    spec["org"] = org_name or "Unknown Organization"

    spec["settings"] = {"languages": ["en"], "enableComments": True}

    # Address levels
    addr_rows = entities.get("address_levels", [])
    if addr_rows:
        sorted_levels = sorted(addr_rows, key=lambda r: -r.get("level", 0))
        spec["addressLevels"] = []
        for row in sorted_levels:
            entry: dict[str, Any] = {
                "name": row["name"],
                "level": row.get("level", 1),
            }
            if row.get("parent"):
                entry["parent"] = row["parent"]
            spec["addressLevels"].append(entry)

    # Subject types
    st_rows = entities.get("subject_types", [])
    if st_rows:
        spec["subjectTypes"] = []
        for st in st_rows:
            st_spec: dict[str, Any] = {
                "name": st["name"],
                "type": st.get("type", "Person"),
            }
            if st.get("allowProfilePicture") is not None:
                st_spec["allowProfilePicture"] = st["allowProfilePicture"]
            if st.get("uniqueName") is not None:
                st_spec["uniqueName"] = st["uniqueName"]
            # Attach registration form if present in forms
            reg_form = _find_form(
                entities.get("forms", []), "IndividualProfile", st["name"]
            )
            if reg_form:
                st_spec["registrationForm"] = _form_to_spec(reg_form)
            spec["subjectTypes"].append(st_spec)

    # Programs
    prog_rows = entities.get("programs", [])
    if prog_rows:
        spec["programs"] = []
        for prog in prog_rows:
            prog_spec: dict[str, Any] = {
                "name": prog["name"],
                "targetSubjectType": prog.get("target_subject_type", ""),
            }
            if prog.get("colour"):
                prog_spec["colour"] = prog["colour"]
            if prog.get("allow_multiple_enrolments") is not None:
                prog_spec["allowMultipleEnrolments"] = prog["allow_multiple_enrolments"]
            enrolment_form = _find_form(
                entities.get("forms", []),
                "ProgramEnrolment",
                subject_type=None,
                program=prog["name"],
            )
            if enrolment_form:
                prog_spec["enrolmentForm"] = _form_to_spec(enrolment_form)
            exit_form = _find_form(
                entities.get("forms", []),
                "ProgramExit",
                subject_type=None,
                program=prog["name"],
            )
            if exit_form:
                prog_spec["exitForm"] = _form_to_spec(exit_form)
            spec["programs"].append(prog_spec)

    # Encounter types
    enc_rows = entities.get("encounter_types", [])
    if enc_rows:
        spec["encounterTypes"] = []
        for enc in enc_rows:
            enc_spec: dict[str, Any] = {"name": enc["name"]}
            if enc.get("program_name"):
                enc_spec["program"] = enc["program_name"]
            if enc.get("subject_type"):
                enc_spec["subjectType"] = enc["subject_type"]
            enc_spec["scheduled"] = bool(enc.get("is_scheduled", True))
            form_type = (
                "ProgramEncounter" if enc.get("is_program_encounter") else "Encounter"
            )
            enc_form = _find_form(
                entities.get("forms", []),
                form_type,
                enc.get("subject_type"),
                enc.get("program_name"),
                enc["name"],
            )
            if enc_form:
                enc_spec["form"] = _form_to_spec(enc_form)
            cancel_form = _find_form(
                entities.get("forms", []),
                "ProgramEncounterCancellation",
                enc.get("subject_type"),
                enc.get("program_name"),
                enc["name"],
            )
            if cancel_form:
                enc_spec["cancellationForm"] = _form_to_spec(cancel_form)
            spec["encounterTypes"].append(enc_spec)

    # Groups
    groups = entities.get("groups", [])
    if groups:
        spec["groups"] = [
            {
                "name": g["name"],
                "hasAllPrivileges": g.get("has_all_privileges", False),
            }
            for g in groups
        ]
    else:
        spec["groups"] = [{"name": "Everyone", "hasAllPrivileges": False}]

    return yaml.dump(
        spec, allow_unicode=True, default_flow_style=False, sort_keys=False
    )


def _find_form(
    forms: list[dict],
    form_type: str,
    subject_type: str | None = None,
    program: str | None = None,
    encounter_type: str | None = None,
) -> dict | None:
    for form in forms:
        if form.get("formType") != form_type:
            continue
        if subject_type and form.get("subjectType") != subject_type:
            continue
        if program and form.get("program") != program:
            continue
        if encounter_type and form.get("encounterType") != encounter_type:
            continue
        return form
    return None


def _form_to_spec(form: dict) -> dict:
    """Convert internal form dict to spec-format form dict.

    Handles two input formats:
    1. Bundle format: form has 'formElementGroups' with 'formElements'
    2. Parser format: form has 'sections' with 'fields' (from scoping_parser)
       or flat 'fields' list with optional 'group' on each field
    """
    form_spec: dict[str, Any] = {}
    sections: list[dict] = []

    # Format 1: Bundle format (formElementGroups)
    if form.get("formElementGroups"):
        for group in form["formElementGroups"]:
            section: dict[str, Any] = {"name": group.get("name", "Details")}
            fields = []
            for fe in group.get("formElements", []):
                field: dict[str, Any] = {"name": fe["name"]}
                if fe.get("dataType"):
                    field["dataType"] = fe["dataType"]
                if fe.get("mandatory"):
                    field["mandatory"] = fe["mandatory"]
                if fe.get("unit"):
                    field["unit"] = fe["unit"]
                concept = fe.get("concept", {})
                if isinstance(concept, dict):
                    if concept.get("lowAbsolute") is not None:
                        field["min"] = concept["lowAbsolute"]
                    if concept.get("hiAbsolute") is not None:
                        field["max"] = concept["hiAbsolute"]
                    if concept.get("answers"):
                        field["options"] = [
                            a["name"] if isinstance(a, dict) else a
                            for a in concept["answers"]
                        ]
                fields.append(field)
            if fields:
                section["fields"] = fields
            sections.append(section)

    # Format 2: Parser format (sections with fields, or flat fields)
    elif form.get("sections"):
        for sec in form["sections"]:
            section = {"name": sec.get("name", "Details")}
            fields = []
            for f in sec.get("fields", []):
                field = _field_dict_to_spec(f)
                if field:
                    fields.append(field)
            if fields:
                section["fields"] = fields
                sections.append(section)

    elif form.get("fields"):
        # Flat fields — group by 'group' attribute
        grouped: dict[str, list] = {}
        for f in form["fields"]:
            group_name = f.get("group", "Details") or "Details"
            grouped.setdefault(group_name, []).append(f)
        for group_name, field_list in grouped.items():
            section = {"name": group_name}
            fields = [_field_dict_to_spec(f) for f in field_list]
            fields = [f for f in fields if f]
            if fields:
                section["fields"] = fields
                sections.append(section)

    if sections:
        form_spec["sections"] = sections
    return form_spec


def _field_dict_to_spec(f: dict) -> dict | None:
    """Convert a raw field dict (from scoping parser) to spec field format."""
    name = f.get("name", "")
    if not name:
        return None
    field: dict[str, Any] = {"name": name}
    if f.get("dataType"):
        field["dataType"] = f["dataType"]
    if f.get("mandatory"):
        field["mandatory"] = f["mandatory"]
    if f.get("unit"):
        field["unit"] = f["unit"]
    if f.get("min") is not None:
        field["min"] = f["min"]
    if f.get("max") is not None:
        field["max"] = f["max"]
    if f.get("options"):
        field["options"] = f["options"]
    if f.get("selectionType"):
        field["selectionType"] = f["selectionType"]
    return field
