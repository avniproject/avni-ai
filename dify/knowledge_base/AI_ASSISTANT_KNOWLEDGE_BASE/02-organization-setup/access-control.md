---
title: Access Control in Avni
category: organization-setup
audience: implementer
difficulty: advanced
priority: medium
keywords:
- access control
- permissions
- subject type access
- program access
- encounter type access
last_updated: '2026-03-16'
task_types:
- configuration
- reference
features:
- users
technical_level:
- procedural
- reference
implementation_phase:
- setup
- development
complexity: complex
retrieval_boost: 1.0
related_topics:
- user-groups-privileges.md
- user-management.md
estimated_reading_time: 5 minutes
version: '1.0'
---
# Access Control in Avni

<!-- CHUNK: tldr -->
## TL;DR

Before the introduction of Access Control, organisation users with access to the field app could access all functions (i.e. registration, enrolments, search etc.) in the app.
<!-- END CHUNK -->

<!-- CHUNK: overview -->
## Overview

Before the introduction of Access Control, organisation users with access to the field app could access all functions (i.e. registration, enrolments, search etc.) in the app. There was a need for some implementations to limit access to specific functions in order to reduce the number of options visible to end users and simplify the workflow for them while also providing a mechanism for access control.

Access Control is implemented via User Groups to facilitate this need. This functionality is available to Organisation admins in the Admin section of the Web app under the User Groups menu.
<!-- END CHUNK -->

<!-- CHUNK: applicability -->
## Applicability

* The access control rules are applicable in the field app, data entry app, and the web app.
* Access control is not applicable to the reporting app.
<!-- END CHUNK -->

<!-- CHUNK: user-groups -->
## User Groups

User Groups represent a collection of users and a set of privileges allowed to these users. User with EditUserGroup and EditUserConfiguration privilege can define as many groups as they need to define the access control required for their organisation. Each group can be assigned a set of privileges (or all privileges using the switch available at the top).

Each user can be added to multiple groups.
<!-- END CHUNK -->

<!-- CHUNK: privileges-are-additive -->
## Privileges are Additive

If any of the groups that a user belongs to allows a particular privilege, the user will have access to that function.
<!-- END CHUNK -->

<!-- CHUNK: default-groups -->
## Default Groups

By default, the system creates an `Everyone` and an `Administrators` group. `Everyone` group includes all the users in the organisation. `Administrators` group grants all the privileges to allow access to all the functionality.

