"""Analytics and reporting for the testing system."""

import datetime
from collections import defaultdict
from typing import List
from .models import ConversationResult, TestStatistics


class StatisticsCalculator:
    """Calculate comprehensive statistics from test results"""

    @staticmethod
    def calculate_statistics(results: List[ConversationResult]) -> TestStatistics:
        """Calculate comprehensive statistics from all results"""
        if not results:
            return TestStatistics(0, [], {}, {}, {})

        # Group results by scenario
        by_scenario = defaultdict(list)
        for result in results:
            by_scenario[result.scenario].append(result)

        # Calculate accuracy by scenario
        accuracy_by_scenario = {}
        consistency_scores = {}
        success_rates = {}

        for scenario, scenario_results in by_scenario.items():
            scores = []
            successes = []

            for result in scenario_results:
                analysis = result.reviewer_analysis
                if "scores" in analysis:
                    # Calculate overall score
                    overall_score = sum(analysis["scores"].values()) / len(
                        analysis["scores"]
                    )
                    scores.append(overall_score)
                    successes.append(analysis.get("overall_success", False))

            if scores:
                accuracy_by_scenario[scenario] = sum(scores) / len(scores)
                consistency_scores[scenario] = scores
                success_rates[scenario] = sum(successes) / len(successes) * 100

        # Count error categories
        error_categories = defaultdict(int)
        for result in results:
            analysis = result.reviewer_analysis
            if "error_categories" in analysis:
                for error in analysis["error_categories"]:
                    error_categories[error] += 1

        return TestStatistics(
            total_cycles=max(r.cycle for r in results) if results else 0,
            scenarios_tested=list(accuracy_by_scenario.keys()),
            accuracy_by_scenario=accuracy_by_scenario,
            consistency_scores=consistency_scores,
            error_categories=dict(error_categories),
        )


class ReportGenerator:
    """Generate comprehensive test reports"""

    @staticmethod
    def generate_report(
        statistics: TestStatistics, results: List[ConversationResult]
    ) -> str:
        """Generate a comprehensive test report"""
        report = []

        report.append("AVNI AI ASSISTANT - TEST REPORT")
        report.append(
            f"Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )
        report.append(f"Total Cycles: {statistics.total_cycles}")
        report.append(f"Scenarios Tested: {len(statistics.scenarios_tested)}")
        report.append(f"Total Conversations: {len(results)}")
        report.append("")

        # Accuracy Summary
        report.append("ACCURACY SUMMARY")

        for scenario, accuracy in statistics.accuracy_by_scenario.items():
            report.append(f"  {scenario:<35} {accuracy:6.1f}%")

        overall_avg = sum(statistics.accuracy_by_scenario.values()) / len(
            statistics.accuracy_by_scenario
        )
        report.append(f"  {'OVERALL AVERAGE':<35} {overall_avg:6.1f}%")
        report.append("")

        # Error Categories
        if statistics.error_categories:
            report.append("ERROR CATEGORIES")
            for error, count in sorted(
                statistics.error_categories.items(), key=lambda x: x[1], reverse=True
            ):
                report.append(f"  {error:<30} {count:4d} occurrences")
            report.append("")

        report.append(
            f"{'Cycle':<6} {'Scenario':<35} {'Config':<8} {'Consist':<8} {'Comm Qual':<10} {'Success':<8}"
        )

        for result in results:
            analysis = result.reviewer_analysis
            if "scores" in analysis:
                scores = analysis["scores"]
                report.append(
                    f"{result.cycle:<6} {result.scenario[:34]:<35} "
                    f"{scores.get('configuration_correctness', 0):<8.0f} "
                    f"{scores.get('consistency', 0):<8.0f} "
                    f"{scores.get('communication_quality', 0):<10.0f} "
                    f"{'Success' if analysis.get('overall_success', False) else 'Failure':<8}"
                )

        report.append("")

        if overall_avg < 70:
            report.append(
                "CRITICAL: Overall accuracy below 70%. Major improvements needed."
            )
        elif overall_avg < 85:
            report.append(
                "WARNING: Overall accuracy below 85%. Improvements recommended."
            )
        else:
            report.append("GOOD: Overall accuracy above 85%.")

        return "\n".join(report)
