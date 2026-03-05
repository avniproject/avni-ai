import json
import os

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


def _resolve_examples():
    start_raw = os.getenv("RULES_GENERATION_START", "").strip()
    max_raw = os.getenv("RULES_GENERATION_MAX_CASES", "").strip()

    start = 0
    if start_raw:
        try:
            start = max(0, int(start_raw))
        except ValueError:
            start = 0

    examples = VISIT_SCHEDULE_RULE_EXAMPLES[start:]

    if max_raw:
        try:
            count = int(max_raw)
            if count > 0:
                examples = examples[:count]
        except ValueError:
            pass

    return examples


_ALL_EXAMPLES = _resolve_examples()


def create_rules_generation_test_config() -> TestConfiguration:
    dify_config = DifyConfig(
        api_key=DIFY_API_KEY or "",
        base_url=DIFY_API_BASE_URL,
        workflow_name="avni_rules_assistant",
        test_user=os.getenv("DIFY_TEST_USER", "rules_tester"),
        timeout_seconds=180,
    )

    evaluation_config = EvaluationConfig(
        evaluation_metrics=[
            "scenario_validation",
            "response_suitability",
            "rule_correctness",
            "timing_accuracy",
            "code_quality",
            "helper_method_correctness",
        ],
        success_thresholds={
            "scenario_validation": 75.0,
            "response_suitability": 75.0,
            "rule_correctness": 80.0,
            "timing_accuracy": 85.0,
            "code_quality": 75.0,
            "helper_method_correctness": 80.0,
        },
        openai_model="gpt-4o",
        openai_temperature=0.1,
        include_detailed_analysis=True,
    )

    static_test_cases = []
    for i, example in enumerate(_ALL_EXAMPLES):
        context = example["context"]
        form_type = context.get("formType", "")
        encounter_type = context.get("encounterType", "")
        concepts = context.get("concepts", [])

        # Embed form_type and encounterType directly in the query so Dify never needs
        # to ask clarifying questions about the entity type or encounter name.
        enriched_query = example["rule_request"]
        if form_type:
            enriched_query = f"[Form type: {form_type}] {enriched_query}"
        if encounter_type:
            enriched_query += f" (Encounter type: {encounter_type})"
        if concepts:
            enriched_query += f". Available concepts: {', '.join(concepts)}"

        # For cancellation form types, add explicit helper method hints so Dify's
        # RAG retrieves the correct KB chunks instead of falling back to deprecated APIs.
        if form_type in ("ProgramEncounterCancellation", "IndividualEncounterCancellation"):
            enriched_query += (
                ". IMPORTANT: Use findCancelEncounterObservationReadableValue(\"Cancellation reason\") for cancellation reason"
                " and findCancelEncounterObservation(\"Cancel date\").getValue() for cancellation date."
                " Do NOT use cancelDateTime or getCancelReason — they are deprecated."
            )

        static_test_cases.append(
            {
                "scenario": example["scenario"],
                "scenario_index": i,
                "initial_query": enriched_query,
                "reference_rule": example["expected_generated_rule"].strip(),
                "reference_context": context,
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
