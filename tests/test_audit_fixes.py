"""
Tests for critical audit fixes: A10 (UUID determinism), A3 (cancellation concepts),
A4 (groupPrivilege filename), C1 (form field extraction from scoping docs).
"""

from __future__ import annotations

import zipfile
from io import BytesIO
from pathlib import Path

import pytest

from src.bundle.generator import BundleGenerator
from src.bundle.scoping_parser import (
    _is_form_sheet,
    _parse_min_max,
    _parse_options,
    _parse_yes_no,
    parse_scoping_doc,
)
from src.bundle.uuid_utils import generate_deterministic_uuid

_SCOPING_DOC = (
    Path(__file__).parent
    / "resources"
    / "scoping"
    / "Durga India Scoping Document.xlsx"
)
_MODELLING_DOC = (
    Path(__file__).parent / "resources" / "scoping" / "Durga India Modelling.xlsx"
)


# ── A10: UUID determinism ────────────────────────────────────────────────────


class TestUUIDDeterminism:
    def test_same_seed_same_uuid(self):
        u1 = generate_deterministic_uuid("subjectType:Cohort")
        u2 = generate_deterministic_uuid("subjectType:Cohort")
        assert u1 == u2

    def test_different_seed_different_uuid(self):
        u1 = generate_deterministic_uuid("subjectType:Cohort")
        u2 = generate_deterministic_uuid("subjectType:Participant")
        assert u1 != u2

    def test_uuid_format(self):
        u = generate_deterministic_uuid("test:seed")
        parts = u.split("-")
        assert len(parts) == 5
        assert all(len(p) > 0 for p in parts)

    def test_empty_seed(self):
        u1 = generate_deterministic_uuid("")
        u2 = generate_deterministic_uuid("")
        assert u1 == u2

    def test_idempotent_bundle_uuids(self):
        """Two independent BundleGenerator runs should produce identical UUIDs."""
        gen1 = BundleGenerator("TestOrg")
        gen1.process_subject_types([{"name": "Person"}])
        gen2 = BundleGenerator("TestOrg")
        gen2.process_subject_types([{"name": "Person"}])
        assert (
            gen1.bundle["subjectTypes"][0]["uuid"]
            == gen2.bundle["subjectTypes"][0]["uuid"]
        )


# ── A3: Cancellation concepts ───────────────────────────────────────────────


class TestCancellationConcepts:
    def test_cancellation_concepts_registered(self):
        """Cancellation form concepts must appear in bundle concepts list."""
        gen = BundleGenerator("TestOrg")
        gen.process_subject_types([{"name": "Person"}])
        gen.process_encounter_types([{"name": "Visit", "programEncounter": False}])
        gen.process_forms(
            [
                {
                    "name": "Visit",
                    "formType": "Encounter",
                    "subjectType": "Person",
                    "encounterType": "Visit",
                    "fields": [],
                }
            ]
        )
        concept_names = [c["name"] for c in gen.bundle["concepts"]]
        assert "Visit cancellation reason" in concept_names

    def test_cancellation_concept_has_uuid(self):
        gen = BundleGenerator("TestOrg")
        gen.process_encounter_types([{"name": "Checkup", "programEncounter": False}])
        gen.process_forms(
            [
                {
                    "name": "Checkup",
                    "formType": "Encounter",
                    "subjectType": "Person",
                    "encounterType": "Checkup",
                    "fields": [],
                }
            ]
        )
        cancel_concepts = [
            c for c in gen.bundle["concepts"] if "cancellation" in c["name"].lower()
        ]
        assert len(cancel_concepts) == 1
        assert cancel_concepts[0]["uuid"]
        assert cancel_concepts[0]["dataType"] == "Text"


# ── A4: groupPrivilege filename ──────────────────────────────────────────────


class TestGroupPrivilegeFilename:
    def test_zip_contains_singular_filename(self):
        gen = BundleGenerator("TestOrg")
        gen.process_subject_types([{"name": "Person"}])
        gen.process_groups([{"name": "Everyone"}])
        gen._generate_operational_configs()
        gen._generate_organisation_config()
        gen._generate_group_privileges()
        gen._generate_report_cards()
        gen._generate_report_dashboard()
        zip_bytes = gen.to_zip_bytes()

        with zipfile.ZipFile(BytesIO(zip_bytes)) as zf:
            names = zf.namelist()
            assert "groupPrivilege.json" in names, (
                f"Expected groupPrivilege.json, got {names}"
            )
            assert "groupPrivileges.json" not in names, (
                "groupPrivileges.json should NOT exist"
            )


# ── C1: Form field extraction ────────────────────────────────────────────────


