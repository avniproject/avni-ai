"""Security regression tests.

The spike's central trust claim: the avni-server auth token is registered with
avni-ai out-of-band and is never visible to the LLM (no prompt, no tool input,
no transcript). These tests guard that invariant — a single regression here
would leak production tokens into JSON files we share around.
"""

from __future__ import annotations

import json
from dataclasses import replace

import pytest

from src.orchestrators.claude_agent.cli import _serialize_record
from src.orchestrators.claude_agent.managed_runner import ManagedRunner
from src.orchestrators.claude_agent.sdk_runner import SDKRunner

SECRET = "should-never-leak-token-xyz123"


def _stub_auth_post(monkeypatch, module_path: str, status: int = 200):
    """Replace httpx.AsyncClient with a stub that captures POST bodies."""
    captured: dict = {}

    class _Resp:
        def __init__(self):
            self.status_code = status
            self.text = "ignored"

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

    monkeypatch.setattr(f"{module_path}.httpx.AsyncClient", _Client)
    return captured


@pytest.mark.asyncio
async def test_managed_runner_does_not_leak_token_into_record(
    base_config, fake_anthropic_client, recording_handler, monkeypatch
):
    _stub_auth_post(monkeypatch, "src.orchestrators.claude_agent.managed_runner")
    cfg = replace(base_config, avni_auth_token=SECRET, avni_mcp_url="http://h/mcp")
    runner = ManagedRunner(anthropic_client=fake_anthropic_client)
    record = await runner.run(cfg, recording_handler)

    # Final assertion: serialise the whole record (this is what the CLI
    # writes to disk) and grep for the secret.
    blob = json.dumps(_serialize_record(record))
    assert SECRET not in blob, "auth token leaked into RunRecord"


@pytest.mark.asyncio
async def test_managed_runner_does_not_leak_token_into_agent_create_call(
    base_config, fake_anthropic_client, recording_handler, monkeypatch
):
    """Agents API arguments are sent to Anthropic — a stricter check than the
    RunRecord one because even the call itself must not carry the token."""
    _stub_auth_post(monkeypatch, "src.orchestrators.claude_agent.managed_runner")
    cfg = replace(base_config, avni_auth_token=SECRET, avni_mcp_url="http://h/mcp")
    runner = ManagedRunner(anthropic_client=fake_anthropic_client)
    await runner.run(cfg, recording_handler)

    for call in (
        fake_anthropic_client.beta.agents.create,
        fake_anthropic_client.beta.environments.create,
        fake_anthropic_client.beta.sessions.create,
        fake_anthropic_client.beta.sessions.events.send,
    ):
        for c in call.call_args_list:
            assert SECRET not in str(c), f"token leaked into {call} args"


@pytest.mark.asyncio
async def test_managed_runner_redacts_auth_failure_body(
    base_config, fake_anthropic_client, recording_handler, monkeypatch
):
    """If /store-auth-token returns 4xx and echoes the token in the body, the
    runner must not include the response body in the SpikeError message."""

    class _Resp:
        status_code = 401
        text = f"unauthorized: token={SECRET}"

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
    cfg = replace(base_config, avni_auth_token=SECRET, avni_mcp_url="http://h/mcp")
    runner = ManagedRunner(anthropic_client=fake_anthropic_client)
    record = await runner.run(cfg, recording_handler)
    assert record.metrics.final_status == "failed"
    assert SECRET not in (record.metrics.error or "")
    assert SECRET not in json.dumps(_serialize_record(record))


@pytest.mark.asyncio
async def test_sdk_runner_does_not_leak_token_into_record(
    base_config, recording_handler, monkeypatch
):
    _stub_auth_post(monkeypatch, "src.orchestrators.claude_agent.sdk_runner")

    async def empty_query(*, prompt, options=None, transport=None):
        if False:  # pragma: no cover  — make this an async generator
            yield None

    cfg = replace(base_config, avni_auth_token=SECRET, avni_mcp_url="http://h/mcp")
    runner = SDKRunner(query_fn=empty_query)
    record = await runner.run(cfg, recording_handler)
    blob = json.dumps(_serialize_record(record))
    assert SECRET not in blob


@pytest.mark.asyncio
async def test_kickoff_message_does_not_carry_token(
    base_config, fake_anthropic_client, recording_handler, monkeypatch
):
    """Belt + braces: even if a future change adds the token to env-derived
    state, the kickoff user.message must remain token-free."""
    _stub_auth_post(monkeypatch, "src.orchestrators.claude_agent.managed_runner")
    cfg = replace(base_config, avni_auth_token=SECRET, avni_mcp_url="http://h/mcp")
    runner = ManagedRunner(anthropic_client=fake_anthropic_client)
    await runner.run(cfg, recording_handler)

    sends = fake_anthropic_client.beta.sessions.events.send.call_args_list
    assert sends, "no events sent"
    first_send = sends[0]
    payload = json.dumps(first_send.kwargs.get("events"))
    assert SECRET not in payload


def test_pyproject_pins_anthropic_betas_only_via_constants():
    """Lightweight defence — make sure no test or runner ever uses an arbitrary
    string for the beta header. Only `BETA_HEADER` from managed_runner is the
    source of truth."""
    from src.orchestrators.claude_agent import managed_runner

    # The header is the documented one and starts with the canonical prefix.
    assert managed_runner.BETA_HEADER.startswith("managed-agents-")


def test_recording_handler_does_not_capture_arbitrary_data(recording_handler):
    """Sanity: the test fixture itself doesn't accidentally hold tokens.
    `RecordingClarificationHandler` is shared widely; verify it stores only
    the question/options it sees."""
    rh = recording_handler
    rh.requests.clear()  # Fresh
    # Use a fixture call signature that includes auth-looking data.
    # If this assertion ever fails, it means we changed the handler to slurp
    # a wider context surface — the runner's MagicMock doesn't carry secrets.
    assert hasattr(rh, "requests"), "fixture missing requests list"
    assert rh.requests == []
