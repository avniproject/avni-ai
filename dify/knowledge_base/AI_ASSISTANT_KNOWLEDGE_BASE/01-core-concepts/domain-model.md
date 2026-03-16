---
title: "Avni Domain Model - Subject, Program, Encounter Relationships"
category: "core-concepts"
audience: "implementer"
difficulty: "beginner"
priority: "high"
keywords:
  - domain model
  - subject
  - program
  - encounter
  - relationships
  - data structure
last_updated: "2026-03-16"
task_types:
  - reference
features:
  - subjects
  - programs
  - encounters
technical_level:
  - conceptual
implementation_phase:
  - planning
  - setup
complexity: "simple"
retrieval_boost: 1.5
related_topics:
  - ../00-getting-started/terminology-glossary.md
  - ../04-subject-types-programs/subject-types.md
  - ../04-subject-types-programs/programs.md
estimated_reading_time: "10 minutes"
version: "1.0"
---

# Avni Domain Model

<!-- CHUNK: tldr -->
## TL;DR

Avni's domain model centers on **Subjects** (people/things you track), **Programs** (services over time), and **Encounters** (data collection events). Subjects are registered, enrolled in programs, and have encounters to record observations. This structure supports longitudinal data collection for health, education, and social programs.

<!-- END CHUNK -->

<!-- CHUNK: overview -->
## Overview

**What:** Understanding how Avni's core entities relate to each other.

**When to use:** Designing your implementation, planning data structure, understanding workflows.

**Core entities:**
- Subject - Who/what you're tracking
- Program - Service/intervention over time
- Encounter - Data collection event
- Form - Data collection template
- Observation - Actual data captured

<!-- END CHUNK -->

<!-- CHUNK: entity-hierarchy -->
## Entity Hierarchy

```
Organization
├── Subject Types
│   ├── Registration Form
│   └── Subjects (instances)
│       ├── Registration Data
│       ├── Program Enrollments
│       │   ├── Enrollment Form Data
│       │   ├── Program Encounters
│       │   │   └── Encounter Form Data
│       │   └── Exit Form Data
│       └── General Encounters
│           └── Encounter Form Data
└── Programs
    ├── Enrollment Form
    ├── Encounter Types
    │   └── Encounter Forms
    └── Exit Form
```

**Key relationships:**
- One Subject Type → Many Subjects
- One Subject → Many Program Enrollments
- One Program Enrollment → Many Program Encounters
- One Subject → Many General Encounters

<!-- END CHUNK -->

<!-- CHUNK: subject-lifecycle -->
## Subject Lifecycle

### 1. Registration
**Action:** Create a new subject in the system

**Process:**
1. Select Subject Type (e.g., "Pregnant Woman")
2. Fill Registration Form (name, age, location, etc.)
3. Subject is created with unique ID
4. Subject appears in user's dashboard

**Example:**
```
Subject Type: Pregnant Woman
Registration Form Fields:
- Name: Priya Sharma
- Age: 25
- Location: Village Wadgaon
- Mobile: 9876543210
- LMP Date: 2024-01-15
```

---

### 2. Program Enrollment
**Action:** Enroll subject in a program

**Process:**
1. Select subject
2. Choose program (e.g., "Pregnancy Program")
3. Fill Enrollment Form (baseline data)
4. Enrollment is created
5. Visit schedule may be generated

**Example:**
```
Program: Pregnancy Program
Enrollment Form Fields:
- Gravida: 2
- Para: 1
- Previous complications: None
- Expected Delivery Date: 2024-10-22
```

---

### 3. Program Encounters
**Action:** Record routine visits/checkups

**Process:**
1. Scheduled or unscheduled encounter
2. Select encounter type (e.g., "ANC Visit 1")
3. Fill encounter form
4. Data is saved
5. Next visit may be scheduled

**Example:**
```
Encounter Type: ANC Visit 1
Encounter Form Fields:
- Weight: 58 kg
- Blood Pressure: 120/80
- Hemoglobin: 11.5 g/dL
- Any complaints: None
```

---

### 4. Program Exit
**Action:** Exit from program

**Process:**
1. Select enrollment
2. Fill Exit Form (outcome, reason)
3. Enrollment is closed
4. No more scheduled visits

**Example:**
```
Exit Form Fields:
- Exit Date: 2024-10-25
- Outcome: Live birth
- Complications: None
```

<!-- END CHUNK -->

<!-- CHUNK: general-encounters -->
## General Encounters

**What:** Encounters not linked to any program.

