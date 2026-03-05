---
title: Helper Functions Reference Guide
excerpt: >-
  Complete structured reference for all JavaScript methods that can be used
  while writing rules in Avni.
---
**Audience**: Rule developers, implementers, and technical teams

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

## Cancel Encounter Methods

> ⚠️ **CRITICAL for Visit Schedule Rules**: When writing rules for `ProgramEncounterCancellation` or `IndividualEncounterCancellation` form types, you MUST use the methods below. `cancelDateTime` and `getCancelReason()` are **deprecated and will fail**.

### Quick Reference — Cancellation Rules

| What you need | ✅ CORRECT | ❌ WRONG (deprecated) |
|---|---|---|
| Cancellation reason | `entity.findCancelEncounterObservationReadableValue("Cancellation reason")` | `entity.getCancelReason()` |
| Cancellation date | `entity.findCancelEncounterObservation("Cancel date").getValue()` | `entity.cancelDateTime` |
| Cancel date with fallback | `cancelDateObs ? cancelDateObs.getValue() : entity.encounterDateTime` | — |

### Form Type → Entity and Builder Init

| Form Type | Entity variable | VisitScheduleBuilder init |
|---|---|---|
| ProgramEncounterCancellation | `programEncounter = params.entity` | `{ programEncounter }` |
| IndividualEncounterCancellation | `encounter = params.entity` | `{ encounter }` |

> **Note**: Do NOT add a program exit guard (`programEnrolment.programExitDateTime`) in cancellation rules.

---

### `findCancelEncounterObservation(conceptNameOrUuid)`

**Available on**: AbstractEncounter (Encounter, ProgramEncounter)

**Purpose**: Finds observation from cancelled encounter data.

**Parameters**:

* `conceptNameOrUuid` (String): Name or UUID of the concept to find

**Returns**: Observation object or undefined

***

```javascript
// Get cancellation date (CORRECT pattern — never use entity.cancelDateTime)
const cancelDateObs = programEncounter.findCancelEncounterObservation("Cancel date");
const cancellationDate = cancelDateObs ? cancelDateObs.getValue() : programEncounter.encounterDateTime;

// Same for IndividualEncounterCancellation
const cancelDateObs = encounter.findCancelEncounterObservation("Cancel date");
const cancellationDate = cancelDateObs ? cancelDateObs.getValue() : encounter.encounterDateTime;

// Find next steps from cancelled encounter
const nextStep = programEncounter.findCancelEncounterObservation('Select next step');
if (nextStep) {
    const value = nextStep.getValue();
}
```

***

### `findCancelEncounterObservationReadableValue(conceptNameOrUuid)`

**Available on**: AbstractEncounter (Encounter, ProgramEncounter)

**Purpose**: Gets the readable value from cancelled encounter observation.

**Parameters**:

* `conceptNameOrUuid` (String): Name or UUID of the concept to find

**Returns**: String (readable value) or undefined

***

```javascript
// Get cancellation reason (CORRECT pattern — never use getCancelReason())
// ProgramEncounterCancellation
const cancellationReason = programEncounter.findCancelEncounterObservationReadableValue("Cancellation reason");

// IndividualEncounterCancellation
const cancellationReason = encounter.findCancelEncounterObservationReadableValue("Cancellation reason");

// Conditional rescheduling logic
if (cancellationReason === 'Patient not available') {
    return { name: "Follow-up Visit", earliestDate: moment().add(3, 'days').toDate(), maxDate: moment().add(7, 'days').toDate() };
} else if (cancellationReason === 'Medical emergency') {
    return { name: "Emergency Follow-up", earliestDate: moment().add(1, 'day').toDate(), maxDate: moment().add(2, 'days').toDate() };
}
```

---

### Full Working Examples — Cancellation Visit Schedule Rules

#### ProgramEncounterCancellation — reason-based branching

