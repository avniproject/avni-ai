---
title: Writing Visit Schedule Rules
category: javascript-rules
audience: implementer
difficulty: intermediate
priority: high
keywords:
- visit schedule
- scheduling
- visit rules
- follow-up visits
- appointment scheduling
last_updated: '2026-03-16'
task_types:
- tutorial
- example
features:
- rules
- encounters
technical_level:
- procedural
implementation_phase:
- development
complexity: moderate
retrieval_boost: 1.5
related_topics:
- rules-introduction.md
- helper-functions.md
estimated_reading_time: 2 minutes
version: '1.0'
---
# Writing Visit Schedule Rules

<!-- CHUNK: tldr -->
## TL;DR

If we break down the visit schedule complexity into three levels simple to complex, we would notice that the testing mechanism for level 2 & 3 visit schedules are quite wasteful due to long feedback loops. The feedback loop is long mainly because the testing of visit schedule logic requires filli...
<!-- END CHUNK -->

<!-- CHUNK: overview -->
## Overview

If we break down the visit schedule complexity into three levels simple to complex, we would notice that the testing mechanism for level 2 & 3 visit schedules are quite wasteful due to long feedback loops. The feedback loop is long mainly because the testing of visit schedule logic requires filling forms to setup data and to see the result. In development mode performing sync the second main reason the feedback loop is long.

It is important to remember that for most (may be not all) bugs the testing of all the scenarios need to be carried our all over again. After certain number iterations of such testing the testing fatigue is likely to kick-in, compromising quality as well.

This feedback loop can be shortened significantly by following age old unit testing written in the form of business specifications. This approach improve quality and reduce waste.

Business specification style will allow for customer, business analyst, developer and testers all to come on the same page about the requirements. Automation of unit tests allows for verification of production code against the specification - repeatedly.
<!-- END CHUNK -->

<!-- CHUNK: business-specification-style-tests -->
## Business specification style tests

These are tests that are written such that they read close normal english using the language of problem domain, but they can be executed as well. It helps in understanding the basic structure of such tests which is capture in a three step process - **given, when, then**. It would be useful to quickly read about it, if you don't know about this already. One such article is [here](https://www.agilealliance.org/glossary/given-when-then/), but there are many.

### Example

This is one test for scheduling visits on edit of an ANC Visit - [https://github.com/avniproject/apf-odisha-2/blob/main/test/ANCTest.js#L117](https://github.com/avniproject/apf-odisha-2/blob/main/test/ANCTest.js#L117).

**Given** that the for beneficiary ANC-1 visit is completed and ANC-2 visit is scheduled for the next month

**When** ANC-1 is edited

**Then** PW Home or ANC visit should not be scheduled
<!-- END CHUNK -->

<!-- CHUNK: qa-strategy -->
## QA strategy

Visit schedules for which such unit tests have been written should be tested differently.

* Review the test scenarios already automated via these tests.  If any scenario is missing, request the developer to add those scenarios to the test suite.
* Pick a handful, not too many, of these to verify whether the mobile application is indeed working in the same way as well.
* **Most importantly - do not manually run all the scenarios.**
<!-- END CHUNK -->

<!-- CHUNK: for-developers -->
## For developers

* Jest - [https://jestjs.io/docs/api](https://jestjs.io/docs/api)
* It is important to learn about test lifecycle and setup, teardown, describe, test/it methods. [https://jestjs.io/docs/setup-teardown](https://jestjs.io/docs/setup-teardown)
* It is important the each test (test/it) runs independent of other tests, so that execution of one test doesn't have any impact on another test. To achieve this all variables should be instantiated in each test, i.e. in move all the code common instantiation code (not functions) to beforeEach. Do not instantiate anything outside beforeEach and it/test. Unit tests run super-fast so optimisation is not useful and is in fact counter-productive.
<!-- END CHUNK -->

<!-- CHUNK: related-topics -->
## Related Topics

<!-- Add links to related documentation -->
<!-- END CHUNK -->