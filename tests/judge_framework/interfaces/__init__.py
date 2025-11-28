"""Core interfaces for the Judge Framework"""

from .test_subject import TestSubject
from .test_executor import TestExecutor  
from .judge_strategy import JudgeStrategy
from .result_models import EvaluationResult, TestConfiguration

__all__ = [
    'TestSubject',
    'TestExecutor',
    'JudgeStrategy', 
    'EvaluationResult',
    'TestConfiguration'
]
