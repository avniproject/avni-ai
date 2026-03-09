# CSJ (Centre for Social Justice) Implementation - Knowledge Base

## Overview

This knowledge base documents the complete CSJ (Centre for Social Justice) implementation in Avni. CSJ is a legal aid NGO based in Gujarat, India. This implementation focuses on managing legal aid cases for marginalized communities, including case management (criminal, civil, labour, land, bail), RTI (Right to Information) filings, PIL (Public Interest Litigation), letter-based advocacy, training programs, outreach activities, claim processing, and influencing state/policy work.

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

The implementation uses 11 subject types (10 active + 1 voided):

### 1. Case (Individual)
- **UUID**: `0bc1dbf5-6790-4c9b-b5eb-d241ec6b0379`
- **Type**: Individual
- **Purpose**: Represents a legal aid case taken up by CSJ on behalf of a client/victim
- **Key Features**:
  - Core subject type — the primary entity around which most work is done
  - Has Case Status program (for tracking legal proceedings)
  - Encounters: Case Registration, Case Status Details, Case Activity Register, Case Documents, Case Legal Fund, Case Fact Finding, Victim Compensation, Case Monetary Impact, Case Disposed
  - Auto-generates name as `Case_<ApplicantName>_<Address>` via group rule
  - Subject name = `"Case_" + nameOfApplicant + '_' + addressName`

### 2. Claim (Individual)
- **UUID**: `cd93d6db-d4be-47a0-9f84-d25391f90e77`
- **Type**: Individual
- **Purpose**: Represents a claim (compensation, entitlement) filed on behalf of a beneficiary
- **Key Features**:
  - Separate from Case — used for compensation/entitlement claims
  - Has Claim Status program
  - Encounters: Claim Registration, Claim Activity Register, Claim Legal Fund, Claim Impact Form

### 3. Influencing State (Individual)
- **UUID**: `cffd3a47-d8cb-4a6f-99fc-21fddfa94b44`
- **Type**: Individual
- **Purpose**: Represents advocacy/policy influencing work (letters, RTI, PIL)
- **Key Features**:
  - Has three programs: Letter Status, RTI Status, PIL Status
  - Each program type has its own enrolment, follow-up, impact, document, and legal fund encounters
  - Program eligibility is determined by the "Nature of Case" concept

### 4. Training (Individual)
- **UUID**: `816da5ca-d4df-449d-bcd4-8eef62930d5a`
- **Type**: Individual
- **Purpose**: Represents a training program organized by CSJ
- **Key Features**:
  - Can be Internal or External training
  - Can be Phased (multiple sessions) or Single Event
  - Encounters: Internal Training, External Training, One Time Training, Training Legal Fund
  - Type of training and phasing determines which encounter types are available
  - Training name is auto-generated

### 5. Outreach (Group)
- **UUID**: `a92cdaae-19cd-4778-920c-235e30c5ecdf`
- **Type**: Group
- **Purpose**: Represents an outreach activity/event at a village or other location
- **Key Features**:
  - Only Group subject type in the implementation
  - Encounter: Outreach Location Specific Details
  - Records where outreach happened (village or other space) and what was done

### 6. Intern (Individual)
- **UUID**: `92bf310a-6ddb-4010-8d44-d7cb009cbc9c`
- **Type**: Individual
- **Purpose**: Tracks interns working with CSJ

### 7. Volunteer (Individual)
- **UUID**: `b3b98338-35af-4f29-a74d-3c8999d92165`
- **Type**: Individual
- **Purpose**: Tracks volunteers working with CSJ

### 8. Recognition/Award (Individual)
- **UUID**: `c26ea079-e6f5-451f-ba38-1ed55f5860a9`
- **Type**: Individual
- **Purpose**: Records recognitions and awards received by CSJ

### 9. Campaign (Individual)
- **UUID**: `0ab6edd4-2a80-4ce9-9bfa-0464cb4ae6b0`
- **Type**: Individual
- **Purpose**: Tracks campaigns run by CSJ

### 10. Issues Identified (Individual)
- **UUID**: `0720e6cc-f0e2-4019-aeb6-b3fba472aa4b`
- **Type**: Individual
- **Purpose**: Records systemic issues identified during fieldwork
- **Key Features**:
  - Has form: Issues Identified (IndividualProfile)

### 11. Court (Individual)
- **UUID**: `cadc8363-b121-4cd4-bbbf-5bee4fd620d1`
- **Type**: Individual
- **Purpose**: Tracks court-related entities and proceedings

### Voided Subject Type
- **Training** (old): `7c618fef-b244-47bc-9e7c-773198b03d94` — voided, replaced by current Training subject type

---

## Programs

The implementation has 5 active programs (+ 2 voided):

### 1. Case Status
- **UUID**: `73651784-823d-43b0-a967-7e4508a6d12f`
- **Subject Type**: Case (`0bc1dbf5-6790-4c9b-b5eb-d241ec6b0379`)
- **Purpose**: Tracks the legal status and progress of a case through litigation stages
- **Eligibility**: Case subject must have Case Status enrolments
- **Enrolment Form**: Case Status Details (ProgramEnrolment)
- **Exit Form**: Case Status Exit
- **Key Program Encounters**: Case Status Details Encounter (for updates)
- **Key Fields in Enrolment**:
  - `Nature of Case` — Criminal prosecution/defence, Civil, Bail, Labour, Land, Domestic Violence, etc.
  - `Status of case` — Active (pre-litigation), Active (litigation), Resolved, Closed, Client not traceable
  - Stage fields that appear conditionally based on Nature + Status combination

### 2. Claim Status
- **UUID**: `13de258f-7f58-421e-95f7-4822b8cb2c41`
- **Subject Type**: Claim (`cd93d6db-d4be-47a0-9f84-d25391f90e77`)
- **Purpose**: Manages the lifecycle of a compensation or entitlement claim
- **Eligibility**: Open/always eligible
- **Enrolment Form**: Claim Status Enrolment
- **Exit Form**: Claim Status Exit

### 3. Letter Status
- **UUID**: `e95f886c-4fbc-4b87-b3af-45bbd12bc86f`
- **Subject Type**: Influencing State (`cffd3a47-d8cb-4a6f-99fc-21fddfa94b44`)
- **Purpose**: Tracks the status of letter-based advocacy campaigns
- **Eligibility**: Nature of Influencing State work = Letter
- **Enrolment Form**: Letter Status (ProgramEnrolment)
- **Exit Form**: Letter Status Exit
- **Enrolment Validation**: Enrolment Date must be today's date (on new enrolments); on edits, date cannot be changed
- **Status Concept**: `Letter Status` — answers: Initial letter filed, Follow up letter filed, Follow up RTI filed, Closed
- **Decision Rule**: Auto-captures `Enrolment DateTime` on new enrolments
- **Program Encounters**: Follow Up Letter, Follow Up RTI, Letter Document, Letter Impact

### 4. RTI Status
- **UUID**: `2fa0b7e8-eae9-4e5e-87dd-0509f2f17017`
- **Subject Type**: Influencing State (`cffd3a47-d8cb-4a6f-99fc-21fddfa94b44`)
- **Purpose**: Tracks RTI (Right to Information) applications and responses
- **Eligibility**: Nature of Influencing State work = RTI
- **Enrolment Form**: RTI Status Enrolment
- **Exit Form**: RTI Status Exit
- **Program Encounters**: RTI Impact, RTI Document, Follow Up RTI

### 5. PIL Status
- **UUID**: `91449b25-83dd-44c5-86cb-8d2eacd33a4e`
- **Subject Type**: Influencing State (`cffd3a47-d8cb-4a6f-99fc-21fddfa94b44`)
- **Purpose**: Tracks PIL (Public Interest Litigation) filings and outcomes
- **Eligibility**: Nature of Influencing State work = PIL
- **Enrolment Form**: PIL Status Enrolment
- **Exit Form**: PIL Status Exit
- **Program Encounters**: PIL Impact, PIL Document, PIL Case Activity, PIL Legal Fund

### Voided Programs
- **Claim Status** (old): `7a4c9ea2-9668-431f-908c-184545fa7e87` — voided
- **Outreach Clients**: voided

---

## Encounter Types

### Active Encounter Types

#### Case Subject Encounters

##### Case Activity Register
- **Subject Type**: Case
- **Eligibility Rule**: Only 1 allowed per case subject (returns false if already filled)
- **Purpose**: Records activity details for the case

##### Case Documents
- **Subject Type**: Case (`0bc1dbf5-6790-4c9b-b5eb-d241ec6b0379`)
- **Encounter Type UUID**: `943dbaea-ad93-493b-b692-47be2ccd7b7a`
- **Eligibility Rule**: Only 1 allowed per case subject
- **Purpose**: Stores case-related documents (file uploads)

