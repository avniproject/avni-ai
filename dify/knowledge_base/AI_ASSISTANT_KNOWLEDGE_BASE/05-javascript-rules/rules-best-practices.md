---
title: Rules Development Best Practices
category: javascript-rules
audience: implementer
difficulty: intermediate
priority: high
keywords:
- best practices
- rules testing
- debugging
- rule development
- rule tips
last_updated: '2026-03-16'
task_types:
- best-practice
features:
- rules
technical_level:
- procedural
implementation_phase:
- development
- testing
complexity: moderate
retrieval_boost: 1.5
related_topics:
- rules-introduction.md
- common-patterns.md
estimated_reading_time: 1 minutes
version: '1.0'
---
# Rules Development Best Practices

<!-- CHUNK: tldr -->
## TL;DR

```sql
set role <organisation_db_user>;
<!-- END CHUNK -->

<!-- CHUNK: overview -->
## Overview

```sql
set role <organisation_db_user>;

-- Subject Type
update subject_type set
    program_eligibility_check_rule = replace(program_eligibility_check_rule, 'ruleServiceLibraryInterfaceForSharingModules', 'imports'),
    last_modified_date_time = current_timestamp
    where program_eligibility_check_rule like '%ruleServiceLibraryInterfaceForSharingModules%';
update subject_type set subject_summary_rule = replace(subject_summary_rule, 'ruleServiceLibraryInterfaceForSharingModules', 'imports'),
                        last_modified_date_time = current_timestamp
    where subject_summary_rule like '%ruleServiceLibraryInterfaceForSharingModules%';

-- Encounter Type
update encounter_type set encounter_eligibility_check_rule = replace(encounter_eligibility_check_rule, 'ruleServiceLibraryInterfaceForSharingModules', 'imports'),
                          last_modified_date_time = current_timestamp
    where encounter_eligibility_check_rule like '%ruleServiceLibraryInterfaceForSharingModules%';

-- Program
update program set enrolment_summary_rule = replace(enrolment_summary_rule, 'ruleServiceLibraryInterfaceForSharingModules', 'imports'),
                          last_modified_date_time = current_timestamp
    where enrolment_summary_rule like '%ruleServiceLibraryInterfaceForSharingModules%';
update program set enrolment_eligibility_check_rule = replace(enrolment_eligibility_check_rule, 'ruleServiceLibraryInterfaceForSharingModules', 'imports'),
                          last_modified_date_time = current_timestamp
    where enrolment_eligibility_check_rule like '%ruleServiceLibraryInterfaceForSharingModules%';
update program set manual_enrolment_eligibility_check_rule = replace(manual_enrolment_eligibility_check_rule, 'ruleServiceLibraryInterfaceForSharingModules', 'imports'),
                          last_modified_date_time = current_timestamp
    where manual_enrolment_eligibility_check_rule like '%ruleServiceLibraryInterfaceForSharingModules%';

-- Form
update form set decision_rule = replace(decision_rule, 'ruleServiceLibraryInterfaceForSharingModules', 'imports'),
                   last_modified_date_time = current_timestamp
where decision_rule like '%ruleServiceLibraryInterfaceForSharingModules%';
update form set validation_rule = replace(validation_rule, 'ruleServiceLibraryInterfaceForSharingModules', 'imports'),
                   last_modified_date_time = current_timestamp
where validation_rule like '%ruleServiceLibraryInterfaceForSharingModules%';
update form set visit_schedule_rule = replace(visit_schedule_rule, 'ruleServiceLibraryInterfaceForSharingModules', 'imports'),
                   last_modified_date_time = current_timestamp
where visit_schedule_rule like '%ruleServiceLibraryInterfaceForSharingModules%';
update form set checklists_rule = replace(checklists_rule, 'ruleServiceLibraryInterfaceForSharingModules', 'imports'),
                   last_modified_date_time = current_timestamp
where checklists_rule like '%ruleServiceLibraryInterfaceForSharingModules%';
update form set task_schedule_rule = replace(task_schedule_rule, 'ruleServiceLibraryInterfaceForSharingModules', 'imports'),
                   last_modified_date_time = current_timestamp
where task_schedule_rule like '%ruleServiceLibraryInterfaceForSharingModules%';

-- Form element

update form_element set "rule" = replace("rule", 'ruleServiceLibraryInterfaceForSharingModules', 'imports'),
<!-- END CHUNK -->

<!-- CHUNK: related-topics -->
## Related Topics

<!-- Add links to related documentation -->
<!-- END CHUNK -->