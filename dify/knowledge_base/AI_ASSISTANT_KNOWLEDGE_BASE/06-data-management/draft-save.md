---
title: Draft Save Feature
category: data-management
audience: implementer
difficulty: beginner
priority: medium
keywords:
- draft save
- save draft
- incomplete forms
- draft data
last_updated: '2026-03-16'
task_types:
- configuration
features:
- forms
technical_level:
- procedural
implementation_phase:
- development
complexity: simple
retrieval_boost: 1.0
related_topics:
- ../03-concepts-and-forms/form-structure.md
estimated_reading_time: 2 minutes
version: '1.0'
---
# Draft Save Feature

<!-- CHUNK: tldr -->
## TL;DR

Sometimes we have huge forms and all the information is not available when you start capturing the data of such forms. Avni gives you the facility to save the half-filled form as a draft.
<!-- END CHUNK -->

<!-- CHUNK: overview -->
## Overview

Sometimes we have huge forms and all the information is not available when you start capturing the data of such forms. Avni gives you the facility to save the half-filled form as a draft. These draft forms are not synced to the server, and once you fill the form completely draft is automatically deleted.
<!-- END CHUNK -->

<!-- CHUNK: enabling-draft-save -->
## Enabling Draft save

You can enable draft to save for your organization using the admin app. Simply go to "organisation Details" and enable "Draft save".

![](https://files.readme.io/d824dc2-draft_save.png "draft save.png")

Once the "draft save" feature is enabled you can see the half-filled forms in the registration tab in the field app. Please note that these drafts will get if the draft is left untouched for more than 30 days.

It gets converted into a regular Subject or Encounter on pressing Save button during modification of a draft.

![](https://files.readme.io/8386271-d.png "d.png")
<!-- END CHUNK -->

<!-- CHUNK: key-points -->
## Key points

* **Applicability:** Currently, this feature works only for the registration and encounter forms. So Program enrolment and program encounter forms won't get saved as a draft if left in middle.
* **Display:** Registration drafts are displayed on the Register screen. Encounter drafts are displayed under the on the 'General' tab on the Subject Dashboard. Unscheduled encounter drafts are displayed under the 'Drafts' section and scheduled encounter drafts are accessible by tapping 'Do' on encounters under the 'Visits Planned' section.
* **Save Checkpoint:** A draft save action is performed on clicking "Next" or "Previous" buttons while filling in a form, therefore, if User fills in a page but does not click on "Next" or "Previous" buttons, then the Draft saved would have content only till the previous page (On which "Next" button was clicked)
* **Exiting a form:** To exit from a form in-between, user may click on the "Header" "Back" button or click on "Footer" "Home" buttons\*\*
* **Stale Drafts clean-up:** Usually drafts get deleted once you perform a final save operation to convert it to an actual entity. Along with that we have a periodic drafts clean-up which gets executed once a day, to delete drafts that were last updated more than 30 days ago.
<!-- END CHUNK -->

<!-- CHUNK: related-topics -->
## Related Topics

<!-- Add links to related documentation -->
<!-- END CHUNK -->