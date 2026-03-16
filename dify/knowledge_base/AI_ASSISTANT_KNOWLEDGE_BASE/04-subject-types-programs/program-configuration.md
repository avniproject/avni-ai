---
title: Program Configuration Options
category: subject-types-programs
audience: implementer
difficulty: intermediate
priority: medium
keywords:
- program configuration
- multiple enrollments
- program settings
last_updated: '2026-03-16'
task_types:
- configuration
features:
- programs
technical_level:
- reference
implementation_phase:
- development
complexity: moderate
retrieval_boost: 1.0
related_topics:
- programs.md
estimated_reading_time: 1 minutes
version: '1.0'
---
# Program Configuration Options

<!-- CHUNK: tldr -->
## TL;DR

Each subject type can have multiple programs within them. If these programs are defined, the user can enroll subjects of these subject types into these programs.
<!-- END CHUNK -->

<!-- CHUNK: overview -->
## Overview

Each subject type can have multiple programs within them. If these programs are defined, the user can enroll subjects of these subject types into these programs.

Number of enrolments per subject

* Typically and hence by default, a subject can have only one active enrolment for a program. This implies that for a subject to be enrolled again the previous enrolment must be exited. e.g. Pregnancy program. Sometimes for chronic diseases, a person may remain in a program forever like diabetes. In such cases, the subject is never exited.
* Starting release 3.37, Avni also supports multiple active enrolments in a program. This can be done by switching on this per program. When this is switched on the above condition is relaxed by Avni.

![image](https://files.readme.io/62b1f10-image.png)
<!-- END CHUNK -->

<!-- CHUNK: related-topics -->
## Related Topics

<!-- Add links to related documentation -->
<!-- END CHUNK -->