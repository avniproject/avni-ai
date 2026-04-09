"""
Interactive prompt tester for the bundle agent.
Simulates what Dify does: stores SRS text server-side, then runs Claude
with the bundle-agent-prompt as system instructions and our custom tools.

Usage:
  uv run python test_prompt.py                    # interactive REPL
  uv run python test_prompt.py --srs path/to.txt  # pre-load SRS from file
"""

import argparse
import json
import os
import sys
import uuid
import httpx
import anthropic
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

SERVER_URL = os.getenv("AVNI_MCP_SERVER_URL", "http://localhost:8023/").rstrip("/")
AUTH_TOKEN = os.getenv("AVNI_AUTH_TOKEN", "")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")

PROMPT_FILE = Path(__file__).parent / "bundle-agent-prompt.txt"
OPENAPI_FILE = Path(__file__).parent / "dify" / "avni-ai-tools-openapi.yaml"


# ---------------------------------------------------------------------------
# Tool executor — calls local server endpoints
# ---------------------------------------------------------------------------

def _call(method: str, path: str, **kwargs) -> dict:
    url = f"{SERVER_URL}{path}"
    r = httpx.request(method, url, timeout=120, **kwargs)
    try:
        return r.json()
    except Exception:
        return {"raw": r.text, "status": r.status_code}


def execute_tool(name: str, args: dict) -> str:
    """Route a tool call to the local server and return JSON string result."""
    try:
        if name == "get_srs_text":
            result = _call("GET", "/get-srs-text", params=args)
        elif name == "store_entities":
            result = _call("POST", "/store-entities", json=args)
        elif name == "validate_entities":
            result = _call("POST", "/validate-entities", json=args)
        elif name == "generate_spec":
            result = _call("POST", "/generate-spec", json=args)
        elif name == "get_spec":
            result = _call("GET", "/get-spec", params=args)
        elif name == "get_spec_section":
            result = _call("GET", "/spec-section", params=args)
        elif name == "update_spec_section":
            result = _call("PUT", "/spec-section", json=args)
        elif name == "get_entities_section":
            result = _call("GET", "/entities-section", params=args)
        elif name == "update_entities_section":
            result = _call("PUT", "/entities-section", json=args)
        elif name == "apply_entity_corrections":
            result = _call("POST", "/apply-entity-corrections", json=args)
        elif name == "generate_bundle":
            result = _call("POST", "/generate-bundle", json=args)
        elif name == "validate_bundle":
            result = _call("POST", "/validate-bundle", json=args)
        elif name == "get_bundle_files":
            result = _call("GET", "/bundle-files", params=args)
        elif name == "get_bundle_file":
            result = _call("GET", "/bundle-file", params=args)
        elif name == "put_bundle_file":
            result = _call("PUT", "/bundle-file", json=args)
        elif name == "upload_bundle":
            result = _call("POST", "/upload-bundle", json=args)
        elif name == "upload_status":
            task_id = args.get("task_id", "")
            result = _call("GET", f"/upload-status/{task_id}")
        elif name == "store_auth_token":
            result = _call("POST", "/store-auth-token", json=args)
        elif name == "download_bundle_b64":
            result = _call("GET", "/download-bundle-b64", params=args)
        elif name == "patch_bundle":
            result = _call("POST", "/patch-bundle", json=args)
        elif name == "bundle_to_spec":
            result = _call("POST", "/bundle-to-spec", json=args)
        elif name == "validate_spec":
            result = _call("POST", "/validate-spec", json=args)
        elif name == "spec_to_entities":
            result = _call("POST", "/spec-to-entities", json=args)
        elif name == "execute_python":
            result = _call("POST", "/execute-python", json=args)
        elif name == "get_existing_config":
            result = _call("GET", "/api/existing-config", params=args)
        else:
            result = {"error": f"Unknown tool: {name}"}
    except Exception as e:
        result = {"error": str(e)}

    return json.dumps(result)


# ---------------------------------------------------------------------------
# Build tool definitions from OpenAPI spec
# ---------------------------------------------------------------------------

def _build_tools() -> list[dict]:
    """Build Anthropic tool definitions from the OpenAPI spec."""
    import yaml
    spec = yaml.safe_load(OPENAPI_FILE.read_text())

    tools = []
    for path, methods in spec.get("paths", {}).items():
        for method, op in methods.items():
            if method not in ("get", "post", "put"):
                continue
            op_id = op.get("operationId")
            if not op_id:
                continue

            desc = op.get("summary", op.get("description", ""))
            if op.get("description") and op.get("description") != desc:
                desc = f"{desc}\n\n{op['description']}"

            # Build input schema from params + requestBody
            props = {}
            required = []

            for param in op.get("parameters", []):
                props[param["name"]] = {
                    "type": param.get("schema", {}).get("type", "string"),
                    "description": param.get("description", ""),
                }
                if param.get("required"):
                    required.append(param["name"])

            body = op.get("requestBody", {})
            body_schema = (
                body.get("content", {})
                    .get("application/json", {})
                    .get("schema", {})
            )
            for prop, pdef in body_schema.get("properties", {}).items():
                props[prop] = {k: v for k, v in pdef.items() if k != "required"}
            required += body_schema.get("required", [])

            tools.append({
                "name": op_id,
                "description": desc.strip(),
                "input_schema": {
                    "type": "object",
                    "properties": props,
                    "required": list(dict.fromkeys(required)),  # dedup
                },
            })
    return tools


