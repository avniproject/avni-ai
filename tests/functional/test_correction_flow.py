"""
Tests for the spec correction + surgical bundle fix flow.

Verifies the second-turn correction path:
  store entities → generate spec → generate bundle
  → correct spec via update_spec_section
  → surgically fix bundle files via put_bundle_file
  → bundle reflects corrections without full regeneration

Also verifies the noop guard on generate_bundle.
"""

from __future__ import annotations

import json

import httpx
import pytest


SAMPLE_ENTITIES = {
    "subject_types": [
        {"name": "Beneficiary", "type": "Person"},
        {"name": "Activity", "type": "Individual"},
    ],
    "programs": [],
    "encounter_types": [
        {
            "name": "Home Visit",
            "subject_type": "Beneficiary",
            "is_program_encounter": False,
            "is_scheduled": True,
        },
        {
            "name": "Assessment",
            "subject_type": "Activity",
            "is_program_encounter": False,
            "is_scheduled": False,
        },
        {
            "name": "Draft",
            "subject_type": "",
            "is_program_encounter": False,
            "is_scheduled": False,
        },
    ],
    "address_levels": [
        {"name": "District", "level": 2},
        {"name": "Village", "level": 1, "parent": "District"},
    ],
    "groups": [{"name": "Everyone", "has_all_privileges": False}],
    "forms": [],
}


async def _setup_full_pipeline(client: httpx.AsyncClient, conversation_id: str) -> dict:
    """Store entities, generate spec and bundle. Returns initial bundle summary."""
    await client.post(
        "/store-entities",
        json={"conversation_id": conversation_id, "entities": SAMPLE_ENTITIES},
    )
    await client.post(
        "/generate-spec",
        json={"conversation_id": conversation_id, "org_name": "TestOrg"},
    )
    resp = await client.post(
        "/generate-bundle",
        json={"conversation_id": conversation_id, "org_name": "TestOrg"},
    )
    assert resp.status_code == 200
    return resp.json().get("summary", {})


@pytest.mark.asyncio(loop_scope="function")
class TestGenerateBundleNoopGuard:
    """generate_bundle returns existing bundle without regenerating."""

    async def test_noop_when_bundle_exists(
        self, client: httpx.AsyncClient, conversation_id: str
    ):
        await _setup_full_pipeline(client, conversation_id)

        # Second call without force: noop
        resp = await client.post(
            "/generate-bundle",
            json={"conversation_id": conversation_id, "org_name": "TestOrg"},
        )
        assert resp.status_code == 200
        assert resp.json()["already_existed"] is True

    async def test_force_overrides_noop(
        self, client: httpx.AsyncClient, conversation_id: str
    ):
        await _setup_full_pipeline(client, conversation_id)

        resp = await client.post(
            "/generate-bundle",
            json={
                "conversation_id": conversation_id,
                "org_name": "TestOrg",
                "force": True,
            },
        )
        assert resp.status_code == 200
        assert resp.json().get("already_existed") is None
        assert resp.json().get("stored") is True


