# Goonj Implementation - Knowledge Base

## Overview

This knowledge base documents the complete Goonj implementation in Avni. This implementation focuses on humanitarian aid distribution and community development activities, including dispatch management, distribution tracking, activity recording, demand management, village assessment, and inventory management across multiple geographies in India.

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

### 1. Demand (Individual)
- **UUID**: `360606c2-3514-4848-8e7e-8b5830325130`
- **Type**: Individual
- **Purpose**: Represents a demand/request for materials from a community or location
- **Key Features**:
  - Location-based syncing enabled
  - Sync registration concept 1: `2978117c-a297-4171-99c6-23c3522ca0f8`
  - Tracks demand status and dispatch status
  - No sub-programs

### 2. Distribution (Individual)
- **UUID**: `461abfde-8767-41f3-993e-b68599999f07`
- **Type**: Individual
- **Purpose**: Represents a distribution event where materials are distributed to beneficiaries
- **Key Features**:
  - Location-based syncing enabled
  - Sync registration concept 1: `2978117c-a297-4171-99c6-23c3522ca0f8`
  - Subject summary rule (sample/placeholder)
  - Program eligibility check rule present

### 3. Dispatch (Individual)
- **UUID**: `bc0a4ae3-77b3-4620-81c4-2d02d1c62280`
- **Type**: Individual
- **Purpose**: Represents a dispatch of materials from Goonj to a field partner location
- **Key Features**:
  - Location-based syncing enabled
  - Sync registration concept 1: `2978117c-a297-4171-99c6-23c3522ca0f8`
  - Subject summary displays "Dispatch Status Id"
  - Has "Dispatch receipt" encounter for tracking material receipt

### 4. Activity (Individual)
- **UUID**: `07d0e5b8-0dad-4469-9623-10278261f829`
- **Type**: Individual
- **Purpose**: Represents a community activity (S2S - Swachhata Se Samridhi, education, health, livelihood interventions)
- **Key Features**:
  - Location-based syncing enabled
  - Sync registration concept 1: `2978117c-a297-4171-99c6-23c3522ca0f8`
  - Tracks activity type, sub-type, participants, measurements

### 5. Inventory Item (Individual)
- **UUID**: `07df088a-7924-461d-9a9b-24a29d43813b`
- **Type**: Individual
- **Purpose**: Represents an individual item in inventory (kit, material, contributed item)
- **Key Features**:
  - Location-based syncing enabled
  - Sync registration concept 1: `41de93e4-daaf-4207-bf70-b32939d09ea5` (different from others)
  - Tracks material type, quantity, dispatch and receipt line item IDs

### 6. Village (Group)
- **UUID**: `c781319c-e47f-49f1-9ed7-7c85cd2bd16a`
- **Type**: Group
- **Purpose**: Represents a village as a group entity, containing individual members (Distribution, Activity subjects)
- **Key Features**:
  - Group subject type
  - Location-based syncing enabled
  - Complex member addition eligibility check rule:
    - Validates address match between member and group
    - Handles "Other" village/block cases using `locationMappings` or `titleLineage`
    - Compares village and block names to prevent cross-village grouping
  - Has Village Assessment Encounter

---

## Programs

No active programs in this implementation. All workflows use General Encounters (not program-based).

---

## Encounter Types

### Active Encounter Types

#### Dispatch receipt
- **UUID**: `543c3eb6-fc01-4e3a-b3e1-ef50ec6a8896`
- **Subject Type**: Dispatch
- **Eligibility Rule**:
  - Dispatch Status Id (`132868ab-...`) must NOT be defined (i.e., not yet dispatched)
  - AND Dispatch Received Date (`78f9d6cb-...`) must NOT be defined in any encounter
  - AND Dispatch Status (`b7e82e4d-...`) must equal "In Transit" in registration
- **Purpose**: Record receipt of dispatched materials at the field partner location
- **Immutable**: No

#### Village Assessment Form
- **UUID**: `770d8de1-9a52-4e54-875a-fba268a7732c`
- **Subject Type**: Village
- **Eligibility Rule**: None (always eligible)
- **Purpose**: Conduct village-level assessment capturing community details, infrastructure, demographics
- **Immutable**: No

### Voided Encounter Types (Historical)

| Name | UUID | Notes |
|------|------|-------|
| Activity (voided) | `639605f9-a202-48dd-b42f-082dc2d172ff` | Replaced by Activity Registration |
| Distribution (voided~1673) | `a29e1dbe-c894-4384-9db4-0fd2df745df8` | Required Dispatch Received Date to be defined |
| Dispatch (voided~1674) | `018267d2-9dac-4636-8458-74e98b4cb150` | Shown only when Dispatch Status Id was NOT defined |

---

## Address Level Types

The implementation uses a 4-level location hierarchy:

### Level 4: State
- **UUID**: `fda77dde-6346-47b9-84e0-25e7f171f55a`
- **Level**: 4.0
- **Parent**: None (top level)

### Level 3: District
- **UUID**: `6b0db0bd-93ad-4f54-b09a-a8f935ba4d85`
- **Level**: 3.0
- **Parent**: State

### Level 2: Block
- **UUID**: `3410e7a2-cefe-4fc7-94b4-6631656c548c`
- **Level**: 2.0
- **Parent**: District

### Level 1: Village
- **UUID**: `47a9e070-090d-46f8-8f06-834c193b8bec`
- **Level**: 1.0
- **Parent**: Block

**Note**: The implementation supports an "Other" village/block concept where users can specify a custom village or block name when the location is not in the standard hierarchy. These are stored as observations (`Other Block` UUID: `e2d35dee-c34f-4f54-a68b-f32ee81835b6`, `Other Village` UUID: `16b4db7c-e0a8-41f1-ac67-07470a762d9f`).

---

## Form Mappings

The implementation has 10 active form mappings (excluding voided ones):

### Registration Forms (IndividualProfile)

1. **Village Registration**
   - Form UUID: `c3d90e78-a3b1-43fb-8f03-96eb2463d8fe`
   - Subject Type: Village
   - Form Type: IndividualProfile

2. **Activity Registration**
   - Form UUID: `c53a160b-d245-44f6-8b47-f0c1f1dee80b`
   - Subject Type: Activity
   - Form Type: IndividualProfile

3. **Distribution Registration**
   - Form UUID: `f19d7b5b-7b8b-4b5a-aa3b-5dcd6b1b496e`
   - Subject Type: Distribution
   - Form Type: IndividualProfile

4. **Inventory Item Registration**
   - Form UUID: `52c11e75-6e11-4d12-8f42-50f83d130d93`
   - Subject Type: Inventory Item
   - Form Type: IndividualProfile

5. **Dispatch Registration**
   - Form UUID: `70bfa0ec-dc10-4e2c-8cd7-edef1b85c090`
   - Subject Type: Dispatch
   - Form Type: IndividualProfile

6. **Demand Registration**
   - Form UUID: `50623132-abbd-45df-9c92-23cdbb76323b`
   - Subject Type: Demand
   - Form Type: IndividualProfile

### General Encounter Forms (Encounter)

7. **Village Assessment Encounter Form**
   - Form UUID: `a2687eec-8161-425e-9745-e3fb0554ae3b`
   - Encounter Type: Village Assessment Form
   - Subject Type: Village
   - Form Type: Encounter

8. **Dispatch receipt form**
   - Form UUID: `57bb2d3a-f8a5-4405-8d2c-514456e91533`
   - Encounter Type: Dispatch receipt
   - Subject Type: Dispatch
   - Form Type: Encounter

### Encounter Cancellation Forms

9. **Village Form Encounter Cancellation**
   - Form UUID: `ba8a6d95-fe73-42c8-8d78-8be681344898`
   - Encounter Type: Village Assessment Form
   - Subject Type: Village
   - Form Type: IndividualEncounterCancellation

10. **Dispatch receipt Encounter Cancellation**
    - Form UUID: `ba3ee4a5-3155-49ef-9d37-4fee9744e95c`
    - Encounter Type: Dispatch receipt
    - Subject Type: Dispatch
    - Form Type: IndividualEncounterCancellation

---

## Forms Structure

### Active Forms (12 total)