# ---------------------------------------------------------------------------
# Agentic loop
# ---------------------------------------------------------------------------

def run_agent(conversation_id: str, messages: list[dict], system: str, tools: list[dict]) -> str:
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    turn = 0

    while True:
        turn += 1
        print(f"\n[turn {turn}] calling Claude...", flush=True)

        with client.messages.stream(
            model="claude-opus-4-6",
            max_tokens=16384,
            system=system,
            messages=messages,
            tools=tools,
            thinking={"type": "adaptive"},
        ) as stream:
            response = stream.get_final_message()

        # Collect text for display
        text_parts = []
        for block in response.content:
            if block.type == "text":
                text_parts.append(block.text)

        if text_parts:
            print("\n[assistant]", " ".join(text_parts), flush=True)

        messages.append({"role": "assistant", "content": response.content})

        if response.stop_reason == "end_turn":
            return " ".join(text_parts)

        # Execute tool calls
        tool_results = []
        for block in response.content:
            if block.type != "tool_use":
                continue
            print(f"\n[tool] {block.name}({json.dumps(block.input, indent=2)[:300]})", flush=True)
            result = execute_tool(block.name, block.input)
            print(f"[result] {result[:500]}", flush=True)
            tool_results.append({
                "type": "tool_result",
                "tool_use_id": block.id,
                "content": result,
            })

        if not tool_results:
            break

        messages.append({"role": "user", "content": tool_results})

    return ""


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Test bundle agent prompt interactively")
    parser.add_argument("--srs", help="Path to SRS text file to pre-load")
    args = parser.parse_args()

    if not ANTHROPIC_API_KEY:
        print("ERROR: ANTHROPIC_API_KEY not set in environment")
        sys.exit(1)

    conversation_id = str(uuid.uuid4())
    print(f"Conversation ID: {conversation_id}")
    print(f"Server: {SERVER_URL}")

    # Store auth token
    r = _call("POST", "/store-auth-token", json={
        "conversation_id": conversation_id,
        "auth_token": AUTH_TOKEN,
    })
    print(f"Auth stored: {r}")

    # Pre-load SRS text if provided
    if args.srs:
        srs_text = Path(args.srs).read_text()
        r = _call("POST", "/store-srs-text", json={
            "conversation_id": conversation_id,
            "srs_text": srs_text,
        })
        print(f"SRS text stored: {r}")

    # Build system prompt
    prompt_body = PROMPT_FILE.read_text()
    system = f"""You are the AVNI SRS Bundle Generator Agent. You help users create complete AVNI configuration bundles from SRS specifications.

Conversation ID: {conversation_id}

IMPORTANT: Use conversation_id (= {conversation_id}) for ALL tool calls that need it.

CRITICAL TOOL-CALL RULES (these override any conflicting instructions below):

RULE 1 — FIRST TOOL CALL IS ALWAYS get_srs_text: At the very start of EVERY new SRS processing task, your first tool call MUST be get_srs_text(conversation_id). Do not show a plan, do not ask the user anything, do not say "let me retrieve" — just call the tool immediately. If it returns ok (200), use the srs_text field as your SRS input. If it returns 404 (no file uploaded), only then ask the user to paste the SRS text. After retrieving the text, call store_entities, then validate_entities, then generate_spec, then get_spec IN SEQUENCE without pausing. Only after get_spec returns do you show spec_yaml and ask for approval.

RULE 2 — generate_bundle uses conversation_id ONLY: When the user approves the spec, call generate_bundle(conversation_id) without any entities field. Entities are already in the server store from RULE 1.

RULE 3 — validate_bundle uses conversation_id ONLY: Call validate_bundle(conversation_id). Do NOT pass bundle_zip_b64.

RULE 4 — upload_bundle uses conversation_id ONLY: Call upload_bundle(conversation_id). Do NOT pass bundle_zip_b64.

{prompt_body}"""

    tools = _build_tools()
    print(f"Loaded {len(tools)} tools from OpenAPI spec")

    messages = []
    print("\nReady. Type your message (or 'quit' to exit).\n")

    while True:
        try:
            user_input = input("you> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting.")
            break

        if user_input.lower() in ("quit", "exit", "q"):
            break
        if not user_input:
            continue

        messages.append({"role": "user", "content": user_input})
        run_agent(conversation_id, messages, system, tools)


if __name__ == "__main__":
    main()
