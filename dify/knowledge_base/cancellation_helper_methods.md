# Cancellation Visit Schedule Rules — MANDATORY Patterns

## CRITICAL: Cancellation Helper Methods

For ProgramEncounterCancellation and IndividualEncounterCancellation form types, you MUST use the correct cancellation helper methods. Using deprecated methods is a critical error.

### Getting Cancellation Reason (string)

CORRECT:
```javascript
// ProgramEncounterCancellation
const cancellationReason = programEncounter.findCancelEncounterObservationReadableValue("Cancellation reason");

// IndividualEncounterCancellation
const cancellationReason = encounter.findCancelEncounterObservationReadableValue("Cancellation reason");
```

WRONG — NEVER use these:
```javascript
programEncounter.getCancelReason()   // ❌ deprecated, will fail
encounter.getCancelReason()          // ❌ deprecated, will fail
```

### Getting Cancellation Date

CORRECT — use findCancelEncounterObservation with "Cancel date":
```javascript
// ProgramEncounterCancellation
const cancelDateObs = programEncounter.findCancelEncounterObservation("Cancel date");
const cancellationDate = cancelDateObs ? cancelDateObs.getValue() : programEncounter.encounterDateTime;

// IndividualEncounterCancellation
const cancelDateObs = encounter.findCancelEncounterObservation("Cancel date");
const cancellationDate = cancelDateObs ? cancelDateObs.getValue() : encounter.encounterDateTime;
```

WRONG — NEVER use cancelDateTime directly:
```javascript
programEncounter.cancelDateTime  // ❌ deprecated, do not use
encounter.cancelDateTime         // ❌ deprecated, do not use
```

## ProgramEncounterCancellation — Complete Pattern

Entity: `programEncounter = params.entity`
VisitScheduleBuilder init: `new imports.rulesConfig.VisitScheduleBuilder({ programEncounter })`
NO program exit guard — do NOT check programExitDateTime in cancellation rules.

### Full Working Example — ProgramEncounterCancellation with reason-based branching
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
    const maxDate = moment(earliestDate).add(3, 'days').toDate();
    scheduleBuilder.add({
      name: "Urgent Follow Up",
      encounterType: "Urgent Follow Up",
      earliestDate,
      maxDate
    });
  } else {
    const earliestDate = moment(cancellationDate).add(2, 'weeks').toDate();
    const maxDate = moment(earliestDate).add(1, 'week').toDate();
    scheduleBuilder.add({
      name: "Routine Follow Up",
      encounterType: "Routine Follow Up",
      earliestDate,
      maxDate
    });
  }

  return scheduleBuilder.getAll();
};
```

### Full Working Example — ProgramEncounterCancellation unconditional reschedule
```javascript
"use strict";
({ params, imports }) => {
  const programEncounter = params.entity;
  const scheduleBuilder = new imports.rulesConfig.VisitScheduleBuilder({ programEncounter });
  const moment = imports.moment;

  const cancelDateObs = programEncounter.findCancelEncounterObservation("Cancel date");
  const cancellationDate = cancelDateObs ? cancelDateObs.getValue() : programEncounter.encounterDateTime;

  const earliestDate = moment(cancellationDate).add(2, 'weeks').toDate();
  const maxDate = moment(earliestDate).add(3, 'days').toDate();

  scheduleBuilder.add({
    name: "Growth Monitoring",
    encounterType: "Growth Monitoring",
    earliestDate,
    maxDate
  });

  return scheduleBuilder.getAll();
};
```

## IndividualEncounterCancellation — Complete Pattern

Entity: `encounter = params.entity`
VisitScheduleBuilder init: `new imports.rulesConfig.VisitScheduleBuilder({ encounter })` (simple form)
Alternative init: `new imports.rulesConfig.VisitScheduleBuilder({ individual: encounter.individual })` (also valid)
NO program exit guard — no programEnrolment exists for individual encounters.

### Full Working Example — IndividualEncounterCancellation with reason-based branching
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
    const earliestDate = moment(cancellationDate).toDate();
    const maxDate = moment(cancellationDate).add(4, 'hours').toDate();
    scheduleBuilder.add({
      name: "Emergency Care",
      encounterType: "Emergency Care",
      earliestDate,
      maxDate
    });
  } else {
    const earliestDate = moment(cancellationDate).add(1, 'week').toDate();
    const maxDate = moment(earliestDate).add(1, 'week').toDate();
    scheduleBuilder.add({
      name: "Consultation Follow Up",
      encounterType: "Consultation Follow Up",
      earliestDate,
      maxDate
    });
  }

  return scheduleBuilder.getAll();
};
```

### Full Working Example — IndividualEncounterCancellation unconditional reschedule
```javascript
"use strict";
({ params, imports }) => {
  const encounter = params.entity;
  const scheduleBuilder = new imports.rulesConfig.VisitScheduleBuilder({ encounter });
  const moment = imports.moment;

  const cancelDateObs = encounter.findCancelEncounterObservation("Cancel date");
  const cancellationDate = cancelDateObs ? cancelDateObs.getValue() : encounter.encounterDateTime;

  const earliestDate = moment(cancellationDate).add(2, 'weeks').toDate();
  const maxDate = moment(earliestDate).add(1, 'week').toDate();

  scheduleBuilder.add({
    name: "Follow Up Visit",
    encounterType: "Follow Up Visit",
    earliestDate,
    maxDate
  });

  return scheduleBuilder.getAll();
};
```

## Quick Reference Table

| What you need | Correct method | Wrong method |
|---|---|---|
| Cancellation reason (string) | `entity.findCancelEncounterObservationReadableValue("Cancellation reason")` | `entity.getCancelReason()` ❌ |
| Cancellation date (Date) | `entity.findCancelEncounterObservation("Cancel date").getValue()` | `entity.cancelDateTime` ❌ |
| Cancel date with fallback | `cancelDateObs ? cancelDateObs.getValue() : entity.encounterDateTime` | — |

## Form Type to Entity and Builder Init

| Form Type | Entity | Builder Init |
|---|---|---|
| ProgramEncounterCancellation | `programEncounter = params.entity` | `{ programEncounter }` |
| IndividualEncounterCancellation | `encounter = params.entity` | `{ encounter }` |

## Anti-Patterns for Cancellation Rules — DO NOT DO THESE

1. DO NOT use `programEncounter.cancelDateTime` or `encounter.cancelDateTime` — use `findCancelEncounterObservation("Cancel date").getValue()` instead
2. DO NOT use `getCancelReason()` — use `findCancelEncounterObservationReadableValue("Cancellation reason")` instead
3. DO NOT add a program exit guard (`if (programEncounter.programEnrolment.programExitDateTime)`) in cancellation rules
4. DO NOT use `programEncounter` as entity variable in IndividualEncounterCancellation — use `encounter`
5. DO NOT use `getObservationReadableValue` or `getObservationValue` for cancellation-specific fields — use the `findCancelEncounter*` family of methods
