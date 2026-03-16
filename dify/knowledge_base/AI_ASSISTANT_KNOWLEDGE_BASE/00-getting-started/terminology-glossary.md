---
title: "Avni Terminology Glossary"
category: "getting-started"
audience: "implementer"
difficulty: "beginner"
priority: "high"
keywords:
  - terminology
  - glossary
  - definitions
  - concepts
  - vocabulary
  - subject
  - program
  - encounter
  - form
  - catchment
last_updated: "2026-03-16"
task_types:
  - reference
technical_level:
  - conceptual
implementation_phase:
  - planning
  - setup
  - development
complexity: "simple"
retrieval_boost: 1.5
related_topics:
  - ../01-core-concepts/domain-model.md
  - ../01-core-concepts/avni-architecture.md
estimated_reading_time: "10 minutes"
version: "1.0"
---

# Avni Terminology Glossary

<!-- CHUNK: tldr -->
## TL;DR

Essential Avni terms every implementer needs to know. This glossary covers the core entities (Subject, Program, Encounter, Form) and organizational concepts (Location, Catchment, User) that form the foundation of Avni implementations.

<!-- END CHUNK -->

<!-- CHUNK: core-entities -->
## Core Entities

### Subject
**Definition:** The person or thing you are tracking in Avni.

**Examples:**
- Individual person (pregnant woman, child, patient)
- Household
- Water source
- School
- Classroom

**Key points:**
- Subjects are registered using a Registration Form
- Each subject belongs to a Subject Type
- Subjects can be enrolled in Programs
- Subjects have a location (address)

**Related:** [Subject Types](../04-subject-types-programs/subject-types.md)

---

### Subject Type
**Definition:** A category that defines what kind of subjects you track.

**Examples:**
- "Pregnant Woman" (Person type)
- "Child" (Person type)
- "Household" (Household type)
- "Water Source" (Thing type)

**Key points:**
- Determines the registration form structure
- Person types get automatic fields (name, gender, DOB)
- Each subject belongs to exactly one subject type
- Subject types can have multiple programs

**Related:** [Creating Subject Types](../04-subject-types-programs/subject-types.md)

---

### Program
**Definition:** A service or intervention that tracks subjects over time through a defined journey.

**Examples:**
- Pregnancy Program (ANC visits, delivery, PNC)
- Child Nutrition Program (growth monitoring, immunization)
- Treatment Program (diagnosis, treatment, follow-up)
- Education Program (enrollment, assessments, graduation)

**Key points:**
- Subjects are enrolled into programs
- Programs have enrollment forms, encounter types, and exit forms
- Programs can have visit schedules
- One subject can be enrolled in multiple programs

**Related:** [Program Design](../04-subject-types-programs/programs.md)

---

### Encounter
**Definition:** A single interaction or data collection event for a subject.

**Types:**

**1. General Encounter**
- Not linked to any program
- Example: One-time health screening, survey

**2. Program Encounter**
- Linked to a program enrollment
- Example: ANC Visit 1, Immunization visit, Monthly assessment

**Key points:**
- Each encounter has an Encounter Type
- Encounters use forms to collect data
- Encounters can be scheduled or unscheduled
- Encounters can be completed, cancelled, or pending

**Related:** [Encounter Types](../04-subject-types-programs/encounter-types.md)

---

### Form
**Definition:** A structured data collection template with questions (form elements).

**Structure:**
```
Form
├── Form Element Group 1
│   ├── Form Element (Question 1)
│   ├── Form Element (Question 2)
│   └── Form Element (Question 3)
├── Form Element Group 2
│   └── ...
```

**Types:**
- Registration Form (for subject registration)
- Enrollment Form (for program enrollment)
- Encounter Form (for encounters)
- Exit Form (for program exit)

**Key points:**
- Forms contain Form Element Groups (sections)
- Form Element Groups contain Form Elements (questions)
- Each Form Element links to a Concept
- Forms can have rules for validation, skip logic, calculations

**Related:** [Form Structure](../03-concepts-and-forms/form-structure.md)

---

### Concept
**Definition:** The underlying data element or question that can be reused across forms.

