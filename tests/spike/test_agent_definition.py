"""Unit tests for the agent_definition module.

These guard the topology that the comparison matrix depends on: same role
names, same tool inventories, prompts that load. If a renaming cascades
through, this test catches it before runtime.
"""

from __future__ import annotations

from src.orchestrators.claude_agent.agent_definition import (
    ALL_AGENTS,
    ERROR_AGENT,
    REVIEW_AGENT,
    SPEC_AGENT,
    with_skill_ids,
)
from src.orchestrators.claude_agent.contracts import AgentRole


class TestAllAgentsTopology:
    def test_three_agents_in_canonical_order(self):
        assert [a.role for a in ALL_AGENTS] == [
            AgentRole.SPEC,
            AgentRole.REVIEW,
            AgentRole.ERROR,
        ]

    def test_each_agent_has_a_loaded_prompt(self):
        for spec in ALL_AGENTS:
            assert spec.system_prompt, f"{spec.role.value} prompt empty"
            assert len(spec.system_prompt) > 200, (
                f"{spec.role.value} prompt suspiciously short — did the file move?"
            )


class TestSpecAgent:
    def test_has_required_mcp_tools_for_spec_loop(self):
        # The Dify v3 plan (avni-ai-iterative-dev-plan.md §"Phase 4") requires
        # this minimal toolset — guarded so we don't accidentally drop one.
        required = {
            "parse-srs-file",
            "validate-entities",
            "generate-spec",
            "validate-spec",
            "apply-entity-corrections",
            "bundle-to-spec",
        }
        assert required.issubset(set(SPEC_AGENT.mcp_tool_names))

    def test_does_not_have_write_tool(self):
        # Spec Agent reasons over files; it does not write to the sandbox FS.
        assert "write" not in SPEC_AGENT.builtin_tools

    def test_max_iterations_capped(self):
        # PEV self-heal cap — staying ≤5 prevents pathological cost loops.
        assert SPEC_AGENT.max_iterations <= 5


class TestReviewAgent:
    def test_no_mutation_tools(self):
        # Review must not call generate-bundle or apply-entity-corrections.
        forbidden = {"generate-bundle", "apply-entity-corrections", "upload-bundle"}
        assert forbidden.isdisjoint(set(REVIEW_AGENT.mcp_tool_names))

    def test_uses_cheaper_model(self):
        # Review is verification — Sonnet, not Opus.
        assert "sonnet" in REVIEW_AGENT.model.lower()


class TestErrorAgent:
    def test_includes_upload_status(self):
        assert "upload-status" in ERROR_AGENT.mcp_tool_names

    def test_one_retry_only(self):
        # error_agent.md says "one automatic retry only"; iter cap matches.
        assert ERROR_AGENT.max_iterations <= 3


class TestWithSkillIds:
    def test_replaces_skills_without_mutating_original(self):
        original = SPEC_AGENT
        new = with_skill_ids(original, ("skill_abc", "skill_def"))
        assert original.skill_ids == ()
        assert new.skill_ids == ("skill_abc", "skill_def")
        # Other fields unchanged
        assert new.role == original.role
        assert new.system_prompt == original.system_prompt
