"""AI Reviewer module for analyzing conversations between tester and assistant."""

import json
import openai
from typing import Dict, List, Any


class AIReviewer:
    """AI that reviews conversations between tester and assistant"""

    def __init__(self):
        from prompts import AI_REVIEWER_PROMPT

        self.review_prompt = AI_REVIEWER_PROMPT

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
