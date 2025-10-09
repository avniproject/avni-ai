import logging
from typing import List
from src.clients import make_avni_request
from src.utils.format_utils import format_list_response, format_creation_response
from src.utils.session_context import log_payload
from src.core import tool_registry

logger = logging.getLogger(__name__)

async def get_catchments(auth_token: str) -> str:
    """Retrieve a list of catchments for an organization to find IDs for assigning users."""
    result = await make_avni_request("GET", "/catchment", auth_token)

    if not result.success:
        return result.format_error("retrieve catchments")

    if not result.data:
        return result.format_empty("catchments")

    return format_list_response(result.data)


async def create_catchment(
        auth_token: str, name: str, location_ids: List[int]
) -> str:
    """Create a catchment grouping locations for data collection in Avni.

    Args:
        auth_token: Authentication token for Avni API
        name: Name of the catchment
        location_ids: List of location IDs
    """
    # Convert location_ids to integers to handle cases where LLM sends strings or string arrays
    try:
        # Handle case where LLM sends location_ids as a string representation of an array
        if isinstance(location_ids, str):
            import json
            # First try to parse as JSON array
            try:
                location_ids = json.loads(location_ids)
            except json.JSONDecodeError:
                # If JSON parsing fails, try to split comma-separated values
                if "," in location_ids:
                    location_ids = [id_str.strip() for id_str in location_ids.split(",")]
                else:
                    return f"Error: location_ids appears to be a malformed string: {location_ids}"
        
        # Ensure location_ids is a list
        if not isinstance(location_ids, list):
            return f"Error: location_ids must be a list, got {type(location_ids)}: {location_ids}"
        
        converted_location_ids = []
        for location_id in location_ids:
            if isinstance(location_id, str):
                converted_location_ids.append(int(location_id))
            elif isinstance(location_id, int):
                converted_location_ids.append(location_id)
            else:
                return f"Invalid location_id type: {type(location_id)}. Expected int or string."
        
        if not converted_location_ids:
            return "Error: location_ids cannot be empty"
            
    except ValueError as e:
        return f"Error converting location_ids to integers: {e}. location_ids: {location_ids}"
    
    payload = {"deleteFastSync": False, "name": name, "locationIds": converted_location_ids}
    
    # Log the actual API payload to both standard and session loggers
    log_payload("Catchment API payload:", payload)

    result = await make_avni_request("POST", "/catchment", auth_token, payload)

    if not result.success:
        return result.format_error("create catchment")

    return format_creation_response("Catchment", name, "id", result.data)


def register_catchment_tools() -> None:
    tool_registry.register_tool(get_catchments)
    tool_registry.register_tool(create_catchment)