"""
Test runner for Spec Agent testing.

Executes Spec Agent tests using the judge framework with conversation variable
injection and monitoring capabilities.
"""

import argparse
import json
import logging
import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from tests.judge_framework.orchestrator import (  # noqa: E402
    JudgeOrchestrator,
    ConsoleProgressReporter,
)
from tests.judge_framework.implementations.specAgent import (  # noqa: E402
    SpecAgentTestSubjectFactory,
    SpecAgentExecutor,
    SpecAgentJudge,
)
from tests.judge_framework.interfaces.result_models import (  # noqa: E402
    TestConfiguration,
    DifyConfig,
    EvaluationConfig,
    TestGenerationConfig,
)
from tests.judge_framework.analytics.statistics import StatisticsCalculator  # noqa: E402
from tests.judge_framework.analytics.reporting import ReportGenerator  # noqa: E402
from tests.judge_framework.implementations.specAgent.monitoring import (  # noqa: E402
    ConversationMonitor,
)

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def load_test_scenarios(scenarios_file: str) -> list:
    """Load test scenarios from JSON file."""
    with open(scenarios_file, "r") as f:
        data = json.load(f)
    return data.get("test_scenarios", [])


def create_test_configuration() -> TestConfiguration:
    """Create test configuration from environment variables."""
    config = TestConfiguration(
        dify_config=DifyConfig(
            api_key=os.getenv("DIFY_API_KEY", ""),
            base_url=os.getenv("DIFY_API_BASE_URL", "https://api.dify.ai/v1"),
            workflow_name="App Configurator [Staging] v3",
        ),
        evaluation_config=EvaluationConfig(
            evaluation_metrics=[
                "tool_call_correctness",
                "spec_validity",
                "entity_coverage",
                "conversation_flow",
            ],
            success_thresholds={
                "tool_call_correctness": 80.0,
                "spec_validity": 90.0,
                "entity_coverage": 70.0,
                "conversation_flow": 60.0,
            },
        ),
        generation_config=TestGenerationConfig(
            static_test_cases=[],  # Loaded separately
            ai_generation_enabled=False,
        ),
    )
    # Add custom attributes for Avni integration
    config.avni_auth_token = os.getenv("AVNI_AUTH_TOKEN", "")
    config.avni_mcp_server_url = os.getenv(
        "AVNI_MCP_SERVER_URL", "https://staging-ai.avniproject.org/"
    )
    return config


def run_spec_agent_tests(
    scenarios_file: str,
    entities_file: str,
    fail_fast: bool = False,
    output_format: str = "console",
    monitor_conversations: bool = True,
) -> int:
    """
    Run Spec Agent tests.

    Args:
        scenarios_file: Path to test scenarios JSON
        entities_file: Path to entities summary JSON
        fail_fast: Stop on first failure
        output_format: Output format (console, json, csv)
        monitor_conversations: Whether to monitor conversation state

    Returns:
        Exit code (0 for success, 1 for failure)
    """
    logger.info("Starting Spec Agent tests with v3 workflow")

    # Load configuration
    config = create_test_configuration()

    # Validate environment
    if not config.dify_config.api_key:
        logger.error("DIFY_API_KEY not set. Please set it in environment.")
        return 1

    if not config.avni_mcp_server_url:
        logger.error("AVNI_MCP_SERVER_URL not set. Please set it in environment.")
        return 1

    # Load test scenarios
    scenarios = load_test_scenarios(scenarios_file)
    logger.info(f"Loaded {len(scenarios)} test scenarios")

    # Add scenarios to config so TestSubjectGenerator can use them
    config.generation_config.static_test_cases = scenarios

    # Create factory
    factory = SpecAgentTestSubjectFactory(entities_file)

    # Create executor and judge
    executor = SpecAgentExecutor(config)
    judge = SpecAgentJudge(config)

    # Create orchestrator
    orchestrator = JudgeOrchestrator(
        executor=executor,
        judge_strategy=judge,
        progress_reporter=ConsoleProgressReporter(),
    )

    # Run tests
    logger.info("Executing tests...")
    suite_result = orchestrator.run_test_suite(
        test_subject_factory=factory,
        config=config,
        fail_fast=fail_fast,
    )

    # Monitor conversations if enabled
    if monitor_conversations and config.avni_mcp_server_url:
        monitor = ConversationMonitor(config.avni_mcp_server_url)
        logger.info("\n" + "=" * 60)
        logger.info("Conversation Monitoring Summary")
        logger.info("=" * 60)

        for result in suite_result.results:
            conv_id = result.evaluation_details.get("conversation_id", "")
            if conv_id:
                logger.info(f"\nTest: {result.test_identifier}")
                monitor.print_conversation_summary(conv_id)

    # Calculate statistics
    statistics = StatisticsCalculator.calculate_statistics(suite_result.results)

    # Generate report
    if output_format == "console":
        report = ReportGenerator.generate_report(statistics, suite_result.results)
        print("\n" + "=" * 60)
        print("SPEC AGENT TEST REPORT")
        print("=" * 60)
        print(report)
    elif output_format == "json":
        report = ReportGenerator.generate_json_report(statistics, suite_result.results)
        print(json.dumps(report, indent=2))
    elif output_format == "csv":
        csv_report = ReportGenerator.generate_csv_report(suite_result.results)
        print(csv_report)

    # Return exit code based on success
    success_rate = (
        (statistics.success_count / statistics.total_tests * 100)
        if statistics.total_tests > 0
        else 0
    )
    logger.info(f"\nOverall Success Rate: {success_rate:.1f}%")

    return 0 if success_rate >= 70.0 else 1


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Run Spec Agent tests")
    parser.add_argument(
        "--scenarios",
        default="tests/judge_framework/test_suites/specAgent/spec_agent_test_scenarios.json",
        help="Path to test scenarios JSON file",
    )
    parser.add_argument(
        "--entities",
        default="tests/resources/scoping/entities_summary.json",
        help="Path to entities summary JSON file",
    )
    parser.add_argument(
        "--fail-fast",
        action="store_true",
        help="Stop on first test failure",
    )
    parser.add_argument(
        "--output-format",
        choices=["console", "json", "csv"],
        default="console",
        help="Output format for test results",
    )
    parser.add_argument(
        "--no-monitor",
        action="store_true",
        help="Disable conversation monitoring",
    )

    args = parser.parse_args()

    # Validate files exist
    scenarios_path = Path(args.scenarios)
    entities_path = Path(args.entities)

    if not scenarios_path.exists():
        logger.error(f"Scenarios file not found: {args.scenarios}")
        return 1

    if not entities_path.exists():
        logger.error(f"Entities file not found: {args.entities}")
        return 1

    # Run tests
    exit_code = run_spec_agent_tests(
        scenarios_file=str(scenarios_path),
        entities_file=str(entities_path),
        fail_fast=args.fail_fast,
        output_format=args.output_format,
        monitor_conversations=not args.no_monitor,
    )

    return exit_code


if __name__ == "__main__":
    sys.exit(main())
