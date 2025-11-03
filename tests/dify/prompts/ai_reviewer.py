"""AI Reviewer module for analyzing conversations between tester and assistant."""

import json
import openai
from typing import Dict, List, Any
from .prompts import AI_REVIEWER_PROMPT


class AIReviewer:
    """AI that reviews conversations between tester and assistant"""

    def __init__(self):
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

    @staticmethod
    def validate_created_configuration(
        actual_config: Dict[str, Any],
        program_requirements: str,
        scenario_name: str,
    ) -> Dict[str, Any]:
        """
        Validate if the actual created Avni configuration meets the program requirements.
        """
        try:
            validation_prompt = f"""
You are an expert Avni configuration reviewer. Evaluate whether this ACTUAL CREATED configuration can support the program requirements.

PROGRAM: {scenario_name}
REQUIREMENTS: {program_requirements}

ACTUAL CREATED CONFIGURATION:
{json.dumps(actual_config, indent=2)}

Evaluate:
1. FUNCTIONAL_ADEQUACY (0-100): Can this config support the program activities?
2. STRUCTURAL_CORRECTNESS (0-100): Are relationships properly set up?
3. COMPLETENESS (0-100): Are all essential components present?

Mark overall_success as TRUE only if ALL scores are 75+.

First provide the JSON response, then add detailed analysis explaining your scores:

{{
    "scores": {{
        "functional_adequacy": <0-100>,
        "structural_correctness": <0-100>,
        "completeness": <0-100>
    }},
    "overall_success": <true/false>,
    "configuration_assessment": {{
        "subject_types_created": ["list of subject types found"],
        "programs_created": ["list of programs found"],
        "encounters_created": ["list of encounter types found"],
        "location_hierarchy": "description of location structure",
        "catchments_created": ["list of catchments found"]
    }}
}}

DETAILED ANALYSIS:
Explain each score in detail:
1. Functional Adequacy (score): Why this score? What's missing or working well?
2. Structural Correctness (score): Are relationships correct? Any hierarchy issues?
3. Completeness (score): What components are missing? What's present?
"""

            response = openai.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "system", "content": validation_prompt}],
                temperature=0.1,
                max_tokens=1500,
            )

            response_content = response.choices[0].message.content.strip()
            print(f"Raw OpenAI response: {response_content[:200]}...")

            if not response_content:
                raise ValueError("Empty response from OpenAI")

            # Handle markdown code blocks
            if response_content.startswith("```json"):
                # Remove the opening ```json and closing ```
                lines = response_content.split("\n")
                # Find the start (skip ```json line)
                start_idx = 1
                # Find the end (stop at closing ```)
                end_idx = len(lines)
                for i in range(1, len(lines)):
                    if lines[i].strip() == "```":
                        end_idx = i
                        break

                # Extract JSON content and any text after
                json_lines = lines[start_idx:end_idx]
                remaining_lines = lines[end_idx + 1 :] if end_idx < len(lines) else []

                json_content = "\n".join(json_lines)
                remaining_text = "\n".join(remaining_lines).strip()

                result = json.loads(json_content)

                if remaining_text:
                    print("📝 Additional analysis found:")
                    print(remaining_text)
                    result["detailed_analysis"] = remaining_text

                return result

            # Extract JSON part if there's additional text after it
            elif response_content.startswith("{"):
                # Find the end of the JSON object by counting braces
                brace_count = 0
                json_end = 0
                for i, char in enumerate(response_content):
                    if char == "{":
                        brace_count += 1
                    elif char == "}":
                        brace_count -= 1
                        if brace_count == 0:
                            json_end = i + 1
                            break

                if json_end > 0:
                    json_part = response_content[:json_end]
                    remaining_text = response_content[json_end:].strip()

                    # Parse the JSON and add the analysis if present
                    result = json.loads(json_part)

                    if remaining_text:
                        print("📝 Additional analysis found:")
                        print(remaining_text)
                        # Add the analysis to the result
                        result["detailed_analysis"] = remaining_text

                    return result

            return json.loads(response_content)

        except json.JSONDecodeError as e:
            print(f"JSON parsing error in configuration validation: {e}")
            print(
                f"Response that failed to parse: {response_content if 'response_content' in locals() else 'No response content'}"
            )
            return {
                "scores": {
                    "functional_adequacy": 0,
                    "structural_correctness": 0,
                    "completeness": 0,
                },
                "configuration_assessment": {},
                "overall_success": False,
                "error_message": f"JSON parsing error: {str(e)}",
            }
        except Exception as e:
            print(f"Error in configuration validation: {e}")
            return {
                "scores": {
                    "functional_adequacy": 0,
                    "structural_correctness": 0,
                    "completeness": 0,
                },
                "configuration_assessment": {},
                "overall_success": False,
                "error_message": str(e),
            }
