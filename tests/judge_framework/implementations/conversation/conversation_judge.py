"""
Conversation judge strategy that wraps existing AIReviewer logic
"""

from typing import Dict, Any
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent))

from tests.judge_framework.interfaces.judge_strategy import JudgeStrategy
from tests.judge_framework.interfaces.result_models import (
    TestConfiguration,
    EvaluationResult,
)


class ConversationJudgeStrategyWrapper(JudgeStrategy):
    """
    Wrapper that adapts the existing ConversationJudgeStrategy to work with the new framework
    while preserving the existing evaluation logic
    """

    def __init__(self, config: TestConfiguration):
        """
        Initialize with configuration that preserves existing evaluation criteria
        """
        # Set up default evaluation metrics for conversations if not provided
        if not config.evaluation_config.evaluation_metrics:
            config.evaluation_config.evaluation_metrics = [
                "configuration_correctness",
                "consistency",
                "communication_quality",
                "task_completion",
            ]

        # Set default success thresholds if not provided
        if not config.evaluation_config.success_thresholds:
            config.evaluation_config.success_thresholds = {
                "configuration_correctness": 75.0,
                "consistency": 75.0,
                "communication_quality": 75.0,
                "task_completion": 75.0,
            }

        super().__init__(config)

        # Instantiate the wrapped strategy once for efficiency
        from ...interfaces.judge_strategy import ConversationJudgeStrategy

        self._wrapped_strategy = ConversationJudgeStrategy(config)

    def evaluate(
        self, test_input: Dict[str, Any], test_output: Dict[str, Any]
    ) -> EvaluationResult:
        """
        Evaluate conversation using the existing ConversationJudgeStrategy logic
        This method preserves the existing evaluation approach while adapting to new interfaces
        """
        # Use the pre-instantiated wrapped strategy
        result = self._wrapped_strategy.evaluate(test_input, test_output)

        # Add wrapper-specific metadata
        result.execution_metadata.update(
            {"wrapped_existing_logic": True, "wrapper_version": "1.0"}
        )

        return result

    def _get_evaluation_prompt(self) -> str:
        """Get the evaluation prompt from the existing conversation judge strategy"""
        from ...interfaces.judge_strategy import ConversationJudgeStrategy

        temp_strategy = ConversationJudgeStrategy(self.config)
        return temp_strategy._get_evaluation_prompt()

    def _get_evaluation_metrics(self) -> list:
        """Get evaluation metrics from configuration"""
        return self.config.evaluation_config.evaluation_metrics
