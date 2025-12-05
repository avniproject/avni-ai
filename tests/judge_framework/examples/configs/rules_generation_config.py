import json

from src.utils.env import DIFY_API_KEY, DIFY_API_BASE_URL
from tests.judge_framework.interfaces.result_models import (
    TestConfiguration,
    DifyConfig,
    EvaluationConfig,
    TestGenerationConfig,
)
from tests.judge_framework.test_suites.rulesGeneration.visit_schedule_rule_examples import (
    VISIT_SCHEDULE_RULE_EXAMPLES,
)

_ALL_EXAMPLES = VISIT_SCHEDULE_RULE_EXAMPLES


def create_rules_generation_test_config() -> TestConfiguration:
    dify_config = DifyConfig(
        api_key=DIFY_API_KEY or "",
        base_url=DIFY_API_BASE_URL,
        workflow_name="avni_rules_assistant",
        test_user="rules_tester",
        timeout_seconds=180,
    )

    evaluation_config = EvaluationConfig(
        evaluation_metrics=[
            "rule_correctness",
            "timing_accuracy",
            "code_quality",
            "user_communication",
        ],
        success_thresholds={
            "rule_correctness": 80.0,
            "timing_accuracy": 85.0,
            "code_quality": 75.0,
            "user_communication": 75.0,
        },
        openai_model="gpt-4o",
        openai_temperature=0.1,
        include_detailed_analysis=True,
    )

    static_test_cases = []
    for i, example in enumerate(_ALL_EXAMPLES):
        static_test_cases.append(
            {
                "scenario": example["scenario"],
                "scenario_index": i,
                "initial_query": example["rule_request"],
                "reference_rule": example["expected_generated_rule"].strip(),
                "reference_context": example["context"],
                "rule_request": example["rule_request"],
                "expected_behavior": "Generate correct JavaScript scheduling rule matching the reference implementation.",
            }
        )

    generation_config = TestGenerationConfig(
        static_test_cases=static_test_cases,
        ai_generation_enabled=False,
        ai_generation_prompt="",
        num_ai_cases=0,
    )

    return TestConfiguration(
        dify_config=dify_config,
        evaluation_config=evaluation_config,
        generation_config=generation_config,
        max_iterations=10,
        custom_report_sections=["rules_generation_analysis"],
    )


def create_rules_generation_prompts() -> list[str]:
    prompts = []

    for example in _ALL_EXAMPLES:
        context_json = json.dumps(example["context"], indent=2)
        prompt = f"{example['scenario']}\n\nContext:\n{context_json}"
        prompts.append(prompt)

    return prompts


__all__ = ["create_rules_generation_test_config", "create_rules_generation_prompts"]
