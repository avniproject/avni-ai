---
title: Designing Workflows and Data Models in Avni
category: subject-types-programs
audience: implementer
difficulty: intermediate
priority: high
keywords:
- workflow design
- data model
- implementation planning
- program design
last_updated: '2026-03-16'
task_types:
- tutorial
- best-practice
features:
- subjects
- programs
- encounters
technical_level:
- conceptual
- procedural
implementation_phase:
- planning
- development
complexity: moderate
retrieval_boost: 1.5
related_topics:
- subject-types.md
- programs.md
- encounter-types.md
estimated_reading_time: 3 minutes
version: '1.0'
---
# Designing Workflows and Data Models in Avni

<!-- CHUNK: tldr -->
## TL;DR

As explained in Implementer's concept guide - Introduction - subject, program and encounter are the three key building blocks you have - using which you can model almost all field-based work. Groups (households) that are a special type of subject will be treated as the fourth building block.
<!-- END CHUNK -->

<!-- CHUNK: overview -->
## Overview

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


title: Introduction
excerpt: ''
    - type: basic
      slug: avnis-domain-model-of-field-based-work
      title: Avni's domain model of field based work
---
Implementer's concept guide is for anyone who would like to implement Avni for any field-based program. We recommend this guide to be the first one to be read by anyone wanting to understand Avni.

While internally there are many parts of the system, if you are an implementer and using the hosted instance then these are the components you will be using. Some of the functions are intended for the end-users but you will use them for testing the application.

![User/Implementer components of Avni](https://files.readme.io/9fa4f1f-Avni_4.png)


title: Developing BI dashboards using AI services
excerpt: >-
  robots: index
next:
  description: ''
---
The tool used for this is Cursor which internally uses other AI services. You can download [Cursor](https://www.cursor.com/).

The source code used in this tool is available here [avni-ai-experiment](https://github.com/avniproject/avni-ai-experiment) (private repository as the CSV files used in the context may contain customer specific information). This repository will become a public repository soon.
<!-- END CHUNK -->

<!-- CHUNK: generate-aggregate-and-line-list-query -->
## Generate aggregate and line list query

### When to use

Excel or spreadsheet contain the requirements for the report all present in a single sheet. This is the input used for generating the SQL. If you do not have this file then the steps below are **not recommended** as it will not be productive approach.

### Setup

1. Open avni-ai-experiment in Cursor.
2. Download the requirement sheet as a CSV file. Copy its contents and put them in any file under `bi-reporting-spike/dataset/workspace` folder. Let's say - `requirement.csv`. An example is present in workspace folder by name `example.csv`.
3. Create one file which contains all the table definition in the `bi-reporting-spike/aggregate/workspace`  or `bi-reporting-spike/linelist/workspace` folder. Let's say - `table-def.sql`. An example is present in workspace folder by name `example-jnpct-def.sql`. This was generated from IntelliJ (select schema and generate).

### Chat

1. Open chat window in Cursor.
2. Prompt to forget everything (line 1 of `aggregate-query-prompt.md` or `linelist-query-prompt.md`)
3. Follow the steps in [https://github.com/avniproject/avni-ai-experiment/blob/main/bi-reporting-spike/aggregate/workspace/aggregate-query-prompt.md](https://github.com/avniproject/avni-ai-experiment/blob/main/bi-reporting-spike/aggregate/workspace/aggregate-query-prompt.md) or [https://github.com/avniproject/avni-ai-experiment/blob/master/bi-reporting-spike/linelist/workspace/line-list-prompt.md](https://github.com/avniproject/avni-ai-experiment/blob/master/bi-reporting-spike/linelist/workspace/line-list-prompt.md)
<!-- END CHUNK -->

<!-- CHUNK: related-topics -->
## Related Topics

<!-- Add links to related documentation -->
<!-- END CHUNK -->