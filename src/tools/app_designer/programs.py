import logging
from src.clients import AvniClient
from src.utils.session_context import log_payload
from src.utils.result_utils import (
    format_error_message,
    format_empty_message,
    format_creation_response,
    format_update_response,
    format_deletion_response,
)
from src.schemas.program_contract import (
    ProgramContract,
    ProgramUpdateContract,
    ProgramDeleteContract,
)
from src.schemas.field_names import ProgramFields
from src.core import tool_registry

logger = logging.getLogger(__name__)


async def create_program(auth_token: str, contract: ProgramContract) -> str:
    payload = {
        ProgramFields.NAME.value: contract.name,
        ProgramFields.UUID.value: contract.uuid,
        ProgramFields.COLOUR.value: contract.colour,
        ProgramFields.SUBJECT_TYPE_UUID.value: contract.subjectTypeUuid,
        ProgramFields.ACTIVE.value: contract.active,
        ProgramFields.VOIDED.value: contract.voided,
        ProgramFields.MANUAL_ELIGIBILITY_CHECK_REQUIRED.value: contract.manualEligibilityCheckRequired,
        ProgramFields.SHOW_GROWTH_CHART.value: contract.showGrowthChart,
        ProgramFields.ALLOW_MULTIPLE_ENROLMENTS.value: contract.allowMultipleEnrolments,
    }

    if contract.programSubjectLabel is not None:
        payload[ProgramFields.PROGRAM_SUBJECT_LABEL.value] = (
            contract.programSubjectLabel
        )
    if contract.enrolmentSummaryRule is not None:
        payload[ProgramFields.ENROLMENT_SUMMARY_RULE.value] = (
            contract.enrolmentSummaryRule
        )
    if contract.enrolmentEligibilityCheckRule is not None:
        payload[ProgramFields.ENROLMENT_ELIGIBILITY_CHECK_RULE.value] = (
            contract.enrolmentEligibilityCheckRule
        )
    if contract.enrolmentEligibilityCheckDeclarativeRule is not None:
        payload[ProgramFields.ENROLMENT_ELIGIBILITY_CHECK_DECLARATIVE_RULE.value] = (
            contract.enrolmentEligibilityCheckDeclarativeRule
        )
    if contract.manualEnrolmentEligibilityCheckDeclarativeRule is not None:
        payload[
            ProgramFields.MANUAL_ENROLMENT_ELIGIBILITY_CHECK_DECLARATIVE_RULE.value
        ] = contract.manualEnrolmentEligibilityCheckDeclarativeRule

    if contract.programEnrolmentFormUuid is not None:
        payload[ProgramFields.PROGRAM_ENROLMENT_FORM_UUID.value] = (
            contract.programEnrolmentFormUuid
        )
    if contract.programExitFormUuid is not None:
        payload[ProgramFields.PROGRAM_EXIT_FORM_UUID.value] = (
            contract.programExitFormUuid
        )

    payload[ProgramFields.MANUAL_ENROLMENT_ELIGIBILITY_CHECK_RULE.value] = (
        str(contract.manualEnrolmentEligibilityCheckRule)
        if isinstance(contract.manualEnrolmentEligibilityCheckRule, bool)
        else contract.manualEnrolmentEligibilityCheckRule
    )

    log_payload("Program CREATE payload:", payload)

    result = await AvniClient().call_avni_server(
        "POST", "/web/program", auth_token, payload
    )

    if not result.success:
        return format_error_message(result, "create program")

    return format_creation_response(
        "Program", contract.name, ProgramFields.UUID.value, result.data
    )


async def update_program(auth_token: str, contract: ProgramUpdateContract) -> str:
    payload = {
        ProgramFields.NAME.value: contract.name,
        ProgramFields.COLOUR.value: contract.colour,
        ProgramFields.SUBJECT_TYPE_UUID.value: contract.subjectTypeUuid,
        ProgramFields.ACTIVE.value: contract.active,
        ProgramFields.VOIDED.value: contract.voided,
        ProgramFields.MANUAL_ELIGIBILITY_CHECK_REQUIRED.value: contract.manualEligibilityCheckRequired,
        ProgramFields.SHOW_GROWTH_CHART.value: contract.showGrowthChart,
        ProgramFields.ALLOW_MULTIPLE_ENROLMENTS.value: contract.allowMultipleEnrolments,
    }

    if contract.programSubjectLabel is not None:
        payload[ProgramFields.PROGRAM_SUBJECT_LABEL.value] = (
            contract.programSubjectLabel
        )
    if contract.enrolmentSummaryRule is not None:
        payload[ProgramFields.ENROLMENT_SUMMARY_RULE.value] = (
            contract.enrolmentSummaryRule
        )
    if contract.enrolmentEligibilityCheckRule is not None:
        payload[ProgramFields.ENROLMENT_ELIGIBILITY_CHECK_RULE.value] = (
            contract.enrolmentEligibilityCheckRule
        )
    if contract.enrolmentEligibilityCheckDeclarativeRule is not None:
        payload[ProgramFields.ENROLMENT_ELIGIBILITY_CHECK_DECLARATIVE_RULE.value] = (
            contract.enrolmentEligibilityCheckDeclarativeRule
        )
    if contract.manualEnrolmentEligibilityCheckDeclarativeRule is not None:
        payload[
            ProgramFields.MANUAL_ENROLMENT_ELIGIBILITY_CHECK_DECLARATIVE_RULE.value
        ] = contract.manualEnrolmentEligibilityCheckDeclarativeRule
    if contract.programEnrolmentFormUuid is not None:
        payload[ProgramFields.PROGRAM_ENROLMENT_FORM_UUID.value] = (
            contract.programEnrolmentFormUuid
        )
    if contract.programExitFormUuid is not None:
        payload[ProgramFields.PROGRAM_EXIT_FORM_UUID.value] = (
            contract.programExitFormUuid
        )

    payload[ProgramFields.MANUAL_ENROLMENT_ELIGIBILITY_CHECK_RULE.value] = (
        str(contract.manualEnrolmentEligibilityCheckRule)
        if isinstance(contract.manualEnrolmentEligibilityCheckRule, bool)
        else contract.manualEnrolmentEligibilityCheckRule
    )

    log_payload("Program UPDATE payload:", payload)

    result = await AvniClient().call_avni_server(
        "PUT", f"/web/program/{contract.id}", auth_token, payload
    )

    if not result.success:
        return format_error_message(result, "update program")

    return format_update_response(
        "Program", contract.name, ProgramFields.ID.value, result.data
    )


async def delete_program(auth_token: str, contract: ProgramDeleteContract) -> str:
    result = await AvniClient().call_avni_server(
        "DELETE", f"/web/program/{contract.id}", auth_token
    )

    if not result.success:
        return format_error_message(result, "delete program")

    return format_deletion_response("Program", contract.id)


def register_program_tools() -> None:
    tool_registry.register_tool(create_program)
    tool_registry.register_tool(update_program)
    tool_registry.register_tool(delete_program)
