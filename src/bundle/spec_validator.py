"""
spec_validator.py — deterministic YAML spec validation

All structural, cross-reference, and completeness checks from
avni-ai-iterative-dev-plan.md § YAML Spec Validator.

Returns: {"valid": bool, "errors": [...], "warnings": [...], "suggestions": [...]}
"""

from __future__ import annotations

from typing import Any

import yaml


VALID_SUBJECT_TYPES = {"Person", "Household", "Individual", "Group"}
VALID_DATA_TYPES = {
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
VALID_STANDARD_CARD_TYPES = {
    "scheduledVisits",
    "overdueVisits",
    "total",
    "recentRegistrations",
    "recentEnrolments",
    "recentVisits",
}


def validate_spec(spec_yaml: str) -> dict[str, Any]:
    """
    Validate a YAML spec string.
    Returns {valid, errors, warnings, suggestions}.
    """
    errors: list[str] = []
    warnings: list[str] = []
    suggestions: list[str] = []

    # Parse YAML
    try:
        spec = yaml.safe_load(spec_yaml)
    except yaml.YAMLError as exc:
        return {
            "valid": False,
            "errors": [f"YAML parse error: {exc}"],
            "warnings": [],
            "suggestions": [],
        }

    if not isinstance(spec, dict):
        return {
            "valid": False,
            "errors": ["Spec must be a YAML mapping (dict)"],
            "warnings": [],
            "suggestions": [],
        }

    # Build name sets for cross-reference
    st_names = {
        s["name"]
        for s in spec.get("subjectTypes", [])
        if isinstance(s, dict) and s.get("name")
    }
    prog_names = {
        p["name"]
        for p in spec.get("programs", [])
        if isinstance(p, dict) and p.get("name")
    }
    enc_names = {
        e["name"]
        for e in spec.get("encounterTypes", [])
        if isinstance(e, dict) and e.get("name")
    }
    group_names = {
        g["name"]
        for g in spec.get("groups", [])
        if isinstance(g, dict) and g.get("name")
    }
    card_names = {
        c["name"]
        for c in spec.get("reportCards", [])
        if isinstance(c, dict) and c.get("name")
    }

    # ── Completeness ───────────────────────────────────────────────
    if not st_names:
        errors.append(
            "No subject types defined — at least one subject type is required"
        )

    if not group_names:
        warnings.append(
            "No groups defined — an 'Everyone' group will be auto-generated"
        )

    addr_levels = spec.get("addressLevels", [])
    if not addr_levels:
        warnings.append(
            "No address levels defined — a default hierarchy will be generated"
        )

    # ── Address levels ─────────────────────────────────────────────
    seen_level_names: set[str] = set()
    level_name_map: dict[str, int] = {}
    for row in addr_levels:
        if not isinstance(row, dict):
            continue
        name = row.get("name", "")
        if not name:
            errors.append("Address level entry missing 'name'")
            continue
        if name.lower() in {n.lower() for n in seen_level_names}:
            errors.append(f"Duplicate address level name: '{name}'")
        seen_level_names.add(name)
        level_name_map[name] = row.get("level", 0)

        parent = row.get("parent")
        if (
            parent
            and parent not in seen_level_names
            and parent not in {r.get("name") for r in addr_levels}
        ):
            errors.append(
                f"Address level '{name}' references unknown parent '{parent}'"
            )

    # ── Subject types ──────────────────────────────────────────────
    seen_st: set[str] = set()
    for st in spec.get("subjectTypes", []):
        if not isinstance(st, dict):
            continue
        name = st.get("name", "")
        if not name:
            errors.append("Subject type entry missing 'name'")
            continue
        if name.lower() in {n.lower() for n in seen_st}:
            errors.append(f"Duplicate subject type: '{name}'")
        seen_st.add(name)

        st_type = st.get("type", "")
        if st_type and st_type not in VALID_SUBJECT_TYPES:
            warnings.append(
                f"Subject type '{name}' has unrecognised type '{st_type}' "
                f"(expected one of {sorted(VALID_SUBJECT_TYPES)})"
            )

        if "registrationForm" in st:
            _validate_form_spec(
                st["registrationForm"],
                f"registrationForm of '{name}'",
                errors,
                warnings,
            )

    # ── Programs ───────────────────────────────────────────────────
    seen_prog: set[str] = set()
    for prog in spec.get("programs", []):
        if not isinstance(prog, dict):
            continue
        name = prog.get("name", "")
        if not name:
            errors.append("Program entry missing 'name'")
            continue
        if name.lower() in {n.lower() for n in seen_prog}:
            errors.append(f"Duplicate program: '{name}'")
        seen_prog.add(name)

        target = prog.get("targetSubjectType", "")
        if not target:
            warnings.append(f"Program '{name}' missing 'targetSubjectType'")
        elif not _fuzzy_match(target, st_names):
            errors.append(
                f"Program '{name}' targetSubjectType '{target}' does not match any defined subject type"
            )

        if "enrolmentForm" not in prog:
            warnings.append(f"Program '{name}' has no enrolmentForm")
        else:
            _validate_form_spec(
                prog["enrolmentForm"], f"enrolmentForm of '{name}'", errors, warnings
            )

        if "exitForm" in prog:
            _validate_form_spec(
                prog["exitForm"], f"exitForm of '{name}'", errors, warnings
            )

    # ── Encounter types ────────────────────────────────────────────
    seen_enc: set[str] = set()
    for enc in spec.get("encounterTypes", []):
        if not isinstance(enc, dict):
            continue
        name = enc.get("name", "")
        if not name:
            errors.append("Encounter type entry missing 'name'")
            continue
        if name.lower() in {n.lower() for n in seen_enc}:
            errors.append(f"Duplicate encounter type: '{name}'")
        seen_enc.add(name)

        program = enc.get("program", "")
        subject = enc.get("subjectType", "")

        if program and not _fuzzy_match(program, prog_names):
            errors.append(
                f"Encounter type '{name}' references unknown program '{program}'"
            )
        if subject and not _fuzzy_match(subject, st_names):
            errors.append(
                f"Encounter type '{name}' references unknown subject type '{subject}'"
            )
        if not subject:
            errors.append(
                f"Encounter type '{name}' has no 'subjectType' — Avni requires every encounter to be linked to a subject type"
            )
        if program and not subject:
            errors.append(
                f"Encounter type '{name}' has program '{program}' but no 'subjectType' — both are required for program encounters"
            )
        if not program and enc.get("scheduled") and subject:
            # Scheduled encounter without a program — likely should be a ProgramEncounter
            warnings.append(
                f"Encounter type '{name}' is scheduled but has no 'program' — should this be a program encounter?"
            )

        if "form" not in enc:
            warnings.append(f"Encounter type '{name}' has no form")
        else:
            _validate_form_spec(
                enc["form"], f"form of encounter '{name}'", errors, warnings
            )

        if "cancellationForm" in enc:
            _validate_form_spec(
                enc["cancellationForm"],
                f"cancellationForm of '{name}'",
                errors,
                warnings,
            )

    # ── Report cards ───────────────────────────────────────────────
    seen_cards: set[str] = set()
    for card in spec.get("reportCards", []):
        if not isinstance(card, dict):
            continue
        cname = card.get("name", "")
        if not cname:
            errors.append("Report card entry missing 'name'")
            continue
        if cname.lower() in {n.lower() for n in seen_cards}:
            errors.append(f"Duplicate report card name: '{cname}'")
        seen_cards.add(cname)

        std_type = card.get("standardType", "")
        if (
            card.get("type") == "standard"
            and std_type
            and std_type not in VALID_STANDARD_CARD_TYPES
        ):
            errors.append(
                f"Report card '{cname}' has unknown standardType '{std_type}' "
                f"(valid: {sorted(VALID_STANDARD_CARD_TYPES)})"
            )

    # ── Dashboard ──────────────────────────────────────────────────
    for dash in spec.get("dashboard", []):
        if not isinstance(dash, dict):
            continue
        dash_name = dash.get("name", "dashboard")
        for section in dash.get("sections", []):
            if not isinstance(section, dict):
                continue
            for card_ref in section.get("cards", []):
                if card_ref not in card_names and card_ref not in seen_cards:
                    errors.append(
                        f"Dashboard '{dash_name}' references unknown report card '{card_ref}'"
                    )

    # ── Suggestions ────────────────────────────────────────────────
    if st_names and not prog_names:
        suggestions.append(
            "No programs defined — consider adding at least one program for a subject type"
        )
    if prog_names and not enc_names:
        suggestions.append(
            "Programs defined but no encounter types — add encounter types for data collection"
        )
    if not spec.get("reportCards"):
        suggestions.append(
            "No report cards defined — standard report cards will be auto-generated"
        )

    # ── Schema-driven field validation ───────────────────────────────
    _validate_against_schema(spec, warnings)

    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings,
        "suggestions": suggestions,
    }


