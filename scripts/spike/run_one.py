"""
Single end-to-end run, headless. Drives the CLI in non-interactive mode and
appends the run record to a runs/ directory. Used by `compare_runs.py` to
build the comparison matrix.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--runner", choices=("managed", "sdk"), default="managed")
    p.add_argument("--doc", action="append", required=True, dest="docs")
    p.add_argument("--org-name", required=True)
    p.add_argument("--mcp-url", default="http://localhost:8023/mcp")
    p.add_argument("--out-dir", default="runs", type=Path)
    p.add_argument(
        "--label",
        default="",
        help="Optional label appended to the output filename.",
    )
    return p


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    args.out_dir.mkdir(exist_ok=True, parents=True)

    ts = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    label = f"-{args.label}" if args.label else ""
    out = args.out_dir / f"run-{args.runner}-{ts}{label}.json"

    cmd = [
        sys.executable,
        "-m",
        "src.orchestrators.claude_agent.cli",
        "--runner",
        args.runner,
        "--mcp-url",
        args.mcp_url,
        "--org-name",
        args.org_name,
        "--non-interactive",
        "-v",
        "--out",
        str(out),
    ]
    for d in args.docs:
        cmd.extend(["--doc", d])

    proc = subprocess.run(cmd, cwd=REPO_ROOT, check=False)
    if proc.returncode != 0:
        print(f"run failed (exit {proc.returncode}); record at {out}")
    else:
        # Pretty-print summary of metrics for quick inspection.
        try:
            data = json.loads(out.read_text())
            metrics = data.get("metrics", {})
            print(json.dumps(metrics, indent=2))
        except Exception as e:  # noqa: BLE001
            print(f"could not read metrics: {e}")
    return proc.returncode


if __name__ == "__main__":
    sys.exit(main())
