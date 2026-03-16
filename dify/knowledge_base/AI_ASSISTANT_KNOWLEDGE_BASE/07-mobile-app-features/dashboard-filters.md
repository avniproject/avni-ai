---
title: My Dashboard and Search Filters
category: mobile-app-features
audience: implementer
difficulty: intermediate
priority: high
keywords:
- dashboard filters
- search filters
- my dashboard
- filter configuration
last_updated: '2026-03-16'
task_types:
- configuration
- tutorial
features:
- dashboards
technical_level:
- procedural
implementation_phase:
- development
complexity: moderate
retrieval_boost: 1.5
related_topics:
- offline-dashboards.md
- custom-search-fields.md
estimated_reading_time: 3 minutes
version: '1.0'
---
# My Dashboard and Search Filters

<!-- CHUNK: tldr -->
## TL;DR

Avni allows the display of custom filter in **Search** and **My Dashboard filter** page. These settings are available within App designer.
<!-- END CHUNK -->

<!-- CHUNK: overview -->
## Overview

Avni allows the display of custom filter in **Search** and **My Dashboard filter** page. These settings are available within App designer. Filter settings are stored in organisation_config table.  You can define filters for different subject types. Please refer to the table below for various options.
<!-- END CHUNK -->

<!-- CHUNK: filter-types -->
## Filter Types

<thead>
    <tr>
      <th style={{ textAlign: "left" }}>
        Type
      </th>

      <th style={{ textAlign: "left" }}>
        Applies on Field
      </th>

      <th style={{ textAlign: "left" }}>
        Widget Types
      </th>
    </tr>
  </thead>

  <tbody>
    <tr>
      <td style={{ textAlign: "left" }}>
        Name
      </td>

      <td style={{ textAlign: "left" }}>
        Name of the subject
      </td>

      <td style={{ textAlign: "left" }}>
        Default (Text)
      </td>
    </tr>

    <tr>
      <td style={{ textAlign: "left" }}>
        Age
      </td>

      <td style={{ textAlign: "left" }}>
        Age of the subject
      </td>

      <td style={{ textAlign: "left" }}>
        Default : Numeric field. Fetches result matching records with values +/- 4.
      </td>
    </tr>

    <tr>
      <td style={{ textAlign: "left" }}>
        Gender
      </td>

      <td style={{ textAlign: "left" }}>
        Gender of the subject
      </td>

      <td style={{ textAlign: "left" }}>
        Default : Multiselect with configured gender options.
      </td>
    </tr>

    <tr>
      <td style={{ textAlign: "left" }}>
        Address
      </td>

      <td style={{ textAlign: "left" }}>
        Address of the subject
      </td>

      <td style={{ textAlign: "left" }}>
        Default : Multiselect option to choose the address of the subject. Nested options appear if multiple levels of address are present. e.g. District -> Taluka -> Village.
      </td>
    </tr>

    <tr>
      <td style={{ textAlign: "left" }}>
        Registration Date
      </td>

      <td style={{ textAlign: "left" }}>
        Date of Registration of the subject
      </td>

      <td style={{ textAlign: "left" }}>
        Default : Fixed date\
        Range : Options to choose Start date and End date
      </td>
    </tr>

    <tr>
      <td style={{ textAlign: "left" }}>
        Enrolment Date
      </td>

      <td style={{ textAlign: "left" }}>
        Date of Enrolment in any program
      </td>

      <td style={{ textAlign: "left" }}>
        Default : Fixed date\
        Range : Options to choose Start date and End date
      </td>
    </tr>

    <tr>
      <td style={{ textAlign: "left" }}>
        Encounter Date
      </td>

      <td style={{ textAlign: "left" }}>
        Date of Encounter in any Encounter
      </td>

      <td style={{ textAlign: "left" }}>
        Default : Fixed date\
        Range : Options to choose Start date and End date
      </td>
    </tr>

    <tr>
      <td style={{ textAlign: "left" }}>
        Program Encounter Date
      </td>

      <td style={{ textAlign: "left" }}>
        Date of Program Encounter in any Program Encounter
      </td>

      <td style={{ textAlign: "left" }}>
        Default : Fixed date\
        Range : Options to choose Start date and End date
      </td>
    </tr>

    <tr>
      <td style={{ textAlign: "left" }}>
        Search All
      </td>

      <td style={{ textAlign: "left" }}>
        Text fields in all the core fields and observations in Registration and Program enrolment
      </td>

      <td style={{ textAlign: "left" }}>
        Default : Text Field
      </td>
    </tr>
  </tbody>


#### Limitation: Right now we cannot have multiple scopes for a filter, i.e. we cannot search a concept in program encounter and encounter with the same filter.
<!-- END CHUNK -->

<!-- CHUNK: users-need-to-sync-the-app-for-getting-any-of-the- -->
## Users need to sync the app for getting any of the above changes.

MyDashboard in Avni comes with some default filters. Additional filters can be added here.

[Look up more details](https://avni.readme.io/docs/my-dashboard-and-search-filters)


title: Move Org to Custom Dashboard from MyDashboard
excerpt: ''
1. As super admin, call `POST /api/defaultDashboard/create?orgId=[organisationId]` (`organisationId` being the id of the organisation for which you want to create the default dashboard - typically your UAT org)
2. This API will only create the default dashboard for non Prod orgs.
3. Assign the newly created dashboard to the required user groups.
4. Test and verify functionality in UAT org
5. Upload bundle from UAT org to live org.
<!-- END CHUNK -->

<!-- CHUNK: related-topics -->
## Related Topics

<!-- Add links to related documentation -->
<!-- END CHUNK -->