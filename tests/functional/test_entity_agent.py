"""
Functional tests for the Entity Agent endpoints.

Exercises /store-entities, /validate-entities, /apply-entity-corrections,
and /entities-section (GET + PUT) across 5 real organisations.
"""

from __future__ import annotations

import copy

import httpx
import pytest

from .conftest import org_parametrize, seed_entities

# ---------------------------------------------------------------------------
# TestStoreEntities
# ---------------------------------------------------------------------------


@pytest.mark.asyncio(loop_scope="function")
class TestStoreEntities:
    """POST /store-entities: happy path and error cases."""

    @org_parametrize()
    async def test_store_ok(
        self,
        client: httpx.AsyncClient,
        conversation_id: str,
        org_entities: dict,
        org_name: str,
    ):
        resp = await client.post(
            "/store-entities",
            json={"conversation_id": conversation_id, "entities": org_entities},
        )
        assert resp.status_code == 200
        body = resp.json()
        assert body.get("ok") is True

    async def test_missing_conversation_id_returns_400(
        self,
        client: httpx.AsyncClient,
    ):
        resp = await client.post(
            "/store-entities",
            json={"entities": {"subject_types": []}},
        )
        assert resp.status_code == 400

    async def test_non_dict_entities_returns_400(
        self,
        client: httpx.AsyncClient,
        conversation_id: str,
    ):
        resp = await client.post(
            "/store-entities",
            json={"conversation_id": conversation_id, "entities": "not-a-dict"},
        )
        assert resp.status_code == 400


# ---------------------------------------------------------------------------
# TestValidateEntities
# ---------------------------------------------------------------------------


@pytest.mark.asyncio(loop_scope="function")
class TestValidateEntities:
    """POST /validate-entities: validate via conversation_id lookup."""

    @org_parametrize()
    async def test_validate_via_conversation_id(
        self,
        client: httpx.AsyncClient,
        conversation_id: str,
        org_entities: dict,
        org_name: str,
    ):
        await seed_entities(client, conversation_id, org_entities)
        resp = await client.post(
            "/validate-entities",
            json={"conversation_id": conversation_id},
        )
        assert resp.status_code == 200
        body = resp.json()
        assert "error_count" in body
        assert "warning_count" in body

    @org_parametrize()
    async def test_no_errors_for_real_data(
        self,
        client: httpx.AsyncClient,
        conversation_id: str,
        org_entities: dict,
        org_name: str,
    ):
        """Real scoping data validation should succeed (errors from known data-quality
        issues like missing subject_type or program_name on encounters are acceptable
        — these are presented to the user for correction by the spec agent)."""
        await seed_entities(client, conversation_id, org_entities)
        resp = await client.post(
            "/validate-entities",
            json={"conversation_id": conversation_id},
        )
        body = resp.json()
        errors = [i for i in body.get("issues", []) if i["severity"] == "error"]
        # Allow known data-quality errors from real SRS docs
        acceptable_patterns = [
            "has no subject_type",
            "has no program_name",
        ]
        unexpected = [
            e for e in errors
            if not any(p in e.get("message", "") for p in acceptable_patterns)
        ]
        assert len(unexpected) == 0, (
            f"Unexpected errors for {org_name}: {unexpected}"
        )

    @org_parametrize()
    async def test_detects_bad_refs(
        self,
        client: httpx.AsyncClient,
        conversation_id: str,
        org_entities: dict,
        org_name: str,
    ):
        """Craft entities with a bad program reference -- validation should flag it."""
        bad = copy.deepcopy(org_entities)
        bad["encounter_types"] = [
            {
                "name": "Phantom Encounter",
                "program_name": "NonExistentProgram_XYZ",
                "subject_type": "Woman",
                "is_program_encounter": True,
                "is_scheduled": True,
            }
        ]
        bad["programs"] = []  # remove all programs so the ref is dangling
        await seed_entities(client, conversation_id, bad)
        resp = await client.post(
            "/validate-entities",
            json={"conversation_id": conversation_id},
        )
        assert resp.status_code == 200
        body = resp.json()
        assert body.get("warning_count", 0) > 0 or body.get("error_count", 0) > 0

    async def test_404_without_store(
        self,
        client: httpx.AsyncClient,
        conversation_id: str,
    ):
        resp = await client.post(
            "/validate-entities",
            json={"conversation_id": conversation_id},
        )
        assert resp.status_code == 404


# ---------------------------------------------------------------------------
# TestApplyEntityCorrections
# ---------------------------------------------------------------------------


