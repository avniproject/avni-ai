"""Unit tests for sdk_runner — drives a stubbed `claude_agent_sdk.query`."""

from __future__ import annotations

from dataclasses import replace
from typing import Any
from unittest.mock import MagicMock

import pytest

from src.orchestrators.claude_agent.sdk_runner import SDKRunner

from .conftest import RecordingClarificationHandler


def _make_query_stub(messages: list[Any]) -> Any:
    """Return an `async def query(prompt, options=...)` that yields `messages`
    on the *first* call and an empty stream on subsequent calls.

    The runner now invokes `query()` once per phase (Spec, Review, optionally
    Error). Tests that want to assert on a single message stream care only
    about phase 1; phases 2+ should be silent so counters don't double up.
    Tests that want to script per-phase behavior can use `_make_phased_query_stub`.
    """
    state = {"calls": 0}

    async def _gen(*, prompt: str, options: Any = None, transport: Any = None):
        state["calls"] += 1
        if state["calls"] == 1:
            for m in messages:
                yield m
        # subsequent calls: empty stream

    return _gen


def _make_phased_query_stub(message_lists: list[list[Any]]) -> Any:
    """Return a query stub that yields a different message list per phase.

    Length of `message_lists` should match the number of phases the runner
    is expected to drive (2 for spec+review, 3 for spec+review+error).
    """
    state = {"calls": 0}

    async def _gen(*, prompt: str, options: Any = None, transport: Any = None):
        idx = state["calls"]
        state["calls"] += 1
        msgs = message_lists[idx] if idx < len(message_lists) else []
        for m in msgs:
            yield m

    return _gen


def _no_auth(monkeypatch):
    """Stub out the httpx auth-token POST so tests stay offline."""

    class _Client:
        def __init__(self, *a, **kw):
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, *a):
            return False

        async def post(self, *a, **kw):
            class _R:
                status_code = 200
                text = ""

            return _R()

    monkeypatch.setattr(
        "src.orchestrators.claude_agent.sdk_runner.httpx.AsyncClient", _Client
    )


@pytest.mark.asyncio
async def test_run_returns_completed_on_empty_stream(
    base_config, recording_handler, monkeypatch
):
    _no_auth(monkeypatch)
    runner = SDKRunner(query_fn=_make_query_stub([]))
    record = await runner.run(base_config, recording_handler)
    assert record.metrics.final_status == "completed"
    assert record.metrics.runner == "sdk"


@pytest.mark.asyncio
async def test_assistant_text_block_recorded(
    base_config, recording_handler, monkeypatch
):
    _no_auth(monkeypatch)
    from claude_agent_sdk import AssistantMessage, TextBlock

    msg = AssistantMessage(
        content=[TextBlock(text="hello world")], model="claude-opus-4-5"
    )
    runner = SDKRunner(query_fn=_make_query_stub([msg]))
    record = await runner.run(base_config, recording_handler)
    texts = [e for e in record.transcript if e["type"] == "assistant_text"]
    assert texts and texts[0]["content"] == "hello world"


@pytest.mark.asyncio
async def test_tool_use_block_recorded(base_config, recording_handler, monkeypatch):
    _no_auth(monkeypatch)
    from claude_agent_sdk import AssistantMessage, ToolUseBlock

    block = ToolUseBlock(
        id="t1", name="parse-srs-file", input={"file_path": "/workspace/x.xlsx"}
    )
    msg = AssistantMessage(content=[block], model="claude-opus-4-5")
    runner = SDKRunner(query_fn=_make_query_stub([msg]))
    record = await runner.run(base_config, recording_handler)
    tool_uses = [e for e in record.transcript if e["type"] == "tool_use"]
    assert tool_uses
    assert tool_uses[0]["tool_name"] == "parse-srs-file"


@pytest.mark.asyncio
async def test_tool_result_error_increments_failures(
    base_config, recording_handler, monkeypatch
):
    _no_auth(monkeypatch)
    from claude_agent_sdk import AssistantMessage, ToolResultBlock

    block = ToolResultBlock(tool_use_id="t1", content="boom", is_error=True)
    msg = AssistantMessage(content=[block], model="claude-opus-4-5")
    runner = SDKRunner(query_fn=_make_query_stub([msg]))
    record = await runner.run(base_config, recording_handler)
    assert record.metrics.tool_call_failures == 1


