"""
Report card and dashboard generation handlers.

Provides endpoints for generating AVNI report card JSON entries and
suggesting sector-specific dashboard cards.

Endpoints:
  POST /reports/generate-cards       — generate reportCard.json entries with UUIDs
  POST /reports/suggest-dashboard    — suggest sector-specific dashboard cards
"""

from __future__ import annotations

import logging
from typing import Any

from starlette.requests import Request
from starlette.responses import JSONResponse

from ..bundle.uuid_utils import generate_deterministic_uuid
from ..utils.sector_templates import get_available_sectors

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Standard card types (from Avni production — stable UUIDs)
# ---------------------------------------------------------------------------

STANDARD_CARD_TYPES: dict[str, dict[str, str]] = {
    "scheduledVisits": {
        "uuid": "27020b32-c21b-43a4-81bd-7b88ad3a6ef0",
        "color": "#388e3c",
        "label": "Scheduled visits",
    },
    "overdueVisits": {
        "uuid": "9f88bee5-2ab9-4ac4-ae19-d07e9715bdb5",
        "color": "#d32f2f",
        "label": "Overdue visits",
    },
    "total": {
        "uuid": "1fbcadf3-bf1a-439e-9e13-24adddfbf6c0",
        "color": "#ffffff",
        "label": "Total",
    },
    "recentRegistrations": {
        "uuid": "88a7514c-48c0-4d5d-a421-d074e43bb36c",
        "color": "#ffffff",
        "label": "Recent registrations",
    },
    "recentEnrolments": {
        "uuid": "a5efc04c-317a-4823-a203-e62603454a65",
        "color": "#ffffff",
        "label": "Recent enrolments",
    },
    "recentVisits": {
        "uuid": "77b5b3fa-de35-4f24-996b-2842492ea6e0",
        "color": "#ffffff",
        "label": "Recent visits",
    },
}

# ---------------------------------------------------------------------------
# Sector-specific dashboard suggestions
# ---------------------------------------------------------------------------

_SECTOR_DASHBOARD_SUGGESTIONS: dict[str, list[dict[str, Any]]] = {
    "MCH": [
        {
            "name": "High Risk Pregnancies",
            "description": "Count of pregnant women with high-risk indicators",
            "type": "custom",
            "color": "#d32f2f",
        },
        {
            "name": "ANC Compliance",
            "description": "Percentage of women with all ANC visits on time",
            "type": "custom",
            "color": "#388e3c",
        },
        {
            "name": "Institutional Deliveries",
            "description": "Count of deliveries at health facilities",
            "type": "custom",
            "color": "#1976d2",
        },
        {
            "name": "Low Birth Weight",
            "description": "Count of newborns with birth weight < 2500g",
            "type": "custom",
            "color": "#ff9800",
        },
        {
            "name": "Immunization Coverage",
            "description": "Percentage of children fully immunized",
            "type": "custom",
            "color": "#4caf50",
        },
    ],
    "Nutrition": [
        {
            "name": "SAM Children",
            "description": "Count of children with severe acute malnutrition",
            "type": "custom",
            "color": "#d32f2f",
        },
        {
            "name": "MAM Children",
            "description": "Count of children with moderate acute malnutrition",
            "type": "custom",
            "color": "#ff9800",
        },
        {
            "name": "Recovery Rate",
            "description": "Percentage of malnourished children who improved",
            "type": "custom",
            "color": "#4caf50",
        },
    ],
    "Livelihoods": [
        {
            "name": "Active SHGs",
            "description": "Count of self help groups with recent meetings",
            "type": "custom",
            "color": "#795548",
        },
        {
            "name": "Placement Rate",
            "description": "Percentage of trained individuals placed in jobs",
            "type": "custom",
            "color": "#4caf50",
        },
        {
            "name": "Training Dropouts",
            "description": "Count of individuals who dropped out of training",
            "type": "custom",
            "color": "#d32f2f",
        },
    ],
    "Education": [
        {
            "name": "Attendance Rate",
            "description": "Average attendance percentage across schools",
            "type": "custom",
            "color": "#2196f3",
        },
        {
            "name": "At Risk Students",
            "description": "Students with attendance below 75%",
            "type": "custom",
            "color": "#d32f2f",
        },
        {
            "name": "Learning Improvement",
            "description": "Students showing improvement in assessments",
            "type": "custom",
            "color": "#4caf50",
        },
    ],
    "WASH": [
        {
            "name": "Unsafe Water Sources",
            "description": "Water sources that failed quality testing",
            "type": "custom",
            "color": "#d32f2f",
        },
        {
            "name": "ODF Households",
            "description": "Households with functional toilets",
            "type": "custom",
            "color": "#4caf50",
        },
        {
            "name": "Pending Follow-ups",
            "description": "Households with unresolved WASH issues",
            "type": "custom",
            "color": "#ff9800",
        },
    ],
}


