import logging
from src.clients import make_avni_request
from src.utils.format_utils import format_creation_response
from src.utils.session_context import log_payload
from src.core import tool_registry

logger = logging.getLogger(__name__)

async def create_encounter_type(
    auth_token: str, name: str, subject_type_uuid: str, program_uuid: str = None
) -> str:
    """Create an encounter type for a program and subject type in Avni.

    Args:
        auth_token: Authentication token for Avni API
        name: Name of the encounter type
        subject_type_uuid: Subject type UUID
        program_uuid: Program UUID (optional, None for general encounters)
    """
    payload = {
        "name": name,
        "entityEligibilityCheckRule": "",
        "entityEligibilityCheckDeclarativeRule": None,
        "loaded": True,
        "subjectTypeUuid": subject_type_uuid,
    }
    
    # Only include programUuid if it's provided, not None, and not empty string
    if program_uuid is not None and program_uuid.strip() != "":
        payload["programUuid"] = program_uuid
    
    # Log the actual API payload to both standard and session loggers
    log_payload("Encounter Type API payload:", payload)

    result = await make_avni_request(
        "POST", "/web/encounterType", auth_token, payload
    )

    if not result.success:
        return result.format_error("create encounter type")

    return format_creation_response("Encounter type", name, "uuid", result.data)


def register_encounter_tools() -> None:
    tool_registry.register_tool(create_encounter_type)
