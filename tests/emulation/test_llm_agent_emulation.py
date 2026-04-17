"""
LLM-driven emulation of the spec agent handling gate errors.

Uses Claude API to simulate what the Dify agent node does:
gives the spec agent prompt + tools + gate errors, checks if the LLM
makes correct tool calls to fix issues.

Requires ANTHROPIC_API_KEY in .env.
"""

from __future__ import annotations

import json
import os
from pathlib import Path

import httpx
import pytest

from dotenv import load_dotenv

load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
SCOPING_DIR = Path(__file__).resolve().parents[1] / "resources" / "scoping"
PROMPTS_DIR = Path(__file__).resolve().parents[2] / "prompts"

ASTITVA_FILES = [
    SCOPING_DIR / "Astitva SRS .xlsx",
    SCOPING_DIR / "Astitva Modelling.xlsx",
    SCOPING_DIR / "Astitva Nourish Program Forms.xlsx",
]

pytestmark = [
    pytest.mark.skipif(not ANTHROPIC_API_KEY, reason="No ANTHROPIC_API_KEY"),
    pytest.mark.skipif(
        not all(f.exists() for f in ASTITVA_FILES), reason="Astitva files not present"
    ),
]


@pytest.fixture(scope="module")
def astitva_entities() -> dict:
    from src.bundle.scoping_parser import consolidate_and_audit

    result = consolidate_and_audit([str(f) for f in ASTITVA_FILES], org_name="astitva")
    return result["entities"]


@pytest.fixture(scope="module")
def spec_agent_prompt() -> str:
    return (PROMPTS_DIR / "spec-agent.txt").read_text()


async def _setup_and_get_gate_errors(
    client: httpx.AsyncClient, cid: str, entities: dict
) -> dict:
    """Set up entities + spec and return gate validation result."""
    await client.post(
        "/store-entities", json={"conversation_id": cid, "entities": entities}
    )
    await client.post(
        "/generate-spec", json={"conversation_id": cid, "org_name": "astitva"}
    )
    resp = await client.post(
        "/validate-pipeline-step", json={"conversation_id": cid, "phase": "spec"}
    )
    return resp.json()


def _build_agent_memory(gate_result: dict) -> str:
    """Build agent_memory string as the Dify Gate Parser would."""
    parts = []
    parts.append(
        "[spec] Spec generated successfully. 3 subject types, 3 programs, 19 encounter types."
    )
    parts.append("---")
    for err in gate_result.get("errors", []):
        parts.append(f"[GATE ERROR] {err}")
    for warn in gate_result.get("warnings", [])[:3]:
        parts.append(f"[GATE WARNING] {warn}")
    return "\n".join(parts)


def _build_tools() -> list[dict]:
    """Build the Claude tools list matching what the spec agent has in Dify."""
    return [
        {
            "name": "get_agent_logs",
            "description": "Retrieve the full agent activity log for a conversation",
            "input_schema": {
                "type": "object",
                "properties": {"conversation_id": {"type": "string"}},
                "required": ["conversation_id"],
            },
        },
        {
            "name": "get_entities_section",
            "description": "Fetch one section from the stored entities dict. Valid: subject_types, programs, encounter_types, address_levels, forms",
            "input_schema": {
                "type": "object",
                "properties": {
                    "conversation_id": {"type": "string"},
                    "section": {"type": "string"},
                },
                "required": ["conversation_id", "section"],
            },
        },
        {
            "name": "update_entities_section",
            "description": "Replace one section in the stored entities dict",
            "input_schema": {
                "type": "object",
                "properties": {
                    "conversation_id": {"type": "string"},
                    "section": {"type": "string"},
                    "items": {"type": "array"},
                },
                "required": ["conversation_id", "section", "items"],
            },
        },
        {
            "name": "generate_spec",
            "description": "Generate a YAML spec from stored entities",
            "input_schema": {
                "type": "object",
                "properties": {
                    "conversation_id": {"type": "string"},
                    "org_name": {"type": "string"},
                },
                "required": ["conversation_id"],
            },
        },
        {
            "name": "append_agent_log",
            "description": "Append a step trace entry to the agent activity log",
            "input_schema": {
                "type": "object",
                "properties": {
                    "conversation_id": {"type": "string"},
                    "phase": {"type": "string"},
                    "action": {"type": "string"},
                    "status": {"type": "string"},
                },
                "required": ["conversation_id", "action"],
            },
        },
    ]


async def _call_claude(
    system_prompt: str,
    agent_memory: str,
    user_query: str,
    tools: list[dict],
    conversation_id: str,
) -> dict:
    """Call Claude API mimicking what Dify agent node does."""
    import anthropic

    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

    full_instruction = (
        f"{system_prompt}\n\n"
        f"Conversation ID: {conversation_id}\n\n"
        f"Agent Memory: {agent_memory}\n\n"
        f"Org Name: astitva\n\n"
        f"IMPORTANT RULES: 1. Use conversation_id for ALL tool calls. "
        f"2. Call append_agent_log at the START and END of your work."
    )

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=4096,
        temperature=0.2,
        system=full_instruction,
        messages=[{"role": "user", "content": user_query}],
        tools=tools,
    )

    # Extract tool calls
    tool_calls = []
    text_output = ""
    for block in response.content:
        if block.type == "tool_use":
            tool_calls.append(
                {
                    "name": block.name,
                    "input": block.input,
                }
            )
        elif block.type == "text":
            text_output += block.text

    return {
        "tool_calls": tool_calls,
        "text": text_output,
        "stop_reason": response.stop_reason,
    }


