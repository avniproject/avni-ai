"""
Conversation executor that wraps existing DifyClient and integrates with the new framework
"""

from typing import Dict, Any, Optional
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent))

from tests.judge_framework.interfaces.test_executor import ConversationExecutor
from tests.judge_framework.interfaces.result_models import TestConfiguration
from tests.judge_framework.interfaces.conversation_strategy import (
    ConversationGenerationStrategy,
    AIConversationStrategy,
)


class ConversationExecutorWrapper(ConversationExecutor):
    """
    Wrapper that adapts the existing conversation execution logic to the new framework
    """

    def __init__(
        self,
        config: TestConfiguration,
        scenario_prompts: list,
        conversation_strategy: Optional[ConversationGenerationStrategy] = None,
    ):
        """
        Initialize with existing conversation testing components

        Args:
            config: Test configuration
            scenario_prompts: List of scenario prompts from existing testing system
            conversation_strategy: Optional custom conversation strategy
        """
        # Create AI conversation strategy if not provided
        if conversation_strategy is None:
            conversation_strategy = AIConversationStrategy(
                scenario_prompts=scenario_prompts,
                openai_model=config.openai_model,
                temperature=0.5,  # Use moderate temperature for conversation generation
            )

        super().__init__(config, conversation_strategy)
        self.scenario_prompts = scenario_prompts

    def execute(self, test_input: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute conversation test using the framework's ConversationExecutor
        This method leverages the existing conversation strategy integration
        """
        return super().execute(test_input)

    def get_executor_metadata(self) -> Dict[str, Any]:
        """Get metadata including information about wrapped components"""
        metadata = super().get_executor_metadata()
        metadata.update(
            {
                "executor_type": "ConversationExecutorWrapper",
                "scenario_prompts_count": len(self.scenario_prompts),
                "wraps_existing_logic": True,
            }
        )
        return metadata