@pytest.mark.asyncio
async def test_result_message_accumulates_usage(
    base_config, recording_handler, monkeypatch
):
    _no_auth(monkeypatch)
    from claude_agent_sdk import ResultMessage

    msg = ResultMessage(
        subtype="success",
        duration_ms=120,
        duration_api_ms=110,
        is_error=False,
        num_turns=1,
        session_id="sess",
        total_cost_usd=0.0,
        usage={"input_tokens": 500, "output_tokens": 50},
    )
    runner = SDKRunner(query_fn=_make_query_stub([msg]))
    record = await runner.run(base_config, recording_handler)
    assert record.metrics.input_tokens == 500
    assert record.metrics.output_tokens == 50


@pytest.mark.asyncio
async def test_can_use_tool_routes_ask_user_question(base_config, monkeypatch):
    """Build the options the runner builds, then call its `can_use_tool`
    callback directly to verify AskUserQuestion routing without hitting the
    SDK loop."""
    _no_auth(monkeypatch)
    handler = RecordingClarificationHandler(answers=["Individual"])
    runner = SDKRunner(query_fn=_make_query_stub([]))

    # Reach into the options the runner would build and call the callback.
    from src.orchestrators.claude_agent.contracts import AgentMetrics

    metrics = AgentMetrics(runner="sdk")
    from src.orchestrators.claude_agent.agent_definition import SPEC_AGENT

    options = runner._build_options(SPEC_AGENT, base_config, handler, metrics)
    fn = options.can_use_tool
    assert fn is not None

    result = await fn(
        "AskUserQuestion",
        {"question": "?", "options": ["Individual", "Household"]},
        MagicMock(),
    )
    # Should be Allow with the chosen answer.
    assert getattr(result, "behavior", None) == "allow"
    assert getattr(result, "updated_input", {}) == {"answer": "Individual"}
    assert metrics.clarifications_asked == 1
    assert handler.requests[0].options == ("Individual", "Household")


@pytest.mark.asyncio
async def test_can_use_tool_allows_avni_mcp_tools(base_config, monkeypatch):
    _no_auth(monkeypatch)
    runner = SDKRunner(query_fn=_make_query_stub([]))
    from src.orchestrators.claude_agent.contracts import AgentMetrics

    metrics = AgentMetrics(runner="sdk")

    async def _h(req):
        from src.orchestrators.claude_agent.contracts import (
            ClarificationResponse,
        )

        return ClarificationResponse(answer="x")

    from src.orchestrators.claude_agent.agent_definition import SPEC_AGENT

    options = runner._build_options(SPEC_AGENT, base_config, _h, metrics)
    result = await options.can_use_tool("mcp__avni-ai__validate-spec", {}, MagicMock())
    assert getattr(result, "behavior", None) == "allow"


@pytest.mark.asyncio
async def test_can_use_tool_denies_unknown_tools(base_config, monkeypatch):
    _no_auth(monkeypatch)
    runner = SDKRunner(query_fn=_make_query_stub([]))
    from src.orchestrators.claude_agent.contracts import AgentMetrics

    metrics = AgentMetrics(runner="sdk")

    async def _h(req):
        from src.orchestrators.claude_agent.contracts import (
            ClarificationResponse,
        )

        return ClarificationResponse(answer="x")

    from src.orchestrators.claude_agent.agent_definition import SPEC_AGENT

    options = runner._build_options(SPEC_AGENT, base_config, _h, metrics)
    result = await options.can_use_tool("evil_tool", {}, MagicMock())
    assert getattr(result, "behavior", None) == "deny"


@pytest.mark.asyncio
async def test_run_short_circuits_on_empty_mcp_url(base_config, recording_handler):
    cfg = replace(base_config, avni_mcp_url="")
    runner = SDKRunner(query_fn=_make_query_stub([]))
    record = await runner.run(cfg, recording_handler)
    assert record.metrics.final_status == "failed"
