"""
Pytest test cases for the App Configurator Flow emulation.

These tests exercise the full PEV loop against the staging backend.

Usage:
    export AVNI_MCP_SERVER_URL="https://staging-ai.avniproject.org/"
    export AVNI_AUTH_TOKEN="<your-staging-token>"
    python -m pytest tests/emulation/test_app_configurator_flow.py -v -s
"""

from __future__ import annotations

import logging
import os

import pytest

from .app_configurator_flow import AppConfiguratorFlow, load_sample_entities
from src.bundle.scoping_parser import load_durga_entities
from src.schemas.bundle_models import EntitySpec

logger = logging.getLogger(__name__)


# ── Fixtures ─────────────────────────────────────────────────────

@pytest.fixture(scope="session")
def env_check():
    """Ensure required environment variables are set."""
    from dotenv import load_dotenv
    load_dotenv()

    token = os.environ.get("AVNI_AUTH_TOKEN", "")
    if not token or token == "new_org_for_testing_auth_token_here":
        pytest.skip(
            "AVNI_AUTH_TOKEN not configured. "
            "Set a valid staging token in .env to run emulation tests."
        )
    url = os.environ.get("AVNI_MCP_SERVER_URL", "")
    if not url:
        pytest.skip("AVNI_MCP_SERVER_URL not configured.")


@pytest.fixture
def flow(env_check) -> AppConfiguratorFlow:
    """Create a fresh AppConfiguratorFlow instance."""
    return AppConfiguratorFlow.from_env()


@pytest.fixture
def sample_entities() -> dict:
    """Load sample entities for testing."""
    return load_sample_entities()


# ── Health Check ─────────────────────────────────────────────────

class TestHealthCheck:
    def test_server_reachable(self, flow: AppConfiguratorFlow):
        """Staging server responds to /health."""
        assert flow.health_check(), (
            f"Server at {flow.state.avni_mcp_server_url} is not reachable. "
            "Check AVNI_MCP_SERVER_URL and network."
        )


# ── Phase A: Entity Store & Validate ─────────────────────────────

class TestEntityPhase:
    def test_store_entities(self, flow: AppConfiguratorFlow, sample_entities: dict):
        """POST /store-entities succeeds."""
        flow.state.entities_jsonl = sample_entities
        result = flow.post(
            "/store-entities",
            {"conversation_id": flow.conversation_id, "entities": flow.state.entities_jsonl},
        )
        assert result.get("ok") is True

    def test_validate_entities(self, flow: AppConfiguratorFlow, sample_entities: dict):
        """POST /validate-entities returns structured validation result."""
        flow.state.entities_jsonl = sample_entities
        # Store first
        flow.post(
            "/store-entities",
            {"conversation_id": flow.conversation_id, "entities": flow.state.entities_jsonl},
        )
        # Validate
        result = flow.post(
            "/validate-entities",
            {"conversation_id": flow.conversation_id},
        )
        assert "issues" in result
        assert "error_count" in result
        assert "warning_count" in result
        assert "has_errors" in result
        assert "entities" in result
        logger.info("Validation: %d errors, %d warnings", result["error_count"], result["warning_count"])

    def test_store_and_validate_combined(self, flow: AppConfiguratorFlow, sample_entities: dict):
        """store_and_validate_entities() method works end-to-end."""
        flow.state.entities_jsonl = sample_entities
        validation = flow.store_and_validate_entities()
        assert isinstance(validation, dict)
        assert "error_count" in validation


# ── Phase C: Spec Generation ─────────────────────────────────────

class TestSpecPhase:
    def test_generate_spec(self, flow: AppConfiguratorFlow, sample_entities: dict):
        """POST /generate-spec produces valid YAML."""
        flow.state.entities_jsonl = sample_entities
        flow.store_and_validate_entities()

        result = flow.post(
            "/generate-spec",
            {"conversation_id": flow.conversation_id, "org_name": flow.state.org_name},
        )
        assert "spec_yaml" in result
        assert len(result["spec_yaml"]) > 0
        logger.info("Generated spec: %d chars", len(result["spec_yaml"]))

    def test_validate_spec(self, flow: AppConfiguratorFlow, sample_entities: dict):
        """POST /validate-spec returns structured result."""
        flow.state.entities_jsonl = sample_entities
        flow.store_and_validate_entities()

        gen_result = flow.post(
            "/generate-spec",
            {"conversation_id": flow.conversation_id, "org_name": flow.state.org_name},
        )
        spec_yaml = gen_result["spec_yaml"]

        val_result = flow.post("/validate-spec", {"spec_yaml": spec_yaml})
        assert "valid" in val_result
        assert "errors" in val_result
        assert "warnings" in val_result
        logger.info(
            "Spec validation: valid=%s, %d errors, %d warnings",
            val_result["valid"],
            len(val_result["errors"]),
            len(val_result["warnings"]),
        )

    def test_spec_agent_loop(self, flow: AppConfiguratorFlow, sample_entities: dict):
        """run_spec_agent() completes successfully."""
        flow.state.entities_jsonl = sample_entities
        flow.store_and_validate_entities()
        flow.state.cycle_count = 1

        result = flow.run_spec_agent()
        assert result is True
        assert len(flow.state.spec_yaml) > 0
        logger.info("Spec agent produced spec: %d chars", len(flow.state.spec_yaml))