**Registration Forms:**
1. `Activity Registration.json` - Activity subject registration (44 non-voided elements, 41 with rules)
2. `Demand Registration.json` - Demand subject registration (8 elements, no rules)
3. `Dispatch Registration.json` - Dispatch subject registration (26 elements, 14 with rules)
4. `Distribution Registration.json` - Distribution subject registration (54 elements, 37 with rules)
5. `Goonj Location.json` - Location form (6 elements, 1 with rule)
6. `Inventory Item Registration.json` - Inventory item registration (24 elements, 12 with rules)
7. `Village Registration.json` - Village group registration (3 elements, 3 with rules)
8. `Village Form.json` - Village simple form (5 elements, no rules)

**Encounter Forms:**
9. `Dispatch receipt form.json` - Dispatch receipt encounter (15 elements, 11 with rules)
10. `Village Assessment Encounter Form.json` - Village assessment encounter (42 elements, 21 with rules)

**Cancellation Forms:**
11. `Village Form Encounter Cancellation.json` - Village assessment cancellation (0 active elements)
12. `Dispatch receipt Encounter Cancellation.json` - Dispatch receipt cancellation (0 active elements)

### Voided Forms (10 total)
- `Activity Encounter Cancellation (voided~3735).json`
- `Activity Form (voided~3734).json`
- `Dispatch Encounter Cancellation (voided~3736).json`
- `Dispatch Form (voided~7027).json`
- `Dispatch Registration (voided~4644).json`
- `Distribution Encounter Cancellation (voided~3737).json`
- `Distribution Form (voided~3731).json`
- `Location Properties Form (voided~12171).json`
- `Test (voided~10162).json`
- `Village Assessment (voided~9597).json`

---

## Key Concepts

### Material & Dispatch Concepts
- **Material category** (`f25402e3-8d6c-4436-ba81-ad7b4f97131e`) - Kit vs. non-kit material type
- **Kit type** (`3b41522d-a009-4d64-a718-9ecf7ea7b624`) - Answer concept for "Kit" category
- **Sub type / Material sub type** (`944cb7a1-a537-4e4f-bd15-74db621abefa`) - Sub-categories of materials
- **Dispatch Status Id** (`132868ab-811a-401e-9fd3-7c87f5512436`) - Unique ID for dispatch tracking
- **Dispatch Received Date** (`78f9d6cb-356e-45dc-90d5-216185784fe6`) - Date material was received
- **Dispatch Status** (`b7e82e4d-ee4c-4a6e-bb98-7a0b4eb21392`) - Status: "In Transit", etc.
- **Materials Dispatched** (group concept UUID: `267fbb23-4168-4fb1-9bce-6b0d5f378c46`) - Repeating group for material line items
- **Quantity**, **Unit**, **Material Name**, **Kit Name**, **Kit Id**

### Activity Concepts
- **Type of initiative** (`d04d6382-91d2-468c-b45f-d3afce94cba2`) - CFW-Rahat, S2S, Education & Health, etc.
- **Activity type**, **Activity sub type**, **Activity category**
- **Activity start date** / **Activity end date** / **No of working days**
- **Number of Participants (Male/Female/Other)** - Tracked by gender
- **Tola / Mohalla** (`5e259bfe-07a8-4c88-a712-d22b9a612429`) - Local area within village
- **Other Block** (`e2d35dee-c34f-4f54-a68b-f32ee81835b6`) - Used when block is "Other"
- **Other Village** (`16b4db7c-e0a8-41f1-ac67-07470a762d9f`) - Used when village is "Other"
- **Source Id (temp field)** - Auto-populated with `individual.uuid`

### Distribution Concepts
- **Distribution date** (`cef5b862-672e-4e94-8ebc-3299a55f416f`) - Date of distribution
- **Reached to** (`a89898dd-5b9b-42dd-babc-a6b2d667ca3a`) - Individual vs. Group recipients
- **Type of disaster** - Flood, drought, etc.
- **Undertaking Form Photographs**, **Distribution Images**, **Receiver List Photographs**

### Village Assessment Concepts
- **Community type** (`fb43296b-9bbc-4cfc-9668-e9764be5ca42`) - Schedule Tribe, Migrant, etc.
- **Occupation**, **Source of Data**, **Infrastructure details**
- **Biggest Challenges Faced by the Village** (`52340496-30d3-4d2f-8c71-f29108ef5fda`)

### Location Concepts
- **Organisation name** - Auto-populated based on district/block from a predefined mapping
- **Name of Surveyor** - Auto-populated from `params.user.name`
- **Date of Survey** - Auto-populated from `encounter.encounterDateTime`

---

## Workflows

### Dispatch Workflow

1. **Dispatch Registration**: Record a dispatch of materials from Goonj HQ/collection center to a field partner. Capture dispatch ID, materials dispatched (repeating group with material type, sub-type, kit details, quantity, unit), and dispatch status.

2. **Dispatch receipt Encounter**: Record when the dispatched materials are received at the field. Triggered only when:
   - Dispatch Status Id is not yet set (not previously dispatched)
   - Dispatch Received Date not yet recorded
   - Dispatch Status is "In Transit"
   Copies material data from the dispatch registration to the receipt form.

3. **Inventory Item Registration**: Track individual inventory items received. Links to the dispatch via Dispatch Line Item Id.

### Distribution Workflow

1. **Distribution Registration**: Record a distribution of materials/aid to beneficiaries in a village. Captures:
   - Location (village, tola/mohalla, other block/village for non-standard locations)
   - Type of initiative (S2S, CFW-Rahat, CFW-NJPC, Education & Health, Specific Initiative, Vaapsi, etc.)
   - Materials distributed (inventory items)
   - Reached-to details (individual or group beneficiaries)
   - Activities conducted alongside distribution
   - Photo documentation (distribution images, receiver list, undertaking form photos)
   - Decision rule auto-populates Tola/Mohalla, Other Block, Other Village in title case

### Activity Workflow

1. **Activity Registration**: Record a community activity (S2S - Swachhata Se Samridhi, education, water management, sanitation, agriculture/plantation, etc.). Captures:
   - Location details (village, tola/mohalla, other block/village)
   - Type of initiative and sub-type
   - Activity dates and number of working days
   - Participant counts (male/female/other, with conditional visibility per initiative type)
   - Measurements (nos, length, breadth, height/depth, diameter based on measurement type)
   - Photo documentation (before/during/after implementation)
   - Decision rule auto-populates location fields in title case

### Demand Workflow

1. **Demand Registration**: Record a demand/request for materials from a community. Captures:
   - Type of disaster
   - Target community
   - Number of people
   - Account name and IDs
   - Demand Status and Dispatch Status (for tracking)

### Village Assessment Workflow

1. **Village Registration**: Register a village as a group subject. Validates uniqueness of village (prevents duplicate registration for same geographical location). Decision rule auto-populates Other Block and Other Village names in proper title case.

2. **Village Assessment Encounter**: Conduct a detailed village assessment capturing:
   - Community details (community type, SC/ST/OBC breakdown, migrant community)
   - Occupation details (top 3 occupations)
   - Infrastructure (drinking water, health facilities, NGO presence, SHGs)
   - Challenges faced by the village (ranked top 3)
   - Previous work done, work needed
   - Data source and surveyor details (auto-populated from user session)

---

## Part 2: Rules Documentation

---

## Rule Types and Structure

### 1. Form Element Rules
**Purpose**: Control visibility, set values, skip answers, and validate individual form elements

**Standard Structure**:
```javascript
'use strict';
({params, imports}) => {
  const individual = params.entity;  // or encounter, programEncounter, etc.
  const moment = imports.moment;
  const formElement = params.formElement;
  const _ = imports.lodash;
  let visibility = true;
  let value = null;
  let answersToSkip = [];
  let validationErrors = [];
  
  // Rule logic here
  
  return new imports.rulesConfig.FormElementStatus(formElement.uuid, visibility, value, answersToSkip, validationErrors);
};
```

