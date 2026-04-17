"""
pipeline_gate.py — Read-only validation gate for the agent pipeline.

Runs after each agent completes. Checks the current pipeline state and
returns a list of errors and warnings. Does NOT modify any state.
Agents read the gate output and decide how to fix issues.

POST /validate-pipeline-step
Body: { "conversation_id": "...", "phase": "spec" }

Returns:
  {
    "ok": true/false,
    "phase": "spec",
    "errors": ["Encounter 'Draft' has no subject_type — assign to a subject type or remove"],
    "warnings": ["..."],
    "next_action": "continue" | "fix_required" | "user_input_needed"
  }
"""

from __future__ import annotations

import logging

from starlette.requests import Request
from starlette.responses import JSONResponse

logger = logging.getLogger(__name__)


async def handle_validate_pipeline_step(request: Request) -> JSONResponse:
    """
    POST /validate-pipeline-step
    Read-only validation gate — checks state, never modifies it.
    """
    try:
        body = await request.json()
    except Exception:
        return JSONResponse({"error": "Invalid JSON body"}, status_code=400)

    conversation_id = body.get("conversation_id")
    phase = body.get("phase", "")
    if not conversation_id:
        return JSONResponse({"error": "Missing conversation_id"}, status_code=400)

    # Accept both agent names and phase names
    validators = {
        "spec": _validate_after_spec,
        "spec_generation": _validate_after_spec,
        "bundle_config": _validate_after_bundle,
        "bundle_generation": _validate_after_bundle,
        "rules": _validate_after_rules,
        "rules_generation": _validate_after_rules,
        "reports": _validate_after_reports,
        "reports_generation": _validate_after_reports,
        "inspect": _validate_after_inspection,
        "inspection": _validate_after_inspection,
    }

    validator = validators.get(phase)
    if not validator:
        return JSONResponse(
            {
                "ok": True,
                "phase": phase,
                "errors": [],
                "warnings": [],
                "next_action": "continue",
            }
        )

    try:
        result = await validator(conversation_id)
        result["phase"] = phase
        logger.info(
            "pipeline-gate [%s] phase=%s ok=%s errors=%d warnings=%d",
            conversation_id[:8],
            phase,
            result["ok"],
            len(result.get("errors", [])),
            len(result.get("warnings", [])),
        )
        return JSONResponse(result)
    except Exception as exc:
        logger.exception("pipeline-gate error for phase=%s", phase)
        return JSONResponse(
            {
                "ok": False,
                "phase": phase,
                "errors": [f"Gate internal error: {exc}"],
                "warnings": [],
                "next_action": "continue",
            },
            status_code=500,
        )


# ---------------------------------------------------------------------------
# Phase-specific validators — read-only, never modify state
# ---------------------------------------------------------------------------


async def _validate_after_spec(conversation_id: str) -> dict:
    """Validate entities and spec after spec_generation phase."""
    from .entity_handlers import get_entity_store
    from .spec_handlers import get_spec_store

    errors: list[str] = []
    warnings: list[str] = []

    entities = get_entity_store().get(conversation_id)
    if not entities:
        return {
            "ok": False,
            "errors": ["No entities found — spec_generation may not have completed"],
            "warnings": [],
            "next_action": "fix_required",
        }

    spec_yaml = get_spec_store().get(conversation_id)
    if not spec_yaml:
        return {
            "ok": False,
            "errors": ["No spec found — generate_spec may not have been called"],
            "warnings": [],
            "next_action": "fix_required",
        }

    # Check entities for missing required fields
    st_names = [s["name"] for s in entities.get("subject_types", []) if s.get("name")]
    prog_names = [p["name"] for p in entities.get("programs", []) if p.get("name")]

    for enc in entities.get("encounter_types", []):
        name = enc.get("name", "")
        subject = enc.get("subject_type", "")
        program = enc.get("program_name", "")
        is_program_enc = enc.get("is_program_encounter", False)

        if not subject:
            errors.append(
                f"Encounter '{name}' has no subject_type. "
                f"Available subject types: {st_names}. "
                f"Assign one or remove this encounter."
            )
        if is_program_enc and not program:
            errors.append(
                f"Program encounter '{name}' has no program_name. "
                f"Available programs: {prog_names}. "
                f"Assign one or convert to general encounter."
            )

    # Schema validation
    from ..bundle.spec_validator import validate_spec

    validation = validate_spec(spec_yaml)
    errors.extend(validation.get("errors", []))
    warnings.extend(validation.get("warnings", []))

    ok = len(errors) == 0
    next_action = "continue" if ok else "fix_required"
    return {
        "ok": ok,
        "errors": errors,
        "warnings": warnings,
        "next_action": next_action,
    }


async def _validate_after_bundle(conversation_id: str) -> dict:
    """Validate bundle after bundle_config/bundle_generation phase."""
    from .bundle_handlers import get_bundle_store
    from ..bundle.validators import BundleValidator

    errors: list[str] = []
    warnings: list[str] = []

    stored = get_bundle_store().get(conversation_id)
    if not stored:
        return {
            "ok": False,
            "errors": ["No bundle found — generate_bundle may not have been called"],
            "warnings": [],
            "next_action": "fix_required",
        }

    bundle = stored["bundle"]
    validator = BundleValidator(bundle)
    result = validator.validate()
    errors.extend(result.get("errors", []))
    warnings.extend(result.get("warnings", []))

    # Surface generator flags (auto-created/defaulted items) as warnings
    for flag in stored.get("flags", []):
        warnings.append(f"[AUTO-RESOLVED] {flag['reason']}")

    ok = len(errors) == 0
    next_action = "continue" if ok else "fix_required"
    return {
        "ok": ok,
        "errors": errors,
        "warnings": warnings,
        "next_action": next_action,
    }


async def _validate_after_rules(conversation_id: str) -> dict:
    """Lightweight check after rules_generation."""
    return {"ok": True, "errors": [], "warnings": [], "next_action": "continue"}


async def _validate_after_reports(conversation_id: str) -> dict:
    """Lightweight check after reports_generation."""
    return {"ok": True, "errors": [], "warnings": [], "next_action": "continue"}


async def _validate_after_inspection(conversation_id: str) -> dict:
    """Check upload status after inspection phase."""
    from .log_handlers import get_log_store

    entries = get_log_store().get(conversation_id)
    upload_success = any(
        e.get("phase") == "upload" and e.get("status") == "success" for e in entries
    )
    upload_error = [
        e for e in entries if e.get("phase") == "upload" and e.get("status") == "error"
    ]

    if upload_success:
        return {"ok": True, "errors": [], "warnings": [], "next_action": "continue"}

    if upload_error:
        error_msg = upload_error[-1].get("error", "Unknown upload error")
        action = upload_error[-1].get("action", "")
        full_error = f"{error_msg} {action}".lower()

        # Auth failures can't be fixed by any agent — stop the pipeline
        if "401" in full_error or "unauthorized" in full_error or "auth" in full_error:
            return {
                "ok": False,
                "errors": [
                    "Upload failed: authentication error (HTTP 401). "
                    "The auth token has expired or is invalid. "
                    "Please re-authenticate and retry."
                ],
                "warnings": [],
                "next_action": "user_input_needed",
            }

        return {
            "ok": False,
            "errors": [f"Upload failed: {error_msg}"],
            "warnings": [],
            "next_action": "fix_required",
        }

    return {"ok": True, "errors": [], "warnings": [], "next_action": "continue"}
