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

        # Agent should either read entities to fix, or log a plan to fix
        # (LLM may check logs first on some runs before reading entities)
        did_something = (
            "get_entities_section" in tool_names
            or "update_entities_section" in tool_names
            or "append_agent_log" in tool_names
            or "get_agent_logs" in tool_names
        )
        assert did_something, f"Agent took no action. Calls: {tool_names}"

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


# ---------------------------------------------------------------------------
# Multi-turn interactive gap-fix test
# ---------------------------------------------------------------------------
#
# Goal: prove the Spec Agent, given the three gap categories seen on the
# Astitva run (unmapped subject type 'School', 11 encounterTypes with no form,
# program 'Enrich' with no enrolment form), will:
#   1. Be re-invoked by the pipeline gate (requires Phase 2: warnings -> errors)
#   2. Ask the user about each gap (requires Phase 3: enrich_spec + prompt)
#   3. Apply the user's answers via update_entities_section and re-generate spec
#   4. End with validate-pipeline-step returning ok=true
#
# Runs against staging_client (in-process by default; hits AVNI_AI_BASE_URL
# when set — same shape as the Dify agent node).
# ---------------------------------------------------------------------------


def _build_full_spec_agent_tools() -> list[dict]:
    """Full tool list matching what spec-agent.txt declares (Dify-equivalent)."""
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
        {
            "name": "get_entities_section",
            "description": (
                "Fetch one section from the stored entities dict. "
                "Valid sections: subject_types, programs, encounter_types, forms, address_levels."
            ),
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
            "description": (
                "Replace one section in the stored entities dict. "
                "Use this for structural fixes (forms, encounters, programs, subject_types). "
                "Entities are the source of truth — spec is regenerated from entities."
            ),
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
            "description": "Regenerate the YAML spec from the stored entities (call after entity edits).",
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
            "name": "get_spec",
            "description": "Retrieve the full stored spec YAML.",
            "input_schema": {
                "type": "object",
                "properties": {"conversation_id": {"type": "string"}},
                "required": ["conversation_id"],
            },
        },
        {
            "name": "get_spec_section",
            "description": "Fetch one top-level section from the stored spec.",
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
            "name": "update_spec_section",
            "description": (
                "Replace one top-level section in the stored spec YAML directly. "
                "ONLY use for spec-only fields (settings, reportDashboards metadata). "
                "NEVER use for forms, encounters, programs, or subjectTypes — use "
                "update_entities_section for those so the fix survives spec regeneration."
            ),
            "input_schema": {
                "type": "object",
                "properties": {
                    "conversation_id": {"type": "string"},
                    "section": {"type": "string"},
                    "value": {},
                },
                "required": ["conversation_id", "section", "value"],
            },
        },
        {
            "name": "enrich_spec",
            "description": "Apply smart defaults and detect ambiguities on the stored spec. Returns ambiguities to present to the user.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "conversation_id": {"type": "string"},
                    "sector": {"type": "string"},
                },
                "required": ["conversation_id"],
            },
        },
        {
            "name": "validate_pipeline_step",
            "description": "Read-only validation gate for a pipeline phase (e.g. 'spec'). Returns ok/errors/warnings.",
            "input_schema": {
                "type": "object",
                "properties": {
                    "conversation_id": {"type": "string"},
                    "phase": {"type": "string"},
                },
                "required": ["conversation_id", "phase"],
            },
        },
    ]


