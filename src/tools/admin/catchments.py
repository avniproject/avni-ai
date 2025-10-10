import logging
from typing import List
from src.clients import make_avni_request
from src.utils.format_utils import format_list_response, format_creation_response
from src.utils.session_context import log_payload
from src.schemas.catchment_contract import (
    CatchmentContract,
    CatchmentUpdateContract,
    CatchmentDeleteContract,
)
from src.schemas.field_names import CatchmentFields
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


async def create_catchment(auth_token: str, contract: CatchmentContract) -> str:
    """Create a catchment grouping locations for data collection in Avni.

    Args:
        auth_token: Authentication token for Avni API
        contract: CatchmentContract with catchment details
    """
    payload = {
        CatchmentFields.DELETE_FAST_SYNC.value: False,
        CatchmentFields.NAME.value: contract.name,
        CatchmentFields.LOCATION_IDS.value: contract.locationIds,
    }

    # Log the actual API payload to both standard and session loggers
    log_payload("Catchment CREATE payload:", payload)

    result = await make_avni_request("POST", "/catchment", auth_token, payload)

    if not result.success:
        return result.format_error("create catchment")

    return format_creation_response("Catchment", contract.name, "id", result.data)


async def update_catchment(auth_token: str, contract: CatchmentUpdateContract) -> str:
    """Update an existing catchment in Avni.

    Args:
        auth_token: Authentication token for Avni API
        contract: CatchmentUpdateContract with update details
    """
    payload = {
        CatchmentFields.NAME.value: contract.name,
        CatchmentFields.LOCATION_IDS.value: contract.locationIds,
        CatchmentFields.DELETE_FAST_SYNC.value: contract.deleteFastSync,
    }

    # Log the actual API payload to both standard and session loggers
    log_payload("Catchment UPDATE payload:", payload)

    result = await make_avni_request(
        "PUT", f"/catchment/{contract.id}", auth_token, payload
    )

    if not result.success:
        return result.format_error("update catchment")

    return format_creation_response("Catchment", contract.name, "id", result.data)


async def delete_catchment(auth_token: str, contract: CatchmentDeleteContract) -> str:
    """Delete (void) an existing catchment in Avni.

    Args:
        auth_token: Authentication token for Avni API
        contract: CatchmentDeleteContract with ID to delete
    """
    # Log the delete operation
    logger.info(f"Catchment DELETE: ID {contract.id}")

    result = await make_avni_request("DELETE", f"/catchment/{contract.id}", auth_token)

    if not result.success:
        return result.format_error("delete catchment")

    return f"Catchment with ID {contract.id} successfully deleted (voided)"


def register_catchment_tools() -> None:
    tool_registry.register_tool(get_catchments)
    tool_registry.register_tool(create_catchment)
    tool_registry.register_tool(update_catchment)
    tool_registry.register_tool(delete_catchment)
