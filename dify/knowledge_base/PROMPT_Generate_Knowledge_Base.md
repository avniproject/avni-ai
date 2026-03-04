# Prompt: Generate Comprehensive Knowledge Base for Avni Implementation

## Objective
Create a comprehensive knowledge base markdown file for use in Dify from an organization's Avni implementation bundle. The knowledge base should document all implementation details, data models, workflows, and JavaScript rules to enable AI-assisted rule generation and implementation support.

## Input Requirements
- **Organization Name**: [Organization Name]
- **Implementation Folder Path**: [Path to implementation context folder, e.g., `reference/[org]_context`]
- **Focus Areas**: [e.g., Maternal health, Child nutrition, Disease surveillance, etc.]

## Output File
- **Filename**: `[org]_context.md`
- **Location**: Same as input folder
- **Format**: Single comprehensive markdown file combining implementation overview and rules documentation

---

## Detailed Instructions

### PART 1: Implementation Overview and Data Model

#### Section 1: Overview
Create an overview section that includes:
- Organization name and implementation focus
- Platform (Avni/OpenCHS)
- Key program areas (e.g., maternal health, child nutrition, disease tracking)
- Brief description of the implementation's purpose and scope

**Template**:
```markdown
# [Organization Name] Implementation - Knowledge Base

## Overview

This knowledge base documents the complete [Organization Name] implementation in Avni. This implementation focuses on [key focus areas], including [list main components].

## Table of Contents

1. [Subject Types](#subject-types)
2. [Programs](#programs)
3. [Encounter Types](#encounter-types)
4. [Address Level Types](#address-level-types)
5. [Form Mappings](#form-mappings)
6. [Forms Structure](#forms-structure)
7. [Key Concepts](#key-concepts)
8. [Workflows](#workflows)
9. [Rule Types and Structure](#rule-types-and-structure)
10. [Common Rule Patterns](#common-rule-patterns)
11. [Helper Functions and Libraries](#helper-functions-and-libraries)
12. [Best Practices](#best-practices)
```

#### Section 2: Subject Types
Read `subjectTypes.json` and document:
- Each subject type's UUID, name, and type (Person, Individual, Group, User)
- Active status
- Purpose and use case
- Key features (sync settings, location-based syncing, subject summary rules)
- Voided/historical types (mark clearly)

**Format**:
```markdown
## Subject Types

The implementation uses [N] subject types to model different entities:

### 1. [Subject Type Name] ([Type])
- **UUID**: `[uuid]`
- **Type**: [Person/Individual/Group/User]
- **Purpose**: [Description of what this subject type represents]
- **Key Features**:
  - [Feature 1]
  - [Feature 2]
  - [Sync/location settings]
```

#### Section 3: Programs
Read `programs.json` and document:
- Program UUID, name, and color
- Eligibility criteria (from enrolment eligibility rules)
- Enrolment summary fields
- Key encounters associated with the program
- Allow multiple enrolments setting
- Growth chart enablement (for child programs)

**Format**:
```markdown
## Programs

The implementation has [N] active programs:

### 1. [Program Name]
- **UUID**: `[uuid]`
- **Color**: [Color name] (`[hex code]`)
- **Eligibility**: [Eligibility criteria from rules]
- **Enrolment Summary**:
  - [Summary field 1]
  - [Summary field 2]
- **Key Encounters**:
  - [Encounter 1]
  - [Encounter 2]
```

#### Section 4: Encounter Types
Read `encounterTypes.json` and document:
- Encounter type UUID and name
- Active/voided status
- Eligibility rules (from entityEligibilityCheckRule)
- Purpose and use case
- Associated program (if applicable)

**Format**:
```markdown
## Encounter Types

### [Program Name] Program Encounters

#### [Encounter Type Name]
- **UUID**: `[uuid]`
- **Eligibility**: [Eligibility logic from rule]
- **Purpose**: [Description]
```

#### Section 5: Address Level Types
Read `addressLevelTypes.json` and document:
- Hierarchical structure (levels)
- Each level's UUID, name, and parent relationship
- Note any parallel hierarchies

