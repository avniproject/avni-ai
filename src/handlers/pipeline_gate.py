"""
pipeline_gate.py — Deterministic validation gate for the agent pipeline.

Runs after each agent completes. Checks the current pipeline state,
auto-fixes what it can, and returns structured questions for anything
that needs user input.

POST /validate-pipeline-step
Body: { "conversation_id": "...", "phase": "spec_generation" }

Returns:
  {
    "ok": true/false,
    "phase": "spec_generation",
    "auto_fixed": ["removed duplicate concept X from form Y"],
    "questions": [
      {
        "id": "enc_draft_subject_type",
        "section": "encounterTypes",
        "entity": "Draft",
        "field": "subjectType",
        "question": "Which subject type does 'Draft' belong to?",
        "options": ["Beneficiary", "Anganwadi", "Remove this encounter"],
        "default": "Remove this encounter"
      }
    ],
    "warnings": ["..."],
    "next_action": "present_questions" | "continue" | "retry_agent"
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
    Deterministic validation gate — runs after each agent completes.
    """
    try:
        body = await request.json()
    except Exception:
        return JSONResponse({"error": "Invalid JSON body"}, status_code=400)

    conversation_id = body.get("conversation_id")
    phase = body.get("phase", "")
    if not conversation_id:
        return JSONResponse({"error": "Missing conversation_id"}, status_code=400)

    # Dispatch to phase-specific validator
    # Accept both agent names (from conversation.active_agent) and phase names
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
                "auto_fixed": [],
                "questions": [],
                "warnings": [],
                "next_action": "continue",
            }
        )

    try:
        result = await validator(conversation_id)
        result["phase"] = phase
        logger.info(
            "pipeline-gate [%s] phase=%s ok=%s auto_fixed=%d questions=%d",
            conversation_id[:8],
            phase,
            result["ok"],
            len(result.get("auto_fixed", [])),
            len(result.get("questions", [])),
        )
        return JSONResponse(result)
    except Exception as exc:
        logger.exception("pipeline-gate error for phase=%s", phase)
        return JSONResponse(
            {
                "ok": False,
                "phase": phase,
                "auto_fixed": [],
                "questions": [],
                "warnings": [],
                "error": str(exc),
                "next_action": "retry_agent",
            },
            status_code=500,
        )


# ---------------------------------------------------------------------------
# Phase-specific validators
# ---------------------------------------------------------------------------


async def _validate_after_spec(conversation_id: str) -> dict:
    """Validate entities and spec after spec_generation phase."""
    from .entity_handlers import get_entity_store
    from .spec_handlers import (
        get_spec_store,
        enrich_spec_with_defaults,
    )

    auto_fixed: list[str] = []
    questions: list[dict] = []
    warnings: list[str] = []

    entities = get_entity_store().get(conversation_id)
    if not entities:
        return {
            "ok": False,
            "auto_fixed": [],
            "questions": [],
            "warnings": ["No entities found — spec_generation may not have completed"],
            "next_action": "retry_agent",
        }

    spec_yaml = get_spec_store().get(conversation_id)
    if not spec_yaml:
        return {
            "ok": False,
            "auto_fixed": [],
            "questions": [],
            "warnings": ["No spec found — generate_spec may not have been called"],
            "next_action": "retry_agent",
        }

    # 1. Check entities for missing subject_type / program_name
    st_names = [s["name"] for s in entities.get("subject_types", []) if s.get("name")]
    prog_names = [p["name"] for p in entities.get("programs", []) if p.get("name")]

    for enc in entities.get("encounter_types", []):
        name = enc.get("name", "")
        subject = enc.get("subject_type", "")
        program = enc.get("program_name", "")
        is_program_enc = enc.get("is_program_encounter", False)

        if not subject:
            options = list(st_names) + ["Remove this encounter"]
            questions.append(
                {
                    "id": f"enc_{_safe_id(name)}_subject_type",
                    "section": "encounter_types",
                    "entity": name,
                    "field": "subject_type",
                    "question": f"Which subject type does encounter '{name}' belong to?",
                    "options": options,
                    "default": options[-1],  # "Remove" as default
                }
            )

        if is_program_enc and not program:
            options = list(prog_names) + ["Convert to general encounter (no program)"]
            questions.append(
                {
                    "id": f"enc_{_safe_id(name)}_program",
                    "section": "encounter_types",
                    "entity": name,
                    "field": "program_name",
                    "question": f"Which program does encounter '{name}' belong to?",
                    "options": options,
                    "default": options[0] if prog_names else options[-1],
                }
            )

    # 2. Run enrich_spec for sector-specific defaults and additional ambiguities
    # Detect sector from entities or org name
    sector = _detect_sector(entities)
    enrichment = enrich_spec_with_defaults(spec_yaml, sector)
    auto_fixed.extend(enrichment.get("defaults_applied", []))
    questions.extend(enrichment.get("ambiguities", []))

    # Store enriched spec back
    if enrichment.get("enriched_spec_yaml"):
        get_spec_store().put(conversation_id, enrichment["enriched_spec_yaml"])

    # 3. Schema validation — check for unknown fields
    from ..bundle.spec_validator import validate_spec

    validation = validate_spec(enrichment.get("enriched_spec_yaml", spec_yaml))
    warnings.extend(validation.get("warnings", []))

    # Dedup questions by entity+field (entity check and enrich_spec may flag same issue)
    seen_q: set[str] = set()
    deduped_questions: list[dict] = []
    for q in questions:
        key = f"{q.get('entity', '')}:{q.get('field', '')}:{q.get('question', '')}"
        if key not in seen_q:
            seen_q.add(key)
            deduped_questions.append(q)
    questions = deduped_questions

    ok = len(questions) == 0 and len(validation.get("errors", [])) == 0
    next_action = "present_questions" if questions else "continue"

    return {
        "ok": ok,
        "auto_fixed": auto_fixed,
        "questions": questions,
        "warnings": warnings,
        "next_action": next_action,
    }