**With RuleCondition (Declarative Style)**:
```javascript
'use strict';
({params, imports}) => {
  const individual = params.entity;
  const formElement = params.formElement;
  let visibility = true;
  let value = null;
  let answersToSkip = [];
  let validationErrors = [];
  
  const condition11 = new imports.rulesConfig.RuleCondition({individual, formElement})
    .when.valueInRegistration("CONCEPT_UUID")
    .containsAnswerConceptName("ANSWER_CONCEPT_NAME")
    .matches();
  
  visibility = condition11;
  
  return new imports.rulesConfig.FormElementStatus(formElement.uuid, visibility, value, answersToSkip, validationErrors);
};
```

### 2. Validation Rules
**Purpose**: Form-level validation across multiple fields, preventing invalid data entry

**Structure**:
```javascript
'use strict';
({params, imports}) => {
  const individual = params.entity;
  const moment = imports.moment;
  const _ = imports.lodash;
  const validationResults = [];
  const individualService = params.services.individualService;
  
  // Validation logic
  if (someCondition) {
    validationResults.push(imports.common.createValidationError("Error message here."));
  }
  
  return validationResults;
};
```

### 3. Visit Schedule Rules
**Purpose**: Schedule future encounters; **not used** in this Goonj implementation (0 visit schedule rules found).

### 4. Decision Rules
**Purpose**: Calculate or derive values and push them as decisions/observations

**Structure**:
```javascript
"use strict";
({params, imports}) => {
  const individual = params.entity;
  const moment = imports.moment;
  const decisions = params.decisions;
  const enrolmentDecisions = [];
  const encounterDecisions = [];
  const registrationDecisions = [];
  
  // Logic to build decisions
  registrationDecisions.push({name: "Concept Name", value: someValue});
  
  decisions.enrolmentDecisions.push(...enrolmentDecisions);
  decisions.encounterDecisions.push(...encounterDecisions);
  decisions.registrationDecisions.push(...registrationDecisions);
  return decisions;
};
```

---

## Common Rule Patterns

### Pattern 1: Conditional Visibility Based on Answer (containsAnswerConceptName)
**Use Case**: Show/hide a field based on whether a coded answer is selected

```javascript
'use strict';
({params, imports}) => {
  const individual = params.entity;
  const formElement = params.formElement;
  let visibility = true;
  let value = null;
  let answersToSkip = [];
  let validationErrors = [];
  
  const condition11 = new imports.rulesConfig.RuleCondition({individual, formElement})
    .when.valueInRegistration("PARENT_CONCEPT_UUID")
    .containsAnswerConceptName("ANSWER_CONCEPT_NAME")
    .matches();
  
  visibility = condition11;
  
  return new imports.rulesConfig.FormElementStatus(formElement.uuid, visibility, value, answersToSkip, validationErrors);
};
```

**Example from Dispatch Registration** — Show Kit-specific fields only when material type is "Kit":
```javascript
'use strict';
({params, imports}) => {
  const individual = params.entity;
  const formElement = params.formElement;
  let visibility = true;
  let value = null;
  let answersToSkip = [];
  let validationErrors = [];
  
  const condition11 = new imports.rulesConfig.RuleCondition({individual, formElement})
    .when.valueInRegistration("f25402e3-8d6c-4436-ba81-ad7b4f97131e", "267fbb23-4168-4fb1-9bce-6b0d5f378c46", params.questionGroupIndex)
    .containsAnswerConceptName("3b41522d-a009-4d64-a718-9ecf7ea7b624")
    .matches();
  
  visibility = condition11;
  
  return new imports.rulesConfig.FormElementStatus(formElement.uuid, visibility, value, answersToSkip, validationErrors);
};
```

---

### Pattern 2: Conditional Visibility Based on Multiple Answers (containsAnyAnswerConceptName)
**Use Case**: Show a field when any one of several answers is selected

```javascript
const condition11 = new imports.rulesConfig.RuleCondition({individual, formElement})
  .when.valueInRegistration("CONCEPT_UUID")
  .containsAnyAnswerConceptName("ANSWER_UUID_1", "ANSWER_UUID_2", "ANSWER_UUID_3")
  .matches();

visibility = condition11;
```

**Example from Distribution Registration** — Show "Type of Educational Institute" when initiative is education-related:
```javascript
'use strict';
({params, imports}) => {
  const individual = params.entity;
  const formElement = params.formElement;
  let visibility = true;
  let value = null;
  let answersToSkip = [];
  let validationErrors = [];
  
  const condition11 = new imports.rulesConfig.RuleCondition({individual, formElement})
    .when.valueInRegistration("d04d6382-91d2-468c-b45f-d3afce94cba2")
    .containsAnyAnswerConceptName(
      "4db0c307-9053-4bd4-b917-580d00e43f1d",  // Education & Health
      "9fd9d626-faf7-4833-a3ab-47ec3b4388f6",  // S2S
      "00e97494-a65b-482b-b919-aab58d52e5b8"   // other education type
    ).matches();
  
  visibility = condition11;
  
  return new imports.rulesConfig.FormElementStatus(formElement.uuid, visibility, value, answersToSkip, validationErrors);
};
```

---

### Pattern 3: Visibility Negation (NOT condition)
**Use Case**: Show a field only when a condition is NOT met (inverted logic)

```javascript
const condition11 = new imports.rulesConfig.RuleCondition({individual, formElement})
  .when.valueInRegistration("CONCEPT_UUID")
  .defined
  .matches();

visibility = !(condition11);
```

**Example from Inventory Item Registration** — Hide "Dispatch Line Item Id" if another ID is already defined:
```javascript
'use strict';
({params, imports}) => {
  const individual = params.entity;
  const formElement = params.formElement;
  let visibility = true;
  let value = null;
  let answersToSkip = [];
  let validationErrors = [];
  
  const condition11 = new imports.rulesConfig.RuleCondition({individual, formElement})
    .when.valueInRegistration("c03c7864-8fbb-4557-907a-1047092bdc37")
    .defined
    .matches();
  
  visibility = !(condition11);
  
  return new imports.rulesConfig.FormElementStatus(formElement.uuid, visibility, value, answersToSkip, validationErrors);
};
```

---

### Pattern 4: Auto-populate Value from Previous Registration Data
**Use Case**: Pre-fill a field with a value from the subject's registration or a related subject's data

```javascript
// Auto-populate from individual's own registration
const someValue = individual.getObservationReadableValue("CONCEPT_UUID");
if (someValue) {
  value = someValue;
}

// Auto-populate from related group/village subject
if (!_.isNil(params.entityContext) && !_.isNil(params.entityContext.group)) {
  value = params.entityContext.group.getObservationReadableValue("CONCEPT_UUID");
}
```

**Example from Dispatch receipt form** — Auto-populate dispatch status id from the linked dispatch subject:
```javascript
'use strict';
({params, imports}) => {
  const encounter = params.entity;
  const formElement = params.formElement;
  let visibility = false;
  let value = null;
  let answersToSkip = [];
  let validationErrors = [];
  
  const dispatchIdValue = encounter.individual.getObservationReadableValue("132868ab-811a-401e-9fd3-7c87f5512436");
  if (dispatchIdValue) {
    visibility = true;
    value = dispatchIdValue;
  }
  
  return new imports.rulesConfig.FormElementStatus(formElement.uuid, visibility, value, answersToSkip, validationErrors);
};
```

---

### Pattern 5: Auto-populate UUID as Source/Tracking ID
**Use Case**: Pre-fill a tracking field with the subject's own UUID for cross-referencing

```javascript
'use strict';
({params, imports}) => {
  const individual = params.entity;
  const formElement = params.formElement;
  let value = individual.uuid;
  return new imports.rulesConfig.FormElementStatus(formElement.uuid, true, value);
};
```

**Example from Activity Registration and Distribution Registration** — Populate "Source Id (temp field)":
```javascript
'use strict';
({params, imports}) => {
  const individual = params.entity;
  const formElement = params.formElement;
  let value = individual.uuid;
  return new imports.rulesConfig.FormElementStatus(formElement.uuid, true, value);
};
```

---

### Pattern 6: Location-Based Visibility (Other Block/Village)
**Use Case**: Show "Other Block" or "Other Village" text fields only when the registered location is "Other"

