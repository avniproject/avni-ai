#!/usr/bin/env python3
"""
Simplified Form Validation Test Runner
Uses the consolidated comprehensive test matrix
"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import Dict, List, Any

# Add project root to Python path
sys.path.insert(0, str(Path(__file__).parent))

from dotenv import load_dotenv
load_dotenv()

from tests.judge_framework.orchestrator import JudgeOrchestrator
from tests.judge_framework.analytics.statistics import StatisticsCalculator
from tests.judge_framework.analytics.reporting import ReportGenerator
from tests.judge_framework.implementations.formElementValidation import (
    FormElementValidationTestSubjectFactory,
    FormElementValidationExecutorWrapper,
    FormElementValidationJudgeStrategyWrapper
)
from tests.judge_framework.examples.configs.form_validation_config import create_form_validation_test_config


def load_test_matrix() -> List[Dict[str, Any]]:
    """Load the consolidated comprehensive test matrix"""
    matrix_file = "/Users/himeshr/IdeaProjects/avni-ai/tests/judge_framework/test_suites/formElementValidation/comprehensive_form_validation_test_matrix.json"
    
    if not os.path.exists(matrix_file):
        print(f"❌ Test matrix file not found: {matrix_file}")
        print(f"   Run the test generation script first to create test cases")
        return []
    
    try:
        with open(matrix_file, 'r') as f:
            test_cases = json.load(f)
        print(f"✅ Loaded {len(test_cases)} test cases from comprehensive test matrix")
        return test_cases
    except Exception as e:
        print(f"❌ Failed to load test matrix: {e}")
        return []


def run_form_validation_tests(fail_fast: bool = False) -> bool:
    """Run the comprehensive form validation test suite"""
    print("🧪 Form Validation Test Runner - Comprehensive Suite")
    print("=" * 60)
    
    # Validate environment
    required_vars = ["OPENAI_API_KEY", "DIFY_FORM_VALIDATION_API_KEY", "DIFY_API_BASE_URL", "AVNI_AUTH_TOKEN", "AVNI_MCP_SERVER_URL"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"❌ Missing environment variables: {missing_vars}")
        return False
    
    print("✅ Environment validation passed")
    
    # Load test cases
    test_cases = load_test_matrix()
    if not test_cases:
        return False
    
    # Set up test components
    config = create_form_validation_test_config()
    executor = FormElementValidationExecutorWrapper(config)
    judge_strategy = FormElementValidationJudgeStrategyWrapper(config)
    orchestrator = JudgeOrchestrator(executor, judge_strategy)
    
    print(f"\n🚀 Running comprehensive test suite with {len(test_cases)} test cases...")
    
    try:
        # Configure test execution
        test_config = create_form_validation_test_config()
        test_config.generation_config.static_test_cases = test_cases
        test_config.generation_config.ai_generation_enabled = False
        
        # Run test suite
        suite_result = orchestrator.run_test_suite(
            test_subject_factory=FormElementValidationTestSubjectFactory([]),
            config=test_config,
            fail_fast=fail_fast
        )
        
        print(f"\n📊 Comprehensive Test Results:")
        print(f"   Total Tests: {suite_result.total_tests}")
        print(f"   Successful: {suite_result.successful_tests}")
        print(f"   Failed: {suite_result.failed_tests}")
        print(f"   Success Rate: {suite_result.success_rate:.1f}%")
        
        # Generate reports
        statistics = StatisticsCalculator.calculate_suite_statistics(suite_result)
        console_report = ReportGenerator.generate_console_report(suite_result, statistics)
        print(console_report)
        
        # Save reports
        report_dir = "/Users/himeshr/IdeaProjects/avni-ai/tests/judge_framework/reports/formElementValidation"
        os.makedirs(report_dir, exist_ok=True)
        
        # Use single consolidated report file
        report_file = f"{report_dir}/form_validation_report.json"
        csv_file = f"{report_dir}/form_validation_report.csv"
        json_report = ReportGenerator.generate_json_report(suite_result, statistics)
        ReportGenerator.save_report_to_file(json_report, report_file)
        
        # Success criteria - target 70%+ success rate
        threshold = 70.0
        success = suite_result.success_rate >= threshold
        
        if success:
            print(f"\n✅ Comprehensive test suite PASSED: {suite_result.success_rate:.1f}% >= {threshold}%")
        else:
            print(f"\n❌ Comprehensive test suite FAILED: {suite_result.success_rate:.1f}% < {threshold}%")
        
        return success
        
    except Exception as e:
        print(f"❌ Test execution failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Main entry point for the simplified test runner"""
    parser = argparse.ArgumentParser(description="Form Validation Test Runner")
    parser.add_argument(
        "--fail-fast",
        action="store_true",
        help="Stop on first failure"
    )
    
    args = parser.parse_args()
    
    success = run_form_validation_tests(args.fail_fast)
    
    print(f"\n🏁 Form Validation Testing {'✅ PASSED' if success else '❌ FAILED'}")
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
