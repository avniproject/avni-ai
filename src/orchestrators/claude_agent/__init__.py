"""
Claude Managed Agents / Agent SDK orchestrator for the Avni App Configurator.

Spike branch (issue avniproject/avni-ai#45). Mirrors the three Dify v3 agent roles
(Spec / Review / Error) but drives them through Anthropic's hosted Managed Agents
API (primary) or the local Claude Agent SDK (parity adapter).

The avni-ai FastMCP server is the single source of bundle-generation logic; this
package contributes only the orchestrator and is a peer of the Dify workflow, not
a replacement for any deterministic generator code.
"""

from .contracts import (
    AgentRole,
    AgentMetrics,
    AgentSpec,
    ClarificationRequest,
    ClarificationResponse,
    OrchestratorConfig,
    RunRecord,
    RunnerProtocol,
    SpikeError,
)

__all__ = [
    "AgentRole",
    "AgentMetrics",
    "AgentSpec",
    "ClarificationRequest",
    "ClarificationResponse",
    "OrchestratorConfig",
    "RunRecord",
    "RunnerProtocol",
    "SpikeError",
]