**Examples:**
- "Age" (Numeric concept)
- "Gender" (Coded concept with answers: Male, Female, Other)
- "Blood Pressure" (Numeric concept)
- "Pregnancy Status" (Coded concept: Yes, No)

**Types:**
- Numeric (numbers)
- Text (free text)
- Coded (predefined options)
- Date (dates)
- DateTime (date and time)
- Image, Video, Audio (media)
- Location (geographic coordinates)

**Key points:**
- Concepts are reusable across multiple forms
- Coded concepts have predefined answers
- Concepts can be organized into Concept Sets
- Good naming is critical for rules

**Related:** [Concept Types](../03-concepts-and-forms/concept-types.md)

---

### Observation
**Definition:** The actual data value captured for a concept during registration, enrollment, or encounter.

**Example:**
- Concept: "Age"
- Observation: 25 (the actual value entered)

**Key points:**
- Observations are stored in JSONB format
- Accessed in rules using helper functions
- Can be voided (soft deleted)
- Historical observations are preserved

**Related:** [Data Model](../01-core-concepts/data-model.md)

<!-- END CHUNK -->

<!-- CHUNK: organizational-concepts -->
## Organizational Concepts

### Organization
**Definition:** Your isolated workspace in Avni where all your data, users, and configuration exist.

**Key points:**
- Each organization is completely separate
- Users belong to one organization
- Data is not shared between organizations
- Configuration is organization-specific

**Related:** [Organization Creation](../02-organization-setup/organization-creation.md)

---

### Location / Address Level
**Definition:** Geographic hierarchy where your program operates.

**Common hierarchy:**
```
State
└── District
    └── Block
        └── Village
```

**Key points:**
- Defines geographic structure
- Subjects are registered at a location
- Users are assigned to locations via catchments
- Used for data filtering and reporting

**Related:** [Address Hierarchy](../02-organization-setup/address-hierarchy.md)

---

### Catchment
**Definition:** A group of locations that determines which data a user can see and sync.

**Example:**
- Catchment: "Pune District"
- Includes: All blocks and villages in Pune District
- Users assigned to this catchment see only subjects in these locations

**Key points:**
- Controls data access and sync
- Users can have multiple catchments
- Subjects must be in user's catchment to be visible
- Critical for offline sync

**Related:** [Catchment Configuration](../02-organization-setup/catchment-configuration.md)

---

### User
**Definition:** A person who uses Avni (field worker, supervisor, admin).

**Types:**
- Field User (mobile app, collects data)
- Web User (admin portal, configuration)
- Organization Admin (full access)

**Key points:**
- Users are assigned to catchments
- Users have privileges (permissions)
- Users can belong to user groups
- Users sync data to mobile app

**Related:** [User Management](../02-organization-setup/user-management.md)

---

### User Group
**Definition:** A collection of users with shared privileges and access patterns.

**Examples:**
- "Field Workers" (can register, enroll, do encounters)
- "Supervisors" (can view reports, approve data)
- "Admins" (can configure forms and programs)

**Key points:**
- Simplifies privilege management
- Users can belong to multiple groups
- Groups can have different data access
- Used for access control

**Related:** [User Groups and Privileges](../02-organization-setup/user-groups-privileges.md)

<!-- END CHUNK -->

<!-- CHUNK: workflow-concepts -->
## Workflow Concepts

### Visit Schedule
**Definition:** Automated scheduling of encounters based on program enrollment or previous encounters.

**Example:**
- Enroll in Pregnancy Program
- Visit Schedule Rule creates:
  - ANC 1 at 12 weeks
  - ANC 2 at 16 weeks
  - ANC 3 at 20 weeks
  - etc.

**Key points:**
- Defined using JavaScript rules
- Creates scheduled encounters
- Has earliest and max visit dates
- Can be cancelled or rescheduled

**Related:** [Visit Schedule Rules](../05-javascript-rules/visit-schedule-rules.md)

---

### Rules
**Definition:** JavaScript code that adds custom logic to forms and workflows.

**Types:**

**1. Validation Rules**
- Check if data is correct
- Show error messages
- Example: Age must be 15-49 for maternal health