```javascript
({params, imports}) => {
  const individual = params.entity;
  const formElement = params.formElement;
  const _ = imports.lodash;
  let visibility = false;
  let value = null;
  
  const isDefined = individual && 
                    individual.lowestAddressLevel && 
                    (Array.isArray(individual.lowestAddressLevel.locationMappings) && 
                     !_.isEmpty(individual.lowestAddressLevel.locationMappings) || 
                     !_.isEmpty(individual.lowestAddressLevel.titleLineage));

  if (isDefined) {
    let block = undefined;
    
    if (Array.isArray(individual.lowestAddressLevel.locationMappings) &&
        !_.isEmpty(individual.lowestAddressLevel.locationMappings) &&
        individual.lowestAddressLevel.locationMappings[0] &&
        individual.lowestAddressLevel.locationMappings[0].parent &&
        individual.lowestAddressLevel.locationMappings[0].parent.name) {
      block = individual.lowestAddressLevel.locationMappings[0].parent.name;
    } else if (individual.lowestAddressLevel.titleLineage) {
      const titleParts = _.split(individual.lowestAddressLevel.titleLineage, ', ');
      block = titleParts.length > 2 ? titleParts[2] : undefined;
    }
    
    visibility = block === 'Other';
  }
  
  return new imports.rulesConfig.FormElementStatus(formElement.uuid, visibility, value, answersToSkip, validationErrors);
};
```

**Example from Village Registration** — Show "Other Block" field:
```javascript
'use strict';
({params, imports}) => {
  const individual = params.entity;
  const moment = imports.moment;
  const formElement = params.formElement;
  const _ = imports.lodash;
  let visibility = false;
  let value = null;
  let answersToSkip = [];
  let validationErrors = [];

  const isDefined = individual && 
                    individual.lowestAddressLevel && 
                    (Array.isArray(individual.lowestAddressLevel.locationMappings) && 
                     !_.isEmpty(individual.lowestAddressLevel.locationMappings) || 
                     !_.isEmpty(individual.lowestAddressLevel.titleLineage));
                     
  function toStartCase(str) {
    return str.toLowerCase().split(/[\s_-]+/)
      .map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ');
  }                   

  if (isDefined) {
    let block = undefined;
    
    if (Array.isArray(individual.lowestAddressLevel.locationMappings) &&
        !_.isEmpty(individual.lowestAddressLevel.locationMappings) &&
        individual.lowestAddressLevel.locationMappings[0] &&
        individual.lowestAddressLevel.locationMappings[0].parent &&
        individual.lowestAddressLevel.locationMappings[0].parent.name) {
      block = individual.lowestAddressLevel.locationMappings[0].parent.name;
    } else if (individual.lowestAddressLevel &&
               individual.lowestAddressLevel.titleLineage) {
      const titleParts = _.split(individual.lowestAddressLevel.titleLineage, ', ');
      block = titleParts.length > 2 ? titleParts[2] : undefined;
    }
    
    visibility = block === 'Other';
  }

  return new imports.rulesConfig.FormElementStatus(formElement.uuid, visibility, value, answersToSkip, validationErrors);
};
```

---

### Pattern 7: Date Validation (No Future Dates)
**Use Case**: Prevent users from entering future dates

```javascript
const condition11 = new imports.rulesConfig.RuleCondition({individual, formElement})
  .when.valueInRegistration("DATE_CONCEPT_UUID")
  .greaterThan(moment().startOf('day').toDate())
  .matches();

if (condition11) {
  validationErrors.push("Date cannot be in the future");
}
```

**Example from Distribution Registration**:
```javascript
'use strict';
({params, imports}) => {
  const individual = params.entity;
  const moment = imports.moment;
  const formElement = params.formElement;
  const _ = imports.lodash;
  let visibility = true;
  let value = null;
  let answersToSkip = [];
  let validationErrors = [];
  
  const condition11 = new imports.rulesConfig.RuleCondition({individual, formElement})
    .when.valueInRegistration("cef5b862-672e-4e94-8ebc-3299a55f416f")
    .greaterThan(moment().startOf('day').toDate())
    .matches();
  
  if (condition11) {
    validationErrors.push("Date cannot be in the future");
  }
  
  return new imports.rulesConfig.FormElementStatus(formElement.uuid, visibility, value, answersToSkip, validationErrors);
};
```

---

### Pattern 8: Skip Answers Based on Condition
**Use Case**: Filter available answer options based on other field values; particularly useful for cascading dropdowns

```javascript
const condition11 = new imports.rulesConfig.RuleCondition({individual, formElement})
  .when.valueInRegistration("CONCEPT_UUID", "GROUP_UUID", params.questionGroupIndex)
  .containsAnswerConceptName("ANSWER_NAME")
  .matches();

if (condition11) {
  _.forEach(["UUID_1", "UUID_2", "UUID_3"], (answer) => {
    const answerToSkip = formElement.getAnswerWithConceptUuid(answer);
    if (answerToSkip) answersToSkip.push(answerToSkip);
  });
}
```

**Example from Dispatch Registration** — Skip irrelevant sub-type answers based on material category:
```javascript
'use strict';
({params, imports}) => {
  const individual = params.entity;
  const formElement = params.formElement;
  const _ = imports.lodash;
  let visibility = true;
  let value = null;
  let answersToSkip = [];
  let validationErrors = [];
  
  const condition11 = new imports.rulesConfig.RuleCondition({individual, formElement})
    .when.valueInRegistration("944cb7a1-a537-4e4f-bd15-74db621abefa", "267fbb23-4168-4fb1-9bce-6b0d5f378c46", params.questionGroupIndex)
    .containsAnswerConceptName("85eda3f4-ee7c-4123-b330-77b4a7f817fd")
    .matches();
  
  if (condition11) {
    _.forEach(["04df33ce-9c6c-4424-b7a3-ee5c77d8d3e6", "05a6aa27-1676-4a29-95a3-75ad8d6fe81b"], (answer) => {
      const answerToSkip = formElement.getAnswerWithConceptUuid(answer);
      if (answerToSkip) answersToSkip.push(answerToSkip);
    });
  }
  
  visibility = true;
  return new imports.rulesConfig.FormElementStatus(formElement.uuid, visibility, value, answersToSkip, validationErrors);
};
```

---

### Pattern 9: Question Group / Repeating Group Rules
**Use Case**: Rules inside repeating group elements must use `questionGroupIndex` to evaluate the right row's data

```javascript
// Access value within a question group at the current row index
const condition11 = new imports.rulesConfig.RuleCondition({individual, formElement})
  .when.valueInRegistration("CONCEPT_UUID", "GROUP_CONCEPT_UUID", params.questionGroupIndex)
  .containsAnswerConceptName("ANSWER_NAME")
  .matches();

// Or use questionGroupValueInRegistration
const condition11 = new imports.rulesConfig.RuleCondition({individual, formElement})
  .when.questionGroupValueInRegistration("GROUP_CONCEPT_UUID", "CONCEPT_IN_GROUP_UUID", params.questionGroupIndex)
  .defined
  .matches();
```

**Example from Distribution Registration** — Show "Implementation Inventory Id" in a repeating group:
```javascript
'use strict';
({params, imports}) => {
  const individual = params.entity;
  const individualService = params.services.individualService;
  const formElement = params.formElement;
  const _ = imports.lodash;
  let visibility = true;
  let value = null;
  let answersToSkip = [];
  let validationErrors = [];
  
  const condition11 = new imports.rulesConfig.RuleCondition({individual, formElement})
    .when.questionGroupValueInRegistration(
      "ccf1fbd6-d59c-40d3-a05a-f31cd6ac2cad",
      "bafb80ac-6088-4649-8ed3-0501e1296c6e",
      params.questionGroupIndex
    ).defined.matches();
  
  visibility = condition11;
  
  return new imports.rulesConfig.FormElementStatus(formElement.uuid, visibility, value, answersToSkip, validationErrors);
};
```

---

### Pattern 10: Auto-populate from Encounter Entity (Encounter Form Rules)
**Use Case**: In encounter forms, use `encounter` (not `individual`) as the entity; access linked individual's data via `encounter.individual`

