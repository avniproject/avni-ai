import logging
from src.clients import AvniClient
from src.utils.result_utils import (
    format_error_message,
    format_implementation_deletion_response,
)
from src.services import tool_registry
from src.schemas.implementation_contract import ImplementationDeleteContract

logger = logging.getLogger(__name__)


async def delete_implementation(
    contract: ImplementationDeleteContract, auth_token: str
) -> str:
    query_params = f"deleteMetadata={str(contract.deleteMetadata).lower()}&deleteAdminConfig={str(contract.deleteAdminConfig).lower()}"

    result = await AvniClient().call_avni_server(
        "DELETE", f"/implementation/delete?{query_params}", auth_token
    )

    if not result.success:
        return format_error_message(result, "delete implementation")

    return format_implementation_deletion_response(
        contract.deleteMetadata, contract.deleteAdminConfig
    )


def register_implementation_tools() -> None:
    tool_registry.register_tool(delete_implementation)
