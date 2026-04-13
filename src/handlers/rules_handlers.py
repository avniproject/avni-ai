"""
Rule generation and validation handlers.

Provides endpoints for generating JavaScript rules for AVNI's rule engine
and performing static analysis on rule code.

Endpoints:
  POST /rules/generate  — generate JS rule code from a specification
  POST /rules/validate  — static analysis of rule code
"""

from __future__ import annotations

import logging
import re
from typing import Any

from starlette.requests import Request
from starlette.responses import JSONResponse


logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Rule types and their templates
# ---------------------------------------------------------------------------

VALID_RULE_TYPES = [
    "visitSchedule",
    "decision",
    "validation",
    "eligibility",
    "summary",
    "worklist",
    "checklist",
]

_RULE_TEMPLATES: dict[str, str] = {
    "visitSchedule": """\
'use strict';
({params, imports}) => {
    const programEncounter = params.entity;
    const scheduleBuilder = new imports.rulesConfig.VisitScheduleBuilder({
        programEnrolment: programEncounter.programEnrolment,
    });
    // Schedule next visit %(schedule_days)d days from today, max %(max_days)d days
    const scheduledDate = new Date();
    scheduledDate.setDate(scheduledDate.getDate() + %(schedule_days)d);
    const maxDate = new Date();
    maxDate.setDate(maxDate.getDate() + %(max_days)d);
    scheduleBuilder.add({
        name: "%(encounter_name)s",
        encounterType: "%(encounter_name)s",
        earliestDate: scheduledDate,
        maxDate: maxDate,
    });
    return scheduleBuilder.getAll();
};""",
    "decision": """\
'use strict';
({params, imports}) => {
    const programEncounter = params.entity;
    const decisions = { encounterDecisions: [], enrolmentDecisions: [], registrationDecisions: [] };
    // Add decision logic here based on observations
    // Example: const value = programEncounter.getObservationValue("%(concept_name)s");
    return decisions;
};""",
    "validation": """\
'use strict';
({params, imports}) => {
    const entity = params.entity;
    const validationResults = [];
    // Add validation checks
    // Example:
    // const value = entity.getObservationValue("%(concept_name)s");
    // if (value < %(min_value)s || value > %(max_value)s) {
    //     validationResults.push(imports.rulesConfig.RuleFactory.createValidationError(
    //         "%(concept_name)s must be between %(min_value)s and %(max_value)s"
    //     ));
    // }
    return validationResults;
};""",
    "eligibility": """\
'use strict';
({params, imports}) => {
    const entity = params.entity;
    // Return true if the entity is eligible, false otherwise
    return true;
};""",
    "summary": """\
'use strict';
({params, imports}) => {
    const enrolment = params.entity;
    const summaryItems = [];
    // Add summary items
    // Example:
    // summaryItems.push({
    //     name: "%(concept_name)s",
    //     value: enrolment.getObservationValue("%(concept_name)s"),
    // });
    return summaryItems;
};""",
    "worklist": """\
'use strict';
({params, imports}) => {
    const context = params.context;
    const worklist = new imports.rulesConfig.WorkLists(
        new imports.rulesConfig.WorkList("%(name)s")
    );
    return worklist;
};""",
    "checklist": """\
'use strict';
({params, imports}) => {
    const programEnrolment = params.entity;
    const checklistDetails = [];
    // Define checklist items
    return checklistDetails;
};""",
}


def _generate_rule_code(rule_type: str, params: dict[str, Any]) -> str:
    """Generate JavaScript rule code from a template and parameters."""
    template = _RULE_TEMPLATES.get(rule_type, "")
    if not template:
        return ""

    # Provide safe defaults for template parameters
    defaults: dict[str, Any] = {
        "schedule_days": params.get("schedule_days", 30),
        "max_days": params.get("max_days", 45),
        "encounter_name": params.get("encounter_name", "Follow-up"),
        "concept_name": params.get("concept_name", ""),
        "min_value": params.get("min_value", 0),
        "max_value": params.get("max_value", 100),
        "name": params.get("name", "Default"),
    }

    try:
        return template % defaults
    except (KeyError, TypeError):
        return template


# ---------------------------------------------------------------------------
# Static analysis
# ---------------------------------------------------------------------------

_REQUIRED_PATTERNS: dict[str, list[str]] = {
    "visitSchedule": [r"VisitScheduleBuilder", r"getAll\(\)"],
    "decision": [r"encounterDecisions", r"return\s+decisions"],
    "validation": [r"validationResults", r"return\s+validationResults"],
    "eligibility": [r"return\s+(true|false)"],
    "summary": [r"summaryItems", r"return\s+summaryItems"],
    "worklist": [r"WorkLists?", r"return\s+worklist"],
    "checklist": [r"checklistDetails", r"return\s+checklistDetails"],
}

