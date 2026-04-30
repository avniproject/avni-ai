"""Unit tests for managed_runner — drives a fully-mocked Anthropic client."""

from __future__ import annotations

from dataclasses import replace
from unittest.mock import MagicMock

import pytest

from src.orchestrators.claude_agent.contracts import (
    SpikeError,
)
from src.orchestrators.claude_agent.managed_runner import (
    BETA_HEADER,
    ManagedRunner,
    _attr,
    _extract_text_delta,
)

from .conftest import RecordingClarificationHandler, make_event


# --------------------------------------------------------------------------- helpers


def _make_event_stream(events: list[dict]) -> MagicMock:
    """Build a mock context manager that yields the given events once."""
    cm = MagicMock()
    cm.__enter__ = MagicMock(return_value=iter(events))
    cm.__exit__ = MagicMock(return_value=False)
    return cm


# --------------------------------------------------------------------------- helpers


class TestAttrHelper:
    def test_reads_object_attribute(self):
        o = MagicMock(spec=["name"])
        o.name = "x"
        assert _attr(o, "name") == "x"

    def test_reads_dict_key(self):
        assert _attr({"foo": "bar"}, "foo") == "bar"

    def test_returns_none_for_missing(self):
        assert _attr({}, "x") is None
        assert _attr(object(), "missing") is None


class TestExtractTextDelta:
    def test_dict_delta(self):
        assert _extract_text_delta({"delta": {"text": "hello"}}) == "hello"

    def test_attr_delta(self):
        ev = MagicMock()
        ev.delta = MagicMock()
        ev.delta.text = "hi"
        assert _extract_text_delta(ev) == "hi"

    def test_no_delta(self):
        assert _extract_text_delta({}) == ""


# --------------------------------------------------------------------------- run()


@pytest.mark.asyncio
async def test_run_rejects_empty_api_key(base_config, recording_handler):
    cfg = replace(base_config, anthropic_api_key="")
    runner = ManagedRunner(anthropic_client=MagicMock())
    record = await runner.run(cfg, recording_handler)
    assert record.metrics.final_status == "failed"
    assert record.metrics.error and "anthropic_api_key" in record.metrics.error


@pytest.mark.asyncio
async def test_run_rejects_empty_mcp_url(base_config, recording_handler):
    cfg = replace(base_config, avni_mcp_url="")
    runner = ManagedRunner(anthropic_client=MagicMock())
    record = await runner.run(cfg, recording_handler)
    assert record.metrics.final_status == "failed"
    assert "avni_mcp_url" in (record.metrics.error or "")


@pytest.mark.asyncio
async def test_happy_path_records_lifecycle(
    base_config, fake_anthropic_client, recording_handler
):
    """Empty event stream + idle status → run completes Spec then Review and
    tears down both phases' managed resources. Error phase is skipped because
    `inject_failure=False`, `upload_task_id=""`, and Review's empty transcript
    classifies as neither approve nor revise."""
    cfg = base_config
    runner = ManagedRunner(anthropic_client=fake_anthropic_client)
    record = await runner.run(cfg, recording_handler)
    assert record.metrics.final_status == "completed"
    # Lifecycle: spec + review = 2 of each (no error phase).
    assert fake_anthropic_client.beta.agents.create.call_count == 2
    assert fake_anthropic_client.beta.environments.create.call_count == 2
    assert fake_anthropic_client.beta.sessions.create.call_count == 2
    # Cleanup happened for both.
    assert fake_anthropic_client.beta.sessions.delete.call_count == 2
    assert fake_anthropic_client.beta.environments.delete.call_count == 2
    assert fake_anthropic_client.beta.agents.archive.call_count == 2
    # Phases were recorded.
    assert record.metrics.phases_run == ["spec", "review"]


@pytest.mark.asyncio
async def test_beta_header_threaded_through_every_call(
    base_config, fake_anthropic_client, recording_handler
):
    """The beta header is the most fragile cross-cutting concern — once we
    get this right we should never regress it."""
    runner = ManagedRunner(anthropic_client=fake_anthropic_client)
    await runner.run(base_config, recording_handler)
    for call in (
        fake_anthropic_client.beta.agents.create,
        fake_anthropic_client.beta.environments.create,
        fake_anthropic_client.beta.sessions.create,
        fake_anthropic_client.beta.sessions.events.send,
    ):
        # Each was called at least once with betas=[BETA_HEADER]
        kwargs = call.call_args.kwargs
        assert "betas" in kwargs, f"{call} missing betas"
        assert BETA_HEADER in kwargs["betas"], f"{call} wrong beta header"


