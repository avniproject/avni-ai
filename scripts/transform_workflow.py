#!/usr/bin/env python3
"""
Transform the Dify workflow YAML from the existing Assistant into the
Sub-Agentic Assistant with 6 specialized agents in an auto-chain loop.
"""

import yaml
import uuid
import os

# ── Paths ──────────────────────────────────────────────────────────────────
SRC = os.path.join(
    os.path.dirname(__file__),
    "..",
    "dify",
    "Avni [Staging] Assistant [Do Not Touch].yml",
)
DST = os.path.join(
    os.path.dirname(__file__), "..", "dify", "Avni [Staging] Sub-Agentic Assistant.yml"
)

# ── Constants ──────────────────────────────────────────────────────────────
PROVIDER_ID = "7f9b21ca-bafb-43f6-8294-4357a954d50d"
PROVIDER_SHOW = "Avni AI Staging NoAuth openapi"
PLUGIN_UID = "langgenius/agent:0.0.14@26958a0e80a10655ce73812bdb7c35a66ce7b16f5ac346d298bda17ff85efd1e"
PROMPT_BASE = "https://raw.githubusercontent.com/avniproject/avni-ai/refs/heads/app-configurator-dev/prompts/"
LOOP_ID = "1800000000700"

NODES_TO_REMOVE = {
    "17756450495350",
    "17756450495361",
    "1775658332808",
    "1775646587226",
    "17580163919060",
    "1760358453289",
    "1760358474156",
    "1760416664434",
    "1760423058735",
    "1760423058735start",
    "1760423070414",
    "1760423078948",
    "1760424086059",
    "1760424123324",
    "1760424043492",
    "1760426022942",
    "1760434909468",
    "1763959812229",
}

CONV_VARS_TO_REMOVE = {"loop", "setup_mode_active"}

NEW_CONV_VARS = [
    {"name": "active_agent", "value": "", "value_type": "string"},
    {"name": "current_phase", "value": "", "value_type": "string"},
    {"name": "agent_memory", "value": [], "value_type": "array[object]"},
    {"name": "spec_complete", "value": False, "value_type": "boolean"},
    {"name": "bundle_complete", "value": True, "value_type": "boolean"},
    {"name": "agent_loop_active", "value": True, "value_type": "boolean"},
    {"name": "workflow_mode", "value": "", "value_type": "string"},
]

# Agent definitions: (id, title, max_iter, prompt_fetch_id, prompt_file, tools)
AGENTS = [
    (
        "1800000000110",
        "Spec Agent",
        5,
        "1800000000101",
        "spec-agent.txt",
        [
            "get_srs_text",
            "store_entities",
            "validate_entities",
            "apply_entity_corrections",
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
            "append_agent_log",
        ],
    ),
    (
        "1800000000210",
        "Bundle Config Agent",
        10,
        "1800000000201",
        "bundle-config-agent.txt",
        [
            "generate_bundle",
            "validate_bundle",
            "patch_bundle",
            "get_bundle_files",
            "get_bundle_file",
            "put_bundle_file",
            "download_bundle_b64",
            "generate_form",
            "suggest_form_fields",
            "generate_skip_logic",
            "execute_python",
            "read_silo_file",
            "upload_bundle",
            "append_agent_log",
        ],
    ),
    (
        "1800000000310",
        "Rules Agent",
        5,
        "1800000000301",
        "rules-agent.txt",
        [
            "generate_rule",
            "validate_rule",
            "get_bundle_file",
            "put_bundle_file",
            "execute_python",
            "append_agent_log",
        ],
    ),
    (
        "1800000000410",
        "Reports Agent",
        5,
        "1800000000401",
        "reports-agent.txt",
        [
            "generate_report_cards",
            "suggest_dashboard",
            "get_bundle_file",
            "put_bundle_file",
            "execute_python",
            "append_agent_log",
        ],
    ),
    (
        "1800000000510",
        "Config Inspector",
        3,
        "1800000000501",
        "config-inspector-agent.txt",
        [
            "compile_requirements",
            "inspect_config",
            "validate_bundle",
            "get_spec",
            "get_bundle_files",
            "get_bundle_file",
            "append_agent_log",
        ],
    ),
    (
        "1800000000610",
        "Admin Agent",
        10,
        "1800000000601",
        "admin-agent.txt",
        [
            "create_location_type",
            "update_location_type",
            "delete_location_type",
            "get_locations",
            "create_location",
            "update_location",
            "delete_location",
            "get_catchments",
            "create_catchment",
            "update_catchment",
            "delete_catchment",
            "find_user",
            "update_user",
            "delete_implementation",
            "upload_bundle",
            "upload_status",
            "append_agent_log",
        ],
    ),
]

