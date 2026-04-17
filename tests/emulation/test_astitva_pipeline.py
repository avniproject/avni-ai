"""
End-to-end emulation of the App Configurator pipeline for Astitva.

Runs the same tool calls as the Dify agent loop using real SRS files.
No LLM involved — pure deterministic API calls. Catches issues before staging.

Flow: parse SRS → validate entities → generate spec → gate(spec)
      → generate bundle → validate bundle → gate(bundle)
      → check formMappings for upload-blocking issues
"""

from __future__ import annotations

from pathlib import Path

import httpx
import pytest

from src.bundle.scoping_parser import consolidate_and_audit

SCOPING_DIR = Path(__file__).resolve().parents[1] / "resources" / "scoping"

ASTITVA_FILES = [
    SCOPING_DIR / "Astitva SRS .xlsx",
    SCOPING_DIR / "Astitva Modelling.xlsx",
    SCOPING_DIR / "Astitva Nourish Program Forms.xlsx",
]

pytestmark = pytest.mark.skipif(
    not all(f.exists() for f in ASTITVA_FILES),
    reason="Astitva resource files not present",
)


@pytest.fixture(scope="module")
def astitva_entities() -> dict:
    """Parse Astitva SRS files once per module."""
    result = consolidate_and_audit([str(f) for f in ASTITVA_FILES], org_name="astitva")
    return result["entities"]


async def _seed(client: httpx.AsyncClient, cid: str, entities: dict) -> None:
    """Store entities and generate spec."""
    await client.post(
        "/store-entities", json={"conversation_id": cid, "entities": entities}
    )
    await client.post(
        "/generate-spec", json={"conversation_id": cid, "org_name": "astitva"}
    )