@pytest.mark.asyncio
async def test_uploads_each_scoping_doc_and_mounts(
    base_config, fake_anthropic_client, recording_handler, tmp_path
):
    p1 = tmp_path / "Yenepoya_SRS.xlsx"
    p1.write_bytes(b"PK\x03\x04")  # bare zip header — content irrelevant
    p2 = tmp_path / "extra.pdf"
    p2.write_bytes(b"%PDF-1.4")
    cfg = replace(base_config, scoping_doc_paths=(str(p1), str(p2)))
    fake_anthropic_client.beta.files.upload.side_effect = [
        MagicMock(id="file_1"),
        MagicMock(id="file_2"),
    ]
    runner = ManagedRunner(anthropic_client=fake_anthropic_client)
    await runner.run(cfg, recording_handler)
    assert fake_anthropic_client.beta.files.upload.call_count == 2
    # Files are mounted only on the Spec phase's session (call index 0);
    # the Review phase creates a session with no resources.
    spec_session_kwargs = (
        fake_anthropic_client.beta.sessions.create.call_args_list[0].kwargs
    )
    assert spec_session_kwargs["resources"] == [
        {
            "type": "file",
            "file_id": "file_1",
            "mount_path": "/workspace/Yenepoya_SRS.xlsx",
        },
        {"type": "file", "file_id": "file_2", "mount_path": "/workspace/extra.pdf"},
    ]
    review_session_kwargs = (
        fake_anthropic_client.beta.sessions.create.call_args_list[1].kwargs
    )
    assert review_session_kwargs["resources"] == []


@pytest.mark.asyncio
async def test_missing_scoping_file_raises(
    base_config, fake_anthropic_client, recording_handler
):
    cfg = replace(base_config, scoping_doc_paths=("/no/such/file.xlsx",))
    runner = ManagedRunner(anthropic_client=fake_anthropic_client)
    record = await runner.run(cfg, recording_handler)
    assert record.metrics.final_status == "failed"
    assert "scoping doc not found" in (record.metrics.error or "")


# --------------------------------------------------------------------------- events


@pytest.mark.asyncio
async def test_handles_assistant_text_delta_into_transcript(
    base_config, fake_anthropic_client, recording_handler
):
    fake_anthropic_client.beta.sessions.events.stream.return_value = _make_event_stream(
        [
            make_event("assistant.message.delta", delta={"text": "hello"}),
            make_event("assistant.message.delta", delta={"text": " world"}),
        ]
    )
    runner = ManagedRunner(anthropic_client=fake_anthropic_client)
    record = await runner.run(base_config, recording_handler)
    texts = [e for e in record.transcript if e["type"] == "assistant_text"]
    assert [e["content"] for e in texts] == ["hello", " world"]


@pytest.mark.asyncio
async def test_tool_use_increments_tool_calls_metric(
    base_config, fake_anthropic_client, recording_handler
):
    fake_anthropic_client.beta.sessions.events.stream.return_value = _make_event_stream(
        [
            make_event("tool_use", tool_name="parse-srs-file", input={"a": 1}),
            make_event("tool_use", tool_name="validate-spec", input={}),
        ]
    )
    runner = ManagedRunner(anthropic_client=fake_anthropic_client)
    record = await runner.run(base_config, recording_handler)
    assert record.metrics.tool_calls == 2


@pytest.mark.asyncio
async def test_tool_result_is_error_increments_failures(
    base_config, fake_anthropic_client, recording_handler
):
    fake_anthropic_client.beta.sessions.events.stream.return_value = _make_event_stream(
        [
            make_event("tool_result", tool_use_id="t1", is_error=True, content="boom"),
        ]
    )
    runner = ManagedRunner(anthropic_client=fake_anthropic_client)
    record = await runner.run(base_config, recording_handler)
    assert record.metrics.tool_call_failures == 1


@pytest.mark.asyncio
async def test_usage_event_accumulates_tokens(
    base_config, fake_anthropic_client, recording_handler
):
    fake_anthropic_client.beta.sessions.events.stream.return_value = _make_event_stream(
        [
            make_event("usage", input_tokens=120, output_tokens=10),
            make_event("usage", input_tokens=80, output_tokens=5),
        ]
    )
    runner = ManagedRunner(anthropic_client=fake_anthropic_client)
    record = await runner.run(base_config, recording_handler)
    assert record.metrics.input_tokens == 200
    assert record.metrics.output_tokens == 15


@pytest.mark.asyncio
async def test_session_error_event_marks_failed(
    base_config, fake_anthropic_client, recording_handler
):
    fake_anthropic_client.beta.sessions.events.stream.return_value = _make_event_stream(
        [make_event("session.error", message="exec failed")]
    )
    runner = ManagedRunner(anthropic_client=fake_anthropic_client)
    record = await runner.run(base_config, recording_handler)
    assert record.metrics.final_status == "failed"
    assert "exec failed" in (record.metrics.error or "")


@pytest.mark.asyncio
async def test_unknown_event_recorded_but_not_fatal(
    base_config, fake_anthropic_client, recording_handler
):
    fake_anthropic_client.beta.sessions.events.stream.return_value = _make_event_stream(
        [make_event("future.api.surface", weird="data")]
    )
    runner = ManagedRunner(anthropic_client=fake_anthropic_client)
    record = await runner.run(base_config, recording_handler)
    assert record.metrics.final_status == "completed"
    assert any(e["type"] == "unknown" for e in record.transcript)


# --------------------------------------------------------------------------- ask user


