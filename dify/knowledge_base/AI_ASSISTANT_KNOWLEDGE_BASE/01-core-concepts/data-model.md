---
title: "Avni Data Model - Forms, Observations, and Storage"
category: "core-concepts"
audience: "implementer"
difficulty: "intermediate"
priority: "medium"
keywords:
  - data model
  - forms
  - observations
  - JSONB
  - storage
  - database
last_updated: "2026-03-16"
task_types:
  - reference
features:
  - forms
  - concepts
technical_level:
  - conceptual
  - reference
implementation_phase:
  - planning
  - development
complexity: "moderate"
retrieval_boost: 1.0
related_topics:
  - ../03-concepts-and-forms/form-structure.md
  - ../03-concepts-and-forms/concept-types.md
estimated_reading_time: "7 minutes"
version: "1.0"
---

# Avni Data Model

<!-- CHUNK: tldr -->
## TL;DR

Avni stores form data as observations in JSONB format, providing flexibility to add fields without schema changes. Forms map to concepts, and observations store actual values. This design enables dynamic forms, fast queries, and easy reporting.

<!-- END CHUNK -->

<!-- CHUNK: form-mapping -->
## Form to Data Mapping

### Form Structure
```
Registration Form
├── Form Element Group: "Basic Info"
│   ├── Form Element: "Name" → Concept: "Name" (Text)
│   ├── Form Element: "Age" → Concept: "Age" (Numeric)
│   └── Form Element: "Gender" → Concept: "Gender" (Coded)
└── Form Element Group: "Contact"
    └── Form Element: "Mobile" → Concept: "Mobile Number" (Text)
```

### Data Storage
```json
{
  "observations": {
    "name-concept-uuid": "Priya Sharma",
    "age-concept-uuid": 25,
    "gender-concept-uuid": "female-answer-uuid",
    "mobile-concept-uuid": "9876543210"
  }
}
```

**Key points:**
- Form elements link to concepts
- Observations store actual values
- Stored as JSONB in PostgreSQL
- Concept UUIDs used as keys

<!-- END CHUNK -->

<!-- CHUNK: observation-storage -->
## Observation Storage

### JSONB Format
Avni uses PostgreSQL JSONB for flexible, performant storage.

**Benefits:**
- Add fields without schema changes
- Fast queries with GIN indexes
- Supports complex data types
- Easy to transform for reporting

**Example observation:**
```json
{
  "concept-uuid-1": "Text value",
  "concept-uuid-2": 123,
  "concept-uuid-3": ["array", "of", "values"],
  "concept-uuid-4": {
    "nested": "object"
  }
}
```

### Data Types Supported
- **Text:** Strings
- **Numeric:** Numbers (integer or decimal)
- **Coded:** References to answer concepts
- **Date/DateTime:** ISO format dates
- **Media:** File references (URLs)
- **Location:** Coordinates
- **Multi-select:** Arrays of answer UUIDs

<!-- END CHUNK -->

<!-- CHUNK: entity-tables -->
## Core Entity Tables

### Subject (Individual)
Stores registered subjects.

**Key fields:**
- UUID (unique identifier)
- Subject Type
- Registration Location
- Registration Date
- Observations (JSONB)
- Voided flag

### Program Enrolment
Tracks program enrollments.

**Key fields:**
- UUID
- Subject UUID (foreign key)
- Program UUID (foreign key)
- Enrolment Date
- Exit Date
- Observations (JSONB)
- Voided flag

### Encounter
Stores all encounters (general and program).

**Key fields:**
- UUID
- Subject UUID (foreign key)
- Encounter Type UUID
- Encounter Date/Time
- Program Enrolment UUID (if program encounter)
- Observations (JSONB)
- Voided flag

<!-- END CHUNK -->

<!-- CHUNK: querying-data -->
## Querying Observations

### In JavaScript Rules
```javascript
// Get observation value
const age = individual.getObservationValue('Age');

// Get coded answer
const gender = individual.getObservationValue('Gender');

// Check if observation exists
const hasPhone = individual.hasObservation('Mobile Number');

// Get from encounter
const bp = programEncounter.getObservationValue('Blood Pressure');
```

### In SQL (for reporting)
```sql
-- Query JSONB observations
SELECT 
  uuid,
  observations->>'concept-uuid' as age
FROM individual
WHERE (observations->>'concept-uuid')::int > 18;

-- Use GIN index for fast queries
CREATE INDEX idx_individual_obs 
ON individual USING GIN (observations);
```

<!-- END CHUNK -->

<!-- CHUNK: voiding -->
## Voiding (Soft Delete)

**What:** Marking data as deleted without actually removing it.

**Why:**
- Maintain audit trail
- Preserve data history
- Allow unvoiding if needed
- Comply with data regulations

**How it works:**
```
Record: {voided: false} → Visible
Record: {voided: true}  → Hidden
```

**What gets voided:**
- Subjects
- Enrollments
- Encounters
- Individual observations

**In queries:**
```sql
-- Exclude voided records
WHERE voided = false
```

<!-- END CHUNK -->

<!-- CHUNK: etl-transformation -->
## ETL Transformation

### Raw Data (Generic Schema)
```
individual table:
- uuid
- observations (JSONB with all concepts)
```

### Transformed Data (Implementation Schema)
```
pregnant_woman table:
- uuid
- name (extracted)
- age (extracted)
- lmp_date (extracted)
- edd (calculated)
```

**Benefits:**
- Easier reporting queries
- Better performance
- Familiar SQL structure
- Type-safe columns

**Process:**
1. ETL reads generic tables
2. Extracts observations by concept
3. Creates implementation-specific tables
4. Updates incrementally

<!-- END CHUNK -->

---

**Navigation:**  
[← Back: Domain Model](domain-model.md) | [Next: Offline Sync →](offline-sync-basics.md)
