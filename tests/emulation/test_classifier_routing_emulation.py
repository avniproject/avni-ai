"""Emulate the Dify Question Classifier against real Haiku to verify it
doesn't re-pick the same agent that just completed applied_fix.

Replays the exact scenario from spec_agent_stuck.json: user said
"Q1:no, Q2-Q3: Yes, Q4: Remove...", Spec Agent ran once successfully
with intent=applied_fix, phase_hint became 'dirty'. Before the fix,
Haiku kept picking 'spec' for 10+ iterations. After the fix (Diff
Parser composes a state-rich classifier_input, classifier reads that
instead of bare sys.query), Haiku must pick 'bundle_config'.

Requires ANTHROPIC_API_KEY. Skips otherwise.
"""

from __future__ import annotations

import os

import pytest

try:
    import anthropic
except ImportError:
    anthropic = None

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")

pytestmark = [
    pytest.mark.skipif(not ANTHROPIC_API_KEY, reason="No ANTHROPIC_API_KEY"),
    pytest.mark.skipif(anthropic is None, reason="anthropic SDK not installed"),
]


# The classifier node's "instruction" field text (must match the live YAML).
CLASSIFIER_INSTRUCTION = (
    "The input_text already contains user message + all routing state "
    "(phase_hint, last_active_agent, last_agent_intent, last_gate_status, "
    "diff_summary) plus the decision rules. Follow rules A-J in the input "
    "strictly. Do NOT infer from the user message alone — rule A is the "
    "single most important check and must be applied first. Return exactly "
    "one class name."
)

# The classes the classifier node lists (ids 1-7).
CLASSES = [
    {"category_id": "1", "category_name": "spec"},
    {"category_id": "2", "category_name": "bundle_config"},
    {"category_id": "3", "category_name": "rules"},
    {"category_id": "4", "category_name": "reports"},
    {"category_id": "5", "category_name": "inspect"},
    {"category_id": "6", "category_name": "admin"},
    {"category_id": "7", "category_name": "done"},
]

# Exact Dify question-classifier system prompt shape (mirrors the
# Dify plugin's serialization). We mimic this to get faithful behaviour.
_SYSTEM_PROMPT = """### Job Description
You are a text classification engine that analyzes text data and assigns categories based on user input or automatically determined categories.
### Task
Your task is to assign one categories ONLY to the input text and only one category may be assigned returned in the output. Additionally, you need to extract the key words from the text that are related to the classification.
### Format
The input text is in the variable input_text. Categories are specified as a category list with two filed category_id and category_name in the variable categories. Classification instructions may be included to improve the classification accuracy.
### Constraint
DO NOT include anything other than the JSON array in your response."""


def _call_classifier(classifier_input: str) -> dict:
    """Call Haiku with the exact Dify classifier prompt shape and return
    the parsed {category_id, category_name} pick."""
    import json as _json

    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

    user_msg = _json.dumps(
        {
            "input_text": [classifier_input],
            "categories": CLASSES,
            "classification_instructions": [CLASSIFIER_INSTRUCTION],
        }
    )

    resp = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=200,
        temperature=0,
        system=_SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_msg}],
    )
    text = resp.content[0].text
    # Strip ```json fences if present
    if "```" in text:
        # Extract content between first and last triple-backticks
        if "```json" in text:
            text = text.split("```json", 1)[-1]
        else:
            text = text.split("```", 1)[-1]
        text = text.rsplit("```", 1)[0]
    parsed = _json.loads(text.strip())
    # Dify's classifier shape: list of 1 classification, or dict directly.
    if isinstance(parsed, list):
        parsed = parsed[0] if parsed else {}
    return parsed