**Use cases:**
- One-time surveys
- Screening camps
- Ad-hoc data collection
- Cross-cutting services

**Example:**
```
Subject: Priya Sharma
Encounter Type: Health Screening
Form Fields:
- Blood Sugar: 95 mg/dL
- Blood Pressure: 118/78
- BMI: 22.5
```

**Difference from Program Encounters:**
- Not part of a program journey
- No enrollment required
- No visit scheduling
- Standalone data collection

<!-- END CHUNK -->

<!-- CHUNK: forms-and-observations -->
## Forms and Observations

### Form Structure
```
Form
├── Form Element Group 1 (Section)
│   ├── Form Element (Question) → Concept
│   ├── Form Element (Question) → Concept
│   └── Form Element (Question) → Concept
├── Form Element Group 2 (Section)
│   └── ...
```

### Observation Storage
**Concept:** "Blood Pressure" (definition)  
**Observation:** 120/80 (actual value captured)

**Storage format:** JSONB in PostgreSQL
```json
{
  "concept-uuid-1": "120/80",
  "concept-uuid-2": 58,
  "concept-uuid-3": "2024-03-16"
}
```

**Benefits:**
- Flexible schema
- Fast queries
- Easy to add new concepts
- Supports complex data types

<!-- END CHUNK -->

<!-- CHUNK: real-world-example -->
## Real-World Example: Maternal Health

### Setup
**Subject Type:** Pregnant Woman  
**Program:** Pregnancy Program  
**Encounter Types:** ANC Visit 1-4, Delivery, PNC Visit 1-3

### Workflow

**Step 1: Registration**
- Field worker registers Priya in village Wadgaon
- Captures basic details (name, age, contact)
- Subject created in system

**Step 2: Enrollment**
- Priya enrolled in Pregnancy Program
- Baseline data captured (gravida, para, LMP)
- Visit schedule generated:
  - ANC 1 at 12 weeks
  - ANC 2 at 16 weeks
  - ANC 3 at 20 weeks
  - ANC 4 at 28 weeks

**Step 3: Program Encounters**
- ANC 1 completed: Weight, BP, Hb checked
- ANC 2 completed: Ultrasound done
- ANC 3 completed: Tetanus vaccine given
- ANC 4 completed: High-risk identified

**Step 4: Delivery**
- Delivery encounter recorded
- Outcome: Live birth, male child
- Mother and baby healthy

**Step 5: PNC Visits**
- PNC 1 at 3 days: Mother and baby checked
- PNC 2 at 7 days: Breastfeeding assessed
- PNC 3 at 42 days: Final checkup

**Step 6: Exit**
- Program exit recorded
- Outcome: Successful completion
- Both mother and baby healthy

<!-- END CHUNK -->

<!-- CHUNK: design-principles -->
## Design Principles

### 1. Flexibility
- Subject types can represent anything (people, things, places)
- Programs are optional (can use just encounters)
- Forms are fully customizable

### 2. Longitudinal Tracking
- Programs track subjects over time
- Historical data preserved
- Relationships maintained

### 3. Offline-First
- All entities work offline
- Sync when connectivity available
- No data loss

### 4. Reusability
- Concepts reused across forms
- Programs reused across subject types
- Encounter types reused in programs

### 5. Scalability
- Multi-tenant architecture
- Efficient data storage
- Optimized for large datasets

<!-- END CHUNK -->

<!-- CHUNK: common-patterns -->
## Common Implementation Patterns

### Pattern 1: Simple Registration Only
**Use case:** One-time surveys, censuses

**Structure:**
- Subject Type: Household
- Registration Form: Demographics, assets
- No programs, no encounters

---

### Pattern 2: Registration + General Encounters
**Use case:** Screening camps, periodic surveys

**Structure:**
- Subject Type: Individual
- Registration Form: Basic details
- General Encounters: Health screening, follow-up

---

### Pattern 3: Full Program Workflow
**Use case:** Health programs, education tracking

**Structure:**
- Subject Type: Student
- Registration Form: Student details
- Program: Academic Year
- Encounters: Assessments, attendance
- Exit: Graduation/dropout

---

### Pattern 4: Multiple Programs
**Use case:** Comprehensive health services

**Structure:**
- Subject Type: Individual
- Programs: Pregnancy, Child Nutrition, Immunization
- Each program has its own encounters
- Subject can be in multiple programs simultaneously

<!-- END CHUNK -->

---

**Navigation:**  
[← Back: Architecture](avni-architecture.md) | [Next: Data Model →](data-model.md)
