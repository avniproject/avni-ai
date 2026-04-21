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
    async def test_missing_references_auto_resolved(
        self, client: httpx.AsyncClient, conversation_id: str
    ):
        """Fall-forward: missing subject_type and program_name are auto-resolved.

        The gate may still report structural gap errors (unmapped subject types,
        encounters with no forms) — those are a separate concern handled by the
        interactive gap-fix flow. Here we assert only that the auto-resolver
        populated flags and that no residual 'has no subject_type' /
        'has no program_name' entity errors remain.
        """
        # generate_spec auto-resolves broken references and returns flags
        await client.post(
            "/store-entities",
            json={"conversation_id": conversation_id, "entities": ENTITIES_WITH_ISSUES},
        )
        spec_resp = await client.post(
            "/generate-spec",
            json={"conversation_id": conversation_id, "org_name": "TestOrg"},
        )
        spec_body = spec_resp.json()
        assert "flags" in spec_body, "generate_spec should return flags"
        flags_text = " ".join(spec_body["flags"])
        assert "Draft" in flags_text, "Draft missing subject_type should be flagged"
        assert "Orphan Encounter" in flags_text, (
            "Orphan missing program should be flagged"
        )

        # The specific auto-resolution errors should be gone. Unrelated structural
        # gap errors (no form / no forms,programs,encounters) are allowed here.
        resp = await client.post(
            "/validate-pipeline-step",
            json={"conversation_id": conversation_id, "phase": "spec"},
        )
        assert resp.status_code == 200
        body = resp.json()
        residual = [
            e
            for e in body["errors"]
            if "has no subject_type" in e or "has no program_name" in e
        ]
        assert not residual, (
            f"Auto-resolution should have cleared subject_type/program_name gaps, "
            f"got residual: {residual}"
        )

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
            e for e in body["errors"] if "subject_type" in e or "program_name" in e
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

    async def test_flags_include_available_options(
        self, client: httpx.AsyncClient, conversation_id: str
    ):
        """Flags from auto-resolution should mention what was available."""
        await client.post(
            "/store-entities",
            json={"conversation_id": conversation_id, "entities": ENTITIES_WITH_ISSUES},
        )
        resp = await client.post(
            "/generate-spec",
            json={"conversation_id": conversation_id, "org_name": "TestOrg"},
        )
        body = resp.json()
        # Flags should mention available subject types
        flags_text = " ".join(body.get("flags", []))
        assert "Beneficiary" in flags_text
        assert "Anganwadi" in flags_text
