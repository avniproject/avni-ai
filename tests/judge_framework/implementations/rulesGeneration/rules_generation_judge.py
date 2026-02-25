import json
from typing import Dict, Any, List

from tests.judge_framework.interfaces.judge_strategy import JudgeStrategy
from tests.judge_framework.interfaces.result_models import (
    TestConfiguration,
    EvaluationResult,
)


class RulesGenerationJudgeWrapper(JudgeStrategy):
    """
    Rules-specific AI judge.
    Evaluates conversation protocol adherence and final JavaScript rule quality.
    """

    def __init__(self, config: TestConfiguration):
        if not config.evaluation_config.evaluation_metrics:
            config.evaluation_config.evaluation_metrics = self._default_metrics()

        if not config.evaluation_config.success_thresholds:
            config.evaluation_config.success_thresholds = self._default_thresholds()

        super().__init__(config)

    def evaluate(
        self, test_input: Dict[str, Any], test_output: Dict[str, Any]
    ) -> EvaluationResult:
        test_identifier = test_input.get("test_identifier", "unknown")
        conversation_history = test_output.get("conversation_history", []) or []
        reference_context = test_input.get("reference_context", {})
        reference_rule = test_input.get("reference_rule", "")
        rule_request = test_input.get("rule_request", test_input.get("query", ""))

        scenario_response = self._extract_scenario_response(conversation_history)
        final_response = self._extract_final_rule_response(conversation_history)
        confirmation_detected = self._confirmation_turn_exists(conversation_history)

        evaluation_context = f"""
TEST IDENTIFIER: {test_identifier}

RULE REQUEST:
{rule_request}

REFERENCE CONTEXT:
{json.dumps(reference_context, indent=2)}

REFERENCE RULE:
```javascript
{reference_rule}
```

CONVERSATION HISTORY:
{json.dumps(conversation_history, indent=2)}

SCENARIO/VALIDATION RESPONSE (first assistant response):
{scenario_response}

FINAL ASSISTANT RESPONSE (expected JS rule):
{final_response}

WAS USER CONFIRMATION TURN PRESENT?:
{confirmation_detected}

Evaluate this run on the required metrics and return JSON only.
"""

        ai_evaluation = self._call_openai_for_evaluation(evaluation_context)
        scores = self._normalize_scores(ai_evaluation.get("scores", {}))

        overall_success = ai_evaluation.get("overall_success")
        if not isinstance(overall_success, bool):
            overall_success = self._calculate_overall_success(scores)

        return EvaluationResult(
            test_identifier=test_identifier,
            test_type="rules_generation",
            success=overall_success,
            scores=scores,
            details={
                "scenario": test_input.get("scenario", ""),
                "conversation_length": len(conversation_history),
                "confirmation_detected": confirmation_detected,
                "scenario_response_excerpt": scenario_response[:2000],
                "final_response_excerpt": final_response[:3000],
                "ai_evaluation": ai_evaluation,
            },
            error_categories=ai_evaluation.get("error_categories", []),
            error_message=ai_evaluation.get("error_message"),
            execution_metadata={
                "total_iterations": test_output.get("total_iterations", 0),
                "final_conversation_id": test_output.get("final_conversation_id", ""),
                "judge_type": "rules_generation_ai_judge",
                "evaluation_mode": "ai_primary",
            },
            raw_input=test_input,
            raw_output=test_output,
        )

    def _get_evaluation_prompt(self) -> str:
        return """
You are an expert evaluator for Avni visit schedule rule generation conversations.

Your job is to evaluate BOTH:
1) Scenario validation quality before code generation
2) Final JavaScript rule quality and suitability

Score strictly on these metrics (0-100):
1. scenario_validation
   - Did assistant present a realistic validation/scenario table before code?
   - Did it include concrete cases and ask for confirmation?
2. response_suitability
   - Is the response sequence suitable (scenario -> confirm -> final code)?
   - Is it clear, concise, and context-aware?
3. rule_correctness
   - Does final rule implement requested scheduling logic correctly?
   - Does it use VisitScheduleBuilder and valid schedule output structure?
4. timing_accuracy
   - Are offsets/thresholds/anchors in request reflected in code logic?
5. code_quality
   - Is it executable, production-ready JavaScript with robust structure?

Important Avni-specific checks:
- Penalize if code is generated before confirmation.
- Penalize if scenario table/pre-validation is missing.
- Penalize if final answer is not executable JavaScript rule.
- For cancellation form types, check helper usage:
  - findCancelEncounterObservation(...)
  - findCancelEncounterObservationReadableValue(...)
- For ProgramExit form type, check exit-date-based scheduling logic.
- Penalize unsafe scheduling patterns (duplicate encounter type overwrite risk,
  createNew without dedupe guard).

Return STRICT JSON only in this format:
{
  "scores": {
    "scenario_validation": <0-100>,
    "response_suitability": <0-100>,
    "rule_correctness": <0-100>,
    "timing_accuracy": <0-100>,
    "code_quality": <0-100>
  },
  "overall_success": <true/false>,
  "error_categories": ["<optional categories>"],
  "detailed_analysis": "<short summary>",
  "issues": ["<specific issues found>"],
  "strengths": ["<specific strengths found>"]
}

EVALUATION INPUT:
"""

    def _get_evaluation_metrics(self) -> List[str]:
        configured = self.config.evaluation_config.evaluation_metrics
        if configured:
            return configured
        return self._default_metrics()

    def get_judge_metadata(self) -> Dict[str, Any]:
        return {
            "judge_type": "RulesGenerationJudgeWrapper",
            "evaluation_focus": "visit_schedule_rules",
            "supported_metrics": self._get_evaluation_metrics(),
            "javascript_aware": True,
            "protocol_aware": True,
            "uses_openai_for_judging": True,
        }

    def _normalize_scores(self, raw_scores: Dict[str, Any]) -> Dict[str, float]:
        normalized = {}
        for metric in self._get_evaluation_metrics():
            value = raw_scores.get(metric, 0)
            try:
                value = float(value)
            except (TypeError, ValueError):
                value = 0.0

            normalized[metric] = max(0.0, min(100.0, value))
        return normalized

    @staticmethod
    def _default_metrics() -> List[str]:
        return [
            "scenario_validation",
            "response_suitability",
            "rule_correctness",
            "timing_accuracy",
            "code_quality",
        ]

    @staticmethod
    def _default_thresholds() -> Dict[str, float]:
        return {
            "scenario_validation": 75.0,
            "response_suitability": 75.0,
            "rule_correctness": 80.0,
            "timing_accuracy": 85.0,
            "code_quality": 75.0,
        }

    @staticmethod
    def _extract_scenario_response(conversation_history: List[Dict[str, Any]]) -> str:
        for turn in conversation_history:
            response = turn.get("assistant_response", "")
            if response:
                return response
        return ""

    @staticmethod
    def _extract_final_rule_response(conversation_history: List[Dict[str, Any]]) -> str:
        if not conversation_history:
            return ""

        code_markers = (
            "```javascript",
            "```js",
            '"use strict";',
            "({params, imports}) =>",
            "({ params, imports }) =>",
            "VisitScheduleBuilder",
        )

        for turn in reversed(conversation_history):
            response = turn.get("assistant_response", "") or ""
            if any(marker in response for marker in code_markers):
                return response

        return conversation_history[-1].get("assistant_response", "")

    @staticmethod
    def _confirmation_turn_exists(conversation_history: List[Dict[str, Any]]) -> bool:
        for turn in conversation_history:
            user_message = (turn.get("user_message", "") or "").strip().lower()
            if user_message in {
                "yes",
                "y",
                "ok",
                "okay",
                "proceed",
                "go ahead",
                "looks good",
                "approved",
                "confirmed",
            }:
                return True
        return False
