"""
Judge Orchestrator - Template Method pattern coordinator
"""

from typing import List, Dict, Any, Optional, Protocol
from datetime import datetime
import hashlib

from .interfaces.test_subject import (
    TestSubject,
    TestSubjectFactory,
    TestSubjectGenerator,
)
from .interfaces.test_executor import TestExecutor
from .interfaces.judge_strategy import JudgeStrategy
from .interfaces.result_models import (
    EvaluationResult,
    TestSuiteResult,
    TestConfiguration,
)


class ProgressReporter(Protocol):
    """Protocol for pluggable progress reporting"""

    def on_test_suite_start(self, test_type: str, total_tests: int):
        """Called when test suite starts"""
        pass

    def on_test_start(self, test_identifier: str, test_number: int, total_tests: int):
        """Called when individual test starts"""
        pass

    def on_test_complete(
        self, result: EvaluationResult, test_number: int, total_tests: int
    ):
        """Called when individual test completes"""
        pass

    def on_test_suite_complete(self, suite_result: TestSuiteResult):
        """Called when test suite completes"""
        pass


class ConsoleProgressReporter:
    """Simple console-based progress reporter"""

    def on_test_suite_start(self, test_type: str, total_tests: int):
        print(f"\n🧪 Starting {test_type} test suite with {total_tests} tests")

    def on_test_start(self, test_identifier: str, test_number: int, total_tests: int):
        print(f"  📋 Test {test_number}/{total_tests}: {test_identifier}")

    def on_test_complete(
        self, result: EvaluationResult, test_number: int, total_tests: int
    ):
        status = "✅" if result.success else "❌"
        print(f"    {status} {result.test_identifier} - Success: {result.success}")
        if result.error_message:
            print(f"      ⚠️  Error: {result.error_message}")

    def on_test_suite_complete(self, suite_result: TestSuiteResult):
        print(f"\n📊 {suite_result.test_type} Test Suite Complete:")
        print(f"   Total: {suite_result.total_tests}")
        print(f"   ✅ Successful: {suite_result.successful_tests}")
        print(f"   ❌ Failed: {suite_result.failed_tests}")
        print(f"   📈 Success Rate: {suite_result.success_rate:.1f}%")


class JudgeOrchestrator:
    """
    Simple orchestrator that coordinates test execution using Template Method pattern
    """

    def __init__(
        self,
        executor: TestExecutor,
        judge_strategy: JudgeStrategy,
        progress_reporter: Optional[ProgressReporter] = None,
    ):
        self.executor = executor
        self.judge_strategy = judge_strategy
        self.progress_reporter = progress_reporter or ConsoleProgressReporter()

    def run_test_suite(
        self,
        test_subject_factory: TestSubjectFactory,
        config: TestConfiguration,
        fail_fast: bool = False,
    ) -> TestSuiteResult:
        """
        Template method: Execute complete test suite workflow
        """
        # 1. Generate test subjects
        test_subjects = self._generate_test_subjects(test_subject_factory, config)

        # 2. Initialize suite result
        start_time = datetime.now().isoformat()
        suite_result = TestSuiteResult(
            test_type=self._get_test_type_name(test_subject_factory),
            total_tests=len(test_subjects),
            successful_tests=0,
            failed_tests=0,
            success_rate=0.0,
            start_time=start_time,
            configuration_hash=self._calculate_config_hash(config),
        )

        # 3. Report suite start
        self.progress_reporter.on_test_suite_start(
            suite_result.test_type, len(test_subjects)
        )

        # 4. Execute individual tests
        for i, test_subject in enumerate(test_subjects):
            test_number = i + 1

            # Report test start
            self.progress_reporter.on_test_start(
                test_subject.get_test_identifier(), test_number, len(test_subjects)
            )

            # Execute test
            result = self._execute_single_test(test_subject)

            # Update suite statistics
            if result.success:
                suite_result.successful_tests += 1
            else:
                suite_result.failed_tests += 1
                if fail_fast:
                    print(f"\n🛑 Stopping early due to failure (fail_fast=True)")
                    break

            # Store result
            suite_result.individual_results.append(result)

            # Report test completion
            self.progress_reporter.on_test_complete(
                result, test_number, len(test_subjects)
            )

        # 5. Finalize suite result
        suite_result.end_time = datetime.now().isoformat()
        suite_result.success_rate = (
            (suite_result.successful_tests / suite_result.total_tests * 100)
            if suite_result.total_tests > 0
            else 0
        )

        # 6. Calculate aggregated statistics
        self._calculate_suite_statistics(suite_result)

        # 7. Report suite completion
        self.progress_reporter.on_test_suite_complete(suite_result)

        return suite_result

    def _generate_test_subjects(
        self, factory: TestSubjectFactory, config: TestConfiguration
    ) -> List[TestSubject]:
        """Generate test subjects using mixed approach"""
        generator = TestSubjectGenerator(factory)
        return generator.generate_test_suite(
            config, config.generation_config.num_ai_cases
        )

    def _execute_single_test(self, test_subject: TestSubject) -> EvaluationResult:
        """Execute a single test and evaluate it"""
        try:
            # Get test input
            test_input = test_subject.get_test_input()
            test_input.update(
                {
                    "test_identifier": test_subject.get_test_identifier(),
                    "expected_behavior": test_subject.get_expected_behavior(),
                    "evaluation_context": test_subject.get_evaluation_context(),
                }
            )

            # Execute test
            test_output = self.executor.execute(test_input)

            # Evaluate result
            result = self.judge_strategy.evaluate(test_input, test_output)

            return result

        except Exception as e:
            # Return error result if anything fails
            return EvaluationResult(
                test_identifier=test_subject.get_test_identifier(),
                test_type=self._get_test_type_name(test_subject),
                success=False,
                timestamp=datetime.now().isoformat(),
                error_message=str(e),
                error_categories=["execution_error"],
            )

    def _calculate_suite_statistics(self, suite_result: TestSuiteResult):
        """Calculate aggregated statistics for the test suite"""
        if not suite_result.individual_results:
            return

        # Calculate average scores
        all_scores = {}
        score_sums = {}
        score_counts = {}

        for result in suite_result.individual_results:
            for metric, score in result.scores.items():
                if metric not in score_sums:
                    score_sums[metric] = 0
                    score_counts[metric] = 0
                score_sums[metric] += score
                score_counts[metric] += 1

        for metric in score_sums:
            suite_result.average_scores[metric] = (
                score_sums[metric] / score_counts[metric]
            )

        # Calculate error summary
        error_counts = {}
        for result in suite_result.individual_results:
            for category in result.error_categories:
                error_counts[category] = error_counts.get(category, 0) + 1

        suite_result.error_summary = error_counts
        suite_result.common_errors = sorted(
            error_counts.keys(), key=lambda x: error_counts[x], reverse=True
        )

    def _get_test_type_name(self, factory: TestSubjectFactory) -> str:
        """Extract test type name from factory class"""
        factory_name = factory.__class__.__name__
        # Remove "Factory" suffix and convert to lowercase
        if factory_name.endswith("Factory"):
            return factory_name[:-7].lower()
        return factory_name.lower()

    def _calculate_config_hash(self, config: TestConfiguration) -> str:
        """Calculate hash of configuration for tracking"""
        config_str = f"{config.workflow_name}_{config.dify_config.api_key[:8]}_{len(config.static_test_cases)}"
        return hashlib.md5(config_str.encode()).hexdigest()[:8]
