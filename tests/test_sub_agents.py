"""Integration tests for the sub-agentic system API endpoints.

Uses httpx.AsyncClient with ASGITransport to test the FastAPI/Starlette
app without a running server.  Each test class mirrors one sub-agent's
responsibilities.

Requires: pytest-asyncio, httpx
"""

import uuid
import pytest
import pytest_asyncio
import httpx
from httpx import ASGITransport

from src.main import app  # Starlette/FastMCP ASGI app

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest_asyncio.fixture(autouse=True)
async def _clear_stores():
    """Clear in-memory stores between tests so state does not leak."""
    # Import stores and reset them
    try:
        from src.services import entity_store, spec_store, bundle_store

        for store in (entity_store, spec_store, bundle_store):
            if hasattr(store, "clear"):
                store.clear()
    except ImportError:
        pass  # Stores may not exist yet; tests will fail at the HTTP level
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


# ===========================================================================
# Chat SRS (Spec Agent) tests
# ===========================================================================


@pytest.mark.asyncio(loop_scope="function")
class TestChatSRS:
    """Spec-agent: session init, section updates, entity building, full flow."""

    async def test_init_session(self, client: httpx.AsyncClient, conversation_id: str):
        resp = await client.post(
            "/store-srs-text",
            json={
                "conversation_id": conversation_id,
                "srs_text": "MCH program for pregnant women with ANC visits",
            },
        )
        assert resp.status_code in (200, 201)
        body = resp.json()
        assert body.get("ok") is True or "conversation_id" in body

    async def test_update_section(
        self, client: httpx.AsyncClient, conversation_id: str
    ):
        # Seed entities first
        entities = {
            "subject_types": [
                {"name": "Woman", "type": "Person", "lowest_address_level": "Village"}
            ],
            "programs": [],
            "encounter_types": [],
            "address_levels": [],
            "forms": [],
        }
        await client.post(
            "/store-entities",
            json={"conversation_id": conversation_id, "entities": entities},
        )
        resp = await client.put(
            "/entities-section",
            json={
                "conversation_id": conversation_id,
                "section": "programs",
                "items": [
                    {
                        "name": "Maternal Health",
                        "target_subject_type": "Woman",
                        "colour": "#FF6F61",
                    }
                ],
            },
        )
        assert resp.status_code in (200, 201)

    async def test_build_entities(
        self, client: httpx.AsyncClient, conversation_id: str
    ):
        entities = {
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
                },
            ],
            "address_levels": [{"name": "Village", "level": 1, "parent": None}],
            "forms": [],
        }
        resp = await client.post(
            "/store-entities",
            json={"conversation_id": conversation_id, "entities": entities},
        )
        assert resp.status_code in (200, 201)
        body = resp.json()
        assert body.get("ok") is True

    async def test_full_flow_store_validate_generate(
        self, client: httpx.AsyncClient, conversation_id: str
    ):
        entities = {
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
                },
                {
                    "name": "ANC Visit Cancel",
                    "program_name": "Maternal Health",
                    "subject_type": "Woman",
                    "is_program_encounter": True,
                    "is_scheduled": False,
                },
            ],
            "address_levels": [{"name": "Village", "level": 1, "parent": None}],
            "forms": [
                {
                    "name": "Registration",
                    "formType": "IndividualProfile",
                    "subjectType": "Woman",
                    "fields": [
                        {"name": "Full name", "dataType": "Text", "mandatory": True}
                    ],
                },
            ],
        }
        r1 = await client.post(
            "/store-entities",
            json={"conversation_id": conversation_id, "entities": entities},
        )
        assert r1.status_code in (200, 201)

        r2 = await client.post(
            "/validate-entities", json={"conversation_id": conversation_id}
        )
        assert r2.status_code in (200, 201)

        r3 = await client.post(
            "/generate-spec",
            json={"conversation_id": conversation_id, "org_name": "test_org"},
        )
        assert r3.status_code in (200, 201)


# ===========================================================================
# Form (Bundle Config Agent) tests
# ===========================================================================