# Prompt fetch definitions: (id, title, file)
PROMPT_FETCHES = [
    ("1800000000101", "SPEC_PROMPT_FETCH", "spec-agent.txt"),
    ("1800000000201", "BUNDLE_CONFIG_PROMPT_FETCH", "bundle-config-agent.txt"),
    ("1800000000301", "RULES_PROMPT_FETCH", "rules-agent.txt"),
    ("1800000000401", "REPORTS_PROMPT_FETCH", "reports-agent.txt"),
    ("1800000000501", "INSPECTOR_PROMPT_FETCH", "config-inspector-agent.txt"),
    ("1800000000601", "ADMIN_PROMPT_FETCH", "admin-agent.txt"),
]

# Dispatcher cases: (case_id, agent_name_value)
DISPATCH_CASES = [
    ("dispatch-spec", "spec"),
    ("dispatch-bundle-config", "bundle_config"),
    ("dispatch-rules", "rules"),
    ("dispatch-reports", "reports"),
    ("dispatch-inspect", "inspect"),
    ("dispatch-admin", "admin"),
]


# ── Helpers ────────────────────────────────────────────────────────────────


def make_uuid():
    return str(uuid.uuid4())


def make_tool_entry(tool_name):
    return {
        "enabled": True,
        "parameters": {
            "conversation_id": {
                "auto": 0,
                "value": {
                    "type": "mixed",
                    "value": "{{#sys.conversation_id#}}",
                },
            },
        },
        "provider_name": PROVIDER_ID,
        "provider_show_name": PROVIDER_SHOW,
        "settings": {},
        "tool_label": tool_name,
        "tool_name": tool_name,
        "type": "api",
    }


def make_edge(
    source,
    source_handle,
    target,
    target_handle,
    source_type,
    target_type,
    in_loop=False,
):
    eid = f"{source}-{source_handle}-{target}-{target_handle}"
    d = {
        "data": {
            "isInLoop": in_loop,
            "sourceType": source_type,
            "targetType": target_type,
        },
        "id": eid,
        "selected": False,
        "source": str(source),
        "sourceHandle": str(source_handle),
        "target": str(target),
        "targetHandle": str(target_handle),
        "type": "custom",
        "zIndex": 1002 if in_loop else 0,
    }
    if in_loop:
        d["data"]["loop_id"] = LOOP_ID
    return d


def loop_node_base(nid, title, ntype, x, y, height=88, width=242, extra_data=None):
    """Create a node dict that lives inside the agent loop."""
    data = {
        "isInLoop": True,
        "loop_id": LOOP_ID,
        "selected": False,
        "title": title,
        "type": ntype,
    }
    if extra_data:
        data.update(extra_data)
    node = {
        "data": data,
        "height": height,
        "id": str(nid),
        "parentId": LOOP_ID,
        "position": {"x": x, "y": y},
        "positionAbsolute": {"x": 2200 + x, "y": 400 + y},
        "selected": False,
        "sourcePosition": "right",
        "targetPosition": "left",
        "type": "custom",
        "width": width,
        "zIndex": 1002,
    }
    return node


def outside_node(nid, title, ntype, x, y, height=88, width=242, extra_data=None):
    data = {
        "selected": False,
        "title": title,
        "type": ntype,
    }
    if extra_data:
        data.update(extra_data)
    return {
        "data": data,
        "height": height,
        "id": str(nid),
        "position": {"x": x, "y": y},
        "positionAbsolute": {"x": x, "y": y},
        "selected": False,
        "sourcePosition": "right",
        "targetPosition": "left",
        "type": "custom",
        "width": width,
    }