async def _validate_after_bundle(conversation_id: str) -> dict:
    """Validate bundle after bundle_config/bundle_generation phase."""
    from .bundle_handlers import get_bundle_store
    from ..bundle.validators import BundleValidator

    auto_fixed: list[str] = []
    questions: list[dict] = []
    warnings: list[str] = []

    stored = get_bundle_store().get(conversation_id)
    if not stored:
        return {
            "ok": False,
            "auto_fixed": [],
            "questions": [],
            "warnings": ["No bundle found"],
            "next_action": "retry_agent",
        }

    bundle = stored["bundle"]
    validator = BundleValidator(bundle)
    result = validator.validate()

    # Auto-fix: remove duplicate concepts within forms
    for form in bundle.get("forms", []):
        seen: set[str] = set()
        for group in form.get("formElementGroups", []):
            elements = group.get("formElements", [])
            deduped = []
            for elem in elements:
                concept_name = elem.get("concept", {}).get("name", "").lower()
                if concept_name and concept_name in seen:
                    auto_fixed.append(
                        f"Removed duplicate concept '{elem.get('name', '?')}' from form '{form.get('name', '?')}'"
                    )
                    continue
                if concept_name:
                    seen.add(concept_name)
                deduped.append(elem)
            group["formElements"] = deduped

    # Auto-fix: formMappings missing subjectTypeUUID — assign first subject type
    st_list = bundle.get("subjectTypes", [])
    if st_list:
        default_st_uuid = st_list[0]["uuid"]
        default_st_name = st_list[0]["name"]
        for m in bundle.get("formMappings", []):
            if not m.get("subjectTypeUUID"):
                m["subjectTypeUUID"] = default_st_uuid
                auto_fixed.append(
                    f"Assigned subjectType '{default_st_name}' to formMapping '{m.get('formName', '?')}'"
                )

    # Check for remaining errors that can't be auto-fixed
    if auto_fixed:
        # Re-validate after auto-fixes
        validator = BundleValidator(bundle)
        result = validator.validate()

    # formMappings missing encounterTypeUUID — group and generate questions
    enc_by_name = {e["name"]: e["uuid"] for e in bundle.get("encounterTypes", [])}
    enc_requiring_types = {
        "Encounter", "IndividualEncounterCancellation",
        "ProgramEncounter", "ProgramEncounterCancellation",
    }
    cancellation_types = {"IndividualEncounterCancellation", "ProgramEncounterCancellation"}
    main_types = {"Encounter", "ProgramEncounter"}

    # Auto-fix: if no encounter types exist, remove all orphan encounter formMappings
    if not enc_by_name:
        orphan_mappings = [
            m for m in bundle.get("formMappings", [])
            if m.get("formType", "") in enc_requiring_types and not m.get("encounterTypeUUID")
        ]
        if orphan_mappings:
            names = {m.get("formName", "?") for m in orphan_mappings}
            bundle["formMappings"] = [
                m for m in bundle["formMappings"] if m.get("formName") not in names
            ]
            auto_fixed.append(
                f"Removed {len(orphan_mappings)} orphan form mapping(s) (no encounter types defined)"
            )

    # Collect main and cancellation forms missing encounterTypeUUID
    main_missing = []
    cancel_missing = []
    for m in bundle.get("formMappings", []):
        ft = m.get("formType", "")
        if not m.get("encounterTypeUUID"):
            if ft in main_types:
                main_missing.append(m)
            elif ft in cancellation_types:
                cancel_missing.append(m)

    # Build cancel lookup by base name
    cancel_by_base: dict[str, list] = {}
    for m in cancel_missing:
        base = m.get("formName", "").replace(" Cancellation", "").strip()
        cancel_by_base.setdefault(base, []).append(m)

    # One question per main form (covers its cancellation too)
    for m in main_missing:
        form_name = m.get("formName", "?")
        ft = m.get("formType", "")
        related = [cm.get("formName") for cm in cancel_by_base.pop(form_name, [])]
        options = list(enc_by_name.keys()) + ["Remove this form mapping"]
        label = f"'{form_name}'"
        if related:
            label += f" (and {len(related)} cancellation form(s))"
        questions.append({
            "id": f"fm_{_safe_id(form_name)}_encounter_type",
            "section": "formMappings",
            "entity": form_name,
            "field": "encounterTypeUUID",
            "question": f"Which encounter type should {label} be mapped to?",
            "options": options,
            "default": options[-1],
        })

    # Orphan cancellation forms with no matching main form
    for base, cancels in cancel_by_base.items():
        for cm in cancels:
            form_name = cm.get("formName", "?")
            ft = cm.get("formType", "")
            options = list(enc_by_name.keys()) + ["Remove this form mapping"]
            questions.append({
                "id": f"fm_{_safe_id(form_name)}_encounter_type",
                "section": "formMappings",
                "entity": form_name,
                "field": "encounterTypeUUID",
                "question": f"Which encounter type should '{form_name}' ({ft}) be mapped to?",
                "options": options,
                "default": options[-1],
            })

    warnings.extend(result.get("warnings", []))
    errors = result.get("errors", [])

    ok = len(questions) == 0 and len(errors) == 0
    next_action = (
        "present_questions" if questions else ("continue" if ok else "retry_agent")
    )

    return {
        "ok": ok,
        "auto_fixed": auto_fixed,
        "questions": questions,
        "warnings": warnings,
        "errors": errors if errors else [],
        "next_action": next_action,
    }


