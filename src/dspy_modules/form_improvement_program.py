"""
FormImprovementProgram - Simplified coordinator for Avni's Smart Form Builder.

This program coordinates two specialized modules:
1. IssueIdentifier - identifies problems in forms
2. SuggestionGenerator - generates improvement recommendations
"""

import dspy
from typing import Dict, List, Any, Optional
import asyncio
import logging
from datetime import datetime
from .issue_identifier import IssueIdentifier
from .suggestion_generator import SuggestionGenerator


logger = logging.getLogger(__name__)


class FormImprovementProgram(dspy.Module):
    """
    Simplified coordinator that provides comprehensive form analysis using two specialized modules.

    Uses a two-step process:
    1. Identify issues in the form
    2. Generate suggestions based on identified issues
    """

    def __init__(self, enable_tracing: bool = True):
        super().__init__()

        # Two specialized modules instead of one unified module
        self.issue_identifier = IssueIdentifier()
        self.suggestion_generator = SuggestionGenerator()
        self.enable_tracing = enable_tracing

    def forward(
        self,
        form_json: Dict[str, Any],
        analysis_options: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Perform comprehensive form analysis using a two-step process.

        Args:
            form_json: Complete form configuration as dictionary
            analysis_options: Optional configuration for analysis behavior

        Returns:
            Comprehensive analysis report with issues and suggestions
        """
        logger.info("=== FormImprovementProgram.forward() Starting ===")

        analysis_start = datetime.now()
        options = analysis_options or {}

        try:
            logger.info("=== Step 1: Identifying Issues ===")

            # Step 1: Identify issues
            issue_results = self.issue_identifier.forward(form_json)
            issues = issue_results.get("issues", [])

            logger.info(f"Found {len(issues)} issues")

            logger.info("=== Step 2: Generating Suggestions ===")

            # Step 2: Generate suggestions based on identified issues
            suggestion_results = self.suggestion_generator.forward(form_json, issues)
            suggestions = suggestion_results.get("suggestions", [])

            logger.info(f"Generated {len(suggestions)} suggestions")

            # Calculate analysis duration
            analysis_duration = (datetime.now() - analysis_start).total_seconds()

            # Create executive summary
            total_issues = len(issues)
            critical_issues = len(
                [i for i in issues if i.get("severity") == "critical"]
            )
            high_issues = len([i for i in issues if i.get("severity") == "high"])

            if total_issues == 0:
                assessment = "excellent"
                top_priority = "No issues found - form follows best practices"
            elif critical_issues > 0:
                assessment = "needs_immediate_attention"
                top_priority = "Fix critical issues immediately"
            elif high_issues > 0:
                assessment = "needs_improvement"
                top_priority = "Address high priority issues"
            else:
                assessment = "minor_improvements_needed"
                top_priority = "Address medium/low priority issues"

            executive_summary = {
                "overview": f"Form analysis completed - {assessment}",
                "total_issues": total_issues,
                "critical_issues": critical_issues,
                "total_suggestions": len(suggestions),
                "top_priority": top_priority,
                "overall_score": max(
                    0,
                    100
                    - (critical_issues * 30)
                    - (high_issues * 15)
                    - (total_issues * 5),
                ),
            }

            # Combine results
            response = {
                "analysis_metadata": {
                    "timestamp": analysis_start.isoformat(),
                    "form_name": form_json.get("name", "Unknown"),
                    "analysis_options": options,
                    "duration_seconds": analysis_duration,
                    "approach": "two_step_analysis",
                },
                "issues": issues,
                "suggestions": suggestions,
                "executive_summary": executive_summary,
            }

            logger.info(
                f"=== FormImprovementProgram.forward() Completed in {analysis_duration:.2f}s ==="
            )
            logger.info(
                f"Final results: {total_issues} issues, {len(suggestions)} suggestions"
            )

            return response

        except Exception as e:
            logger.error(f"Form analysis error: {e}")
            import traceback

            logger.error(f"Form analysis traceback: {traceback.format_exc()}")
            return {
                "analysis_metadata": {
                    "timestamp": analysis_start.isoformat(),
                    "form_name": form_json.get("name", "Unknown"),
                    "error": str(e),
                },
                "issues": [],
                "suggestions": [],
                "executive_summary": {"message": "Analysis failed", "error": str(e)},
            }

    async def analyze_multiple_forms(
        self, forms: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Analyze multiple forms concurrently."""
        tasks = []
        for form in forms:
            task = asyncio.create_task(self._async_analyze_form(form))
            tasks.append(task)

        results = await asyncio.gather(*tasks, return_exceptions=True)

        return {
            "batch_analysis": {
                "total_forms": len(forms),
                "successful_analyses": len(
                    [r for r in results if not isinstance(r, Exception)]
                ),
                "failed_analyses": len(
                    [r for r in results if isinstance(r, Exception)]
                ),
            },
            "results": results,
        }

    async def _async_analyze_form(self, form_json: Dict[str, Any]) -> Dict[str, Any]:
        """Asynchronous form analysis wrapper."""
        return self.forward(form_json)

    def get_analysis_trace(self) -> Dict[str, Any]:
        """Get detailed trace of the last analysis (if tracing enabled)."""
        if not self.enable_tracing:
            return {"tracing_disabled": True}

        # DSPy 3.x handles tracing internally
        return {
            "trace_available": False,
            "note": "DSPy 3.x handles tracing internally - check DSPy logs for execution details",
        }
