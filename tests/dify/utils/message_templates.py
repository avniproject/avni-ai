"""
Hardcoded message templates for Dify configuration testing.
These messages are used to initiate conversations with the Dify workflow.
"""


def get_create_message() -> str:
    """Get hardcoded CREATE configuration message"""

    return """Hi, I need help setting up an Avni configuration for my organization.

I need address level types:
- State at level 3.0
- District at level 2.0 under State
- Block at level 1.0 under District

I need to track these subject types:
- Individual (type: Person)
- Household (type: Household) - this is a household type that should have 2 group roles:
  - Head of Household: 1-1 members (primary)
  - Household Member: 1-20 members

I need these programs:
- Health Program (color: #4CAF50) with participants called 'Health Participant' and growth chart enabled
- Family Welfare (color: #2196F3) with participants called 'Family Unit'

I need these locations:
- Karnataka (type: State, level: 3)
- Bangalore (type: District, level: 2)
- Electronic City (type: Block, level: 1)

I need these catchments:
- Urban Catchment covering locations: Karnataka, Bangalore
- Rural Catchment covering locations: Electronic City

I need these encounter types:
- Registration (general encounter)
- Health Checkup (program encounter)
- Family Survey (program encounter)

Can you help me create this configuration?"""


def get_update_message() -> str:
    """Get hardcoded UPDATE configuration message with existing context"""

    # Since we're testing with dummy auth token, provide existing config context
    existing_config = """My current configuration includes:

Address Level Types:
- State (level 3.0, parentId: null) 
- District (level 2.0, parentId: "id of State")
- Block (level 1.0, parentId: "id of District")

Locations:
- Karnataka (State, level 3, parents: [])
- Bangalore (District, level 2, parents: [{"id": "id of Karnataka"}]) 
- Electronic City (Block, level 1, parents: [{"id": "id of Bangalore"}])

Catchments:
- Urban Catchment (locationIds: ["id of Karnataka", "id of Bangalore"])
- Rural Catchment (locationIds: ["id of Electronic City"])

Subject Types:
- Individual (Person type, not household, uuid: "existing-individual-uuid")
- Household (Household type, with group roles: Head of Household 1-1 members, Household Member 1-20 members, uuid: "existing-household-uuid")

Programs:
- Health Program (#4CAF50, Health Participant, growth chart enabled, uuid: "existing-health-program-uuid")
- Family Welfare (#2196F3, Family Unit, uuid: "existing-family-welfare-uuid")

Encounter Types:
- Registration (general, uuid: "existing-registration-uuid")
- Health Checkup (program, uuid: "existing-health-checkup-uuid")
- Family Survey (program, uuid: "existing-family-survey-uuid")

"""

    update_request = """I need to update my existing Avni configuration with these changes:

Address Level Types:
- Rename State to "Updated State" (keep level 3.0, parentId: null)
- Rename District to "Updated District" (keep level 2.0, parentId: "id of Updated State") 
- Rename Block to "Updated Block" (keep level 1.0, parentId: "id of Updated District")

Locations:
- Update Karnataka to "Updated Karnataka" (keep as State, level 3)
- Update Bangalore to "Updated Bangalore" (keep as District, level 2, parentId: "id of Updated Karnataka")
- Update Electronic City to "Updated Electronic City" (keep as Block, level 1, parentId: "id of Updated Bangalore")

Catchments:
- Update Urban Catchment to "Updated Urban Catchment" (locationIds: ["id of Updated Karnataka", "id of Updated Bangalore"])
- Update Rural Catchment to "Updated Rural Catchment" (locationIds: ["id of Updated Electronic City"])

Subject Types:
- Update Individual to "Updated Individual" and enable middle names
- Update Household to "Updated Household"

Programs:
- Update Health Program to "Updated Health Program" with orange color (#FF9800) and multiple enrollments
- Update Family Welfare to "Updated Family Welfare" with purple color (#9C27B0)

Encounter Types:
- Update Registration to "Updated Registration" and make it immutable
- Update Health Checkup to "Updated Health Checkup" 
- Update Family Survey to "Updated Family Survey"

Can you help me update this configuration?"""

    return existing_config + update_request


def get_delete_message() -> str:
    """Get hardcoded DELETE configuration message"""

    return """Hi, I need to remove some items from my Avni configuration.

I need to delete these encounter types:
- Updated Family Survey

I need to delete these programs:
- Updated Family Welfare

I need to delete these subject types:
- Updated Household

I need to delete these catchments:
- Updated Rural Catchment
- Updated Urban Catchment

I need to delete these locations:
- Updated Electronic City
- Updated Bangalore
- Updated Karnataka

I need to delete these address level types:
- Updated Block
- Updated District
- Updated State

Can you help me remove these items safely?"""
