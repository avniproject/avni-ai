"""
Tests for Story #1706: Create entities based on field workflow specification document.

Tests the bundle generator, UUID registry, and uploader using
manually constructed ParsedEntities (simulating LLM extraction output).
"""

import json

import pytest

from src.tools.bundle.bundle_generator import generate_bundle, export_bundle_to_directory
from src.tools.bundle.uuid_registry import generate_uuid, get_standard_uuid
from src.tools.bundle.bundle_uploader import assemble_metadata_zip
from src.tools.bundle.models import (
    Bundle,
    AddressLevelTypeContract,
    EncounterTypeContract,
    FormMappingContract,
    ProgramContract,
    SubjectTypeContract,
    SubjectTypeEnum,
    ParsedEncounter,
    ParsedEntities,
    ParsedLocationHierarchy,
    ParsedLocationLevel,
    ParsedProgram,
    ParsedSubjectType,
)


# ─── Test fixtures ─────────────────────────────────────────────────────────


@pytest.fixture
def sample_entities():
    """Simulates what the LLM extraction + handler rebuild produces."""
    return ParsedEntities(
        subject_types=[
            ParsedSubjectType(name="Beneficiary Registration", type="Person", form_link="Beneficiary Registration"),
            ParsedSubjectType(name="School Registration", type="Individual", description="They will provide the list of schools"),
            ParsedSubjectType(name="Anganwadi Registration", type="Individual"),
        ],
        programs=[
            ParsedProgram(name="Nourish - Pregnancy Enrollment", target_subject_type="Beneficiary Registration",
                          enrolment_form="Nourish Enrollment", exit_form="Nourish - Pregnancy Exit"),
            ParsedProgram(name="Nourish - Child Enrolment", target_subject_type="Beneficiary Registration",
                          enrolment_form="Nourish - Child Enrolment", exit_form="Nourish - Child Exit"),
            ParsedProgram(name="Enrich", target_subject_type="Beneficiary Registration",
                          enrolment_form="Enrich Enrollment", exit_form="Enrich Exit"),
        ],
        encounters=[
            ParsedEncounter(name="Leave form", subject_type="User", encounter_type="Unscheduled"),
            ParsedEncounter(name="Indent Register (Stock Requirement)", subject_type="Anganwadi", encounter_type="Scheduled"),
            ParsedEncounter(name="Field Visit", subject_type="Anganwadi", encounter_type="Scheduled"),
            ParsedEncounter(name="Awareness Register", subject_type="Beneficiary", encounter_type="Scheduled"),
        ],
        program_encounters=[
            ParsedEncounter(name="AN Growth Monitoring", program_name="Nourish", encounter_type="Scheduled", is_program_encounter=True),
            ParsedEncounter(name="Delivery", program_name="Nourish", encounter_type="Unscheduled", is_program_encounter=True),
            ParsedEncounter(name="Growth Monitoring", program_name="Nourish", encounter_type="Scheduled", is_program_encounter=True),
            ParsedEncounter(name="Enrich Growth Monitoring - Baseline", program_name="Enrich", encounter_type="Scheduled", is_program_encounter=True),
            ParsedEncounter(name="Enrich Endline", program_name="Enrich", encounter_type="Scheduled", is_program_encounter=True),
            ParsedEncounter(name="Health Education Session", program_name="Enrich", encounter_type="Scheduled", is_program_encounter=True),
        ],
        location_hierarchies=[
            ParsedLocationHierarchy(levels=[
                ParsedLocationLevel(name="District", level=3, parent=None),
                ParsedLocationLevel(name="Block", level=2, parent="District"),
                ParsedLocationLevel(name="Hamlet", level=1, parent="Block"),
            ]),
            ParsedLocationHierarchy(levels=[
                ParsedLocationLevel(name="District", level=3, parent=None),
                ParsedLocationLevel(name="Block", level=2, parent="District"),
                ParsedLocationLevel(name="School", level=1, parent="Block"),
            ]),
        ],
    )


# ─── UUID Registry ─────────────────────────────────────────────────────────


class TestUUIDRegistry:
    def test_standard_answer_lookup(self):
        assert get_standard_uuid("YES") == "4dc151b8-3333-4293-9169-07c58280c0ee"
        assert get_standard_uuid("NO") == "4eaf65b5-a032-40b3-927a-2d03e44b934f"
        assert get_standard_uuid("Male") == "924de7e5-47d9-401a-9178-3336fee5ee03"

    def test_standard_uuid_returns_none_for_unknown(self):
        assert get_standard_uuid("Some Custom Answer") is None

    def test_generates_valid_uuid4(self):
        result = generate_uuid()
        parts = result.split("-")
        assert len(parts) == 5
        assert [len(p) for p in parts] == [8, 4, 4, 4, 12]

    def test_generates_unique_uuids(self):
        uuids = {generate_uuid() for _ in range(100)}
        assert len(uuids) == 100


# ─── Bundle Generator ─────────────────────────────────────────────────────


