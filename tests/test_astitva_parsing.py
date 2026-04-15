"""
Tests for Astitva SRS parsing — form type classification, fuzzy encounter
matching, subject type resolution, and end-to-end bundle generation.
"""

from pathlib import Path

import pytest

from src.bundle.scoping_parser import (
    parse_scoping_docs,
    _clean_subject_name,
    _is_header_row,
)
from src.bundle.generator import BundleGenerator
from src.bundle.validators import BundleValidator

_ASTITVA_FILES = [
    Path("tests/resources/scoping/Astitva SRS .xlsx"),
    Path("tests/resources/scoping/Astitva Modelling.xlsx"),
    Path("tests/resources/scoping/Astitva Nourish Program Forms.xlsx"),
]

# Skip all tests if resource files are missing
pytestmark = pytest.mark.skipif(
    not all(f.exists() for f in _ASTITVA_FILES),
    reason="Astitva SRS resource files not present",
)


@pytest.fixture(scope="module")
def parsed_spec():
    spec, misc = parse_scoping_docs([str(f) for f in _ASTITVA_FILES])
    return spec, misc


@pytest.fixture(scope="module")
def bundle_validation(parsed_spec):
    spec, _ = parsed_spec
    entities = spec.model_dump()
    gen = BundleGenerator("Astitva")
    gen.generate(entities)
    validator = BundleValidator(gen.bundle)
    return gen.bundle, validator.validate()


class TestSubjectNameCleaning:
    """Subject type names should strip form-like suffixes."""

    @pytest.mark.parametrize(
        "raw,expected",
        [
            ("Beneficiary Registration", "Beneficiary"),
            ("School Registration", "School"),
            ("Anganwadi Registration", "Anganwadi"),
            ("Woman", "Woman"),
            ("Child Enrolment", "Child"),
        ],
    )
    def test_clean_subject_name(self, raw, expected):
        assert _clean_subject_name(raw) == expected


class TestHeaderRowFiltering:
    """Header row values should be detected and filtered."""

    @pytest.mark.parametrize(
        "name,is_header",
        [
            ("Encounter Name", True),
            ("Subject Type", True),
            ("Program Name", True),
            ("Type", True),
            ("AN Growth Monitoring", False),
            ("Beneficiary", False),
        ],
    )
    def test_is_header_row(self, name, is_header):
        assert _is_header_row(name) == is_header


class TestAstitvaSubjectTypes:
    """Subject types parsed from Astitva SRS."""

    def test_count(self, parsed_spec):
        spec, _ = parsed_spec
        assert len(spec.subject_types) == 3

    def test_names_cleaned(self, parsed_spec):
        spec, _ = parsed_spec
        names = {st.name for st in spec.subject_types}
        assert "Beneficiary" in names
        assert "School" in names
        assert "Anganwadi" in names
        # Should NOT have "Registration" suffix
        assert not any("Registration" in n for n in names)

    def test_no_header_rows(self, parsed_spec):
        spec, _ = parsed_spec
        names = {st.name.lower() for st in spec.subject_types}
        assert "subject type" not in names
        assert "name" not in names


class TestAstitvaEncounterTypes:
    """Encounter type parsing and subject/program linkage."""

    def test_no_header_rows(self, parsed_spec):
        spec, _ = parsed_spec
        names = {et.name.lower() for et in spec.encounter_types}
        assert "encounter name" not in names
        assert "subject type" not in names

    def test_program_encounters_have_subject_type(self, parsed_spec):
        spec, _ = parsed_spec
        nourish_encounters = [et for et in spec.encounter_types if et.program_name]
        for et in nourish_encounters:
            assert et.subject_type, (
                f"Encounter '{et.name}' has program '{et.program_name}' "
                f"but no subject_type"
            )


