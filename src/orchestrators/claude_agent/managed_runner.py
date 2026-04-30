"""
Managed Agents runner — the primary path for the spike.

Talks to Anthropic's hosted Managed Agents API (`anthropic-beta:
managed-agents-2026-04-01`). The avni-ai FastMCP server is wired in as a remote
MCP server via `mcp_servers` + `mcp_toolset`; auth for avni-server itself is
threaded through `/store-auth-token` *before* the session starts so it never
appears in any agent prompt or tool argument.

This module is deliberately thin: it owns lifecycle (agents, environments,
sessions, files), the event-stream consumer, and metrics; everything else
(prompts, agent specs, error semantics) lives in sibling modules.
"""

from __future__ import annotations

import logging
import os
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from uuid import uuid4

import httpx

from .agent_definition import (
    ALL_AGENTS,
    ERROR_AGENT,
    REVIEW_AGENT,
    SPEC_AGENT,
    attach_skills,
    load_skills_manifest,
)
from .contracts import (
    AgentMetrics,
    AgentRole,
    AgentSpec,
    ClarificationHandler,
    ClarificationRequest,
    OrchestratorConfig,
    RunRecord,
    SpikeError,
)

logger = logging.getLogger(__name__)

BETA_HEADER = "managed-agents-2026-04-01"
"""Pinned beta header. If Anthropic ships a v2 we update this single constant."""


@dataclass
class _SessionCtx:
    """Lifecycle handles we collect during a run; cleaned up on exit."""

    agent_id: str
    environment_id: str
    session_id: str
    file_ids: list[str]


