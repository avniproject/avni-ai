"""
Form Validation Executor interface for the Judge Framework
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from .result_models import TestConfiguration


class FormValidationExecutor(ABC):
    """
    Abstract interface for form validation executors.
    Validates form elements against Avni rules and best practices.
    """
    
    def __init__(self, config: TestConfiguration):
        self.config = config
    
    @abstractmethod
    def execute(self, test_input: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute form validation test
        
        Args:
            test_input: Dictionary containing form element data to validate
                - form_element: Form element definition with name, dataType, type, etc.
                - form_context: Overall form structure and domain context
                - validation_rules: Specific rules to check against
        
        Returns:
            Dictionary containing validation results
                - success: Whether validation completed successfully
                - validation_feedback: AI-generated validation feedback
                - issues_found: List of identified issues
                - recommendations: List of improvement suggestions
                - executive_summary: Overall assessment and scores
        """
        pass
    
    @abstractmethod
    def get_executor_metadata(self) -> Dict[str, Any]:
        """Get metadata about this executor"""
        pass


class DifyFormValidationExecutor(FormValidationExecutor):
    """
    Form validation executor that uses Dify workflow for validation
    """
    
    def __init__(self, config: TestConfiguration):
        super().__init__(config)
        self.dify_client = None
        self._initialize_dify_client()
    
    def _initialize_dify_client(self):
        """Initialize Dify client for form validation workflow"""
        try:
            from tests.dify.common.dify_client import DifyClient
            self.dify_client = DifyClient(
                api_key=self.config.dify_config.api_key
            )
        except ImportError:
            raise ImportError("DifyClient not available. Please ensure tests.dify.common.dify_client is accessible.")
    
    def execute(self, test_input: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute form validation using Dify workflow
        """
        if not self.dify_client:
            return {
                "success": False,
                "error": "Dify client not initialized",
                "validation_feedback": None
            }
        
        try:
            # Prepare form validation input for Dify
            form_element = test_input.get("form_element", {})
            form_context = test_input.get("form_context", {})
            
            # Format input according to Dify workflow expectations
            query_text = self._format_form_validation_query(form_element, form_context)
            
            # Execute via Dify
            response = self.dify_client.send_message(
                query=query_text,
                inputs={
                    "auth_token": test_input.get("auth_token"),
                    "org_name": test_input.get("org_name", "Social Welfare Foundation Trust"),
                    "org_type": test_input.get("org_type", "trial"),
                    "user_name": test_input.get("user_name", "Arjun"),
                    "avni_mcp_server_url": test_input.get("avni_mcp_server_url")
                }
            )
            
            # Parse validation response
            validation_feedback = response.get("answer", "")
            
            return {
                "success": True,
                "validation_feedback": validation_feedback,
                "response_metadata": {
                    "conversation_id": response.get("conversation_id", ""),
                    "message_id": response.get("message_id", "")
                }
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "validation_feedback": None
            }
    
    def _format_form_validation_query(self, form_element: Dict[str, Any], form_context: Dict[str, Any]) -> str:
        """Format form element data into query text for Dify workflow"""
        
        question_text = form_element.get("name", "Unnamed field")
        current_options = form_element.get("concept", {}).get("answers", [])
        context_info = self._build_context_string(form_element, form_context)
        
        query = f"""Question Text: {question_text}
Options: {', '.join(map(str, current_options)) if current_options else 'None'}
Context: {context_info}

Please validate this form element according to Avni rules and provide recommendations."""
        
        return query
    
    def _build_context_string(self, form_element: Dict[str, Any], form_context: Dict[str, Any]) -> str:
        """Build context string for form validation"""
        context_parts = []
        
        # Add current field configuration
        if "concept" in form_element:
            concept = form_element["concept"]
            context_parts.append(f"Current dataType: {concept.get('dataType', 'Unknown')}")
            context_parts.append(f"Current type: {form_element.get('type', 'Unknown')}")
        
        # Add form context
        if "formType" in form_context:
            context_parts.append(f"Form type: {form_context['formType']}")
        
        if "domain" in form_context:
            context_parts.append(f"Domain: {form_context['domain']}")
        
        return " | ".join(context_parts) if context_parts else "No specific context provided"
    
    def get_executor_metadata(self) -> Dict[str, Any]:
        """Get metadata about this executor"""
        return {
            "executor_type": "DifyFormValidationExecutor",
            "workflow_name": self.config.dify_config.workflow_name,
            "api_base_url": self.config.dify_config.base_url,
            "timeout": self.config.dify_config.timeout_seconds
        }
