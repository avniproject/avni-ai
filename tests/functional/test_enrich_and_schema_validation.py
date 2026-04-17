"""
Tests for enrich-spec (smart defaults + ambiguity detection) and
schema-driven spec validation (catches LLM hallucinations / unknown fields).
"""

from __future__ import annotations


import httpx
import pytest


SAMPLE_ENTITIES = {
    "subject_types": [
        {"name": "Beneficiary", "type": "Person"},
        {"name": "Household", "type": "Group"},
    ],
    "programs": [
        {"name": "MCH", "target_subject_type": "Beneficiary"},
    ],
    "encounter_types": [
        {
            "name": "ANC Visit",
            "subject_type": "Beneficiary",
            "program_name": "MCH",
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
    ],
    "address_levels": [{"name": "Village", "level": 1}],
    "groups": [],
    "forms": [],
}


async def _setup_spec(client: httpx.AsyncClient, cid: str) -> None:
    """Store entities and generate spec."""
    await client.post(
        "/store-entities",
        json={"conversation_id": cid, "entities": SAMPLE_ENTITIES},
    )
    resp = await client.post(
        "/generate-spec",
        json={"conversation_id": cid, "org_name": "TestOrg"},
    )
    assert resp.status_code == 200


# ---------------------------------------------------------------------------
# Enrich spec tests
# ---------------------------------------------------------------------------


@pytest.mark.asyncio(loop_scope="function")
class TestEnrichSpec:
    """POST /enrich-spec applies defaults and detects ambiguities."""

    async def test_applies_defaults(
        self, client: httpx.AsyncClient, conversation_id: str
    ):
        await _setup_spec(client, conversation_id)

        resp = await client.post(
            "/enrich-spec",
            json={"conversation_id": conversation_id, "sector": "MCH"},
        )
        assert resp.status_code == 200
        body = resp.json()
        assert body["enriched"] is True
        assert len(body["defaults_applied"]) > 0
        # Should set lastNameOptional, group flag for Household, default colour
        defaults_text = " ".join(body["defaults_applied"])
        assert "lastNameOptional" in defaults_text
        assert "group=true" in defaults_text

    async def test_missing_subject_type_auto_resolved_with_flag(
        self, client: httpx.AsyncClient, conversation_id: str
    ):
        """Draft has no subject_type — fall-forward resolves it and returns a flag."""
        await client.post(
            "/store-entities",
            json={"conversation_id": conversation_id, "entities": SAMPLE_ENTITIES},
        )
        resp = await client.post(
            "/generate-spec",
            json={"conversation_id": conversation_id, "org_name": "TestOrg"},
        )
        assert resp.status_code == 200
        body = resp.json()
        # Fall-forward should auto-resolve Draft's missing subject_type and flag it
        assert "flags" in body, (
            "generate_spec should return flags for auto-resolved issues"
        )
        draft_flags = [f for f in body["flags"] if "Draft" in f]
        assert len(draft_flags) > 0, f"Expected flag for Draft, got: {body['flags']}"
        assert "Beneficiary" in draft_flags[0], (
            "Draft should be defaulted to Beneficiary"
        )

    async def test_mch_sector_suggests_growth_chart(
        self, client: httpx.AsyncClient, conversation_id: str
    ):
        await _setup_spec(client, conversation_id)

        resp = await client.post(
            "/enrich-spec",
            json={"conversation_id": conversation_id, "sector": "MCH"},
        )
        body = resp.json()
        growth_chart_ambs = [
            a for a in body["ambiguities"] if a["field"] == "showGrowthChart"
        ]
        assert len(growth_chart_ambs) > 0
        assert growth_chart_ambs[0]["default"] == "Yes"

    async def test_enriched_spec_stored_back(
        self, client: httpx.AsyncClient, conversation_id: str
    ):
        await _setup_spec(client, conversation_id)

        # Get spec before enrichment
        resp_before = await client.get(
            "/get-spec", params={"conversation_id": conversation_id}
        )
        yaml_before = resp_before.json()["spec_yaml"]

        # Enrich
        await client.post(
            "/enrich-spec",
            json={"conversation_id": conversation_id, "sector": "MCH"},
        )

        # Get spec after enrichment
        resp_after = await client.get(
            "/get-spec", params={"conversation_id": conversation_id}
        )
        yaml_after = resp_after.json()["spec_yaml"]

        # Should be different (defaults added)
        assert yaml_after != yaml_before
        assert "lastNameOptional" in yaml_after

    async def test_no_ambiguities_when_all_fields_present(
        self, client: httpx.AsyncClient, conversation_id: str
    ):
        """Entities with all fields set should produce 0 ambiguities."""
        complete_entities = {
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
        await client.post(
            "/store-entities",
            json={"conversation_id": conversation_id, "entities": complete_entities},
        )
        await client.post(
            "/generate-spec",
            json={"conversation_id": conversation_id, "org_name": "Complete"},
        )

        resp = await client.post(
            "/enrich-spec",
            json={"conversation_id": conversation_id, "sector": ""},
        )
        body = resp.json()
        # No subject type or program ambiguities (encounter has both set)
        entity_ambs = [
            a for a in body["ambiguities"] if a["field"] in ("subjectType", "program")
        ]
        assert len(entity_ambs) == 0

    async def test_404_without_spec(
        self, client: httpx.AsyncClient, conversation_id: str
    ):
        resp = await client.post(
            "/enrich-spec",
            json={"conversation_id": conversation_id},
        )
        assert resp.status_code == 404


# ---------------------------------------------------------------------------
# Schema-driven spec validation tests
# ---------------------------------------------------------------------------


@pytest.mark.asyncio(loop_scope="function")
class TestSchemaValidation:
    """validate_spec catches unknown fields using the comprehensive format schema."""

    async def test_unknown_subject_type_field_flagged(self, client: httpx.AsyncClient):
        spec = """
org: Test
subjectTypes:
  - name: Individual
    type: Person
    enableGPS: true
    trackHistory: true
"""
        resp = await client.post("/validate-spec", json={"spec_yaml": spec})
        body = resp.json()
        unknown_warnings = [w for w in body["warnings"] if "unknown field" in w.lower()]
        assert len(unknown_warnings) >= 2
        fields_flagged = " ".join(unknown_warnings)
        assert "enableGPS" in fields_flagged
        assert "trackHistory" in fields_flagged

    async def test_unknown_program_field_flagged(self, client: httpx.AsyncClient):
        spec = """
org: Test
subjectTypes:
  - name: Individual
    type: Person
programs:
  - name: MCH
    targetSubjectType: Individual
    enableNotifications: true
    maxParticipants: 100
"""
        resp = await client.post("/validate-spec", json={"spec_yaml": spec})
        body = resp.json()
        unknown_warnings = [w for w in body["warnings"] if "unknown field" in w.lower()]
        fields_flagged = " ".join(unknown_warnings)
        assert "enableNotifications" in fields_flagged
        assert "maxParticipants" in fields_flagged

    async def test_unknown_top_level_section_flagged(self, client: httpx.AsyncClient):
        spec = """
org: Test
subjectTypes:
  - name: Individual
    type: Person
randomSection:
  - foo: bar
automationRules:
  enabled: true
"""
        resp = await client.post("/validate-spec", json={"spec_yaml": spec})
        body = resp.json()
        section_warnings = [
            w for w in body["warnings"] if "unknown top-level section" in w.lower()
        ]
        assert len(section_warnings) >= 2
        flagged = " ".join(section_warnings)
        assert "randomSection" in flagged
        assert "automationRules" in flagged

    async def test_valid_spec_no_unknown_field_warnings(
        self, client: httpx.AsyncClient
    ):
        spec = """
org: Test
settings:
  languages: [en]
  enableComments: true
subjectTypes:
  - name: Individual
    type: Person
    allowProfilePicture: true
    uniqueName: true
programs:
  - name: MCH
    targetSubjectType: Individual
    colour: "#ff0000"
    showGrowthChart: true
encounterTypes:
  - name: ANC
    program: MCH
    subjectType: Individual
    scheduled: true
groups:
  - name: Everyone
"""
        resp = await client.post("/validate-spec", json={"spec_yaml": spec})
        body = resp.json()
        unknown_warnings = [w for w in body["warnings"] if "unknown field" in w.lower()]
        assert len(unknown_warnings) == 0

    async def test_unknown_encounter_field_flagged(self, client: httpx.AsyncClient):
        spec = """
org: Test
subjectTypes:
  - name: Individual
    type: Person
encounterTypes:
  - name: Visit
    subjectType: Individual
    maxVisitsPerDay: 5
    requiresApproval: true
"""
        resp = await client.post("/validate-spec", json={"spec_yaml": spec})
        body = resp.json()
        unknown_warnings = [w for w in body["warnings"] if "unknown field" in w.lower()]
        fields_flagged = " ".join(unknown_warnings)
        assert "maxVisitsPerDay" in fields_flagged
        assert "requiresApproval" in fields_flagged
