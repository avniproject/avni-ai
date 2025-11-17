"""
DSPy modules for Avni Smart Form Builder.

This package contains trainable AI components for:
- Issue identification in forms
- Improvement suggestions generation
- Training and optimization utilities
"""

from .issue_identifier import IssueIdentifier
from .suggestion_generator import SuggestionGenerator

__all__ = ["IssueIdentifier", "SuggestionGenerator"]
