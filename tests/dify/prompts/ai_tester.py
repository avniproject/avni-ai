"""
AI agents for the testing system - tester and Dify assistant.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

import openai
from typing import Dict, List


class AITester:
    """AI that acts as a program manager testing the Avni assistant"""

    def __init__(self, prompts):
        self.prompts = prompts

    def generate_message(self, chat_history: List[Dict], scenario_index: int) -> str:
        try:
            messages = [
                {"role": "system", "content": self.prompts[scenario_index]}
            ] + chat_history

            response = openai.chat.completions.create(
                model="gpt-4o", messages=messages, temperature=0.5, max_tokens=500
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error in AI tester: {e}")
            return "Error: Could not generate message."
