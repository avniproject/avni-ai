"""
Claude Agent SDK runner — parity adapter for the spike.

Same agent specs as `managed_runner.py`, but driven through the local
`claude_agent_sdk.query` loop. The SDK runs the agent loop in our process and
talks to Anthropic for inference; tools are the same `avni-ai` MCP server we
expose to Managed Agents (via streamable-HTTP).

Why we need it: the issue and the comparison matrix benefit from a runner the
team can iterate on locally without burning the Managed Agents beta quota or
provisioning a public ingress for the FastMCP server. It also acts as a parity
test — if the SDK and Managed Agents disagree on the same input, that
disagreement is interesting on its own.

Mapping decisions:
  - `system_prompt`         → SPEC_AGENT.system_prompt (same .md file).
  - `mcp_servers`           → {"avni-ai": HttpServerConfig(url=...)}.
  - `allowed_tools`         → SPEC_AGENT.builtin_tools + AskUserQuestion +
                              all tools the avni-ai MCP server publishes
                              (filtered by SPEC_AGENT.mcp_tool_names).
  - `setting_sources`       → ["project"] so .claude/skills/ in the supplied
                              cwd is picked up; tests inject a tmp_path with
                              symlinked avni-skills.
  - `can_use_tool`          → routes AskUserQuestion to the clarification
                              handler and accepts everything else.
"""

from __future__ import annotations

import logging
import time
from pathlib import Path
from typing import Any
from uuid import uuid4

import httpx

from .agent_definition import (
    ERROR_AGENT,
    REVIEW_AGENT,
    SPEC_AGENT,
    attach_skills,
    load_skills_manifest,
)
from .contracts import (
    AgentMetrics,
    AgentSpec,
    ClarificationHandler,
    ClarificationRequest,
    OrchestratorConfig,
    RunRecord,
    SpikeError,
)
from .managed_runner import _classify_review, _trailing_assistant_text

logger = logging.getLogger(__name__)