```javascript
"use strict";
({ params, imports }) => {
  const programEncounter = params.entity;
  const scheduleBuilder = new imports.rulesConfig.VisitScheduleBuilder({ programEncounter });
  const moment = imports.moment;

  const cancellationReason = programEncounter.findCancelEncounterObservationReadableValue("Cancellation reason");
  const cancelDateObs = programEncounter.findCancelEncounterObservation("Cancel date");
  const cancellationDate = cancelDateObs ? cancelDateObs.getValue() : programEncounter.encounterDateTime;

  if (cancellationReason === 'Patient Unwell') {
    const earliestDate = moment(cancellationDate).add(3, 'days').toDate();
    scheduleBuilder.add({ name: "Urgent Follow Up", encounterType: "Urgent Follow Up", earliestDate, maxDate: moment(earliestDate).add(3, 'days').toDate() });
  } else {
    const earliestDate = moment(cancellationDate).add(2, 'weeks').toDate();
    scheduleBuilder.add({ name: "Routine Follow Up", encounterType: "Routine Follow Up", earliestDate, maxDate: moment(earliestDate).add(1, 'week').toDate() });
  }

  return scheduleBuilder.getAll();
};
```

#### IndividualEncounterCancellation — reason-based branching

```javascript
"use strict";
({ params, imports }) => {
  const encounter = params.entity;
  const scheduleBuilder = new imports.rulesConfig.VisitScheduleBuilder({ encounter });
  const moment = imports.moment;

  const cancellationReason = encounter.findCancelEncounterObservationReadableValue("Cancellation reason");
  const cancelDateObs = encounter.findCancelEncounterObservation("Cancel date");
  const cancellationDate = cancelDateObs ? cancelDateObs.getValue() : encounter.encounterDateTime;

  if (cancellationReason === 'Severe Reaction') {
    scheduleBuilder.add({ name: "Emergency Care", encounterType: "Emergency Care", earliestDate: moment(cancellationDate).toDate(), maxDate: moment(cancellationDate).add(4, 'hours').toDate() });
  } else {
    const earliestDate = moment(cancellationDate).add(1, 'week').toDate();
    scheduleBuilder.add({ name: "Consultation Follow Up", encounterType: "Consultation Follow Up", earliestDate, maxDate: moment(earliestDate).add(1, 'week').toDate() });
  }

  return scheduleBuilder.getAll();
};
```

***

## Encounter Navigation Methods

### `getEncounters(removeCancelledEncounters)`

**Available on**: Individual, ProgramEnrolment

**Purpose**: Retrieves encounters sorted by date (most recent first), with option to exclude cancelled encounters.

**Parameters**:

* `removeCancelledEncounters` (Boolean):
  * `true` - Return only completed encounters
  * `false` - Return all encounters including cancelled ones

**Returns**: Array of Encounter/ProgramEncounter objects sorted by encounter date (descending)

***

```javascript
// Get completed encounters only
const completedEncounters = individual.getEncounters(true);
const completedProgramEncounters = programEnrolment.getEncounters(true);

// Get all encounters including cancelled
const allEncounters = individual.getEncounters(false);

// Find most recent encounter
const latestEncounter = individual.getEncounters(true)[0];

// Filter by encounter type
const ancEncounters = individual.getEncounters(true)
    .filter(enc => enc.encounterType.name === 'ANC');

// Count encounters
const visitCount = programEnrolment.getEncounters(true).length;

// Find encounters in date range
const recentEncounters = individual.getEncounters(true)
    .filter(enc => moment(enc.encounterDateTime).isAfter(moment().subtract(30, 'days')));

// Check if any encounters exist
if (individual.getEncounters(true).length === 0) {
    return "No completed visits found";
}
```

***

### `findLatestObservationFromEncounters(conceptNameOrUuid, currentEncounter)`

**Available on**: Individual

**Purpose**: Finds the latest observation for a concept from all individual encounters (across all programs).

**Parameters**:

* `conceptNameOrUuid` (String): Name or UUID of the concept to find
* `currentEncounter` (Encounter, optional): Current encounter to exclude from search

**Returns**: Observation object or undefined

***