@pytest.mark.asyncio
async def test_ask_user_question_round_trip(base_config, fake_anthropic_client):
    handler = RecordingClarificationHandler(answers=["Individual"])
    fake_anthropic_client.beta.sessions.events.stream.return_value = _make_event_stream(
        [
            make_event(
                "tool_use",
                tool_name="AskUserQuestion",
                input={
                    "question": "Which subject type does Encounter X belong to?",
                    "options": ["Individual", "Household"],
                    "context": "encounter_x has no program AND no subject_type",
                },
            )
        ]
    )
    runner = ManagedRunner(anthropic_client=fake_anthropic_client)
    record = await runner.run(base_config, handler)

    assert handler.requests, "handler not called"
    req = handler.requests[0]
    assert req.options == ("Individual", "Household")
    assert "subject type" in req.question.lower()

    # Metrics: the tool_use + clarification fire in the Spec phase only.
    # (Phase 2 sees an exhausted iterator → no events.)
    assert record.metrics.tool_calls == 1
    assert record.metrics.clarifications_asked == 1

    # The clarification answer was posted back into the Spec session via
    # sessions.events.send. We don't assert on call ordering vs. the Review
    # kickoff, just that a user.message containing the answer was sent at
    # some point.
    send_calls = fake_anthropic_client.beta.sessions.events.send.call_args_list
    answer_payloads = [
        call.kwargs["events"][0]["content"][0]["text"]
        for call in send_calls
        if call.kwargs["events"][0]["type"] == "user.message"
    ]
    assert "Individual" in answer_payloads


# --------------------------------------------------------------------------- auth


@pytest.mark.asyncio
async def test_auth_token_post_skipped_when_empty(
    base_config, fake_anthropic_client, recording_handler, monkeypatch
):
    """No HTTP call should be made when avni_auth_token is empty — keeps the
    fully-offline test path airtight."""
    called = {"n": 0}

    class _Client:
        def __init__(self, *a, **kw):
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, *a):
            return False

        async def post(self, *a, **kw):  # pragma: no cover  — not called
            called["n"] += 1
            raise AssertionError("no auth call expected when token is empty")

    monkeypatch.setattr(
        "src.orchestrators.claude_agent.managed_runner.httpx.AsyncClient", _Client
    )
    runner = ManagedRunner(anthropic_client=fake_anthropic_client)
    await runner.run(base_config, recording_handler)
    assert called["n"] == 0


@pytest.mark.asyncio
async def test_auth_token_posted_when_configured(
    base_config, fake_anthropic_client, recording_handler, monkeypatch
):
    """When a token is set we POST to /store-auth-token before doing anything
    else — and we never log the token value."""
    captured: dict = {}

    class _Resp:
        status_code = 200
        text = ""

    class _Client:
        def __init__(self, *a, **kw):
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, *a):
            return False

        async def post(self, url, json):
            captured["url"] = url
            captured["json"] = json
            return _Resp()

    monkeypatch.setattr(
        "src.orchestrators.claude_agent.managed_runner.httpx.AsyncClient", _Client
    )
    cfg = replace(
        base_config, avni_auth_token="secret-token", avni_mcp_url="http://h/mcp"
    )
    runner = ManagedRunner(anthropic_client=fake_anthropic_client)
    await runner.run(cfg, recording_handler)
    assert captured["url"].endswith("/store-auth-token")
    assert captured["json"]["auth_token"] == "secret-token"
    assert captured["json"]["conversation_id"]


@pytest.mark.asyncio
async def test_auth_post_failure_short_circuits(
    base_config, fake_anthropic_client, recording_handler, monkeypatch
):
    class _Resp:
        status_code = 500
        text = "boom"

    class _Client:
        def __init__(self, *a, **kw):
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, *a):
            return False

        async def post(self, url, json):
            return _Resp()

    monkeypatch.setattr(
        "src.orchestrators.claude_agent.managed_runner.httpx.AsyncClient", _Client
    )
    cfg = replace(base_config, avni_auth_token="x", avni_mcp_url="http://h/mcp")
    runner = ManagedRunner(anthropic_client=fake_anthropic_client)
    record = await runner.run(cfg, recording_handler)
    assert record.metrics.final_status == "failed"


# --------------------------------------------------------------------------- cleanup


@pytest.mark.asyncio
async def test_cleanup_swallows_exceptions(
    base_config, fake_anthropic_client, recording_handler
):
    """Teardown is best-effort: a failing delete must not mask the run's
    primary error or status."""
    fake_anthropic_client.beta.sessions.delete.side_effect = RuntimeError("nope")
    fake_anthropic_client.beta.environments.delete.side_effect = RuntimeError("nope")
    fake_anthropic_client.beta.agents.archive.side_effect = RuntimeError("nope")
    runner = ManagedRunner(anthropic_client=fake_anthropic_client)
    record = await runner.run(base_config, recording_handler)
    # Still completed despite cleanup throwing.
    assert record.metrics.final_status == "completed"


# --------------------------------------------------------------------------- error type


def test_spike_error_is_runtime_error():
    e = SpikeError("x")
    assert isinstance(e, RuntimeError)
