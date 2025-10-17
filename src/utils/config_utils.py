"""Configuration processing utilities for Avni MCP Server."""

import json
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)


def build_system_instructions() -> str:
    """Build system instructions for the LLM.


    Returns:
        Complete system instructions string
    """
    instructions = """You are an AI assistant that processes Avni platform configurations with CRUD operations (Create, Read, Update, Delete).

Your task is to analyze the provided existing config and execute the requested CRUD operations using available tools.
You must create contract objects with the exact field structure.

CRITICAL CRUD OPERATION RULES:
1. Process operations in order: DELETE first, then UPDATE, then CREATE
2. For DELETE operations: Make contract objects with only the 'id' field
3. For UPDATE operations: Make contract objects with 'id' field plus all fields to update
4. For CREATE operations: Make contract objects with all required fields (no 'id' field)

CRITICAL CONTRACT-BASED TOOL USAGE:
- We require proper objects as parameters, we dont have primitives as arguments
- Each entity type has specific contract classes: AddressLevelTypeContract, LocationContract, etc.

CRITICAL PARENT-CHILD RELATIONSHIP RULES:
1. NEVER create child items and parent items simultaneously in the same response
2. ALWAYS create parent items first, wait for their creation results, then use the ACTUAL database IDs
3. Config uses descriptive references (e.g., "id of TestState") - you must resolve to actual database IDs
4. CREATE ITEMS SEQUENTIALLY, not all at once
5. **MANDATORY ID TRACKING**: When a function returns "created successfully with ID 1234", you MUST extract and use that exact ID (1234) for any dependent items
6. **EXAMPLE**: If create_location_type returns "Location type 'CRUD State' created successfully with ID 1732", then use parentId: 1732 for any child items that reference "id of CRUD State"
7. **NEVER USE DEFAULT VALUES**: Do not use parentId: 0 when the config specifies a parent reference - always resolve to the actual database ID. However, when config explicitly has parentId: null, preserve that null value.

CRITICAL DISTINCTION: ADDRESS LEVEL TYPES vs LOCATIONS:
- Address Level Types (location types) are TEMPLATES that define location hierarchy levels
- Locations are ACTUAL geographic instances that use those templates
- **NEVER** use an AddressLevelType ID as a Location parent ID
- Location parents must reference OTHER LOCATION IDs, not AddressLevelType IDs
- When creating locations: location_type parameter = AddressLevelType NAME, parents[].id = actual LOCATION ID

CRITICAL DATA TYPE CONVERSION RULES:
- ALL database IDs (parentId, locationIds, parents[].id) MUST be sent as INTEGERS, not strings
- When resolving "id of ItemName" references, convert the result to integer before using
- When there are multiple location Ids they need to be in an array for Example: locationIds: [269896, 269895] is correct wheras  ["269896", "269895"] and "269903,269904" are incorrect especially when creating catchments
- UUIDs remain as strings

CRITICAL NULL/PARENT HANDLING RULES:
- When parentId is null in config: PRESERVE null, do NOT convert to 0 or any other value
- For top-level items with parentId: null in config: Keep parentId: null in the contract object
- NEVER convert null values to 0, empty string, or any default value
- **CRITICAL SELF-REFERENCE BUG**: NEVER set parentId to the same value as the item's own ID - an item cannot be its own parent
- When config has "parent_id": null, ensure parentId: null in contract, NOT parentId: <item's own ID>
- Only omit parentId field completely when the config doesn't specify it at all
- For locations with no parent: DO NOT include parentId parameter in function calls
- For location creation: location_type parameter must be the addressLevelType NAME (e.g., "TestState"), not the database ID

OTHER CONVERSION RULES:
- For encounter types: entityEligibilityCheckRule must be empty string "", entityEligibilityCheckDeclarativeRule must be null
- For general encounters:DO NOT include program_uuid parameter in function calls payload at all (do not send "program_uuid": "" ,program_uuid should be completely neglected), otherwise it will fail to create encounter type
- For program-specific encounters: include program_uuid parameter with actual program UUID

UUID GENERATION AND REFERENCE RULES:
- When config contains "uuid": "generate-v4-uuid" or "subjectTypeUuid": "generate-v4-uuid" → Generate a new UUID version 4 and use that value
- When config contains "subjectTypeUuid": "reference-subject-uuid-for-individuals" → Find the existing "Individual" subject type UUID from operational context and use that value
- When config contains "subjectTypeUuid": "reference-subject-uuid-for-household" → Find the existing "Household" subject type UUID from operational context and use that value
- When config contains any field with "generate-v4-uuid" → Generate a new UUID v4 for that field
- When config contains any field with "reference-subject-uuid-for-X" → Find the existing subject type with name X and use its UUID
- Generated UUIDs must be in standard format: xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx
- Always use the EXACT UUID from operational context when referencing existing items

EXAMPLES:

**STEP-BY-STEP ID RESOLUTION EXAMPLE**:
Config: "parentId": "id of CRUD State"
1. First, create CRUD State: create_location_type(name="CRUD State", level=3)
2. Function returns: "Location type 'CRUD State' created successfully with ID 1732"
3. Extract and store: "CRUD State" → 1732
4. For child item: use parentId: 1732 (NOT parentId: 0 or parentId: null)

**NULL/PARENT HANDLING EXAMPLES**:
- Config: {"name":"Updated CRUD State","parentId":null} → Contract: {"name":"Updated CRUD State","parentId":null} (PRESERVE null)
- Config: {"name":"SubCounty","parentId":"id of TestState"} → Contract: {"name":"SubCounty","parentId":1234} (resolve to actual DB ID)
- Config: {"name":"TopLevel"} → Contract: {"name":"TopLevel"} (omit parentId field entirely if not in config)

**COMMON MISTAKES TO AVOID**:
- WRONG: parentId: 0 (never use 0)
- WRONG: parentId: 269937 when id: 269937 (self-reference)  
- CORRECT: parentId: null for top-level items
- CORRECT: parentId: 5678 when referencing actual parent location ID 5678

**ADDRESS LEVEL TYPE vs LOCATION EXAMPLES**:
- AddressLevelTypes: {"name":"SubCounty","parentId":"id of TestState"} → resolve "TestState" ADDRESS LEVEL TYPE to actual DB ID (e.g., 1732)
- Locations: {"parents":[{"id":"id of TestState"}]} → resolve "TestState" LOCATION to actual LOCATION ID (e.g., 5678)
- WRONG: create_location with parents:[{"id": 1732}] where 1732 is AddressLevelType ID
- CORRECT: create_location with parents:[{"id": 5678}] where 5678 is actual Location ID
- Location creation: use create_location(name="Karnataka Test", level=3, location_type="TestState") → location_type is AddressLevelType NAME

**REFERENCE RESOLUTION PROCESS**:
1. "id of TestState" in AddressLevelType context → Find AddressLevelType named "TestState" → Use its ID (e.g., 1732)
2. "id of TestState" in Location context → Find Location named "TestState" → Use its ID (e.g., 5678)
3. Always check context: are you creating AddressLevelType or Location?

**OTHER EXAMPLES**:
- Programs: {"subjectTypeUuid":"uuid of Test Individual"} → resolve to actual UUID from creation
- EncounterTypes: {"programUuid":"uuid of Test Health Program"} → resolve to actual UUID

IMPORTANT: You must respond in JSON format with these fields:
{
  "done": boolean,  // true only when ALL CRUD operations are successfully processed
  "status": "processing|completed|error",
  "results": {
    "deleted_address_level_types": [...],
    "deleted_locations": [...],
    "deleted_catchments": [...], 
    "deleted_subject_types": [...],
    "deleted_programs": [...],
    "deleted_encounter_types": [...],
    "updated_address_level_types": [...],
    "updated_locations": [...],
    "updated_catchments": [...], 
    "updated_subject_types": [...],
    "updated_programs": [...],
    "updated_encounter_types": [...],
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
  "endUserResult": "✅ Successfully created 3 address level types (State, District, Block), 2 locations (Karnataka, Bangalore), and 1 health program. Configuration is ready for use!",
  "next_action": "description of what you plan to do next"
}

Only set done=true when you have successfully processed ALL requested CRUD operations.

Available tools will help you:
- Get existing location types, locations, programs, subject types, encounter types
- Create, update, and delete items using contract objects

CRUD Processing order should be:
1. DELETE operations first (in any order since they remove dependencies)
2. UPDATE operations next (modify existing items)
3. CREATE operations last (in dependency order):
   a. Address Level Types (location types) - CREATE TOP LEVEL FIRST, then children with actual parent IDs
   b. Locations - CREATE TOP LEVEL FIRST, then children with actual parent IDs
   c. Catchments - after all required locations exist
   d. Subject Types - for household/group types, CREATE MEMBER SUBJECT TYPES FIRST before creating the household/group
   e. Programs - after all required subject types exist
   f. Encounter Types - after all required subject types and programs exist

SEQUENTIAL CREATION WORKFLOW:
- Create one item at a time if there are dependencies
- Wait for creation result to get the actual database ID
- Use that actual ID for dependent items
- Do NOT create multiple dependent items in the same function call batch

SPECIFIC DEPENDENCY RULES:
1. For AddressLevelTypes: Create top-level (parentId: null) first, then children using actual parent database ID
2. For Locations: Create top-level (parents: []) first, then children using actual parent location ID
   - CRITICAL: Use addressLevelType NAME for location_type parameter, NOT the database ID
   - CRITICAL: parents[].id must be LOCATION ID, NEVER use AddressLevelType ID
   - Example: create_location(name="Karnataka", level=3, location_type="TestState") ← "TestState" is the AddressLevelType NAME
   - Example: parents:[{"id": 5678}] where 5678 is an actual Location ID, NOT AddressLevelType ID
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

**CRITICAL REFERENCE RESOLUTION PROCESS**:
1. **Extract IDs from function results**: When create_location_type returns "Location type 'CRUD State' created successfully with ID 1732", store "CRUD State" → 1732
2. **Use exact extracted IDs**: For "parentId": "id of CRUD State", use parentId: 1732 (the exact ID returned)
3. **Track all created items**: Maintain a mapping of item names to their actual database IDs/UUIDs
4. **Never guess or default**: If config says "id of X", you MUST find the actual ID of X from function results or existing data

- First check existing operational context, then check newly created items for reference resolution
- Keep track of both existing and created items for resolving references
- CRITICAL: When resolving to database IDs, always convert strings to integers for numeric fields (parentId, locationIds, etc.)

OPERATIONAL CONTEXT:
The 'existing_config' key in the message will contain what already exists in the system. Use this to:
- Check if items already exist before creating (MANDATORY - see rules above). You must do this for all the entities (AddressLevelTypes, Locations, Catchments, SubjectTypes, Programs, EncounterTypes )
- Reference existing UUIDs and IDs when creating relationships
- Avoid duplicating existing configuration

MANDATORY EXISTENCE CHECKING RULES:
Before ANY CREATE operation, you MUST:
1. **CHECK EXISTING CONFIGURATION FIRST**: Search the 'existing_config' for items with the same name
2. **CASE-INSENSITIVE NAME MATCHING**: Compare names using case-insensitive comparison (e.g., "State" matches "state" or "STATE")
3. **SKIP CREATION IF EXISTS**: If an item with the same name already exists (ignoring case), DO NOT create it
4. **RECORD AS EXISTING**: Add existing items to the appropriate "existing_*" arrays in results
5. **CONTINUE PROCESSING**: Move to the next item without treating this as an error

EXISTENCE CHECKING WORKFLOW EXAMPLE:
1. CRUD config wants to create AddressLevelType "State"
2. Check existing_config.addressLevelTypes for any item where name is "state" (case-insensitive)
3. IF FOUND: Skip creation, add to existing_address_level_types: [{"name": "State", "id": 123, "reason": "already_exists"}])
3. IF FOUND: Skip creation, add to existing_address_level_types: [{"name": "State", "id": 123, "reason": "already_exists"}]
4. IF NOT FOUND: Proceed with creation using create_address_level_type()

"""

    return instructions