def _compose_classifier_input(
    user_query: str,
    phase_hint: str,
    active_agent: str,
    agent_structured: str,
    last_gate_status: str,
    summary: str,
) -> str:
    """Pure-Python reimplementation of the Diff Parser's composition step.
    Kept here so the emulator tests the SAME string the live workflow sends.
    If you change this text, update dify/Avni [Staging] Sub-Agentic Assistant.yml
    Diff Parser node in lockstep."""
    import json as _json

    last_intent = ""
    try:
        if agent_structured:
            struct = _json.loads(agent_structured) or {}
            last_intent = str(struct.get("intent") or "")
    except Exception:
        pass
    return (
        f"User message: {user_query}\n"
        f"phase_hint: {phase_hint}\n"
        f"last_active_agent: {active_agent or '<none>'}\n"
        f"last_agent_intent: {last_intent or '<none>'}\n"
        f"last_gate_status: {last_gate_status or 'not_run'}\n"
        f"diff_summary: {summary}\n\n"
        "Pick ONE class. Rules (first match wins):\n"
        "A. If last_agent_intent is applied_fix or phase_complete, DO NOT pick "
        "last_active_agent. Instead: phase_hint=dirty AND last_active_agent != "
        "bundle_config -> bundle_config; phase_hint=dirty AND last_active_agent "
        "== bundle_config -> done; phase_hint=stable -> done; phase_hint=pre_bundle "
        "-> bundle_config; phase_hint=pre_spec -> spec.\n"
        "B. last_gate_status=errors -> pick last_active_agent (retry).\n"
        "C. phase_hint=fresh -> spec.\n"
        "D. phase_hint=pre_spec (entities parsed, spec not generated) -> spec. "
        "Needed so enrich_spec can surface ambiguities before bundling.\n"
        "E. phase_hint=pre_bundle (spec exists, no bundle) -> bundle_config.\n"
        "F. User says add report card/dashboard/chart -> reports.\n"
        "G. User says skip logic/decision rule/validation -> rules.\n"
        "H. User asks about locations/users/catchments/delete-implementation -> admin.\n"
        "I. phase_hint=dirty + user asked for a structural change -> spec.\n"
        "J. phase_hint=stable + approval/thanks/continue -> done.\n"
        "K. Default -> done."
    )


# ---------------------------------------------------------------------------
# Test cases
# ---------------------------------------------------------------------------


def test_fresh_turn_picks_spec():
    """Iter 1 of a new conversation with an SRS upload — classifier should
    route to spec (nothing else exists yet)."""
    inp = _compose_classifier_input(
        user_query="Setup avni using scoping srs docs uploaded here",
        phase_hint="fresh",
        active_agent="",
        agent_structured="",
        last_gate_status="not_run",
        summary="No entities stored yet. User is starting a new configuration.",
    )
    pick = _call_classifier(inp)
    assert pick.get("category_name") == "spec", pick


def test_post_spec_applied_fix_dirty_picks_bundle_config():
    """Regression for spec_agent_stuck.json iter 2 — this is the case that
    was looping forever. After the fix, Haiku MUST pick bundle_config."""
    inp = _compose_classifier_input(
        user_query="Q1:no, Q2-Q3: Yes, Q4: Remove, Q5-Q20: Create a basic form, Q21: Add an basic enrolmentForm",
        phase_hint="dirty",
        active_agent="spec",
        agent_structured='{"intent":"applied_fix","target_phase":"bundle_generating","ambiguities":[],"applied_changes":[{"section":"programs","operation":"update","item_names":["Nourish - Pregnancy Enrollment","Nourish - Child Enrolment","Enrich"]}],"reason":"All 21 ambiguities resolved"}',
        last_gate_status="ok",
        summary="Since last upload: programs (~3 modified), forms (+17 added)",
    )
    pick = _call_classifier(inp)
    assert pick.get("category_name") == "bundle_config", (
        f"Expected bundle_config (rule A: spec just applied_fix → advance to "
        f"bundle_config on dirty). Got {pick}. "
        f"This is the exact loop that ate 11 spec iterations in spec_agent_stuck.json."
    )


def test_post_bundle_config_applied_fix_stable_picks_done():
    """After bundle_config reconciles successfully, baseline_entities is
    reset so phase_hint flips back to 'stable'. Classifier should pick
    'done' (rule A: stable + applied_fix → done)."""
    inp = _compose_classifier_input(
        user_query="Q1:no, Q2-Q3: Yes, Q4: Remove, Q5-Q20: Create a basic form, Q21: Add an basic enrolmentForm",
        phase_hint="stable",
        active_agent="bundle_config",
        agent_structured='{"intent":"applied_fix","target_phase":"completed"}',
        last_gate_status="ok",
        summary="No changes since last upload.",
    )
    pick = _call_classifier(inp)
    assert pick.get("category_name") == "done", pick


def test_stable_phase_with_approval_picks_done():
    """User says 'looks good' on a stable bundle → done."""
    inp = _compose_classifier_input(
        user_query="looks good, proceed",
        phase_hint="stable",
        active_agent="bundle_config",
        agent_structured='{"intent":"applied_fix"}',
        last_gate_status="ok",
        summary="No changes since last upload.",
    )
    pick = _call_classifier(inp)
    assert pick.get("category_name") == "done", pick


