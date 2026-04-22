"""Emulate the Dify Question Classifier against real Haiku.

The classifier now reads its rubric + state from the `instruction` field
(singular) with `{{#conversation.X#}}` placeholders Dify interpolates at
node-run time. The classifier's query_variable_selector = sys.query — only
the user's raw message. This mirrors the production YAML shape exactly:
  sys.query                                     (input_text)
  conversation.phase_hint, active_agent, etc.  (substituted into instruction)

To test this faithfully, we:
  1. Pull the `instruction` text from the live YAML.
  2. Substitute {{#conversation.X#}} placeholders with test state.
  3. Send sys.query, categories, and the resolved instruction to Haiku in
     the exact Dify classifier prompt shape.

Requires ANTHROPIC_API_KEY. Skips otherwise.
"""

from __future__ import annotations

import json as _json
import os
import re

import pytest
import yaml

try:
    import anthropic
except ImportError:
    anthropic = None

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")

pytestmark = [
    pytest.mark.skipif(not ANTHROPIC_API_KEY, reason="No ANTHROPIC_API_KEY"),
    pytest.mark.skipif(anthropic is None, reason="anthropic SDK not installed"),
]


_CLASSES = [
    {"category_id": "1", "category_name": "spec"},
    {"category_id": "2", "category_name": "bundle_config"},
    {"category_id": "3", "category_name": "rules"},
    {"category_id": "4", "category_name": "reports"},
    {"category_id": "5", "category_name": "inspect"},
    {"category_id": "6", "category_name": "admin"},
    {"category_id": "7", "category_name": "done"},
]

_SYSTEM_PROMPT = """### Job Description
You are a text classification engine that analyzes text data and assigns categories based on user input or automatically determined categories.
### Task
Your task is to assign one categories ONLY to the input text and only one category may be assigned returned in the output. Additionally, you need to extract the key words from the text that are related to the classification.
### Format
The input text is in the variable input_text. Categories are specified as a category list with two filed category_id and category_name in the variable categories. Classification instructions may be included to improve the classification accuracy.
### Constraint
DO NOT include anything other than the JSON array in your response."""


def _load_classifier_instruction() -> str:
    """Read the live YAML's Question Classifier.instruction."""
    path = "dify/Avni [Staging] Sub-Agentic Assistant.yml"
    with open(path) as f:
        doc = yaml.safe_load(f)
    nodes = doc["workflow"]["graph"]["nodes"]
    qc = next(
        n for n in nodes if n.get("data", {}).get("title") == "Question Classifier"
    )
    return qc["data"]["instruction"]


def _resolve_vars(instruction: str, state: dict[str, str]) -> str:
    """Substitute {{#conversation.X#}} placeholders with test state values.
    Dify does this at node-run time; we mimic to test the resolved text."""

    def repl(m: re.Match) -> str:
        key = m.group(1)
        return str(state.get(key, ""))

    return re.sub(r"\{\{#conversation\.(\w+)#\}\}", repl, instruction)


