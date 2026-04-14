"""Functional tests for Chat SRS, Ambiguity Resolution, Config Inspector,
and Bulk Admin agent endpoints.

Exercises the chat-srs session lifecycle, ambiguity store, inspect-config,
compile-requirements, bulk-locations, and bulk-users endpoints through
the ASGI test client without a running server.

Requires: pytest-asyncio, httpx
"""

import uuid

import pytest
import pytest_asyncio
import httpx
from httpx import ASGITransport

from src.main import app

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest_asyncio.fixture(autouse=True)
async def _clear_stores():
    """Clear in-memory stores between tests so state does not leak."""
    try:
        from src.services import entity_store, spec_store, bundle_store

        for store in (entity_store, spec_store, bundle_store):
            if hasattr(store, "clear"):
                store.clear()
    except ImportError:
        pass
    try:
        from src.handlers.chat_srs_handlers import get_chat_srs_session_store

        store = get_chat_srs_session_store()
        store._store.clear()
    except ImportError:
        pass
    try:
        from src.handlers.ambiguity_handlers import get_ambiguity_store

        store = get_ambiguity_store()
        store._store.clear()
    except ImportError:
        pass
    yield


@pytest_asyncio.fixture
def conversation_id() -> str:
    return f"test-{uuid.uuid4().hex[:12]}"


@pytest_asyncio.fixture
async def client():
    transport = ASGITransport(app=app)
    async with httpx.AsyncClient(
        transport=transport, base_url="http://testserver"
    ) as c:
        yield c


# ---------------------------------------------------------------------------
# Org fixture data used across parametrized tests
# ---------------------------------------------------------------------------

ORG_CONFIGS = [
    {
        "sector": "MCH",
        "org_name": "Maternal Health NGO",
        "subject_types": [
            {"name": "Woman", "type": "Person", "lowest_address_level": "Village"}
        ],
        "programs": [
            {
                "name": "Maternal Health",
                "target_subject_type": "Woman",
                "colour": "#FF6F61",
            }
        ],
        "encounter_types": [
            {
                "name": "ANC Visit",
                "program_name": "Maternal Health",
                "subject_type": "Woman",
                "is_program_encounter": True,
                "is_scheduled": True,
            }
        ],
    },
    {
        "sector": "Nutrition",
        "org_name": "Child Nutrition Program",
        "subject_types": [
            {"name": "Child", "type": "Person", "lowest_address_level": "Village"}
        ],
        "programs": [
            {
                "name": "Nutrition Program",
                "target_subject_type": "Child",
                "colour": "#6FA3EF",
            }
        ],
        "encounter_types": [
            {
                "name": "Growth Monitoring",
                "program_name": "Nutrition Program",
                "subject_type": "Child",
                "is_program_encounter": True,
                "is_scheduled": True,
            }
        ],
    },
    {
        "sector": "Education",
        "org_name": "School Attendance Tracker",
        "subject_types": [
            {"name": "Student", "type": "Person", "lowest_address_level": "Village"}
        ],
        "programs": [
            {
                "name": "Education Program",
                "target_subject_type": "Student",
                "colour": "#2196F3",
            }
        ],
        "encounter_types": [
            {
                "name": "Attendance Check",
                "program_name": "Education Program",
                "subject_type": "Student",
                "is_program_encounter": True,
                "is_scheduled": True,
            }
        ],
    },
    {
        "sector": "WASH",
        "org_name": "Water Sanitation Project",
        "subject_types": [
            {
                "name": "Household",
                "type": "Household",
                "lowest_address_level": "Village",
            }
        ],
        "programs": [
            {
                "name": "WASH Program",
                "target_subject_type": "Household",
                "colour": "#00BCD4",
            }
        ],
        "encounter_types": [
            {
                "name": "Water Quality Test",
                "program_name": "WASH Program",
                "subject_type": "Household",
                "is_program_encounter": True,
                "is_scheduled": True,
            }
        ],
    },
    {
        "sector": "Livelihoods",
        "org_name": "Skills Training Centre",
        "subject_types": [
            {"name": "Beneficiary", "type": "Person", "lowest_address_level": "Village"}
        ],
        "programs": [
            {
                "name": "Livelihoods Program",
                "target_subject_type": "Beneficiary",
                "colour": "#795548",
            }
        ],
        "encounter_types": [
            {
                "name": "Skills Assessment",
                "program_name": "Livelihoods Program",
                "subject_type": "Beneficiary",
                "is_program_encounter": True,
                "is_scheduled": False,
            }
        ],
    },
]


