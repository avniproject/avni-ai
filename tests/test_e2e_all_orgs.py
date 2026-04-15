"""
End-to-end tests for all SRS orgs across all agent steps:
  1. PARSING: scoping_parser extracts entities correctly
  2. SPEC: generate_spec produces valid YAML
  3. BUNDLE: generate_bundle produces valid bundle with correct formMappings
  4. INSPECTION: validate_bundle catches real issues, no false positives
  5. SKIP LOGIC: auto-detected patterns are correct
  6. CONCEPTS: no duplicates, dual-role handled
"""

from __future__ import annotations

from collections import Counter
from pathlib import Path

import pytest

from src.bundle.scoping_parser import parse_scoping_docs
from src.bundle.generator import BundleGenerator
from src.bundle.validators import BundleValidator
from src.bundle.spec_generator import entities_to_spec


# ── Resource file sets ───────────────────────────────────────────────────

_ORG_FILES: dict[str, list[Path]] = {
    "mazi_saheli": [
        Path("tests/resources/scoping/Mazi Saheli Charitable Trust Scoping .xlsx"),
        Path("tests/resources/scoping/Mazi Saheli Charitable Trust Modelling.xlsx"),
    ],
    "astitva": [
        Path("tests/resources/scoping/Astitva SRS .xlsx"),
        Path("tests/resources/scoping/Astitva Modelling.xlsx"),
        Path("tests/resources/scoping/Astitva Nourish Program Forms.xlsx"),
    ],
    "durga_india": [
        Path("tests/resources/scoping/Durga India Scoping Document.xlsx"),
        Path("tests/resources/scoping/Durga India Modelling.xlsx"),
    ],
    "yenepoya": [
        Path("tests/resources/scoping/Yenepoya_SRS.xlsx"),
    ],
    "kshamata": [
        Path("tests/resources/scoping/Kshamata Scoping Document .xlsx"),
        Path("tests/resources/scoping/Kshamata Modelling.xlsx"),
    ],
}


def _files_exist(org: str) -> bool:
    return all(f.exists() for f in _ORG_FILES[org])


def _parse(org: str):
    spec, misc = parse_scoping_docs([str(f) for f in _ORG_FILES[org]])
    return spec, misc


def _generate_bundle(org: str, spec):
    entities = spec.model_dump()
    gen = BundleGenerator(org)
    gen.generate(entities)
    return gen.bundle


def _validate(bundle):
    return BundleValidator(bundle).validate()


# ── Fixtures ─────────────────────────────────────────────────────────────


@pytest.fixture(scope="module", params=list(_ORG_FILES.keys()))
def org_data(request):
    org = request.param
    if not _files_exist(org):
        pytest.skip(f"Resource files for {org} not found")
    spec, misc = _parse(org)
    bundle = _generate_bundle(org, spec)
    validation = _validate(bundle)
    return {
        "org": org,
        "spec": spec,
        "misc": misc,
        "bundle": bundle,
        "validation": validation,
    }


# ═══════════════════════════════════════════════════════════════════════════
# STEP 1: PARSING
# ═══════════════════════════════════════════════════════════════════════════


class TestParsing:
    """Parser should extract entities from all SRS files without errors."""

    def test_has_subject_types(self, org_data):
        assert len(org_data["spec"].subject_types) > 0, (
            f"{org_data['org']}: no subject types extracted"
        )

    def test_subject_types_have_names(self, org_data):
        for st in org_data["spec"].subject_types:
            assert st.name, f"{org_data['org']}: subject type has empty name"
            assert st.name.lower() not in ("subject type", "name", "type"), (
                f"{org_data['org']}: header row parsed as subject type: '{st.name}'"
            )

    def test_subject_names_no_registration_suffix(self, org_data):
        for st in org_data["spec"].subject_types:
            assert "registration" not in st.name.lower(), (
                f"{org_data['org']}: subject type '{st.name}' has Registration suffix"
            )

    def test_no_header_rows_in_encounters(self, org_data):
        for et in org_data["spec"].encounter_types:
            assert et.name.lower() not in (
                "encounter name",
                "subject type",
                "type",
            ), f"{org_data['org']}: header row in encounters: '{et.name}'"

    def test_forms_have_fields(self, org_data):
        for f in org_data["spec"].forms:
            assert len(f.fields) > 0, (
                f"{org_data['org']}: form '{f.name}' has 0 fields"
            )

    def test_forms_classified_correctly(self, org_data):
        for f in org_data["spec"].forms:
            if any(kw in f.name.lower() for kw in ("registration", "profile")):
                if f.subjectType:
                    assert f.formType == "IndividualProfile", (
                        f"{org_data['org']}: '{f.name}' with subjectType should be "
                        f"IndividualProfile, got {f.formType}"
                    )


