"""Functional tests for Form Designer, Rules, and Reports agent endpoints.

Exercises the generate-form, suggest-form-fields, generate-skip-logic,
generate-rule, validate-rule, generate-report-cards, and suggest-dashboard
endpoints through the ASGI test client without a running server.

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
# TestGenerateForm
# ===========================================================================


@pytest.mark.asyncio(loop_scope="function")
class TestGenerateForm:
    """POST /generate-form: generate AVNI form JSON from name + fields."""

    async def test_generate_form_with_name_and_fields(self, client: httpx.AsyncClient):
        resp = await client.post(
            "/generate-form",
            json={
                "name": "ANC Registration",
                "formType": "ProgramEncounter",
                "fields": [
                    {"name": "Weight", "dataType": "Numeric", "mandatory": True},
                    {"name": "BP Systolic", "dataType": "Numeric", "mandatory": True},
                    {
                        "name": "Blood Group",
                        "dataType": "Coded",
                        "mandatory": False,
                        "options": ["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"],
                    },
                ],
            },
        )
        assert resp.status_code == 200
        body = resp.json()
        assert body.get("ok") is True
        assert body["field_count"] == 3
        assert body["concept_count"] >= 3
        assert "form" in body

    async def test_generate_form_missing_name_returns_400(
        self, client: httpx.AsyncClient
    ):
        resp = await client.post(
            "/generate-form",
            json={
                "formType": "Encounter",
                "fields": [
                    {"name": "Weight", "dataType": "Numeric", "mandatory": True}
                ],
            },
        )
        assert resp.status_code == 400
        assert "name" in resp.json().get("error", "").lower()


# ===========================================================================
# TestSuggestFormFields
# ===========================================================================


SECTORS = ["MCH", "Nutrition", "Education", "WASH", "Livelihoods"]


@pytest.mark.asyncio(loop_scope="function")
class TestSuggestFormFields:
    """POST /suggest-form-fields: sector-aware field suggestions."""

    @pytest.mark.parametrize("sector", SECTORS)
    async def test_suggest_fields_per_sector(
        self, client: httpx.AsyncClient, sector: str
    ):
        resp = await client.post(
            "/suggest-form-fields",
            json={"encounter_name": "Home Visit", "sector": sector},
        )
        assert resp.status_code == 200
        body = resp.json()
        assert body.get("ok") is True
        assert isinstance(body.get("fields"), list)
        assert sector in body.get("available_sectors", [])


# ===========================================================================
# TestSkipLogic
# ===========================================================================

SKIP_PATTERNS = [
    "show when Gender is Female",
    "hide when Age > 60",
    "show when Status is not Active",
    "hide when Score < 50",
]


@pytest.mark.asyncio(loop_scope="function")
class TestSkipLogic:
    """POST /generate-skip-logic: natural language to declarative rules."""

    @pytest.mark.parametrize("rule_text", SKIP_PATTERNS)
    async def test_skip_logic_pattern(self, client: httpx.AsyncClient, rule_text: str):
        resp = await client.post(
            "/generate-skip-logic",
            json={"rules": [rule_text]},
        )
        assert resp.status_code == 200
        body = resp.json()
        assert body.get("ok") is True
        assert body["parsed_count"] == 1
        assert body["error_count"] == 0
        result = body["results"][0]
        assert result["input"] == rule_text
        assert "declarativeRule" in result
        parsed = result["parsed"]
        assert "action" in parsed
        assert "condition" in parsed
        assert "dependsOn" in parsed
        assert "value" in parsed


# ===========================================================================
# TestGenerateRule
# ===========================================================================

VALID_RULE_TYPES = [
    "visitSchedule",
    "decision",
    "validation",
    "eligibility",
    "summary",
    "worklist",
    "checklist",
]


@pytest.mark.asyncio(loop_scope="function")
class TestGenerateRule:
    """POST /generate-rule: parametrized across all 7 rule types."""

    @pytest.mark.parametrize("rule_type", VALID_RULE_TYPES)
    async def test_generate_rule_type(self, client: httpx.AsyncClient, rule_type: str):
        resp = await client.post(
            "/generate-rule",
            json={
                "rule_type": rule_type,
                "params": {
                    "schedule_days": 30,
                    "max_days": 45,
                    "encounter_name": "ANC Visit",
                    "concept_name": "Haemoglobin",
                    "min_value": 2,
                    "max_value": 20,
                    "name": "Default Worklist",
                },
            },
        )
        assert resp.status_code == 200
        body = resp.json()
        assert body.get("ok") is True
        assert body["rule_type"] == rule_type
        assert len(body["code"]) > 0
        # Generated code should pass its own validation
        validation = body.get("validation", {})
        assert validation.get("valid") is True

    async def test_generate_invalid_rule_type_returns_400(
        self, client: httpx.AsyncClient
    ):
        resp = await client.post(
            "/generate-rule",
            json={"rule_type": "nonexistentType", "params": {}},
        )
        assert resp.status_code == 400
        assert "Invalid rule_type" in resp.json().get("error", "")


# ===========================================================================
# TestValidateRule
# ===========================================================================


@pytest.mark.asyncio(loop_scope="function")
class TestValidateRule:
    """POST /validate-rule: static analysis on rule JS code."""

    async def test_validate_generated_rule_passes(self, client: httpx.AsyncClient):
        # First generate a valid rule
        gen_resp = await client.post(
            "/generate-rule",
            json={
                "rule_type": "visitSchedule",
                "params": {"encounter_name": "ANC Visit"},
            },
        )
        assert gen_resp.status_code == 200
        code = gen_resp.json()["code"]

        # Now validate it
        val_resp = await client.post(
            "/validate-rule",
            json={"code": code, "rule_type": "visitSchedule"},
        )
        assert val_resp.status_code == 200
        body = val_resp.json()
        assert body.get("ok") is True
        assert body["valid"] is True
        assert body["error_count"] == 0

    async def test_validate_rule_with_eval_fails(self, client: httpx.AsyncClient):
        bad_code = """'use strict';