# ===========================================================================
# TestChatSrsSession
# ===========================================================================


@pytest.mark.asyncio(loop_scope="function")
class TestChatSrsSession:
    """Chat SRS session lifecycle: init, duplicate, update, build."""

    @pytest.mark.parametrize(
        "org_cfg", ORG_CONFIGS, ids=[c["sector"] for c in ORG_CONFIGS]
    )
    async def test_init_session_with_sector(
        self, client: httpx.AsyncClient, org_cfg: dict
    ):
        cid = f"test-chat-{uuid.uuid4().hex[:8]}"
        resp = await client.post(
            "/chat-srs/init-session",
            json={
                "conversation_id": cid,
                "sector": org_cfg["sector"],
                "org_name": org_cfg["org_name"],
            },
        )
        assert resp.status_code == 200
        body = resp.json()
        assert body.get("ok") is True
        assert body["conversation_id"] == cid
        assert body["sector"] == org_cfg["sector"]
        assert "sections" in body

    async def test_duplicate_session_returns_409(
        self, client: httpx.AsyncClient, conversation_id: str
    ):
        # First init succeeds
        resp1 = await client.post(
            "/chat-srs/init-session",
            json={
                "conversation_id": conversation_id,
                "sector": "MCH",
                "org_name": "Test",
            },
        )
        assert resp1.status_code == 200

        # Duplicate init returns 409
        resp2 = await client.post(
            "/chat-srs/init-session",
            json={
                "conversation_id": conversation_id,
                "sector": "MCH",
                "org_name": "Test",
            },
        )
        assert resp2.status_code == 409

    async def test_update_subject_types_section(
        self, client: httpx.AsyncClient, conversation_id: str
    ):
        # Init session
        await client.post(
            "/chat-srs/init-session",
            json={
                "conversation_id": conversation_id,
                "sector": "MCH",
                "org_name": "Test",
            },
        )

        # Update subject_types section
        resp = await client.post(
            "/chat-srs/update-section",
            json={
                "conversation_id": conversation_id,
                "section": "subject_types",
                "data": [
                    {
                        "name": "Woman",
                        "type": "Person",
                        "lowest_address_level": "Village",
                    }
                ],
            },
        )
        assert resp.status_code == 200
        body = resp.json()
        assert body.get("ok") is True
        assert "subject_types" in body["completed_sections"]

    @pytest.mark.parametrize(
        "org_cfg", ORG_CONFIGS, ids=[c["sector"] for c in ORG_CONFIGS]
    )
    async def test_build_entities_produces_subject_types(
        self, client: httpx.AsyncClient, org_cfg: dict
    ):
        cid = f"test-build-{uuid.uuid4().hex[:8]}"
        # Init
        await client.post(
            "/chat-srs/init-session",
            json={
                "conversation_id": cid,
                "sector": org_cfg["sector"],
                "org_name": org_cfg["org_name"],
            },
        )
        # Populate subject_types
        await client.post(
            "/chat-srs/update-section",
            json={
                "conversation_id": cid,
                "section": "subject_types",
                "data": org_cfg["subject_types"],
            },
        )
        # Populate programs
        await client.post(
            "/chat-srs/update-section",
            json={
                "conversation_id": cid,
                "section": "programs",
                "data": org_cfg["programs"],
            },
        )
        # Populate encounter_types
        await client.post(
            "/chat-srs/update-section",
            json={
                "conversation_id": cid,
                "section": "encounter_types",
                "data": org_cfg["encounter_types"],
            },
        )

        # Build entities
        resp = await client.post(
            "/chat-srs/build-entities",
            json={"conversation_id": cid},
        )
        assert resp.status_code == 200
        body = resp.json()
        assert body.get("ok") is True
        entities = body["entities"]
        assert len(entities["subject_types"]) >= 1


