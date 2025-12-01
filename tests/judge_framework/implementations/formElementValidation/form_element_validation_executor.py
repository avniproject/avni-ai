"""
Correct Form Element Validation executor that matches the actual Dify workflow
"""

from typing import Dict, Any
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent))

from tests.judge_framework.interfaces.form_validation_executor import (
    DifyFormValidationExecutor,
)
from tests.judge_framework.interfaces.result_models import TestConfiguration


class FormElementValidationExecutorWrapper(DifyFormValidationExecutor):
    """
    Wrapper for form element validation that uses the Dify Form Assistant workflow
    """

    def __init__(self, config: TestConfiguration):
        """
        Initialize with form validation configuration

        Args:
            config: Test configuration with Dify API settings
        """
        super().__init__(config)

    def execute(self, test_input: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute form element validation using the Dify Form Assistant workflow
        This matches the actual YAML workflow structure
        """
        return super().execute(test_input)

    def get_executor_metadata(self) -> Dict[str, Any]:
        """Get metadata including information about form validation workflow"""
        metadata = super().get_executor_metadata()
        metadata.update(
            {
                "executor_type": "FormElementValidationExecutorWrapper",
                "workflow_type": "form_validation",
                "validates_against_avni_rules": True,
                "single_turn_validation": True,
            }
        )
        return metadata