##### Case Legal Fund
- **Subject Type**: Case (`0bc1dbf5-6790-4c9b-b5eb-d241ec6b0379`)
- **Encounter Type UUID**: `763a7f8e-6aec-4a9b-b4ca-7f74e5309597`
- **Eligibility Rule**: Only 1 allowed per case subject
- **Purpose**: Records legal fund receipts for the case — repeatable QuestionGroup with Date of receipt, Amount, Stage at which taken, Upload receipt (file, max 1 MB), Upload Image
- **Validation Rule**: Date of receipt cannot be a future date

##### Case Monetary Impact
- **Subject Type**: Case (`0bc1dbf5-6790-4c9b-b5eb-d241ec6b0379`)
- **Encounter Type UUID**: `37920b3f-5ad5-48c5-b11e-ae969bf8ffff`
- **Eligibility Rule**: Only 1 allowed per case subject
- **Purpose**: Records monetary impact/compensation received for the case

##### Case Status Details (Encounter)
- **Subject Type**: Case (`0bc1dbf5-6790-4c9b-b5eb-d241ec6b0379`)
- **Encounter Type UUID**: `d8f9b41a-abe2-4677-84a0-c3ead8542af4`
- **Purpose**: Updates to the case status (used as a follow-up encounter, separate from Program Enrolment form)

##### Victim Compensation
- **Subject Type**: Case (`0bc1dbf5-6790-4c9b-b5eb-d241ec6b0379`)
- **Encounter Type UUID**: `312ad861-3f2b-4b5a-8611-d2d170a4eb1c`
- **Eligibility Rule**: Only for specific criminal case types (based on Nature of Case)
- **Purpose**: Records compensation received under various schemes (NALSA 2018 Scheme, SC ST PoA Compensation Rules, Other scheme)
- **Validation**: Multiple date fields — none can be future dates

##### Case Fact Finding
- **Subject Type**: Case (`0bc1dbf5-6790-4c9b-b5eb-d241ec6b0379`)
- **Encounter Type UUID**: Referenced in formMappings
- **Eligibility Rule**: Only for specific criminal case types
- **Purpose**: Records fact-finding visits — Date of incident, Date of receiving info, Date of fact finding, Location
- **Validation**: All date fields — no future dates allowed

##### Case Disposed
- **Subject Type**: Case (`0bc1dbf5-6790-4c9b-b5eb-d241ec6b0379`)
- **Encounter Type UUID**: `a6290741-b145-474a-812a-6c0270452c92`
- **Eligibility Rule**: Always returns false (disabled — cannot be created)
- **Purpose**: Marks case as disposed (currently disabled)

#### Claim Subject Encounters

##### Claim Activity Register
- **Subject Type**: Claim (`cd93d6db-d4be-47a0-9f84-d25391f90e77`)
- **Encounter Type UUID**: `57486413-7045-491c-9596-c66c6fc61a2a`
- **Eligibility Rule**: Only 1 allowed per claim subject
- **Purpose**: Records activities done for the claim

##### Claim Legal Fund
- **Subject Type**: Claim (`cd93d6db-d4be-47a0-9f84-d25391f90e77`)
- **Encounter Type UUID**: `6afe3ea4-a64a-4861-a586-9d8fa54edf5c`
- **Eligibility Rule**: Only 1 allowed per claim subject
- **Purpose**: Records legal fund receipts for the claim

##### Claim Impact Form
- **Subject Type**: Claim (`cd93d6db-d4be-47a0-9f84-d25391f90e77`)
- **Encounter Type UUID**: `0bb3b428-6057-4cf3-9d15-22851ecce74b`
- **Eligibility Rule**: Only 1 allowed per claim subject
- **Purpose**: Records the impact of the claim (monetary and non-monetary)

#### Training Subject Encounters

##### Internal Training
- **Subject Type**: Training (`816da5ca-d4df-449d-bcd4-8eef62930d5a`)
- **Encounter Type UUID**: `a5d29b8a-69d8-4a76-b18e-c28883ca82ba`
- **Eligibility Rule**: Only when `Type of training = Internal` AND training is phased
- **Purpose**: Records individual sessions/phases of an internal training program
- **Key Fields**: Which phase, Nature of training, Visit Date

##### External Training
- **Subject Type**: Training (`816da5ca-d4df-449d-bcd4-8eef62930d5a`)
- **Encounter Type UUID**: `107721e2-1ee1-4d51-a3c8-5f9ed7983ba7`
- **Eligibility Rule**: Only when `Type of training = External` AND training is phased
- **Purpose**: Records individual sessions/phases of an external training program

##### One Time Training
- **Subject Type**: Training (`816da5ca-d4df-449d-bcd4-8eef62930d5a`)
- **Encounter Type UUID**: `a3e30cab-ff81-4ed1-8706-9773ec2372c2`
- **Eligibility Rule**: Only when training is NOT phased AND no One Time Training encounter has been filled yet
- **Purpose**: Records a single-session (non-phased) training event

##### Training Legal Fund
- **Subject Type**: Training (`816da5ca-d4df-449d-bcd4-8eef62930d5a`)
- **Encounter Type UUID**: `5bc44f70-46a9-4e7a-85e9-8cf0e44dc55b`
- **Eligibility Rule**: Only 1 allowed, and only for non-Internal training types
- **Purpose**: Records legal fund receipts for training programs

#### Outreach Group Encounters

##### Outreach Location Specific Details
- **Subject Type**: Outreach (`a92cdaae-19cd-4778-920c-235e30c5ecdf`)
- **Encounter Type UUID**: `04175152-5f03-4e3c-b7b7-c07914b8d67e`
- **Eligibility Rule**: Complex location-based rule — determines if outreach was at Village or Other Space
- **Purpose**: Records location-specific details of an outreach event — venue type (village/school/court/government office/other), number of participants, topics covered
- **Key Fields**: Where did the Outreach Activity happen (Village/Other Space), specific location within village

#### Influencing State Program Encounters

##### Follow Up Letter (Letter Status Program)
- **Subject Type**: Influencing State, under Letter Status program (`e95f886c-4fbc-4b87-b3af-45bbd12bc86f`)
- **Encounter Type UUID**: `6a52bd71-f499-476d-ba39-7ce0977698e5`
- **Purpose**: Records follow-up letter activities

##### Follow Up RTI (Letter Status Program)
- **Subject Type**: Influencing State, under Letter Status program
- **Encounter Type UUID**: `a80cfec5-6436-457f-bdac-ba2d37860baf`
- **Purpose**: Records follow-up RTI activities under letter campaigns

##### Letter Document (Letter Status Program)
- **Encounter Type UUID**: `ecdc98b0-9b69-49c9-a798-faa8ed48ddbe`
- **Purpose**: Stores documents related to letter campaigns

##### Letter Impact (Letter Status Program)
- **Encounter Type UUID**: `688c8097-c617-4acf-8281-864319da35d4`
- **Eligibility Rule**: Only 1 allowed per Letter Status enrolment
- **Purpose**: Records impact of the letter campaign
- **Form**: Letter Impact Encounter — repeatable QuestionGroup with Date of impact, Description of Impact, Monetary Impact
- **Validation**: 
  - Encounter Date must be today's date (on new encounters)
  - Encounter Date cannot be changed (on edits)
  - At least one of "Impact Description" OR "Monetary Impact" must be filled per group entry

##### RTI Impact (RTI Status Program)
- **Encounter Type UUID**: `42e4c852-fa15-4ad0-bfab-80dab90de421`
- **Eligibility Rule**: Only 1 allowed per RTI Status enrolment
- **Purpose**: Records impact of the RTI filing

##### RTI Document (RTI Status Program)
- **Encounter Type UUID**: `ac2a5462-1656-4c4e-98ee-9b108bf806d4`
- **Eligibility Rule**: Only 1 allowed per RTI Status enrolment
- **Purpose**: Stores RTI-related documents

##### PIL Impact (PIL Status Program)
- **Encounter Type UUID**: `bdbd3d89-e1fb-4c4b-ae6a-ca0d745b2652`
- **Eligibility Rule**: Only 1 allowed per PIL Status enrolment
- **Purpose**: Records impact of PIL filing

##### PIL Document (PIL Status Program)
- **Encounter Type UUID**: `dac30d7e-97eb-4da9-8882-b3411fb39f26`
- **Eligibility Rule**: Only 1 allowed per PIL Status enrolment
- **Purpose**: Stores PIL-related documents

##### PIL Case Activity / PIL Case Activity Register (PIL Status Program)
- **Encounter Type UUID**: `7e42c11e-e3f1-4f04-8562-f67471ee157c`
- **Eligibility Rule**: Only 1 allowed per PIL Status enrolment
- **Purpose**: Records activity register for PIL case

##### PIL Legal Fund (PIL Status Program)
- **Encounter Type UUID**: `252c33f0-bd3f-48ff-bf80-22db679cff8c`
- **Eligibility Rule**: Only 1 allowed per PIL Status enrolment
- **Purpose**: Records legal fund receipts for PIL