_DISALLOWED_API_PATTERNS = [
    (r"\bfetch\s*\(", "Direct fetch() calls are not allowed in AVNI rules"),
    (r"\brequire\s*\(", "require() is not allowed in AVNI rules"),
    (r"\bimport\s+", "ES module imports are not allowed in AVNI rules"),
    (r"\beval\s*\(", "eval() is not allowed in AVNI rules"),
    (r"\bFunction\s*\(", "Function() constructor is not allowed in AVNI rules"),
    (r"process\.env", "process.env access is not allowed in AVNI rules"),
]


def _validate_rule_code(code: str, rule_type: str = "") -> dict[str, Any]:
    """
    Perform static analysis on rule code.

    Checks:
    - Bracket matching (parens, braces, brackets)
    - Required patterns for the rule type
    - Disallowed API usage
    """
    errors: list[str] = []
    warnings: list[str] = []

    if not code or not code.strip():
        return {
            "valid": False,
            "errors": ["Rule code is empty"],
            "warnings": [],
        }

    # Bracket matching
    stack: list[str] = []
    bracket_map = {")": "(", "}": "{", "]": "["}
    open_brackets = set(bracket_map.values())
    close_brackets = set(bracket_map.keys())

    for char in code:
        if char in open_brackets:
            stack.append(char)
        elif char in close_brackets:
            if not stack or stack[-1] != bracket_map[char]:
                errors.append(f"Mismatched bracket: unexpected '{char}'")
                break
            stack.pop()

    if stack:
        errors.append(f"Unclosed bracket(s): {''.join(stack)}")

    # Check 'use strict'
    if "'use strict'" not in code and '"use strict"' not in code:
        warnings.append("Missing 'use strict' directive")

    # Check arrow function wrapper
    if "({params, imports})" not in code and "({ params, imports })" not in code:
        warnings.append(
            "Missing standard AVNI rule function signature: ({params, imports}) => {}"
        )

    # Required patterns
    if rule_type and rule_type in _REQUIRED_PATTERNS:
        for pattern in _REQUIRED_PATTERNS[rule_type]:
            if not re.search(pattern, code):
                warnings.append(
                    f"Expected pattern not found for {rule_type} rule: {pattern}"
                )

    # Disallowed API usage
    for pattern, message in _DISALLOWED_API_PATTERNS:
        if re.search(pattern, code):
            errors.append(message)

    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "warnings": warnings,
    }


# ---------------------------------------------------------------------------
# Handlers
# ---------------------------------------------------------------------------


async def handle_generate_rule(request: Request) -> JSONResponse:
    """
    POST /rules/generate
    Body: {
        "rule_type": "visitSchedule",
        "params": {"schedule_days": 30, "max_days": 45, "encounter_name": "ANC"}
    }
    Generates JavaScript rule code for one of 7 supported rule types.
    """
    try:
        body = await request.json()
    except Exception:
        return JSONResponse({"error": "Invalid JSON body"}, status_code=400)

    rule_type = body.get("rule_type", "")
    params = body.get("params", {})

    if not rule_type:
        return JSONResponse({"error": "Missing 'rule_type'"}, status_code=400)
    if rule_type not in VALID_RULE_TYPES:
        return JSONResponse(
            {
                "error": f"Invalid rule_type '{rule_type}'. "
                f"Valid types: {VALID_RULE_TYPES}"
            },
            status_code=400,
        )
    if not isinstance(params, dict):
        return JSONResponse({"error": "'params' must be an object"}, status_code=400)

    try:
        code = _generate_rule_code(rule_type, params)

        # Validate the generated code
        validation = _validate_rule_code(code, rule_type)

        logger.info(
            "rules/generate: generated %s rule (%d chars)",
            rule_type,
            len(code),
        )
        return JSONResponse(
            {
                "ok": True,
                "rule_type": rule_type,
                "code": code,
                "validation": validation,
            }
        )

    except Exception as exc:
        logger.exception("rules/generate failed: %s", exc)
        return JSONResponse({"error": str(exc)}, status_code=500)


async def handle_validate_rule(request: Request) -> JSONResponse:
    """
    POST /rules/validate
    Body: { "code": "...", "rule_type": "visitSchedule" }
    Performs static analysis on rule code.
    """
    try:
        body = await request.json()
    except Exception:
        return JSONResponse({"error": "Invalid JSON body"}, status_code=400)

    code = body.get("code", "")
    rule_type = body.get("rule_type", "")

    if not code:
        return JSONResponse({"error": "Missing 'code'"}, status_code=400)
    if rule_type and rule_type not in VALID_RULE_TYPES:
        return JSONResponse(
            {
                "error": f"Invalid rule_type '{rule_type}'. "
                f"Valid types: {VALID_RULE_TYPES}"
            },
            status_code=400,
        )

    result = _validate_rule_code(code, rule_type)

    logger.info(
        "rules/validate: valid=%s errors=%d warnings=%d",
        result["valid"],
        len(result["errors"]),
        len(result["warnings"]),
    )
    return JSONResponse(
        {
            "ok": True,
            "valid": result["valid"],
            "errors": result["errors"],
            "warnings": result["warnings"],
            "error_count": len(result["errors"]),
            "warning_count": len(result["warnings"]),
        }
    )