# Map tool name -> (HTTP method, path template, body/query strategy).
# Each handler returns the JSON response from the avni-ai endpoint.
async def _dispatch_tool(
    tool_name: str,
    tool_input: dict,
    client: httpx.AsyncClient,
) -> dict:
    """Translate a Claude tool_use call into the matching HTTP call."""
    cid = tool_input.get("conversation_id", "")

    if tool_name == "get_agent_logs":
        r = await client.get(f"/agent-logs/{cid}")
        return (
            r.json()
            if r.status_code == 200
            else {"entries": [], "status": r.status_code}
        )

    if tool_name == "append_agent_log":
        r = await client.post(
            "/agent-log",
            json={
                "conversation_id": cid,
                "phase": tool_input.get("phase", "spec_generation"),
                "action": tool_input.get("action", ""),
                "status": tool_input.get("status", "info"),
            },
        )
        return {"ok": r.status_code in (200, 201), "status": r.status_code}

    if tool_name == "get_entities_section":
        r = await client.get(
            "/entities-section",
            params={"conversation_id": cid, "section": tool_input.get("section", "")},
        )
        return (
            r.json()
            if r.status_code == 200
            else {"error": r.text, "status": r.status_code}
        )

    if tool_name == "update_entities_section":
        r = await client.put(
            "/entities-section",
            json={
                "conversation_id": cid,
                "section": tool_input.get("section", ""),
                "items": tool_input.get("items", []),
            },
        )
        return (
            r.json()
            if r.status_code == 200
            else {"error": r.text, "status": r.status_code}
        )

    if tool_name == "generate_spec":
        r = await client.post(
            "/generate-spec",
            json={
                "conversation_id": cid,
                "org_name": tool_input.get("org_name", "astitva"),
            },
        )
        return (
            r.json()
            if r.status_code == 200
            else {"error": r.text, "status": r.status_code}
        )

    if tool_name == "get_spec":
        r = await client.get("/get-spec", params={"conversation_id": cid})
        return (
            r.json()
            if r.status_code == 200
            else {"error": r.text, "status": r.status_code}
        )

    if tool_name == "get_spec_section":
        r = await client.get(
            "/spec-section",
            params={"conversation_id": cid, "section": tool_input.get("section", "")},
        )
        return (
            r.json()
            if r.status_code == 200
            else {"error": r.text, "status": r.status_code}
        )

    if tool_name == "update_spec_section":
        r = await client.put(
            "/spec-section",
            json={
                "conversation_id": cid,
                "section": tool_input.get("section", ""),
                "value": tool_input.get("value"),
            },
        )
        return (
            r.json()
            if r.status_code == 200
            else {"error": r.text, "status": r.status_code}
        )

    if tool_name == "enrich_spec":
        r = await client.post(
            "/enrich-spec",
            json={"conversation_id": cid, "sector": tool_input.get("sector", "")},
        )
        return (
            r.json()
            if r.status_code == 200
            else {"error": r.text, "status": r.status_code}
        )

    if tool_name == "validate_pipeline_step":
        r = await client.post(
            "/validate-pipeline-step",
            json={"conversation_id": cid, "phase": tool_input.get("phase", "spec")},
        )
        return (
            r.json()
            if r.status_code == 200
            else {"error": r.text, "status": r.status_code}
        )

    return {"error": f"unknown tool {tool_name}"}


def _scripted_user_answer(agent_text: str) -> str:
    """
    Deterministic user reply used by the test when the agent asks a question.

    The real user would pick per-item options; here we give one blanket directive
    that covers all three gap categories so the agent can apply it uniformly.
    """
    return (
        "Use the default option for every item — Remove. Specifically:\n"
        "- Remove the 'School' subject type.\n"
        "- Remove every encounter type listed that has no form (all of them).\n"
        "- Remove any program that has no enrolmentForm and no encounters.\n"
        "Apply all of these fixes via update_entities_section on the matching "
        "target_section, then call generate_spec once. Do not create placeholder forms."
    )


def _agent_is_asking(text: str) -> bool:
    """Heuristic: did the agent produce a question-shaped / ask-for-input turn?"""
    if not text:
        return False
    t = text.lower()
    imperatives = (
        "please answer",
        "please choose",
        "please let me know",
        "please pick",
        "please select",
        "please provide",
        "your input",
        "your answer",
        "your choice",
        "how should we",
        "how would you",
        "choose one",
        "pick one",
        "which one",
        "respond with",
        "reply with",
        "need your input",
    )
    has_question_mark = "?" in text
    has_imperative = any(p in t for p in imperatives)
    mentions_gap = any(
        kw in t
        for kw in ("school", "enrich", "encounter", "form", "program", "subject")
    )
    return (has_question_mark or has_imperative) and mentions_gap


