"""
Report generation for test results
"""

from typing import Dict, List, Any
from datetime import datetime
import json
from ..interfaces.result_models import TestSuiteResult, EvaluationResult


class ReportGenerator:
    """Generate comprehensive reports for test results"""
    
    @staticmethod
    def generate_console_report(suite_result: TestSuiteResult, statistics: Dict[str, Any] = None) -> str:
        """Generate a detailed console report"""
        report = []
        
        # Header
        report.append("\n" + "="*80)
        report.append(f"🧪 JUDGE FRAMEWORK TEST REPORT")
        report.append(f"Test Type: {suite_result.test_type.upper()}")
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("="*80)
        
        # Summary
        report.append("\n📊 EXECUTION SUMMARY")
        report.append(f"   Total Tests: {suite_result.total_tests}")
        report.append(f"   ✅ Successful: {suite_result.successful_tests}")
        report.append(f"   ❌ Failed: {suite_result.failed_tests}")
        report.append(f"   📈 Success Rate: {suite_result.success_rate:.1f}%")
        
        # Score Analysis
        if suite_result.average_scores:
            report.append("\n📈 SCORE ANALYSIS")
            for metric, score in suite_result.average_scores.items():
                status = "🟢" if score >= 90 else "🟡" if score >= 75 else "🔴"
                report.append(f"   {status} {metric}: {score:.1f}")
        
        # Detailed Statistics (if provided)
        if statistics:
            report.append("\n📋 DETAILED STATISTICS")
            
            # Score statistics
            if "score_statistics" in statistics:
                report.append("   Score Distributions:")
                for metric, stats in statistics["score_statistics"].items():
                    report.append(f"     • {metric}:")
                    report.append(f"       - Mean: {stats['mean']:.1f}")
                    report.append(f"       - Range: {stats['min']:.1f} - {stats['max']:.1f}")
                    report.append(f"       - Pass Rate (75+): {stats['pass_rate']:.1f}%")
            
            # Error analysis
            if "error_analysis" in statistics and statistics["error_analysis"]:
                report.append("   Error Categories:")
                for category, count in statistics["error_analysis"].items():
                    report.append(f"     • {category}: {count}")
        
        # Individual Results Summary
        report.append("\n📝 INDIVIDUAL TEST RESULTS")
        for i, result in enumerate(suite_result.individual_results[:10], 1):  # Show first 10
            status = "✅" if result.success else "❌"
            report.append(f"   {i:2d}. {status} {result.test_identifier}")
            
            # Show key scores
            if result.scores:
                score_summary = ", ".join([f"{k}: {v:.0f}" for k, v in list(result.scores.items())[:3]])
                report.append(f"       Scores: {score_summary}")
            
            if result.error_message:
                report.append(f"       Error: {result.error_message}")
        
        if len(suite_result.individual_results) > 10:
            report.append(f"   ... and {len(suite_result.individual_results) - 10} more tests")
        
        # Footer
        report.append("\n" + "="*80)
        report.append("🏁 END OF REPORT")
        report.append("="*80)
        
        return "\n".join(report)
    
    @staticmethod
    def generate_json_report(suite_result: TestSuiteResult, statistics: Dict[str, Any] = None) -> str:
        """Generate a JSON report for programmatic consumption"""
        report_data = {
            "metadata": {
                "test_type": suite_result.test_type,
                "generated_at": datetime.now().isoformat(),
                "configuration_hash": suite_result.configuration_hash
            },
            "summary": {
                "total_tests": suite_result.total_tests,
                "successful_tests": suite_result.successful_tests,
                "failed_tests": suite_result.failed_tests,
                "success_rate": suite_result.success_rate
            },
            "scores": {
                "average_scores": suite_result.average_scores,
                "score_distributions": suite_result.score_distributions
            },
            "error_analysis": {
                "error_summary": suite_result.error_summary,
                "common_errors": suite_result.common_errors
            },
            "execution": {
                "start_time": suite_result.start_time,
                "end_time": suite_result.end_time
            },
            "individual_results": [
                {
                    "test_identifier": result.test_identifier,
                    "success": result.success,
                    "scores": result.scores,
                    "error_categories": result.error_categories,
                    "error_message": result.error_message,
                    "timestamp": result.timestamp
                }
                for result in suite_result.individual_results
            ]
        }
        
        if statistics:
            report_data["statistics"] = statistics
        
        return json.dumps(report_data, indent=2)
    
    @staticmethod
    def generate_csv_report(suite_result: TestSuiteResult) -> str:
        """Generate a CSV report for data analysis"""
        import csv
        import io
        
        output = io.StringIO()
        
        # Get all possible metrics
        all_metrics = set()
        for result in suite_result.individual_results:
            all_metrics.update(result.scores.keys())
        
        # Write header
        header = ["test_identifier", "success", "timestamp"]
        header.extend(sorted(all_metrics))
        header.extend(["error_categories", "error_message"])
        
        writer = csv.writer(output)
        writer.writerow(header)
        
        # Write rows
        for result in suite_result.individual_results:
            row = [
                result.test_identifier,
                result.success,
                result.timestamp
            ]
            
            # Add scores
            for metric in sorted(all_metrics):
                row.append(result.scores.get(metric, ""))
            
            # Add error info
            row.append(";".join(result.error_categories))
            row.append(result.error_message or "")
            
            writer.writerow(row)
        
        return output.getvalue()
    
    @staticmethod
    def generate_comparison_report(suite_results: List[TestSuiteResult], 
                                 comparison_stats: Dict[str, Any] = None) -> str:
        """Generate a comparison report for multiple test suites"""
        report = []
        
        # Header
        report.append("\n" + "="*80)
        report.append(f"🔄 TEST SUITE COMPARISON REPORT")
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("="*80)
        
        # Summary table
        report.append("\n📊 SUITE COMPARISON SUMMARY")
        report.append(f"{'Suite Type':<20} {'Total':<8} {'✅ Success':<10} {'❌ Failed':<8} {'📈 Rate':<8}")
        report.append("-" * 60)
        
        for suite in suite_results:
            report.append(f"{suite.test_type:<20} {suite.total_tests:<8} "
                         f"{suite.successful_tests:<10} {suite.failed_tests:<8} "
                         f"{suite.success_rate:<8.1f}%")
        
        # Metric comparison
        if comparison_stats and "metric_comparison" in comparison_stats:
            report.append("\n📈 METRIC COMPARISON")
            for metric, data in comparison_stats["metric_comparison"].items():
                report.append(f"\n{metric}:")
                report.append(f"   Best: {data['best_performance']:.1f}")
                report.append(f"   Worst: {data['worst_performance']:.1f}")
                report.append(f"   Average: {data['average_performance']:.1f}")
                report.append("   By Suite:")
                for suite_type, value in data['values'].items():
                    report.append(f"     • {suite_type}: {value:.1f}")
        
        # Footer
        report.append("\n" + "="*80)
        report.append("🏁 END OF COMPARISON REPORT")
        report.append("="*80)
        
        return "\n".join(report)
    
    @staticmethod
    def save_report_to_file(report_content: str, filename: str):
        """Save report content to file"""
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(report_content)
        print(f"📄 Report saved to: {filename}")
