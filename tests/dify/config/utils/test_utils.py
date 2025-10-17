"""General utility functions for integration tests."""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Any

logger = logging.getLogger(__name__)


def save_test_results(
    result: Dict[str, Any], test_name: str, logs_dir_path: Path
) -> Path:
    """Save test results to JSON file in logs directory"""
    logs_dir_path.mkdir(exist_ok=True)

    output_file = (
        logs_dir_path
        / f"{test_name}_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    )

    with open(output_file, "w") as f:
        json.dump(result, f, indent=2)

    return output_file


def print_test_results(result: Dict[str, Any], test_name: str) -> None:
    """Print formatted test results to console"""
    print(f"\n📊 {test_name} Integration Test Results:")
    print("=" * 50)
    print(f"Test ID: {result['test_id']}")
    print(f"Success: {'✅ PASS' if result['success'] else '❌ FAIL'}")

    if result["success"]:
        validation = result["validation"]
        print("\n🎯 Validation Scores:")
        scores = validation["scores"]
        print(
            f"  • Functional Adequacy: {scores.get('functional_adequacy', 'N/A')}/100"
        )
        print(
            f"  • Structural Correctness: {scores.get('structural_correctness', 'N/A')}/100"
        )
        print(f"  • Completeness: {scores.get('completeness', 'N/A')}/100")

        config_assessment = validation["configuration_assessment"]
        print("\n📋 Configuration Created:")
        print(
            f"  • Subject Types: {len(config_assessment.get('subject_types_created', []))}"
        )
        print(f"  • Programs: {len(config_assessment.get('programs_created', []))}")
        print(f"  • Encounters: {len(config_assessment.get('encounters_created', []))}")
        print(f"  • Catchments: {len(config_assessment.get('catchments_created', []))}")

    else:
        print(f"\n💥 Error: {result.get('error', 'Unknown error')}")


def validate_environment_variables(*required_vars: str) -> bool:
    """Validate that all required environment variables are set"""
    import os

    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)

    if missing_vars:
        print("❌ Error: Missing required environment variables:")
        for var in missing_vars:
            print(f"   - {var}")
        return False

    return True