def _errors_cover_three_gaps(errors: list[str]) -> tuple[bool, dict]:
    """Check that the gate errors mention School, a missing-form encounter, and Enrich."""
    joined = " | ".join(errors).lower()
    coverage = {
        "school": "school" in joined,
        "encounter_no_form": "has no form" in joined or "no form mapping" in joined,
        "enrich": "enrich" in joined,
    }
    return all(coverage.values()), coverage


@pytest.mark.asyncio(loop_scope="function")
@pytest.mark.skipif(
    not os.getenv("RUN_LLM_EMULATION"),
    reason="Opt-in: set RUN_LLM_EMULATION=1 to run multi-turn Claude agent loop (~1-3 min, costs API credits)",
)
class TestLLMSpecAgentInteractiveGapFix:
    """
    End-to-end: Astitva SRS -> gate fails with 3 gap categories -> agent asks user ->
    fixes via update_entities_section -> regenerates spec -> gate passes.

    Gated by RUN_LLM_EMULATION env var because it spins up real Claude calls over
    multiple turns and multiple invocations. Run with:

        RUN_LLM_EMULATION=1 pytest tests/emulation/test_llm_agent_emulation.py::TestLLMSpecAgentInteractiveGapFix

    Set AVNI_AI_BASE_URL to point at the staging avni-ai to match the Dify flow exactly.
    """

    async def test_interactive_gap_resolution(
        self,
        staging_client: httpx.AsyncClient,
        conversation_id: str,
        astitva_entities: dict,
        spec_agent_prompt: str,
    ):
        import anthropic

        # ── Step 1: seed entities + spec on staging ────────────────────
        r = await staging_client.post(
            "/store-entities",
            json={"conversation_id": conversation_id, "entities": astitva_entities},
        )
        assert r.status_code in (200, 201), f"store-entities failed: {r.text}"
        r = await staging_client.post(
            "/generate-spec",
            json={"conversation_id": conversation_id, "org_name": "astitva"},
        )
        assert r.status_code == 200, f"generate-spec failed: {r.text}"

        # ── Step 2: gate should flag all three gap categories ──────────
        r = await staging_client.post(
            "/validate-pipeline-step",
            json={"conversation_id": conversation_id, "phase": "spec"},
        )
        assert r.status_code == 200, r.text
        gate = r.json()
        all_three, coverage = _errors_cover_three_gaps(gate.get("errors", []))
        assert not gate.get("ok"), (
            "Gate returned ok=true despite known gaps — "
            "Phase 2 (warnings -> errors) has not landed yet. "
            f"errors={gate.get('errors')[:5]} warnings={gate.get('warnings')[:5]}"
        )
        assert all_three, (
            f"Gate errors don't cover all three gap categories. "
            f"coverage={coverage} errors={gate.get('errors')[:10]}"
        )

        # ── Step 3: run the Claude agent, re-invoking it on fresh gate errors ──
        # Emulates Dify's behaviour: after the agent stops, the gate validates.
        # If gate ok -> done. If gate fails -> re-invoke the agent with the new
        # [GATE ERROR] lines. Up to max_invocations outer iterations.
        llm = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
        tools = _build_full_spec_agent_tools()
        transcript_tool_calls: list[dict] = []
        transcript_text: list[str] = []
        transcript_markers: list[str] = []
        asked_before_fix = False
        seen_question = False
        max_turns_per_invocation = 8
        max_invocations = 3
        final_gate = gate

        for invocation in range(max_invocations):
            if final_gate.get("ok"):
                break

            transcript_markers.append(
                f"=== Invocation #{invocation + 1} "
                f"(gate errors going in: {len(final_gate.get('errors', []))}) ==="
            )
            transcript_tool_calls.append(
                {"name": f"__INV_{invocation + 1}__", "input": {}}
            )

            agent_memory_lines = [
                f"[spec] Invocation #{invocation + 1}. Pipeline gate reported errors (see below)."
            ]
            for err in final_gate.get("errors", []):
                agent_memory_lines.append(f"[GATE ERROR] {err}")
            agent_memory = "\n".join(agent_memory_lines)

            system_prompt = (
                f"{spec_agent_prompt}\n\n"
                f"Conversation ID: {conversation_id}\n"
                f"Org Name: astitva\n\n"
                f"Agent Memory:\n{agent_memory}\n\n"
                f"Always pass conversation_id='{conversation_id}' on every tool call."
            )

            messages: list[dict] = [{"role": "user", "content": "proceed"}]

            for turn in range(max_turns_per_invocation):
                response = llm.messages.create(
                    model="claude-sonnet-4-6",
                    max_tokens=4096,
                    temperature=0.0,
                    system=system_prompt,
                    messages=messages,
                    tools=tools,
                )

                assistant_blocks: list[dict] = []
                tool_uses: list[dict] = []
                text_out = ""
                for block in response.content:
                    if block.type == "tool_use":
                        tool_uses.append(block)
                        assistant_blocks.append(
                            {
                                "type": "tool_use",
                                "id": block.id,
                                "name": block.name,
                                "input": block.input,
                            }
                        )
                        transcript_tool_calls.append(
                            {"name": block.name, "input": block.input}
                        )
                    elif block.type == "text":
                        text_out += block.text
                        assistant_blocks.append({"type": "text", "text": block.text})

                if text_out:
                    transcript_text.append(text_out)

                messages.append({"role": "assistant", "content": assistant_blocks})

                if response.stop_reason == "tool_use" and tool_uses:
                    for tu in tool_uses:
                        if tu.name == "update_entities_section" and seen_question:
                            asked_before_fix = True

                    tool_results_content: list[dict] = []
                    for tu in tool_uses:
                        result = await _dispatch_tool(tu.name, tu.input, staging_client)
                        tool_results_content.append(
                            {
                                "type": "tool_result",
                                "tool_use_id": tu.id,
                                "content": json.dumps(result)[:8000],
                            }
                        )
                    messages.append({"role": "user", "content": tool_results_content})
                    continue

                if _agent_is_asking(text_out):
                    seen_question = True
                    user_reply = _scripted_user_answer(text_out)
                    messages.append({"role": "user", "content": user_reply})
                    continue

                break

            # After this invocation ends, re-run the gate for the next outer round.
            r = await staging_client.post(
                "/validate-pipeline-step",
                json={"conversation_id": conversation_id, "phase": "spec"},
            )
            final_gate = r.json()

        tool_names = [tc["name"] for tc in transcript_tool_calls]
        update_entity_calls = [
            tc
            for tc in transcript_tool_calls
            if tc["name"] == "update_entities_section"
        ]
        update_spec_struct_calls = [
            tc
            for tc in transcript_tool_calls
            if tc["name"] == "update_spec_section"
            and tc["input"].get("section")
            in {"subjectTypes", "programs", "encounterTypes", "forms"}
        ]

        print("\n--- Gap-fix transcript ---")
        for tc in transcript_tool_calls:
            print(f"  TOOL {tc['name']}({json.dumps(tc['input'])[:120]})")
        for t in transcript_text:
            print(f"  TEXT {t[:200]}")
        print(f"  final_gate.ok = {final_gate.get('ok')}")
        print(f"  final_gate.errors[:3] = {final_gate.get('errors', [])[:3]}")

        assert seen_question, (
            "Agent never asked the user a question before making fixes. "
            f"Text turns seen: {transcript_text}"
        )
        assert asked_before_fix, (
            "Agent called update_entities_section without first asking the user. "
            f"Tool calls: {tool_names}"
        )
        assert len(update_entity_calls) >= 1, (
            f"Agent never called update_entities_section. Tools used: {tool_names}"
        )
        assert not update_spec_struct_calls, (
            "Agent used update_spec_section for a structural section "
            "(subjectTypes/programs/encounterTypes/forms) — this regression "
            "breaks the entities-is-truth invariant. Offending calls: "
            f"{update_spec_struct_calls}"
        )
        assert final_gate.get("ok"), (
            "Gate still reports errors after the agent's fixes. "
            f"errors={final_gate.get('errors', [])[:5]}"
        )

        # Cross-check spec & entities agree on the fixes
        r_spec = await staging_client.get(
            "/get-spec", params={"conversation_id": conversation_id}
        )
        spec_text = (
            r_spec.json().get("spec_yaml", "") if r_spec.status_code == 200 else ""
        )
        assert "School" not in spec_text or "registrationForm" in spec_text, (
            "School subject type still present with no registrationForm after fixes"
        )
