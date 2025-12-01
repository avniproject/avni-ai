#!/usr/bin/env python3
"""
Debug script to check actual Dify Form Assistant API responses
"""

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from dotenv import load_dotenv

load_dotenv()


def test_dify_form_assistant():
    """Test the Dify Form Assistant workflow directly"""
    print("🔍 Debugging Dify Form Assistant API")
    print("=" * 50)

    # Initialize Dify client
    try:
        from tests.dify.common.dify_client import DifyClient

        api_key = os.getenv(
            "DIFY_FORM_VALIDATION_API_KEY", os.getenv("DIFY_API_KEY", "")
        )
        if not api_key:
            print("❌ No DIFY_FORM_VALIDATION_API_KEY found")
            return False

        client = DifyClient(api_key)
        print(f"✅ DifyClient initialized with API key: {api_key[:10]}...")

    except Exception as e:
        print(f"❌ Failed to initialize DifyClient: {e}")
        return False

    # Test different query formats
    test_queries = [
        {
            "name": "Current format (from executor)",
            "query": """Question Text: Age of patient
Options: None
Context: Current dataType: Text | Current type: SingleSelect | Form type: IndividualProfile | Domain: health

Please validate this form element according to Avni rules and provide recommendations.""",
        },
        {
            "name": "Simple format",
            "query": "Age field using Text dataType instead of Numeric - please validate",
        },
        {
            "name": "JSON format",
            "query": """{"question_text": "Age of patient", "current_dataType": "Text", "current_type": "SingleSelect"}""",
        },
    ]

    for i, test_case in enumerate(test_queries, 1):
        print(f"\n📋 Test {i}: {test_case['name']}")
        print("-" * 40)

        try:
            response = client.send_message(
                query=test_case["query"],
                user="debug_tester",
                inputs={
                    "auth_token": os.getenv("AVNI_AUTH_TOKEN", ""),
                    "org_name": "Social Welfare Foundation Trust",
                    "org_type": "trial",
                    "user_name": "Arjun",
                    "avni_mcp_server_url": os.getenv("AVNI_MCP_SERVER_URL", ""),
                },
                timeout=30,
            )

            print(f"✅ Response received")
            print(f"   Success: {response.get('success', False)}")
            print(f"   Conversation ID: {response.get('conversation_id', 'N/A')}")
            print(f"   Message ID: {response.get('message_id', 'N/A')}")
            print(f"   Answer length: {len(response.get('answer', ''))}")

            answer = response.get("answer", "")
            if answer:
                print(f"   Answer preview: {answer[:200]}...")

                # Check for expected validation keywords
                validation_keywords = [
                    "critical",
                    "high",
                    "medium",
                    "issue",
                    "recommend",
                    "dataType",
                    "Numeric",
                ]
                found_keywords = [
                    kw for kw in validation_keywords if kw.lower() in answer.lower()
                ]
                print(f"   Found validation keywords: {found_keywords}")
            else:
                print("   ❌ Empty answer!")

        except Exception as e:
            print(f"   ❌ Error: {e}")

    return True


if __name__ == "__main__":
    test_dify_form_assistant()
