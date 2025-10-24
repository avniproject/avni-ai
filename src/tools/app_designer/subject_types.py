import logging
from src.clients import AvniClient
from src.utils.session_context import log_payload
from src.utils.result_utils import (
    format_error_message,
    format_creation_response,
    format_update_response,
    format_deletion_response,
)
from src.schemas.subject_type_contract import (
    SubjectTypeContract,
    SubjectTypeUpdateContract,
    SubjectTypeDeleteContract,
)
from src.schemas.field_names import SubjectTypeFields
from src.core import tool_registry

logger = logging.getLogger(__name__)


async def create_subject_type(auth_token: str, contract: SubjectTypeContract) -> str:
    payload = {
        SubjectTypeFields.NAME.value: contract.name,
        SubjectTypeFields.UUID.value: contract.uuid,
        SubjectTypeFields.TYPE.value: contract.type,
        SubjectTypeFields.ACTIVE.value: contract.active,
        SubjectTypeFields.VOIDED.value: contract.voided,
        SubjectTypeFields.GROUP.value: contract.group,
        SubjectTypeFields.HOUSEHOLD.value: contract.household,
        SubjectTypeFields.ALLOW_EMPTY_LOCATION.value: contract.allowEmptyLocation,
        SubjectTypeFields.ALLOW_MIDDLE_NAME.value: contract.allowMiddleName,
        SubjectTypeFields.LAST_NAME_OPTIONAL.value: contract.lastNameOptional,
        SubjectTypeFields.ALLOW_PROFILE_PICTURE.value: contract.allowProfilePicture,
        SubjectTypeFields.UNIQUE_NAME.value: contract.uniqueName,
        SubjectTypeFields.DIRECTLY_ASSIGNABLE.value: contract.directlyAssignable,
        SubjectTypeFields.SHOULD_SYNC_BY_LOCATION.value: contract.shouldSyncByLocation,
        SubjectTypeFields.SETTINGS.value: {
            "displayRegistrationDetails": contract.settings.displayRegistrationDetails,
            "displayPlannedEncounters": contract.settings.displayPlannedEncounters,
        },
    }

    if contract.subjectSummaryRule is not None:
        payload[SubjectTypeFields.SUBJECT_SUMMARY_RULE.value] = (
            contract.subjectSummaryRule
        )
    if contract.programEligibilityCheckRule is not None:
        payload[SubjectTypeFields.PROGRAM_ELIGIBILITY_CHECK_RULE.value] = (
            contract.programEligibilityCheckRule
        )
    if contract.memberAdditionEligibilityCheckRule is not None:
        payload[SubjectTypeFields.MEMBER_ADDITION_ELIGIBILITY_CHECK_RULE.value] = (
            contract.memberAdditionEligibilityCheckRule
        )
    if contract.validFirstNameFormat is not None:
        payload[SubjectTypeFields.VALID_FIRST_NAME_FORMAT.value] = (
            contract.validFirstNameFormat
        )
    if contract.validMiddleNameFormat is not None:
        payload[SubjectTypeFields.VALID_MIDDLE_NAME_FORMAT.value] = (
            contract.validMiddleNameFormat
        )
    if contract.validLastNameFormat is not None:
        payload[SubjectTypeFields.VALID_LAST_NAME_FORMAT.value] = (
            contract.validLastNameFormat
        )
    if contract.iconFileS3Key is not None:
        payload[SubjectTypeFields.ICON_FILE_S3_KEY.value] = contract.iconFileS3Key
    if contract.syncRegistrationConcept1 is not None:
        payload[SubjectTypeFields.SYNC_REGISTRATION_CONCEPT1.value] = (
            contract.syncRegistrationConcept1
        )
    if contract.syncRegistrationConcept2 is not None:
        payload[SubjectTypeFields.SYNC_REGISTRATION_CONCEPT2.value] = (
            contract.syncRegistrationConcept2
        )
    if contract.nameHelpText is not None:
        payload[SubjectTypeFields.NAME_HELP_TEXT.value] = contract.nameHelpText
    if contract.registrationFormUuid is not None:
        payload[SubjectTypeFields.REGISTRATION_FORM_UUID.value] = (
            contract.registrationFormUuid
        )

    payload[SubjectTypeFields.GROUP_ROLES.value] = [
        {
            "subjectMemberName": role.subjectMemberName,
            "groupRoleUUID": role.groupRoleUUID,
            "groupSubjectTypeUUID": role.groupSubjectTypeUUID,
            "memberSubjectTypeUUID": role.memberSubjectTypeUUID,
            "role": role.role,
            "minimumNumberOfMembers": role.minimumNumberOfMembers,
            "maximumNumberOfMembers": role.maximumNumberOfMembers,
            "isPrimary": role.isPrimary,
            "voided": role.voided,
        }
        for role in contract.groupRoles
    ]

    log_payload("SubjectType CREATE payload:", payload)

    result = await AvniClient().call_avni_server(
        "POST", "/web/subjectType", auth_token, payload
    )

    if not result.success:
        return format_error_message(result, "create subject type")

    return format_creation_response(
        "Subject type", contract.name, SubjectTypeFields.UUID.value, result.data
    )


