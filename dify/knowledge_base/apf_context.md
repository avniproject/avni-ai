# APF Odisha Implementation - Knowledge Base

## Overview

This knowledge base documents the complete APF (Azim Premji Foundation) Odisha implementation in Avni. This implementation focuses on maternal and child nutrition tracking, including pregnancy monitoring, child growth monitoring, NRC (Nutrition Rehabilitation Center) management, and quality response team (QRT) interventions.

## Table of Contents

1. [Subject Types](#subject-types)
2. [Programs](#programs)
3. [Encounter Types](#encounter-types)
4. [Address Level Types](#address-level-types)
5. [Form Mappings](#form-mappings)
6. [Forms Structure](#forms-structure)
7. [Key Concepts](#key-concepts)
8. [Workflows](#workflows)

---

## Subject Types

The implementation uses 6 subject types to model different entities:

### 1. Individual (Person)
- **UUID**: `ec69af69-8fd2-40b3-b429-025504c18a01`
- **Type**: Person
- **Purpose**: Main subject type for beneficiaries (pregnant women, children, individuals)
- **Key Features**:
  - Subject summary rule displays "To be monitored by QRT" status
  - Sync registration concept enabled
  - Location-based syncing enabled
  - Used for pregnancy and child program enrollments

### 2. Household (Group)
- **UUID**: `f2ffc396-2acc-4e97-af90-d9585eb2df75`
- **Type**: Group
- **Purpose**: Groups individuals into household units
- **Key Features**:
  - Group subject type
  - Location-based syncing enabled

### 3. AWC Profile (Individual)
- **UUID**: `eb642a9c-ae1b-4247-81ba-87800227d981`
- **Type**: Individual
- **Purpose**: Anganwadi Center profile tracking
- **Key Features**:
  - Used for supervisor monitoring encounters
  - Location-based syncing enabled

### 4. Village Profile (Individual)
- **UUID**: `bfc36f13-831c-445a-ada9-5696840f8cee`
- **Type**: Individual
- **Purpose**: Village-level data collection
- **Key Features**:
  - Location-based syncing enabled

### 5. TIMS for Poshan Sathi (User)
- **UUID**: `542e9019-04c8-4aec-9801-26a7be8a39ad`
- **Type**: User
- **Purpose**: User tracking for Poshan Sathi field workers
- **Key Features**:
  - Empty location allowed
  - No location-based syncing
  - Used for training encounters

### 6. AWC area inputs (Voided)
- **UUID**: `387cc2ab-3981-4ffd-85fa-faf9fdb04150`
- **Status**: Voided
- **Note**: Historical subject type, no longer in use

---

## Programs

The implementation has 2 active programs:

### 1. Pregnancy Program
- **UUID**: `7e905823-0326-4f67-8bc3-84cc4bb9f407`
- **Color**: Purple (`#8b008b`)
- **Eligibility**: Females aged 10+ years
- **Enrolment Summary**:
  - Displays "To be monitored by QRT" status
  - Shows high risk conditions
  - Summary only shown before delivery encounter completion
- **Key Encounters**:
  - ANC (Antenatal Care)
  - PNC (Postnatal Care)
  - Delivery
  - PW Home Visit
  - QRT PW (Quality Response Team for Pregnant Women)
  - Supervisor PW Home Visit
  - Supervisor VHSND Visit

### 2. Child Program
- **UUID**: `5538d0f1-194c-4055-9311-dcc0239fe1ce`
- **Color**: Orange (`#ff8c00`)
- **Eligibility**: Children aged 5 years or below
- **Growth Chart**: Enabled
- **Enrolment Summary**:
  - To be monitored by QRT status
  - Weight for age z-score, grade, and status
  - Height for age z-score, grade, and status
  - Weight for height z-score and status
  - BMI for age z-score and status
  - MUAC (Mid-Upper Arm Circumference)
- **Key Encounters**:
  - Growth Monitoring
  - Child Home Visit
  - NRC Admission
  - NRC Discharge
  - QRT Child
  - Medical Facilitation for Poshan Sathi
  - Medical Facilitation for QRT
  - Supervisor Child Home Visit
  - Supervisor Growth Monitoring Session

---

## Encounter Types

### Pregnancy Program Encounters

#### ANC (Antenatal Care)
- **UUID**: `25c6c7d8-d779-43e2-b53e-d1cbf92f3865`
- **Eligibility**: Age in days < 0 (i.e., pregnant)
- **Purpose**: Regular antenatal checkups during pregnancy

#### PNC (Postnatal Care)
- **UUID**: `aaaa9032-072c-4662-acb1-f651e6b67946`
- **Eligibility**: Date of delivery must be recorded
- **Purpose**: Postnatal checkups after delivery

#### Delivery
- **UUID**: `0ffc5fe0-eb12-40e2-b707-65ef26efc70e`
- **Eligibility**: Always false (scheduled/planned encounter)
- **Purpose**: Record delivery details

#### PW Home Visit
- **UUID**: `c901cd8b-fcc3-44c6-bbd2-848e8466e00e`
- **Purpose**: Home visits for pregnant women

#### QRT PW
- **UUID**: `231e81b3-8f1c-474a-bc2e-4398006e2579`
- **Purpose**: Quality Response Team interventions for high-risk pregnant women

#### Supervisor PW Home Visit
- **UUID**: `ca5a7ad8-0705-4d50-9086-4aca7f1efc9d`
- **Purpose**: Supervisor monitoring of PW home visits

#### Supervisor VHSND Visit
- **UUID**: `ce028f08-b09a-43d5-8924-2313700a841b`
- **Purpose**: Supervisor monitoring of Village Health, Sanitation and Nutrition Day

### Child Program Encounters

#### Growth Monitoring
- **UUID**: `5c68b335-0456-4111-ae77-4697cb61cd56`
- **Purpose**: Regular growth monitoring sessions for children
- **Key Measurements**: Weight, height, MUAC, z-scores

#### Child Home Visit
- **UUID**: `91719f2a-0312-41ad-80ce-9e010f193e0b`
- **Purpose**: Home visits for children

#### NRC Admission
- **UUID**: `ad2fc18b-c8e8-4b49-bc8e-61b457983998`
- **Purpose**: Admission to Nutrition Rehabilitation Center

#### NRC Discharge
- **UUID**: `fd529739-fc2f-493d-a557-e13cbe071d09`
- **Purpose**: Discharge from Nutrition Rehabilitation Center

#### QRT Child
- **UUID**: `24474001-f69a-433f-8a65-737c1662bbca`
- **Purpose**: Quality Response Team interventions for high-risk children

#### Medical Facilitation for Poshan Sathi
- **UUID**: `362996b5-aaef-4474-b037-03a7f52df5ce`
- **Purpose**: Medical facilitation tracking for Poshan Sathi workers

#### Medical Facilitation for QRT
- **UUID**: `7cd16d3f-ecc1-442d-8f77-9125edb31a4a`
- **Purpose**: Medical facilitation tracking for QRT team

#### Supervisor Child Home Visit
- **UUID**: `8163b4ff-c075-4a5e-862c-514288562c3a`
- **Purpose**: Supervisor monitoring of child home visits

#### Supervisor Growth Monitoring Session
- **UUID**: `3cb520a0-6ac1-44b4-89cd-a2c3158a606c`
- **Purpose**: Supervisor monitoring of growth monitoring sessions

### User/Training Encounters

#### Training
- **UUID**: `039b6488-5395-4fda-989e-d3b00760c5bd`
- **Subject Type**: TIMS for Poshan Sathi
- **Eligibility**: Complex logic to prevent multiple trainings in same month
- **Purpose**: Track training sessions for field workers

#### Training Completion
- **UUID**: `e8ec379d-8cc7-4617-a74e-264854b7139d`
- **Purpose**: Mark training completion

### AWC Encounters

#### AWC inputs
- **UUID**: `818786a0-eb92-413d-85ab-c7fff52a5cbb`
- **Eligibility**: Only if no previous encounter exists
- **Purpose**: One-time AWC data collection

---

## Address Level Types

The implementation uses a 6-level location hierarchy:

### Level 6: Project/Block
- **UUID**: `d4714a9a-9d64-4796-b550-ae0bae6d502d`
- **Level**: 6.0
- **Parent**: None (top level)

### Level 5: Sector
- **UUID**: `94f8c5d6-dec7-447d-ade1-75145e661397`
- **Level**: 5.0
- **Parent**: Project/Block

### Level 4: AWC
- **UUID**: `0a997062-ff85-464d-b51f-95d1fd9ba8a7`
- **Level**: 4.0
- **Parent**: Sector

### Level 3: Block
- **UUID**: `b8ad2233-c9fa-4d22-b355-c0c7c1757786`
- **Level**: 3.0
- **Parent**: None (parallel hierarchy)

### Level 2: GP (Gram Panchayat)
- **UUID**: `a55fde74-637a-450a-87e0-1b88653bbe85`
- **Level**: 2.0
- **Parent**: Block

### Level 1: Village/Hamlet
- **UUID**: `55cb37d1-9dfa-440a-8410-2eb2def15dad`
- **Level**: 1.0
- **Parent**: GP

**Note**: The implementation has two parallel hierarchies:
1. Project/Block → Sector → AWC (administrative/program structure)
2. Block → GP → Village/Hamlet (geographical structure)

---

## Form Mappings

The implementation has 36 active form mappings (excluding voided ones):

### Registration Forms

1. **Individual Registration**
   - Form UUID: `a3ec1c7a-e561-4604-84c0-271511427a87`
   - Subject Type: Individual
   - Form Type: IndividualProfile

2. **Household Registration**
   - Form UUID: `58773442-5d9b-4369-9c94-97331b09c19c`
   - Subject Type: Household
   - Form Type: IndividualProfile

3. **AWC Profile**
   - Form UUID: `573820dd-a1e2-4087-a266-c65a9af08584`
   - Subject Type: AWC Profile
   - Form Type: IndividualProfile

4. **Village Profile**
   - Form UUID: `abe9d333-996c-4487-9cd9-12a812643490`
   - Subject Type: Village Profile
   - Form Type: IndividualProfile

### Program Enrolment Forms

5. **Pregnancy Enrolment**
   - Form UUID: `73473142-3bc9-48f4-b70b-d54a710b01f5`
   - Program: Pregnancy
   - Form Type: ProgramEnrolment

6. **Child Enrolment**
   - Form UUID: `4a35c83e-f7a0-4181-b839-7983923a914d`
   - Program: Child
   - Form Type: ProgramEnrolment

### Program Exit Forms

7. **Pregnancy Exit**
   - Form UUID: `3f695853-4661-43c5-a0b6-e2112ecea266`
   - Program: Pregnancy
   - Form Type: ProgramExit

8. **Child Exit**
   - Form UUID: `76ba0500-e9fa-4fa0-aae3-c4b88a2d2554`
   - Program: Child
   - Form Type: ProgramExit

### Pregnancy Program Encounter Forms

9. **ANC**
   - Form UUID: `de627061-b255-4cdd-bf82-db02390fa406`
   - Encounter Type: ANC
   - Form Type: ProgramEncounter

10. **ANC Encounter Cancellation**
    - Form UUID: `a9411e3b-0122-4a09-a892-960a556cff33`
    - Form Type: ProgramEncounterCancellation

11. **PNC Encounter**
    - Form UUID: `7fc029bc-9fd9-44d9-a176-5022dc7829fd`
    - Encounter Type: PNC
    - Form Type: ProgramEncounter

12. **PNC Encounter Cancellation**
    - Form UUID: `17cbfc90-56ff-4726-9e0a-9ba5267855d0`
    - Form Type: ProgramEncounterCancellation

13. **Delivery Encounter**
    - Form UUID: `d0121564-50e3-445c-b909-439d0cd74ef0`
    - Encounter Type: Delivery
    - Form Type: ProgramEncounter

14. **Delivery Encounter Cancellation**
    - Form UUID: `44c4a4bf-e992-4c35-ba9e-1aa1396f78b0`
    - Form Type: ProgramEncounterCancellation

15. **PW Home Visit**
    - Form UUID: `f8da4ed8-d2ae-48e0-82ea-0dcff67bdaf6`
    - Encounter Type: PW Home Visit
    - Form Type: ProgramEncounter

16. **PW Home Visit Cancellation**
    - Form UUID: `a30962ee-0929-4568-b3d3-12762792365c`
    - Form Type: ProgramEncounterCancellation

17. **QRT PW**
    - Form UUID: `d2680f33-cfff-4e3d-95b1-4e68d7996c6d`
    - Encounter Type: QRT PW
    - Form Type: ProgramEncounter

18. **QRT PW Encounter Cancellation**
    - Form UUID: `aab0e6b2-b297-4d5e-b0fd-c4121b05e3fa`
    - Form Type: ProgramEncounterCancellation

19. **Supervisor PW Home Visit Encounter**
    - Form UUID: `e246ff37-dc99-4b55-b0d8-163c0a3adac8`
    - Encounter Type: Supervisor PW Home Visit
    - Form Type: ProgramEncounter

20. **Supervisor PW Home Visit Encounter Cancellation**
    - Form UUID: `e0b6ba6c-5adf-4049-aff8-315e270163c0`
    - Form Type: ProgramEncounterCancellation

### Child Program Encounter Forms

21. **Growth Monitoring**
    - Form UUID: `847c45ab-9b06-470a-9229-7e848ad597b6`
    - Encounter Type: Growth Monitoring
    - Form Type: ProgramEncounter

22. **Growth Monitoring Encounter Cancellation**
    - Form UUID: `7111e360-8815-4b34-aef9-be4f084c7f81`
    - Form Type: ProgramEncounterCancellation

23. **Child Home Visit**
    - Form UUID: `ad1c49aa-6297-4e42-99f1-ede058cc2872`
    - Encounter Type: Child Home Visit
    - Form Type: ProgramEncounter

24. **Child Home Visit cancellation**
    - Form UUID: `29df0a40-59f6-4ef7-853d-7a378655c170`
    - Form Type: ProgramEncounterCancellation

25. **NRC Admission**
    - Form UUID: `dc4d7dc9-3ae8-429a-afe5-bf2a560fca53`
    - Encounter Type: NRC Admission
    - Form Type: ProgramEncounter

26. **NRC Admission Encounter Cancellation**
    - Form UUID: `79620e77-5ab8-46b7-8fb6-d72e83edad61`
    - Form Type: ProgramEncounterCancellation

27. **NRC Discharge**
    - Form UUID: `081750b9-55cc-43c5-9bce-4f617e71ab1e`
    - Encounter Type: NRC Discharge
    - Form Type: ProgramEncounter

28. **NRC Encounter Cancellation**
    - Form UUID: `cae3fba7-6ee1-4e72-91be-03434ff6687a`
    - Form Type: ProgramEncounterCancellation

29. **QRT Child**
    - Form UUID: `d8c3e537-284e-47a3-8c1f-013c37f301bd`
    - Encounter Type: QRT Child
    - Form Type: ProgramEncounter

30. **QRT Child Encounter Cancellation**
    - Form UUID: `35261d15-1645-4a09-821f-feddabb572a5`
    - Form Type: ProgramEncounterCancellation

31. **Medical Facilitation for Poshan Sathi**
    - Form UUID: `acbfb98e-0317-4cc9-8bfa-fe2aecd8960c`
    - Encounter Type: Medical Facilitation for Poshan Sathi
    - Form Type: ProgramEncounter

32. **Medical Facilitation for Poshan Sathi Encounter Cancellation**
    - Form UUID: `7fb48e7d-74f8-4733-b978-87e421c77bb9`
    - Form Type: ProgramEncounterCancellation

33. **Medical Facilitation for QRT Encounter**
    - Form UUID: `a3db2137-b6d0-411e-bb38-09ad4f8cc2e1`
    - Encounter Type: Medical Facilitation for QRT
    - Form Type: ProgramEncounter

34. **Medical Facilitation for QRT Encounter Cancellation**
    - Form UUID: `b2cdb6fd-70ff-47e3-8835-df6757a7d7cd`
    - Form Type: ProgramEncounterCancellation

35. **Supervisor Child Home visit Encounter**
    - Form UUID: `b2cfdafb-e5c6-4f3a-9ee1-31ffe59cda38`
    - Encounter Type: Supervisor Child Home visit
    - Form Type: ProgramEncounter

36. **Supervisor Child Home visit Encounter Cancellation**
    - Form UUID: `897bacca-b8dc-4435-abe8-016b0a7d4fc8`
    - Form Type: ProgramEncounterCancellation

### AWC/Supervisor Encounter Forms

37. **Supervisor VHSND Visit Encounter**
    - Form UUID: `de3157ed-87ea-4190-a9dd-c21f22a54286`
    - Subject Type: AWC Profile
    - Encounter Type: Supervisor VHSND Visit
    - Form Type: Encounter

38. **Supervisor VHSND Visit cancellation**
    - Form UUID: `9539504c-979d-4201-80e5-a65a7e10a847`
    - Form Type: IndividualEncounterCancellation

39. **Supervisor Growth Monitoring Session Encounter**
    - Form UUID: `06500e9b-f8d2-4169-9e24-29ad9de47f7d`
    - Subject Type: AWC Profile
    - Encounter Type: Supervisor Growth Monitoring Session
    - Form Type: Encounter

40. **Supervisor Growth Monitoring Encounter Cancellation**
    - Form UUID: `7a94ae08-8e57-4872-8a44-712f96f0cf77`
    - Form Type: IndividualEncounterCancellation

### Training Forms

41. **Training**
    - Form UUID: `82b377ed-7154-4994-8922-5c12886d0376`
    - Subject Type: TIMS for Poshan Sathi
    - Encounter Type: Training
    - Form Type: Encounter

42. **Training Encounter Cancellation**
    - Form UUID: `854bac40-f1aa-4909-9d91-1e6bf43946c8`
    - Form Type: IndividualEncounterCancellation

43. **Training Completion**
    - Form UUID: `3e3266ae-b09d-4145-9bbb-4a6bc50e3492`
    - Encounter Type: Training Completion
    - Form Type: Encounter

44. **Training Completion Cancellation**
    - Form UUID: `e6fcc84a-2c5d-4c0d-8c7b-90fa9f992d67`
    - Form Type: IndividualEncounterCancellation

---

## Forms Structure

The implementation contains 70 form JSON files in the `/forms/` directory:

### Registration Forms (4 files)
- Individual Registration.json
- Household Registration.json
- AWC Profile.json
- Village Profile (via Location Attribute Form.json)

### Pregnancy Program Forms (14 files)
- Pregnancy Enrolment (via Checklist Form.json)
- Pregnancy Exit (inferred)
- ANC.json
- ANC Encounter Cancellation.json
- PNC (via multiple files)
- Delivery Encounter.json
- Delivery Encounter Cancellation.json
- PW Home Visit (inferred)
- QRT PW (inferred)
- Supervisor PW Home Visit (inferred)

### Child Program Forms (18 files)
- Child Enrolment.json
- Child Exit.json
- Growth Monitoring.json
- Growth Monitoring Encounter Cancellation.json
- Child Home Visit.json
- Child Home Visit cancellation.json
- NRC Admission.json
- NRC Admission Encounter Cancellation.json
- NRC Discharge.json
- NRC Encounter Cancellation (multiple versions, some voided)
- QRT Child (inferred)
- Medical Facilitation for Poshan Sathi.json
- Medical Facilitation for Poshan Sathi Encounter Cancellation.json
- Medical Facilitation for QRT Encounter.json
- Medical Facilitation for QRT Encounter Cancellation.json
- Supervisor Child Home visit (inferred)

### AWC/Supervisor Forms (6 files)
- Supervisor VHSND Visit (inferred)
- Supervisor Growth Monitoring Session (inferred)
- AWC inputs (voided files)

### Training Forms (4 files)
- Training (inferred)
- Training Completion (inferred)
- Training Encounter Cancellation (inferred)
- Training Completion Cancellation (inferred)

### Voided Forms (24 files)
Multiple voided versions of forms marked with "(voided~XXXX)" suffix

---

## Key Concepts

The implementation uses 257KB of concept definitions covering:

### Anthropometric Measurements
- Weight (kg)
- Height (cm)
- MUAC (Mid-Upper Arm Circumference)
- Weight for age z-score, grade, status
- Height for age z-score, grade, status
- Weight for height z-score, status
- BMI for age z-score, status

### Pregnancy Tracking
- LMP (Last Menstrual Period)
- EDD (Expected Date of Delivery)
- Gravida, Para
- ANC visit number
- High risk conditions
- Pregnancy complications
- Delivery details
- Birth outcomes

### Child Health
- Immunization status
- Feeding practices
- Developmental milestones
- Illness tracking
- Referral status

### NRC Management
- Admission criteria
- Daily monitoring
- Discharge criteria
- Follow-up plans

### QRT Monitoring
- High risk identification
- "To be monitored by QRT" flag
- Intervention tracking
- Outcome monitoring

### Administrative
- Location details
- Worker information
- Training records
- Supervisor monitoring

---

## Workflows

### Pregnancy Workflow

1. **Registration**: Individual Registration → Female, Age 10+
2. **Enrolment**: Pregnancy Enrolment → Triggers ANC scheduling
3. **ANC Visits**: Regular ANC encounters (scheduled based on gestational age)
4. **High Risk Identification**: QRT flag set if high-risk conditions detected
5. **QRT Intervention**: QRT PW encounters for high-risk cases
6. **Home Visits**: PW Home Visits by field workers
7. **Supervisor Monitoring**: Supervisor PW Home Visit encounters
8. **Delivery**: Delivery encounter → Triggers PNC scheduling
9. **PNC Visits**: Postnatal care encounters
10. **Exit**: Pregnancy Exit (after completion or other reasons)

### Child Workflow

1. **Registration**: Individual Registration → Child
2. **Enrolment**: Child Enrolment → Triggers Growth Monitoring scheduling
3. **Growth Monitoring**: Regular growth monitoring sessions
4. **Anthropometry Assessment**: Weight, height, MUAC measurements
5. **Z-score Calculation**: Automatic calculation of nutritional indices
6. **High Risk Identification**: QRT flag for SAM/MAM cases
7. **NRC Admission**: For severe acute malnutrition cases
8. **NRC Monitoring**: Daily monitoring during NRC stay
9. **NRC Discharge**: Discharge planning and follow-up
10. **QRT Intervention**: QRT Child encounters for high-risk cases
11. **Home Visits**: Child Home Visits by field workers
12. **Supervisor Monitoring**: Supervisor Child Home Visit encounters
13. **Medical Facilitation**: Tracking medical referrals and facilitation
14. **Exit**: Child Exit (after age 5 or other reasons)

### Training Workflow

1. **User Registration**: TIMS for Poshan Sathi registration
2. **Training**: Training encounter (monthly limit enforced)
3. **Training Completion**: Training Completion encounter
4. **Monitoring**: Track training completion rates

### Supervisor Workflow

1. **AWC Profile**: Register AWC
2. **VHSND Monitoring**: Supervisor VHSND Visit encounters
3. **Growth Monitoring Session**: Supervisor Growth Monitoring Session encounters
4. **Home Visit Monitoring**: Supervisor PW/Child Home Visit encounters
5. **Quality Checks**: Monitor field worker performance

---

## Data Files

### Configuration Files
- **addressLevelTypes.json** (939 bytes): Location hierarchy definition
- **checklist.json** (36KB): Checklist configurations
- **concepts.json** (257KB): All concept definitions
- **encounterTypes.json** (8.6KB): Encounter type definitions
- **formMappings.json** (21KB): Form to entity mappings
- **groupDashboards.json** (22KB): Dashboard configurations
- **groupPrivilege.json** (225KB): User group privileges
- **groupRole.json** (419 bytes): Group role definitions
- **groups.json** (712 bytes): User group definitions
- **identifierSource.json** (594 bytes): ID generation configuration
- **individualRelation.json** (929 bytes): Relationship definitions
- **operationalEncounterTypes.json** (5.2KB): Operational encounter mappings
- **operationalPrograms.json** (512 bytes): Operational program mappings
- **operationalSubjectTypes.json** (1.3KB): Operational subject type mappings
- **organisationConfig.json** (2.6KB): Organization-level configuration
- **programs.json** (4.8KB): Program definitions
- **relationshipType.json** (2.3KB): Relationship type definitions
- **reportCard.json** (105KB): Report card definitions
- **reportDashboard.json** (45KB): Dashboard report definitions
- **subjectTypes.json** (4KB): Subject type definitions

### Translation Files
- **en.json**: English translations
- **od_IN.json**: Odia (Odisha language) translations

### Forms Directory
Contains 70 JSON files defining form structures, validations, and decision support rules

---

## Implementation Notes

### High Risk Monitoring
The implementation has a strong focus on identifying and monitoring high-risk cases:
- Pregnancy: High-risk conditions trigger QRT monitoring
- Child: SAM/MAM cases trigger QRT monitoring and potential NRC admission
- "To be monitored by QRT" flag is prominently displayed in summaries

### Growth Monitoring
Child program includes comprehensive growth monitoring:
- WHO growth standards (z-scores)
- Multiple anthropometric indices
- Growth chart visualization enabled
- Automatic nutritional status classification

### Supervisor Monitoring
Dedicated supervisor encounters for quality assurance:
- VHSND visit monitoring
- Growth monitoring session quality checks
- Home visit supervision
- Training completion tracking

### Location Hierarchy
Dual location hierarchy supports:
- Administrative structure (Project/Block → Sector → AWC)
- Geographical structure (Block → GP → Village/Hamlet)

### Data Syncing
- Most subject types use location-based syncing
- TIMS for Poshan Sathi allows empty location for flexibility
- Sync registration concept enabled for Individual subject type

---

## Technical Specifications

### Programming Rules
- Extensive use of JavaScript rules for:
  - Eligibility checks
  - Summary calculations
  - Visit scheduling
  - Validation logic
  - Decision support

### Form Features
- Approval workflow disabled for all forms
- Cancellation forms available for all encounter types
- Voided forms retained for historical reference

### Identifiers
- Custom identifier source configuration
- UUID-based entity identification
- Support for external system IDs

---

## Version History

This knowledge base documents the current state of the APF Odisha implementation. Voided entities indicate historical versions that have been superseded by newer implementations.

**Last Updated**: Based on reference data structure
**Implementation**: APF Odisha
**Platform**: Avni (OpenCHS)
**Focus Areas**: Maternal health, Child nutrition, NRC management, QRT interventions


---


# APF Odisha Implementation - Rules Knowledge Base

## Overview

This knowledge base documents all JavaScript rules from the APF Odisha implementation in Avni. These rules serve as reference examples for generating new rules based on user requirements.

**Total Rules Extracted:**
- **Form Element Rules**: 303 (visibility, value calculation, validation)
- **Validation Rules**: 22 (form-level validation)
- **Visit Schedule Rules**: 23 (encounter scheduling logic)
- **Decision Rules**: 10 (decision support and calculations)

---

## Table of Contents

1. [Rule Types and Structure](#rule-types-and-structure)
2. [Common Rule Patterns](#common-rule-patterns)
3. [Form Element Rules](#form-element-rules)
4. [Validation Rules](#validation-rules)
5. [Visit Schedule Rules](#visit-schedule-rules)
6. [Decision Rules](#decision-rules)
7. [Helper Functions and Libraries](#helper-functions-and-libraries)
8. [Best Practices](#best-practices)

---

## Rule Types and Structure

### 1. Form Element Rules
**Purpose**: Control visibility, set values, skip answers, and validate individual form elements

**Structure**:
```javascript
'use strict';
({params, imports}) => {
  const entity = params.entity; // programEncounter, programEnrolment, or individual
  const formElement = params.formElement;
  const moment = imports.moment;
  const _ = imports.lodash;
  
  let visibility = true;
  let value = null;
  let answersToSkip = [];
  let validationErrors = [];
  
  // Rule logic here
  
  return new imports.rulesConfig.FormElementStatus(
    formElement.uuid, 
    visibility, 
    value, 
    answersToSkip, 
    validationErrors
  );
};
```

### 2. Validation Rules
**Purpose**: Form-level validation across multiple fields

**Structure**:
```javascript
'use strict';
({params, imports}) => {
  const entity = params.entity;
  const validationResults = [];
  
  // Validation logic
  if (condition) {
    validationResults.push(imports.rulesConfig.createValidationError('Error message'));
  }
  
  return validationResults;
};
```

### 3. Visit Schedule Rules
**Purpose**: Schedule future encounters based on current encounter or enrolment

**Structure**:
```javascript
'use strict';
({params, imports}) => {
  const scheduleBuilder = new imports.rulesConfig.VisitScheduleBuilder({
    programEnrolment: params.entity
  });
  
  const moment = imports.moment;
  
  // Scheduling logic
  scheduleBuilder.add({
    name: 'Encounter Name',
    encounterType: 'Encounter Type',
    earliestDate: moment().add(7, 'days').toDate(),
    maxDate: moment().add(14, 'days').toDate()
  });
  
  return scheduleBuilder.getAllUnique('encounterType');
};
```

### 4. Decision Rules
**Purpose**: Calculate values and make decisions based on observations

**Structure**:
```javascript
'use strict';
({params, imports}) => {
  const entity = params.entity;
  const decisions = params.decisions;
  
  // Decision logic
  decisions.encounterDecisions.push({name: 'Concept Name', value: calculatedValue});
  decisions.enrolmentDecisions.push({name: 'Concept Name', value: calculatedValue});
  decisions.registrationDecisions.push({name: 'Concept Name', value: calculatedValue});
  
  return decisions;
};
```

---

## Common Rule Patterns

### Pattern 1: Conditional Visibility Based on Answer
**Use Case**: Show/hide field based on another field's answer

```javascript
'use strict';
({params, imports}) => {
  const programEncounter = params.entity;
  const formElement = params.formElement;
  let visibility = true;
  let value = null;
  let answersToSkip = [];
  let validationErrors = [];
  
  // Using RuleCondition
  const condition = new imports.rulesConfig.RuleCondition({programEncounter, formElement})
    .when.valueInEncounter("concept-uuid")
    .containsAnswerConceptName("answer-uuid")
    .matches();
  
  visibility = condition;
  
  return new imports.rulesConfig.FormElementStatus(
    formElement.uuid, visibility, value, answersToSkip, validationErrors
  );
};
```

**Example from ANC Form**:
```javascript
// Show "Specify other govt facility" only if "Any other govt facility" is selected
const condition11 = new imports.rulesConfig.RuleCondition({programEncounter, formElement})
  .when.valueInEncounter("6c44c836-8c53-4e7e-b8dd-c61aae7599fb")
  .containsAnswerConceptName("9c1de644-0982-474c-a7e9-28036ab376dd")
  .matches();

visibility = condition11;
```

### Pattern 2: Age-Based Visibility
**Use Case**: Show field only for specific age ranges

```javascript
'use strict';
({params, imports}) => {
  const programEnrolment = params.entity;
  const formElement = params.formElement;
  let visibility = true;
  
  // Age in months >= 6
  const condition = new imports.rulesConfig.RuleCondition({programEnrolment, formElement})
    .when.ageInMonths.greaterThanOrEqualTo(6)
    .matches();
  
  visibility = condition;
  
  return new imports.rulesConfig.FormElementStatus(
    formElement.uuid, visibility, null, [], []
  );
};
```

**Example from Child Enrolment**:
```javascript
// Show "Is the child exclusively breastfed till 6 months?" only if age >= 6 months
const condition11 = new imports.rulesConfig.RuleCondition({programEnrolment, formElement})
  .when.ageInMonths.greaterThanOrEqualTo(6)
  .matches();

visibility = condition11;
```

### Pattern 3: Previous Encounter Value Display
**Use Case**: Show value from previous encounter (read-only)

```javascript
'use strict';
({params, imports}) => {
  const programEncounter = params.entity;
  const formElement = params.formElement;
  const _ = imports.lodash;
  let visibility = true;
  let value = null;
  
  // Get all encounters of same type, ordered by date
  let encounterList = programEncounter.programEnrolment.encounters
    .filter(enc => enc.encounterType.name === 'Growth Monitoring' && 
                   enc.voided == false && 
                   enc.cancelDateTime == null);
  
  encounterList = _.orderBy(encounterList, ['earliestVisitDateTime'], ['asc']);
  
  const currentIndex = _.findIndex(encounterList, enc => enc.uuid === programEncounter.uuid);
  visibility = currentIndex > 0;
  
  if (visibility) {
    encounterList = encounterList.filter(enc => enc.encounterDateTime != null);
    const prevEncounter = encounterList[currentIndex - 1];
    
    if (prevEncounter && prevEncounter.encounterDateTime) {
      const prevValue = prevEncounter.getObservationValue('concept-uuid');
      if (prevValue) {
        value = prevValue;
      } else {
        visibility = false;
      }
    } else {
      visibility = false;
    }
  }
  
  return new imports.rulesConfig.FormElementStatus(
    formElement.uuid, visibility, value, [], []
  );
};
```

**Example from Growth Monitoring**:
```javascript
// Display height from previous month
let encounterList = programEncounter.programEnrolment.encounters
  .filter(enc => enc.encounterType.name === 'Growth Monitoring' && 
                 enc.voided == false && 
                 enc.cancelDateTime == null);

encounterList = _.orderBy(encounterList, ['earliestVisitDateTime'], ['asc']);

const currentIndex = _.findIndex(encounterList, enc => enc.uuid === programEncounter.uuid);
visibility = currentIndex > 0;

if (visibility) {
  encounterList = encounterList.filter(enc => enc.encounterDateTime != null);
  const prevEncounter = encounterList[currentIndex - 1];
  
  if (prevEncounter && prevEncounter.encounterDateTime) {
    const prevValue = prevEncounter.getObservationValue('346902c4-9938-4ba5-90d1-587f36f1ab92');
    if (prevValue) {
      value = prevValue;
    } else {
      visibility = false;
    }
  } else {
    visibility = false;
  }
}
```

### Pattern 4: Calculated Value (Auto-filled)
**Use Case**: Calculate and auto-fill value based on other observations

```javascript
'use strict';
({params, imports}) => {
  const programEncounter = params.entity;
  const formElement = params.formElement;
  const _ = imports.lodash;
  let value = null;
  
  let weight = programEncounter.findObservation("Weight of women");
  let height = programEncounter.programEnrolment.findObservation("Height of women");
  
  height = height && height.getValue();
  weight = weight && weight.getValue();
  
  if (_.isFinite(weight) && _.isFinite(height)) {
    value = ruleServiceLibraryInterfaceForSharingModules.common.calculateBMI(weight, height);
  }
  
  return new imports.rulesConfig.FormElementStatus(formElement.uuid, true, value);
};
```

**Example from ANC Form - BMI Calculation**:
```javascript
let weight = programEncounter.findObservation("Weight of women");
let height = programEncounter.programEnrolment.findObservation("Height of women");

height = height && height.getValue();
weight = weight && weight.getValue();
let value = '';

if (_.isFinite(weight) && _.isFinite(height)) {
  value = ruleServiceLibraryInterfaceForSharingModules.common.calculateBMI(weight, height);
}

return new imports.rulesConfig.FormElementStatus(formElement.uuid, true, value);
```

### Pattern 5: Validation with Error Messages
**Use Case**: Validate field value and show error message

```javascript
'use strict';
({params, imports}) => {
  const programEncounter = params.entity;
  const formElement = params.formElement;
  let visibility = true;
  let value = null;
  let validationErrors = [];
  
  const currentValue = programEncounter.getObservationValue('concept-uuid');
  
  if (currentValue > 50) {
    validationErrors.push("Should be 50, or less than 50");
  }
  
  return new imports.rulesConfig.FormElementStatus(
    formElement.uuid, visibility, value, [], validationErrors
  );
};
```

**Example from Growth Monitoring - Weight Validation**:
```javascript
const condition11 = new imports.rulesConfig.RuleCondition({programEncounter, formElement})
  .when.valueInEncounter("8b187dda-a88e-487a-981a-0e4cb6142904")
  .greaterThan(50)
  .matches();

if(condition11) {
  validationErrors.push("Should be 50, or less than 50");  
}
```

### Pattern 6: Cross-Field Validation
**Use Case**: Validate current value against previous encounter value

```javascript
'use strict';
({params, imports}) => {
  const programEncounter = params.entity;
  const formElement = params.formElement;
  const _ = imports.lodash;
  let validationErrors = [];
  
  let encounterList = programEncounter.programEnrolment.encounters
    .filter(enc => enc.encounterType.name === 'Growth Monitoring' && 
                   enc.voided == false && 
                   enc.cancelDateTime == null);
  
  encounterList = _.orderBy(encounterList, ['earliestVisitDateTime'], ['asc']);
  
  const currentIndex = _.findIndex(encounterList, enc => enc.uuid === programEncounter.uuid);  
  const prevEncounter = encounterList[currentIndex - 1]; 
  const prevValue = prevEncounter.getObservationValue('concept-uuid');  
  let currentObs = programEncounter.getObservationValue('concept-uuid');
  
  if (prevValue && prevValue != undefined) {
    if(prevValue > currentObs) {
      validationErrors.push("Current value cannot be less than previous value");
    }
    
    if ((currentObs - prevValue) > 10) {
      validationErrors.push("Increase of more than 10 since last visit is not allowed");
    }
  }
  
  return new imports.rulesConfig.FormElementStatus(
    formElement.uuid, true, null, [], validationErrors
  );
};
```

**Example from Growth Monitoring - Height Validation**:
```javascript
const prevEncounter = encounterList[currentIndex - 1]; 
const prevValue = prevEncounter.getObservationValue('346902c4-9938-4ba5-90d1-587f36f1ab92');  
let currentObs = programEncounter.getObservationValue('346902c4-9938-4ba5-90d1-587f36f1ab92');

if (prevValue && prevValue != undefined) {
  if(prevValue > currentObs) {
    validationErrors.push("Height in current growth monitoring session cant be less than previous growth monitoring session");
  }
  
  if ((currentObs - prevValue) > 10) {
    validationErrors.push("Height increase of more than 10 cm since last visit is not allowed. Please re-measure.");
  }
}
```

### Pattern 7: Location-Based Visibility
**Use Case**: Show field based on location properties

```javascript
'use strict';
({params, imports}) => {
  const programEncounter = params.entity;
  const formElement = params.formElement;
  const moment = imports.moment;
  let visibility = false;
  
  // Age condition
  let age = moment(programEncounter.earliestVisitDateTime)
    .diff(programEncounter.programEnrolment.individual.dateOfBirth, 'months');
  let condition11 = (age >= 36) && (age <= 60);
  
  // Location property condition
  let condition12 = false;
  const locationProperties = programEncounter.programEnrolment.individual
    .lowestAddressLevel.locationProperties;  
  
  if(locationProperties.length > 0) {
    const locationProperty = locationProperties.filter(prop => 
      prop.concept.name == 'PPK Village'
    );
    
    if(locationProperty.length == 1) {
      const valueJSON = locationProperty[0].valueJSON;
      const answer = JSON.parse(valueJSON).answer;
      if(answer == "8ebbf088-f292-483e-9084-7de919ce67b7") {
        condition12 = true;
      } 
    }
  }
  
  visibility = condition11 && condition12;
  
  return new imports.rulesConfig.FormElementStatus(
    formElement.uuid, visibility, null, [], []
  );
};
```

**Example from Growth Monitoring - PPK Village Check**:
```javascript
// Show "Is the child going to PPK?" only for age 36-60 months in PPK villages
let age = moment(programEncounter.earliestVisitDateTime)
  .diff(programEncounter.programEnrolment.individual.dateOfBirth,'months');

let condition11 = (age >= 36) && (age <= 60);
let condition12 = false;

const locationProperties = programEncounter.programEnrolment.individual
  .lowestAddressLevel.locationProperties;  

if(locationProperties.length > 0) {
  const locationProperty = locationProperties.filter(prop => 
    prop.concept.name == 'PPK Village'
  );
  
  if(locationProperty.length == 1) {
    const valueJSON = locationProperty[0].valueJSON;
    const answer = JSON.parse(valueJSON).answer;
    if(answer == "8ebbf088-f292-483e-9084-7de919ce67b7") {
      condition12 = true;
    } 
  }
}

visibility = condition11 && condition12;
```

### Pattern 8: Date Validation
**Use Case**: Prevent future dates or validate date ranges

```javascript
'use strict';
({params, imports}) => {
  const programEncounter = params.entity;
  const formElement = params.formElement;
  const moment = imports.moment;
  let validationErrors = [];
  
  const encounterDateTime = moment(programEncounter.encounterDateTime).startOf('day');
  let dateValue = programEncounter.getObservationValue("concept-uuid");
  
  if(dateValue) {
    dateValue = moment(dateValue).startOf('day');
    
    if(dateValue.isAfter(encounterDateTime)) {
      validationErrors.push("Invalid date: Do not enter future date.");
    }
  }
  
  return new imports.rulesConfig.FormElementStatus(
    formElement.uuid, true, null, [], validationErrors
  );
};
```

**Example from ANC - USG Date Validation**:
```javascript
const encounterDateTime = moment(programEncounter.encounterDateTime).startOf('day');
let usgDate = programEncounter.getObservationValue("590d73d0-0547-4e14-89d7-c66c98a07b87");

if(usgDate) {
  usgDate = moment(usgDate).startOf('day');
  if(usgDate.isAfter(encounterDateTime)) {
    validationErrors.push("Invalid date: Do not enter future date.");
  }
}
```

### Pattern 9: Growth Faltering Detection
**Use Case**: Compare values across multiple previous encounters

```javascript
'use strict';
({params, imports}) => {
  const programEncounter = params.entity;
  const formElement = params.formElement;
  const _ = imports.lodash;
  let value = null;
  
  const encounters = programEncounter.programEnrolment.getEncountersOfType('Growth Monitoring');
  
  // Get previous 2 encounters
  let enc1 = _.chain(encounters)
    .filter((enc) => !_.isNil(enc.encounterDateTime) && 
                     !_.isNil(enc.earliestVisitDateTime) && 
                     _.isNil(enc.cancelDateTime))
    .filter((enc) => enc.uuid !== programEncounter.uuid)
    .filter((enc) => enc.encounterDateTime < programEncounter.encounterDateTime)
    .sortBy((enc) => -imports.moment(enc.earliestVisitDateTime)) 
    .nth(0)
    .value();
  
  let enc2 = _.chain(encounters)
    .filter((enc) => !_.isNil(enc.encounterDateTime) && 
                     !_.isNil(enc.earliestVisitDateTime) && 
                     _.isNil(enc.cancelDateTime))
    .filter((enc) => enc.uuid !== programEncounter.uuid)
    .filter((enc) => enc.encounterDateTime < programEncounter.encounterDateTime)
    .sortBy((enc) => -imports.moment(enc.earliestVisitDateTime))
    .nth(1)
    .value();
  
  let enc1Weight = null, enc2Weight = null;
  let currentWeight = programEncounter.getObservationReadableValue('Weight');
  
  if (enc1) {
    enc1Weight = enc1.getObservationReadableValue('Weight');
  }
  if (enc2) {
    enc2Weight = enc2.getObservationReadableValue('Weight');
  }
  
  if(enc1Weight && enc2Weight && (currentWeight <= enc1Weight) && (enc1Weight <= enc2Weight)) {
    value = "GF2"; // Growth Faltering 2
  } else if(enc1Weight && (currentWeight <= enc1Weight)) {
    value = "GF1"; // Growth Faltering 1
  } else {
    value = "No GF";
  }
  
  return new imports.rulesConfig.FormElementStatus(
    formElement.uuid, true, value, [], []
  );
};
```

### Pattern 10: Z-Score Calculation and Nutritional Status
**Use Case**: Calculate WHO z-scores and determine nutritional status

```javascript
'use strict';
({params, imports}) => {
  const programEncounter = params.entity;
  const formElement = params.formElement;
  const _ = imports.lodash;
  let value = null;
  
  const height = programEncounter.getObservationValue("Height");
  const weight = programEncounter.getObservationValue("Weight");
  const asOnDate = programEncounter.encounterDateTime;
  const individual = programEncounter.programEnrolment.individual;
  
  const getGradeforZscore = (zScore) => {
    let grade;
    if (zScore <= -3) {
      grade = 3;
    } else if (zScore > -3 && zScore < -2) {
      grade = 2;
    } else if (zScore >= -2) {
      grade = 1;
    }
    return grade;
  };
  
  const zScoresForChild = ruleServiceLibraryInterfaceForSharingModules.common
    .getZScore(individual, asOnDate, weight, height);
  
  const zScoreGradeStatusMappingWeightForHeight = [
    ["SAM", -3],
    ["MAM", -2],
    ["Normal", 1],
    ["Normal", 2],
    ["Normal", 3],
    ["Normal", Infinity],
  ];
  
  const weightForHeightStatus = function (zScore) {
    let found = _.find(zScoreGradeStatusMappingWeightForHeight, function (currentStatus) {
      return zScore <= currentStatus[1];
    });
    return found && found[0];
  };
  
  const wfhStatus = weightForHeightStatus(zScoresForChild.wfh);
  const wfhGrade = getGradeforZscore(zScoresForChild.wfh);
  
  value = wfhStatus;
  
  return new imports.rulesConfig.FormElementStatus(
    formElement.uuid, true, value, [], []
  );
};
```

---

## Form Element Rules

### Visibility Rules by Form

#### ANC Form (Pregnancy Program)
1. **Conditional Field Display**: Show/hide fields based on previous answers
2. **Previous Month Values**: Display BP, weight from previous ANC visit
3. **USG-Related Fields**: Show USG details only if USG was taken
4. **IFA Tablet Tracking**: Show IFA consumption fields conditionally
5. **High-Risk Conditions**: Display high-risk related questions based on conditions

#### Growth Monitoring Form (Child Program)
1. **Weight Validation**: Weight must be ≤ 50 kg
2. **Height Tracking**: Display previous month height, validate against previous value
3. **Nutritional Status Calculation**: Auto-calculate based on z-scores
4. **Growth Faltering Detection**: Compare weight across 3 visits
5. **PPK/Creche Attendance**: Show based on age and location properties
6. **MUAC Measurement**: Show for children 6-59 months

#### Child Enrolment Form
1. **Age-Based Questions**: Show breastfeeding questions only if age ≥ 6 months
2. **Annaprassan**: Show only for children ≥ 6 months
3. **Birth Details**: Mandatory fields for place of birth, birth weight

#### NRC Admission Form
1. **Admission Criteria**: Validate MUAC, weight-for-height for SAM criteria
2. **Medical History**: Show relevant medical history fields
3. **Referral Details**: Track referral source and reason

#### Delivery Form
1. **Birth Outcome**: Show fields based on live birth/stillbirth
2. **Complications**: Show complication fields conditionally
3. **Newborn Details**: Show for each live birth

---

## Validation Rules

### Form-Level Validation Examples

#### 1. Pregnancy Enrolment Validation
```javascript
'use strict';
({params, imports}) => {
  const programEnrolment = params.entity;
  const validationResults = [];
  const moment = imports.moment;
  
  const lmp = programEnrolment.getObservationValue('LMP');
  const edd = programEnrolment.getObservationValue('EDD');
  
  if (lmp && edd) {
    const calculatedEDD = moment(lmp).add(280, 'days');
    const providedEDD = moment(edd);
    
    const daysDiff = Math.abs(calculatedEDD.diff(providedEDD, 'days'));
    
    if (daysDiff > 7) {
      validationResults.push(
        imports.rulesConfig.createValidationError(
          'EDD does not match LMP. Please verify dates.'
        )
      );
    }
  }
  
  return validationResults;
};
```

#### 2. Growth Monitoring Validation
```javascript
'use strict';
({params, imports}) => {
  const programEncounter = params.entity;
  const validationResults = [];
  
  const weight = programEncounter.getObservationValue('Weight');
  const height = programEncounter.getObservationValue('Height');
  
  if (!weight || !height) {
    validationResults.push(
      imports.rulesConfig.createValidationError(
        'Both weight and height are mandatory for growth monitoring'
      )
    );
  }
  
  return validationResults;
};
```

---

## Visit Schedule Rules

### Scheduling Patterns

#### Pattern 1: Regular Interval Scheduling
**Use Case**: Schedule visits at fixed intervals

```javascript
'use strict';
({params, imports}) => {
  const programEnrolment = params.entity;
  const scheduleBuilder = new imports.rulesConfig.VisitScheduleBuilder({
    programEnrolment: programEnrolment
  });
  
  const moment = imports.moment;
  const enrolmentDate = moment(programEnrolment.enrolmentDateTime);
  
  // Schedule monthly visits for 6 months
  for (let i = 1; i <= 6; i++) {
    scheduleBuilder.add({
      name: `Month ${i} Visit`,
      encounterType: 'Growth Monitoring',
      earliestDate: enrolmentDate.clone().add(i, 'months').toDate(),
      maxDate: enrolmentDate.clone().add(i, 'months').add(7, 'days').toDate()
    });
  }
  
  return scheduleBuilder.getAllUnique('encounterType');
};
```

#### Pattern 2: Conditional Scheduling Based on Observations
**Use Case**: Schedule follow-up only if certain conditions are met

```javascript
'use strict';
({params, imports}) => {
  const programEncounter = params.entity;
  const scheduleBuilder = new imports.rulesConfig.VisitScheduleBuilder({
    programEnrolment: programEncounter.programEnrolment
  });
  
  const moment = imports.moment;
  const encounterDate = moment(programEncounter.encounterDateTime);
  
  const nutritionalStatus = programEncounter.getObservationReadableValue('Nutritional Status');
  
  // Schedule QRT visit only for SAM/MAM cases
  if (nutritionalStatus === 'SAM' || nutritionalStatus === 'MAM') {
    scheduleBuilder.add({
      name: 'QRT Follow-up',
      encounterType: 'QRT Child',
      earliestDate: encounterDate.clone().add(7, 'days').toDate(),
      maxDate: encounterDate.clone().add(14, 'days').toDate()
    });
  }
  
  return scheduleBuilder.getAllUnique('encounterType');
};
```

#### Pattern 3: Gestational Age-Based Scheduling
**Use Case**: Schedule ANC visits based on gestational age

```javascript
'use strict';
({params, imports}) => {
  const programEnrolment = params.entity;
  const scheduleBuilder = new imports.rulesConfig.VisitScheduleBuilder({
    programEnrolment: programEnrolment
  });
  
  const moment = imports.moment;
  const lmp = moment(programEnrolment.getObservationValue('LMP'));
  const edd = moment(programEnrolment.getObservationValue('EDD'));
  
  // ANC 1: 12-16 weeks
  scheduleBuilder.add({
    name: 'ANC 1',
    encounterType: 'ANC',
    earliestDate: lmp.clone().add(12, 'weeks').toDate(),
    maxDate: lmp.clone().add(16, 'weeks').toDate()
  });
  
  // ANC 2: 20-24 weeks
  scheduleBuilder.add({
    name: 'ANC 2',
    encounterType: 'ANC',
    earliestDate: lmp.clone().add(20, 'weeks').toDate(),
    maxDate: lmp.clone().add(24, 'weeks').toDate()
  });
  
  // ANC 3: 28-32 weeks
  scheduleBuilder.add({
    name: 'ANC 3',
    encounterType: 'ANC',
    earliestDate: lmp.clone().add(28, 'weeks').toDate(),
    maxDate: lmp.clone().add(32, 'weeks').toDate()
  });
  
  // ANC 4: 36 weeks to EDD
  scheduleBuilder.add({
    name: 'ANC 4',
    encounterType: 'ANC',
    earliestDate: lmp.clone().add(36, 'weeks').toDate(),
    maxDate: edd.toDate()
  });
  
  return scheduleBuilder.getAllUnique('encounterType');
};
```

#### Pattern 4: Prevent Duplicate Scheduling
**Use Case**: Check if encounter already scheduled before adding

```javascript
'use strict';
({params, imports}) => {
  const programEncounter = params.entity;
  const scheduleBuilder = new imports.rulesConfig.VisitScheduleBuilder({
    programEnrolment: programEncounter.programEnrolment
  });
  
  const moment = imports.moment;
  
  // Helper function to check if encounter already scheduled
  const isAlreadyScheduled = (encounterTypeName) => {
    const scheduledEncounters = programEncounter.programEnrolment.scheduledEncounters();
    return scheduledEncounters.some(enc => 
      enc.encounterType.name === encounterTypeName && 
      enc.encounterDateTime === null &&
      enc.cancelDateTime === null
    );
  };
  
  if (!isAlreadyScheduled('Growth Monitoring')) {
    scheduleBuilder.add({
      name: 'Next Growth Monitoring',
      encounterType: 'Growth Monitoring',
      earliestDate: moment().add(1, 'month').toDate(),
      maxDate: moment().add(1, 'month').add(7, 'days').toDate()
    });
  }
  
  return scheduleBuilder.getAllUnique('encounterType');
};
```

---

## Decision Rules

### Decision Support Patterns

#### Pattern 1: Z-Score Calculation and High-Risk Flagging
**Use Case**: Calculate anthropometric indices and flag high-risk cases

```javascript
'use strict';
({params, imports}) => {
  const programEncounter = params.entity;
  const decisions = params.decisions;
  const _ = imports.lodash;
  
  const height = programEncounter.getObservationValue("Height");
  const weight = programEncounter.getObservationValue("Weight");
  const asOnDate = programEncounter.encounterDateTime;
  const individual = programEncounter.programEnrolment.individual;
  
  const addIfRequired = (decisions, name, value) => {
    if (value === -0) value = 0;
    if (value !== undefined) decisions.push({name: name, value: value});
  };
  
  const getGradeforZscore = (zScore) => {
    let grade;
    if (zScore <= -3) {
      grade = 3;
    } else if (zScore > -3 && zScore < -2) {
      grade = 2;
    } else if (zScore >= -2) {
      grade = 1;
    }
    return grade;
  };
  
  const zScoresForChild = ruleServiceLibraryInterfaceForSharingModules.common
    .getZScore(individual, asOnDate, weight, height);
  
  const zScoreGradeStatusMappingWeightForAge = {
    '1': 'Normal',
    '2': 'Moderately Underweight',
    '3': 'Severely Underweight'
  };
  
  const zScoreGradeStatusMappingHeightForAge = {
    '1': 'Normal',
    '2': 'Stunted',
    '3': 'Severely stunted'
  };
  
  const zScoreGradeStatusMappingWeightForHeight = [
    ["SAM", -3],
    ["MAM", -2],
    ["Normal", 1],
    ["Normal", 2],
    ["Normal", 3],
    ["Normal", Infinity],
  ];
  
  const weightForHeightStatus = function (zScore) {
    let found = _.find(zScoreGradeStatusMappingWeightForHeight, function (currentStatus) {
      return zScore <= currentStatus[1];
    });
    return found && found[0];
  };
  
  const wfaGrade = getGradeforZscore(zScoresForChild.wfa);
  const wfaStatus = zScoreGradeStatusMappingWeightForAge[wfaGrade];
  
  const wfhStatus = weightForHeightStatus(zScoresForChild.wfh);
  const wfhGrade = getGradeforZscore(zScoresForChild.wfh);
  
  const hfaGrade = getGradeforZscore(zScoresForChild.hfa);
  const hfaStatus = zScoreGradeStatusMappingHeightForAge[hfaGrade];
  
  // Add z-scores to encounter decisions
  addIfRequired(decisions.encounterDecisions, "Weight for age z-score", zScoresForChild.wfa);
  addIfRequired(decisions.encounterDecisions, "Weight for age Grade", wfaGrade);
  addIfRequired(decisions.encounterDecisions, "Weight for age Status", wfaStatus ? [wfaStatus] : []);
  
  addIfRequired(decisions.encounterDecisions, "Height for age z-score", zScoresForChild.hfa);
  addIfRequired(decisions.encounterDecisions, "Height for age Grade", hfaGrade);
  addIfRequired(decisions.encounterDecisions, "Height for age Status", hfaStatus ? [hfaStatus] : []);
  
  addIfRequired(decisions.encounterDecisions, "Weight for height z-score", zScoresForChild.wfh);
  addIfRequired(decisions.encounterDecisions, "Weight for Height Status", wfhStatus ? [wfhStatus] : []);
  
  // Flag for QRT monitoring
  if(wfhStatus == "SAM" || wfaStatus == "Severely Underweight") {
    decisions.registrationDecisions.push({name : "To be monitored by QRT", value : "Yes"});
    decisions.enrolmentDecisions.push({name : "To be monitored by QRT", value : "Yes"});
    decisions.encounterDecisions.push({name : "To be monitored by QRT", value : "Yes"});
  } else {
    decisions.registrationDecisions.push({name : "To be monitored by QRT", value : "No"});
    decisions.enrolmentDecisions.push({name : "To be monitored by QRT", value : "No"});
    decisions.encounterDecisions.push({name : "To be monitored by QRT", value : "No"});
  }
  
  return decisions;
};
```

#### Pattern 2: High-Risk Pregnancy Detection
**Use Case**: Identify high-risk pregnancy conditions

```javascript
'use strict';
({params, imports}) => {
  const programEnrolment = params.entity;
  const decisions = params.decisions;
  
  const highRiskConditions = [];
  
  // Age-based risk
  const age = programEnrolment.individual.getAgeInYears();
  if (age < 18 || age > 35) {
    highRiskConditions.push("Age related risk");
  }
  
  // Gravida/Para-based risk
  const gravida = programEnrolment.getObservationValue('Gravida');
  if (gravida && gravida > 4) {
    highRiskConditions.push("Grand multipara");
  }
  
  // Previous complications
  const prevComplications = programEnrolment.getObservationValue('Previous pregnancy complications');
  if (prevComplications && prevComplications.length > 0) {
    highRiskConditions.push("Previous complications");
  }
  
  // Medical conditions
  const medicalConditions = programEnrolment.getObservationValue('Medical conditions');
  if (medicalConditions && medicalConditions.length > 0) {
    highRiskConditions.push(...medicalConditions);
  }
  
  if (highRiskConditions.length > 0) {
    decisions.enrolmentDecisions.push({
      name: "High risk condition", 
      value: highRiskConditions
    });
    decisions.enrolmentDecisions.push({
      name: "To be monitored by QRT", 
      value: "Yes"
    });
    decisions.registrationDecisions.push({
      name: "To be monitored by QRT", 
      value: "Yes"
    });
  } else {
    decisions.enrolmentDecisions.push({
      name: "To be monitored by QRT", 
      value: "No"
    });
    decisions.registrationDecisions.push({
      name: "To be monitored by QRT", 
      value: "No"
    });
  }
  
  return decisions;
};
```

#### Pattern 3: Clear QRT Flag on Exit
**Use Case**: Reset high-risk flag when program exits

```javascript
'use strict';
({params, imports}) => {
  const programEnrolment = params.entity;
  const decisions = params.decisions;
  
  decisions.registrationDecisions.push({name : "To be monitored by QRT", value : "No"});
  decisions.enrolmentDecisions.push({name : "To be monitored by QRT", value : "No"});
  
  return decisions;
};
```

---

## Helper Functions and Libraries

### Available Imports

#### 1. Moment.js (Date/Time Manipulation)
```javascript
const moment = imports.moment;

// Common operations
moment().add(7, 'days')
moment().subtract(1, 'month')
moment(date1).diff(date2, 'days')
moment(date).startOf('day')
moment(date).isAfter(otherDate)
moment(date).isBefore(otherDate)
```

#### 2. Lodash (Utility Functions)
```javascript
const _ = imports.lodash;

// Common operations
_.isFinite(value)
_.isNil(value)
_.orderBy(array, ['field'], ['asc'])
_.findIndex(array, predicate)
_.chain(array).filter().sortBy().nth(0).value()
_.find(array, predicate)
```

#### 3. RulesConfig (Avni-Specific)
```javascript
const imports.rulesConfig;

// RuleCondition
new imports.rulesConfig.RuleCondition({entity, formElement})
  .when.valueInEncounter("uuid")
  .containsAnswerConceptName("uuid")
  .matches()

// FormElementStatus
new imports.rulesConfig.FormElementStatus(
  formElement.uuid, 
  visibility, 
  value, 
  answersToSkip, 
  validationErrors
)

// VisitScheduleBuilder
new imports.rulesConfig.VisitScheduleBuilder({programEnrolment})

// Validation
imports.rulesConfig.createValidationError('message')
```

#### 4. Rule Service Library (Shared Functions)
```javascript
ruleServiceLibraryInterfaceForSharingModules.common

// Available functions
.calculateBMI(weight, height)
.getZScore(individual, asOnDate, weight, height)
// Returns: {wfa, hfa, wfh, bfa}
```

### Entity Methods

#### Individual
```javascript
individual.getAgeInYears()
individual.getAgeInMonths()
individual.getAgeInDays()
individual.isFemale()
individual.isMale()
individual.dateOfBirth
individual.lowestAddressLevel
individual.lowestAddressLevel.locationProperties
```

#### Program Enrolment
```javascript
programEnrolment.individual
programEnrolment.enrolmentDateTime
programEnrolment.encounters
programEnrolment.getEncountersOfType('encounterTypeName')
programEnrolment.scheduledEncounters()
programEnrolment.findObservation('conceptName')
programEnrolment.getObservationValue('conceptName')
programEnrolment.getObservationReadableValue('conceptName')
programEnrolment.findLatestObservationInEntireEnrolment('conceptName')
programEnrolment.findLatestObservationFromEncounters('conceptName')
programEnrolment.hasCompletedEncounterOfType('encounterTypeName')
programEnrolment.lastFulfilledEncounter('encounterType1', 'encounterType2')
```

#### Program Encounter
```javascript
programEncounter.programEnrolment
programEncounter.encounterType
programEncounter.encounterDateTime
programEncounter.earliestVisitDateTime
programEncounter.maxVisitDateTime
programEncounter.cancelDateTime
programEncounter.voided
programEncounter.uuid
programEncounter.findObservation('conceptName')
programEncounter.getObservationValue('conceptName')
programEncounter.getObservationReadableValue('conceptName')
```

---

## Best Practices

### 1. Performance Optimization
- Filter encounters early to reduce iterations
- Use `_.orderBy` instead of multiple sorts
- Cache frequently accessed values
- Avoid nested loops where possible

```javascript
// Good
let encounterList = programEncounter.programEnrolment.encounters
  .filter(enc => enc.encounterType.name === 'Growth Monitoring' && 
                 enc.voided == false && 
                 enc.cancelDateTime == null);
encounterList = _.orderBy(encounterList, ['earliestVisitDateTime'], ['asc']);

// Avoid
for (let enc of allEncounters) {
  if (enc.encounterType.name === 'Growth Monitoring') {
    // Process
  }
}
```

### 2. Null/Undefined Checks
- Always check for null/undefined before using values
- Use `_.isNil()` for comprehensive checks
- Provide fallback values

```javascript
// Good
const prevValue = prevEncounter && prevEncounter.getObservationValue('concept');
if (prevValue && prevValue != undefined) {
  // Use prevValue
}

// Better
if (!_.isNil(prevValue)) {
  // Use prevValue
}
```

### 3. Date Handling
- Always use `moment().startOf('day')` for date comparisons
- Be explicit about date formats
- Handle timezone considerations

```javascript
// Good
const encounterDate = moment(programEncounter.encounterDateTime).startOf('day');
const dateValue = moment(observationValue).startOf('day');

if (dateValue.isAfter(encounterDate)) {
  // Handle
}
```

### 4. Error Messages
- Provide clear, actionable error messages
- Include context in validation errors
- Use consistent messaging style

```javascript
// Good
validationErrors.push("Height cannot be less than previous visit. Previous: 85cm, Current: 80cm");

// Avoid
validationErrors.push("Invalid height");
```

### 5. Code Reusability
- Extract common logic into helper functions
- Use consistent patterns across forms
- Document complex logic

```javascript
// Good
const getGradeforZscore = (zScore) => {
  let grade;
  if (zScore <= -3) {
    grade = 3;
  } else if (zScore > -3 && zScore < -2) {
    grade = 2;
  } else if (zScore >= -2) {
    grade = 1;
  }
  return grade;
};

const wfaGrade = getGradeforZscore(zScoresForChild.wfa);
const hfaGrade = getGradeforZscore(zScoresForChild.hfa);
```

### 6. Declarative vs Imperative Rules
- Use declarative rules for simple conditions
- Use imperative rules for complex logic
- Both can coexist in the same form element

```javascript
// Declarative (auto-generated from UI)
"declarativeRule": [{
  "actions": [{"actionType": "showFormElement"}],
  "conditions": [{
    "compoundRule": {
      "rules": [{
        "lhs": {"type": "ageInMonths"},
        "rhs": {"type": "value", "value": 6},
        "operator": "greaterThanOrEqualTo"
      }]
    }
  }]
}]

// Imperative (custom JavaScript)
"rule": "'use strict';\n({params, imports}) => { ... }"
```

### 7. Testing Considerations
- Test edge cases (null, undefined, zero, negative)
- Test with different encounter sequences
- Verify date boundary conditions
- Test with missing previous encounters

### 8. Documentation
- Add comments for complex logic
- Document assumptions
- Explain magic numbers
- Reference business rules

```javascript
// Good
// Growth Faltering Grade 2: Weight decreasing for 2 consecutive visits
// As per WHO guidelines and program requirements
if(enc1Weight && enc2Weight && 
   (currentWeight <= enc1Weight) && 
   (enc1Weight <= enc2Weight)) {
  value = "GF2";
}
```

---

## Rule Categories Summary

### By Purpose

**Visibility Control (150+ rules)**
- Conditional field display
- Age-based visibility
- Answer-dependent visibility
- Location-based visibility

**Value Calculation (80+ rules)**
- Auto-fill from previous encounters
- BMI calculation
- Z-score calculation
- Gestational age calculation
- Growth faltering detection

**Validation (70+ rules)**
- Range validation
- Cross-field validation
- Date validation
- Previous value comparison
- Logical consistency checks

**Visit Scheduling (23 rules)**
- Regular interval scheduling
- Gestational age-based scheduling
- Conditional scheduling
- Duplicate prevention

**Decision Support (10 rules)**
- High-risk identification
- Nutritional status classification
- QRT flagging
- Complication detection

---

## Usage Guidelines

### When to Use Each Rule Type

**Form Element Rule**:
- Show/hide fields
- Calculate and display values
- Validate individual fields
- Skip answer options

**Validation Rule**:
- Cross-field validation
- Form-level business rules
- Complex validation logic

**Visit Schedule Rule**:
- Schedule future encounters
- Set visit windows
- Conditional scheduling

**Decision Rule**:
- Calculate derived values
- Make clinical decisions
- Flag high-risk cases
- Push decisions to registration/enrolment

---

## Reference Data Location

All extracted rules are available in:
`/Users/himeshr/IdeaProjects/avni-impl-bundles/reference/apfodisha_context/extracted_rules.json`

This JSON file contains:
- 303 form element rules with form name, element name, and full JavaScript code
- 22 validation rules with form context
- 23 visit schedule rules with scheduling logic
- 10 decision rules with decision support logic

---

## Generating New Rules

### Step-by-Step Process

1. **Identify Requirement**: Understand what the rule should do
2. **Find Similar Pattern**: Search this knowledge base for similar rules
3. **Adapt Pattern**: Modify the pattern to match your requirement
4. **Test Edge Cases**: Consider null values, missing data, boundary conditions
5. **Add Error Handling**: Include validation and error messages
6. **Document**: Add comments explaining the logic

### Example: Creating a New Validation Rule

**Requirement**: Validate that current weight is not more than 2kg different from previous weight

**Steps**:
1. Find Pattern: "Cross-Field Validation" (Pattern 6)
2. Adapt:
```javascript
'use strict';
({params, imports}) => {
  const programEncounter = params.entity;
  const formElement = params.formElement;
  const _ = imports.lodash;
  let validationErrors = [];
  
  // Get previous encounter
  let encounterList = programEncounter.programEnrolment.encounters
    .filter(enc => enc.encounterType.name === 'Growth Monitoring' && 
                   enc.voided == false && 
                   enc.cancelDateTime == null);
  
  encounterList = _.orderBy(encounterList, ['earliestVisitDateTime'], ['asc']);
  const currentIndex = _.findIndex(encounterList, enc => enc.uuid === programEncounter.uuid);  
  
  if (currentIndex > 0) {
    const prevEncounter = encounterList[currentIndex - 1]; 
    const prevWeight = prevEncounter.getObservationValue('Weight');  
    const currentWeight = programEncounter.getObservationValue('Weight');
    
    if (prevWeight && currentWeight) {
      const weightDiff = Math.abs(currentWeight - prevWeight);
      
      if (weightDiff > 2) {
        validationErrors.push(
          `Weight change of ${weightDiff.toFixed(1)}kg is unusual. ` +
          `Previous: ${prevWeight}kg, Current: ${currentWeight}kg. ` +
          `Please verify measurement.`
        );
      }
    }
  }
  
  return new imports.rulesConfig.FormElementStatus(
    formElement.uuid, true, null, [], validationErrors
  );
};
```

---

**Last Updated**: Based on APF Odisha implementation forms
**Total Rules Documented**: 358 rules across all types
**Implementation**: APF Odisha - Maternal and Child Nutrition Tracking
**Platform**: Avni (OpenCHS)