def test_gate_errors_retries_same_agent():
    """last_gate_status=errors → pick the retry agent."""
    inp = _compose_classifier_input(
        user_query="Q1:no, Q2-Q3: Yes",
        phase_hint="dirty",
        active_agent="bundle_config",
        agent_structured='{"intent":"applied_fix"}',
        last_gate_status="errors",
        summary="Since last upload: forms (+1 modified)",
    )
    pick = _call_classifier(inp)
    # Rule B should fire: pick last_active_agent (bundle_config).
    # (Rule A has higher priority but rule B explicitly handles the errors case.)
    assert pick.get("category_name") == "bundle_config", pick


def test_user_asks_for_report_card():
    """User explicitly asks for a dashboard card → reports, regardless of phase."""
    inp = _compose_classifier_input(
        user_query="Add a report card for active beneficiaries",
        phase_hint="stable",
        active_agent="",
        agent_structured="",
        last_gate_status="ok",
        summary="No changes since last upload.",
    )
    pick = _call_classifier(inp)
    assert pick.get("category_name") == "reports", pick


# ---------------------------------------------------------------------------
# Regression replays from stuck_classifier.json
# ---------------------------------------------------------------------------


def test_stuck_iter1_pre_spec_routes_to_spec():
    """quick_exit.json regression: Parse SRS File stored entities but the Spec
    Agent hasn't run yet (no spec generated). phase_hint=pre_spec. Classifier
    MUST route to spec so enrich_spec can surface ambiguities before bundling.
    Before the pre_spec split, this case was wrongly phase_hint=pre_bundle and
    the classifier jumped straight to bundle_config, skipping the entire
    ambiguity dialog."""
    inp = _compose_classifier_input(
        user_query="Setup avni using scoping srs docs uploaded here",
        phase_hint="pre_spec",
        active_agent="spec",  # residual; should NOT trigger RULE A
        agent_structured="",  # turn-start reset cleared it
        last_gate_status="not_run",
        summary="Entities parsed (2 subject_types, 3 programs, 19 encounters, 28 forms). Spec not yet generated.",
    )
    pick = _call_classifier(inp)
    assert pick.get("category_name") == "spec", pick


def test_pre_bundle_after_spec_routes_to_bundle_config():
    """After Spec Agent generates spec and resolves ambiguities, phase flips
    to pre_bundle. Classifier routes to bundle_config."""
    inp = _compose_classifier_input(
        user_query="Q1:no, Q2:Yes, Q3:Yes",
        phase_hint="pre_bundle",
        active_agent="spec",
        agent_structured='{"intent":"applied_fix","target_phase":"bundle_generating"}',
        last_gate_status="ok",
        summary="Spec generated (2 subject_types, 3 programs, 19 encounters, 28 forms). No bundle yet.",
    )
    pick = _call_classifier(inp)
    assert pick.get("category_name") == "bundle_config", pick


def test_stuck_iter2_after_bundle_config_phase_complete_picks_done():
    """stuck_classifier.json iter 2 exact replay: bundle_config just ran with
    intent=phase_complete, baseline reset → phase_hint=stable. Classifier
    must pick 'done'. (The bug was NOT here — classifier was already picking
    'done'; NAD wasn't honoring it, so the loop spun. This test guards
    against the classifier regressing.)"""
    inp = _compose_classifier_input(
        user_query="Setup avni using scoping srs docs uploaded here",
        phase_hint="stable",
        active_agent="",  # blanked by old Continue Loop bug — keeping inputs faithful
        agent_structured='{"intent":"phase_complete","target_phase":"completed"}',
        last_gate_status="ok",
        summary="No changes since last upload.",
    )
    pick = _call_classifier(inp)
    assert pick.get("category_name") == "done", pick


def test_stuck_iter2_with_active_agent_preserved_still_picks_done():
    """Post-fix (Continue Loop no longer blanks active_agent): the same iter 2
    state but with last_active_agent correctly preserved as 'bundle_config'.
    RULE A: stable + last_active_agent=bundle_config + phase_complete → done."""
    inp = _compose_classifier_input(
        user_query="Setup avni using scoping srs docs uploaded here",
        phase_hint="stable",
        active_agent="bundle_config",
        agent_structured='{"intent":"phase_complete","target_phase":"completed"}',
        last_gate_status="ok",
        summary="No changes since last upload.",
    )
    pick = _call_classifier(inp)
    assert pick.get("category_name") == "done", pick