class TestFormSheetDetection:
    @pytest.mark.skipif(not _SCOPING_DOC.exists(), reason="Scoping doc not available")
    def test_scoping_doc_form_sheets_detected(self):
        import pandas as pd

        xf = pd.ExcelFile(_SCOPING_DOC)
        form_sheets = [s for s in xf.sheet_names if _is_form_sheet(xf, s)]
        assert len(form_sheets) >= 7
        # Known form sheets
        form_names_lower = [s.lower().strip() for s in form_sheets]
        assert any("session" in n for n in form_names_lower)
        assert any("baseline for women" in n for n in form_names_lower)
        assert any("participant" in n for n in form_names_lower)

    @pytest.mark.skipif(
        not _MODELLING_DOC.exists(), reason="Modelling doc not available"
    )
    def test_modelling_doc_no_form_sheets(self):
        import pandas as pd

        xf = pd.ExcelFile(_MODELLING_DOC)
        form_sheets = [s for s in xf.sheet_names if _is_form_sheet(xf, s)]
        assert len(form_sheets) == 0


class TestFormFieldParsing:
    @pytest.mark.skipif(not _SCOPING_DOC.exists(), reason="Scoping doc not available")
    def test_scoping_doc_parses_forms(self):
        spec = parse_scoping_doc(str(_SCOPING_DOC))
        assert len(spec.forms) >= 7
        # Check that forms have populated fields (not empty)
        total_fields = sum(len(f.fields) for f in spec.forms)
        assert total_fields > 50, f"Expected >50 total fields, got {total_fields}"

    @pytest.mark.skipif(not _SCOPING_DOC.exists(), reason="Scoping doc not available")
    def test_form_fields_have_data_types(self):
        spec = parse_scoping_doc(str(_SCOPING_DOC))
        for form in spec.forms:
            for field in form.fields:
                assert field.dataType in (
                    "Text",
                    "Numeric",
                    "Date",
                    "Coded",
                    "Subject",
                    "Duration",
                    "Notes",
                    "ImageV2",
                    "PhoneNumber",
                    "Location",
                    "DateTime",
                    "File",
                    "Audio",
                    "Video",
                ), f"Unexpected dataType '{field.dataType}' for field '{field.name}'"

    @pytest.mark.skipif(not _SCOPING_DOC.exists(), reason="Scoping doc not available")
    def test_coded_fields_have_options(self):
        spec = parse_scoping_doc(str(_SCOPING_DOC))
        coded_fields = [
            f for form in spec.forms for f in form.fields if f.dataType == "Coded"
        ]
        # At least some Coded fields should have options
        with_options = [f for f in coded_fields if f.options]
        assert len(with_options) > 0, "No Coded fields have options parsed"

    @pytest.mark.skipif(not _SCOPING_DOC.exists(), reason="Scoping doc not available")
    def test_form_sections_populated(self):
        spec = parse_scoping_doc(str(_SCOPING_DOC))
        for form in spec.forms:
            assert len(form.sections) > 0, f"Form '{form.name}' has no sections"

    @pytest.mark.skipif(
        not _MODELLING_DOC.exists(), reason="Modelling doc not available"
    )
    def test_modelling_doc_backward_compat(self):
        """Modelling-only doc should still work — returns 0 forms."""
        spec = parse_scoping_doc(str(_MODELLING_DOC))
        assert len(spec.subject_types) >= 2
        assert len(spec.encounter_types) >= 5
        assert len(spec.forms) == 0


# ── Helper function tests ────────────────────────────────────────────────────


class TestHelpers:
    def test_parse_yes_no(self):
        assert _parse_yes_no("Yes") is True
        assert _parse_yes_no("yes") is True
        assert _parse_yes_no("Y") is True
        assert _parse_yes_no("No") is False
        assert _parse_yes_no("") is False
        assert _parse_yes_no(None) is False

    def test_parse_options_newline(self):
        assert _parse_options("A\nB\nC") == ["A", "B", "C"]

    def test_parse_options_comma(self):
        assert _parse_options("A,B,C") == ["A", "B", "C"]

    def test_parse_options_semicolon(self):
        assert _parse_options("A;B;C") == ["A", "B", "C"]

    def test_parse_options_empty(self):
        assert _parse_options("") == []
        assert _parse_options(None) == []

    def test_parse_min_max_dash(self):
        assert _parse_min_max("0-100") == (0.0, 100.0)

    def test_parse_min_max_to(self):
        assert _parse_min_max("18 to 99") == (18.0, 99.0)

    def test_parse_min_max_empty(self):
        assert _parse_min_max("") == (None, None)
        assert _parse_min_max(None) == (None, None)
