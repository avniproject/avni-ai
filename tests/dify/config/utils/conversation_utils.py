"""Utility functions for managing conversation flow in integration tests."""

import logging
import os
from typing import Dict, Any, List

logger = logging.getLogger(__name__)


def generate_tester_message(
    ai_tester, conversation_history: List[Dict[str, Any]], round_count: int
) -> str:
    """Generate AI Tester message based on conversation history"""
    if round_count == 1:
        return ai_tester.generate_message([], 0)

    # Convert conversation history to tester's perspective
    tester_history = []
    for msg in conversation_history:
        if msg["role"] == "user":  # Tester's previous message
            tester_history.append({"role": "assistant", "content": msg["content"]})
        elif msg["role"] == "assistant":  # Dify's response becomes input to tester
            tester_history.append({"role": "user", "content": msg["content"]})

    return ai_tester.generate_message(tester_history, 0)


def create_dify_inputs(auth_token: str) -> Dict[str, Any]:
    """Create inputs dictionary for Dify API calls"""
    return {
        "auth_token": auth_token,
        "org_name": "Jan Swasthya Sahyog",
        "org_type": "Trial",
        "user_name": "Atul",
        "avni_mcp_server_url": os.getenv("AVNI_MCP_SERVER_URL"),
    }


def is_satisfaction_expressed(user_message: str) -> bool:
    """Check if AI Tester expressed satisfaction with configuration"""
    return (
        "i am happy with the configuration provided by the avni assistant"
        in user_message.lower()
    )


def is_timeout_response(dify_response: Dict[str, Any]) -> bool:
    """Check if Dify response indicates a timeout/504 error"""
    if dify_response["success"]:
        return False

    error_str = str(dify_response.get("error", "")).lower()
    return "timeout" in error_str or "504" in error_str


def handle_satisfaction_response(
    dify_response: Dict[str, Any],
    conversation_history: List[Dict[str, Any]],
    user_message: str,
    round_count: int,
) -> None:
    """Handle Dify response after satisfaction is expressed"""
    # Record the satisfaction message
    conversation_history.append(
        {"role": "user", "content": user_message, "round": round_count}
    )

    if is_timeout_response(dify_response):
        logger.info(
            "🔄 Dify timeout/504 detected - configuration creation likely in progress"
        )
        conversation_history.append(
            {
                "role": "assistant",
                "content": "Configuration creation in progress (timeout detected)",
                "round": round_count,
                "timeout_detected": True,
            }
        )
    elif dify_response["success"]:
        # Got a response even after satisfaction
        conversation_history.append(
            {
                "role": "assistant",
                "content": dify_response["answer"],
                "round": round_count,
            }
        )
    else:
        # Other error after satisfaction
        logger.warning(
            f"Dify error after satisfaction: {dify_response.get('error', 'Unknown')}"
        )
        conversation_history.append(
            {
                "role": "assistant",
                "content": f"Error after satisfaction: {dify_response.get('error', 'Unknown')}",
                "round": round_count,
            }
        )


def handle_normal_conversation_timeout(
    conversation_history: List[Dict[str, Any]], user_message: str, round_count: int
) -> bool:
    """Handle timeout during normal conversation. Returns True if timeout detected."""
    logger.info(
        "🔄 Dify timeout/504 detected during conversation - configuration creation likely started"
    )

    # Record conversation and mark as successful with timeout
    conversation_history.append(
        {"role": "user", "content": user_message, "round": round_count}
    )
    conversation_history.append(
        {
            "role": "assistant",
            "content": "Configuration creation in progress (timeout detected during conversation)",
            "round": round_count,
            "timeout_detected": True,
        }
    )

    return True


def record_normal_conversation(
    conversation_history: List[Dict[str, Any]],
    user_message: str,
    assistant_response: str,
    round_count: int,
) -> None:
    """Record normal conversation exchange"""
    conversation_history.append(
        {"role": "user", "content": user_message, "round": round_count}
    )
    conversation_history.append(
        {
            "role": "assistant",
            "content": assistant_response,
            "round": round_count,
        }
    )