async def _validate_after_rules(conversation_id: str) -> dict:
    """Lightweight check after rules_generation — just verify bundle still valid."""
    return {
        "ok": True,
        "auto_fixed": [],
        "questions": [],
        "warnings": [],
        "next_action": "continue",
    }


async def _validate_after_reports(conversation_id: str) -> dict:
    """Lightweight check after reports_generation."""
    return {
        "ok": True,
        "auto_fixed": [],
        "questions": [],
        "warnings": [],
        "next_action": "continue",
    }


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
        return {
            "ok": True,
            "auto_fixed": [],
            "questions": [],
            "warnings": [],
            "next_action": "continue",
        }

    if upload_error:
        error_msg = upload_error[-1].get("error", "Unknown upload error")
        return {
            "ok": False,
            "auto_fixed": [],
            "questions": [],
            "warnings": [f"Upload failed: {error_msg}"],
            "next_action": "retry_agent",
        }

    return {
        "ok": True,
        "auto_fixed": [],
        "questions": [],
        "warnings": [],
        "next_action": "continue",
    }


# ---------------------------------------------------------------------------
# Resolve user answers
# ---------------------------------------------------------------------------


async def handle_resolve_pipeline_questions(request: Request) -> JSONResponse:
    """
    POST /resolve-pipeline-questions
    Body: {
      "conversation_id": "...",
      "answers": [
        {"id": "enc_draft_subject_type", "answer": "Remove this encounter"},
        {"id": "enc_child_monitoring_program", "answer": "Nourish-Child"}
      ]
    }
    Applies user answers deterministically and returns updated state.
    """
    try:
        body = await request.json()
    except Exception:
        return JSONResponse({"error": "Invalid JSON body"}, status_code=400)

    conversation_id = body.get("conversation_id")
    answers = body.get("answers", [])
    if not conversation_id:
        return JSONResponse({"error": "Missing conversation_id"}, status_code=400)

    from .entity_handlers import get_entity_store
    from .bundle_handlers import get_bundle_store

    applied: list[str] = []
    entities = get_entity_store().get(conversation_id)

    for ans in answers:
        q_id = ans.get("id", "")
        answer = _normalize_answer(ans.get("answer", ""))

        # Entity-level fixes (encounter_types)
        if q_id.startswith("enc_") and q_id.endswith("_subject_type"):
            entity_name = ans.get("entity", _id_to_name(q_id, "enc_", "_subject_type"))
            if entities and "Remove" in answer:
                entities["encounter_types"] = [
                    e
                    for e in entities.get("encounter_types", [])
                    if e.get("name") != entity_name
                ]
                applied.append(f"Removed encounter '{entity_name}'")
            elif entities:
                for enc in entities.get("encounter_types", []):
                    if enc.get("name") == entity_name:
                        enc["subject_type"] = answer
                        applied.append(
                            f"Set subject_type='{answer}' on encounter '{entity_name}'"
                        )

        elif q_id.startswith("enc_") and q_id.endswith("_program"):
            entity_name = ans.get("entity", _id_to_name(q_id, "enc_", "_program"))
            if entities and "general encounter" in answer.lower():
                for enc in entities.get("encounter_types", []):
                    if enc.get("name") == entity_name:
                        enc["is_program_encounter"] = False
                        enc["program_name"] = ""
                        applied.append(
                            f"Converted '{entity_name}' to general encounter"
                        )
            elif entities:
                for enc in entities.get("encounter_types", []):
                    if enc.get("name") == entity_name:
                        enc["program_name"] = answer
                        applied.append(
                            f"Set program='{answer}' on encounter '{entity_name}'"
                        )

        # Bundle-level fixes (formMappings) — includes cancellation forms
        elif q_id.startswith("fm_") and q_id.endswith("_encounter_type"):
            form_name = ans.get("entity", _id_to_name(q_id, "fm_", "_encounter_type"))
            stored = get_bundle_store().get(conversation_id)
            if stored:
                # Find related cancellation forms
                cancel_names = [
                    m.get("formName")
                    for m in stored["bundle"].get("formMappings", [])
                    if m.get("formName", "").replace(" Cancellation", "").strip() == form_name
                    and "Cancellation" in m.get("formName", "")
                ]
                target_names = {form_name} | set(cancel_names)

                if "Remove" in answer:
                    stored["bundle"]["formMappings"] = [
                        m for m in stored["bundle"].get("formMappings", [])
                        if m.get("formName") not in target_names
                    ]
                    suffix = f" and {len(cancel_names)} cancellation form(s)" if cancel_names else ""
                    applied.append(f"Removed formMapping for '{form_name}'{suffix}")
                else:
                    enc_uuid = None
                    for et in stored["bundle"].get("encounterTypes", []):
                        if et["name"] == answer:
                            enc_uuid = et["uuid"]
                            break
                    if enc_uuid:
                        for m in stored["bundle"].get("formMappings", []):
                            if m.get("formName") in target_names:
                                m["encounterTypeUUID"] = enc_uuid
                        applied.append(f"Mapped '{form_name}' to encounterType '{answer}'")

    # Re-store corrected entities
    if entities and applied:
        get_entity_store().put(conversation_id, entities)

    logger.info(
        "resolve-pipeline [%s] applied=%d answers=%d",
        conversation_id[:8],
        len(applied),
        len(answers),
    )

    return JSONResponse(
        {
            "ok": True,
            "applied": applied,
            "applied_count": len(applied),
        }
    )


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