@pytest.mark.asyncio(loop_scope="function")
class TestApplyEntityCorrections:
    """POST /apply-entity-corrections: add, delete, and error cases."""

    @org_parametrize()
    async def test_add_new_encounter_type(
        self,
        client: httpx.AsyncClient,
        conversation_id: str,
        org_entities: dict,
        org_name: str,
    ):
        await seed_entities(client, conversation_id, org_entities)
        corrections = [
            {
                "entity_type": "encounter_type",
                "name": "New Functional Test Encounter",
                "program_name": "",
                "subject_type": "Person",
                "is_program_encounter": False,
                "is_scheduled": False,
            }
        ]
        resp = await client.post(
            "/apply-entity-corrections",
            json={
                "conversation_id": conversation_id,
                "corrections": corrections,
            },
        )
        assert resp.status_code == 200
        body = resp.json()
        assert body.get("ok") is True
        assert body.get("corrections_applied") == 1

    @org_parametrize()
    async def test_delete_first_encounter(
        self,
        client: httpx.AsyncClient,
        conversation_id: str,
        org_entities: dict,
        org_name: str,
    ):
        await seed_entities(client, conversation_id, org_entities)
        encounters = org_entities.get("encounter_types", [])
        if not encounters:
            pytest.skip(f"{org_name} has no encounter_types to delete")
        first_name = encounters[0]["name"]
        corrections = [
            {
                "entity_type": "encounter_type",
                "name": first_name,
                "_delete": True,
            }
        ]
        resp = await client.post(
            "/apply-entity-corrections",
            json={
                "conversation_id": conversation_id,
                "corrections": corrections,
            },
        )
        assert resp.status_code == 200
        body = resp.json()
        assert body.get("ok") is True

        # Verify the encounter was actually removed
        section_resp = await client.get(
            "/entities-section",
            params={
                "conversation_id": conversation_id,
                "section": "encounter_types",
            },
        )
        items = section_resp.json().get("items", [])
        names = [i["name"] for i in items]
        assert first_name not in names

    async def test_404_without_store(
        self,
        client: httpx.AsyncClient,
        conversation_id: str,
    ):
        resp = await client.post(
            "/apply-entity-corrections",
            json={
                "conversation_id": conversation_id,
                "corrections": [
                    {"entity_type": "program", "name": "X", "_delete": True}
                ],
            },
        )
        assert resp.status_code == 404


# ---------------------------------------------------------------------------
# TestEntitiesSectionCRUD
# ---------------------------------------------------------------------------


@pytest.mark.asyncio(loop_scope="function")
class TestEntitiesSectionCRUD:
    """GET /entities-section and PUT /entities-section."""

    @org_parametrize()
    async def test_get_subject_types_section(
        self,
        client: httpx.AsyncClient,
        conversation_id: str,
        org_entities: dict,
        org_name: str,
    ):
        await seed_entities(client, conversation_id, org_entities)
        resp = await client.get(
            "/entities-section",
            params={
                "conversation_id": conversation_id,
                "section": "subject_types",
            },
        )
        assert resp.status_code == 200
        body = resp.json()
        assert body["section"] == "subject_types"
        assert body["count"] == len(org_entities.get("subject_types", []))
        assert isinstance(body["items"], list)

    @org_parametrize()
    async def test_put_new_programs_list(
        self,
        client: httpx.AsyncClient,
        conversation_id: str,
        org_entities: dict,
        org_name: str,
    ):
        await seed_entities(client, conversation_id, org_entities)
        new_programs = [
            {
                "name": "Functional Test Program",
                "target_subject_type": "Person",
                "colour": "#123456",
            }
        ]
        resp = await client.put(
            "/entities-section",
            json={
                "conversation_id": conversation_id,
                "section": "programs",
                "items": new_programs,
            },
        )
        assert resp.status_code == 200
        body = resp.json()
        assert body["updated"] is True
        assert body["count"] == 1

        # Read-back
        get_resp = await client.get(
            "/entities-section",
            params={"conversation_id": conversation_id, "section": "programs"},
        )
        assert get_resp.json()["items"][0]["name"] == "Functional Test Program"

    async def test_invalid_section_returns_400(
        self,
        client: httpx.AsyncClient,
        conversation_id: str,
    ):
        # Need to seed first so we don't get a 404
        await seed_entities(
            client,
            conversation_id,
            {
                "subject_types": [],
                "programs": [],
                "encounter_types": [],
                "address_levels": [],
                "forms": [],
            },
        )
        resp = await client.get(
            "/entities-section",
            params={
                "conversation_id": conversation_id,
                "section": "nonexistent_section",
            },
        )
        assert resp.status_code == 400
