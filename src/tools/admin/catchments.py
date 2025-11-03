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
from src.schemas.catchment_contract import (
    CatchmentContract,
    CatchmentUpdateContract,
    CatchmentDeleteContract,
)
from src.schemas.field_names import CatchmentFields
from src.core import tool_registry

logger = logging.getLogger(__name__)


async def get_catchments(auth_token: str) -> str:
    result = await AvniClient().call_avni_server("GET", "/catchment", auth_token)

    if not result.success:
        return format_error_message(result, "retrieve catchments")

    if not result.data:
        return format_empty_message("catchments")

    return format_list_response(result.data)


async def create_catchment(auth_token: str, contract: CatchmentContract) -> str:
    payload = {
        CatchmentFields.DELETE_FAST_SYNC.value: False,
        CatchmentFields.NAME.value: contract.name,
        CatchmentFields.LOCATION_IDS.value: contract.locationIds,
    }

    log_payload("Catchment CREATE payload:", payload)

    result = await AvniClient().call_avni_server(
        "POST", "/catchment", auth_token, payload
    )

    if not result.success:
        return format_error_message(result, "create catchment")

    return format_creation_response(
        "Catchment", contract.name, CatchmentFields.ID.value, result.data
    )


async def update_catchment(auth_token: str, contract: CatchmentUpdateContract) -> str:
    payload = {
        CatchmentFields.NAME.value: contract.name,
        CatchmentFields.LOCATION_IDS.value: contract.locationIds,
        CatchmentFields.DELETE_FAST_SYNC.value: contract.deleteFastSync,
    }

    log_payload("Catchment UPDATE payload:", payload)

    result = await AvniClient().call_avni_server(
        "PUT", f"/catchment/{contract.id}", auth_token, payload
    )

    if not result.success:
        return format_error_message(result, "update catchment")

    return format_update_response(
        "Catchment", contract.name, CatchmentFields.ID.value, result.data
    )


async def delete_catchment(auth_token: str, contract: CatchmentDeleteContract) -> str:
    result = await AvniClient().call_avni_server(
        "DELETE", f"/catchment/{contract.id}", auth_token
    )

    if not result.success:
        return format_error_message(result, "delete catchment")

    return format_deletion_response("Catchment", contract.id)


def register_catchment_tools() -> None:
    tool_registry.register_tool(get_catchments)
    tool_registry.register_tool(create_catchment)
    tool_registry.register_tool(update_catchment)
    tool_registry.register_tool(delete_catchment)