```javascript
// For encounter forms
const encounter = params.entity;

// Access registration data of the linked individual
const dispatchId = encounter.individual.getObservationReadableValue("CONCEPT_UUID");

// Access encounter-level observations
const condition11 = new imports.rulesConfig.RuleCondition({encounter, formElement})
  .when.valueInEncounter("CONCEPT_UUID")
  .containsAnswerConceptName("ANSWER_NAME")
  .matches();

// Access question group values in encounter
const condition11 = new imports.rulesConfig.RuleCondition({encounter, formElement})
  .when.questionGroupValueInEncounter("GROUP_UUID", "CONCEPT_UUID", params.questionGroupIndex)
  .defined
  .matches();
```

**Example from Dispatch receipt form** — Show kit-related fields in received material group:
```javascript
'use strict';
({params, imports}) => {
  const encounter = params.entity;
  const formElement = params.formElement;
  let visibility = true;
  let value = null;
  let answersToSkip = [];
  let validationErrors = [];
  
  const condition11 = new imports.rulesConfig.RuleCondition({encounter, formElement})
    .when.questionGroupValueInEncounter(
      "f25402e3-8d6c-4436-ba81-ad7b4f97131e",
      "5dfb2f28-b866-4442-be01-0ed451c6aad9",
      params.questionGroupIndex
    ).containsAnswerConceptName("3b41522d-a009-4d64-a718-9ecf7ea7b624").matches();
  
  visibility = condition11;
  
  return new imports.rulesConfig.FormElementStatus(formElement.uuid, visibility, value, answersToSkip, validationErrors);
};
```

---

### Pattern 11: Auto-populate from User Session
**Use Case**: Pre-fill fields with the logged-in user's name, organisation, or other user attributes

```javascript
// Auto-populate surveyor name from current user
if (!_.isNil(params.user)) {
  const name = params.user.name;
  value = name;
}
```

**Example from Village Assessment Encounter Form** — Auto-fill Name of Surveyor:
```javascript
'use strict';
({params, imports}) => {
  const encounter = params.entity;
  const formElement = params.formElement;
  const _ = imports.lodash;
  let visibility = true;
  let value = null;
  let answersToSkip = [];
  let validationErrors = [];
  
  if (!_.isNil(params.user)) {
    const name = params.user.name;
    value = name;
  }
  
  return new imports.rulesConfig.FormElementStatus(formElement.uuid, visibility, value, answersToSkip, validationErrors);
};
```

---

### Pattern 12: Auto-populate from Encounter Date
**Use Case**: Set a date field to the current encounter's date/time

```javascript
const encounterDate = encounter.encounterDateTime;
if (encounterDate) {
  value = moment(encounterDate).format('YYYY-MM-DD');
} else {
  value = moment().format('YYYY-MM-DD');
}
```

**Example from Village Assessment Encounter Form** — Auto-fill Date of Survey:
```javascript
'use strict';
({params, imports}) => {
  const encounter = params.entity;
  const moment = imports.moment;
  const formElement = params.formElement;
  const _ = imports.lodash;
  let visibility = true;
  let value = null;
  let answersToSkip = [];
  let validationErrors = [];
  
  const encounterDate = encounter.encounterDateTime;
  if (encounterDate) {
    value = moment(encounterDate).format('YYYY-MM-DD');
  } else {
    value = moment().format('YYYY-MM-DD');
  }
  
  return new imports.rulesConfig.FormElementStatus(formElement.uuid, visibility, value, answersToSkip, validationErrors);
};
```

---

### Pattern 13: Decision Rule with Title Case Transformation
**Use Case**: Auto-derive registration decisions (stored observations) from entered text, applying title case normalization

```javascript
"use strict";
({params, imports}) => {
  const individual = params.entity;
  const moment = imports.moment;
  const decisions = params.decisions;
  const registrationDecisions = [];
  
  function toStartCase(str) {
    return str
      .trim()
      .toLowerCase()
      .split(/[\s]+/)
      .map(word => word.charAt(0).toUpperCase() + word.slice(1))
      .join(' ');
  }
  
  const block = individual.getObservationReadableValue("OTHER_BLOCK_CONCEPT_UUID");
  const village = individual.getObservationReadableValue("OTHER_VILLAGE_CONCEPT_UUID");
  
  if (block) {
    registrationDecisions.push({name: "Other Block", value: toStartCase(block)});
  }
  if (village) {
    registrationDecisions.push({name: "Other Village", value: toStartCase(village)});
  }
  
  decisions.registrationDecisions.push(...registrationDecisions);
  return decisions;
};
```

**Example from Village Registration** — Normalize Other Block and Other Village:
```javascript
"use strict";
({params, imports}) => {
  const individual = params.entity;
  const moment = imports.moment;
  const decisions = params.decisions;
  const enrolmentDecisions = [];
  const encounterDecisions = [];
  const registrationDecisions = [];
  
  function toStartCase(str) {
    return str.trim().toLowerCase().split(/[\s]+/)
      .map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ');
  }
  
  const block = individual.getObservationReadableValue("e2d35dee-c34f-4f54-a68b-f32ee81835b6");
  const village = individual.getObservationReadableValue("16b4db7c-e0a8-41f1-ac67-07470a762d9f");
  
  if (block) {
    registrationDecisions.push({name: "Other Block", value: toStartCase(block)});
  }
  if (village) {
    registrationDecisions.push({name: "Other Village", value: toStartCase(village)});
  }
  
  decisions.enrolmentDecisions.push(...enrolmentDecisions);
  decisions.encounterDecisions.push(...encounterDecisions);
  decisions.registrationDecisions.push(...registrationDecisions);
  return decisions;
};
```

---

### Pattern 14: Validation Rule - Duplicate Prevention
**Use Case**: Prevent duplicate registration of the same entity (e.g., same village) using `individualService.getSubjectsInLocation`

```javascript
'use strict';
({params, imports}) => {
  const individual = params.entity;
  const moment = imports.moment;
  const _ = imports.lodash;
  const validationResults = [];
  const individualService = params.services.individualService;
  
  let existingSubjects = individualService.getSubjectsInLocation(individual.lowestAddressLevel, 'SubjectTypeName');
  
  if (existingSubjects && existingSubjects.length > 0) {
    existingSubjects = existingSubjects.filter(({voided, uuid}) => !voided && uuid !== individual.uuid);
    if (existingSubjects.length > 0) {
      validationResults.push(imports.common.createValidationError("Entity for this location already exists."));
    }
  }
  
  return validationResults;
};
```

**Example from Village Registration** — Prevent duplicate village registration:
```javascript
'use strict';
({params, imports}) => {
  const individual = params.entity;
  const moment = imports.moment;
  const _ = imports.lodash;
  const validationResults = [];
  const individualService = params.services.individualService;

  function toStartCase(str) {
    return str.trim().toLowerCase().split(/[\s]+/)
      .map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ');
  }

  const isLocationMatch = (e1, e2, location) => {
    const {uuid, name} = location;
    const loc1 = e1.getObservationReadableValue(uuid) || "";
    const loc2 = e2.getObservationReadableValue(uuid) || "";
    return toStartCase(loc1) === toStartCase(loc2);
  };

  const OtherLocations = [
    {name: "Other Block", uuid: "e2d35dee-c34f-4f54-a68b-f32ee81835b6"},
    {name: "Other Village", uuid: "16b4db7c-e0a8-41f1-ac67-07470a762d9f"}
  ];

  let villages = individualService.getSubjectsInLocation(individual.lowestAddressLevel, 'Village');

  if (villages && villages.length > 0) {
    villages = villages.filter(({voided, uuid}) => !voided && uuid !== individual.uuid);
    if (villages.length > 0) {
      let isPresent = true;
      const otherBlock = individual.getObservationReadableValue("e2d35dee-c34f-4f54-a68b-f32ee81835b6");
      const otherVillage = individual.getObservationReadableValue("16b4db7c-e0a8-41f1-ac67-07470a762d9f");
      
      if (otherBlock || otherVillage) {
        villages = villages.filter(village =>
          isLocationMatch(village, individual, OtherLocations[0]) &&
          isLocationMatch(village, individual, OtherLocations[1])
        );
        isPresent = villages.length > 0;
      }
      
      if (isPresent) {
        validationResults.push(imports.common.createValidationError("Village for specified geographical location already exists."));
      }
    }
  }

  return validationResults;
};
```

