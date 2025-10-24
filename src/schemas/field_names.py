from enum import Enum

class AddressLevelTypeFields(Enum):

    NAME = "name"
    LEVEL = "level"
    PARENT_ID = "parentId"
    UUID = "uuid"
    VOIDED = "voided"
    ID = "id"


class LocationFields(Enum):

    NAME = "name"
    TITLE = "title"
    LEVEL = "level"
    TYPE = "type"
    PARENTS = "parents"
    PARENT_ID = "parentId"
    ID = "id"


class CatchmentFields(Enum):

    NAME = "name"
    LOCATION_IDS = "locationIds"
    DELETE_FAST_SYNC = "deleteFastSync"
    ID = "id"


class SubjectTypeFields(Enum):

    NAME = "name"
    UUID = "uuid"
    ID = "id"
    TYPE = "type"
    ACTIVE = "active"
    VOIDED = "voided"
    GROUP = "group"
    HOUSEHOLD = "household"
    ALLOW_EMPTY_LOCATION = "allowEmptyLocation"
    ALLOW_MIDDLE_NAME = "allowMiddleName"
    LAST_NAME_OPTIONAL = "lastNameOptional"
    ALLOW_PROFILE_PICTURE = "allowProfilePicture"
    UNIQUE_NAME = "uniqueName"
    DIRECTLY_ASSIGNABLE = "directlyAssignable"
    SHOULD_SYNC_BY_LOCATION = "shouldSyncByLocation"
    SETTINGS = "settings"
    SUBJECT_SUMMARY_RULE = "subjectSummaryRule"
    PROGRAM_ELIGIBILITY_CHECK_RULE = "programEligibilityCheckRule"
    MEMBER_ADDITION_ELIGIBILITY_CHECK_RULE = "memberAdditionEligibilityCheckRule"
    VALID_FIRST_NAME_FORMAT = "validFirstNameFormat"
    VALID_MIDDLE_NAME_FORMAT = "validMiddleNameFormat"
    VALID_LAST_NAME_FORMAT = "validLastNameFormat"
    ICON_FILE_S3_KEY = "iconFileS3Key"
    SYNC_REGISTRATION_CONCEPT1 = "syncRegistrationConcept1"
    SYNC_REGISTRATION_CONCEPT2 = "syncRegistrationConcept2"
    NAME_HELP_TEXT = "nameHelpText"
    GROUP_ROLES = "groupRoles"
    REGISTRATION_FORM_UUID = "registrationFormUuid"


class ProgramFields(Enum):

    NAME = "name"
    UUID = "uuid"
    ID = "id"
    COLOUR = "colour"
    SUBJECT_TYPE_UUID = "subjectTypeUuid"
    PROGRAM_SUBJECT_LABEL = "programSubjectLabel"
    ENROLMENT_SUMMARY_RULE = "enrolmentSummaryRule"
    ENROLMENT_ELIGIBILITY_CHECK_RULE = "enrolmentEligibilityCheckRule"
    ENROLMENT_ELIGIBILITY_CHECK_DECLARATIVE_RULE = (
        "enrolmentEligibilityCheckDeclarativeRule"
    )
    MANUAL_ELIGIBILITY_CHECK_REQUIRED = "manualEligibilityCheckRequired"
    SHOW_GROWTH_CHART = "showGrowthChart"
    MANUAL_ENROLMENT_ELIGIBILITY_CHECK_RULE = "manualEnrolmentEligibilityCheckRule"
    MANUAL_ENROLMENT_ELIGIBILITY_CHECK_DECLARATIVE_RULE = (
        "manualEnrolmentEligibilityCheckDeclarativeRule"
    )
    ALLOW_MULTIPLE_ENROLMENTS = "allowMultipleEnrolments"
    PROGRAM_ENROLMENT_FORM_UUID = "programEnrolmentFormUuid"
    PROGRAM_EXIT_FORM_UUID = "programExitFormUuid"
    ACTIVE = "active"
    VOIDED = "voided"


class EncounterTypeFields(Enum):

    NAME = "name"
    UUID = "uuid"
    ID = "id"
    SUBJECT_TYPE_UUID = "subjectTypeUuid"
    PROGRAM_UUID = "programUuid"
    ACTIVE = "active"
    VOIDED = "voided"
    IS_IMMUTABLE = "isImmutable"
    ENTITY_ELIGIBILITY_CHECK_RULE = "entityEligibilityCheckRule"
    ENTITY_ELIGIBILITY_CHECK_DECLARATIVE_RULE = "entityEligibilityCheckDeclarativeRule"


class UserFields(Enum):

    ID = "id"
    NAME = "name"
    USERNAME = "username"
    PHONE_NUMBER = "phoneNumber"
    EMAIL = "email"
    ORGANISATION_ID = "organisationId"
    CATCHMENT_ID = "catchmentId"
