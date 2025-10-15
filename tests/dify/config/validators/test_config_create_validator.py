"""
Specific validator for test-config-create.json structure.
This validator knows exactly what should be in the test create configuration.
"""

import logging
from typing import Dict, Any, List, Tuple

logger = logging.getLogger(__name__)


class TestConfigCreateValidator:
    """Validates the specific structure expected in test-config-create.json"""

    @staticmethod
    def validate_test_create_config(config: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """
        Validate that the generated config matches test-config-create.json structure exactly.

        Returns:
            Tuple of (is_valid, list_of_errors)
        """
        errors = []

        if not isinstance(config, dict):
            return False, ["Config must be a dictionary"]

        if "create" not in config:
            return False, ["Config must have 'create' key"]

        create_config = config["create"]
        if not isinstance(create_config, dict):
            return False, ["'create' must be a dictionary"]

        # Validate address level types - expecting exactly 3
        errors.extend(
            TestConfigCreateValidator._validate_crud_address_level_types(create_config)
        )

        # Validate locations - expecting exactly 3
        errors.extend(TestConfigCreateValidator._validate_crud_locations(create_config))

        # Validate catchments - expecting exactly 2
        errors.extend(
            TestConfigCreateValidator._validate_crud_catchments(create_config)
        )

        # Validate subject types - expecting exactly 2
        errors.extend(
            TestConfigCreateValidator._validate_crud_subject_types(create_config)
        )

        # Validate programs - expecting exactly 2
        errors.extend(TestConfigCreateValidator._validate_crud_programs(create_config))

        # Validate encounter types - expecting exactly 3
        errors.extend(
            TestConfigCreateValidator._validate_crud_encounter_types(create_config)
        )

        return len(errors) == 0, errors

    @staticmethod
    def _validate_crud_address_level_types(create_config: Dict[str, Any]) -> List[str]:
        """Validate specific address level types for CRUD test"""
        errors = []

        if "addressLevelTypes" not in create_config:
            return ["Missing 'addressLevelTypes' section"]

        addr_types = create_config["addressLevelTypes"]
        if not isinstance(addr_types, list):
            return ["'addressLevelTypes' must be a list"]

        if len(addr_types) != 3:
            errors.append(
                f"Expected exactly 3 addressLevelTypes, got {len(addr_types)}"
            )
            return errors

        # Expected structure (clean names):
        expected_types = [
            {"name": "State", "level": 3.0, "parentId": None},
            {"name": "District", "level": 2.0, "parentId": "id of State"},
            {"name": "Block", "level": 1.0, "parentId": "id of District"},
        ]

        for i, (actual, expected) in enumerate(zip(addr_types, expected_types)):
            if actual.get("name") != expected["name"]:
                errors.append(
                    f"addressLevelTypes[{i}] name should be '{expected['name']}', got '{actual.get('name')}'"
                )

            if actual.get("level") != expected["level"]:
                errors.append(
                    f"addressLevelTypes[{i}] level should be {expected['level']}, got {actual.get('level')}"
                )

            if actual.get("parentId") != expected["parentId"]:
                errors.append(
                    f"addressLevelTypes[{i}] parentId should be {expected['parentId']}, got {actual.get('parentId')}"
                )

            if actual.get("voided") is not False:
                errors.append(f"addressLevelTypes[{i}] voided should be false")

        return errors

    @staticmethod
    def _validate_crud_locations(create_config: Dict[str, Any]) -> List[str]:
        """Validate specific locations for CRUD test"""
        errors = []

        if "locations" not in create_config:
            return ["Missing 'locations' section"]

        locations = create_config["locations"]
        if not isinstance(locations, list):
            return ["'locations' must be a list"]

        if len(locations) != 3:
            errors.append(f"Expected exactly 3 locations, got {len(locations)}")
            return errors

        # Expected structure (clean names):
        expected_locations = [
            {"name": "Karnataka", "level": 3, "type": "State", "parents": []},
            {
                "name": "Bangalore",
                "level": 2,
                "type": "District",
                "parents": [{"id": "id of Karnataka"}],
            },
            {
                "name": "Electronic City",
                "level": 1,
                "type": "Block",
                "parents": [{"id": "id of Bangalore"}],
            },
        ]

        for i, (actual, expected) in enumerate(zip(locations, expected_locations)):
            if actual.get("name") != expected["name"]:
                errors.append(
                    f"locations[{i}] name should be '{expected['name']}', got '{actual.get('name')}'"
                )

            if actual.get("level") != expected["level"]:
                errors.append(
                    f"locations[{i}] level should be {expected['level']}, got {actual.get('level')}"
                )

            if actual.get("type") != expected["type"]:
                errors.append(
                    f"locations[{i}] type should be '{expected['type']}', got '{actual.get('type')}'"
                )

        return errors

    @staticmethod
    def _validate_crud_catchments(create_config: Dict[str, Any]) -> List[str]:
        """Validate specific catchments for CRUD test"""
        errors = []

        if "catchments" not in create_config:
            return ["Missing 'catchments' section"]

        catchments = create_config["catchments"]
        if not isinstance(catchments, list):
            return ["'catchments' must be a list"]

        if len(catchments) != 2:
            errors.append(f"Expected exactly 2 catchments, got {len(catchments)}")
            return errors

        # Expected structure:
        expected_catchments = [
            {
                "name": "Urban Catchment",
                "locationIds": ["id of Karnataka", "id of Bangalore"],
            },
            {"name": "Rural Catchment", "locationIds": ["id of Electronic City"]},
        ]

        for i, (actual, expected) in enumerate(zip(catchments, expected_catchments)):
            if actual.get("name") != expected["name"]:
                errors.append(
                    f"catchments[{i}] name should be '{expected['name']}', got '{actual.get('name')}'"
                )

        return errors

    @staticmethod
    def _validate_crud_subject_types(create_config: Dict[str, Any]) -> List[str]:
        """Validate specific subject types for CRUD test"""
        errors = []

        if "subjectTypes" not in create_config:
            return ["Missing 'subjectTypes' section"]

        subject_types = create_config["subjectTypes"]
        if not isinstance(subject_types, list):
            return ["'subjectTypes' must be a list"]

        if len(subject_types) != 2:
            errors.append(f"Expected exactly 2 subjectTypes, got {len(subject_types)}")
            return errors

        # Find Individual and Household subject types (clean names)
        individual_st = None
        household_st = None

        for st in subject_types:
            if st.get("name") == "Individual":
                individual_st = st
            elif st.get("name") == "Household":
                household_st = st

        # Validate Individual
        if individual_st is None:
            errors.append("Missing 'Individual' subject type")
        else:
            # Expected properties for Individual
            if individual_st.get("type") != "Person":
                errors.append("Individual type should be 'Person'")
            if individual_st.get("group") is not False:
                errors.append("Individual group should be false")
            if individual_st.get("household") is not False:
                errors.append("Individual household should be false")
            if individual_st.get("allowEmptyLocation") is not True:
                errors.append("Individual allowEmptyLocation should be true")
            if not individual_st.get("uuid"):
                errors.append("Individual must have uuid")

        # Validate Household
        if household_st is None:
            errors.append("Missing 'Household' subject type")
        else:
            # Expected properties for Household
            if household_st.get("type") != "Household":
                errors.append("Household type should be 'Household'")
            if household_st.get("group") is not True:
                errors.append("Household group should be true")
            if household_st.get("household") is not True:
                errors.append("Household household should be true")
            # Don't validate allowEmptyLocation and uniqueName since we didn't specify them in the message
            # The Dify workflow can set these to reasonable defaults
            if not household_st.get("uuid"):
                errors.append("Household must have uuid")

            # Validate group roles
            group_roles = household_st.get("groupRoles", [])
            if len(group_roles) != 2:
                errors.append(
                    f"Household should have exactly 2 group roles, got {len(group_roles)}"
                )
            else:
                # Check for Head of Household and Household Member roles
                head_role = None
                member_role = None

                for role in group_roles:
                    if role.get("role") == "Head of Household":
                        head_role = role
                    elif role.get("role") == "Household Member":
                        member_role = role

                if head_role is None:
                    errors.append("Missing 'Head of Household' role in Household")
                else:
                    if head_role.get("minimumNumberOfMembers") != 1:
                        errors.append(
                            "Head of Household minimumNumberOfMembers should be 1"
                        )
                    if head_role.get("maximumNumberOfMembers") != 1:
                        errors.append(
                            "Head of Household maximumNumberOfMembers should be 1"
                        )
                    if head_role.get("isPrimary") is not True:
                        errors.append("Head of Household isPrimary should be true")

                if member_role is None:
                    errors.append("Missing 'Household Member' role in Household")
                else:
                    if member_role.get("minimumNumberOfMembers") != 1:
                        errors.append(
                            "Household Member minimumNumberOfMembers should be 1"
                        )
                    if member_role.get("maximumNumberOfMembers") != 20:
                        errors.append(
                            "Household Member maximumNumberOfMembers should be 20"
                        )
                    if member_role.get("isPrimary") is not False:
                        errors.append("Household Member isPrimary should be false")

        return errors

    @staticmethod
    def _validate_crud_programs(create_config: Dict[str, Any]) -> List[str]:
        """Validate specific programs for CRUD test"""
        errors = []

        if "programs" not in create_config:
            return ["Missing 'programs' section"]

        programs = create_config["programs"]
        if not isinstance(programs, list):
            return ["'programs' must be a list"]

        if len(programs) != 2:
            errors.append(f"Expected exactly 2 programs, got {len(programs)}")
            return errors

        # Expected programs (clean names)
        expected_programs = [
            {
                "name": "Health Program",
                "colour": "#4CAF50",
                "programSubjectLabel": "Health Participant",
            },
            {
                "name": "Family Welfare",
                "colour": "#2196F3",
                "programSubjectLabel": "Family Unit",
            },
        ]

        # Find programs by name
        health_program = None
        family_program = None

        for prog in programs:
            if prog.get("name") == "Health Program":
                health_program = prog
            elif prog.get("name") == "Family Welfare":
                family_program = prog

        if health_program is None:
            errors.append("Missing 'Health Program'")
        else:
            if health_program.get("colour") != "#4CAF50":
                errors.append("Health Program colour should be '#4CAF50'")
            if health_program.get("programSubjectLabel") != "Health Participant":
                errors.append(
                    "Health Program programSubjectLabel should be 'Health Participant'"
                )
            if health_program.get("showGrowthChart") is not True:
                errors.append("Health Program showGrowthChart should be true")

        if family_program is None:
            errors.append("Missing 'Family Welfare'")
        else:
            if family_program.get("colour") != "#2196F3":
                errors.append("Family Welfare colour should be '#2196F3'")
            if family_program.get("programSubjectLabel") != "Family Unit":
                errors.append(
                    "Family Welfare programSubjectLabel should be 'Family Unit'"
                )

        return errors

    @staticmethod
    def _validate_crud_encounter_types(create_config: Dict[str, Any]) -> List[str]:
        """Validate specific encounter types for CRUD test"""
        errors = []

        if "encounterTypes" not in create_config:
            return ["Missing 'encounterTypes' section"]

        encounter_types = create_config["encounterTypes"]
        if not isinstance(encounter_types, list):
            return ["'encounterTypes' must be a list"]

        if len(encounter_types) != 3:
            errors.append(
                f"Expected exactly 3 encounterTypes, got {len(encounter_types)}"
            )
            return errors

        # Expected encounter types
        expected_encounters = [
            {"name": "Registration", "programUuid": None},
            {
                "name": "Health Checkup",
                "programUuid": "crud2468-acef-1357-9bdf-02468acef135",
            },
            {
                "name": "Family Survey",
                "programUuid": "crud3579-bdef-2468-acef-13579bdef246",
            },
        ]

        # Find encounters by name
        registration_enc = None
        health_checkup_enc = None
        family_survey_enc = None

        for enc in encounter_types:
            if enc.get("name") == "Registration":
                registration_enc = enc
            elif enc.get("name") == "Health Checkup":
                health_checkup_enc = enc
            elif enc.get("name") == "Family Survey":
                family_survey_enc = enc

        if registration_enc is None:
            errors.append("Missing 'Registration' encounter type")
        else:
            if registration_enc.get("programUuid") is not None:
                errors.append(
                    "Registration programUuid should be null (general encounter)"
                )

        if health_checkup_enc is None:
            errors.append("Missing 'Health Checkup' encounter type")
        else:
            if not health_checkup_enc.get("programUuid"):
                errors.append(
                    "Health Checkup must have programUuid (program encounter)"
                )

        if family_survey_enc is None:
            errors.append("Missing 'Family Survey' encounter type")
        else:
            if not family_survey_enc.get("programUuid"):
                errors.append("Family Survey must have programUuid (program encounter)")

        return errors