**Format**:
```markdown
## Address Level Types

The implementation uses a [N]-level location hierarchy:

### Level [N]: [Level Name]
- **UUID**: `[uuid]`
- **Level**: [N.0]
- **Parent**: [Parent level name or "None (top level)"]
```

#### Section 6: Form Mappings
Read `formMappings.json` and document:
- Total count of active mappings (exclude voided)
- Group by category:
  - Registration Forms (IndividualProfile)
  - Program Enrolment Forms (ProgramEnrolment)
  - Program Exit Forms (ProgramExit)
  - Program Encounter Forms (ProgramEncounter)
  - Program Encounter Cancellation Forms (ProgramEncounterCancellation)
  - General Encounter Forms (Encounter)
  - General Encounter Cancellation Forms (IndividualEncounterCancellation)

**Format**:
```markdown
## Form Mappings

The implementation has [N] active form mappings (excluding voided ones):

### Registration Forms

1. **[Form Name]**
   - Form UUID: `[uuid]`
   - Subject Type: [subject type]
   - Form Type: IndividualProfile
```

#### Section 7: Forms Structure
List all form JSON files in the `/forms/` directory:
- Count total forms
- Group by category (Registration, Program Enrolment, Encounters, etc.)
- Note voided forms separately

#### Section 8: Key Concepts
Read `concepts.json` and summarize key concept categories:
- Anthropometric measurements
- Health tracking concepts
- Administrative concepts
- Program-specific concepts

**Do not list all concepts** - provide high-level categories with examples.

#### Section 9: Workflows
Document typical workflows for each program:
- Step-by-step process from registration to exit
- Key decision points
- Scheduling logic
- High-risk identification and intervention flows

**Format**:
```markdown
## Workflows

### [Program Name] Workflow

1. **Registration**: [Description]
2. **Enrolment**: [Description] → Triggers [scheduling]
3. **[Encounter Type]**: [Description]
...
```

---

### PART 2: Rules Documentation

#### Section 10: Rule Types and Structure
Document all 4 rule types with complete structure templates:

1. **Form Element Rules** - Control visibility, set values, skip answers, validate fields
2. **Validation Rules** - Form-level validation across multiple fields
3. **Visit Schedule Rules** - Schedule future encounters
4. **Decision Rules** - Calculate values and make decisions

For each type, provide:
- Purpose
- Complete JavaScript structure template
- Parameter explanations

**Template**:
```markdown
## Rule Types and Structure

### 1. Form Element Rules
**Purpose**: Control visibility, set values, skip answers, and validate individual form elements

**Structure**:
\`\`\`javascript
'use strict';
({params, imports}) => {
  const entity = params.entity; // programEncounter, programEnrolment, or individual
  const formElement = params.formElement;
  const moment = imports.moment;
  const _ = imports.lodash;
  
  let visibility = true;
  let value = null;
  let answersToSkip = [];
  let validationErrors = [];
  
  // Rule logic here
  
  return new imports.rulesConfig.FormElementStatus(
    formElement.uuid, 
    visibility, 
    value, 
    answersToSkip, 
    validationErrors
  );
};
\`\`\`
```

#### Section 11: Extract and Document All Rules

**Step 1: Extract Rules from Forms**

For each form JSON file in `/forms/` directory (excluding voided forms):

1. **Form Element Rules**: Extract from `formElementGroup[].formElement[].rule` field
2. **Validation Rules**: Extract from `validationRule` field
3. **Visit Schedule Rules**: Extract from form-level or encounter-level scheduling rules
4. **Decision Rules**: Extract from `decisionRule` field

**Step 2: Categorize Rules by Pattern**

Identify and document at least 10 common rule patterns with real examples:

1. **Conditional Visibility Based on Answer**
   - Use case, code example, real form example
   
2. **Age-Based Visibility**
   - Use case, code example, real form example
   
3. **Previous Encounter Value Display**
   - Use case, code example, real form example
   
4. **Calculated Value (Auto-filled)**
   - Use case, code example (BMI, z-scores, etc.)
   
5. **Validation with Error Messages**
   - Use case, code example
   
6. **Cross-Field Validation**
   - Use case, code example (comparing current vs previous values)
   
7. **Location-Based Visibility**
   - Use case, code example (location properties)
   
