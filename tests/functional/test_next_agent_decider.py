"""Unit tests for the Next Agent Decider code node in the Dify workflow.

Extracts the Python code from the YAML and verifies its routing decisions
against the scenarios we hit in production traces:
  - classifier picks 'done' → loop exits (regression from stuck_classifier.json)
  - targeted mode → exit
  - ask_user / error intent → exit
  - gate user_input_needed → exit
  - gate errors under retry cap → continue
  - gate errors at retry cap → exit
  - happy path (applied_fix + gate ok) → continue so classifier can advance
"""

from __future__ import annotations


import pytest
import yaml


@pytest.fixture(scope="module")
def nad_main():
    """Parse the Dify YAML, extract the Next Agent Decider's code, and return
    its `main` function. Uses exec in a fresh namespace."""
    path = "dify/Avni [Staging] Sub-Agentic Assistant.yml"
    with open(path) as f:
        doc = yaml.safe_load(f)
    nodes = doc["workflow"]["graph"]["nodes"]
    nad = next(
        n for n in nodes if n.get("data", {}).get("title") == "Next Agent Decider"
    )
    ns: dict = {}
    exec(nad["data"]["code"], ns)  # noqa: S102
    return ns["main"]


def _call(nad, **overrides):
    """Call NAD with all 7 inputs, defaults sane for 'happy path advance'."""
    kwargs = {
        "active_agent": "",
        "workflow_mode": "generic",
        "agent_output": "",
        "agent_memory": "",
        "last_gate_status": "ok",
        "agent_structured": "",
        "classifier_pick": "",
    }
    kwargs.update(overrides)
    return nad(**kwargs)


# ---------------------------------------------------------------------------
# Regression: classifier picks 'done' must exit the loop
# ---------------------------------------------------------------------------


def test_classifier_done_exits_loop(nad_main):
    """stuck_classifier.json regression: 10 iterations of 'done' because NAD
    ignored classifier_pick. After the fix, 'done' → loop_done=True."""
    r = _call(
        nad_main,
        classifier_pick="done",
        active_agent="bundle_config",
        agent_structured='{"intent":"phase_complete"}',
    )
    assert r["loop_done"] is True
    assert "done" in r["reason"].lower()


def test_classifier_done_even_with_dirty_state(nad_main):
    """Even if phase-like signals suggest continuation, classifier 'done' wins."""
    r = _call(
        nad_main,
        classifier_pick="done",
        agent_structured='{"intent":"applied_fix"}',
        active_agent="spec",
    )
    assert r["loop_done"] is True


# ---------------------------------------------------------------------------
# Happy path: agent succeeded, classifier will decide next iteration
# ---------------------------------------------------------------------------


def test_agent_applied_fix_continues(nad_main):
    """Spec/bundle_config finished with applied_fix + gate ok → loop continues
    so classifier can advance (or pick 'done' on next iteration)."""
    r = _call(
        nad_main,
        classifier_pick="spec",
        active_agent="spec",
        agent_structured='{"intent":"applied_fix"}',
        last_gate_status="ok",
    )
    assert r["loop_done"] is False
    assert r["next_agent"] == ""


# ---------------------------------------------------------------------------
# Early exits
# ---------------------------------------------------------------------------


def test_targeted_mode_always_exits(nad_main):
    r = _call(nad_main, workflow_mode="targeted", classifier_pick="spec")
    assert r["loop_done"] is True


def test_ask_user_intent_exits(nad_main):
    r = _call(
        nad_main,
        classifier_pick="spec",
        active_agent="spec",
        agent_structured='{"intent":"ask_user"}',
    )
    assert r["loop_done"] is True
    assert "ask_user" in r["reason"]


def test_error_intent_exits(nad_main):
    r = _call(
        nad_main,
        classifier_pick="bundle_config",
        active_agent="bundle_config",
        agent_structured='{"intent":"error"}',
    )
    assert r["loop_done"] is True


def test_gate_user_input_needed_exits(nad_main):
    r = _call(
        nad_main,
        classifier_pick="spec",
        active_agent="spec",
        last_gate_status="user_input_needed",
    )
    assert r["loop_done"] is True


# ---------------------------------------------------------------------------
# Gate retries
# ---------------------------------------------------------------------------


def test_gate_errors_under_retry_cap_continues(nad_main):
    r = _call(
        nad_main,
        classifier_pick="spec",
        active_agent="spec",
        last_gate_status="errors",
        agent_memory="[spec] ran once\n---\n[gate-ran:spec]",
    )
    assert r["loop_done"] is False
    assert "classifier will pick retry agent" in r["reason"]


def test_gate_errors_over_retry_cap_exits(nad_main):
    memory = "\n".join([f"[gate-ran:spec] try {i}" for i in range(4)])
    r = _call(
        nad_main,
        classifier_pick="spec",
        active_agent="spec",
        last_gate_status="errors",
        agent_memory=memory,
    )
    assert r["loop_done"] is True
    assert "persist after" in r["reason"]


# ---------------------------------------------------------------------------
# classifier_pick precedence
# ---------------------------------------------------------------------------


def test_classifier_done_beats_gate_errors(nad_main):
    """If classifier chose done, even a gate error shouldn't force a retry —
    there's nothing to retry because no agent was routed to."""
    r = _call(
        nad_main,
        classifier_pick="done",
        last_gate_status="errors",
    )
    assert r["loop_done"] is True


def test_classifier_done_beats_intent_applied_fix(nad_main):
    r = _call(
        nad_main,
        classifier_pick="done",
        agent_structured='{"intent":"applied_fix"}',
    )
    assert r["loop_done"] is True
