"""
Configuration example for form validation testing
This demonstrates how to extend the framework for new test types
"""

import os
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent))

from tests.judge_framework.interfaces.result_models import (
    TestConfiguration, 
    DifyConfig, 
    EvaluationConfig, 
    TestGenerationConfig
)


def create_form_validation_test_config() -> TestConfiguration:
    """Create configuration for form validation testing"""
    
    # Dify configuration for form validation workflow
    dify_config = DifyConfig(
        api_key=os.getenv("DIFY_FORM_VALIDATION_API_KEY", os.getenv("DIFY_API_KEY", "")),
        base_url=os.getenv("DIFY_API_BASE_URL", "https://api.dify.ai/v1"),
        workflow_name="avni_form_assistant",  # Exact name from YAML
        test_user="form_validation_tester",
        timeout_seconds=60
    )
    
    # Evaluation configuration for form validation
    evaluation_config = EvaluationConfig(
        evaluation_metrics=[
            "validation_correctness",
            "rule_coverage", 
            "recommendation_quality",
            "completeness"
        ],
        success_thresholds={
            "validation_correctness": 75.0,
            "rule_coverage": 70.0,
            "recommendation_quality": 75.0,
            "completeness": 70.0
        },
        openai_model="gpt-4o",
        openai_temperature=0.1,
        include_detailed_analysis=True
    )
    
    # Static test cases for form validation
    static_test_cases = [
        {
            "form_name": "Patient Registration Form",
            "form_definition": {
                "name": "Patient Registration",
                "fields": [
                    {"name": "firstName", "type": "text", "required": True},
                    {"name": "lastName", "type": "text", "required": True},
                    {"name": "age", "type": "number", "required": True, "min": 0, "max": 150},
                    {"name": "email", "type": "email", "required": False}
                ]
            },
            "validation_rules": [
                {"field": "firstName", "rule": "required", "message": "First name is required"},
                {"field": "age", "rule": "range", "min": 0, "max": 150, "message": "Age must be between 0 and 150"}
            ],
            "test_scenarios": [
                {"input": {"firstName": "John", "age": 25}, "expected": "valid"},
                {"input": {"age": -5}, "expected": "invalid"},
                {"input": {"firstName": "", "age": 25}, "expected": "invalid"}
            ],
            "expected_behavior": "Form should validate required fields and age constraints correctly"
        },
        {
            "form_name": "Medical History Form",
            "form_definition": {
                "name": "Medical History",
                "fields": [
                    {"name": "hasDiabetes", "type": "boolean", "required": True},
                    {"name": "diabetesType", "type": "select", "required": False, "options": ["Type 1", "Type 2"]},
                    {"name": "lastCheckup", "type": "date", "required": True}
                ]
            },
            "validation_rules": [
                {"field": "diabetesType", "rule": "conditional_required", "condition": "hasDiabetes=true"},
                {"field": "lastCheckup", "rule": "date_not_future", "message": "Checkup date cannot be in the future"}
            ],
            "test_scenarios": [
                {"input": {"hasDiabetes": True, "diabetesType": "Type 1", "lastCheckup": "2024-01-15"}, "expected": "valid"},
                {"input": {"hasDiabetes": True, "lastCheckup": "2024-01-15"}, "expected": "invalid"},
                {"input": {"hasDiabetes": False, "lastCheckup": "2025-12-01"}, "expected": "invalid"}
            ],
            "expected_behavior": "Form should handle conditional validation and date constraints"
        }
    ]
    
    generation_config = TestGenerationConfig(
        static_test_cases=static_test_cases,
        ai_generation_enabled=True,
        ai_generation_prompt="Generate additional form validation test cases with complex validation rules",
        num_ai_cases=1
    )
    
    return TestConfiguration(
        dify_config=dify_config,
        evaluation_config=evaluation_config,
        generation_config=generation_config,
        max_iterations=1,  # Form validation is typically single-turn
        custom_report_sections=["validation_rule_analysis", "edge_case_coverage"]
    )
