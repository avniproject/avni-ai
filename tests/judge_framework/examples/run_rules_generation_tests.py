#!/usr/bin/env python3
import argparse
import sys

from src.utils.env import OPENAI_API_KEY, DIFY_API_KEY
from tests.judge_framework.orchestrator import (
    JudgeOrchestrator,
    ConsoleProgressReporter,
)
from tests.judge_framework.analytics.statistics import StatisticsCalculator
from tests.judge_framework.analytics.reporting import ReportGenerator
from tests.judge_framework.implementations.rulesGeneration import (
    RulesGenerationExecutorWrapper,
    RulesGenerationJudgeWrapper,
)
from tests.judge_framework.implementations.conversation import (
    ConversationTestSubjectFactory,
)
from tests.judge_framework.examples.configs.rules_generation_config import (
    create_rules_generation_test_config,
    create_rules_generation_prompts,
)


def validate_environment():
    missing_vars = []

    if not OPENAI_API_KEY:
        missing_vars.append("OPENAI_API_KEY")

    if not DIFY_API_KEY:
        missing_vars.append("DIFY_API_KEY")

    if missing_vars:
        print(f"❌ Missing required environment variables: {', '.join(missing_vars)}")
        return False

    return True


def setup_rules_test_components(config):
    tester_prompts = create_rules_generation_prompts()

    # Create test subject factory
    test_subject_factory = ConversationTestSubjectFactory(tester_prompts)

    # Create rules generation executor
    executor = RulesGenerationExecutorWrapper(
        config=config, scenario_prompts=tester_prompts
    )

    # Create judge strategy
    judge_strategy = RulesGenerationJudgeWrapper(config)

    # Create orchestrator
    orchestrator = JudgeOrchestrator(
        executor=executor,
        judge_strategy=judge_strategy,
        progress_reporter=ConsoleProgressReporter(),
    )

    return orchestrator, test_subject_factory


def run_rules_generation_tests(args):
    """Run rules generation tests"""

    print("🚀 Starting Rules Generation Testing with Judge Framework")
    print("=" * 60)

    # Validate environment
    if not validate_environment():
        sys.exit(1)

    # Create test configuration
    config = create_rules_generation_test_config()
    print(f"📋 Configuration loaded for workflow: {config.dify_config.workflow_name}")
    print(f"   Static test cases: {len(config.generation_config.static_test_cases)}")
    print(f"   AI-generated cases: {config.generation_config.num_ai_cases}")
    print(
        f"   Evaluation metrics: {', '.join(config.evaluation_config.evaluation_metrics)}"
    )

    # Set up test components
    orchestrator, test_subject_factory = setup_rules_test_components(config)

    # Run test suite
    print(f"\n🧪 Running rules generation tests...")
    suite_result = orchestrator.run_test_suite(
        test_subject_factory=test_subject_factory,
        config=config,
        fail_fast=args.fail_fast,
    )

    # Calculate statistics
    statistics = StatisticsCalculator.calculate_suite_statistics(suite_result)

    # Generate reports
    print(f"\n📊 Generating reports...")

    if args.output_format in ["console", "all"]:
        console_report = ReportGenerator.generate_console_report(
            suite_result, statistics
        )
        print(console_report)

    if args.output_format in ["json", "all"]:
        json_report = ReportGenerator.generate_json_report(suite_result, statistics)
        ReportGenerator.save_report_to_file(
            json_report, "rules_generation_test_report.json"
        )

    if args.output_format in ["csv", "all"]:
        csv_report = ReportGenerator.generate_csv_report(suite_result)
        ReportGenerator.save_report_to_file(
            csv_report, "rules_generation_test_report.csv"
        )

    # Print summary
    print(f"\n✅ Test execution completed!")
    print(f"   Success Rate: {suite_result.success_rate:.1f}%")
    print(f"   Total Tests: {suite_result.total_tests}")
    print(f"   Successful: {suite_result.successful_tests}")
    print(f"   Failed: {suite_result.failed_tests}")

    return suite_result.success_rate >= 75.0


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Run rules generation tests using the Judge Framework",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run_rules_generation_tests.py
  python run_rules_generation_tests.py --output-format json
  python run_rules_generation_tests.py --fail-fast --output-format all
        """,
    )

    parser.add_argument(
        "--output-format",
        choices=["console", "json", "csv", "all"],
        default="console",
        help="Output format for reports (default: console)",
    )

    parser.add_argument(
        "--fail-fast", action="store_true", help="Stop testing on first failure"
    )

    args = parser.parse_args()

    print("🧪 Rules Generation Testing Tool")
    print("=" * 50)

    try:
        success = run_rules_generation_tests(args)
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n⚠️  Test execution interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