![image](https://files.readme.io/9c003c1-Screenshot_2023-08-08_at_3.46.23_PM.png)

Users cannot be removed from `Everyone` group but the privileges associated with this group can be modified. The has all privileges flag cannot be reset for `Administrators` group.
<!-- END CHUNK -->

<!-- CHUNK: privileges -->
## Privileges

The following privileges are available in order to allow organisation admins to configure fine-grained access to functions for the org users. These privileges are configurable per entity type i.e. a group could have the 'View subject' privilege allowed for subject type 'abc' but disallowed for subject type 'xyz'.

* The Subject level privileges are configurable for each Subject Type setup in your organisation.
* The Enrolment level privileges are configurable for each program setup in your organisation.
* The Encounter level privileges are configurable for each Encounter Type (General or Program) setup in your organisation.
* The Checklist level privileges are configurable for each Program containing checklists for your organisation. 


  <thead>
    <tr>
      <th>
        Entity Type
      </th>

      <th>
        Privilege
      </th>

      <th>
        Explanation
      </th>
    </tr>
  </thead>

  <tbody>
    <tr>
      <td>
        Subject
      </td>

      <td>
        View subject
      </td>

      <td>
        Controls whether field users can see subjects of a particular subject type in the app.  

        All other privileges are dependent on this privilege. If disallowed, field users cannot see or access any functionality for the specific subject type.
      </td>
    </tr>

    <tr>
      <td>
        Subject
      </td>

      <td>
        Register subject
      </td>

      <td>
        Allows field users to register new subjects.
      </td>
    </tr>

    <tr>
      <td>
        Subject
      </td>

      <td>
        Edit subject
      </td>

      <td>
        Allows field users to edit previously registered subjects.
      </td>
    </tr>

    <tr>
      <td>
        Subject
      </td>

      <td>
        Void subject
      </td>

      <td>
        Allows field users to void previously registered subjects.
      </td>
    </tr>

    <tr>
      <td>
        Subject
      </td>

      <td>
        Add member\*
      </td>

      <td>
        Allows field users to add a member to household subject.
      </td>
    </tr>

    <tr>
      <td>
        Subject
      </td>

      <td>
        Edit member\*
      </td>

      <td>
        Allows field users to edit previously added household members.
      </td>
    </tr>

    <tr>
      <td>
        Subject
      </td>

      <td>
        Remove member\*
      </td>

      <td>
        Allows field users to remove previously added household members.
      </td>
    </tr>

    <tr>
      <td>
        Enrolment
      </td>

      <td>
        Enrol subject
      </td>

      <td>
        Allows field users to enrol a subject into a program.
      </td>
    </tr>

    <tr>
      <td>
        Enrolment
      </td>

      <td>
        View enrolment details
      </td>

      <td>
        Allows field users to view the program enrolment details for a subject.
      </td>
    </tr>

    <tr>
      <td>
        Enrolment
      </td>

      <td>
        Edit enrolment details
      </td>

      <td>
        Allows field users to edit the program enrolment details for a subject.
      </td>
    </tr>

    <tr>
      <td>
        Enrolment
      </td>

      <td>
        Exit enrolment
      </td>

      <td>
        Allows field users to exit a subject from a program.
      </td>
    </tr>

    <tr>
      <td>
        Encounter
      </td>

      <td>
        View visit
      </td>

      <td>
        Allows field users to view encounters for a subject.
      </td>
    </tr>

    <tr>
      <td>
        Encounter
      </td>

      <td>
        Schedule visit
      </td>

      <td>
        Allows field users to schedule encounters for a subject.
      </td>
    </tr>

    <tr>
      <td>
        Encounter
      </td>

      <td>
        Perform visit
      </td>

      <td>
        Allows field users to perform encounters for a subject.
      </td>
    </tr>

    <tr>
      <td>
        Encounter
      </td>

      <td>
        Edit visit
      </td>

      <td>
        Allows field users to edit previously saved encounter details.
      </td>
    </tr>

    <tr>
      <td>
        Encounter
      </td>

      <td>
        Cancel visit
      </td>

      <td>
        Allows field users to cancel a previously scheduled encounter.
      </td>
    </tr>

    <tr>
      <td>
        Encounter
      </td>

      <td>
        Void visit\*\*
      </td>

      <td>
        Allows field users to void an encounter
      </td>
    </tr>

    <tr>
      <td>
        Checklist
      </td>

      <td>
        View checklist
      </td>

      <td>
        Allows field users to view checklist.
      </td>
    </tr>

    <tr>
      <td>
        Checklist
      </td>

      <td>
        Edit checklist
      </td>

      <td>
        Allows field users to edit checklist.
      </td>
    </tr>
  </tbody>


`*` Only for 'Household' subject types

`**` Only available as part of Avni 4.0 release (not a full list)

Some of these privileges imply others. For example, allowing the 'Register Subject' privilege implies that the group will also have 'View Subject' allowed. The system handles these dependencies automatically.
<!-- END CHUNK -->

<!-- CHUNK: what-if-i-have-a-simple-setup-with-no-separate-use -->
## What if I have a simple setup with no separate users?

You can add all your users to the `Administrators` group.
<!-- END CHUNK -->

<!-- CHUNK: is-some-data-with-no-access-control -->
## Is some data with no access control?

Yes some of the app designer and admin user interface (or non-operational data) is open to all users with read access. This data is not confidential in any of the implementations of Avni, hence this has been kept open for any user with login to the organisation.
<!-- END CHUNK -->

<!-- CHUNK: can-users-update-metadata-using-the-api -->
## Can users update metadata using the API

No, the server also check for the access privileges of the user.
<!-- END CHUNK -->

<!-- CHUNK: super-admin-access -->
## Super admin access

Access of super admin is restricted to non-operational data of the organisations. Operational data cannot be viewed as well by super admin. This is to provide visibility to the organisations about who can view their data.
<!-- END CHUNK -->

<!-- CHUNK: related-topics -->
## Related Topics

<!-- Add links to related documentation -->
<!-- END CHUNK -->