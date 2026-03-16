---
title: JavaScript Helper Functions Reference
category: javascript-rules
audience: implementer
difficulty: intermediate
priority: critical
keywords:
- helper functions
- API reference
- getObservationValue
- getAgeInYears
- rule helpers
last_updated: '2026-03-16'
task_types:
- reference
features:
- rules
technical_level:
- reference
implementation_phase:
- development
complexity: moderate
retrieval_boost: 2.0
related_topics:
- rules-introduction.md
- validation-rules.md
- common-patterns.md
estimated_reading_time: 8 minutes
version: '1.0'
---
# JavaScript Helper Functions Reference

<!-- CHUNK: tldr -->
## TL;DR

**Audience**: Rule developers, implementers, and technical teams
<!-- END CHUNK -->

<!-- CHUNK: table-of-contents -->
## 📋 Table of Contents

* [Observation Access Methods](#observation-access-methods)
  * [`getObservationReadableValue()`](#getobservationreadablevalueconceptnameoruuid-parentconceptnameoruuid)
  * [`getObservationValue()`](#getobservationvalueconceptnameoruuid-parentconceptnameoruuid)
  * [`findObservation()`](#findobservationconceptnameoruuid-parentconceptnameoruuid)
  * [`findLatestObservationInEntireEnrolment()`](#findlatestobservationinentirenrolmentconceptnameoruuid-currentencounter)
  * [`hasObservation()`](#hasobservationconceptnameoruuid)
* [Age and Time Calculation Methods](#age-and-time-calculation-methods)
  * [`getAgeInYears()`](#getageinyearsasondate-precise)
  * [`getAgeInMonths()`](#getageinmonthsasondate-precise)
  * [`getAgeInWeeks()`](#getageinweeksondate-precise)
  * [`getAge()`](#getageasondate)
* [Cancel Encounter Methods](#cancel-encounter-methods)
  * [`findCancelEncounterObservation()`](#findcancelencounterobservationconceptnameoruuid)
  * [`findCancelEncounterObservationReadableValue()`](#findcancelencounterobservationreadablevalueconceptnameoruuid)
* [Encounter Navigation Methods](#encounter-navigation-methods)
  * [`getEncounters()`](#getencountersremovecancelledencounters)
  * [`findLatestObservationFromEncounters()`](#findlatestobservationfromencountersconceptnameoruuid-currentencounter)
  * [`findLastEncounterOfType()`](#findlastencounteroftypecurrentencounter-encountertypes)
  * [`scheduledEncounters()`](#scheduledencounters)
  * [`scheduledEncountersOfType()`](#scheduledencountersoftypeencountertypename)
* [Individual and Subject Methods](#individual-and-subject-methods)
  * [`isFemale()`](#isfemale)
  * [`isMale()`](#ismale)
  * [`isPerson()`](#isperson)
  * [`isHousehold()`](#ishousehold)
  * [`isGroup()`](#isgroup)
  * [`getMobileNumber()`](#getmobilenumber)
  * [`nameString`](#namestring)
* [Location and Address Methods](#location-and-address-methods)
  * [`lowestAddressLevel`](#lowestaddresslevel)
  * [`lowestTwoLevelAddress()`](#lowesttwoleveladdressi18n)
  * [`fullAddress()`](#fulladdressi18n)
* [Relationship and Group Methods](#relationship-and-group-methods)
  * [`getRelatives()`](#getrelativesrelationname-inverse)
  * [`getRelative()`](#getrelativerelationname-inverse)
  * [`getGroups()`](#getgroups)
  * [`getGroupSubjects()`](#getgroupsubjects)
* [Validation and Status Methods](#validation-and-status-methods)
  * [`hasBeenEdited()`](#hasbeenedited)
  * [`isCancelled()`](#iscancelled)
  * [`isScheduled()`](#isscheduled)
  * [`isRejectedEntity()`](#isrejectedentity)
* [Media and Utility Methods](#media-and-utility-methods)
  * [`findMediaObservations()`](#findmediaobservations)
  * [`getProfilePicture()`](#getprofilepicture)
  * [`getEntityTypeName()`](#getentitytypename)
  * [`toJSON()`](#tojson)

***
<!-- END CHUNK -->

<!-- CHUNK: quick-reference -->
## 📊 Quick Reference

| Category             | Most Used Methods               | Purpose                             |
| -------------------- | ------------------------------- | ----------------------------------- |
| **Observations**     | `getObservationReadableValue()` | Get formatted values for display    |
| **Observations**     | `getObservationValue()`         | Get raw values for calculations     |
| **Age Calculations** | `getAgeInYears()`               | Calculate age in years              |
| **Age Calculations** | `getAgeInMonths()`              | Calculate age in months (pediatric) |
| **Encounters**       | `getEncounters()`               | Get encounter history               |
| **Individual Info**  | `isFemale()` / `isMale()`       | Gender checks                       |
| **Individual Info**  | `getMobileNumber()`             | Get contact number                  |
| **Validation**       | `hasObservation()`              | Check if data exists                |
| **Validation**       | `hasBeenEdited()`               | Check encounter completion          |

***
<!-- END CHUNK -->

<!-- CHUNK: observation-helpers -->
## Observation Access Methods

### `getObservationReadableValue(conceptNameOrUuid, parentConceptNameOrUuid)`

**Available on**: Individual, ProgramEnrolment, AbstractEncounter (Encounter, ProgramEncounter)

**Purpose**: Gets the human-readable/display value of an observation, automatically formatting based on concept type.

**Parameters**:

* `conceptNameOrUuid` (String): Name or UUID of the concept to find
* `parentConceptNameOrUuid` (String, optional): Parent concept for grouped observations

**Returns**: String, Number, Date, Array, or undefined - The readable representation of the observation value

***

```javascript
// Basic usage on different entities
const treatmentDate = programEnrolment.getObservationReadableValue("Treatment Start date");
const childWeight = programEncounter.getObservationReadableValue('Weight of Child');
const mobileNumber = individual.getObservationReadableValue('Mobile Number');

// For coded concepts - returns answer names instead of UUIDs
const status = individual.getObservationReadableValue('Treatment Status'); 
// Returns: "Completed" instead of "uuid-12345"

// With grouped observations
const systolic = encounter.getObservationReadableValue('Systolic', 'Blood Pressure');

// Null-safe usage with fallback
const value = individual.getObservationReadableValue('Optional Field') || 'Not specified';

// Date formatting example
const dueDate = programEnrolment.getObservationReadableValue("Expected Date of Delivery");
// Returns: "15/03/2024" (formatted date) instead of Date object
```

***

### `getObservationValue(conceptNameOrUuid, parentConceptNameOrUuid)`

**Available on**: Individual, ProgramEnrolment, AbstractEncounter (Encounter, ProgramEncounter)

**Purpose**: Gets the raw value of an observation without formatting.

**Parameters**:

* `conceptNameOrUuid` (String): Name or UUID of the concept to find
* `parentConceptNameOrUuid` (String, optional): Parent concept for grouped observations

**Returns**: Raw value (String, Number, Date, Array, concept UUID for coded) or undefined

***

```javascript
// Get raw values for calculations
const weight = programEncounter.getObservationValue("Weight");
const height = individual.getObservationValue("Height in cm");

// For coded concepts - returns concept UUIDs
const genderUUID = individual.getObservationValue("Gender");
// Returns: "uuid-male-concept" instead of "Male"

// Use in mathematical calculations
if (height && weight) {
    const bmi = weight / ((height / 100) * (height / 100));
}

// Date comparisons with raw dates
const dueDate = programEnrolment.getObservationValue("Expected Date of Delivery");
if (dueDate && moment().isAfter(dueDate)) {
    // Pregnancy is overdue
}

// Multi-select coded values return arrays of UUIDs
const symptoms = encounter.getObservationValue("Symptoms");
// Returns: ["fever-uuid", "cough-uuid", "headache-uuid"]
```

***

### `findObservation(conceptNameOrUuid, parentConceptNameOrUuid)`

**Available on**: Individual, AbstractEncounter (Encounter, ProgramEncounter)

**Purpose**: Finds and returns the observation object itself, allowing access to all observation properties and methods.

**Parameters**:

* `conceptNameOrUuid` (String): Name or UUID of the concept to find
* `parentConceptNameOrUuid` (String, optional): Parent concept for grouped observations

**Returns**: Observation object or undefined

***

```javascript
// Find observation object
const mobileObs = individual.findObservation('Mobile Number');
const weightObs = encounter.findObservation('Weight');

// Check existence and access properties
if (mobileObs) {
    const value = mobileObs.getValue();
    const readableValue = mobileObs.getReadableValue();
    const isAbnormal = mobileObs.isAbnormal();
}

// Using with concept UUIDs
const obs = individual.findObservation('a1b2c3d4-e5f6-7890-abcd-ef1234567890');

// Grouped observations
const systolicObs = encounter.findObservation('Systolic', 'Blood Pressure Group');

// Chain operations
const weight = encounter.findObservation('Weight')?.getValue() || 0;
```

***

### `findLatestObservationInEntireEnrolment(conceptNameOrUuid, currentEncounter)`

**Available on**: ProgramEnrolment, ProgramEncounter

**Purpose**: Finds the most recent observation for a concept across the entire program enrolment lifecycle, including all encounters.

**Parameters**:

* `conceptNameOrUuid` (String): Name or UUID of the concept to find
* `currentEncounter` (ProgramEncounter, optional): Current encounter to exclude from search

**Returns**: Observation object or undefined

***

```javascript
// Track treatment progression
const latestPhase = programEnrolment.findLatestObservationInEntireEnrolment("Treatment phase type");
if (latestPhase) {
    const currentPhase = latestPhase.getReadableValue();
}

// Monitor compliance over time
const compliance = programEnrolment.findLatestObservationInEntireEnrolment("Compliance of previous month");

// Compare with previous values (excluding current encounter)
const previousWeight = programEncounter.findLatestObservationInEntireEnrolment("Weight", programEncounter);
const currentWeight = programEncounter.getObservationValue("Weight");
if (previousWeight && currentWeight) {
    const weightChange = currentWeight - previousWeight.getValue();
}

// Historical data for decision making
const lastTestResult = programEnrolment.findLatestObservationInEntireEnrolment("Lab Test Result");
const daysSinceTest = lastTestResult ? 
    moment().diff(lastTestResult.encounterDateTime, 'days') : null;
```

***

### `hasObservation(conceptNameOrUuid)`

**Available on**: AbstractEncounter (Encounter, ProgramEncounter), ProgramEnrolment

**Purpose**: Checks if an observation exists for the given concept without retrieving the value.

**Parameters**:

* `conceptNameOrUuid` (String): Name or UUID of the concept to check

**Returns**: Boolean

***

```javascript
// Conditional logic based on data availability
if (programEnrolment.hasObservation("Comorbidity")) {
    const comorbidity = programEnrolment.getObservationReadableValue("Comorbidity");
    // Process comorbidity data
}

// Form completion validation
if (!encounter.hasObservation("Blood Pressure")) {
    validationErrors.push("Blood pressure measurement is required");
}

// Check multiple required fields
const requiredFields = ['Weight', 'Height', 'Temperature'];
const missingFields = requiredFields.filter(field => !encounter.hasObservation(field));
if (missingFields.length > 0) {
    return `Missing required fields: ${missingFields.join(', ')}`;
}
```

***
<!-- END CHUNK -->

<!-- CHUNK: age-and-time-calculation-methods -->
## Age and Time Calculation Methods

### `getAgeInYears(asOnDate, precise)`

**Available on**: Individual

**Purpose**: Calculates age in years from the individual's date of birth.

**Parameters**:

* `asOnDate` (Date, optional): Date to calculate age as of (defaults to current date)
* `precise` (Boolean, optional): Whether to use precise calculation (defaults to false)

**Returns**: Number (age in years)

***

```javascript
// Basic usage - current age
const currentAge = individual.getAgeInYears();

// Age at specific date (enrollment, encounter, etc.)
const ageAtEnrolment = individual.getAgeInYears(programEnrolment.enrolmentDateTime);
const ageAtEncounter = individual.getAgeInYears(encounter.encounterDateTime);

// Eligibility rules
return individual.isFemale() && individual.getAgeInYears() >= 15 && individual.getAgeInYears() <= 49;

// Age-based protocols
if (individual.getAgeInYears() < 18) {
    // Pediatric protocols
    return "Pediatric dosage required";
} else if (individual.getAgeInYears() >= 65) {
    // Geriatric considerations
    return "Monitor for age-related complications";
}

// Precise calculation when needed
const preciseAge = individual.getAgeInYears(moment(), true);

// Validation
if (individual.getAgeInYears() > 120) {
    return ValidationResult.failure("age", "Age seems unrealistic");
}
```

***

### `getAgeInMonths(asOnDate, precise)`

**Available on**: Individual

**Purpose**: Calculates age in months from the individual's date of birth, particularly useful for pediatric care.

**Parameters**:

* `asOnDate` (Date, optional): Date to calculate age as of (defaults to current date)
* `precise` (Boolean, optional): Whether to use precise calculation (defaults to false)

**Returns**: Number (age in months)

***

```javascript
// Basic usage for infants and children
const ageInMonths = individual.getAgeInMonths();

// Pediatric age categories
if (individual.getAgeInMonths() < 6) {
    return "Newborn (0-6 months)";
} else if (individual.getAgeInMonths() < 12) {
    return "Infant (6-12 months)";
} else if (individual.getAgeInMonths() < 24) {
    return "Toddler (12-24 months)";
}

// Immunization scheduling
const currentMonths = individual.getAgeInMonths();
if (currentMonths >= 9 && currentMonths <= 11) {
    return "9-11 month vaccinations due";
}

// Growth monitoring protocols
if (individual.getAgeInMonths() < 24) {
    return "Monthly weight monitoring required";
} else if (individual.getAgeInMonths() < 60) {
    return "Quarterly growth assessment";
}

// Nutritional guidelines
const months = individual.getAgeInMonths();
if (months >= 6 && months < 24) {
    return "Complementary feeding period";
}
```

***

### `getAgeInWeeks(asOnDate, precise)`

**Available on**: Individual

**Purpose**: Calculates age in weeks from the individual's date of birth, useful for newborn care.

**Parameters**:

* `asOnDate` (Date, optional): Date to calculate age as of (defaults to current date)
* `precise` (Boolean, optional): Whether to use precise calculation (defaults to false)

**Returns**: Number (age in weeks)

***

```javascript
// Newborn care protocols
const ageInWeeks = individual.getAgeInWeeks();

if (ageInWeeks < 2) {
    return "First 2 weeks - daily monitoring required";
} else if (ageInWeeks <= 6) {
    return "6-week pediatric checkup due";
}

// Early immunization schedule
if (ageInWeeks >= 6) {
    return "6-week vaccinations (DPT, OPV, Hepatitis B) due";
} else if (ageInWeeks >= 10) {
    return "10-week vaccinations due";
}

// Breastfeeding support
if (ageInWeeks < 26) { // Less than 6 months
    return "Exclusive breastfeeding recommended";
}
```

***

### `getAge(asOnDate)`

**Available on**: Individual

**Purpose**: Returns age as a Duration object with appropriate units, providing smart formatting.

**Parameters**:

* `asOnDate` (Date, optional): Date to calculate age as of (defaults to current date)

**Returns**: Duration object with smart unit selection

***

```javascript
// Smart age display
const ageDuration = individual.getAge();
console.log(ageDuration.toString()); // "25 years" or "8 months" or "3 weeks"

// Use in summary strings
const summary = `${individual.name}, Age: ${individual.getAge().toString()}, ${individual.gender.name}`;

// Duration object automatically chooses appropriate units:
// - Years if age > 1 year
// - Months if age < 1 year but > 0 months  
// - Zero years if age < 1 month

// Access duration properties
const age = individual.getAge();
if (age.isInYears()) {
    // Handle adult protocols
} else if (age.isInMonths()) {
    // Handle infant protocols
}
```

***
<!-- END CHUNK -->

<!-- CHUNK: encounter-helpers -->
## Cancel Encounter Methods

### `findCancelEncounterObservation(conceptNameOrUuid)`

**Available on**: AbstractEncounter (Encounter, ProgramEncounter)

**Purpose**: Finds observation from cancelled encounter data.

**Parameters**:

* `conceptNameOrUuid` (String): Name or UUID of the concept to find

**Returns**: Observation object or undefined

***

```javascript
// Find cancellation reason
const cancelReason = encounter.findCancelEncounterObservation('Cancellation reason');
if (cancelReason) {
    const reason = cancelReason.getReadableValue();
}

// Find next steps from cancelled encounter
const nextStep = programEncounter.findCancelEncounterObservation('Select next step');

// Rescheduling logic based on cancellation data
const cancelObs = encounter.findCancelEncounterObservation('Cancel reason UUID');
if (cancelObs) {
    const value = cancelObs.getValue();
    if (value === 'patient-not-available-uuid') {
        // Schedule follow-up
    }
}

// Analyze cancellation patterns
const cancelDate = encounter.findCancelEncounterObservation('Cancel date');
const cancelReason = encounter.findCancelEncounterObservation('Cancel reason');
```

***

### `findCancelEncounterObservationReadableValue(conceptNameOrUuid)`

**Available on**: AbstractEncounter (Encounter, ProgramEncounter)

**Purpose**: Gets the readable value from cancelled encounter observation.
<!-- END CHUNK -->

<!-- CHUNK: related-topics -->
## Related Topics

<!-- Add links to related documentation -->
<!-- END CHUNK -->