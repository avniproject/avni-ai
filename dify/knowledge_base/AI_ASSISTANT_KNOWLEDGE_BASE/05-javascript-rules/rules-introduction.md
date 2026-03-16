---
title: Introduction to Avni Rules Engine
category: javascript-rules
audience: implementer
difficulty: beginner
priority: critical
keywords:
- rules engine
- JavaScript rules
- rule types
- rules overview
last_updated: '2026-03-16'
task_types:
- reference
- tutorial
features:
- rules
technical_level:
- conceptual
implementation_phase:
- development
complexity: simple
retrieval_boost: 2.0
related_topics:
- validation-rules.md
- decision-rules.md
- visit-schedule-rules.md
estimated_reading_time: 2 minutes
version: '1.0'
---
# Introduction to Avni Rules Engine

<!-- CHUNK: tldr -->
## TL;DR

Avni uses rules, or more accurately snippets of code (functions are written in JavaScript) in multiple places to provide flexibility to the implementers/developers to customise what Avni can do for the users. One can think of the rule system of Avni as a set of hooks that can be used by the rule ...
<!-- END CHUNK -->

<!-- CHUNK: overview -->
## Overview

Avni uses rules, or more accurately snippets of code (functions are written in JavaScript) in multiple places to provide flexibility to the implementers/developers to customise what Avni can do for the users. One can think of the rule system of Avni as a set of hooks that can be used by the rule authors to plug their own data/behaviour/logic to the app when it is used in the field and in the data entry application.

The rules are simple JavaScript functions that receive all the data via function parameters and they should return to the platform what it wants to get done. There is no state that needs to be maintained by JavaScript functions across invocations.
<!-- END CHUNK -->

<!-- CHUNK: why-are-rules-needed-in-avni -->
## Why are rules needed in Avni?

Since Avni is a general-purpose platform it doesn't know certain details about your problem domain. Wherever Avni doesn't know this - it leaves a hook for the implementer to provide the missing functionality.
<!-- END CHUNK -->

<!-- CHUNK: overview-of-various-rules -->
## Overview of various rules

Complete programmatic reference is provided in the Writing rules, the following diagram explains how most of the rules are used. It displays navigation between the different screens and shows the rules that are triggered in the yellow boxes.

![image](https://files.readme.io/37b4a00-Screenshot_2024-02-21_at_8.51.57_PM.png)

In most rules, the rule has access to all the data of the subject and any data that is logically linked to the subject. e.g. In an encounter form level rule, one can access its subject form data, subject's relatives data, subject's relatives encounter data and so on.

#### Validation Rule

Validate the entire form. Last page of the form wizard. One per form.

#### Decision Rule

Add additional system generated observations. Last page of the form wizard. One per form.

#### Visit (Encounter) Schedule Rule

Create scheduled encounters with only due dates and no data.

#### Worklist Updation Rule

To display next forms on completion of one form.

#### Subject/Enrolment Summary

Display chosen information to summarise subject/enrolment on Subject dashboard screen.

#### Encounter/Enrolment Eligibility Check Rule

Before displaying list of forms that the user can fill check and filter out forms.

#### Manual Enrolment Eligibility Check Rule

If this rule is present, a custom form is shown to the user when the user starts enrolment. Based on the data filled and other subject data the rule decides which programs to display.

#### Edit Form Rule

If defined it can disallow editing of any form based on the rule. This rule is applied after access control is checked. This is available for: Registration, Enrolment, Enrolment Exit, Program Encounter, Program Encounter Cancel, General Encounter, General Encounter Cancel, Group Subject Registration, Form Element Group Edit and Checklist Item. It is not available/applicable for:

* Location
* Task (as there is no edit screen for it)
* SubjectEnrolmentEligibility, ManualProgramEnrolmentEligibility (these are unused features as of now)
* Encounter Drafts, Scheduled Encounters - should always be editable/fillable unless controlled by access control.
<!-- END CHUNK -->

<!-- CHUNK: related-topics -->
## Related Topics

<!-- Add links to related documentation -->
<!-- END CHUNK -->