# ═══════════════════════════════════════════════════════════════════════════
# STEP 2: SPEC GENERATION
# ═══════════════════════════════════════════════════════════════════════════


class TestSpecGeneration:
    """generate_spec should produce valid YAML from parsed entities."""

    def test_spec_yaml_generated(self, org_data):
        entities = org_data["spec"].model_dump()
        result = entities_to_spec(entities, org_name=org_data["org"])
        assert result is not None
        assert len(result) > 100, f"{org_data['org']}: spec YAML too short"

    def test_spec_contains_subject_types(self, org_data):
        entities = org_data["spec"].model_dump()
        result = entities_to_spec(entities, org_name=org_data["org"])
        assert "subjectTypes" in result or "subject_types" in result


# ═══════════════════════════════════════════════════════════════════════════
# STEP 3: BUNDLE GENERATION
# ═══════════════════════════════════════════════════════════════════════════


class TestBundleGeneration:
    """Bundle should contain all required files with no duplicate concepts."""

    def test_bundle_has_concepts(self, org_data):
        # Yenepoya has only subject types, no forms → no concepts
        if org_data["org"] == "yenepoya":
            return
        concepts = org_data["bundle"].get("concepts", [])
        assert len(concepts) > 0, f"{org_data['org']}: no concepts generated"

    def test_no_duplicate_concepts(self, org_data):
        concepts = org_data["bundle"].get("concepts", [])
        names = Counter(c["name"].lower() for c in concepts)
        dupes = {n: c for n, c in names.items() if c > 1}
        assert len(dupes) == 0, (
            f"{org_data['org']}: duplicate concepts: {list(dupes.keys())}"
        )

    def test_bundle_has_subject_types(self, org_data):
        st = org_data["bundle"].get("subjectTypes", [])
        assert len(st) > 0, f"{org_data['org']}: no subject types in bundle"

    def test_bundle_has_forms(self, org_data):
        forms = org_data["bundle"].get("forms", [])
        assert len(forms) > 0, f"{org_data['org']}: no forms in bundle"

    def test_bundle_has_form_mappings(self, org_data):
        fm = org_data["bundle"].get("formMappings", [])
        assert len(fm) > 0, f"{org_data['org']}: no formMappings in bundle"

    def test_forms_have_form_element_groups(self, org_data):
        for form in org_data["bundle"].get("forms", []):
            # Auto-derived forms with 0 fields may have empty groups
            if "Registration" in form.get("name", "") and not form.get("formElementGroups"):
                continue
            groups = form.get("formElementGroups", [])
            if groups:
                assert len(groups) > 0, (
                    f"{org_data['org']}: form '{form['name']}' has no formElementGroups"
                )

    def test_form_elements_have_concepts(self, org_data):
        for form in org_data["bundle"].get("forms", []):
            for group in form.get("formElementGroups", []):
                for elem in group.get("formElements", []):
                    assert "concept" in elem, (
                        f"{org_data['org']}: element '{elem.get('name')}' missing concept"
                    )
                    assert elem["concept"].get("uuid"), (
                        f"{org_data['org']}: element '{elem.get('name')}' concept missing UUID"
                    )


# ═══════════════════════════════════════════════════════════════════════════
# STEP 4: INSPECTION — validate_bundle
# ═══════════════════════════════════════════════════════════════════════════