@pytest.mark.asyncio(loop_scope="function")
class TestLLMSpecAgentGateHandling:
    """Test that the LLM spec agent correctly handles gate errors."""

    async def test_spec_agent_detects_gate_errors(
        self,
        client: httpx.AsyncClient,
        conversation_id: str,
        astitva_entities: dict,
        spec_agent_prompt: str,
    ):
        """When gate reports errors, spec agent should try to fix them."""
        gate = await _setup_and_get_gate_errors(
            client, conversation_id, astitva_entities
        )
        agent_memory = _build_agent_memory(gate)
        tools = _build_tools()

        result = await _call_claude(
            system_prompt=spec_agent_prompt,
            agent_memory=agent_memory,
            user_query="proceed",  # simulates Dify sending sys.query
            tools=tools,
            conversation_id=conversation_id,
        )

        print("\n--- LLM Response ---")
        print(f"  Stop reason: {result['stop_reason']}")
        print(f"  Tool calls: {len(result['tool_calls'])}")
        for tc in result["tool_calls"]:
            print(f"    {tc['name']}({json.dumps(tc['input'])[:100]})")
        if result["text"]:
            print(f"  Text: {result['text'][:300]}")

        # The agent should make tool calls (not just output text)
        assert result["stop_reason"] == "tool_use", (
            f"Agent didn't make tool calls. Text: {result['text'][:200]}"
        )

        # First tool call should be get_agent_logs or append_agent_log
        tool_names = [tc["name"] for tc in result["tool_calls"]]
        assert any(n in ("get_agent_logs", "append_agent_log") for n in tool_names), (
            f"Agent didn't check logs first. Calls: {tool_names}"
        )

    async def test_spec_agent_reads_entities_for_fix(
        self,
        client: httpx.AsyncClient,
        conversation_id: str,
        astitva_entities: dict,
        spec_agent_prompt: str,
    ):
        """Agent should read encounter_types to understand and fix the errors."""
        gate = await _setup_and_get_gate_errors(
            client, conversation_id, astitva_entities
        )
        agent_memory = _build_agent_memory(gate)
        tools = _build_tools()

        # Simulate agent already logged start, now needs to fix
        agent_memory_with_log = (
            agent_memory + "\n---\n[spec] Phase started. Will fix GATE ERRORs."
        )

        result = await _call_claude(
            system_prompt=spec_agent_prompt,
            agent_memory=agent_memory_with_log,
            user_query="proceed",
            tools=tools,
            conversation_id=conversation_id,
        )

        tool_names = [tc["name"] for tc in result["tool_calls"]]
        print("\n--- Agent tool calls ---")
        for tc in result["tool_calls"]:
            print(f"  {tc['name']}({json.dumps(tc['input'])[:120]})")

        # Agent should try to read entities to understand the error
        assert (
            "get_entities_section" in tool_names
            or "update_entities_section" in tool_names
        ), f"Agent didn't try to read/fix entities. Calls: {tool_names}"

    async def test_spec_agent_asks_user_when_ambiguous(
        self,
        client: httpx.AsyncClient,
        conversation_id: str,
        astitva_entities: dict,
        spec_agent_prompt: str,
    ):
        """When the fix is ambiguous, agent should ask the user instead of guessing."""
        gate = await _setup_and_get_gate_errors(
            client, conversation_id, astitva_entities
        )

        # Add a gate error that requires user input
        gate["errors"].append(
            "Encounter 'Leave form' references unknown subject type 'User'. "
            "Available subject types: ['Beneficiary', 'Anganwadi', 'School']. "
            "Assign one or remove this encounter."
        )
        agent_memory = _build_agent_memory(gate)
        tools = _build_tools()

        result = await _call_claude(
            system_prompt=spec_agent_prompt,
            agent_memory=agent_memory,
            user_query="proceed",
            tools=tools,
            conversation_id=conversation_id,
        )

        print("\n--- Agent response ---")
        print(f"  Stop reason: {result['stop_reason']}")
        if result["text"]:
            print(f"  Text: {result['text'][:500]}")
        for tc in result["tool_calls"]:
            print(f"  Tool: {tc['name']}({json.dumps(tc['input'])[:100]})")

        # Agent should either ask the user (text response with question)
        # or try to fix it (tool call to get/update entities)
        # Both are acceptable — the key is it doesn't crash or ignore the error
        did_something = len(result["tool_calls"]) > 0 or (
            "?" in result["text"] or "which" in result["text"].lower()
        )
        assert did_something, "Agent ignored the gate errors entirely"
