"""Unit tests for the contracts module — types, defaults, env wiring."""

from __future__ import annotations

import os
from unittest import mock

from src.orchestrators.claude_agent.contracts import (
    AgentMetrics,
    AgentRole,
    AgentSpec,
    ClarificationRequest,
    ClarificationResponse,
    OrchestratorConfig,
    SpikeError,
)


class TestOrchestratorConfig:
    def test_from_env_uses_defaults_when_unset(self):
        # Deliberately blank the env to test the fallback path.
        with mock.patch.dict(os.environ, {}, clear=True):
            cfg = OrchestratorConfig.from_env()
        assert cfg.avni_mcp_url == "http://localhost:8023/mcp"
        assert cfg.avni_auth_token == ""
        assert cfg.anthropic_api_key == ""
        assert cfg.model_default == "claude-opus-4-5"

    def test_from_env_reads_each_var(self):
        env = {
            "AVNI_MCP_SERVER_URL": "https://example.test/mcp",
            "AVNI_AUTH_TOKEN": "tok",
            "ANTHROPIC_API_KEY": "ak",
            "AVNI_ORG_NAME": "Acme",
            "AVNI_CLAUDE_MODEL": "claude-sonnet-4-5",
        }
        with mock.patch.dict(os.environ, env, clear=True):
            cfg = OrchestratorConfig.from_env()
        assert cfg.avni_mcp_url == "https://example.test/mcp"
        assert cfg.avni_auth_token == "tok"
        assert cfg.anthropic_api_key == "ak"
        assert cfg.org_name == "Acme"
        assert cfg.model_default == "claude-sonnet-4-5"

    def test_from_env_overrides_take_precedence(self):
        with mock.patch.dict(os.environ, {"ANTHROPIC_API_KEY": "from-env"}):
            cfg = OrchestratorConfig.from_env(anthropic_api_key="explicit")
        assert cfg.anthropic_api_key == "explicit"

    def test_config_is_frozen(self):
        cfg = OrchestratorConfig(
            avni_mcp_url="x", avni_auth_token="", anthropic_api_key=""
        )
        # Frozen dataclass: assigning to a field raises FrozenInstanceError.
        try:
            cfg.avni_mcp_url = "y"  # type: ignore[misc]
        except Exception as e:  # noqa: BLE001
            assert (
                "frozen" in str(e).lower() or "FrozenInstanceError" in type(e).__name__
            )


class TestAgentSpec:
    def test_defaults(self):
        spec = AgentSpec(
            role=AgentRole.SPEC,
            name="X",
            model="claude-opus-4-5",
            system_prompt="hi",
        )
        assert spec.builtin_tools == ("read", "glob", "bash")
        assert spec.max_iterations == 5
        assert spec.skill_ids == ()


class TestAgentMetrics:
    def test_latency_is_zero_until_finished(self):
        m = AgentMetrics(runner="managed")
        assert m.latency_s == 0.0
        m.started_at = 100.0
        assert m.latency_s == 0.0
        m.finished_at = 105.5
        assert m.latency_s == 5.5

    def test_negative_durations_clamp_to_zero(self):
        # If finished_at <= 0 we treat it as not-yet-finished, even if
        # started_at is set; protects against partially-populated records.
        m = AgentMetrics(runner="sdk", started_at=10.0, finished_at=0.0)
        assert m.latency_s == 0.0


class TestClarification:
    def test_request_is_immutable(self):
        r = ClarificationRequest(question="?", options=("a", "b"))
        # Frozen
        try:
            r.question = "??"  # type: ignore[misc]
        except Exception as e:  # noqa: BLE001
            assert (
                "frozen" in str(e).lower() or "FrozenInstanceError" in type(e).__name__
            )

    def test_options_default_empty_means_free_text(self):
        r = ClarificationRequest(question="describe the field")
        assert r.options == ()


class TestSpikeError:
    def test_inherits_from_runtime_error(self):
        # Catching RuntimeError must catch SpikeError so existing handlers
        # in callers don't have to know our type.
        try:
            raise SpikeError("boom")
        except RuntimeError as e:
            assert str(e) == "boom"


def test_clarification_response_is_dataclass():
    r = ClarificationResponse(answer="hi")
    assert r.answer == "hi"