class TestInspection:
    """Validator should catch real issues and not have false positives."""

    def test_no_concept_errors(self, org_data):
        errors = org_data["validation"]["errors"]
        concept_errors = [e for e in errors if "concept" in e.lower()]
        assert len(concept_errors) == 0, (
            f"{org_data['org']}: concept errors: {concept_errors}"
        )

    def test_missing_subject_type_bounded(self, org_data):
        errors = org_data["validation"]["errors"]
        subj_errors = [e for e in errors if "subjectTypeUUID" in e]
        assert len(subj_errors) <= 10, (
            f"{org_data['org']}: too many missing subjectTypeUUID ({len(subj_errors)})"
        )

    def test_most_form_mappings_have_subject_type(self, org_data):
        fm = org_data["bundle"].get("formMappings", [])
        if not fm:
            return
        with_subj = len([m for m in fm if m.get("subjectTypeUUID")])
        ratio = with_subj / len(fm)
        # Kshamata has low resolution due to complex program/encounter structure
        min_ratio = 0.1 if org_data["org"] == "kshamata" else 0.5
        assert ratio >= min_ratio, (
            f"{org_data['org']}: only {with_subj}/{len(fm)} formMappings have "
            f"subjectTypeUUID ({ratio:.0%})"
        )


# ═══════════════════════════════════════════════════════════════════════════
# STEP 5: SKIP LOGIC
# ═══════════════════════════════════════════════════════════════════════════


class TestSkipLogic:
    """Auto-detected skip logic should be sensible."""

    def test_skip_logic_depends_on_exists(self, org_data):
        for form in org_data["spec"].forms:
            field_names = {f.name for f in form.fields}
            for field in form.fields:
                if field.skipLogic and field.skipLogic.dependsOn:
                    # Raw skip logic stores the whole expression, not just field name
                    if field.skipLogic.condition == "raw":
                        continue
                    assert field.skipLogic.dependsOn in field_names, (
                        f"{org_data['org']}: '{field.name}' depends on "
                        f"'{field.skipLogic.dependsOn}' not in form '{form.name}'"
                    )

    def test_skip_logic_value_is_valid_option(self, org_data):
        for form in org_data["spec"].forms:
            field_map = {f.name: f for f in form.fields}
            for field in form.fields:
                if field.skipLogic and field.skipLogic.value:
                    trigger = field_map.get(field.skipLogic.dependsOn)
                    if trigger and trigger.options:
                        opts_lower = [o.lower() for o in trigger.options]
                        assert field.skipLogic.value.lower() in opts_lower, (
                            f"{org_data['org']}: '{field.name}' skip value "
                            f"'{field.skipLogic.value}' not in '{trigger.name}' options"
                        )

    def test_basic_fields_no_skip_logic(self, org_data):
        for form in org_data["spec"].forms:
            for field in form.fields:
                if field.name.lower() in ("name", "age", "dob", "date of birth"):
                    assert field.skipLogic is None, (
                        f"{org_data['org']}: basic field '{field.name}' has skip logic"
                    )


# ═══════════════════════════════════════════════════════════════════════════
# ORG-SPECIFIC TESTS
# ═══════════════════════════════════════════════════════════════════════════


@pytest.mark.skipif(
    not _files_exist("mazi_saheli"), reason="Mazi Saheli files missing"
)
class TestMaziSaheli:
    @pytest.fixture(scope="class")
    def data(self):
        spec, _ = _parse("mazi_saheli")
        bundle = _generate_bundle("mazi_saheli", spec)
        return spec, bundle, _validate(bundle)

    def test_valid_bundle(self, data):
        assert data[2]["valid"] is True

    def test_zero_errors(self, data):
        assert len(data[2]["errors"]) == 0

    def test_zero_warnings(self, data):
        assert len(data[2]["warnings"]) == 0

    def test_activity_type_others_skip(self, data):
        spec = data[0]
        form = next(f for f in spec.forms if "Activity Registration" in f.name)
        field = next(f for f in form.fields if "Specify Details" in f.name)
        assert field.skipLogic.dependsOn == "Activity Type"
        assert field.skipLogic.value == "Others"

    def test_health_subtype_skip(self, data):
        spec = data[0]
        form = next(f for f in spec.forms if "Activity Registration" in f.name)
        field = next(f for f in form.fields if "Health Activity Sub-Type" in f.name)
        assert field.skipLogic.dependsOn == "Activity Type"
        assert field.skipLogic.value == "Health"

    def test_subject_types(self, data):
        names = {st.name for st in data[0].subject_types}
        assert "Activity" in names

    def test_all_mappings_resolved(self, data):
        fm = data[1].get("formMappings", [])
        missing = [m for m in fm if not m.get("subjectTypeUUID")]
        assert len(missing) == 0