```javascript
// Find latest vital signs across all visits
const latestBP = individual.findLatestObservationFromEncounters('Blood Pressure');
const latestWeight = individual.findLatestObservationFromEncounters('Weight');

// Exclude current encounter from search
const previousWeight = individual.findLatestObservationFromEncounters('Weight', currentEncounter);
const currentWeight = currentEncounter.getObservationValue('Weight');

if (previousWeight && currentWeight) {
    const weightChange = currentWeight - previousWeight.getValue();
    if (weightChange > 5) {
        return "Significant weight gain since last visit";
    }
}

// Cross-program data access
const techStatus = individual.findLatestObservationFromEncounters('Tech Mahindra Status');
const statusValue = techStatus ? techStatus.getReadableValue() : "No previous status";

// Trend analysis
const latestHbA1c = individual.findLatestObservationFromEncounters('HbA1c');
if (latestHbA1c) {
    const daysSinceTest = moment().diff(latestHbA1c.encounterDateTime, 'days');
    if (daysSinceTest > 90) {
        return "HbA1c test overdue (last test " + daysSinceTest + " days ago)";
    }
}
```

***

### `findLastEncounterOfType(currentEncounter, encounterTypes)`

**Available on**: Individual

**Purpose**: Finds the most recent encounter of specified types before the current encounter.

**Parameters**:

* `currentEncounter` (Encounter): Current encounter to exclude from search
* `encounterTypes` (Array): Array of encounter type names to search for

**Returns**: Encounter object or undefined

***

```javascript
// Find last ANC visit
const lastANC = individual.findLastEncounterOfType(currentEncounter, ['ANC']);

// Find last follow-up of any type
const lastFollowUp = individual.findLastEncounterOfType(currentEncounter, 
    ['Follow-up 1', 'Follow-up 2', 'Follow-up 3']);

// Calculate interval between visits
if (lastANC) {
    const daysSinceLastVisit = moment(currentEncounter.encounterDateTime)
        .diff(lastANC.encounterDateTime, 'days');
    
    if (daysSinceLastVisit > 28) {
        return "Visit interval exceeded recommended 4 weeks";
    }
}

// Access data from previous visit
if (lastFollowUp) {
    const previousCompliance = lastFollowUp.getObservationReadableValue('Treatment Compliance');
    const currentCompliance = currentEncounter.getObservationReadableValue('Treatment Compliance');
    
    if (previousCompliance === 'Good' && currentCompliance === 'Poor') {
        return "Compliance has declined since last visit";
    }
}
```

***

### `scheduledEncounters()`

**Available on**: Individual

**Purpose**: Gets all scheduled encounters that haven't been completed or cancelled.

**Returns**: Array of scheduled encounters

***

```javascript
// Check for pending visits
const pendingVisits = individual.scheduledEncounters();

// Count overdue visits
const overdueVisits = individual.scheduledEncounters()
    .filter(enc => moment().isAfter(enc.maxVisitDateTime));

if (overdueVisits.length > 0) {
    return `${overdueVisits.length} visits are overdue`;
}

// Find next due visit
const nextVisit = individual.scheduledEncounters()
    .sort((a, b) => a.earliestVisitDateTime - b.earliestVisitDateTime)[0];

if (nextVisit) {
    const daysUntilDue = moment(nextVisit.earliestVisitDateTime).diff(moment(), 'days');
    return `Next visit due in ${daysUntilDue} days`;
}
```

***

### `scheduledEncountersOfType(encounterTypeName)`

**Available on**: Individual

**Purpose**: Gets scheduled encounters of a specific type.

**Parameters**:

* `encounterTypeName` (String): Name of the encounter type to filter by

**Returns**: Array of scheduled encounters of the specified type

***

```javascript
// Check for scheduled ANC visits
const scheduledANC = individual.scheduledEncountersOfType('ANC');

// Check if delivery is scheduled
const scheduledDelivery = individual.scheduledEncountersOfType('Delivery');
if (scheduledDelivery.length > 0) {
    const deliveryDue = moment(scheduledDelivery[0].earliestVisitDateTime);
    return `Delivery scheduled for ${deliveryDue.format('DD/MM/YYYY')}`;
}

// Immunization scheduling
const scheduledVaccination = individual.scheduledEncountersOfType('Vaccination');
if (scheduledVaccination.length === 0 && individual.getAgeInMonths() >= 6) {
    return "6-month vaccination overdue";
}
```

***

## Individual and Subject Methods

### `isFemale()`

**Available on**: Individual

**Purpose**: Checks if the individual's gender is female.

**Returns**: Boolean

**Examples**:

```javascript
// Basic gender check
if (individual.isFemale()) {
    // Female-specific logic
}

// Eligibility for reproductive health programs
return individual.isFemale() && individual.getAgeInYears() >= 15 && individual.getAgeInYears() <= 49;

// Pregnancy program eligibility
if (programName === 'Pregnancy Care' && !individual.isFemale()) {
    return {
        eligible: false,
        message: "Only females are eligible for pregnancy care program"
    };
}

// Gender-specific screening
if (individual.isFemale() && individual.getAgeInYears() >= 21) {
    return "Eligible for cervical cancer screening";
}

// Combined conditions
if (individual.isFemale() && individual.getAgeInYears() > 10 && individual.getAgeInYears() < 19) {
    return "Eligible for adolescent girl program";
}
```

***

### `isMale()`

**Available on**: Individual

**Purpose**: Checks if the individual's gender is male.

**Returns**: Boolean

**Examples**:

```javascript
// Basic gender check
if (individual.isMale()) {
    // Male-specific logic
}

// Male-specific screening eligibility
if (individual.isMale() && individual.getAgeInYears() >= 50) {
    return "Eligible for prostate screening";
}

// Program exclusion validation
if (programName === 'Maternal Health' && individual.isMale()) {
    return {
        eligible: false,
        message: "Males cannot enroll in maternal health program"
    };
}

// Age and gender combined rules
if (individual.isMale() && individual.getAgeInYears() >= 40) {
    return "Consider cardiovascular risk assessment";
}
```

***

### `isPerson()`

**Available on**: Individual

**Purpose**: Checks if the subject type is a person (as opposed to household, group, etc.).

**Returns**: Boolean

**Examples**:

```javascript
// Person-specific logic
if (individual.isPerson()) {
    const genderText = individual.gender.name;
    const ageText = individual.getAge().toString();
} else {
    // Handle non-person subjects (groups, households)
}

// Display formatting
const subtitle1 = individual.isPerson() ? individual.gender.name : "";
const subtitle2 = individual.isPerson() ? individual.getAge().toString() : "";

// Validation rules
if (individual.isPerson()) {
    // Apply person-specific validation
    return individual.isFemale() && individual.getAgeInYears() >= 15;
} else {
    // Handle group/household validation
}
```

***

### `isHousehold()`

**Available on**: Individual

**Purpose**: Checks if the subject type is a household.

**Returns**: Boolean

**Examples**:

```javascript
// Household-specific rules
if (individual.isHousehold()) {
    // Apply household-level validation and logic
}

// Filter household subjects
const households = subjects.filter(subject => subject.isHousehold());

// Check if individual belongs to households
const belongsToHousehold = _.some(individual.groups, group => 
    group.groupSubject.isHousehold());

// Household member count validation
if (individual.isHousehold()) {
    const memberCount = individual.groupSubjects.length;
    if (memberCount === 0) {
        return "Household must have at least one member";
    }
}
```

***

### `isGroup()`

**Available on**: Individual

**Purpose**: Checks if the subject type is a group.

**Returns**: Boolean

**Examples**:

```javascript
// Group-specific processing
if (individual.isGroup()) {
    // Handle group operations
    const memberCount = individual.groupSubjects.length;
}

// Group validation
if (individual.isGroup() && individual.groupSubjects.length < 5) {
    return "Self-help group must have at least 5 members";
}
```

***

### `getMobileNumber()`

**Available on**: Individual

**Purpose**: Gets mobile number from observations using mobile number concept.

**Returns**: String (mobile number) or undefined

**Examples**:

```javascript
// Get mobile number for notifications
const mobileNumber = individual.getMobileNumber();
if (mobileNumber) {
    // Send SMS notification
    console.log(`Sending SMS to ${mobileNumber}`);
}

// Validation
const mobile = individual.getMobileNumber();
if (!mobile && isRequired) {
    return ValidationResult.failure("mobile", "Mobile number is required");
}

// Display with fallback
const displayNumber = individual.getMobileNumber() || "Not provided";
```

***

### `nameString`

**Available on**: Individual

**Purpose**: Gets formatted name string based on subject type.

**Returns**: String (formatted name)

**Examples**:

```javascript
// Get formatted name
const displayName = individual.nameString;

// For persons: "John Doe Smith"
// For users: "Admin(You)" 
// For other subjects: "Group Name"

// Use in displays
const summary = `Patient: ${individual.nameString}, Age: ${individual.getAge()}`;

// Name with unique identifier (for specific subject types like Farmer)
const uniqueName = individual.nameStringWithUniqueAttribute;
// Returns: "John Doe (9876543210)" if mobile number exists
```

***

## Location and Address Methods

### `lowestAddressLevel`

**Available on**: Individual

**Purpose**: Gets the lowest (most specific) address level for the individual.

**Returns**: AddressLevel object

**Examples**:

```javascript
// Access address information
const addressLevel = individual.lowestAddressLevel;
const villageName = addressLevel.name;
const addressType = addressLevel.type;

// Get address lineage
const titleLineage = addressLevel.titleLineage;

// Check for web application context
const webapp = individual.lowestAddressLevel.titleLineage;
if (webapp) {
    // Web application specific logic
    // Skip location-based validations
} else {
    // Mobile application logic
}

// Address-based rules
if (individual.lowestAddressLevel.name === "High Risk Village") {
    return "Apply high-risk protocols";
}
```

***

### `lowestTwoLevelAddress(i18n)`

**Available on**: Individual

**Purpose**: Gets formatted address string with the lowest two levels of address hierarchy.

**Parameters**:

* `i18n` (Object): Internationalization object for translation

**Returns**: String (formatted address)

**Examples**:

```javascript
// Display compact address
const compactAddress = individual.lowestTwoLevelAddress(i18n);
// Returns: "Village Name, Block Name"

// Use in summaries with fallback
const location = individual.lowestTwoLevelAddress(i18n) || 'Address not specified';

// Address validation
const address = individual.lowestTwoLevelAddress(i18n);
if (!address || address.trim() === '') {
    return ValidationResult.failure("address", "Address is required");
}
```

***

### `fullAddress(i18n)`

**Available on**: Individual

**Purpose**: Gets complete address lineage from lowest to highest level.

**Parameters**:

* `i18n` (Object): Internationalization object for translation

**Returns**: String (complete address hierarchy)

**Examples**:

```javascript
// Full address hierarchy
const fullAddr = individual.fullAddress(i18n);
// Returns: "Village, Block, District, State"

// Use for detailed address display
const addressDetail = {
    compact: individual.lowestTwoLevelAddress(i18n),
    full: individual.fullAddress(i18n)
};

// Geographic analysis
const addressComponents = individual.fullAddress(i18n).split(', ');
const state = addressComponents[addressComponents.length - 1];
```

***

## Relationship and Group Methods

### `getRelatives(relationName, inverse)`

**Available on**: Individual

**Purpose**: Gets all relatives by relation name.

**Parameters**:

* `relationName` (String): Name of the relation to find
* `inverse` (Boolean, optional): Whether to check inverse relation (default: false)

**Returns**: Array of Individual objects

**Examples**:

```javascript
// Get all children (inverse of parent relation)
const children = individual.getRelatives('Parent', true);

// Get all siblings
const siblings = individual.getRelatives('Sibling');

// Family size calculation
const spouse = individual.getRelative('Spouse');
const children = individual.getRelatives('Parent', true);
const familySize = 1 + children.length + (spouse ? 1 : 0);

// Child immunization tracking
children.forEach(child => {
    const childAge = child.getAgeInMonths();
    if (childAge >= 6 && childAge < 24) {
        // Track immunization status
    }
});

// Family history analysis
const parents = individual.getRelatives('Child', true); // Get parents
const familyHistory = [];
parents.forEach(parent => {
    const diabetes = parent.getObservationReadableValue('Diabetes History');
    if (diabetes === 'Yes') {
        familyHistory.push('Parental diabetes');
    }
});
```

***

### `getRelative(relationName, inverse)`

**Available on**: Individual

**Purpose**: Gets the first relative by relation name.

**Parameters**:

* `relationName` (String): Name of the relation to find
* `inverse` (Boolean, optional): Whether to check inverse relation (default: false)

**Returns**: Individual object or undefined

**Examples**:

```javascript
// Get spouse
const spouse = individual.getRelative('Spouse');
if (spouse) {
    const spouseAge = spouse.getAgeInYears();
}

// Get mother
const mother = individual.getRelative('Mother');

// Get primary child (useful for parent-child relationships)
const primaryChild = individual.getRelative('Parent', true);

// Conditional logic based on relationships
if (spouse && spouse.isFemale() && spouse.getAgeInYears() >= 15) {
    // Include spouse in reproductive health program
}

// Family contact information
const emergencyContact = individual.getRelative('Emergency Contact');
const emergencyNumber = emergencyContact ? emergencyContact.getMobileNumber() : null;
```

***

### `getGroups()`

**Available on**: Individual

**Purpose**: Gets all non-voided groups that this individual belongs to.

**Returns**: Array of GroupSubject objects

**Examples**:

```javascript
// Get household information
const household = individual.getGroups().filter(grp => 
    grp.groupSubject.subjectType.type === 'Household')[0];

if (household) {
    const householdName = household.groupSubject.name;
    const householdMembers = household.groupSubject.groupSubjects.length;
}

// Check group membership
const groups = individual.getGroups();
if (groups.length > 0) {
    // Individual belongs to groups
    const groupNames = groups.map(g => g.groupSubject.name);
}

// Self-help group membership
const shgMembership = individual.getGroups().find(g => 
    g.groupSubject.subjectType.name === 'Self Help Group');

if (shgMembership) {
    // Access SHG-specific benefits
}
```

***

### `getGroupSubjects()`

**Available on**: Individual

**Purpose**: Gets all non-voided group subjects where this individual is a member.

**Returns**: Array of GroupSubject objects

**Examples**:

```javascript
// Get all group memberships
const groupMemberships = individual.getGroupSubjects();

// Find specific group type membership
const shgMembership = individual.getGroupSubjects()
    .find(gs => gs.groupSubject.subjectType.name === 'SHG');

// Check member role
groupMemberships.forEach(membership => {
    if (membership.groupRole.isHeadOfHousehold) {
        // Individual is head of household
    }
});

// Count group memberships
const membershipCount = individual.getGroupSubjects().length;
if (membershipCount === 0) {
    return "Individual is not part of any group";
}
```

***

## Validation and Status Methods

### `hasBeenEdited()`

**Available on**: AbstractEncounter (Encounter, ProgramEncounter)

**Purpose**: Checks if encounter has been edited (filled with data).

**Returns**: Boolean

**Examples**:

```javascript
// Check if encounter is completed
if (encounter.hasBeenEdited()) {
    // Encounter has been filled with data
    const completionDate = encounter.encounterDateTime;
} else {
    // Encounter is still scheduled/pending
}

// Validation for editing
if (encounter.hasBeenEdited() && !userCanEditCompletedEncounters) {
    return {
        editable: false,
        message: "Cannot edit completed encounters"
    };
}

// Cancellation eligibility
if (!encounter.hasBeenEdited() && !encounter.isCancelled()) {
    // Can be cancelled
}
```

***

### `isCancelled()`

**Available on**: AbstractEncounter (Encounter, ProgramEncounter)

**Purpose**: Checks if encounter has been cancelled.

**Returns**: Boolean

**Examples**:

```javascript
// Check cancellation status
if (encounter.isCancelled()) {
    const cancelReason = encounter.findCancelEncounterObservationReadableValue('Cancel Reason');
    const cancelDate = encounter.cancelDateTime;
}

// Filter active encounters
const activeEncounters = individual.encounters.filter(enc => 
    !enc.isCancelled() && enc.hasBeenEdited());

// Rescheduling logic
if (encounter.isCancelled()) {
    const reason = encounter.findCancelEncounterObservationReadableValue('Cancel Reason');
    if (reason === 'Patient unavailable') {
        // Automatic rescheduling
        return {
            name: "Rescheduled Visit",
            earliestDate: moment().add(7, 'days').toDate()
        };
    }
}
```

***

### `isScheduled()`

**Available on**: AbstractEncounter (Encounter, ProgramEncounter)

**Purpose**: Checks if encounter is scheduled (not filled and not cancelled).

**Returns**: Boolean

**Examples**:

```javascript
// Check if visit is pending
if (encounter.isScheduled()) {
    const daysUntilDue = moment(encounter.earliestVisitDateTime).diff(moment(), 'days');
    if (daysUntilDue < 0) {
        return "Visit is overdue";
    } else {
        return `Visit due in ${daysUntilDue} days`;
    }
}

// Count scheduled visits
const pendingVisits = individual.encounters.filter(enc => enc.isScheduled()).length;

// Overdue visit check
const overdueVisits = individual.encounters.filter(enc => 
    enc.isScheduled() && moment().isAfter(enc.maxVisitDateTime));
```

***

### `isRejectedEntity()`

**Available on**: Individual, AbstractEncounter (Encounter, ProgramEncounter)

**Purpose**: Checks if entity has been rejected in the approval workflow.

**Returns**: Boolean

**Examples**:

```javascript
// Check individual approval status
if (individual.isRejectedEntity()) {
    return "Individual registration has been rejected";
}

// Check encounter approval status
if (encounter.isRejectedEntity()) {
    const rejectionReason = encounter.latestEntityApprovalStatus.comment;
    return `Encounter rejected: ${rejectionReason}`;
}

// Filter approved entities
const approvedEncounters = encounters.filter(enc => !enc.isRejectedEntity());
const approvedIndividuals = individuals.filter(ind => !ind.isRejectedEntity());

// Conditional processing
if (!individual.isRejectedEntity()) {
    // Process approved individual
}
```

***

## Media and Utility Methods

### `findMediaObservations()`

**Available on**: Individual, AbstractEncounter (Encounter, ProgramEncounter)

**Purpose**: Finds all media observations (images, videos, audio files).

**Returns**: Array of media observations

**Examples**:

```javascript
// Get all media attachments
const mediaObs = individual.findMediaObservations();

// Process different media types
mediaObs.forEach(obs => {
    if (obs.concept.datatype === 'Image') {
        // Handle image observation
        const imageUrl = obs.getValue();
    } else if (obs.concept.datatype === 'Video') {
        // Handle video observation
    }
});

// Check for profile pictures or documents
const profileImages = individual.findMediaObservations()
    .filter(obs => obs.concept.name.includes('Profile'));

// Count media attachments
const mediaCount = encounter.findMediaObservations().length;
if (mediaCount === 0) {
    return "No supporting documents attached";
}
```

***

### `getProfilePicture()`

**Available on**: Individual

**Purpose**: Gets the profile picture path/URL.

**Returns**: String (image path) or undefined

**Examples**:

```javascript
// Display profile picture
const profilePic = individual.getProfilePicture();
if (profilePic) {
    // Show image in UI
    console.log(`Profile picture: ${profilePic}`);
} else {
    // Show default avatar
}

// Validation
const hasPicture = !!individual.getProfilePicture();
if (requiresPhoto && !hasPicture) {
    return ValidationResult.failure("photo", "Profile picture is required");
}
```

***

### `getEntityTypeName()`

**Available on**: Individual, AbstractEncounter (Encounter, ProgramEncounter)

**Purpose**: Gets the entity type name for identification and logging.

**Returns**: String

**Examples**:

```javascript
// Get type for logging
const entityType = individual.getEntityTypeName(); // Returns subject type name like "Person", "Household"
const encounterType = encounter.getEntityTypeName(); // Returns encounter type name like "ANC", "Delivery"

// Conditional logic based on type
if (individual.getEntityTypeName() === "Household") {
    // Household-specific logic
} else if (individual.getEntityTypeName() === "Person") {
    // Person-specific logic
}

// Logging and auditing
console.log(`Processing ${entity.getEntityTypeName()}: ${entity.uuid}`);
```

***

### `toJSON()`

**Available on**: Individual, ProgramEncounter

**Purpose**: Gets JSON representation of the entity for serialization.

**Returns**: Object (JSON representation)

**Examples**:

```javascript
// Serialize for logging or transmission
const individualData = individual.toJSON();
const encounterData = programEncounter.toJSON();

// Log for debugging
console.log("Individual data:", JSON.stringify(individual.toJSON(), null, 2));

// Data export
const exportData = {
    individual: individual.toJSON(),
    encounters: individual.encounters.map(enc => enc.toJSON ? enc.toJSON() : enc)
};
```

***

## 📚 Additional Resources

* [Writing Rules Guide](../docs/writing-rules#/) - Complete guide to writing Avni rules
* [Concept Reference](../docs/concepts#/) - Working with concepts and observations

<br />