# ── Phase D: Bundle Patch & Upload ───────────────────────────────

class TestBundlePhase:
    def test_download_existing_bundle(self, flow: AppConfiguratorFlow):
        """GET /download-bundle-b64 returns a b64 ZIP."""
        resp = flow.get(
            "/download-bundle-b64",
            auth=True,
            params={"includeLocations": "false"},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert "bundle_zip_b64" in data
        assert len(data["bundle_zip_b64"]) > 0
        logger.info(
            "Downloaded existing bundle: %d bytes",
            data.get("size_bytes", 0),
        )

    def test_patch_bundle(self, flow: AppConfiguratorFlow, sample_entities: dict):
        """POST /patch-bundle produces a patched b64 ZIP."""
        # Setup: generate spec first
        flow.state.entities_jsonl = sample_entities
        flow.store_and_validate_entities()
        gen = flow.post("/generate-spec", {"conversation_id": flow.conversation_id, "org_name": flow.state.org_name})
        spec_yaml = gen["spec_yaml"]

        # Download existing
        resp = flow.get("/download-bundle-b64", auth=True, params={"includeLocations": "false"})
        existing_b64 = resp.json()["bundle_zip_b64"]

        # Patch
        patch_result = flow.post(
            "/patch-bundle",
            {"existing_bundle_b64": existing_b64, "spec_yaml": spec_yaml},
        )
        assert patch_result.get("success") is True
        assert "patched_bundle_b64" in patch_result
        assert patch_result.get("files_patched", 0) > 0
        logger.info(
            "Patched bundle: %d files, %d bytes",
            patch_result["files_patched"],
            patch_result.get("size_bytes", 0),
        )


# ── Full PEV Loop ────────────────────────────────────────────────

class TestFullFlow:
    def test_happy_path(self, flow: AppConfiguratorFlow, sample_entities: dict):
        """
        Full PEV flow: entities → spec → patch bundle → upload → poll.
        Should complete within max_cycles.
        """
        flow.state.entities_jsonl = sample_entities
        result = flow.run()
        flow.print_summary(result)

        # The flow should produce at least one cycle
        assert result.total_cycles >= 1
        assert len(result.cycles) >= 1

        # Log outcome (don't assert success — staging may have issues)
        if result.success:
            logger.info("Full flow SUCCEEDED in %d cycle(s)", result.total_cycles)
        else:
            logger.warning(
                "Full flow did not succeed after %d cycle(s): %s",
                result.total_cycles,
                result.final_error,
            )

    def test_retry_behavior(self, flow: AppConfiguratorFlow, sample_entities: dict):
        """
        Verify the retry loop executes correctly.
        We set max_cycles=2 and observe cycle behavior.
        """
        flow.state.entities_jsonl = sample_entities
        flow.state.max_cycles = 2
        result = flow.run()
        flow.print_summary(result)

        # Should have attempted at most 2 cycles
        assert result.total_cycles <= 2
        assert len(result.cycles) <= 2


# ── Individual Endpoint Tests ────────────────────────────────────

class TestEndpoints:
    """Test individual endpoints in isolation for debugging."""

    def test_apply_entity_corrections(self, flow: AppConfiguratorFlow, sample_entities: dict):
        """POST /apply-entity-corrections updates stored entities."""
        flow.state.entities_jsonl = sample_entities
        flow.post(
            "/store-entities",
            {"conversation_id": flow.conversation_id, "entities": flow.state.entities_jsonl},
        )

        # Add a new encounter type via correction — must reference a known program/subject_type
        durga_programs = [p["name"] for p in sample_entities.get("programs", [])]
        durga_subject_types = [s["name"] for s in sample_entities.get("subject_types", [])]
        prog_ref = durga_programs[0] if durga_programs else "Work With Women"
        st_ref = durga_subject_types[0] if durga_subject_types else "Cohort"

        result = flow.post(
            "/apply-entity-corrections",
            {
                "conversation_id": flow.conversation_id,
                "corrections": [
                    {
                        "entity_type": "encounter_type",
                        "name": "Extra Visit",
                        "program_name": prog_ref,
                        "subject_type": st_ref,
                        "is_program_encounter": True,
                        "is_scheduled": False,
                    }
                ],
            },
        )
        assert "result" in result
        enc_types = result["result"].get("encounter_types", [])
        names = [e["name"] for e in enc_types]
        assert "Extra Visit" in names

    def test_upload_status_not_found(self, flow: AppConfiguratorFlow):
        """GET /upload-status with bad task_id returns 404."""
        resp = flow.get("/upload-status/nonexistent-task-id")
        assert resp.status_code == 404


# ── Durga Ground-Truth Tests (no staging server needed) ──────────

class TestDurgaEntities:
    """
    Unit tests that verify the scoping parser produces entities
    faithful to the Durga India scoping documents.
    These run without any network connection — pure local parsing.
    """

    def test_load_durga_entities_returns_dict(self):
        """load_durga_entities() returns a non-empty dict."""
        entities = load_durga_entities()
        assert isinstance(entities, dict)
        assert len(entities.get("subject_types", [])) > 0

    def test_durga_subject_types(self):
        """Durga has exactly Cohort (Group) and Participant (Individual) subject types."""
        entities = load_durga_entities()
        names = {s["name"] for s in entities["subject_types"]}
        assert "Cohort" in names, f"Expected 'Cohort' in subject types, got: {names}"
        assert "Participant" in names, f"Expected 'Participant' in subject types, got: {names}"

        cohort = next(s for s in entities["subject_types"] if s["name"] == "Cohort")
        participant = next(s for s in entities["subject_types"] if s["name"] == "Participant")
        assert cohort["type"] == "Group", f"Cohort type should be Group, got: {cohort['type']}"
        assert participant["type"] == "Person", f"Participant type should be Person, got: {participant['type']}"

    def test_durga_location_hierarchy(self):
        """Durga location hierarchy has State and City levels."""
        entities = load_durga_entities()
        names = {a["name"] for a in entities["address_levels"]}
        assert "State" in names, f"Expected 'State' in address levels, got: {names}"
        assert "City" in names, f"Expected 'City' in address levels, got: {names}"

    def test_durga_encounter_types_no_duplicates(self):
        """Durga encounter types have no duplicates — fixes the 5x repetition bug."""
        entities = load_durga_entities()
        names = [e["name"] for e in entities["encounter_types"]]
        assert len(names) == len(set(names)), f"Duplicate encounter types found: {names}"

    def test_durga_entities_pass_pydantic_validation(self):
        """Parsed Durga entities pass EntitySpec cross-ref validation."""
        entities = load_durga_entities()
        spec = EntitySpec.model_validate(entities)
        assert len(spec.subject_types) >= 2
        assert len(spec.address_levels) >= 2

    def test_durga_entities_no_mach_placeholders(self):
        """Ensure no old placeholder data (Maternal Health, ANC Visit, Individual) leaks in."""
        entities = load_durga_entities()
        all_names = (
            {s["name"] for s in entities["subject_types"]}
            | {p["name"] for p in entities["programs"]}
            | {e["name"] for e in entities["encounter_types"]}
        )
        placeholder_names = {"Maternal Health", "Child Health", "ANC Visit", "PNC Visit", "Child Growth Monitoring"}
        leaked = placeholder_names & all_names
        assert not leaked, f"Old placeholder entities found in Durga config: {leaked}"

    def test_flow_state_from_env_has_defaults(self):
        """FlowState.from_env() sets correct defaults for non-configured env."""
        from src.schemas.flow_state import FlowState
        state = FlowState.from_env()
        assert state.max_cycles == 3
        assert state.poll_interval_secs == 3.0
        assert state.poll_max_attempts == 20
        assert state.plan_status == "idle"
        assert state.upload_status == "unknown"

    def test_flow_state_mirrors_dify_conv_vars(self):
        """FlowState fields map 1:1 to Dify conversation variable names."""
        from src.schemas.flow_state import FlowState
        state = FlowState()
        dify_conv_var_names = {
            "auth_token", "avni_mcp_server_url", "entities_jsonl",
            "spec_yaml", "existing_bundle_b64", "bundle_zip_b64", "upload_task_id",
        }
        state_fields = set(FlowState.model_fields.keys())
        missing = dify_conv_var_names - state_fields
        assert not missing, f"FlowState missing Dify conv var fields: {missing}"

    def test_org_name_always_in_spec_yaml(self):
        """entities_to_spec always emits org: even when org_name is empty."""
        from src.bundle.spec_generator import entities_to_spec
        entities = load_durga_entities()

        # Without org_name
        spec_no_org = entities_to_spec(entities, org_name="")
        assert "org:" in spec_no_org, "spec_yaml must contain org: even when org_name is empty"
        assert "Unknown Organization" in spec_no_org

        # With explicit org_name
        spec_with_org = entities_to_spec(entities, org_name="Durga India")
        assert "Durga India" in spec_with_org

    def test_org_name_roundtrips_through_spec_parser(self):
        """org_name written by spec_generator is recoverable by spec_parser for patch-bundle."""
        from src.bundle.spec_generator import entities_to_spec
        from src.bundle.spec_parser import spec_to_entities
        entities = load_durga_entities()

        spec_yaml = entities_to_spec(entities, org_name="Durga India")
        parsed = spec_to_entities(spec_yaml)
        assert parsed.get("org_name") == "Durga India", (
            f"org_name not recovered from spec YAML; got: {parsed.get('org_name')!r}"
        )

    def test_entity_spec_rejects_unknown_cross_refs(self):
        """EntitySpec raises ValueError when encounter references unknown program."""
        entities = {
            "subject_types": [{"name": "Cohort", "type": "Group"}],
            "programs": [],
            "encounter_types": [
                {
                    "name": "Session",
                    "program_name": "NonExistentProgram",
                    "subject_type": "Cohort",
                    "is_program_encounter": True,
                    "is_scheduled": True,
                }
            ],
            "address_levels": [{"name": "State", "level": 1, "parent": None}],
            "groups": [],
        }
        with pytest.raises(ValueError, match="references unknown program"):
            EntitySpec.model_validate(entities)

    def test_entity_spec_rejects_duplicates(self):
        """EntitySpec raises ValueError on duplicate encounter type names."""
        entities = {
            "subject_types": [{"name": "Cohort", "type": "Group"}],
            "programs": [],
            "encounter_types": [
                {"name": "Session", "subject_type": "Cohort", "is_program_encounter": False},
                {"name": "Session", "subject_type": "Cohort", "is_program_encounter": False},
            ],
            "address_levels": [{"name": "State", "level": 1, "parent": None}],
            "groups": [],
        }
        with pytest.raises(ValueError, match="Duplicate encounter_type"):
            EntitySpec.model_validate(entities)

    def test_pev_retry_triggered_on_spec_error(self):
        """
        When run_spec_agent() raises (e.g. EntitySpec ValueError from bad entities),
        the PEV loop catches it, records the cycle as failed, and increments cycle_count.
        No network required — we mock the POST call.
        """
        from unittest.mock import MagicMock, patch
        from src.schemas.flow_state import FlowState

        state = FlowState(
            auth_token="test-token",
            avni_mcp_server_url="http://localhost:9999/",
            max_cycles=2,
        )
        state.entities_jsonl = {
            "subject_types": [{"name": "Cohort", "type": "Group"}],
            "programs": [],
            "encounter_types": [
                {
                    "name": "Session",
                    "program_name": "BadProgram",
                    "subject_type": "Cohort",
                    "is_program_encounter": True,
                    "is_scheduled": True,
                }
            ],
            "address_levels": [{"name": "State", "level": 1, "parent": None}],
            "groups": [],
            "forms": [],
        }

        from tests.emulation.app_configurator_flow import AppConfiguratorFlow

        flow = AppConfiguratorFlow(state=state)

        # Mock store-entities and validate-entities to succeed (Phase A)
        def _fake_post(path, body, auth=False):
            if "store-entities" in path:
                return {"ok": True}
            if "validate-entities" in path:
                return {"error_count": 0, "warning_count": 0, "has_errors": False,
                        "issues_summary": "No issues found.", "issues": [], "entities": body}
            if "generate-spec" in path:
                # Force EntitySpec validation failure by returning spec with bad cross-ref
                raise ValueError("EntitySpec validation failed:\n  - EncounterType 'Session' references unknown program 'BadProgram'")
            return {}

        flow.post = _fake_post  # type: ignore[method-assign]

        result = flow.run()

        # The loop should have attempted max_cycles and failed each time on spec
        assert result.total_cycles == 2, f"Expected 2 cycles, got {result.total_cycles}"
        assert result.success is False
        assert all(c.phase_failed == "spec" for c in result.cycles)
        assert state.error_diagnosis != "", "error_diagnosis should be set after failure"