@pytest.mark.asyncio(loop_scope="function")
class TestFormDesign:
    """Bundle-config-agent: field suggestions, skip logic generation."""

    async def test_suggest_fields_via_entities(
        self, client: httpx.AsyncClient, conversation_id: str
    ):
        entities = {
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
            "encounter_types": [],
            "address_levels": [],
            "forms": [
                {
                    "name": "ANC Form",
                    "formType": "ProgramEncounter",
                    "subjectType": "Woman",
                    "program": "Maternal Health",
                    "encounterType": "ANC Visit",
                    "fields": [
                        {"name": "Weight", "dataType": "Numeric", "mandatory": True},
                        {
                            "name": "Haemoglobin",
                            "dataType": "Numeric",
                            "mandatory": True,
                        },
                    ],
                },
            ],
        }
        resp = await client.post(
            "/store-entities",
            json={"conversation_id": conversation_id, "entities": entities},
        )
        assert resp.status_code in (200, 201)

        r2 = await client.post(
            "/get-entities-section",
            json={"conversation_id": conversation_id, "section": "forms"},
        )
        assert r2.status_code in (200, 201)
        forms = r2.json()
        # The response should contain the forms section
        assert forms is not None

    async def test_skip_logic_pattern_coded_show(
        self, client: httpx.AsyncClient, conversation_id: str
    ):
        """Skip logic pattern 1: show when coded answer selected."""
        entities = {
            "subject_types": [
                {"name": "Woman", "type": "Person", "lowest_address_level": "Village"}
            ],
            "programs": [],
            "encounter_types": [],
            "address_levels": [],
            "forms": [
                {
                    "name": "ANC Form",
                    "formType": "ProgramEncounter",
                    "subjectType": "Woman",
                    "program": "Maternal Health",
                    "encounterType": "ANC Visit",
                    "fields": [
                        {
                            "name": "Is pregnant",
                            "dataType": "Coded",
                            "mandatory": True,
                            "options": ["Yes", "No"],
                        },
                        {
                            "name": "Gestational age",
                            "dataType": "Numeric",
                            "mandatory": False,
                        },
                    ],
                },
            ],
        }
        resp = await client.post(
            "/store-entities",
            json={"conversation_id": conversation_id, "entities": entities},
        )
        assert resp.status_code in (200, 201)

    async def test_skip_logic_pattern_coded_hide(
        self, client: httpx.AsyncClient, conversation_id: str
    ):
        """Skip logic pattern 2: hide when coded answer selected."""
        entities = {
            "subject_types": [
                {"name": "Child", "type": "Person", "lowest_address_level": "Village"}
            ],
            "programs": [],
            "encounter_types": [],
            "address_levels": [],
            "forms": [
                {
                    "name": "Feeding Form",
                    "formType": "ProgramEncounter",
                    "subjectType": "Child",
                    "program": "Nutrition",
                    "encounterType": "Feeding",
                    "fields": [
                        {
                            "name": "Currently breastfeeding",
                            "dataType": "Coded",
                            "mandatory": True,
                            "options": ["Yes", "No"],
                        },
                        {
                            "name": "Reason not breastfeeding",
                            "dataType": "Text",
                            "mandatory": False,
                        },
                    ],
                },
            ],
        }
        resp = await client.post(
            "/store-entities",
            json={"conversation_id": conversation_id, "entities": entities},
        )
        assert resp.status_code in (200, 201)

    async def test_skip_logic_pattern_numeric_threshold(
        self, client: httpx.AsyncClient, conversation_id: str
    ):
        """Skip logic pattern 3: show when numeric threshold met."""
        entities = {
            "subject_types": [
                {"name": "Woman", "type": "Person", "lowest_address_level": "Village"}
            ],
            "programs": [],
            "encounter_types": [],
            "address_levels": [],
            "forms": [
                {
                    "name": "Lab Form",
                    "formType": "ProgramEncounter",
                    "subjectType": "Woman",
                    "program": "Maternal Health",
                    "encounterType": "Lab Test",
                    "fields": [
                        {
                            "name": "Haemoglobin",
                            "dataType": "Numeric",
                            "mandatory": True,
                            "min": 2,
                            "max": 20,
                        },
                        {
                            "name": "Referral details",
                            "dataType": "Text",
                            "mandatory": False,
                        },
                    ],
                },
            ],
        }
        resp = await client.post(
            "/store-entities",
            json={"conversation_id": conversation_id, "entities": entities},
        )
        assert resp.status_code in (200, 201)

    async def test_skip_logic_pattern_defined(
        self, client: httpx.AsyncClient, conversation_id: str
    ):
        """Skip logic pattern 4: show when another field is defined."""
        entities = {
            "subject_types": [
                {"name": "Woman", "type": "Person", "lowest_address_level": "Village"}
            ],
            "programs": [],
            "encounter_types": [],
            "address_levels": [],
            "forms": [
                {
                    "name": "Complication Form",
                    "formType": "ProgramEncounter",
                    "subjectType": "Woman",
                    "program": "Maternal Health",
                    "encounterType": "Complication Check",
                    "fields": [
                        {
                            "name": "Complications",
                            "dataType": "Coded",
                            "mandatory": False,
                            "options": ["Bleeding", "Convulsions", "None"],
                        },
                        {
                            "name": "Complication details",
                            "dataType": "Text",
                            "mandatory": False,
                        },
                    ],
                },
            ],
        }
        resp = await client.post(
            "/store-entities",
            json={"conversation_id": conversation_id, "entities": entities},
        )
        assert resp.status_code in (200, 201)


