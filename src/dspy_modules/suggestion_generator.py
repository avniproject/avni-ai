"""
SuggestionGenerator module for generating improvement recommendations based on identified issues.

This DSPy module generates contextual suggestions for:
- Fixing identified issues
- Improving form structure
- Adding beneficial fields
- Implementation recommendations
"""

import dspy
from typing import Dict, List, Any, Optional
import json
import logging

logger = logging.getLogger(__name__)


class SuggestionGenerator(dspy.Module):
    """
    Generates improvement suggestions based on identified form issues.
    
    Takes identified issues and generates actionable recommendations
    for fixing problems and improving the form.
    """
    
    def __init__(self):
        super().__init__()
        self.suggester = dspy.ChainOfThought(AvniSuggestionSignature)
    
    def forward(self, form_json: Dict[str, Any], issues: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate suggestions based on identified issues.
        
        Args:
            form_json: Complete form configuration
            issues: List of identified issues with severity and details
            
        Returns:
            Structured suggestions with priorities and implementation details
        """
        form_str = json.dumps(form_json, indent=2)
        issues_str = json.dumps(issues, indent=2)
        
        try:
            result = self.suggester(
                form_structure=form_str,
                identified_issues=issues_str
            )
            
            # Parse JSON outputs if they're strings
            try:
                suggestions = json.loads(result.suggestions) if isinstance(result.suggestions, str) else result.suggestions
            except json.JSONDecodeError:
                suggestions = result.suggestions
            
            return {
                "suggestions": suggestions
            }
        except Exception as e:
            logger.error(f"Suggestion generation failed: {e}")
            return {
                "suggestions": []
            }


class AvniSuggestionSignature(dspy.Signature):
    """You are an expert Avni form improvement consultant specializing in generating actionable suggestions.
    
    Your task is to analyze identified form issues and generate practical, prioritized recommendations for improvement.
    
    Key Responsibilities:
    1. Generate specific suggestions to fix each identified issue
    2. Provide additional improvement recommendations beyond just fixing issues
    3. Suggest new fields that would benefit the form
    
    Suggestion Categories:
    - Issue Fixes: Direct solutions to identified problems
    - Field Improvements: Better dataTypes, validation, constraints
    - New Fields: Additional beneficial fields for the form
    - Structure Improvements: Better organization, grouping, flow
    - Validation Enhancements: Add missing validations and constraints
    
    Output Format Requirements:
    - Suggestions: JSON array with type, title, description, priority, implementation details, affected elements
    
    Always provide specific implementation details and reference form element UUIDs when available."""
    
    form_structure = dspy.InputField(desc="Complete Avni form JSON with formElementGroups and field configurations")
    identified_issues = dspy.InputField(desc="JSON array of identified issues with severity, messages, and affected elements")
    
    suggestions = dspy.OutputField(desc="JSON array of suggestions: [{\"type\": \"Issue Fix\", \"title\": \"Fix Age dataType\", \"description\": \"Change Age field from Text to Numeric\", \"priority\": \"High\", \"formElementUuid\": \"uuid-123\", \"implementation\": {\"dataType\": \"Numeric\", \"lowAbsolute\": 0, \"highAbsolute\": 120}, \"rationale\": \"Age should be numeric for proper validation\"}]")