---

### Pattern 15: Organisation Auto-populate Based on District Mapping
**Use Case**: Auto-populate organisation/partner name based on the user's district, using a predefined lookup map

```javascript
'use strict';
({params, imports}) => {
  const encounter = params.entity;
  const moment = imports.moment;
  const formElement = params.formElement;
  const _ = imports.lodash;
  const user = params.user;
  let visibility = true;
  let value = null;
  
  // District → organisation mapping
  const partners = {
    "Agra": ["Gramonnati Sansthan", "Samudaik Kalyan Evam Vikas Sansthan", "Vikas Sansthan"],
    "Aligarh": ["Gramonnati Sansthan", ...],
    // ... more districts
  };
  
  // Determine district from address hierarchy or user profile
  // Then look up and set organisation value
  
  return new imports.rulesConfig.FormElementStatus(formElement.uuid, visibility, value, answersToSkip, validationErrors);
};
```

---

## All Form Element Rules

### Village Registration Form (3 rules)

**Element: Other Location Details**
```javascript
//SAMPLE RULE EXAMPLE
'use strict';
({params, imports}) => {
  const individual = params.entity;
  const formElement = params.formElement;
  individual.first_name = individual.lowestAddressLevel.name;
  const statusBuilder = new imports.rulesConfig.FormElementStatusBuilder({individual, formElement});
  const formElementValue1 = "1";
  const formElementValue2 = "1";
  const showCondition = formElementValue1 === formElementValue2;
  statusBuilder.show().whenItem(showCondition).is.truthy;
  if (!showCondition) {
    statusBuilder.validationError("Values are not equal");
  }
  return statusBuilder.build();
};
```

**Element: Other Block** — Show when block is "Other" (see Pattern 6 above)

**Element: Other Village** — Show when village is "Other"
```javascript
'use strict';
({params, imports}) => {
  const individual = params.entity;
  const formElement = params.formElement;
  const _ = imports.lodash;
  let visibility = false;
  
  const isDefined = individual && individual.lowestAddressLevel &&
    (Array.isArray(individual.lowestAddressLevel.locationMappings) &&
     !_.isEmpty(individual.lowestAddressLevel.locationMappings) ||
     !_.isEmpty(individual.lowestAddressLevel.titleLineage));

  if (isDefined) {
    let village = undefined;
    if (Array.isArray(individual.lowestAddressLevel.locationMappings) &&
        !_.isEmpty(individual.lowestAddressLevel.locationMappings) &&
        individual.lowestAddressLevel.locationMappings[0] &&
        individual.lowestAddressLevel.locationMappings[0].child &&
        individual.lowestAddressLevel.locationMappings[0].child.name) {
      village = individual.lowestAddressLevel.locationMappings[0].child.name;
    } else if (individual.lowestAddressLevel.titleLineage) {
      const titleParts = _.split(individual.lowestAddressLevel.titleLineage, ', ');
      village = titleParts.length > 3 ? titleParts[3] : undefined;
    }
    visibility = village === 'Other';
  }

  return new imports.rulesConfig.FormElementStatus(formElement.uuid, visibility);
};
```

---

### Dispatch Registration Form (14 rules — key examples)

**Element: Demand Id / Demand name** — Always hidden (visibility = false):
```javascript
'use strict';
({params, imports}) => {
  const individual = params.entity;
  const formElement = params.formElement;
  let visibility = false;
  return new imports.rulesConfig.FormElementStatus(formElement.uuid, visibility);
};
```

**Element: Kit type / Kit Name / Kit Id** — Show when material type is "Kit" in repeating group (Pattern 1 with questionGroupIndex)

**Element: Sub type** — Show with conditional answer skipping based on material type category (Pattern 8)

**Element: Quantity** — Show when material type is defined in repeating group:
```javascript
const condition11 = new imports.rulesConfig.RuleCondition({individual, formElement})
  .when.valueInRegistration("f25402e3-8d6c-4436-ba81-ad7b4f97131e", "267fbb23-4168-4fb1-9bce-6b0d5f378c46", params.questionGroupIndex)
  .defined.matches();
visibility = condition11;
```

---

### Dispatch receipt form (11 rules — key examples)

**Element: Dispatch status id** — Show and auto-populate from linked individual:
```javascript
const dispatchIdValue = encounter.individual.getObservationReadableValue("132868ab-811a-401e-9fd3-7c87f5512436");
if (dispatchIdValue) { visibility = true; value = dispatchIdValue; }
```

**Element: Received Material** — Copy materials data from dispatch registration to receipt:
```javascript
const statusBuilder = new imports.rulesConfig.FormElementStatusBuilder({encounter, formElement});
const conceptsToCopy = ['f25402e3-8d6c-4436-ba81-ad7b4f97131e', '944cb7a1-...', /* ... */];
if (encounter.individual) {
  const materialsDispatchedValue = encounter.individual.getObservationValue('267fbb23-...');
  // Copy and set value
}
```

**Element: Kit type / Kit Name / Sub type / Material Name / Unit / Quantity** — All conditionally visible based on `questionGroupValueInEncounter` (Pattern 10)

---

### Activity Registration Form (41 rules — key patterns)

**Element: Tola / Mohalla** — Auto-populate from location hierarchy:
```javascript
({params, imports}) => {
  const individual = params.entity;
  const formElement = params.formElement;
  
  const getBlockFromAddress = (address) => {
    if (!address) return "";
    if (address.locationMappings && address.locationMappings[0] &&
        address.locationMappings[0].parent && address.locationMappings[0].parent.name) {
      return address.locationMappings[0].parent.name;
    }
    if (address.titleLineage) {
      const titleParts = address.titleLineage.split(', ');
      return titleParts.length > 2 ? titleParts[2] : "";
    }
    return "";
  };
  // ... populates tola/mohalla based on address
};
```

**Element: Other Block / Other Village** — Same as Village Registration (Pattern 6); also pre-fills from `params.entityContext.group` when available

**Element: Source Id (temp field)** — Always `individual.uuid` (Pattern 5)

**Element: Number of students (Male/Female)** — Hidden when `true` (inverted condition with measurement type)

**Element: Activity start date** — Conditional validation: must be defined when certain initiative type selected

**Element: Activity end date** — Custom validation: end date must be after start date:
```javascript
let activityStartDate = individual.getObservationReadableValue("ACTIVITY_START_DATE_UUID");
// Check if end date >= start date
if (activityStartDate && value && moment(value).isBefore(moment(activityStartDate))) {
  validationErrors.push("End date must be after start date");
}
```

**Element: Measurements type / Nos / Length / Breadth / Height / Diameter** — Each has conditional visibility based on measurement type selected

**Element: Before/During/After implementation photos** — Shown based on activity type context:
```javascript
const beforeImage = individual.getObservationReadableValue("BEFORE_IMAGE_UUID");
// Show/validate based on image count restrictions per initiative type
```

---

### Distribution Registration Form (37 rules — key patterns)

**Element: Distribution date** — Date validation, no future dates (Pattern 7)

**Element: The material provided as part of Rahat?** — Shown only when initiative is "CFW-Rahat":
```javascript
const condition11 = new imports.rulesConfig.RuleCondition({individual, formElement})
  .when.valueInRegistration("d04d6382-91d2-468c-b45f-d3afce94cba2")
  .containsAnswerConceptName("54d27687-374e-4988-ad81-e4d26bf02bf3")
  .matches();
visibility = condition11;
```

**Element: Type of Educational Institute / School Name** — Shown for education-type initiatives (Pattern 2)

**Element: Type of disaster** — Shown for Rahat/disaster-related initiatives with OR conditions:
```javascript
const condition11 = new imports.rulesConfig.RuleCondition({individual, formElement})
  .when.valueInRegistration("d04d6382-91d2-468c-b45f-d3afce94cba2")
  .containsAnyAnswerConceptName("RAHAT_UUID", "OTHER_DISASTER_UUID")
  .or.when.valueInRegistration("ANOTHER_CONCEPT")
  .containsAnyAnswerConceptName("SOME_ANSWER")
  .matches();
```