# ===========================================================================
# TestAmbiguityResolution
# ===========================================================================


@pytest.mark.asyncio(loop_scope="function")
class TestAmbiguityResolution:
    """GET /get-ambiguities: returns empty list when no ambiguities stored."""

    async def test_get_without_store_returns_empty(
        self, client: httpx.AsyncClient, conversation_id: str
    ):
        resp = await client.get(
            "/get-ambiguities",
            params={"conversation_id": conversation_id},
        )
        assert resp.status_code == 200
        body = resp.json()
        assert body["ambiguities"] == []
        assert body["total"] == 0
        assert body["all_resolved"] is True


# ===========================================================================
# TestInspectConfig
# ===========================================================================


@pytest.mark.asyncio(loop_scope="function")
class TestInspectConfig:
    """POST /inspect-config: gap analysis with completeness score."""

    @pytest.mark.parametrize(
        "org_cfg", ORG_CONFIGS, ids=[c["sector"] for c in ORG_CONFIGS]
    )
    async def test_inspect_config_completeness(
        self, client: httpx.AsyncClient, org_cfg: dict
    ):
        entities = {
            "subject_types": org_cfg["subject_types"],
            "programs": org_cfg["programs"],
            "encounter_types": org_cfg["encounter_types"],
            "address_levels": [{"name": "Village", "level": 1, "parent": None}],
            "forms": [
                {
                    "name": "Registration",
                    "formType": "IndividualProfile",
                    "subjectType": org_cfg["subject_types"][0]["name"],
                    "fields": [{"name": "Name", "dataType": "Text", "mandatory": True}],
                }
            ],
        }
        resp = await client.post(
            "/inspect-config",
            json={"entities": entities},
        )
        assert resp.status_code == 200
        body = resp.json()
        assert body.get("ok") is True
        score = body["completeness_score"]
        assert 0.0 <= score <= 1.0
        # Entity counts should match what we sent
        counts = body["entity_counts"]
        assert counts["subject_types"] == len(org_cfg["subject_types"])
        assert counts["programs"] == len(org_cfg["programs"])
        assert counts["encounter_types"] == len(org_cfg["encounter_types"])


# ===========================================================================
# TestCompileRequirements
# ===========================================================================


@pytest.mark.asyncio(loop_scope="function")
class TestCompileRequirements:
    """POST /compile-requirements: requirement checking against entities."""

    @pytest.mark.parametrize(
        "org_cfg", ORG_CONFIGS, ids=[c["sector"] for c in ORG_CONFIGS]
    )
    async def test_build_requirements_from_entities(
        self, client: httpx.AsyncClient, org_cfg: dict
    ):
        entities = {
            "subject_types": org_cfg["subject_types"],
            "programs": org_cfg["programs"],
            "encounter_types": org_cfg["encounter_types"],
            "address_levels": [],
            "forms": [],
        }
        requirements = [
            {
                "description": f"Must have {org_cfg['subject_types'][0]['name']} subject type",
                "entity_type": "subject_type",
                "name": org_cfg["subject_types"][0]["name"],
            },
            {
                "description": f"Must have {org_cfg['programs'][0]['name']} program",
                "entity_type": "program",
                "name": org_cfg["programs"][0]["name"],
            },
            {
                "description": f"Must have {org_cfg['encounter_types'][0]['name']} encounter",
                "entity_type": "encounter_type",
                "name": org_cfg["encounter_types"][0]["name"],
            },
        ]
        resp = await client.post(
            "/compile-requirements",
            json={"requirements": requirements, "entities": entities},
        )
        assert resp.status_code == 200
        body = resp.json()
        assert body.get("ok") is True
        assert body["total"] == 3
        assert body["all_met"] is True
        assert body["met_count"] == 3
        assert body["not_met_count"] == 0

    async def test_unmet_requirements_detected(self, client: httpx.AsyncClient):
        entities = {
            "subject_types": [],
            "programs": [],
            "encounter_types": [],
            "address_levels": [],
            "forms": [],
        }
        requirements = [
            {
                "description": "Must have Woman subject type",
                "entity_type": "subject_type",
                "name": "Woman",
            },
        ]
        resp = await client.post(
            "/compile-requirements",
            json={"requirements": requirements, "entities": entities},
        )
        assert resp.status_code == 200
        body = resp.json()
        assert body.get("ok") is True
        assert body["all_met"] is False
        assert body["not_met_count"] >= 1


