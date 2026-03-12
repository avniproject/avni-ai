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

FORM TYPE: {reference_context.get("formType", "Unknown")}
ENCOUNTER TYPE: {reference_context.get("encounterType", "Unknown")}

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

Evaluate this run on ALL required metrics including helper_method_correctness and return JSON only.
"""

        ai_evaluation = self._call_openai_for_evaluation(evaluation_context)
        scores = self._normalize_scores(ai_evaluation.get("scores", {}))

        # Always derive overall_success from scores — never trust the LLM's
        # overall_success field, which can contradict the numeric scores.
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

=== AVNI HELPER METHODS REFERENCE ===

Use these rules to judge helper method correctness:

OBSERVATION ACCESS:
- getObservationReadableValue(conceptName) → returns String (coded answer name, formatted date)
  Use for: displaying values, comparing to string literals (e.g., === 'SAM', === 'Yes')
- getObservationValue(conceptName) → returns raw value (Number, Date, UUID for coded)
  Use for: numeric comparisons (>, <, ===) with numbers, date arithmetic
- findObservation(conceptName) → returns Observation object
  Use for: checking existence, accessing .getValue(), .isAbnormal()

CRITICAL RULE: Never compare getObservationReadableValue() result to a number using > or <.
  WRONG: programEncounter.getObservationReadableValue('hba1c') > 9
  RIGHT: programEncounter.getObservationValue('hba1c') > 9
  ALSO VALID: programEncounter.getObservationReadableValue('status') === 'SAM'  (string comparison)

AGE METHODS (on Individual):
- individual.getAgeInYears() → Number: use for year-based age conditions
- individual.getAgeInMonths() → Number: use for infant/pediatric age checks (< 5 years)
- individual.getAgeInWeeks() → Number: use for newborn checks (< 6 weeks)
- individual.getAge() → Duration object: use for display only

Access pattern from ProgramEncounter: programEncounter.programEnrolment.individual.getAgeInYears()
Access pattern from Encounter: encounter.individual.getAgeInYears()

GENDER METHODS (on Individual):
- individual.isFemale() → Boolean
- individual.isMale() → Boolean
Always gate gender-specific scheduling behind isFemale() or isMale() when the request implies it.

CANCELLATION FORM TYPES (ProgramEncounterCancellation, IndividualEncounterCancellation):
- Use findCancelEncounterObservationReadableValue("Cancellation reason") for reason (string)
- Use findCancelEncounterObservation("Cancel date") for date object, then .getValue() for Date
- NEVER use programEncounter.cancelDateTime or encounter.cancelDateTime (legacy, deprecated)
- NEVER use getCancelReason() (legacy, deprecated)
- Cancellation date fallback: cancelDateObs ? cancelDateObs.getValue() : entity.encounterDateTime
- ProgramEncounterCancellation: entity=programEncounter, builder init: { programEncounter }
- IndividualEncounterCancellation: entity=encounter, builder init: { encounter } OR { individual: encounter.individual } (both valid)

PROGRAM EXIT FORM TYPE:
- Entity is programEnrolment (not programEncounter)
- Access exit date via: programEnrolment.programExitDateTime
- Access individual subject: programEnrolment.individual
- VisitScheduleBuilder init: new imports.rulesConfig.VisitScheduleBuilder({ programEnrolment })
- For REGISTRATION-LEVEL observations on the subject (recorded during registration, e.g. delivery-date,
  school-readiness, transplant-date), use: individual.getObservationValue(conceptName)
  or individual.getObservationReadableValue(conceptName) — this is CORRECT
- For PROGRAM/ENROLMENT-LEVEL observations (recorded during enrolment or program encounters),
  use: programEnrolment.getObservationValue() or programEnrolment.getObservationReadableValue()
- Do NOT use programEncounter in ProgramExit rules — entity is programEnrolment

PROGRAM ENROLMENT FORM TYPE:
- Entity is programEnrolment
- VisitScheduleBuilder init: new imports.rulesConfig.VisitScheduleBuilder({ programEnrolment })
- Access enrolment date: programEnrolment.enrolmentDateTime

ENCOUNTER FORM TYPE (General/Individual):
- Entity is encounter (not programEncounter)
- VisitScheduleBuilder init: new imports.rulesConfig.VisitScheduleBuilder({ encounter })
- No programEnrolment available; access individual via encounter.individual

PROGRAM EXIT GUARD (for ProgramEncounter only):
- Always guard: if (programEncounter.programEnrolment.programExitDateTime) return scheduleBuilder.getAll();
- NOT required for and MUST NOT appear in: ProgramExit, ProgramEnrolment, Encounter,
  ProgramEncounterCancellation, IndividualEncounterCancellation form types
- Having a programEncounter-style exit guard in a cancellation rule is WRONG — penalize

SCHEDULING PATTERNS:
- scheduleBuilder.add({ name, encounterType, earliestDate, maxDate }) — standard
- maxDate should always be AFTER earliestDate (typically 3-14 days after)
- Avoid createNew strategy unless request explicitly requires multiple instances

CROSS-ENCOUNTER OBSERVATION:
- programEnrolment.findLatestObservationInEntireEnrolment(conceptName) → finds latest obs across all encounters
- individual.findLatestObservationFromEncounters(conceptName) → finds latest obs across all individual encounters
- Use these for trend-based scheduling (e.g., "based on latest reading")

=== SCORING METRICS (0-100) ===

1. scenario_validation
   - Did assistant present a realistic scenario/validation table before code?
   - Did it include concrete cases and ask for user confirmation?
   - Score 0 if code was generated directly without scenario step.

2. response_suitability
   - Is the response sequence correct: scenario → confirmation → final code?
   - Is it clear, concise, and context-aware?
   - Penalize (not zero) if confirmation step was absent — deduct 20-30 points.

3. rule_correctness
   - Does the final rule implement the requested scheduling logic correctly?
   - Does it use VisitScheduleBuilder with correct entity initialization?
   - Is the correct entity used (programEncounter vs encounter vs programEnrolment)?
   - Are all branches from the request implemented?

4. timing_accuracy
   - Are offsets/thresholds/anchors from the request reflected correctly in code?
   - Are date anchors appropriate (encounterDateTime, programExitDateTime, lmpDate, cancelDate)?
   - Are time units correct (days, weeks, months)?

5. code_quality
   - Is it executable, production-ready JavaScript?
   - Are null/undefined guards present for observations used in numeric comparisons?
   - Is the code free of deprecated API usage?

6. helper_method_correctness
   - Is getObservationValue used for numeric comparisons (not getObservationReadableValue)?
   - Is getObservationReadableValue used for string/coded comparisons?
   - Are cancellation helpers (findCancelEncounterObservation*) used for cancellation form types?
   - Is the correct individual access chain used (programEncounter.programEnrolment.individual)?
   - Are age methods used correctly (getAgeInYears vs getAgeInMonths vs getAgeInWeeks)?
   - Are gender guards (isFemale/isMale) used when gender-specific scheduling is required?
   - Is cross-encounter observation lookup (findLatestObservationInEntireEnrolment) used when appropriate?

=== TOLERANCE FOR EXTRA DEFENSIVE CHECKS ===
The generated code may include extra defensive checks not in the reference rule, such as:
- Additional encounter type name verification
- Duplicate scheduling guards (checking existing scheduled visits)
- Extra null checks beyond what's strictly necessary
These are NOT errors — they show defensive coding. Do NOT penalize rule_correctness or code_quality
for extra guards that don't change the core logic. Only penalize if the extra logic is WRONG
(e.g., wrong entity name, wrong API call) or if a REQUIRED check from the request is MISSING.

=== PENALIZE THESE PATTERNS ===
- Using cancelDateTime property directly (e.g. programEncounter.cancelDateTime, encounter.cancelDateTime) in cancellation rules → SEVERE deduction from helper_method_correctness (this is the #1 cancellation error)
- Using getCancelReason() in cancellation rules → SEVERE deduction from helper_method_correctness
- Not using findCancelEncounterObservation("Cancel date") for cancel date in cancellation rules → deduct from helper_method_correctness
- Not using findCancelEncounterObservationReadableValue("Cancellation reason") for cancel reason in cancellation rules → deduct from helper_method_correctness
- getObservationReadableValue() result compared numerically (> < >= <=) → deduct from helper_method_correctness
  (e.g., const hba1c = entity.getObservationReadableValue('hba1c'); if (hba1c > 9) — WRONG)
- getCancelReason() or .cancelDateTime in cancellation forms → deduct from helper_method_correctness
- Program exit guard (hasExitedProgram / programExitDateTime check) in cancellation rules → deduct from rule_correctness
- programEncounter entity used in ProgramExit rules → deduct from rule_correctness
- isFemale()/isMale() missing when request explicitly requires gender-specific scheduling → deduct from rule_correctness
- individual.getAgeInYears() used when request requires pediatric age (< 2 years) — should use getAgeInMonths() → deduct from helper_method_correctness
- individual.getAgeInYears() used when request requires newborn age (< 6 weeks) — should use getAgeInWeeks() → deduct from helper_method_correctness
- Unused observation variable (read but never referenced in logic) → deduct from code_quality
- maxDate set to BEFORE or equal to earliestDate → deduct from code_quality
- No null/undefined guard before numeric observation comparison → deduct from code_quality
- createNew strategy without duplicate guard → deduct from code_quality

Return STRICT JSON only in this format:
{
  "scores": {
    "scenario_validation": <0-100>,
    "response_suitability": <0-100>,
    "rule_correctness": <0-100>,
    "timing_accuracy": <0-100>,
    "code_quality": <0-100>,
    "helper_method_correctness": <0-100>
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
            "helper_method_aware": True,
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
            "helper_method_correctness",
        ]

    @staticmethod
    def _default_thresholds() -> Dict[str, float]:
        return {
            "scenario_validation": 75.0,
            "response_suitability": 75.0,
            "rule_correctness": 80.0,
            "timing_accuracy": 85.0,
            "code_quality": 75.0,
            "helper_method_correctness": 80.0,
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
        _CONFIRMATION_TOKENS = {
            "yes",
            "y",
            "ok",
            "okay",
            "proceed",
            "go ahead",
            "looks good",
            "approved",
            "confirmed",
            "confirm",
            "sure",
            "yep",
            "yup",
            "correct",
            "that's correct",
            "sounds good",
            "perfect",
            "great",
        }
        # Keywords that indicate a confirmation message containing a code-generation request
        _CONFIRMATION_KEYWORDS = (
            "scenarios look correct",
            "scenarios are correct",
            "looks correct",
            "generate the final",
            "generate the rule code",
            "please generate",
            "go ahead and generate",
            "proceed with generating",
            "generate the executable",
        )
        for turn in conversation_history:
            user_message = (turn.get("user_message", "") or "").strip().lower()
            if not user_message:
                continue
            # Exact match against known short confirmation tokens
            if user_message in _CONFIRMATION_TOKENS:
                return True
            # Short message (≤ 30 chars) that starts with an affirmative
            if len(user_message) <= 30 and any(
                user_message.startswith(token)
                for token in ("yes", "ok", "sure", "confirm", "proceed")
            ):
                return True
            # Longer confirmation message (strategy sends "YES. These scenarios look correct...")
            if any(keyword in user_message for keyword in _CONFIRMATION_KEYWORDS):
                return True
        return False