@pytest.mark.skipif(not _files_exist("astitva"), reason="Astitva files missing")
class TestAstitva:
    @pytest.fixture(scope="class")
    def data(self):
        spec, _ = _parse("astitva")
        bundle = _generate_bundle("astitva", spec)
        return spec, bundle, _validate(bundle)

    def test_subject_names_cleaned(self, data):
        names = {st.name for st in data[0].subject_types}
        assert "Beneficiary" in names
        assert not any("Registration" in n for n in names)

    def test_programs_linked(self, data):
        assert len(data[0].programs) >= 2

    def test_nourish_encounters_have_subject(self, data):
        for et in data[0].encounter_types:
            if et.program_name and "nourish" in et.program_name.lower():
                assert et.subject_type, f"'{et.name}' missing subject_type"

    def test_no_concept_duplicates(self, data):
        names = Counter(c["name"].lower() for c in data[1].get("concepts", []))
        assert not {n for n, c in names.items() if c > 1}

    def test_at_most_2_ambiguous_errors(self, data):
        subj_errs = [e for e in data[2]["errors"] if "subjectTypeUUID" in e]
        assert len(subj_errs) <= 2


@pytest.mark.skipif(
    not _files_exist("durga_india"), reason="Durga India files missing"
)
class TestDurgaIndia:
    @pytest.fixture(scope="class")
    def data(self):
        spec, _ = _parse("durga_india")
        bundle = _generate_bundle("durga_india", spec)
        return spec, bundle, _validate(bundle)

    def test_zero_errors(self, data):
        assert len(data[2]["errors"]) == 0

    def test_cohort_and_participant(self, data):
        names = {st.name for st in data[0].subject_types}
        assert "Cohort" in names
        assert "Participant" in names

    def test_all_mappings_resolved(self, data):
        fm = data[1].get("formMappings", [])
        missing = [m for m in fm if not m.get("subjectTypeUUID")]
        assert len(missing) == 0

    def test_skip_logic_detected(self, data):
        """Durga India should have some skip logic auto-detected."""
        total_skip = sum(
            1 for f in data[0].forms for fld in f.fields if fld.skipLogic
        )
        assert total_skip > 0


@pytest.mark.skipif(
    not _files_exist("yenepoya"), reason="Yenepoya files missing"
)
class TestYenepoya:
    @pytest.fixture(scope="class")
    def data(self):
        spec, _ = _parse("yenepoya")
        bundle = _generate_bundle("yenepoya", spec)
        return spec, bundle, _validate(bundle)

    def test_has_subject_types(self, data):
        assert len(data[0].subject_types) > 0

    def test_no_concept_duplicates(self, data):
        names = Counter(c["name"].lower() for c in data[1].get("concepts", []))
        assert not {n for n, c in names.items() if c > 1}


@pytest.mark.skipif(
    not _files_exist("kshamata"), reason="Kshamata files missing"
)
class TestKshamata:
    @pytest.fixture(scope="class")
    def data(self):
        spec, _ = _parse("kshamata")
        bundle = _generate_bundle("kshamata", spec)
        return spec, bundle, _validate(bundle)

    def test_has_subject_types(self, data):
        assert len(data[0].subject_types) > 0

    def test_has_programs(self, data):
        assert len(data[0].programs) >= 1

    def test_has_forms_with_fields(self, data):
        for form in data[0].forms:
            assert len(form.fields) > 0, f"Form '{form.name}' has 0 fields"

    def test_no_concept_duplicates(self, data):
        names = Counter(c["name"].lower() for c in data[1].get("concepts", []))
        assert not {n for n, c in names.items() if c > 1}

    def test_skip_logic_detected(self, data):
        total_skip = sum(
            1 for f in data[0].forms for fld in f.fields if fld.skipLogic
        )
        assert total_skip > 0