def _call_classifier(user_query: str, state: dict[str, str]) -> dict:
    instruction = _resolve_vars(_load_classifier_instruction(), state)
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    user_msg = _json.dumps(
        {
            "input_text": [user_query],
            "categories": _CLASSES,
            "classification_instructions": [instruction],
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
    if "```" in text:
        text = (
            text.split("```json", 1)[-1]
            if "```json" in text
            else text.split("```", 1)[-1]
        )
        text = text.rsplit("```", 1)[0]
    parsed = _json.loads(text.strip())
    if isinstance(parsed, list):
        parsed = parsed[0] if parsed else {}
    return parsed


# ---------------------------------------------------------------------------
# Turn-start / lifecycle phases
# ---------------------------------------------------------------------------


def test_fresh_phase_routes_to_spec():
    pick = _call_classifier(
        user_query="Setup avni using scoping srs docs uploaded here",
        state={
            "phase_hint": "fresh",
            "active_agent": "",
            "agent_structured": "",
            "last_gate_status": "not_run",
            "turn_diff_summary": "No entities stored yet. User is starting a new configuration.",
            "agent_memory": "",
        },
    )
    assert pick.get("category_name") == "spec", pick


def test_pre_spec_routes_to_spec_for_enrich_dialog():
    """quick_exit.json regression: Parse SRS File stored entities but Spec
    Agent hasn't generated spec. Classifier MUST route to spec so
    enrich_spec can surface ambiguities before bundling."""
    pick = _call_classifier(
        user_query="Setup avni using scoping srs docs uploaded here",
        state={
            "phase_hint": "pre_spec",
            "active_agent": "",
            "agent_structured": "",
            "last_gate_status": "not_run",
            "turn_diff_summary": "Entities parsed (2 subject_types, 3 programs, 19 encounters, 28 forms). Spec not yet generated.",
            "agent_memory": "",
        },
    )
    assert pick.get("category_name") == "spec", pick


def test_pre_bundle_after_spec_routes_to_bundle_config():
    pick = _call_classifier(
        user_query="Q1:no, Q2:Yes, Q3:Yes",
        state={
            "phase_hint": "pre_bundle",
            "active_agent": "spec",
            "agent_structured": '{"intent":"applied_fix","target_phase":"bundle_generating"}',
            "last_gate_status": "ok",
            "turn_diff_summary": "Spec generated (2 subject_types, 3 programs, 19 encounters, 28 forms). No bundle yet.",
            "agent_memory": "[spec] applied 21 ambiguities",
        },
    )
    assert pick.get("category_name") == "bundle_config", pick


# ---------------------------------------------------------------------------
# RULE A: don't re-pick the agent that just succeeded
# ---------------------------------------------------------------------------


def test_post_spec_applied_fix_dirty_picks_bundle_config():
    """spec_agent_stuck.json regression. Was picking 'spec' 10x in a row."""
    pick = _call_classifier(
        user_query="Q1:no, Q2-Q3: Yes, Q4: Remove, Q5-Q20: Create a basic form, Q21: Add an basic enrolmentForm",
        state={
            "phase_hint": "dirty",
            "active_agent": "spec",
            "agent_structured": '{"intent":"applied_fix","target_phase":"bundle_generating"}',
            "last_gate_status": "ok",
            "turn_diff_summary": "Since last upload: programs (~3 modified), forms (+17 added)",
            "agent_memory": "[spec] applied_fix",
        },
    )
    assert pick.get("category_name") == "bundle_config", pick


def test_post_bundle_config_stable_picks_rules_via_L():
    """After bundle_config finishes on a first-time run, Rule L advances
    through the pipeline. Memory has [bundle_config] but not [rules] →
    classifier picks rules."""
    pick = _call_classifier(
        user_query="Setup avni using scoping srs docs uploaded here",
        state={
            "phase_hint": "stable",
            "active_agent": "bundle_config",
            "agent_structured": '{"intent":"phase_complete","target_phase":"completed"}',
            "last_gate_status": "ok",
            "turn_diff_summary": "No changes since last upload.",
            "agent_memory": "[spec] applied ambiguities\n---\n[bundle_config] bundle generated",
        },
    )
    assert pick.get("category_name") == "rules", pick


def test_full_pipeline_complete_memory_picks_done():
    """Memory shows spec → bundle_config → rules → reports → inspect all
    ran. Rule L: memory contains [inspect] → done."""
    pick = _call_classifier(
        user_query="Setup avni using scoping srs docs uploaded here",
        state={
            "phase_hint": "stable",
            "active_agent": "inspect",
            "agent_structured": '{"intent":"phase_complete","target_phase":"completed"}',
            "last_gate_status": "ok",
            "turn_diff_summary": "No changes since last upload.",
            "agent_memory": "[spec] ...\n---\n[bundle_config] ...\n---\n[rules] ...\n---\n[reports] ...\n---\n[inspect] UPLOAD_SUCCESS",
        },
    )
    assert pick.get("category_name") == "done", pick


# ---------------------------------------------------------------------------
# RULE B: gate errors retry same agent
# ---------------------------------------------------------------------------


def test_gate_errors_retries_same_agent():
    pick = _call_classifier(
        user_query="Q1:no",
        state={
            "phase_hint": "dirty",
            "active_agent": "bundle_config",
            "agent_structured": '{"intent":"applied_fix"}',
            "last_gate_status": "errors",
            "turn_diff_summary": "Since last upload: forms (+1 modified)",
            "agent_memory": "[gate-ran:bundle_config]",
        },
    )
    assert pick.get("category_name") == "bundle_config", pick


# ---------------------------------------------------------------------------
# User-intent rules (F/G/H/J)
# ---------------------------------------------------------------------------


def test_user_asks_for_report_card():
    pick = _call_classifier(
        user_query="Add a report card for active beneficiaries",
        state={
            "phase_hint": "stable",
            "active_agent": "",
            "agent_structured": "",
            "last_gate_status": "ok",
            "turn_diff_summary": "No changes since last upload.",
            "agent_memory": "",
        },
    )
    assert pick.get("category_name") == "reports", pick


# ---------------------------------------------------------------------------
# RULE L: pipeline progression through Rules → Reports → Inspect
# ---------------------------------------------------------------------------


def test_L_progression_rules_to_reports():
    pick = _call_classifier(
        user_query="Setup avni using scoping srs docs uploaded here",
        state={
            "phase_hint": "stable",
            "active_agent": "rules",
            "agent_structured": '{"intent":"phase_complete"}',
            "last_gate_status": "ok",
            "turn_diff_summary": "No changes since last upload.",
            "agent_memory": "[spec] ...\n---\n[bundle_config] ...\n---\n[rules] attached skip logic",
        },
    )
    assert pick.get("category_name") == "reports", pick


def test_L_progression_reports_to_inspect():
    pick = _call_classifier(
        user_query="Setup avni using scoping srs docs uploaded here",
        state={
            "phase_hint": "stable",
            "active_agent": "reports",
            "agent_structured": '{"intent":"phase_complete"}',
            "last_gate_status": "ok",
            "turn_diff_summary": "No changes since last upload.",
            "agent_memory": "[spec]...[bundle_config]...[rules]...[reports] 18 cards added",
        },
    )
    assert pick.get("category_name") == "inspect", pick


# ---------------------------------------------------------------------------
# RULE M: explicit upload-retry routing
# ---------------------------------------------------------------------------


def test_explicit_upload_request_routes_to_inspect():
    """User asks to re-upload after pipeline already completed. Rule M →
    inspect (which re-validates and uploads)."""
    pick = _call_classifier(
        user_query="upload the bundle again",
        state={
            "phase_hint": "stable",
            "active_agent": "inspect",
            "agent_structured": "",
            "last_gate_status": "ok",
            "turn_diff_summary": "No changes since last upload.",
            "agent_memory": "[spec]...[bundle_config]...[rules]...[reports]...[inspect] UPLOAD_SUCCESS",
        },
    )
    assert pick.get("category_name") == "inspect", pick


# ---------------------------------------------------------------------------
# RULE A2: Inspector re_route
# ---------------------------------------------------------------------------


def test_inspector_reroute_to_spec():
    pick = _call_classifier(
        user_query="",
        state={
            "phase_hint": "stable",
            "active_agent": "inspect",
            "agent_structured": '{"intent":"re_route","re_route_target":"spec","reason":"missing Enrich enrolmentForm"}',
            "last_gate_status": "ok",
            "turn_diff_summary": "No changes since last upload.",
            "agent_memory": "[inspect] found gap",
        },
    )
    assert pick.get("category_name") == "spec", pick


# ---------------------------------------------------------------------------
# RULE K: phase-driven default fallback
# ---------------------------------------------------------------------------


def test_pending_ambiguities_routes_to_spec_not_bundle_config():
    """2fa57e0e-039d-476f regression: user answered 21 ambiguities, classifier
    routed to bundle_config instead of spec. bundle_config then tried to apply
    answers itself via put_bundle_file, creating malformed cancellation forms.
    Rule A3 must fire: pending_ambiguities non-empty → spec."""
    pick = _call_classifier(
        user_query="Q1:no, Q2:yes, Q3:yes, Q4:Remove, Q5-Q20:Create a basic form, Q21:Add basic enrolmentForm",
        state={
            "phase_hint": "pre_bundle",  # spec exists from prior turn, no bundle yet
            "active_agent": "spec",  # set by Resume Awaiting Assigner
            "agent_structured": "",  # turn-start reset
            "last_gate_status": "user_input_needed",  # prior turn paused for user
            "pending_ambiguities": '[{"id":"prog_enrich_showGrowthChart"},{"id":"spec_st_school_unmapped"},{"id":"spec_enc_career_guidance_no_form"}]',
            "turn_diff_summary": "Spec generated. No bundle yet.",
            "agent_memory": "[spec] enrich_spec returned 21 ambiguities — presenting to user for resolution.",
        },
    )
    assert pick.get("category_name") == "spec", (
        f"Expected 'spec' per Rule A3 (user replying to ambiguities). Got {pick}. "
        f"If this routes to bundle_config, Bundle Config will incorrectly try to "
        f"apply the answers via put_bundle_file."
    )


def test_empty_pending_ambiguities_pre_bundle_routes_to_bundle_config():
    """Sanity check: pending_ambiguities is '[]' (cleared), phase=pre_bundle →
    still route to bundle_config (Rule E). Rule A3 must NOT trigger on empty."""
    pick = _call_classifier(
        user_query="continue",
        state={
            "phase_hint": "pre_bundle",
            "active_agent": "spec",
            "agent_structured": '{"intent":"applied_fix"}',
            "last_gate_status": "ok",
            "pending_ambiguities": "[]",  # cleared after apply_ambiguity_answers
            "turn_diff_summary": "Spec generated. No bundle yet.",
            "agent_memory": "[spec] applied 21 answers",
        },
    )
    assert pick.get("category_name") == "bundle_config", pick


def test_default_fallback_on_pre_spec_routes_to_spec():
    """Empty / ambiguous user query with phase=pre_spec should NOT silently
    drop into done. Rule K maps phase→agent so work advances."""
    pick = _call_classifier(
        user_query="",
        state={
            "phase_hint": "pre_spec",
            "active_agent": "",
            "agent_structured": "",
            "last_gate_status": "not_run",
            "turn_diff_summary": "Entities parsed. Spec not yet generated.",
            "agent_memory": "",
        },
    )
    assert pick.get("category_name") == "spec", pick


def test_stable_phase_with_approval_picks_done():
    pick = _call_classifier(
        user_query="looks good, proceed",
        state={
            "phase_hint": "stable",
            "active_agent": "bundle_config",
            "agent_structured": '{"intent":"applied_fix"}',
            "last_gate_status": "ok",
            "turn_diff_summary": "No changes since last upload.",
            "agent_memory": "[bundle_config] UPLOAD_SUCCESS",
        },
    )
    assert pick.get("category_name") == "done", pick
