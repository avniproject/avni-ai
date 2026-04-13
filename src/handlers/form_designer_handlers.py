"""
Form designer handlers.

Provides endpoints for generating AVNI form JSON, suggesting form fields
based on encounter type and sector, and parsing natural-language skip
logic into declarative rules.

Endpoints:
  POST /form-designer/generate-form       — generate AVNI form JSON from field specs
  POST /form-designer/suggest-fields      — suggest fields for encounter + sector
  POST /form-designer/generate-skip-logic — parse natural language to declarative rules
"""

from __future__ import annotations

import logging
import re
from typing import Any

from starlette.requests import Request
from starlette.responses import JSONResponse

from ..bundle.forms import FormGenerator
from ..bundle.concepts import ConceptGenerator
from ..bundle.uuid_utils import generate_deterministic_uuid
from ..utils.sector_templates import get_sector_form_fields, get_available_sectors

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Skip logic pattern definitions
# ---------------------------------------------------------------------------

_SKIP_PATTERNS: list[dict[str, Any]] = [
    {
        "pattern": r"show\s+when\s+(.+?)\s+is\s+(.+)",
        "action": "show",
        "condition": "equals",
    },
    {
        "pattern": r"hide\s+when\s+(.+?)\s+is\s+(.+)",
        "action": "hide",
        "condition": "equals",
    },
    {
        "pattern": r"show\s+when\s+(.+?)\s+is\s+not\s+(.+)",
        "action": "show",
        "condition": "not_equals",
    },
    {
        "pattern": r"hide\s+when\s+(.+?)\s+is\s+not\s+(.+)",
        "action": "hide",
        "condition": "not_equals",
    },
    {
        "pattern": r"show\s+when\s+(.+?)\s*>\s*(\d+(?:\.\d+)?)",
        "action": "show",
        "condition": "greater_than",
    },
    {
        "pattern": r"hide\s+when\s+(.+?)\s*>\s*(\d+(?:\.\d+)?)",
        "action": "hide",
        "condition": "greater_than",
    },
    {
        "pattern": r"show\s+when\s+(.+?)\s*<\s*(\d+(?:\.\d+)?)",
        "action": "show",
        "condition": "less_than",
    },
    {
        "pattern": r"hide\s+when\s+(.+?)\s*<\s*(\d+(?:\.\d+)?)",
        "action": "hide",
        "condition": "less_than",
    },
]


def _parse_skip_logic(text: str) -> dict | None:
    """
    Parse a natural language skip logic expression into a structured rule.

    Supported patterns:
      - "show when X is Y"
      - "hide when X is Y"
      - "show when X is not Y"
      - "hide when X is not Y"
      - "show when X > N"
      - "hide when X > N"
      - "show when X < N"
      - "hide when X < N"

    Returns a dict with {action, condition, dependsOn, value} or None if
    no pattern matches.
    """
    if not text:
        return None

    cleaned = text.strip().lower()

    for sp in _SKIP_PATTERNS:
        match = re.match(sp["pattern"], cleaned, re.IGNORECASE)
        if match:
            depends_on = match.group(1).strip()
            value = match.group(2).strip()

            # Try to convert numeric values
            if sp["condition"] in ("greater_than", "less_than"):
                try:
                    value = float(value)
                    if value == int(value):
                        value = int(value)
                except ValueError:
                    pass

            return {
                "action": sp["action"],
                "condition": sp["condition"],
                "dependsOn": depends_on,
                "value": value,
            }

    return None


def _build_declarative_rule(parsed: dict, concept_uuid: str = "") -> list[dict]:
    """
    Convert a parsed skip logic dict into an AVNI declarative rule structure.
    """
    action_type = (
        "showFormElement" if parsed["action"] == "show" else "hideFormElement"
    )

    rhs: dict[str, Any] = {}
    operator = "containsAnswerConceptName"

    if parsed["condition"] == "equals":
        rhs = {
            "type": "answerConcept",
            "answerConceptNames": [parsed["value"]],
            "answerConceptUuids": [],
        }
        operator = "containsAnswerConceptName"
    elif parsed["condition"] == "not_equals":
        rhs = {
            "type": "answerConcept",
            "answerConceptNames": [parsed["value"]],
            "answerConceptUuids": [],
        }
        operator = "notContainsAnswerConceptName"
    elif parsed["condition"] == "greater_than":
        rhs = {"type": "value", "value": parsed["value"]}
        operator = "greaterThan"
    elif parsed["condition"] == "less_than":
        rhs = {"type": "value", "value": parsed["value"]}
        operator = "lessThan"

    return [
        {
            "actions": [{"actionType": action_type}],
            "conditions": [
                {
                    "compoundRule": {
                        "rules": [
                            {
                                "lhs": {
                                    "type": "concept",
                                    "scope": "encounter",
                                    "conceptName": parsed["dependsOn"],
                                    "conceptUuid": concept_uuid,
                                },
                                "rhs": rhs,
                                "operator": operator,
                            }
                        ]
                    }
                }
            ],
        }
    ]