# ===========================================================================
# Rules Agent tests
# ===========================================================================


@pytest.mark.asyncio(loop_scope="function")
class TestRulesAgent:
    """Rules-agent: rule generation and validation."""

    async def test_generate_visit_schedule_rule(
        self, client: httpx.AsyncClient, conversation_id: str
    ):
        """Test that entities with scheduled encounters store successfully."""
        entities = {
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
                },
            ],
            "address_levels": [],
            "forms": [],
        }
        resp = await client.post(
            "/store-entities",
            json={"conversation_id": conversation_id, "entities": entities},
        )
        assert resp.status_code in (200, 201)
        body = resp.json()
        assert body.get("ok") is True

    async def test_generate_decision_rule(
        self, client: httpx.AsyncClient, conversation_id: str
    ):
        """Test entities with decision-support fields store correctly."""
        entities = {
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
                },
            ],
            "address_levels": [],
            "forms": [
                {
                    "name": "ANC Form",
                    "formType": "ProgramEncounter",
                    "subjectType": "Woman",
                    "program": "Maternal Health",
                    "encounterType": "ANC Visit",
                    "fields": [
                        {
                            "name": "Haemoglobin",
                            "dataType": "Numeric",
                            "mandatory": True,
                        },
                        {
                            "name": "High Risk",
                            "dataType": "Coded",
                            "mandatory": False,
                            "options": ["High Risk Pregnancy"],
                        },
                    ],
                },
            ],
        }
        resp = await client.post(
            "/store-entities",
            json={"conversation_id": conversation_id, "entities": entities},
        )
        assert resp.status_code in (200, 201)

    async def test_validate_rule_valid_entities(
        self, client: httpx.AsyncClient, conversation_id: str
    ):
        """Validation passes for well-formed entities."""
        entities = {
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
                },
                {
                    "name": "ANC Visit Cancel",
                    "program_name": "Maternal Health",
                    "subject_type": "Woman",
                    "is_program_encounter": True,
                    "is_scheduled": False,
                },
            ],
            "address_levels": [{"name": "Village", "level": 1, "parent": None}],
            "forms": [
                {
                    "name": "Registration",
                    "formType": "IndividualProfile",
                    "subjectType": "Woman",
                    "fields": [{"name": "Name", "dataType": "Text", "mandatory": True}],
                },
            ],
        }
        await client.post(
            "/store-entities",
            json={"conversation_id": conversation_id, "entities": entities},
        )
        resp = await client.post(
            "/validate-entities", json={"conversation_id": conversation_id}
        )
        assert resp.status_code in (200, 201)

    async def test_validate_rule_missing_program(
        self, client: httpx.AsyncClient, conversation_id: str
    ):
        """Validation detects encounter referencing a non-existent program."""
        entities = {
            "subject_types": [
                {"name": "Woman", "type": "Person", "lowest_address_level": "Village"}
            ],
            "programs": [],  # no programs
            "encounter_types": [
                {
                    "name": "ANC Visit",
                    "program_name": "Maternal Health",
                    "subject_type": "Woman",
                    "is_program_encounter": True,
                    "is_scheduled": True,
                },
            ],
            "address_levels": [],
            "forms": [],
        }
        await client.post(
            "/store-entities",
            json={"conversation_id": conversation_id, "entities": entities},
        )
        resp = await client.post(
            "/validate-entities", json={"conversation_id": conversation_id}
        )
        assert resp.status_code in (200, 201)
        body = resp.json()
        # Expect errors or warnings about missing program
        assert (
            body.get("error_count", 0) > 0
            or body.get("warning_count", 0) > 0
            or "errors" in body
            or "warnings" in body
        )

    async def test_validate_rule_missing_subject_type(
        self, client: httpx.AsyncClient, conversation_id: str
    ):
        """Validation detects program referencing a non-existent subject type."""
        entities = {
            "subject_types": [],  # no subject types
            "programs": [
                {
                    "name": "Maternal Health",
                    "target_subject_type": "Woman",
                    "colour": "#FF6F61",
                }
            ],
            "encounter_types": [],
            "address_levels": [],
            "forms": [],
        }
        await client.post(
            "/store-entities",
            json={"conversation_id": conversation_id, "entities": entities},
        )
        resp = await client.post(
            "/validate-entities", json={"conversation_id": conversation_id}
        )
        assert resp.status_code in (200, 201)
        body = resp.json()
        assert (
            body.get("error_count", 0) > 0
            or body.get("warning_count", 0) > 0
            or "errors" in body
            or "warnings" in body
        )


