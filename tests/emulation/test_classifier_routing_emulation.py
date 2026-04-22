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
        text = text.split("```json", 1)[-1] if "```json" in text else text.split("```", 1)[-1]
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


def test_post_bundle_config_stable_picks_done():
    pick = _call_classifier(
        user_query="Setup avni using scoping srs docs uploaded here",
        state={
            "phase_hint": "stable",
            "active_agent": "bundle_config",
            "agent_structured": '{"intent":"phase_complete","target_phase":"completed"}',
            "last_gate_status": "ok",
            "turn_diff_summary": "No changes since last upload.",
            "agent_memory": "[spec]...[bundle_config] UPLOAD_SUCCESS",
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
