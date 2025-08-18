"""Program and subject management tools."""

from typing import Optional

from mcp.server.fastmcp import FastMCP

from client import make_avni_request
from utils import format_creation_response


def register_program_tools(mcp: FastMCP) -> None:
    """Register program and subject-related tools with the MCP server."""

    @mcp.tool()
    async def create_subject_type(
        name: str, subject_type: str, location_type_uuid: Optional[str] = None
    ) -> str:
        """Create a subject type (e.g., Person, Household) for data collection in Avni.

        Args:
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

        result = await make_avni_request("POST", "/web/subjectType", payload)

        if not result.success:
            return result.format_error("create subject type")

        return format_creation_response("Subject type", name, "uuid", result.data)

    @mcp.tool()
    async def create_program(name: str, subject_type_uuid: str) -> str:
        """Create a program in Avni for managing data collection activities.

        Args:
            name: Name of the program
            subject_type_uuid: Subject type UUID
        """
        payload = {
            "name": name,
            "colour": "#611717",
            "programSubjectLabel": name.lower().replace(" ", "_"),
            "enrolmentSummaryRule": "",
            "subjectTypeUuid": subject_type_uuid,
            "enrolmentEligibilityCheckRule": "",
            "enrolmentEligibilityCheckDeclarativeRule": None,
            "manualEligibilityCheckRequired": False,
            "showGrowthChart": False,
            "allowMultipleEnrolments": True,
            "manualEnrolmentEligibilityCheckRule": "",
        }

        result = await make_avni_request("POST", "/web/program", payload)

        if not result.success:
            return result.format_error("create program")

        return format_creation_response("Program", name, "uuid", result.data)

    @mcp.tool()
    async def create_encounter_type(
        name: str, subject_type_uuid: str, program_uuid: str
    ) -> str:
        """Create an encounter type for a program and subject type in Avni.

        Args:
            name: Name of the encounter type
            subject_type_uuid: Subject type UUID
            program_uuid: Program UUID
        """
        payload = {
            "name": name,
            "encounterEligibilityCheckRule": name,
            "loaded": True,
            "subjectTypeUuid": subject_type_uuid,
            "programUuid": program_uuid,
        }

        result = await make_avni_request("POST", "/web/encounterType", payload)

        if not result.success:
            return result.format_error("create encounter type")

        return format_creation_response("Encounter type", name, "uuid", result.data)