class ManagedRunner:
    """Drive a full SRS-to-bundle run on Managed Agents."""

    def __init__(self, anthropic_client: Any | None = None):
        # Lazy-imported so test code can pass a mock without paying the import.
        if anthropic_client is None:
            from anthropic import Anthropic

            anthropic_client = Anthropic(
                api_key=os.environ.get("ANTHROPIC_API_KEY", "")
            )
        self.client = anthropic_client

    # ------------------------------------------------------------------ run

    async def run(
        self,
        config: OrchestratorConfig,
        clarification_handler: ClarificationHandler,
    ) -> RunRecord:
        """End-to-end run: spec → review → upload → (error on failure).

        Each phase runs in its own agent + environment + session; lifecycle
        handles are stacked in `cleanup_stack` so `_cleanup` tears them down
        even if a later phase raises. The phases share `config.conversation_id`
        so avni-ai's in-memory state (parsed entities, generated bundle,
        upload task_id) is visible across them.
        """
        metrics = AgentMetrics(runner="managed", started_at=time.time())
        record = RunRecord(config=config, metrics=metrics)
        cleanup_stack: list[_SessionCtx] = []
        try:
            if not config.anthropic_api_key:
                raise SpikeError("anthropic_api_key is empty; nothing to do.")
            if not config.avni_mcp_url:
                raise SpikeError("avni_mcp_url is empty; the agent needs the MCP URL.")

            await self._register_auth_token(config)
            file_ids = await self._upload_scoping_docs(config)
            manifest = load_skills_manifest()

            # Phase 1 — Spec: ingest SRS, ask clarifying questions, produce
            # bundle. The spec agent invokes `generate-bundle` itself so by the
            # time it goes idle we expect a bundle to exist for this conversation.
            await self._run_phase(
                spec=attach_skills(SPEC_AGENT, manifest),
                kickoff=self._spec_kickoff(config),
                file_ids=file_ids,
                config=config,
                metrics=metrics,
                record=record,
                clarification_handler=clarification_handler,
                cleanup_stack=cleanup_stack,
            )

            # Phase 2 — Review: round-trip the bundle, validate, decide.
            review_text = await self._run_phase(
                spec=attach_skills(REVIEW_AGENT, manifest),
                kickoff=self._review_kickoff(config),
                file_ids=[],  # review reads bundle via MCP, not mounted files
                config=config,
                metrics=metrics,
                record=record,
                clarification_handler=clarification_handler,
                cleanup_stack=cleanup_stack,
            )
            metrics.review_outcome = _classify_review(review_text)

            # Phase 3 — Error: only when the upload fails (or M5 inject flag).
            should_run_error = (
                config.inject_failure
                or bool(config.upload_task_id)
                or metrics.review_outcome == "revise"
            )
            if should_run_error:
                await self._run_phase(
                    spec=attach_skills(ERROR_AGENT, manifest),
                    kickoff=self._error_kickoff(config, metrics.review_outcome),
                    file_ids=[],
                    config=config,
                    metrics=metrics,
                    record=record,
                    clarification_handler=clarification_handler,
                    cleanup_stack=cleanup_stack,
                )

            metrics.final_status = "completed"
            return record
        except SpikeError as e:
            metrics.final_status = "failed"
            metrics.error = str(e)
            return record
        except Exception as e:  # noqa: BLE001  — runner is the top of stack
            logger.exception("managed runner crashed")
            metrics.final_status = "failed"
            metrics.error = repr(e)
            return record
        finally:
            metrics.finished_at = time.time()
            for ctx in reversed(cleanup_stack):
                await self._cleanup(ctx)

    # ----------------------------------------------------------------- phases

    async def _run_phase(
        self,
        *,
        spec: AgentSpec,
        kickoff: str,
        file_ids: list[str],
        config: OrchestratorConfig,
        metrics: AgentMetrics,
        record: RunRecord,
        clarification_handler: ClarificationHandler,
        cleanup_stack: list[_SessionCtx],
    ) -> str:
        """Drive one agent through one session. Returns the trailing assistant
        text so the orchestrator can branch (e.g. APPROVE vs REVISE).

        Lifecycle handles are appended to `cleanup_stack` so `run()`'s finally
        block tears them down even if a later phase raises. The phase's role
        is appended to `metrics.phases_run` *before* the event loop starts so
        a crash inside the phase is still attributable.
        """
        metrics.phases_run.append(spec.role.value)
        record.transcript.append(
            {"type": "phase_start", "phase": spec.role.value, "agent": spec.name}
        )

        agent = await self._create_agent(spec, config)
        env = await self._create_environment(config)
        session = await self._create_session(
            agent_id=agent.id,
            environment_id=env.id,
            file_ids=file_ids,
            doc_paths=config.scoping_doc_paths if file_ids else (),
        )
        ctx = _SessionCtx(
            agent_id=agent.id,
            environment_id=env.id,
            session_id=session.id,
            file_ids=file_ids,
        )
        cleanup_stack.append(ctx)

        # Phase-scoped index so we can extract the trailing text without
        # re-walking the full transcript.
        phase_start_idx = len(record.transcript)
        await self._send_user_message(ctx.session_id, kickoff)
        await self._drive_event_loop(
            ctx=ctx,
            config=config,
            metrics=metrics,
            record=record,
            clarification_handler=clarification_handler,
        )
        record.transcript.append({"type": "phase_end", "phase": spec.role.value})
        return _trailing_assistant_text(record.transcript[phase_start_idx:])

    def _spec_kickoff(self, config: OrchestratorConfig) -> str:
        files_listing = "\n".join(
            f"- /workspace/{Path(p).name}" for p in config.scoping_doc_paths
        )
        org = config.org_name or "the organisation"
        return (
            f"You are configuring an Avni app for **{org}**.\n\n"
            f"Scoping docs are mounted at:\n{files_listing}\n\n"
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

    # ------------------------------------------------------------ lifecycle

    async def _register_auth_token(self, config: OrchestratorConfig) -> None:
        """POST the avni-server auth token to /store-auth-token, indexed by
        conversation_id, so subsequent MCP calls can find it without putting
        the token in any prompt or argument.
        """
        if not config.avni_auth_token:
            logger.info("no avni_auth_token configured; skipping store-auth-token")
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
                    # Deliberately do NOT include resp.text — it could echo
                    # the auth token back in an error body and end up in the
                    # serialized run record.
                    raise SpikeError(
                        f"store-auth-token returned HTTP {resp.status_code}"
                    )
            except httpx.HTTPError as e:
                raise SpikeError(f"could not reach avni-ai at {url}: {e}") from e

    async def _upload_scoping_docs(self, config: OrchestratorConfig) -> list[str]:
        """Upload each scoping doc via the Files API. Returns parallel list of
        file IDs (same order as config.scoping_doc_paths).
        """
        ids: list[str] = []
        for p in config.scoping_doc_paths:
            path = Path(p)
            if not path.exists():
                raise SpikeError(f"scoping doc not found: {p}")
            with path.open("rb") as f:
                uploaded = self.client.beta.files.upload(file=f, betas=[BETA_HEADER])
            ids.append(uploaded.id)
            logger.info("uploaded %s -> %s", path.name, uploaded.id)
        return ids

    async def _create_agent(self, spec: AgentSpec, config: OrchestratorConfig) -> Any:
        """Create the agent. Skills attached only if upload step has populated
        skill_ids; otherwise the agent runs prompt-only (still functional, less
        Avni-domain context).

        Note: org_name is *not* threaded into the system prompt here because we
        send it as the kickoff user message instead (see `_kickoff_user_message`)
        — that way the same agent definition can be reused across orgs without
        a new version per org.
        """
        tools: list[dict[str, Any]] = [
            {
                "type": "agent_toolset_20260401",
                "default_config": {"enabled": False},
                "configs": [{"name": n, "enabled": True} for n in spec.builtin_tools],
            },
            {"type": "mcp_toolset", "mcp_server_name": "avni-ai"},
        ]
        skills = [
            {"type": "custom", "skill_id": sid, "version": "latest"}
            for sid in spec.skill_ids
        ]
        return self.client.beta.agents.create(
            name=spec.name,
            model=spec.model,
            system=spec.system_prompt,
            mcp_servers=[
                {"type": "url", "name": "avni-ai", "url": config.avni_mcp_url}
            ],
            tools=tools,
            skills=skills,
            betas=[BETA_HEADER],
        )

    async def _create_environment(self, config: OrchestratorConfig) -> Any:
        """Spin up a per-run environment. Cheap; cleaned up at end."""
        return self.client.beta.environments.create(
            name=f"avni-spike-{uuid4().hex[:8]}",
            betas=[BETA_HEADER],
        )

    async def _create_session(
        self,
        *,
        agent_id: str,
        environment_id: str,
        file_ids: list[str],
        doc_paths: tuple[str, ...],
    ) -> Any:
        resources = [
            {
                "type": "file",
                "file_id": fid,
                "mount_path": f"/workspace/{Path(p).name}",
            }
            for fid, p in zip(file_ids, doc_paths, strict=True)
        ]
        return self.client.beta.sessions.create(
            agent=agent_id,
            environment_id=environment_id,
            resources=resources,
            betas=[BETA_HEADER],
        )

    async def _send_user_message(self, session_id: str, text: str) -> None:
        """Post a single user.message to a session — replaces the old
        per-phase kickoff helper now that all three phases use the same shape.
        """
        self.client.beta.sessions.events.send(
            session_id,
            events=[
                {"type": "user.message", "content": [{"type": "text", "text": text}]}
            ],
            betas=[BETA_HEADER],
        )

    # ----------------------------------------------------------- event loop

    async def _drive_event_loop(
        self,
        *,
        ctx: _SessionCtx,
        config: OrchestratorConfig,
        metrics: AgentMetrics,
        record: RunRecord,
        clarification_handler: ClarificationHandler,
    ) -> None:
        """Consume the SSE event stream until the session goes idle.

        Handles:
          - text deltas → captured into transcript
          - tool_use events for built-in MCP tools → noop (Anthropic executes)
          - tool_use for AskUserQuestion → call user, post answer back
          - usage events → metrics
          - session.error / session.terminated → SpikeError
        """
        # The SDK exposes `events.stream(session_id=...)` as a streamed iterator
        # of typed events. We consume it with httpx-backed retry: if the
        # connection drops we resume from the last seen event.
        while True:
            stream = self.client.beta.sessions.events.stream(
                session_id=ctx.session_id, betas=[BETA_HEADER]
            )
            try:
                with stream as events:
                    for event in events:
                        await self._handle_event(
                            event=event,
                            ctx=ctx,
                            metrics=metrics,
                            record=record,
                            clarification_handler=clarification_handler,
                        )
                # Session finished a turn — check status to decide whether to
                # close, wait for a user event, or keep streaming.
                session = self.client.beta.sessions.retrieve(
                    ctx.session_id, betas=[BETA_HEADER]
                )
                if session.status in ("idle", "terminated"):
                    return
            except httpx.HTTPError as e:
                logger.warning("event stream dropped (%s); resubscribing", e)
                continue

    async def _handle_event(
        self,
        *,
        event: Any,
        ctx: _SessionCtx,
        metrics: AgentMetrics,
        record: RunRecord,
        clarification_handler: ClarificationHandler,
    ) -> None:
        """Route a single SSE event to the right place.

        Anthropic event shapes are documented at
        https://platform.claude.com/docs/en/managed-agents/events-and-streaming
        We touch only fields the spike needs; unknown events are recorded and
        skipped so future API additions don't crash the runner.
        """
        etype = getattr(event, "type", None) or (
            event.get("type") if isinstance(event, dict) else None
        )

        if etype == "assistant.message.delta":
            text = _extract_text_delta(event)
            if text:
                record.transcript.append({"type": "assistant_text", "content": text})

        elif etype == "tool_use":
            tool_name = _attr(event, "tool_name") or _attr(event, "name")
            metrics.tool_calls += 1
            record.transcript.append(
                {
                    "type": "tool_use",
                    "tool_name": tool_name,
                    "tool_input": _attr(event, "input"),
                }
            )
            if tool_name == "AskUserQuestion":
                await self._handle_ask_user_question(
                    event=event,
                    ctx=ctx,
                    metrics=metrics,
                    record=record,
                    handler=clarification_handler,
                )

        elif etype == "tool_result":
            record.transcript.append(
                {
                    "type": "tool_result",
                    "tool_use_id": _attr(event, "tool_use_id"),
                    "is_error": bool(_attr(event, "is_error")),
                    "content": _attr(event, "content"),
                }
            )
            if _attr(event, "is_error"):
                metrics.tool_call_failures += 1

        elif etype == "usage":
            metrics.input_tokens += int(_attr(event, "input_tokens") or 0)
            metrics.output_tokens += int(_attr(event, "output_tokens") or 0)

        elif etype == "session.error":
            raise SpikeError(f"session.error: {_attr(event, 'message')}")

        elif etype == "session.terminated":
            raise SpikeError(
                f"session terminated unexpectedly: {_attr(event, 'reason')}"
            )

        else:
            # Record unknown events so the comparison report can flag API
            # surface drift, but don't fail.
            record.transcript.append({"type": "unknown", "raw": str(event)[:500]})

    async def _handle_ask_user_question(
        self,
        *,
        event: Any,
        ctx: _SessionCtx,
        metrics: AgentMetrics,
        record: RunRecord,
        handler: ClarificationHandler,
    ) -> None:
        """Pause for user input, then post the answer back as a user.message
        event so the agent resumes."""
        tool_input = _attr(event, "input") or {}
        request = ClarificationRequest(
            question=tool_input.get("question", ""),
            options=tuple(tool_input.get("options", []) or []),
            context=tool_input.get("context", ""),
        )
        metrics.clarifications_asked += 1
        record.transcript.append(
            {
                "type": "clarification_request",
                "question": request.question,
                "options": list(request.options),
            }
        )
        response = await handler(request)
        record.transcript.append(
            {"type": "clarification_response", "answer": response.answer}
        )
        await self._send_user_message(ctx.session_id, response.answer)

    # --------------------------------------------------------------- cleanup

    async def _cleanup(self, ctx: _SessionCtx) -> None:
        """Best-effort teardown. Swallow errors — the run is over."""
        for op_name, op in (
            (
                "delete session",
                lambda: self.client.beta.sessions.delete(
                    ctx.session_id, betas=[BETA_HEADER]
                ),
            ),
            (
                "delete environment",
                lambda: self.client.beta.environments.delete(
                    ctx.environment_id, betas=[BETA_HEADER]
                ),
            ),
            (
                "archive agent",
                lambda: self.client.beta.agents.archive(
                    ctx.agent_id, betas=[BETA_HEADER]
                ),
            ),
        ):
            try:
                op()
            except Exception as e:  # noqa: BLE001
                logger.info("%s failed (ignored): %s", op_name, e)


# ---------------------------------------------------------------------------
# Helpers — kept at module level so the test suite can import them directly.
# ---------------------------------------------------------------------------


def _attr(obj: Any, name: str) -> Any:
    """Read an attribute or dict key uniformly. The Anthropic SDK emits typed
    objects but the tests mock with plain dicts, so we accept either.
    """
    if hasattr(obj, name):
        return getattr(obj, name)
    if isinstance(obj, dict):
        return obj.get(name)
    return None


def _extract_text_delta(event: Any) -> str:
    """Pull the `text` field out of an assistant message delta. Returns ""
    if the event shape doesn't carry text (e.g. it's a thinking delta).
    """
    delta = _attr(event, "delta")
    if delta is None:
        return ""
    if isinstance(delta, dict):
        return delta.get("text", "") or ""
    return getattr(delta, "text", "") or ""


def _trailing_assistant_text(phase_events: list[dict[str, Any]]) -> str:
    """Concatenate assistant text from a phase's transcript slice.

    The Review Agent answers in plain text; the orchestrator only needs the
    last block of assistant output to detect APPROVE / REVISE. Tool calls and
    intermediate thinking are skipped.
    """
    parts: list[str] = []
    for ev in phase_events:
        if ev.get("type") == "assistant_text":
            content = ev.get("content")
            if isinstance(content, str):
                parts.append(content)
    return "".join(parts)


def _classify_review(text: str) -> str:
    """Return 'approve', 'revise', or '' for the Review Agent's last reply.

    Looks for explicit markers — case-insensitive but order-sensitive: an
    APPROVE that follows a REVISE in the same reply still counts as REVISE,
    because the agent's final word is what matters.
    """
    if not text:
        return ""
    upper = text.upper()
    last_revise = upper.rfind("REVISE")
    last_approve = upper.rfind("APPROVE")
    if last_revise == -1 and last_approve == -1:
        return ""
    return "revise" if last_revise > last_approve else "approve"


# ---------------------------------------------------------------------------
# Module-level convenience
# ---------------------------------------------------------------------------


async def run(
    config: OrchestratorConfig,
    clarification_handler: ClarificationHandler,
) -> RunRecord:
    """Module-level entrypoint matching RunnerProtocol.run."""
    return await ManagedRunner().run(config, clarification_handler)


__all__ = [
    "ManagedRunner",
    "BETA_HEADER",
    "ALL_AGENTS",  # re-export for tests' convenience
    "run",
]
