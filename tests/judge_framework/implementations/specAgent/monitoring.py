"""
Client-side monitoring tools for Spec Agent testing.

Provides utilities to query the avni-ai server for conversation state,
inspect cached entities, and export debug snapshots.
"""

import json
import logging
import requests
from typing import Dict, Any
from pathlib import Path

logger = logging.getLogger(__name__)


class ConversationMonitor:
    """Monitor and inspect conversation state on avni-ai server."""

    def __init__(self, mcp_server_url: str):
        """
        Initialize conversation monitor.

        Args:
            mcp_server_url: Base URL of avni-ai MCP server (e.g., http://localhost:8023)
        """
        self.base_url = mcp_server_url.rstrip("/")

    def get_conversation_state(self, conversation_id: str) -> Dict[str, Any]:
        """
        Get conversation state from server.

        Args:
            conversation_id: Dify conversation ID

        Returns:
            Dict with conversation state or error info
        """
        url = f"{self.base_url}/debug/conversation/{conversation_id}"

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Failed to get conversation state: {e}")
            return {"error": str(e), "conversation_id": conversation_id}

    def list_conversations(self) -> Dict[str, Any]:
        """
        List all cached conversations on server.

        Returns:
            Dict with list of conversations
        """
        url = f"{self.base_url}/debug/conversations"

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Failed to list conversations: {e}")
            return {"error": str(e), "conversations": []}

    def clear_conversation(self, conversation_id: str) -> Dict[str, Any]:
        """
        Clear cached state for a conversation.

        Args:
            conversation_id: Dify conversation ID

        Returns:
            Dict with success status
        """
        url = f"{self.base_url}/debug/conversation/{conversation_id}"

        try:
            response = requests.delete(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Failed to clear conversation: {e}")
            return {"error": str(e), "success": False}

    def inspect_cached_entities(self, conversation_id: str) -> Dict[str, Any]:
        """
        Inspect cached entities for a conversation.

        Args:
            conversation_id: Dify conversation ID

        Returns:
            Dict with entities or empty dict
        """
        state = self.get_conversation_state(conversation_id)

        if "error" in state:
            return {}

        return state.get("entities_summary", {})

    def get_tool_call_history(self, conversation_id: str) -> list:
        """
        Get tool call history for a conversation.

        Args:
            conversation_id: Dify conversation ID

        Returns:
            List of tool call dicts
        """
        state = self.get_conversation_state(conversation_id)

        if "error" in state:
            return []

        return state.get("tool_calls", [])

    def export_debug_snapshot(self, conversation_id: str, output_path: str) -> bool:
        """
        Export complete conversation state to a JSON file.

        Args:
            conversation_id: Dify conversation ID
            output_path: Path to save JSON snapshot

        Returns:
            True if successful, False otherwise
        """
        state = self.get_conversation_state(conversation_id)

        if "error" in state:
            logger.error(
                f"Cannot export snapshot - error getting state: {state['error']}"
            )
            return False

        try:
            output_file = Path(output_path)
            output_file.parent.mkdir(parents=True, exist_ok=True)

            with open(output_file, "w") as f:
                json.dump(state, f, indent=2)

            logger.info(f"Exported debug snapshot to {output_path}")
            return True

        except Exception as e:
            logger.error(f"Failed to export snapshot: {e}")
            return False

    def print_conversation_summary(self, conversation_id: str):
        """
        Print a human-readable summary of conversation state.

        Args:
            conversation_id: Dify conversation ID
        """
        state = self.get_conversation_state(conversation_id)

        if "error" in state:
            print(f"❌ Error: {state['error']}")
            return

        if not state.get("found", False):
            print(f"❌ No state found for conversation: {conversation_id}")
            return

        print(f"\n{'=' * 60}")
        print(f"Conversation: {conversation_id}")
        print(f"{'=' * 60}")

        # Entities summary
        entities_summary = state.get("entities_summary", {})
        print(f"\n📦 Entities Cached: {state.get('entities_cached', False)}")
        if entities_summary:
            print("   Entity Counts:")
            for entity_type, count in entities_summary.items():
                print(f"   - {entity_type}: {count}")

        # Tool calls
        tool_calls = state.get("tool_calls", [])
        print(f"\n🔧 Tool Calls: {len(tool_calls)}")
        for i, tc in enumerate(tool_calls, 1):
            print(
                f"   {i}. {tc.get('tool', 'unknown')} - {tc.get('status', 'unknown')}"
            )

        # Spec status
        spec_preview = state.get("conversation_variables", {}).get("spec_yaml", "")
        has_spec = bool(spec_preview and spec_preview != "...")
        print(f"\n📝 Spec Generated: {has_spec}")
        if has_spec:
            print(f"   Preview: {spec_preview[:80]}...")

        # Timestamps
        print(f"\n⏰ Created: {state.get('created_at', 'N/A')}")
        print(f"   Updated: {state.get('updated_at', 'N/A')}")
        print(f"{'=' * 60}\n")


def monitor_test_execution(
    conversation_id: str, mcp_server_url: str, verbose: bool = True
) -> Dict[str, Any]:
    """
    Monitor a test execution and return state summary.

    Convenience function for monitoring during test runs.

    Args:
        conversation_id: Dify conversation ID
        mcp_server_url: Base URL of avni-ai MCP server
        verbose: Whether to print summary

    Returns:
        Conversation state dict
    """
    monitor = ConversationMonitor(mcp_server_url)

    if verbose:
        monitor.print_conversation_summary(conversation_id)

    return monitor.get_conversation_state(conversation_id)
