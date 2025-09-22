"""
AI agents for the testing system - tester and Dify assistant.
"""

import openai
from typing import Dict, List
from prompts import TESTER_PROMPTS
from dify_client import DifyClient


class AITester:
    """AI that acts as a program manager testing the Avni assistant"""

    def __init__(self):
        self.prompts = TESTER_PROMPTS

    def generate_message(self, chat_history: List[Dict], scenario_index: int) -> str:
        """Generate tester message"""
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


class DifyAssistant:
    """Dify-powered AI assistant being tested"""

    def __init__(self, dify_api_key: str):
        self.dify_client = DifyClient(dify_api_key)
        self.conversation_id = ""

    def generate_response(self, message: str) -> str:
        """Generate assistant response using Dify API"""
        try:
            response = self.dify_client.send_message(message, self.conversation_id)

            if response["success"]:
                self.conversation_id = response["conversation_id"]
                return response["answer"]
            else:
                print(f"Dify API error: {response.get('error', 'Unknown error')}")
                return "Sorry, I encountered an error."

        except Exception as e:
            print(f"Error in Dify assistant: {e}")
            return "Sorry, I encountered an error."

    def reset_conversation(self):
        """Reset conversation state for new test"""
        self.conversation_id = ""