async def update_subject_type(
    auth_token: str, contract: SubjectTypeUpdateContract
) -> str:
    payload = {
        SubjectTypeFields.NAME.value: contract.name,
        SubjectTypeFields.TYPE.value: contract.type,
        SubjectTypeFields.ACTIVE.value: contract.active,
        SubjectTypeFields.VOIDED.value: contract.voided,
        SubjectTypeFields.GROUP.value: contract.group,
        SubjectTypeFields.HOUSEHOLD.value: contract.household,
        SubjectTypeFields.ALLOW_EMPTY_LOCATION.value: contract.allowEmptyLocation,
        SubjectTypeFields.ALLOW_MIDDLE_NAME.value: contract.allowMiddleName,
        SubjectTypeFields.LAST_NAME_OPTIONAL.value: contract.lastNameOptional,
        SubjectTypeFields.ALLOW_PROFILE_PICTURE.value: contract.allowProfilePicture,
        SubjectTypeFields.UNIQUE_NAME.value: contract.uniqueName,
        SubjectTypeFields.DIRECTLY_ASSIGNABLE.value: contract.directlyAssignable,
        SubjectTypeFields.SHOULD_SYNC_BY_LOCATION.value: contract.shouldSyncByLocation,
        SubjectTypeFields.SETTINGS.value: {
            "displayRegistrationDetails": contract.settings.displayRegistrationDetails,
            "displayPlannedEncounters": contract.settings.displayPlannedEncounters,
        },
    }

    if contract.subjectSummaryRule is not None:
        payload[SubjectTypeFields.SUBJECT_SUMMARY_RULE.value] = (
            contract.subjectSummaryRule
        )
    if contract.programEligibilityCheckRule is not None:
        payload[SubjectTypeFields.PROGRAM_ELIGIBILITY_CHECK_RULE.value] = (
            contract.programEligibilityCheckRule
        )
    if contract.memberAdditionEligibilityCheckRule is not None:
        payload[SubjectTypeFields.MEMBER_ADDITION_ELIGIBILITY_CHECK_RULE.value] = (
            contract.memberAdditionEligibilityCheckRule
        )
    if contract.validFirstNameFormat is not None:
        payload[SubjectTypeFields.VALID_FIRST_NAME_FORMAT.value] = (
            contract.validFirstNameFormat
        )
    if contract.validMiddleNameFormat is not None:
        payload[SubjectTypeFields.VALID_MIDDLE_NAME_FORMAT.value] = (
            contract.validMiddleNameFormat
        )
    if contract.validLastNameFormat is not None:
        payload[SubjectTypeFields.VALID_LAST_NAME_FORMAT.value] = (
            contract.validLastNameFormat
        )
    if contract.iconFileS3Key is not None:
        payload[SubjectTypeFields.ICON_FILE_S3_KEY.value] = contract.iconFileS3Key
    if contract.syncRegistrationConcept1 is not None:
        payload[SubjectTypeFields.SYNC_REGISTRATION_CONCEPT1.value] = (
            contract.syncRegistrationConcept1
        )
    if contract.syncRegistrationConcept2 is not None:
        payload[SubjectTypeFields.SYNC_REGISTRATION_CONCEPT2.value] = (
            contract.syncRegistrationConcept2
        )
    if contract.nameHelpText is not None:
        payload[SubjectTypeFields.NAME_HELP_TEXT.value] = contract.nameHelpText
    if contract.registrationFormUuid is not None:
        payload[SubjectTypeFields.REGISTRATION_FORM_UUID.value] = (
            contract.registrationFormUuid
        )

    payload[SubjectTypeFields.GROUP_ROLES.value] = [
        {
            "subjectMemberName": role.subjectMemberName,
            "groupRoleUUID": role.groupRoleUUID,
            "groupSubjectTypeUUID": role.groupSubjectTypeUUID,
            "memberSubjectTypeUUID": role.memberSubjectTypeUUID,
            "role": role.role,
            "minimumNumberOfMembers": role.minimumNumberOfMembers,
            "maximumNumberOfMembers": role.maximumNumberOfMembers,
            "isPrimary": role.isPrimary,
            "voided": role.voided,
        }
        for role in contract.groupRoles
    ]

    log_payload("SubjectType UPDATE payload:", payload)

    result = await AvniClient().call_avni_server(
        "PUT", f"/web/subjectType/{contract.id}", auth_token, payload
    )

    if not result.success:
        return format_error_message(result, "update subject type")

    return format_update_response(
        "Subject type", contract.name, SubjectTypeFields.ID.value, result.data
    )


async def delete_subject_type(
    auth_token: str, contract: SubjectTypeDeleteContract
) -> str:
    result = await AvniClient().call_avni_server(
        "DELETE", f"/web/subjectType/{contract.id}", auth_token
    )

    if not result.success:
        return format_error_message(result, "delete subject type")

    return format_deletion_response("Subject type", contract.id)


def register_subject_type_tools() -> None:
    tool_registry.register_tool(create_subject_type)
    tool_registry.register_tool(update_subject_type)
    tool_registry.register_tool(delete_subject_type)