8. **Date Validation**
   - Use case, code example (prevent future dates, date ranges)
   
9. **Complex Multi-Encounter Logic**
   - Use case, code example (growth faltering, trends)
   
10. **Clinical Calculations**
    - Use case, code example (z-scores, nutritional status)

**Format for Each Pattern**:
```markdown
### Pattern [N]: [Pattern Name]
**Use Case**: [Description]

\`\`\`javascript
'use strict';
({params, imports}) => {
  // Generic pattern code
};
\`\`\`

**Example from [Form Name]**:
\`\`\`javascript
// Real implementation from the organization's forms
\`\`\`
```

**Step 3: Document Rule Statistics**

Provide counts:
- Total form element rules: [N]
- Total validation rules: [N]
- Total visit schedule rules: [N]
- Total decision rules: [N]

#### Section 12: Helper Functions and Libraries

Document all available helper functions and entity methods:

1. **Moment.js** - Date/time manipulation
2. **Lodash** - Utility functions
3. **RulesConfig** - Avni-specific (RuleCondition, FormElementStatus, VisitScheduleBuilder)
4. **Rule Service Library** - Shared functions (calculateBMI, getZScore, etc.)

For each, provide:
- Import statement
- Common operations with examples
- Entity methods (Individual, ProgramEnrolment, ProgramEncounter)

**Format**:
```markdown
## Helper Functions and Libraries

### Available Imports

#### 1. Moment.js (Date/Time Manipulation)
\`\`\`javascript
const moment = imports.moment;

// Common operations
moment().add(7, 'days')
moment().subtract(1, 'month')
moment(date1).diff(date2, 'days')
\`\`\`

### Entity Methods

#### Individual
\`\`\`javascript
individual.getAgeInYears()
individual.getAgeInMonths()
individual.dateOfBirth
individual.lowestAddressLevel.locationProperties
\`\`\`
```

#### Section 13: Best Practices

Document 8-10 best practices with code examples:

1. **Performance Optimization** - Filter early, avoid nested loops
2. **Null/Undefined Checks** - Always check before using values
3. **Date Handling** - Use startOf('day') for comparisons
4. **Error Messages** - Clear, actionable messages
5. **Code Reusability** - Extract common logic
6. **Declarative vs Imperative Rules** - When to use each
7. **Testing Considerations** - Edge cases to test
8. **Documentation** - Comment complex logic

**Format**:
```markdown
## Best Practices

### 1. [Practice Name]
- [Guideline]
- [Guideline]

\`\`\`javascript
// Good
[example]

// Avoid
[counter-example]
\`\`\`
```

#### Section 14: Usage Guidelines

Document when to use each rule type:
- Form Element Rule: Show/hide fields, calculate values, validate individual fields
- Validation Rule: Cross-field validation, form-level business rules
- Visit Schedule Rule: Schedule future encounters, set visit windows
- Decision Rule: Calculate derived values, flag high-risk cases

#### Section 15: Generating New Rules

Provide step-by-step process:
1. Identify requirement
2. Find similar pattern in knowledge base
3. Adapt pattern to requirement
4. Test edge cases
5. Add error handling
6. Document logic

Include a complete worked example.

---

## Execution Steps

### Step 1: Read Configuration Files
```
Read the following files from the implementation folder:
- subjectTypes.json
- programs.json
- encounterTypes.json
- addressLevelTypes.json
- formMappings.json
- concepts.json (for summary only)
```

### Step 2: List Form Files
```
List all JSON files in the /forms/ directory
Identify and exclude voided forms
```

### Step 3: Extract Rules
```
For each non-voided form file:
  1. Read the form JSON
  2. Extract all rule types:
     - Form element rules (from formElementGroup[].formElement[].rule)
     - Validation rules (from validationRule)
     - Visit schedule rules (from form-level scheduling)
     - Decision rules (from decisionRule)
  3. Store with context (form name, element name, rule type)
```

### Step 4: Analyze and Categorize Rules
```
1. Group rules by pattern type
2. Identify the 10+ most common patterns
3. Select representative examples for each pattern
4. Extract helper function usage
5. Document best practices observed
```

