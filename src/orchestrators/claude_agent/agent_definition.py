"""
Declarative agent definitions for the spike.

Single source of truth for both runners. Adding a new agent here, or changing
its tool surface, ripples through Managed Agents AND the SDK without code
changes anywhere else.

The system prompts live in `prompts/<role>_agent.md` so they are diffable in
PRs without touching Python.
"""

from __future__ import annotations

import json
from importlib import resources
from pathlib import Path

from .contracts import AgentRole, AgentSpec


def _load_prompt(role: AgentRole) -> str:
    """Read a system prompt from the prompts/ directory.

    Falls back to a filesystem read for development; in installed packages we
    use importlib.resources so the .md files travel with the wheel.
    """
    fname = f"{role.value}_agent.md"
    try:
        return (resources.files(__package__) / "prompts" / fname).read_text()
    except (FileNotFoundError, AttributeError):
        # Editable install / dev path
        here = Path(__file__).parent / "prompts" / fname
        return here.read_text()


# Spec Agent: drives the requirements-gathering + spec loop. Mirrors Dify v3
# Spec Agent (avni-ai-iterative-dev-plan.md §"Phase 4"). Tool list is the
# subset that does not require avni-server auth.
SPEC_AGENT = AgentSpec(
    role=AgentRole.SPEC,
    name="Avni Spec Agent",
    model="claude-opus-4-5",
    system_prompt=_load_prompt(AgentRole.SPEC),
    mcp_tool_names=(
        "parse-srs-file",
        "store-entities",
        "validate-entities",
        "apply-entity-corrections",
        "generate-spec",
        "validate-spec",
        "bundle-to-spec",
        "enrich-spec",
        "knowledge-search",
        "get-spec",
    ),
    builtin_tools=("read", "glob", "bash"),
    skill_ids=(),  # Set at config time — depends on whether skills uploaded
    max_iterations=5,
)


# Review Agent: inspects the generated bundle before upload. Read-mostly tools,
# plus execute-python for ad-hoc invariant checks.
REVIEW_AGENT = AgentSpec(
    role=AgentRole.REVIEW,
    name="Avni Review Agent",
    model="claude-sonnet-4-5",  # cheaper — review is mostly verification
    system_prompt=_load_prompt(AgentRole.REVIEW),
    mcp_tool_names=(
        "validate-bundle",
        "bundle-to-spec",
        "download-bundle-b64",
        "bundle-files",
        "bundle-file",
        "execute-python",
    ),
    builtin_tools=("read", "glob"),
    skill_ids=(),
    max_iterations=3,
)


# Error Agent: diagnoses upload failures and proposes targeted fixes.
ERROR_AGENT = AgentSpec(
    role=AgentRole.ERROR,
    name="Avni Error Agent",
    model="claude-sonnet-4-5",
    system_prompt=_load_prompt(AgentRole.ERROR),
    mcp_tool_names=(
        "upload-status",
        "execute-python",
        "generate-bundle",
        "validate-bundle",
        "bundle-files",
    ),
    builtin_tools=("read", "glob"),
    skill_ids=(),
    max_iterations=3,
)


ALL_AGENTS: tuple[AgentSpec, ...] = (SPEC_AGENT, REVIEW_AGENT, ERROR_AGENT)


def with_skill_ids(spec: AgentSpec, skill_ids: tuple[str, ...]) -> AgentSpec:
    """Return a copy of spec with skill_ids replaced.

    Frozen dataclasses don't accept attribute writes; this is the canonical
    way to attach skill IDs after they've been uploaded to Anthropic.
    """
    from dataclasses import replace

    return replace(spec, skill_ids=skill_ids)


# Which uploaded skills each agent should attach. Names are the manifest keys
# (matching `SPIKE_SKILLS` in scripts/spike/upload_avni_skills.py). Anthropic
# picks among attached skills by description, so over-attaching is cheap; we
# still scope per-agent so the comparison report can attribute usage.
_SKILL_ASSIGNMENTS: dict[AgentRole, tuple[str, ...]] = {
    AgentRole.SPEC: (
        "srs-bundle-generator",
        "project-scoping",
        "implementation-engineer",
        "architecture-patterns",
    ),
    AgentRole.REVIEW: (
        "srs-bundle-generator",
        "architecture-patterns",
    ),
    AgentRole.ERROR: (
        "support-engineer",
        "support-patterns",
    ),
}


_MANIFEST_PATH = Path(__file__).parent / "skills.json"


def load_skills_manifest() -> dict[str, str]:
    """Read skills.json (manifest written by upload_avni_skills.py).

    Returns `{}` if the manifest is missing — agents then run prompt-only.
    Callers don't have to handle the absence specially: `attach_skills`
    silently passes empty tuples through.
    """
    if not _MANIFEST_PATH.exists():
        return {}
    return json.loads(_MANIFEST_PATH.read_text())


def attach_skills(
    spec: AgentSpec, manifest: dict[str, str] | None = None
) -> AgentSpec:
    """Return a copy of `spec` with the right skill_ids attached.

    Drops manifest entries that are missing instead of erroring; missing
    skills typically mean the manifest predates a `_SKILL_ASSIGNMENTS`
    rename, and crashing here would block the whole run.
    """
    manifest = load_skills_manifest() if manifest is None else manifest
    wanted = _SKILL_ASSIGNMENTS.get(spec.role, ())
    ids = tuple(manifest[n] for n in wanted if n in manifest)
    return with_skill_ids(spec, ids)