@pytest.mark.asyncio(loop_scope="function")
class TestSurgicalSpecCorrection:
    """Correct spec + surgically fix bundle files — no full regeneration."""

    async def test_remove_encounter_type_surgically(
        self, client: httpx.AsyncClient, conversation_id: str
    ):
        summary = await _setup_full_pipeline(client, conversation_id)
        assert summary["encounterTypes"] == 3

        # 1. Read spec encounterTypes
        resp = await client.get(
            "/spec-section",
            params={"conversation_id": conversation_id, "section": "encounterTypes"},
        )
        enc_types = resp.json()["value"]
        assert any(e["name"] == "Draft" for e in enc_types)

        # 2. Remove Draft from spec
        corrected = [e for e in enc_types if e["name"] != "Draft"]
        resp = await client.put(
            "/spec-section",
            json={
                "conversation_id": conversation_id,
                "section": "encounterTypes",
                "value": corrected,
            },
        )
        assert resp.json()["updated"] is True

        # 3. Surgically fix bundle: read encounterTypes.json, remove Draft
        resp = await client.get(
            "/bundle-file",
            params={
                "conversation_id": conversation_id,
                "filename": "encounterTypes.json",
            },
        )
        bundle_enc = resp.json()["content"]
        fixed_enc = [e for e in bundle_enc if e["name"] != "Draft"]
        resp = await client.put(
            "/bundle-file",
            json={
                "conversation_id": conversation_id,
                "filename": "encounterTypes.json",
                "content": json.dumps(fixed_enc),
            },
        )
        assert resp.json()["updated"] is True

        # 4. Also fix formMappings — remove any mapping referencing Draft
        resp = await client.get(
            "/bundle-file",
            params={
                "conversation_id": conversation_id,
                "filename": "formMappings.json",
            },
        )
        mappings = resp.json()["content"]
        fixed_mappings = [m for m in mappings if "Draft" not in m.get("formName", "")]
        resp = await client.put(
            "/bundle-file",
            json={
                "conversation_id": conversation_id,
                "filename": "formMappings.json",
                "content": json.dumps(fixed_mappings),
            },
        )
        assert resp.json()["updated"] is True

        # 5. Verify: noop guard still protects the corrected bundle
        resp = await client.post(
            "/generate-bundle",
            json={"conversation_id": conversation_id, "org_name": "TestOrg"},
        )
        assert resp.json()["already_existed"] is True

        # 6. Validate the corrected bundle
        resp = await client.post(
            "/validate-bundle",
            json={"conversation_id": conversation_id},
        )
        assert resp.status_code == 200

    async def test_fix_missing_subject_type_surgically(
        self, client: httpx.AsyncClient, conversation_id: str
    ):
        await _setup_full_pipeline(client, conversation_id)

        # 1. Fix spec: assign Beneficiary to Draft
        resp = await client.get(
            "/spec-section",
            params={"conversation_id": conversation_id, "section": "encounterTypes"},
        )
        enc_types = resp.json()["value"]
        for et in enc_types:
            if et["name"] == "Draft" and not et.get("subjectType"):
                et["subjectType"] = "Beneficiary"

        resp = await client.put(
            "/spec-section",
            json={
                "conversation_id": conversation_id,
                "section": "encounterTypes",
                "value": enc_types,
            },
        )
        assert resp.json()["updated"] is True

        # 2. Fix bundle: update formMappings to add subjectTypeUUID for Draft
        resp = await client.get(
            "/bundle-file",
            params={
                "conversation_id": conversation_id,
                "filename": "subjectTypes.json",
            },
        )
        st_list = resp.json()["content"]
        beneficiary_uuid = next(
            (s["uuid"] for s in st_list if s["name"] == "Beneficiary"), None
        )
        assert beneficiary_uuid is not None

        resp = await client.get(
            "/bundle-file",
            params={
                "conversation_id": conversation_id,
                "filename": "formMappings.json",
            },
        )
        mappings = resp.json()["content"]
        for m in mappings:
            if "Draft" in m.get("formName", "") and not m.get("subjectTypeUUID"):
                m["subjectTypeUUID"] = beneficiary_uuid

        resp = await client.put(
            "/bundle-file",
            json={
                "conversation_id": conversation_id,
                "filename": "formMappings.json",
                "content": json.dumps(mappings),
            },
        )
        assert resp.json()["updated"] is True

        # 3. Validate
        resp = await client.post(
            "/validate-bundle",
            json={"conversation_id": conversation_id},
        )
        assert resp.status_code == 200

    async def test_surgical_fix_survives_noop_guard(
        self, client: httpx.AsyncClient, conversation_id: str
    ):
        """Surgical put_bundle_file changes survive subsequent generate_bundle noop."""
        await _setup_full_pipeline(client, conversation_id)

        # Surgical fix: remove Draft from encounterTypes.json
        resp = await client.get(
            "/bundle-file",
            params={
                "conversation_id": conversation_id,
                "filename": "encounterTypes.json",
            },
        )
        original = resp.json()["content"]
        fixed = [e for e in original if e["name"] != "Draft"]
        await client.put(
            "/bundle-file",
            json={
                "conversation_id": conversation_id,
                "filename": "encounterTypes.json",
                "content": json.dumps(fixed),
            },
        )

        # generate_bundle noop should NOT overwrite the fix
        resp = await client.post(
            "/generate-bundle",
            json={"conversation_id": conversation_id, "org_name": "TestOrg"},
        )
        assert resp.json()["already_existed"] is True

        # Verify fix is still there
        resp = await client.get(
            "/bundle-file",
            params={
                "conversation_id": conversation_id,
                "filename": "encounterTypes.json",
            },
        )
        current = resp.json()["content"]
        names = [e["name"] for e in current]
        assert "Draft" not in names
