"""
Test executor for Spec Agent testing.

Executes Dify conversations with the Spec Agent, injecting conversation variables
and extracting generated specs from responses.
"""

import json
import logging
from typing import Dict, Any
from tests.judge_framework.interfaces.test_executor import TestExecutor
from tests.judge_framework.interfaces.result_models import TestConfiguration
from tests.dify.common.dify_client import DifyClient

logger = logging.getLogger(__name__)


class SpecAgentExecutor(TestExecutor):
    """Executor for Spec Agent tests with conversation variable injection."""

    def __init__(self, config: TestConfiguration):
        """
        Initialize Spec Agent executor.

        Args:
            config: Test configuration with Dify API settings
        """
        super().__init__(config)
        self.dify_client = DifyClient(config.dify_config.api_key)
        self.conversation_id = ""

    def execute(self, test_input: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute Spec Agent test with conversation variable injection.

        Args:
            test_input: Test input from SpecAgentTestSubject.get_test_input()

        Returns:
            Dict with:
            - success: bool
            - conversation_id: str
            - agent_response: str
            - spec_yaml: str (if generated)
            - tool_calls: list of tool calls made by agent
            - error: str (if failed)
        """
        query = test_input.get("query", "")
        inputs = test_input.get("inputs", {})
        test_scenario = test_input.get("test_scenario", "unknown")

        logger.info(f"Executing Spec Agent test: {test_scenario}")
        logger.debug(f"Query: {query}")
        logger.debug(f"Inputs: {json.dumps(inputs, indent=2)}")

        try:
            # Send message to Dify with injected conversation variables
            response = self.dify_client.send_message(
                query=query,
                conversation_id=self.conversation_id,
                inputs=inputs,
                user=f"spec_agent_test_{test_scenario}",
                timeout=180,  # Longer timeout for agent processing
            )

            if not response.get("success", False):
                error_msg = response.get("error", "Unknown Dify error")
                logger.error(f"Dify execution failed: {error_msg}")
                return {
                    "success": False,
                    "conversation_id": self.conversation_id,
                    "error": error_msg,
                    "agent_response": "",
                    "spec_yaml": "",
                    "tool_calls": [],
                }

            # Update conversation ID for potential follow-up messages
            self.conversation_id = response.get("conversation_id", "")
            agent_response = response.get("answer", "")

            # Extract spec_yaml from response
            spec_yaml = self._extract_spec_from_response(agent_response)

            # Extract tool calls from response metadata
            tool_calls = self._extract_tool_calls(response)

            logger.info(
                f"Spec Agent execution completed. Tool calls: {len(tool_calls)}"
            )

            return {
                "success": True,
                "conversation_id": self.conversation_id,
                "agent_response": agent_response,
                "spec_yaml": spec_yaml,
                "tool_calls": tool_calls,
                "raw_response": response,
            }

        except Exception as e:
            logger.exception(f"Exception during Spec Agent execution: {e}")
            return {
                "success": False,
                "conversation_id": self.conversation_id,
                "error": str(e),
                "agent_response": "",
                "spec_yaml": "",
                "tool_calls": [],
            }

    def _extract_spec_from_response(self, response_text: str) -> str:
        """
        Extract YAML spec from agent response.

        Looks for:
        1. SPEC_APPROVED marker followed by YAML
        2. YAML code blocks (```yaml or ```yml)
        3. Any YAML-like content

        Args:
            response_text: Agent's response text

        Returns:
            Extracted YAML spec or empty string
        """
        if not response_text:
            return ""

        # Look for SPEC_APPROVED marker
        if "SPEC_APPROVED" in response_text:
            # Extract everything after SPEC_APPROVED
            parts = response_text.split("SPEC_APPROVED", 1)
            if len(parts) > 1:
                spec_content = parts[1].strip()
                # Remove markdown code blocks if present
                spec_content = self._remove_code_blocks(spec_content)
                return spec_content

        # Look for YAML code blocks
        if "```yaml" in response_text or "```yml" in response_text:
            return self._extract_from_code_block(response_text, ["yaml", "yml"])

        # Look for any code block
        if "```" in response_text:
            return self._extract_from_code_block(response_text, [""])

        return ""

    def _remove_code_blocks(self, text: str) -> str:
        """Remove markdown code block markers from text."""
        text = text.strip()
        if text.startswith("```"):
            lines = text.split("\n")
            # Remove first line (```yaml or similar)
            if len(lines) > 0:
                lines = lines[1:]
            # Remove last line if it's closing ```
            if len(lines) > 0 and lines[-1].strip() == "```":
                lines = lines[:-1]
            text = "\n".join(lines)
        return text.strip()

    def _extract_from_code_block(self, text: str, languages: list) -> str:
        """Extract content from markdown code blocks."""
        for lang in languages:
            marker = f"```{lang}"
            if marker in text:
                parts = text.split(marker, 1)
                if len(parts) > 1:
                    content = parts[1].split("```", 1)[0]
                    return content.strip()
        return ""

    def _extract_tool_calls(self, response: Dict[str, Any]) -> list:
        """
        Extract tool calls from Dify response metadata.

        Args:
            response: Full Dify response dict

        Returns:
            List of tool call dicts with tool name, status, etc.
        """
        tool_calls = []

        # Check for tool_responses in response
        if "tool_responses" in response:
            for tool_resp in response.get("tool_responses", []):
                tool_calls.append(
                    {
                        "tool": tool_resp.get("tool_name", "unknown"),
                        "status": "success"
                        if tool_resp.get("success", False)
                        else "failed",
                        "output": tool_resp.get("output", ""),
                    }
                )

        # Check for workflow_run_id and fetch detailed logs if available
        # (This would require additional Dify API calls - implement if needed)

        return tool_calls

    def get_executor_metadata(self) -> Dict[str, Any]:
        """Get metadata about this executor."""
        return {
            "executor_type": "SpecAgentExecutor",
            "dify_base_url": self.dify_client.base_url,
            "current_conversation_id": self.conversation_id,
            "supports_variable_injection": True,
        }

    def reset_conversation(self):
        """Reset conversation ID for a new test."""
        self.conversation_id = ""