def _fuzzy_match(name: str, known: set[str]) -> bool:
    lower = name.strip().lower()
    for k in known:
        if lower == k.lower() or lower in k.lower() or k.lower() in lower:
            return True
    return False


def _validate_form_spec(form: dict, label: str, errors: list, warnings: list) -> None:
    """Validate a single form spec (sections+fields)."""
    if not isinstance(form, dict):
        errors.append(f"{label}: form spec must be a mapping")
        return

    sections = form.get("sections", [])
    if not sections:
        warnings.append(f"{label}: has no sections")
        return

    for sidx, section in enumerate(sections, 1):
        if not isinstance(section, dict):
            continue
        fields = section.get("fields", [])
        if not fields:
            warnings.append(
                f"{label} section {sidx} ('{section.get('name', '?')}') has no fields"
            )
            continue

        all_field_names: list[str] = []
        for field in fields:
            if not isinstance(field, dict):
                continue
            fname = field.get("name", "")
            if not fname:
                errors.append(
                    f"{label}: field missing 'name' in section '{section.get('name', '?')}'"
                )
            all_field_names.append(fname)

            data_type = field.get("dataType", "")
            if data_type and data_type not in VALID_DATA_TYPES:
                warnings.append(
                    f"{label}: field '{fname}' has unrecognised dataType '{data_type}'"
                )

            if data_type == "Coded" and not field.get("options"):
                warnings.append(
                    f"{label}: Coded field '{fname}' has no options defined"
                )

            skip = field.get("skipLogic")
            if skip and isinstance(skip, dict):
                dep = skip.get("dependsOn", "")
                if dep and dep not in all_field_names:
                    warnings.append(
                        f"{label}: field '{fname}' skipLogic.dependsOn '{dep}' "
                        "references a field not yet seen in this section"
                    )


