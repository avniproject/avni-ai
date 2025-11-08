"""
DSPy modules for Avni Smart Form Builder.

This package contains simplified, trainable AI components for:
- Issue identification in forms
- Improvement suggestions generation
- Form improvement coordination
"""

from .issue_identifier import IssueIdentifier
from .suggestion_generator import SuggestionGenerator
from .form_improvement_program import FormImprovementProgram

__all__ = [
    "IssueIdentifier",
    "SuggestionGenerator",
    "FormImprovementProgram"
]