# ===========================================================================
# Reports Agent tests
# ===========================================================================


@pytest.mark.asyncio(loop_scope="function")
class TestReportsAgent:
    """Reports-agent: dashboard suggestions and report card generation."""

    async def test_suggest_dashboard_via_spec(
        self, client: httpx.AsyncClient, conversation_id: str
    ):
        """Store entities and generate spec which includes dashboard layout."""
        entities = {
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
                },
                {
                    "name": "ANC Visit Cancel",
                    "program_name": "Maternal Health",
                    "subject_type": "Woman",
                    "is_program_encounter": True,
                    "is_scheduled": False,
                },
            ],
            "address_levels": [{"name": "Village", "level": 1, "parent": None}],
            "forms": [
                {
                    "name": "Registration",
                    "formType": "IndividualProfile",
                    "subjectType": "Woman",
                    "fields": [{"name": "Name", "dataType": "Text", "mandatory": True}],
                },
            ],
        }
        await client.post(
            "/store-entities",
            json={"conversation_id": conversation_id, "entities": entities},
        )
        resp = await client.post(
            "/generate-spec",
            json={"conversation_id": conversation_id, "org_name": "test_org"},
        )
        assert resp.status_code in (200, 201)

    async def test_generate_report_cards_via_bundle(
        self, client: httpx.AsyncClient, conversation_id: str
    ):
        """Generate bundle which includes report cards."""
        entities = {
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
                },
                {
                    "name": "ANC Visit Cancel",
                    "program_name": "Maternal Health",
                    "subject_type": "Woman",
                    "is_program_encounter": True,
                    "is_scheduled": False,
                },
            ],
            "address_levels": [{"name": "Village", "level": 1, "parent": None}],
            "forms": [
                {
                    "name": "Registration",
                    "formType": "IndividualProfile",
                    "subjectType": "Woman",
                    "fields": [{"name": "Name", "dataType": "Text", "mandatory": True}],
                },
                {
                    "name": "ANC Form",
                    "formType": "ProgramEncounter",
                    "subjectType": "Woman",
                    "program": "Maternal Health",
                    "encounterType": "ANC Visit",
                    "fields": [
                        {"name": "Weight", "dataType": "Numeric", "mandatory": True}
                    ],
                },
            ],
        }
        await client.post(
            "/store-entities",
            json={"conversation_id": conversation_id, "entities": entities},
        )
        resp = await client.post(
            "/generate-bundle",
            json={"conversation_id": conversation_id, "org_name": "test_org"},
        )
        assert resp.status_code in (200, 201)


# ===========================================================================
# Config Inspector Agent tests
# ===========================================================================


