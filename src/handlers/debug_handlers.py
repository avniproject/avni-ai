"""
Debug handlers for monitoring conversation state and tool calls.

Provides endpoints for inspecting conversation_id state, cached entities,
and tool call history for debugging Dify workflows.
"""

import logging
from typing import Dict, Any
from fastapi import Request
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)

# In-memory storage for conversation state (replace with Redis/DB in production)
_conversation_cache: Dict[str, Dict[str, Any]] = {}


def store_conversation_state(
    conversation_id: str,
    entities: Dict[str, Any] = None,
    spec_yaml: str = None,
    tool_calls: list = None,
):
    """
    Store conversation state for debugging.

    Args:
        conversation_id: Dify conversation ID
        entities: Cached entities for this conversation
        spec_yaml: Generated spec YAML
        tool_calls: List of tool calls made
    """
    if conversation_id not in _conversation_cache:
        _conversation_cache[conversation_id] = {
            "conversation_id": conversation_id,
            "entities": {},
            "spec_yaml": "",
            "tool_calls": [],
            "created_at": None,
            "updated_at": None,
        }

    state = _conversation_cache[conversation_id]

    if entities is not None:
        state["entities"] = entities
    if spec_yaml is not None:
        state["spec_yaml"] = spec_yaml
    if tool_calls is not None:
        state["tool_calls"].extend(tool_calls)

    import datetime

    state["updated_at"] = datetime.datetime.now().isoformat()
    if state["created_at"] is None:
        state["created_at"] = state["updated_at"]


def get_conversation_state(conversation_id: str) -> Dict[str, Any]:
    """
    Get conversation state for debugging.

    Args:
        conversation_id: Dify conversation ID

    Returns:
        Conversation state dict or empty dict if not found
    """
    return _conversation_cache.get(conversation_id, {})


async def handle_debug_conversation(request: Request) -> JSONResponse:
    """
    Handle GET /debug/conversation/{conversation_id} requests.

    Returns conversation state including cached entities, tool calls, and variables.

    Args:
        request: FastAPI request with conversation_id in path params

    Returns:
        JSONResponse with conversation state
    """
    conversation_id = request.path_params.get("conversation_id", "")

    if not conversation_id:
        return JSONResponse(
            {"error": "Missing conversation_id parameter"}, status_code=400
        )

    logger.info(f"Debug request for conversation: {conversation_id}")

    state = get_conversation_state(conversation_id)

    if not state:
        return JSONResponse(
            {
                "conversation_id": conversation_id,
                "found": False,
                "message": "No state found for this conversation_id",
            },
            status_code=404,
        )

    # Build response with summary
    entities = state.get("entities", {})
    entities_summary = {
        "subject_types": len(entities.get("subject_types", [])),
        "programs": len(entities.get("programs", [])),
        "encounter_types": len(entities.get("encounter_types", [])),
        "address_levels": len(entities.get("address_levels", [])),
        "forms": len(entities.get("forms", [])),
    }

    response = {
        "conversation_id": conversation_id,
        "found": True,
        "entities_cached": bool(entities),
        "entities_summary": entities_summary,
        "tool_calls": state.get("tool_calls", []),
        "conversation_variables": {
            "entities_jsonl": "..." if entities else "",
            "spec_yaml": state.get("spec_yaml", "")[:100] + "..."
            if state.get("spec_yaml")
            else "",
            "setup_mode_active": True,  # Would need to track this
        },
        "created_at": state.get("created_at"),
        "updated_at": state.get("updated_at"),
    }

    return JSONResponse(response)


async def handle_debug_list_conversations(request: Request) -> JSONResponse:
    """
    Handle GET /debug/conversations requests.

    Lists all cached conversations for debugging.

    Returns:
        JSONResponse with list of conversation IDs and summaries
    """
    conversations = []

    for conv_id, state in _conversation_cache.items():
        entities = state.get("entities", {})
        conversations.append(
            {
                "conversation_id": conv_id,
                "has_entities": bool(entities),
                "has_spec": bool(state.get("spec_yaml")),
                "tool_call_count": len(state.get("tool_calls", [])),
                "created_at": state.get("created_at"),
                "updated_at": state.get("updated_at"),
            }
        )

    return JSONResponse({"total": len(conversations), "conversations": conversations})


async def handle_debug_clear_conversation(request: Request) -> JSONResponse:
    """
    Handle DELETE /debug/conversation/{conversation_id} requests.

    Clears cached state for a conversation.

    Args:
        request: FastAPI request with conversation_id in path params

    Returns:
        JSONResponse with success status
    """
    conversation_id = request.path_params.get("conversation_id", "")

    if not conversation_id:
        return JSONResponse(
            {"error": "Missing conversation_id parameter"}, status_code=400
        )

    if conversation_id in _conversation_cache:
        del _conversation_cache[conversation_id]
        return JSONResponse(
            {"success": True, "message": f"Cleared state for {conversation_id}"}
        )
    else:
        return JSONResponse(
            {"success": False, "message": f"No state found for {conversation_id}"},
            status_code=404,
        )
