from typing import Optional
from src.clients import make_avni_request
from src.utils.format_utils import format_creation_response
from src.core import tool_registry

async def create_subject_type(
    auth_token: str,
    name: str,
    subject_type: str,
    location_type_uuid: Optional[str] = None,
) -> str:
    """Create a subject type (e.g., Person, Household) for data collection in Avni.

    Args:
        auth_token: Authentication token for Avni API
        name: Name of the subject type
        subject_type: Type of the subject: Person, Individual, Group, Household or User
        location_type_uuid: Location type UUID (optional)
    """
    settings = {
        "displayRegistrationDetails": True,
        "displayPlannedEncounters": True,
    }

    payload = {
        "name": name,
        "groupRoles": [],
        "subjectSummaryRule": "",
        "programEligibilityCheckRule": "",
        "shouldSyncByLocation": True,
        "lastNameOptional": False,
        "settings": settings,
        "type": subject_type,
        "active": True,
        "locationTypeUUIDs": [location_type_uuid] if location_type_uuid else [],
    }

    result = await make_avni_request(
        "POST", "/web/subjectType", auth_token, payload
    )

    if not result.success:
        return result.format_error("create subject type")

    return format_creation_response("Subject type", name, "uuid", result.data)

def register_subject_type_tools() -> None:
    """Register program tools for direct function calling."""
    tool_registry.register_tool(create_subject_type)