**Element: Name / Gender / Father-Mother Name / Age / Phone / Occupation** (in "Reached to details" group) — All shown only when individual is selected as recipient type

**Element: Group's Name** — Shown when group is selected as recipient type

**Element: Implementation Inventory Id / Distributed to / Unit / Initial Quantity / Current Quantity / Quantity** — All in repeating inventory group using `questionGroupValueInRegistration` (Pattern 9)

**Element: Activities Done** — Shows related Activity subjects from same location:
```javascript
const OtherLocations = [
  {name: "Tola / Mohalla", uuid: "5e259bfe-07a8-4c88-a712-d22b9a612429"},
  {name: "Other Block", uuid: "e2d35dee-c34f-4f54-a68b-f32ee81835b6"},
  {name: "Other Village", uuid: "16b4db7c-e0a8-41f1-ac67-07470a762d9f"}
];
// Fetch activities in same location using individualService
```

**Element: Reports Cross Checked** — Default to "No" when not defined:
```javascript
const condition11 = new imports.rulesConfig.RuleCondition({individual, formElement})
  .when.valueInRegistration("02226c59-2e8f-4f00-b977-4f68e95856c1")
  .notDefined.matches();
if (condition11) { value = "No"; }
```

---

### Inventory Item Registration Form (12 rules — key patterns)

**Element: Material type / Material Name / Material sub category / Other material name / Unit** — Shown when material type is NOT "Kit":
```javascript
const condition11 = new imports.rulesConfig.RuleCondition({individual, formElement})
  .when.valueInRegistration("f25402e3-8d6c-4436-ba81-ad7b4f97131e")
  .containsAnswerConceptNameOtherThan("3b41522d-a009-4d64-a718-9ecf7ea7b624")
  .matches();
visibility = condition11;
```

**Element: Kit Type / Sub type** — Shown when material type IS "Kit":
```javascript
const condition11 = new imports.rulesConfig.RuleCondition({individual, formElement})
  .when.valueInRegistration("f25402e3-8d6c-4436-ba81-ad7b4f97131e")
  .containsAnswerConceptName("3b41522d-a009-4d64-a718-9ecf7ea7b624")
  .matches();
visibility = condition11;
```

**Element: Dispatch Line Item Id / Dispatch Received Status Line Item Id / Bill name** — Hidden when inventory source ID is defined (inverted condition, Pattern 3):
```javascript
const condition11 = new imports.rulesConfig.RuleCondition({individual, formElement})
  .when.valueInRegistration("c03c7864-8fbb-4557-907a-1047092bdc37")
  .defined.matches();
visibility = !(condition11);
```

**Element: Created or received - Kit** — Shows when status is "Received" or "Purchased":
```javascript
const condition11 = new imports.rulesConfig.RuleCondition({individual, formElement})
  .when.valueInRegistration("dfc56fc1-108b-421a-9fff-0801c4fde74e")
  .equals("Received").matches();
const condition21 = ... .equals("Purchased").matches();
visibility = condition11 || condition21;
```

---

### Village Assessment Encounter Form (21 rules — key patterns)

**Element: Schedule Tribe Type** — Shown when community type includes "Scheduled Tribe":
```javascript
const condition11 = new imports.rulesConfig.RuleCondition({encounter, formElement})
  .when.valueInEncounter("fb43296b-9bbc-4cfc-9668-e9764be5ca42")
  .containsAnswerConceptName("1af456ea-b84d-41d5-972d-52f134e33599")
  .matches();
visibility = condition11;
```

**Element: Other Schedule Tribe / Other Missed Out Communities / Other Occupation** — Show when "Other" is selected

**Element: Select the top three occupations** — Show with count validation (max 3):
```javascript
const condition11 = new imports.rulesConfig.RuleCondition({encounter, formElement})
  .when.valueInEncounter("c58fa8fb-606a-4714-aa5a-95b7036efaca")
  .defined.matches();
if (condition11) {
  const answer = encounter.getObservationReadableValue("c58fa8fb-606a-4714-aa5a-95b7036efaca");
  if (answer.length >= 3) {
    // Skip remaining answer options
  }
}
```

**Element: Biggest Challenges Faced by the Village (Rank Top 3)** — Similar max-3 selection validation

**Element: Source of Data** — Max 2 selections validation

**Element: Name of Surveyor** — Auto-populated from `params.user.name` (Pattern 11)

**Element: Date of Survey** — Auto-populated from `encounter.encounterDateTime` (Pattern 12)

**Element: Organisation name** — Auto-populated from district-based partner mapping (Pattern 15)

---

## Helper Functions and Libraries

### Available Imports

#### 1. Moment.js (Date/Time Manipulation)
```javascript
const moment = imports.moment;

// Common operations
moment().startOf('day').toDate()         // Today at midnight
moment().add(7, 'days').toDate()         // 7 days from now
moment(date).format('YYYY-MM-DD')        // Format date
moment(date1).isBefore(moment(date2))    // Date comparison
moment(date).diff(moment(), 'days')      // Difference in days
```

#### 2. Lodash (Utility Functions)
```javascript
const _ = imports.lodash;

_.isNil(value)                           // Check null or undefined
_.isEmpty(array)                         // Check empty array/object
_.forEach(array, (item) => { ... })      // Iterate array
_.find(array, condition)                 // Find item in array
_.filter(array, condition)               // Filter array
_.split(string, delimiter)              // Split string
_.get(object, path, default)            // Safe property access
```

#### 3. RulesConfig (Avni-specific)
```javascript
const rulesConfig = imports.rulesConfig;

// RuleCondition - declarative condition builder
new rulesConfig.RuleCondition({individual, formElement})
  .when.valueInRegistration("CONCEPT_UUID")
  .containsAnswerConceptName("ANSWER_NAME")
  .matches()

// FormElementStatus - return value for form element rules
new rulesConfig.FormElementStatus(formElement.uuid, visibility, value, answersToSkip, validationErrors)

// FormElementStatusBuilder - alternative builder pattern
const statusBuilder = new rulesConfig.FormElementStatusBuilder({individual, formElement});
statusBuilder.show().whenItem(condition).is.truthy;
statusBuilder.validationError("message");
statusBuilder.build()
```

#### 4. Available Services
```javascript
// individualService - access subjects and location data
const individualService = params.services.individualService;
individualService.getSubjectsInLocation(addressLevel, 'SubjectTypeName')
```

### RuleCondition Methods Reference

| Method | Description | Example |
|--------|-------------|---------|
| `.valueInRegistration("uuid")` | Check value from individual's registration | Subject-level concept |
| `.valueInRegistration("concept", "group", groupIndex)` | Value within a question group row | Repeating group |
| `.valueInEncounter("uuid")` | Check value from current encounter | Encounter-level concept |
| `.questionGroupValueInRegistration("group", "concept", index)` | Check question group value | Repeating group in registration |
| `.questionGroupValueInEncounter("group", "concept", index)` | Check question group value in encounter | Repeating group in encounter |
| `.latestValueInAllEncounters("uuid")` | Latest value across all encounters | Historical value |
| `.containsAnswerConceptName("name")` | Check if coded answer is selected | Single-select or multi-select |
| `.containsAnyAnswerConceptName("n1","n2")` | Check if any answer is selected | Multi-condition check |
| `.containsAnswerConceptNameOtherThan("name")` | Exclude a specific answer | Inverse matching |
| `.defined` | Check if value is not null/empty | Existence check |
| `.notDefined` | Check if value is null/empty | Absence check |
| `.equals("value")` | Exact text match | Text/coded value |
| `.greaterThan(value)` | Numeric/date greater than | Date validation |
| `.lessThanOrEqualTo(value)` | Numeric/date less than or equal | Range check |
| `.or` | Combine conditions with OR | Multi-condition |
| `.and` | Combine conditions with AND (default) | Multi-condition |
| `.matches()` | Execute and return boolean | End of chain |

### Entity Methods Reference

