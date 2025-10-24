import logging
from src.clients import AvniClient
from src.utils.session_context import log_payload
from src.utils.result_utils import (
    format_error_message,
    format_empty_message,
    format_list_response,
    format_creation_response,
    format_update_response,
    format_deletion_response,
)
from src.schemas.location_contract import (
    LocationContract,
    LocationUpdateContract,
    LocationDeleteContract,
)
from src.schemas.field_names import LocationFields
from src.core import tool_registry

logger = logging.getLogger(__name__)


async def get_locations(auth_token: str) -> str:
    result = await AvniClient().call_avni_server("GET", "/locations", auth_token)

    if not result.success:
        return format_error_message(result, "retrieve location types")

    if not result.data:
        return format_empty_message("location types")

    return format_list_response(result.data, extra_key="level")


async def create_location(auth_token: str, contract: LocationContract) -> str:
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

    log_payload("Location CREATE payload:", payload)

    result = await AvniClient().call_avni_server(
        "POST", "/locations", auth_token, payload
    )

    if not result.success:
        return format_error_message(result, "create location")

    return format_creation_response(
        "Location", contract.name, LocationFields.ID.value, result.data
    )


async def update_location(auth_token: str, contract: LocationUpdateContract) -> str:
    # Auto-correct self-referencing parentId (common LLM mistake)
    if contract.parentId is not None and contract.parentId == contract.id:
        logger.info(
            f"Auto-correcting self-referencing parentId from {contract.parentId} to null for location {contract.id}"
        )
        contract.parentId = None

    # Auto-correct parentId: 0 to null (common LLM mistake)
    if contract.parentId == 0:
        logger.info(
            f"Auto-correcting parentId from 0 to null for location {contract.id}"
        )
        contract.parentId = None

    payload = {
        LocationFields.ID.value: contract.id,
        LocationFields.TITLE.value: contract.title,
        LocationFields.LEVEL.value: contract.level,
    }

    # Only include parentId if it's not None
    if contract.parentId is not None:
        payload[LocationFields.PARENT_ID.value] = contract.parentId

    log_payload("Location UPDATE payload:", payload)

    result = await AvniClient().call_avni_server(
        "PUT", f"/locations/{contract.id}", auth_token, payload
    )

    if not result.success:
        return format_error_message(result, "update location")

    return format_update_response(
        "Location", contract.title, LocationFields.ID.value, result.data
    )


async def delete_location(auth_token: str, contract: LocationDeleteContract) -> str:
    result = await AvniClient().call_avni_server(
        "DELETE", f"/locations/{contract.id}", auth_token
    )

    if not result.success:
        return format_error_message(result, "delete location")

    return format_deletion_response("Location", contract.id)


def register_location_tools() -> None:
    tool_registry.register_tool(get_locations)
    tool_registry.register_tool(create_location)
    tool_registry.register_tool(update_location)
    tool_registry.register_tool(delete_location)