**2. Decision Rules**
- Show/hide fields (skip logic)
- Calculate values
- Show messages
- Example: Show hemoglobin field only if anemic

**3. Visit Schedule Rules**
- Determine when visits should happen
- Example: Schedule PNC visits after delivery

**4. Task Schedule Rules**
- Create tasks for users
- Example: Create follow-up task if high-risk

**Key points:**
- Written in JavaScript
- Use helper functions to access data
- Can be complex or simple
- Critical for custom workflows

**Related:** [JavaScript Rules](../05-javascript-rules/README.md)

<!-- END CHUNK -->

<!-- CHUNK: data-concepts -->
## Data Concepts

### Sync
**Definition:** The process of uploading and downloading data between mobile app and server.

**What syncs:**
- Reference data (forms, concepts, locations)
- Transaction data (subjects, encounters, observations)
- Media files (images, videos)

**Key points:**
- Works offline (data stored locally)
- Automatic or manual sync
- Incremental (only changes sync)
- Catchment-based (only user's data)

**Related:** [Offline Sync Basics](../01-core-concepts/offline-sync-basics.md)

---

### Voiding
**Definition:** Soft delete - marking data as deleted without actually removing it.

**What can be voided:**
- Subjects
- Encounters
- Enrollments
- Observations

**Key points:**
- Voided data is hidden but not deleted
- Can be unvoided if needed
- Excluded from reports by default
- Maintains data history

**Related:** [Voiding Data](../06-data-management/voiding-data.md)

---

### Dashboard
**Definition:** Mobile app home screen showing pending work and summaries.

**Types:**
- My Dashboard (user's assigned work)
- Custom Dashboards (configured cards)

**Shows:**
- Scheduled visits (due, overdue)
- Registered subjects
- Completed encounters
- Custom report cards

**Key points:**
- Offline-capable
- Configurable filters
- Real-time updates
- User-specific

**Related:** [Offline Dashboards](../07-mobile-app-features/offline-dashboards.md)

<!-- END CHUNK -->

<!-- CHUNK: quick-reference -->
## Quick Reference

| Term | What It Is | Example |
|------|-----------|---------|
| **Subject** | Person/thing you track | Pregnant woman, Child |
| **Subject Type** | Category of subjects | "Pregnant Woman" type |
| **Program** | Service/intervention over time | Pregnancy Program |
| **Encounter** | Single data collection event | ANC Visit 1 |
| **Form** | Data collection template | ANC Visit Form |
| **Concept** | Reusable data element | "Age", "Blood Pressure" |
| **Observation** | Actual data value | Age = 25 |
| **Location** | Geographic place | Village, Block, District |
| **Catchment** | Group of locations | "Pune District Catchment" |
| **User** | Person using Avni | Field worker, Admin |
| **Visit Schedule** | Automated encounter scheduling | ANC visits at 12, 16, 20 weeks |
| **Rules** | Custom JavaScript logic | Validation, Skip logic |
| **Sync** | Upload/download data | Mobile ↔ Server |
| **Voiding** | Soft delete | Mark as deleted |

<!-- END CHUNK -->

<!-- CHUNK: relationships -->
## How Concepts Relate

```
Organization
├── Users (assigned to Catchments)
├── Locations (grouped into Catchments)
└── Subject Types
    ├── Registration Form
    ├── Subjects (registered at Locations)
    │   ├── Program Enrollments
    │   │   ├── Enrollment Form
    │   │   ├── Program Encounters (scheduled by Visit Schedule Rules)
    │   │   │   └── Encounter Forms
    │   │   └── Exit Form
    │   └── General Encounters
    │       └── Encounter Forms
    └── Programs
        └── Encounter Types
```

**Key relationships:**
- Subjects belong to Subject Types
- Subjects are registered at Locations
- Subjects can enroll in Programs
- Programs have Encounter Types
- Encounters use Forms
- Forms contain Concepts
- Concepts capture Observations
- Users access data via Catchments

<!-- END CHUNK -->

---

**Navigation:**  
[← Back to Getting Started](README.md) | [Next: Core Concepts →](../01-core-concepts/README.md)