#### Individual (Registration/Subject)
```javascript
individual.uuid                                          // Subject's UUID
individual.getObservationValue("CONCEPT_UUID")           // Get coded/numeric value
individual.getObservationReadableValue("CONCEPT_UUID")   // Get human-readable value
individual.lowestAddressLevel                            // Address level object
individual.lowestAddressLevel.name                       // Village/location name
individual.lowestAddressLevel.titleLineage               // Full "State, District, Block, Village"
individual.lowestAddressLevel.locationMappings           // Array of parent-child location mappings
individual.registrationDate                              // Date of registration
individual.groups                                        // Array of groups this individual belongs to
```

#### Encounter (General Encounter)
```javascript
encounter.individual                                     // Linked individual/subject
encounter.encounterDateTime                              // Date/time of encounter
encounter.findObservation("CONCEPT_UUID")               // Find observation object
encounter.getObservationReadableValue("CONCEPT_UUID")   // Get readable value
encounter.individual.getObservationReadableValue("CONCEPT_UUID") // From linked subject
```

#### params Object
```javascript
params.entity              // Current entity (individual, encounter, etc.)
params.formElement         // Current form element being evaluated
params.questionGroupIndex  // Index of current row in a repeating group
params.entityContext        // Context including group, affiliatedGroups etc.
params.entityContext.group  // The group subject if individual is a member
params.services             // Available services (individualService, etc.)
params.user                 // Current logged-in user
params.user.name            // User's display name
params.user.username        // User's login username
```

---

## Best Practices

### 1. Always Handle Null/Undefined Checks
```javascript
// Good - check before accessing nested properties
const isDefined = individual && 
                  individual.lowestAddressLevel && 
                  !_.isNil(individual.lowestAddressLevel.name);

// Also good - use _.isNil
if (!_.isNil(params.user)) {
  value = params.user.name;
}

// Avoid - direct access without null check
const name = individual.lowestAddressLevel.locationMappings[0].parent.name; // Can throw!
```

### 2. Use questionGroupIndex for Repeating Groups
```javascript
// Good - use questionGroupIndex for repeating group context
new imports.rulesConfig.RuleCondition({individual, formElement})
  .when.valueInRegistration("CONCEPT_UUID", "GROUP_UUID", params.questionGroupIndex)
  .defined.matches();

// Wrong - omitting group context returns wrong result in repeating groups
new imports.rulesConfig.RuleCondition({individual, formElement})
  .when.valueInRegistration("CONCEPT_UUID")
  .defined.matches();
```

### 3. Initialize All Variables Before Logic
```javascript
// Good - always initialize
let visibility = true;
let value = null;
let answersToSkip = [];
let validationErrors = [];

// Then apply conditions
if (condition) { visibility = false; }
```

### 4. Use containsAnswerConceptNameOtherThan for Inverse Answer Matching
```javascript
// Good - show field for everything EXCEPT "Kit"
const condition11 = new imports.rulesConfig.RuleCondition({individual, formElement})
  .when.valueInRegistration("CATEGORY_UUID")
  .containsAnswerConceptNameOtherThan("3b41522d-a009-4d64-a718-9ecf7ea7b624")
  .matches();

// Verbose alternative (avoid)
const isKit = ... .containsAnswerConceptName("3b41522d-...").matches();
visibility = !isKit;
```

### 5. Keep Decision Rules Simple and Focused
```javascript
// Good - each decision rule pushes to appropriate decisions array
decisions.registrationDecisions.push(...registrationDecisions);
decisions.encounterDecisions.push(...encounterDecisions);
decisions.enrolmentDecisions.push(...enrolmentDecisions);
return decisions;

// Ensure you always return decisions, never return null
```

### 6. Use toStartCase Helper for Text Normalization
```javascript
// Good - normalize user-entered text to title case
function toStartCase(str) {
  return str.trim().toLowerCase().split(/[\s]+/)
    .map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ');
}

const value = toStartCase(individual.getObservationReadableValue("CONCEPT_UUID"));
```

### 7. Access Location Hierarchy Safely (locationMappings vs titleLineage)
```javascript
// Good - try locationMappings first, fall back to titleLineage
let block = undefined;

if (Array.isArray(address.locationMappings) &&
    !_.isEmpty(address.locationMappings) &&
    address.locationMappings[0]?.parent?.name) {
  block = address.locationMappings[0].parent.name;
} else if (address.titleLineage) {
  const parts = address.titleLineage.split(', ');
  // titleLineage format: "State, District, Block, Village"
  block = parts.length > 2 ? parts[2] : undefined;
}
```

### 8. For Encounter Forms, Use Correct Entity Variable Name
```javascript
// For Encounter forms - use 'encounter'
'use strict';
({params, imports}) => {
  const encounter = params.entity;  // ✅ Correct for Encounter forms
  const condition11 = new imports.rulesConfig.RuleCondition({encounter, formElement})
    .when.valueInEncounter("UUID").defined.matches();
};

// For Registration/IndividualProfile forms - use 'individual'
'use strict';
({params, imports}) => {
  const individual = params.entity;  // ✅ Correct for IndividualProfile forms
  const condition11 = new imports.rulesConfig.RuleCondition({individual, formElement})
    .when.valueInRegistration("UUID").defined.matches();
};
```

### 9. Use services.individualService for Cross-Subject Lookups
```javascript
// Good - use available service for looking up subjects in location
const individualService = params.services.individualService;
let subjects = individualService.getSubjectsInLocation(individual.lowestAddressLevel, 'Village');
subjects = subjects.filter(({voided, uuid}) => !voided && uuid !== individual.uuid);
```

### 10. Validate Image Counts with Object-Based Restrictions
```javascript
// Good - use a lookup map to define per-type image restrictions
const imagerestriction = {
  "CFW-Rahat": 2,
  "CFW-NJPC": 2,
  "S2S": null,  // null = no restriction
  "Specific Initiative": 2
};

const initiativeType = individual.getObservationReadableValue("TYPE_CONCEPT_UUID");
const maxImages = imagerestriction[initiativeType];
const currentImages = individual.getObservationReadableValue("IMAGE_CONCEPT_UUID");

if (maxImages && currentImages && currentImages.length > maxImages) {
  validationErrors.push(`Maximum ${maxImages} images allowed for ${initiativeType}`);
}
```

---

## Usage Guidelines

### When to Use Each Rule Type

| Rule Type | Use When |
|-----------|----------|
| **Form Element Rule** | Show/hide a single field; set a field's default value; skip answer options in a coded field; validate a single field in context of other fields |
| **Validation Rule** | Cross-form validation; duplicate prevention (checking other subjects); complex business logic that spans multiple fields; uniqueness constraints |
| **Visit Schedule Rule** | *Not used in Goonj implementation* — would be used to schedule follow-up encounters |
| **Decision Rule** | Auto-calculate derived values from user input; normalize and store text in title case; push computed data as observations for reporting |

### Rule Scope Reference

| Form Type | Entity Variable | Method Prefix |
|-----------|-----------------|---------------|
| `IndividualProfile` | `individual` | `valueInRegistration`, `questionGroupValueInRegistration` |
| `Encounter` | `encounter` | `valueInEncounter`, `questionGroupValueInEncounter` |
| `ProgramEncounter` | `programEncounter` | `valueInEncounter`, `latestValueInProgramEncounters` |
| `ProgramEnrolment` | `programEnrolment` | `valueInEnrolment` |

---

## Rule Statistics

| Rule Type | Count |
|-----------|-------|
| Form Element Rules (non-voided) | 140 |
| Validation Rules | 1 |
| Visit Schedule Rules | 0 |
| Decision Rules | 3 |
| **Total** | **144** |

---

## Metadata

- **Organization**: Goonj
- **Platform**: Avni / OpenCHS
- **Focus Areas**: Humanitarian aid dispatch, material distribution, community activities (S2S, CFW, Education & Health, Specific Initiative, Vaapsi), demand management, village assessment, inventory management
- **Implementation Type**: Supply chain and community development tracking (non-health domain)
- **No Programs**: All workflows use General Encounters (not program-based)
- **Last Updated**: March 2026
- **Total Forms**: 12 active, 10 voided
- **Subject Types**: 6 (Demand, Distribution, Dispatch, Activity, Inventory Item, Village)
- **Total Active Rules**: 144
- **Dify Chunking**: Delimiter `\n\n`, Max chunk 1000 chars, Overlap 150 chars
