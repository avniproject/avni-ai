"""
spec_generator.py — entities dict → YAML spec

Converts the internal entities representation (as extracted by the LLM)
into the human-readable YAML spec format defined in avni-ai-iterative-dev-plan.md.

Comprehensive format: captures all real-world patterns found across 21+ org bundles.
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
                   groups, forms (optional), settings (optional),
                   identifier_sources, relationship_types, group_roles,
                   checklists, videos, documentations, custom_queries,
                   report_cards, report_dashboards
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

    # Settings — use provided settings or defaults
    settings = entities.get("settings", {})
    if not settings:
        settings = {"languages": ["en"], "enableComments": True}
    spec["settings"] = settings

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
            # Comprehensive subject type fields
            if st.get("group"):
                st_spec["group"] = True
            if st.get("household"):
                st_spec["household"] = True
            if st.get("allowProfilePicture"):
                st_spec["allowProfilePicture"] = True
            if st.get("uniqueName"):
                st_spec["uniqueName"] = True
            if st.get("allowEmptyLocation"):
                st_spec["allowEmptyLocation"] = True
            if st.get("allowMiddleName"):
                st_spec["allowMiddleName"] = True
            if st.get("lastNameOptional") is False:
                st_spec["lastNameOptional"] = False
            if st.get("validFirstNameFormat"):
                st_spec["validFirstNameFormat"] = st["validFirstNameFormat"]
            if st.get("iconFileS3Key"):
                st_spec["iconFileS3Key"] = st["iconFileS3Key"]
            if st.get("subjectSummaryRule"):
                st_spec["subjectSummaryRule"] = st["subjectSummaryRule"]
            if st.get("programEligibilityCheckRule"):
                st_spec["programEligibilityCheckRule"] = st["programEligibilityCheckRule"]
            if st.get("syncRegistrationConcept1"):
                st_spec["syncRegistrationConcept1"] = st["syncRegistrationConcept1"]
            if st.get("syncRegistrationConcept1Usable"):
                st_spec["syncRegistrationConcept1Usable"] = st["syncRegistrationConcept1Usable"]
            if st.get("memberAdditionEligibilityCheckRule"):
                st_spec["memberAdditionEligibilityCheckRule"] = st["memberAdditionEligibilityCheckRule"]
            st_settings = st.get("settings")
            if isinstance(st_settings, dict) and st_settings:
                st_spec["settings"] = st_settings

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
            if prog.get("allow_multiple_enrolments"):
                prog_spec["allowMultipleEnrolments"] = True
            if prog.get("programSubjectLabel"):
                prog_spec["programSubjectLabel"] = prog["programSubjectLabel"]
            if prog.get("enrolmentSummaryRule"):
                prog_spec["enrolmentSummaryRule"] = prog["enrolmentSummaryRule"]
            if prog.get("enrolmentEligibilityCheckRule"):
                prog_spec["enrolmentEligibilityCheckRule"] = prog["enrolmentEligibilityCheckRule"]
            if prog.get("manualEnrolmentEligibilityCheckRule"):
                prog_spec["manualEnrolmentEligibilityCheckRule"] = prog["manualEnrolmentEligibilityCheckRule"]
            if prog.get("enrolmentEligibilityCheckDeclarativeRule"):
                prog_spec["enrolmentEligibilityCheckDeclarativeRule"] = prog["enrolmentEligibilityCheckDeclarativeRule"]
            if prog.get("showGrowthChart"):
                prog_spec["showGrowthChart"] = True

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
            if enc.get("encounterEligibilityCheckRule"):
                enc_spec["encounterEligibilityCheckRule"] = enc["encounterEligibilityCheckRule"]
            if enc.get("entityEligibilityCheckDeclarativeRule"):
                enc_spec["entityEligibilityCheckDeclarativeRule"] = enc["entityEligibilityCheckDeclarativeRule"]
            if enc.get("immutable"):
                enc_spec["immutable"] = True
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
            if not cancel_form:
                cancel_form = _find_form(
                    entities.get("forms", []),
                    "IndividualEncounterCancellation",
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
                **({"hasAllPrivileges": True} if g.get("has_all_privileges") else {}),
            }
            for g in groups
        ]
    else:
        spec["groups"] = [{"name": "Everyone"}]

    # Group roles
    group_roles = entities.get("group_roles", [])
    if group_roles:
        spec["groupRoles"] = group_roles

    # Identifier sources
    id_sources = entities.get("identifier_sources", [])
    if id_sources:
        spec["identifierSources"] = id_sources

    # Relationship types
    rel_types = entities.get("relationship_types", [])
    if rel_types:
        spec["relationshipTypes"] = rel_types

    # Checklists
    checklists = entities.get("checklists", [])
    if checklists:
        spec["checklists"] = checklists

    # Videos
    videos = entities.get("videos", [])
    if videos:
        spec["videos"] = videos

    # Documentations
    docs = entities.get("documentations", [])
    if docs:
        spec["documentations"] = docs

    # Custom queries
    custom_queries = entities.get("custom_queries", [])
    if custom_queries:
        spec["customQueries"] = custom_queries

    # Report cards
    report_cards = entities.get("report_cards", [])
    if report_cards:
        spec["reportCards"] = report_cards

    # Report dashboards
    report_dashboards = entities.get("report_dashboards", [])
    if report_dashboards:
        spec["reportDashboards"] = report_dashboards

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

    # Form-level rules
    if form.get("decisionRule"):
        form_spec["decisionRule"] = form["decisionRule"]
    if form.get("visitScheduleRule"):
        form_spec["visitScheduleRule"] = form["visitScheduleRule"]
    if form.get("validationRule"):
        form_spec["validationRule"] = form["validationRule"]
    if form.get("checklistsRule"):
        form_spec["checklistsRule"] = form["checklistsRule"]

    # Format 1: Bundle format (formElementGroups)
    if form.get("formElementGroups"):
        for group in form["formElementGroups"]:
            if group.get("voided"):
                continue
            section: dict[str, Any] = {"name": group.get("name", "Details")}
            fields = []
            for fe in sorted(
                group.get("formElements", []),
                key=lambda e: e.get("displayOrder", 0),
            ):
                if fe.get("voided"):
                    continue
                field: dict[str, Any] = {"name": fe.get("name", "")}
                concept = fe.get("concept", {}) or {}
                data_type = concept.get("dataType", fe.get("dataType", ""))

                if data_type and data_type != "NA":
                    field["dataType"] = data_type

                # Selection type from element type
                fe_type = fe.get("type", "")
                if fe_type == "MultiSelect":
                    field["selectionType"] = "Multi"
                elif fe_type == "SingleSelect" and data_type == "Coded":
                    field["selectionType"] = "Single"

                if fe.get("mandatory"):
                    field["mandatory"] = True

                # Numeric bounds
                if data_type == "Numeric":
                    if concept.get("lowAbsolute") is not None:
                        field["min"] = concept["lowAbsolute"]
                    if concept.get("hiAbsolute") is not None:
                        field["max"] = concept["hiAbsolute"]
                    if concept.get("lowNormal") is not None:
                        field["lowNormal"] = concept["lowNormal"]
                    if concept.get("hiNormal") is not None:
                        field["hiNormal"] = concept["hiNormal"]
                    if concept.get("unit"):
                        field["unit"] = concept["unit"]
                elif fe.get("unit"):
                    field["unit"] = fe["unit"]

                # Coded options
                if data_type == "Coded" and concept.get("answers"):
                    field["options"] = [
                        a["name"] if isinstance(a, dict) else str(a)
                        for a in concept["answers"]
                        if not (isinstance(a, dict) and a.get("voided"))
                    ]

                # Skip logic
                if fe.get("skipLogic"):
                    field["skipLogic"] = fe["skipLogic"]

                # KeyValues
                kv_list = fe.get("keyValues", [])
                if kv_list:
                    if isinstance(kv_list, list):
                        kv_dict = {}
                        for kv in kv_list:
                            if isinstance(kv, dict):
                                kv_dict[kv.get("key", "")] = kv.get("value")
                        if kv_dict:
                            field["keyValues"] = kv_dict
                    elif isinstance(kv_list, dict):
                        field["keyValues"] = kv_list

                # Valid format
                if fe.get("validFormat"):
                    field["validFormat"] = fe["validFormat"]

                # Rule on form element
                if fe.get("rule"):
                    field["rule"] = fe["rule"]

                # Declarative rule (newer rule format)
                if fe.get("declarativeRule"):
                    field["declarativeRule"] = fe["declarativeRule"]

                # Documentation (inline help text)
                if fe.get("documentation"):
                    field["documentation"] = fe["documentation"]

                # Parent form element (for QuestionGroup children)
                if fe.get("parentFormElementUuid"):
                    field["parentFormElementUuid"] = fe["parentFormElementUuid"]

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
    if f.get("lowNormal") is not None:
        field["lowNormal"] = f["lowNormal"]
    if f.get("hiNormal") is not None:
        field["hiNormal"] = f["hiNormal"]
    if f.get("options"):
        field["options"] = f["options"]
    if f.get("selectionType"):
        field["selectionType"] = f["selectionType"]
    if f.get("skipLogic"):
        field["skipLogic"] = f["skipLogic"]
    if f.get("keyValues"):
        field["keyValues"] = f["keyValues"]
    if f.get("validFormat"):
        field["validFormat"] = f["validFormat"]
    if f.get("rule"):
        field["rule"] = f["rule"]
    if f.get("declarativeRule"):
        field["declarativeRule"] = f["declarativeRule"]
    if f.get("documentation"):
        field["documentation"] = f["documentation"]
    if f.get("parentFormElementUuid"):
        field["parentFormElementUuid"] = f["parentFormElementUuid"]
    return field
