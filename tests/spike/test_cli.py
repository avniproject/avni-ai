"""CLI tests — argparse, serialisation, non-interactive answer routing."""

from __future__ import annotations

import json
from typing import Any
from unittest.mock import patch

import pytest

from src.orchestrators.claude_agent import cli as cli_mod
from src.orchestrators.claude_agent.contracts import (
    AgentMetrics,
    ClarificationRequest,
    OrchestratorConfig,
    RunRecord,
)


def test_argparse_defaults_to_managed():
    args = cli_mod._build_parser().parse_args(["--doc", "x.xlsx"])
    assert args.runner == "managed"
    assert args.docs == ["x.xlsx"]


def test_argparse_supports_multiple_docs():
    args = cli_mod._build_parser().parse_args(["--doc", "a.xlsx", "--doc", "b.pdf"])
    assert args.docs == ["a.xlsx", "b.pdf"]


def test_argparse_runner_choice_validates():
    with pytest.raises(SystemExit):
        cli_mod._build_parser().parse_args(["--runner", "frankenstein"])


@pytest.mark.asyncio
async def test_make_auto_handler_picks_first_option():
    h = cli_mod._make_auto_handler()
    resp = await h(ClarificationRequest(question="?", options=("opt-a", "opt-b")))
    assert resp.answer == "opt-a"


@pytest.mark.asyncio
async def test_make_auto_handler_skips_when_no_options():
    h = cli_mod._make_auto_handler()
    resp = await h(ClarificationRequest(question="describe it"))
    assert resp.answer == "auto-skip"


def test_serialize_record_round_trips_through_json(tmp_path):
    cfg = OrchestratorConfig(
        avni_mcp_url="http://x", avni_auth_token="", anthropic_api_key="k"
    )
    metrics = AgentMetrics(runner="managed", started_at=1.0, finished_at=2.0)
    record = RunRecord(config=cfg, metrics=metrics)
    record.transcript.append({"type": "assistant_text", "content": "hi"})
    payload = cli_mod._serialize_record(record)
    # Round-trips through json without TypeError.
    s = json.dumps(payload)
    parsed = json.loads(s)
    assert parsed["metrics"]["runner"] == "managed"
    assert parsed["transcript"][0]["content"] == "hi"


def test_main_requires_at_least_one_doc(capsys):
    """Invoking the CLI with no docs must SystemExit clearly."""
    with pytest.raises(SystemExit) as excinfo:
        cli_mod.main([])
    # argparse does its own SystemExit too — accept either path.
    assert excinfo.value.code != 0


def test_main_writes_record_to_out_path(tmp_path, monkeypatch):
    """Patch _run to return a known record; assert main writes it and exits 0."""
    out = tmp_path / "rec.json"
    cfg = OrchestratorConfig(
        avni_mcp_url="http://x", avni_auth_token="", anthropic_api_key="k"
    )
    metrics = AgentMetrics(
        runner="managed",
        started_at=10.0,
        finished_at=11.5,
        input_tokens=42,
        final_status="completed",
    )
    fake_record = RunRecord(config=cfg, metrics=metrics)

    async def _fake_run(args: Any) -> RunRecord:
        return fake_record

    monkeypatch.setattr(cli_mod, "_run", _fake_run)
    rc = cli_mod.main(["--doc", "any.xlsx", "--out", str(out), "--non-interactive"])
    assert rc == 0
    assert out.exists()
    parsed = json.loads(out.read_text())
    assert parsed["metrics"]["input_tokens"] == 42


def test_main_returns_nonzero_on_failed_status(tmp_path, monkeypatch):
    out = tmp_path / "rec.json"
    cfg = OrchestratorConfig(
        avni_mcp_url="http://x", avni_auth_token="", anthropic_api_key="k"
    )
    metrics = AgentMetrics(runner="sdk", final_status="failed", error="x")
    fake_record = RunRecord(config=cfg, metrics=metrics)

    async def _fake_run(args: Any) -> RunRecord:
        return fake_record

    monkeypatch.setattr(cli_mod, "_run", _fake_run)
    rc = cli_mod.main(["--doc", "x.xlsx", "--out", str(out), "--runner", "sdk"])
    assert rc != 0


def test_runner_env_default_picked_up(monkeypatch):
    monkeypatch.setenv("AVNI_ORCHESTRATOR", "sdk")
    args = cli_mod._build_parser().parse_args(["--doc", "x.xlsx"])
    assert args.runner == "sdk"


@patch("builtins.input", return_value="2")
@pytest.mark.asyncio
async def test_interactive_picks_numbered_option(_mock_input):
    """Numeric input maps to the option index; out-of-range falls through to
    free-text (which is not what we want, but the indexing must be 1-based)."""
    resp = await cli_mod._interactive_clarification(
        ClarificationRequest(question="pick", options=("alpha", "beta"))
    )
    assert resp.answer == "beta"


@patch("builtins.input", return_value="manual answer")
@pytest.mark.asyncio
async def test_interactive_free_text_fallback(_mock_input):
    resp = await cli_mod._interactive_clarification(
        ClarificationRequest(question="describe", options=())
    )
    assert resp.answer == "manual answer"