---

## Address Level Types

Two active address level hierarchies:

### Hierarchy 1 — Operational (4 levels)
Used for field operations, case registrations, outreach, training:
- **State** (level 7) — UUID: `b11a3eba-5e28-4b7a-886d-5cec856d02ba`
- **District** (level 6) — UUID: `f25882dc-2a0f-4267-ae88-7ae4bfb264ee`
- **Block** (level 5) — UUID: `c6a4422b-07b6-40ba-bf9b-d5cc312549cf` (also `4dcc08c0-cf4f-4c15-a946-1658beaa3376`)
- **Village** (level 4) — UUID: `c1f26e98-816d-4cf5-aada-6f4dcab46487` (also `8f1d7866-0ad1-4026-bbcb-37cea12ee641`)

### Hierarchy 2 — Administrative (2 levels)
- **Administrative State** (level 9) — UUID: `e68249ed-c278-4c38-b838-a1d52896018a`
- **Administrative Unit** (level 8) — UUID: (child of Administrative State)

---

## Form Mappings

Summary of active form mappings by subject type and form type:

### Case Subject (`0bc1dbf5-6790-4c9b-b5eb-d241ec6b0379`)
| Form Type | Form Name |
|-----------|-----------|
| IndividualProfile | Case Registration |
| ProgramEnrolment (Case Status) | Case Status Details |
| ProgramExit (Case Status) | Case Status Exit |
| Encounter | Case Status Details Encounter |
| Encounter | Case Activity Register |
| Encounter | Case Documents Encounter |
| Encounter | Case Legal Fund |
| Encounter | Case Monetary Impact |
| Encounter | Victim Compensation |
| Encounter | Case Fact Finding |
| Encounter | Case Disposed |
| IndividualEncounterCancellation | (cancellations for each encounter) |

### Claim Subject (`cd93d6db-d4be-47a0-9f84-d25391f90e77`)
| Form Type | Form Name |
|-----------|-----------|
| IndividualProfile | Claim Registration |
| ProgramEnrolment (Claim Status) | Claim Status Enrolment |
| ProgramExit (Claim Status) | Claim Status Exit |
| Encounter | Claim Activity Register |
| Encounter | Claim Legal Fund |
| Encounter | Claim Impact Form |
| IndividualEncounterCancellation | (cancellations for each encounter) |

### Influencing State Subject (`cffd3a47-d8cb-4a6f-99fc-21fddfa94b44`)
| Form Type | Form Name |
|-----------|-----------|
| IndividualProfile | Influencing State Registration |
| ProgramEnrolment (Letter Status) | Letter Status |
| ProgramExit (Letter Status) | Letter Status Exit |
| ProgramEncounter (Letter Status) | Follow Up Letter Encounter |
| ProgramEncounter (Letter Status) | Follow Up RTI Encounter |
| ProgramEncounter (Letter Status) | Letter Document Encounter |
| ProgramEncounter (Letter Status) | Letter Impact Encounter |
| ProgramEnrolment (RTI Status) | RTI Status Enrolment |
| ProgramExit (RTI Status) | RTI Status Exit |
| ProgramEncounter (RTI Status) | RTI Impact Encounter |
| ProgramEncounter (RTI Status) | RTI Document Encounter |
| ProgramEnrolment (PIL Status) | PIL Status Enrolment |
| ProgramExit (PIL Status) | PIL Status Exit |
| ProgramEncounter (PIL Status) | PIL Impact Encounter |
| ProgramEncounter (PIL Status) | PIL Document Encounter |
| ProgramEncounter (PIL Status) | PIL Case Activity |
| ProgramEncounter (PIL Status) | PIL Legal Fund Encounter |

### Training Subject (`816da5ca-d4df-449d-bcd4-8eef62930d5a`)
| Form Type | Form Name |
|-----------|-----------|
| IndividualProfile | Training Registration |
| Encounter | Internal Training |
| Encounter | External Training |
| Encounter | One Time Training |
| Encounter | Training Legal Fund |
| IndividualEncounterCancellation | (cancellations for each encounter) |

### Outreach Subject (`a92cdaae-19cd-4778-920c-235e30c5ecdf`)
| Form Type | Form Name |
|-----------|-----------|
| IndividualProfile | Outreach Registration |
| Encounter | Outreach Location Specific Details |
| IndividualEncounterCancellation | Outreach Location Specific Details Cancellation |

### Issues Identified Subject (`0720e6cc-f0e2-4019-aeb6-b3fba472aa4b`)
| Form Type | Form Name |
|-----------|-----------|
| IndividualProfile | Issues Identified |

---

## Forms Structure

### Case Registration (IndividualProfile — Case Subject)
**Purpose**: Registers a new legal aid case

**Form Element Groups**:

#### 1. Applicant Details
Key fields:
- **Name of applicant** (Text, mandatory) — used to auto-generate the Case name
- **Phone number of applicant** (Text, optional) — validation: must start with 6-9 and be 10 digits
- **Does the phone number belong to the applicant?** (Coded: Yes/No, UUID: `7d720c7b-7f5c-43f7-a091-6f5cff171c21`)
  - When `No`: shows "Name of person" and "Relation" fields
- **Address of Applicant** (Location — Village level, within State hierarchy, mandatory)
- **Group Rule**: Auto-sets `individual.name = "Case_" + nameOfApplicant + "_" + addressName`; if either missing, name = "Case_"

#### 2. Victim Details
Key fields:
- **Whether applicant same as victim?** (Coded: Yes/No, UUID: `8a45b281-8e39-4ea7-9e85-58dfd186275d`, mandatory)
- **Name of victim** — visible only when `Whether applicant same as victim? = No` (mandatory when visible)
- **Phone no. of victim** — visible only when `Whether applicant same as victim? = No`; validation: 10-digit, starts with 6-9
- **Address of Victim** — visible only when `Whether applicant same as victim? = No` (mandatory when visible)

#### 3. Case Details
Key fields:
- **Nature of Case** (UUID: `252f4c55-d113-4951-8ebb-eed01b9ccbb9`, Coded, mandatory) — answers include: Criminal prosecution fresh filing, Criminal defence fresh filing, Civil, Bail, Labour, Land, Domestic Violence, POCSO, Prant Darji (Caste atrocity), Other
- **Claim Source** (UUID: `9cf2776d-8fd2-42db-8c74-dfc9433e2af1`)
- **Visit Date** (UUID: `ff308558-e951-46bf-8115-c41bf16b02da`, Date) — validation: cannot be a future date

**Group-Level Rule** (Applicant Details group): Sets the individual's name in the database based on applicant name and address.

---

### Case Status Details (ProgramEnrolment — Case Status Program)
**Purpose**: Records the current legal status of a case when enrolling into Case Status program

**Key Fields**:
- **Nature of Case** (UUID: `252f4c55-d113-4951-8ebb-eed01b9ccbb9`, read from enrolment) — determines which stage fields are shown
- **Status of case** (UUID: `b1927aeb-ab4c-46a6-8eff-6ccdf38f5478`, Coded, mandatory) — answers: Active (pre-litigation), Active (litigation), Resolved, Closed, Client not traceable

**Conditional Stage Fields** (all shown based on Nature of Case + Status of case combination):
- **Stage of Active (pre-litigation) - Criminal Prosecution/Defence fresh filing**
  - Visible when: Nature of Case = Criminal prosecution fresh filing OR Criminal defence fresh filing AND Status = Active (pre-litigation)
  - Answers: Pre-Investigation, Investigation, Chargesheet filed

- **Stage of Active (litigation) - Criminal Prosecution/Defence fresh filing**
  - Visible when: Nature of Case = Criminal prosecution/defence AND Status = Active (litigation)
  - Answers: Framing of charges, Committal, Prosecution evidence, Defence evidence, Final arguments, Judgment and sentencing

- Additional stage fields exist for other Nature of Case types (Civil, Labour, Land, Bail, etc.) with their own status/stage combinations

**Visibility Pattern**: Every stage field uses a two-condition AND rule:
```javascript
const condition11 = RuleCondition.when.valueInEnrolment("252f4c55-...").containsAnyAnswerConceptName("Criminal prosecution...", "Criminal defence...").matches();
const condition21 = RuleCondition.when.valueInEnrolment("b1927aeb-...").containsAnswerConceptName("Active (pre-litigation)").matches();
visibility = condition11 && condition21;
```

---

### Training Registration (IndividualProfile — Training Subject)
**Purpose**: Registers a new training program

**Key Fields**:
- **Title of Training** — hidden when `Type of training = Internal`
  - Rule: `visibility = !(condition11)` where condition11 checks Type = Internal
- **Type of training** (UUID: `c7afa395-baae-4434-b8f7-b938b78051bd`, Coded: Internal/External, mandatory)
  - **Edit prevention**: Cannot be changed after enrolments or encounters exist
  - Rule checks `individual.enrolments.length > 0 || individual.encounters.length > 0` → if true, sets value back to existing value
