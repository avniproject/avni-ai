"""
CLI entrypoint for the spike: `python -m src.orchestrators.claude_agent.cli`.

Single binary that can drive either runner. Picks Managed Agents by default
(per the issue) and falls back to the SDK if `--runner sdk` is passed or
`AVNI_ORCHESTRATOR=sdk`.

Output is a `RunRecord` serialised to JSON at the path given by `--out`,
suitable for consumption by `scripts/spike/compare_runs.py`.
"""

from __future__ import annotations

import argparse
import asyncio
import dataclasses
import json
import logging
import os
import sys
from pathlib import Path
from typing import Any
from uuid import uuid4

from .contracts import (
    ClarificationRequest,
    ClarificationResponse,
    OrchestratorConfig,
    RunRecord,
)

logger = logging.getLogger("avni.spike")


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="avni-spike",
        description="Run an Avni App Configurator spike via Claude Managed Agents or the Agent SDK.",
    )
    p.add_argument(
        "--runner",
        choices=("managed", "sdk"),
        default=os.environ.get("AVNI_ORCHESTRATOR", "managed"),
        help="Which runner to use (default: managed; env: AVNI_ORCHESTRATOR).",
    )
    p.add_argument(
        "--doc",
        action="append",
        dest="docs",
        default=[],
        metavar="PATH",
        help="Scoping document(s) to ingest. Repeatable.",
    )
    p.add_argument(
        "--org-name",
        default=os.environ.get("AVNI_ORG_NAME", ""),
        help="Org name threaded into /generate-spec.",
    )
    p.add_argument(
        "--mcp-url",
        default=os.environ.get("AVNI_MCP_SERVER_URL", "http://localhost:8023/mcp"),
        help="avni-ai FastMCP HTTP URL.",
    )
    p.add_argument(
        "--model",
        default=os.environ.get("AVNI_CLAUDE_MODEL", "claude-opus-4-5"),
        help="Claude model id.",
    )
    p.add_argument(
        "--out",
        default="run_record.json",
        help="Where to write the RunRecord JSON.",
    )
    p.add_argument(
        "--non-interactive",
        action="store_true",
        help="Auto-answer the first option for any clarification (CI / smoke).",
    )
    p.add_argument(
        "--inject-failure",
        action="store_true",
        help="Force the Error Agent path with a synthetic upload failure (M5).",
    )
    p.add_argument(
        "--upload-task-id",
        default="",
        help="Run the Error Agent against an existing avni-server upload task_id.",
    )
    p.add_argument(
        "--verbose", "-v", action="count", default=0, help="-v, -vv for log verbosity."
    )
    return p


def _setup_logging(verbosity: int) -> None:
    level = logging.WARNING
    if verbosity == 1:
        level = logging.INFO
    elif verbosity >= 2:
        level = logging.DEBUG
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )


async def _interactive_clarification(
    request: ClarificationRequest,
) -> ClarificationResponse:
    """Print the question, read a line from stdin. Blocks the loop, which is
    fine for a CLI."""
    print(f"\n[Avni AI] {request.question}")
    if request.context:
        print(f"  context: {request.context}")
    if request.options:
        for i, opt in enumerate(request.options, 1):
            print(f"  {i}) {opt}")
        prompt = f"Pick 1-{len(request.options)} (or type a free-text answer): "
    else:
        prompt = "Answer: "
    answer = await asyncio.to_thread(input, prompt)
    answer = answer.strip()
    if request.options and answer.isdigit():
        idx = int(answer) - 1
        if 0 <= idx < len(request.options):
            return ClarificationResponse(answer=request.options[idx])
    return ClarificationResponse(answer=answer)


def _make_auto_handler() -> Any:
    """Auto-pick option 1 when --non-interactive is set."""

    async def handler(request: ClarificationRequest) -> ClarificationResponse:
        if request.options:
            return ClarificationResponse(answer=request.options[0])
        return ClarificationResponse(answer="auto-skip")

    return handler


_REDACTED_FIELDS = frozenset({"avni_auth_token", "anthropic_api_key"})
"""Config fields that hold secrets and must never reach disk.

Keep these in sync with `OrchestratorConfig` whenever a new credential field is
added — and add a corresponding test in `tests/spike/test_security.py`.
"""


def _redact(obj: Any) -> Any:
    """Recursively replace _REDACTED_FIELDS values with a sentinel.

    `dataclasses.asdict` already recurses through nested dataclasses, so by the
    time `json.dumps`'s `default` callback would see a value it's already
    flattened to dicts/lists/strings — meaning a per-call redact in `default`
    only catches the outermost dataclass. Redacting after the fact, on the
    materialised dict, is the simplest invariant.
    """
    if isinstance(obj, dict):
        return {
            k: ("***REDACTED***" if k in _REDACTED_FIELDS and v else _redact(v))
            for k, v in obj.items()
        }
    if isinstance(obj, list):
        return [_redact(x) for x in obj]
    return obj


def _serialize_record(record: RunRecord) -> dict[str, Any]:
    """Make the RunRecord JSON-safe and redact secrets.

    `OrchestratorConfig` carries the avni-server auth token and Anthropic API
    key; both are needed at runtime but must not appear in the JSON we write
    to disk or share. We replace them with a sentinel string so the consumer
    can tell *that* a value was set without learning what it was.
    """

    def default(o: Any) -> Any:
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        if isinstance(o, tuple):
            return list(o)
        return str(o)

    raw = json.dumps(record, default=default)
    return _redact(json.loads(raw))


async def _run(args: argparse.Namespace) -> RunRecord:
    if not args.docs:
        raise SystemExit("at least one --doc is required")

    config = OrchestratorConfig(
        avni_mcp_url=args.mcp_url,
        avni_auth_token=os.environ.get("AVNI_AUTH_TOKEN", ""),
        anthropic_api_key=os.environ.get("ANTHROPIC_API_KEY", ""),
        model_default=args.model,
        org_name=args.org_name,
        scoping_doc_paths=tuple(args.docs),
        conversation_id=os.environ.get("AVNI_CONVERSATION_ID") or uuid4().hex,
        inject_failure=args.inject_failure,
        upload_task_id=args.upload_task_id,
    )

    handler = (
        _make_auto_handler() if args.non_interactive else _interactive_clarification
    )

    if args.runner == "managed":
        from .managed_runner import ManagedRunner

        runner: Any = ManagedRunner()
    else:
        from .sdk_runner import SDKRunner

        runner = SDKRunner()
    return await runner.run(config, handler)


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    _setup_logging(args.verbose)
    record = asyncio.run(_run(args))

    out = Path(args.out)
    out.write_text(json.dumps(_serialize_record(record), indent=2))
    print(f"\nrun complete: status={record.metrics.final_status}")
    print(f"  phases: {' → '.join(record.metrics.phases_run) or '(none)'}")
    if record.metrics.review_outcome:
        print(f"  review: {record.metrics.review_outcome}")
    print(
        f"  tokens: {record.metrics.input_tokens} in / {record.metrics.output_tokens} out"
    )
    print(
        f"  tool_calls: {record.metrics.tool_calls} ({record.metrics.tool_call_failures} failed)"
    )
    print(f"  clarifications: {record.metrics.clarifications_asked}")
    print(f"  latency: {record.metrics.latency_s:.2f}s")
    print(f"  written to {out}")
    return 0 if record.metrics.final_status == "completed" else 1


if __name__ == "__main__":
    sys.exit(main())
