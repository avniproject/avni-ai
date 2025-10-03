#!/usr/bin/env python3
"""Test the process-config endpoint with a sample config object."""

import asyncio
import json
import os
import httpx
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "http://localhost:8024"

# Sample config object based on prompts.py structure
SAMPLE_CONFIG = {
    "config": {
        "addressLevelTypes": [
            {
                "name": "State",
                "level": 3.0,
                "parentId": None
            },
            {
                "name": "District", 
                "level": 2.0,
                "parentId": None
            },
            {
                "name": "Village",
                "level": 1.0,
                "parentId": None
            }
        ],
        "locations": [
            {
                "name": "Karnataka",
                "level": 3.0,
                "type": "State"
            },
            {
                "name": "Bangalore",
                "level": 2.0,
                "type": "District"
            }
        ],
        "subjectTypes": [
            {
                "name": "Patient",
                "type": "Person",
                "uuid": "550e8400-e29b-41d4-a716-446655440001"
            },
            {
                "name": "Healthcare Worker",
                "type": "Person", 
                "uuid": "550e8400-e29b-41d4-a716-446655440002"
            }
        ],
        "programs": [
            {
                "name": "Maternal Health Program",
                "uuid": "550e8400-e29b-41d4-a716-446655440003",
                "colour": "#FF5733",
                "subjectTypeUuid": "550e8400-e29b-41d4-a716-446655440001"
            }
        ],
        "encounterTypes": [
            {
                "name": "Antenatal Checkup",
                "uuid": "550e8400-e29b-41d4-a716-446655440004",
                "subjectTypeUuid": "550e8400-e29b-41d4-a716-446655440001",
                "programUuid": "550e8400-e29b-41d4-a716-446655440003"
            }
        ]
    }
}

async def test_process_config():
    """Test the process-config endpoint with a sample config."""
    print("🔧 Testing process-config endpoint...")
    print("=" * 60)
    
    avni_token = os.getenv("AVNI_API_TOKEN")
    if not avni_token:
        print("❌ AVNI_API_TOKEN not found in environment")
        return
    
    headers = {
        "Content-Type": "application/json",
        "X-Avni-Auth-Token": avni_token
    }
    
    print("📋 Sample config object:")
    print(json.dumps(SAMPLE_CONFIG, indent=2))
    print()
    
    try:
        async with httpx.AsyncClient(timeout=120.0) as client:
            print("🚀 Sending config to process-config endpoint...")
            response = await client.post(
                f"{BASE_URL}/process-config",
                headers=headers,
                json=SAMPLE_CONFIG
            )
            
            print(f"📊 Response Status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print("✅ Config processing completed!")
                print()
                
                # Display results for each section
                for section, data in result["result"].items():
                    print(f"📍 {section.upper()}:")
                    print(f"  ✅ Created: {len(data['created'])}")
                    print(f"  ♻️  Existing: {len(data['existing'])}")
                    print(f"  ❌ Errors: {len(data['errors'])}")
                    
                    if data['created']:
                        print("  Created items:")
                        for item in data['created']:
                            print(f"    - {item}")
                    
                    if data['existing']:
                        print("  Existing items:")
                        for item in data['existing']:
                            print(f"    - {item}")
                    
                    if data['errors']:
                        print("  Errors:")
                        for error in data['errors']:
                            print(f"    - {error}")
                    
                    print()
                
            else:
                print(f"❌ Error: {response.status_code}")
                print(f"Response: {response.text}")
                
    except Exception as e:
        print(f"❌ Request failed: {e}")

async def test_simple_config():
    """Test with a simpler config object."""
    print("\n🧪 Testing with simple config...")
    print("=" * 60)
    
    simple_config = {
        "config": {
            "addressLevelTypes": [
                {
                    "name": "TestState",
                    "level": 2.0
                }
            ],
            "subjectTypes": [
                {
                    "name": "TestPerson",
                    "type": "Person"
                }
            ]
        }
    }
    
    avni_token = os.getenv("AVNI_API_TOKEN")
    if not avni_token:
        print("❌ AVNI_API_TOKEN not found in environment")
        return
    
    headers = {
        "Content-Type": "application/json",
        "X-Avni-Auth-Token": avni_token
    }
    
    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"{BASE_URL}/process-config",
                headers=headers,
                json=simple_config
            )
            
            print(f"📊 Response Status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print("✅ Simple config processing completed!")
                print(json.dumps(result, indent=2))
            else:
                print(f"❌ Error: {response.text}")
                
    except Exception as e:
        print(f"❌ Request failed: {e}")

async def main():
    """Run all tests."""
    print("🚀 Testing Config Processing Endpoint")
    print("=" * 80)
    
    # Test if server is running
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{BASE_URL}/health")
            if response.status_code != 200:
                print("❌ Config Agent server is not running!")
                print("   Please start it with: python3 configagent.py")
                return
    except Exception:
        print("❌ Config Agent server is not running!")
        print("   Please start it with: python3 configagent.py")
        return
    
    print("✅ Config Agent server is running")
    print()
    
    # Run tests
    await test_simple_config()
    await test_process_config()
    
    print("🎯 Testing completed!")

if __name__ == "__main__":
    asyncio.run(main())