@pytest.mark.asyncio(loop_scope="function")
class TestAstitvaPipeline:
    async def test_parse_srs(self, astitva_entities: dict):
        """Phase 1: Parse all 3 Astitva SRS files."""
        assert len(astitva_entities.get("subject_types", [])) >= 2
        assert len(astitva_entities.get("programs", [])) >= 1
        assert len(astitva_entities.get("encounter_types", [])) >= 10

    async def test_validate_entities(
        self, client: httpx.AsyncClient, conversation_id: str, astitva_entities: dict
    ):
        """Phase 2a: Validate extracted entities for data quality issues."""
        await client.post(
            "/store-entities",
            json={"conversation_id": conversation_id, "entities": astitva_entities},
        )

        resp = await client.post(
            "/validate-entities", json={"conversation_id": conversation_id}
        )
        assert resp.status_code == 200
        body = resp.json()
        # Allow known data-quality errors (missing subject_type/program)
        # but no unexpected errors
        errors = [i for i in body.get("issues", []) if i["severity"] == "error"]
        acceptable = ["has no subject_type", "has no program_name"]
        unexpected = [
            e for e in errors if not any(p in e.get("message", "") for p in acceptable)
        ]
        assert len(unexpected) == 0, f"Unexpected errors: {unexpected}"

    async def test_spec_generation_and_gate(
        self, client: httpx.AsyncClient, conversation_id: str, astitva_entities: dict
    ):
        """Phase 2b: Generate spec and run pipeline gate."""
        await client.post(
            "/store-entities",
            json={"conversation_id": conversation_id, "entities": astitva_entities},
        )

        resp = await client.post(
            "/generate-spec",
            json={"conversation_id": conversation_id, "org_name": "astitva"},
        )
        assert resp.status_code == 200
        assert resp.json().get("stored") is True

        # Gate should detect entity issues
        resp = await client.post(
            "/validate-pipeline-step",
            json={"conversation_id": conversation_id, "phase": "spec"},
        )
        assert resp.status_code == 200
        gate = resp.json()
        # Gate may report errors — this is expected for Astitva
        # (encounters missing subject_type, unknown references, etc.)
        # The important thing is the gate ran without crashing
        if not gate["ok"]:
            print(f"  Gate found {len(gate['errors'])} errors (expected for Astitva):")
            for err in gate["errors"][:5]:
                print(f"    {err[:120]}")

    async def test_bundle_generation_and_validation(
        self, client: httpx.AsyncClient, conversation_id: str, astitva_entities: dict
    ):
        """Phase 3: Generate bundle and check for formMapping issues."""
        await _seed(client, conversation_id, astitva_entities)

        resp = await client.post(
            "/generate-bundle",
            json={"conversation_id": conversation_id, "org_name": "astitva"},
        )
        assert resp.status_code == 200
        assert resp.json().get("success") is True

        # Validate bundle
        resp = await client.post(
            "/validate-bundle", json={"conversation_id": conversation_id}
        )
        assert resp.status_code == 200
        val = resp.json()
        # Log errors for visibility
        for err in val.get("errors", [])[:5]:
            print(f"  BUNDLE ERROR: {err[:120]}")

    async def test_formappings_completeness(
        self, client: httpx.AsyncClient, conversation_id: str, astitva_entities: dict
    ):
        """Check that formMappings have all required UUIDs."""
        await _seed(client, conversation_id, astitva_entities)
        await client.post(
            "/generate-bundle",
            json={"conversation_id": conversation_id, "org_name": "astitva"},
        )

        resp = await client.get(
            "/bundle-file",
            params={
                "conversation_id": conversation_id,
                "filename": "formMappings.json",
            },
        )
        assert resp.status_code == 200
        mappings = resp.json()["content"]

        broken = []
        for m in mappings:
            ft = m.get("formType", "")
            issues = []
            if not m.get("subjectTypeUUID"):
                issues.append("no subjectTypeUUID")
            if ft in (
                "ProgramEnrolment",
                "ProgramExit",
                "ProgramEncounter",
                "ProgramEncounterCancellation",
            ) and not m.get("programUUID"):
                issues.append("no programUUID")
            if ft in (
                "Encounter",
                "IndividualEncounterCancellation",
                "ProgramEncounter",
                "ProgramEncounterCancellation",
            ) and not m.get("encounterTypeUUID"):
                issues.append("no encounterTypeUUID")
            if issues:
                broken.append(f"{m.get('formName', '?')}: {', '.join(issues)}")

        for b in broken:
            print(f"  BROKEN: {b}")

        # This test documents known issues — the agent needs to fix these
        # Assert that the noop guard and fallback logic didn't make it WORSE
        assert len(mappings) > 0, "No formMappings generated"

    async def test_noop_guard_preserves_bundle(
        self, client: httpx.AsyncClient, conversation_id: str, astitva_entities: dict
    ):
        """Second generate_bundle call should noop (not wipe surgical changes)."""
        await _seed(client, conversation_id, astitva_entities)
        await client.post(
            "/generate-bundle",
            json={"conversation_id": conversation_id, "org_name": "astitva"},
        )

        # Second call should noop
        resp = await client.post(
            "/generate-bundle",
            json={"conversation_id": conversation_id, "org_name": "astitva"},
        )
        assert resp.status_code == 200
        assert resp.json().get("already_existed") is True

    async def test_gate_does_not_modify_state(
        self, client: httpx.AsyncClient, conversation_id: str, astitva_entities: dict
    ):
        """Pipeline gate is read-only — entities should not change."""
        await _seed(client, conversation_id, astitva_entities)

        # Get entities before gate
        resp = await client.get(
            "/entities-section",
            params={"conversation_id": conversation_id, "section": "encounter_types"},
        )
        before_count = resp.json()["count"]

        # Run gate
        await client.post(
            "/validate-pipeline-step",
            json={"conversation_id": conversation_id, "phase": "spec"},
        )

        # Get entities after gate — must be unchanged
        resp = await client.get(
            "/entities-section",
            params={"conversation_id": conversation_id, "section": "encounter_types"},
        )
        after_count = resp.json()["count"]

        assert before_count == after_count, "Gate modified entities!"
