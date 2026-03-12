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
            "confirm",
            "reply yes",
            "do these scenarios match",
            "do these scenarios align",
            "if yes, i'll generate the rule code",
            "if yes, i will generate the rule code",
            "if this looks correct",
            "shall i generate",
            "should i generate",
            "want me to generate",
            "can i proceed",
            "let me know what to change",
            "confirm and i'll generate",
            "confirm and i will generate",
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
        self._pre_code_patterns = (
            "scenario",
            "validation",
            "case",
            "trigger",
            "schedule date",
            "will schedule",
            "review",
        )
        self._terminal_failure_patterns = (
            "not supported",
            "cannot",
            "can't",
            "unable to",
            "outside scope",
            "do not have access",
        )
        self._affirmative_messages = {
            "yes",
            "yes.",
            "y",
            "ok",
            "okay",
            "proceed",
            "go ahead",
            "looks good",
            "approved",
            "confirmed",
        }
        self._confirmation_reply = (
            "YES. These scenarios look correct. "
            "Please generate the final executable JavaScript visit scheduling rule code now."
        )
        self._force_code_reply = (
            "Please provide only the final executable JavaScript VisitScheduleBuilder "
            "rule code for the request."
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

        if self._contains_rule_code(normalized_response):
            return ""

        already_confirmed = self._already_confirmed(conversation_history)

        if self._is_confirmation_request(normalized_response):
            return (
                self._force_code_reply
                if already_confirmed
                else self._confirmation_reply
            )

        if self._looks_like_pre_code_response(normalized_response):
            return (
                self._force_code_reply
                if already_confirmed
                else self._confirmation_reply
            )

        if already_confirmed:
            return self._force_code_reply

        # Fallback once in early turns to avoid one-turn drop-offs.
        if len(conversation_history) <= 2:
            return self._confirmation_reply

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

        if self._is_terminal_failure(normalized_response):
            return False

        max_iterations = int(context.get("max_iterations", 5) or 5)
        hard_limit = max(2, min(max_iterations, 6))
        return len(conversation_history) < hard_limit

    @staticmethod
    def _normalize(text: str) -> str:
        text = text or ""
        text = text.lower()
        text = re.sub(r"\s+", " ", text).strip()
        return text

    def _contains_rule_code(self, normalized_response: str) -> bool:
        return any(
            pattern in normalized_response for pattern in self._rule_code_patterns
        )

    @staticmethod
    def _has_scenario_table(normalized_response: str) -> bool:
        has_case = "| case |" in normalized_response
        has_trigger_like = any(
            marker in normalized_response
            for marker in ("| trigger |", "| condition |", "| when |")
        )
        return has_case and has_trigger_like

    def _is_confirmation_request(self, normalized_response: str) -> bool:
        if any(
            pattern in normalized_response for pattern in self._confirmation_patterns
        ):
            return True

        # Some model responses provide only the scenario table without explicit
        # confirmation sentence.
        if self._has_scenario_table(normalized_response):
            return True

        is_question = normalized_response.endswith("?")
        if is_question and any(
            token in normalized_response
            for token in ("confirm", "scenarios", "generate", "proceed", "looks right")
        ):
            return True

        return False

    def _looks_like_pre_code_response(self, normalized_response: str) -> bool:
        if self._contains_rule_code(normalized_response):
            return False
        if self._has_scenario_table(normalized_response):
            return True
        return any(
            pattern in normalized_response for pattern in self._pre_code_patterns
        )

    def _is_terminal_failure(self, normalized_response: str) -> bool:
        return any(
            pattern in normalized_response
            for pattern in self._terminal_failure_patterns
        )

    def _already_confirmed(self, conversation_history: List[Dict[str, Any]]) -> bool:
        for turn in conversation_history:
            user_message = self._normalize(turn.get("user_message", ""))
            if not user_message:
                continue
            if user_message in self._affirmative_messages:
                return True
            if "generate" in user_message and "code" in user_message:
                return True
        return False
