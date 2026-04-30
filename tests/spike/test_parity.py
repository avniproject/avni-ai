"""Parity tests — same scripted behaviour produces same transcript shape on
both runners. Guards us from accidentally diverging the two paths during
prompt edits or refactors."""

from __future__ import annotations

from typing import Any
from unittest.mock import MagicMock

import pytest

from src.orchestrators.claude_agent.managed_runner import ManagedRunner
from src.orchestrators.claude_agent.sdk_runner import SDKRunner

from .conftest import RecordingClarificationHandler, make_event


# Helpers reused from the per-runner tests (kept inline so the parity test is
# self-contained and obvious to read).


def _managed_event_stream(events: list[dict]) -> MagicMock:
    cm = MagicMock()
    cm.__enter__ = MagicMock(return_value=iter(events))
    cm.__exit__ = MagicMock(return_value=False)
    return cm


def _sdk_query_stub(messages: list[Any]):
    """Yields `messages` on the first call only — phases 2+ get an empty stream
    so per-message metrics aren't double-counted across phases."""
    state = {"calls": 0}

    async def gen(*, prompt: str, options: Any = None, transport: Any = None):
        state["calls"] += 1
        if state["calls"] == 1:
            for m in messages:
                yield m

    return gen


def _no_auth(monkeypatch, module_path: str) -> None:
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

    monkeypatch.setattr(f"{module_path}.httpx.AsyncClient", _Client)


@pytest.mark.asyncio
async def test_assistant_text_normalises_identically(
    base_config, recording_handler, fake_anthropic_client, monkeypatch
):
    """Both runners must produce the same `{type:assistant_text, content:...}`
    transcript entry for a "hello" assistant message."""
    _no_auth(monkeypatch, "src.orchestrators.claude_agent.managed_runner")
    _no_auth(monkeypatch, "src.orchestrators.claude_agent.sdk_runner")

    # Managed: feed an assistant.message.delta event.
    fake_anthropic_client.beta.sessions.events.stream.return_value = (
        _managed_event_stream(
            [make_event("assistant.message.delta", delta={"text": "hello"})]
        )
    )
    managed = ManagedRunner(anthropic_client=fake_anthropic_client)
    rec_managed = await managed.run(base_config, recording_handler)

    # SDK: feed an AssistantMessage(TextBlock).
    from claude_agent_sdk import AssistantMessage, TextBlock

    msg = AssistantMessage(content=[TextBlock(text="hello")], model="claude-opus-4-5")
    sdk = SDKRunner(query_fn=_sdk_query_stub([msg]))
    rec_sdk = await sdk.run(base_config, RecordingClarificationHandler())

    managed_texts = [e for e in rec_managed.transcript if e["type"] == "assistant_text"]
    sdk_texts = [e for e in rec_sdk.transcript if e["type"] == "assistant_text"]
    assert [e["content"] for e in managed_texts] == ["hello"]
    assert [e["content"] for e in sdk_texts] == ["hello"]


@pytest.mark.asyncio
async def test_clarification_count_matches(
    base_config, fake_anthropic_client, monkeypatch
):
    """Same scripted user clarification → same `clarifications_asked` metric
    on both runners."""
    _no_auth(monkeypatch, "src.orchestrators.claude_agent.managed_runner")
    _no_auth(monkeypatch, "src.orchestrators.claude_agent.sdk_runner")

    handler_managed = RecordingClarificationHandler(answers=["Individual"])
    handler_sdk = RecordingClarificationHandler(answers=["Individual"])

    # Managed-side path: tool_use(AskUserQuestion).
    fake_anthropic_client.beta.sessions.events.stream.return_value = (
        _managed_event_stream(
            [
                make_event(
                    "tool_use",
                    tool_name="AskUserQuestion",
                    input={
                        "question": "Subject type?",
                        "options": ["Individual", "Household"],
                    },
                )
            ]
        )
    )
    managed = ManagedRunner(anthropic_client=fake_anthropic_client)
    rec_m = await managed.run(base_config, handler_managed)

    # SDK-side path: invoke can_use_tool callback directly with the same
    # tool input. Build options first.
    sdk = SDKRunner(query_fn=_sdk_query_stub([]))
    from src.orchestrators.claude_agent.contracts import AgentMetrics

    sdk_metrics = AgentMetrics(runner="sdk")
    from src.orchestrators.claude_agent.agent_definition import SPEC_AGENT

    options = sdk._build_options(SPEC_AGENT, base_config, handler_sdk, sdk_metrics)
    await options.can_use_tool(
        "AskUserQuestion",
        {"question": "Subject type?", "options": ["Individual", "Household"]},
        MagicMock(),
    )
    assert rec_m.metrics.clarifications_asked == 1
    assert sdk_metrics.clarifications_asked == 1


@pytest.mark.asyncio
async def test_both_runners_label_themselves(
    base_config, recording_handler, fake_anthropic_client, monkeypatch
):
    _no_auth(monkeypatch, "src.orchestrators.claude_agent.managed_runner")
    _no_auth(monkeypatch, "src.orchestrators.claude_agent.sdk_runner")
    rec_m = await ManagedRunner(anthropic_client=fake_anthropic_client).run(
        base_config, recording_handler
    )
    rec_s = await SDKRunner(query_fn=_sdk_query_stub([])).run(
        base_config, RecordingClarificationHandler()
    )
    assert rec_m.metrics.runner == "managed"
    assert rec_s.metrics.runner == "sdk"
