"""
spec_parser.py — YAML spec → entities dict with full forms+fields

Parses the human-readable YAML spec (see avni-ai-iterative-dev-plan.md)
and returns an entities dict that can be fed directly into BundleGenerator.generate().
"""

from __future__ import annotations

from typing import Any

import yaml


def spec_to_entities(spec_yaml: str) -> dict[str, Any]:
    """
    Parse YAML spec string and return full entities dict.

    Returns:
        {
          org_name: str,
          subject_types: [...],
          programs: [...],
          encounter_types: [...],
          address_levels: [...],
          groups: [...],
          forms: [...],
        }
    """
    try:
        spec = yaml.safe_load(spec_yaml)
    except yaml.YAMLError as exc:
        raise ValueError(f"Invalid YAML: {exc}") from exc

    if not isinstance(spec, dict):
        raise ValueError("Spec must be a YAML mapping")

    entities: dict[str, Any] = {
        "org_name": spec.get("org", ""),
        "subject_types": [],
        "programs": [],
        "encounter_types": [],
        "address_levels": [],
        "groups": [],
        "forms": [],
    }

    # Address levels
    for row in spec.get("addressLevels", []):
        entities["address_levels"].append(
            {
                "name": row["name"],
                "level": row.get("level", 1),
                "parent": row.get("parent"),
            }
        )

    # Subject types
    for st in spec.get("subjectTypes", []):
        entities["subject_types"].append(
            {
                "name": st["name"],
                "type": st.get("type", "Person"),
                "allowProfilePicture": st.get("allowProfilePicture", False),
                "uniqueName": st.get("uniqueName", False),
                "lastNameOptional": st.get("lastNameOptional", True),
            }
        )
        if "registrationForm" in st:
            entities["forms"].append(
                _parse_form(st["registrationForm"], "IndividualProfile", st["name"])
            )

    # Programs
    for prog in spec.get("programs", []):
        entities["programs"].append(
            {
                "name": prog["name"],
                "target_subject_type": prog.get("targetSubjectType", ""),
                "colour": prog.get("colour", "#4A148C"),
                "allow_multiple_enrolments": prog.get("allowMultipleEnrolments", False),
            }
        )
        if "enrolmentForm" in prog:
            entities["forms"].append(
                _parse_form(
                    prog["enrolmentForm"], "ProgramEnrolment", program=prog["name"]
                )
            )
        if "exitForm" in prog:
            entities["forms"].append(
                _parse_form(prog["exitForm"], "ProgramExit", program=prog["name"])
            )

    # Encounter types
    for enc in spec.get("encounterTypes", []):
        is_program_enc = bool(enc.get("program"))
        entities["encounter_types"].append(
            {
                "name": enc["name"],
                "program_name": enc.get("program", ""),
                "subject_type": enc.get("subjectType", ""),
                "is_program_encounter": is_program_enc,
                "is_scheduled": enc.get("scheduled", True),
            }
        )
        form_type = "ProgramEncounter" if is_program_enc else "Encounter"
        if "form" in enc:
            entities["forms"].append(
                _parse_form(
                    enc["form"],
                    form_type,
                    subject_type=enc.get("subjectType"),
                    program=enc.get("program"),
                    encounter_type=enc["name"],
                )
            )
        if "cancellationForm" in enc:
            entities["forms"].append(
                _parse_form(
                    enc["cancellationForm"],
                    "ProgramEncounterCancellation",
                    subject_type=enc.get("subjectType"),
                    program=enc.get("program"),
                    encounter_type=enc["name"],
                )
            )

    # Groups
    for grp in spec.get("groups", []):
        entities["groups"].append(
            {
                "name": grp["name"],
                "has_all_privileges": grp.get("hasAllPrivileges", False),
            }
        )
    if not entities["groups"]:
        entities["groups"] = [{"name": "Everyone", "has_all_privileges": False}]

    return entities


def _parse_form(
    form_spec: dict,
    form_type: str,
    subject_type: str | None = None,
    program: str | None = None,
    encounter_type: str | None = None,
) -> dict:
    """Convert spec form dict to internal form dict with formElementGroups."""
    groups = []
    for idx, section in enumerate(form_spec.get("sections", []), 1):
        elements = []
        for fidx, field in enumerate(section.get("fields", []), 1):
            field_name = field["name"] if isinstance(field, dict) else field
            data_type = (
                field.get("dataType", "Text") if isinstance(field, dict) else "Text"
            )
            elem: dict[str, Any] = {
                "name": field_name,
                "displayOrder": float(fidx),
                "mandatory": field.get("mandatory", False)
                if isinstance(field, dict)
                else False,
                "dataType": data_type,
                "concept": _build_concept(field if isinstance(field, dict) else {}),
            }
            if isinstance(field, dict) and field.get("unit"):
                elem["unit"] = field["unit"]
            if isinstance(field, dict) and field.get("skipLogic"):
                elem["skipLogic"] = field["skipLogic"]
            elements.append(elem)

        groups.append(
            {
                "name": section.get("name", f"Section {idx}"),
                "displayOrder": float(idx),
                "formElements": elements,
            }
        )

    form_name_parts = filter(None, [form_type, subject_type, program, encounter_type])
    form_name = " - ".join(form_name_parts)

    return {
        "name": form_name,
        "formType": form_type,
        "subjectType": subject_type,
        "program": program,
        "encounterType": encounter_type,
        "formElementGroups": groups,
        "fields": [],
    }


def _build_concept(field: dict) -> dict:
    """Build concept object from field spec."""
    concept: dict[str, Any] = {"name": field.get("name", "")}
    data_type = field.get("dataType", "Text")
    concept["dataType"] = data_type

    if data_type == "Numeric":
        if field.get("min") is not None:
            concept["lowAbsolute"] = field["min"]
        if field.get("max") is not None:
            concept["hiAbsolute"] = field["max"]
        if field.get("unit"):
            concept["unit"] = field["unit"]

    if data_type == "Coded" and field.get("options"):
        concept["answers"] = [{"name": opt} for opt in field["options"]]

    return concept
