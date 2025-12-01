"""
Correct Form Element Validation judge strategy that matches the actual Dify workflow
"""

from typing import Dict, Any
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent))

from tests.judge_framework.interfaces.form_validation_judge import (
    DifyFormValidationJudgeStrategy,
)
from tests.judge_framework.interfaces.result_models import (
    TestConfiguration,
    EvaluationResult,
)


class FormElementValidationJudgeStrategyWrapper(DifyFormValidationJudgeStrategy):
    """
    Wrapper for form element validation judge strategy that evaluates Dify workflow results
    """

    def __init__(self, config: TestConfiguration):
        """
        Initialize with configuration that preserves form validation evaluation criteria
        """
        # Set up default evaluation metrics for form validation if not provided
        if not config.evaluation_config.evaluation_metrics:
            config.evaluation_config.evaluation_metrics = [
                "validation_correctness",
                "rule_coverage",
                "recommendation_quality",
                "completeness",
                "performance_score",
            ]

        # Set default success thresholds if not provided
        if not config.evaluation_config.success_thresholds:
            config.evaluation_config.success_thresholds = {
                "validation_correctness": 75.0,
                "rule_coverage": 70.0,
                "recommendation_quality": 75.0,
                "completeness": 70.0,
                "performance_score": 75.0,  # Require acceptable performance (≤1500ms)
            }

        super().__init__(config)

    def evaluate(
        self, test_input: Dict[str, Any], test_output: Dict[str, Any]
    ) -> EvaluationResult:
        """
        Evaluate form validation using the Dify Form Assistant workflow logic
        """
        # Use the parent class evaluation logic
        result = super().evaluate(test_input, test_output)

        # Add wrapper-specific metadata
        result.execution_metadata.update(
            {
                "wrapped_existing_logic": True,
                "wrapper_version": "1.0",
                "validation_workflow": "dify_form_assistant",
            }
        )

        return result
