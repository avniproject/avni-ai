---
title: Rule Extension Points in Avni
category: javascript-rules
audience: implementer
difficulty: advanced
priority: medium
keywords:
- extension points
- rule hooks
- custom logic
- rule types
last_updated: '2026-03-16'
task_types:
- reference
features:
- rules
technical_level:
- reference
implementation_phase:
- development
complexity: complex
retrieval_boost: 1.0
related_topics:
- rules-introduction.md
estimated_reading_time: 1 minutes
version: '1.0'
---
# Rule Extension Points in Avni

<!-- CHUNK: tldr -->
## TL;DR

Extensions are points in Avni where custom html can be used to enhance functionality. There are a few such predefined points where custom html can be inserted.
<!-- END CHUNK -->

<!-- CHUNK: overview -->
## Overview

Extensions are points in Avni where custom html can be used to enhance functionality. There are a few such predefined points where custom html can be inserted. 

In Data Entry App

* Subject Dashboard
* Subject Dashboard for a specific program
* Search Results page

In the Field-App

* Splash Screen
<!-- END CHUNK -->

<!-- CHUNK: creating-extensions -->
## Creating Extensions

### Creating the extension

In order to create an extension, first you need to create a web app. For each extension point, there will be parameters that you will receive that can be used for custom behaviour. Data can be fetched from the database using the Avni API.

Parameters

* Subject Dashboard - subjectUUIDs (subject's uuid), token (auth token)
* Search Results page - subjectUUIDs (Comma separated list of subjects that have been selected), token
* Splash screen - nothing

The token field must be added as a header AUTH-TOKEN in case you need to use the public API to interact with the Avni server.

### Adding the extension on the App Designer

Extensions can now be added to Avni through the app designer ([https://app.avniproject.org/#/appdesigner/extensions](https://app.avniproject.org/#/appdesigner/extensions)).\
All your extensions must be zipped and uploaded on this screen. You can enter the name of the extension, the file name in the zip file that must be rendered (use relative paths if your HTML file is within a directory), and the type of extension (called Extension Scope). 

![](https://files.readme.io/e772f7d-Screenshot_2021-10-27_at_10.58.02_AM.png "Screenshot 2021-10-27 at 10.58.02 AM.png")
<!-- END CHUNK -->

<!-- CHUNK: related-topics -->
## Related Topics

<!-- Add links to related documentation -->
<!-- END CHUNK -->