"""
Test Executor interface for the Judge Framework
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from .result_models import TestConfiguration
from .conversation_strategy import ConversationGenerationStrategy, EndConversationStrategy


class TestExecutor(ABC):
    """
    Abstract interface for test executors - how we run the tests.
    Each implementation knows how to execute a specific type of test.
    """
    
    def __init__(self, config: TestConfiguration):
        self.config = config
    
    @abstractmethod
    def execute(self, test_input: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a test with the given input and return the raw output
        
        Args:
            test_input: Input data from TestSubject.get_test_input()
            
        Returns:
            Raw output from the test execution (to be passed to JudgeStrategy)
        """
        pass
    
    @abstractmethod
    def get_executor_metadata(self) -> Dict[str, Any]:
        """Get metadata about this executor"""
        pass
    
    def validate_execution_requirements(self, test_input: Dict[str, Any]) -> bool:
        """
        Validate that all requirements for execution are met
        Override in subclasses for specific validation logic
        """
        return True
    
    def cleanup(self):
        """
        Cleanup resources after execution
        Override in subclasses if needed
        """
        pass


class DifyWorkflowExecutor(TestExecutor):
    """
    Base executor for Dify workflow interactions
    Reuses the existing DifyClient with configurable API keys
    """
    
    def __init__(self, config: TestConfiguration):
        super().__init__(config)
        self.dify_client = None
        self._initialize_dify_client()
    
    def _initialize_dify_client(self):
        """Initialize Dify client with configuration"""
        # Import here to avoid circular imports
        import sys
        from pathlib import Path
        sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))
        
        from tests.dify.common.dify_client import DifyClient
        
        self.dify_client = DifyClient(self.config.dify_api_key)
        # Override base URL if configured
        if hasattr(self.config, 'dify_base_url') and self.config.dify_base_url:
            self.dify_client.base_url = self.config.dify_base_url
    
    def execute(self, test_input: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute test via Dify workflow
        """
        if not self.dify_client:
            raise RuntimeError("Dify client not initialized")
        
        # Extract query and inputs from test_input
        query = test_input.get("query", "")
        inputs = test_input.get("inputs", {})
        conversation_id = test_input.get("conversation_id", "")
        
        # Add default inputs if not provided
        if not inputs:
            inputs = self._get_default_inputs()
        
        # Send message to Dify
        response = self.dify_client.send_message(
            query=query,
            conversation_id=conversation_id,
            user=self.config.test_user,
            inputs=inputs,
            timeout=self.config.timeout_seconds
        )
        
        return {
            "success": response.get("success", False),
            "answer": response.get("answer", ""),
            "conversation_id": response.get("conversation_id", ""),
            "message_id": response.get("message_id", ""),
            "error": response.get("error"),
            "raw_response": response
        }
    
    def _get_default_inputs(self) -> Dict[str, Any]:
        """Get default inputs for Dify workflow"""
        import os
        return {
            "auth_token": os.getenv("AVNI_AUTH_TOKEN"),
            "org_name": "Social Welfare Foundation Trust",
            "org_type": "trial", 
            "user_name": "Arjun",
            "avni_mcp_server_url": os.getenv("AVNI_MCP_SERVER_URL"),
        }
    
    def get_executor_metadata(self) -> Dict[str, Any]:
        return {
            "executor_type": "DifyWorkflowExecutor",
            "workflow_name": self.config.workflow_name,
            "max_iterations": self.config.max_iterations,
            "timeout": self.config.timeout_seconds
        }


class ConversationExecutor(DifyWorkflowExecutor):
    """
    Specialized executor for chat conversation testing
    Handles multi-turn conversations with pluggable message generation
    """
    
    def __init__(self, config: TestConfiguration, conversation_strategy: Optional[ConversationGenerationStrategy] = None):
        super().__init__(config)
        self.conversation_strategy = conversation_strategy or EndConversationStrategy()
    
    def execute(self, test_input: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a multi-turn conversation test
        """
        initial_query = test_input.get("query", "")
        scenario = test_input.get("scenario", "")
        scenario_index = test_input.get("scenario_index", 0)
        max_iterations = test_input.get("max_iterations", self.config.max_iterations)
        
        conversation_history = []
        conversation_id = ""
        
        # Context for conversation strategy
        context = {
            "scenario": scenario,
            "scenario_index": scenario_index,
            "max_iterations": max_iterations
        }
        
        for iteration in range(max_iterations):
            # Get current message to send
            if iteration == 0:
                current_query = initial_query
            else:
                if not self.conversation_strategy.should_continue_conversation(conversation_history, context):
                    break
                
                current_query = self.conversation_strategy.generate_next_message(conversation_history, context)
                if not current_query:
                    break  # Conversation ended
            
            # Execute via Dify
            response = super().execute({
                "query": current_query,
                "inputs": test_input.get("inputs", {}),
                "conversation_id": conversation_id
            })
            
            # Record exchange
            turn_data = {
                "iteration": iteration + 1,
                "user_message": current_query,
                "assistant_response": response.get("answer", ""),
                "success": response.get("success", False),
                "error": response.get("error")
            }
            conversation_history.append(turn_data)
            
            # Update conversation ID for next turn
            if response.get("success"):
                conversation_id = response.get("conversation_id", "")
            
            # Break if there was an error
            if not response.get("success"):
                break
        
        return {
            "success": True,  # Overall execution succeeded even if some turns failed
            "conversation_history": conversation_history,
            "total_iterations": len(conversation_history),
            "final_conversation_id": conversation_id
        }
    
    def get_executor_metadata(self) -> Dict[str, Any]:
        metadata = super().get_executor_metadata()
        metadata.update({
            "executor_type": "ConversationExecutor",
            "conversation_strategy": self.conversation_strategy.__class__.__name__
        })
        return metadata