# ── Main transform ────────────────────────────────────────────────────────


def transform():
    with open(SRC, "r") as f:
        doc = yaml.safe_load(f)

    wf = doc["workflow"]

    # ── 1. Update app name ──────────────────────────────────────────────
    doc["app"]["name"] = "Avni [Staging] Sub-Agentic Assistant"

    # ── 2. Conversation variables ────────────────────────────────────────
    wf["conversation_variables"] = [
        cv
        for cv in wf["conversation_variables"]
        if cv["name"] not in CONV_VARS_TO_REMOVE
    ]
    for var in NEW_CONV_VARS:
        wf["conversation_variables"].append(
            {
                "description": "",
                "id": make_uuid(),
                "name": var["name"],
                "selector": ["conversation", var["name"]],
                "value": var["value"],
                "value_type": var["value_type"],
            }
        )

    # ── 3. Remove nodes ─────────────────────────────────────────────────
    wf["graph"]["nodes"] = [
        n for n in wf["graph"]["nodes"] if n["id"] not in NODES_TO_REMOVE
    ]

    # ── 4. Remove edges ─────────────────────────────────────────────────
    def should_remove_edge(e):
        eid = e.get("id", "")
        src = str(e.get("source", ""))
        tgt = str(e.get("target", ""))
        # Remove edges connected to removed nodes
        if src in NODES_TO_REMOVE or tgt in NODES_TO_REMOVE:
            return True
        # Remove edges with specific case handles
        if "case-bundle-setup" in eid:
            return True
        if "00ce954d-b2ca-42aa-b302-dc2c163dd1d0" in eid:
            return True
        return False

    wf["graph"]["edges"] = [
        e for e in wf["graph"]["edges"] if not should_remove_edge(e)
    ]

    # Also remove edges that targeted 1775646587226 from 1775648480416
    # (Store Auth → Bundle Prompt Fetch) — already covered by node removal above

    # ── 5. Modify IF/ELSE Router (1757493270484) ────────────────────────
    for node in wf["graph"]["nodes"]:
        if node["id"] == "1757493270484":
            cases = node["data"]["cases"]
            # Remove case-bundle-setup and 00ce954d cases
            cases[:] = [
                c
                for c in cases
                if c["case_id"]
                not in ("case-bundle-setup", "00ce954d-b2ca-42aa-b302-dc2c163dd1d0")
            ]
            # Add AGENT_WORK case
            cases.append(
                {
                    "case_id": "case-agent-work",
                    "conditions": [
                        {
                            "comparison_operator": "is",
                            "id": make_uuid(),
                            "value": "AGENT_WORK",
                            "varType": "string",
                            "variable_selector": [
                                "1757492907627",
                                "structured_output",
                                "service",
                            ],
                        }
                    ],
                    "id": "case-agent-work",
                    "logical_operator": "and",
                }
            )
            break

    # ── 6. Create new nodes ─────────────────────────────────────────────
    new_nodes = []
    new_edges = []

    # 6a. Set Initial Agent (assigner, outside loop)
    new_nodes.append(
        outside_node(
            "1800000000040",
            "Set Initial Agent",
            "assigner",
            1600,
            600,
            height=136,
            extra_data={
                "items": [
                    {
                        "input_type": "variable",
                        "operation": "over-write",
                        "value": [
                            "1757492907627",
                            "structured_output",
                            "initial_agent",
                        ],
                        "variable_selector": ["conversation", "active_agent"],
                        "write_mode": "over-write",
                    },
                    {
                        "input_type": "variable",
                        "operation": "over-write",
                        "value": [
                            "1757492907627",
                            "structured_output",
                            "workflow_mode",
                        ],
                        "variable_selector": ["conversation", "workflow_mode"],
                        "write_mode": "over-write",
                    },
                    {
                        "input_type": "variable",
                        "operation": "over-write",
                        "value": ["conversation", "True"],
                        "variable_selector": ["conversation", "agent_loop_active"],
                        "write_mode": "over-write",
                    },
                ],
                "version": "2",
            },
        )
    )

    # 6b. Agent Loop (outside)
    new_nodes.append(
        {
            "data": {
                "break_conditions": [
                    {
                        "comparison_operator": "is",
                        "id": make_uuid(),
                        "value": False,
                        "varType": "boolean",
                        "variable_selector": ["conversation", "agent_loop_active"],
                    }
                ],
                "error_handle_mode": "terminated",
                "height": 900,
                "logical_operator": "and",
                "loop_count": 6,
                "loop_variables": [
                    {
                        "id": make_uuid(),
                        "label": "agent_loop_active",
                        "value": ["conversation", "agent_loop_active"],
                        "value_type": "variable",
                        "var_type": "boolean",
                    }
                ],
                "selected": False,
                "start_node_id": f"{LOOP_ID}start",
                "title": "Agent Loop",
                "type": "loop",
                "width": 4000,
            },
            "height": 900,
            "id": LOOP_ID,
            "position": {"x": 2200, "y": 400},
            "positionAbsolute": {"x": 2200, "y": 400},
            "selected": False,
            "sourcePosition": "right",
            "targetPosition": "left",
            "type": "custom",
            "width": 4000,
            "zIndex": 1,
        }
    )

    # 6c. Loop Start
    new_nodes.append(
        {
            "data": {
                "desc": "",
                "isInLoop": True,
                "selected": False,
                "title": "",
                "type": "loop-start",
            },
            "draggable": False,
            "height": 48,
            "id": f"{LOOP_ID}start",
            "parentId": LOOP_ID,
            "position": {"x": 60, "y": 113},
            "positionAbsolute": {"x": 2260, "y": 513},
            "selectable": False,
            "selected": False,
            "sourcePosition": "right",
            "targetPosition": "left",
            "type": "custom-loop-start",
            "width": 44,
            "zIndex": 1002,
        }
    )

    # 6d. Agent Dispatcher (if-else, inside loop)
    dispatcher_cases = []
    for case_id, agent_val in DISPATCH_CASES:
        dispatcher_cases.append(
            {
                "case_id": case_id,
                "conditions": [
                    {
                        "comparison_operator": "is",
                        "id": make_uuid(),
                        "value": agent_val,
                        "varType": "string",
                        "variable_selector": ["conversation", "active_agent"],
                    }
                ],
                "id": case_id,
                "logical_operator": "and",
            }
        )

    new_nodes.append(
        loop_node_base(
            "1800000000710",
            "Agent Dispatcher",
            "if-else",
            180,
            50,
            height=400,
            extra_data={"cases": dispatcher_cases, "desc": ""},
        )
    )

    # 6e. Prompt Fetch HTTP nodes (inside loop)
    for pf_id, pf_title, pf_file in PROMPT_FETCHES:
        idx = PROMPT_FETCHES.index((pf_id, pf_title, pf_file))
        new_nodes.append(
            loop_node_base(
                pf_id,
                pf_title,
                "http-request",
                550,
                50 + idx * 130,
                height=205,
                extra_data={
                    "authorization": {"config": None, "type": "no-auth"},
                    "body": {"data": [], "type": "none"},
                    "error_strategy": "fail-branch",
                    "headers": "",
                    "method": "get",
                    "params": "",
                    "retry_config": {
                        "max_retries": 3,
                        "retry_enabled": True,
                        "retry_interval": 100,
                    },
                    "ssl_verify": True,
                    "timeout": {
                        "max_connect_timeout": 0,
                        "max_read_timeout": 0,
                        "max_write_timeout": 0,
                    },
                    "url": f"{PROMPT_BASE}{pf_file}",
                    "variables": [],
                },
            )
        )

    # 6f. Agent nodes (inside loop)
    for agent_id, agent_title, max_iter, pf_id, pf_file, tools in AGENTS:
        idx = AGENTS.index((agent_id, agent_title, max_iter, pf_id, pf_file, tools))
        instruction = (
            f"{{{{#{pf_id}.body#}}}}\n\n"
            "Conversation ID: {{#sys.conversation_id#}}\n"
            "Agent Memory: {{#conversation.agent_memory#}}\n"
            "Org Name: {{#conversation.org_name#}}\n"
            "IMPORTANT: Use conversation_id for ALL tool calls."
        )
        tool_list = [make_tool_entry(t) for t in tools]

        new_nodes.append(
            loop_node_base(
                agent_id,
                agent_title,
                "agent",
                950,
                50 + idx * 130,
                height=312,
                extra_data={
                    "agent_parameters": {
                        "instruction": {
                            "type": "constant",
                            "value": instruction,
                        },
                        "maximum_iterations": {
                            "type": "constant",
                            "value": max_iter,
                        },
                        "model": {
                            "type": "constant",
                            "value": {
                                "completion_params": {
                                    "max_tokens": 16384,
                                    "temperature": 0.2,
                                },
                                "mode": "chat",
                                "model": "claude-sonnet-4-6",
                                "model_type": "llm",
                                "provider": "langgenius/anthropic/anthropic",
                                "type": "model-selector",
                            },
                        },
                        "query": {
                            "type": "constant",
                            "value": "{{#sys.query#}}",
                        },
                        "tools": {
                            "type": "constant",
                            "value": tool_list,
                        },
                    },
                    "agent_strategy_label": "FunctionCalling",
                    "agent_strategy_name": "function_calling",
                    "agent_strategy_provider_name": "langgenius/agent/agent",
                    "desc": f"{agent_title} - specialized agent",
                    "error_strategy": "fail-branch",
                    "memory": {
                        "query_prompt_template": "{{#sys.query#}}\n\n{{#sys.files#}}",
                        "window": {"enabled": True, "size": 5},
                    },
                    "output_schema": None,
                    "plugin_unique_identifier": PLUGIN_UID,
                    "tool_node_version": "2",
                },
            )
        )

    # 6g. Output Collector (code, inside loop)
    output_collector_code = """import json

def main(active_agent: str,
         spec_text: str, bundle_text: str, rules_text: str,
         reports_text: str, inspect_text: str, admin_text: str) -> dict:
    texts = {
        "spec": spec_text,
        "bundle_config": bundle_text,
        "rules": rules_text,
        "reports": reports_text,
        "inspect": inspect_text,
        "admin": admin_text,
    }
    agent_text = texts.get(active_agent, "") or ""
    memory_entry = json.dumps({
        "agent": active_agent,
        "summary": agent_text[:500],
    })
    spec_just_completed = (
        active_agent == "spec"
        and "spec" in agent_text.lower()
        and ("generated" in agent_text.lower() or "complete" in agent_text.lower())
    )
    bundle_just_completed = (
        active_agent == "bundle_config"
        and "bundle" in agent_text.lower()
        and ("generated" in agent_text.lower() or "complete" in agent_text.lower())
    )
    return {
        "memory_entry": memory_entry,
        "agent_output": agent_text,
        "spec_just_completed": spec_just_completed,
        "bundle_just_completed": bundle_just_completed,
    }
"""
    new_nodes.append(
        loop_node_base(
            "1800000000720",
            "Output Collector",
            "code",
            1400,
            200,
            height=112,
            extra_data={
                "code": output_collector_code,
                "code_language": "python3",
                "outputs": {
                    "memory_entry": {"type": "string"},
                    "agent_output": {"type": "string"},
                    "spec_just_completed": {"type": "boolean"},
                    "bundle_just_completed": {"type": "boolean"},
                },
                "variables": [
                    {
                        "value_selector": ["conversation", "active_agent"],
                        "value_type": "string",
                        "variable": "active_agent",
                    },
                    {
                        "value_selector": ["1800000000110", "text"],
                        "value_type": "string",
                        "variable": "spec_text",
                    },
                    {
                        "value_selector": ["1800000000210", "text"],
                        "value_type": "string",
                        "variable": "bundle_text",
                    },
                    {
                        "value_selector": ["1800000000310", "text"],
                        "value_type": "string",
                        "variable": "rules_text",
                    },
                    {
                        "value_selector": ["1800000000410", "text"],
                        "value_type": "string",
                        "variable": "reports_text",
                    },
                    {
                        "value_selector": ["1800000000510", "text"],
                        "value_type": "string",
                        "variable": "inspect_text",
                    },
                    {
                        "value_selector": ["1800000000610", "text"],
                        "value_type": "string",
                        "variable": "admin_text",
                    },
                ],
            },
        )
    )

    # 6h. State Update (assigner, inside loop)
    new_nodes.append(
        loop_node_base(
            "1800000000730",
            "State Update",
            "assigner",
            1700,
            200,
            height=136,
            extra_data={
                "items": [
                    {
                        "input_type": "variable",
                        "operation": "append",
                        "value": ["1800000000720", "memory_entry"],
                        "variable_selector": ["conversation", "agent_memory"],
                        "write_mode": "append",
                    },
                    {
                        "input_type": "variable",
                        "operation": "over-write",
                        "value": ["1800000000720", "spec_just_completed"],
                        "variable_selector": ["conversation", "spec_complete"],
                        "write_mode": "over-write",
                    },
                    {
                        "input_type": "variable",
                        "operation": "over-write",
                        "value": ["1800000000720", "bundle_just_completed"],
                        "variable_selector": ["conversation", "bundle_complete"],
                        "write_mode": "over-write",
                    },
                ],
                "version": "2",
            },
        )
    )

    # 6i. Next Agent Decider (code, inside loop)
    decider_code = """def main(active_agent: str, workflow_mode: str,
         spec_complete: bool, bundle_complete: bool) -> dict:
    if workflow_mode == "targeted":
        return {"next_agent": "done", "loop_done": True}

    chain = ["spec", "bundle_config", "rules", "reports", "inspect", "admin"]
    try:
        idx = chain.index(active_agent)
        if idx < len(chain) - 1:
            next_a = chain[idx + 1]
            if next_a == "bundle_config" and not spec_complete:
                return {"next_agent": "done", "loop_done": True,
                        "reason": "Spec incomplete"}
            if next_a in ("rules", "reports", "inspect") and not bundle_complete:
                return {"next_agent": "done", "loop_done": True,
                        "reason": "Bundle incomplete"}
            return {"next_agent": next_a, "loop_done": False}
        return {"next_agent": "done", "loop_done": True}
    except ValueError:
        return {"next_agent": "done", "loop_done": True}
"""
    new_nodes.append(
        loop_node_base(
            "1800000000740",
            "Next Agent Decider",
            "code",
            2000,
            200,
            height=112,
            extra_data={
                "code": decider_code,
                "code_language": "python3",
                "outputs": {
                    "next_agent": {"type": "string"},
                    "loop_done": {"type": "boolean"},
                    "reason": {"type": "string"},
                },
                "variables": [
                    {
                        "value_selector": ["conversation", "active_agent"],
                        "value_type": "string",
                        "variable": "active_agent",
                    },
                    {
                        "value_selector": ["conversation", "workflow_mode"],
                        "value_type": "string",
                        "variable": "workflow_mode",
                    },
                    {
                        "value_selector": ["conversation", "spec_complete"],
                        "value_type": "boolean",
                        "variable": "spec_complete",
                    },
                    {
                        "value_selector": ["conversation", "bundle_complete"],
                        "value_type": "boolean",
                        "variable": "bundle_complete",
                    },
                ],
            },
        )
    )

    # 6j. Loop Done Check (if-else, inside loop)
    new_nodes.append(
        loop_node_base(
            "1800000000745",
            "Loop Done Check",
            "if-else",
            2300,
            150,
            height=148,
            extra_data={
                "cases": [
                    {
                        "case_id": "loop-done",
                        "conditions": [
                            {
                                "comparison_operator": "is",
                                "id": make_uuid(),
                                "value": "true",
                                "varType": "boolean",
                                "variable_selector": ["1800000000740", "loop_done"],
                            }
                        ],
                        "id": "loop-done",
                        "logical_operator": "and",
                    }
                ],
                "desc": "",
            },
        )
    )

    # 6k. Break Loop (assigner, inside loop)
    new_nodes.append(
        loop_node_base(
            "1800000000751",
            "Break Loop",
            "assigner",
            2600,
            100,
            height=84,
            extra_data={
                "items": [
                    {
                        "input_type": "variable",
                        "operation": "over-write",
                        "value": ["conversation", "False"],
                        "variable_selector": ["conversation", "agent_loop_active"],
                        "write_mode": "over-write",
                    }
                ],
                "version": "2",
            },
        )
    )

    # 6l. Continue Loop (assigner, inside loop)
    new_nodes.append(
        loop_node_base(
            "1800000000752",
            "Continue Loop",
            "assigner",
            2600,
            300,
            height=84,
            extra_data={
                "items": [
                    {
                        "input_type": "variable",
                        "operation": "over-write",
                        "value": ["1800000000740", "next_agent"],
                        "variable_selector": ["conversation", "active_agent"],
                        "write_mode": "over-write",
                    }
                ],
                "version": "2",
            },
        )
    )

    # 6m. Error Handler (answer, inside loop)
    new_nodes.append(
        loop_node_base(
            "1800000000760",
            "Error Handler",
            "answer",
            2600,
            500,
            height=137,
            extra_data={
                "answer": "Error in {{#conversation.active_agent#}} agent. Please try again or contact support.",
                "variables": [],
            },
        )
    )

    # 7. Post-Loop Answer (outside loop)
    new_nodes.append(
        outside_node(
            "1800000000800",
            "Post-Loop Answer",
            "answer",
            6400,
            600,
            height=103,
            extra_data={
                "answer": "{{#1800000000700.output#}}",
                "variables": [],
            },
        )
    )

    # 8. Pre-Loop Error (outside loop)
    new_nodes.append(
        outside_node(
            "1800000000112",
            "Pre-Loop Error",
            "answer",
            2200,
            1300,
            height=137,
            extra_data={
                "answer": "An error occurred while setting up. Please try again or contact support.",
                "variables": [],
            },
        )
    )

    # Add all new nodes
    wf["graph"]["nodes"].extend(new_nodes)

    # ── 9. Add new edges ────────────────────────────────────────────────

    # Pre-loop edges
    new_edges.append(
        make_edge(
            "1757493270484",
            "case-agent-work",
            "1800000000040",
            "target",
            "if-else",
            "assigner",
        )
    )
    new_edges.append(
        make_edge(
            "1800000000040", "source", "1775719228711", "target", "assigner", "if-else"
        )
    )
    new_edges.append(
        make_edge("1775648480416", "source", LOOP_ID, "target", "http-request", "loop")
    )
    new_edges.append(
        make_edge(
            "1775648480416",
            "fail-branch",
            "1800000000112",
            "target",
            "http-request",
            "answer",
        )
    )
    new_edges.append(
        make_edge(
            "1775800000002",
            "fail-branch",
            "1800000000112",
            "target",
            "http-request",
            "answer",
        )
    )
    new_edges.append(
        make_edge(LOOP_ID, "source", "1800000000800", "target", "loop", "answer")
    )

    # Inside loop edges
    # Start → Dispatcher
    new_edges.append(
        make_edge(
            f"{LOOP_ID}start",
            "source",
            "1800000000710",
            "target",
            "loop-start",
            "if-else",
            in_loop=True,
        )
    )

    # Dispatcher → Prompt Fetches
    pf_map = {
        "dispatch-spec": "1800000000101",
        "dispatch-bundle-config": "1800000000201",
        "dispatch-rules": "1800000000301",
        "dispatch-reports": "1800000000401",
        "dispatch-inspect": "1800000000501",
        "dispatch-admin": "1800000000601",
    }
    for case_id, pf_id in pf_map.items():
        new_edges.append(
            make_edge(
                "1800000000710",
                case_id,
                pf_id,
                "target",
                "if-else",
                "http-request",
                in_loop=True,
            )
        )

    # Prompt Fetches → Agents
    pf_to_agent = {
        "1800000000101": "1800000000110",
        "1800000000201": "1800000000210",
        "1800000000301": "1800000000310",
        "1800000000401": "1800000000410",
        "1800000000501": "1800000000510",
        "1800000000601": "1800000000610",
    }
    for pf_id, ag_id in pf_to_agent.items():
        new_edges.append(
            make_edge(
                pf_id, "source", ag_id, "target", "http-request", "agent", in_loop=True
            )
        )

    # Agents → Output Collector (success)
    agent_ids = [
        "1800000000110",
        "1800000000210",
        "1800000000310",
        "1800000000410",
        "1800000000510",
        "1800000000610",
    ]
    for ag_id in agent_ids:
        new_edges.append(
            make_edge(
                ag_id,
                "source",
                "1800000000720",
                "target",
                "agent",
                "code",
                in_loop=True,
            )
        )

    # Agents → Error Handler (fail)
    for ag_id in agent_ids:
        new_edges.append(
            make_edge(
                ag_id,
                "fail-branch",
                "1800000000760",
                "target",
                "agent",
                "answer",
                in_loop=True,
            )
        )

    # Prompt Fetches → Error Handler (fail)
    pf_ids = [
        "1800000000101",
        "1800000000201",
        "1800000000301",
        "1800000000401",
        "1800000000501",
        "1800000000601",
    ]
    for pf_id in pf_ids:
        new_edges.append(
            make_edge(
                pf_id,
                "fail-branch",
                "1800000000760",
                "target",
                "http-request",
                "answer",
                in_loop=True,
            )
        )

    # Output Collector → State Update → Decider → Loop Done Check
    new_edges.append(
        make_edge(
            "1800000000720",
            "source",
            "1800000000730",
            "target",
            "code",
            "assigner",
            in_loop=True,
        )
    )
    new_edges.append(
        make_edge(
            "1800000000730",
            "source",
            "1800000000740",
            "target",
            "assigner",
            "code",
            in_loop=True,
        )
    )
    new_edges.append(
        make_edge(
            "1800000000740",
            "source",
            "1800000000745",
            "target",
            "code",
            "if-else",
            in_loop=True,
        )
    )

    # Loop Done Check → Break / Continue
    new_edges.append(
        make_edge(
            "1800000000745",
            "loop-done",
            "1800000000751",
            "target",
            "if-else",
            "assigner",
            in_loop=True,
        )
    )
    new_edges.append(
        make_edge(
            "1800000000745",
            "false",
            "1800000000752",
            "target",
            "if-else",
            "assigner",
            in_loop=True,
        )
    )

    # Remove the old edge from 1775648480416 → 1775658332808 (fail-branch)
    # since 1775658332808 was removed. Also remove edge from
    # 1775719228711-false → 1775648480416 which we need to keep but redirect.
    # Actually the old edge 1775719228711-false-1775648480416-target should stay.
    # And old edges 1775648480416-source-1775646587226-target should be removed
    # (already done since 1775646587226 is in NODES_TO_REMOVE).

    # We also need to remove the old fail-branch edges pointing to 1775658332808
    # from non-removed nodes (1775648480416 and 1775800000002). They were already
    # removed since 1775658332808 is in NODES_TO_REMOVE.

    wf["graph"]["edges"].extend(new_edges)

    # ── Write output ────────────────────────────────────────────────────
    with open(DST, "w") as f:
        yaml.dump(
            doc,
            f,
            default_flow_style=False,
            allow_unicode=True,
            sort_keys=False,
            width=1000,
        )

    print(f"Wrote transformed workflow to: {DST}")
    print(f"  Nodes: {len(wf['graph']['nodes'])}")
    print(f"  Edges: {len(wf['graph']['edges'])}")
    print(f"  Conversation variables: {len(wf['conversation_variables'])}")


if __name__ == "__main__":
    transform()
