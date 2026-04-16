#!/usr/bin/env python3
"""
batch_bundle_to_spec.py — Convert real Avni org bundles to comprehensive YAML specs.

Reads extracted bundle directories, converts each to a comprehensive YAML spec,
and reports coverage metrics. This is the reference implementation for the
comprehensive spec format that captures everything real orgs use.

Usage:
    python scripts/batch_bundle_to_spec.py /path/to/orgs-bundle [--output-dir /path/to/output]
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import sys
from pathlib import Path
from typing import Any

import yaml

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Bundle directory reader — reads extracted bundle dirs (not ZIPs)
# ---------------------------------------------------------------------------


def read_bundle_dir(bundle_path: Path) -> dict[str, Any]:
    """Read all JSON files from an extracted bundle directory into a dict."""
    bundle: dict[str, Any] = {}

    for json_file in sorted(bundle_path.glob("*.json")):
        key = json_file.stem  # e.g. "subjectTypes", "programs"
        try:
            with open(json_file, "r", encoding="utf-8") as f:
                bundle[key] = json.load(f)
        except (json.JSONDecodeError, UnicodeDecodeError) as exc:
            logger.warning("  Skipping %s: %s", json_file.name, exc)

    # Read forms from forms/ subdirectory
    forms_dir = bundle_path / "forms"
    if forms_dir.is_dir():
        forms = []
        for form_file in sorted(forms_dir.glob("*.json")):
            try:
                with open(form_file, "r", encoding="utf-8") as f:
                    form_data = json.load(f)
                    forms.append(form_data)
            except (json.JSONDecodeError, UnicodeDecodeError) as exc:
                logger.warning("  Skipping form %s: %s", form_file.name, exc)
        bundle["forms"] = forms

    # Read translations
    trans_dir = bundle_path / "translations"
    if trans_dir.is_dir():
        translations = {}
        for tf in sorted(trans_dir.glob("*.json")):
            try:
                with open(tf, "r", encoding="utf-8") as f:
                    translations[tf.stem] = json.load(f)
            except Exception:
                pass
        if translations:
            bundle["translations"] = translations

    return bundle


# ---------------------------------------------------------------------------
# Comprehensive bundle → spec conversion
# ---------------------------------------------------------------------------


def bundle_to_comprehensive_spec(bundle: dict[str, Any], org_name: str = "") -> dict[str, Any]:
    """
    Convert a full Avni bundle dict to a comprehensive YAML spec.

    This captures everything real orgs use, not just the subset the old
    pipeline handled. The spec is designed to be:
    1. Human-readable YAML
    2. Complete enough to reproduce the org
    3. Roundtrip-safe (spec → entities → bundle → spec)
    """
    spec: dict[str, Any] = {}
    spec["org"] = org_name or "Unknown Organization"

    # ── Settings (from organisationConfig) ─────────────────────────────────
    org_config = bundle.get("organisationConfig", {})
    if isinstance(org_config, list) and org_config:
        org_config = org_config[0]
    elif not isinstance(org_config, dict):
        org_config = {}

    settings_val = org_config.get("settings", {}) or {}
    config_settings = org_config.get("organisationConfig", settings_val)
    if isinstance(config_settings, str):
        try:
            config_settings = json.loads(config_settings)
        except Exception:
            config_settings = {}

    # Extract languages from settings or translations
    languages = config_settings.get("languages", ["en"])
    if not languages:
        trans = bundle.get("translations", {})
        if isinstance(trans, dict):
            languages = list(trans.keys()) or ["en"]

    settings: dict[str, Any] = {"languages": languages}

    # Capture org config settings that matter
    for key in [
        "enableComments", "enableMessaging", "saveDrafts",
        "skipRuleExecution", "enableRuleDesigner",
        "metabaseSetupEnabled", "showHierarchicalLocation",
    ]:
        if config_settings.get(key) is not None:
            settings[key] = config_settings[key]

    # Search filters
    search_filters = config_settings.get("searchFilters")
    if search_filters:
        settings["searchFilters"] = search_filters

    # Dashboard filters
    dash_filters = config_settings.get("myDashboardFilters")
    if dash_filters:
        settings["myDashboardFilters"] = dash_filters

    # Custom registration locations
    custom_reg = config_settings.get("customRegistrationLocations")
    if custom_reg:
        settings["customRegistrationLocations"] = custom_reg

    # Search result fields
    search_result_fields = config_settings.get("searchResultFields")
    if search_result_fields:
        settings["searchResultFields"] = search_result_fields

    spec["settings"] = settings

    # ── Build UUID lookup maps ─────────────────────────────────────────────
    # Subject type UUID → name
    st_uuid_to_name: dict[str, str] = {}
    for st in bundle.get("subjectTypes", []):
        if st.get("uuid"):
            st_uuid_to_name[st["uuid"]] = st.get("name", "")

    # Program UUID → name and program UUID → subject type (via formMappings)
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

    # Encounter type UUID → name
    enc_uuid_to_name: dict[str, str] = {}
    for enc in bundle.get("encounterTypes", []):
        if enc.get("uuid"):
            enc_uuid_to_name[enc["uuid"]] = enc.get("name", "")

    # formMappings: build encounter→program and encounter→subjectType links
    enc_uuid_to_prog: dict[str, str] = {}
    enc_uuid_to_st: dict[str, str] = {}
    st_uuid_to_prog_for_enc: dict[str, str] = {}  # for program encounters
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
        # Also resolve program → subject type
        if prog_uuid and st_uuid and fm.get("formType") == "ProgramEnrolment":
            st_uuid_to_prog_for_enc[prog_uuid] = st_uuid_to_name.get(st_uuid, "")

    # Form UUID → form data, and form name matching for form lookups
    form_by_name: dict[str, dict] = {}
    form_by_uuid: dict[str, dict] = {}
    for form in bundle.get("forms", []):
        if isinstance(form, dict):
            fname = form.get("name", "")
            if fname:
                form_by_name[fname] = form
            fuuid = form.get("uuid")
            if fuuid:
                form_by_uuid[fuuid] = form

    # formMapping: formName → formType + entity refs
    fm_by_form_name: dict[str, dict] = {}
    for fm in bundle.get("formMappings", []):
        if fm.get("voided"):
            continue
        fname = fm.get("formName", "")
        if fname:
            fm_by_form_name[fname] = fm

    # ── Address levels ─────────────────────────────────────────────────────
    addr_types = bundle.get("addressLevelTypes", [])
    if addr_types:
        # Filter out voided
        active_addr = [a for a in addr_types if not a.get("voided", False)]
        sorted_addr = sorted(active_addr, key=lambda a: -a.get("level", 0))

        # Build UUID→name map for parent resolution
        addr_uuid_to_name: dict[str, str] = {}
        for alt in active_addr:
            if alt.get("uuid"):
                addr_uuid_to_name[alt["uuid"]] = alt.get("name", "")

        spec["addressLevels"] = []
        for alt in sorted_addr:
            entry: dict[str, Any] = {
                "name": alt["name"],
                "level": alt.get("level", 1),
            }
            parent = alt.get("parent")
            if isinstance(parent, dict):
                parent_name = parent.get("name") or addr_uuid_to_name.get(parent.get("uuid", ""))
                if parent_name:
                    entry["parent"] = parent_name
            elif isinstance(parent, str) and parent:
                entry["parent"] = parent
            spec["addressLevels"].append(entry)

    # ── Subject types ──────────────────────────────────────────────────────
    subject_types_raw = bundle.get("subjectTypes", [])
    active_sts = [st for st in subject_types_raw if not st.get("voided", False)]
    if active_sts:
        spec["subjectTypes"] = []
        for st in active_sts:
            st_spec: dict[str, Any] = {
                "name": st["name"],
                "type": st.get("type", "Person"),
            }
            # Capture all real-world settings
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

            # Settings sub-object
            st_settings = st.get("settings", {})
            if isinstance(st_settings, dict) and st_settings:
                st_spec["settings"] = st_settings

            # Sync registration concept
            if st.get("syncRegistrationConcept1"):
                st_spec["syncRegistrationConcept1"] = st["syncRegistrationConcept1"]
            if st.get("syncRegistrationConcept1Usable"):
                st_spec["syncRegistrationConcept1Usable"] = st["syncRegistrationConcept1Usable"]
            if st.get("memberAdditionEligibilityCheckRule"):
                st_spec["memberAdditionEligibilityCheckRule"] = st["memberAdditionEligibilityCheckRule"]

            # Attach registration form
            reg_form = _find_form_for_entity(
                bundle, "IndividualProfile", st_uuid=st.get("uuid")
            )
            if reg_form:
                st_spec["registrationForm"] = _form_to_spec(reg_form)

            spec["subjectTypes"].append(st_spec)

    # ── Programs ───────────────────────────────────────────────────────────
    programs_raw = bundle.get("programs", [])
    active_progs = [p for p in programs_raw if not p.get("voided", False)]
    if active_progs:
        spec["programs"] = []
        for prog in active_progs:
            prog_uuid = prog.get("uuid", "")
            target_st = st_uuid_to_prog_for_enc.get(prog_uuid, "")

            prog_spec: dict[str, Any] = {
                "name": prog["name"],
                "targetSubjectType": target_st,
            }
            if prog.get("colour"):
                prog_spec["colour"] = prog["colour"]
            if prog.get("allowMultipleEnrolments"):
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

            # Enrolment form
            enrol_form = _find_form_for_entity(
                bundle, "ProgramEnrolment", prog_uuid=prog_uuid
            )
            if enrol_form:
                prog_spec["enrolmentForm"] = _form_to_spec(enrol_form)

            # Exit form
            exit_form = _find_form_for_entity(
                bundle, "ProgramExit", prog_uuid=prog_uuid
            )
            if exit_form:
                prog_spec["exitForm"] = _form_to_spec(exit_form)

            spec["programs"].append(prog_spec)

    # ── Encounter types ────────────────────────────────────────────────────
    enc_types_raw = bundle.get("encounterTypes", [])
    active_encs = [e for e in enc_types_raw if not e.get("voided", False)]
    if active_encs:
        spec["encounterTypes"] = []
        for enc in active_encs:
            enc_uuid = enc.get("uuid", "")
            prog_name = enc_uuid_to_prog.get(enc_uuid, "")
            st_name = enc_uuid_to_st.get(enc_uuid, "")
            is_program_enc = bool(prog_name)

            enc_spec: dict[str, Any] = {"name": enc["name"]}
            if prog_name:
                enc_spec["program"] = prog_name
            if st_name:
                enc_spec["subjectType"] = st_name

            elig_rule = enc.get("encounterEligibilityCheckRule") or enc.get("entityEligibilityCheckRule")
            if elig_rule:
                enc_spec["encounterEligibilityCheckRule"] = elig_rule
            if enc.get("entityEligibilityCheckDeclarativeRule"):
                enc_spec["entityEligibilityCheckDeclarativeRule"] = enc["entityEligibilityCheckDeclarativeRule"]
            if enc.get("immutable"):
                enc_spec["immutable"] = True

            # Find the encounter form
            form_type = "ProgramEncounter" if is_program_enc else "Encounter"
            enc_form = _find_form_for_entity(
                bundle, form_type, enc_uuid=enc_uuid
            )
            if enc_form:
                enc_spec["form"] = _form_to_spec(enc_form)

            # Cancellation form
            cancel_type = (
                "ProgramEncounterCancellation" if is_program_enc
                else "IndividualEncounterCancellation"
            )
            cancel_form = _find_form_for_entity(
                bundle, cancel_type, enc_uuid=enc_uuid
            )
            if cancel_form:
                enc_spec["cancellationForm"] = _form_to_spec(cancel_form)

            spec["encounterTypes"].append(enc_spec)

    # ── Groups ─────────────────────────────────────────────────────────────
    groups_raw = bundle.get("groups", [])
    active_groups = [g for g in groups_raw if not g.get("voided", False)]
    if active_groups:
        spec["groups"] = []
        for grp in active_groups:
            g_spec: dict[str, Any] = {"name": grp["name"]}
            if grp.get("hasAllPrivileges"):
                g_spec["hasAllPrivileges"] = True
            spec["groups"].append(g_spec)

    # ── Group roles ────────────────────────────────────────────────────────
    group_roles = bundle.get("groupRole", [])
    if not group_roles:
        group_roles = bundle.get("groupRoles", [])
    if group_roles:
        active_roles = [r for r in group_roles if not r.get("voided", False)]
        if active_roles:
            spec["groupRoles"] = []
            for role in active_roles:
                role_spec: dict[str, Any] = {"role": role.get("role", "")}
                # Resolve group and member subject type
                if role.get("groupSubjectTypeUUID"):
                    role_spec["groupSubjectType"] = st_uuid_to_name.get(
                        role["groupSubjectTypeUUID"], ""
                    )
                if role.get("memberSubjectTypeUUID"):
                    role_spec["memberSubjectType"] = st_uuid_to_name.get(
                        role["memberSubjectTypeUUID"], ""
                    )
                if role.get("maximumNumberOfMembers"):
                    role_spec["maximumNumberOfMembers"] = role["maximumNumberOfMembers"]
                if role.get("minimumNumberOfMembers"):
                    role_spec["minimumNumberOfMembers"] = role["minimumNumberOfMembers"]
                spec["groupRoles"].append(role_spec)

    # ── Identifier sources ─────────────────────────────────────────────────
    id_sources = bundle.get("identifierSource", [])
    if id_sources:
        active_ids = [s for s in id_sources if not s.get("voided", False)]
        if active_ids:
            spec["identifierSources"] = []
            for src in active_ids:
                id_spec: dict[str, Any] = {
                    "name": src.get("name", ""),
                    "type": src.get("type", ""),
                }
                if src.get("prefix"):
                    id_spec["prefix"] = src["prefix"]
                if src.get("minLength"):
                    id_spec["minLength"] = src["minLength"]
                if src.get("maxLength"):
                    id_spec["maxLength"] = src["maxLength"]
                if src.get("batchGenerationSize"):
                    id_spec["batchGenerationSize"] = src["batchGenerationSize"]
                spec["identifierSources"].append(id_spec)

    # ── Relationships ──────────────────────────────────────────────────────
    rel_types = bundle.get("relationshipType", [])
    if rel_types:
        active_rels = [r for r in rel_types if not r.get("voided", False)]
        if active_rels:
            spec["relationshipTypes"] = []
            for rel in active_rels:
                rel_spec: dict[str, Any] = {}
                ind_a = rel.get("individualAIsToBRelation", {})
                ind_b = rel.get("individualBIsToARelation", {})
                if isinstance(ind_a, dict):
                    rel_spec["aIsToB"] = ind_a.get("name", "")
                if isinstance(ind_b, dict):
                    rel_spec["bIsToA"] = ind_b.get("name", "")
                spec["relationshipTypes"].append(rel_spec)

    # ── Checklists ─────────────────────────────────────────────────────────
    checklists = bundle.get("checklist", [])
    if checklists:
        active_cl = [c for c in checklists if not c.get("voided", False)]
        if active_cl:
            spec["checklists"] = []
            for cl in active_cl:
                cl_spec: dict[str, Any] = {"name": cl.get("name", "")}
                items = cl.get("items", [])
                if items:
                    cl_items = []
                    for item in items:
                        if item.get("voided", False):
                            continue
                        concept = item.get("concept", {})
                        item_spec: dict[str, Any] = {
                            "name": concept.get("name", "") if isinstance(concept, dict) else "",
                        }
                        # Status can be a list of state objects or a dict with statuses
                        status = item.get("status")
                        if isinstance(status, list):
                            states = [s.get("state", "") for s in status if isinstance(s, dict) and s.get("state")]
                            if states:
                                item_spec["states"] = states
                        elif isinstance(status, dict):
                            statuses = status.get("statuses", [])
                            states = [s.get("state", "") for s in statuses if isinstance(s, dict) and s.get("state")]
                            if states:
                                item_spec["states"] = states
                        cl_items.append(item_spec)
                    if cl_items:
                        cl_spec["items"] = cl_items
                spec["checklists"].append(cl_spec)

    # ── Videos ─────────────────────────────────────────────────────────────
    videos = bundle.get("video", [])
    if videos:
        active_vids = [v for v in videos if not v.get("voided", False)]
        if active_vids:
            spec["videos"] = [
                {"title": v.get("title", ""), "filePath": v.get("filePath", "")}
                for v in active_vids
            ]

    # ── Documentations ─────────────────────────────────────────────────────
    docs = bundle.get("documentations", [])
    if docs:
        active_docs = [d for d in docs if not d.get("voided", False)]
        if active_docs:
            spec["documentations"] = [
                {
                    "name": d.get("name", ""),
                    "content": d.get("content", ""),
                }
                for d in active_docs[:20]  # Cap to avoid bloat
            ]

    # ── Custom queries ─────────────────────────────────────────────────────
    custom_queries = bundle.get("customQueries", [])
    if custom_queries:
        active_cq = [q for q in custom_queries if not q.get("voided", False)]
        if active_cq:
            spec["customQueries"] = [
                {
                    "name": q.get("name", ""),
                    "query": q.get("query", ""),
                }
                for q in active_cq
            ]

    # ── Worklist updation rule ─────────────────────────────────────────────
    worklist_rule = config_settings.get("worklistUpdationRule")
    if worklist_rule:
        spec["settings"]["worklistUpdationRule"] = worklist_rule

    # ── Report cards (summary only) ────────────────────────────────────────
    report_cards = bundle.get("reportCard", [])
    if report_cards:
        active_cards = [c for c in report_cards if not c.get("voided", False)]
        if active_cards:
            spec["reportCards"] = [
                {
                    "name": c.get("name", ""),
                    "colour": c.get("colour", c.get("color", "")),
                    "description": c.get("description", ""),
                }
                for c in active_cards
            ]

    # ── Report dashboards (summary only) ───────────────────────────────────
    report_dashboards = bundle.get("reportDashboard", [])
    if report_dashboards:
        active_dashes = [d for d in report_dashboards if not d.get("voided", False)]
        if active_dashes:
            spec["reportDashboards"] = [
                {
                    "name": d.get("name", ""),
                    "description": d.get("description", ""),
                }
                for d in active_dashes
            ]

    # ── Translations (language list) ───────────────────────────────────────
    trans = bundle.get("translations", {})
    if isinstance(trans, dict) and trans:
        # Already captured in settings.languages
        pass

    return spec


# ---------------------------------------------------------------------------
# Form lookup and conversion helpers
# ---------------------------------------------------------------------------


def _find_form_for_entity(
    bundle: dict,
    form_type: str,
    st_uuid: str | None = None,
    prog_uuid: str | None = None,
    enc_uuid: str | None = None,
) -> dict | None:
    """Find a form from the bundle using formMappings to resolve entity links."""
    for fm in bundle.get("formMappings", []):
        if fm.get("voided"):
            continue
        if fm.get("formType") != form_type:
            continue
        if st_uuid and fm.get("subjectTypeUUID") != st_uuid:
            # For program forms, subjectType match is optional
            if form_type == "IndividualProfile":
                continue
        if prog_uuid and fm.get("programUUID") != prog_uuid:
            continue
        if enc_uuid and fm.get("encounterTypeUUID") != enc_uuid:
            continue

        # Found matching mapping — find the form by name
        form_name = fm.get("formName", "")
        for form in bundle.get("forms", []):
            if isinstance(form, dict) and form.get("name") == form_name:
                return form
            # Also try UUID match
            if isinstance(form, dict) and form.get("uuid") == fm.get("formUUID"):
                return form

    return None


def _form_to_spec(form: dict) -> dict[str, Any]:
    """Convert a bundle form dict to the comprehensive spec format."""
    form_spec: dict[str, Any] = {}
    sections: list[dict] = []

    # Extract rules at form level
    if form.get("decisionRule"):
        form_spec["decisionRule"] = form["decisionRule"]
    if form.get("visitScheduleRule"):
        form_spec["visitScheduleRule"] = form["visitScheduleRule"]
    if form.get("validationRule"):
        form_spec["validationRule"] = form["validationRule"]
    if form.get("checklistsRule"):
        form_spec["checklistsRule"] = form["checklistsRule"]

    for group in form.get("formElementGroups", []):
        if group.get("voided"):
            continue
        section: dict[str, Any] = {"name": group.get("name", "Details")}
        fields: list[dict] = []

        for fe in sorted(
            group.get("formElements", []),
            key=lambda e: e.get("displayOrder", 0),
        ):
            if fe.get("voided"):
                continue
            field: dict[str, Any] = {"name": fe.get("name", "")}

            # Type / selection type
            fe_type = fe.get("type", "")
            concept = fe.get("concept", {}) or {}
            data_type = concept.get("dataType", fe.get("dataType", ""))

            if data_type and data_type != "NA":
                field["dataType"] = data_type

            if fe_type in ("MultiSelect",):
                field["selectionType"] = "Multi"
            elif fe_type in ("SingleSelect",) and data_type == "Coded":
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

            # Coded options
            if data_type == "Coded" and concept.get("answers"):
                field["options"] = [
                    a["name"] if isinstance(a, dict) else str(a)
                    for a in concept["answers"]
                    if not (isinstance(a, dict) and a.get("voided"))
                ]

            # KeyValues
            kv_list = fe.get("keyValues", [])
            if kv_list:
                kv_dict = {}
                for kv in kv_list:
                    if isinstance(kv, dict):
                        kv_dict[kv.get("key", "")] = kv.get("value")
                if kv_dict:
                    field["keyValues"] = kv_dict

            # Valid format
            if fe.get("validFormat"):
                field["validFormat"] = fe["validFormat"]

            # Rule on form element
            if fe.get("rule"):
                field["rule"] = fe["rule"]
            if fe.get("declarativeRule"):
                field["declarativeRule"] = fe["declarativeRule"]
            if fe.get("documentation"):
                field["documentation"] = fe["documentation"]
            if fe.get("parentFormElementUuid"):
                field["parentFormElementUuid"] = fe["parentFormElementUuid"]

            fields.append(field)

        if fields:
            section["fields"] = fields
        sections.append(section)

    if sections:
        form_spec["sections"] = sections
    return form_spec


# ---------------------------------------------------------------------------
# Coverage analysis
# ---------------------------------------------------------------------------


def analyze_coverage(bundle: dict, spec: dict, org_name: str) -> dict[str, Any]:
    """Analyze what percentage of the bundle is captured in the spec."""
    report: dict[str, Any] = {"org": org_name}

    # Count bundle entities
    all_sts = bundle.get("subjectTypes", [])
    active_sts = [s for s in all_sts if not s.get("voided", False)]
    all_progs = bundle.get("programs", [])
    active_progs = [p for p in all_progs if not p.get("voided", False)]
    all_encs = bundle.get("encounterTypes", [])
    active_encs = [e for e in all_encs if not e.get("voided", False)]

    # Count active form mappings (not voided) to get actual expected forms
    active_fm = [fm for fm in bundle.get("formMappings", []) if not fm.get("voided", False)]
    # Count unique form names from active mappings
    active_form_names = {fm.get("formName", "") for fm in active_fm if fm.get("formName")}

    report["bundle"] = {
        "subjectTypes": len(active_sts),
        "programs": len(active_progs),
        "encounterTypes": len(active_encs),
        "forms": len(bundle.get("forms", [])),
        "activeForms": len(active_form_names),
        "concepts": len(bundle.get("concepts", [])),
        "groups": len([g for g in bundle.get("groups", []) if not g.get("voided", False)]),
    }

    # Count spec entities
    report["spec"] = {
        "subjectTypes": len(spec.get("subjectTypes", [])),
        "programs": len(spec.get("programs", [])),
        "encounterTypes": len(spec.get("encounterTypes", [])),
        "groups": len(spec.get("groups", [])),
    }

    # Count forms in spec
    form_count = 0
    for st in spec.get("subjectTypes", []):
        if "registrationForm" in st:
            form_count += 1
    for prog in spec.get("programs", []):
        if "enrolmentForm" in prog:
            form_count += 1
        if "exitForm" in prog:
            form_count += 1
    for enc in spec.get("encounterTypes", []):
        if "form" in enc:
            form_count += 1
        if "cancellationForm" in enc:
            form_count += 1
    report["spec"]["formsAttached"] = form_count

    # Field counts in spec
    field_count = 0
    for st in spec.get("subjectTypes", []):
        for sec in st.get("registrationForm", {}).get("sections", []):
            field_count += len(sec.get("fields", []))
    for prog in spec.get("programs", []):
        for sec in prog.get("enrolmentForm", {}).get("sections", []):
            field_count += len(sec.get("fields", []))
        for sec in prog.get("exitForm", {}).get("sections", []):
            field_count += len(sec.get("fields", []))
    for enc in spec.get("encounterTypes", []):
        for sec in enc.get("form", {}).get("sections", []):
            field_count += len(sec.get("fields", []))
        for sec in enc.get("cancellationForm", {}).get("sections", []):
            field_count += len(sec.get("fields", []))
    report["spec"]["totalFields"] = field_count

    # Extra features captured
    extras = []
    if spec.get("identifierSources"):
        extras.append(f"identifierSources({len(spec['identifierSources'])})")
    if spec.get("relationshipTypes"):
        extras.append(f"relationshipTypes({len(spec['relationshipTypes'])})")
    if spec.get("groupRoles"):
        extras.append(f"groupRoles({len(spec['groupRoles'])})")
    if spec.get("checklists"):
        extras.append(f"checklists({len(spec['checklists'])})")
    if spec.get("videos"):
        extras.append(f"videos({len(spec['videos'])})")
    if spec.get("documentations"):
        extras.append(f"documentations({len(spec['documentations'])})")
    if spec.get("customQueries"):
        extras.append(f"customQueries({len(spec['customQueries'])})")
    if spec.get("reportCards"):
        extras.append(f"reportCards({len(spec['reportCards'])})")
    if spec.get("reportDashboards"):
        extras.append(f"reportDashboards({len(spec['reportDashboards'])})")
    report["extras"] = extras

    # Coverage percentage (against active form mappings, not all form files)
    active_form_count = report["bundle"]["activeForms"]
    form_coverage = (form_count / active_form_count * 100) if active_form_count > 0 else 0
    report["formCoverage"] = f"{form_coverage:.0f}%"

    return report


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main():
    parser = argparse.ArgumentParser(
        description="Convert Avni org bundles to comprehensive YAML specs"
    )
    parser.add_argument("bundle_dir", help="Directory containing org bundle subdirectories")
    parser.add_argument(
        "--output-dir",
        default=None,
        help="Output directory for spec YAML files (default: <bundle_dir>/specs)",
    )
    parser.add_argument(
        "--report-only",
        action="store_true",
        help="Only print coverage report, don't write spec files",
    )
    args = parser.parse_args()

    bundle_root = Path(args.bundle_dir)
    if not bundle_root.is_dir():
        print(f"Error: {bundle_root} is not a directory")
        sys.exit(1)

    output_dir = Path(args.output_dir) if args.output_dir else bundle_root / "specs"
    if not args.report_only:
        output_dir.mkdir(parents=True, exist_ok=True)

    # Find all org directories
    org_dirs = sorted([
        d for d in bundle_root.iterdir()
        if d.is_dir() and not d.name.startswith(".") and d.name != "specs"
    ])

    if not org_dirs:
        print(f"No org directories found in {bundle_root}")
        sys.exit(1)

    print(f"\nProcessing {len(org_dirs)} org bundles from {bundle_root}\n")
    print("=" * 80)

    all_reports = []
    errors = []

    for org_dir in org_dirs:
        org_name = org_dir.name
        print(f"\n{'─' * 60}")
        print(f"  {org_name}")
        print(f"{'─' * 60}")

        try:
            bundle = read_bundle_dir(org_dir)
            spec = bundle_to_comprehensive_spec(bundle, org_name=org_name)
            report = analyze_coverage(bundle, spec, org_name)
            all_reports.append(report)

            # Print summary
            b = report["bundle"]
            s = report["spec"]
            print(f"  Bundle: {b['subjectTypes']} ST, {b['programs']} Prog, {b['encounterTypes']} Enc, {b['forms']} Forms, {b['concepts']} Concepts")
            print(f"  Spec:   {s['subjectTypes']} ST, {s['programs']} Prog, {s['encounterTypes']} Enc, {s['formsAttached']} Forms, {s['totalFields']} Fields")
            print(f"  Form coverage: {report['formCoverage']}")
            if report["extras"]:
                print(f"  Extras: {', '.join(report['extras'])}")

            # Write spec YAML
            if not args.report_only:
                safe_name = org_name.replace("/", "_").replace(" ", "_")
                spec_file = output_dir / f"{safe_name}.yaml"
                spec_yaml = yaml.dump(
                    spec,
                    allow_unicode=True,
                    default_flow_style=False,
                    sort_keys=False,
                    width=120,
                )
                with open(spec_file, "w", encoding="utf-8") as f:
                    f.write(spec_yaml)
                print(f"  Written: {spec_file} ({len(spec_yaml):,} chars)")

        except Exception as exc:
            logger.error("  FAILED: %s — %s", org_name, exc)
            errors.append({"org": org_name, "error": str(exc)})
            import traceback
            traceback.print_exc()

    # ── Summary ────────────────────────────────────────────────────────────
    print(f"\n\n{'=' * 80}")
    print("SUMMARY")
    print(f"{'=' * 80}")
    print(f"  Processed: {len(all_reports)} orgs")
    print(f"  Errors:    {len(errors)} orgs")

    if all_reports:
        total_sts = sum(r["bundle"]["subjectTypes"] for r in all_reports)
        total_progs = sum(r["bundle"]["programs"] for r in all_reports)
        total_encs = sum(r["bundle"]["encounterTypes"] for r in all_reports)
        total_forms = sum(r["bundle"]["forms"] for r in all_reports)
        total_concepts = sum(r["bundle"]["concepts"] for r in all_reports)
        total_fields = sum(r["spec"]["totalFields"] for r in all_reports)
        total_forms_attached = sum(r["spec"]["formsAttached"] for r in all_reports)

        print(f"\n  Across all orgs:")
        print(f"    Subject types:  {total_sts}")
        print(f"    Programs:       {total_progs}")
        print(f"    Encounter types:{total_encs}")
        print(f"    Bundle forms:   {total_forms}")
        print(f"    Concepts:       {total_concepts}")
        print(f"    Spec forms:     {total_forms_attached}")
        print(f"    Spec fields:    {total_fields}")
        print(f"    Avg form coverage: {sum(float(r['formCoverage'].rstrip('%')) for r in all_reports) / len(all_reports):.0f}%")

    if errors:
        print(f"\n  Failed orgs:")
        for e in errors:
            print(f"    - {e['org']}: {e['error']}")

    # Write summary report JSON
    if not args.report_only:
        report_file = output_dir / "_coverage_report.json"
        with open(report_file, "w", encoding="utf-8") as f:
            json.dump({"reports": all_reports, "errors": errors}, f, indent=2)
        print(f"\n  Coverage report: {report_file}")

    print()


if __name__ == "__main__":
    main()
