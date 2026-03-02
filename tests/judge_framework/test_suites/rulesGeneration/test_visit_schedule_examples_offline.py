"""
Offline validation of the 100 visit-schedule rule examples.
Runs instantly — no Dify / OpenAI calls needed.

Validates:
  1. Example structure & required keys
  2. Context consistency (formType, encounterType, concepts, etc.)
  3. Expected rule code quality (syntax markers, builder usage, date logic)
  4. Distribution across form types
  5. Uniqueness of IDs and scenarios

Usage:
  .venv/bin/python -m pytest tests/judge_framework/test_suites/rulesGeneration/test_visit_schedule_examples_offline.py -v
"""

import re
import pytest
from collections import Counter

from tests.judge_framework.test_suites.rulesGeneration.visit_schedule_rule_examples import (
    VISIT_SCHEDULE_RULE_EXAMPLES,
)

# ── constants ─────────────────────────────────────────────────────────────────

VALID_FORM_TYPES = {
    "ProgramEncounter",
    "Encounter",
    "ProgramEnrolment",
    "ProgramEncounterCancellation",
    "IndividualEncounterCancellation",
    "ProgramExit",
}

REQUIRED_EXAMPLE_KEYS = {"id", "scenario", "context", "rule_request", "expected_generated_rule"}
REQUIRED_CONTEXT_KEYS = {"formType"}  # minimum; encounterType is optional for some

# Patterns that should appear in every well-formed generated rule
RULE_MUST_CONTAIN = [
    "use strict",                   # strict-mode pragma
    "params",                       # destructured params
    "imports",                      # destructured imports
    "scheduleBuilder",              # builder variable
    "VisitScheduleBuilder",         # builder constructor
    "scheduleBuilder.getAll()",     # return value
]

# At least one date helper must be used
DATE_PATTERNS = [
    r"moment\(",
    r"\.add\(",
    r"\.subtract\(",
    r"\.toDate\(\)",
    r"earliestDate",
    r"maxDate",
]


# ── fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture(scope="module")
def all_examples():
    return VISIT_SCHEDULE_RULE_EXAMPLES


@pytest.fixture(scope="module")
def examples_by_form_type(all_examples):
    grouped = {}
    for ex in all_examples:
        ft = ex["context"].get("formType", "Unknown")
        grouped.setdefault(ft, []).append(ex)
    return grouped


# ── structural tests ──────────────────────────────────────────────────────────

class TestExampleStructure:
    """Verify that every example has the required shape."""

    def test_total_count(self, all_examples):
        assert len(all_examples) == 100, (
            f"Expected 100 examples, got {len(all_examples)}"
        )

    def test_unique_ids(self, all_examples):
        ids = [e["id"] for e in all_examples]
        duplicates = [id_ for id_, cnt in Counter(ids).items() if cnt > 1]
        assert not duplicates, f"Duplicate IDs found: {duplicates}"

    def test_ids_are_sequential(self, all_examples):
        ids = [e["id"] for e in all_examples]
        assert ids == list(range(1, 101)), "IDs should be 1..100 in order"

    def test_unique_scenarios(self, all_examples):
        scenarios = [e["scenario"] for e in all_examples]
        duplicates = [s for s, cnt in Counter(scenarios).items() if cnt > 1]
        assert not duplicates, f"Duplicate scenarios: {duplicates}"

    @pytest.mark.parametrize(
        "example",
        VISIT_SCHEDULE_RULE_EXAMPLES,
        ids=[f"id_{e['id']}" for e in VISIT_SCHEDULE_RULE_EXAMPLES],
    )
    def test_required_keys(self, example):
        missing = REQUIRED_EXAMPLE_KEYS - example.keys()
        assert not missing, (
            f"Example {example.get('id', '?')} missing keys: {missing}"
        )

    @pytest.mark.parametrize(
        "example",
        VISIT_SCHEDULE_RULE_EXAMPLES,
        ids=[f"id_{e['id']}" for e in VISIT_SCHEDULE_RULE_EXAMPLES],
    )
    def test_context_has_form_type(self, example):
        ctx = example["context"]
        assert "formType" in ctx, f"Example {example['id']} context missing formType"
        assert ctx["formType"] in VALID_FORM_TYPES, (
            f"Example {example['id']} has invalid formType: {ctx['formType']}"
        )

    @pytest.mark.parametrize(
        "example",
        VISIT_SCHEDULE_RULE_EXAMPLES,
        ids=[f"id_{e['id']}" for e in VISIT_SCHEDULE_RULE_EXAMPLES],
    )
    def test_rule_request_non_empty(self, example):
        assert example["rule_request"].strip(), (
            f"Example {example['id']} has empty rule_request"
        )

    @pytest.mark.parametrize(
        "example",
        VISIT_SCHEDULE_RULE_EXAMPLES,
        ids=[f"id_{e['id']}" for e in VISIT_SCHEDULE_RULE_EXAMPLES],
    )
    def test_expected_rule_non_empty(self, example):
        assert example["expected_generated_rule"].strip(), (
            f"Example {example['id']} has empty expected_generated_rule"
        )


