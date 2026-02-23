"""
Rules Generation Conversation Strategy for the Judge Framework
"""

import re
from typing import Dict, Any, List

from tests.judge_framework.interfaces.conversation_strategy import (
    ConversationGenerationStrategy,
)


class RulesGenerationConversationStrategy(ConversationGenerationStrategy):
    """
    Conversation strategy for rules generation that knows when to end conversations
    based on rule generation patterns.
    """

    def __init__(self):
        self._confirmation_patterns = (
            "reply yes",
            "do these scenarios match",
            "do these scenarios align",
            "if yes, i'll generate the rule code",
            "let me know what to change",
            "confirm and i'll generate",
            "here are the scheduling scenarios",
            "here are scheduling scenarios",
        )
        self._rule_code_patterns = (
            "```javascript",
            "```js",
            '"use strict";',
            "({params, imports}) =>",
            "({ params, imports }) =>",
            "visitschedulebuilder",
        )

    def generate_next_message(
        self, conversation_history: List[Dict[str, Any]], context: Dict[str, Any]
    ) -> str:
        """
        Generate the next user message for rules generation conversation.
        """
        if len(conversation_history) < 1:
            return ""

        last_assistant_response = conversation_history[-1].get("assistant_response", "")
        normalized_response = self._normalize(last_assistant_response)

        if self._is_confirmation_request(normalized_response):
            return "YES"

        return ""

    def should_continue_conversation(
        self, conversation_history: List[Dict[str, Any]], context: Dict[str, Any]
    ) -> bool:
        """
        Determine if rules generation conversation should continue.
        """
        if len(conversation_history) < 1:
            return True

        last_assistant_response = conversation_history[-1].get("assistant_response", "")
        normalized_response = self._normalize(last_assistant_response)

        if self._contains_rule_code(normalized_response):
            return False

        if self._is_confirmation_request(normalized_response):
            return True

        return len(conversation_history) < 5

    @staticmethod
    def _normalize(text: str) -> str:
        text = text or ""
        text = text.lower()
        text = re.sub(r"\s+", " ", text).strip()
        return text

    def _contains_rule_code(self, normalized_response: str) -> bool:
        return any(pattern in normalized_response for pattern in self._rule_code_patterns)

    def _is_confirmation_request(self, normalized_response: str) -> bool:
        if any(
            pattern in normalized_response for pattern in self._confirmation_patterns
        ):
            return True

        # Some model responses provide only the scenario table and do not include
        # explicit confirmation sentence at the end.
        has_table_markers = (
            "| case |" in normalized_response
            and "| trigger |" in normalized_response
            and "| will schedule? |" in normalized_response
        )
        if has_table_markers:
            return True

        return normalized_response.endswith("?")
