---
title: Subject Types in Avni
category: subject-types-programs
audience: implementer
difficulty: beginner
priority: critical
keywords:
- subject types
- individual
- household
- group
- subject creation
last_updated: '2026-03-16'
task_types:
- configuration
- reference
features:
- subjects
technical_level:
- conceptual
- procedural
implementation_phase:
- setup
- development
complexity: simple
retrieval_boost: 2.0
related_topics:
- subject-type-settings.md
- programs.md
estimated_reading_time: 4 minutes
version: '1.0'
---
# Subject Types in Avni

<!-- CHUNK: tldr -->
## TL;DR

Subject Types define the subjects that you collect information on. Eg: Individual, Tractor, Water source, Classroom session.
<!-- END CHUNK -->

<!-- CHUNK: overview -->
## Overview

Subject Types define the subjects that you collect information on. Eg: Individual, Tractor, Water source, Classroom session. Service Providers in an organisation could be 

* taking action "Against" or "For" beneficiaries, citizens, patients, students, children, etc.
* collecting data for non-living objects like Water-body, School, Health Centre, etc.
<!-- END CHUNK -->

<!-- CHUNK: different-types-of-subject-in-avni -->
## Different types of Subject in Avni

Avni allows for creating multiple Subject Types, each of which can be of any one of the following kind: 

* **Group** - Used for representing an entity which constitutes a group of another subject type. Ex: A group of Interns enrolled for a specific Program for the Year 2023
* **Household** - Special kind of Group, which usually refers to a Household of beneficiaries living in a single postal address location. Ex: A household consisting of a family of Father, Mother and children. Additionally, has a feature to assign one of the members as Head of the Household.
* **Individual** - Generic type of Subject to represent a Place, Person, Thing, Action. etc.. Ex: School, Student, Pocelain Machine, Distribution of Materials, etc.
* **Person** - Special kind of Individual, to specifically indicate a Human Being. Additionally has in-built capability to save First and Last Names, Gender and Date of Birth.
* **User** - A type of Subject used to provide self-refer to the Service Providers in Avni. Read more about User Subject Types


Subject Types define the subjects (or things) that you collect information on. eg: Individual, Tractor, Water source, Classroom session.

**Person**

If you use this type, you get some bonus questions for free in the registration form - first and last names, gender and date of birth.

**Individual**

Use this type when you want to record data against non-human and single entity.

**Group**

Use the group type to define groups of a certain subject type. eg: A school might decide to define "Class" as a subject type against which information can be captured. It can also contain member subjects that are can have their own information.

**Household**

A household is a special kind of group. Groups roles are predefined when you choose household type, but you can choose any of the existing Person as member subject.

**User**

A user subject type is a type that can be used to manage information about users of the system. Each user will have one subject created based on this subject type. This subject and any data collected against it will or encounters and enrolments are only for single user.

[Learn more about Avni's domain model](https://avni.readme.io/docs/avnis-domain-model-of-field-based-work)


title: User Subject Types
excerpt: ''
A user subject type is a type that can be used to manage information about users of the system. Each user will have one subject created based on a User type SubjectType. This subject and any data collected against it's encounters and enrolments correspond only to that particular user.
<!-- END CHUNK -->

<!-- CHUNK: special-characteristics -->
## Special Characteristics

* **Subject Type Create / Edit**: Once a User type SubjectType is created, Avni doesnot allow Administrators to modify the basic configurations of the SubjectType. Ensure that you configure the Subject as needed at the outset. Contact Avni Support if you need any modifications to be done for the User type SubjectType.

  * Registration Date for the subject will be same as User Creation DateTime
  * Toggle of 'Allow empty location' is disabled and is always set to true
  * User's username is inserted as Subject's Firstname
* **Subject Type Create / Edit**: You may only edit the below shown properties post SubjectType creation.

![* **Sync**: By default, User type Subjects follow their own Sync strategy, which is currently, to sync a User type Subject only to its corresponding User
* **Subject Creation**: On creation of a "User" type SubjectType, we **automatically** create User type subjects :
  * for every new User created thereafter via the "Webapp" 
  * for new Users created via "CSV Uploads", by triggering a Background Job
  * for all existing Users, by triggering a Background Job
* **Ability to Disable Registration of User type SubjectTypes on Client**: Currently, Avni allows an Organisation Administrator to disable User's ability to create any new User Subject Type Subjects on client, by following the below steps:

  1. Navigate to "App Designer", Forms Section

     ![image](https://files.readme.io/af7a60f-Screenshot_2024-05-17_at_3.51.29_PM.png)
  2. Click on the "Gear Wheel" icon, to load the Form-Mapping Edit view

     ![image](https://files.readme.io/2c4cffc-Screenshot_2024-05-17_at_3.52.44_PM.png)
  3. Click on the "Bin (Delete)" icon to Void the Form to Subject type association (Form Mapping)
* **Access to User type Subject on the client**: Users cannot make use of "Subject Search" capability to access the User type Subject on the Client. They would always have to make use of "Filter" button on "My Dashboard" to select the User type Subject, as shown below.

![image](https://files.readme.io/f265252-Screenshot_2024-05-17_at_4.23.24_PM.png)
  Select User type in the Subject Filter](https://files.readme.io/ba11a11-Screenshot_2024-05-17_at_3.40.56_PM.png)

For organisations that use a Custom Dashboard as the Primary Dashboard, they can easily configure a Offline Report card to provide access to User type Subject.

* **Actions allowed on the User type Subject**: Avni allows organisation to configure a User type Subject similar to the way they would configure a "Person" / "Individual" type Subject types. i.e. they are free to setup Program, Encounter, VisitScheduleRules and so on. They can also configure Privileges in-order to restrict these actions across different UserGroups. A sample screen recording of the client, which has full access to a User type Subject is attached below for reference.

![image](https://files.readme.io/d966e6d-output.gif)
<!-- END CHUNK -->

<!-- CHUNK: related-topics -->
## Related Topics

<!-- Add links to related documentation -->
<!-- END CHUNK -->