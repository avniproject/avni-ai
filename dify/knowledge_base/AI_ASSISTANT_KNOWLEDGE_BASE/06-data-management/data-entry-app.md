---
title: Web-Based Data Entry Application
category: data-management
audience: implementer
difficulty: beginner
priority: medium
keywords:
- data entry
- web app
- data entry application
- web-based data entry
last_updated: '2026-03-16'
task_types:
- tutorial
features:
- forms
technical_level:
- procedural
implementation_phase:
- deployment
complexity: simple
retrieval_boost: 1.0
related_topics:
- ../03-concepts-and-forms/form-structure.md
estimated_reading_time: 1 minutes
version: '1.0'
---
# Web-Based Data Entry Application

<!-- CHUNK: tldr -->
## TL;DR

The Data Entry App, as the name suggests, is used to view and enter data directly without relying on mobile syncing. It can be accessed by clicking on the 'Data Entry app' tile in the home page.
<!-- END CHUNK -->

<!-- CHUNK: overview -->
## Overview

The Data Entry App, as the name suggests, is used to view and enter data directly without relying on mobile syncing. It can be accessed by clicking on the 'Data Entry app' tile in the home page.

![image](https://files.readme.io/be9c75e10c6f8e1eb905f84e0714b46475192e039bac88837f38b62c87cabf91-Screenshot_2025-08-25_at_7.10.40_PM.png)

### Advantages:

* **Instant access**: When you are on a computer with internet access, you can view and enter data without downloading or syncing data like in the mobile app.
* **Larger data coverage**: On the mobile app, the maximum number of catchment locations that can be synced is 65,535. If you need to view data across more locations, the Data Entry App can be used.

### Features not supported in Data Entry App:

**Rules related limitations:**

* [Edit form rule](https://avni.readme.io/docs/writing-rules#17-edit-form-rule)
* [Member addition eligibility check rule](https://avni.readme.io/docs/writing-rules#16-member-addition-eligibility-check-rule)
* [Manual programs eligibility check rule](https://avni.readme.io/docs/writing-rules#15-manual-programs-eligibility-check-rule)
* [Rules that use service methods to filter across subjects](https://avni.readme.io/docs/writing-rules#using-service-methods-in-the-rules)


**Other unsupported features:**

* [User subject type](https://avni.readme.io/docs/user-subject-types)
* [Dashboards and report cards](https://avni.readme.io/docs/offline-reports)
* [Drafts](https://avni.readme.io/docs/draft-save)
* [Approval workflows](https://avni.readme.io/docs/approval-workflow)
* [Vaccination checklist](https://avni.readme.io/docs/upload-checklist)
* [Growth chart](https://avni.readme.io/docs/child-growth-charts)
* Details on who performed a registration, enrolment or visit
* Viewing of data outside of a user's catchment and configured sync attribute cannot be restricted. Only editing can be restricted.
<!-- END CHUNK -->

<!-- CHUNK: related-topics -->
## Related Topics

<!-- Add links to related documentation -->
<!-- END CHUNK -->