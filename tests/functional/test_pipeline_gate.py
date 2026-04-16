"""
Tests for the pipeline validation gate.

POST /validate-pipeline-step — deterministic validation after each agent
POST /resolve-pipeline-questions — apply user answers deterministically
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
            json={"conversation_id": conversation_id, "phase": "spec_generation"},
        )
        assert resp.status_code == 200
        body = resp.json()
        assert body["ok"] is False
        assert body["next_action"] == "present_questions"

        # Should have questions about Draft and Orphan Encounter
        entity_names = {q["entity"] for q in body["questions"]}
        assert "Draft" in entity_names
        assert "Orphan Encounter" in entity_names

    async def test_questions_have_options(
        self, client: httpx.AsyncClient, conversation_id: str
    ):
        await _setup(client, conversation_id, ENTITIES_WITH_ISSUES)

        resp = await client.post(
            "/validate-pipeline-step",
            json={"conversation_id": conversation_id, "phase": "spec_generation"},
        )
        body = resp.json()
        for q in body["questions"]:
            assert len(q["options"]) >= 2
            assert q.get("default")

    async def test_clean_entities_pass(
        self, client: httpx.AsyncClient, conversation_id: str
    ):
        await _setup(client, conversation_id, CLEAN_ENTITIES)

        resp = await client.post(
            "/validate-pipeline-step",
            json={"conversation_id": conversation_id, "phase": "spec_generation"},
        )
        body = resp.json()
        # No entity-level questions (subject type and program are set)
        entity_questions = [
            q
            for q in body["questions"]
            if q.get("field") in ("subject_type", "program_name")
        ]
        assert len(entity_questions) == 0

    async def test_auto_fixes_applied(
        self, client: httpx.AsyncClient, conversation_id: str
    ):
        await _setup(client, conversation_id, ENTITIES_WITH_ISSUES)

        resp = await client.post(
            "/validate-pipeline-step",
            json={"conversation_id": conversation_id, "phase": "spec_generation"},
        )
        body = resp.json()
        assert len(body["auto_fixed"]) > 0
        auto_text = " ".join(body["auto_fixed"])
        assert "lastNameOptional" in auto_text

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


@pytest.mark.asyncio(loop_scope="function")
class TestResolvePipelineQuestions:
    async def test_remove_encounter(
        self, client: httpx.AsyncClient, conversation_id: str
    ):
        await _setup(client, conversation_id, ENTITIES_WITH_ISSUES)

        # Get questions
        resp = await client.post(
            "/validate-pipeline-step",
            json={"conversation_id": conversation_id, "phase": "spec_generation"},
        )
        questions = resp.json()["questions"]
        draft_q = next(
            (
                q
                for q in questions
                if q["entity"] == "Draft" and q["field"] == "subject_type"
            ),
            None,
        )
        assert draft_q is not None

        # Resolve: remove Draft
        resp = await client.post(
            "/resolve-pipeline-questions",
            json={
                "conversation_id": conversation_id,
                "answers": [
                    {
                        "id": draft_q["id"],
                        "answer": "Remove this encounter",
                        "entity": "Draft",
                    },
                ],
            },
        )
        body = resp.json()
        assert body["ok"] is True
        assert any("Removed" in a and "Draft" in a for a in body["applied"])

    async def test_assign_subject_type(
        self, client: httpx.AsyncClient, conversation_id: str
    ):
        await _setup(client, conversation_id, ENTITIES_WITH_ISSUES)

        resp = await client.post(
            "/validate-pipeline-step",
            json={"conversation_id": conversation_id, "phase": "spec_generation"},
        )
        questions = resp.json()["questions"]
        orphan_q = next(
            (
                q
                for q in questions
                if q["entity"] == "Orphan Encounter" and q["field"] == "subject_type"
            ),
            None,
        )
        assert orphan_q is not None

        resp = await client.post(
            "/resolve-pipeline-questions",
            json={
                "conversation_id": conversation_id,
                "answers": [
                    {
                        "id": orphan_q["id"],
                        "answer": "Beneficiary",
                        "entity": "Orphan Encounter",
                    },
                ],
            },
        )
        body = resp.json()
        assert any("Beneficiary" in a for a in body["applied"])

    async def test_resolve_then_revalidate_fewer_questions(
        self, client: httpx.AsyncClient, conversation_id: str
    ):
        await _setup(client, conversation_id, ENTITIES_WITH_ISSUES)

        # First validation
        resp = await client.post(
            "/validate-pipeline-step",
            json={"conversation_id": conversation_id, "phase": "spec_generation"},
        )
        q1_count = len(resp.json()["questions"])

        # Resolve all entity questions
        questions = resp.json()["questions"]
        answers = []
        for q in questions:
            if q.get("field") == "subject_type" and q.get("entity") == "Draft":
                answers.append(
                    {
                        "id": q["id"],
                        "answer": "Remove this encounter",
                        "entity": "Draft",
                    }
                )
            elif q.get("field") == "subject_type":
                answers.append(
                    {"id": q["id"], "answer": "Beneficiary", "entity": q["entity"]}
                )
            elif q.get("field") == "program_name":
                answers.append(
                    {"id": q["id"], "answer": "Nourish", "entity": q["entity"]}
                )

        if answers:
            await client.post(
                "/resolve-pipeline-questions",
                json={"conversation_id": conversation_id, "answers": answers},
            )

        # Re-validate — should have fewer questions
        resp = await client.post(
            "/validate-pipeline-step",
            json={"conversation_id": conversation_id, "phase": "spec_generation"},
        )
        q2_count = len(resp.json()["questions"])
        assert q2_count < q1_count