def build_initial_input(
    config: Dict[str, Any], operational_context: Dict[str, Any]
) -> str:
    """Build initial input for the LLM.

    Args:
        config: CRUD configuration object to process
        operational_context: Existing configuration from Avni

    Returns:
        Initial input string for the LLM
    """
    input_data = {"existing_config": operational_context, "crud_config": config}

    # Identify which operations are requested
    operations = []
    if "delete" in config and config["delete"]:
        operations.append("DELETE")
    if "update" in config and config["update"]:
        operations.append("UPDATE")
    if "create" in config and config["create"]:
        operations.append("CREATE")

    return f"""Please process the CRUD configuration below. 

FIRST: Analyze the 'existing_config' to understand what already exists in the system:
- List all existing address level types, locations, subject types, programs, and encounter types
- Note their IDs, UUIDs, and names for reference resolution

THEN: Process 'crud_config' operations in this order: {" → ".join(operations)}

CRITICAL RULES FOR EACH OPERATION TYPE:
- DELETE: Use delete contract objects with only 'id' field (e.g., {{"id": 123}})
- UPDATE: Use update contract objects with 'id' field plus all fields to update
- CREATE: Use create contract objects with all required fields (no 'id' field)
- Process DELETE operations first, then UPDATE, then CREATE
- For CREATE operations, follow dependency order (parents before children)
- Check existing_config first to avoid operating on non-existent items
- ALWAYS convert descriptive references to actual database values with correct data types
- For locationIds in catchments: MUST be integers [123, 456, 789], NOT strings ["123", "456", "789"]
- For parentId and location parents: MUST be integers, NOT strings
- Wait for operation results to get actual IDs/UUIDs before proceeding to dependent operations

{json.dumps(input_data, indent=2)}



Remember to respond in JSON format with the required fields and track all CRUD operations separately."""


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
                        json_str = response_content[start : end + 1]
                        try:
                            parsed = json.loads(json_str)
                            json_blocks.append(parsed)
                            logger.info(
                                f"Found valid JSON block with done={parsed.get('done', 'unknown')}"
                            )
                        except json.JSONDecodeError:
                            logger.warning(
                                f"Invalid JSON block found: {json_str[:100]}..."
                            )
                        break
                end += 1
            i = end + 1

        # Return the last valid JSON block (most recent response)
        if json_blocks:
            final_response = json_blocks[-1]
            logger.info(
                f"Using final JSON block with done={final_response.get('done', 'unknown')}"
            )
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
    if hasattr(response, "output_text"):
        return response.output_text or ""

    return ""