class TestBundleGenerator:
    def test_returns_typed_bundle(self, sample_entities):
        bundle = generate_bundle(sample_entities, org_name="Test-Org")
        assert isinstance(bundle, Bundle)

    def test_subject_types(self, sample_entities):
        bundle = generate_bundle(sample_entities, org_name="Test-Org")
        assert len(bundle.subject_types) == 3
        for st in bundle.subject_types:
            assert isinstance(st, SubjectTypeContract)
            assert st.uuid
            assert isinstance(st.type, SubjectTypeEnum)

    def test_programs(self, sample_entities):
        bundle = generate_bundle(sample_entities, org_name="Test-Org")
        assert len(bundle.programs) == 3
        for prog in bundle.programs:
            assert isinstance(prog, ProgramContract)
            assert prog.uuid
            assert prog.colour

    def test_encounter_types_no_duplicates(self, sample_entities):
        bundle = generate_bundle(sample_entities, org_name="Test-Org")
        assert len(bundle.encounter_types) == 10
        names = [et.name for et in bundle.encounter_types]
        assert len(names) == len(set(n.lower() for n in names))

    def test_address_level_types(self, sample_entities):
        bundle = generate_bundle(sample_entities, org_name="Test-Org")
        assert len(bundle.address_level_types) == 4  # District, Block, Hamlet, School
        for alt in bundle.address_level_types:
            assert isinstance(alt, AddressLevelTypeContract)
            assert alt.uuid
            assert alt.name
            assert alt.level >= 1

    def test_form_mappings(self, sample_entities):
        bundle = generate_bundle(sample_entities, org_name="Test-Org")
        assert len(bundle.form_mappings) >= 5
        for fm in bundle.form_mappings:
            assert isinstance(fm, FormMappingContract)
            assert fm.subject_type_uuid

    def test_form_mapping_types(self, sample_entities):
        bundle = generate_bundle(sample_entities, org_name="Test-Org")
        form_types = {fm.form_type for fm in bundle.form_mappings}
        assert "IndividualProfile" in form_types
        assert "ProgramEnrolment" in form_types

    def test_to_asset_dict(self, sample_entities):
        bundle = generate_bundle(sample_entities, org_name="Test-Org")
        assets = bundle.to_asset_dict()
        assert "subjectTypes" in assets
        assert "programs" in assets
        assert "encounterTypes" in assets
        assert "formMappings" in assets
        assert isinstance(assets["subjectTypes"], list)
        st = assets["subjectTypes"][0]
        assert "allowMiddleName" in st
        assert "shouldSyncByLocation" in st

    def test_export_to_directory(self, sample_entities, tmp_path):
        bundle = generate_bundle(sample_entities, org_name="Test-Org")
        output_dir = export_bundle_to_directory(bundle, tmp_path / "test-output")
        assert output_dir.exists()
        assert (output_dir / "subjectTypes.json").exists()
        with open(output_dir / "subjectTypes.json") as f:
            data = json.load(f)
            assert len(data) == 3

    def test_cancellation_form_mappings(self, sample_entities):
        bundle = generate_bundle(sample_entities, org_name="Test-Org")
        cancel_mappings = [fm for fm in bundle.form_mappings if "Cancellation" in fm.form_type]
        assert len(cancel_mappings) >= 1


# ─── Bundle Uploader ──────────────────────────────────────────────────────


class TestBundleUploader:
    def test_assemble_zip(self):
        bundle = Bundle(
            subject_types=[SubjectTypeContract(name="Test", uuid="test-uuid", type=SubjectTypeEnum.PERSON)],
        )
        zip_bytes = assemble_metadata_zip(bundle)
        assert len(zip_bytes) > 0

        import zipfile
        import io
        zf = zipfile.ZipFile(io.BytesIO(zip_bytes))
        assert "subjectTypes.json" in zf.namelist()
        content = json.loads(zf.read("subjectTypes.json"))
        assert content[0]["name"] == "Test"


# ─── Full Pipeline ────────────────────────────────────────────────────────


class TestFullPipeline:
    def test_end_to_end(self, sample_entities, tmp_path):
        # 1. Generate bundle
        bundle = generate_bundle(sample_entities, org_name="Pipeline-Test")
        assert bundle.subject_types
        assert bundle.programs
        assert bundle.encounter_types

        # 2. Export
        export_bundle_to_directory(bundle, tmp_path / "pipeline")

        # 3. ZIP
        zip_bytes = assemble_metadata_zip(bundle)
        assert len(zip_bytes) > 0

        # 4. Verify referential integrity
        st_uuids = {st.uuid for st in bundle.subject_types}
        for fm in bundle.form_mappings:
            assert fm.subject_type_uuid in st_uuids

        et_uuids = {et.uuid for et in bundle.encounter_types}
        for oet in bundle.operational_encounter_types:
            assert oet["encounterType"]["uuid"] in et_uuids

    def test_uuids_are_unique(self, sample_entities):
        bundle = generate_bundle(sample_entities, org_name="UUID-Test")
        all_uuids = []
        all_uuids.extend(st.uuid for st in bundle.subject_types)
        all_uuids.extend(p.uuid for p in bundle.programs)
        all_uuids.extend(et.uuid for et in bundle.encounter_types)
        all_uuids.extend(alt.uuid for alt in bundle.address_level_types)
        all_uuids.extend(fm.uuid for fm in bundle.form_mappings)
        assert len(all_uuids) == len(set(all_uuids))
