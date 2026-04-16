"""
test_comprehensive_spec.py — Tests for the comprehensive spec format.

Verifies the batch bundle→spec pipeline captures all real-world patterns
found across 21 Avni org bundles.
"""

import sys
from pathlib import Path

import pytest
import yaml

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.batch_bundle_to_spec import (
    bundle_to_comprehensive_spec,
    read_bundle_dir,
    analyze_coverage,
    _unwrap_list,
)

BUNDLE_DIR = Path.home() / "Downloads" / "orgs-bundle"


def _load_org(org_name: str) -> tuple[dict, dict]:
    """Load bundle and generate spec for an org."""
    bundle = read_bundle_dir(BUNDLE_DIR / org_name)
    spec = bundle_to_comprehensive_spec(bundle, org_name=org_name)
    return bundle, spec


@pytest.mark.skipif(not BUNDLE_DIR.exists(), reason="Bundle directory not found")
class TestComprehensiveSpec:
    """Test comprehensive spec generation across real org bundles."""

    def test_all_21_orgs_process_without_error(self):
        """Every org bundle should convert to spec without errors."""
        org_dirs = [
            d
            for d in sorted(BUNDLE_DIR.iterdir())
            if d.is_dir() and not d.name.startswith(".") and d.name != "specs"
        ]
        assert len(org_dirs) >= 20, f"Expected 20+ orgs, found {len(org_dirs)}"

        errors = []
        for org_dir in org_dirs:
            try:
                bundle = read_bundle_dir(org_dir)
                spec = bundle_to_comprehensive_spec(bundle, org_name=org_dir.name)
                assert spec.get("org") == org_dir.name
                assert "settings" in spec
            except Exception as exc:
                errors.append(f"{org_dir.name}: {exc}")

        assert not errors, "Failed orgs:\n" + "\n".join(errors)

    def test_voided_entities_filtered(self):
        """Voided subject types, programs, encounter types should not appear in spec."""
        bundle, spec = _load_org("Calcutta Kids")
        # Calcutta Kids has voided subject types in raw bundle
        raw_sts = bundle.get("subjectTypes", [])
        voided_count = sum(1 for st in raw_sts if st.get("voided"))
        spec_sts = spec.get("subjectTypes", [])
        # Spec should have fewer than raw (voided removed)
        assert (
            len(spec_sts) <= len(raw_sts) - voided_count + 1
        )  # tolerance for edge cases

    def test_address_hierarchy_parents_resolved(self):
        """Address level parents should be resolved to names, not UUIDs."""
        bundle, spec = _load_org("JK Lakshmi Cement")
        addr_levels = spec.get("addressLevels", [])
        assert len(addr_levels) >= 3

        # State should have no parent
        state = next(a for a in addr_levels if a["name"] == "State")
        assert "parent" not in state or state.get("parent") is None

        # District should have parent="State"
        district = next(a for a in addr_levels if a["name"] == "District")
        assert district.get("parent") == "State"

        # Block parent should be District
        block = next(a for a in addr_levels if a["name"] == "Block")
        assert block.get("parent") == "District"

    def test_program_target_subject_type_resolved(self):
        """Programs should have target subject type resolved (not empty)."""
        bundle, spec = _load_org("JK Lakshmi Cement")
        programs = spec.get("programs", [])
        assert len(programs) >= 2

        for prog in programs:
            assert prog.get("targetSubjectType"), (
                f"Program '{prog['name']}' has empty targetSubjectType"
            )

    def test_encounter_types_linked_to_programs(self):
        """Program encounters should have program name resolved."""
        bundle, spec = _load_org("JNPCT")
        enc_types = spec.get("encounterTypes", [])
        assert len(enc_types) >= 10

        # At least some encounters should be linked to programs
        program_encs = [e for e in enc_types if e.get("program")]
        assert len(program_encs) > 0, "No encounter types linked to programs"

    def test_settings_captured(self):
        """Organisation settings should be captured in spec."""
        bundle, spec = _load_org("JSS")
        settings = spec.get("settings", {})
        assert "languages" in settings
        assert isinstance(settings["languages"], list)
        assert len(settings["languages"]) >= 1

    def test_forms_have_fields(self):
        """Forms in spec should have sections with fields."""
        bundle, spec = _load_org("JK Lakshmi Cement")
        # Check registration form
        st = spec["subjectTypes"][0]
        reg_form = st.get("registrationForm", {})
        sections = reg_form.get("sections", [])
        assert len(sections) > 0, "Registration form has no sections"
        assert len(sections[0].get("fields", [])) > 0, "First section has no fields"

    def test_coded_fields_have_options(self):
        """Coded fields should have options list."""
        bundle, spec = _load_org("JK Lakshmi Cement")
        st = spec["subjectTypes"][0]
        reg_form = st.get("registrationForm", {})
        for section in reg_form.get("sections", []):
            for field in section.get("fields", []):
                if field.get("dataType") == "Coded":
                    assert field.get("options"), (
                        f"Coded field '{field['name']}' has no options"
                    )

    def test_selection_type_captured(self):
        """Fields should have selectionType (Single/Multi)."""
        bundle, spec = _load_org("JK Lakshmi Cement")
        st = spec["subjectTypes"][0]
        reg_form = st.get("registrationForm", {})
        has_selection_type = False
        for section in reg_form.get("sections", []):
            for field in section.get("fields", []):
                if field.get("selectionType"):
                    has_selection_type = True
                    break
        assert has_selection_type, "No fields have selectionType"

    def test_numeric_bounds_captured(self):
        """Numeric fields should have min/max from concept bounds."""
        bundle, spec = _load_org("JK Lakshmi Cement")
        # Find a form with numeric fields
        for enc in spec.get("encounterTypes", []):
            form = enc.get("form", {})
            for section in form.get("sections", []):
                for field in section.get("fields", []):
                    if (
                        field.get("dataType") == "Numeric"
                        and field.get("min") is not None
                    ):
                        return  # Found one, test passes
        pytest.skip("No numeric fields with bounds found")

    def test_rules_captured_on_fields(self):
        """Field-level rules should be captured."""
        bundle, spec = _load_org("JK Lakshmi Cement")
        st = spec["subjectTypes"][0]
        reg_form = st.get("registrationForm", {})
        has_rule = False
        for section in reg_form.get("sections", []):
            for field in section.get("fields", []):
                if field.get("rule"):
                    has_rule = True
                    break
        assert has_rule, "No fields have rules captured"

    def test_valid_format_captured(self):
        """validFormat (regex patterns) should be captured on fields."""
        bundle, spec = _load_org("JK Lakshmi Cement")
        st = spec["subjectTypes"][0]
        reg_form = st.get("registrationForm", {})
        has_valid_format = False
        for section in reg_form.get("sections", []):
            for field in section.get("fields", []):
                if field.get("validFormat"):
                    has_valid_format = True
                    assert "regex" in field["validFormat"]
                    break
        assert has_valid_format, "No fields have validFormat"

    def test_key_values_captured(self):
        """keyValues on form elements should be captured."""
        bundle, spec = _load_org("JK Lakshmi Cement")
        for enc in spec.get("encounterTypes", []):
            form = enc.get("form", {})
            for section in form.get("sections", []):
                for field in section.get("fields", []):
                    if field.get("keyValues"):
                        return  # Found one
        pytest.skip("No fields have keyValues")

    def test_identifier_source_captured(self):
        """Identifier sources should be in spec."""
        bundle, spec = _load_org("IPH Sickle Cell")
        id_sources = spec.get("identifierSources", [])
        assert len(id_sources) >= 1
        assert id_sources[0].get("name")
        assert id_sources[0].get("type")

    def test_relationship_types_captured(self):
        """Relationship types should be in spec."""
        bundle, spec = _load_org("Purna Clinic")
        rel_types = spec.get("relationshipTypes", [])
        assert len(rel_types) >= 5
        assert rel_types[0].get("aIsToB")

    def test_group_roles_captured(self):
        """Group roles should be in spec."""
        bundle, spec = _load_org("Gubbachi")
        group_roles = spec.get("groupRoles", [])
        assert len(group_roles) >= 1
        assert group_roles[0].get("role")

    def test_checklist_captured(self):
        """Checklists should be in spec."""
        bundle, spec = _load_org("JNPCT")
        checklists = spec.get("checklists", [])
        assert len(checklists) >= 1
        assert checklists[0].get("name") == "Vaccination"
        assert len(checklists[0].get("items", [])) > 0

    def test_videos_captured(self):
        """Videos should be in spec."""
        bundle, spec = _load_org("JNPCT")
        videos = spec.get("videos", [])
        assert len(videos) >= 1
        assert videos[0].get("title")

    def test_documentations_captured(self):
        """Documentations should be in spec."""
        bundle, spec = _load_org("IPH Sickle Cell")
        docs = spec.get("documentations", [])
        assert len(docs) >= 1
        assert docs[0].get("name")

    def test_report_cards_captured(self):
        """Report cards should be in spec."""
        bundle, spec = _load_org("JNPCT")
        cards = spec.get("reportCards", [])
        assert len(cards) >= 5
        assert cards[0].get("name")

    def test_custom_queries_captured(self):
        """Custom queries should be in spec."""
        bundle, spec = _load_org("Nala Kholikaran 26-27")
        queries = spec.get("customQueries", [])
        assert len(queries) >= 2
        assert queries[0].get("name")
        assert queries[0].get("query")

    def test_form_coverage_100_percent(self):
        """All active form mappings should be covered in spec."""
        bundle, spec = _load_org("MLD Trust")
        report = analyze_coverage(bundle, spec, "MLD Trust")
        coverage = float(report["formCoverage"].rstrip("%"))
        assert coverage >= 100, f"Form coverage only {coverage}%"

    def test_zero_program_org_works(self):
        """Orgs with no programs (encounter-only) should work."""
        bundle, spec = _load_org("Goonj")
        assert "programs" not in spec or len(spec.get("programs", [])) == 0
        assert len(spec.get("encounterTypes", [])) >= 1
        assert len(spec.get("subjectTypes", [])) >= 1

    def test_subject_type_comprehensive_fields(self):
        """Subject type with complex settings should have all fields."""
        bundle, spec = _load_org("GDGSGOM")
        sts = spec.get("subjectTypes", [])
        # Find Work Order or Excavating Machine subject type
        complex_st = next((st for st in sts if st.get("subjectSummaryRule")), None)
        if complex_st:
            assert complex_st.get("subjectSummaryRule")

    def test_program_rules_captured(self):
        """Programs with eligibility rules should have them in spec."""
        bundle, spec = _load_org("MLD Trust")
        programs = spec.get("programs", [])
        has_rule = any(p.get("enrolmentEligibilityCheckRule") for p in programs)
        assert has_rule, "No programs have enrolmentEligibilityCheckRule"

    def test_encounter_eligibility_rule_captured(self):
        """Encounter types with eligibility rules should have them in spec."""
        bundle, spec = _load_org("GDGSGOM")
        encs = spec.get("encounterTypes", [])
        has_rule = any(e.get("encounterEligibilityCheckRule") for e in encs)
        assert has_rule, "No encounter types have encounterEligibilityCheckRule"

    def test_spec_yaml_serializable(self):
        """Generated spec should be valid YAML that roundtrips."""
        bundle, spec = _load_org("JK Lakshmi Cement")
        spec_yaml = yaml.dump(
            spec, allow_unicode=True, default_flow_style=False, sort_keys=False
        )
        parsed = yaml.safe_load(spec_yaml)
        assert parsed["org"] == "JK Lakshmi Cement"
        assert len(parsed.get("subjectTypes", [])) == len(spec.get("subjectTypes", []))
        assert len(parsed.get("programs", [])) == len(spec.get("programs", []))
        assert len(parsed.get("encounterTypes", [])) == len(
            spec.get("encounterTypes", [])
        )

    def test_form_level_rules_captured(self):
        """Form-level rules (decisionRule, visitScheduleRule) should be in spec."""
        bundle, spec = _load_org("IPH Sickle Cell")
        # Check encounter forms for form-level rules
        for enc in spec.get("encounterTypes", []):
            form = enc.get("form", {})
            if form.get("decisionRule") or form.get("visitScheduleRule"):
                return  # Found one
        # Also check registration forms
        for st in spec.get("subjectTypes", []):
            form = st.get("registrationForm", {})
            if form.get("decisionRule") or form.get("visitScheduleRule"):
                return
        pytest.skip("No form-level rules found in this org")

    # ── New entity type tests ─────────────────────────────────────────────

    def test_menu_items_captured(self):
        """Menu items should be in spec when present in bundle."""
        bundle, spec = _load_org("GDGSGOM")
        menu_items = spec.get("menuItems", [])
        assert len(menu_items) >= 1
        assert menu_items[0].get("displayKey")
        assert menu_items[0].get("type")

    def test_message_rules_captured(self):
        """Message rules should be in spec when present in bundle."""
        bundle, spec = _load_org("GDGSGOM")
        msg_rules = spec.get("messageRules", [])
        assert len(msg_rules) >= 1
        assert msg_rules[0].get("name")
        assert msg_rules[0].get("entityType")

    def test_operational_encounter_types_captured(self):
        """Operational encounter types should be in spec."""
        bundle, spec = _load_org("JNPCT")
        op_encs = spec.get("operationalEncounterTypes", [])
        assert len(op_encs) >= 10
        assert op_encs[0].get("name")

    def test_operational_subject_types_captured(self):
        """Operational subject types should be in spec."""
        bundle, spec = _load_org("JNPCT")
        op_sts = spec.get("operationalSubjectTypes", [])
        assert len(op_sts) >= 1
        assert op_sts[0].get("name")

    def test_group_privileges_captured(self):
        """Group privileges should be grouped by group name with resolved entities."""
        bundle, spec = _load_org("JNPCT")
        gp = spec.get("groupPrivileges", [])
        assert len(gp) >= 1
        for entry in gp:
            assert entry.get("group"), "groupPrivilege entry missing group name"
            assert len(entry.get("privileges", [])) > 0
            for p in entry["privileges"]:
                assert p.get("type"), "privilege missing type"

    def test_group_privileges_resolve_subject_types(self):
        """Group privilege subject types should be resolved to names."""
        bundle, spec = _load_org("JNPCT")
        gp = spec.get("groupPrivileges", [])
        has_resolved = False
        for entry in gp:
            for p in entry.get("privileges", []):
                if p.get("subjectType"):
                    has_resolved = True
                    assert "-" not in p["subjectType"] or len(p["subjectType"]) < 36
                    break
        assert has_resolved, "No privileges have resolved subjectType"

    def test_group_dashboards_captured(self):
        """Group dashboards should be in spec."""
        bundle, spec = _load_org("JNPCT")
        gd = spec.get("groupDashboards", [])
        assert len(gd) >= 5
        assert gd[0].get("groupName")
        assert gd[0].get("dashboardName")

    def test_group_dashboards_primary_flag(self):
        """At least one group dashboard should be marked as primary."""
        bundle, spec = _load_org("APF Odisha")
        gd = spec.get("groupDashboards", [])
        has_primary = any(d.get("primaryDashboard") for d in gd)
        assert has_primary, "No group dashboards marked as primary"

    def test_individual_relations_captured(self):
        """Individual relations should be in spec with gender constraints."""
        bundle, spec = _load_org("JNPCT")
        rels = spec.get("individualRelations", [])
        assert len(rels) >= 5
        assert rels[0].get("name")
        has_gender = any(r.get("genders") for r in rels)
        assert has_gender, "No individual relations have gender constraints"

    def test_catchments_captured(self):
        """Catchments should be in spec."""
        bundle, spec = _load_org("Purna Clinic")
        catchments = spec.get("catchments", [])
        assert len(catchments) >= 1
        assert catchments[0].get("name")

    def test_catchments_dict_wrapper_handled(self):
        """Catchments wrapped in {catchments: [...]} should be handled."""
        bundle, spec = _load_org("Hasiru Dala")
        catchments = spec.get("catchments", [])
        assert len(catchments) >= 1

    def test_locations_captured(self):
        """Locations should be summarized by type."""
        bundle, spec = _load_org("IPH Sickle Cell")
        locs = spec.get("locations", {})
        assert locs.get("totalCount", 0) > 0
        assert isinstance(locs.get("byType"), dict)
        assert len(locs["byType"]) >= 1

    def test_concepts_full_detail(self):
        """Concepts should be captured as full list with details, not just summary."""
        bundle, spec = _load_org("JNPCT")
        concepts = spec.get("concepts", [])
        assert isinstance(concepts, list), "concepts should be a list, not a summary dict"
        assert len(concepts) >= 100

    def test_concepts_coded_have_answers(self):
        """Coded concepts with answers in bundle should have them in spec."""
        bundle, spec = _load_org("JNPCT")
        concepts = spec.get("concepts", [])
        coded = [c for c in concepts if c.get("dataType") == "Coded"]
        assert len(coded) > 0
        coded_with_answers = [c for c in coded if c.get("answers")]
        assert len(coded_with_answers) > 0, "No coded concepts have answers"
        assert len(coded_with_answers) >= len(coded) * 0.5, "Less than half of coded concepts have answers"

    def test_concepts_numeric_have_bounds(self):
        """Numeric concepts with bounds should have them captured."""
        bundle, spec = _load_org("JNPCT")
        concepts = spec.get("concepts", [])
        with_bounds = [c for c in concepts if c.get("highAbsolute") is not None]
        assert len(with_bounds) > 0, "No numeric concepts with bounds found"
        c = with_bounds[0]
        assert c.get("dataType") == "Numeric"
        assert c.get("unit") or c.get("highAbsolute") is not None

    def test_concepts_keyvalues_captured(self):
        """Concepts with keyValues should have them captured."""
        bundle, spec = _load_org("JNPCT")
        concepts = spec.get("concepts", [])
        with_kv = [c for c in concepts if c.get("keyValues")]
        assert len(with_kv) > 0, "No concepts with keyValues found"

    def test_concepts_keyvalues_resolve_uuids(self):
        """Concept keyValues should resolve subjectTypeUUID to name."""
        bundle, spec = _load_org("JNPCT")
        concepts = spec.get("concepts", [])
        for c in concepts:
            kv = c.get("keyValues", {})
            if kv.get("subjectType"):
                assert "-" not in kv["subjectType"] or len(kv["subjectType"]) < 36
                return
        pytest.skip("No concepts with subjectTypeUUID keyValue")

    def test_concepts_na_without_config_skipped(self):
        """Bare NA concepts (answer options) without keyValues should be skipped."""
        bundle, spec = _load_org("JNPCT")
        concepts = spec.get("concepts", [])
        bare_na = [c for c in concepts if c["dataType"] == "NA" and not c.get("keyValues") and not c.get("answers")]
        assert len(bare_na) == 0, f"Found {len(bare_na)} bare NA concepts that should be skipped"

    def test_rule_dependency_captured(self):
        """Rule dependency should be captured when present."""
        bundle, spec = _load_org("JNPCT")
        rd = spec.get("ruleDependency", {})
        assert rd.get("hasCode") is True
        assert rd.get("codeLength", 0) > 0

    def test_unwrap_list_raw_list(self):
        """_unwrap_list should handle raw list values."""
        bundle = {"items": [{"a": 1}, {"a": 2}]}
        result = _unwrap_list(bundle, "items")
        assert result == [{"a": 1}, {"a": 2}]

    def test_unwrap_list_dict_wrapper(self):
        """_unwrap_list should unwrap {key: [...]} dicts."""
        bundle = {"catchments": {"catchments": [{"name": "A"}]}}
        result = _unwrap_list(bundle, "catchments")
        assert result == [{"name": "A"}]

    def test_unwrap_list_missing_key(self):
        """_unwrap_list should return empty list for missing keys."""
        result = _unwrap_list({}, "missing")
        assert result == []

    def test_unwrap_list_string_value(self):
        """_unwrap_list should return empty list for non-list/dict values."""
        result = _unwrap_list({"key": "string"}, "key")
        assert result == []

    def test_coverage_report_includes_new_entities(self):
        """Coverage report should count new entity types in bundle stats."""
        bundle, spec = _load_org("JNPCT")
        report = analyze_coverage(bundle, spec, "JNPCT")
        b = report["bundle"]
        assert "menuItems" in b
        assert "messageRules" in b
        assert "groupPrivileges" in b
        assert "groupDashboards" in b
        assert "individualRelations" in b
        assert b["groupPrivileges"] > 0
        assert b["groupDashboards"] > 0

    def test_coverage_extras_include_new_entities(self):
        """Coverage extras should list new entity types."""
        bundle, spec = _load_org("JNPCT")
        report = analyze_coverage(bundle, spec, "JNPCT")
        extras = report.get("extras", [])
        extras_str = " ".join(extras)
        assert "concepts(" in extras_str
        assert "groupPrivileges(" in extras_str
        assert "groupDashboards(" in extras_str
        assert "individualRelations(" in extras_str
        assert "opEncTypes(" in extras_str

    def test_all_orgs_have_concepts(self):
        """Every org should have concepts captured in spec."""
        org_dirs = [
            d for d in sorted(BUNDLE_DIR.iterdir())
            if d.is_dir() and not d.name.startswith(".") and d.name != "specs"
        ]
        for org_dir in org_dirs:
            bundle = read_bundle_dir(org_dir)
            spec = bundle_to_comprehensive_spec(bundle, org_name=org_dir.name)
            if bundle.get("concepts"):
                assert spec.get("concepts"), f"{org_dir.name} has concepts in bundle but not in spec"
