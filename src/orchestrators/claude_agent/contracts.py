"""
Type contracts for the Claude orchestrator spike.

These are the only types both runners (Managed Agents + Agent SDK) and the test
suite agree on. Keeping them in one module prevents the parity test from drifting.

Anthropic SDK objects are referenced as `Any` here so unit tests can mock them
freely without pulling SDK internals into the contract surface.
"""

from __future__ import annotations

from collections.abc import Awaitable, Callable
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Protocol


class AgentRole(str, Enum):
    """The three Dify v3 agent roles, mirrored for parity."""

    SPEC = "spec"
    REVIEW = "review"
    ERROR = "error"


class SpikeError(RuntimeError):
    """Raised when the spike runner cannot continue and the user should know why.

    Use a typed error rather than a bare RuntimeError so the CLI can decide
    whether to retry, escalate, or abort without string matching.
    """


@dataclass(frozen=True)
class AgentSpec:
    """Declarative description of one agent.

    Both runners turn an AgentSpec into a concrete agent: Managed Agents calls
    `client.beta.agents.create`; the SDK builds a ClaudeAgentOptions from it.
    """

    role: AgentRole
    name: str
    model: str
    system_prompt: str
    mcp_tool_names: tuple[str, ...] = ()
    """Names of avni-ai MCP tools this agent is allowed to invoke. Empty tuple
    means: no tool restriction (rely on the MCP server's own surface)."""

    builtin_tools: tuple[str, ...] = ("read", "glob", "bash")
    """Built-in toolset members enabled for the agent. Excludes write/edit by
    default — review and error agents don't need to write to the sandbox FS."""

    skill_ids: tuple[str, ...] = ()
    """Anthropic-published or custom skill_ids attached to the agent. Order
    matters only for documentation; Claude picks skills by description match."""

    max_iterations: int = 5
    """Hard cap on tool-loop iterations (PEV self-heal cycle limit)."""


@dataclass(frozen=True)
class OrchestratorConfig:
    """All configuration the runners need to start up.

    Read from env in `from_env()` so the CLI and the tests construct it the same
    way. Tests override fields explicitly.
    """

    avni_mcp_url: str
    """Streamable-HTTP URL of the avni-ai FastMCP server reachable from the
    runtime (Anthropic infra for Managed Agents; localhost for SDK)."""

    avni_auth_token: str
    """Avni server auth token — POSTed to /store-auth-token, never to Claude."""

    anthropic_api_key: str
    """Anthropic API key. Must be live for managed_runner; sdk_runner can
    function with a Claude Code session instead, but we require it for parity."""

    model_default: str = "claude-opus-4-5"
    """Pinned model. Opus 4.5 is the lowest-version-Manage-Agents-supports per
    docs (`All Claude 4.5 and later models are supported.`). Override per
    agent in AgentSpec.model when cost-tier matters."""

    org_name: str = ""
    """Org name threaded into /generate-spec — fixes Dify pain point #1
    (DifyWorkflowLearnings.md §1)."""

    scoping_doc_paths: tuple[str, ...] = ()
    """Local paths to XLS / PDF / image scoping docs to ingest."""

    conversation_id: str = ""
    """Stable id used by avni-ai's in-memory stores (entities/spec/bundle).
    Empty string → runners generate one."""

    max_pev_cycles: int = 3
    """Max self-healing retries (PEV plan-emulate-verify). Matches Dify."""

    request_timeout_s: float = 120.0
    """HTTP timeout for any request the runner makes itself."""

    inject_failure: bool = False
    """When True, the runner forces the upload step into a failure path so the
    Error Agent fires (M5). Used in spike comparisons; harmless in real runs."""

    upload_task_id: str = ""
    """Optional: pass an existing avni-server upload task_id straight to the
    Error Agent for diagnosis without running the spec/review phases. Useful
    for ad-hoc post-mortems on a real failure. Empty string → normal flow."""

    @classmethod
    def from_env(cls, **overrides: Any) -> OrchestratorConfig:
        """Build a config from env vars, with optional overrides for testing."""
        import os

        defaults: dict[str, Any] = {
            "avni_mcp_url": os.environ.get(
                "AVNI_MCP_SERVER_URL", "http://localhost:8023/mcp"
            ),
            "avni_auth_token": os.environ.get("AVNI_AUTH_TOKEN", ""),
            "anthropic_api_key": os.environ.get("ANTHROPIC_API_KEY", ""),
            "org_name": os.environ.get("AVNI_ORG_NAME", ""),
            "model_default": os.environ.get("AVNI_CLAUDE_MODEL", "claude-opus-4-5"),
        }
        defaults.update(overrides)
        return cls(**defaults)