- **Whether phased** (UUID: `387e72d2-1ced-4032-b273-ea3ef5c5a159`, Coded: Phased/Single event, mandatory)
- **Nature of training** (UUID: `302ce25a-1fe7-4c5a-9a31-e1e54009187b`, Coded) — shown only when Type = Internal
  - Rule: `visibility = condition11` (same internal check)
- **Which phase** (UUID: `1732f13a-26c0-4ef9-a92b-78d65519b024`) — visible when "Other Phase" selected
- **Visit Date** (UUID: `ff308558-e951-46bf-8115-c41bf16b02da`) — validation: cannot be a future date

---

### Internal Training (Encounter — Training Subject)
**Purpose**: Records each session of a phased internal training

**Key Fields**:
- Phase selection (which training phase this session corresponds to)
- Nature of training shown/updated
- **Other Phase** concept shown when "Other Phase" is selected
- **Visit Date** — validation: cannot be a future date
- Participant details

---

### Outreach Registration (IndividualProfile — Outreach Group Subject)
**Purpose**: Registers an outreach group/event

**Key Fields**:
- **Visit Date** (UUID: `ff308558-e951-46bf-8115-c41bf16b02da`) — validation: cannot be a future date
- Location details
- Type of outreach activity

---

### Claim Registration (IndividualProfile — Claim Subject)
**Purpose**: Registers a new claim

**Key Fields**:
- Applicant/beneficiary details
- **Does the phone number belong to the applicant?** — same pattern as Case Registration (shows Name of person + Relation when No)
- **Claim Source** (UUID: `9cf2776d-8fd2-42db-8c74-dfc9433e2af1`)
- **Visit Date** (UUID: `ff308558-e951-46bf-8115-c41bf16b02da`) — validation: cannot be a future date

---

### Letter Status (ProgramEnrolment — Letter Status Program)
**Purpose**: Enrolls an Influencing State subject into Letter Status program

**Key Fields**:
- **Letter Status** (Coded, UUID: `8bda3fb7-379c-4eaa-95fb-41a13fe28796`) — answers: Initial letter filed, Follow up letter filed, Follow up RTI filed, Closed

**Validation Rule**:
- On new enrolment: Enrolment Date MUST be today's date
- On edit: Enrolment Date CANNOT be changed from the original

**Decision Rule**:
- On new enrolment: auto-captures current `Enrolment DateTime` (as `YYYY-MM-DD HH:mm:ss`)

---

### Letter Impact Encounter (ProgramEncounter — Letter Status Program)
**Purpose**: Records impact of a letter advocacy campaign

**Key Fields**:
- **Details of the impact** (QuestionGroup, repeatable):
  - **Date of impact** (mandatory per group entry)
  - **Description of Impact** (text, optional)
  - **Monetary Impact** (text, optional)

**Validation Rules**:
1. In each impact group entry: at least one of "Impact Description" OR "Monetary Impact" must be filled (if both are null, error: "Please answer either Impact Description OR Monetary Impact Question")
2. Encounter Date must be today's date (on new encounters)
3. Encounter Date cannot be changed (on edits)

---

### Case Legal Fund (Encounter — Case Subject)
**Purpose**: Records legal fund receipts for a case

**Key Fields**:
- **Fill details of the legal fund received** (QuestionGroup, repeatable):
  - **Date of receipt** (mandatory) — validation: cannot be a future date ("Invalid date: Future dates are not allowed")
  - **Amount** (Numeric, mandatory, min: 0)
  - **Stage at which taken** (Text, mandatory)
  - **Upload receipt** (File, max 1 MB, optional)
  - **Upload Image** (Image, optional)

---

### Case Fact Finding (Encounter — Case Subject)
**Purpose**: Records fact-finding visits for criminal cases

**Key Fields**:
- **Date of incident (Fact Finding)** (mandatory) — validation: no future dates
- **Date of receiving info about fact finding** (mandatory) — validation: no future dates
- **Date of fact finding** (mandatory) — validation: no future dates
- **Location of fact-finding** (Location — Village level)

---

### Victim Compensation (Encounter — Case Subject)
**Purpose**: Records victim compensation received under various schemes

**Key Fields** (active fields — many older fields are voided):
- Compensation details grouped by stage (immediate, interim, final)
- Date fields for each stage — all validated: no future dates
- Amount received fields
- Applicable schemes vary by case type

---

### Issues Identified (IndividualProfile — Issues Identified Subject)
**Purpose**: Registers systemic issues identified during fieldwork
- Standalone form, no programs or additional encounters

---

## Key Concepts

### Universal Concepts (Used Across Multiple Forms)

| Concept Name | UUID | Data Type | Purpose |
|---|---|---|---|
| Visit Date | `ff308558-e951-46bf-8115-c41bf16b02da` | Date | Common date field used in most encounters/registrations — always validated: no future dates |
| Does the phone number belong to the applicant? | `7d720c7b-7f5c-43f7-a091-6f5cff171c21` | Coded (Yes/No) | Determines if victim/person details need to be collected separately |
| Nature of Case | `252f4c55-d113-4951-8ebb-eed01b9ccbb9` | Coded | Type of legal case — drives all conditional stage visibility in Case Status |
| Status of case | `b1927aeb-ab4c-46a6-8eff-6ccdf38f5478` | Coded | Current litigation status — used with Nature of Case to show correct stage |
| Type of training | `c7afa395-baae-4434-b8f7-b938b78051bd` | Coded (Internal/External) | Controls Training form visibility (Title hidden for Internal) and encounter eligibility |
| Whether phased | `387e72d2-1ced-4032-b273-ea3ef5c5a159` | Coded (Phased/Single event) | Determines encounter type availability for Training |
| Nature of training | `302ce25a-1fe7-4c5a-9a31-e1e54009187b` | Coded | Shown for Internal training type — records the nature/topic |
| Which phase | `1732f13a-26c0-4ef9-a92b-78d65519b024` | Coded | Phase selection for phased trainings |
| Claim Source | `9cf2776d-8fd2-42db-8c74-dfc9433e2af1` | Coded | Source of the claim — used in both Case and Claim registrations |
| Whether applicant same as victim? | `8a45b281-8e39-4ea7-9e85-58dfd186275d` | Coded (Yes/No) | In Case Registration — shows victim details section when No |
| Letter Status | `8bda3fb7-379c-4eaa-95fb-41a13fe28796` | Coded | Status of letter advocacy campaign |
| Legal Fund | `c1cf21d1-5ce0-4246-ad0d-23137f8d8cdc` | QuestionGroup | Repeatable group for legal fund entries |
| Date of receipt | `c329c903-d7cd-4378-adae-b2b99eb2311f` | Date | Date of legal fund receipt — no future dates |
| Amount | `6163fe31-4acc-43bb-a9ff-bfc8d4b98259` | Numeric | Fund amount received — min 0 |
| Enrolment DateTime | `3ecdf82a-adf3-4e29-aa3f-244db1109a2d` | DateTime | Auto-captured on new enrolments (Letter Status); used to lock enrolment date on edits |
| Encounter DateTime | `1f4bc226-9e3f-42c9-a332-2d81cd8e64f7` | DateTime | Auto-captured on new encounters; used to lock encounter date on edits |
| Letter Impact Details | `6a66028e-e11c-4b47-a94d-695d1b232577` | QuestionGroup | Repeatable group for letter impact entries |
| Date of impact | `8812d295-05b7-4c0a-8b9b-3fd55ad162c7` | Date | Date of impact within Letter Impact group |
| Impact Description | `bed28fd5-e245-42d5-b547-6b100a90c1d9` | Text | Description of impact (one of Description/Monetary required) |
| Impact Monetary Letter | `35d197f1-e61c-4efe-a8a9-7d65f741edad` | Text | Monetary impact amount for Letter Impact |

### Answers to Key Coded Concepts

#### Nature of Case (`252f4c55-d113-4951-8ebb-eed01b9ccbb9`)
- Criminal prosecution fresh filing — UUID: `a3d1b65d-0e00-4e78-9cf2-0bbd29e77642`
- Criminal defence fresh filing — UUID: `0fc2f7cb-ab3e-4474-8d85-c4e40917409f`
- Civil
- Bail
- Labour
- Land
- Domestic Violence
- POCSO
- Prant Darji (Caste atrocity)
- Other

#### Status of case (`b1927aeb-ab4c-46a6-8eff-6ccdf38f5478`)
- Active (pre-litigation) — UUID: `b5d60cc0-716a-4980-ac26-13559bfb31ac`
- Active (litigation) — UUID: `df2c6f91-cf67-494c-9e85-8816918f0fed`
- Resolved
- Closed
- Client not traceable

#### Type of training (`c7afa395-baae-4434-b8f7-b938b78051bd`)
- Internal
- External