### Step 5: Generate Knowledge Base File
```
1. Create [org]_context.md file
2. Write Part 1: Implementation Overview (Sections 1-9)
3. Write Part 2: Rules Documentation (Sections 10-15)
4. Include separator between parts
5. Add metadata footer (last updated, total rules, platform)
```

### Step 6: Create Supporting JSON File (Optional)
```
Create extracted_rules.json with:
{
  "formElementRules": [
    {
      "formName": "...",
      "formType": "...",
      "elementName": "...",
      "rule": "..."
    }
  ],
  "validationRules": [...],
  "visitScheduleRules": [...],
  "decisionRules": [...]
}
```

---

## Quality Checklist

Ensure the generated knowledge base includes:

- [ ] Complete metadata (organization, platform, focus areas)
- [ ] All subject types documented with UUIDs and purposes
- [ ] All programs with eligibility and summary fields
- [ ] All encounter types with eligibility rules
- [ ] Complete address hierarchy
- [ ] All form mappings categorized
- [ ] Workflow diagrams for each program
- [ ] At least 10 common rule patterns with examples
- [ ] Complete rule type structures (all 4 types)
- [ ] Helper function documentation
- [ ] Entity method documentation
- [ ] Best practices (8-10 items)
- [ ] Usage guidelines for each rule type
- [ ] Step-by-step guide for generating new rules
- [ ] Rule statistics (total counts by type)
- [ ] Real code examples from the implementation
- [ ] Proper markdown formatting with code blocks
- [ ] Table of contents with working links
- [ ] Metadata footer

---

## Example Usage

### Input
```
Organization Name: APF Odisha
Implementation Folder: reference/apfodisha_context
Focus Areas: Maternal and child nutrition tracking, NRC management, QRT interventions
```

### Command
```
Create a comprehensive knowledge base markdown file for the APF Odisha implementation 
in the reference/apfodisha_context folder. Document all content including subject types, 
programs, encounters, forms, and extract all JavaScript rules (form element, validation, 
visit scheduling, decision) from the forms. Categorize rules by type and pattern, and 
provide usage guidelines for generating new rules.
```

### Expected Output
- File: `reference/apfodisha_context/apfodisha_context.md`
- Size: ~2000-2500 lines
- Structure: Part 1 (Implementation) + Part 2 (Rules)
- Total rules documented: 300-400+ rules
- Common patterns: 10+ with examples
- Complete helper function reference
- Best practices and usage guidelines

---

## Notes

1. **Preserve Code Formatting**: Keep all JavaScript code properly formatted with correct indentation
2. **Use Absolute UUIDs**: Always include full UUIDs for traceability
3. **Mark Voided Items**: Clearly indicate voided/historical entities
4. **Real Examples**: Use actual code from the implementation, not generic examples
5. **Context Preservation**: Include enough context for each rule to understand its purpose
6. **Searchability**: Use consistent terminology and include keywords for easy searching
7. **Completeness**: Document ALL rules, not just a sample
8. **Categorization**: Group similar rules together for pattern recognition
9. **Practical Focus**: Emphasize patterns that will help generate new rules
10. **Dify Optimization**: Structure content for optimal chunking and retrieval in Dify

---

## File Structure Summary

```
[org]_context.md
├── Part 1: Implementation Overview
│   ├── Overview
│   ├── Table of Contents
│   ├── Subject Types
│   ├── Programs
│   ├── Encounter Types
│   ├── Address Level Types
│   ├── Form Mappings
│   ├── Forms Structure
│   ├── Key Concepts
│   └── Workflows
├── Separator (---)
└── Part 2: Rules Documentation
    ├── Rule Types and Structure
    ├── Common Rule Patterns (10+)
    ├── Form Element Rules
    ├── Validation Rules
    ├── Visit Schedule Rules
    ├── Decision Rules
    ├── Helper Functions and Libraries
    ├── Best Practices
    ├── Usage Guidelines
    ├── Generating New Rules
    └── Metadata Footer
```

---

**Last Updated**: Template Version 1.0
**Purpose**: Generate comprehensive knowledge bases for Avni implementations
**Target Platform**: Dify Knowledge Base with RAG pipeline
**Chunking Recommendation**: Delimiter `\n\n`, Max chunk 1000 chars, Overlap 150 chars
