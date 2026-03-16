---
title: Programs in Avni
category: subject-types-programs
audience: implementer
difficulty: beginner
priority: critical
keywords:
- programs
- program enrollment
- program exit
- longitudinal tracking
last_updated: '2026-03-16'
task_types:
- configuration
- reference
features:
- programs
technical_level:
- conceptual
- procedural
implementation_phase:
- development
complexity: moderate
retrieval_boost: 2.0
related_topics:
- encounter-types.md
- subject-types.md
- workflow-design.md
estimated_reading_time: 2 minutes
version: '1.0'
---
# Programs in Avni

<!-- CHUNK: tldr -->
## TL;DR

A program defines the service, or intervention that you provide to subjects.
<!-- END CHUNK -->

<!-- CHUNK: overview -->
## Overview

A program defines the service, or intervention that you provide to subjects.

A subject is enrolled into the program using the Enrolment Form. Routine information is collected through Encounters. A subject exits a program by filling in the Exit Form.

- [Learn more about Avni's domain model](https://avni.readme.io/docs/avnis-domain-model-of-field-based-work)
- [Learn more about writing rules](https://avni.readme.io/docs/rules-concept-guide)


title: Setting up your data model
excerpt: ''
    - type: basic
      slug: my-dashboard-and-search-filters
      title: My Dashboard and Search Filters
---
As explained in Implementer's concept guide - Introduction - subject, program and encounter are the three key building blocks you have - using which you can model almost all field-based work. Groups (households) that are a special type of subject will be treated as the fourth building block.

In the web application, you would see three menus which map to above - subject types, programs and encounter types. You must be assigned an organisation admin role to be able to do this. If you are, then you can see these options under the Admin section. Each one of the following is linked to their respective forms which you can navigate from the user interface.

![](https://files.readme.io/f4090d7-Screenshot_2020-04-28_at_11.30.58_AM.png "Screenshot 2020-04-28 at 11.30.58 AM.png")

When setting up your model you will be defining the concepts and forms. The diagram below explains the relationship between entities above, form and concepts. Currently, in the application, you may need to go to the concept's view to edit it fully. Soon we would provide seamless editability of the underlying concept via form editing.

![](https://files.readme.io/f678cdd-Screenshot_2020-04-28_at_6.44.23_PM.png "Screenshot 2020-04-28 at 6.44.23 PM.png")

An example form below of name "Child Enrolment", with one form element group called "Child Enrolment Basic Details". This form element group has 6 form elements.

![](https://files.readme.io/eb3a4bf-Screenshot_2020-04-28_at_7.13.21_PM.png "Screenshot 2020-04-28 at 7.13.21 PM.png")

One of the form element is displayed below with all the details. The concept used by the form element is also displayed like allow data range values. From this screen, as of now, it is not editable you need to go to the concepts tab to edit it.

![](https://files.readme.io/f968766-Screenshot_2020-04-28_at_7.17.04_PM.png "Screenshot 2020-04-28 at 7.17.04 PM.png")

You can specify the skip logic for under the rule tab within the form element. This currently is done only using JavaScript, but in future, one would be able to do it using the UI directly. For more on rules please see the Writing rules.

![](https://files.readme.io/661ab7b-Screenshot_2020-05-19_at_4.49.43_PM.png "Screenshot 2020-05-19 at 4.49.43 PM.png")
<!-- END CHUNK -->

<!-- CHUNK: related-topics -->
## Related Topics

<!-- Add links to related documentation -->
<!-- END CHUNK -->