def log_openai_response_summary(response, session_logger):
    """Log OpenAI response summary with key fields, avoiding expensive full serialization.

    Args:
        response: OpenAI response object
        session_logger: Logger instance to use
    """
    try:
        # Extract key fields without full serialization
        response_id = getattr(response, "id", "N/A")
        model = getattr(response, "model", "N/A")
        created_at = getattr(response, "created_at", "N/A")
        object_type = getattr(response, "object", "N/A")

        # Check for choices and tool calls
        choices_count = 0
        tool_calls_count = 0
        if hasattr(response, "choices") and response.choices:
            choices_count = len(response.choices)
            if hasattr(response.choices[0], "message") and hasattr(
                response.choices[0].message, "tool_calls"
            ):
                tool_calls_count = (
                    len(response.choices[0].message.tool_calls)
                    if response.choices[0].message.tool_calls
                    else 0
                )

        # Check for other key fields
        temperature = getattr(response, "temperature", "N/A")
        tool_choice = getattr(response, "tool_choice", "N/A")
        parallel_tool_calls = getattr(response, "parallel_tool_calls", "N/A")

        session_logger.info(
            f"Response Summary: id={response_id}, model={model}, created_at={created_at}, "
            f"object={object_type}, choices={choices_count}, tool_calls={tool_calls_count}, "
            f"temperature={temperature}, tool_choice={tool_choice}, parallel_tool_calls={parallel_tool_calls}"
        )

    except Exception as e:
        session_logger.warning(f"Could not log response summary: {e}")
        session_logger.info("Response: [Could not extract summary]")


def log_input_list(input_list, session_logger, prefix="Current input list"):
    """Log input list items for debugging.

    Args:
        input_list: List of input items to log
        session_logger: Logger instance to use
        prefix: Prefix message for the log
    """
    session_logger.info(f"{prefix}:")
    for i, item in enumerate(input_list):
        if isinstance(item, dict):
            session_logger.info(
                f"  {i}: {item.get('type', item.get('role', 'unknown'))} - {str(item)[:100]}..."
            )
        else:
            session_logger.info(f"  {i}: {type(item)} - {str(item)[:100]}...")


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
            "deleted_address_level_types": [],
            "deleted_locations": [],
            "deleted_catchments": [],
            "deleted_subject_types": [],
            "deleted_programs": [],
            "deleted_encounter_types": [],
            "updated_address_level_types": [],
            "updated_locations": [],
            "updated_catchments": [],
            "updated_subject_types": [],
            "updated_programs": [],
            "updated_encounter_types": [],
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
            "errors": [],
        },
        "next_action": next_action,
    }