({params, imports}) => {
    const result = eval("1+1");
    return result;
};"""
        resp = await client.post(
            "/validate-rule",
            json={"code": bad_code},
        )
        assert resp.status_code == 200
        body = resp.json()
        assert body.get("ok") is True
        assert body["valid"] is False
        assert body["error_count"] > 0
        # Should flag eval() usage
        assert any("eval" in e.lower() for e in body["errors"])


# ===========================================================================
# TestReportCards
# ===========================================================================


@pytest.mark.asyncio(loop_scope="function")
class TestReportCards:
    """POST /generate-report-cards: standard and custom card generation."""

    async def test_generate_6_standard_cards(self, client: httpx.AsyncClient):
        card_types = [
            "scheduledVisits",
            "overdueVisits",
            "total",
            "recentRegistrations",
            "recentEnrolments",
            "recentVisits",
        ]
        resp = await client.post(
            "/generate-report-cards",
            json={"org_name": "TestOrg", "card_types": card_types},
        )
        assert resp.status_code == 200
        body = resp.json()
        assert body.get("ok") is True
        assert body["card_count"] == 6
        cards = body["report_cards"]
        assert len(cards) == 6
        # Each card has a uuid
        for card in cards:
            assert "uuid" in card
            assert "name" in card
            assert card["voided"] is False

    async def test_generate_custom_cards(self, client: httpx.AsyncClient):
        resp = await client.post(
            "/generate-report-cards",
            json={
                "org_name": "TestOrg",
                "card_types": [],
                "custom_cards": [
                    {"name": "High Risk Pregnancies", "color": "#d32f2f"},
                    {"name": "Active SHGs", "color": "#795548"},
                ],
            },
        )
        assert resp.status_code == 200
        body = resp.json()
        assert body.get("ok") is True
        assert body["card_count"] == 2
        names = [c["name"] for c in body["report_cards"]]
        assert any("High Risk" in n for n in names)
        assert any("Active SHGs" in n for n in names)


# ===========================================================================
# TestSuggestDashboard
# ===========================================================================

DASHBOARD_SECTORS = ["MCH", "Nutrition", "Livelihoods"]


@pytest.mark.asyncio(loop_scope="function")
class TestSuggestDashboard:
    """POST /suggest-dashboard: sector-specific dashboard card suggestions."""

    @pytest.mark.parametrize("sector", DASHBOARD_SECTORS)
    async def test_suggest_dashboard_per_sector(
        self, client: httpx.AsyncClient, sector: str
    ):
        resp = await client.post(
            "/suggest-dashboard",
            json={"sector": sector, "org_name": "TestOrg"},
        )
        assert resp.status_code == 200
        body = resp.json()
        assert body.get("ok") is True
        assert body["sector"] == sector
        # Standard cards always present
        assert len(body["standard_cards"]) >= 1
        # Sector-specific cards returned
        assert len(body["sector_cards"]) >= 1
        # Layout includes sector section
        section_names = [s["name"] for s in body["suggested_layout"]]
        assert any(sector in n for n in section_names)
