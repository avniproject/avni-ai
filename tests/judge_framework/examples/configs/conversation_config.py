"""
Configuration for conversation testing using the Judge Framework
"""

import os
# Use absolute imports from project root
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent))

from tests.judge_framework.interfaces.result_models import (
    TestConfiguration, 
    DifyConfig, 
    EvaluationConfig, 
    TestGenerationConfig
)

# Load existing conversation prompts from the original testing system
def load_conversation_prompts():
    """Load conversation prompts from the existing testing system"""
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent))
    
    try:
        from tests.dify.prompts.prompts import SCENARIO_NAMES, TESTER_PROMPTS
        return SCENARIO_NAMES, TESTER_PROMPTS
    except ImportError:
        # Fallback prompts if import fails
        scenario_names = [
            "Maternal Health Program Setup",
            "Form Validation Configuration", 
            "Visit Scheduling Rules",
            "Location Hierarchy Setup"
        ]
        
        tester_prompts = [
            """You are a program manager setting up a maternal health program. 
            Configure the necessary Avni entities including subject types, programs, 
            and encounter types for antenatal care visits.""",
            
            """You are configuring form validation for patient registration.
            Set up appropriate validation rules, form elements, and ensure data integrity.""",
            
            """You are setting up visit scheduling rules for chronic disease management.
            Configure appropriate visit frequencies, reminder schedules, and follow-up rules.""",
            
            """You are establishing the location hierarchy for a new district.
            Set up states, districts, blocks, and villages with proper catchment areas."""
        ]
        
        return scenario_names, tester_prompts


def create_conversation_test_config() -> TestConfiguration:
    """Create configuration for conversation testing"""
    
    # Dify configuration
    dify_config = DifyConfig(
        api_key=os.getenv("DIFY_API_KEY", ""),
        base_url=os.getenv("DIFY_API_BASE_URL", "https://api.dify.ai/v1"),
        workflow_name="avni_assistant_conversation",
        test_user="conversation_tester",
        timeout_seconds=120
    )
    
    # Evaluation configuration
    evaluation_config = EvaluationConfig(
        evaluation_metrics=[
            "configuration_correctness",
            "consistency", 
            "communication_quality",
            "task_completion"
        ],
        success_thresholds={
            "configuration_correctness": 75.0,
            "consistency": 75.0,
            "communication_quality": 75.0,
            "task_completion": 75.0
        },
        openai_model="gpt-4o",
        openai_temperature=0.1,
        include_detailed_analysis=True
    )
    
    # Test generation configuration
    scenario_names, tester_prompts = load_conversation_prompts()
    
    # Create static test cases from existing prompts
    static_test_cases = []
    for i, (name, prompt) in enumerate(zip(scenario_names, tester_prompts)):
        static_test_cases.append({
            "scenario": name,
            "scenario_index": i,
            "initial_query": f"I need help setting up {name.lower()}. Can you guide me through the configuration?",
            "expected_behavior": f"AI assistant should correctly configure {name.lower()} and create necessary Avni entities"
        })
    
    generation_config = TestGenerationConfig(
        static_test_cases=static_test_cases,
        ai_generation_enabled=True,
        ai_generation_prompt="Generate additional realistic scenarios for Avni healthcare program configuration",
        num_ai_cases=2  # Generate 2 additional AI test cases
    )
    
    # Main configuration
    return TestConfiguration(
        dify_config=dify_config,
        evaluation_config=evaluation_config,
        generation_config=generation_config,
        max_iterations=8,
        custom_report_sections=["conversation_flow_analysis", "entity_configuration_summary"]
    )