# ---------------------------------------------------------------------------
# Handlers
# ---------------------------------------------------------------------------


async def handle_generate_report_cards(request: Request) -> JSONResponse:
    """
    POST /reports/generate-cards
    Body: {
        "org_name": "MyOrg",
        "card_types": ["scheduledVisits", "overdueVisits", "total"],
        "custom_cards": [{"name": "High Risk", "color": "#d32f2f"}]
    }
    Generates reportCard.json entries with deterministic UUIDs.
    """
    try:
        body = await request.json()
    except Exception:
        return JSONResponse({"error": "Invalid JSON body"}, status_code=400)

    org_name = body.get("org_name", "MyOrg")
    card_types = body.get("card_types", list(STANDARD_CARD_TYPES.keys()))
    custom_cards = body.get("custom_cards", [])

    if not isinstance(card_types, list):
        return JSONResponse({"error": "'card_types' must be an array"}, status_code=400)
    if not isinstance(custom_cards, list):
        return JSONResponse(
            {"error": "'custom_cards' must be an array"}, status_code=400
        )

    report_cards: list[dict] = []

    # Generate standard cards
    for card_type in card_types:
        card_meta = STANDARD_CARD_TYPES.get(card_type)
        if not card_meta:
            continue

        card_uuid = generate_deterministic_uuid(f"reportCard:{org_name}:{card_type}")
        card: dict[str, Any] = {
            "uuid": card_uuid,
            "name": f"{org_name}: {card_meta['label']}",
            "color": card_meta["color"],
            "nested": False,
            "count": 1,
            "standardReportCardType": card_meta["uuid"],
            "standardReportCardInputSubjectTypes": [],
            "standardReportCardInputPrograms": [],
            "standardReportCardInputEncounterTypes": [],
            "voided": False,
        }
        report_cards.append(card)

    # Generate custom cards
    for cc in custom_cards:
        if not isinstance(cc, dict) or not cc.get("name"):
            continue
        card_uuid = generate_deterministic_uuid(
            f"reportCard:{org_name}:custom:{cc['name']}"
        )
        card = {
            "uuid": card_uuid,
            "name": f"{org_name}: {cc['name']}",
            "color": cc.get("color", "#ffffff"),
            "nested": False,
            "count": 1,
            "query": cc.get("query", ""),
            "voided": False,
        }
        report_cards.append(card)

    logger.info(
        "reports/generate-cards: generated %d cards for org=%s",
        len(report_cards),
        org_name,
    )
    return JSONResponse(
        {
            "ok": True,
            "report_cards": report_cards,
            "card_count": len(report_cards),
            "available_card_types": list(STANDARD_CARD_TYPES.keys()),
        }
    )


async def handle_suggest_dashboard(request: Request) -> JSONResponse:
    """
    POST /reports/suggest-dashboard
    Body: { "sector": "MCH", "org_name": "MyOrg" }
    Suggests sector-specific dashboard cards and layout.
    """
    try:
        body = await request.json()
    except Exception:
        return JSONResponse({"error": "Invalid JSON body"}, status_code=400)

    sector = body.get("sector", "")

    # Always include standard cards
    standard_suggestions = [
        {
            "name": "Scheduled Visits",
            "type": "standard",
            "card_type": "scheduledVisits",
        },
        {"name": "Overdue Visits", "type": "standard", "card_type": "overdueVisits"},
        {"name": "Total Registrations", "type": "standard", "card_type": "total"},
        {
            "name": "Recent Registrations",
            "type": "standard",
            "card_type": "recentRegistrations",
        },
        {
            "name": "Recent Enrolments",
            "type": "standard",
            "card_type": "recentEnrolments",
        },
        {"name": "Recent Visits", "type": "standard", "card_type": "recentVisits"},
    ]

    # Get sector-specific suggestions
    sector_suggestions = _SECTOR_DASHBOARD_SUGGESTIONS.get(sector, [])

    # Build suggested dashboard layout
    sections: list[dict] = [
        {
            "name": "Visit Overview",
            "cards": ["scheduledVisits", "overdueVisits"],
        },
        {
            "name": "Recent Activity",
            "cards": ["recentRegistrations", "recentEnrolments", "recentVisits"],
        },
        {
            "name": "Summary",
            "cards": ["total"],
        },
    ]

    if sector_suggestions:
        sections.append(
            {
                "name": f"{sector} Indicators",
                "cards": [s["name"] for s in sector_suggestions],
            }
        )

    logger.info(
        "reports/suggest-dashboard: sector=%s standard=%d sector_specific=%d",
        sector,
        len(standard_suggestions),
        len(sector_suggestions),
    )
    return JSONResponse(
        {
            "ok": True,
            "sector": sector,
            "standard_cards": standard_suggestions,
            "sector_cards": sector_suggestions,
            "suggested_layout": sections,
            "available_sectors": get_available_sectors(),
        }
    )
