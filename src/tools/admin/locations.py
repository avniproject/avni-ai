import logging
from src.clients import make_avni_request
from src.utils.format_utils import format_list_response, format_creation_response
from src.utils.session_context import log_payload
from src.schemas.location_contract import (
    LocationContract,
    LocationUpdateContract,
    LocationDeleteContract,
)
from src.schemas.field_names import LocationFields
from src.core import tool_registry

logger = logging.getLogger(__name__)


async def get_locations(auth_token: str) -> str:
    """Retrieve a list of location types for an organization to find IDs for creating locations or sub-location types."""
    result = await make_avni_request("GET", "/locations", auth_token)

    if not result.success:
        return result.format_error("retrieve location types")

    if not result.data:
        return result.format_empty("location types")

    return format_list_response(result.data, extra_key="level")


async def create_location(auth_token: str, contract: LocationContract) -> str:
    """Create a real location (e.g., Himachal Pradesh, Kullu) in Avni's location hierarchy.

    Args:
        auth_token: Authentication token for Avni API
        contract: LocationContract with location details
    """
    # Convert LocationParent objects to API format
    parents_payload = []
    for parent in contract.parents:
        parents_payload.append({LocationFields.ID.value: parent.id})

    payload = [
        {
            LocationFields.NAME.value: contract.name,
            LocationFields.LEVEL.value: contract.level,
            LocationFields.TYPE.value: contract.type,
            LocationFields.PARENTS.value: parents_payload,
        }
    ]

    # Log the actual API payload to both standard and session loggers
    log_payload("Location CREATE payload:", payload)

    result = await make_avni_request("POST", "/locations", auth_token, payload)

    if not result.success:
        return result.format_error("create location")

    return format_creation_response("Location", contract.name, "id", result.data)


async def update_location(auth_token: str, contract: LocationUpdateContract) -> str:
    """Update an existing location in Avni's location hierarchy.

    Args:
        auth_token: Authentication token for Avni API
        contract: LocationUpdateContract with update details
    """
    # Convert LocationParent objects to API format
    parents_payload = []
    for parent in contract.parents:
        parents_payload.append({LocationFields.ID.value: parent.id})

    payload = {
        LocationFields.ID.value: contract.id,
        LocationFields.TITLE.value: contract.title,
        LocationFields.LEVEL.value: contract.level,
        LocationFields.PARENTS.value: parents_payload,
    }

    # Log the actual API payload to both standard and session loggers
    log_payload("Location UPDATE payload:", payload)

    result = await make_avni_request(
        "PUT", f"/locations/{contract.id}", auth_token, payload
    )

    if not result.success:
        return result.format_error("update location")

    return format_creation_response("Location", contract.title, "id", result.data)


async def delete_location(auth_token: str, contract: LocationDeleteContract) -> str:
    """Delete (void) an existing location in Avni.

    Args:
        auth_token: Authentication token for Avni API
        contract: LocationDeleteContract with ID to delete
    """
    # Log the delete operation
    logger.info(f"Location DELETE: ID {contract.id}")

    result = await make_avni_request("DELETE", f"/locations/{contract.id}", auth_token)

    if not result.success:
        return result.format_error("delete location")

    return f"Location with ID {contract.id} successfully deleted (voided)"


def register_location_tools() -> None:
    tool_registry.register_tool(get_locations)
    tool_registry.register_tool(create_location)
    tool_registry.register_tool(update_location)
    tool_registry.register_tool(delete_location)
