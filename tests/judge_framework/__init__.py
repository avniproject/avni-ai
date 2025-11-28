"""
Reusable LLM-as-Judge Framework for Avni Testing

This framework provides a pluggable architecture for testing different types of AI interactions:
1. LLM Chat conversations (existing Dify workflow testing)
2. Avni Form Element validations
3. Avni Visit Scheduling Rules Validation
"""

from .interfaces.test_subject import TestSubject
from .interfaces.test_executor import TestExecutor
from .interfaces.judge_strategy import JudgeStrategy
from .interfaces.result_models import EvaluationResult, TestConfiguration
from .orchestrator import JudgeOrchestrator
from .analytics.statistics import StatisticsCalculator
from .analytics.reporting import ReportGenerator

__all__ = [
    'TestSubject',
    'TestExecutor', 
    'JudgeStrategy',
    'EvaluationResult',
    'TestConfiguration',
    'JudgeOrchestrator',
    'StatisticsCalculator',
    'ReportGenerator'
]