def _load_schema() -> dict:
    """Load the comprehensive spec format as a schema reference."""
    try:
        from ..handlers.spec_handlers import _load_spec_format

        return _load_spec_format()
    except Exception:
        return {}


def _validate_against_schema(spec: dict, warnings: list[str]) -> None:
    """Check spec fields against the comprehensive format schema.

    Flags unknown field names (likely LLM hallucinations or typos) as warnings.
    """
    schema = _load_schema()
    if not schema:
        return

    # Build valid field sets per section from schema examples
    valid_fields: dict[str, set[str]] = {}
    for section_name, section_val in schema.items():
        if (
            isinstance(section_val, list)
            and section_val
            and isinstance(section_val[0], dict)
        ):
            valid_fields[section_name] = set(section_val[0].keys())
        elif isinstance(section_val, dict):
            valid_fields[section_name] = set(section_val.keys())

    # Check each section in the spec
    sections_to_check = [
        ("subjectTypes", "subjectTypes"),
        ("programs", "programs"),
        ("encounterTypes", "encounterTypes"),
        ("addressLevels", "addressLevels"),
        ("groupRoles", "groupRoles"),
        ("identifierSources", "identifierSources"),
        ("relationshipTypes", "relationshipTypes"),
        ("reportCards", "reportCards"),
        ("reportDashboards", "reportDashboards"),
    ]

    for spec_key, schema_key in sections_to_check:
        schema_fields = valid_fields.get(schema_key)
        if not schema_fields:
            continue
        items = spec.get(spec_key, [])
        if not isinstance(items, list):
            continue
        for item in items:
            if not isinstance(item, dict):
                continue
            entity_name = item.get("name", "?")
            for field_name in item:
                if field_name not in schema_fields:
                    warnings.append(
                        f"{spec_key} '{entity_name}': unknown field '{field_name}' "
                        f"(valid fields: {sorted(schema_fields)})"
                    )

    # Check top-level sections
    valid_sections = set(schema.keys())
    for key in spec:
        if key not in valid_sections:
            warnings.append(
                f"Unknown top-level section '{key}' "
                f"(valid sections: {sorted(valid_sections)})"
            )
