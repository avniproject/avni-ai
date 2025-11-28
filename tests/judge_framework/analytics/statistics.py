"""
Statistics calculation for test results
"""

from typing import Dict, List, Any
import statistics
from ..interfaces.result_models import TestSuiteResult, EvaluationResult


class StatisticsCalculator:
    """Calculate comprehensive statistics for test results"""
    
    @staticmethod
    def calculate_suite_statistics(suite_result: TestSuiteResult) -> Dict[str, Any]:
        """
        Calculate detailed statistics for a test suite
        """
        if not suite_result.individual_results:
            return {}
        
        stats = {
            "basic_metrics": {
                "total_tests": suite_result.total_tests,
                "successful_tests": suite_result.successful_tests,
                "failed_tests": suite_result.failed_tests,
                "success_rate": suite_result.success_rate
            },
            "score_statistics": {},
            "error_analysis": suite_result.error_summary,
            "performance_metrics": {}
        }
        
        # Calculate score statistics
        score_data = StatisticsCalculator._calculate_score_statistics(suite_result.individual_results)
        stats["score_statistics"] = score_data
        
        # Calculate performance metrics
        performance_data = StatisticsCalculator._calculate_performance_metrics(suite_result.individual_results)
        stats["performance_metrics"] = performance_data
        
        return stats
    
    @staticmethod
    def _calculate_score_statistics(results: List[EvaluationResult]) -> Dict[str, Any]:
        """Calculate statistical measures for each scoring metric"""
        score_stats = {}
        
        # Collect scores by metric
        metric_scores = {}
        for result in results:
            for metric, score in result.scores.items():
                if metric not in metric_scores:
                    metric_scores[metric] = []
                metric_scores[metric].append(score)
        
        # Calculate statistics for each metric
        for metric, scores in metric_scores.items():
            if scores:
                score_stats[metric] = {
                    "mean": statistics.mean(scores),
                    "median": statistics.median(scores),
                    "min": min(scores),
                    "max": max(scores),
                    "std_dev": statistics.stdev(scores) if len(scores) > 1 else 0,
                    "count": len(scores),
                    "pass_rate": len([s for s in scores if s >= 75]) / len(scores) * 100
                }
        
        return score_stats
    
    @staticmethod
    def _calculate_performance_metrics(results: List[EvaluationResult]) -> Dict[str, Any]:
        """Calculate performance-related metrics"""
        metrics = {
            "error_frequency": {},
            "common_failure_patterns": [],
            "test_consistency": {}
        }
        
        # Error frequency analysis
        error_categories = {}
        for result in results:
            for category in result.error_categories:
                error_categories[category] = error_categories.get(category, 0) + 1
        
        metrics["error_frequency"] = error_categories
        
        # Common failure patterns (top errors)
        sorted_errors = sorted(error_categories.items(), key=lambda x: x[1], reverse=True)
        metrics["common_failure_patterns"] = [f"{category} ({count})" for category, count in sorted_errors[:5]]
        
        # Test consistency (score variance)
        metric_variances = {}
        for result in results:
            for metric, score in result.scores.items():
                if metric not in metric_variances:
                    metric_variances[metric] = []
                metric_variances[metric].append(score)
        
        for metric, scores in metric_variances.items():
            if len(scores) > 1:
                metrics["test_consistency"][metric] = {
                    "variance": statistics.variance(scores),
                    "coefficient_of_variation": statistics.stdev(scores) / statistics.mean(scores) if statistics.mean(scores) > 0 else 0
                }
        
        return metrics
    
    @staticmethod
    def compare_test_suites(suite_results: List[TestSuiteResult]) -> Dict[str, Any]:
        """Compare multiple test suites"""
        if not suite_results:
            return {}
        
        comparison = {
            "suite_summary": {},
            "metric_comparison": {},
            "trend_analysis": {}
        }
        
        # Basic summary
        total_tests = sum(suite.total_tests for suite in suite_results)
        total_successful = sum(suite.successful_tests for suite in suite_results)
        overall_success_rate = (total_successful / total_tests * 100) if total_tests > 0 else 0
        
        comparison["suite_summary"] = {
            "total_suites": len(suite_results),
            "total_tests": total_tests,
            "total_successful": total_successful,
            "overall_success_rate": overall_success_rate,
            "suite_types": list(set(suite.test_type for suite in suite_results))
        }
        
        # Metric comparison across suites
        all_metrics = set()
        for suite in suite_results:
            all_metrics.update(suite.average_scores.keys())
        
        for metric in all_metrics:
            metric_values = []
            suite_names = []
            for suite in suite_results:
                if metric in suite.average_scores:
                    metric_values.append(suite.average_scores[metric])
                    suite_names.append(suite.test_type)
            
            if metric_values:
                comparison["metric_comparison"][metric] = {
                    "values": dict(zip(suite_names, metric_values)),
                    "best_performance": max(metric_values),
                    "worst_performance": min(metric_values),
                    "average_performance": statistics.mean(metric_values)
                }
        
        return comparison
