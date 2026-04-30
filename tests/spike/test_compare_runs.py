"""Tests for scripts/spike/compare_runs.py — pure-Python aggregation."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest

# Load the script as a module (it's not a package) so we can unit-test the
# helpers without going through subprocess.
_HERE = Path(__file__).resolve().parent.parent.parent
_SPEC_PATH = _HERE / "scripts" / "spike" / "compare_runs.py"
_spec = importlib.util.spec_from_file_location("compare_runs", _SPEC_PATH)
compare_runs = importlib.util.module_from_spec(_spec)  # type: ignore[arg-type]
_spec.loader.exec_module(compare_runs)  # type: ignore[union-attr]


def _record(
    runner: str,
    *,
    started: float,
    finished: float,
    input_tokens: int,
    output_tokens: int,
    tool_calls: int = 0,
    failures: int = 0,
    clarifications: int = 0,
    final: str = "completed",
    model: str = "claude-opus-4-5",
) -> dict:
    return {
        "config": {"model_default": model},
        "metrics": {
            "runner": runner,
            "started_at": started,
            "finished_at": finished,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "tool_calls": tool_calls,
            "tool_call_failures": failures,
            "clarifications_asked": clarifications,
            "final_status": final,
        },
    }


def test_record_cost_uses_price_table():
    rec = _record(
        "managed",
        started=0,
        finished=1,
        input_tokens=1_000_000,
        output_tokens=1_000_000,
        model="claude-opus-4-5",
    )
    cost = compare_runs._record_cost(rec)
    # Opus: $15/M input, $75/M output → $90 for one of each.
    assert cost == pytest.approx(90.0, rel=1e-6)


def test_record_cost_unknown_model_defaults_to_zero():
    rec = _record(
        "managed",
        started=0,
        finished=1,
        input_tokens=1000,
        output_tokens=1000,
        model="claude-mystery",
    )
    assert compare_runs._record_cost(rec) == 0.0


def test_summarise_aggregates_correctly():
    records = [
        _record(
            "managed", started=0, finished=10.0, input_tokens=100, output_tokens=10
        ),
        _record(
            "managed", started=0, finished=20.0, input_tokens=200, output_tokens=20
        ),
        _record(
            "managed", started=0, finished=15.0, input_tokens=300, output_tokens=30
        ),
    ]
    s = compare_runs._summarise(records)
    assert s["runs"] == 3
    assert s["completed"] == 3
    # Median of [10,20,15] = 15.
    assert s["latency_p50_s"] == 15.0
    assert s["mean_input_tokens"] == 200
    assert s["mean_output_tokens"] == 20


def test_summarise_handles_empty_records():
    assert compare_runs._summarise([]) == {"runs": 0}


def test_summarise_counts_only_completed():
    records = [
        _record("sdk", started=0, finished=5.0, input_tokens=10, output_tokens=1),
        _record(
            "sdk",
            started=0,
            finished=5.0,
            input_tokens=10,
            output_tokens=1,
            final="failed",
        ),
    ]
    s = compare_runs._summarise(records)
    assert s["runs"] == 2
    assert s["completed"] == 1


def test_format_md_renders_table_header():
    table = compare_runs._format_md({"managed": {"runs": 0}})
    assert "Runner" in table
    assert "Latency p50" in table
    # Header + separator + one data row
    assert table.count("\n") >= 2


def test_main_writes_results_file(tmp_path, monkeypatch):
    runs_dir = tmp_path / "runs"
    runs_dir.mkdir()
    out = tmp_path / "result.md"

    rec = _record("managed", started=0, finished=12.0, input_tokens=10, output_tokens=1)
    (runs_dir / "run-managed-001.json").write_text(json.dumps(rec))

    rc = compare_runs.main(["--runs-dir", str(runs_dir), "--out", str(out)])
    assert rc == 0
    text = out.read_text()
    assert "Runner" in text
    assert "managed" in text


def test_main_returns_error_on_missing_runs_dir(tmp_path):
    rc = compare_runs.main(
        ["--runs-dir", str(tmp_path / "nope"), "--out", str(tmp_path / "out.md")]
    )
    assert rc == 1
