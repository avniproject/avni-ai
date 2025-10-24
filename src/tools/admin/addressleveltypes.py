import logging
from src.clients import AvniClient
from src.utils.session_context import log_payload
from src.utils.result_utils import format_error_message, format_creation_response, format_update_response, format_deletion_response, format_validation_error
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

    payload = {
        AddressLevelTypeFields.NAME.value: contract.name,
        AddressLevelTypeFields.LEVEL.value: contract.level,
    }

    if contract.parentId is not None and contract.parentId != "":
        try:
            if isinstance(contract.parentId, str):
                if contract.parentId.strip() == "":
                    pass
                else:
                    payload[AddressLevelTypeFields.PARENT_ID.value] = int(
                        contract.parentId
                    )
            else:
                payload[AddressLevelTypeFields.PARENT_ID.value] = contract.parentId
        except ValueError as e:
            return format_validation_error("create location type", f"Invalid parentId '{contract.parentId}': {str(e)}")

    log_payload("AddressLevelType CREATE payload:", payload)

    result = await AvniClient().call_avni_server("POST", "/addressLevelType", auth_token, payload)

    if not result.success:
        return format_error_message(result, "create location type")

    return format_creation_response("Location type", contract.name, AddressLevelTypeFields.ID.value, result.data)


async def update_location_type(
    auth_token: str, contract: AddressLevelTypeUpdateContract
) -> str:

    # Auto-correct self-referencing parentId (common LLM mistake)
    if contract.parentId is not None and contract.parentId == contract.id:
        contract.parentId = None

    # Auto-correct parentId: 0 to null (common LLM mistake)
    if contract.parentId == 0:
        contract.parentId = None

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
            return format_validation_error("update location type", f"Invalid parentId '{contract.parentId}': {str(e)}")

    log_payload("AddressLevelType UPDATE payload:", payload)

    result = await AvniClient().call_avni_server(
        "PUT", f"/addressLevelType/{contract.id}", auth_token, payload
    )

    if not result.success:
        return format_error_message(result, "update location type")

    return format_update_response("Location type", contract.name, AddressLevelTypeFields.ID.value, result.data)


async def delete_location_type( auth_token: str, contract: AddressLevelTypeDeleteContract) -> str:

    result = await AvniClient().call_avni_server(
        "DELETE", f"/addressLevelType/{contract.id}", auth_token
    )

    if not result.success:
        return format_error_message(result, "delete location type")

    return format_deletion_response("Location type", contract.id)


def register_address_level_type_tools() -> None:
    tool_registry.register_tool(create_location_type)
    tool_registry.register_tool(update_location_type)
    tool_registry.register_tool(delete_location_type)