# ── form-type distribution ────────────────────────────────────────────────────

class TestFormTypeDistribution:
    """Ensure roughly equal coverage across all 6 form types."""

    def test_all_form_types_present(self, examples_by_form_type):
        missing = VALID_FORM_TYPES - set(examples_by_form_type.keys())
        assert not missing, f"Missing form types: {missing}"

    def test_no_unknown_form_types(self, examples_by_form_type):
        extra = set(examples_by_form_type.keys()) - VALID_FORM_TYPES
        assert not extra, f"Unexpected form types: {extra}"

    def test_minimum_per_form_type(self, examples_by_form_type):
        for ft, examples in examples_by_form_type.items():
            assert len(examples) >= 10, (
                f"Form type '{ft}' has only {len(examples)} examples (min 10)"
            )

    def test_maximum_per_form_type(self, examples_by_form_type):
        for ft, examples in examples_by_form_type.items():
            assert len(examples) <= 20, (
                f"Form type '{ft}' has {len(examples)} examples (max 20)"
            )


# ── context quality ───────────────────────────────────────────────────────────

class TestContextQuality:
    """Validate that context objects are well-formed."""

    @pytest.mark.parametrize(
        "example",
        VISIT_SCHEDULE_RULE_EXAMPLES,
        ids=[f"id_{e['id']}" for e in VISIT_SCHEDULE_RULE_EXAMPLES],
    )
    def test_encounter_types_list(self, example):
        ctx = example["context"]
        if ctx["formType"] in ("ProgramEncounter", "ProgramEncounterCancellation",
                                "ProgramEnrolment", "ProgramExit"):
            assert "encounterTypes" in ctx, (
                f"Example {example['id']} ({ctx['formType']}) should have encounterTypes"
            )
            assert isinstance(ctx["encounterTypes"], list), (
                f"Example {example['id']} encounterTypes must be a list"
            )
            assert len(ctx["encounterTypes"]) > 0, (
                f"Example {example['id']} has empty encounterTypes"
            )

    @pytest.mark.parametrize(
        "example",
        VISIT_SCHEDULE_RULE_EXAMPLES,
        ids=[f"id_{e['id']}" for e in VISIT_SCHEDULE_RULE_EXAMPLES],
    )
    def test_concepts_list(self, example):
        ctx = example["context"]
        if "concepts" in ctx:
            assert isinstance(ctx["concepts"], list), (
                f"Example {example['id']} concepts must be a list"
            )
            assert len(ctx["concepts"]) > 0, (
                f"Example {example['id']} has empty concepts list"
            )


# ── expected rule code quality ────────────────────────────────────────────────

