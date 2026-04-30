"""
Aggregate run records into the comparison matrix.

Reads every `runs/run-*.json`, groups by (runner, org), reports median + p95
on latency, mean tokens & cost, and counts of clarifications, retries, and
failures.

Output is the markdown table that lives in
docs/app_configurator/claude-managed-agents-spike-results.md.

This script is intentionally pure-Python with no extra deps so it runs in CI.
"""

from __future__ import annotations

import argparse
import json
import statistics
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

# Approximate prices per 1M tokens (USD). Update when Anthropic updates pricing.
PRICES = {
    "claude-opus-4-5": (15.0, 75.0),
    "claude-opus-4-6": (15.0, 75.0),
    "claude-opus-4-7": (15.0, 75.0),
    "claude-sonnet-4-5": (3.0, 15.0),
    "claude-sonnet-4-6": (3.0, 15.0),
    "claude-haiku-4-5": (1.0, 5.0),
}


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--runs-dir",
        type=Path,
        default=Path("runs"),
        help="Bulk mode: scan this dir for *.json run records.",
    )
    p.add_argument(
        "--managed",
        type=Path,
        default=None,
        help="Pair mode: path to a single managed-runner JSON record.",
    )
    p.add_argument(
        "--sdk",
        type=Path,
        default=None,
        help="Pair mode: path to a single sdk-runner JSON record.",
    )
    p.add_argument(
        "--out",
        type=Path,
        default=Path("docs/app_configurator/claude-managed-agents-spike-results.md"),
    )
    p.add_argument(
        "--print-only",
        action="store_true",
        help="Print the table to stdout instead of overwriting --out.",
    )
    return p


def _record_cost(record: dict[str, Any]) -> float:
    metrics = record.get("metrics", {})
    model = record.get("config", {}).get("model_default", "")
    in_p, out_p = PRICES.get(model, (0.0, 0.0))
    return (
        metrics.get("input_tokens", 0) / 1_000_000 * in_p
        + metrics.get("output_tokens", 0) / 1_000_000 * out_p
    )


def _summarise(records: list[dict[str, Any]]) -> dict[str, Any]:
    if not records:
        return {"runs": 0}
    # Compute deltas. Treat missing keys as None, but allow 0.0 for either
    # bound — tests use started_at=0 deliberately.
    latencies = []
    for r in records:
        m = r["metrics"]
        if m.get("finished_at") is not None and m.get("started_at") is not None:
            latencies.append(m["finished_at"] - m["started_at"])
    if not latencies:
        latencies = [0.0]
    completed = [r for r in records if r["metrics"]["final_status"] == "completed"]
    return {
        "runs": len(records),
        "completed": len(completed),
        "latency_p50_s": statistics.median(latencies),
        "latency_p95_s": statistics.quantiles(latencies, n=20)[-1]
        if len(latencies) >= 5
        else max(latencies),
        "mean_input_tokens": int(
            statistics.mean(r["metrics"]["input_tokens"] for r in records)
        ),
        "mean_output_tokens": int(
            statistics.mean(r["metrics"]["output_tokens"] for r in records)
        ),
        "mean_cost_usd": round(statistics.mean(_record_cost(r) for r in records), 4),
        "tool_calls_total": sum(r["metrics"]["tool_calls"] for r in records),
        "tool_failures_total": sum(r["metrics"]["tool_call_failures"] for r in records),
        "clarifications_total": sum(
            r["metrics"]["clarifications_asked"] for r in records
        ),
        "phases_run": _most_common_phases(records),
        "review_outcomes": _count_outcomes(records),
    }


def _most_common_phases(records: list[dict[str, Any]]) -> str:
    """Return the dominant Spec→Review→Error chain seen across runs.

    If runs disagree (some go all 3 phases, others stop at 2), the modal
    chain is reported. Empty string when no run recorded any phases.
    """
    chains = ["→".join(r["metrics"].get("phases_run", []) or []) for r in records]
    chains = [c for c in chains if c]
    if not chains:
        return ""
    return statistics.mode(chains)


def _count_outcomes(records: list[dict[str, Any]]) -> str:
    """Compact 'A: x, R: y, –: z' across runs for the review_outcome field."""
    counts = {"approve": 0, "revise": 0, "": 0}
    for r in records:
        counts[r["metrics"].get("review_outcome", "")] = counts.get(
            r["metrics"].get("review_outcome", ""), 0
        ) + 1
    return f"A:{counts['approve']} R:{counts['revise']} –:{counts['']}"


def _format_md(buckets: dict[str, dict[str, Any]]) -> str:
    headers = [
        "Runner",
        "Runs",
        "Done",
        "Latency p50 (s)",
        "Latency p95 (s)",
        "Mean tokens (in / out)",
        "Mean cost (USD)",
        "Tool calls (fail)",
        "Clarifications",
        "Phases",
        "Review (A/R/–)",
    ]
    lines = [
        "| " + " | ".join(headers) + " |",
        "|" + "|".join("---" for _ in headers) + "|",
    ]
    for runner, summary in sorted(buckets.items()):
        lines.append(
            "| "
            + " | ".join(
                [
                    runner,
                    str(summary["runs"]),
                    str(summary.get("completed", 0)),
                    f"{summary.get('latency_p50_s', 0):.2f}",
                    f"{summary.get('latency_p95_s', 0):.2f}",
                    f"{summary.get('mean_input_tokens', 0)} / {summary.get('mean_output_tokens', 0)}",
                    f"${summary.get('mean_cost_usd', 0):.4f}",
                    f"{summary.get('tool_calls_total', 0)} ({summary.get('tool_failures_total', 0)})",
                    str(summary.get("clarifications_total", 0)),
                    summary.get("phases_run", "") or "–",
                    summary.get("review_outcomes", "–"),
                ]
            )
            + " |"
        )
    return "\n".join(lines)


def _load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)

    buckets: dict[str, list[dict[str, Any]]] = defaultdict(list)

    if args.managed or args.sdk:
        # Pair mode — for the spike, this is the common case after one
        # managed + one sdk run.
        for path in (args.managed, args.sdk):
            if path is None:
                continue
            if not path.exists():
                print(f"missing run file: {path}", file=sys.stderr)
                return 1
            data = _load(path)
            runner = data.get("metrics", {}).get("runner", "unknown")
            buckets[runner].append(data)
    else:
        if not args.runs_dir.exists():
            print(f"runs dir not found: {args.runs_dir}", file=sys.stderr)
            return 1
        # Scan both `run-*.json` (legacy naming) and any other *.json so the
        # runbook's `runs/managed.json` / `runs/sdk.json` form also works.
        for path in sorted(args.runs_dir.glob("*.json")):
            try:
                data = _load(path)
            except json.JSONDecodeError as e:
                print(f"skip {path}: {e}", file=sys.stderr)
                continue
            runner = data.get("metrics", {}).get("runner", "unknown")
            buckets[runner].append(data)

    summaries = {runner: _summarise(records) for runner, records in buckets.items()}
    table = _format_md(summaries)

    if args.print_only or not args.out:
        print(table)
        return 0

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(
        "# Spike results — Claude Managed Agents\n\n"
        "_Auto-generated by `scripts/spike/compare_runs.py`._\n\n" + table + "\n"
    )
    print(f"wrote {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