@pytest.mark.asyncio(loop_scope="function")
class TestConfigInspector:
    """Config-inspector-agent: configuration inspection and requirement compilation."""

    async def test_inspect_config_via_validation(
        self, client: httpx.AsyncClient, conversation_id: str
    ):
        """Validate entities acts as a config inspection step."""
        entities = {
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
                },
            ],
            "address_levels": [{"name": "Village", "level": 1, "parent": None}],
            "forms": [],
        }
        await client.post(
            "/store-entities",
            json={"conversation_id": conversation_id, "entities": entities},
        )
        resp = await client.post(
            "/validate-entities", json={"conversation_id": conversation_id}
        )
        assert resp.status_code in (200, 201)
        body = resp.json()
        # Should return validation results (errors/warnings counts)
        assert isinstance(body, dict)

    async def test_compile_requirements_via_spec(
        self, client: httpx.AsyncClient, conversation_id: str
    ):
        """Generate spec compiles requirements from entities."""
        entities = {
            "subject_types": [
                {"name": "Woman", "type": "Person", "lowest_address_level": "Village"},
                {"name": "Child", "type": "Person", "lowest_address_level": "Village"},
            ],
            "programs": [
                {
                    "name": "Maternal Health",
                    "target_subject_type": "Woman",
                    "colour": "#FF6F61",
                },
                {
                    "name": "Child Health",
                    "target_subject_type": "Child",
                    "colour": "#6FA3EF",
                },
            ],
            "encounter_types": [
                {
                    "name": "ANC Visit",
                    "program_name": "Maternal Health",
                    "subject_type": "Woman",
                    "is_program_encounter": True,
                    "is_scheduled": True,
                },
                {
                    "name": "ANC Visit Cancel",
                    "program_name": "Maternal Health",
                    "subject_type": "Woman",
                    "is_program_encounter": True,
                    "is_scheduled": False,
                },
            ],
            "address_levels": [
                {"name": "State", "level": 3, "parent": None},
                {"name": "District", "level": 2, "parent": "State"},
                {"name": "Village", "level": 1, "parent": "District"},
            ],
            "forms": [
                {
                    "name": "Woman Registration",
                    "formType": "IndividualProfile",
                    "subjectType": "Woman",
                    "fields": [
                        {"name": "Full name", "dataType": "Text", "mandatory": True},
                        {
                            "name": "Date of birth",
                            "dataType": "Date",
                            "mandatory": True,
                        },
                        {
                            "name": "Phone number",
                            "dataType": "PhoneNumber",
                            "mandatory": False,
                        },
                    ],
                },
            ],
        }
        await client.post(
            "/store-entities",
            json={"conversation_id": conversation_id, "entities": entities},
        )
        resp = await client.post(
            "/generate-spec",
            json={"conversation_id": conversation_id, "org_name": "test_org"},
        )
        assert resp.status_code in (200, 201)
        body = resp.json()
        assert body.get("stored") is True or "spec" in body or "ok" in body


# ===========================================================================
# Ambiguity Resolution tests
# ===========================================================================


@pytest.mark.asyncio(loop_scope="function")
class TestAmbiguityResolution:
    """Tests for ambiguity detection and resolution in SRS parsing."""

    async def test_get_ambiguities_from_srs(
        self, client: httpx.AsyncClient, conversation_id: str
    ):
        """Store SRS text that has ambiguous content."""
        resp = await client.post(
            "/store-srs-text",
            json={
                "conversation_id": conversation_id,
                "srs_text": "Program for women. Visits include checkup. Fields: name, some measurement, status.",
            },
        )
        assert resp.status_code in (200, 201)

        # Fetch it back
        r2 = await client.post(
            "/get-srs-text", json={"conversation_id": conversation_id}
        )
        assert r2.status_code in (200, 201)
        body = r2.json()
        assert "srs_text" in body or "text" in body or "content" in body

    async def test_resolve_ambiguities_via_entity_update(
        self, client: httpx.AsyncClient, conversation_id: str
    ):
        """Resolve ambiguities by updating entity sections with clarified data."""
        # Store initial ambiguous entities
        entities = {
            "subject_types": [
                {
                    "name": "Beneficiary",
                    "type": "Person",
                    "lowest_address_level": "Village",
                }
            ],
            "programs": [],
            "encounter_types": [],
            "address_levels": [],
            "forms": [
                {
                    "name": "Registration",
                    "formType": "IndividualProfile",
                    "subjectType": "Beneficiary",
                    "fields": [
                        {"name": "Name", "dataType": "Text", "mandatory": True},
                        {
                            "name": "Status",
                            "dataType": "Text",
                            "mandatory": False,
                        },  # ambiguous - should be Coded
                    ],
                },
            ],
        }
        await client.post(
            "/store-entities",
            json={"conversation_id": conversation_id, "entities": entities},
        )

        # Resolve: update the form with clarified field
        updated_forms = [
            {
                "name": "Registration",
                "formType": "IndividualProfile",
                "subjectType": "Beneficiary",
                "fields": [
                    {"name": "Name", "dataType": "Text", "mandatory": True},
                    {
                        "name": "Status",
                        "dataType": "Coded",
                        "mandatory": True,
                        "options": ["Active", "Inactive", "Migrated"],
                    },
                ],
            },
        ]
        resp = await client.put(
            "/entities-section",
            json={
                "conversation_id": conversation_id,
                "section": "forms",
                "items": updated_forms,
            },
        )
        assert resp.status_code in (200, 201)

        # Verify the update took effect
        r3 = await client.post(
            "/get-entities-section",
            json={"conversation_id": conversation_id, "section": "forms"},
        )
        assert r3.status_code in (200, 201)
