import logging
from src.clients import make_avni_request
from src.utils.format_utils import format_creation_response
from src.utils.session_context import log_payload
from src.schemas.address_level_type_contract import (
    AddressLevelTypeContract,
    AddressLevelTypeUpdateContract,
    AddressLevelTypeDeleteContract,
)
from src.schemas.field_names import AddressLevelTypeFields
from src.core import tool_registry

logger = logging.getLogger(__name__)


async def create_location_type(
    auth_token: str, contract: AddressLevelTypeContract
) -> str:
    """Create a location type (e.g., State, District) for hierarchical location setup in Avni.

    Args:
        auth_token: Authentication token for Avni API
        contract: AddressLevelTypeContract with location type details
    """
    payload = {
        AddressLevelTypeFields.NAME.value: contract.name,
        AddressLevelTypeFields.LEVEL.value: contract.level,
    }

    if contract.parentId is not None and contract.parentId != "":
        # Convert parentId to int if it's a string, but only include if not empty
        try:
            if isinstance(contract.parentId, str):
                if contract.parentId.strip() == "":
                    # Empty string means no parent - don't include parentId in payload
                    pass
                else:
                    payload[AddressLevelTypeFields.PARENT_ID.value] = int(
                        contract.parentId
                    )
            else:
                payload[AddressLevelTypeFields.PARENT_ID.value] = contract.parentId
        except ValueError as e:
            return f"Error converting parentId to integer for '{contract.name}': {e}. parentId: {contract.parentId}"

    # Log the actual API payload to both standard and session loggers
    log_payload("AddressLevelType CREATE payload:", payload)

    result = await make_avni_request("POST", "/addressLevelType", auth_token, payload)

    if not result.success:
        return result.format_error("create location type")

    return format_creation_response("Location type", contract.name, "id", result.data)


async def update_location_type(
    auth_token: str, contract: AddressLevelTypeUpdateContract
) -> str:
    """Update an existing location type (e.g., State, District) in Avni.

    Args:
        auth_token: Authentication token for Avni API
        contract: AddressLevelTypeUpdateContract with update details
    """
    payload = {
        AddressLevelTypeFields.UUID.value: contract.uuid,
        AddressLevelTypeFields.NAME.value: contract.name,
        AddressLevelTypeFields.LEVEL.value: contract.level,
    }

    if contract.parentId is not None and contract.parentId != "":
        # Convert parentId to int if it's a string, but only include if not empty
        try:
            if isinstance(contract.parentId, str):
                if contract.parentId.strip() == "":
                    # Empty string means no parent - don't include parentId in payload
                    pass
                else:
                    payload[AddressLevelTypeFields.PARENT_ID.value] = int(
                        contract.parentId
                    )
            else:
                payload[AddressLevelTypeFields.PARENT_ID.value] = contract.parentId
        except ValueError as e:
            return f"Error converting parentId to integer for '{contract.name}': {e}. parentId: {contract.parentId}"

    # Log the actual API payload to both standard and session loggers
    log_payload("AddressLevelType UPDATE payload:", payload)

    result = await make_avni_request(
        "PUT", f"/addressLevelType/{contract.id}", auth_token, payload
    )

    if not result.success:
        return result.format_error("update location type")

    return format_creation_response("Location type", contract.name, "id", result.data)


async def delete_location_type(
    auth_token: str, contract: AddressLevelTypeDeleteContract
) -> str:
    """Delete (void) an existing location type in Avni.

    Args:
        auth_token: Authentication token for Avni API
        contract: AddressLevelTypeDeleteContract with ID to delete
    """
    # Log the delete operation
    logger.info(f"AddressLevelType DELETE: ID {contract.id}")

    result = await make_avni_request(
        "DELETE", f"/addressLevelType/{contract.id}", auth_token
    )

    if not result.success:
        return result.format_error("delete location type")

    return f"Location type with ID {contract.id} successfully deleted (voided)"


def register_address_level_type_tools() -> None:
    tool_registry.register_tool(create_location_type)
    tool_registry.register_tool(update_location_type)
    tool_registry.register_tool(delete_location_type)
