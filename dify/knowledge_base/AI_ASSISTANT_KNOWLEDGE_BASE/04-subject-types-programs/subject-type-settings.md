---
title: Subject Type Settings and Configuration
category: subject-types-programs
audience: implementer
difficulty: intermediate
priority: medium
keywords:
- subject type settings
- registration
- profile
- active subjects
- subject configuration
last_updated: '2026-03-16'
task_types:
- configuration
- reference
features:
- subjects
technical_level:
- reference
implementation_phase:
- development
complexity: moderate
retrieval_boost: 1.0
related_topics:
- subject-types.md
estimated_reading_time: 2 minutes
version: '1.0'
---
# Subject Type Settings and Configuration

<!-- CHUNK: tldr -->
## TL;DR

If the view name exceeds 63 characters we trim some parts from different entity type names to keep it below 63 characters. For trimming, we follow the below rule.
<!-- END CHUNK -->

<!-- CHUNK: overview -->
## Overview

If the view name exceeds 63 characters we trim some parts from different entity type names to keep it below 63 characters. For trimming, we follow the below rule.

*\{UsernameSuffix}*\{First 6 characters of SubjectTypeName}*\{First 6 characters of ProgramName}_\{First 20 characters of EncounterTypeName}*

Some view names exceed the character limit even after the above optimisation. In such a case we take away the last few characters and replace them with the hashcode of the full name. Hashcode is used so that the name remains unique.


title: Introduction to excel based import [Deprecated]
excerpt: >-
next:
  description: ''
  pages:
    - type: basic
      slug: importing-excel-data
      title: Importing Excel data
---
> ❗️ Avni does not support Excel based import any longer, please refer to Admin App based approach to upload data [Bulk Data Upload page](https://avni.readme.io/docs/upload-data#is-the-order-of-values-important)


We can Import transactional data from excel files. Data can be Subject Registration, Enrolment, Encounters, relationships between Subjects, Vaccinations, etc. The data file, ideally, should have columns like RegistrationDate, FirstName, LastName, DOB, .. in case of Registration, and SubjectUUID, DateOfEnrolment, Program, .. in case of Enrolment, and SubjectUUID, EnrolmentUUID, EncounterType, Name, .. for Encounters. Along with these default fields, all the observations specific to the implementation should be present in the data file.

The definition of those forms cannot be imported this way. Only the data recorded against those forms can be imported this way.

We need a metaData.xlsx file that would work as an adapter between the data.xlsx file and the avni system.  
The data.xlsx file will be provided by the org-admin which should have consistent and tabular data. The metaData.xlsx file defines the relationship between each column and its corresponding field in the avni system/implementation.
<!-- END CHUNK -->

<!-- CHUNK: structure-of-metadata-xlsx-file -->
## Structure of metaData.xlsx file:

The following are the various spreadsheets within a metaData.xlsx file.

### Sheets

Sheets represent a logical sheet of data. A physical sheet of data can be mapped to multiple logical sheets of data.

<table>
<thead>
<tr>
  <th>Column</th>
  <th>Description</th>
</tr>
</thead>
<tbody>
<tr>
  <td>File Name</td>
  <td>The data migration service is used by supplying the metadata excel file, a data excel file, and a fileName (since the server reads the data excel file via a stream it doesn&#39;t know the name of the file originally uploaded hence it needs to be explicitly provided).  
Only the sheets which have the file name matching the fileName via the API would be imported.</td>
</tr>
<tr>
  <td>User File Type</td>
  <td>This is the unique name given to the file of specific types. There can be more than one physical file of the same type, in which case the user file type will be the same but file names will be different.</td>
</tr>
<tr>
  <td>Sheet Name</td>
  <td>This is the name of the actual sheet in the data file uploaded where the data should be read.</td>
</tr>
<tr>
  <td>Entity Type, Program Name and Visit Type, Address</td>
  <td>Core but optional data to be provided depending on the type of data being imported</td>
<!-- END CHUNK -->

<!-- CHUNK: related-topics -->
## Related Topics

<!-- Add links to related documentation -->
<!-- END CHUNK -->