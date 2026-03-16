---
title: Writing Task Schedule Rules
category: javascript-rules
audience: implementer
difficulty: advanced
priority: medium
keywords:
- task schedule
- task rules
- task assignment
- task management
last_updated: '2026-03-16'
task_types:
- tutorial
- example
features:
- rules
technical_level:
- procedural
implementation_phase:
- development
complexity: complex
retrieval_boost: 1.0
related_topics:
- rules-introduction.md
- helper-functions.md
estimated_reading_time: 2 minutes
version: '1.0'
---
# Writing Task Schedule Rules

<!-- CHUNK: tldr -->
## TL;DR

Most activities in Avni are modeled as encounters with subjects, sometimes linked to a program. However, there are other kinds of data collection that happens in field work that is not related to any subject.\
eg: A list of contacts that need to be contacted first before creating subjects etc.
<!-- END CHUNK -->

<!-- CHUNK: overview -->
## Overview

Most activities in Avni are modeled as encounters with subjects, sometimes linked to a program. However, there are other kinds of data collection that happens in field work that is not related to any subject.\
eg: A list of contacts that need to be contacted first before creating subjects etc.  

To handle such flows, Avni now has a new mechanism called tasks. Tasks can currently be created only through the external API. They can be assigned to people, who can change the status of a task.
<!-- END CHUNK -->

<!-- CHUNK: task-concepts -->
## Task Configuration

Task configuration is handled currently through SQL inserts since there are no mechanisms on the App Designer. Given below are the new concepts introduced in the task configuration. 

### Task types

A task can have a type. There are currently two kinds of task types - Call and Open Subject. A Call type task helps the user call the user, while the open subject task allows the user to navigate to the subject assigned to the task. 

### Task status

A number of statuses can be configured for a task. This helps in moving these calls into buckets. Some of these cards can be marked as "terminal" tasks. A terminal task indicates that the task is complete. 

### Task search fields

If you configure a list of concepts as task search fields, they are available in the Assignment screen for filtering. This is configured per task type

### Task metadata

Some metadata (concept:value array) can be set on a task when creating it. This will help users get more information on a task before taking actions on them. 

### Task observations

Task observations are filled in when completing a task. A new form type called "Task" is configured for this purpose. The user will be given the option to fill in the form when completing a task. 

### Standard report cards for task

There is a standard report card that can be configured for tasks. This is currently the only way tasks will be visible on the Avni android app.
<!-- END CHUNK -->

<!-- CHUNK: task-assignment -->
## Task assignment

The web application provides a new option - "Assignment" to assign users to a task. Only one user can be assigned to a task at this time. If you assign a new user, the old user is unassigned. 

### Caveats

* Task type configuration does not have an interface on the App Designer. 
* Tasks can only be created through the external API
* Tasks can be assigned through the Assignment feature on the web application
* Tasks are not currently supported on the Data Entry App
<!-- END CHUNK -->

<!-- CHUNK: related-topics -->
## Related Topics

<!-- Add links to related documentation -->
<!-- END CHUNK -->