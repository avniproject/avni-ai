"""AI Reviewer module for analyzing conversations between tester and assistant."""

import json
import openai
from typing import Dict, List, Any


class AIReviewer:
    """AI that reviews conversations between tester and assistant"""

    def __init__(self):
        self.review_prompt = """
You are an expert AI reviewer analyzing conversations between an AI Tester and the Avni AI Assistant. Your role is to evaluate the quality, correctness, and consistency of the AI Assistant's configuration recommendations.

Evaluate the conversation on these dimensions:

1. CONFIGURATION CORRECTNESS (0-100):
   - Are the suggested Subject Types appropriate for the program?
   - Are Programs, Program Encounters, and General Encounters correctly identified?
   - Does the configuration match the program requirements?

2. CONSISTENCY (0-100):
   - Are recommendations logically consistent throughout the conversation?
   - Are there any contradictions in the assistant's responses?

3. COMMUNICATION QUALITY (0-100):
   - Did the assistant use appropriate non-technical language during discussion?
   - Were questions clear and easy to understand?
   - Was the final configuration summary proper with Avni terminology?

CRITICAL: Mark overall_success as FALSE if ANY of these conditions are met:
- configuration_correctness score is below 75
- consistency score is below 75  
- communication_quality score is below 75
- No final configuration was provided
- Major configuration errors (wrong subject types, programs, encounters)
- Assistant completely misunderstood the program requirements
- Communication breakdown preventing proper evaluation

Mark overall_success as TRUE only if ALL core scores are 75+ AND a proper configuration was delivered.

Provide your analysis in this JSON format:
{
    "scores": {
        "configuration_correctness": <0-100>,
        "consistency": <0-100>,
        "communication_quality": <0-100>
    },
    "overall_success": <true/false>,
    "configuration_elements": {
        "subject_types": ["list of identified subject types"],
        "programs": ["list of identified programs"],
        "program_encounters": ["list of program encounters"],
        "general_encounters": ["list of general encounters"],
        "location_hierarchy": "description of location structure"
    },
    "error_categories": ["list of error types found"],
    "key_strengths": ["list of strengths"],
    "areas_for_improvement": ["list of improvements needed"],
    "edge_cases_handled": <true/false>,
    "technical_terminology_usage": "appropriate/inappropriate/mixed",
    "final_config_provided": <true/false>
}

Conversation to analyze:
"""

    def analyze_conversation(
        self, conversation: List[Dict[str, str]], scenario: str
    ) -> Dict[str, Any]:
        """Analyze a conversation between tester and assistant"""
        try:
            # Format conversation for analysis
            conversation_text = f"Scenario: {scenario}\n\n"
            for i, msg in enumerate(conversation):
                role = "Tester" if msg["role"] == "user" else "AI Assistant"
                conversation_text += f"{role}: {msg['content']}\n\n"

            full_prompt = self.review_prompt + conversation_text

            response = openai.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "system", "content": full_prompt}],
                temperature=0.1,
                max_tokens=1500,
            )

            analysis = json.loads(response.choices[0].message.content.strip())
            return analysis

        except Exception as e:
            print(f"Error in AI reviewer analysis: {e}")
            return {
                "scores": {
                    "configuration_correctness": 0,
                    "consistency": 0,
                    "communication_quality": 0,
                },
                "overall_success": False,
                "error_categories": ["analysis_error"],
                "error_message": str(e),
            }
