#!/usr/bin/env python3
"""Test OpenAI tool calling with actual API calls to test location and program tools."""

import asyncio
import os
import logging

import pytest
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import our components
from src.openai_function_client import create_openai_function_client
from src.tools.location import register_location_tools_direct
from src.tools.program import register_program_tools_direct
from src.tool_registry import tool_registry

pytest.skip("Skipping all tests in this module", allow_module_level=True)
async def test_location_tools():
    """Test location-related tools via OpenAI function calling."""

    print("🧪 Testing Location Tools...")
    print("=" * 50)

    # Test message asking for location types
    messages = [
        {
            "role": "system",
            "content": "You are an AI assistant that helps with Avni platform operations. Use the available tools to help users."
        },
        {
            "role": "user",
            "content": "Can you get the list of location types available in the system?"
        }
    ]

    return await make_openai_call(messages, "Location Types")


async def test_program_tools():
    """Test program-related tools via OpenAI function calling."""

    print("🧪 Testing Program Tools...")
    print("=" * 50)

    # Test message asking to create a subject type
    messages = [
        {
            "role": "system",
            "content": "You are an AI assistant that helps with Avni platform operations. Use the available tools to help users."
        },
        {
            "role": "user",
            "content": "I want to create a new subject type called 'Patient' of type 'Person' for my health program."
        }
    ]

    return await make_openai_call(messages, "Create Subject Type")


async def test_catchments():
    """Test getting catchments via OpenAI function calling."""

    print("🧪 Testing Catchments...")
    print("=" * 50)

    messages = [
        {
            "role": "system",
            "content": "You are an AI assistant that helps with Avni platform operations. Use the available tools to help users."
        },
        {
            "role": "user",
            "content": "Show me all the catchments available in the system."
        }
    ]

    return await make_openai_call(messages, "Get Catchments")


async def make_openai_call(messages, test_name):
    """Make an OpenAI API call and process any function calls."""

    try:
        # Get API key
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            print("❌ OPENAI_API_KEY not found in environment variables")
            return False

        # Validate API key format
        if not api_key.startswith('sk-') or len(api_key) < 40:
            print(f"❌ Invalid OpenAI API key format. Key should start with 'sk-' and be longer than 40 characters.")
            print(f"   Current key: {api_key[:10]}... (length: {len(api_key)})")
            return False

        # Get auth token for Avni API
        auth_token = os.getenv("AVNI_API_TOKEN") or "test-token-123"

        # Get available tools
        available_tools = tool_registry.get_openai_tools()
        print(f"📋 Available tools: {len(available_tools)}")

        # Create OpenAI client
        async with create_openai_function_client(api_key) as client:
            print(f"🤖 Making OpenAI API call for: {test_name}")

            # First API call
            response = await client.create_chat_completion(
                messages=messages,
                tools=available_tools,
                model="gpt-4o-mini"  # Using mini for cost efficiency
            )

            # Check the response
            choice = response["choices"][0]
            assistant_message = choice["message"]

            print(f"💬 Assistant response: {assistant_message.get('content', 'No content')}")

            # Add assistant message to conversation
            messages.append(assistant_message)

            # Check if assistant wants to call functions
            if assistant_message.get("tool_calls"):
                print(f"🔧 Assistant wants to call {len(assistant_message['tool_calls'])} function(s)")

                # Process function calls
                function_results = await client.process_function_calls(
                    response, tool_registry, auth_token
                )

                print(f"📊 Function call results:")
                for i, result in enumerate(function_results, 1):
                    print(f"   {i}. {result['name']}: {result['content'][:200]}...")

                # Add function results to conversation
                messages.extend(function_results)

                # Make final API call to get assistant's summary
                print("🔄 Making final API call for summary...")
                final_response = await client.create_chat_completion(
                    messages=messages,
                    tools=available_tools,
                    model="gpt-4o-mini"
                )

                final_message = final_response["choices"][0]["message"]
                final_text = final_message.get("content", "No final response")
                print(f"✅ Final response: {final_text}")

            else:
                print("ℹ️  No function calls requested by assistant")

            print(f"✅ {test_name} test completed successfully!")
            return True

    except Exception as e:
        print(f"❌ Error in {test_name} test: {e}")
        logger.error(f"Full error: {e}", exc_info=True)
        return False


async def main():
    """Run all tool calling tests."""

    print("🚀 Starting OpenAI Tool Calling Tests")
    print("=" * 60)

    # Register all tools
    print("📝 Registering tools...")
    register_location_tools_direct()
    register_program_tools_direct()

    tools = tool_registry.list_tools()
    print(f"✅ Registered {len(tools)} tools: {', '.join(tools)}")
    print()

    # Check for required environment variables
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ OPENAI_API_KEY environment variable is required")
        print("   Please set it in your .env file or environment")
        return

    # Run tests
    test_results = []

    # Test 1: Location Types
    result1 = await test_location_tools()
    test_results.append(("Location Tools", result1))
    print()

    # Test 2: Catchments
    result2 = await test_catchments()
    test_results.append(("Catchments", result2))
    print()

    # Test 3: Program Tools
    result3 = await test_program_tools()
    test_results.append(("Program Tools", result3))
    print()

    # Summary
    print("📊 Test Results Summary")
    print("=" * 60)
    passed = 0
    for test_name, result in test_results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name}: {status}")
        if result:
            passed += 1

    print(f"\n🎯 Overall: {passed}/{len(test_results)} tests passed")

    if passed == len(test_results):
        print("🎉 All tests passed! OpenAI tool calling is working correctly.")
    else:
        print("⚠️  Some tests failed. Check the logs above for details.")


if __name__ == "__main__":
    asyncio.run(main())