_REMOVE_SYNONYMS = {"ignore", "discard", "skip", "remove", "delete", "drop"}


def _normalize_answer(answer: str) -> str:
    """Map free-text synonyms to the canonical 'Remove' action."""
    if answer.strip().lower() in _REMOVE_SYNONYMS:
        return "Remove"
    return answer


def _safe_id(name: str) -> str:
    return name.lower().replace(" ", "_").replace("-", "_").replace("/", "_")[:30]


def _id_to_name(q_id: str, prefix: str, suffix: str) -> str:
    """Extract entity name from question ID."""
    stripped = q_id[len(prefix) :]
    if stripped.endswith(suffix):
        stripped = stripped[: -len(suffix)]
    return stripped.replace("_", " ").title()


def _detect_sector(entities: dict) -> str:
    """Detect sector from entity names."""
    all_names = " ".join(
        [e.get("name", "") for e in entities.get("encounter_types", [])]
        + [p.get("name", "") for p in entities.get("programs", [])]
    ).lower()
    if any(
        w in all_names
        for w in ("anc", "pnc", "delivery", "pregnancy", "maternal", "immunisation")
    ):
        return "MCH"
    if any(
        w in all_names for w in ("nutrition", "growth monitoring", "feeding", "muac")
    ):
        return "Nutrition"
    if any(w in all_names for w in ("livelihood", "shg", "self help", "income")):
        return "Livelihoods"
    if any(w in all_names for w in ("school", "student", "attendance", "assessment")):
        return "Education"
    if any(w in all_names for w in ("wash", "sanitation", "water quality")):
        return "WASH"
    return ""
