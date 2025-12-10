"""
Rules Generation Conversation Strategy for the Judge Framework
"""

from typing import Dict, Any, List

from tests.judge_framework.interfaces.conversation_strategy import ConversationGenerationStrategy


class RulesGenerationConversationStrategy(ConversationGenerationStrategy):
    """
    Conversation strategy for rules generation that knows when to end conversations
    based on rule generation patterns
    """

    def __init__(self):
        pass

    def generate_next_message(
        self, conversation_history: List[Dict[str, Any]], context: Dict[str, Any]
    ) -> str:
        """
        Generate the next user message for rules generation conversation
        """
        if len(conversation_history) < 1:
            return ""
            
        # Get the last assistant response
        last_assistant_response = conversation_history[-1].get("assistant_response", "")
        
        # If assistant is asking for confirmation, respond with YES
        if ("Reply YES" in last_assistant_response or 
            "tell me what to change" in last_assistant_response or
            "Do these scenarios match exactly what you want?" in last_assistant_response):
            return "YES"
            
        # Otherwise, no more messages needed
        return ""

    def should_continue_conversation(
        self, conversation_history: List[Dict[str, Any]], context: Dict[str, Any]
    ) -> bool:
        """
        Determine if rules generation conversation should continue
        Rules generation conversations should end when:
        1. Assistant provides the final JavaScript rule code
        2. Assistant provides final explanation after rule code
        """
        if len(conversation_history) < 1:
            return True  # Always continue if no history yet
        
        # Get the last assistant response
        last_assistant_response = conversation_history[-1].get("assistant_response", "")
        
        # Check if the last assistant response contains JavaScript code
        has_rule_code = ("```js" in last_assistant_response or 
                        "```javascript" in last_assistant_response or
                        "Js\n\n" in last_assistant_response)
        
        # If assistant just provided rule code, end the conversation
        if has_rule_code:
            return False
        
        # If assistant is asking for confirmation (ends with question or "Reply YES"), continue
        if (last_assistant_response.strip().endswith("?") or 
            "Reply YES" in last_assistant_response or
            "tell me what to change" in last_assistant_response):
            return True
            
        # Continue for clarification but limit to max rounds
        return len(conversation_history) < 5