#!/usr/bin/env python3
"""Test the Config Agent API endpoints."""

import asyncio
import json
import os
import httpx
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "http://localhost:8024"

async def test_health_check():
    """Test the health check endpoint."""
    print("🏥 Testing health check...")
    
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/health")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        print()

async def test_list_tools():
    """Test the tools listing endpoint."""
    print("🔧 Testing tools listing...")
    
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/v1/tools")
        data = response.json()
        print(f"Status: {response.status_code}")
        print(f"Tools count: {data['count']}")
        print("Available tools:")
        for i, tool in enumerate(data['tools'], 1):
            print(f"  {i}. {tool['function']['name']}: {tool['function']['description']}")
        print()

async def test_simple_chat():
    """Test the simple chat endpoint."""
    print("💬 Testing simple chat endpoint...")
    
    avni_token = os.getenv("AVNI_API_TOKEN")
    if not avni_token:
        print("❌ AVNI_API_TOKEN not found in environment")
        return
    
    headers = {
        "Content-Type": "application/json",
        "X-Avni-Auth-Token": avni_token
    }
    
    payload = {
        "message": "Can you get the list of location types available in the system?"
    }
    
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(
            f"{BASE_URL}/chat",
            headers=headers,
            json=payload
        )
        
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Response: {data['response']}")
        else:
            print(f"Error: {response.text}")
        print()

async def test_openai_compatible_endpoint():
    """Test the OpenAI-compatible chat completions endpoint."""
    print("🤖 Testing OpenAI-compatible endpoint...")
    
    openai_key = os.getenv("OPENAI_API_KEY")
    avni_token = os.getenv("AVNI_API_TOKEN")
    
    if not openai_key:
        print("❌ OPENAI_API_KEY not found in environment")
        return
    if not avni_token:
        print("❌ AVNI_API_TOKEN not found in environment")
        return
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {openai_key}",
        "X-Avni-Auth-Token": avni_token
    }
    
    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {
                "role": "user",
                "content": "Create a new subject type called 'Student' of type 'Person'"
            }
        ],
        "temperature": 0.7,
        "max_tokens": 1000
    }
    
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(
            f"{BASE_URL}/v1/chat/completions",
            headers=headers,
            json=payload
        )
        
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            content = data["choices"][0]["message"]["content"]
            print(f"Response: {content}")
        else:
            print(f"Error: {response.text}")
        print()

async def test_root_endpoint():
    """Test the root endpoint."""
    print("🏠 Testing root endpoint...")
    
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        print()

async def main():
    """Run all tests."""
    print("🚀 Testing Avni Config Agent API")
    print("=" * 50)
    
    try:
        await test_root_endpoint()
        await test_health_check()
        await test_list_tools()
        await test_simple_chat()
        await test_openai_compatible_endpoint()
        
        print("✅ All tests completed!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")

if __name__ == "__main__":
    asyncio.run(main())
