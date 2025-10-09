"""Configuration processing utilities for Avni MCP Server."""

import json
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)


def build_system_instructions(operational_context: Dict[str, Any]) -> str:
    """Build system instructions for the LLM.
    
    Args:
        operational_context: Context from Avni operational modules
        
    Returns:
        Complete system instructions string
    """
    instructions = """You are an AI assistant that processes Avni platform configurations.

Your task is to analyze the provided existing config and expected config, then create the necessary items using available tools.
Do not create items that already exist in the config .

CRITICAL PARENT-CHILD RELATIONSHIP RULES:
1. NEVER create child items and parent items simultaneously in the same response
2. ALWAYS create parent items first, wait for their creation results, then use the ACTUAL database IDs
3. Config uses descriptive references (e.g., "id of TestState") - you must resolve to actual database IDs
4. CREATE ITEMS SEQUENTIALLY, not all at once

CRITICAL DATA TYPE CONVERSION RULES:
- ALL database IDs (parentId, locationIds, parents[].id) MUST be sent as INTEGERS, not strings
- When resolving "id of ItemName" references, convert the result to integer before using
- When there are multiple location Ids they need to be in an array for Example: locationIds: [269896, 269895] is correct wheras  ["269896", "269895"] and "269903,269904" are incorrect especially when creating catchments
- UUIDs remain as strings
- For top-level items (no parent): DO NOT include parentId field in the payload at all
- For locations with no parent: DO NOT include parentId parameter in function calls
- For location creation: location_type parameter must be the addressLevelType NAME (e.g., "TestState"), not the database ID
- For encounter types: entityEligibilityCheckRule must be empty string "", entityEligibilityCheckDeclarativeRule must be null
- For general encounters:DO NOT include program_uuid parameter in function calls payload at all (do not send "program_uuid": "" ,program_uuid should be completely neglected), otherwise it will fail to create encounter type
- For program-specific encounters: include program_uuid parameter with actual program UUID

EXAMPLES:
- AddressLevelTypes: {"name":"SubCounty","parentId":"id of TestState"} → resolve "TestState" to actual DB ID
- Locations: {"parents":[{"id":"id of TestState"}]} → resolve "TestState" location to actual DB ID
- Location creation: use create_location(name="Karnataka Test", level=3, location_type="TestState", parent_id=None) → location_type is NAME not ID
- Programs: {"subjectTypeUuid":"uuid of Test Individual"} → resolve to actual UUID from creation
- EncounterTypes: {"programUuid":"uuid of Test Health Program"} → resolve to actual UUID

IMPORTANT: You must respond in JSON format with these fields:
{
  "done": boolean,  // true only when ALL config items are successfully created
  "status": "processing|completed|error",
  "results": {
    "created_address_level_types": [...],
    "created_locations": [...],
    "created_catchments": [...], 
    "created_subject_types": [...],
    "created_programs": [...],
    "created_encounter_types": [...],
    "existing_address_level_types": [...],
    "existing_locations": [...],
    "existing_catchments": [...],
    "existing_subject_types": [...],
    "existing_programs": [...],
    "existing_encounter_types": [...],
    "errors": [...]    // any errors encountered
  },
  "next_action": "description of what you plan to do next"
}

Only set done=true when you have successfully processed the entire config and all items are created or already exist.

Available tools will help you:
- Get existing location types, locations, programs, subject types, encounter types
- Create new items as needed
- Check what already exists to avoid duplicates

Processing order should be:
1. Address Level Types (location types) - CREATE TOP LEVEL FIRST, then children with actual parent IDs
2. Locations - CREATE TOP LEVEL FIRST, then children with actual parent IDs
   - IMPORTANT: location_type parameter must be the ADDRESS LEVEL TYPE NAME (e.g., "TestState", "TestDistrict"), NOT the database ID
3. Catchments - after all required locations exist
4. Subject Types - for household/group types, CREATE MEMBER SUBJECT TYPES FIRST before creating the household/group
5. Programs - after all required subject types exist
6. Encounter Types - after all required subject types and programs exist
   - For general encounters: use create_encounter_type(auth_token, name, subject_type_uuid) - do NOT include program_uuid parameter
   - For program-specific encounters: use create_encounter_type(auth_token, name, subject_type_uuid, program_uuid)

SEQUENTIAL CREATION WORKFLOW:
- Create one item at a time if there are dependencies
- Wait for creation result to get the actual database ID
- Use that actual ID for dependent items
- Do NOT create multiple dependent items in the same function call batch

SPECIFIC DEPENDENCY RULES:
1. For AddressLevelTypes: Create top-level (parentId: null) first, then children using actual parent database ID
2. For Locations: Create top-level (parents: []) first, then children using actual parent location ID
   - CRITICAL: Use addressLevelType NAME for location_type parameter, NOT the database ID
   - Example: create_location(name="Karnataka", level=3, location_type="TestState") ← "TestState" is the NAME
3. For Household/Group SubjectTypes: Create member subject types first, then reference them in groupRoles
4. For Programs: Ensure referenced subjectTypeUuid exists first
5. For EncounterTypes: Ensure referenced subjectTypeUuid and programUuid (if applicable) exist first
6. For Catchments: Ensure all referenced locationIds exist first and are provided as INTEGERS, not strings

RESOLVING DESCRIPTIVE REFERENCES:
When config contains descriptive references like:
- "parentId": "id of TestState" → Find TestState in existing operational context OR created items, use its actual database ID AS INTEGER
- "parents": [{"id": "id of TestState"}] → Find TestState location in existing OR created items, use its actual ID AS INTEGER
- "locationIds": ["id of TestState", "id of TestDistrict"] → Find locations in existing OR created items, use actual IDs AS INTEGERS
- "subjectTypeUuid": "uuid of Test Individual" → Find Test Individual in existing OR created items, use its actual UUID AS STRING
- First check existing operational context, then check newly created items for reference resolution
- Keep track of both existing and created items for resolving references
- CRITICAL: When resolving to database IDs, always convert strings to integers for numeric fields (parentId, locationIds, etc.)

OPERATIONAL CONTEXT:
The 'existing_config' key in the message will contain what already exists in the system. Use this to:
- Check if items already exist before creating
- Reference existing UUIDs and IDs when creating relationships
- Avoid duplicating existing configuration"""
        
    return instructions


