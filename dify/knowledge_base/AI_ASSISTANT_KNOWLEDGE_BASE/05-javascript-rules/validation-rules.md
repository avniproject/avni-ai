---
title: Writing Validation Rules in Avni
category: javascript-rules
audience: implementer
difficulty: intermediate
priority: critical
keywords:
- validation rules
- form validation
- data validation
- validation logic
last_updated: '2026-03-16'
task_types:
- tutorial
- example
features:
- rules
- forms
technical_level:
- procedural
implementation_phase:
- development
complexity: moderate
retrieval_boost: 2.0
related_topics:
- rules-introduction.md
- helper-functions.md
- common-patterns.md
estimated_reading_time: 35 minutes
version: '1.0'
---
# Writing Validation Rules in Avni

<!-- CHUNK: tldr -->
## TL;DR

> 🚧 Important Update on Rules Execution
> 
> Please be informed that all existing rules stored in the rules table will become obsolete by the end of this year, 2024. This means that starting January 1, 2025, these rules will no longer be executed.
<!-- END CHUNK -->

<!-- CHUNK: overview -->
## Overview

> 🚧 Important Update on Rules Execution
> 
> Please be informed that all existing rules stored in the rules table will become obsolete by the end of this year, 2024. This means that starting January 1, 2025, these rules will no longer be executed.
> 
> However, any rules added through the App Designer and avni-health-modules will continue to work as expected.
> 
> If you have any questions or need assistance with migrating your rules, please contact our support team.
<!-- END CHUNK -->

<!-- CHUNK: contents -->
## Contents:

[Introduction](/docs/writing-rules#introduction)  
[Rule types](/docs/writing-rules#rule-types)  
[Using service methods in the rules](/docs/writing-rules#using-service-methods-in-the-rules)  
[Using other group/household individuals' information in the rules](/docs/writing-rules#using-other-grouphousehold-individuals-information-in-the-rules)  
[Types of rules and their support/availability in Data Entry App](/docs/writing-rules#types-of-rules-and-their-supportavailability-in-data-entry-app)  
[Types of rules and their support/availability in transaction data upload](/docs/writing-rules#types-of-rules-and-their-supportavailability-in-transaction-data-upload)
<!-- END CHUNK -->

<!-- CHUNK: introduction -->
## Introduction:

Rules are just normal JavaScript functions that take some input and returns something. You can use the full power of JavaScript in these functions. We also provide you with some helper libraries that make it easier to write rules. We will introduce you to these libraries in the examples below.

All rule functions get passed an object as a parameter. The parameter object has two properties: 1. imports 2. params. The imports object is used to pass down common libraries. The params object is used to pass rule-specific parameters. In params object, we pass the relevant entity on which rule is being executed e.g. if a rule is invoked when a program encounter is being performed then we pass the ProgramEncounter object. The entities that we pass are an instance of classes defined in [avni-models](https://github.com/avniproject/avni-models)

### Shape of common imports object:

```javascript
{
  rulesConfig: {}, //It exposes everything exported by rules-config library. https://github.com/avniproject/rules-config/blob/master/rules.js.
  common: {}, // Library we have for common functions https://github.com/avniproject/avni-client/blob/master/packages/openchs-health-modules/health_modules/common.js
  lodash: {}, // lodash library
  moment: {}, // momentjs library
  motherCalculations: {}, //mother program calculations https://github.com/avniproject/avni-health-modules/blob/master/src/health_modules/mother/calculations.js
  log: {} //console.log object
}
```

### Shape of common parameters in all params object

Note there are other elements in params object which are specific to the rule hence have been described below.

```javascript
{    
  user, //Current User's UserInfo object  
  myUserGroups //List of Group objects, to which the User is assigned to 
}
```

User: [https://github.com/avniproject/avni-models/blob/master/src/UserInfo.js](https://github.com/avniproject/avni-models/blob/master/src/UserInfo.js)

Group: [https://github.com/avniproject/avni-models/blob/master/src/Groups.js](https://github.com/avniproject/avni-models/blob/master/src/Groups.js)

#### Entities passed to the rule

All rule receives an entity from the `params` object. Depending on the rule type an entity can be one of [Individual](https://github.com/avniproject/avni-models/blob/master/src/Individual.ts), [ProgramEncounter](https://github.com/avniproject/avni-models/blob/master/src/ProgramEncounter.js), [ProgramEnrolment](https://github.com/avniproject/avni-models/blob/master/src/ProgramEnrolment.js), [Encounter](https://github.com/avniproject/avni-models/blob/master/src/Encounter.js), or [ChecklistItem](https://github.com/avniproject/avni-models/blob/master/src/ChecklistItem.js). The shape of the entity object and the supported methods can be viewed from the above links on each entity.
<!-- END CHUNK -->

<!-- CHUNK: rule-types -->
## Rule types

1. [Enrolment summary rule](/docs/writing-rules#1-enrolment-summary-rule)
2. [Form element rule](/docs/writing-rules#2-form-element-rule)
3. [Form element group rule](/docs/writing-rules#3-form-element-group-rule)
4. [Visit schedule rule](/docs/writing-rules#4-visit-schedule-rule)
5. [Decision rule](/docs/writing-rules#5-decision-rule)
6. [Validation rule](/docs/writing-rules#6-validation-rule)
7. [Enrolment eligibility check rule](/docs/writing-rules#7-enrolment-eligibility-check-rule)
8. [Encounter eligibility check rule](/docs/writing-rules#8-encounter-eligibility-check-rule)
9. [Checklists rule](/docs/writing-rules#9-checklists-rule)
10. [Work list updation rule](/docs/writing-rules#10-work-list-updation-rule)
11. [Subject summary rule](/docs/writing-rules#11-subject-summary-rule)
12. [Hyperlink menu item rule](/docs/writing-rules#12-hyperlink-menu-item-rule)
13. [Message rule](https://avni.readme.io/docs/writing-rules#13-message-rule)
14. [Dashboard Card rule](https://avni.readme.io/docs/writing-rules#14-dashboard-card-rule)
15. [Manual Programs Eligibility Check Rule](https://avni.readme.io/docs/writing-rules#15-manual-programs-eligibility-check-rule)
16. [Member Addition Eligibility Check Rule](https://avni.readme.io/docs/writing-rules#16-member-addition-eligibility-check-rule)
17. [Edit Form Rule](https://avni.readme.io/docs/writing-rules#17-edit-form-rule)
18. [Global reusable code rule](https://avni.readme.io/docs/writing-rules#18-global-reusable-code-rule-alpha)


![Invocation of different rule types](https://files.readme.io/2284f79-Screenshot_2020-07-03_at_9.33.55_AM.png)


![](https://files.readme.io/baad794-Screenshot_2020-07-03_at_9.59.42_AM.png)

<hr/>
<!-- END CHUNK -->

<!-- CHUNK: 1-enrolment-summary-rule -->
## 1. Enrolment summary rule

- Logical scope = Program Enrolment
- Trigger = Before the opening of a subject dashboard with default program selection. On program change of subject dashboard.
- In designer = Program (Enrolment Summary Rule)
- When to use = Display important information in the subject dashboard for a program

You can use this rule to highlight important information about the program on the Subject Dashboard in table format. It can pull data from all the encounters of enrolment and the enrolment itself. You can use this when the information you want to show is not entered by the user in any of the forms and is also not required for any reporting purposes (hence you wouldn't also generate this data via decision rule).

### Shape of params object:

```javascript
{ 
  summaries: [],
  programEnrolment: {}, // ProgramEnrolment model
	services,
  user, //Current User's UserInfo object  
  myUserGroups //List of Group objects  
}
```

You need to return an array of summary objects from this function.

### Shape of the summary object:

```
{
  "name": "name of the summary concept",
  "value": <text> | <number> | <date> | <datetime> | <concept list in case of Coded question>
}
```

### Example:

```
({params, imports}) =>  {
    const summaries = [];
    const programEnrolment = params.programEnrolment;
    const birthWeight = programEnrolment.findObservationInEntireEnrolment('Birth Weight');
    if (birthWeight) {
      summaries.push({name: 'Birth Weight', value: birthWeight.getValue()});
    }
    return summaries;
};
```
![](https://files.readme.io/4f29afe-Screenshot_2020-05-19_at_3.09.44_PM.png)


![](https://files.readme.io/6fdb1f3-4bf85d9-encounter-scheduling-2.png)

<hr/>
<!-- END CHUNK -->

<!-- CHUNK: 2-form-element-rule -->
## 2. Form element rule

- Logical scope = Form Element
- Trigger = Before display of form element in the form wizard and on any change done by the user in on that page
- In designer = Form Element (RULES tab)
- When to use = 
  - Hide/show a form element
  - auto calculate the value of a form element
  - reset value of a form element

### Shape of params object:

```javascript
{
  entity: {}, //it could be one of Individual, ProgramEncounter, ProgramEnrolment, Encounter and ChecklistItem depending on what type of form is this rule attached to
  formElement: {}, //form element to which this rule is attached to
  questionGroupIndex,
  services,
  entityContext,
  user, //Current User's UserInfo object  
  myUserGroups //List of Group objects  
}
```

This function should return an instance of [FormElementStatus](https://github.com/avniproject/avni-models/blob/master/src/application/FormElementStatus.js) to show/hide the element, show validation error, set its value, reset a value, or skip answers.

To reset a value, you can use FormElementStatus._resetIfValueIsNull() method.  
You can either use FormElementStatusBuilder or use normal JavaScript to build the return value. FormElementStatusBuilder is a helper class provided by Avni that helps writing rules in a declarative way.

### Examples using FormElementStatusBuilder.

```javascript Registration Form
'use strict';
({params, imports}) => {
  const individual = params.entity;
  const formElement = params.formElement;
  const statusBuilder = new imports.rulesConfig.FormElementStatusBuilder({individual, formElement});
  statusBuilder.show().when.valueInRegistration("Number of hywas required").is.greaterThan(0);
  return statusBuilder.build();
};
```
```javascript Program Enrolment Form 1
({params, imports}) => {
  const programEnrolment = params.entity;
  const formElement = params.formElement;
  const statusBuilder = new imports.rulesConfig.FormElementStatusBuilder({programEnrolment, formElement});
  statusBuilder.show().when.valueInEnrolment('Is child getting registered at Birth').containsAnswerConceptName("No");
  return statusBuilder.build();//this method returns FormElementStatus object with visibility true if the conditions given above matches
};
```
```javascript Program Enrolment Form 2
({params, imports}) => {
    const gravidaBreakup = [
        'Number of miscarriages',
        'Number of abortions',
        'Number of stillbirths',
        'Number of child deaths',
        'Number of living children'
    ];
    const computeGravida = (programEnrolment) => gravidaBreakup
        .map((cn) => programEnrolment.getObservationValue(cn))
        .filter(Number.isFinite)
        .reduce((a, b) => a + b, 1);
    
    const [formElement, programEnrolment] = params.programEnrolment;
    const firstPregnancy = programEnrolment.getObservationReadableValue('Is this your first pregnancy?');
    const value = firstPregnancy === 'Yes' ? 1 : firstPregnancy === 'No' ? computeGravida(programEnrolment) : undefined;
    return new FormElementStatus(formElement.uuid, true, value);
};
```
```javascript Program Encounter Form
'use strict';
({params, imports}) => {
  const programEncounter = params.entity;
  const formElement = params.formElement;
  const statusBuilder = new imports.rulesConfig.FormElementStatusBuilder({programEncounter, formElement});
  const value = programEncounter.findLatestObservationInEntireEnrolment('Have you received first dose of TT');
  statusBuilder.show().whenItem( value.getReadableValue() == 'No').is.truthy;
  return statusBuilder.build();
};
```
```javascript Encounter Form
'use strict';
({params, imports}) => {
  const encounter = params.entity;
  const formElement = params.formElement;
  const statusBuilder = new imports.rulesConfig.FormElementStatusBuilder({encounter, formElement});
  statusBuilder.show().when.valueInEncounter("Are machine start and end hour readings recorded").is.yes;
  return statusBuilder.build();
};
```
```Text AffiliatedGroups
//In-order to fetch affiliatedGroups set as part of GroupAffiliation Concept in the same form,
//one needs to access params.entityContext.affiliatedGroups variable.

// Old Rule snippet
// const phulwariName = _.get(_.find(programEnrolment.individual.affiliatedGroups, ({voided}) => !voided), ['groupSubject', 'firstName'], '');

// New Rule snippet
const phulwariName = _.get(_.find(params.entityContext.affiliatedGroups, ({voided}) => !voided), ['groupSubject', 'firstName'], '');

```
![](https://files.readme.io/ece1355-Screenshot_2020-07-02_at_6.21.43_PM.png)

![](https://files.readme.io/abb6bcf-4692c21-SkipLogic.gif)

Please note that form element rules are not transitive and cannot depend on the result of another form element's form element rule. The rule logic for a particular element will need to cater to this. 

i.e. If rule C on element C depends on value of element B and rule B depends on value of element A, updating A will only update B's value and not C's value. 

<hr/>
<!-- END CHUNK -->

<!-- CHUNK: 3-form-element-group-rule -->
## 3. Form element group rule

- Scope = Form Element Group
- Trigger = Before display of form element group to the user (including previous or next)
- In designer = Form Element Group (RULES tab)
- When to use = Hide/show a form element group

Sometimes we want to hide the entire form element group based on some conditions. This can be done using a form element group (FEG) rule. There is a rules tab on each FEG where this type of rule can be written. Note that this rule gets executed before form element rule so if the form element is hidden by this rule then the _form element rule_ will not get executed.

### Shape of params object:

```javascript
{
  entity: {}, //it could be one of Individual, ProgramEncounter, ProgramEnrolment, Encounter and ChecklistItem depending on what type of form is this rule attached to
  formElementGroup: {}, //form element group to which this rule is attached to
  services,
  entityContext,
  user, //Current User's UserInfo object
  myUserGroups //List of Group objects
}
```

This function should return an array of  [FormElementStatus](https://github.com/avniproject/avni-models/blob/master/src/application/FormElementStatus.js)

### Example:

```
({params, imports}) => {
    const formElementGroup = params.formElementGroup;
    return formElementGroup.formElements.map(({uuid}) => {
        return new imports.rulesConfig.FormElementStatus(uuid, false, null);
    });
};
```

<hr/>
<!-- END CHUNK -->

<!-- CHUNK: 4-visit-schedule-rule -->
## 4. Visit schedule rule

- Logical scope = Encounter (aka Visit), Subject, or Program Enrolment
- Trigger = On completion of an form wizard before final screen is displayed
- In designer = Form (RULES tab)
- When to use = For scheduling one or more encounters in the future

### Shape of params object:

```javascript
{
  entity: {}, //it could be one of ProgramEncounter, ProgramEnrolment, Encounter depending on what type of form is this rule attached to.
  visitSchedule: []// Array of already scheduled visits.
  entityContext
  services,
  user, //Current User's UserInfo object  
  myUserGroups //List of Group objects  
}
```

You need to return an array of visit schedules from this function.

### Shape of the return value

```
[
  <visit schedule object>
  ...
]
```

### visit schedule object

```
{
	name: "visit name", 
	encounterType: "encounter type name", 
	earliestDate: <date>, 
	maxDate: <date>,
	visitCreationStrategy: "Optional. One of default|createNew",
	programEnrolment: "<Optional. Used if you want to create a visit in a different program enrolment. If the program enrolment is tied to another subject, the visit will be schedule for that subject. Do not pass this parameter if you want to schedule a general encounter.>",
	subjectUUID: "<Optional UUID string. Used if you want to create a general visit for another subject.>"
}
```

### Example

```
({ params, imports }) => {
  const programEnrolment = params.entity;
  const scheduleBuilder = new imports.rulesConfig.VisitScheduleBuilder({
    programEnrolment
  });
  scheduleBuilder
    .add({
      name: "First Birth Registration Visit",
      encounterType: "Birth Registration",
      earliestDate: programEnrolment.enrolmentDateTime,
      maxDate: programEnrolment.enrolmentDateTime
    })
    .whenItem(programEnrolment.getEncounters(true).length)
    .equals(0);
  return scheduleBuilder.getAll();
};
```

### Example 2 - Schedule a general visit on a household when a member completes a program enrolment

```
.
.
  scheduleBuilder.add({
      name: "TB Family Screening Form",
      encounterType: "TB Family Screening Form",
      earliestDate: imports.moment(programEnrolment.encounterDateTime).toDate(),
      maxDate: imports.moment(programEnrolment.encounterDateTime).add(15, 'days').toDate(),
      subjectUUID: programEnrolment.individual.groups[0].groupSubject.uuid
  });
.
.
```
![](https://files.readme.io/42b7d6b-Screenshot_2020-05-19_at_7.04.19_PM.png)


![](https://files.readme.io/cbaef6a-4fff50b-encounter-scheduling-1.png)

### Strategies that Avni uses.

For all the visit schedules that are returned, Avni evaluates how to create a visit. Assume you provide the default visitCreationStrategy (this is the default behaviour). Avni checks if there is already a scheduled visit for the given encounter type. If it is there, then it is updated with the incoming scheduled visit's name and other parameters. This strategy works well in most cases. 

- Remember that the VisitSchedule rule gets called whether you create a visit, or edit it. 
- Remember not to send multiple visit schedule objects for the same encounter type. If you do, the last one will overwrite the previous objects. 

### Using the "createNew" visit strategy

Do this only if you know what you are doing. If you add visitCreationStrategy of "createNew", then a new visit will be created no matter what. 

You need to be careful while using this strategy because, in edit scenarios, we might end up creating the same kind of visits multiple times. 

### Using the VisitScheduleBuilder.getAllUniqueVisits

VisitSchedulBuilder class has a getAllUniqueVisits method that provides some shortcuts to reduce the cruft you might have to do while creating scheduled visits. It mostly does the right thing, so you don't have to worry about its logic. However, if you think it is doing something you didn't intend, then you can replace it with your own implementation. Look up the [code](https://github.com/avniproject/rules-config/blob/master/src/rules/builder/VisitScheduleBuilder.js) for more details. 

<hr/>
<!-- END CHUNK -->

<!-- CHUNK: 5-decision-rule -->
## 5. Decision rule

- Logical scope = Encounter (aka Visit), Subject, or Program Enrolment
- Trigger = On completion of an form wizard before final screen is displayed
- In designer = Form (RULES tab)
- When to use = To create any additional observations based on all the data filled by the user in the form

Used to add decisions/recommendations to the form. The decisions are displayed on the last page of the form and are also saved in the form's observations.

### Shape of params object:

```javascript
{
	entity: {}, //it could be ProgramEncounter, ProgramEnrolment or Encounter depending on what type of form is this rule attached to.
 	entityContext,
  services,
  user, //Current User's UserInfo object  
  myUserGroups, //List of Group objects  
  decisions: {
     	"enrolmentDecisions": [],
    	"encounterDecisions": [],
      "registrationDecisions": []
  } // Decisions object on which you need to add decisions. 
}
```

### Shape of decisions parameter:

```javascript
{
  "enrolmentDecisions": [],
  "encounterDecisions": [],
  "registrationDecisions": []
}
```

You need to add `<decision object>` to decisions parameter's appropriate field and return it back.  
Inside the function, you will build decisions using ComplicationsBuilder and push the decisions to the decisions parameter's appropriate field. The return value will be the modified decisions parameter. You can also choose to not use ComplicationsBuilder and directly construct the return value as per the contract shown below:

### Shape of the return value

```
{
  "enrolmentDecisions": [<decision object>, ...],
  "encounterDecisions": [<decision object>, ...],
  "registrationDecisions": [<decision object>, ...]
}
The shape of <decision object>
{
  "name": "name of the decision concept",
  "value": <text> | <number> | <date> | <datetime> | <name of anwer concepts in case of Coded question>
}
```

### Example

```
({params, imports}) => {
    const programEncounter = params.entity;
    const decisions = params.decisions;
    const complicationsBuilder = new imports.rulesConfig.complicationsBuilder({
        programEncounter: programEncounter,
        complicationsConcept: "Birth status"
    });
    complicationsBuilder
        .addComplication("Baby is over weight")
        .when.valueInEncounter("Birth Weight")
        .is.greaterThanOrEqualTo(8);
    complicationsBuilder
        .addComplication("Baby is under weight")
        .when.valueInEncounter("Birth Weight")
        .is.lessThanOrEqualTo(5);
    complicationsBuilder
        .addComplication("Baby is normal")
        .when.valueInEncounter("Birth Weight")
        .is.lessThan(8)
        .and.when.valueInEncounter("Birth Weight")
        .is.greaterThan(5);
    decisions.encounterDecisions.push(complicationsBuilder.getComplications());
    return decisions;
};
```
![](https://files.readme.io/f0f898a-Screenshot_2020-05-19_at_7.09.58_PM.png)


![](https://files.readme.io/4b488cc-4fff50b-encounter-scheduling-1.png)

<hr/>
<!-- END CHUNK -->

<!-- CHUNK: validation-basics -->
## 6. Validation rule

- Logical scope = Encounter (aka Visit), Subject, or Program Enrolment
- Trigger = On completion of an form wizard before final screen is displayed
- In designer = Form (RULES tab)
- When to use = To provide validation error(s) to the user that are not specific to one form element but involved data in multiple form elements.

Used to stop users from filling invalid data

### Shape of params object:

```
{
  entity: {}, //it could be ProgramEncounter, ProgramEnrolment or Encounter depending on what type of form is this rule attached to.
  entityContext,
  services,
  user, //Current User's UserInfo object  
  myUserGroups //List of Group objects  
}
```

The return value of this function is an array with validation errors.

### Example:

```
({params, imports}) => {
  const validationResults = [];
  if(programEncounter.getObservationReadableValue('Parity') > programEncounter.getObservationReadableValue('Gravida')) {
    validationResults.push(imports.common.createValidationError('Para Cannot be greater than Gravida'));
  }
  return validationResults;
};
```
![](https://files.readme.io/fb8e5df-Screenshot_2020-05-19_at_7.14.05_PM.png)

<hr/>
<!-- END CHUNK -->

<!-- CHUNK: 7-enrolment-eligibility-check-rule -->
## 7. Enrolment Eligibility Check Rule

- Logical scope = Subject
- Trigger = On launch of program list when user enrols a subject into program
- In designer = Program page
- When to use = To restrict the programs which are available for enrolment based on subject's data (e.g. not allowing males to enrol in pregnancy programs)

### Shape of params object:

```
{
  entity: {}//Subject will be passed here.
  program,
  services,
  user, //Current User's UserInfo object  
  myUserGroups //List of Group objects  
}
```

### Shape of the return value

The return value of this function should be a boolean.

### Example:

```
({params, imports}) => {
  const individual = params.entity;
  return individual.isFemale() && individual.getAgeInYears() > 5;
};
```

**Notes**: The eligibility check is triggered only when someone tries to create a visit manually. Form stitching rules can override this default behaviour. 
![](https://files.readme.io/bc76050-Screenshot_2020-05-20_at_3.57.52_PM.png)


![](https://files.readme.io/ba63cb1-cbe944e-Screenshot_2019-11-20_at_6.51.40_PM.png)

<hr/>
<!-- END CHUNK -->

<!-- CHUNK: 8-encounter-eligibility-check-rule -->
## 8. Encounter Eligibility Check Rule

- Logical scope = Subject or Program Enrolment
- Trigger = On launch of new visit (encounter) list
- In designer = Encounter page
- When to use = To restrict the encounters which are available based on subject's full data (e.g. not showing postnatal care form if the delivery form has not been filed yet)

Used to hide some visit types depending on some data. If there existed scheduled encounters for that subject or program enrolment, clicking on an ineligible visit type, will fill up the scheduled encounter. 

### Shape of params object:

```javascript
{
  entity: {}//Subject will be passed here.
  services,
  user, //Current User's UserInfo object  
  myUserGroups //List of Group objects  
}
```

### Shape of the return value

The return value of this function should be a boolean.

### Example:

```
({params, imports}) => {
  const individual = params.entity;
  const visitCount = individual.enrolments[0].encounters.filter(e => e.encounterType.uuid === 'a30afe96-cdbb-42d9-bf30-6cf4b07354d1').length;
  let visibility = true;
  if (_.isEqual(visitCount, 1)) visibility = false;
  return visibility;
};
```

**Notes**: The eligibility check is triggered only when someone tries to create a visit manually. Form stitching rules can override this default behaviour. 
![](https://files.readme.io/0d034b9-Screenshot_2020-05-20_at_4.02.24_PM.png)

<hr/>
<!-- END CHUNK -->

<!-- CHUNK: 9-checklists-rule -->
## 9. Checklists rule

Used to add a checklist to an enrolment

### Shape of params object:

```javascript
{
  entity: {} //ProgramEnrolment
  checklistDetails: [] // Array of ChecklistDetail
  services,
  user, //Current User's UserInfo object  
  myUserGroups //List of Group objects  
}
```

### Example

```
({params, imports}) => {
  let vaccination = params.checklistDetails.find(cd => cd.name === 'Vaccination');
  if (vaccination === undefined) return [];
  const vaccinationList = {
    baseDate: params.entity.individual.dateOfBirth,
    detail: {uuid: vaccination.uuid},
    items: vaccination.items.map(vi => ({
      detail: {uuid: vi.uuid}
    }))
  };
  return [vaccinationList];
};
```

<hr/>
<!-- END CHUNK -->

<!-- CHUNK: 10-work-list-updation-rule -->
## 10. Work List Updation rule

- Logical scope = Subject, Program Enrolment, or Encounters
- Trigger = On display of system recommendation's page in form wizard
- In designer = Main Menu
- When to use = Stitch together multiple forms which can be filled back to back

The System Recommendations screen of Avni can be configured to direct a user to go to the next task to be done. Typically, if a new encounter is scheduled for a person on the same day, then the system automatically prompts the user to perform that encounter.  
This is performed using worklists. A worklist is an array of [work items](https://github.com/avniproject/avni-models/blob/master/src/application/WorkItem.js). 

The WorkListUpdation rule is used to customize this flow. The WorkLists object is passed on to this rule just before showing the System Recommendations screen. Any modification in the worklists is applied immediately to the flow. 

You can add a new WorkItem anywhere after the currentWorkList.currentItem. 

### Shape of params object:

```javascript
{
  worklists: {},
  context: {},
  services,
  user, //Current User's UserInfo object  
  myUserGroups //List of Group objects  
}
```

### Example

[https://gist.github.com/hithacker/d0fe89107b974797fbb11ced1feda146](https://gist.github.com/hithacker/d0fe89107b974797fbb11ced1feda146)
![](https://files.readme.io/ef3535d-Screenshot_2020-05-21_at_3.25.33_PM.png)


<hr/>
<!-- END CHUNK -->

<!-- CHUNK: 11-subject-summary-rule -->
## 11. Subject summary rule

- Logical scope = Subject registration
- Trigger = Before the opening of the subject dashboard profile tab.
- In designer = Subject (Subject Summary Rule)
- When to use = Display important information in the subject's profile. It can be used to show the summary if there are no programs.

This rule is very similar to the Enrolment summary rule. Except its scope is the Subject's registration.

### Shape of params object:

```
{ 
  individual: {}, // Subject model,
  user, //Current User's UserInfo object  
  myUserGroups //List of Group objects  
}
```

You need to return an array of summary objects from this function.

### Shape of the summary object:

```
{
  "name": "name of the summary concept",
  "value": <text> | <number> | <date> | <datetime> | <concept list in case of Coded question>
}
```

### Example:

```
({params, imports}) =>  {
    const summaries = [];
    const individual = params.individual;
    const mobileNumber = individual.findObservation('Mobile Number'); 
    if(mobileNumber) {
      summaries.push({name: 'Mobile Number', value: mobileNumber.getValueWrapper()});
    }
    return summaries;
};
```

<hr/>
<!-- END CHUNK -->

<!-- CHUNK: 12-hyperlink-menu-item-rule -->
## 12. Hyperlink menu item rule

- Logical scope = User
- Trigger = When More navigation is opened in the mobile app
- In designer = Coming very soon...
- When to use = When a dynamic link has to be provided to the user (these links cannot be specific to subjects)

### Shape of params object:

```
{
  user: {}, // User
  moment: {}, // moment. note other parameters are not supported yet,
  token, //Auth-token of the logged-in user
  myUserGroups //List of Group objects  
}
```

User: [https://github.com/avniproject/avni-models/blob/master/src/UserInfo.js](https://github.com/avniproject/avni-models/blob/master/src/UserInfo.js)

You need to return a string that is the full URL that can be opened in a browser.

### Example:

```
({params}) => {return `https://reporting.avniproject.org/public/question/11265388-5909-438e-9d9a-6faaa0c5863f?username=${encodeURIComponent(user.username)}&name=${encodeURIComponent(user.name)}&month=${imports.moment().month() + 1}&year=${imports.moment().year()}`;}
```

<hr/>
<!-- END CHUNK -->

<!-- CHUNK: 13-message-rule -->
## 13. Message rule

- When to use =  To configure sending Glific messages
- Logical scope = User, Subject, General and Program Encounter, Program Enrolment
- Trigger = 
  - For User : Only on creation of an User . 
  - For Subject, General and Program Encounter, Program Enrolment : On every save (create / update)
- In designer = "User Messaging Config", "Subject Type" , "Encounter type" and "Programs" page

Message Rule can be configured only when 'Messaging' is enabled for the organisation. Its configuration constitutes specifying following details:

- **Name** identifier name for the Message Rule
- **Template** Used to indicate the Skeleton of the message with placeholders for parameters
- **Receiver Type** Used to indicate the target audience for the Glific Whatsap message
- **Schedule** date and time configuration should return the time to send the message.
- **Message** content configuration should return the parameters to be filled in the Glific message template selected under 'Select Template' dropdown.

 Any number of message Rules can be configured.

### Example configuration:

Say, 'common_otp' Glific message template is 'Your OTP for `{{1}}` is `{{2}}`. This is valid for `{{3}}`.' If we want to send a OTP message that says 'Your OTP for receiving books is 1458. This is valid for 2 hours.' to a student after 1 day of their registration, then we need to configure for student subject type as shown in the below image (Note the shape of the return objects): 
![](https://files.readme.io/2e3e442-Screenshot_2023-12-27_at_6.15.54_PM.png)

```Text Schedule
'use strict';  
({params, imports}) => ({  
  scheduledDateTime: new Date("2023-01-05T10:10:00.000+05:30")  
});
```
```text Message
'use strict';  
({params, imports}) => {  
  const individual = params.entity;  
  return {  
    parameters: ['Verify user phone number', '0123', '1 day']  
  }  
};
```

### Shape of params object:

```
{
  entity: {}, //it could be one of User, Individual, General Encounter, ProgramEncounter or Program Enrolment depending on the type of form this rule is attached to
  user, //Current User's UserInfo object  
  myUserGroups //List of Group objects  
}
```
<!-- END CHUNK -->

<!-- CHUNK: 14-dashboard-card-rule -->
## 14. Dashboard Card Rule

The shape of dashboard card rule

```javascript
{
  db: "the realm db instance",
  user,
  myUserGroups,
  // ruleInput object can be null
  ruleInput: {
    type: "string. see 14.1 below",
    dataType: "values can be Default or Range",
    subjectType: "SubjectType model object. The subject type of the subjects to query and display to the user",
    groupSubjectTypeFilter: {
      subjectType: "SubjectType. The group subject type to filter by"
    },
    observationBasedFilter: {
      scope: "string. See 14.2 below",
      concept: "Concept. the observation value being referred to by the filter value",
      programs: {
         "UUID of the program": "Program model object"
      },
      encounterTypes: {
         "UUID of the encounter type": "Encounter Type model object"
      }
    },
    // filterValue can be null or empty array when there are no filters chosen by the user
    filterValue: "value chosen by the user. the type of data depends on the type of the filter"
  }
}
```

### Filter Value Shapes

**Address Filter**

```json
{
  "uuid":"924674dc-d32b-4276-b7b5-fb782f5511f2",
  "name":"Kerala",
  "level":4,
  "type":"State",
  "parentUuid":null,
}
```


14.1) [https://github.com/avniproject/avni-models/blob/8613b53edbf88e9b19150eda9e13da573e2a59ba/src/CustomFilter.js#L2](https://github.com/avniproject/avni-models/blob/8613b53edbf88e9b19150eda9e13da573e2a59ba/src/CustomFilter.js#L2)

14.2) [https://github.com/avniproject/avni-models/blob/8613b53edbf88e9b19150eda9e13da573e2a59ba/src/CustomFilter.js#L30](https://github.com/avniproject/avni-models/blob/8613b53edbf88e9b19150eda9e13da573e2a59ba/src/CustomFilter.js#L30)

<hr/>

### 15. Manual Programs Eligibility Check Rule

This rule is used when the user fills a form based on which the eligibility of given program is determined by this rule.

#### Shape of Input Object

```javascript
params: {
  entity: typeof SubjectProgramEligibility,
  subject: typeof Individual,
  program: typeof Program,
  services,
  user, //Current User's UserInfo object  
  myUserGroups //List of Group objects  
},
imports: {}
```

#### Return

_boolean_

### 16. Member Addition Eligibility Check Rule

This rule is used to determine whether an **existing** member can be added to a group or household. The rule is configured at the subject type level and is executed when a user attempts to add an existing member to a group/household.

- Logical scope = Group/Household and Individual
- Trigger = On attempt to add a member to a group/household
- In designer = Subject Type (Member Addition Eligibility Check Rule)
- When to use = To validate if an **existing** individual can be added as a member to a specific group/household based on custom business rules

#### Shape of Input Object

```javascript
params: {
  member: typeof Individual, // The individual being added as a member
  group: typeof Individual, // The group/household to which the member is being added
  context: Object, // The execution context
  services,
  user, // Current User's UserInfo object  
  myUserGroups // List of Group objects  
},
imports: {}
```

#### Return

This rule should return an object that follows the ActionEligibilityResponse format, with the following structure:

```javascript
// For allowing addition
{
  eligible: {
    value: true
  }
}

// For disallowing addition with a reason
{
  eligible: {
    value: false,
    message: "Reason why the member cannot be added" //Value of message has translation support.
  }
}
```

#### Example

**Use Case:**

While adding members to a "Self-help" group, we need to validate that the person is an adult, in-which case we would come up with the following

**Member Addition Eligibility Check Rule:**

```javascript
"use strict";
({params, imports}) => {
  const member = params.member;
  const group = params.group;
  
  // Example: Only allow adding members who are above 18 years of age
  const age = member.getAgeInYears();//As on current date
  
  if (age < 18) {
    return {
      eligible: {
        value: false,
        message: "Only individuals above 18 years can be added to this group"
      }
    };
  }
  
  return {
    eligible: {
      value: true
    }
  };
};
```

**Reference Screenshot, when Member Addition Eligibility Check Rule fails:**
![](https://files.readme.io/aaa48f09aa4c5bcaebf2d9ae72f19c0777e719bd463b213b43e011796fd8db0a-Screenshot_2025-06-27_at_7.41.28_PM.png)

#### Error Handling

When a Member Addition Eligibility Check rule fails (throws an exception), the error is logged and stored in the RuleFailureTelemetry with the following information:

- source_type: 'MemberAdditionEligibilityCheck'
- source_id: UUID of the subject type
- entity_type: 'Individual'
- entity_id: UUID of the group/household to which a member is being added
- individual_uuid: UUID of the individual being added to the group/household

### 17. Edit Form Rule

This rule is used when the user tries to edit a form. If non-boolean value is returned in the value, or the rule fails, then it would be treated as true and edit will be allowed. To check the places where it is available, not available, & not applicable - [https://avni.readme.io/docs/rules-concept-guide#edit-form-rule](https://avni.readme.io/docs/rules-concept-guide#edit-form-rule).Value of message has translation support.

#### Sample Rule

```
"use strict";
({params, imports}) => {
    const {entity, form, services, entityContext, myUserGroups, userInfo} = params;

    const output = {
      eligible : {
        value: false, //return false to disallow, true to allow;
        message: 'Edit access denied: <Specify reason here>.' //optional
      } 
    }; 

    return output;
};
```

#### Shape of Input Object

```javascript
params: {entity, services, form, myUserGroups,user},
imports: {}
```

#### Shape of return object

```javascript
// Previous format (still supported)
const output = {
  editable : {
    value: true/false,
    messageKey: 'foo'
  }
};

// New format (generic for all rule based access control)
const output = {
  eligible : {
    value: true/false,
    message: 'foo'
  }
};
```

### 18. Global reusable code rule (Alpha)

This rule is intended maintaining reusable JavaScript functions across implementations. While this could also be used within implementation only but that is not the purpose of this. If you want to create reusable JavaScript code within an implementation only, please check with the product management team to get it prioritised.

> 📘 Not supported in Data entry app. Feature available from 11.0 version.

#### Shape of Input Object

```javascript
// Get handle to the reusable function
const globalFunction = imports.globalFn;
// invoke your function, two examples below.
globalFn().hello();
globalFn().sum(1,2);
```

Note that you can define the signature of your new function (like hello, sum). It is not determined by the global function.

#### How to deploy global function (TBD)

1. Use `make deploy-global-rule`.
   1. Provide the origin and token
   2. The token will determine the organisation to which it is deployed. Rerunning it will update the previous rule.
2. Run sync in the mobile app
<!-- END CHUNK -->

<!-- CHUNK: accessing-address-level-properties -->
## Accessing Address Level Properties :

Old Way is to get the address level properties and extract from the json object. In new way, get the address level and access its observation value as per location attribute form.

```Text JavaScript
'use strict';
({params, imports}) => {
  const programEncounter = params.entity;
  const moment = imports.moment;
  const formElement = params.formElement;
  const _ = imports.lodash;
  let visibility = false;
  let value = 'No';
  let answersToSkip = [];
  let validationErrors = [];
  
  const address_level = programEncounter.programEnrolment.individual.lowestAddressLevel;  
  
  const gHighRisk = address_level.getObservationReadableValue("Geographically hard to reach village");

  if(gHighRisk === "Yes"){
      value = 'Yes';
  }

  
  return new imports.rulesConfig.FormElementStatus(formElement.uuid, visibility, value, answersToSkip, validationErrors);
};
```
<!-- END CHUNK -->

<!-- CHUNK: handling-rule-evaluation-across-mobile-and-web-app -->
## Handling rule-evaluation across Mobile and Web Applications

This section provides guidelines for handling rule-evaluation across Mobile and Web Applications in Avni implementations. It includes practical examples from the Goonj implementation.

### Detecting Web Application Context

To determine if the application is running in a web context, you can check the `titleLineage` property of the lowest address level:

```javascript
const webapp = individual.lowestAddressLevel.titleLineage;
```

This pattern is used to identify if the application is running in a web context and adjust behavior accordingly.

### Handling Webapp-Specific Scenarios

When working with web applications, consider the following:

- Some validations might need to be bypassed in web context
- UI/UX might need adjustments for web vs mobile
- Performance considerations might differ between platforms

#### Basic Pattern

```javascript
function handleWebappContext(individual) {
    const webapp = individual.lowestAddressLevel.titleLineage;
    
    // Apply webapp-specific logic
    if (webapp) {
        // Webapp-specific code here
    } else {
        // Mobile-specific code here
    }
}

try {
    handleWebappContext(individual);
} catch (error) {
    console.error('Error handling webapp context:', error);
}
```

#### Examples

In the Goonj implementation, we encountered an issue where certain validations were failing in the web context but were not applicable to web users.

##### 1. Webapp Detection and Validation Bypass

```javascript
function validateForm(individual, formData) {
    const webapp = individual.lowestAddressLevel.titleLineage;
    const errors = [];
    
    // Skip webapp-specific validations for web users
    if (!webapp) {
        // Mobile-only validations go here
        if (!formData.requiredField) {
            errors.push('This field is required for mobile users');
        }
    }
    
    // Common validations for both web and mobile
    if (!formData.commonField) {
        errors.push('This field is required for all users');
    }
    
    return errors.length ? errors : null;
}
```

##### 2. Location Validation Example

```javascript
function validateLocation(individual, locationData) {
    const webapp = individual.lowestAddressLevel.titleLineage;
    
    // Skip location validation for webapp
    if (webapp) {
        return null;
    }
    
    // Mobile location validation logic
    if (!locationData || !locationData.coordinates) {
        return ['Location is required for mobile users'];
    }
    
    return null;
}
```
<!-- END CHUNK -->

<!-- CHUNK: accessing-audit-fields-when-writing-rules -->
## Accessing audit fields when writing rules

#### When writing rules, you often need to access information about who created or modified entities, and when these actions occurred. Avni provides several audit fields that can be accessed through the entity object in your rules.

Available Audit Fields

  The following audit fields are available :

- createdByUUID
- lastModifiedByUUID
- createdBy
- lastModifiedBy
- filledBy (only for program and general encounters)
- filledByUUID (only for program and general encounters)

```coffeescript JS
//SAMPLE EDIT FORM RULE
  "use strict";
({params, imports}) => {
const {entity} = params;
console.log("params.entity.createdByUUID:", params.entity.createdByUUID);
console.log("params.entity.lastModifiedByUUID:", params.entity.lastModifiedByUUID);

console.log("params.entity.createdBy:", params.entity.createdBy);
console.log("params.entity.lastModifiedBy:", params.entity.lastModifiedBy);

console.log("params.entity.filledBy:", params.entity.filledBy);
console.log("params.entity.filledByUUID:", params.entity.filledByUUID);

return output;
};
```
<!-- END CHUNK -->

<!-- CHUNK: using-params-db-object-when-writing-rules -->
## Using params.db object when writing rules

In many of the rules params db object is available to query the offline database directly. The db object is an instance of type [Realm](https://www.mongodb.com/docs/realm-sdks/js/latest/classes/Realm-1.html) on which [objects](https://www.mongodb.com/docs/realm-sdks/js/latest/classes/Realm-1.html#objects) is first method that will get called. This returns [Realm Results](https://www.mongodb.com/docs/realm-sdks/js/latest/classes/Results.html) instance, on which one may further call the [filtered](https://www.mongodb.com/docs/realm-sdks/js/latest/classes/Results.html#filtered) method one or more times each time returning realm results. Realm result a list with each item being of type (model object's schema name) originally passed in objects method.

```coffeescript JS
'use strict';
({params, imports}) => {
  //...
  
  const db = params.db;
  const farmers = db.objects("Individual").filtered(`voided = false AND subjectType.uuid = "73271784-512d-4435-8dc8-0f102b99d682"`);
  console.log('Found farmers with count', farmers && farmers.length > 0 && farmers.length);

  //...
  return new imports.rulesConfig.FormElementStatus(formElement.uuid, visibility, value, answersToSkip, validationErrors);
};
```


**Realm Query Language Reference** - [https://www.mongodb.com/docs/realm/realm-query-language](https://www.mongodb.com/docs/realm/realm-query-language)

### Difference between filter and filtered

`filtered` method is like running SQL query executed closer or in the database process and hence it orders of magnitude faster than `filter` - which is JavaScript method ran by constructing model object for each item is JS memory and then passing it through the filter function. As much as possible filtered should be used for best performance and user experience.

### Example of filtered

```javascript
({params}) => {
  const db = {params};
  return db.objects("Individual").filtered(`voided = true AND subjectType.name = "Foo"`);
}
```
<!-- END CHUNK -->

<!-- CHUNK: using-service-methods-in-the-rules -->
## Using service methods in the rules

Often, there is the need to get the context of implementation beyond what the models themselves provide. For example, knowing other subjects in the location might be necessary to run a specific rule. For such scenarios, Avni provides querying the DB using the services passed to the rules.

The services object looks like this

```javascript
{
    individualService: '',
}
```

Right now only individual service is injected into all the rules. One method which is implemented right now returns an array of subjects in a particular location. The method looks like the following, it takes address-level object and subject type name as its parameters and returns a list of all the subjects in that location.

```javascript
getSubjectsInLocation(addressLevel, subjectTypeName) {
  const allSubjects = ....;
  return allSubjects;
}
```

Note that this function is not implemented for the data entry app and throws a "method not supported" error for all the rules when run from the data entry app.

### Service methods available are:

- [https://github.com/avniproject/avni-client/blob/master/packages/openchs-android/src/service/facade/IndividualServiceFacade.js](https://github.com/avniproject/avni-client/blob/master/packages/openchs-android/src/service/facade/IndividualServiceFacade.js)
- [https://github.com/avniproject/avni-client/blob/master/packages/openchs-android/src/service/facade/AddressLevelServiceFacade.js](https://github.com/avniproject/avni-client/blob/master/packages/openchs-android/src/service/facade/AddressLevelServiceFacade.js)

### Examples

The view-filter rule is for the subject data type concept that displays all the subjects of type 'Person' in the passed location. 

```
'use strict';
({params, imports}) => {
  const encounter = params.entity;
  const formElement = params.formElement;
  const statusBuilder = new imports.rulesConfig.FormElementStatusBuilder({encounter, formElement});
  const individualService = params.services.individualService;
  const subjects = individualService.getSubjectsInLocation(encounter.individual.lowestAddressLevel, 'Person');
  const uuids = _.map(subjects, ({uuid}) => uuid);
  statusBuilder.showAnswers(...uuids);
  return statusBuilder.build();
};
```


#### Fetch Subjects by Subject Type with Custom Filtering

For business reasons, you may need to fetch subjects of a specific type with additional filtering criteria.

##### Using IndividualServiceFacade "getSubjects" method

Use IndividualServiceFacade`getSubjects(subjectTypeName, realmFilter)` method to get subjects by type with optional filtering.

##### Method Signature

- subjectTypeName (string): The name of the subject type (e.g., 'Volunteer', 'Patient', 'Household')
- realmFilter (string, optional): Realm query filter string for additional filtering

```js

  const individualService = params.services.individualService;
  const volunteers = individualService.getSubjects('Volunteer');
  console.log('volunteers:', volunteers.length);

  const subjectsWithObservation = individualService.getSubjects(
    'Patient',
    'SUBQUERY(observations, $obs, $obs.concept.uuid == "concept-uuid-here").@count > 0'
  );
  console.log('Patients with specific observation:', subjectsWithObservation.length);

  
```
<!-- END CHUNK -->

<!-- CHUNK: using-other-group-household-individuals-informatio -->
## Using other group/household individuals' information in the rules

Say, an individual belongs to a group A. Sometimes, there is a need to use data of other individuals in the group A.  For example, to auto-populate caste information in an individual's registration form (say, when navigated to individual's registration form when tried to add a member to group/household A), we might need to know the caste information of other individuals in that group/household. For such scenarios, Avni provides a way to access `group` object from `params.entityContext`.

### Example

The below rule is for the case when an individual's concept named `Caste` needs to be auto-populated based on other member's data in the same group.

```
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
  
  const groupSubject = params.entityContext.group;
  if(groupSubject.groupSubjects.length > 0) {
     const ind = params.entityContext.group.groupSubjects[0].memberSubject;
     const caste = ind.getObservationReadableValue('Caste');
     value = caste; 
  }
  
  return new imports.rulesConfig.FormElementStatus(formElement.uuid, visibility, value, answersToSkip, validationErrors);
};
```
<!-- END CHUNK -->

<!-- CHUNK: handling-special-scenarios-while-updating-value-us -->
## Handling special scenarios while updating value using FormElementStatus rule

### How to reset value using FormElement Rule logic

When the FormElementStatus value is set to null, by default it is treated as a No-action operation and hence we do not reset the value of the concept.

But instead, if we are trying to say that "I am not setting the value", and any previous value has to be reset, then we need to specify the resetValueIfNull argument to be **true** in the FormElementStatus constructor, used to generate response during the rule execution.

```
'use strict';
({params, imports}) => {

//Rule content
  
//FormElementStatus Constructor signature
return new imports.rulesConfig.FormElementStatus(formElementUUID, visibility, value, answersToSkip = [], validationErrors = [], answersToShow = [], resetValueIfNull = false);
}
```


### Handle set of Modifiable Select Coded Concepts

In-order to init a modifiable Select Coded Concept FormElement's Value in a form, you can specify the AnswerConcept **Name** as the value, which should be enough to set the initial value as expected.

### Handle set of Read-Only Select Coded Concepts

There were 2 issues that were preventing implementation team from reliably setting a **Read-only** SingleSelectCodeConcept's value via FormElement Rules:

1. Selection of a AnswerConcept
2. Stablizing the selected value over multiple execution of FormElement rule due to changes elsewhere in the FormElementGroup

#### Recommended solution

To resolve these issues, we only needed to make following adjustments in the FormElement Rule:

1. Selection of a AnswerConcept => Make use of AnswerConcept's UUID instead of name as value
2. Stablizing the selected value  => 
   > - Mark the SelectedCodedConcept value as ReadOnly 
   > - For Multi-select: Return a FormElementStatus object with only the difference between previous valueArray and new valueArray. If no change in value, then return empty array.
   > - For Single-select: Return a FormElementStatus object with selected value, only if previousValue was null. If not, return null.

This would toggle the answers as expected and result in only the expected value(s) being shown as selected. 

#### Example Rule for SingleSelect FormElement set via Rule

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
    
    const condition11 = triue; //some visibility condition
    visibility = condition11;
     
    if (condition11) {
       //some business logic
          if(someCondition) {
             value = "conceptUUID1";
          }
          else{
             value = "conceptUUID2";
          }
       }
    }
    let que = individual.findGroupedObservation('bafb80ac-6088-4649-8ed3-0501e1296c6e')[params.questionGroupIndex];
    if(que){
      let obs = que.findObservationByConceptUUID('ef952d55-f879-4c34-99e2-722c680ed2e2');
      if(obs && obs.getValue() === value) {//i.e obs.getValue() are both same answerConcept
         return null;//Old value is retained
       }   
    }
    else {
       return new imports.rulesConfig.FormElementStatus(formElement.uuid, visibility, value, answersToSkip, validationErrors); //new value is updated
    }
};
```

### Handle Uniqueness validation for Read-Only Text field

As the value for the ReadOnly TextFormElement is set via Rule of some sort, the validation for enforcing uniqueness too has to be done during the same rule execution.

#### Example FE rule for enforcing Uniqueness validation on Read-only Text field

```Text Javascript
'use strict';
({params, imports}) => {
    const individual = params.entity;
    const moment = imports.moment;
    const _ = imports.lodash;
    const formElement = params.formElement;
    let visibility = true;
    let value = null;
    let validationErrors = [];
    let nameNotUnique = false;
    
    
   //Business logic to set value
   value = '[dummy3]as';


    //Execute some business logic to update nameNotUnique 
    nameNotUnique = (value === '[dummy3]as');
    
    if(nameNotUnique) {
       validationErrors.push('Another Work Order has same value');
    }
   
    return new imports.rulesConfig.FormElementStatus(formElement.uuid, visibility, value, null, validationErrors);
};

```


### Handle Fetch of Individuals with specific Phone Numbers for duplicates validation

For business reasons, we might need to verify that there are **No / Limited number of** duplicate Subjects with the same Phone Number. To do this, we have 2 possible approaches:

#### 1. Use IndividualServiceFacade "findAllSubjectsWithMobileNumberForType" helper method

Use IndividualServiceFacade.findAllSubjectsWithMobileNumberForType(mobileNumber, subjectTypeUUID) method to get subjects with same phone number.

**Requires the PhoneNumber concept to have, KeyValue (primary_contact : yes) or (contact_number : yes)**
![](https://files.readme.io/f48da098be8218e797e7dd841e023036199eb0b7aa696ece422a6974e0b3f56f-421821795-e7b7766d-3865-4a66-a66e-93f4ddc8b13d.png)

```js

  const individualService = params.services.individualService;
  const subjects = individualService.findAllSubjectsWithMobileNumberForType('', "<subject_type_uuid>");
  console.log('found subjects with number', subjects && subjects.length > 0);
  
```

#### 2. [Using params.db object to find duplicates with custom filter logic](/docs/writing-rules#using-paramsdb-object-when-writing-rules)
<!-- END CHUNK -->

<!-- CHUNK: types-of-rules-and-their-support-availability-in-d -->
## Types of rules and their support/availability in Data Entry App

| Not supported                          | Supported via rules-server       | Supported in browser     |
| :------------------------------------- | :------------------------------- | :----------------------- |
| Global reusable function               | Enrolment eligibility check rule | Form Element Rule        |
| Dashboard Card rule (NA)               | Encounter eligibility check rule | Form Element GroupRule   |
| Checklists rule                        | Visit schedule rule              | Enrolment Summary Rule   |
| Work list updation rule                | Message rule                     | Hyperlink menu item rule |
| Hyperlink menu item rule               | Decision rule                    |                          |
| Validation rule                        |                                  |                          |
| Edit Form rule                         |                                  |                          |
| Member addition eligibility check rule |                                  |                          |
<!-- END CHUNK -->

<!-- CHUNK: types-of-rules-and-their-support-availability-in-t -->
## Types of rules and their support/availability in transaction data upload

| Not supported | Supported via rules-server | Not Applicable                   |
| :------------ | :------------------------- | :------------------------------- |
| Message rule  | Visit schedule rule        | Hyperlink menu item rule         |
|               | Decision rule              | Enrolment Summary Rule           |
|               | Validation rule            | Form Element GroupRule           |
|               |                            | Form Element Rule                |
|               |                            | Encounter eligibility check rule |
|               |                            | Enrolment eligibility check rule |
|               |                            | Hyperlink menu item rule         |
|               |                            | Work list updation rule          |
|               |                            | Checklists rule                  |
|               |                            | Dashboard Card rule              |
<!-- END CHUNK -->

<!-- CHUNK: related-topics -->
## Related Topics

<!-- Add links to related documentation -->
<!-- END CHUNK -->