# ---------------------------------------------------------------------------
# Multi-turn clarification surface
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class ClarificationRequest:
    """Normalized AskUserQuestion payload from either runner.

    Managed Agents emits this as a tool-use event named `AskUserQuestion`; the
    SDK surfaces it via the `canUseTool` callback. The CLI consumes the same
    shape regardless of source so parity tests can compare side-by-side.
    """

    question: str
    options: tuple[str, ...] = ()
    """Multiple-choice options. Empty tuple → free-text answer expected."""
    context: str = ""
    """Optional context the agent provided (e.g. validator error excerpt)."""


@dataclass(frozen=True)
class ClarificationResponse:
    """The user's answer to a ClarificationRequest."""

    answer: str
    """Selected option text (if options non-empty) or free-text answer."""


ClarificationHandler = Callable[
    [ClarificationRequest], Awaitable[ClarificationResponse]
]
"""Async callback the CLI passes to runners. Tests pass a deterministic stub."""


# ---------------------------------------------------------------------------
# Run record (the thing M7 compare_runs.py joins with the Dify CSV)
# ---------------------------------------------------------------------------


@dataclass
class AgentMetrics:
    """Per-run metrics captured by both runners.

    Mutable so runners can update incrementally; serialised to JSON at end of
    run for compare_runs.py.
    """

    runner: str
    """'managed' or 'sdk' — populated by the runner itself."""

    started_at: float = 0.0
    """time.time() at run start, populated by runner."""

    finished_at: float = 0.0
    """time.time() at run end (success or failure)."""

    input_tokens: int = 0
    output_tokens: int = 0

    tool_calls: int = 0
    tool_call_failures: int = 0
    tool_call_retries: int = 0
    """Same arg + same tool within a single agent run = retry."""

    clarifications_asked: int = 0
    pev_cycles: int = 0
    """Number of validate-spec ↔ regen iterations that actually fired."""

    final_status: str = "pending"
    """One of: pending, completed, failed, escalated."""

    error: str | None = None

    phases_run: list[str] = field(default_factory=list)
    """Ordered list of phases the runner actually drove this run, e.g.
    ['spec', 'review', 'error']. Useful for the comparison matrix to confirm
    Spec→Review→Error sequencing. Mutated as each phase begins."""

    review_outcome: str = ""
    """'approve', 'revise', or '' if the review phase didn't run. Set by the
    runner from the Review Agent's final assistant message."""

    @property
    def latency_s(self) -> float:
        """Wall-clock seconds — only meaningful after finished_at is set."""
        if self.finished_at <= 0 or self.started_at <= 0:
            return 0.0
        return self.finished_at - self.started_at


@dataclass
class RunRecord:
    """Complete record of one end-to-end run; persisted to disk by the CLI."""

    config: OrchestratorConfig
    metrics: AgentMetrics
    final_spec_yaml: str = ""
    final_bundle_b64: str = ""
    upload_task_id: str = ""
    transcript: list[dict[str, Any]] = field(default_factory=list)
    """Ordered list of normalised events (user/assistant/tool/clarification).
    Shape: {type, role?, content?, tool_name?, tool_input?, tool_output?}."""


# ---------------------------------------------------------------------------
# Runner protocol — implemented by managed_runner and sdk_runner
# ---------------------------------------------------------------------------


class RunnerProtocol(Protocol):
    """Both runners must satisfy this so the CLI is runner-agnostic."""

    async def run(
        self,
        config: OrchestratorConfig,
        clarification_handler: ClarificationHandler,
    ) -> RunRecord:
        """End-to-end: ingest scoping docs → spec → bundle → upload → record."""
        ...