def build_initial_input(config: Dict[str, Any], operational_context: Dict[str, Any]) -> str:
    """Build initial input for the LLM.
    
    Args:
        config: Configuration object to process
        operational_context: Existing configuration from Avni
        
    Returns:
        Initial input string for the LLM
    """
    input_data = {
        "existing_config": operational_context,
        "expected_config": config
    }
    
    return f"""Please process the configuration below. 

FIRST: Analyze the 'existing_config' to understand what already exists in the system:
- List all existing address level types, locations, subject types, programs, and encounter types
- Note their IDs, UUIDs, and names for reference resolution

THEN: Process 'expected_config' to create missing items in the correct order (DO NOT RECREATE EXISTING ITEMS):
- Create items in the following order (top-level first, then children using actual parent database IDs as INTEGERS):
1. Address Level Types (top-level first with NO parentId, then children using actual parent database IDs as INTEGERS)
2. Locations (top-level first with NO parentId, then children using actual parent location IDs as INTEGERS)
3. Catchments (using actual location IDs as INTEGER ARRAY [123, 456] NOT comma-separated string "123,456")
4. Subject Types (member types before household/group types)
5. Programs (using actual subject type UUIDs)
6. Encounter Types (using actual subject type UUIDs, program UUIDs for program-specific encounters, null for general encounters)

CRITICAL RULES:
- Check existing_config first to avoid recreating existing items
- ALWAYS convert descriptive references to actual database values with correct data types
- For locationIds in catchments: MUST be integers [123, 456, 789], NOT strings ["123", "456", "789"]
- NEVER send locationIds as comma-separated string "123,456,789" - use proper array format [123, 456, 789]
- For parentId and location parents: MUST be integers, NOT strings
- Complete each category fully before moving to the next
- Wait for creation results to get actual IDs/UUIDs before proceeding:

{json.dumps(input_data, indent=2)}



Remember to respond in JSON format with the required fields."""


def parse_llm_response(response_content: str) -> Dict[str, Any]:
    """Parse JSON response from LLM.
    
    Args:
        response_content: Raw response content from LLM
        
    Returns:
        Parsed response dictionary with fallback structure
    """
    try:
        # Extract the last complete JSON block from response (LLM might provide multiple JSON blocks)
        # Find all potential JSON blocks by looking for opening braces
        json_blocks = []
        i = 0
        while i < len(response_content):
            start = response_content.find("{", i)
            if start == -1:
                break
            
            # Find the matching closing brace
            brace_count = 0
            end = start
            while end < len(response_content):
                if response_content[end] == "{":
                    brace_count += 1
                elif response_content[end] == "}":
                    brace_count -= 1
                    if brace_count == 0:
                        # Found complete JSON block
                        json_str = response_content[start:end + 1]
                        try:
                            parsed = json.loads(json_str)
                            json_blocks.append(parsed)
                            logger.info(f"Found valid JSON block with done={parsed.get('done', 'unknown')}")
                        except json.JSONDecodeError:
                            logger.warning(f"Invalid JSON block found: {json_str[:100]}...")
                        break
                end += 1
            i = end + 1
        
        # Return the last valid JSON block (most recent response)
        if json_blocks:
            final_response = json_blocks[-1]
            logger.info(f"Using final JSON block with done={final_response.get('done', 'unknown')}")
            return final_response
        else:
            # Fallback if no valid JSON found
            logger.warning("No valid JSON blocks found in LLM response")
            return _create_fallback_response("Continue processing")
    except Exception as e:
        logger.warning(f"Error parsing LLM JSON response: {e}")
        return _create_fallback_response("Continue processing")


def extract_text_content(response) -> str:
    """Extract text content from OpenAI response.
    
    Args:
        response: OpenAI response object
        
    Returns:
        Extracted text content or empty string
    """
    # Use OpenAI response object method
    if hasattr(response, 'output_text'):
        return response.output_text or ""
    
    return ""


def _create_fallback_response(next_action: str) -> Dict[str, Any]:
    """Create fallback response structure when parsing fails.
    
    Args:
        next_action: Description of next action
        
    Returns:
        Fallback response dictionary
    """
    return {
        "done": False,
        "status": "processing", 
        "results": {
            "created_address_level_types": [],
            "created_locations": [],
            "created_catchments": [],
            "created_subject_types": [],
            "created_programs": [],
            "created_encounter_types": [],
            "existing_address_level_types": [],
            "existing_locations": [],
            "existing_catchments": [],
            "existing_subject_types": [],
            "existing_programs": [],
            "existing_encounter_types": [],
            "errors": []
        },
        "next_action": next_action
    }