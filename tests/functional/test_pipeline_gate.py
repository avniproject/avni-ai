"""
Tests for the pipeline validation gate (read-only).

POST /validate-pipeline-step — validates state, returns errors/warnings
"""

from __future__ import annotations

import httpx
import pytest


ENTITIES_WITH_ISSUES = {
    "subject_types": [
        {"name": "Beneficiary", "type": "Person"},
        {"name": "Anganwadi", "type": "Person"},
    ],
    "programs": [
        {"name": "Nourish", "target_subject_type": "Beneficiary"},
    ],
    "encounter_types": [
        {
            "name": "ANC Visit",
            "subject_type": "Beneficiary",
            "program_name": "Nourish",
            "is_program_encounter": True,
            "is_scheduled": True,
        },
        {
            "name": "Draft",
            "subject_type": "",
            "program_name": "",
            "is_program_encounter": False,
            "is_scheduled": False,
        },
        {
            "name": "Orphan Encounter",
            "subject_type": "",
            "program_name": "",
            "is_program_encounter": True,
            "is_scheduled": True,
        },
    ],
    "address_levels": [{"name": "Village", "level": 1}],
    "groups": [],
    "forms": [],
}

CLEAN_ENTITIES = {
    "subject_types": [{"name": "Person", "type": "Person"}],
    "programs": [{"name": "Health", "target_subject_type": "Person"}],
    "encounter_types": [
        {
            "name": "Visit",
            "subject_type": "Person",
            "program_name": "Health",
            "is_program_encounter": True,
            "is_scheduled": True,
        },
    ],
    "address_levels": [{"name": "Village", "level": 1}],
    "groups": [{"name": "Everyone", "has_all_privileges": False}],
    "forms": [],
}


async def _setup(client: httpx.AsyncClient, cid: str, entities: dict) -> None:
    await client.post(
        "/store-entities", json={"conversation_id": cid, "entities": entities}
    )
    await client.post(
        "/generate-spec", json={"conversation_id": cid, "org_name": "TestOrg"}
    )


@pytest.mark.asyncio(loop_scope="function")
class TestValidatePipelineStep:

    async def test_detects_missing_subject_type(
        self, client: httpx.AsyncClient, conversation_id: str
    ):
        await _setup(client, conversation_id, ENTITIES_WITH_ISSUES)
        resp = await client.post(
            "/validate-pipeline-step",
            json={"conversation_id": conversation_id, "phase": "spec"},
        )
        assert resp.status_code == 200
        body = resp.json()
        assert body["ok"] is False
        assert body["next_action"] == "fix_required"
        errors_text = " ".join(body["errors"])
        assert "Draft" in errors_text
        assert "subject_type" in errors_text

    async def test_detects_missing_program(
        self, client: httpx.AsyncClient, conversation_id: str
    ):
        await _setup(client, conversation_id, ENTITIES_WITH_ISSUES)
        resp = await client.post(
            "/validate-pipeline-step",
            json={"conversation_id": conversation_id, "phase": "spec"},
        )
        body = resp.json()
        errors_text = " ".join(body["errors"])
        assert "Orphan Encounter" in errors_text
        assert "program_name" in errors_text

    async def test_clean_entities_pass(
        self, client: httpx.AsyncClient, conversation_id: str
    ):
        await _setup(client, conversation_id, CLEAN_ENTITIES)
        resp = await client.post(
            "/validate-pipeline-step",
            json={"conversation_id": conversation_id, "phase": "spec"},
        )
        body = resp.json()
        # Filter out schema warnings (unknown fields etc) — just check entity errors
        entity_errors = [
            e for e in body["errors"]
            if "subject_type" in e or "program_name" in e
        ]
        assert len(entity_errors) == 0

    async def test_unknown_phase_passes(
        self, client: httpx.AsyncClient, conversation_id: str
    ):
        resp = await client.post(
            "/validate-pipeline-step",
            json={"conversation_id": conversation_id, "phase": "unknown_phase"},
        )
        body = resp.json()
        assert body["ok"] is True
        assert body["next_action"] == "continue"

    async def test_no_state_modification(
        self, client: httpx.AsyncClient, conversation_id: str
    ):
        """Gate should not modify entities or spec."""
        await _setup(client, conversation_id, ENTITIES_WITH_ISSUES)

        # Get entities before gate
        resp1 = await client.get(
            "/entities-section",
            params={"conversation_id": conversation_id, "section": "encounter_types"},
        )
        before = resp1.json()["count"]

        # Run gate
        await client.post(
            "/validate-pipeline-step",
            json={"conversation_id": conversation_id, "phase": "spec"},
        )

        # Get entities after gate — should be unchanged
        resp2 = await client.get(
            "/entities-section",
            params={"conversation_id": conversation_id, "section": "encounter_types"},
        )
        after = resp2.json()["count"]
        assert before == after

    async def test_errors_include_available_options(
        self, client: httpx.AsyncClient, conversation_id: str
    ):
        """Errors should tell the agent what options are available."""
        await _setup(client, conversation_id, ENTITIES_WITH_ISSUES)
        resp = await client.post(
            "/validate-pipeline-step",
            json={"conversation_id": conversation_id, "phase": "spec"},
        )
        body = resp.json()
        # Errors should mention available subject types
        errors_text = " ".join(body["errors"])
        assert "Beneficiary" in errors_text
        assert "Anganwadi" in errors_text