class TestExpectedRuleQuality:
    """Validate that reference rules look like valid Avni visit-schedule rules."""

    @pytest.mark.parametrize(
        "example",
        VISIT_SCHEDULE_RULE_EXAMPLES,
        ids=[f"id_{e['id']}" for e in VISIT_SCHEDULE_RULE_EXAMPLES],
    )
    def test_rule_contains_strict_mode(self, example):
        rule = example["expected_generated_rule"]
        assert '"use strict"' in rule, (
            f"Example {example['id']} rule missing \"use strict\""
        )

    @pytest.mark.parametrize(
        "example",
        VISIT_SCHEDULE_RULE_EXAMPLES,
        ids=[f"id_{e['id']}" for e in VISIT_SCHEDULE_RULE_EXAMPLES],
    )
    def test_rule_contains_builder(self, example):
        rule = example["expected_generated_rule"]
        assert "VisitScheduleBuilder" in rule, (
            f"Example {example['id']} rule missing VisitScheduleBuilder"
        )
        assert "scheduleBuilder.getAll()" in rule, (
            f"Example {example['id']} rule missing scheduleBuilder.getAll()"
        )

    @pytest.mark.parametrize(
        "example",
        VISIT_SCHEDULE_RULE_EXAMPLES,
        ids=[f"id_{e['id']}" for e in VISIT_SCHEDULE_RULE_EXAMPLES],
    )
    def test_rule_contains_params_imports(self, example):
        rule = example["expected_generated_rule"]
        assert "params" in rule and "imports" in rule, (
            f"Example {example['id']} rule missing params/imports destructuring"
        )

    @pytest.mark.parametrize(
        "example",
        VISIT_SCHEDULE_RULE_EXAMPLES,
        ids=[f"id_{e['id']}" for e in VISIT_SCHEDULE_RULE_EXAMPLES],
    )
    def test_rule_has_date_logic(self, example):
        rule = example["expected_generated_rule"]
        has_date = any(re.search(p, rule) for p in DATE_PATTERNS)
        assert has_date, (
            f"Example {example['id']} rule has no date logic "
            f"(expected moment/add/subtract/earliestDate/maxDate)"
        )

    @pytest.mark.parametrize(
        "example",
        VISIT_SCHEDULE_RULE_EXAMPLES,
        ids=[f"id_{e['id']}" for e in VISIT_SCHEDULE_RULE_EXAMPLES],
    )
    def test_rule_has_schedule_add(self, example):
        rule = example["expected_generated_rule"]
        assert "scheduleBuilder.add(" in rule, (
            f"Example {example['id']} rule never calls scheduleBuilder.add()"
        )

    @pytest.mark.parametrize(
        "example",
        VISIT_SCHEDULE_RULE_EXAMPLES,
        ids=[f"id_{e['id']}" for e in VISIT_SCHEDULE_RULE_EXAMPLES],
    )
    def test_rule_schedules_have_name_and_type(self, example):
        rule = example["expected_generated_rule"]
        # Every scheduleBuilder.add() call should include name and encounterType
        assert "name:" in rule.replace('"name"', "name:").replace("'name'", "name:"), (
            f"Example {example['id']} scheduled visit missing 'name' field"
        )
        assert "encounterType:" in rule.replace('"encounterType"', "encounterType:").replace("'encounterType'", "encounterType:"), (
            f"Example {example['id']} scheduled visit missing 'encounterType' field"
        )

    @pytest.mark.parametrize(
        "example",
        VISIT_SCHEDULE_RULE_EXAMPLES,
        ids=[f"id_{e['id']}" for e in VISIT_SCHEDULE_RULE_EXAMPLES],
    )
    def test_rule_matches_form_type_pattern(self, example):
        """Verify the rule uses the right entity variable for its formType."""
        rule = example["expected_generated_rule"]
        ft = example["context"]["formType"]

        if ft == "ProgramEncounter" or ft == "ProgramEncounterCancellation":
            assert "programEncounter" in rule, (
                f"Example {example['id']} ({ft}) should reference programEncounter"
            )
        elif ft == "Encounter" or ft == "IndividualEncounterCancellation":
            # Encounter-based rules use 'encounter' or 'individual'
            has_encounter = "encounter" in rule.lower()
            assert has_encounter, (
                f"Example {example['id']} ({ft}) should reference encounter"
            )
        elif ft == "ProgramEnrolment":
            assert "programEnrolment" in rule, (
                f"Example {example['id']} ({ft}) should reference programEnrolment"
            )
        elif ft == "ProgramExit":
            assert "programEnrolment" in rule, (
                f"Example {example['id']} ({ft}) should reference programEnrolment"
            )


# ── cross-example consistency ─────────────────────────────────────────────────

class TestCrossExampleConsistency:
    """Check relationships across examples."""

    def test_scenario_describes_rule_request(self, all_examples):
        """scenario and rule_request should relate (both non-empty, different)."""
        for ex in all_examples:
            assert ex["scenario"] != ex["rule_request"], (
                f"Example {ex['id']}: scenario and rule_request are identical"
            )

    def test_encounter_type_in_context(self, all_examples):
        """If encounterType is in context, it should appear in encounterTypes list."""
        for ex in all_examples:
            ctx = ex["context"]
            et = ctx.get("encounterType")
            ets = ctx.get("encounterTypes", [])
            if et and ets:
                et_names = [e["name"] if isinstance(e, dict) else e for e in ets]
                assert et in et_names, (
                    f"Example {ex['id']}: encounterType '{et}' not in encounterTypes list"
                )