# ===========================================================================
# TestBulkLocations
# ===========================================================================


@pytest.mark.asyncio(loop_scope="function")
class TestBulkLocations:
    """POST /api/bulk-locations: hierarchy validation and sorting."""

    async def test_valid_hierarchy_state_district_village(
        self, client: httpx.AsyncClient
    ):
        resp = await client.post(
            "/api/bulk-locations",
            json={
                "locations": [
                    {"name": "Karnataka", "type": "State", "level": 3},
                    {
                        "name": "Bangalore",
                        "type": "District",
                        "level": 2,
                        "parent": "Karnataka",
                    },
                    {
                        "name": "Koramangala",
                        "type": "Village",
                        "level": 1,
                        "parent": "Bangalore",
                    },
                ]
            },
        )
        assert resp.status_code == 200
        body = resp.json()
        assert body.get("ok") is True
        assert body["location_count"] == 3
        # Verify creation order: highest level first
        order = body["creation_order"]
        assert order.index("Karnataka") < order.index("Bangalore")
        assert order.index("Bangalore") < order.index("Koramangala")
        # Each location gets a UUID
        for loc in body["locations"]:
            assert "uuid" in loc

    async def test_missing_parent_returns_422(self, client: httpx.AsyncClient):
        resp = await client.post(
            "/api/bulk-locations",
            json={
                "locations": [
                    {
                        "name": "Orphan Village",
                        "type": "Village",
                        "level": 1,
                        "parent": "NonExistentDistrict",
                    },
                ]
            },
        )
        assert resp.status_code == 422
        body = resp.json()
        assert "validation_errors" in body


# ===========================================================================
# TestBulkUsers
# ===========================================================================


@pytest.mark.asyncio(loop_scope="function")
class TestBulkUsers:
    """POST /api/bulk-users: user validation and UUID assignment."""

    async def test_valid_users(self, client: httpx.AsyncClient):
        resp = await client.post(
            "/api/bulk-users",
            json={
                "users": [
                    {
                        "username": "field_worker_1",
                        "name": "Field Worker 1",
                        "email": "fw1@example.com",
                        "phone": "9876543210",
                        "catchment": "Block A",
                        "groups": ["Everyone"],
                    },
                    {
                        "username": "supervisor_1",
                        "name": "Supervisor 1",
                        "email": "sup1@example.com",
                        "catchment": "Block A",
                        "groups": ["Everyone", "Supervisors"],
                    },
                ]
            },
        )
        assert resp.status_code == 200
        body = resp.json()
        assert body.get("ok") is True
        assert body["user_count"] == 2
        for user in body["users"]:
            assert "uuid" in user
            assert "username" in user

    async def test_missing_username_returns_422(self, client: httpx.AsyncClient):
        resp = await client.post(
            "/api/bulk-users",
            json={
                "users": [
                    {"name": "No Username User", "email": "no@example.com"},
                ]
            },
        )
        assert resp.status_code == 422
        body = resp.json()
        assert "validation_errors" in body