class TestAstitvaFormTypeClassification:
    """Forms should be classified as IndividualProfile, ProgramEnrolment, etc."""

    def test_registration_forms_are_individual_profile(self, parsed_spec):
        spec, _ = parsed_spec
        reg_forms = [f for f in spec.forms if "Registration" in f.name]
        for f in reg_forms:
            assert f.formType == "IndividualProfile", (
                f"'{f.name}' should be IndividualProfile, got {f.formType}"
            )

    def test_enrolment_forms_are_program_enrolment(self, parsed_spec):
        spec, _ = parsed_spec
        enrol_forms = [
            f for f in spec.forms if "Enrolment" in f.name or "Enrollment" in f.name
        ]
        for f in enrol_forms:
            assert f.formType == "ProgramEnrolment", (
                f"'{f.name}' should be ProgramEnrolment, got {f.formType}"
            )

    def test_exit_forms_are_program_exit(self, parsed_spec):
        spec, _ = parsed_spec
        exit_forms = [f for f in spec.forms if "Exit" in f.name]
        for f in exit_forms:
            assert f.formType == "ProgramExit", (
                f"'{f.name}' should be ProgramExit, got {f.formType}"
            )

    def test_registration_forms_have_subject_type(self, parsed_spec):
        spec, _ = parsed_spec
        reg_forms = [f for f in spec.forms if f.formType == "IndividualProfile"]
        for f in reg_forms:
            assert f.subjectType, f"Registration form '{f.name}' has no subjectType"


class TestAstitvaFuzzyEncounterMatching:
    """Forms should match to encounter types even with truncated/partial names."""

    def test_truncated_name_matches(self, parsed_spec):
        """'Mother Monitoring - HCCM Daily' should match encounter
        'Mother Monitoring - HCCM Daily Consumption'."""
        spec, _ = parsed_spec
        form = next((f for f in spec.forms if "Mother Monitoring" in f.name), None)
        assert form is not None
        assert form.encounterType == "Mother Monitoring - HCCM Daily Consumption"

    def test_partial_name_matches(self, parsed_spec):
        """'Indent Register' should match 'Indent Register (Stock Requirement)'."""
        spec, _ = parsed_spec
        form = next((f for f in spec.forms if f.name == "Indent Register"), None)
        assert form is not None
        assert form.encounterType == "Indent Register (Stock Requirement)"

    def test_substring_match_field_visit(self, parsed_spec):
        """'Field Visit Page (Nourish – Sup' should match 'Field Visit'."""
        spec, _ = parsed_spec
        form = next((f for f in spec.forms if "Field Visit" in f.name), None)
        assert form is not None
        assert form.encounterType == "Field Visit"


class TestAstitvaProgramSubjectResolution:
    """Encounters linked to programs should resolve subject type from program."""

    def test_nourish_encounters_resolve_to_beneficiary(self, parsed_spec):
        spec, _ = parsed_spec
        nourish_enc = [
            et
            for et in spec.encounter_types
            if et.program_name and "nourish" in et.program_name.lower()
        ]
        assert len(nourish_enc) > 0
        for et in nourish_enc:
            assert et.subject_type == "Beneficiary", (
                f"'{et.name}' (program={et.program_name}) should resolve to "
                f"Beneficiary, got '{et.subject_type}'"
            )


class TestAstitvaBundleGeneration:
    """End-to-end bundle generation from Astitva SRS."""

    def test_bundle_valid(self, bundle_validation):
        _, vr = bundle_validation
        assert vr["valid"] is True

    def test_zero_errors(self, bundle_validation):
        _, vr = bundle_validation
        assert len(vr["errors"]) == 0

    def test_no_duplicate_concepts(self, bundle_validation):
        bundle, _ = bundle_validation
        from collections import Counter

        names = Counter(c["name"].lower() for c in bundle.get("concepts", []))
        dupes = {n: c for n, c in names.items() if c > 1}
        assert len(dupes) == 0, f"Duplicate concepts: {dupes}"

    def test_most_form_mappings_have_subject_type(self, bundle_validation):
        bundle, _ = bundle_validation
        fm = bundle.get("formMappings", [])
        missing = [m for m in fm if not m.get("subjectTypeUUID")]
        # Allow at most 2 missing (genuinely ambiguous cases)
        assert len(missing) <= 2, (
            f"{len(missing)} formMappings missing subjectTypeUUID: "
            f"{[m['formName'] for m in missing]}"
        )

    def test_most_encounter_mappings_have_encounter_type(self, bundle_validation):
        bundle, _ = bundle_validation
        fm = bundle.get("formMappings", [])
        enc_types = (
            "Encounter",
            "ProgramEncounter",
            "IndividualEncounterCancellation",
            "ProgramEncounterCancellation",
        )
        enc_fm = [m for m in fm if m.get("formType") in enc_types]
        missing = [m for m in enc_fm if not m.get("encounterTypeUUID")]
        assert len(missing) <= 2, (
            f"{len(missing)} encounter formMappings missing encounterTypeUUID: "
            f"{[m['formName'] for m in missing]}"
        )