# ---------------------------------------------------------------------------
# Handlers
# ---------------------------------------------------------------------------


async def handle_generate_form(request: Request) -> JSONResponse:
    """
    POST /form-designer/generate-form
    Body: {
        "name": "ANC",
        "formType": "ProgramEncounter",
        "fields": [{"name": "Weight", "dataType": "Numeric", ...}],
        "subjectType": "Individual",
        "program": "Pregnancy",
        "encounterType": "ANC"
    }
    Generates a complete AVNI form JSON with concepts, elements, and groups.
    """
    try:
        body = await request.json()
    except Exception:
        return JSONResponse({"error": "Invalid JSON body"}, status_code=400)

    name = body.get("name")
    form_type = body.get("formType", "Encounter")
    fields = body.get("fields", [])

    if not name:
        return JSONResponse({"error": "Missing 'name'"}, status_code=400)
    if not isinstance(fields, list):
        return JSONResponse({"error": "'fields' must be an array"}, status_code=400)

    try:
        # Generate concepts from field definitions
        concept_gen = ConceptGenerator()
        concepts = concept_gen.generate_from_fields(fields)

        # Build concept map
        concept_map: dict[str, dict] = {}
        for c in concepts:
            concept_map[c["name"]] = {
                "uuid": c["uuid"],
                "dataType": c["dataType"],
                "answers": c.get("answers"),
            }

        # Generate form
        form_gen = FormGenerator()
        form = form_gen.generate_form(
            name=name,
            form_type=form_type,
            fields=fields,
            concepts=concept_map,
        )

        logger.info(
            "form-designer/generate-form: generated form '%s' with %d fields",
            name,
            len(fields),
        )
        return JSONResponse(
            {
                "ok": True,
                "form": form,
                "concepts": concepts,
                "field_count": len(fields),
                "concept_count": len(concepts),
            }
        )

    except Exception as exc:
        logger.exception("form-designer/generate-form failed: %s", exc)
        return JSONResponse({"error": str(exc)}, status_code=500)


async def handle_suggest_form_fields(request: Request) -> JSONResponse:
    """
    POST /form-designer/suggest-fields
    Body: { "encounter_name": "ANC", "sector": "MCH" }
    Suggests pre-built field definitions for a given encounter and sector.
    """
    try:
        body = await request.json()
    except Exception:
        return JSONResponse({"error": "Invalid JSON body"}, status_code=400)

    encounter_name = body.get("encounter_name", "")
    sector = body.get("sector", "")

    if not encounter_name:
        return JSONResponse({"error": "Missing 'encounter_name'"}, status_code=400)

    fields = get_sector_form_fields(sector, encounter_name)

    logger.info(
        "form-designer/suggest-fields: sector=%s encounter=%s fields=%d",
        sector,
        encounter_name,
        len(fields),
    )
    return JSONResponse(
        {
            "ok": True,
            "encounter_name": encounter_name,
            "sector": sector,
            "fields": fields,
            "field_count": len(fields),
            "available_sectors": get_available_sectors(),
        }
    )


async def handle_generate_skip_logic(request: Request) -> JSONResponse:
    """
    POST /form-designer/generate-skip-logic
    Body: { "rules": ["show when Gender is Female", "hide when Age > 60"] }
    Parses natural language skip logic expressions into AVNI declarative rules.
    """
    try:
        body = await request.json()
    except Exception:
        return JSONResponse({"error": "Invalid JSON body"}, status_code=400)

    rules_input = body.get("rules", [])
    if not isinstance(rules_input, list):
        return JSONResponse({"error": "'rules' must be an array"}, status_code=400)

    results: list[dict] = []
    parse_errors: list[str] = []

    for idx, rule_text in enumerate(rules_input):
        if not isinstance(rule_text, str):
            parse_errors.append(f"Rule at index {idx} is not a string")
            continue

        parsed = _parse_skip_logic(rule_text)
        if parsed is None:
            parse_errors.append(
                f"Could not parse rule: '{rule_text}'. "
                "Supported patterns: 'show/hide when X is Y', "
                "'show/hide when X is not Y', 'show/hide when X > N', "
                "'show/hide when X < N'."
            )
            continue

        # Generate a concept UUID for the dependency
        concept_uuid = generate_deterministic_uuid(f"concept:{parsed['dependsOn']}")
        declarative_rule = _build_declarative_rule(parsed, concept_uuid)

        results.append(
            {
                "input": rule_text,
                "parsed": parsed,
                "declarativeRule": declarative_rule,
            }
        )

    logger.info(
        "form-designer/generate-skip-logic: parsed %d rules, %d errors",
        len(results),
        len(parse_errors),
    )
    return JSONResponse(
        {
            "ok": True,
            "results": results,
            "parsed_count": len(results),
            "error_count": len(parse_errors),
            "errors": parse_errors,
        }
    )
