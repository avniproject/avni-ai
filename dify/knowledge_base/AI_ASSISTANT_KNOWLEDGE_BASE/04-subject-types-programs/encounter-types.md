---
title: Encounter Types in Avni
category: subject-types-programs
audience: implementer
difficulty: beginner
priority: critical
keywords:
- encounter types
- general encounters
- program encounters
- visits
last_updated: '2026-03-16'
task_types:
- configuration
- reference
features:
- encounters
technical_level:
- conceptual
- procedural
implementation_phase:
- development
complexity: simple
retrieval_boost: 2.0
related_topics:
- programs.md
- subject-types.md
estimated_reading_time: 1 minutes
version: '1.0'
---
# Encounter Types in Avni

<!-- CHUNK: tldr -->
## TL;DR

Encounter Types (also called Visit Types) are used to determine the kinds of encounters/visits that can be performed. An encounter can be scheduled for a specific encounter type using rules.
<!-- END CHUNK -->

<!-- CHUNK: overview -->
## Overview

Encounter Types (also called Visit Types) are used to determine the kinds of encounters/visits that can be performed. An encounter can be scheduled for a specific encounter type using rules. Here, we define that encounter type and the forms associated with the encounter type.

An encounter type is either associated directly with a Subject type or is associated with a Program type, which in-turn would be associated with a subject type. It need not always be associated with programs (you can perform an annual survey of a population using encounter types not associated with programs, and use this information to enrol subjects into a program).
<!-- END CHUNK -->

<!-- CHUNK: immutable-encounter-type -->
## Immutable encounter type

The encounter type can be made immutable by switching on the immutable flag on the encounter type create/edit screen. If the encounter type is marked as immutable then data from the last encounter is copied to the next encounter. Since the encounter is immutable, the edit is not allowed on these encounters.


Encounter Types (also called Visit Types) are used to determine the kinds of encounters/visits that can be performed. An encounter can be scheduled for a specific encounter type using rules. Here, we define that encounter type and the forms associated with the encounter type.

An encounter type is associated to a subject type. It need not be associated with programs (you can perform an annual survey of a population using encounter types not associated with programs, and use this information to enrol subjects into a program).

The encounter eligibility check rule is used to determine eligibility of an encounter type for a subject at any time.

- [Learn more about Avni's domain model](https://avni.readme.io/docs/avnis-domain-model-of-field-based-work)
- [Learn more about writing rules](https://avni.readme.io/docs/rules-concept-guide)
<!-- END CHUNK -->

<!-- CHUNK: related-topics -->
## Related Topics

<!-- Add links to related documentation -->
<!-- END CHUNK -->