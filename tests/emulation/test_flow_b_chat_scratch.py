"""
Flow B — Chat-based configuration from scratch.

Emulates the guided chat flow for building an AVNI configuration
without any pre-existing SRS documents:
  init-session(sector) -> update subject_types -> update programs
  -> update encounter_types -> update address_levels -> build-entities
  -> store-entities -> validate-entities -> generate-spec -> generate-bundle
  -> generate-rule -> generate-report-cards -> inspect-config

Single test method parametrized across 5 orgs via the ``org_config`` fixture.
Uses sector defaults from the init-session response to populate sections.
"""

from __future__ import annotations

import pytest
import httpx

from .flow_helpers import StepRecorder, assert_ok_response
from .org_registry import OrgConfig


# ---------------------------------------------------------------------------
# Minimal section data per org, derived from their known configurations.
# In the real chat flow the LLM would generate these; here we use minimal
# representative data to exercise the full pipeline.
# ---------------------------------------------------------------------------

_ORG_SECTION_DATA: dict[str, dict] = {
    "astitva": {
        "subject_types": [
            {
                "name": "Beneficiary",
                "type": "Person",
                "lowest_address_level": "Village",
            },
        ],
        "programs": [
            {
                "name": "Health Program",
                "target_subject_type": "Beneficiary",
                "colour": "#4A148C",
            },
        ],
        "encounter_types": [
            {
                "name": "Health Visit",
                "program_name": "Health Program",
                "subject_type": "Beneficiary",
                "is_program_encounter": True,
                "is_scheduled": True,
            },
        ],
        "address_levels": [
            {"name": "State", "level": 1, "parent": None},
            {"name": "District", "level": 2, "parent": "State"},
            {"name": "Village", "level": 3, "parent": "District"},
        ],
    },
    "durga": {
        "subject_types": [
            {"name": "Cohort", "type": "Group", "lowest_address_level": "City"},
            {"name": "Participant", "type": "Person", "lowest_address_level": "City"},
        ],
        "programs": [
            {
                "name": "Work With Women",
                "target_subject_type": "Participant",
                "colour": "#E91E63",
            },
        ],
        "encounter_types": [
            {
                "name": "Session",
                "program_name": "Work With Women",
                "subject_type": "Participant",
                "is_program_encounter": True,
                "is_scheduled": True,
            },
        ],
        "address_levels": [
            {"name": "State", "level": 1, "parent": None},
            {"name": "City", "level": 2, "parent": "State"},
        ],
    },
    "kshamata": {
        "subject_types": [
            {"name": "Child", "type": "Person", "lowest_address_level": "Village"},
        ],
        "programs": [
            {
                "name": "Nutrition Program",
                "target_subject_type": "Child",
                "colour": "#388E3C",
            },
        ],
        "encounter_types": [
            {
                "name": "Growth Monitoring",
                "program_name": "Nutrition Program",
                "subject_type": "Child",
                "is_program_encounter": True,
                "is_scheduled": True,
            },
        ],
        "address_levels": [
            {"name": "State", "level": 1, "parent": None},
            {"name": "District", "level": 2, "parent": "State"},
            {"name": "Village", "level": 3, "parent": "District"},
        ],
    },
    "mazisaheli": {
        "subject_types": [
            {"name": "Woman", "type": "Person", "lowest_address_level": "Village"},
        ],
        "programs": [
            {
                "name": "MCH Program",
                "target_subject_type": "Woman",
                "colour": "#D32F2F",
            },
        ],
        "encounter_types": [
            {
                "name": "ANC Visit",
                "program_name": "MCH Program",
                "subject_type": "Woman",
                "is_program_encounter": True,
                "is_scheduled": True,
            },
        ],
        "address_levels": [
            {"name": "State", "level": 1, "parent": None},
            {"name": "District", "level": 2, "parent": "State"},
            {"name": "Village", "level": 3, "parent": "District"},
        ],
    },
    "yenepoya": {
        "subject_types": [
            {"name": "Patient", "type": "Person", "lowest_address_level": "Ward"},
        ],
        "programs": [],
        "encounter_types": [
            {
                "name": "Screening",
                "subject_type": "Patient",
                "is_program_encounter": False,
                "is_scheduled": False,
            },
        ],
        "address_levels": [
            {"name": "District", "level": 1, "parent": None},
            {"name": "Ward", "level": 2, "parent": "District"},
        ],
    },
}


