#!/usr/bin/env python3

import json
import argparse
from pathlib import Path
from typing import Dict, List, Any

from tests.judge_framework.test_suites.rulesGeneration.visit_schedule_rule_examples import (
    VISIT_SCHEDULE_RULE_EXAMPLES,
)


def get_tests() -> List[Dict[str, Any]]:
    test_cases = []

    for i, example in enumerate(VISIT_SCHEDULE_RULE_EXAMPLES):
        test_cases.append(
            {
                "test_case_name": f"rule_{example['id']}_{example['scenario'][:30].replace(' ', '_').lower()}",
                "scenario": example["scenario"],
                "context": example["context"],
                "rule_request": example["rule_request"],
                "expected_rule": example["expected_generated_rule"].strip(),
                "test_priority": "HIGH",
                "test_type": "rules_generation",
                "form_type": example["context"]["formType"],
                "encounter_type": example["context"]["encounterType"],
            }
        )

    return test_cases


def save_test_matrix(test_cases: List[Dict[str, Any]], filename: str) -> bool:
    try:
        output_dir = Path(__file__).parent.parent / "test_suites" / "rulesGeneration"
        output_dir.mkdir(parents=True, exist_ok=True)

        output_file = output_dir / filename
        with open(output_file, "w") as f:
            json.dump(test_cases, f, indent=2)

        print(f"✅ Test matrix saved to: {output_file}")
        return True

    except Exception as e:
        print(f"❌ Failed to save test matrix: {e}")
        return False


def main():
    """Main entry point for rules generation test generator"""
    parser = argparse.ArgumentParser(description="Rules Generation Test Generator")
    parser.add_argument(
        "--filename",
        default="rules_generation_test_matrix.json",
        help="Output filename (default: rules_generation_test_matrix.json)",
    )

    args = parser.parse_args()

    print("🧪 Rules Generation Test Generator")
    print("=" * 50)

    # Generate test cases
    test_cases = get_tests()
    print(f"📊 Generated {len(test_cases)} test cases from rule examples")

    # Save test matrix
    success = save_test_matrix(test_cases, args.filename)

    # Generate summary
    if success and test_cases:
        summary = {
            "total_test_cases": len(test_cases),
            "form_types_covered": list(set(tc["form_type"] for tc in test_cases)),
            "encounter_types_covered": list(
                set(tc["encounter_type"] for tc in test_cases)
            ),
            "source": "VISIT_SCHEDULE_RULE_EXAMPLES",
        }

        print("📋 Summary:")
        print(f"   Total test cases: {summary['total_test_cases']}")
        print(f"   Form types: {len(summary['form_types_covered'])}")
        print(f"   Encounter types: {len(summary['encounter_types_covered'])}")

        # Save summary
        summary_file = (
            Path(__file__).parent.parent
            / "test_suites"
            / "rulesGeneration"
            / "test_generation_summary.json"
        )
        with open(summary_file, "w") as f:
            json.dump(summary, f, indent=2)

        print(f"✅ Summary saved to: {summary_file}")

    return 0 if success else 1


if __name__ == "__main__":
    exit(main())