class SDKRunner:
    """Local-process runner using `claude_agent_sdk.query`."""

    def __init__(self, query_fn: Any | None = None):
        # Lazy import + DI hook so unit tests can pass a stub iterator.
        if query_fn is None:
            from claude_agent_sdk import query

            query_fn = query
        self._query = query_fn

    # ------------------------------------------------------------------ run

    async def run(
        self,
        config: OrchestratorConfig,
        clarification_handler: ClarificationHandler,
    ) -> RunRecord:
        """End-to-end: same Spec → Review → (Error) sequence as the managed
        runner, driven through `claude_agent_sdk.query` instead of the
        Managed Agents API. Each phase issues its own `query()` call with
        agent-specific options, so the SDK loop sees the right system prompt
        and tool surface per phase.
        """
        metrics = AgentMetrics(runner="sdk", started_at=time.time())
        record = RunRecord(config=config, metrics=metrics)
        try:
            if not config.avni_mcp_url:
                raise SpikeError("avni_mcp_url is empty; the SDK runner needs the URL.")
            await self._register_auth_token(config)
            manifest = load_skills_manifest()

            # Phase 1 — Spec
            await self._run_phase(
                spec=attach_skills(SPEC_AGENT, manifest),
                kickoff=self._spec_kickoff(config),
                config=config,
                metrics=metrics,
                record=record,
                clarification_handler=clarification_handler,
            )

            # Phase 2 — Review
            review_text = await self._run_phase(
                spec=attach_skills(REVIEW_AGENT, manifest),
                kickoff=self._review_kickoff(config),
                config=config,
                metrics=metrics,
                record=record,
                clarification_handler=clarification_handler,
            )
            metrics.review_outcome = _classify_review(review_text)

            # Phase 3 — Error (only on failure / inject)
            should_run_error = (
                config.inject_failure
                or bool(config.upload_task_id)
                or metrics.review_outcome == "revise"
            )
            if should_run_error:
                await self._run_phase(
                    spec=attach_skills(ERROR_AGENT, manifest),
                    kickoff=self._error_kickoff(config, metrics.review_outcome),
                    config=config,
                    metrics=metrics,
                    record=record,
                    clarification_handler=clarification_handler,
                )

            metrics.final_status = "completed"
            return record
        except SpikeError as e:
            metrics.final_status = "failed"
            metrics.error = str(e)
            return record
        except Exception as e:  # noqa: BLE001
            logger.exception("sdk runner crashed")
            metrics.final_status = "failed"
            metrics.error = repr(e)
            return record
        finally:
            metrics.finished_at = time.time()

    async def _run_phase(
        self,
        *,
        spec: AgentSpec,
        kickoff: str,
        config: OrchestratorConfig,
        metrics: AgentMetrics,
        record: RunRecord,
        clarification_handler: ClarificationHandler,
    ) -> str:
        """Run one agent through one `query()` call. Returns the trailing
        assistant text so the orchestrator can branch on it."""
        metrics.phases_run.append(spec.role.value)
        record.transcript.append(
            {"type": "phase_start", "phase": spec.role.value, "agent": spec.name}
        )
        phase_start_idx = len(record.transcript)

        options = self._build_options(spec, config, clarification_handler, metrics)
        async for message in self._query(prompt=kickoff, options=options):
            self._consume_message(message, metrics, record)

        record.transcript.append({"type": "phase_end", "phase": spec.role.value})
        return _trailing_assistant_text(record.transcript[phase_start_idx:])

    # ------------------------------------------------------------ ancillary

    async def _register_auth_token(self, config: OrchestratorConfig) -> None:
        """Same auth-out-of-band trick as managed_runner — tested once, here."""
        if not config.avni_auth_token:
            return
        cid = config.conversation_id or uuid4().hex
        url = f"{config.avni_mcp_url.rstrip('/').removesuffix('/mcp')}/store-auth-token"
        async with httpx.AsyncClient(timeout=config.request_timeout_s) as ac:
            try:
                resp = await ac.post(
                    url,
                    json={
                        "conversation_id": cid,
                        "auth_token": config.avni_auth_token,
                    },
                )
                if resp.status_code >= 400:
                    # See managed_runner._register_auth_token: never echo body.
                    raise SpikeError(
                        f"store-auth-token returned HTTP {resp.status_code}"
                    )
            except httpx.HTTPError as e:
                raise SpikeError(f"could not reach avni-ai at {url}: {e}") from e

    def _build_options(
        self,
        spec: AgentSpec,
        config: OrchestratorConfig,
        clarification_handler: ClarificationHandler,
        metrics: AgentMetrics,
    ) -> Any:
        """Return a ClaudeAgentOptions tuned for the given agent.

        Unlike the managed runner (which uses the agent's own MCP toolset),
        the SDK runs in-process and we filter tools per phase via
        `allowed_tools`. The clarification handler is a closure so per-call
        state stays scoped to this phase.
        """
        # Lazy import keeps the contracts module SDK-free.
        from claude_agent_sdk import (
            ClaudeAgentOptions,
            PermissionResultAllow,
            PermissionResultDeny,
        )

        async def can_use_tool(
            tool_name: str,
            tool_input: dict[str, Any],
            _ctx: Any,
        ) -> Any:
            metrics.tool_calls += 1
            if tool_name == "AskUserQuestion":
                request = ClarificationRequest(
                    question=tool_input.get("question", ""),
                    options=tuple(tool_input.get("options", []) or []),
                    context=tool_input.get("context", ""),
                )
                metrics.clarifications_asked += 1
                response = await clarification_handler(request)
                # KNOWN LIMITATION: returning Allow + updated_input here makes
                # the SDK execute AskUserQuestion as a built-in with that input
                # rather than feeding the user's answer back as the tool result
                # the model sees. Anthropic's CLI handles this in-process; the
                # SDK exposes the same primitive only when running through
                # Claude Code. For Managed Agents (the spike's primary path)
                # the round-trip is correct because we send a user.message
                # event back. Tracked in the spike-results writeup.
                return PermissionResultAllow(
                    behavior="allow",
                    updated_input={"answer": response.answer},
                )
            # Sandbox safety: only this phase's MCP tools + builtins.
            allowed = set(spec.builtin_tools) | {
                f"mcp__avni-ai__{n}" for n in spec.mcp_tool_names
            }
            if tool_name in allowed:
                return PermissionResultAllow(behavior="allow")
            return PermissionResultDeny(
                behavior="deny",
                message=f"tool {tool_name!r} not in {spec.role.value} allowlist",
            )

        mcp_servers = {
            "avni-ai": {"type": "http", "url": config.avni_mcp_url},
        }

        return ClaudeAgentOptions(
            system_prompt=spec.system_prompt,
            mcp_servers=mcp_servers,
            allowed_tools=list(spec.builtin_tools)
            + ["AskUserQuestion"]
            + [f"mcp__avni-ai__{n}" for n in spec.mcp_tool_names],
            can_use_tool=can_use_tool,
            model=spec.model or config.model_default,
            max_turns=spec.max_iterations * 4 + 5,  # rough budget per phase
            setting_sources=["project"],
            cwd=str(Path.cwd()),
            permission_mode="default",
        )

    # ------------------------------------------------------------ kickoffs
    # Same wording as managed_runner — keep them in sync so the comparison is
    # fair. Diverging text would let one runner appear smarter purely by prompt
    # engineering rather than by Managed-Agents-vs-SDK behaviour.

    def _spec_kickoff(self, config: OrchestratorConfig) -> str:
        files_listing = (
            "\n".join(f"- {Path(p).resolve()}" for p in config.scoping_doc_paths)
            or "(no files attached — request from the user)"
        )
        org = config.org_name or "the organisation"
        return (
            f"You are configuring an Avni app for **{org}**.\n\n"
            f"Scoping docs (use the Read tool to open them):\n{files_listing}\n\n"
            f"conversation_id (use this in all avni-ai MCP calls): "
            f"`{config.conversation_id}`\n\n"
            "Begin by calling `parse-srs-file` on each doc, then summarise. "
            "Ask clarifying questions whenever validation surfaces an issue. "
            "When the spec is approved, call `generate-bundle` so the next "
            "agent can review it."
        )

    def _review_kickoff(self, config: OrchestratorConfig) -> str:
        return (
            "A bundle has just been generated for "
            f"conversation_id `{config.conversation_id}`. "
            "Validate it with `validate-bundle`, round-trip with "
            "`bundle-to-spec`, and inspect any suspicious files with "
            "`bundle-files` / `bundle-file`. Reply with **APPROVE** "
            "and a one-paragraph summary, or **REVISE** with a "
            "structured list of issues. Stay under 3 iterations."
        )

    def _error_kickoff(
        self, config: OrchestratorConfig, review_outcome: str
    ) -> str:
        if config.upload_task_id:
            return (
                "Upload failed for "
                f"conversation_id `{config.conversation_id}`, "
                f"task_id `{config.upload_task_id}`. "
                "Call `upload-status` to read the failure payload, then "
                "produce the structured Failure / Cause / Confidence / "
                "Proposed fix / User decision report described in your "
                "system prompt."
            )
        if config.inject_failure:
            return (
                "**Spike injected failure**: simulate that the upload for "
                f"conversation_id `{config.conversation_id}` failed with "
                "`Concept name already exists with different UUID`. "
                "Diagnose using your usual playbook (upload-status, "
                "bundle-files, etc. — they may not all return real data) "
                "and return the structured report. Confidence may be low; "
                "that is expected for a synthetic failure."
            )
        return (
            f"The Review Agent flagged the bundle for "
            f"conversation_id `{config.conversation_id}` as REVISE. "
            "Read the previous transcript via the MCP `bundle-files` "
            "surface, identify the smallest fix, and produce the "
            "structured report."
        )

    def _consume_message(
        self,
        message: Any,
        metrics: AgentMetrics,
        record: RunRecord,
    ) -> None:
        """Translate SDK message types into our normalised transcript shape."""
        # Lazy imports so the test harness can pass plain mocks.
        try:
            from claude_agent_sdk import (
                AssistantMessage,
                ResultMessage,
                TextBlock,
                ToolResultBlock,
                ToolUseBlock,
            )
        except ImportError:  # pragma: no cover  — only happens in degraded envs
            AssistantMessage = ResultMessage = type("X", (), {})
            TextBlock = ToolResultBlock = ToolUseBlock = type("X", (), {})

        if isinstance(message, AssistantMessage):
            for block in getattr(message, "content", []) or []:
                if isinstance(block, TextBlock):
                    record.transcript.append(
                        {"type": "assistant_text", "content": block.text}
                    )
                elif isinstance(block, ToolUseBlock):
                    record.transcript.append(
                        {
                            "type": "tool_use",
                            "tool_name": block.name,
                            "tool_input": block.input,
                        }
                    )
                elif isinstance(block, ToolResultBlock):
                    record.transcript.append(
                        {
                            "type": "tool_result",
                            "tool_use_id": getattr(block, "tool_use_id", None),
                            "content": getattr(block, "content", None),
                            "is_error": bool(getattr(block, "is_error", False)),
                        }
                    )
                    if getattr(block, "is_error", False):
                        metrics.tool_call_failures += 1
        elif isinstance(message, ResultMessage):
            usage = getattr(message, "usage", None) or {}
            metrics.input_tokens += int(usage.get("input_tokens", 0) or 0)
            metrics.output_tokens += int(usage.get("output_tokens", 0) or 0)
        else:
            # System / Stream / RateLimit events — record as raw for debugging.
            record.transcript.append({"type": "raw", "repr": repr(message)[:300]})


async def run(
    config: OrchestratorConfig,
    clarification_handler: ClarificationHandler,
) -> RunRecord:
    return await SDKRunner().run(config, clarification_handler)


__all__ = ["SDKRunner", "run"]