@pytest.mark.asyncio(loop_scope="function")
class TestFlowBChatScratch:
    """Chat-based from-scratch pipeline across all registered organisations."""

    async def test_chat_scratch_e2e(
        self,
        client: httpx.AsyncClient,
        conversation_id: str,
        org_config: OrgConfig,
        recorder: StepRecorder,
    ):
        org_data = _ORG_SECTION_DATA.get(org_config.org_id)
        if org_data is None:
            pytest.skip(f"No chat section data configured for {org_config.org_id}")

        # ------------------------------------------------------------------
        # Step 1: init-session
        # ------------------------------------------------------------------
        resp = await client.post(
            "/chat-srs/init-session",
            json={
                "conversation_id": conversation_id,
                "sector": org_config.sector,
                "org_name": org_config.org_name,
                "is_new_org": True,
            },
        )
        step = assert_ok_response(resp, step_name="init-session")
        recorder.record(step)
        assert step.ok, f"init-session failed: {step.detail}"
        init_body = resp.json()
        assert init_body.get("ok") is True
        assert "sections" in init_body

        # ------------------------------------------------------------------
        # Step 2: update subject_types
        # ------------------------------------------------------------------
        resp = await client.post(
            "/chat-srs/update-section",
            json={
                "conversation_id": conversation_id,
                "section": "subject_types",
                "data": org_data["subject_types"],
            },
        )
        step = assert_ok_response(resp, step_name="update-subject_types")
        recorder.record(step)
        assert step.ok, f"update subject_types failed: {step.detail}"

        # ------------------------------------------------------------------
        # Step 3: update programs
        # ------------------------------------------------------------------
        resp = await client.post(
            "/chat-srs/update-section",
            json={
                "conversation_id": conversation_id,
                "section": "programs",
                "data": org_data["programs"],
            },
        )
        step = assert_ok_response(resp, step_name="update-programs")
        recorder.record(step)
        assert step.ok, f"update programs failed: {step.detail}"

        # ------------------------------------------------------------------
        # Step 4: update encounter_types
        # ------------------------------------------------------------------
        resp = await client.post(
            "/chat-srs/update-section",
            json={
                "conversation_id": conversation_id,
                "section": "encounter_types",
                "data": org_data["encounter_types"],
            },
        )
        step = assert_ok_response(resp, step_name="update-encounter_types")
        recorder.record(step)
        assert step.ok, f"update encounter_types failed: {step.detail}"

        # ------------------------------------------------------------------
        # Step 5: update address_levels
        # ------------------------------------------------------------------
        resp = await client.post(
            "/chat-srs/update-section",
            json={
                "conversation_id": conversation_id,
                "section": "address_levels",
                "data": org_data["address_levels"],
            },
        )
        step = assert_ok_response(resp, step_name="update-address_levels")
        recorder.record(step)
        assert step.ok, f"update address_levels failed: {step.detail}"

        # ------------------------------------------------------------------
        # Step 6: build-entities
        # ------------------------------------------------------------------
        resp = await client.post(
            "/chat-srs/build-entities",
            json={"conversation_id": conversation_id},
        )
        step = assert_ok_response(resp, step_name="build-entities")
        recorder.record(step)
        assert step.ok, f"build-entities failed: {step.detail}"
        build_body = resp.json()
        assert build_body.get("ok") is True
        entities = build_body.get("entities", {})
        assert len(entities.get("subject_types", [])) >= 1

        # ------------------------------------------------------------------
        # Step 7: store-entities
        # ------------------------------------------------------------------
        resp = await client.post(
            "/store-entities",
            json={"conversation_id": conversation_id, "entities": entities},
        )
        step = assert_ok_response(resp, step_name="store-entities")
        recorder.record(step)
        assert step.ok, f"store-entities failed: {step.detail}"

        # ------------------------------------------------------------------
        # Step 8: validate-entities
        # ------------------------------------------------------------------
        resp = await client.post(
            "/validate-entities",
            json={"conversation_id": conversation_id},
        )
        step = assert_ok_response(resp, step_name="validate-entities")
        recorder.record(step)
        assert step.ok, f"validate-entities failed: {step.detail}"

        # ------------------------------------------------------------------
        # Step 9: generate-spec
        # ------------------------------------------------------------------
        resp = await client.post(
            "/generate-spec",
            json={
                "conversation_id": conversation_id,
                "org_name": org_config.org_name,
            },
        )
        step = assert_ok_response(resp, step_name="generate-spec")
        recorder.record(step)
        assert step.ok, f"generate-spec failed: {step.detail}"

        # ------------------------------------------------------------------
        # Step 10: generate-bundle
        # ------------------------------------------------------------------
        resp = await client.post(
            "/generate-bundle",
            json={
                "conversation_id": conversation_id,
                "org_name": org_config.org_name,
            },
        )
        step = assert_ok_response(resp, step_name="generate-bundle")
        recorder.record(step)
        assert step.ok, f"generate-bundle failed: {step.detail}"
        assert resp.json().get("success") is True

        # ------------------------------------------------------------------
        # Step 11: generate-rule
        # ------------------------------------------------------------------
        enc_name = org_data["encounter_types"][0].get("name", "Follow-up")
        resp = await client.post(
            "/generate-rule",
            json={
                "rule_type": "visitSchedule",
                "params": {
                    "schedule_days": 30,
                    "max_days": 45,
                    "encounter_name": enc_name,
                },
            },
        )
        step = assert_ok_response(resp, step_name="generate-rule")
        recorder.record(step)
        assert step.ok, f"generate-rule failed: {step.detail}"
        assert resp.json().get("ok") is True

        # ------------------------------------------------------------------
        # Step 12: generate-report-cards
        # ------------------------------------------------------------------
        resp = await client.post(
            "/generate-report-cards",
            json={
                "org_name": org_config.org_name,
                "card_types": ["scheduledVisits", "overdueVisits", "total"],
            },
        )
        step = assert_ok_response(resp, step_name="generate-report-cards")
        recorder.record(step)
        assert step.ok, f"generate-report-cards failed: {step.detail}"
        assert resp.json().get("card_count", 0) >= 3

        # ------------------------------------------------------------------
        # Step 13: inspect-config
        # ------------------------------------------------------------------
        resp = await client.post(
            "/inspect-config",
            json={"entities": entities},
        )
        step = assert_ok_response(resp, step_name="inspect-config")
        recorder.record(step)
        assert step.ok, f"inspect-config failed: {step.detail}"
        assert resp.json().get("ok") is True
        assert resp.json().get("completeness_score", 0) > 0

        # ------------------------------------------------------------------
        # Final summary
        # ------------------------------------------------------------------
        assert recorder.all_ok(), (
            f"Flow B failed for {org_config.org_id}: {recorder.summary()}"
        )