#### Whether phased (`387e72d2-1ced-4032-b273-ea3ef5c5a159`)
- Phased
- Single event

---

## Workflows

### 1. Legal Case Workflow (Case Subject)

```
Case Registration (IndividualProfile)
  ↓
Case Status Program Enrolment
  → Case Status Details (ProgramEnrolment) — records Nature of Case + initial status
  ↓
Ongoing Encounters (any order, most limited to 1 each):
  → Case Activity Register (1 only)
  → Case Documents (1 only — for document uploads)
  → Case Legal Fund (1 only — repeatable fund entries)
  → Case Monetary Impact (1 only)
  → Case Fact Finding (only for criminal case types, 1 only)
  → Victim Compensation (only for criminal case types, 1 only)
  → Case Status Details Encounter (follow-up status updates)
  ↓
Case Status Program Exit (case resolved/closed)
```

**Key Rules**:
- Auto-generates Case name: `"Case_" + applicantName + "_" + address`
- If applicant ≠ victim, collect victim's Name + Phone + Address separately
- Stage fields in Case Status Details appear conditionally based on Nature of Case + Status of case
- Date validation across all forms: no future dates

---

### 2. Influencing State Workflows

#### Letter Advocacy Workflow
```
Influencing State Registration
  ↓
Letter Status Program Enrolment
  → Letter Status form (Status: Initial letter filed / Follow up letter filed / Closed)
  → Enrolment Date locked to today on creation; cannot change on edit
  ↓
Program Encounters:
  → Follow Up Letter (ongoing follow-ups)
  → Follow Up RTI (if escalated to RTI)
  → Letter Document (1 only — document uploads)
  → Letter Impact (1 only — records impact with date + description/monetary)
  ↓
Letter Status Exit
```

#### RTI Workflow
```
Influencing State Registration
  ↓
RTI Status Program Enrolment
  ↓
Program Encounters:
  → RTI Document (1 only — document uploads)
  → RTI Impact (1 only — impact recording)
  ↓
RTI Status Exit
```

#### PIL Workflow
```
Influencing State Registration
  ↓
PIL Status Program Enrolment
  ↓
Program Encounters:
  → PIL Case Activity Register (1 only)
  → PIL Document (1 only)
  → PIL Impact (1 only)
  → PIL Legal Fund (1 only)
  ↓
PIL Status Exit
```

---

### 3. Training Workflow

```
Training Registration (IndividualProfile)
  → Set Type of training (Internal/External) — CANNOT BE CHANGED after encounters exist
  → Set Whether phased (Phased/Single event)
  → If Internal: Title of Training hidden, Nature of training shown
  ↓
If Phased:
  → If Internal: Internal Training encounters (one per phase)
  → If External: External Training encounters (one per phase)
  → Training Legal Fund (1 only — only for non-Internal type)
If Single Event:
  → One Time Training (1 only — only if no One Time Training encounter exists yet)
  → Training Legal Fund (1 only — only for non-Internal type)
```

**Key Rules**:
- `Type of training` field cannot be edited once enrolments or encounters exist
- `Title of Training` hidden when Internal training
- `Nature of training` shown only when Internal
- Visit Date in all training encounters: no future dates

---

### 4. Claim Workflow

```
Claim Registration (IndividualProfile)
  ↓
Claim Status Program Enrolment
  ↓
Encounters (each limited to 1):
  → Claim Activity Register
  → Claim Legal Fund
  → Claim Impact Form
  ↓
Claim Status Exit
```

---

### 5. Outreach Workflow

```
Outreach Registration (IndividualProfile for Group subject)
  ↓
Outreach Location Specific Details (Encounter)
  → Records location (Village or Other Space)
  → Records venue within village (school, court, government office, community space, etc.)
  → Records participants and activities covered
```

---

## Key Rules Reference

### Rule Pattern 1: No Future Date Validation
Used in: Visit Date (Case Registration, Claim Registration, Training Registration, Outreach Registration), all training encounter dates, Case Legal Fund date of receipt, Victim Compensation dates, Case Fact Finding dates

**Pattern**:
```javascript
let selectedDate = encounter.getObservationValue('<concept-uuid>');
if (selectedDate) {
  const currentDate = moment().startOf('day');
  selectedDate = moment(selectedDate).startOf('day');
  if (selectedDate.isAfter(currentDate)) {
    validationErrors.push("Invalid date: Future dates are not allowed");
  }
}
```

