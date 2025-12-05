"""
Conversation generation strategy for pluggable message generation
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any


class ConversationGenerationStrategy(ABC):
    """
    Strategy interface for generating conversation messages
    Allows different implementations (AI-based, rule-based, etc.)
    """

    @abstractmethod
    def generate_next_message(
        self, conversation_history: List[Dict[str, Any]], context: Dict[str, Any]
    ) -> str:
        """
        Generate the next message in a conversation

        Args:
            conversation_history: List of previous conversation turns
            context: Additional context (scenario, test objectives, etc.)

        Returns:
            Next message to send, or empty string to end conversation
        """
        pass

    @abstractmethod
    def should_continue_conversation(
        self, conversation_history: List[Dict[str, Any]], context: Dict[str, Any]
    ) -> bool:
        """
        Determine if conversation should continue

        Args:
            conversation_history: List of previous conversation turns
            context: Additional context

        Returns:
            True if conversation should continue, False otherwise
        """
        pass


class AIConversationStrategy(ConversationGenerationStrategy):
    """
    AI-powered conversation generation using OpenAI
    Reuses the existing AITester logic
    """

    def __init__(
        self,
        scenario_prompts: List[str],
        openai_model: str = "gpt-4o",
        temperature: float = 0.5,
    ):
        self.scenario_prompts = scenario_prompts
        self.openai_model = openai_model
        self.temperature = temperature

    def generate_next_message(
        self, conversation_history: List[Dict[str, Any]], context: Dict[str, Any]
    ) -> str:
        """
        Generate next message using AI (similar to existing AITester)
        """
        import openai

        scenario_index = context.get("scenario_index", 0)
        if scenario_index >= len(self.scenario_prompts):
            return ""

        # Convert conversation history for AI tester perspective
        tester_history = self._convert_to_tester_perspective(conversation_history)

        try:
            messages = [
                {"role": "system", "content": self.scenario_prompts[scenario_index]}
            ] + tester_history

            response = openai.chat.completions.create(
                model=self.openai_model,
                messages=messages,
                temperature=self.temperature,
                max_tokens=500,
            )

            return response.choices[0].message.content.strip()

        except Exception as e:
            print(f"Error in AI conversation generation: {e}")
            return ""

    def should_continue_conversation(
        self, conversation_history: List[Dict[str, Any]], context: Dict[str, Any]
    ) -> bool:
        """
        Determine if conversation should continue based on length and content
        """
        max_iterations = context.get("max_iterations", 4)
        current_length = len(conversation_history)

        # Continue if we haven't reached max iterations
        if current_length < max_iterations:
            return True

        return False

    def _convert_to_tester_perspective(
        self, conversation_history: List[Dict[str, Any]]
    ) -> List[Dict[str, str]]:
        """
        Convert conversation history to tester's perspective
        User messages become assistant responses, and vice versa
        """
        tester_history = []
        for turn in conversation_history:
            user_msg = turn.get("user_message", "")
            assistant_msg = turn.get("assistant_response", "")

            if user_msg:
                # Tester's message becomes assistant response
                tester_history.append({"role": "assistant", "content": user_msg})
            if assistant_msg:
                # Assistant's response becomes user input to tester
                tester_history.append({"role": "user", "content": assistant_msg})

        return tester_history


class RuleBasedConversationStrategy(ConversationGenerationStrategy):
    """
    Rule-based conversation generation for predictable testing
    """

    def __init__(self, message_sequence: List[str]):
        self.message_sequence = message_sequence

    def generate_next_message(
        self, conversation_history: List[Dict[str, Any]], context: Dict[str, Any]
    ) -> str:
        """
        Generate next message from predefined sequence
        """
        current_index = len(conversation_history)
        if current_index < len(self.message_sequence):
            return self.message_sequence[current_index]
        return ""

    def should_continue_conversation(
        self, conversation_history: List[Dict[str, Any]], context: Dict[str, Any]
    ) -> bool:
        """
        Continue if we have more messages in sequence
        """
        current_index = len(conversation_history)
        return current_index < len(self.message_sequence)


class EndConversationStrategy(ConversationGenerationStrategy):
    """
    Strategy that immediately ends conversation (for single-turn testing)
    """

    def generate_next_message(
        self, conversation_history: List[Dict[str, Any]], context: Dict[str, Any]
    ) -> str:
        return ""

    def should_continue_conversation(
        self, conversation_history: List[Dict[str, Any]], context: Dict[str, Any]
    ) -> bool:
        return False
