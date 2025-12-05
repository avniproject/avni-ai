from typing import Dict, Any

from tests.judge_framework.implementations.conversation.conversation_executor import (
    ConversationExecutorWrapper,
)
from tests.judge_framework.interfaces.result_models import TestConfiguration
from .rules_generation_conversation_strategy import RulesGenerationConversationStrategy


class RulesGenerationExecutorWrapper(ConversationExecutorWrapper):
    def __init__(self, config: TestConfiguration, scenario_prompts: list[str]):
        # Use rules-specific conversation strategy
        rules_strategy = RulesGenerationConversationStrategy()
        super().__init__(config, scenario_prompts, rules_strategy)

    def execute(self, test_input: Dict[str, Any]) -> Dict[str, Any]:
        return super().execute(test_input)

    def get_executor_metadata(self) -> Dict[str, Any]:
        metadata = super().get_executor_metadata()
        metadata.update(
            {
                "executor_type": "RulesGenerationExecutorWrapper",
                "workflow_type": "rules_generation",
                "validates_against_avni_rules": True,
                "supports_visit_scheduling": True,
                "test_focus": "visit_schedule_rule_generation",
            }
        )
        return metadata