### Rule Pattern 2: Conditional Visibility Based on Single Answer
Used in: Victim name/phone/address (when applicant ≠ victim), Name of person (when phone doesn't belong to applicant)

**Pattern**:
```javascript
const condition11 = new imports.rulesConfig.RuleCondition({individual, formElement})
  .when.valueInRegistration("<concept-uuid>")
  .containsAnswerConceptName("No")
  .matches();
visibility = condition11;
```

### Rule Pattern 3: Conditional Stage Visibility (Two-Condition AND)
Used in: All stage fields in Case Status Details

**Pattern**:
```javascript
const condition11 = RuleCondition.when.valueInEnrolment("<nature-of-case-uuid>")
  .containsAnyAnswerConceptName("Criminal prosecution...", "Criminal defence...").matches();
const condition21 = RuleCondition.when.valueInEnrolment("<status-of-case-uuid>")
  .containsAnswerConceptName("Active (pre-litigation)").matches();
visibility = condition11 && condition21;
```

### Rule Pattern 4: Field Edit Prevention
Used in: Type of training (cannot change after encounters exist)

**Pattern**:
```javascript
const hasEnrolmentsOrEncounters = individual.enrolments.length > 0 || individual.encounters.length > 0;
if (hasEnrolmentsOrEncounters) {
  value = individual.getObservationValue("<concept-uuid>"); // Reset to existing value
}
```

### Rule Pattern 5: Hide When Condition
Used in: Title of Training (hidden when Internal)

**Pattern**:
```javascript
const condition11 = RuleCondition.when.valueInRegistration("<type-of-training-uuid>")
  .containsAnswerConceptName("Internal").matches();
visibility = !(condition11);
```

### Rule Pattern 6: Show When Condition (Positive)
Used in: Nature of training (shown when Internal)

**Pattern**:
```javascript
const condition11 = RuleCondition.when.valueInRegistration("<type-of-training-uuid>")
  .containsAnswerConceptName("Internal").matches();
visibility = condition11;
```

### Rule Pattern 7: Encounter Date Locking (Today's Date + No Edit)
Used in: Letter Status enrolment, Letter Impact encounter, and pattern followed across most CSJ encounter forms

**Pattern (Validation)**:
```javascript
const encounterDateForEditCase = entity.getObservationValue("<edit-lock-concept-uuid>");
const encounterDate = entity.encounterDateTime; // or enrolmentDateTime

if (!encounterDateForEditCase) {
  // New encounter/enrolment — date must be today
  const today = moment().startOf('day');
  const encDate = moment(encounterDate).startOf('day');
  if (!encDate.isSame(today, 'day')) {
    validationResults.push(createValidationError("Encounter Date should be today's date."));
  }
} else {
  // Edit — date cannot change
  const encDateEdit = moment(encounterDate).startOf('day');
  const encDateOriginal = moment(encounterDateForEditCase).startOf('day');
  if (!encDateEdit.isSame(encDateOriginal, 'day')) {
    validationResults.push(createValidationError("Encounter Date cannot be changed."));
  }
}
```

**Pattern (Decision)**:
```javascript
const encounterDateForEditCase = entity.getObservationValue("<edit-lock-concept-uuid>");
if (!encounterDateForEditCase) {
  let encDateTime = moment().format("YYYY-MM-DD HH:mm:ss");
  encounterDecisions.push({ name: "Encounter DateTime", value: encDateTime });
}
```

### Rule Pattern 8: QuestionGroup Validation (At Least One of Multiple Fields)
Used in: Letter Impact Encounter (Description OR Monetary Impact required per group entry)

**Pattern**:
```javascript
let documentDetails = entity.findGroupedObservation("<question-group-concept-uuid>");
if (documentDetails && documentDetails.length > 0) {
  for (let i = 0; i < documentDetails.length; i++) {
    let currentGroup = documentDetails[i];
    let field1 = currentGroup.findObservationByConceptUUID("<concept-uuid-1>");
    let field2 = currentGroup.findObservationByConceptUUID("<concept-uuid-2>");
    if ((field1 === null || field1 === undefined) && (field2 === null || field2 === undefined)) {
      validationResults.push(createValidationError('Please answer either Field1 OR Field2'));
    }
  }
}
```

### Rule Pattern 9: Auto-Name Generation (Case Subject)
Used in: Case Registration form's Applicant Details group

**Pattern**:
```javascript
const nameOfapplicant = individual.getObservationReadableValue("Name of applicant");
const addressOfapplicantUUID = individual.getObservationReadableValue("Address of Applicant");
let addressOfapplicantName = '';
const locationResults = db.objects("LocationHierarchy").filtered('uuid == $0', addressOfapplicantUUID);
if (locationResults.length > 0) {
  addressOfapplicantName = locationResults[0].name;
}
if (!nameOfapplicant || !addressOfapplicantName) {
  individual.firstName = "Case_";
  individual.name = "Case_";
} else {
  individual.firstName = "Case_" + nameOfapplicant + '_' + addressOfapplicantName;
  individual.name = "Case_" + nameOfapplicant + '_' + addressOfapplicantName;
}
```

### Rule Pattern 10: Registration Date Locking (Today's Date + No Edit)
Used in: **All Individual Profile (registration) forms** — Campaign Registration, Claim Registration, Case Registration (Visit Date), Influencing State Registration, Intern Registration, Volunteer Registration, Recognition/Award Registration, Outreach Registration, Issues Identified

**Concept**: `registrationDateForEditCase` — UUID: `7b1a1540-bfd5-484d-987f-4d6f3635a448`

**Pattern (Validation Rule on registration form)**:
```javascript
const registrationDateForEditCase = individual.getObservationValue("7b1a1540-bfd5-484d-987f-4d6f3635a448");
const registrationDate = individual.registrationDate;

if (!registrationDateForEditCase) {
  // New registration — date must be today
  const today = moment().startOf('day');
  const regDate = moment(registrationDate).startOf('day');
  if (!regDate.isSame(today, 'day')) {
    validationResults.push(createValidationError("Registration Date should be today's date."));
  }
} else {
  // Edit — date cannot change
  const regDateEdit = moment(registrationDate).startOf('day');
  const regDateOriginal = moment(registrationDateForEditCase).startOf('day');
  if (!regDateEdit.isSame(regDateOriginal, 'day')) {
    validationResults.push(createValidationError("Registration Date cannot be changed."));
  }
}
```

**Pattern (Decision Rule on registration form)**:
```javascript
const registrationDateForEditCase = individual.getObservationValue("7b1a1540-bfd5-484d-987f-4d6f3635a448");
if (!registrationDateForEditCase) {
  let regDateTime = moment().format("YYYY-MM-DD HH:mm:ss");
  registrationDecisions.push({ name: "Registration DateTime", value: regDateTime });
}
```

Note: This is the same dual-lock mechanism as Pattern 7 (Encounter Date Locking) but applied to `individual.registrationDate` and using the `registrationDateForEditCase` concept.

---

### Rule Pattern 11: User Info Capture in Decision Rule
Used in: Campaign Registration, Claim Registration (and all registrations that track who created the record)

**Purpose**: Automatically captures the logged-in user's name and UUID at the time of registration.

**Pattern**:
```javascript
const encounterDateForEditCase = entity.getObservationValue("<edit-lock-concept-uuid>");
if (!encounterDateForEditCase) {
  // Only capture on initial creation, not on edits
  const createdByName = params.user.name;
  const createdByUUID = params.user.uuid;
  registrationDecisions.push({ name: "createdByName", value: createdByName });
  registrationDecisions.push({ name: "createdByUUID", value: createdByUUID });
}
```

---

### Rule Pattern 12: "Other" Answer Specifier Visibility
Used in: Claim Registration (Source="Other" → show "Other Source, please specify"), Claim Registration (Scheme="Other" → show "Others Scheme, please specify"), Influencing State Registration (Theme="Other" → show "Other Theme, please specify"), Case Registration (Religion="Other" → show "Other Religion, please specify"), Claim Activity Register (Action="Other" → show "Other Action, please specify"), Claim Activity Register (Step="Other" → show "Other Steps, please specify"), Volunteer Registration (NGO affiliation conditional)

**Pattern**:
```javascript
const condition11 = new imports.rulesConfig.RuleCondition({individual, formElement})
  .when.valueInRegistration("<parent-concept-uuid>")
  .containsAnswerConceptName("Other")
  .matches();
visibility = condition11;
```

For encounter-based forms:
```javascript
const condition11 = new imports.rulesConfig.RuleCondition({programEncounter, formElement})
  .when.valueInEncounter("<parent-concept-uuid>")
  .containsAnswerConceptName("Other")
  .matches();
visibility = condition11;
```

---

### Rule Pattern 13: Training Date Range Validation (End Date After Start Date)
Used in: Intern Registration (End Date of Internship), One Time Training (End Date), External Training (End Date)

**Pattern**:
```javascript
const startDate = individual.getObservationReadableValue("<start-date-concept-uuid>");
const endDate = formElement.getValue();
if (startDate && endDate) {
  if (moment(endDate).isBefore(moment(startDate))) {
    validationErrors.push("End date must be after start date");
  }
}
```

---

### Rule Pattern 14: Training Computed Fields (Number of Days + Hours)
Used in: One Time Training, External Training (Number of Days, Hours fields)

**Pattern**:
```javascript
// Number of Days — auto-computed from Start Date and End Date
const startDate = individual.getObservationReadableValue("<start-date-uuid>");
const endDate = encounter.getObservationReadableValue("<end-date-uuid>");
if (startDate && endDate) {
  const days = moment(endDate).diff(moment(startDate), 'days') + 1;
  value = days;
}

// Hours — derived from End Date observation
let dateEndDateObservation = encounter.findObservation("<end-date-uuid>");
// hours computed based on date difference
```

---

### Rule Pattern 15: Gender-Based Total Computation
Used in: Influencing State Registration, One Time Training, External Training — wherever Male/Female/Other participant count fields exist

**Pattern (Total auto-computed)**:
```javascript
let noOfMales = encounter.getObservationValue("<male-uuid>");
let noOfFemales = encounter.getObservationValue("<female-uuid>");
let noOfOthers = encounter.getObservationValue("<other-uuid>");
value = (noOfMales || 0) + (noOfFemales || 0) + (noOfOthers || 0);
```

**Pattern (Individual field validation — non-negative)**:
```javascript
const selectedNumber = encounter.getObservationValue("<gender-uuid>");
if (selectedNumber && selectedNumber < 0) {
  validationErrors.push("Value cannot be negative");
}
```

---

### Rule Pattern 16: Follow-Up Date Sequence Validation
Used in: Follow Up Letter Encounter (Date of Posting → Date of Receipt by Authority → Date of Response), Follow Up RTI Encounter (similar chain)

**Pattern**:
```javascript
// Date of Receipt must be on or after Date of Posting
let dateOfPosting = encounter.getObservationValue("<date-of-posting-uuid>");
let dateOfReceipt = formElement.getValue();
if (dateOfPosting && dateOfReceipt) {
  if (moment(dateOfReceipt).isBefore(moment(dateOfPosting))) {
    validationErrors.push("Date of receipt cannot be before Date of Posting");
  }
}

// Date of Response must be on or after Date of Receipt
let receiptDate = encounter.getObservationValue("<date-of-receipt-uuid>");
let responseDate = formElement.getValue();
if (receiptDate && responseDate) {
  if (moment(responseDate).isBefore(moment(receiptDate))) {
    validationErrors.push("Date of response cannot be before Date of receipt by authority");
  }
}
```

---

### Rule Pattern 17: QuestionGroup Field Visibility (Within a Group Based on Context)
Used in: Case Activity Register (Court hearing fields shown only when "Was it a court hearing date? = Yes"), Follow Up RTI Encounter (first appeal fields shown conditionally), Influencing State Registration (section-specific fields)

**Pattern**:
```javascript
const condition11 = new imports.rulesConfig.RuleCondition({programEncounter, formElement})
  .when.valueInEncounter("<context-concept-uuid>")
  .containsAnswerConceptName("Yes")
  .matches();
visibility = condition11;
```

---

### Rule Pattern 18: Client Info Auto-Fill (Client Follow Up Encounter)
Used in: Client Follow Up Encounter — pre-fills client name, phone, and issue type from the parent enrolment

**Pattern**:
```javascript
const value = programEncounter.programEnrolment.getObservationValue("<concept-uuid>");
// Sets field value from program enrolment data
// Used for Name of client, Phone Number, Describe the Type of Issue identified
```

These fields are read-only displays — they pull existing enrolment data into the encounter for reference.

---

### Rule Pattern 19: Case Disposed Conditional Outcome Fields
Used in: Case Disposed — all outcome fields shown conditionally based on "Whether resolved in ADR or Litigation" AND Nature of Case

**Fields and their visibility conditions**:
- **Whether resolved in ADR or Litigation** — date locking only (encounter date lock)
- **Date of resolution** — visible for ADR resolution
- **Date of judgment - Civil Case Type** — visible when Litigation + Nature of Case = Civil
- **Outcome of Litigation** — visible when Litigation + Civil
- **Date of judgment: Criminal Prosecution Case Type** — visible when Litigation + Criminal prosecution
- **Outcome: Criminal Prosecution Case Type** — visible when Litigation + Criminal prosecution
- **Date of judgment: Criminal Defence Case Type** — visible when Litigation + Criminal defence
- **Outcome: Criminal Defence Case Type** — visible when Litigation + Criminal defence
- **Date of judgment Bail or HC** — visible when Litigation + Bail
- **Outcome Bail or HC Judgment** — visible when Litigation + Bail
- **Whether challenging decision?** — visible when outcome entered
- **Reason** — visible when "Whether challenging decision? = Yes"

**Pattern**:
```javascript
const condition11 = new imports.rulesConfig.RuleCondition({programEncounter, formElement})
  .when.valueInEncounter("<adr-or-litigation-uuid>")
  .containsAnswerConceptName("Litigation").matches();
const condition21 = new imports.rulesConfig.RuleCondition({programEncounter, formElement})
  .when.valueInEnrolment("<nature-of-case-uuid>")
  .containsAnswerConceptName("Civil").matches();
visibility = condition11 && condition21;
```

---

## Missing/Additional Form Documentation

### Case Activity Register (Encounter — Case Subject)
**Purpose**: Records activities taken on a case — pre-litigation and litigation activities, court dates, next steps, and deadlines

**Form Groups**:
- **Activity Details** (active group — non-repeatable)
  - **Fill the details of Action Taken** — section header
  - **Was it a court hearing date?** (Coded: Yes/No) — determines which sub-fields are shown
  - **Date** (Date) — date of activity; validation: date locking (encounter date)
  - **Action Taken** (Text/Coded) — what was done; conditional visibility
  - **Next step** (Text) — next planned action; conditional
  - **Deadline for next step** (Date) — deadline; conditional
  - **Court Date** (Date) — shown only when "Was it a court hearing date? = Yes"
  - **What happened in the court date** (Text) — shown only when court date field has a value
  - **Next Step** (Text) — what to do next after court
  - **Deadline for Next Step** (Date) — deadline for post-court next step

**Key Rules**:
- Date field uses encounter date locking pattern (Pattern 7)
- Court-specific fields (Court Date, What happened in court, Next Step after court) shown only when "Was it a court hearing date? = Yes"
- Multiple versions of Action Taken / Next Step / Deadline fields — earlier versions are voided; active versions are in "Activity Details" group

---

### Case Disposed (Encounter — Case Subject)
**Purpose**: Records the disposal/resolution of a case — whether through ADR or Litigation, outcome, dates of judgment, and whether the decision is being challenged

**Form Group**: Disposed Details (non-repeatable)

**Fields**:
- **Whether resolved in ADR or Litigation** (Coded: ADR/Litigation) — determines all subsequent field visibility
- **Date of resolution** (Date) — for ADR resolution
- **Date of judgment - Civil Case Type** (Date) — for Litigation + Civil
- **Outcome of Litigation** (Coded) — for Litigation + Civil
- **Date of judgment: Criminal Prosecution Case Type** (Date) — for Litigation + Criminal prosecution
- **Outcome: Criminal Prosecution Case Type** (Coded) — for Litigation + Criminal prosecution
- **Date of judgment: Criminal Defence Case Type** (Date) — for Litigation + Criminal defence
- **Outcome: Criminal Defence Case Type** (Coded) — for Litigation + Criminal defence
- **Date of judgment Bail or HC** (Date) — for Litigation + Bail
- **Outcome Bail or HC Judgment** (Coded) — for Litigation + Bail
- **Whether challenging decision?** (Coded: Yes/No)
- **Reason** (Text) — shown when challenging decision = Yes
- **Description of outcome** (Text, unconditional)
- **Description of strategies used** (Text, unconditional)

**Key Rules**:
- All date and outcome fields are conditional (Pattern 19)
- Encounter date locking (Pattern 7)
- Note: This form may be disabled/voided but rules still exist in the form file

---

### Client Follow Up Encounter (ProgramEncounter)
**Purpose**: Follow-up encounter for clients with ongoing issues — displays pre-filled client info from enrolment and tracks issue status

**Form Group**: Issue Details (non-repeatable)

**Fields**:
- **Name of client** (Text) — auto-filled from `programEncounter.programEnrolment` (Pattern 18)
- **Phone Number** (Text) — auto-filled from program enrolment
- **Describe the Type of Issue identified** (Text/Coded) — auto-filled from program enrolment
- **Status** (Coded) — current status of the issue
- **Do you have any more identified issues?** (Coded: Yes/No) — tracks whether more issues remain

**Key Rules**:
- Name of client, Phone Number, and Issue Type are read-only display fields pulled from the enrolment (Pattern 18)
- Separate from Case Activity Register — used for simpler follow-up tracking

---

### Follow Up Letter Encounter (ProgramEncounter — Letter Status Program)
**Purpose**: Records follow-up on letters sent to authorities

**Form Group**: Letter Details (non-repeatable)

**Fields**:
- **Date of Posting** (Date) — validation: no future dates; also validated that subsequent dates are after this
- **Applicant Name** (Text)
- **Subject matter of letter** (Text)
- **Posted to (Name of Authority)** (Text)
- **Date of receipt by authority** (Date) — must be on or after Date of Posting
- **Date of response** (Date) — must be on or after Date of Receipt by Authority

**Key Rules**:
- Encounter date locking (Pattern 7)
- Sequential date validation: Posting → Receipt → Response (Pattern 16)
- Decision Rule: auto-captures `encounterDateForEditCase` on new encounters

---

### Follow Up RTI Encounter (ProgramEncounter — RTI Status Program)
**Purpose**: Records RTI application and follow-up chain (application → first appeal → response)

**Form Groups**:
1. **RTI application** (active version — non-repeatable):
   - If RTI filed, date of posting RTI
   - Applicant Name, Subject matter, Posted to (Authority)
   - Date of receipt by authority
   - Status at end of 30 days
   - Date of response — conditional (shown when Status has value)
   - Date of rejection (if rejection) — conditional

2. **Details of first appeal** (non-repeatable):
   - Date of posting first appeal
   - Status of info after first appeal
   - Date of response — conditional
   - Date of rejection (if rejection) — conditional
   - Do you want to file a first appeal?

**Key Rules**:
- Encounter date locking (Pattern 7)
- Conditional visibility: Date of response and Date of rejection shown only when "Do you want to file a first appeal? = Yes" (Pattern 2)
- Note: An older voided "RTI application" group exists — only the active groups are used

---

### Claim Status Enrolment (ProgramEnrolment — Claim Status Program)
**Purpose**: Enrolls a Claim subject into the Claim Status program

**Key Rules**:
- Enrolment date locking: same pattern as Letter Status (Pattern 7), using `enrolmentDateForEditCase` concept UUID `3ecdf82a-adf3-4e29-aa3f-244db1109a2d`
- On new enrolment: date must be today
- On edit: date cannot change

---

### Influencing State Registration (IndividualProfile — Influencing State Subject)
**Purpose**: Registers a new Influencing State subject (letter/RTI/PIL case)

**Form Elements and Rules**:
- **Visit Date** (Date) — no future dates validation (Pattern 1)
- **Theme of Influencing State** (Coded) — conditional visibility based on enrolment type
- **Other Theme, please specify** (Text) — shown when Theme = "Other" (Pattern 12)
- **Nature of engagement** (Coded) — visibility based on active enrolments (`individual.enrolments`)
- **Other nature of engagement, please specify** (Text) — shown when engagement = "Other" (Pattern 12)
- Registration date locking (Pattern 10) — UUID: `7b1a1540-bfd5-484d-987f-4d6f3635a448`

**Influencing State also has section-specific fields** (for meetings, consultations, representations):
- **Collaborator Details** (conditional)
- **Name of the collaborator** (conditional on Collaborator Details)
- **Participants** (conditional)
- **Designations of important government functionaries** (conditional)
- **Date of the event** (conditional)
- **Mode of Consultation** (conditional)
- **Topics Covered** (conditional)
- **Male / Female / Other / Total** (participant counts — Total auto-computed, Pattern 15)
- **Title of Consultation / Objective / List of speakers** (conditional)
- **Description of representations submitted** (conditional)
- **Next steps** / **Any other relevant info** (conditional)
- **Upload Photo / Upload file** (conditional)

---

### Claim Registration (IndividualProfile — Claim Subject) — Updated
**Purpose**: Registers a new claim

**Key Fields** (with rules):
- **Visit Date** (UUID: `ff308558-e951-46bf-8115-c41bf16b02da`) — no future dates (Pattern 1)
- **Source** (Coded)
- **Other Source, please specify** (Text) — shown when Source = "Other" (Pattern 12)
- **Whether group claim?** (Coded: Yes/No)
- **Number of Total Beneficiary** (Numeric) — has a rule (visibility or computation)
- **Scheme** (Coded)
- **Others Scheme, please specify** (Text) — shown when Scheme = "Other" (Pattern 12)
- Registration date locking (Pattern 10)
- User info capture: `createdByName`, `createdByUUID` from `params.user` (Pattern 11)

---

### Training Legal Fund (Encounter — Training Subject)
**Purpose**: Records legal fund received for a training (identical structure to Case Legal Fund)

**Form Group**: Legal Fund Details (with both active and voided versions of QuestionGroup)

**Key Rules**:
- QuestionGroup validation: at least Date of Receipt required per entry (Pattern 8)
- **Date of Receipt** (Date, in QuestionGroup) — no future dates (Pattern 1)
- **Amount** (Numeric) — conditional visibility
- Encounter date locking (Pattern 7)

---

### PIL Document Encounter (ProgramEncounter — PIL Status Program)
**Purpose**: Uploads PIL documents — same structure as Case Documents / Letter Document

**Key Rules**:
- QuestionGroup validation: at least one document field required per entry (Pattern 8)
- Encounter date locking (Pattern 7)
- QuestionGroup UUID: `25beb318-696f-4496-921c-cb3a78ac7f43`

---

### RTI Document Encounter (ProgramEncounter — RTI Status Program)
**Purpose**: Uploads RTI documents

**Key Rules**:
- QuestionGroup validation: at least one document field required per entry (Pattern 8)
- Encounter date locking (Pattern 7)
- **Date of Document** field in group — no future dates validation (Pattern 1)
- QuestionGroup UUID: `62a7209d-40b2-46e9-85df-357d4e7b04b0`

---

### Claim Activity Register (Encounter — Claim Subject) — Updated
**Purpose**: Records activities/actions taken on a claim

**Key Rules**:
- Encounter date locking (Pattern 7)
- **Other Action, please specify** — shown when Action = "Other" (Pattern 12)
- **Other Steps, please specify** — shown when Step/Next Step = "Other" (Pattern 12)

---

### Outreach Registration (IndividualProfile — Outreach Group Subject) — Updated
**Purpose**: Registers an outreach event for a Group subject

**Key Rules**:
- Registration date locking (Pattern 10) — UUID `7b1a1540-bfd5-484d-987f-4d6f3635a448`
- **Visit Date** (UUID: `ff308558-e951-46bf-8115-c41bf16b02da`) — no future dates (Pattern 1); appears twice (for different sections)
- **Campaign** (Coded) — conditional visibility
- **Address Details** (conditional on location type selection)
- **Anya Sthal** (Text, "other place") — conditional
- **Outreach Address Details** (conditional)
- **If anya sthal, where did you go?** — conditional on "Anya Sthal" selected
- **Campaign Name** — filtered list based on existing campaigns (`individual` records)

---

### Issues Identified (IndividualProfile — Issues Identified Subject) — Updated
**Purpose**: Records systemic issues identified during field activities (outreach, village visits)

**Key Rules**:
- Registration date locking (Pattern 10)
- **Where did you go?** — visibility based on `isActivityHappenedInVillage` condition
- Multiple "Other ... please specify" fields (Pattern 12) for:
  - Description of place (Vishesh Samuday, Ganv ke logon ki rozgaar, places of public gathering, Mahila Baithak, place of worship, etc.)
- **What did you do?** — conditional visibility based on village selection
- **Encounter type** — conditional display
- **Visit Date** — no future dates (Pattern 1)
- **Address / Anya Sthal** — conditional fields

---

### One Time Training (Encounter — Training Subject)
**Purpose**: Records a single-event training session (for non-phased training)

**Key Rules**:
- Encounter date locking (Pattern 7) — decision rule auto-captures date
- **Other Phase, please specify** — shown when Phase = "Other" (Pattern 12)
- **End Date** — must be after Start Date (Pattern 13)
- **Number of Days** — auto-computed from Start Date and End Date (Pattern 14)
- **Hours** — computed from End Date observation (Pattern 14)
- **Topics Covered** — conditional
- **Other Topics Covered, please specify** — shown when Topics = "Other" (Pattern 12)
- **Total** (participant count) — auto-computed from Male + Female + Other (Pattern 15)

---

### External Training (Encounter — Training Subject)
**Purpose**: Records each session of an external training (for External type trainings)

**Key Rules** (same as One Time Training plus):
- Validation Rule: encounter date locking (Pattern 7) — both validation + decision rule
- **Other Phase, please specify** — shown when Phase = "Other" (Pattern 12)
- **End Date** — must be after Start Date (Pattern 13)
- **Number of Days** — auto-computed (Pattern 14)
- **Hours** — computed (Pattern 14)
- **Other Topics Covered, please specify** — shown when Topics = "Other" (Pattern 12)
- **Total** (participant count) — auto-computed (Pattern 15)

---

## Updated Key Concepts

### Additional Concepts (Supplement to Key Concepts table)

| Concept Name | UUID | Data Type | Purpose |
|---|---|---|---|
| Registration DateTime | `7b1a1540-bfd5-484d-987f-4d6f3635a448` | DateTime | Auto-captured on new registrations; used to lock registration date on edits (same mechanism as Encounter DateTime but for IndividualProfile forms) |
| createdByName | varies per form | Text | Auto-captured decision: stores the logged-in user's display name at time of registration |
| createdByUUID | varies per form | Text | Auto-captured decision: stores the logged-in user's UUID at time of registration |

---

## Important Implementation Notes

1. **Three-Tier Date Locking Pattern**: CSJ uses a dual date-locking mechanism applied at three levels:
   - **Enrolment date locking**: `enrolmentDateForEditCase` UUID `3ecdf82a-adf3-4e29-aa3f-244db1109a2d` — used in Letter Status, Claim Status enrolments
   - **Encounter date locking**: `encounterDateForEditCase` UUID `1f4bc226-9e3f-42c9-a332-2d81cd8e64f7` — used in ALL encounter forms (Letter Impact, Case Activity Register, Case Disposed, Case Documents, Case Monetary Impact, Follow Up Letter, Follow Up RTI, External Training, One Time Training, Training Legal Fund, PIL Document, RTI Document, Claim Activity Register)
   - **Registration date locking**: `registrationDateForEditCase` UUID `7b1a1540-bfd5-484d-987f-4d6f3635a448` — used in ALL IndividualProfile forms (Campaign, Claim, Case, Influencing State, Intern, Volunteer, Recognition/Award, Outreach, Issues Identified registrations)

2. **Nature of Case drives everything**: The `Nature of Case` field (`252f4c55-d113-4951-8ebb-eed01b9ccbb9`) is the most critical field — it determines which encounter types are available (Victim Compensation, Case Fact Finding), which stage fields are shown in Case Status Details, which outcome fields appear in Case Disposed, and overall case workflow.

3. **Training Type Lock**: Once a Training subject has encounters or enrolments, the `Type of training` field is effectively locked and cannot be changed. This prevents data inconsistency.

4. **One-Encounter-Per-Subject Pattern**: Most CSJ encounter types are limited to 1 per subject. The eligibility rule returns `false` once the encounter has been filled. This is the dominant pattern for document, legal fund, impact, and activity register encounters.

5. **Program-Based Influencing State**: The Letter Status, RTI Status, and PIL Status programs all belong to the same Influencing State subject type. The eligibility for each program is determined by the "Nature" of the work — Letter, RTI, or PIL respectively.

6. **Phone Number Validation**: Phone numbers across all forms follow the regex `^[6-9]\\d{9}$` — must start with 6, 7, 8, or 9 and be exactly 10 digits.

7. **Location Fields**: Most location fields are not within catchment (`isWithinCatchment: false`), allowing entry of addresses anywhere in India, not just within the operational catchment area.

8. **File Uploads**: Case Documents, Letter Document, PIL Document, RTI Document, and Legal Fund forms all include file upload fields with a max size of 1 MB.

9. **"Other" Specifier Pattern is Ubiquitous**: Nearly every Coded field with an "Other" answer has a paired "Other ... please specify" Text field that appears only when "Other" is selected (Pattern 12). This applies to: Religion, Social Category, Case Theme, Act/Offence type, Training Topics, Campaign Phase, Engagement Type, Source, Scheme, Outreach location, Visit location, and many more.

10. **Auto-Computed Fields**: Several fields are automatically computed and should not be manually editable by the user:
    - **Total participants** — sum of Male + Female + Other (Pattern 15) — used in Influencing State, One Time Training, External Training
    - **Number of Days** — computed from Start Date to End Date (Pattern 14) — used in trainings
    - **Hours** — derived from training dates (Pattern 14)
    - **Subject Name** — "Case_ApplicantName_Address" for Case subjects (Pattern 9)

11. **Claim vs Case**: Claims and Cases are separate subject types with their own programs. Claims track entitlement/compensation claims; Cases track legal proceedings. Both have Activity Register, Legal Fund, and program enrolments, but follow separate workflows.

12. **User Info Capture**: All registration forms that have a `decisionRule` capture `params.user.name` and `params.user.uuid` into `createdByName` / `createdByUUID` decision observations on first creation (Pattern 11). This is used for audit trail purposes.
