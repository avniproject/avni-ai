"""Tool wiring tests (Mode 3 - pure YAML parsing, no server).

Validates consistency between:
  - The OpenAPI spec (dify/avni-ai-tools-openapi.yaml)
  - The Dify workflow definition (dify/Avni [Staging] Sub-Agentic Assistant.yml)
  - The FastAPI/Starlette routes in src/main.py

No server is started; these tests parse YAML files and grep source directly.

Requires: pyyaml
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest
import yaml

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
_OPENAPI_PATH = _PROJECT_ROOT / "dify" / "avni-ai-tools-openapi.yaml"
_WORKFLOW_PATH = _PROJECT_ROOT / "dify" / "Avni [Staging] Sub-Agentic Assistant.yml"
_MAIN_PY_PATH = _PROJECT_ROOT / "src" / "main.py"

EXPECTED_PROVIDER_ID = "fa71db84-aa31-44cc-95a2-6b5b7961a51e"

# Tools that are legitimately not assigned to any agent (infrastructure tools)
ALLOWED_ORPHAN_TOOLS = {
    "parse_srs_file",
    "store_auth_token",
    "store_entities",  # used by orchestrator directly
    "validate_entities",
    "get_srs_text",
    "apply_entity_corrections",
    "get_existing_config",
    "generate_spec",
    "get_spec",
    "get_spec_section",
    "update_spec_section",
    "get_entities_section",
    "update_entities_section",
    "resolve_ambiguities",
    "get_ambiguities",
    "chat_srs_init_session",
    "chat_srs_update_section",
    "chat_srs_build_entities",
    "validate_spec",
    "spec_to_entities",
    "bundle_to_spec",
}

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _load_yaml(path: Path) -> dict:
    with open(path, "r") as f:
        return yaml.safe_load(f)


def _get_openapi_paths(openapi: dict) -> set[str]:
    """Return all path strings from the OpenAPI spec."""
    return set(openapi.get("paths", {}).keys())


def _get_openapi_operation_ids(openapi: dict) -> set[str]:
    """Return all operationId values from the OpenAPI spec."""
    ids: set[str] = set()
    for path_item in openapi.get("paths", {}).values():
        for method_obj in path_item.values():
            if isinstance(method_obj, dict) and "operationId" in method_obj:
                ids.add(method_obj["operationId"])
    return ids


def _get_main_py_routes(main_py_text: str) -> set[str]:
    """Extract route path strings from main.py custom_route decorators."""
    routes: set[str] = set()
    # Match patterns like: @server.custom_route("/store-entities", ...)
    for m in re.finditer(r'custom_route\(\s*"([^"]+)"', main_py_text):
        routes.add(m.group(1))
    return routes


def _normalize_path(path: str) -> str:
    """Normalize path for comparison: strip param placeholders to {param}."""
    return re.sub(r"\{[^}]+\}", "{id}", path)


def _extract_agent_tools_from_workflow(workflow: dict) -> dict[str, list[str]]:
    """
    Extract tool names grouped by agent node from the workflow YAML.

    Returns: { agent_node_id: [tool_name, ...], ... }
    """
    agents: dict[str, list[str]] = {}
    nodes = workflow.get("workflow", {}).get("graph", {}).get("nodes", [])
    for node in nodes:
        data = node.get("data", {})
        if data.get("type") == "agent":
            node_id = node.get("id", "unknown")
            # Tools live under data.agent_parameters.tools (Dify workflow format)
            agent_params = data.get("agent_parameters", {})
            tools_spec = agent_params.get("tools", {})
            tool_list = tools_spec.get("value", [])
            if isinstance(tool_list, list):
                names = [
                    t.get("tool_name", "")
                    for t in tool_list
                    if isinstance(t, dict) and t.get("tool_name")
                ]
                agents[node_id] = names
    return agents


def _extract_all_agent_tool_names(workflow: dict) -> set[str]:
    """Return the union of all tool names across every agent node."""
    agents = _extract_agent_tools_from_workflow(workflow)
    all_names: set[str] = set()
    for names in agents.values():
        all_names.update(names)
    return all_names


def _extract_tools_with_cid_wiring(workflow: dict) -> list[dict]:
    """
    Return tool entries that have a conversation_id parameter,
    along with their auto flag and value.
    """
    results: list[dict] = []
    agents = _extract_agent_tools_from_workflow_raw(workflow)
    for agent_id, tools in agents.items():
        for tool in tools:
            params = tool.get("parameters", {})
            if "conversation_id" in params:
                cid_param = params["conversation_id"]
                results.append(
                    {
                        "agent": agent_id,
                        "tool_name": tool.get("tool_name", ""),
                        "auto": cid_param.get("auto"),
                        "value": cid_param.get("value", {}),
                    }
                )
    return results


def _extract_agent_tools_from_workflow_raw(workflow: dict) -> dict[str, list[dict]]:
    """Extract raw tool dicts grouped by agent node."""
    agents: dict[str, list[dict]] = {}
    nodes = workflow.get("workflow", {}).get("graph", {}).get("nodes", [])
    for node in nodes:
        data = node.get("data", {})
        if data.get("type") == "agent":
            node_id = node.get("id", "unknown")
            agent_params = data.get("agent_parameters", {})
            tools_spec = agent_params.get("tools", {})
            tool_list = tools_spec.get("value", [])
            if isinstance(tool_list, list):
                agents[node_id] = [t for t in tool_list if isinstance(t, dict)]
    return agents


def _extract_all_provider_names(workflow: dict) -> set[str]:
    """Return all unique provider_name values from agent tool entries."""
    providers: set[str] = set()
    agents = _extract_agent_tools_from_workflow_raw(workflow)
    for tools in agents.values():
        for tool in tools:
            pn = tool.get("provider_name", "")
            if pn:
                providers.add(pn)
    return providers


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def openapi() -> dict:
    assert _OPENAPI_PATH.exists(), f"OpenAPI spec not found: {_OPENAPI_PATH}"
    return _load_yaml(_OPENAPI_PATH)


@pytest.fixture(scope="module")
def workflow() -> dict:
    assert _WORKFLOW_PATH.exists(), f"Workflow YAML not found: {_WORKFLOW_PATH}"
    return _load_yaml(_WORKFLOW_PATH)


@pytest.fixture(scope="module")
def main_py_text() -> str:
    assert _MAIN_PY_PATH.exists(), f"main.py not found: {_MAIN_PY_PATH}"
    return _MAIN_PY_PATH.read_text()


# ===========================================================================
# Tests
# ===========================================================================


class TestOpenApiOperationsMatchRoutes:
    """Every OpenAPI path should have a corresponding backend route in main.py."""

    def test_openapi_paths_have_backend_routes(self, openapi: dict, main_py_text: str):
        openapi_paths = _get_openapi_paths(openapi)
        backend_routes = _get_main_py_routes(main_py_text)

        # Normalize both sets for comparison (collapse path params)
        normalized_openapi = {_normalize_path(p) for p in openapi_paths}
        normalized_backend = {_normalize_path(r) for r in backend_routes}

        missing = normalized_openapi - normalized_backend
        assert not missing, (
            f"OpenAPI paths without backend routes: {sorted(missing)}. "
            f"Backend has: {sorted(normalized_backend)}"
        )


class TestAgentToolsExistInOpenapi:
    """Every tool_name referenced by any of the 6 agents must exist as an
    operationId in the OpenAPI spec."""

    def test_all_agent_tools_in_openapi(self, openapi: dict, workflow: dict):
        openapi_ids = _get_openapi_operation_ids(openapi)
        agent_tools = _extract_all_agent_tool_names(workflow)

        missing = agent_tools - openapi_ids
        assert not missing, (
            f"Agent tools not found in OpenAPI operationIds: {sorted(missing)}. "
            f"Available operationIds: {sorted(openapi_ids)}"
        )


class TestNoOrphanTools:
    """Warn about OpenAPI operations that are not used by any agent.
    Allowed orphans (infrastructure tools) are excluded from the check."""

    def test_no_unexpected_orphan_tools(self, openapi: dict, workflow: dict):
        openapi_ids = _get_openapi_operation_ids(openapi)
        agent_tools = _extract_all_agent_tool_names(workflow)

        orphans = openapi_ids - agent_tools - ALLOWED_ORPHAN_TOOLS
        if orphans:
            # This is a warning, not a hard failure -- but flag it
            import warnings

            warnings.warn(
                f"OpenAPI tools not used by any agent (and not in allow-list): "
                f"{sorted(orphans)}"
            )
        # The set of truly unexpected orphans should be small
        assert len(orphans) <= 5, (
            f"Too many orphan tools ({len(orphans)}): {sorted(orphans)}. "
            "Add them to ALLOWED_ORPHAN_TOOLS if intentional."
        )


class TestConversationIdHardwiring:
    """Tools that take a conversation_id parameter should have auto:0
    with a hardwired value of {{#sys.conversation_id#}} so Dify injects
    the conversation ID automatically via template variable."""

    def test_tools_with_cid_have_auto_0(self, workflow: dict):
        cid_tools = _extract_tools_with_cid_wiring(workflow)

        # There should be at least some tools with conversation_id
        assert len(cid_tools) > 0, "No tools found with conversation_id parameter"

        bad_tools: list[str] = []
        for entry in cid_tools:
            if entry["auto"] != 0:
                bad_tools.append(
                    f"{entry['tool_name']} in agent {entry['agent']} "
                    f"has auto={entry['auto']} (expected 0)"
                )

        assert not bad_tools, (
            "Tools with conversation_id not set to auto:0:\n" + "\n".join(bad_tools)
        )

    def test_cid_value_is_sys_conversation_id(self, workflow: dict):
        """With auto:0, value should be the sys.conversation_id template variable."""
        cid_tools = _extract_tools_with_cid_wiring(workflow)

        bad_tools: list[str] = []
        for entry in cid_tools:
            value = entry.get("value")
            expected = {"type": "mixed", "value": "{{#sys.conversation_id#}}"}
            if value != expected:
                bad_tools.append(
                    f"{entry['tool_name']}: value={value} (expected {expected})"
                )

        assert not bad_tools, (
            "Tools with conversation_id should have sys.conversation_id value:\n"
            + "\n".join(bad_tools)
        )


class TestToolProviderConsistency:
    """All agent tools should use the same provider ID."""

    def test_all_tools_use_expected_provider(self, workflow: dict):
        providers = _extract_all_provider_names(workflow)

        # Filter to only the openapi tool provider (exclude agent strategy providers)
        assert EXPECTED_PROVIDER_ID in providers, (
            f"Expected provider {EXPECTED_PROVIDER_ID} not found. "
            f"Found providers: {sorted(providers)}"
        )

        # Check that there are no unexpected providers
        unexpected = providers - {EXPECTED_PROVIDER_ID}
        if unexpected:
            import warnings

            warnings.warn(
                f"Additional providers found besides the expected one: "
                f"{sorted(unexpected)}"
            )

    def test_every_tool_entry_has_expected_provider(self, workflow: dict):
        agents = _extract_agent_tools_from_workflow_raw(workflow)
        bad_tools: list[str] = []

        for agent_id, tools in agents.items():
            for tool in tools:
                pn = tool.get("provider_name", "")
                tool_name = tool.get("tool_name", "unknown")
                if pn != EXPECTED_PROVIDER_ID:
                    bad_tools.append(
                        f"{tool_name} in agent {agent_id}: "
                        f"provider={pn} (expected {EXPECTED_PROVIDER_ID})"
                    )

        assert not bad_tools, "Tools with incorrect provider_name:\n" + "\n".join(
            bad_tools
        )
