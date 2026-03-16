# Avni AI Assistant Knowledge Base

**For Implementers** | Version 2.0 | Last Updated: March 16, 2026

## Welcome

This knowledge base helps Avni implementers configure and troubleshoot Avni implementations. It covers JavaScript rules, form configuration, concept management, organization setup, and implementation patterns.

**What's new in v2.0:**
- ✅ Reorganized into 10 focused categories
- ✅ 68 topic-specific files (vs 5 monolithic files)
- ✅ Implementer-focused content (96% relevant)
- ✅ LLM-optimized with metadata and semantic chunks
- ✅ Troubleshooting guides from 90,000+ support tickets
- ✅ Clear navigation and cross-references


## Quick Navigation

### 🚀 New to Avni?
**Start here:** [Getting Started Guide](00-getting-started/README.md)
- [AI Assistant Capabilities](00-getting-started/ai-capabilities.md) - What the AI can help with
- [Quick Start Tutorial](00-getting-started/quick-start-implementer.md) - 15-minute setup guide
- [Terminology Glossary](00-getting-started/terminology-glossary.md) - Essential terms

### 🔧 Common Tasks
- **Create a form:** [Form Structure](03-concepts-and-forms/form-structure.md)
- **Write a rule:** [JavaScript Rules](05-javascript-rules/README.md)
- **Schedule visits:** [Visit Schedule Rules](05-javascript-rules/visit-schedule-rules.md)
- **Set up users:** [User Management](02-organization-setup/user-management.md)
- **Import data:** [Bulk Data Upload](06-data-management/bulk-data-upload.md)

### 🐛 Troubleshooting
- [Form fields not showing](08-troubleshooting/form-configuration-issues.md)
- [Rules not working](08-troubleshooting/rules-debugging.md)
- [Visits not appearing](08-troubleshooting/visit-scheduling-issues.md)
- [Data import errors](08-troubleshooting/data-import-troubleshooting.md)


## Knowledge Base Structure

### [00 - Getting Started](00-getting-started/README.md)
**For:** New implementers, quick reference  
**Priority:** Critical ⭐⭐⭐⭐⭐

Essential information to begin your Avni journey:
- AI Assistant capabilities and limitations
- 15-minute quick start tutorial
- Terminology glossary
- First steps guidance

---

### [01 - Core Concepts](01-core-concepts/README.md)
**For:** Understanding Avni's architecture and data model  
**Priority:** High ⭐⭐⭐⭐

Foundational knowledge about how Avni works:
- Avni architecture overview
- Domain model (Subject, Program, Encounter)
- Data model (Forms, Observations)
- Offline sync basics

---

### [02 - Organization Setup](02-organization-setup/README.md)
**For:** Setting up organizations, users, and locations  
**Priority:** Critical ⭐⭐⭐⭐⭐

Configure your organizational structure:
- Organization creation
- Address hierarchy and locations
- Catchment configuration
- User management and privileges
- Access control

---

### [03 - Concepts and Forms](03-concepts-and-forms/README.md)
**For:** Designing data collection forms  
**Priority:** Critical ⭐⭐⭐⭐⭐

Build forms to collect data:
- Concept types and management
- Form structure and design patterns
- Form element types
- Repeatable question groups
- Multi-language forms
- Media in forms

---

### [04 - Subject Types and Programs](04-subject-types-programs/README.md)
**For:** Designing program workflows  
**Priority:** Critical ⭐⭐⭐⭐⭐

Structure your programs and subjects:
- Subject types configuration
- Program design
- Encounter types
- Workflow design patterns
- Auto-generated identifiers

---

### [05 - JavaScript Rules](05-javascript-rules/README.md)
**For:** Adding custom logic and automation  
**Priority:** Critical ⭐⭐⭐⭐⭐

Write rules for validation, calculations, and scheduling:
- Rules introduction
- Validation rules
- Decision rules (skip logic, calculations)
- Visit schedule rules
- Task schedule rules
- Helper functions reference
- Common patterns and best practices

---

### [06 - Data Management](06-data-management/README.md)
**For:** Importing, managing, and maintaining data  
**Priority:** High ⭐⭐⭐⭐

Handle data operations:
- Bulk data upload (CSV)
- Data import validation
- Web-based data entry
- Subject migration
- Voiding data

---

### [07 - Mobile App Features](07-mobile-app-features/README.md)
**For:** Configuring mobile app functionality  
**Priority:** Medium ⭐⭐⭐

Customize the mobile experience:
- Offline dashboards
- Dashboard filters
- Custom search fields
- Quick form edit
- App configuration

---

### [08 - Troubleshooting](08-troubleshooting/README.md)
**For:** Solving common implementation issues  
**Priority:** High ⭐⭐⭐⭐

Debug and fix problems:
- Form configuration issues
- Rules debugging
- Visit scheduling issues
- Data import troubleshooting
- Duplicate data handling
- Testing and verification queries
- Quick fixes reference

---

### [09 - Implementation Guides](09-implementation-guides/README.md)
**For:** Real-world implementation examples  
**Priority:** Medium ⭐⭐⭐

Learn from complete implementations:
- Maternal health example
- Child nutrition example
- Education monitoring example
- Implementation checklist

---

### [10 - Reference](10-reference/README.md)
**For:** Quick lookups and FAQs  
**Priority:** Medium ⭐⭐⭐

Reference materials:
- FAQ (from 200+ implementation questions)
- API endpoints
- Version compatibility


## How to Use This Knowledge Base

### For New Implementers
1. Start with [Getting Started](00-getting-started/README.md)
2. Read [Core Concepts](01-core-concepts/README.md) to understand the system
3. Follow [Quick Start Tutorial](00-getting-started/quick-start-implementer.md)
4. Explore specific topics as needed

### For Experienced Implementers
- Jump directly to relevant sections
- Use search or ask the AI Assistant
- Check [Troubleshooting](08-troubleshooting/README.md) for issues
- Reference [FAQ](10-reference/faq-implementation.md) for quick answers

### For Specific Tasks
- **Designing a form?** → [Concepts and Forms](03-concepts-and-forms/README.md)
- **Writing rules?** → [JavaScript Rules](05-javascript-rules/README.md)
- **Setting up users?** → [Organization Setup](02-organization-setup/README.md)
- **Debugging an issue?** → [Troubleshooting](08-troubleshooting/README.md)


## Working with the AI Assistant

### Ask Specific Questions
❌ "How do I create a form?"  
✅ "How do I create a registration form for pregnant women with fields for name, age, LMP date, and phone number?"

### Provide Context
Include:
- What you're trying to achieve
- What you've already tried
- Any error messages
- Your implementation scenario

### Share Code for Debugging
When asking about rules, share your JavaScript code so the AI can identify issues.

### Learn More
See [AI Assistant Capabilities](00-getting-started/ai-capabilities.md) for full details on what the AI can help with.


## What Changed in v2.0?

### Content Reorganization
- **Before:** 5 large files (1.4 MB, 50% relevant)
- **After:** 68 focused files (1.2 MB, 96% relevant)

### Removed Content
- ❌ Reporting and analytics setup (Metabase/Superset)
- ❌ Infrastructure and deployment
- ❌ Integration architecture
- ❌ Database administration
- ❌ System monitoring

**Why?** These topics are not implementer responsibilities. Contact support for:
- Infrastructure issues
- Reporting setup
- External integrations
- Database operations

### Added Content
- ✅ ~7,000 lines of unique implementer guides (from merged.md)
- ✅ ~600 lines of troubleshooting (from 90,000+ support tickets)
- ✅ LLM optimization (metadata, semantic chunks)
- ✅ Cross-references and navigation

### Improved Organization
- Topic-based files (not monolithic)
- Clear navigation hierarchy
- Focused content (one topic per file)
- Better searchability


## Finding Content from Old Structure

### Old README.md → New Structure

| Old Section | New Location |
|-------------|--------------|
| Getting Started | [00-getting-started/](00-getting-started/README.md) |
| Terminology | [00-getting-started/terminology-glossary.md](00-getting-started/terminology-glossary.md) |
| Architecture | [01-core-concepts/avni-architecture.md](01-core-concepts/avni-architecture.md) |
| Domain Model | [01-core-concepts/domain-model.md](01-core-concepts/domain-model.md) |
| Forms | [03-concepts-and-forms/](03-concepts-and-forms/README.md) |
| Rules | [05-javascript-rules/](05-javascript-rules/README.md) |
| Helper Functions | [05-javascript-rules/helper-functions.md](05-javascript-rules/helper-functions.md) |

### Old merged.md → New Structure

| Content | New Location |
|---------|--------------|
| Access Control | [02-organization-setup/access-control.md](02-organization-setup/access-control.md) |
| Bulk Upload | [06-data-management/bulk-data-upload.md](06-data-management/bulk-data-upload.md) |
| Offline Dashboards | [07-mobile-app-features/offline-dashboards.md](07-mobile-app-features/offline-dashboards.md) |
| Repeatable Groups | [03-concepts-and-forms/repeatable-question-groups.md](03-concepts-and-forms/repeatable-question-groups.md) |

### Old test-prompts.md → New Structure

| Content | New Location |
|---------|--------------|
| Q&A | [10-reference/faq-implementation.md](10-reference/faq-implementation.md) |
| Code Examples | [05-javascript-rules/common-patterns.md](05-javascript-rules/common-patterns.md) |

**Note:** Old files are archived in `_archive/` folder for reference.


---

## Need Help?

- **Ask the AI Assistant:** Specific implementation questions
- **Check Troubleshooting:** [08-troubleshooting/](08-troubleshooting/README.md)
- **Review FAQ:** [10-reference/faq-implementation.md](10-reference/faq-implementation.md)
- **Contact Support:** Infrastructure, reporting, integration issues

---

**Version:** 2.0  
**Last Updated:** 2026-03-16  
**Total Files:** 68 organized documents  
**Focus:** Implementer tasks (JavaScript rules, forms, configuration, troubleshooting)


================================================================================
# Section: Getting Started
================================================================================


---
<!-- Source: 00-getting-started/README.md -->

# Getting Started with Avni Implementation

## Overview

Welcome to the Avni AI Assistant knowledge base for implementers. This section helps you understand what Avni is, what the AI Assistant can help with, and how to get started with your first implementation.

**What you'll find here:**
- Understanding AI Assistant capabilities
- Quick start guide (15 minutes)
- Essential terminology
- Navigation to detailed topics

**Who this is for:** New implementers starting their first Avni project, or experienced implementers looking for quick reference.


## Contents

### 1. [AI Assistant Capabilities](ai-capabilities.md)
**What:** Understanding what the AI Assistant can and cannot help with  
**When to use:** Before asking questions, to understand the AI's scope  
**Priority:** Critical ⭐⭐⭐⭐⭐

Learn about:
- What the AI can help with (rules, forms, workflows, troubleshooting)
- What to contact support for (infrastructure, reporting, integrations)
- How to ask effective questions
- Example queries

### 2. [Quick Start Guide](quick-start-implementer.md)
**What:** 15-minute tutorial to set up your first Avni implementation  
**When to use:** Starting a new project, need step-by-step guidance  
**Priority:** Critical ⭐⭐⭐⭐⭐

Covers:
- Organization setup
- Creating locations and concepts
- Building your first form
- Writing a simple rule
- Testing the workflow

### 3. [Terminology Glossary](terminology-glossary.md)
**What:** Essential Avni terms and concepts  
**When to use:** When you encounter unfamiliar terms  
**Priority:** High ⭐⭐⭐⭐

Includes:
- Subject, Program, Encounter
- Form, Concept, Observation
- Location, Catchment, User
- And more...


## Next Steps

After completing the getting started section:

### Learn Core Concepts
→ [Core Concepts](../01-core-concepts/README.md) - Understand Avni's architecture and data model

### Set Up Your Organization
→ [Organization Setup](../02-organization-setup/README.md) - Configure users, locations, and access control

### Design Forms and Workflows
→ [Concepts and Forms](../03-concepts-and-forms/README.md) - Create data collection forms  
→ [Subject Types and Programs](../04-subject-types-programs/README.md) - Design program workflows

### Write JavaScript Rules
→ [JavaScript Rules](../05-javascript-rules/README.md) - Add custom logic and automation


## Quick Links

**Common Questions:**
- [How do I create a form?](../03-concepts-and-forms/form-structure.md)
- [How do I write a validation rule?](../05-javascript-rules/validation-rules.md)
- [How do I schedule visits?](../05-javascript-rules/visit-schedule-rules.md)
- [How do I set up users?](../02-organization-setup/user-management.md)

**Troubleshooting:**
- [Form not showing fields](../08-troubleshooting/form-configuration-issues.md)
- [Rules not working](../08-troubleshooting/rules-debugging.md)
- [Visits not appearing](../08-troubleshooting/visit-scheduling-issues.md)

**Examples:**
- [Maternal health implementation](../09-implementation-guides/maternal-health-example.md)
- [Child nutrition program](../09-implementation-guides/child-nutrition-example.md)


## Recommended Learning Path

### For New Implementers (Week 1)
1. ✅ Read [AI Capabilities](ai-capabilities.md)
2. ✅ Complete [Quick Start Guide](quick-start-implementer.md)
3. ✅ Review [Terminology Glossary](terminology-glossary.md)
4. → Move to [Core Concepts](../01-core-concepts/README.md)

### For Experienced Implementers
- Jump directly to specific topics using navigation above
- Use [FAQ](../10-reference/faq-implementation.md) for quick answers
- Check [Troubleshooting](../08-troubleshooting/README.md) for common issues


---

**Navigation:**  
[← Back to Knowledge Base](../README.md) | [Next: Core Concepts →](../01-core-concepts/README.md)


---
<!-- Source: 00-getting-started/ai-capabilities.md -->

# Avni AI Assistant Capabilities

## What the AI Assistant Can Help With

The Avni AI Assistant is designed to help **implementers** configure and troubleshoot Avni implementations. It specializes in:

### 1. Answering Questions About Avni
- Explaining Avni concepts and terminology
- Clarifying how features work
- Providing implementation guidance
- Sharing best practices

### 2. Designing Workflows and Forms
- Designing program structures
- Creating form layouts
- Configuring subject types
- Planning encounter types
- Structuring multi-stage workflows

### 3. Writing JavaScript Rules
- **Validation Rules** - Checking data correctness
- **Decision Rules** - Skip logic, field visibility, calculations
- **Visit Schedule Rules** - Determining when visits should happen
- **Task Schedule Rules** - Creating tasks for users
- Providing code examples and patterns
- Debugging rule issues

### 4. Creating Configuration Entities
- Location Types and Locations
- Catchments
- Subject Types
- Programs
- Encounter Types
- Concepts and form elements

### 5. Troubleshooting Implementation Issues
- Form configuration problems
- Rules not working as expected
- Visit scheduling issues
- Data import errors
- Common implementation mistakes


## What the AI Assistant Focuses On

The AI Assistant is optimized for **implementation tasks**. For other needs, you may need to contact support:

### Implementation Tasks (AI Can Help) ✅
- Configuring forms, rules, and workflows
- Writing JavaScript for validation, decisions, and scheduling
- Setting up organizations, users, and locations
- Designing programs and encounters
- Troubleshooting configuration issues
- Understanding Avni concepts

### Operations Tasks (Contact Support) 📞
- Infrastructure and deployment issues
- Server performance problems
- Database administration
- Backup and restore operations
- Network and connectivity issues

### Analytics Tasks (Contact Data Team) 📊
- Metabase report creation
- Superset dashboard setup
- ETL job configuration
- Complex SQL queries for reports
- Data warehouse management

### Integration Tasks (Contact Dev Team) 🔧
- External system integrations
- API development
- Custom integrations with Bahmni, DHIS2, etc.
- Integration service configuration


## How to Get the Best Results

### Be Specific
❌ "How do I create a form?"
✅ "How do I create a registration form for pregnant women with fields for name, age, LMP date, and phone number?"

### Provide Context
Include relevant details:
- What you're trying to achieve
- What you've already tried
- Any error messages
- Your implementation scenario

### Ask Follow-up Questions
The AI can help you refine your approach through conversation.

### Share Code for Debugging
When asking about rules, share your JavaScript code so the AI can identify issues.


## Example Queries

**Good questions to ask:**
- "How do I add skip logic to hide a field based on a previous answer?"
- "Why is my visit schedule rule not creating visits after enrollment?"
- "What's the difference between a program encounter and a general encounter?"
- "How do I create a validation rule to check if age is between 15 and 49?"
- "Can you show me an example of a maternal health program structure?"

**Questions better for support:**
- "Why is my server slow?"
- "How do I set up Metabase?"
- "Can you integrate Avni with our hospital system?"
- "How do I backup the database?"


---
<!-- Source: 00-getting-started/quick-start-implementer.md -->

# Quick Start Guide for Avni Implementers

## TL;DR

This guide walks you through the essential steps to start implementing on Avni. You'll learn to create organizations, define subject types, build forms, and write basic rules. Estimated time: 2-3 hours for a basic setup.

**Core workflow:** Organization → Locations → Subject Types → Forms → Programs → Rules


## Overview

**What:** A step-by-step guide to get your first Avni implementation running.

**When to use:** You're starting a new Avni implementation and need to understand the basic setup flow.

**Prerequisites:** 
- Access to Avni admin portal
- Understanding of your program requirements (who you're tracking, what data you need)
- Basic familiarity with forms and data collection

**What you'll build:** A simple maternal health tracking system with beneficiary registration and ANC visit forms.


## Step 1: Set Up Your Organization

**Goal:** Create the organizational structure for your implementation.

### What is an Organization?

An organization in Avni is your isolated workspace. All your data, users, and configuration belong to one organization.

### Actions:

1. **Access admin portal:** `https://app.avniproject.org`
2. **Log in** with your credentials
3. **Verify organization** is created (usually done by Avni team)

**Expected result:** You can see the admin dashboard with options for Forms, Concepts, Subject Types, etc.

**Troubleshooting:** If you don't have access, contact Avni support to create your organization.


## Step 2: Define Location Hierarchy

**Goal:** Set up the geographic structure where your program operates.

### What are Locations?

Locations represent the geographic hierarchy (State → District → Block → Village). They determine:
- Where subjects are registered
- Which users see which data
- How data is organized in reports

### Actions:

1. **Go to:** Admin → Address Levels
2. **Create hierarchy:**
   - State (Level 1)
   - District (Level 2)
   - Block (Level 3)
   - Village (Level 4)

3. **Add locations:**
   - Admin → Locations → Upload CSV
   - Or create manually through UI

**Example CSV format:**
```csv
Name,Type,Parent
Maharashtra,State,
Pune,District,Maharashtra
Haveli,Block,Pune
Wadgaon,Village,Haveli
```

**Expected result:** You can see your location hierarchy in the Locations page.


## Step 3: Create Concepts

**Goal:** Define the data elements you'll collect.

### What are Concepts?

Concepts are the underlying data fields - like "Age", "Blood Pressure", "Pregnancy Status". They can be reused across multiple forms.

### Common Concept Types:

| Type | Use Case | Example |
|------|----------|---------|
| Numeric | Numbers | Age, Weight, Hemoglobin |
| Text | Free text | Name, Address |
| Coded | Predefined options | Gender (Male/Female), Yes/No |
| Date | Dates | Date of Birth, Visit Date |

### Actions:

1. **Go to:** Admin → Concepts
2. **Create basic concepts:**
   - Name (Text)
   - Age (Numeric)
   - Gender (Coded: Male, Female, Other)
   - Date of Birth (Date)
   - Mobile Number (Text)
   - LMP Date (Date) - for maternal health
   - Blood Pressure (Numeric)

**Expected result:** You have a library of reusable concepts.


## Step 4: Create Subject Type

**Goal:** Define what/who you're tracking.

### What is a Subject Type?

A subject type defines the entities you track - usually people (beneficiaries, patients) but can also be things (water sources, schools).

### Actions:

1. **Go to:** Admin → Subject Types
2. **Click:** Create Subject Type
3. **Configure:**
   - Name: "Pregnant Woman"
   - Type: Person (gives you name, gender, DOB fields automatically)
   - Active: Yes

**Expected result:** You have a subject type ready for registration.


## Step 5: Build Registration Form

**Goal:** Create the form to register new subjects.

### What is a Registration Form?

The registration form captures baseline information when you first register a subject in the system.

### Actions:

1. **Go to:** Admin → Forms
2. **Find:** Registration form for "Pregnant Woman" (auto-created)
3. **Add form elements:**
   - Form Element Group: "Basic Information"
     - Name (auto-included)
     - Age (auto-included)
     - Date of Birth (auto-included)
     - Mobile Number (link to concept)
   - Form Element Group: "Pregnancy Details"
     - LMP Date (link to concept)
     - Expected Delivery Date (calculated)

4. **Configure properties:**
   - Make Mobile Number mandatory
   - Make LMP Date mandatory

**Expected result:** You have a working registration form.


## Step 6: Create Program

**Goal:** Set up the program structure for tracking over time.

### What is a Program?

A program tracks a subject through a journey (pregnancy, treatment, education). It includes:
- Enrollment form (baseline data)
- Encounter types (visits/checkups)
- Exit form (completion/dropout)

### Actions:

1. **Go to:** Admin → Programs
2. **Click:** Create Program
3. **Configure:**
   - Name: "Pregnancy Program"
   - Subject Type: Pregnant Woman
   - Active: Yes

4. **Create enrollment form:**
   - Add fields for enrollment baseline data
   - Link to concepts

**Expected result:** You have a program ready for enrollments.


## Step 7: Add Encounter Types

**Goal:** Define the types of visits/checkups in your program.

### What are Encounter Types?

Encounter types represent different kinds of interactions - ANC visits, delivery, PNC visits, etc.

### Actions:

1. **Go to:** Admin → Encounter Types
2. **Create:** "ANC Visit"
   - Type: Program Encounter
   - Program: Pregnancy Program

3. **Create form for ANC Visit:**
   - Weight
   - Blood Pressure
   - Hemoglobin
   - Any complications
   - Next visit date

**Expected result:** You have encounter types with forms ready for data collection.


## Step 8: Add a Simple Rule

**Goal:** Add logic to calculate expected delivery date.

### What are Rules?

Rules add custom logic - calculations, validations, skip logic, visit scheduling.

### Example: Calculate Expected Delivery Date

```javascript
// Decision rule to calculate EDD from LMP
const CalculateEDD = {
  'calculatedEDD': function(individual, formElement) {
    const lmp = individual.getObservationValue('LMP Date');
    if (lmp) {
      // Add 280 days (40 weeks) to LMP
      const edd = new Date(lmp);
      edd.setDate(edd.getDate() + 280);
      return edd;
    }
    return null;
  }
};
```

### Actions:

1. **Go to:** Admin → Forms → Registration Form
2. **Find:** Expected Delivery Date field
3. **Add rule:** Paste the calculation code
4. **Test:** Register a woman with LMP date, verify EDD calculates

**Expected result:** EDD automatically calculates when LMP is entered.


## Step 9: Test Your Setup

**Goal:** Verify everything works end-to-end.

### Testing Checklist:

1. **Register a subject:**
   - Go to web app or mobile app
   - Register a pregnant woman
   - Verify all fields save correctly

2. **Enroll in program:**
   - Enroll the woman in Pregnancy Program
   - Verify enrollment form works

3. **Create an encounter:**
   - Do an ANC visit
   - Fill the form
   - Verify data saves

4. **Check calculations:**
   - Verify EDD calculated correctly
   - Check any other rules

**Expected result:** Complete workflow from registration to encounter works smoothly.


## Next Steps

Now that you have a basic setup, you can:

### Add More Features:
- **Visit scheduling rules** - Automatically schedule ANC visits
- **Validation rules** - Ensure data quality
- **Skip logic** - Show/hide fields based on answers
- **Multiple programs** - Track different interventions

### Improve Your Forms:
- Add more detailed questions
- Use coded concepts for better reporting
- Add help text for field workers
- Configure multi-language support

### Set Up Users:
- Create user accounts
- Assign catchments
- Configure privileges
- Set up user groups

### Learn Advanced Topics:
- Complex rules with helper functions
- Multi-stage programs
- Repeatable question groups
- Offline dashboards


## FAQ

**Q: How long does initial setup take?**

A: Basic setup (organization, locations, one subject type, one form): 2-3 hours. Full implementation with rules and testing: 1-2 weeks.

**Q: Can I change things after going live?**

A: Yes! You can add fields, modify forms, update rules. Users need to sync to get changes.

**Q: What if I make a mistake?**

A: Most configuration can be edited. Data can be voided (soft delete). Test thoroughly before going live.

**Q: Do I need to know programming?**

A: Basic setup: No. Advanced rules: Yes, JavaScript knowledge helps.


## Common Issues

### Issue: Can't see my form in the app

**Cause:** App hasn't synced yet

**Solution:**
1. Go to Settings → Sync Now
2. Wait for sync to complete
3. Check if form appears

### Issue: Calculated field not working

**Cause:** Rule syntax error or concept name mismatch

**Solution:**
1. Check concept name is exact (case-sensitive)
2. Verify rule syntax in admin portal
3. Check browser console for errors

### Issue: User can't see registered subjects

**Cause:** Catchment not assigned or location mismatch

**Solution:**
1. Verify user has catchment assigned
2. Check subject's location is in user's catchment
3. Force sync on mobile app


## Resources

**Documentation:**
- [Concept Management](concepts-and-forms/concept-types.md)
- [Form Design](concepts-and-forms/form-structure.md)
- [JavaScript Rules](javascript-rules/rules-introduction.md)
- [Organization Setup](organization-setup/organization-creation.md)

**Get Help:**
- Ask the AI Assistant specific questions
- Contact Avni support for technical issues
- Join community forums for best practices


---
<!-- Source: 00-getting-started/terminology-glossary.md -->

# Avni Terminology Glossary

## TL;DR

Essential Avni terms every implementer needs to know. This glossary covers the core entities (Subject, Program, Encounter, Form) and organizational concepts (Location, Catchment, User) that form the foundation of Avni implementations.


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


---

**Navigation:**  
[← Back to Getting Started](README.md) | [Next: Core Concepts →](../01-core-concepts/README.md)


================================================================================
# Section: Core Concepts
================================================================================


---
<!-- Source: 01-core-concepts/README.md -->

# Core Concepts - Avni Architecture and Data Model

Understanding Avni's architecture and data model is essential for effective implementation.

## Contents

### 1. [Avni Architecture](avni-architecture.md)
High-level overview of Avni's components and how they work together.

### 2. [Domain Model](domain-model.md)
How subjects, programs, and encounters relate to each other.

### 3. [Data Model](data-model.md)
How data is structured (forms, observations, JSONB).

### 4. [Offline Sync Basics](offline-sync-basics.md)
How offline functionality and data synchronization works.

---

**Navigation:**  
[← Back to Knowledge Base](../README.md) | [Next: Organization Setup →](../02-organization-setup/README.md)


---
<!-- Source: 01-core-concepts/avni-architecture.md -->

# Avni Architecture Overview

## TL;DR

Avni is a multi-tenant platform with mobile field apps that work offline, a web-based admin interface for configuration, and a central server for data storage and synchronization. The architecture supports multiple organizations on shared infrastructure while maintaining complete data isolation.


## Overview

**What:** Understanding Avni's component architecture and how they interact.

**When to use:** Planning your implementation, understanding system capabilities, troubleshooting issues.

**Key components:**
- Field App (Android) - Offline data collection
- Admin Web App - Configuration and management
- Avni Server - Central data storage
- Rules Server - JavaScript rule execution
- ETL Server - Reporting data preparation


## Avni Components

### Field App (Android)

**Purpose:** Primary interface for field workers to collect data.

**Key features:**
- Works completely offline
- Syncs data when internet available
- Form-based data collection
- Dashboard for pending work
- Media capture (photos, videos)

**Use cases:**
- Health workers visiting villages
- Teachers conducting assessments
- Surveyors collecting data in remote areas

**Technical details:**
- Android 7.0+ required
- Uses Realm database for offline storage
- Syncs incrementally (only changes)
- Catchment-based data access

---

### Administration App and App Designer (Web)

**Purpose:** Configure and manage Avni implementations.

**Key features:**
- Form designer
- Program configuration
- User management
- Location setup
- Data import/export
- Web-based data entry

**Who uses it:**
- Organization administrators
- Implementation engineers
- Data managers

**Access:** Web browser, requires admin credentials

---

### Avni Server

**Purpose:** Central data storage and API server.

**Key responsibilities:**
- Store all transactional data
- Provide APIs for mobile sync
- Manage metadata (forms, programs)
- Handle user authentication
- Support multi-tenancy

**Technical details:**
- PostgreSQL database
- Row-level security for multi-tenancy
- REST APIs
- AWS Cognito for authentication

---

### Rules Server

**Purpose:** Execute JavaScript rules on the server side.

**Why needed:**
- Web data entry needs rule execution
- Can't run JavaScript in browser for security
- Needs access to database for complex rules

**What it does:**
- Executes validation rules
- Runs decision rules
- Calculates visit schedules
- Generates task schedules

---

### ETL Server

**Purpose:** Prepare data for reporting and analytics.

**What it does:**
- Transforms generic form data into implementation-specific schema
- Creates reporting-friendly tables
- Updates at configured frequency
- Optimizes for query performance

**Used by:** Reporting tools (Metabase, Superset)


## Multi-Tenancy

**What:** Multiple organizations share the same server infrastructure while maintaining complete data isolation.

**How it works:**
- Each organization has isolated data
- Row-level security in PostgreSQL
- Users belong to one organization
- Configuration is organization-specific

**Benefits:**
- Cost-effective (shared infrastructure)
- Easier maintenance and updates
- Consistent platform across organizations
- Simplified deployment

**Security:**
- Complete data isolation
- No cross-organization access
- Separate user spaces
- Audit trails per organization


## Data Flow

### Registration Flow
```
Field Worker → Field App (offline) → Sync → Avni Server → ETL → Reports
```

### Configuration Flow
```
Admin → Web App → Avni Server → Sync → Field App
```

### Rule Execution Flow
```
Mobile: Field App → Local Rules Engine
Web: Web App → Rules Server → Database
```

**Key points:**
- Mobile app works offline, syncs later
- Configuration changes require sync
- Rules execute locally on mobile
- Server-side rules for web data entry


## Deployment Options

### Hosted Service (Recommended)
- Managed by Avni team
- Regular updates and maintenance
- Shared infrastructure
- Most cost-effective

### On-Premise
- Self-hosted on your infrastructure
- Full control over deployment
- Requires technical expertise
- Used in areas with limited internet

**For implementers:** Hosted service is recommended. On-premise is only for special cases (no internet, data sovereignty requirements).


## Related Concepts

**For deeper understanding:**
- [Domain Model](domain-model.md) - How entities relate
- [Offline Sync](offline-sync-basics.md) - How sync works
- [Data Model](data-model.md) - How data is structured

**For implementation:**
- [Organization Setup](../02-organization-setup/README.md) - Setting up your org
- [User Management](../02-organization-setup/user-management.md) - Managing users


---

**Navigation:**  
[← Back to Core Concepts](README.md) | [Next: Domain Model →](domain-model.md)


---
<!-- Source: 01-core-concepts/data-model.md -->

# Avni Data Model

## TL;DR

Avni stores form data as observations in JSONB format, providing flexibility to add fields without schema changes. Forms map to concepts, and observations store actual values. This design enables dynamic forms, fast queries, and easy reporting.


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


---

**Navigation:**  
[← Back: Domain Model](domain-model.md) | [Next: Offline Sync →](offline-sync-basics.md)


---
<!-- Source: 01-core-concepts/domain-model.md -->

# Avni Domain Model

## TL;DR

Avni's domain model centers on **Subjects** (people/things you track), **Programs** (services over time), and **Encounters** (data collection events). Subjects are registered, enrolled in programs, and have encounters to record observations. This structure supports longitudinal data collection for health, education, and social programs.


## Overview

**What:** Understanding how Avni's core entities relate to each other.

**When to use:** Designing your implementation, planning data structure, understanding workflows.

**Core entities:**
- Subject - Who/what you're tracking
- Program - Service/intervention over time
- Encounter - Data collection event
- Form - Data collection template
- Observation - Actual data captured


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


---

**Navigation:**  
[← Back: Architecture](avni-architecture.md) | [Next: Data Model →](data-model.md)


---
<!-- Source: 01-core-concepts/offline-sync-basics.md -->

# Offline Sync Basics

## TL;DR

Avni's mobile app works completely offline, storing data locally. When internet is available, it syncs changes bidirectionally - uploading new data and downloading updates. Sync is catchment-based, so users only get data for their assigned locations.


## Overview

**What:** Understanding how Avni enables offline data collection and synchronization.

**Why important:**
- Field workers often have no internet
- Data collection can't wait for connectivity
- Sync must be efficient (limited bandwidth)
- Data integrity must be maintained

**Key concepts:**
- Offline-first architecture
- Local database on mobile
- Incremental sync
- Catchment-based data access


## How Offline Works

### Local Storage
**Mobile app uses Realm database:**
- Stores all data locally
- Fast queries
- Works without internet
- Syncs when connected

**What's stored locally:**
- Reference data (forms, concepts, locations)
- User's subjects (based on catchment)
- Encounters and observations
- Media files (photos, videos)
- Pending sync queue

### Offline Capabilities
**What you can do offline:**
- ✅ Register new subjects
- ✅ Enroll in programs
- ✅ Complete encounters
- ✅ Capture media
- ✅ View dashboards
- ✅ Search subjects
- ✅ View reports (offline cards)

**What requires internet:**
- ❌ Initial app setup
- ❌ Sync data
- ❌ Download configuration changes
- ❌ View online reports


## Sync Process

### Sync Flow
```
1. User clicks "Sync"
2. Upload local changes to server
   - New subjects
   - New encounters
   - Modified data
   - Media files
3. Download server changes
   - Other users' data (in catchment)
   - Configuration updates
   - New forms/concepts
4. Resolve conflicts (if any)
5. Update local database
6. Sync complete
```

### Incremental Sync
**Only changes sync, not everything:**
- Tracks last sync timestamp
- Uploads only new/modified records
- Downloads only updates since last sync
- Efficient for limited bandwidth

**Example:**
```
Last sync: March 15, 10:00 AM
New sync: March 16, 9:00 AM

Upload:
- 5 new subjects registered
- 12 encounters completed
- 3 photos captured

Download:
- 2 subjects from other users
- 1 form update
- 0 configuration changes
```


## Catchment-Based Sync

### What is Catchment-Based Sync?
**Users only sync data for their assigned locations.**

**Example:**
```
User: Priya (Field Worker)
Catchment: Pune District
  ├── Haveli Block
  │   ├── Wadgaon Village
  │   └── Kharadi Village
  └── Mulshi Block
      └── Paud Village

Syncs:
✅ Subjects in Wadgaon, Kharadi, Paud
❌ Subjects in other districts
```

**Benefits:**
- Reduced data transfer
- Faster sync
- Better privacy
- Manageable data size

### Multiple Catchments
**Users can have multiple catchments:**
```
User: Supervisor
Catchments:
- Pune District (all blocks)
- Mumbai District (selected blocks)

Syncs data from both catchments
```


## Common Sync Scenarios

### Scenario 1: First Sync (New User)
**Downloads everything:**
- All forms and concepts
- All locations in catchment
- All subjects in catchment (historical)
- All configuration

**Time:** 5-30 minutes (depending on data size)

---

### Scenario 2: Daily Sync
**Incremental updates:**
- Upload today's work
- Download others' updates
- Get configuration changes

**Time:** 1-5 minutes

---

### Scenario 3: After Long Offline Period
**Larger sync:**
- Upload accumulated data
- Download many updates
- May take longer

**Time:** 5-15 minutes

---

### Scenario 4: Configuration Change
**Admin updates form:**
1. Admin publishes form change
2. Users sync
3. New form downloaded
4. Old data preserved
5. New form used going forward


## Conflict Resolution

### When Conflicts Occur
**Two users edit same subject offline:**
```
User A (offline): Updates phone number
User B (offline): Updates address
Both sync later
```

**Resolution:**
- Last write wins (by server timestamp)
- Both changes preserved in audit log
- No data loss
- Rare in practice (different users, different subjects)

### Preventing Conflicts
**Best practices:**
- Assign users to different catchments
- Avoid overlapping work areas
- Sync frequently
- Clear ownership of subjects


## Troubleshooting Sync Issues

### Sync Fails
**Common causes:**
1. No internet connection
2. Server down
3. Invalid auth token
4. Data validation errors

**Solutions:**
- Check internet connectivity
- Retry sync later
- Re-login if token expired
- Fix validation errors in data

---

### Sync Takes Too Long
**Causes:**
1. First sync (large download)
2. Slow internet
3. Many pending uploads

**Solutions:**
- Use WiFi for first sync
- Sync in batches
- Compress media before sync

---

### Data Not Appearing
**Causes:**
1. Not in user's catchment
2. Voided data
3. Sync not complete

**Solutions:**
- Check catchment assignment
- Verify data not voided
- Complete full sync


## Best Practices

### For Field Workers
1. **Sync daily** - Don't accumulate too much data
2. **Use WiFi** - Faster and no data charges
3. **Charge device** - Sync uses battery
4. **Check sync status** - Ensure complete before closing app

### For Administrators
1. **Plan catchments carefully** - Avoid overlaps
2. **Test configuration changes** - Before rolling out
3. **Monitor sync health** - Check for failed syncs
4. **Provide WiFi access** - At field offices

### For Implementers
1. **Keep forms reasonable size** - Large forms slow sync
2. **Optimize media** - Compress images
3. **Design for offline** - Don't require constant connectivity
4. **Test offline scenarios** - Ensure app works without internet


---

**Navigation:**  
[← Back: Data Model](data-model.md) | [Next: Organization Setup →](../02-organization-setup/README.md)


================================================================================
# Section: Organization Setup
================================================================================


---
<!-- Source: 02-organization-setup/README.md -->

# Organization Setup

Configure your organizational structure, users, locations, and access control.

## Contents

### 1. [Organization Creation](organization-creation.md)
Create a new Avni organization (usually done by Avni team).

### 2. [Address Hierarchy](address-hierarchy.md)
Set up geographic hierarchy (State → District → Block → Village).

### 3. [Location Setup via CSV](location-setup-csv.md)
Bulk upload locations using CSV files.

### 4. [Catchment Configuration](catchment-configuration.md)
Group locations to control data access and sync.

### 5. [User Management](user-management.md)
Create and manage field workers, supervisors, and admins.

### 6. [User Groups and Privileges](user-groups-privileges.md)
Configure permissions and access patterns.

### 7. [Access Control](access-control.md)
Advanced access control and operating scopes.

---

**Navigation:**  
[← Back: Core Concepts](../01-core-concepts/README.md) | [Next: Concepts and Forms →](../03-concepts-and-forms/README.md)


---
<!-- Source: 02-organization-setup/access-control.md -->

# Access Control in Avni

## TL;DR

Before the introduction of Access Control, organisation users with access to the field app could access all functions (i.e. registration, enrolments, search etc.) in the app.

## Overview

Before the introduction of Access Control, organisation users with access to the field app could access all functions (i.e. registration, enrolments, search etc.) in the app. There was a need for some implementations to limit access to specific functions in order to reduce the number of options visible to end users and simplify the workflow for them while also providing a mechanism for access control.

Access Control is implemented via User Groups to facilitate this need. This functionality is available to Organisation admins in the Admin section of the Web app under the User Groups menu.

## Applicability

* The access control rules are applicable in the field app, data entry app, and the web app.
* Access control is not applicable to the reporting app.

## User Groups

User Groups represent a collection of users and a set of privileges allowed to these users. User with EditUserGroup and EditUserConfiguration privilege can define as many groups as they need to define the access control required for their organisation. Each group can be assigned a set of privileges (or all privileges using the switch available at the top).

Each user can be added to multiple groups.

## Privileges are Additive

If any of the groups that a user belongs to allows a particular privilege, the user will have access to that function.

## Default Groups

By default, the system creates an `Everyone` and an `Administrators` group. `Everyone` group includes all the users in the organisation. `Administrators` group grants all the privileges to allow access to all the functionality.

![image](https://files.readme.io/9c003c1-Screenshot_2023-08-08_at_3.46.23_PM.png)

Users cannot be removed from `Everyone` group but the privileges associated with this group can be modified. The has all privileges flag cannot be reset for `Administrators` group.

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

## What if I have a simple setup with no separate users?

You can add all your users to the `Administrators` group.

## Is some data with no access control?

Yes some of the app designer and admin user interface (or non-operational data) is open to all users with read access. This data is not confidential in any of the implementations of Avni, hence this has been kept open for any user with login to the organisation.

## Can users update metadata using the API

No, the server also check for the access privileges of the user.

## Super admin access

Access of super admin is restricted to non-operational data of the organisations. Operational data cannot be viewed as well by super admin. This is to provide visibility to the organisations about who can view their data.

## Related Topics

<!-- Add links to related documentation -->


---
<!-- Source: 02-organization-setup/address-hierarchy.md -->

# Address Hierarchy Setup in Avni

## TL;DR

Below is a list of definitions that are essential for understanding this document.

## Definitions

Below is a list of definitions that are essential for understanding this document.

* **Locations:** These can be names of Villages, Schools or Dams, or other such  places which correspond to Geographical locations in the real world.  
* **Location Types:** As its name suggests, Location Types are used to classify Locations into different categories. Ex: Karnataka and Maharashtra are 2 locations that could be classified into a single Location Type called “State”. Additional caveats related to the Location Type are as follows:  
  * You may associate a “Parent” Location Type for it, which would be instrumental in coming up with Location Type Hierarchy  
  * Each location type also has an additional field called “Level” associated with it. This is a Floating point number used to indicate relative position of a Location type in-comparison to others.   
  * There can be more than one location type with the same “Level” value in an organisation.  
  * The value for “Level” should less than the “Parent” Location Type’s “Level” field value  
* **Location Type Hierarchy:** Location types using the “Parent” field can construct a hierarchy of sorts. Ex:  State(3) \-\> District(2) \-\> City(1)\
  A single organisation can have **any** number of Location Type Hierarchies within it. Note that the example is a single hierarchy.  
* **Lineage:** Location Type hierarchy, are in-turn used to come up with Location lineage. Ex: Given a “Location Type Hierarchy” of State(3) \-\> District(2) \-\> City(1) being present, we could correspondingly create Location “Lineage” of the kind “Karnataka, Hassan, Girinagara”, where-in “Karnataka” corresponds to “State” Location-type, “Hassan” to “District” and “Girinagara” to “City”.

## Related Topics

<!-- Add links to related documentation -->


---
<!-- Source: 02-organization-setup/catchment-configuration.md -->

# Configuring Catchments in Avni

## TL;DR

A Catchment is a group of locations. Catchments are used to segregate areas of operation of each user (or group of users).

## Overview

A Catchment is a group of locations. Catchments are used to segregate areas of operation of each user (or group of users).

The field app will sync only data for the catchment assigned to the logged in user. By dividing into catchments, we ensure that the user has a smaller set of information to work with.

**Uploading catchments**
Catchments can also be created along with users in bulk using the [upload screen](/#/admin/upload).

[Learn more about Avni's domain model](https://avni.readme.io/docs/avnis-domain-model-of-field-based-work)

## Related Topics

<!-- Add links to related documentation -->


---
<!-- Source: 02-organization-setup/location-setup-csv.md -->

# Setting Up Locations via CSV Upload

## TL;DR

Below is a list of definitions that are essential for understanding this document.

## Definitions

Below is a list of definitions that are essential for understanding this document.

* **Locations:** These can be names of Villages, Schools or Dams, or other such  places which correspond to Geographical locations in the real world.  
* **Location Types:** As its name suggests, Location Types are used to classify Locations into different categories. Ex: Karnataka and Maharashtra are 2 locations that could be classified into a single Location Type called “State”. Additional caveats related to the Location Type are as follows:  
  * You may associate a “Parent” Location Type for it, which would be instrumental in coming up with Location Type Hierarchy  
  * Each location type also has an additional field called “Level” associated with it. This is a Floating point number used to indicate relative position of a Location type in-comparison to others.   
  * There can be more than one location type with the same “Level” value in an organisation.  
  * The value for “Level” should less than the “Parent” Location Type’s “Level” field value  
* **Location Type Hierarchy:** Location types using the “Parent” field can construct a hierarchy of sorts. Ex:  State(3) \-\> District(2) \-\> City(1)\
  A single organisation can have **any** number of Location Type Hierarchies within it. Note that the example is a single hierarchy.  
* **Lineage:** Location Type hierarchy, are in-turn used to come up with Location lineage. Ex: Given a “Location Type Hierarchy” of State(3) \-\> District(2) \-\> City(1) being present, we could correspondingly create Location “Lineage” of the kind “Karnataka, Hassan, Girinagara”, where-in “Karnataka” corresponds to “State” Location-type, “Hassan” to “District” and “Girinagara” to “City”.

## Overview

In Avni, Locations refer to geographical entities which could be a State, Village, Schools, Hospital, etc.. where an organisation provides services. It plays an important role in identifying the “Where” aspect of the data being captured / service that was provided. Locations are also used to group together Avni entities (Subjects, Encounters, GroupSubjects) based on their Geographical proximity, using the Catchments. This simplifies the assignment of Avni entities in the Geographical area of influence of a Field-Worker to him/her as a single composite entity rather than individually allocating each entity to the User.

Avni **“Upload\- Locations”** functionality, allows Avni Admin Users to perform following actions in **bulk**

* Create new locations   
* Update name, GPS coordinates and other properties for existing locations  
* Modify the parent location for an existing location and there-after reflect the change in lineage for it and all its children

This is achieved by means of uploading a CSV(Comma-separated Values) file of a specific format. Please read through the rest of the document to learn more about initializing Location Types and setting up large amounts of Locations for each of those types for specific Location Type Hierarchy.

## Steps to create Location Types Hierarchy

### Navigation to the Bulk Uploads screen

* Login to Avni Web Console 

![](https://files.readme.io/35932d9141d5744753f1730b6b5a4aa04a4b755a9fd18c25586ca98b58639177-image.png)

* Go to **Admin** app

![](https://files.readme.io/b51402bda3d8cf3a6aefd515b8e19cecc2c0200c5c557ae973cb38d3fa4e172e-image.png)

* Click on the **“Location Types”** section

![](https://files.readme.io/b846e3e44e146727fc20ad58b6c881cb8d2a96ac3dcdac90ae90f84b1fc81d2f-image.png)

### Create Location Types Hierarchy

When we start with creation of Location types, we do so from the highest Location type to the lowest in descending order of its level within the Location Hierarchy.

For example, to set up a Location Hierarchy of State(3) \-\> District(2) \-\> City(1), you would repeat the below process 3 times, first for “State”, then “District” and finally for “City”.

#### Create Location Type

1. Click on “CREATE” button on the top right corner, in “Location Types” screen  
2. Initialize “Name” field, to an appropriate String value starting with Upper-case Alphabet  
3. Initialize the “Level” field to appropriate Numeric value, which would be lower than its “Parent” Location Type’s “Level” value. Ex: “2.0”, “3”, “4.5”  
4. Associate “Parent” Location Type, as long as this isn’t the Highest Location type in its hierarchy  
5. Save the Location type, by clicking on the “SAVE” button

![](https://files.readme.io/2c1cb4ff350002b55cb86e570dc8f22baf8f5c5a1738bf1575def95eb6a7e1a3-image.png)

#### About Multiple Location Type Hierarchies within a single organization

Avni allows for an organization to have more than one Location hierarchy. The hierarchies could be linked at a specific location type or otherwise.

##### Example for Multiple Hierarchy joined at a common location type

![](https://files.readme.io/785775716ea75efb92621f34ebf17f014cb5f1b5a478a2c4e7d1ffff90e26b2a-image.png)

##### Example for Multiple Hierarchies not linked with each other

![](https://files.readme.io/4c530ae55ff631715c497aef020ef6591e2189c5df01b3bc034a34797acc6bc4-image.png)

### Review Location Types Hierarchy

Do a quick review of the Location Types Hierarchy, to ensure that its created as per requirement.

![](https://files.readme.io/6fccd280624ae8da4252f2bf7b3bb2bdb4950fabd5f7132f2820cc4849d6b628-image.png)

## Steps to create Form of type Locations (Optional)

For your organization, if there is a need to specify additional details as part of each Location, then Avni allows you to configure a “Location” type Form, which can be configured to store those additional details as Observations for each Location. This is an optional feature to be done only if such need arises.

* Navigate to the App Designer app

  ![](https://files.readme.io/45b6cf059a148183cb5597b2e09a93dc6d705c9af4eb09f99df0c9cdbd246050-image.png)
* Click on Forms in the left side tab, to open up the Forms section.  
* Create a new Form of type “Locations” by clicking on the “CREATE” button on the Top-Right corner of the screen.  

  ![](https://files.readme.io/2ad5b18293dfb28f217f3a87bd633dccb766d962a56c68f2c3fdb4b1611e6237-image.png)
* Setup the Locations type Form in the same way as you do for any other Avni Entity Data collection Forms. See below sample screenshot for reference.

  ![](https://files.readme.io/b5c2e8c75e8660ff5eaa3fba63826e1b2898aab32cf942beeec47d8cba11dd19-image.png)

## Steps to create Locations via CSV upload

### Prerequisites

* **Ensure Location Types Hierarchy already exists**\
  In order to start with the locations upload in the Avni app, organisation needs to have Location Types created in the requisite hierarchical order.  
* **Ensure Location Form if needed, has already been configured**\
  If your organisation needs additional properties to be set during Location creation, then ensure that you have configured a form of type “Locations” in the aforementioned manner 

### Navigation to the Bulk Uploads screen

* Login to Avni Web Console

![](https://files.readme.io/93db597e0607f374895d82942c940eca42ff9954f008e28fb2933b459a2bc280-image.png)

* Go to **Admin** app

![](https://files.readme.io/a0bfd4fcaa19d3275985307bdc624b89237c508ee94eb2a9f6a992c0f3d30348-image.png)

* Click on the **“Upload”** section

![](https://files.readme.io/81b9a7ec02dcba7ee588ceb2c4a6a508e9346610ef43e9b29c2c30ba0fb6b8fa-image.png)

### Download sample CSV file

In the Avni “Admin” app, “Upload” section, we provide the users with an option to download a sample file, which would give you a rough example for coming up with the required “Locations” upload CSV file.

The locations upload file format is different for the “Create” and “Edit” modes, therefore choose the appropriate mode and apply the same, when uploading the file later as well.

If your organization has multiple Location hierarchies, then you would have to select the specific location hierarchy for which you need the sample file. This is applicable only for “Create” mode.\
Finally, click on the “Download Sample” button, to get the sample file.

![](https://files.readme.io/31cbacad108b87cdd4a90ad196fbd4b879761676b333fe0cdfbd7baa6814f30c-image.png)

#### Sample Locations upload csv file screenshot

As part of the sample Locations csv file downloaded, you’ll have following information available to you for quick reference:

* All Headers configurable for the selected Mode and Location hierarchy  
* Descriptor row with guidance and examples on what values should be specified for each of the columns

1. **Create** mode

   ![](https://files.readme.io/00dc42970a69fea2eac1a114935cb3b2cbefe588aa540a5147cd51e7bdc930bc-image.png)
2. **Edit** mode

   ![](https://files.readme.io/42250968ba2ed5feec3e8da58e4c0521e1aa8bbe1418530de90a3f61a4eaf71f-image.png)

### Compose Locations upload CSV file

1. ### "Create" Mode

#### Headers Row

The first row of your upload file should contain Location types, arranged in descending order of their Level, in the selected Location Hierarchy from Left to Right, as comma-separated values.\
Refer Sample Locations Upload documents available [here](https://docs.google.com/spreadsheets/d/1R3l_tRUKZ7_WoZa4QIRctecFqJZoB2jdltyKUPMSD0Q/edit?usp=sharing) for Location Hierarchy of: Block(3) \-\> GP(2) \-\> Village/Hamlet(1). This is followed by “GPS Coordinates” and other Location properties name as column names.

![](https://files.readme.io/1a1dff92a0cb11f31704ee8f6d87ac78013ae49e56e8b878dc8657bb96762ece-image.png)

#### Descriptor Row

The second row of your upload file can optionally be a descriptor row, retained as is from the sample location upload file downloaded earlier. Avni would ignore the row, if its starting text matches the Sample file Descriptor row content’s starting text.

#### Data Rows

Entries provided in each of the address-level-type columns would be created as individual locations. (For example, the “Jawhar” block, “Sarsun” GP, and “Dehere” village will be created as a unique location with the appropriate location lineage, as specified during upload.)\
If the Parent locations already exists during a new location creation, then they are not re-created and are just used as is to build the location lineage.

#### GPS Coordinates

In-case, user would like to set the GPS Coordinates for locations during upload, then they would need to additionally specify values in the "GPS coordinates" column. The value for this column should be of the Format “\<Decimal number\>,\<Decimal number\>”.\
Ex: “123.456789,234.567890”, “12.34,45.67”, “13,77”

#### Additional Location Properties

Avni allows an organisation to configure Forms of Type “FormType.Location” for enabling inclusion of additional properties for each Location. These Forms are made up of the same building blocks of Pages and Questions like Forms of other types.

In-order to configure Location properties, you would need to specify the Concept “name” as the Column Header and specify the value for each of the locations in the corresponding columnar position.

![](https://files.readme.io/d779bbd3674a887c54b1f320d9e7cceb881b841f3360697f9d450c0bbf2795d1-image.png)

2. ### “Edit” Mode

This mode is to be used to perform bulk updates to locations. The type of updates allowed are as follows:

* Update name of existing locations  
* Update GPS coordinates and other properties for existing locations  
* Modify the parent location for an existing location and there-after reflect the change in lineage for it and all its children

#### Headers Row

The first row of your upload file, would usually contain following data as columns headers:

1. Location with full hierarchy  
2. New location name  
3. Parent location with full hierarchy  
4. GPS coordinates  
5. Multiple Location Properties name  

Refer Sample Locations Upload documents available [here](https://docs.google.com/spreadsheets/d/1EFpeMuQe-BEGvghUAeQWsLumfJ88B2Iv8w-lVqzQX4c/edit?usp=sharing).

![](https://files.readme.io/9d903fe0c5fe2d9d8fc93622312ef7e23efbc3fd6c2d811ade340d362c37db39-image.png)

#### Data Rows

Entries provided for the columns listed below would be used as specified here:

* Location with full hierarchy (Mandatory): Used to identify the specific location to be modified  
* New location name (Optional):  Used to specify the new title value for a location  
* Parent location with full hierarchy (Optional):  Used to identify the new parent location to move this location to. Ex: Move “Vil B” to “PHC C, Sub C” from “PHC B, Sub B”  
* GPS coordinates (Optional):  Used to update the GPS coordinates. Format:  “\<Double\>,\<Double\>”. Ex: “123.456789,234.567890”  
* Values for multiple Location Properties columns that are part of the Form of type “FormType.Location”. These again are optional.

#### Edit Row validations

1. If the “Location with full hierarchy” does not exist during location updation, then the update operation fails for that row.  
2. Atleast one among the following columns should have a valid value for the updation operation to be performed successfully for that row:  
   * New location name  
   * Parent location with full hierarchy  
   * GPS coordinates  

### Upload the CSV file

Project team then downloads the sheet in the CSV format. Navigate to the “**Upload”** tab of the Admin section, and perform the following steps to upload the file:

* Select the “Type” to be “Locations”   
* Specify the file to be uploaded using the “CHOOSE FILE” option  
* Select the appropriate “Mod&#x65;**”** of CSV Upload  
  * Create: For creating new locations  
  * Edit: For updating existing location’s Name, Parent, GPS coordinates or other properties  
* Choose appropriate “Location Hierarchy” (Applicable only for “Create” mode)  
* Click on the “Upload” button

![](https://files.readme.io/225211b913de07fb56c6a7676b1b6c88a78aecc2c92f97833c646b304b8ce6c4-image.png)

## Monitoring Progress of the Upload

Avni provides users with an easy way to monitor the progress of the CSV file uploads. In the same “Upload” tab of the Admin section, the bottom-half contains a list of all uploads triggered by users of the organization.

![](https://files.readme.io/ac1a32f7738e8035e5ad076005a218693044cfc7f00348d080bdd3a3e50d2d22-image.png)The “Status” column will indicate the overall status of the specific upload activity. With other columns like “Rows/File read” , “Rows/File completed” and “Rows/File skipped” indicating the Granular row-level progress of the file processing.

The final “Failure” column, will consist of Hyperlinks to Download an Error Information file, which would be present, only upon Erroneous completion of the upload activity.

![](https://files.readme.io/f38defc143785372fa7b8963c14e555d89eaa5feebe009aa7d55a20a40445bbf-image.png)

## Verification of Uploaded content

On successful upload of a file, the Project team can verify from the Locations tab in the “Admin” application, whether the uploaded content was indeed processed successfully as per requirement. Search for the newly created Locations and click on the same to view its details, to confirm that its created with exact configuration as intended.

![](https://files.readme.io/8457449146f1308efc4d6a9e690368dd3818a1ac9d78f329004771e7422d4fb7-image.png)

## Related Topics

<!-- Add links to related documentation -->


---
<!-- Source: 02-organization-setup/organization-creation.md -->

# Organization Creation

## TL;DR

Organization creation is typically done by Avni team. You'll receive admin credentials to configure your organization. Setup involves creating admin users, uploading configuration bundles, and setting up address hierarchy. Time: ~2 hours for basic setup.


## Overview

**What:** Creating a new Avni organization (tenant) on the platform.

**Who does it:** Usually Avni team (requires super admin access).

**What you do:** Configure the organization after creation (users, locations, forms).

**Prerequisites:**
- Organization name and details
- Configuration bundle (forms, programs)
- Admin user details


## Creation Steps (Super Admin)

### Step 1: Create Organization
1. Login as Super Admin at `https://app.avniproject.org/`
2. Navigate to **Admin** → **Organisations**
3. Click **+ Create Organisation**
4. Fill in details:
   - **Name**: Organization name (e.g., "MLD Trust")
   - **DB User**: Lowercase, no spaces (e.g., "mld_trust")
   - **Schema Name**: Same as DB User
   - **Media Directory**: Same as DB User

### Step 2: Create Admin User
1. Navigate to **Users** in the new org
2. Create first admin user:
   - **Username**: `admin@orgname`
   - **Name**: Admin full name
   - **Email**: Admin email
   - **Admin**: ✓ Checked
   - **Operating Scope**: "By Catchment"

### Step 3: Configure Organization Settings
Navigate to **Settings** → **Organisation Config**:
```json
{
  "enableComments": true,
  "enableOfflineDashboard": true,
  "searchFilters": ["Name", "Address"]
}
```

### Step 4: Upload Configuration Bundle
Upload files in order:
1. `addressLevelTypes.json`
2. `locationHierarchy.json`
3. `subjectTypes.json`
4. `programs.json`
5. `encounterTypes.json`
6. `concepts.json`
7. All files in `forms/`
8. `formMappings.json`


## Post-Creation Setup (Implementer)

After receiving admin credentials:

### 1. Verify Access
- Login to admin portal
- Confirm organization appears
- Check subject types and programs loaded

### 2. Set Up Address Hierarchy
- Define location levels
- Upload locations
- See [Address Hierarchy](address-hierarchy.md)

### 3. Create Users
- Field workers
- Supervisors
- Data managers
- See [User Management](user-management.md)

### 4. Configure Catchments
- Group locations
- Assign to users
- See [Catchment Configuration](catchment-configuration.md)

### 5. Test Setup
- Register test subject
- Complete test encounter
- Verify sync works


## Common Issues

### Organization Not Found
**Symptoms:** Can't see organization in dropdown

**Causes:**
- DB user spelling incorrect
- Cache not refreshed

**Solutions:**
- Wait 5 minutes for cache
- Contact Avni support if persists

---

### User Sync Failed
**Symptoms:** Mobile app sync fails for new user

**Causes:**
- No catchment assigned
- User is voided

**Solutions:**
- Assign catchment to user
- Check user is active (not voided)

---

### Forms Not Loading
**Symptoms:** Forms don't appear in app

**Causes:**
- Upload order incorrect
- Concept UUID mismatches
- Form mapping missing

**Solutions:**
- Re-upload in correct order
- Verify concept UUIDs match
- Check formMappings.json


## Setup Checklist

### Organization Creation
- [ ] Organization created by Avni team
- [ ] Admin user created
- [ ] Admin can login
- [ ] Organization config set

### Configuration Upload
- [ ] Address level types uploaded
- [ ] Subject types uploaded
- [ ] Programs uploaded
- [ ] Encounter types uploaded
- [ ] Concepts uploaded
- [ ] Forms uploaded
- [ ] Form mappings uploaded

### Basic Setup
- [ ] Address hierarchy defined
- [ ] Locations uploaded
- [ ] First catchment created
- [ ] First field user created
- [ ] User assigned to catchment

### Verification
- [ ] Can register test subject
- [ ] Can enroll in program
- [ ] Can complete encounter
- [ ] Mobile app syncs successfully


---

**Navigation:**  
[← Back to Organization Setup](README.md) | [Next: Address Hierarchy →](address-hierarchy.md)


---
<!-- Source: 02-organization-setup/user-groups-privileges.md -->

# User Groups and Privileges in Avni

## TL;DR

Avni users can be grouped into different Users Groups based on their roles and responsibilities and different permissions can be given to them. It ensures that users have the right access levels to perform their tasks effectively while maintaining data integrity:

## Overview

### Why are User Groups needed?

Avni users can be grouped into different Users Groups based on their roles and responsibilities and different permissions can be given to them. It ensures that users have the right access levels to perform their tasks effectively while maintaining data integrity:

1. **Role-based Access Control:** User groups ensure each user gets permissions suited to their role. For example, field workers, supervisors, and administrators may need different access levels.
2. **Permission Management:**  Instead of setting permissions individually, administrators can manage them for entire groups, reducing errors and saving time.
3. **Enhanced Security:** User groups help to  define which group can access certain data or perform certain activities in the Avni app like registration, enrolments, edits, and canceling the visit. This 
4. **Customization and Flexibility:** User groups allow for tailored permissions based on specific user roles. A user can have multiple user groups assigned based on their area of work. 
5. **Scalability:** As organizations grow, user groups can adapt to changes in roles and responsibilities, keeping the app aligned with evolving needs.

### Special kind of User Groups

There are 2 User Groups that are automatically created when an Organisation is created. They are:

1. **Everyone**: Default group to which all Users of an Org will always belong to.
2. **Administrators**: A group which would always have all privileges.

### Steps to Create User Groups:

Before creating Users & Catchment, the first step is to create User Groups. Different user groups can have different permissions depending on the roles and responsibilities. Eg. in a project, there are Field Workers who would be using the Avni app, we can create a user group called “Field Workers”

1. **Login to Avni Web Console**

![](https://files.readme.io/ced1805-image4.png)

2. **Go to Admin**

![](https://files.readme.io/172d1bf-image2.png)

3. **Click on User Groups:**

![](https://files.readme.io/6575689-image6.png)

4. **Click on Create Group**\
   Enter the Group name and click on the CREATE NEW GROUP button

![](https://files.readme.io/bb4854b-image5.png)

![](https://files.readme.io/f04a374-image8.png)

5. **Configure Group Users** By clicking on the respective user group, the list of users who are part of the user group is shown along with the permissions given to the user group. User group will show the list of users who are part of this user group along with the user id and registered email.

![](https://files.readme.io/22984c4-image7.png)

6. **Configure Group Permissions:** The permissions section contains a list of permissions which are grouped by subject/entity type. When a subject/entity type is expanded, it will display permissions specific to the subject/entity type like edit, view, perform visit, schedule visit, void any visit or subject registration, cancel visit.

![](https://files.readme.io/1ca8b52-image10.png)

![](https://files.readme.io/2a71433-image9.png)

As shown in the screenshot below, “all privileges” will provide all the permissions and accesses to the entire user group.

When a user is assigned to 2 or more user groups, the union of permissions provided to the assigned user groups will be accessible. (For example, edit access permissions disabled for a form  in one user group and enabled in another user group will allow the user to edit that form)

![](https://files.readme.io/7636af7-image11.png)

7. **Configure Group Dashboards:** This section in user groups allows users to add and provide permission to access the dashboard in the mobile app. Here multiple dashboards added to the user groups will be synced as per the user groups assigned to the user. Out of the dashboards added, primary and secondary dashboards can be defined which would be shown on the user’s mobile screen immediately after logging in. (Refer to the screenshot below)

![](https://files.readme.io/0540e63-image3.png)

Refer to Offline Report Cards and Custom Dashboards section for more details regarding this.

### Assign User Groups while creating Users

Once the user groups are updated with the necessary details given above, it should be used while creating users via the Admin -> Users screen.

![](https://files.readme.io/5ea372d-image1.png)


User Groups can be created to finely control user access to functions in the field and data entry apps.

By default, no configuration is required here as there is already an Everyone group that has all privileges.

[Learn more about Access Control and User Groups](https://avni.readme.io/docs/access-control)

## Related Topics

<!-- Add links to related documentation -->


---
<!-- Source: 02-organization-setup/user-management.md -->

# User Management in Avni

## TL;DR

To access the features of the Avni app, users need to have a unique username and password to log in to the app and perform the activities as and when required. These login credentials can be created through Avni web-app where certain permission can be provided to each unique user as per the area ...

## How to guide: Creating Users and Catchments from the Avni web-app

To access the features of the Avni app, users need to have a unique username and password to log in to the app and perform the activities as and when required. These login credentials can be created through Avni web-app where certain permission can be provided to each unique user as per the area of work and authority to access the data generated in the app.

### Prerequisites before creating the users:

The following items must be configured in the web app before proceeding with the user creation process.

1. Location Hierarchy, Locations ([Refer to this guide \[TO BE ADDED\]]())
2. Languages
3. User Groups ([Refer to this guide](https://avni.readme.io/docs/user-groups))
4. Catchments

### Creating Catchments:

A catchment is a group of locations that are serviced by a user i.e. the locations that a user works in. Only data captured against the locations within the catchments assigned to the user are synced to the android app of the user. The following steps can be followed to create catchments in the web app:

1. Navigate to the admin console

![alt_text](https://files.readme.io/d32ed8d-image8.png "image_tooltip")

2. Click on the catchments and create a catchment

![](https://files.readme.io/8c7e39e-image2.png)


3. Provide a unique name for the catchment in the field given below.

![](https://files.readme.io/537772e-image7.png)


4. Add the locations which are to be part of the catchment.

![](https://files.readme.io/4220102-image11.png)


### Creating Users:

Once the above-provided prerequisites have been created successfully, we can proceed with the user creation process.

1. Navigate to the admin console in the Avni web app.

![](https://files.readme.io/d32ed8d-image8.png)


2. Click on the Users section and Create button as given below.

![](https://files.readme.io/a60ebcd-image9.png)


3. Provide a unique Login ID for each user. Login ID allows to have alphanumeric values which will be followed by @ProjectName. A Login ID that is already in use cannot be re-used to create another user. **Note:** The login name is a case-sensitive field. The user needs to provide the same login ID while logging in to the Avni app.

![](https://files.readme.io/18b704a-image4.png)


4. While creating a user, the administrator can provide a custom password by clicking on the toggle button highlighted below. This would populate two additional fields to enter a custom password and verify it by giving the same password again. 

![](https://files.readme.io/ee06b59-image3.png)


5. In case the custom password toggle button is not on, the system will continue with creating the default password. The default password would have the first four letters of the username followed by the last four digits of the mobile number provided while creating the user.
6. Provide the full name of the user along with mobile number and email address. The same mobile number and email can be used multiple times to create different users.

![](https://files.readme.io/6185872-image5.png)


7. Catchment created as given in this guide can be set here while creating the user. The system doesn’t allow to assign more than one catchment per user.

![](https://files.readme.io/ef2a51f-image10.png)


8. Set user groups as per the operational roles of the user. Multiple user groups can be assigned to a user. 

![](https://files.readme.io/511929c-image6.png)


9. Further settings specific to the user can be setup to customise the user experience 

   1. Preferred Language
   2. Track location - Switches on visit location tracking on the Field App
   3. Beneficiary mode - Enables the Beneficiary mode - a limited mode that allows beneficiaries to use the Field App
   4. Disable dashboard auto refresh - Disables Auto-refresh of MyDashboard of the Field App. Use if the dashboard is slow to refresh
   5. Disable auto sync - Disables automatic background sync. Use it if you want to trigger sync only manually
   6. Register + Enrol - Adds extra quick menu items on the Register tab to register and enrol to programs in a single flow
   7. Enable Call Masking - Enables Exotel call masking for the user
   8. Identifier Prefix - Identifier prefix for ids generated for this user. See[ documentation](https://avni.readme.io/docs/creating-identifiers) for more information
   9. Date Picker Mode - Set default date picker for the Field App
   10. Time Picker Mode - Set default time picker for the Field App

   ![](https://files.readme.io/a73b680-image1.png)

   


Logins for Avni. Users will get their first login details on email and SMS.

Ensure that you have created catchments for your users before creating them. Users can be created either through the [Users screen](/#/admin/user) or through the [upload screen](/#/admin/upload).

Users can be created or disabled. Disabled users cannot login. In case of password issues, the field application has the capability to reset passwords.

[Learn more about Users](https://avni.readme.io/docs/access-control)

## Related Topics

<!-- Add links to related documentation -->


================================================================================
# Section: Concepts And Forms
================================================================================


---
<!-- Source: 03-concepts-and-forms/README.md -->

# Concepts and Forms - Avni Configuration

Everything about defining concepts (data fields) and building forms for data collection in Avni.

## Contents

### 1. [Concept Types and Data Types in Avni](concept-types.md)
concept types  data types  numeric  coded

### 2. [Creating and Managing Concepts in Avni](concept-management.md)
concept creation  concept reuse  naming conventions  concept management

### 3. [Form Structure and Design in Avni](form-structure.md)
form structure  form elements  form groups  form mapping

### 4. [Form Design Patterns and Best Practices](form-design-patterns.md)
form design  skip logic  mandatory fields  conditional fields

### 5. [Form Element Types and Configuration](form-element-types.md)
form elements  field types  question types  form configuration

### 6. [Adding Documentation to Forms](form-documentation.md)
form documentation  help text  in-form documentation  form instructions

### 7. [Repeatable Question Groups in Avni](repeatable-question-groups.md)
repeatable question group  question group  repeatable fields  grouped questions

### 8. [Multi-Language Forms and Translation Management](multi-language-forms.md)
translation  multi-language  localization  language support

### 9. [Using Media in Forms (Images, Video, Audio)](media-in-forms.md)
media  images  video  audio


---
<!-- Source: 03-concepts-and-forms/concept-management.md -->

# Creating and Managing Concepts in Avni

## TL;DR

Concepts define the different pieces of information that you collect as part of your service delivery.

## Overview

Concepts define the different pieces of information that you collect as part of your service delivery.

For example, if you collect the blood pressure of a subject in a form, then "Blood Pressure" should be defined as a concept. You would notice that every question in a form requires a concept

- [More information about concepts](https://avni.readme.io/docs/concepts)
- [Learn more about Avni's domain model](https://avni.readme.io/docs/avnis-domain-model-of-field-based-work)

## Related Topics

<!-- Add links to related documentation -->


---
<!-- Source: 03-concepts-and-forms/concept-types.md -->

# Concept Types and Data Types in Avni

## TL;DR

**Concepts** define the different pieces of information that you collect as part of your service delivery.

## Overview

**Concepts** define the different pieces of information that you collect as part of your service delivery.  

For example, if you collect the blood pressure of a subject in a form, then "*Blood Pressure*" should be defined as a concept. You would notice that every question in a form requires a concept.  

The *datatype* of a concept determines the kind of data can be stored against a concept, and therefor against the form question or form element. Using concepts with datatypes ensures incorrect answers are not captured in a form question, and is helpful for eventually data aggregation, validation and reporting.

## Supported DataTypes in Concepts

The following datatypes are supported while defining concepts to be used in forms:


  <thead>
    <tr>
      <th>
        Concept DataType
      </th>

      <th>
        Description
      </th>
    </tr>
  </thead>

  <tbody>
    <tr>
      <td>
        * Numeric_ **concepts** 
      </td>

      <td>
        Numeric concepts are used to capture numbers. When creating a numeric concept, you can define normal ranges and absolute ranges. In the field application, if an observation for a concept collected goes beyond the normal range, then it is highlighted in red. Values above the absolute range are not allowed.  For instance for concept: Blood Pressure (Systolic), you can choose a Numeric concept with ranges.
      </td>
    </tr>

    <tr>
      <td>
        **Coded concepts (and NA concepts)** 
      </td>

      <td>
        Coded concepts are those that have a fixed set of answers. For instance for Blood Group you would choose a coded concept with values: A+, B+, AB+, etc.  

        These answers are also defined as concepts of NA datatype.
      </td>
    </tr>

    <tr>
      <td>
        **ID datatype** 
      </td>

      <td>
        A concept of Id datatype is used to store autogenerated ids. See Creating identifiers for more information on creating autogenerated ids.  For instance PatientIDs, TestIDs, etc.
      </td>
    </tr>

    <tr>
      <td>
        **Media concepts (Image, Video and Audio)**
      </td>

      <td>
        Images and videos can be captured using Image and Video concept datatypes. For audio recording, Audio datatype can be used.
      </td>
    </tr>

    <tr>
      <td>
        **Text (and Notes) concepts** 
      </td>

      <td>
        The *Text* data type helps capture one-line text while the *Notes* datatype is used to capture longer **form** text.
      </td>
    </tr>

    <tr>
      <td>
        **Date and time concepts**
      </td>

      <td>
        There are different datatypes that can be used to capture date and time.  

        * \*Date\*\* - A simple date with no time  
        * \*Time\*\* - Just the time of day, with no date  
        * \*DateTime\*\* - To store both date and time in a single observation  
        * \*Duration\*\* - To capture durations such as 4 weeks, 2 days etc.
      </td>
    </tr>

    <tr>
      <td>
        **Location concepts**
      </td>

      <td>
        * Location_ concepts can be used to capture locations based on the location types configured in your implementation.  

        Location concepts have 3 attributes:  

        1. Within Catchment - Denotes whether the location to be captured would be within the catchment already assigned to your field workers. This attribute defaults to true and is mandatory.

        2. Lowest Level(s) - Denotes the lowest location type(s) you intend to capture via form elements using this concept. This attribute is mandatory.

        3. Highest Level - Denotes the highest location type that you would like to capture via form elements using this concept. This attribute is optional.
      </td>
    </tr>

    <tr>
      <td>
        **Subject concepts**
      </td>

      <td>
        * Subject_ concepts can be used to link to other subjects.  

        Each Subject concept can map to a single subject type.  

        Any form element using this concept can capture one or multiple subjects of the specified subject type.
      </td>
    </tr>

    <tr>
      <td>
        **Phone Number concepts**
      </td>

      <td>
        For capturing the phone number. It comes with a 10 digit validation. OTP verification can be enabled by turning on the "Switch on Verification" option. Avni uses msg91 for OTP messages, so msg91 `Auth key` and `Template` need to be step up using the admin app.
      </td>
    </tr>

    <tr>
      <td>
        **Group Affiliation concepts** 
      </td>

      <td>
        Whenever automatic addition of a subject to a group is required  Group Affiliation concept can be used. It provides the list of all the group subjects in the form and choosing any group will add that subject to that group when the form is saved.
      </td>
    </tr>

    <tr>
      <td>
        **Encounter** 
      </td>

      <td>
        * Encounter_ concepts can be used to link an encounter to any form.  

        Each Encounter concept can map to a single encounter type.  It should also provide the scope to search that encounter. Also, name identifiers can be constructed by specifying the concepts used in the encounter form.  

        Any form element using this concept can capture one or multiple encounters of the specified encounter type.
      </td>
    </tr>
  </tbody>

## Showing counselling points in Forms

For showing counselling points in a form, always create a Form Element, using below coded Concept:

* Concept UUID: b4e5a662-97bf-4846-b9b7-9baeab4d89c4
* Concept Name: Placeholder for counselling form element
* Answers: \<None, no answers, to avoid showing them any options>

Specify counselling point as the Form Element Name, add numbering if needed.

Note: **You can reuse the same "Placeholder for counselling form element" multiple times in a single form**, without worrying about uniqueness constraint breach concerns.

## What types of data fields are supported in Avni?

Concept DataType - Description
Numeric concepts - Numeric concepts are used to capture numbers. When creating a numeric concept, you can define normal ranges and absolute ranges. In the field application, if an observation for a concept collected goes beyond the normal range, then it is highlighted in red. Values above the absolute range are not allowed. For instance for concept: Blood Pressure (Systolic), you can choose a Numeric concept with ranges.

Coded concepts (and NA concepts) - Coded concepts are those that have a fixed set of answers. For instance for Blood Group you would choose a coded concept with values: A+, B+, AB+, etc.

These answers are also defined as concepts of NA datatype.

ID datatype - A concept of Id datatype is used to store autogenerated ids. See Creating identifiers for more information on creating autogenerated ids. For instance PatientIDs, TestIDs, etc.

Media concepts (Image, Video and Audio) - Images and videos can be captured using Image and Video concept datatypes. For audio recording, Audio datatype can be used.

Text (and Notes) concepts - The Text data type helps capture one-line text while the Notes datatype is used to capture longer form text.

Date and time concepts - There are different datatypes that can be used to capture date and time.
*Date** - A simple date with no time
*Time** - Just the time of day, with no date
*DateTime** - To store both date and time in a single observation
*Duration** - To capture durations such as 4 weeks, 2 days etc.
Location concepts - Location concepts can be used to capture locations based on the location types configured in your implementation.
Location concepts have 3 attributes:
- Within Catchment - Denotes whether the location to be captured would be within the catchment already assigned to your field workers. This attribute defaults to true and is mandatory.
- Lowest Level(s) - Denotes the lowest location type(s) you intend to capture via form elements using this concept. This attribute is mandatory.
- Highest Level - Denotes the highest location type that you would like to capture via form elements using this concept. This attribute is optional.
Subject concepts - Subject concepts can be used to link to other subjects. Each Subject concept can map to a single subject type. Any form element using this concept can capture one or multiple subjects of the specified subject type.
Phone Number concepts - For capturing the phone number. It comes with a 10 digit validation. OTP verification can be enabled by turning on the "Switch on Verification" option. Avni uses msg91 for OTP messages, so msg91 Auth key and Template need to be step up using the admin app.

## Related Topics

<!-- Add links to related documentation -->


---
<!-- Source: 03-concepts-and-forms/form-design-patterns.md -->

# Form Design Patterns and Best Practices

## TL;DR

Fields can be added to forms through the App Designer. You can reach the form through different means.

## How do I add or remove a new field to an existing form?

Fields can be added to forms through the App Designer. You can reach the form through different means.
1. Go to App Designer > Forms > Select the form
2. Go to App Designer > Subject Types, Programs or Encounter Types > Select the form you need to edit
3. Navigate to the section/page you wish to add the field to. If required, add a new section/page As you hover over the left portion, you will see a + button. Click on it to add a new field.
Each Form field has a few components.
1. Question - This is what shows up in your form
2. Concept - This is the internal name of the field. It is also shown in patient dashboards, reports etc. Normally, we keep the name of the concept to be the same as the question. Remember that there can only be one concept with a certain name in the entire system. Also, a concept can be used only once in a form. Based on the data type of the concept, you will have a few questions to answer to configure it correctly.
3. Rule - There are three rules that you can configure for a question -
1. Show/Hide question - This is used to show or hide the question based on a certain condition.
2. Validation Rule - Based on conditions, you might show an error to the user
3. Value Rule - Based on conditions, you might set an answer value
The rules section is available by clicking on "RULE" section on the left side of the question

## Frequently Asked Questions

### Q: What types of data fields are supported in Avni?

Concept DataType - Description
Numeric concepts - Numeric concepts are used to capture numbers. When creating a numeric concept, you can define normal ranges and absolute ranges. In the field application, if an observation for a concept collected goes beyond the normal range, then it is highlighted in red. Values above the absolute range are not allowed. For instance for concept: Blood Pressure (Systolic), you can choose a Numeric concept with ranges.

Coded concepts (and NA concepts) - Coded concepts are those that have a fixed set of answers. For instance for Blood Group you would choose a coded concept with values: A+, B+, AB+, etc.

These answers are also defined as concepts of NA datatype.

ID datatype - A concept of Id datatype is used to store autogenerated ids. See Creating identifiers for more information on creating autogenerated ids. For instance PatientIDs, TestIDs, etc.

Media concepts (Image, Video and Audio) - Images and videos can be captured using Image and Video concept datatypes. For audio recording, Audio datatype can be used.

Text (and Notes) concepts - The Text data type helps capture one-line text while the Notes datatype is used to capture longer form text.

Date and time concepts - There are different datatypes that can be used to capture date and time.
*Date** - A simple date with no time
*Time** - Just the time of day, with no date
*DateTime** - To store both date and time in a single observation
*Duration** - To capture durations such as 4 weeks, 2 days etc.
Location concepts - Location concepts can be used to capture locations based on the location types configured in your implementation.
Location concepts have 3 attributes:
- Within Catchment - Denotes whether the location to be captured would be within the catchment already assigned to your field workers. This attribute defaults to true and is mandatory.
- Lowest Level(s) - Denotes the lowest location type(s) you intend to capture via form elements using this concept. This attribute is mandatory.
- Highest Level - Denotes the highest location type that you would like to capture via form elements using this concept. This attribute is optional.
Subject concepts - Subject concepts can be used to link to other subjects. Each Subject concept can map to a single subject type. Any form element using this concept can capture one or multiple subjects of the specified subject type.
Phone Number concepts - For capturing the phone number. It comes with a 10 digit validation. OTP verification can be enabled by turning on the "Switch on Verification" option. Avni uses msg91 for OTP messages, so msg91 Auth key and Template need to be step up using the admin app.
Group Affiliation concepts - Whenever automatic addition of a subject to a group is required Group Affiliation concept can be used. It provides the list of all the group subjects in the form and choosing any group will add that subject to that group when the form is saved.
Encounter - Encounter concepts can be used to link an encounter to any form. Each Encounter concept can map to a single encounter type. It should also provide the scope to search that encounter. Also, name identifiers can be constructed by specifying the concepts used in the encounter form. Any form element using this concept can capture one or multiple encounters of the specified encounter type.

### Q: How can I configure skip logic between form fields?

Skip logic is implemented through rules in Avni. Every field on the Form Designer has a "Rule" section. You can configure skip logic by adding the logic and then clicking on "Show/Hide question".

### Q: How do I make a question appear only if another answer is “Yes”?

This can be achieved by adding skip logic rule on the form fields

### Q: How do I mark a field as mandatory?

In the form designer, go to the field you want to mark as mandatory. Check the box, and it will be shown as mandatory.
Remember that a field is mandatory only if it is visible. If you have created a visibility rule through which your form field is not visible, then the mandatory field on it will not be respected.

### Q: How can I model seasonal data collection (e.g., crops)?

Modeling Seasonal Data Collection (e.g., Crops) in Avni

1.Schedule Forms at Predefined Times

In Avni, forms can be scheduled to appear at specific times of the year using predefined scheduling rules or logic.

This allows you to capture seasonal crop information at the right time for each subject (e.g., farm, field).

2. Use Conditional Logic for Fields

If the same form is used across seasons, you can hide or show fields dynamically based on:

Season

Crop type

Other user input or data logic

This ensures that only relevant information is captured during each season.

Multiple approaches in Avni allow flexible and accurate collection of seasonal data without creating separate forms for each season.

### Q: How do I create a rule for conditional program enrollment?

In Avni, conditional program enrollment can be handled using the Enrolment Eligibility Check Rule available under program configuration. You can add a custom rule here to define the eligibility criteria for a subject. When an individual does not meet the defined conditions, the option to enroll them in that program will not appear on their profile.

### Q: How do I migrate data from another system into Avni?

Avni provides comprehensive bulk data upload functionality through the Admin web console:

- **Supported uploads:**
  - Subjects (individuals/entities)
  - Program enrollments 
  - Program encounters
  - General encounters
  - Locations and catchments
  - Users and their catchments

- **Process:** Download sample CSV templates from the Admin interface, fill with your data, and upload
- **Validation:** Basic level of form validations and rules executions are done during upload - mandatory fields are enforced, hidden fields are ignored based on form element rules
- **Automated processing:** Visit schedules and decisions are automatically created based on your configured logic

### Q: How do I make a yes/no field mandatory?

Yes. It can be done by setting Concept type = Coded, Data type = Single Select (Yes/No), and marking it as Required.

### Q: How do I enable conditional skip logic across sections?

You can implement conditional skip logic either by manually writing a rule or by using the Rule Builder. To do this, go to App Designer, then create a new form or open an existing form. You will find the Rule option next to Details, where you can define the skip logic as needed.

### Q: How do I model a program for chronic disease management?

1. Create a Subject Type

Go to Webapp → App Designer → Subject Types → Create New.

Give it a name like Person or Individual.

Select Person from the subject type dropdown.

On save, a default registration form is created.

This form already includes first name, last name, age, gender, and location. You can add more fields as needed.

2.Create a Program

Go to Webapp → App Designer → Programs → Create New.

Name it Chronic Disease.

On save, Avni automatically creates an Enrolment Form and an Exit Form.

3 Create Encounters

Go to Webapp → App Designer → Encounters → Create New.

Select your program (Chronic Disease).

Give the encounter a name.

Avni automatically creates and maps the form for this encounter.

Customize Forms

Go to Forms and edit the Registration, Enrolment, Exit, and Encounter forms.

Add fields, rules, and logic as per your requirements.

## Related Topics

<!-- Add links to related documentation -->


---
<!-- Source: 03-concepts-and-forms/form-documentation.md -->

# Adding Documentation to Forms

## TL;DR

Custom documentation can be created in Avni. Documentation supports rich text and can be written in different\
languages supported by an organization.

## Overview

Custom documentation can be created in Avni. Documentation supports rich text and can be written in different\
languages supported by an organization. Right now you can also link particular documentation to a form element and it'll show up in the mobile app. This is useful where more context is required for any question.

## Steps to configure and link documentation

The below GIF displays how documentation can be created and linked to a form element.

![Configuring and linking documentation](https://files.readme.io/d2a237f-Documentation-linking.gif)

Once documentation is linked to the form element, it'll start appearing in the mobile app. Users can expand and close the documentation while filling out the form.

![Documentation on the mobile app.](https://files.readme.io/542e811-form-element-documentation.png)


You can create documentation for the app. Currently documentation can be attached to a form element.

## Related Topics

<!-- Add links to related documentation -->


---
<!-- Source: 03-concepts-and-forms/form-element-types.md -->

# Form Element Types and Configuration

## TL;DR

Concept DataType - Description
Numeric concepts - Numeric concepts are used to capture numbers. When creating a numeric concept, you can define normal ranges and absolute ranges.

## What types of data fields are supported in Avni?

Concept DataType - Description
Numeric concepts - Numeric concepts are used to capture numbers. When creating a numeric concept, you can define normal ranges and absolute ranges. In the field application, if an observation for a concept collected goes beyond the normal range, then it is highlighted in red. Values above the absolute range are not allowed. For instance for concept: Blood Pressure (Systolic), you can choose a Numeric concept with ranges.

Coded concepts (and NA concepts) - Coded concepts are those that have a fixed set of answers. For instance for Blood Group you would choose a coded concept with values: A+, B+, AB+, etc.

These answers are also defined as concepts of NA datatype.

ID datatype - A concept of Id datatype is used to store autogenerated ids. See Creating identifiers for more information on creating autogenerated ids. For instance PatientIDs, TestIDs, etc.

Media concepts (Image, Video and Audio) - Images and videos can be captured using Image and Video concept datatypes. For audio recording, Audio datatype can be used.

Text (and Notes) concepts - The Text data type helps capture one-line text while the Notes datatype is used to capture longer form text.

Date and time concepts - There are different datatypes that can be used to capture date and time.
*Date** - A simple date with no time
*Time** - Just the time of day, with no date
*DateTime** - To store both date and time in a single observation
*Duration** - To capture durations such as 4 weeks, 2 days etc.
Location concepts - Location concepts can be used to capture locations based on the location types configured in your implementation.
Location concepts have 3 attributes:
- Within Catchment - Denotes whether the location to be captured would be within the catchment already assigned to your field workers. This attribute defaults to true and is mandatory.
- Lowest Level(s) - Denotes the lowest location type(s) you intend to capture via form elements using this concept. This attribute is mandatory.
- Highest Level - Denotes the highest location type that you would like to capture via form elements using this concept. This attribute is optional.
Subject concepts - Subject concepts can be used to link to other subjects. Each Subject concept can map to a single subject type. Any form element using this concept can capture one or multiple subjects of the specified subject type.
Phone Number concepts - For capturing the phone number. It comes with a 10 digit validation. OTP verification can be enabled by turning on the "Switch on Verification" option. Avni uses msg91 for OTP messages, so msg91 Auth key and Template need to be step up using the admin app.

## Frequently Asked Questions

### Q: What types of data fields are supported in Avni?

Concept DataType - Description
Numeric concepts - Numeric concepts are used to capture numbers. When creating a numeric concept, you can define normal ranges and absolute ranges. In the field application, if an observation for a concept collected goes beyond the normal range, then it is highlighted in red. Values above the absolute range are not allowed. For instance for concept: Blood Pressure (Systolic), you can choose a Numeric concept with ranges.

Coded concepts (and NA concepts) - Coded concepts are those that have a fixed set of answers. For instance for Blood Group you would choose a coded concept with values: A+, B+, AB+, etc.

These answers are also defined as concepts of NA datatype.

ID datatype - A concept of Id datatype is used to store autogenerated ids. See Creating identifiers for more information on creating autogenerated ids. For instance PatientIDs, TestIDs, etc.

Media concepts (Image, Video and Audio) - Images and videos can be captured using Image and Video concept datatypes. For audio recording, Audio datatype can be used.

Text (and Notes) concepts - The Text data type helps capture one-line text while the Notes datatype is used to capture longer form text.

Date and time concepts - There are different datatypes that can be used to capture date and time.
*Date** - A simple date with no time
*Time** - Just the time of day, with no date
*DateTime** - To store both date and time in a single observation
*Duration** - To capture durations such as 4 weeks, 2 days etc.
Location concepts - Location concepts can be used to capture locations based on the location types configured in your implementation.
Location concepts have 3 attributes:
- Within Catchment - Denotes whether the location to be captured would be within the catchment already assigned to your field workers. This attribute defaults to true and is mandatory.
- Lowest Level(s) - Denotes the lowest location type(s) you intend to capture via form elements using this concept. This attribute is mandatory.
- Highest Level - Denotes the highest location type that you would like to capture via form elements using this concept. This attribute is optional.
Subject concepts - Subject concepts can be used to link to other subjects. Each Subject concept can map to a single subject type. Any form element using this concept can capture one or multiple subjects of the specified subject type.
Phone Number concepts - For capturing the phone number. It comes with a 10 digit validation. OTP verification can be enabled by turning on the "Switch on Verification" option. Avni uses msg91 for OTP messages, so msg91 Auth key and Template need to be step up using the admin app.
Group Affiliation concepts - Whenever automatic addition of a subject to a group is required Group Affiliation concept can be used. It provides the list of all the group subjects in the form and choosing any group will add that subject to that group when the form is saved.
Encounter - Encounter concepts can be used to link an encounter to any form. Each Encounter concept can map to a single encounter type. It should also provide the scope to search that encounter. Also, name identifiers can be constructed by specifying the concepts used in the encounter form. Any form element using this concept can capture one or multiple encounters of the specified encounter type.

### Q: How can I make a numeric field accept only integers?

By applying a validation rule on that particular numeric field

### Q: How do I design a workflow for maternal health tracking?

Maternal Health / Pregnancy Workflow in Avni
1. Create the Subject

Type: Person

Purpose: Represents the pregnant woman whose health is being tracked.

2. Registration Form

Contains: Basic personal and demographic details.

Captured once at the time of creating the subject.

3. Configure the Program

Program Name: Pregnancy / Maternal Health

Program Components:

Enrolment Form

Captures one-time pregnancy details:

Last Menstrual Period (LMP)

Expected Delivery Date (EDD)

Height, weight

Previous pregnancy details

ANC (Antenatal Care) Forms

Scheduled automatically based on LMP date.

Tracks visits, vitals, investigations, and interventions during pregnancy.

Delivery Form

Captures delivery details, mode of delivery, complications, birth outcomes.

PNC (Postnatal Care) Forms

Scheduled after delivery.

Tracks maternal and newborn health.

Exit Form

Marks the completion of the program for that subject.

4. Scheduling

All ANC and PNC visits are scheduled based on the LMP or delivery date.

Reminders and follow-ups can be set automatically.

5. Data Flow

Subject created → registration form filled

Subject enrolled into Pregnancy Program → enrolment form captures one-time pregnancy details

ANC visits tracked and scheduled automatically

Delivery recorded → triggers PNC scheduling

PNC visits tracked

Exit form completes the program
This structure ensures complete lifecycle tracking of maternal health, from registration to postnatal follow-up, with automated scheduling based on pregnancy dates.

### Q: How do I write a rule to calculate BMI in Avni?

// SAMPLE RULE EXAMPLE: Calculate BMI from Height and Weight
'use strict';
({ params, imports }) => {
  const programEnrolment = params.entity;        // Current program enrolment
  const formElement = params.formElement;        // The form element this rule is linked to
  
  // Fetch observations for Height and Weight (update names as per your form)
  let height = programEnrolment.findObservation("Height of women");
  let weight = programEnrolment.findObservation("Weight of women");
  
  height = height && height.getValue();
  weight = weight && weight.getValue();

  let value = '';
  
  // If both height and weight are valid numbers, calculate BMI
  if (_.isFinite(weight) && _.isFinite(height)) {
    value = ruleServiceLibraryInterfaceForSharingModules
              .common
              .calculateBMI(weight, height);
  }

  // Return the BMI value into the current form element
  return new imports.rulesConfig.FormElementStatus(formElement.uuid, true, value);  
};

Replace "Height of women" and "Weight of women" with the exact observation names in your form.

calculateBMI is already available in the shared rule service library, so no need to manually code the math.

This rule is from the Pregnancy Program Enrolment form

### Q: How do I create a rule to send an alert for high blood pressure?

Avni does not provide an in-app alert or notification feature. However, abnormal values like high blood pressure can still be highlighted during data entry. For example, while configuring a numeric field (such as BP Diastolic) in the App Designer, you can set thresholds (e.g., High Normal = 80). If a user enters a value above this, it will automatically be highlighted in red to indicate an abnormal condition. Additionally, these abnormal values can be included in decisions within the form, and the resulting decision outcomes can be displayed in the program summary of that individual, making it easier to track and review cases of high blood pressure. Furthermore, an offline report card can be configured to list and navigate to such cases, allowing field teams to easily identify and follow up on individuals with high BP.

### Q: How do I validate a phone number with a regex rule?

A phone number is typically added as a Text concept with a validation rule. There are different regex rules that you can write. Some examples are

^[0-9]{10}$ - 10 digits only
((\+*)((0[ -]*)*|((91 )*))((\d{12})+|(\d{10})+))|\d{5}([- ]*)\d{6} - All different kinds of phone numbers

### Q: How do I enforce that visits happen within 30 days?

You can add two dates when you schedule a visit. 
Due Date - The earliest date on which a visit is expected to happen
Overdue Date - The latest date by when a visit is expected to happen

Visits that are due and overdue can be shown on the app on the dashboard, and on reports. This allows users to understand which visits are due to be completed, and which ones have gone past the due date

### Q: Can I write a rule to calculate gestational age?

Sample rule to calculate - "use strict";
({params, imports}) => {
    const programEncounter = params.entity;
    const formElement = params.formElement;
    
 let edd = programEncounter.programEnrolment
 .getObservationReadableValueInEntireEnrolment('Estimated Date of Delivery', programEncounter);
let dateOfDelivery = programEncounter.getObservationReadableValue('Date of delivery');
 
    
 const value = imports.motherCalculations
      .gestationalAgeForEDD(edd,dateOfDelivery);
      
 return new imports.rulesConfig.FormElementStatus(formElement.uuid, true, value);
};

### Q: Can I update a subject’s information after registration?

Yes, Avni allows to edit the registration information.

### Q: How do I record a missed visit?

Avni allows to do data entry for the back dates, just select the date on top of the visit while filling the form

## Related Topics

<!-- Add links to related documentation -->


---
<!-- Source: 03-concepts-and-forms/form-structure.md -->

# Form Structure and Design in Avni

## TL;DR

To understand how Avni works lets first understand the domain model of field-based work. Any field-based work can be broadly subdivided into three components.

## Overview

To understand how Avni works lets first understand the domain model of field-based work. Any field-based work can be broadly subdivided into three components.

1. **Service delivery organisation** - The organisation, with providers and the geographical area where they work.
2. **Services (or schema of data to be collected)** - The actual set of services provided by the above organisation to the people (or data to be collected about something in a said geographical area).
3. **Service encounter** - Each service is broken down into a discrete set of type of encounters that providers of the organisation have with the people.

Now lets further explore each one of the above one by one and how Avni models it into the software system.

## 1.  The architecture of the service delivery organisation

Avni allows for modelling of the work geography of the organisation and mapping of service providers to their geographical units. In avni, one can set up the complete geographical area into multiple levels and locations at the same level.

Lets first identify the key domain concepts with their names. A service delivery organisation consists of the following:

* An **organisation** (e.g. NGO, or government department, university), the entity that provides the service or collects some data.
* In order to provide this service or collect data, this organisation employs, hires or engages service providers. They can be called field workers, frontline worker, health worker, etc - we will simply call them **provider or user**.
* The service provided by the organisation via the providers is received by *beneficiaries, citizens, patients, students, children* so on. In the case where the work is data collection, the provider may be additionally or only collecting data for non-living objects like *water body, school, health centre*, etc. Since Avni is a generic platform, let's call of them by a rather imaginative name **subject**.
* In most Avni use cases, the subjects may be spread across a geographical area such that one provider cannot service (or collect data from) all subjects. Hence each provider is assigned a specific area that is called **catchment** in Avni. A catchment could be a block, a cluster of slums, etc.
* Each catchment may have one or more geographical units which are called **location**s in Avni. A location could a village, slum, subcenter area so on.

Each user **must** to be associated with at least one catchment.

![1918](https://files.readme.io/4343bff-Screenshot_2019-11-15_at_5.17.05_PM.png "Screenshot 2019-11-15 at 5.17.05 PM.png")

![An example of service delivery organisation](https://files.readme.io/514028d-Screenshot_2020-11-16_at_11.50.38_AM.png)

In Avni system, the organisation, provider, catchment and location are setup via web application by the implementer, IT or program administrator. When a subject is created/registered in the system, they are assigned a location. This is usually done by the field user using their mobile device

## 2.  Modelling the services provided into Avni

Avni allows for modelling of the services provided (or data collected) via a three-level configurable data structure. Avni allows for setting up subjects, enrolment of subjects in programs, and defining encounters for enrolments/subjects. There can be multiple programs per subject type and multiple encounter types per program.

* An organisation may have one or more **subject types** to which they provide service (or collect data for).
* To each subject type, the organisation may be providing one or more service types (or have the purpose of data collection). In Avni, each service type is called a **program**.
* Each service type may involve one or more types of interactions which are called **encounter type**s. Avni also allows one to avoid the service type completely and define encounter types directly for the subject types - allowing for modelling of interactions which are not required to be grouped under services.

![2084](https://files.readme.io/b63d3c9-Screenshot_2019-11-15_at_5.26.15_PM.png "Screenshot 2019-11-15 at 5.26.15 PM.png")

![1942](https://files.readme.io/93a551a-Screenshot_2019-11-15_at_5.27.48_PM.png "Screenshot 2019-11-15 at 5.27.48 PM.png")

![1906](https://files.readme.io/3ca82d4-Screenshot_2020-09-23_at_6.00.45_PM.png "Screenshot 2020-09-23 at 6.00.45 PM.png")

## 3. Groups and relationships

Avni allows for creating groups of subjects and more specifically a special type of group called household or family whereby another subject types (created to represent people) can be members of the household. These members can also be linked to each other via relationships. Do note though that in Avni we have modelled group and households via attributes on subject types. The subjects of such types can be linked as child elements of the parent subject. Please the diagrams below. Avni application behaves differently for groups and households.

![Group also can behave like subjects also, along with being a group of subjects.](https://files.readme.io/a5fd36e-Screenshot_2020-04-28_at_11.20.04_AM.png)

![Household is a special type of group, which has persons as members. The persons can be related to each other via human relationship types.](https://files.readme.io/740185f-Screenshot_2020-04-28_at_11.16.09_AM.png)

## 4.  Design of a service encounter

Service encounter is an encapsulation of a type of interaction between the service provider and the beneficiary - as explained above. Each service encounter consists of the following:

* observation made by the service provider (field workers)
* answer is given by the beneficiary for a question asked by the provider
* information/suggestion/recommendation made by provider
* computed or preset information provided by the avni app to the provider
* photos/videos taken by the provider

Avni allows you to arrange these sequentially and including based on conditions set by you. It also allows to schedule next service encounters based on a rule set by you. This is modelled using form, rules and content. Each service encounter can be defined in this way.

![Anatomy of an encounter type (or a subject registration form)](https://files.readme.io/d7f0b31-Screenshot_2019-11-15_at_5.30.31_PM.png)

![Example of a few form element groups.](https://files.readme.io/5fdb3eb-Screenshot_2019-11-15_at_1.53.16_PM.png)

![Example of form elements within a form element group.](https://files.readme.io/2c87d92-Screenshot_2019-11-15_at_1.55.34_PM.png)

## Related Topics

<!-- Add links to related documentation -->


---
<!-- Source: 03-concepts-and-forms/media-in-forms.md -->

# Using Media in Forms (Images, Video, Audio)

## TL;DR

Avni allows for adding media like data (image and video) in the forms. It can be in form of single or multiple media files in the same question.

## Overview

Avni allows for adding media like data (image and video) in the forms. It can be in form of single or multiple media files in the same question. These can be added by the user using the camera and the file system. Multiple files can be added too in one go. Please see the following table for the capabilities.

| Media Type  | Selection type | Android Version | Supported?    |
| :---------- | :------------- | :-------------- | :------------ |
| Image/Video | Single         | &lt; 13.0       | Supported     |
| Image/Video | Multiple       | &lt; 13.0       | Not Supported |
| Image/Video | Single         | &gt;= 13.0      | Supported     |
| Image/Video | Multiple       | &gt;= 13.0      | Supported     |

## Why multi-select is not supported in older versions of android

This capability has been restricted by the react native (framework) library used by us. [https://www.npmjs.com/package/react-native-image-picker](https://www.npmjs.com/package/react-native-image-picker)

## My media is in a folder that is not showing in the albums when I am using Avni

If you have images in android folders (in storage) as archive then it is possible that they are shown when you want to upload images in Avni forms. Please see the following as a way to solve this issue.

Android displays only folders which are **considered** albums. A plain folder with images may not be shown here for this reason.

### Option 1

You can setup a folder you want to upload media in Avni by making it show up as albums. You can do that by setting it as Google Photos backup folder. You can do that by:

* going to `Google Photos` app, then `Settings`, then `Choose backup device` folders option, then choose your folder.
* going to `Google Photos` app, then `Library`, then `Utilities`, then choose `Backup Device Folders`, then choose your folder.

### Option 2

Copy/move the folder which has the media to one of the folders which are picked by the Avni form.

*Please note that Google Photos have storage limits.*

We cannot find any means by which an album be added only locally, without it being backed up on Google Photos. [https://www.reddit.com/r/googlephotos/comments/x331q9/create_albums_that_dont_sync_with_the_cloud/](https://www.reddit.com/r/googlephotos/comments/x331q9/create_albums_that_dont_sync_with_the_cloud/)

## How do apps like Dropbox, Facebook, etc support multi-select and have better album support

Since these are not open source projects we can only guess. But it is likely that they have developed their own screens that uses the android file system API.

## Why does Avni not do the same as other apps

1. It is significant amount of work to develop this from scratch compared to use the android's media picker.
2. About 50% and rapidly growing number of Avni users are already on android 13 or later.

## Also see

* Media Viewer

## Related Topics

<!-- Add links to related documentation -->


---
<!-- Source: 03-concepts-and-forms/multi-language-forms.md -->

# Multi-Language Forms and Translation Management

## TL;DR

Since Avni is widely used for Data-collection by field workers, it is most likely to have a need for the Forms to be read and filled-up in their native language. For example, field workers providing health-care services in the remote villages of Gujarat would be most comfortable performing data-c...

## Overview

Since Avni is widely used for Data-collection by field workers, it is most likely to have a need for the Forms to be read and filled-up in their native language. For example, field workers providing health-care services in the remote villages of Gujarat would be most comfortable performing data-collection in Gujarathi, as opposed to English or Hindi.\
For this reason, Avni supports translation of data-collections forms to native language of the user(field worker) in the Avni "client" mobile application and "Data-Entry" Web application.

## Supported Languages

Avni currently supports Translation capabilities from English to following languages:

* Hindi  
* Marathi  
* Gujarathi  
* Tamil  
* Kannada  
* Bengali  
* Telugu  
* Odia  
* Malayalam  
* Punjabi  
* Sanskrit  
* Urdu  
* Assamese

We additionally have some default translations already available for a few of the above languages, that would make it easier for an organisation to get started on its “Translations” journey. The languages that have some baked-in translations in Avni are as follows:

* Hindi  
* Marathi  
* Gujarathi  
* Tamil  
* Kannada

## Prerequisites

In-order to set up translation for any of the aforementioned languages, the organisation should have enabled the language in the Languages section of the Organisation config.

### Steps to enable Languages for the Organisation

1. Navigate to the “Admin” application

   ![](https://files.readme.io/7bf088b321b670a88c9b73d86ed5d50999afb0ea9553067a0c3483c38e53c7b8-image.png)
2. Select the “Languages” section in the left-tab  
3. Add all the languages that are to be made available to the translation framework, using the drop-down and then click on “Save” button

   ![](https://files.readme.io/0dd7d20b674af9c7257ea0b6e3566e31a8f12dc66b8372251c4e8f305210398d-image.png)

## Steps involved in the translation process

Avni allows the management of translations using the Admin web interface. Below are the steps to translate the content of the app from English to the preferred language

### Navigation to ‘Translations’ module

Login to Avni Web Console and go to the ‘Translations’ module. 

![](https://files.readme.io/ebee37b87a4225d75c86d2c0ff612fcb9bd2ca653fd70d3e95a557ddb9c0a697-image.png)


### Downloading Translation Keys from Avni

* From the “Translations Dashboard”,download the keys after choosing the desired platform. Platforms are:  
  * Web  
  * Android  
* In general, most organisations need translations only for their field users who perform data-collection using their mobile devices. In such cases, the platform of interest is “Android” (Mobile).  
* If additionally, your organisation also wants translations to be done for the Data-Entry App, then also download the keys for the “Web” platform. 

![](https://files.readme.io/9a5030ec956f7983bf2edff00650c0a2d00367fee775375ecafb49957a8e4a6c-image.png)


* For each platform selection download, the app will download a zip file containing one JSON file per language available in the organisation config.   
* The JSON file will contain keys for both the standard platform app as well as those specific to your implementation, covering all labels in the app, form fields, location names and any other concepts created in the implementation.  
* The file will also contain existing translated values, if any. This is useful when you have to update the translations after a while, as you will already have all previously uploaded translations available for retention or modifications as needed  
* IMPORTANT Note: When organisations do not want Locations to be part of translations, then they need to bundle export without locations, import those into a temporary org and export translations from that temporary organisation. This was required for one of our organisations since they had a very large number of locations (More than 100,000) and hence were in need to translate other things before locations.

### Setting up a project in Translation Management System (TMS)

* The JSON files can be edited with any tool that the implementer is comfortable with, to come up with translated values for the target language.  
* But for most use cases, we would have multiple translators involved and/or a lot of keys are to be translated. In such cases, we highly recommend using an external translation management system (TMS) like [Lokalise](https://lokalise.com/) which provides a sophisticated editor for performing translations. The TMS provides the ability to import/export JSON files and supports a variety of use cases related to translations.  
* Avni has an enterprise-free plan for Lokalise. If you would like to use Lokalise, please request the Avni team to create your account and project to get started.

#### Creating an implementation project in Lokalise

This is an optional step, required only if the implementation project does not already exist. 

1. In the Project section, a new project needs to be created as shown in the screenshot below.   

   ![](https://files.readme.io/cde8ae8c4f81316f321973918c3717b138e529eb0c1bac0e8c305f1c74e4fb98-image.png)

   ![](https://files.readme.io/46fc019a73c69cd626060e89701fba69edf2894fdad9ccb112a85fd58cb08fd3-image.png)

   

2. While creating the project, provide the Project name, Base language (Which will be english always), and target language in which translations are needed.

   ![](https://files.readme.io/3b1d13d3c4ee9db1eb2f247b44fb36b44f98063d143c684a8c620aae8f1d4d96-image.png)

#### Uploading Translation keys to Lokalise

Once the project is ready in TMS and you have downloaded the translation ZIP file(s), log in to [Lokalise](https://app.lokalise.com/projects) with Samanvay's official email address, if not already done.

* Unzip the downloaded translation zip file  

* Before uploading the JSON, please make sure that null values are removed from the json files

  ![](https://files.readme.io/db2521a87f4b27a65fbac3b98fdf384aaf6024f21dd04d864bb95df03bceff93-image.png)

* In your project, navigate to the ‘Upload’ section and import the JSON file from the unzipped folder of the previously downloaded Translations zip file.

  ![](https://files.readme.io/7d26a129395f40bc2e2bbca4a770a27cf61fa0258d5129fd75a95538a51536d6-image.png)

* In the translation zip file that is downloaded, go to the local folder and select the English json file  

* Once the JSON file has been uploaded successfully, you will see the ‘Ready for Import’ message.

  ![](https://files.readme.io/6a0496a0ba800eb383d5b8f8978defe60bbaf01130868d8e2de18ab6f4324fbe-image.png)

* Go to the ‘editor’ section and verify the keys available for the translation.

  ![](https://files.readme.io/775e3003e6a87eade2045a7acf5b844ea1d1f60efac77cd4f74370fc3572c1b0-image.png)

  

#### Inviting Contributors to the project

Next, Navigate to the ‘Contributors’ section to send out invites to other people

![](https://files.readme.io/0903aa35f4aa3b0b7cc8ec50506511d0e99f0dd8b624eeaf5c403d816b204d3c-image.png)


Perform below mentioned tasks to invite users to collaborate on the project

* Role should be selected as ‘Translator’   
* “Reference language” should have the base language (Usually English) and  
* “Contributable language” should have target language

![](https://files.readme.io/c3a2ff0b427c727aea29a09ff339a6c7a7219079cf034cd76a114b956f0c3ec8-image.png)


### Guide for translating keys using Lokalise

* All invitees will receive an Email invite from Lokalise with instructions to login and access the project.

  ![](https://files.readme.io/0f9fcf8ad025f5dd50c754a3736618988e51eced350063df791a20145073c8fb-image.png)

* Once logged in, available projects will be shown in the projects tab/ home screen. you can click on the project name to access the translation items.

  ![](https://files.readme.io/29a4f970e6de4969a115870182c25584f55b1fc1a65eaa09a46b2786fc9317f6-image.png)

* The project would display the editor page by default, and the list of keys should be visible at the bottom.

  ![](https://files.readme.io/e0ab4bd3396825a5df93f6cd6f2e39997d51e8a82b9d33c9ff65d10c9f9e7e25-image.png)

* You can select the Bilingual option shown in the screenshot below and search the question or required field names to be translated.

  ![](https://files.readme.io/0de7bfccf120d85d1154466d2ae52a542f12b0ef10eddf0f133b228d3e6a49cf-image.png)

* After giving the keywords in the search bar, you can see the results below which show questions and field names on the left side. against which you need to provide the Kannada translation and save the response.

  ![](https://files.readme.io/914ab3acbc6c6d25788f872ceecca5160f1420ad85d29afc3ff45d3e240d5d16-image.png)

* Additional notes  
  * Keep the required forms handy while you start the translation process, you can refer to the questions from respective and update the values in Lokalise.  
  * In case of questions, the box on the left side might show "empty" and the question would be visible above that in blue fonts. you can provide the appropriate translation against that on the right-hand side box.

#### Translating Keys with Dynamic string having placeholders

Consider the following “Android” Platform keys, which are examples for Dynamic strings with placeholders:

| numberAboveHiAbsolute | "Should be \{\{limit}}, or less than \{\{limit}}" |
| :-------------------- | :------------------------------------------------ |
| enrolmentSavedMsg     | "\{\{programName}} Enrolment Saved"               |

In-order to translate them to Hindi, you would have to specify following in the translated json file:

| numberAboveHiAbsolute | "\{\{limit}} के बराबर या \{\{limit}} से कम" |
| :-------------------- | :------------------------------------------ |
| enrolmentSavedMsg     | "\{\{programName}} एनरोलमेण्ट सेव हुआ"      |

As shown above, ensure that you retain the string placeholder content within “\{\{” and “}}” as is in native english. Ex: “\{\{limit}}”, "\{\{programName}}”

### Uploading Translations

After completing translation for all the required keys, questions and forms you can download the translated values JSON file of the target language.

* Go to the “Downloads” section of the project  

  ![](https://files.readme.io/934b5c2b87ce2127c6983e5f97739abd5aa4381c3c0c884f7d53a040f9c4d8a1-image.png)
* As seen above, select the ‘Don’t Export’ option for the “Empty Translations” field, so as to export only the translated fields.  
* Click on “Build and Download” option to download the Translated values ZIP file

  ![](https://files.readme.io/ae74952cda34852fe4c7d78933624066f83514681cf5fe52ec8d17b53e911303-image.png)
* Please note that the downloaded ZIP file would contain the JSON file of the base language (English) and targeted language JSON.

  ![](https://files.readme.io/f61d4ac05c7f32ff80ce10f556145a89b11b3ef9f0a43ee2509c4515d31c321c-image.png)
* Now the JSON file of the translation language needs to be uploaded into the Avni. Navigate to the “Translations Dashboard“. Using its “Upload Translations” functionality, upload the JSON file, after choosing an appropriate language. Be careful about choosing the target language, it should be same as the language of the translated values.

  ![](https://files.readme.io/1cc8a1416150da1c1961d5b82bb4508b387a4be7a71d4679ad68f4778ce47301-image.png)
* On successful upload of the translated values, you should see a change in the value of the “Keys with translations” column for the corresponding Language, in the “Translations Dashboard”.

## **Using the Avni client application in User’s native Language**

On the Avni client app, users would need to sync their devices in-order to get the new translations.

If the default language for the User hasn’t been set to his/her desired native language, then the user should be able to switch to it, by navigating to the “More” menu and clicking on the “Edit Settings” button at the top, and selecting the language in which he/she wants to see the app content.

![image](https://files.readme.io/28964f670ac61932780ce5d1a5d3c2553a005e392960a59852aacc0c130b57b9-image.png)

![image](https://files.readme.io/aed7f494a90af456f84dc6caa5ec5c80c32e9f469b61ec7295d60a7deaa86503-image.png)


After adding [languages](#/admin/language) you will be able to download/upload the translation file for all the different languages.

Learn more about [translation management](https://avni.readme.io/docs/translation-management).

## Related Topics

<!-- Add links to related documentation -->


---
<!-- Source: 03-concepts-and-forms/repeatable-question-groups.md -->

# Repeatable Question Groups in Avni

## TL;DR

A repeatable question group is an extension of the question group form element. A Question group is like any other data type in Avni.

## Overview

A repeatable question group is an extension of the question group form element. A Question group is like any other data type in Avni. The only difference is it allows implementers to group similar fields together and show those questions like a group. Now there are cases where you want to repeat the same set of questions(group) multiple times. This can be easily done by just marking the question group as repeatable.

## Steps to configure repeatable Question group

1. Create a form element having a question group concept.
2. This will allow you to add multiple questions inside the question group.
3. Once all the questions are added, mark it repeatable and finally save the form.

![Notice how the question group is marked repeatable.](https://files.readme.io/ae26aab-Repeaable-question-group.png)

![Repeatable questions in mobile app](https://files.readme.io/61bee14-repeatable-question.gif)

### Limitations

At this time, the following elements that are part of the forms are not yet supported. 

* Nested Groups
* Encounter form element
* Id form element
* Subject form element with the "Show all members" option (Regular subject form elements are supported)

  * To get this working within a Question-Group/ Repeatable-Question-Group, for a Non "Group" Subject Type, please select the **"Search Option"** in the Subject FormElement while configuring the Form inside **App Designer**

  ![image](https://files.readme.io/c5c15ae-Screenshot_2024-06-10_at_2.35.04_PM.png)

## Related Topics

<!-- Add links to related documentation -->


================================================================================
# Section: Subject Types Programs
================================================================================


---
<!-- Source: 04-subject-types-programs/README.md -->

# Subject Types, Programs, and Encounter Types

Configuring the core building blocks of Avni: subject types (who/what you track), programs (longitudinal workflows), and encounter types (data collection events).

## Contents

### 1. [Subject Types in Avni](subject-types.md)
subject types  individual  household  group

### 2. [Subject Type Settings and Configuration](subject-type-settings.md)
subject type settings  registration  profile  active subjects

### 3. [Programs in Avni](programs.md)
programs  program enrollment  program exit  longitudinal tracking

### 4. [Program Configuration Options](program-configuration.md)
program configuration  multiple enrollments  program settings

### 5. [Encounter Types in Avni](encounter-types.md)
encounter types  general encounters  program encounters  visits

### 6. [Designing Workflows and Data Models in Avni](workflow-design.md)
workflow design  data model  implementation planning  program design

### 7. [Creating Auto-Generated Identifiers](identifiers.md)
identifiers  auto-generated IDs  ID source  unique IDs


---
<!-- Source: 04-subject-types-programs/encounter-types.md -->

# Encounter Types in Avni

## TL;DR

Encounter Types (also called Visit Types) are used to determine the kinds of encounters/visits that can be performed. An encounter can be scheduled for a specific encounter type using rules.

## Overview

Encounter Types (also called Visit Types) are used to determine the kinds of encounters/visits that can be performed. An encounter can be scheduled for a specific encounter type using rules. Here, we define that encounter type and the forms associated with the encounter type.

An encounter type is either associated directly with a Subject type or is associated with a Program type, which in-turn would be associated with a subject type. It need not always be associated with programs (you can perform an annual survey of a population using encounter types not associated with programs, and use this information to enrol subjects into a program).

## Immutable encounter type

The encounter type can be made immutable by switching on the immutable flag on the encounter type create/edit screen. If the encounter type is marked as immutable then data from the last encounter is copied to the next encounter. Since the encounter is immutable, the edit is not allowed on these encounters.


Encounter Types (also called Visit Types) are used to determine the kinds of encounters/visits that can be performed. An encounter can be scheduled for a specific encounter type using rules. Here, we define that encounter type and the forms associated with the encounter type.

An encounter type is associated to a subject type. It need not be associated with programs (you can perform an annual survey of a population using encounter types not associated with programs, and use this information to enrol subjects into a program).

The encounter eligibility check rule is used to determine eligibility of an encounter type for a subject at any time.

- [Learn more about Avni's domain model](https://avni.readme.io/docs/avnis-domain-model-of-field-based-work)
- [Learn more about writing rules](https://avni.readme.io/docs/rules-concept-guide)

## Related Topics

<!-- Add links to related documentation -->


---
<!-- Source: 04-subject-types-programs/identifiers.md -->

# Creating Auto-Generated Identifiers

## TL;DR

Identifiers are unique strings generated by the system, which can be used to identify a beneficiary. Usually, these have special patterns - prefixes, suffixes, special numbering patterns etc, which aid users in understanding a beneficiary.

## Overview

### Identifiers

Identifiers are unique strings generated by the system, which can be used to identify a beneficiary. Usually, these have special patterns - prefixes, suffixes, special numbering patterns etc, which aid users in understanding a beneficiary. 

### ID Generation in Avni

In usual systems, identifiers are generated from a central place because we need them to be unique. However, the Avni Android app is expected to work offline. Offline ID generation is possible, but is done differently. IDs in Avni are generated in batches and sent to a user. 

There is a special form element type called ID. If you configure a form element to be of ID type, then the Avni android app will automatically retrieve the next ID from this batch and assign it as the value. 

*Advanced* - It is also possible to create rules that modify the final ID that is stored for the beneficiary. For example, if there is the need of adding a date to the final ID being generated, you would write a ViewFilter rule that will use the generated ID and append a date to it. 

### Identifier sources

It is possible to have multiple IDs being generated at the same time. Each ID type is called an identifier source. An identifier source will have a certain type (discussed later), prefix (optional), minimum and maximum lengths and can be assigned to a  catchment.\
The type of an identifier source determines the strategy used to generate IDS of that source. There are currently two types available. The only difference between them is the place where the prefix is stored. 

1. User pool based identifier generation - Here, a pool of users within a catchment share the same prefix. The prefix is stored within the identifier source within options. Every user asking for ids is provided with a set of ids prefixed with this value. 
2. User based identifier generation - Here, the prefix is stored in the "idPrefix" value of the user's settings.

### Rules

1. User pool based identifier generation - overlaps in ID for the same identifier source not allowed.
2. User based identifier generation - Two users in the same organisation cannot have same prefix. This check is case in-sensitive.

Queries to analyse existing data is available here - [https://github.com/avniproject/avni-webapp/issues/1022#issuecomment-1693064436](https://github.com/avniproject/avni-webapp/issues/1022#issuecomment-1693064436)

### Tutorial

#### 1. Create Identifier Source from admin section:

1. Give name
2. Choose type - User pool based identifier generator or User based identifier generator. Difference between the two is explained above.
3. Choose catchment
4. Choose batch generation size. This is the number of identifiers that will be generated at once and be sent to client app on sync. If your field users can not sync for a long time then you should estimate how many identifiers they may need.
5. Choose minimum balance. This is useful to make sure that your users get a warning to sync before they run out of identifiers.
6. Choose Min length and max length. This specifies the min and max length of the generated identifiers.
7. You will get an option to add Prefix if you chose User Pool Based Identifier Generator in the Type field(1.2). This prefix will be shared by all identifiers generated for users sharing the same identifier source.

#### 2. Create Identifier User Assignment from admin section:

1. Choose User. The user that you select will start getting auto-generated ids  once they Sync.
2. Choose Identifier Source. This is the resource that you created in Step 1 above(Create Identifier Source from admin section).
3. Enter initial identifier to be generated for this user. It should also include the prefix. E.g. if you had set the prefix to be ANC and min length to be 3, and you want the identifiers to start from 100 then the value of this field could ANC100.
4. Enter last identifier to be generated for this user. System will not generate any identifiers beyond this. E.g. If your prefix is ANC, max length is 4 and you want identifiers only till 2000 then this could be ANC2000.

#### 3. Create a question in the form with concept type Id

1. In the form where you want the auto generated identifier, do create a question with concept type Id and select the identifier source.


Create autogenerated Ids by configuring Identifier Sources, and creating Identifier user assignments

[Learn more about setting up identifiers](https://avni.readme.io/docs/creating-identifiers)


[Learn more about setting up identifiers](https://avni.readme.io/docs/creating-identifiers)

## Related Topics

<!-- Add links to related documentation -->


---
<!-- Source: 04-subject-types-programs/program-configuration.md -->

# Program Configuration Options

## TL;DR

Each subject type can have multiple programs within them. If these programs are defined, the user can enroll subjects of these subject types into these programs.

## Overview

Each subject type can have multiple programs within them. If these programs are defined, the user can enroll subjects of these subject types into these programs.

Number of enrolments per subject

* Typically and hence by default, a subject can have only one active enrolment for a program. This implies that for a subject to be enrolled again the previous enrolment must be exited. e.g. Pregnancy program. Sometimes for chronic diseases, a person may remain in a program forever like diabetes. In such cases, the subject is never exited.
* Starting release 3.37, Avni also supports multiple active enrolments in a program. This can be done by switching on this per program. When this is switched on the above condition is relaxed by Avni.

![image](https://files.readme.io/62b1f10-image.png)

## Related Topics

<!-- Add links to related documentation -->


---
<!-- Source: 04-subject-types-programs/programs.md -->

# Programs in Avni

## TL;DR

A program defines the service, or intervention that you provide to subjects.

## Overview

A program defines the service, or intervention that you provide to subjects.

A subject is enrolled into the program using the Enrolment Form. Routine information is collected through Encounters. A subject exits a program by filling in the Exit Form.

- [Learn more about Avni's domain model](https://avni.readme.io/docs/avnis-domain-model-of-field-based-work)
- [Learn more about writing rules](https://avni.readme.io/docs/rules-concept-guide)


title: Setting up your data model
excerpt: ''
    - type: basic
      slug: my-dashboard-and-search-filters
      title: My Dashboard and Search Filters
---
As explained in Implementer's concept guide - Introduction - subject, program and encounter are the three key building blocks you have - using which you can model almost all field-based work. Groups (households) that are a special type of subject will be treated as the fourth building block.

In the web application, you would see three menus which map to above - subject types, programs and encounter types. You must be assigned an organisation admin role to be able to do this. If you are, then you can see these options under the Admin section. Each one of the following is linked to their respective forms which you can navigate from the user interface.

![](https://files.readme.io/f4090d7-Screenshot_2020-04-28_at_11.30.58_AM.png "Screenshot 2020-04-28 at 11.30.58 AM.png")

When setting up your model you will be defining the concepts and forms. The diagram below explains the relationship between entities above, form and concepts. Currently, in the application, you may need to go to the concept's view to edit it fully. Soon we would provide seamless editability of the underlying concept via form editing.

![](https://files.readme.io/f678cdd-Screenshot_2020-04-28_at_6.44.23_PM.png "Screenshot 2020-04-28 at 6.44.23 PM.png")

An example form below of name "Child Enrolment", with one form element group called "Child Enrolment Basic Details". This form element group has 6 form elements.

![](https://files.readme.io/eb3a4bf-Screenshot_2020-04-28_at_7.13.21_PM.png "Screenshot 2020-04-28 at 7.13.21 PM.png")

One of the form element is displayed below with all the details. The concept used by the form element is also displayed like allow data range values. From this screen, as of now, it is not editable you need to go to the concepts tab to edit it.

![](https://files.readme.io/f968766-Screenshot_2020-04-28_at_7.17.04_PM.png "Screenshot 2020-04-28 at 7.17.04 PM.png")

You can specify the skip logic for under the rule tab within the form element. This currently is done only using JavaScript, but in future, one would be able to do it using the UI directly. For more on rules please see the Writing rules.

![](https://files.readme.io/661ab7b-Screenshot_2020-05-19_at_4.49.43_PM.png "Screenshot 2020-05-19 at 4.49.43 PM.png")

## Related Topics

<!-- Add links to related documentation -->


---
<!-- Source: 04-subject-types-programs/subject-type-settings.md -->

# Subject Type Settings and Configuration

## TL;DR

If the view name exceeds 63 characters we trim some parts from different entity type names to keep it below 63 characters. For trimming, we follow the below rule.

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

## Related Topics

<!-- Add links to related documentation -->


---
<!-- Source: 04-subject-types-programs/subject-types.md -->

# Subject Types in Avni

## TL;DR

Subject Types define the subjects that you collect information on. Eg: Individual, Tractor, Water source, Classroom session.

## Overview

Subject Types define the subjects that you collect information on. Eg: Individual, Tractor, Water source, Classroom session. Service Providers in an organisation could be 

* taking action "Against" or "For" beneficiaries, citizens, patients, students, children, etc.
* collecting data for non-living objects like Water-body, School, Health Centre, etc.

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

## Related Topics

<!-- Add links to related documentation -->


---
<!-- Source: 04-subject-types-programs/workflow-design.md -->

# Designing Workflows and Data Models in Avni

## TL;DR

As explained in Implementer's concept guide - Introduction - subject, program and encounter are the three key building blocks you have - using which you can model almost all field-based work. Groups (households) that are a special type of subject will be treated as the fourth building block.

## Overview

As explained in Implementer's concept guide - Introduction - subject, program and encounter are the three key building blocks you have - using which you can model almost all field-based work. Groups (households) that are a special type of subject will be treated as the fourth building block.

In the web application, you would see three menus which map to above - subject types, programs and encounter types. You must be assigned an organisation admin role to be able to do this. If you are, then you can see these options under the Admin section. Each one of the following is linked to their respective forms which you can navigate from the user interface.

![](https://files.readme.io/f4090d7-Screenshot_2020-04-28_at_11.30.58_AM.png "Screenshot 2020-04-28 at 11.30.58 AM.png")

When setting up your model you will be defining the concepts and forms. The diagram below explains the relationship between entities above, form and concepts. Currently, in the application, you may need to go to the concept's view to edit it fully. Soon we would provide seamless editability of the underlying concept via form editing.

![](https://files.readme.io/f678cdd-Screenshot_2020-04-28_at_6.44.23_PM.png "Screenshot 2020-04-28 at 6.44.23 PM.png")

An example form below of name "Child Enrolment", with one form element group called "Child Enrolment Basic Details". This form element group has 6 form elements.

![](https://files.readme.io/eb3a4bf-Screenshot_2020-04-28_at_7.13.21_PM.png "Screenshot 2020-04-28 at 7.13.21 PM.png")

One of the form element is displayed below with all the details. The concept used by the form element is also displayed like allow data range values. From this screen, as of now, it is not editable you need to go to the concepts tab to edit it.

![](https://files.readme.io/f968766-Screenshot_2020-04-28_at_7.17.04_PM.png "Screenshot 2020-04-28 at 7.17.04 PM.png")

You can specify the skip logic for under the rule tab within the form element. This currently is done only using JavaScript, but in future, one would be able to do it using the UI directly. For more on rules please see the Writing rules.

![](https://files.readme.io/661ab7b-Screenshot_2020-05-19_at_4.49.43_PM.png "Screenshot 2020-05-19 at 4.49.43 PM.png")


title: Introduction
excerpt: ''
    - type: basic
      slug: avnis-domain-model-of-field-based-work
      title: Avni's domain model of field based work
---
Implementer's concept guide is for anyone who would like to implement Avni for any field-based program. We recommend this guide to be the first one to be read by anyone wanting to understand Avni.

While internally there are many parts of the system, if you are an implementer and using the hosted instance then these are the components you will be using. Some of the functions are intended for the end-users but you will use them for testing the application.

![User/Implementer components of Avni](https://files.readme.io/9fa4f1f-Avni_4.png)


title: Developing BI dashboards using AI services
excerpt: >-
  robots: index
next:
  description: ''
---
The tool used for this is Cursor which internally uses other AI services. You can download [Cursor](https://www.cursor.com/).

The source code used in this tool is available here [avni-ai-experiment](https://github.com/avniproject/avni-ai-experiment) (private repository as the CSV files used in the context may contain customer specific information). This repository will become a public repository soon.

## Generate aggregate and line list query

### When to use

Excel or spreadsheet contain the requirements for the report all present in a single sheet. This is the input used for generating the SQL. If you do not have this file then the steps below are **not recommended** as it will not be productive approach.

### Setup

1. Open avni-ai-experiment in Cursor.
2. Download the requirement sheet as a CSV file. Copy its contents and put them in any file under `bi-reporting-spike/dataset/workspace` folder. Let's say - `requirement.csv`. An example is present in workspace folder by name `example.csv`.
3. Create one file which contains all the table definition in the `bi-reporting-spike/aggregate/workspace`  or `bi-reporting-spike/linelist/workspace` folder. Let's say - `table-def.sql`. An example is present in workspace folder by name `example-jnpct-def.sql`. This was generated from IntelliJ (select schema and generate).

### Chat

1. Open chat window in Cursor.
2. Prompt to forget everything (line 1 of `aggregate-query-prompt.md` or `linelist-query-prompt.md`)
3. Follow the steps in [https://github.com/avniproject/avni-ai-experiment/blob/main/bi-reporting-spike/aggregate/workspace/aggregate-query-prompt.md](https://github.com/avniproject/avni-ai-experiment/blob/main/bi-reporting-spike/aggregate/workspace/aggregate-query-prompt.md) or [https://github.com/avniproject/avni-ai-experiment/blob/master/bi-reporting-spike/linelist/workspace/line-list-prompt.md](https://github.com/avniproject/avni-ai-experiment/blob/master/bi-reporting-spike/linelist/workspace/line-list-prompt.md)

## Related Topics

<!-- Add links to related documentation -->


================================================================================
# Section: Javascript Rules
================================================================================


---
<!-- Source: 05-javascript-rules/README.md -->

# JavaScript Rules Engine

Writing JavaScript rules for validation, decision logic (skip/show/hide), visit scheduling, and task scheduling. Includes helper functions reference and common patterns.

## Contents

### 1. [Introduction to Avni Rules Engine](rules-introduction.md)
rules engine  JavaScript rules  rule types  rules overview

### 2. [Writing Validation Rules in Avni](validation-rules.md)
validation rules  form validation  data validation  validation logic

### 3. [Writing Decision Rules (Skip Logic, Calculated Fields)](decision-rules.md)
decision rules  skip logic  show hide  calculated fields

### 4. [Writing Visit Schedule Rules](visit-schedule-rules.md)
visit schedule  scheduling  visit rules  follow-up visits

### 5. [Writing Task Schedule Rules](task-schedule-rules.md)
task schedule  task rules  task assignment  task management

### 6. [JavaScript Helper Functions Reference](helper-functions.md)
helper functions  API reference  getObservationValue  getAgeInYears

### 7. [Common JavaScript Rule Patterns](common-patterns.md)
rule patterns  BMI calculation  phone validation  age calculation

### 8. [Rule Extension Points in Avni](extension-points.md)
extension points  rule hooks  custom logic  rule types

### 9. [Rules Development Best Practices](rules-best-practices.md)
best practices  rules testing  debugging  rule development


---
<!-- Source: 05-javascript-rules/common-patterns.md -->

# Common JavaScript Rule Patterns

## TL;DR

<!-- TODO: Add 2-3 sentence summary of Common JavaScript Rule Patterns -->

## Overview

**What:** <!-- TODO: One-sentence description -->

**When to use:** <!-- TODO: Scenarios -->

**Prerequisites:** <!-- TODO: What to know first -->

## Bmi Calculation

<!-- TODO: Add content for bmi-calculation -->

## Age Based Logic

<!-- TODO: Add content for age-based-logic -->

## Phone Validation

<!-- TODO: Add content for phone-validation -->

## Date Validations

<!-- TODO: Add content for date-validations -->

## Conditional Logic

<!-- TODO: Add content for conditional-logic -->

## Related Topics

<!-- TODO: Add links to related documentation -->


---
<!-- Source: 05-javascript-rules/decision-rules.md -->

# Writing Decision Rules (Skip Logic, Calculated Fields)

## TL;DR

<!-- TODO: Add 2-3 sentence summary of Writing Decision Rules (Skip Logic, Calculated Fields) -->

## Overview

**What:** <!-- TODO: One-sentence description -->

**When to use:** <!-- TODO: Scenarios -->

**Prerequisites:** <!-- TODO: What to know first -->

## Skip Logic Basics

<!-- TODO: Add content for skip-logic-basics -->

## Calculated Fields

<!-- TODO: Add content for calculated-fields -->

## Code Examples

<!-- TODO: Add content for code-examples -->

## Common Patterns

<!-- TODO: Add content for common-patterns -->

## Related Topics

<!-- TODO: Add links to related documentation -->


---
<!-- Source: 05-javascript-rules/extension-points.md -->

# Rule Extension Points in Avni

## TL;DR

Extensions are points in Avni where custom html can be used to enhance functionality. There are a few such predefined points where custom html can be inserted.

## Overview

Extensions are points in Avni where custom html can be used to enhance functionality. There are a few such predefined points where custom html can be inserted. 

In Data Entry App

* Subject Dashboard
* Subject Dashboard for a specific program
* Search Results page

In the Field-App

* Splash Screen

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

## Related Topics

<!-- Add links to related documentation -->


---
<!-- Source: 05-javascript-rules/helper-functions.md -->

# JavaScript Helper Functions Reference

## TL;DR

**Audience**: Rule developers, implementers, and technical teams

## 📋 Table of Contents

* [Observation Access Methods](#observation-access-methods)
  * [`getObservationReadableValue()`](#getobservationreadablevalueconceptnameoruuid-parentconceptnameoruuid)
  * [`getObservationValue()`](#getobservationvalueconceptnameoruuid-parentconceptnameoruuid)
  * [`findObservation()`](#findobservationconceptnameoruuid-parentconceptnameoruuid)
  * [`findLatestObservationInEntireEnrolment()`](#findlatestobservationinentirenrolmentconceptnameoruuid-currentencounter)
  * [`hasObservation()`](#hasobservationconceptnameoruuid)
* [Age and Time Calculation Methods](#age-and-time-calculation-methods)
  * [`getAgeInYears()`](#getageinyearsasondate-precise)
  * [`getAgeInMonths()`](#getageinmonthsasondate-precise)
  * [`getAgeInWeeks()`](#getageinweeksondate-precise)
  * [`getAge()`](#getageasondate)
* [Cancel Encounter Methods](#cancel-encounter-methods)
  * [`findCancelEncounterObservation()`](#findcancelencounterobservationconceptnameoruuid)
  * [`findCancelEncounterObservationReadableValue()`](#findcancelencounterobservationreadablevalueconceptnameoruuid)
* [Encounter Navigation Methods](#encounter-navigation-methods)
  * [`getEncounters()`](#getencountersremovecancelledencounters)
  * [`findLatestObservationFromEncounters()`](#findlatestobservationfromencountersconceptnameoruuid-currentencounter)
  * [`findLastEncounterOfType()`](#findlastencounteroftypecurrentencounter-encountertypes)
  * [`scheduledEncounters()`](#scheduledencounters)
  * [`scheduledEncountersOfType()`](#scheduledencountersoftypeencountertypename)
* [Individual and Subject Methods](#individual-and-subject-methods)
  * [`isFemale()`](#isfemale)
  * [`isMale()`](#ismale)
  * [`isPerson()`](#isperson)
  * [`isHousehold()`](#ishousehold)
  * [`isGroup()`](#isgroup)
  * [`getMobileNumber()`](#getmobilenumber)
  * [`nameString`](#namestring)
* [Location and Address Methods](#location-and-address-methods)
  * [`lowestAddressLevel`](#lowestaddresslevel)
  * [`lowestTwoLevelAddress()`](#lowesttwoleveladdressi18n)
  * [`fullAddress()`](#fulladdressi18n)
* [Relationship and Group Methods](#relationship-and-group-methods)
  * [`getRelatives()`](#getrelativesrelationname-inverse)
  * [`getRelative()`](#getrelativerelationname-inverse)
  * [`getGroups()`](#getgroups)
  * [`getGroupSubjects()`](#getgroupsubjects)
* [Validation and Status Methods](#validation-and-status-methods)
  * [`hasBeenEdited()`](#hasbeenedited)
  * [`isCancelled()`](#iscancelled)
  * [`isScheduled()`](#isscheduled)
  * [`isRejectedEntity()`](#isrejectedentity)
* [Media and Utility Methods](#media-and-utility-methods)
  * [`findMediaObservations()`](#findmediaobservations)
  * [`getProfilePicture()`](#getprofilepicture)
  * [`getEntityTypeName()`](#getentitytypename)
  * [`toJSON()`](#tojson)

***

## 📊 Quick Reference

| Category             | Most Used Methods               | Purpose                             |
| -------------------- | ------------------------------- | ----------------------------------- |
| **Observations**     | `getObservationReadableValue()` | Get formatted values for display    |
| **Observations**     | `getObservationValue()`         | Get raw values for calculations     |
| **Age Calculations** | `getAgeInYears()`               | Calculate age in years              |
| **Age Calculations** | `getAgeInMonths()`              | Calculate age in months (pediatric) |
| **Encounters**       | `getEncounters()`               | Get encounter history               |
| **Individual Info**  | `isFemale()` / `isMale()`       | Gender checks                       |
| **Individual Info**  | `getMobileNumber()`             | Get contact number                  |
| **Validation**       | `hasObservation()`              | Check if data exists                |
| **Validation**       | `hasBeenEdited()`               | Check encounter completion          |

***

## Observation Access Methods

### `getObservationReadableValue(conceptNameOrUuid, parentConceptNameOrUuid)`

**Available on**: Individual, ProgramEnrolment, AbstractEncounter (Encounter, ProgramEncounter)

**Purpose**: Gets the human-readable/display value of an observation, automatically formatting based on concept type.

**Parameters**:

* `conceptNameOrUuid` (String): Name or UUID of the concept to find
* `parentConceptNameOrUuid` (String, optional): Parent concept for grouped observations

**Returns**: String, Number, Date, Array, or undefined - The readable representation of the observation value

***

```javascript
// Basic usage on different entities
const treatmentDate = programEnrolment.getObservationReadableValue("Treatment Start date");
const childWeight = programEncounter.getObservationReadableValue('Weight of Child');
const mobileNumber = individual.getObservationReadableValue('Mobile Number');

// For coded concepts - returns answer names instead of UUIDs
const status = individual.getObservationReadableValue('Treatment Status'); 
// Returns: "Completed" instead of "uuid-12345"

// With grouped observations
const systolic = encounter.getObservationReadableValue('Systolic', 'Blood Pressure');

// Null-safe usage with fallback
const value = individual.getObservationReadableValue('Optional Field') || 'Not specified';

// Date formatting example
const dueDate = programEnrolment.getObservationReadableValue("Expected Date of Delivery");
// Returns: "15/03/2024" (formatted date) instead of Date object
```

***

### `getObservationValue(conceptNameOrUuid, parentConceptNameOrUuid)`

**Available on**: Individual, ProgramEnrolment, AbstractEncounter (Encounter, ProgramEncounter)

**Purpose**: Gets the raw value of an observation without formatting.

**Parameters**:

* `conceptNameOrUuid` (String): Name or UUID of the concept to find
* `parentConceptNameOrUuid` (String, optional): Parent concept for grouped observations

**Returns**: Raw value (String, Number, Date, Array, concept UUID for coded) or undefined

***

```javascript
// Get raw values for calculations
const weight = programEncounter.getObservationValue("Weight");
const height = individual.getObservationValue("Height in cm");

// For coded concepts - returns concept UUIDs
const genderUUID = individual.getObservationValue("Gender");
// Returns: "uuid-male-concept" instead of "Male"

// Use in mathematical calculations
if (height && weight) {
    const bmi = weight / ((height / 100) * (height / 100));
}

// Date comparisons with raw dates
const dueDate = programEnrolment.getObservationValue("Expected Date of Delivery");
if (dueDate && moment().isAfter(dueDate)) {
    // Pregnancy is overdue
}

// Multi-select coded values return arrays of UUIDs
const symptoms = encounter.getObservationValue("Symptoms");
// Returns: ["fever-uuid", "cough-uuid", "headache-uuid"]
```

***

### `findObservation(conceptNameOrUuid, parentConceptNameOrUuid)`

**Available on**: Individual, AbstractEncounter (Encounter, ProgramEncounter)

**Purpose**: Finds and returns the observation object itself, allowing access to all observation properties and methods.

**Parameters**:

* `conceptNameOrUuid` (String): Name or UUID of the concept to find
* `parentConceptNameOrUuid` (String, optional): Parent concept for grouped observations

**Returns**: Observation object or undefined

***

```javascript
// Find observation object
const mobileObs = individual.findObservation('Mobile Number');
const weightObs = encounter.findObservation('Weight');

// Check existence and access properties
if (mobileObs) {
    const value = mobileObs.getValue();
    const readableValue = mobileObs.getReadableValue();
    const isAbnormal = mobileObs.isAbnormal();
}

// Using with concept UUIDs
const obs = individual.findObservation('a1b2c3d4-e5f6-7890-abcd-ef1234567890');

// Grouped observations
const systolicObs = encounter.findObservation('Systolic', 'Blood Pressure Group');

// Chain operations
const weight = encounter.findObservation('Weight')?.getValue() || 0;
```

***

### `findLatestObservationInEntireEnrolment(conceptNameOrUuid, currentEncounter)`

**Available on**: ProgramEnrolment, ProgramEncounter

**Purpose**: Finds the most recent observation for a concept across the entire program enrolment lifecycle, including all encounters.

**Parameters**:

* `conceptNameOrUuid` (String): Name or UUID of the concept to find
* `currentEncounter` (ProgramEncounter, optional): Current encounter to exclude from search

**Returns**: Observation object or undefined

***

```javascript
// Track treatment progression
const latestPhase = programEnrolment.findLatestObservationInEntireEnrolment("Treatment phase type");
if (latestPhase) {
    const currentPhase = latestPhase.getReadableValue();
}

// Monitor compliance over time
const compliance = programEnrolment.findLatestObservationInEntireEnrolment("Compliance of previous month");

// Compare with previous values (excluding current encounter)
const previousWeight = programEncounter.findLatestObservationInEntireEnrolment("Weight", programEncounter);
const currentWeight = programEncounter.getObservationValue("Weight");
if (previousWeight && currentWeight) {
    const weightChange = currentWeight - previousWeight.getValue();
}

// Historical data for decision making
const lastTestResult = programEnrolment.findLatestObservationInEntireEnrolment("Lab Test Result");
const daysSinceTest = lastTestResult ? 
    moment().diff(lastTestResult.encounterDateTime, 'days') : null;
```

***

### `hasObservation(conceptNameOrUuid)`

**Available on**: AbstractEncounter (Encounter, ProgramEncounter), ProgramEnrolment

**Purpose**: Checks if an observation exists for the given concept without retrieving the value.

**Parameters**:

* `conceptNameOrUuid` (String): Name or UUID of the concept to check

**Returns**: Boolean

***

```javascript
// Conditional logic based on data availability
if (programEnrolment.hasObservation("Comorbidity")) {
    const comorbidity = programEnrolment.getObservationReadableValue("Comorbidity");
    // Process comorbidity data
}

// Form completion validation
if (!encounter.hasObservation("Blood Pressure")) {
    validationErrors.push("Blood pressure measurement is required");
}

// Check multiple required fields
const requiredFields = ['Weight', 'Height', 'Temperature'];
const missingFields = requiredFields.filter(field => !encounter.hasObservation(field));
if (missingFields.length > 0) {
    return `Missing required fields: ${missingFields.join(', ')}`;
}
```

***

## Age and Time Calculation Methods

### `getAgeInYears(asOnDate, precise)`

**Available on**: Individual

**Purpose**: Calculates age in years from the individual's date of birth.

**Parameters**:

* `asOnDate` (Date, optional): Date to calculate age as of (defaults to current date)
* `precise` (Boolean, optional): Whether to use precise calculation (defaults to false)

**Returns**: Number (age in years)

***

```javascript
// Basic usage - current age
const currentAge = individual.getAgeInYears();

// Age at specific date (enrollment, encounter, etc.)
const ageAtEnrolment = individual.getAgeInYears(programEnrolment.enrolmentDateTime);
const ageAtEncounter = individual.getAgeInYears(encounter.encounterDateTime);

// Eligibility rules
return individual.isFemale() && individual.getAgeInYears() >= 15 && individual.getAgeInYears() <= 49;

// Age-based protocols
if (individual.getAgeInYears() < 18) {
    // Pediatric protocols
    return "Pediatric dosage required";
} else if (individual.getAgeInYears() >= 65) {
    // Geriatric considerations
    return "Monitor for age-related complications";
}

// Precise calculation when needed
const preciseAge = individual.getAgeInYears(moment(), true);

// Validation
if (individual.getAgeInYears() > 120) {
    return ValidationResult.failure("age", "Age seems unrealistic");
}
```

***

### `getAgeInMonths(asOnDate, precise)`

**Available on**: Individual

**Purpose**: Calculates age in months from the individual's date of birth, particularly useful for pediatric care.

**Parameters**:

* `asOnDate` (Date, optional): Date to calculate age as of (defaults to current date)
* `precise` (Boolean, optional): Whether to use precise calculation (defaults to false)

**Returns**: Number (age in months)

***

```javascript
// Basic usage for infants and children
const ageInMonths = individual.getAgeInMonths();

// Pediatric age categories
if (individual.getAgeInMonths() < 6) {
    return "Newborn (0-6 months)";
} else if (individual.getAgeInMonths() < 12) {
    return "Infant (6-12 months)";
} else if (individual.getAgeInMonths() < 24) {
    return "Toddler (12-24 months)";
}

// Immunization scheduling
const currentMonths = individual.getAgeInMonths();
if (currentMonths >= 9 && currentMonths <= 11) {
    return "9-11 month vaccinations due";
}

// Growth monitoring protocols
if (individual.getAgeInMonths() < 24) {
    return "Monthly weight monitoring required";
} else if (individual.getAgeInMonths() < 60) {
    return "Quarterly growth assessment";
}

// Nutritional guidelines
const months = individual.getAgeInMonths();
if (months >= 6 && months < 24) {
    return "Complementary feeding period";
}
```

***

### `getAgeInWeeks(asOnDate, precise)`

**Available on**: Individual

**Purpose**: Calculates age in weeks from the individual's date of birth, useful for newborn care.

**Parameters**:

* `asOnDate` (Date, optional): Date to calculate age as of (defaults to current date)
* `precise` (Boolean, optional): Whether to use precise calculation (defaults to false)

**Returns**: Number (age in weeks)

***

```javascript
// Newborn care protocols
const ageInWeeks = individual.getAgeInWeeks();

if (ageInWeeks < 2) {
    return "First 2 weeks - daily monitoring required";
} else if (ageInWeeks <= 6) {
    return "6-week pediatric checkup due";
}

// Early immunization schedule
if (ageInWeeks >= 6) {
    return "6-week vaccinations (DPT, OPV, Hepatitis B) due";
} else if (ageInWeeks >= 10) {
    return "10-week vaccinations due";
}

// Breastfeeding support
if (ageInWeeks < 26) { // Less than 6 months
    return "Exclusive breastfeeding recommended";
}
```

***

### `getAge(asOnDate)`

**Available on**: Individual

**Purpose**: Returns age as a Duration object with appropriate units, providing smart formatting.

**Parameters**:

* `asOnDate` (Date, optional): Date to calculate age as of (defaults to current date)

**Returns**: Duration object with smart unit selection

***

```javascript
// Smart age display
const ageDuration = individual.getAge();
console.log(ageDuration.toString()); // "25 years" or "8 months" or "3 weeks"

// Use in summary strings
const summary = `${individual.name}, Age: ${individual.getAge().toString()}, ${individual.gender.name}`;

// Duration object automatically chooses appropriate units:
// - Years if age > 1 year
// - Months if age < 1 year but > 0 months  
// - Zero years if age < 1 month

// Access duration properties
const age = individual.getAge();
if (age.isInYears()) {
    // Handle adult protocols
} else if (age.isInMonths()) {
    // Handle infant protocols
}
```

***

## Cancel Encounter Methods

### `findCancelEncounterObservation(conceptNameOrUuid)`

**Available on**: AbstractEncounter (Encounter, ProgramEncounter)

**Purpose**: Finds observation from cancelled encounter data.

**Parameters**:

* `conceptNameOrUuid` (String): Name or UUID of the concept to find

**Returns**: Observation object or undefined

***

```javascript
// Find cancellation reason
const cancelReason = encounter.findCancelEncounterObservation('Cancellation reason');
if (cancelReason) {
    const reason = cancelReason.getReadableValue();
}

// Find next steps from cancelled encounter
const nextStep = programEncounter.findCancelEncounterObservation('Select next step');

// Rescheduling logic based on cancellation data
const cancelObs = encounter.findCancelEncounterObservation('Cancel reason UUID');
if (cancelObs) {
    const value = cancelObs.getValue();
    if (value === 'patient-not-available-uuid') {
        // Schedule follow-up
    }
}

// Analyze cancellation patterns
const cancelDate = encounter.findCancelEncounterObservation('Cancel date');
const cancelReason = encounter.findCancelEncounterObservation('Cancel reason');
```

***

### `findCancelEncounterObservationReadableValue(conceptNameOrUuid)`

**Available on**: AbstractEncounter (Encounter, ProgramEncounter)

**Purpose**: Gets the readable value from cancelled encounter observation.

## Related Topics

<!-- Add links to related documentation -->


---
<!-- Source: 05-javascript-rules/rules-best-practices.md -->

# Rules Development Best Practices

## TL;DR

```sql
set role <organisation_db_user>;

## Overview

```sql
set role <organisation_db_user>;

-- Subject Type
update subject_type set
    program_eligibility_check_rule = replace(program_eligibility_check_rule, 'ruleServiceLibraryInterfaceForSharingModules', 'imports'),
    last_modified_date_time = current_timestamp
    where program_eligibility_check_rule like '%ruleServiceLibraryInterfaceForSharingModules%';
update subject_type set subject_summary_rule = replace(subject_summary_rule, 'ruleServiceLibraryInterfaceForSharingModules', 'imports'),
                        last_modified_date_time = current_timestamp
    where subject_summary_rule like '%ruleServiceLibraryInterfaceForSharingModules%';

-- Encounter Type
update encounter_type set encounter_eligibility_check_rule = replace(encounter_eligibility_check_rule, 'ruleServiceLibraryInterfaceForSharingModules', 'imports'),
                          last_modified_date_time = current_timestamp
    where encounter_eligibility_check_rule like '%ruleServiceLibraryInterfaceForSharingModules%';

-- Program
update program set enrolment_summary_rule = replace(enrolment_summary_rule, 'ruleServiceLibraryInterfaceForSharingModules', 'imports'),
                          last_modified_date_time = current_timestamp
    where enrolment_summary_rule like '%ruleServiceLibraryInterfaceForSharingModules%';
update program set enrolment_eligibility_check_rule = replace(enrolment_eligibility_check_rule, 'ruleServiceLibraryInterfaceForSharingModules', 'imports'),
                          last_modified_date_time = current_timestamp
    where enrolment_eligibility_check_rule like '%ruleServiceLibraryInterfaceForSharingModules%';
update program set manual_enrolment_eligibility_check_rule = replace(manual_enrolment_eligibility_check_rule, 'ruleServiceLibraryInterfaceForSharingModules', 'imports'),
                          last_modified_date_time = current_timestamp
    where manual_enrolment_eligibility_check_rule like '%ruleServiceLibraryInterfaceForSharingModules%';

-- Form
update form set decision_rule = replace(decision_rule, 'ruleServiceLibraryInterfaceForSharingModules', 'imports'),
                   last_modified_date_time = current_timestamp
where decision_rule like '%ruleServiceLibraryInterfaceForSharingModules%';
update form set validation_rule = replace(validation_rule, 'ruleServiceLibraryInterfaceForSharingModules', 'imports'),
                   last_modified_date_time = current_timestamp
where validation_rule like '%ruleServiceLibraryInterfaceForSharingModules%';
update form set visit_schedule_rule = replace(visit_schedule_rule, 'ruleServiceLibraryInterfaceForSharingModules', 'imports'),
                   last_modified_date_time = current_timestamp
where visit_schedule_rule like '%ruleServiceLibraryInterfaceForSharingModules%';
update form set checklists_rule = replace(checklists_rule, 'ruleServiceLibraryInterfaceForSharingModules', 'imports'),
                   last_modified_date_time = current_timestamp
where checklists_rule like '%ruleServiceLibraryInterfaceForSharingModules%';
update form set task_schedule_rule = replace(task_schedule_rule, 'ruleServiceLibraryInterfaceForSharingModules', 'imports'),
                   last_modified_date_time = current_timestamp
where task_schedule_rule like '%ruleServiceLibraryInterfaceForSharingModules%';

-- Form element

update form_element set "rule" = replace("rule", 'ruleServiceLibraryInterfaceForSharingModules', 'imports'),

## Related Topics

<!-- Add links to related documentation -->


---
<!-- Source: 05-javascript-rules/rules-introduction.md -->

# Introduction to Avni Rules Engine

## TL;DR

Avni uses rules, or more accurately snippets of code (functions are written in JavaScript) in multiple places to provide flexibility to the implementers/developers to customise what Avni can do for the users. One can think of the rule system of Avni as a set of hooks that can be used by the rule ...

## Overview

Avni uses rules, or more accurately snippets of code (functions are written in JavaScript) in multiple places to provide flexibility to the implementers/developers to customise what Avni can do for the users. One can think of the rule system of Avni as a set of hooks that can be used by the rule authors to plug their own data/behaviour/logic to the app when it is used in the field and in the data entry application.

The rules are simple JavaScript functions that receive all the data via function parameters and they should return to the platform what it wants to get done. There is no state that needs to be maintained by JavaScript functions across invocations.

## Why are rules needed in Avni?

Since Avni is a general-purpose platform it doesn't know certain details about your problem domain. Wherever Avni doesn't know this - it leaves a hook for the implementer to provide the missing functionality.

## Overview of various rules

Complete programmatic reference is provided in the Writing rules, the following diagram explains how most of the rules are used. It displays navigation between the different screens and shows the rules that are triggered in the yellow boxes.

![image](https://files.readme.io/37b4a00-Screenshot_2024-02-21_at_8.51.57_PM.png)

In most rules, the rule has access to all the data of the subject and any data that is logically linked to the subject. e.g. In an encounter form level rule, one can access its subject form data, subject's relatives data, subject's relatives encounter data and so on.

#### Validation Rule

Validate the entire form. Last page of the form wizard. One per form.

#### Decision Rule

Add additional system generated observations. Last page of the form wizard. One per form.

#### Visit (Encounter) Schedule Rule

Create scheduled encounters with only due dates and no data.

#### Worklist Updation Rule

To display next forms on completion of one form.

#### Subject/Enrolment Summary

Display chosen information to summarise subject/enrolment on Subject dashboard screen.

#### Encounter/Enrolment Eligibility Check Rule

Before displaying list of forms that the user can fill check and filter out forms.

#### Manual Enrolment Eligibility Check Rule

If this rule is present, a custom form is shown to the user when the user starts enrolment. Based on the data filled and other subject data the rule decides which programs to display.

#### Edit Form Rule

If defined it can disallow editing of any form based on the rule. This rule is applied after access control is checked. This is available for: Registration, Enrolment, Enrolment Exit, Program Encounter, Program Encounter Cancel, General Encounter, General Encounter Cancel, Group Subject Registration, Form Element Group Edit and Checklist Item. It is not available/applicable for:

* Location
* Task (as there is no edit screen for it)
* SubjectEnrolmentEligibility, ManualProgramEnrolmentEligibility (these are unused features as of now)
* Encounter Drafts, Scheduled Encounters - should always be editable/fillable unless controlled by access control.

## Related Topics

<!-- Add links to related documentation -->


---
<!-- Source: 05-javascript-rules/task-schedule-rules.md -->

# Writing Task Schedule Rules

## TL;DR

Most activities in Avni are modeled as encounters with subjects, sometimes linked to a program. However, there are other kinds of data collection that happens in field work that is not related to any subject.\
eg: A list of contacts that need to be contacted first before creating subjects etc.

## Overview

Most activities in Avni are modeled as encounters with subjects, sometimes linked to a program. However, there are other kinds of data collection that happens in field work that is not related to any subject.\
eg: A list of contacts that need to be contacted first before creating subjects etc.  

To handle such flows, Avni now has a new mechanism called tasks. Tasks can currently be created only through the external API. They can be assigned to people, who can change the status of a task.

## Task Configuration

Task configuration is handled currently through SQL inserts since there are no mechanisms on the App Designer. Given below are the new concepts introduced in the task configuration. 

### Task types

A task can have a type. There are currently two kinds of task types - Call and Open Subject. A Call type task helps the user call the user, while the open subject task allows the user to navigate to the subject assigned to the task. 

### Task status

A number of statuses can be configured for a task. This helps in moving these calls into buckets. Some of these cards can be marked as "terminal" tasks. A terminal task indicates that the task is complete. 

### Task search fields

If you configure a list of concepts as task search fields, they are available in the Assignment screen for filtering. This is configured per task type

### Task metadata

Some metadata (concept:value array) can be set on a task when creating it. This will help users get more information on a task before taking actions on them. 

### Task observations

Task observations are filled in when completing a task. A new form type called "Task" is configured for this purpose. The user will be given the option to fill in the form when completing a task. 

### Standard report cards for task

There is a standard report card that can be configured for tasks. This is currently the only way tasks will be visible on the Avni android app.

## Task assignment

The web application provides a new option - "Assignment" to assign users to a task. Only one user can be assigned to a task at this time. If you assign a new user, the old user is unassigned. 

### Caveats

* Task type configuration does not have an interface on the App Designer. 
* Tasks can only be created through the external API
* Tasks can be assigned through the Assignment feature on the web application
* Tasks are not currently supported on the Data Entry App

## Related Topics

<!-- Add links to related documentation -->


---
<!-- Source: 05-javascript-rules/validation-rules.md -->

# Writing Validation Rules in Avni

## TL;DR

> 🚧 Important Update on Rules Execution
> 
> Please be informed that all existing rules stored in the rules table will become obsolete by the end of this year, 2024. This means that starting January 1, 2025, these rules will no longer be executed.

## Overview

> 🚧 Important Update on Rules Execution
> 
> Please be informed that all existing rules stored in the rules table will become obsolete by the end of this year, 2024. This means that starting January 1, 2025, these rules will no longer be executed.
> 
> However, any rules added through the App Designer and avni-health-modules will continue to work as expected.
> 
> If you have any questions or need assistance with migrating your rules, please contact our support team.

## Contents:

[Introduction](/docs/writing-rules#introduction)  
[Rule types](/docs/writing-rules#rule-types)  
[Using service methods in the rules](/docs/writing-rules#using-service-methods-in-the-rules)  
[Using other group/household individuals' information in the rules](/docs/writing-rules#using-other-grouphousehold-individuals-information-in-the-rules)  
[Types of rules and their support/availability in Data Entry App](/docs/writing-rules#types-of-rules-and-their-supportavailability-in-data-entry-app)  
[Types of rules and their support/availability in transaction data upload](/docs/writing-rules#types-of-rules-and-their-supportavailability-in-transaction-data-upload)

## Introduction:

Rules are just normal JavaScript functions that take some input and returns something. You can use the full power of JavaScript in these functions. We also provide you with some helper libraries that make it easier to write rules. We will introduce you to these libraries in the examples below.

All rule functions get passed an object as a parameter. The parameter object has two properties: 1. imports 2. params. The imports object is used to pass down common libraries. The params object is used to pass rule-specific parameters. In params object, we pass the relevant entity on which rule is being executed e.g. if a rule is invoked when a program encounter is being performed then we pass the ProgramEncounter object. The entities that we pass are an instance of classes defined in [avni-models](https://github.com/avniproject/avni-models)

### Shape of common imports object:

```javascript
{
  rulesConfig: {}, //It exposes everything exported by rules-config library. https://github.com/avniproject/rules-config/blob/master/rules.js.
  common: {}, // Library we have for common functions https://github.com/avniproject/avni-client/blob/master/packages/openchs-health-modules/health_modules/common.js
  lodash: {}, // lodash library
  moment: {}, // momentjs library
  motherCalculations: {}, //mother program calculations https://github.com/avniproject/avni-health-modules/blob/master/src/health_modules/mother/calculations.js
  log: {} //console.log object
}
```

### Shape of common parameters in all params object

Note there are other elements in params object which are specific to the rule hence have been described below.

```javascript
{    
  user, //Current User's UserInfo object  
  myUserGroups //List of Group objects, to which the User is assigned to 
}
```

User: [https://github.com/avniproject/avni-models/blob/master/src/UserInfo.js](https://github.com/avniproject/avni-models/blob/master/src/UserInfo.js)

Group: [https://github.com/avniproject/avni-models/blob/master/src/Groups.js](https://github.com/avniproject/avni-models/blob/master/src/Groups.js)

#### Entities passed to the rule

All rule receives an entity from the `params` object. Depending on the rule type an entity can be one of [Individual](https://github.com/avniproject/avni-models/blob/master/src/Individual.ts), [ProgramEncounter](https://github.com/avniproject/avni-models/blob/master/src/ProgramEncounter.js), [ProgramEnrolment](https://github.com/avniproject/avni-models/blob/master/src/ProgramEnrolment.js), [Encounter](https://github.com/avniproject/avni-models/blob/master/src/Encounter.js), or [ChecklistItem](https://github.com/avniproject/avni-models/blob/master/src/ChecklistItem.js). The shape of the entity object and the supported methods can be viewed from the above links on each entity.

## Rule types

1. [Enrolment summary rule](/docs/writing-rules#1-enrolment-summary-rule)
2. [Form element rule](/docs/writing-rules#2-form-element-rule)
3. [Form element group rule](/docs/writing-rules#3-form-element-group-rule)
4. [Visit schedule rule](/docs/writing-rules#4-visit-schedule-rule)
5. [Decision rule](/docs/writing-rules#5-decision-rule)
6. [Validation rule](/docs/writing-rules#6-validation-rule)
7. [Enrolment eligibility check rule](/docs/writing-rules#7-enrolment-eligibility-check-rule)
8. [Encounter eligibility check rule](/docs/writing-rules#8-encounter-eligibility-check-rule)
9. [Checklists rule](/docs/writing-rules#9-checklists-rule)
10. [Work list updation rule](/docs/writing-rules#10-work-list-updation-rule)
11. [Subject summary rule](/docs/writing-rules#11-subject-summary-rule)
12. [Hyperlink menu item rule](/docs/writing-rules#12-hyperlink-menu-item-rule)
13. [Message rule](https://avni.readme.io/docs/writing-rules#13-message-rule)
14. [Dashboard Card rule](https://avni.readme.io/docs/writing-rules#14-dashboard-card-rule)
15. [Manual Programs Eligibility Check Rule](https://avni.readme.io/docs/writing-rules#15-manual-programs-eligibility-check-rule)
16. [Member Addition Eligibility Check Rule](https://avni.readme.io/docs/writing-rules#16-member-addition-eligibility-check-rule)
17. [Edit Form Rule](https://avni.readme.io/docs/writing-rules#17-edit-form-rule)
18. [Global reusable code rule](https://avni.readme.io/docs/writing-rules#18-global-reusable-code-rule-alpha)


![Invocation of different rule types](https://files.readme.io/2284f79-Screenshot_2020-07-03_at_9.33.55_AM.png)


![](https://files.readme.io/baad794-Screenshot_2020-07-03_at_9.59.42_AM.png)

<hr/>

## 1. Enrolment summary rule

- Logical scope = Program Enrolment
- Trigger = Before the opening of a subject dashboard with default program selection. On program change of subject dashboard.
- In designer = Program (Enrolment Summary Rule)
- When to use = Display important information in the subject dashboard for a program

You can use this rule to highlight important information about the program on the Subject Dashboard in table format. It can pull data from all the encounters of enrolment and the enrolment itself. You can use this when the information you want to show is not entered by the user in any of the forms and is also not required for any reporting purposes (hence you wouldn't also generate this data via decision rule).

### Shape of params object:

```javascript
{ 
  summaries: [],
  programEnrolment: {}, // ProgramEnrolment model
	services,
  user, //Current User's UserInfo object  
  myUserGroups //List of Group objects  
}
```

You need to return an array of summary objects from this function.

### Shape of the summary object:

```
{
  "name": "name of the summary concept",
  "value": <text> | <number> | <date> | <datetime> | <concept list in case of Coded question>
}
```

### Example:

```
({params, imports}) =>  {
    const summaries = [];
    const programEnrolment = params.programEnrolment;
    const birthWeight = programEnrolment.findObservationInEntireEnrolment('Birth Weight');
    if (birthWeight) {
      summaries.push({name: 'Birth Weight', value: birthWeight.getValue()});
    }
    return summaries;
};
```
![](https://files.readme.io/4f29afe-Screenshot_2020-05-19_at_3.09.44_PM.png)


![](https://files.readme.io/6fdb1f3-4bf85d9-encounter-scheduling-2.png)

<hr/>

## 2. Form element rule

- Logical scope = Form Element
- Trigger = Before display of form element in the form wizard and on any change done by the user in on that page
- In designer = Form Element (RULES tab)
- When to use = 
  - Hide/show a form element
  - auto calculate the value of a form element
  - reset value of a form element

### Shape of params object:

```javascript
{
  entity: {}, //it could be one of Individual, ProgramEncounter, ProgramEnrolment, Encounter and ChecklistItem depending on what type of form is this rule attached to
  formElement: {}, //form element to which this rule is attached to
  questionGroupIndex,
  services,
  entityContext,
  user, //Current User's UserInfo object  
  myUserGroups //List of Group objects  
}
```

This function should return an instance of [FormElementStatus](https://github.com/avniproject/avni-models/blob/master/src/application/FormElementStatus.js) to show/hide the element, show validation error, set its value, reset a value, or skip answers.

To reset a value, you can use FormElementStatus._resetIfValueIsNull() method.  
You can either use FormElementStatusBuilder or use normal JavaScript to build the return value. FormElementStatusBuilder is a helper class provided by Avni that helps writing rules in a declarative way.

### Examples using FormElementStatusBuilder.

```javascript Registration Form
'use strict';
({params, imports}) => {
  const individual = params.entity;
  const formElement = params.formElement;
  const statusBuilder = new imports.rulesConfig.FormElementStatusBuilder({individual, formElement});
  statusBuilder.show().when.valueInRegistration("Number of hywas required").is.greaterThan(0);
  return statusBuilder.build();
};
```
```javascript Program Enrolment Form 1
({params, imports}) => {
  const programEnrolment = params.entity;
  const formElement = params.formElement;
  const statusBuilder = new imports.rulesConfig.FormElementStatusBuilder({programEnrolment, formElement});
  statusBuilder.show().when.valueInEnrolment('Is child getting registered at Birth').containsAnswerConceptName("No");
  return statusBuilder.build();//this method returns FormElementStatus object with visibility true if the conditions given above matches
};
```
```javascript Program Enrolment Form 2
({params, imports}) => {
    const gravidaBreakup = [
        'Number of miscarriages',
        'Number of abortions',
        'Number of stillbirths',
        'Number of child deaths',
        'Number of living children'
    ];
    const computeGravida = (programEnrolment) => gravidaBreakup
        .map((cn) => programEnrolment.getObservationValue(cn))
        .filter(Number.isFinite)
        .reduce((a, b) => a + b, 1);
    
    const [formElement, programEnrolment] = params.programEnrolment;
    const firstPregnancy = programEnrolment.getObservationReadableValue('Is this your first pregnancy?');
    const value = firstPregnancy === 'Yes' ? 1 : firstPregnancy === 'No' ? computeGravida(programEnrolment) : undefined;
    return new FormElementStatus(formElement.uuid, true, value);
};
```
```javascript Program Encounter Form
'use strict';
({params, imports}) => {
  const programEncounter = params.entity;
  const formElement = params.formElement;
  const statusBuilder = new imports.rulesConfig.FormElementStatusBuilder({programEncounter, formElement});
  const value = programEncounter.findLatestObservationInEntireEnrolment('Have you received first dose of TT');
  statusBuilder.show().whenItem( value.getReadableValue() == 'No').is.truthy;
  return statusBuilder.build();
};
```
```javascript Encounter Form
'use strict';
({params, imports}) => {
  const encounter = params.entity;
  const formElement = params.formElement;
  const statusBuilder = new imports.rulesConfig.FormElementStatusBuilder({encounter, formElement});
  statusBuilder.show().when.valueInEncounter("Are machine start and end hour readings recorded").is.yes;
  return statusBuilder.build();
};
```
```Text AffiliatedGroups
//In-order to fetch affiliatedGroups set as part of GroupAffiliation Concept in the same form,
//one needs to access params.entityContext.affiliatedGroups variable.

// Old Rule snippet
// const phulwariName = _.get(_.find(programEnrolment.individual.affiliatedGroups, ({voided}) => !voided), ['groupSubject', 'firstName'], '');

// New Rule snippet
const phulwariName = _.get(_.find(params.entityContext.affiliatedGroups, ({voided}) => !voided), ['groupSubject', 'firstName'], '');

```
![](https://files.readme.io/ece1355-Screenshot_2020-07-02_at_6.21.43_PM.png)

![](https://files.readme.io/abb6bcf-4692c21-SkipLogic.gif)

Please note that form element rules are not transitive and cannot depend on the result of another form element's form element rule. The rule logic for a particular element will need to cater to this. 

i.e. If rule C on element C depends on value of element B and rule B depends on value of element A, updating A will only update B's value and not C's value. 

<hr/>

## 3. Form element group rule

- Scope = Form Element Group
- Trigger = Before display of form element group to the user (including previous or next)
- In designer = Form Element Group (RULES tab)
- When to use = Hide/show a form element group

Sometimes we want to hide the entire form element group based on some conditions. This can be done using a form element group (FEG) rule. There is a rules tab on each FEG where this type of rule can be written. Note that this rule gets executed before form element rule so if the form element is hidden by this rule then the _form element rule_ will not get executed.

### Shape of params object:

```javascript
{
  entity: {}, //it could be one of Individual, ProgramEncounter, ProgramEnrolment, Encounter and ChecklistItem depending on what type of form is this rule attached to
  formElementGroup: {}, //form element group to which this rule is attached to
  services,
  entityContext,
  user, //Current User's UserInfo object
  myUserGroups //List of Group objects
}
```

This function should return an array of  [FormElementStatus](https://github.com/avniproject/avni-models/blob/master/src/application/FormElementStatus.js)

### Example:

```
({params, imports}) => {
    const formElementGroup = params.formElementGroup;
    return formElementGroup.formElements.map(({uuid}) => {
        return new imports.rulesConfig.FormElementStatus(uuid, false, null);
    });
};
```

<hr/>

## 4. Visit schedule rule

- Logical scope = Encounter (aka Visit), Subject, or Program Enrolment
- Trigger = On completion of an form wizard before final screen is displayed
- In designer = Form (RULES tab)
- When to use = For scheduling one or more encounters in the future

### Shape of params object:

```javascript
{
  entity: {}, //it could be one of ProgramEncounter, ProgramEnrolment, Encounter depending on what type of form is this rule attached to.
  visitSchedule: []// Array of already scheduled visits.
  entityContext
  services,
  user, //Current User's UserInfo object  
  myUserGroups //List of Group objects  
}
```

You need to return an array of visit schedules from this function.

### Shape of the return value

```
[
  <visit schedule object>
  ...
]
```

### visit schedule object

```
{
	name: "visit name", 
	encounterType: "encounter type name", 
	earliestDate: <date>, 
	maxDate: <date>,
	visitCreationStrategy: "Optional. One of default|createNew",
	programEnrolment: "<Optional. Used if you want to create a visit in a different program enrolment. If the program enrolment is tied to another subject, the visit will be schedule for that subject. Do not pass this parameter if you want to schedule a general encounter.>",
	subjectUUID: "<Optional UUID string. Used if you want to create a general visit for another subject.>"
}
```

### Example

```
({ params, imports }) => {
  const programEnrolment = params.entity;
  const scheduleBuilder = new imports.rulesConfig.VisitScheduleBuilder({
    programEnrolment
  });
  scheduleBuilder
    .add({
      name: "First Birth Registration Visit",
      encounterType: "Birth Registration",
      earliestDate: programEnrolment.enrolmentDateTime,
      maxDate: programEnrolment.enrolmentDateTime
    })
    .whenItem(programEnrolment.getEncounters(true).length)
    .equals(0);
  return scheduleBuilder.getAll();
};
```

### Example 2 - Schedule a general visit on a household when a member completes a program enrolment

```
.
.
  scheduleBuilder.add({
      name: "TB Family Screening Form",
      encounterType: "TB Family Screening Form",
      earliestDate: imports.moment(programEnrolment.encounterDateTime).toDate(),
      maxDate: imports.moment(programEnrolment.encounterDateTime).add(15, 'days').toDate(),
      subjectUUID: programEnrolment.individual.groups[0].groupSubject.uuid
  });
.
.
```
![](https://files.readme.io/42b7d6b-Screenshot_2020-05-19_at_7.04.19_PM.png)


![](https://files.readme.io/cbaef6a-4fff50b-encounter-scheduling-1.png)

### Strategies that Avni uses.

For all the visit schedules that are returned, Avni evaluates how to create a visit. Assume you provide the default visitCreationStrategy (this is the default behaviour). Avni checks if there is already a scheduled visit for the given encounter type. If it is there, then it is updated with the incoming scheduled visit's name and other parameters. This strategy works well in most cases. 

- Remember that the VisitSchedule rule gets called whether you create a visit, or edit it. 
- Remember not to send multiple visit schedule objects for the same encounter type. If you do, the last one will overwrite the previous objects. 

### Using the "createNew" visit strategy

Do this only if you know what you are doing. If you add visitCreationStrategy of "createNew", then a new visit will be created no matter what. 

You need to be careful while using this strategy because, in edit scenarios, we might end up creating the same kind of visits multiple times. 

### Using the VisitScheduleBuilder.getAllUniqueVisits

VisitSchedulBuilder class has a getAllUniqueVisits method that provides some shortcuts to reduce the cruft you might have to do while creating scheduled visits. It mostly does the right thing, so you don't have to worry about its logic. However, if you think it is doing something you didn't intend, then you can replace it with your own implementation. Look up the [code](https://github.com/avniproject/rules-config/blob/master/src/rules/builder/VisitScheduleBuilder.js) for more details. 

<hr/>

## 5. Decision rule

- Logical scope = Encounter (aka Visit), Subject, or Program Enrolment
- Trigger = On completion of an form wizard before final screen is displayed
- In designer = Form (RULES tab)
- When to use = To create any additional observations based on all the data filled by the user in the form

Used to add decisions/recommendations to the form. The decisions are displayed on the last page of the form and are also saved in the form's observations.

### Shape of params object:

```javascript
{
	entity: {}, //it could be ProgramEncounter, ProgramEnrolment or Encounter depending on what type of form is this rule attached to.
 	entityContext,
  services,
  user, //Current User's UserInfo object  
  myUserGroups, //List of Group objects  
  decisions: {
     	"enrolmentDecisions": [],
    	"encounterDecisions": [],
      "registrationDecisions": []
  } // Decisions object on which you need to add decisions. 
}
```

### Shape of decisions parameter:

```javascript
{
  "enrolmentDecisions": [],
  "encounterDecisions": [],
  "registrationDecisions": []
}
```

You need to add `<decision object>` to decisions parameter's appropriate field and return it back.  
Inside the function, you will build decisions using ComplicationsBuilder and push the decisions to the decisions parameter's appropriate field. The return value will be the modified decisions parameter. You can also choose to not use ComplicationsBuilder and directly construct the return value as per the contract shown below:

### Shape of the return value

```
{
  "enrolmentDecisions": [<decision object>, ...],
  "encounterDecisions": [<decision object>, ...],
  "registrationDecisions": [<decision object>, ...]
}
The shape of <decision object>
{
  "name": "name of the decision concept",
  "value": <text> | <number> | <date> | <datetime> | <name of anwer concepts in case of Coded question>
}
```

### Example

```
({params, imports}) => {
    const programEncounter = params.entity;
    const decisions = params.decisions;
    const complicationsBuilder = new imports.rulesConfig.complicationsBuilder({
        programEncounter: programEncounter,
        complicationsConcept: "Birth status"
    });
    complicationsBuilder
        .addComplication("Baby is over weight")
        .when.valueInEncounter("Birth Weight")
        .is.greaterThanOrEqualTo(8);
    complicationsBuilder
        .addComplication("Baby is under weight")
        .when.valueInEncounter("Birth Weight")
        .is.lessThanOrEqualTo(5);
    complicationsBuilder
        .addComplication("Baby is normal")
        .when.valueInEncounter("Birth Weight")
        .is.lessThan(8)
        .and.when.valueInEncounter("Birth Weight")
        .is.greaterThan(5);
    decisions.encounterDecisions.push(complicationsBuilder.getComplications());
    return decisions;
};
```
![](https://files.readme.io/f0f898a-Screenshot_2020-05-19_at_7.09.58_PM.png)


![](https://files.readme.io/4b488cc-4fff50b-encounter-scheduling-1.png)

<hr/>

## 6. Validation rule

- Logical scope = Encounter (aka Visit), Subject, or Program Enrolment
- Trigger = On completion of an form wizard before final screen is displayed
- In designer = Form (RULES tab)
- When to use = To provide validation error(s) to the user that are not specific to one form element but involved data in multiple form elements.

Used to stop users from filling invalid data

### Shape of params object:

```
{
  entity: {}, //it could be ProgramEncounter, ProgramEnrolment or Encounter depending on what type of form is this rule attached to.
  entityContext,
  services,
  user, //Current User's UserInfo object  
  myUserGroups //List of Group objects  
}
```

The return value of this function is an array with validation errors.

### Example:

```
({params, imports}) => {
  const validationResults = [];
  if(programEncounter.getObservationReadableValue('Parity') > programEncounter.getObservationReadableValue('Gravida')) {
    validationResults.push(imports.common.createValidationError('Para Cannot be greater than Gravida'));
  }
  return validationResults;
};
```
![](https://files.readme.io/fb8e5df-Screenshot_2020-05-19_at_7.14.05_PM.png)

<hr/>

## 7. Enrolment Eligibility Check Rule

- Logical scope = Subject
- Trigger = On launch of program list when user enrols a subject into program
- In designer = Program page
- When to use = To restrict the programs which are available for enrolment based on subject's data (e.g. not allowing males to enrol in pregnancy programs)

### Shape of params object:

```
{
  entity: {}//Subject will be passed here.
  program,
  services,
  user, //Current User's UserInfo object  
  myUserGroups //List of Group objects  
}
```

### Shape of the return value

The return value of this function should be a boolean.

### Example:

```
({params, imports}) => {
  const individual = params.entity;
  return individual.isFemale() && individual.getAgeInYears() > 5;
};
```

**Notes**: The eligibility check is triggered only when someone tries to create a visit manually. Form stitching rules can override this default behaviour. 
![](https://files.readme.io/bc76050-Screenshot_2020-05-20_at_3.57.52_PM.png)


![](https://files.readme.io/ba63cb1-cbe944e-Screenshot_2019-11-20_at_6.51.40_PM.png)

<hr/>

## 8. Encounter Eligibility Check Rule

- Logical scope = Subject or Program Enrolment
- Trigger = On launch of new visit (encounter) list
- In designer = Encounter page
- When to use = To restrict the encounters which are available based on subject's full data (e.g. not showing postnatal care form if the delivery form has not been filed yet)

Used to hide some visit types depending on some data. If there existed scheduled encounters for that subject or program enrolment, clicking on an ineligible visit type, will fill up the scheduled encounter. 

### Shape of params object:

```javascript
{
  entity: {}//Subject will be passed here.
  services,
  user, //Current User's UserInfo object  
  myUserGroups //List of Group objects  
}
```

### Shape of the return value

The return value of this function should be a boolean.

### Example:

```
({params, imports}) => {
  const individual = params.entity;
  const visitCount = individual.enrolments[0].encounters.filter(e => e.encounterType.uuid === 'a30afe96-cdbb-42d9-bf30-6cf4b07354d1').length;
  let visibility = true;
  if (_.isEqual(visitCount, 1)) visibility = false;
  return visibility;
};
```

**Notes**: The eligibility check is triggered only when someone tries to create a visit manually. Form stitching rules can override this default behaviour. 
![](https://files.readme.io/0d034b9-Screenshot_2020-05-20_at_4.02.24_PM.png)

<hr/>

## 9. Checklists rule

Used to add a checklist to an enrolment

### Shape of params object:

```javascript
{
  entity: {} //ProgramEnrolment
  checklistDetails: [] // Array of ChecklistDetail
  services,
  user, //Current User's UserInfo object  
  myUserGroups //List of Group objects  
}
```

### Example

```
({params, imports}) => {
  let vaccination = params.checklistDetails.find(cd => cd.name === 'Vaccination');
  if (vaccination === undefined) return [];
  const vaccinationList = {
    baseDate: params.entity.individual.dateOfBirth,
    detail: {uuid: vaccination.uuid},
    items: vaccination.items.map(vi => ({
      detail: {uuid: vi.uuid}
    }))
  };
  return [vaccinationList];
};
```

<hr/>

## 10. Work List Updation rule

- Logical scope = Subject, Program Enrolment, or Encounters
- Trigger = On display of system recommendation's page in form wizard
- In designer = Main Menu
- When to use = Stitch together multiple forms which can be filled back to back

The System Recommendations screen of Avni can be configured to direct a user to go to the next task to be done. Typically, if a new encounter is scheduled for a person on the same day, then the system automatically prompts the user to perform that encounter.  
This is performed using worklists. A worklist is an array of [work items](https://github.com/avniproject/avni-models/blob/master/src/application/WorkItem.js). 

The WorkListUpdation rule is used to customize this flow. The WorkLists object is passed on to this rule just before showing the System Recommendations screen. Any modification in the worklists is applied immediately to the flow. 

You can add a new WorkItem anywhere after the currentWorkList.currentItem. 

### Shape of params object:

```javascript
{
  worklists: {},
  context: {},
  services,
  user, //Current User's UserInfo object  
  myUserGroups //List of Group objects  
}
```

### Example

[https://gist.github.com/hithacker/d0fe89107b974797fbb11ced1feda146](https://gist.github.com/hithacker/d0fe89107b974797fbb11ced1feda146)
![](https://files.readme.io/ef3535d-Screenshot_2020-05-21_at_3.25.33_PM.png)


<hr/>

## 11. Subject summary rule

- Logical scope = Subject registration
- Trigger = Before the opening of the subject dashboard profile tab.
- In designer = Subject (Subject Summary Rule)
- When to use = Display important information in the subject's profile. It can be used to show the summary if there are no programs.

This rule is very similar to the Enrolment summary rule. Except its scope is the Subject's registration.

### Shape of params object:

```
{ 
  individual: {}, // Subject model,
  user, //Current User's UserInfo object  
  myUserGroups //List of Group objects  
}
```

You need to return an array of summary objects from this function.

### Shape of the summary object:

```
{
  "name": "name of the summary concept",
  "value": <text> | <number> | <date> | <datetime> | <concept list in case of Coded question>
}
```

### Example:

```
({params, imports}) =>  {
    const summaries = [];
    const individual = params.individual;
    const mobileNumber = individual.findObservation('Mobile Number'); 
    if(mobileNumber) {
      summaries.push({name: 'Mobile Number', value: mobileNumber.getValueWrapper()});
    }
    return summaries;
};
```

<hr/>

## 12. Hyperlink menu item rule

- Logical scope = User
- Trigger = When More navigation is opened in the mobile app
- In designer = Coming very soon...
- When to use = When a dynamic link has to be provided to the user (these links cannot be specific to subjects)

### Shape of params object:

```
{
  user: {}, // User
  moment: {}, // moment. note other parameters are not supported yet,
  token, //Auth-token of the logged-in user
  myUserGroups //List of Group objects  
}
```

User: [https://github.com/avniproject/avni-models/blob/master/src/UserInfo.js](https://github.com/avniproject/avni-models/blob/master/src/UserInfo.js)

You need to return a string that is the full URL that can be opened in a browser.

### Example:

```
({params}) => {return `https://reporting.avniproject.org/public/question/11265388-5909-438e-9d9a-6faaa0c5863f?username=${encodeURIComponent(user.username)}&name=${encodeURIComponent(user.name)}&month=${imports.moment().month() + 1}&year=${imports.moment().year()}`;}
```

<hr/>

## 13. Message rule

- When to use =  To configure sending Glific messages
- Logical scope = User, Subject, General and Program Encounter, Program Enrolment
- Trigger = 
  - For User : Only on creation of an User . 
  - For Subject, General and Program Encounter, Program Enrolment : On every save (create / update)
- In designer = "User Messaging Config", "Subject Type" , "Encounter type" and "Programs" page

Message Rule can be configured only when 'Messaging' is enabled for the organisation. Its configuration constitutes specifying following details:

- **Name** identifier name for the Message Rule
- **Template** Used to indicate the Skeleton of the message with placeholders for parameters
- **Receiver Type** Used to indicate the target audience for the Glific Whatsap message
- **Schedule** date and time configuration should return the time to send the message.
- **Message** content configuration should return the parameters to be filled in the Glific message template selected under 'Select Template' dropdown.

 Any number of message Rules can be configured.

### Example configuration:

Say, 'common_otp' Glific message template is 'Your OTP for `{{1}}` is `{{2}}`. This is valid for `{{3}}`.' If we want to send a OTP message that says 'Your OTP for receiving books is 1458. This is valid for 2 hours.' to a student after 1 day of their registration, then we need to configure for student subject type as shown in the below image (Note the shape of the return objects): 
![](https://files.readme.io/2e3e442-Screenshot_2023-12-27_at_6.15.54_PM.png)

```Text Schedule
'use strict';  
({params, imports}) => ({  
  scheduledDateTime: new Date("2023-01-05T10:10:00.000+05:30")  
});
```
```text Message
'use strict';  
({params, imports}) => {  
  const individual = params.entity;  
  return {  
    parameters: ['Verify user phone number', '0123', '1 day']  
  }  
};
```

### Shape of params object:

```
{
  entity: {}, //it could be one of User, Individual, General Encounter, ProgramEncounter or Program Enrolment depending on the type of form this rule is attached to
  user, //Current User's UserInfo object  
  myUserGroups //List of Group objects  
}
```

## 14. Dashboard Card Rule

The shape of dashboard card rule

```javascript
{
  db: "the realm db instance",
  user,
  myUserGroups,
  // ruleInput object can be null
  ruleInput: {
    type: "string. see 14.1 below",
    dataType: "values can be Default or Range",
    subjectType: "SubjectType model object. The subject type of the subjects to query and display to the user",
    groupSubjectTypeFilter: {
      subjectType: "SubjectType. The group subject type to filter by"
    },
    observationBasedFilter: {
      scope: "string. See 14.2 below",
      concept: "Concept. the observation value being referred to by the filter value",
      programs: {
         "UUID of the program": "Program model object"
      },
      encounterTypes: {
         "UUID of the encounter type": "Encounter Type model object"
      }
    },
    // filterValue can be null or empty array when there are no filters chosen by the user
    filterValue: "value chosen by the user. the type of data depends on the type of the filter"
  }
}
```

### Filter Value Shapes

**Address Filter**

```json
{
  "uuid":"924674dc-d32b-4276-b7b5-fb782f5511f2",
  "name":"Kerala",
  "level":4,
  "type":"State",
  "parentUuid":null,
}
```


14.1) [https://github.com/avniproject/avni-models/blob/8613b53edbf88e9b19150eda9e13da573e2a59ba/src/CustomFilter.js#L2](https://github.com/avniproject/avni-models/blob/8613b53edbf88e9b19150eda9e13da573e2a59ba/src/CustomFilter.js#L2)

14.2) [https://github.com/avniproject/avni-models/blob/8613b53edbf88e9b19150eda9e13da573e2a59ba/src/CustomFilter.js#L30](https://github.com/avniproject/avni-models/blob/8613b53edbf88e9b19150eda9e13da573e2a59ba/src/CustomFilter.js#L30)

<hr/>

### 15. Manual Programs Eligibility Check Rule

This rule is used when the user fills a form based on which the eligibility of given program is determined by this rule.

#### Shape of Input Object

```javascript
params: {
  entity: typeof SubjectProgramEligibility,
  subject: typeof Individual,
  program: typeof Program,
  services,
  user, //Current User's UserInfo object  
  myUserGroups //List of Group objects  
},
imports: {}
```

#### Return

_boolean_

### 16. Member Addition Eligibility Check Rule

This rule is used to determine whether an **existing** member can be added to a group or household. The rule is configured at the subject type level and is executed when a user attempts to add an existing member to a group/household.

- Logical scope = Group/Household and Individual
- Trigger = On attempt to add a member to a group/household
- In designer = Subject Type (Member Addition Eligibility Check Rule)
- When to use = To validate if an **existing** individual can be added as a member to a specific group/household based on custom business rules

#### Shape of Input Object

```javascript
params: {
  member: typeof Individual, // The individual being added as a member
  group: typeof Individual, // The group/household to which the member is being added
  context: Object, // The execution context
  services,
  user, // Current User's UserInfo object  
  myUserGroups // List of Group objects  
},
imports: {}
```

#### Return

This rule should return an object that follows the ActionEligibilityResponse format, with the following structure:

```javascript
// For allowing addition
{
  eligible: {
    value: true
  }
}

// For disallowing addition with a reason
{
  eligible: {
    value: false,
    message: "Reason why the member cannot be added" //Value of message has translation support.
  }
}
```

#### Example

**Use Case:**

While adding members to a "Self-help" group, we need to validate that the person is an adult, in-which case we would come up with the following

**Member Addition Eligibility Check Rule:**

```javascript
"use strict";
({params, imports}) => {
  const member = params.member;
  const group = params.group;
  
  // Example: Only allow adding members who are above 18 years of age
  const age = member.getAgeInYears();//As on current date
  
  if (age < 18) {
    return {
      eligible: {
        value: false,
        message: "Only individuals above 18 years can be added to this group"
      }
    };
  }
  
  return {
    eligible: {
      value: true
    }
  };
};
```

**Reference Screenshot, when Member Addition Eligibility Check Rule fails:**
![](https://files.readme.io/aaa48f09aa4c5bcaebf2d9ae72f19c0777e719bd463b213b43e011796fd8db0a-Screenshot_2025-06-27_at_7.41.28_PM.png)

#### Error Handling

When a Member Addition Eligibility Check rule fails (throws an exception), the error is logged and stored in the RuleFailureTelemetry with the following information:

- source_type: 'MemberAdditionEligibilityCheck'
- source_id: UUID of the subject type
- entity_type: 'Individual'
- entity_id: UUID of the group/household to which a member is being added
- individual_uuid: UUID of the individual being added to the group/household

### 17. Edit Form Rule

This rule is used when the user tries to edit a form. If non-boolean value is returned in the value, or the rule fails, then it would be treated as true and edit will be allowed. To check the places where it is available, not available, & not applicable - [https://avni.readme.io/docs/rules-concept-guide#edit-form-rule](https://avni.readme.io/docs/rules-concept-guide#edit-form-rule).Value of message has translation support.

#### Sample Rule

```
"use strict";
({params, imports}) => {
    const {entity, form, services, entityContext, myUserGroups, userInfo} = params;

    const output = {
      eligible : {
        value: false, //return false to disallow, true to allow;
        message: 'Edit access denied: <Specify reason here>.' //optional
      } 
    }; 

    return output;
};
```

#### Shape of Input Object

```javascript
params: {entity, services, form, myUserGroups,user},
imports: {}
```

#### Shape of return object

```javascript
// Previous format (still supported)
const output = {
  editable : {
    value: true/false,
    messageKey: 'foo'
  }
};

// New format (generic for all rule based access control)
const output = {
  eligible : {
    value: true/false,
    message: 'foo'
  }
};
```

### 18. Global reusable code rule (Alpha)

This rule is intended maintaining reusable JavaScript functions across implementations. While this could also be used within implementation only but that is not the purpose of this. If you want to create reusable JavaScript code within an implementation only, please check with the product management team to get it prioritised.

> 📘 Not supported in Data entry app. Feature available from 11.0 version.

#### Shape of Input Object

```javascript
// Get handle to the reusable function
const globalFunction = imports.globalFn;
// invoke your function, two examples below.
globalFn().hello();
globalFn().sum(1,2);
```

Note that you can define the signature of your new function (like hello, sum). It is not determined by the global function.

#### How to deploy global function (TBD)

1. Use `make deploy-global-rule`.
   1. Provide the origin and token
   2. The token will determine the organisation to which it is deployed. Rerunning it will update the previous rule.
2. Run sync in the mobile app

## Accessing Address Level Properties :

Old Way is to get the address level properties and extract from the json object. In new way, get the address level and access its observation value as per location attribute form.

```Text JavaScript
'use strict';
({params, imports}) => {
  const programEncounter = params.entity;
  const moment = imports.moment;
  const formElement = params.formElement;
  const _ = imports.lodash;
  let visibility = false;
  let value = 'No';
  let answersToSkip = [];
  let validationErrors = [];
  
  const address_level = programEncounter.programEnrolment.individual.lowestAddressLevel;  
  
  const gHighRisk = address_level.getObservationReadableValue("Geographically hard to reach village");

  if(gHighRisk === "Yes"){
      value = 'Yes';
  }

  
  return new imports.rulesConfig.FormElementStatus(formElement.uuid, visibility, value, answersToSkip, validationErrors);
};
```

## Handling rule-evaluation across Mobile and Web Applications

This section provides guidelines for handling rule-evaluation across Mobile and Web Applications in Avni implementations. It includes practical examples from the Goonj implementation.

### Detecting Web Application Context

To determine if the application is running in a web context, you can check the `titleLineage` property of the lowest address level:

```javascript
const webapp = individual.lowestAddressLevel.titleLineage;
```

This pattern is used to identify if the application is running in a web context and adjust behavior accordingly.

### Handling Webapp-Specific Scenarios

When working with web applications, consider the following:

- Some validations might need to be bypassed in web context
- UI/UX might need adjustments for web vs mobile
- Performance considerations might differ between platforms

#### Basic Pattern

```javascript
function handleWebappContext(individual) {
    const webapp = individual.lowestAddressLevel.titleLineage;
    
    // Apply webapp-specific logic
    if (webapp) {
        // Webapp-specific code here
    } else {
        // Mobile-specific code here
    }
}

try {
    handleWebappContext(individual);
} catch (error) {
    console.error('Error handling webapp context:', error);
}
```

#### Examples

In the Goonj implementation, we encountered an issue where certain validations were failing in the web context but were not applicable to web users.

##### 1. Webapp Detection and Validation Bypass

```javascript
function validateForm(individual, formData) {
    const webapp = individual.lowestAddressLevel.titleLineage;
    const errors = [];
    
    // Skip webapp-specific validations for web users
    if (!webapp) {
        // Mobile-only validations go here
        if (!formData.requiredField) {
            errors.push('This field is required for mobile users');
        }
    }
    
    // Common validations for both web and mobile
    if (!formData.commonField) {
        errors.push('This field is required for all users');
    }
    
    return errors.length ? errors : null;
}
```

##### 2. Location Validation Example

```javascript
function validateLocation(individual, locationData) {
    const webapp = individual.lowestAddressLevel.titleLineage;
    
    // Skip location validation for webapp
    if (webapp) {
        return null;
    }
    
    // Mobile location validation logic
    if (!locationData || !locationData.coordinates) {
        return ['Location is required for mobile users'];
    }
    
    return null;
}
```

## Accessing audit fields when writing rules

#### When writing rules, you often need to access information about who created or modified entities, and when these actions occurred. Avni provides several audit fields that can be accessed through the entity object in your rules.

Available Audit Fields

  The following audit fields are available :

- createdByUUID
- lastModifiedByUUID
- createdBy
- lastModifiedBy
- filledBy (only for program and general encounters)
- filledByUUID (only for program and general encounters)

```coffeescript JS
//SAMPLE EDIT FORM RULE
  "use strict";
({params, imports}) => {
const {entity} = params;
console.log("params.entity.createdByUUID:", params.entity.createdByUUID);
console.log("params.entity.lastModifiedByUUID:", params.entity.lastModifiedByUUID);

console.log("params.entity.createdBy:", params.entity.createdBy);
console.log("params.entity.lastModifiedBy:", params.entity.lastModifiedBy);

console.log("params.entity.filledBy:", params.entity.filledBy);
console.log("params.entity.filledByUUID:", params.entity.filledByUUID);

return output;
};
```

## Using params.db object when writing rules

In many of the rules params db object is available to query the offline database directly. The db object is an instance of type [Realm](https://www.mongodb.com/docs/realm-sdks/js/latest/classes/Realm-1.html) on which [objects](https://www.mongodb.com/docs/realm-sdks/js/latest/classes/Realm-1.html#objects) is first method that will get called. This returns [Realm Results](https://www.mongodb.com/docs/realm-sdks/js/latest/classes/Results.html) instance, on which one may further call the [filtered](https://www.mongodb.com/docs/realm-sdks/js/latest/classes/Results.html#filtered) method one or more times each time returning realm results. Realm result a list with each item being of type (model object's schema name) originally passed in objects method.

```coffeescript JS
'use strict';
({params, imports}) => {
  //...
  
  const db = params.db;
  const farmers = db.objects("Individual").filtered(`voided = false AND subjectType.uuid = "73271784-512d-4435-8dc8-0f102b99d682"`);
  console.log('Found farmers with count', farmers && farmers.length > 0 && farmers.length);

  //...
  return new imports.rulesConfig.FormElementStatus(formElement.uuid, visibility, value, answersToSkip, validationErrors);
};
```


**Realm Query Language Reference** - [https://www.mongodb.com/docs/realm/realm-query-language](https://www.mongodb.com/docs/realm/realm-query-language)

### Difference between filter and filtered

`filtered` method is like running SQL query executed closer or in the database process and hence it orders of magnitude faster than `filter` - which is JavaScript method ran by constructing model object for each item is JS memory and then passing it through the filter function. As much as possible filtered should be used for best performance and user experience.

### Example of filtered

```javascript
({params}) => {
  const db = {params};
  return db.objects("Individual").filtered(`voided = true AND subjectType.name = "Foo"`);
}
```

## Using service methods in the rules

Often, there is the need to get the context of implementation beyond what the models themselves provide. For example, knowing other subjects in the location might be necessary to run a specific rule. For such scenarios, Avni provides querying the DB using the services passed to the rules.

The services object looks like this

```javascript
{
    individualService: '',
}
```

Right now only individual service is injected into all the rules. One method which is implemented right now returns an array of subjects in a particular location. The method looks like the following, it takes address-level object and subject type name as its parameters and returns a list of all the subjects in that location.

```javascript
getSubjectsInLocation(addressLevel, subjectTypeName) {
  const allSubjects = ....;
  return allSubjects;
}
```

Note that this function is not implemented for the data entry app and throws a "method not supported" error for all the rules when run from the data entry app.

### Service methods available are:

- [https://github.com/avniproject/avni-client/blob/master/packages/openchs-android/src/service/facade/IndividualServiceFacade.js](https://github.com/avniproject/avni-client/blob/master/packages/openchs-android/src/service/facade/IndividualServiceFacade.js)
- [https://github.com/avniproject/avni-client/blob/master/packages/openchs-android/src/service/facade/AddressLevelServiceFacade.js](https://github.com/avniproject/avni-client/blob/master/packages/openchs-android/src/service/facade/AddressLevelServiceFacade.js)

### Examples

The view-filter rule is for the subject data type concept that displays all the subjects of type 'Person' in the passed location. 

```
'use strict';
({params, imports}) => {
  const encounter = params.entity;
  const formElement = params.formElement;
  const statusBuilder = new imports.rulesConfig.FormElementStatusBuilder({encounter, formElement});
  const individualService = params.services.individualService;
  const subjects = individualService.getSubjectsInLocation(encounter.individual.lowestAddressLevel, 'Person');
  const uuids = _.map(subjects, ({uuid}) => uuid);
  statusBuilder.showAnswers(...uuids);
  return statusBuilder.build();
};
```


#### Fetch Subjects by Subject Type with Custom Filtering

For business reasons, you may need to fetch subjects of a specific type with additional filtering criteria.

##### Using IndividualServiceFacade "getSubjects" method

Use IndividualServiceFacade`getSubjects(subjectTypeName, realmFilter)` method to get subjects by type with optional filtering.

##### Method Signature

- subjectTypeName (string): The name of the subject type (e.g., 'Volunteer', 'Patient', 'Household')
- realmFilter (string, optional): Realm query filter string for additional filtering

```js

  const individualService = params.services.individualService;
  const volunteers = individualService.getSubjects('Volunteer');
  console.log('volunteers:', volunteers.length);

  const subjectsWithObservation = individualService.getSubjects(
    'Patient',
    'SUBQUERY(observations, $obs, $obs.concept.uuid == "concept-uuid-here").@count > 0'
  );
  console.log('Patients with specific observation:', subjectsWithObservation.length);

  
```

## Using other group/household individuals' information in the rules

Say, an individual belongs to a group A. Sometimes, there is a need to use data of other individuals in the group A.  For example, to auto-populate caste information in an individual's registration form (say, when navigated to individual's registration form when tried to add a member to group/household A), we might need to know the caste information of other individuals in that group/household. For such scenarios, Avni provides a way to access `group` object from `params.entityContext`.

### Example

The below rule is for the case when an individual's concept named `Caste` needs to be auto-populated based on other member's data in the same group.

```
'use strict';
({params, imports}) => {
  const individual = params.entity;
  const moment = imports.moment;
  const formElement = params.formElement;
  const _ = imports.lodash;
  let visibility = true;
  let value = null;
  let answersToSkip = [];
  let validationErrors = [];
  
  const groupSubject = params.entityContext.group;
  if(groupSubject.groupSubjects.length > 0) {
     const ind = params.entityContext.group.groupSubjects[0].memberSubject;
     const caste = ind.getObservationReadableValue('Caste');
     value = caste; 
  }
  
  return new imports.rulesConfig.FormElementStatus(formElement.uuid, visibility, value, answersToSkip, validationErrors);
};
```

## Handling special scenarios while updating value using FormElementStatus rule

### How to reset value using FormElement Rule logic

When the FormElementStatus value is set to null, by default it is treated as a No-action operation and hence we do not reset the value of the concept.

But instead, if we are trying to say that "I am not setting the value", and any previous value has to be reset, then we need to specify the resetValueIfNull argument to be **true** in the FormElementStatus constructor, used to generate response during the rule execution.

```
'use strict';
({params, imports}) => {

//Rule content
  
//FormElementStatus Constructor signature
return new imports.rulesConfig.FormElementStatus(formElementUUID, visibility, value, answersToSkip = [], validationErrors = [], answersToShow = [], resetValueIfNull = false);
}
```


### Handle set of Modifiable Select Coded Concepts

In-order to init a modifiable Select Coded Concept FormElement's Value in a form, you can specify the AnswerConcept **Name** as the value, which should be enough to set the initial value as expected.

### Handle set of Read-Only Select Coded Concepts

There were 2 issues that were preventing implementation team from reliably setting a **Read-only** SingleSelectCodeConcept's value via FormElement Rules:

1. Selection of a AnswerConcept
2. Stablizing the selected value over multiple execution of FormElement rule due to changes elsewhere in the FormElementGroup

#### Recommended solution

To resolve these issues, we only needed to make following adjustments in the FormElement Rule:

1. Selection of a AnswerConcept => Make use of AnswerConcept's UUID instead of name as value
2. Stablizing the selected value  => 
   > - Mark the SelectedCodedConcept value as ReadOnly 
   > - For Multi-select: Return a FormElementStatus object with only the difference between previous valueArray and new valueArray. If no change in value, then return empty array.
   > - For Single-select: Return a FormElementStatus object with selected value, only if previousValue was null. If not, return null.

This would toggle the answers as expected and result in only the expected value(s) being shown as selected. 

#### Example Rule for SingleSelect FormElement set via Rule

```javascript
'use strict';
({params, imports}) => {
  const individual = params.entity;
  const moment = imports.moment;
  const formElement = params.formElement;
  const _ = imports.lodash;
  let visibility = true;
  let value = null;
  let answersToSkip = [];
  let validationErrors = [];
    
    const condition11 = triue; //some visibility condition
    visibility = condition11;
     
    if (condition11) {
       //some business logic
          if(someCondition) {
             value = "conceptUUID1";
          }
          else{
             value = "conceptUUID2";
          }
       }
    }
    let que = individual.findGroupedObservation('bafb80ac-6088-4649-8ed3-0501e1296c6e')[params.questionGroupIndex];
    if(que){
      let obs = que.findObservationByConceptUUID('ef952d55-f879-4c34-99e2-722c680ed2e2');
      if(obs && obs.getValue() === value) {//i.e obs.getValue() are both same answerConcept
         return null;//Old value is retained
       }   
    }
    else {
       return new imports.rulesConfig.FormElementStatus(formElement.uuid, visibility, value, answersToSkip, validationErrors); //new value is updated
    }
};
```

### Handle Uniqueness validation for Read-Only Text field

As the value for the ReadOnly TextFormElement is set via Rule of some sort, the validation for enforcing uniqueness too has to be done during the same rule execution.

#### Example FE rule for enforcing Uniqueness validation on Read-only Text field

```Text Javascript
'use strict';
({params, imports}) => {
    const individual = params.entity;
    const moment = imports.moment;
    const _ = imports.lodash;
    const formElement = params.formElement;
    let visibility = true;
    let value = null;
    let validationErrors = [];
    let nameNotUnique = false;
    
    
   //Business logic to set value
   value = '[dummy3]as';


    //Execute some business logic to update nameNotUnique 
    nameNotUnique = (value === '[dummy3]as');
    
    if(nameNotUnique) {
       validationErrors.push('Another Work Order has same value');
    }
   
    return new imports.rulesConfig.FormElementStatus(formElement.uuid, visibility, value, null, validationErrors);
};

```


### Handle Fetch of Individuals with specific Phone Numbers for duplicates validation

For business reasons, we might need to verify that there are **No / Limited number of** duplicate Subjects with the same Phone Number. To do this, we have 2 possible approaches:

#### 1. Use IndividualServiceFacade "findAllSubjectsWithMobileNumberForType" helper method

Use IndividualServiceFacade.findAllSubjectsWithMobileNumberForType(mobileNumber, subjectTypeUUID) method to get subjects with same phone number.

**Requires the PhoneNumber concept to have, KeyValue (primary_contact : yes) or (contact_number : yes)**
![](https://files.readme.io/f48da098be8218e797e7dd841e023036199eb0b7aa696ece422a6974e0b3f56f-421821795-e7b7766d-3865-4a66-a66e-93f4ddc8b13d.png)

```js

  const individualService = params.services.individualService;
  const subjects = individualService.findAllSubjectsWithMobileNumberForType('', "<subject_type_uuid>");
  console.log('found subjects with number', subjects && subjects.length > 0);
  
```

#### 2. [Using params.db object to find duplicates with custom filter logic](/docs/writing-rules#using-paramsdb-object-when-writing-rules)

## Types of rules and their support/availability in Data Entry App

| Not supported                          | Supported via rules-server       | Supported in browser     |
| :------------------------------------- | :------------------------------- | :----------------------- |
| Global reusable function               | Enrolment eligibility check rule | Form Element Rule        |
| Dashboard Card rule (NA)               | Encounter eligibility check rule | Form Element GroupRule   |
| Checklists rule                        | Visit schedule rule              | Enrolment Summary Rule   |
| Work list updation rule                | Message rule                     | Hyperlink menu item rule |
| Hyperlink menu item rule               | Decision rule                    |                          |
| Validation rule                        |                                  |                          |
| Edit Form rule                         |                                  |                          |
| Member addition eligibility check rule |                                  |                          |

## Types of rules and their support/availability in transaction data upload

| Not supported | Supported via rules-server | Not Applicable                   |
| :------------ | :------------------------- | :------------------------------- |
| Message rule  | Visit schedule rule        | Hyperlink menu item rule         |
|               | Decision rule              | Enrolment Summary Rule           |
|               | Validation rule            | Form Element GroupRule           |
|               |                            | Form Element Rule                |
|               |                            | Encounter eligibility check rule |
|               |                            | Enrolment eligibility check rule |
|               |                            | Hyperlink menu item rule         |
|               |                            | Work list updation rule          |
|               |                            | Checklists rule                  |
|               |                            | Dashboard Card rule              |

## Related Topics

<!-- Add links to related documentation -->


---
<!-- Source: 05-javascript-rules/visit-schedule-rules.md -->

# Writing Visit Schedule Rules

## TL;DR

If we break down the visit schedule complexity into three levels simple to complex, we would notice that the testing mechanism for level 2 & 3 visit schedules are quite wasteful due to long feedback loops. The feedback loop is long mainly because the testing of visit schedule logic requires filli...

## Overview

If we break down the visit schedule complexity into three levels simple to complex, we would notice that the testing mechanism for level 2 & 3 visit schedules are quite wasteful due to long feedback loops. The feedback loop is long mainly because the testing of visit schedule logic requires filling forms to setup data and to see the result. In development mode performing sync the second main reason the feedback loop is long.

It is important to remember that for most (may be not all) bugs the testing of all the scenarios need to be carried our all over again. After certain number iterations of such testing the testing fatigue is likely to kick-in, compromising quality as well.

This feedback loop can be shortened significantly by following age old unit testing written in the form of business specifications. This approach improve quality and reduce waste.

Business specification style will allow for customer, business analyst, developer and testers all to come on the same page about the requirements. Automation of unit tests allows for verification of production code against the specification - repeatedly.

## Business specification style tests

These are tests that are written such that they read close normal english using the language of problem domain, but they can be executed as well. It helps in understanding the basic structure of such tests which is capture in a three step process - **given, when, then**. It would be useful to quickly read about it, if you don't know about this already. One such article is [here](https://www.agilealliance.org/glossary/given-when-then/), but there are many.

### Example

This is one test for scheduling visits on edit of an ANC Visit - [https://github.com/avniproject/apf-odisha-2/blob/main/test/ANCTest.js#L117](https://github.com/avniproject/apf-odisha-2/blob/main/test/ANCTest.js#L117).

**Given** that the for beneficiary ANC-1 visit is completed and ANC-2 visit is scheduled for the next month

**When** ANC-1 is edited

**Then** PW Home or ANC visit should not be scheduled

## QA strategy

Visit schedules for which such unit tests have been written should be tested differently.

* Review the test scenarios already automated via these tests.  If any scenario is missing, request the developer to add those scenarios to the test suite.
* Pick a handful, not too many, of these to verify whether the mobile application is indeed working in the same way as well.
* **Most importantly - do not manually run all the scenarios.**

## For developers

* Jest - [https://jestjs.io/docs/api](https://jestjs.io/docs/api)
* It is important to learn about test lifecycle and setup, teardown, describe, test/it methods. [https://jestjs.io/docs/setup-teardown](https://jestjs.io/docs/setup-teardown)
* It is important the each test (test/it) runs independent of other tests, so that execution of one test doesn't have any impact on another test. To achieve this all variables should be instantiated in each test, i.e. in move all the code common instantiation code (not functions) to beforeEach. Do not instantiate anything outside beforeEach and it/test. Unit tests run super-fast so optimisation is not useful and is in fact counter-productive.

## Related Topics

<!-- Add links to related documentation -->


================================================================================
# Section: Data Management
================================================================================


---
<!-- Source: 06-data-management/README.md -->

# Data Management in Avni

Managing data in Avni: bulk uploads, data entry, imports, drafts, migrations, and voiding records.

## Contents

### 1. [Bulk Data Upload (v2)](bulk-data-upload.md)
bulk upload  data upload  CSV upload  data migration

### 2. [Data Import Validation and Pre-checks](data-import-validation.md)
data validation  import validation  data quality  pre-import checks

### 3. [Web-Based Data Entry Application](data-entry-app.md)
data entry  web app  data entry application  web-based data entry

### 4. [Draft Save Feature](draft-save.md)
draft save  save draft  incomplete forms  draft data

### 5. [Migrating Subjects Between Locations](subject-migration.md)
subject migration  move subject  location change  migrate location

### 6. [Voiding (Soft Deleting) Data in Avni](voiding-data.md)
void  soft delete  remove data  void subjects


---
<!-- Source: 06-data-management/bulk-data-upload.md -->

# Bulk Data Upload (v2)

## TL;DR

* Prepare data in bulk, review, and upload. * Migrating away from an existing implementation, and need to seed with existing data.

## Purpose

* Prepare data in bulk, review, and upload.
* Migrating away from an existing implementation, and need to seed with existing data.
* Your organization has a separate component where data is collected outside Avni, but you still need this data to be present with field workers using Avni.

## Using the Admin app to upload data

The Admin app of the web console has an upload option. Currently, this supports the following. Essentially for each form present in you organisation there is a corresponding upload option in the dropdown, with a sample file.

* Upload subjects
* Upload program enrolment (excluding exit information and observations)
* Upload program encounters (excluding cancel information and observations)
* Upload encounters (excluding cancel information and observations)
* [Upload locations](location-and-catchment-in-avni)
* Upload users and catchments
* Upload metadata zip file downloaded from a different implementation

## Sample file

Sample files are available in the interface. Download the file, fill in values and then upload. The file is in a [CSV](https://www.howtogeek.com/348960/what-is-a-csv-file-and-how-do-i-open-it/) format.\
Sample file acts as an up-to-date documentation on the following.

* fields
* whether they are mandatory for upload
* possible values
* format of the value

> 📘 Since above has already been documented and maintain in the sample file these are not documented here again, please refer to it as a reference documentation.

## Mandatory fields in the form

The mandatory fields in the form element are not applicable when uploading the data via CSV files - since we have seen when made mandatory especially for the legacy data, the users are force to upload some junk information (this may be added in the future).

## Rules

No rules are run as part of CSV upload. This implies that:

* field values created automatically via form element rules will not get created (such columns are present in the sample hence can be uploaded manually)
* observations created by decision rules will not be created automatically (such columns are present in the sample hence can be uploaded manually)
* Validation rule is not applied
* Edit rule is not applied

> 📘 Avni currently doesn't have a robust framework to run these rules on the server side. This may be added in future, if we observe that users need these.

## Identifiers

The primary purpose of these identifiers is for the users to be able to link different CSV file types upload data to each  other - in the same way as foreign key linkages between different records. These linkages can be created using identifiers of user's choosing. Lets try to understand this via an example. Lets assume there are three forms.

* Woman Registration (Subject)
* Pregnancy Program Enrolment (Program Enrolment)
  * links to woman
* Ante Natal Visit Form (Program Encounter)
  * links to pregnancy program


  <thead>
    <tr>
      <th>
        Form
      </th>

      <th>
        Columns
      </th>

      <th>
        Description
      </th>
    </tr>
  </thead>

  <tbody>
    <tr>
      <td>
        Woman Registration
      </td>

      <td>
        Id from previous system
      </td>

      <td>
        Any unique identifier that you may want to use. Note that you can make this up if you don't already have one. e.g. WOMAN-100001, WOMAN-100002
      </td>
    </tr>

    <tr>
      <td>
        Pregnancy Program Enrolment
      </td>

      <td>
        Id from previous system
      </td>

      <td>
        Any unique identifier that you may want to use. It should unique for all program enrolments. They can be same as woman registration id, but we recommend you use something like e.g. WOMAN-100001-01, WOMAN-100001-02 so that you can use multiple enrolments for the same woman.  

        It is possible that at the time of preparing this data, you are don't plan to upload woman registration via CSV and it is already present in Avni. In such a case you should use the Avni UUID value of the woman registration in this field.
      </td>
    </tr>

    <tr>
      <td>
        Pregnancy Program Enrolment
      </td>

      <td>
        Subject Id from previous system
      </td>

      <td>
        This should be used to match the pregnancy enrolment record woman registration record. Hence, for our example used so far, this field would have values like - WOMAN-100001, WOMAN-100002
      </td>
    </tr>

    <tr>
      <td>
        Ante Natal Visit Form
      </td>

      <td>
        Id from previous system
      </td>

      <td>
        You can leave this blank, if you intention is to create new records only and not edit them.
      </td>
    </tr>

    <tr>
      <td>
        Ante Natal Visit Form
      </td>

      <td>
        Program Enrolment Id
      </td>

      <td>
        This should be used to match the program ante natal visit form record with woman registration record. Hence, for our example used so far, this field would have values like - WOMAN-100001-01, WOMAN-100002-01  

        It is possible that at the time of preparing this data, you are don't plan to upload pregnancy enrolment data via CSV and it is already present in Avni. In such a case you should use the Avni UUID value of the woman registration in this field.
      </td>
    </tr>
  </tbody>


> 📘 The identifiers used above, for Id from previous system, are saved in Avni but is not visible in Avni after uploading, it is used only for matching records during CSV upload.

## Scheduling a visit and Upload visit details

Please note that sample file for uploading visit details and scheduling a visit are different. These two options allow for  either creating a scheduled encounter/visit or completed encounter/visit. Note that scheduling a visit and then uploading the visit details for the same visit is not supported (as that is similar to edit).

![image](https://files.readme.io/30f7062dbe6572554955d88df13530e6e45c5a4cd5986fd81499661a294f78a2-image.png)

## Important Notes / Gotchas

* **Limited Concept Support in CSV Upload**: Not all concepts are supported when uploading data via CSV. Specifically, the following are not supported:
  * GroupAffiliation
  * Id
  * File
* **Id Confusion**: The identifiers (used in Id from previous system) are different from Id elements in the form, if you have them.
* **Form Data Editing**: Editing previously submitted form data is not currently supported through the CSV upload process.

## Questions

### What if I have a comma in my observation value?

* Wrap your value in quotes.

### Why are decision concepts not appearing the sample file

If you are using decision concepts in the rule but not linked those concepts then this will happen.

### Is the order of values important?

* No. Columns can be in any order.

### How do I upload images?

* For images, use a url that the avni server can download. Ensure that
  * The images are a direct download link (not a redirect to a page that uses javascript to download)
  * The image urls end with the image type. eg: [https://somedomain.com/images/abc.png](https://somedomain.com/images/abc.png)


You can upload users, subjects, enrolments and encounters in bulk in this screen. Metadata zip files that have been downloaded from another organisation can also be uploaded in this screen.

All files except the metadata zip are supposed to be in a [CSV](https://en.wikipedia.org/wiki/Comma-separated_values) format. If you use Microsoft Excel, it has an option to save your spreadsheet in CSV format.

Use the **Download Sample** option to download a sample file. More details about the sample file are available [here](https://avni.readme.io/docs/upload-data)

## Related Topics

<!-- Add links to related documentation -->


---
<!-- Source: 06-data-management/data-entry-app.md -->

# Web-Based Data Entry Application

## TL;DR

The Data Entry App, as the name suggests, is used to view and enter data directly without relying on mobile syncing. It can be accessed by clicking on the 'Data Entry app' tile in the home page.

## Overview

The Data Entry App, as the name suggests, is used to view and enter data directly without relying on mobile syncing. It can be accessed by clicking on the 'Data Entry app' tile in the home page.

![image](https://files.readme.io/be9c75e10c6f8e1eb905f84e0714b46475192e039bac88837f38b62c87cabf91-Screenshot_2025-08-25_at_7.10.40_PM.png)

### Advantages:

* **Instant access**: When you are on a computer with internet access, you can view and enter data without downloading or syncing data like in the mobile app.
* **Larger data coverage**: On the mobile app, the maximum number of catchment locations that can be synced is 65,535. If you need to view data across more locations, the Data Entry App can be used.

### Features not supported in Data Entry App:

**Rules related limitations:**

* [Edit form rule](https://avni.readme.io/docs/writing-rules#17-edit-form-rule)
* [Member addition eligibility check rule](https://avni.readme.io/docs/writing-rules#16-member-addition-eligibility-check-rule)
* [Manual programs eligibility check rule](https://avni.readme.io/docs/writing-rules#15-manual-programs-eligibility-check-rule)
* [Rules that use service methods to filter across subjects](https://avni.readme.io/docs/writing-rules#using-service-methods-in-the-rules)


**Other unsupported features:**

* [User subject type](https://avni.readme.io/docs/user-subject-types)
* [Dashboards and report cards](https://avni.readme.io/docs/offline-reports)
* [Drafts](https://avni.readme.io/docs/draft-save)
* [Approval workflows](https://avni.readme.io/docs/approval-workflow)
* [Vaccination checklist](https://avni.readme.io/docs/upload-checklist)
* [Growth chart](https://avni.readme.io/docs/child-growth-charts)
* Details on who performed a registration, enrolment or visit
* Viewing of data outside of a user's catchment and configured sync attribute cannot be restricted. Only editing can be restricted.

## Related Topics

<!-- Add links to related documentation -->


---
<!-- Source: 06-data-management/data-import-validation.md -->

# Data Import Validation and Pre-checks

## TL;DR

<!-- TODO: Add 2-3 sentence summary of Data Import Validation and Pre-checks -->

## Overview

**What:** <!-- TODO: One-sentence description -->

**When to use:** <!-- TODO: Scenarios -->

**Prerequisites:** <!-- TODO: What to know first -->

## Validation Checklist

<!-- TODO: Add content for validation-checklist -->

## Common Errors

<!-- TODO: Add content for common-errors -->

## Related Topics

<!-- TODO: Add links to related documentation -->


---
<!-- Source: 06-data-management/draft-save.md -->

# Draft Save Feature

## TL;DR

Sometimes we have huge forms and all the information is not available when you start capturing the data of such forms. Avni gives you the facility to save the half-filled form as a draft.

## Overview

Sometimes we have huge forms and all the information is not available when you start capturing the data of such forms. Avni gives you the facility to save the half-filled form as a draft. These draft forms are not synced to the server, and once you fill the form completely draft is automatically deleted.

## Enabling Draft save

You can enable draft to save for your organization using the admin app. Simply go to "organisation Details" and enable "Draft save".

![](https://files.readme.io/d824dc2-draft_save.png "draft save.png")

Once the "draft save" feature is enabled you can see the half-filled forms in the registration tab in the field app. Please note that these drafts will get if the draft is left untouched for more than 30 days.

It gets converted into a regular Subject or Encounter on pressing Save button during modification of a draft.

![](https://files.readme.io/8386271-d.png "d.png")

## Key points

* **Applicability:** Currently, this feature works only for the registration and encounter forms. So Program enrolment and program encounter forms won't get saved as a draft if left in middle.
* **Display:** Registration drafts are displayed on the Register screen. Encounter drafts are displayed under the on the 'General' tab on the Subject Dashboard. Unscheduled encounter drafts are displayed under the 'Drafts' section and scheduled encounter drafts are accessible by tapping 'Do' on encounters under the 'Visits Planned' section.
* **Save Checkpoint:** A draft save action is performed on clicking "Next" or "Previous" buttons while filling in a form, therefore, if User fills in a page but does not click on "Next" or "Previous" buttons, then the Draft saved would have content only till the previous page (On which "Next" button was clicked)
* **Exiting a form:** To exit from a form in-between, user may click on the "Header" "Back" button or click on "Footer" "Home" buttons\*\*
* **Stale Drafts clean-up:** Usually drafts get deleted once you perform a final save operation to convert it to an actual entity. Along with that we have a periodic drafts clean-up which gets executed once a day, to delete drafts that were last updated more than 30 days ago.

## Related Topics

<!-- Add links to related documentation -->


---
<!-- Source: 06-data-management/subject-migration.md -->

# Migrating Subjects Between Locations

## TL;DR

[https://editor.swagger.io/?url=https://raw.githubusercontent.com/avniproject/avni-server/master/avni-server-api/src/main/resources/api/external-api.yaml](https://editor.swagger.io/?url=https://raw.githubusercontent.com/avniproject/avni-server/master/avni-server-api/src/main/resources/api/externa...

## Please refer to API Doc

[https://editor.swagger.io/?url=https://raw.githubusercontent.com/avniproject/avni-server/master/avni-server-api/src/main/resources/api/external-api.yaml](https://editor.swagger.io/?url=https://raw.githubusercontent.com/avniproject/avni-server/master/avni-server-api/src/main/resources/api/external-api.yaml)

## Documentation Deprecated

Since there are multiple entities that need to be changed, the migration should not be done by making changes directly to the database using SQL commands. In order to migrate a subject use the follow API.

### Endpoint

`{{origin}}/subjectMigration/bulk`

e.g. [https://app.avniproject.org/subjectMigration/bulk](https://app.avniproject.org/subjectMigration/bulk)

### Headers

`auth-token`

### Body

* destinationAddresses is a map of source address level id and destination address level id.
* subject type ids is an array of subject types that you want migrated

```Text JSON
{
    "destinationAddresses": {
        "330785": "330856",
        "334657": "335043",
        "331106": "331466"
    },
    "subjectTypeIds": [
        672,
        671
    ]
}
```

### Also know

* if you have a lot of addresses then the request may timeout, but the server will continue to process
* Each source to destination mapping for each subject type, will be done in its own transaction. So for above example there will be 6 transactions (3 address mapping multiplied by 2 subject types).

## Related Topics

<!-- Add links to related documentation -->


---
<!-- Source: 06-data-management/voiding-data.md -->

# Voiding (Soft Deleting) Data in Avni

## TL;DR

<!-- TODO: Add 2-3 sentence summary of Voiding (Soft Deleting) Data in Avni -->

## Overview

**What:** <!-- TODO: One-sentence description -->

**When to use:** <!-- TODO: Scenarios -->

**Prerequisites:** <!-- TODO: What to know first -->

## When To Void

<!-- TODO: Add content for when-to-void -->

## Step By Step Guide

<!-- TODO: Add content for step-by-step-guide -->

## Related Topics

<!-- TODO: Add links to related documentation -->


================================================================================
# Section: Mobile App Features
================================================================================


---
<!-- Source: 07-mobile-app-features/README.md -->

# Mobile App Features for Implementers

Mobile app features that implementers configure: offline dashboards, dashboard filters, custom search fields, quick form edit, and app configuration.

## Contents

### 1. [Offline Report Cards and Dashboards](offline-dashboards.md)
offline dashboards  report cards  offline reports  dashboard configuration

### 2. [My Dashboard and Search Filters](dashboard-filters.md)
dashboard filters  search filters  my dashboard  filter configuration

### 3. [Custom Fields in Search Results](custom-search-fields.md)
custom search  search results  search fields  custom fields

### 4. [Quick Form Edit and Jump to Summary](quick-form-edit.md)
quick edit  form edit  jump to summary  fast editing

### 5. [Mobile App Configuration Settings](app-configuration.md)
app configuration  mobile settings  app menu  application menu


---
<!-- Source: 07-mobile-app-features/app-configuration.md -->

# Mobile App Configuration Settings

## TL;DR

The customizable "Application menu" feature helps you add a new menu item that will show up on the "More" option of the Android app.

## Overview

The customizable "Application menu" feature helps you add a new menu item that will show up on the "More" option of the Android app. 

This new menu item can either be an http link, or a whatsapp number. Popular apps that can be used with this linking scheme are available [here](https://gist.github.com/imbudhiraja/5b0a485fb7f36fb16c9d7d5f19b6ee40)

eg: 

* To open Whatsapp for a number, you would use a url like "whatsapp\://send?text=hello\&phone=xxxxxxxxxxxxx"
* To open a link on youtube, you would use this - youtube://watch?v=dQw4w9WgXcQ
* To open the Avniproject website on the browser, you would use [https://avniproject.org](https://avniproject.org)

### Configuration

In order to set this up, add a row to the menu_item table. 

```sql Add new menu iterm
INSERT INTO public.menu_item (organisation_id, uuid, is_voided, version, created_by_id, last_modified_by_id,
                              created_date_time, last_modified_date_time, display_key, type, menu_group, icon,
                              link_function)
VALUES (156, uuid_generate_v4(), false, 0, 1, 1, '2022-08-25 11:05:57.791 +00:00',
        now(), 'Support', 'Link', 'Support', 'whatsapp',
        '() => "whatsapp://send?phone=+919292929292"');
```

The link_function is a function that can create a dynamic url. See [here](https://avni.readme.io/docs/writing-rules#12-hyperlink-menu-item-rule) for more information on how these functions can be written.


The customizable "Application menu" feature helps you add a new menu item that will show up on the "More" option of the Android app.

[Learn about creating an entry in Application Menu.](https://avni.readme.io/docs/application-menu)

## Related Topics

<!-- Add links to related documentation -->


---
<!-- Source: 07-mobile-app-features/custom-search-fields.md -->

# Custom Fields in Search Results

## TL;DR

Avni app has the capability to setup [custom search filters](https://avni.readme.io/docs/my-dashboard-and-search-filters), but the results do not show any of these fields. Using this feature one can add additional fields to the search result.

## Overview

Avni app has the capability to setup [custom search filters](https://avni.readme.io/docs/my-dashboard-and-search-filters), but the results do not show any of these fields. Using this feature one can add additional fields to the search result.

## Setting up custom fields in search results

1. In the app designer go to Search Result Fields and select the subject type for which you want to setup the custom search result fields.
2. Next From the dropdown choose the concept name.
3. You can reorder the custom search fields by drag and drop and finally save the changes.
4. Sync the mobile app and you should see the newly added concept in the search result field.

![1031](https://files.readme.io/8c14b56-custom-search-result-fields2.gif "custom-search-result-fields(2).gif")

**Note**: Only concepts in the registration form are supported.\
**Supported data types**: Text, Id, coded, numeric, and date.


Filters on the Search tab of the field app can be enhanced by adding filters here.

[Look up more details](https://avni.readme.io/docs/my-dashboard-and-search-filters)


Custom search result fields can be setup for each subject type. User can choose concepts from the
registration form. If no fields are setup for a subject type default fields will show up in the search result.

## Related Topics

<!-- Add links to related documentation -->


---
<!-- Source: 07-mobile-app-features/dashboard-filters.md -->

# My Dashboard and Search Filters

## TL;DR

Avni allows the display of custom filter in **Search** and **My Dashboard filter** page. These settings are available within App designer.

## Overview

Avni allows the display of custom filter in **Search** and **My Dashboard filter** page. These settings are available within App designer. Filter settings are stored in organisation_config table.  You can define filters for different subject types. Please refer to the table below for various options.

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

## Related Topics

<!-- Add links to related documentation -->


---
<!-- Source: 07-mobile-app-features/offline-dashboards.md -->

# Offline Report Cards and Dashboards

## TL;DR

Avni allows you to create different indicator reports that are available offline to the field users. These reports help field users to derive more insights on the captured data.

## Overview

Avni allows you to create different indicator reports that are available offline to the field users. These reports help field users to derive more insights on the captured data. 

Creating an offline report is a two-step process. First, we need to create a report card that holds the actual query function. Second, we group multiple cards into to a dashboard.

## Creating a Report Card

Creating a new report card is no different than creating any other Avni entity. Open app designer and go to the report card tab. Click on the new report card and provide the details like name description, etc.

### Report Card Types

Report cards can be of 2 types - 'Standard' and 'Custom'. The logic used to display the values in 'Standard' type cards are already implemented in Avni whereas the logic needs to be written by the implementer for 'Custom' type cards.

1. Standard Report Cards, the different types of which are as follows (Entity specified in brackets indicates the type of entity listed on clicking on the card):

   * Pending approval (Entity Approval Statuses)

   * Approved (Entity Approval Statuses)

   * Rejected (Entity Approval Statuses)

   * Scheduled visits (Subjects)

   * Overdue visits (Subjects)

   * Recent registrations (Subjects)

   * Recent enrolments (Subjects)

   * Recent visits (Subjects)

   * Total (Subjects)

   * Comments (Subjects)

   * Call tasks (Tasks)

   * Open subject tasks (Tasks)

   * Due checklist (Individuals)

   ![2. Custom Report cards: Report card with configurable **Query**, which returns a list of Individuals as the response. Length of the list is shown on the card and on clicking the card, the list of Individuals returned is shown. Please note that the query function can return a list of Individuals or an object with these properties, ` { primaryValue: '20', secondaryValue: '(5%)',  lineListFunction  }`, here `lineListFunction` should always return the list of subjects.

![](https://files.readme.io/387d221-Report_card.png "Report card.png")

#### Standard Report Card Type Filters

Filters can be added at the report card level for certain standard report types. The following filters are supported:

1. Subject Type
2. Program
3. Encounter Type
4. Recent Duration

Subject Type, Program and Encounter Type filters are supported for 'Overdue Visits', 'Scheduled Visits', 'Total' and 'Recent' types ('Recent registrations', 'Recent enrolments', 'Recent visits').

![](https://files.readme.io/c2f3eb0a468c1e8e3efb808ccb831cf87e19c5da5ba92ae9ed99a0af619d528f-image.png) 


Filters can also be configured at the dashboard level (covered below). If a filter is configured both at the report card level and the dashboard level, the filter at the report card level is applied first. Hence, mixing of the same type of filter at both levels should be avoided as it could lead to the unintuitive behaviour of the field user selecting a value, say 'Household' for the subject type filter at the dashboard level but still seeing the numbers for the 'Individual' subject type which is configured at the report card level.

## Creating a Dashboard

After all the cards are done it's time to group them together using the dashboard. Offline Dashboards have the following sub-components:

* Sections : Visual Partitions used to club together cards of specific grouping type
* Offline (Custom) Report Cards : Usually Clickable blocks with count information about grouping of Individuals or EntityApprovals of specific type
* Filters : Configurable filters that get applied to all "Report Cards" count and listing

Users with access to the "App Designer" can Create, Modifiy or Delete Custom Dashboards as seen below. 

![](https://files.readme.io/824878a-image.png)

### Steps to configure a Custom Dashboard

* Click on the dashboard tab on the app designer and click on the new dashboard.
* This will take you to the new dashboard screen. Provide the name and description of the dashboard.
* You can create sections on this screen and
* Select all the cards you need to add to the section in the dashboard.
* After adding all the cards, you can re-arrange the cards in the order you want them to see in the field app.

![image](https://files.readme.io/b6a8b74-Screenshot_2023-12-11_at_4.45.34_PM.png)

### Dashboard Filters

You can also create filters for a dashboard on the same screen by clicking on "Add Filter". This shows a popup as in the below screenshot where you can configure your filter and set the filter name, type, widget type and other values based on your filter type.

![](https://files.readme.io/91f1aa1-image.png)

Once all the changes are done. Save the dashboard.

#### For the filters to be applied to the cards in the dashboard, the code for the cards will need to handle the filters.

Sample Code for handling filters in report card:

```
'use strict';
({params, imports}) => {
//console.log('------>',params.ruleInput.filter( type => type.Name === "Gender" ));
//console.log("params:::", JSON.stringify(params.ruleInput));
  let individualList = params.db.objects('Individual').filtered("voided = false and subjectType.name = 'Individual'" )
     .filter( (individual) => individual.getAgeInYears() >= 18 && individual.getAgeInYears() <= 49  &&  individual.getObservationReadableValue('Is sterilisation done') === 'No');
  
  if (params.ruleInput) {

       let genderFilter = params.ruleInput.filter(rule => rule.type === "Gender");
       let genderValue = genderFilter[0].filterValue[0].name;
      
        console.log('genderFilter---------',genderFilter);
        console.log('genderValue---------',genderValue);        
        
      return individualList
     .filter( (individual) => {
     console.log("individual.gender:::", JSON.stringify(individual.gender.name));
     return individual.gender.name === genderValue;
     });
     }
     else return individualList;
};
```

### Assigning custom Dashboards to User Groups

Custom Dashboards created need to be assigned specifically to a User Group, in-order for Users to see it on the Avni-client mobile app. You may do this, by navigating to the "Admin" app -> "User Groups" -> (User_GROUP) -> "Dashboards" tab, and assigning one or more Custom Dashboards to a User-Group.

In addition, You can also mark one of these Custom Dashboards as the Primary (Is Primary: True) dashboard from the "Admin" app -> "User Groups" -> (User_GROUP) -> "Dashboards".

![image](https://files.readme.io/54b6434-Screenshot_2024-06-26_at_12.14.37_PM.png)

## Using the Dashboard in the Field App

After saving the dashboard sync the field app, and from the bottom "More" tab click on the "Dashboards" option. It will take you to the dashboard screen and will show all the cards that are added to the dashboard.

![image](https://files.readme.io/8b37cf6-Screenshot_2024-06-26_at_12.15.37_PM.png)
  Report cards only passing List of subjects.](https://files.readme.io/5093034-Screenshot_2023-12-11_at_4.55.48_PM.png)

![Report cards  returning `primaryValue` and `secondaryValue` object](https://files.readme.io/548f99d-offline-dashboard.png)

Clicking any card will take the user to the subject listing page, which will display all the subject names returned by the card query.

![Users can click on any subject and navigate to their dashboard.

## Secondary Dashboard

### Web app configuration

As part of Avni release 8.0.0, a new feature of a secondary dashboard is added which can be configured at user group level to populate an additional option on the Avni mobile app bottom drawer to navigate to a secondary dashboard. This configuration has to be done in the user group in Avni web app. 

* By navigating to the dashboard section in a particular user group where dashboards can be added to user groups, the secondary dashboard can be defined apart from the home dashboard. As shown in the screenshot below, any dashboard can be selected as the secondary dashboard.

![image](https://files.readme.io/68ac5d9-Screenshot_2024-06-26_at_12.14.37_PM.png)

![image](https://files.readme.io/a5640e1-Se.png)

### Secondary dashboard in mobile app

The configuration mentioned above would display the particular dashboard in the mobile app as given below. This would allow users to access the home and secondary dashboard from the bottom drawer of the mobile app instead of navigating to the more page. 

![image](https://files.readme.io/d95166d-Screenshot_2024-06-26_at_12.17.40_PM.png)

### Clash in Dashboards configuration across different UserGroups

In-case a User belongs to multiple UserGroups, where-in each has a different Primary and/or Secondary Dashboards, then the behaviour is undeterministic. I.e, any of the possible Primary Dashboards across the various UserGroups, would show up as the Primary on the app. Similar behaviour should be expected of the Secondary Dashboard as well.

## Report card query example

As mentioned earlier query can return a list of Individuals or an object with properties, ` { primaryValue: '20', secondaryValue: '(5%)',  lineListFunction  }`. DB instance is passed using the params and useful libraries like lodash and moment are available in the imports parameter of the function. Below are some examples of writing the `lineListFunction`.

The below function returns a list of pregnant women having any high-risk conditions.

```javascript High risk condition women
'use strict';
({params, imports}) => {
    const isHighRiskWomen = (enrolment) => {
        const weight = enrolment.findLatestObservationInEntireEnrolment('Weight');
        const hb = enrolment.findLatestObservationInEntireEnrolment('Hb');
        const numberOfLiveChildren = enrolment.findLatestObservationInEntireEnrolment('Number of live children');
        return (weight && weight.getReadableValue() < 40) || (hb && hb.getReadableValue() < 8) ||
            (numberOfLiveChildren && numberOfLiveChildren.getReadableValue() > 3)
    };
    return {
      lineListFunction: () => params.db.objects('Individual')
        .filtered(`SUBQUERY(enrolments, $enrolment, SUBQUERY($enrolment.encounters, $encounter, $encounter.encounterType.name = 'Monthly monitoring of pregnant woman' and $encounter.voided = false).@count > 0 and $enrolment.voided = false and voided = false).@count > 0`)
        .filter((individual) => individual.voided === false && _.some(individual.enrolments, (enrolment) => enrolment.program.name === 'Pregnant Woman' && isHighRiskWomen(enrolment)))
    }
};
```

It is important to write optimised query and load very less data in memory for processing. There will be the cases where query can't be written in realm and we need to load the data in memory, but remember more data we load into the memory slower will be the reports. As an example consider below two cases, in the first case we directly query realm to fetch all the individuals enrolled in Child program, but in the second case we first load all individuals into memory and then filter those cases. 

```javascript Query in Realm context (better performance)
'use strict';
({params, imports}) => ({
    lineListFunction: () => params.db.objects('Individual')
        .filtered(`SUBQUERY(enrolments, $enrolment, $enrolment.program.name = 'Child' and voided = false).@count > 0`)
});
```
```javascript Query in app context (poor performance)
'use strict';
({params, imports}) => {
    return params.db.objects('Individual')
        .filter((individual) => individual.voided === false && _.some(individual.enrolments, (enrolment) => enrolment.program.name === 'Child'))
};
```

For using the filters in the rules also check section on Dashboard Card Rule here - Writing rules

## Performance of queries

The report cards requires one to return a list individuals. This can be done by:

1. Performing db.objects on Individual and filtering them down.
2. Performing db.objects on descendants of Subject (like encounter, enrolment), filter them down, then return list of Individuals from each filtered object. Example is given below.

## Implementation Patterns for writing performant queries

Please refer to [this reference for Realm Query Language](https://www.mongodb.com/docs/atlas/device-sdks/realm-query-language/).

To understand difference between filter and filtered that is referred below, please see, [https://avni.readme.io/docs/writing-rules#difference-between-filter-and-filtered](https://avni.readme.io/docs/writing-rules#difference-between-filter-and-filtered)

Please also get in touch with platform team if you identify a new pattern and a new type of requirement where none of the following fits.

1. Filter based on chronological data
   1. The matching has to be done on specific chronological descendant entity. e.g. `first` encounter of a specific type, `recent` encounter of specific type.
   2. In this case performing `db.objects` on Individual will lead to either very complex queries or will demand performing filtering in memory using JS.
   3. In this case one can do `db.objects` on descendant entity and then use something like `.filtered('TRUEPREDICATE sort(programEnrolment.individual.uuid asc , encounterDateTime desc) Distinct(programEnrolment.individual.uuid)')` to get the chronological relevant entity at the top in each group. Distinct keyword picks only the first entity in the sorted group.
   4. After performing `filtered`, one can return Subjects by performing `list.map(enc => enc.programEnrolment.individual)`
2. Filter based exact observation value
   1. Matching observations by loading them in memory and calling JS functions will lead to slower reports.
   2. A combination of `subquery` and realm query based match will have much better performance. For example: matching observation that has a specific value - `SUBQUERY(observations, $observation, $observation.concept.name = 'Phone number' and $observation.valueJSON CONTAINS '7555795537'`
3. Filter based on exact specific coded observation value
   1. Matching coded value using its name will require one to load data in memory and perform the match. But this could result in sub-optimal performance. Hence the readability of the report should be sacrificed here for performance.
   2. The query will be like `SUBQUERY(observations, $observation, $observation.concept.uuid = 'Marital Status' and $observation.valueJSON CONTAINS 'fb1080b4-d1ec-4c87-a10d-3838ba9abc5b'`
   3. Please note here that multiple observations can be matched here using OR, AND etc.
4. Filter based on a custom observation value expression.
   1. Instead of matching against a single value match using numeric expression. e.g. match BMI greater than 20.0.
   2. This kind of match cannot be done using realm query and implementing them in JS may result in poor performance.
   3. In such cases we should find out the significance of magic number 20.0. Usually we also have a coded decision observation associated that has meaning behind 20.0, like malnutrition status, BMI Status etc. If there is one then we should match against that using pattern 3 above. If such observation is not present then consider adding them to decisions.
   4. In requirements where such associated coded observation are not present and cannot be added, the performance will depend on the number of observations and entities being matched. If this number is large the performance is expected to be slow, it is better to avoid making reports, or move such reports to their own dashboard - so that they don't impact the usability of other reports.

### Detailed examples

#### DEPRECATED: Avoid using generic functions:

* The following is deprecated cause we should use `Filter based on chronological data` pattern from above.
* To find observation of a concept avoid using the function `findLatestObservationInEntireEnrolment` unless absolutely necessary since it searches for the observation in all encounters and enrolment observations. Use specific functions.
* Eg: To find observation in enrolment can use the function `enrolment.findObservation` or to find observations in specific encounter type can get the encounters using `enrolment.lastFulfilledEncounter(...encounterTypeNames)` and then find observation. Refer code examples for the below 3 usecases.
* ```text Usecase 1
  Find children with birth weight less than 2. Birth weight is captured in enrolment
  ```
  ```javascript Recommended way
  'use strict';
  ({params, imports}) => {
      const isLowBirthWeight = (enrolment) => {
          const obs = enrolment.findObservation('Birth Weight');
          return obs ? obs.getReadableValue() <= 2 : false;
      };
      return params.db.objects('Individual')
          .filtered(`voided = false and SUBQUERY(enrolments, $enrolment, $enrolment.program.name = 'Child' and $enrolment.programExitDateTime = null and $enrolment.voided = false).@count > 0`)
          .filter((individual) => _.some(individual.enrolments, enrolment => enrolment.program.name === 'Child' && _.isNil(enrolment.programExitDateTime) && !enrolment.voided && isLowBirthWeight(enrolment)))
  };
  ```
  ```javascript Not recommended way
  'use strict';
  ({params, imports}) => {
      const isLowBirthWeight = (enrolment) => {
          const obs = enrolment.findLatestObservationInEntireEnrolment('Birth Weight');
          return obs ? obs.getReadableValue() <= 2 : false;
      };
      return params.db.objects('Individual')
          .filtered(`SUBQUERY(enrolments, $enrolment, $enrolment.program.name = 'Child' and $enrolment.programExitDateTime = null and $enrolment.voided = false and SUBQUERY($enrolment.observations, $observation, $observation.concept.uuid = 'c82cd1c8-d0a9-4237-b791-8d64e52b6c4a').@count > 0 and voided = false).@count > 0`)
          .filter((individual) => individual.voided === false && _.some(individual.enrolments, enrolment => enrolment.program.name === 'Child' && isLowBirthWeight(enrolment)))
  };
  ```
  ```Text How optimized
  do voided check first in realm instead of JS - helps in filtering ahead
  Check for concept where it is used - no need to check in all encounters and enrolment
  ```
  ```Text Usecase 2
  Find MAM status from value of Nutritional status concept captured in Child Followup encounter
  ```
  ```javascript Recommended way
  // While this example is illustrating the right JS function to use, but it may be better to filter(ed)
  // encounter schema than to start with Individual
  // i.e. someting like db.objects("ProgramEncounter").filtered("programEnrolment.individual.voided = false AND programEnrolment.voided = false AND ...")
  // then return Individuals using .map(enc => enc.programEnrolment.individual) after filtering all program encounters
  'use strict';
  ({params, imports}) => {
      const isUndernourished = (enrolment) => {
          const encounter = enrolment.lastFulfilledEncounter('Child Followup'); 
          if(_.isNil(encounter)) return false; 
         
         const obs = encounter.findObservation("Nutritional status of child");
         return (!_.isNil(obs) && _.isEqual(obs.getValueWrapper().getValue(), "MAM"));
      };
      
      return params.db.objects('Individual')
          .filtered(`voided = false and SUBQUERY(enrolments, $enrolment,$enrolment.program.name = 'Child' and $enrolment.programExitDateTime = null and $enrolment.voided = false and SUBQUERY($enrolment.encounters, $encounter, $encounter.encounterType.name = 'Child Followup' and $encounter.voided = false).@count > 0).@count > 0`)
          .filter((individual) => individual.getAgeInMonths() > 6 && _.some(individual.enrolments, enrolment => enrolment.program.name === 'Child' && _.isNil(enrolment.programExitDateTime) && !enrolment.voided && isUndernourished(enrolment)))
  };
  ```
  ```javascript Not recommended way
  'use strict';
  ({params, imports}) => {
      const isUndernourished = (enrolment) => {
          const obs = enrolment.findLatestObservationInEntireEnrolment('Nutritional status of child');
          return obs ? _.includes(['MAM'], obs.getReadableValue()) : false;
      };
      return params.db.objects('Individual')
          .filtered(`SUBQUERY(enrolments, $enrolment, $enrolment.program.name = 'Child' and $enrolment.programExitDateTime = null and $enrolment.voided = false and SUBQUERY($enrolment.encounters, $encounter, $encounter.encounterType.name = 'Child Followup' and $encounter.voided = false and SUBQUERY($encounter.observations, $observation, $observation.concept.uuid = '3fb85722-fd53-43db-9e8b-d34767af9f7e').@count > 0).@count > 0 and voided = false).@count > 0`)
          .filter((individual) => individual.voided === false && individual.getAgeInMonths() > 6 && _.some(individual.enrolments, enrolment => enrolment.program.name === 'Child' && isUndernourished(enrolment)))
  };
  ```
  ```Text How optimized
  Check only in specific encounter type
  ```
  ```Text Usecase 3
  Find sick children using the presence of value for concept 'Refer to the hospital for' which is not a mandatory concept
  ```
  ```javascript Recommended way
  // also see comments in Recommended way for use case 2
  'use strict';
  ({params, imports}) => {
      const isChildSick = (enrolment) => {
        const encounter = enrolment.lastFulfilledEncounter('Child Followup', 'Child PNC'); 
        if(_.isNil(encounter)) return false; 
         
        const obs = encounter.findObservation('Refer to the hospital for');
        return !_.isNil(obs);
      };
      
      return params.db.objects('Individual')
          .filtered(`voided = false and SUBQUERY(enrolments, $enrolment, $enrolment.program.name = 'Child' and $enrolment.programExitDateTime = null and $enrolment.voided = false).@count > 0`)
          .filter(individual => _.some(individual.enrolments, enrolment => enrolment.program.name === 'Child' && _.isNil(enrolment.programExitDateTime) && !enrolment.voided && isChildSick(enrolment)))
  };
  ```
  ```javascript Not recommended way
  'use strict';
  ({params, imports}) => {
      const isChildSick = (enrolment) => {
           const obs = enrolment.findLatestObservationFromEncounters('Refer to the hospital for');    
           return obs ? obs.getReadableValue() != undefined : false;
      };
      
      return params.db.objects('Individual')
          .filtered(`SUBQUERY(enrolments, $enrolment, $enrolment.program.name = 'Child' and $enrolment.programExitDateTime = null and $enrolment.voided = false).@count > 0`)
          .filter((individual) => individual.voided === false && (_.some(individual.enrolments, enrolment => enrolment.program.name === 'Child' && isChildSick(enrolment))) )
  };
  ```
  ```Text How optimized
  Check only in last encounter, not all encounters since the concept is not a mandatory concept. 
  Using findLatestObservationFromEncounters will check in all encounters and mark child has sick even if the concept value had represented sick in any of the previous encounters, resulting in bug, since the concept is not a mandatory concept.
  ```

#### Based on the use case decide whether to write the logic using realm query or JS.

* Not always achieving the purpose using realm queries might be efficient/possible. 

  * **DEPRECATED** cause we should use `Filter based on chronological data` pattern from above. Eg: consider a use case where a mandatory concept is used in a program encounter. Now to check the latest value of the concept, its sufficient to check the last encounter and need not iterate all encounters. Since realm subquery doesn't support searching only in the last encounter, for such usecases, using realm queries not only becomes slow and also sometimes inappropriate depending on the usecase. So in such cases, using JS code for the logic, is more efficient. (refer the below code example)

    * ```Text Usecase
      Find dead children using concept value captured in encounter cancel or program exit form.
      ```
      ```javascript Recommended way
      'use strict';
      ({params, imports}) => { 
         const moment = imports.moment;

         const isChildDead = (enrolment) => {
            const exitObservation = enrolment.findExitObservation('29238876-fbd8-4f39-b749-edb66024e25e');
            if(!_.isNil(exitObservation) && _.isEqual(exitObservation.getValueWrapper().getValue(), "cbb0969c-c7fe-4ce4-b8a2-670c4e3c5039"))
              return true;
            
            const encounters = enrolment.getEncounters(false);
            const sortedEncounters = _.sortBy(encounters, (encounter) => {
            return _.isNil(encounter.cancelDateTime)? moment().diff(encounter.encounterDateTime) : 
            moment().diff(encounter.cancelDateTime)}); 
            const latestEncounter = _.head(sortedEncounters);
            if(_.isNil(latestEncounter)) return false; 
             
            const cancelObservation = latestEncounter.findCancelEncounterObservation('0066a0f7-c087-40f4-ae44-a3e931967767');
            if(_.isNil(cancelObservation)) return false;
            return _.isEqual(cancelObservation.getValueWrapper().getValue(), "cbb0969c-c7fe-4ce4-b8a2-670c4e3c5039")
          };

      return params.db.objects('Individual')
              .filtered(`voided = false`)
              .filter(individual => _.some(individual.enrolments, enrolment => enrolment.program.name === 'Child' && isChildDead(enrolment)));
      }
      ```
      ```javascript Not recommended way
      'use strict';
      ({params, imports}) => {

      return params.db.objects('Individual')
              .filtered(`subquery(enrolments, $enrolment, $enrolment.program.name == "Child" and subquery(programExitObservations, $exitObservation, $exitObservation.concept.uuid ==  "29238876-fbd8-4f39-b749-edb66024e25e" and ( $exitObservation.valueJSON ==  '{"answer":"cbb0969c-c7fe-4ce4-b8a2-670c4e3c5039"}')  ).@count > 0 ).@count > 0 OR subquery(enrolments.encounters, $encounter, $encounter.voided == false and subquery(cancelObservations, $cancelObservation, $cancelObservation.concept.uuid ==  "0066a0f7-c087-40f4-ae44-a3e931967767" and ( $cancelObservation.valueJSON ==  '{"answer":"cbb0969c-c7fe-4ce4-b8a2-670c4e3c5039"}')  ).@count > 0 ).@count > 0`)
              .filter(ind => ind.voided == false)
      };
      ```
      ```Text How optimized
      Moving to JS since realm query iterates through all encounters which can be avoided in JS
      In this cases since the intention is to find if child is dead, hence it can be assumed to be captured in the last encounter or in program exit form based on the domain knowledge

      ```
  * Please also refer to `Filter based on a custom observation value expression` pattern above, before using this. Consider another use case, where observations of numeric concepts need to be compared. This is not possible to achieve via realm query since the solution would involve the need for JSON parsing of the stored observation. Hence JS logic is appropriate here. (refer below code example)
    * ```Text Usecase
      Find children with birth weight less than 2. Birth weight is captured in enrolment
      ```
      ```javascript Recommended way
      'use strict';
      ({params, imports}) => {
          const isLowBirthWeight = (enrolment) => {
              const obs = enrolment.findObservation('Birth Weight');
              return obs ? obs.getReadableValue() <= 2 : false;
          };
          return params.db.objects('Individual')
              .filtered(`voided = false and SUBQUERY(enrolments, $enrolment, $enrolment.program.name = 'Child' and $enrolment.programExitDateTime = null and $enrolment.voided = false).@count > 0`)
              .filter((individual) => _.some(individual.enrolments, enrolment => enrolment.program.name === 'Child' && _.isNil(enrolment.programExitDateTime) && !enrolment.voided && isLowBirthWeight(enrolment)))
      };
      ```
      ```javascript Not recommended way
      'use strict';
      ({params, imports}) => {
          const isLowBirthWeight = (enrolment) => {
              const obs = enrolment.findLatestObservationInEntireEnrolment('Birth Weight');
              return obs ? obs.getReadableValue() <= 2 : false;
          };
          return params.db.objects('Individual')
              .filtered(`SUBQUERY(enrolments, $enrolment, $enrolment.program.name = 'Child' and $enrolment.programExitDateTime = null and $enrolment.voided = false and SUBQUERY($enrolment.observations, $observation, $observation.concept.uuid = 'c82cd1c8-d0a9-4237-b791-8d64e52b6c4a').@count > 0 and voided = false).@count > 0`)
              .filter((individual) => individual.voided === false && _.some(individual.enrolments, enrolment => enrolment.program.name === 'Child' && isLowBirthWeight(enrolment)))
      };
      ```
      ```Text How optimized
      Moving to realm query for checking birth weight was not possible. If it were a equals comparison it can be achieved using 'CONTAINS' in realm
      ```
* But in cases where time complexity is the same for both cases, writing realm queries would be efficient to achieve the purpose. (refer below code example). Also refer to `Filter based on a custom observation value expression` pattern above.

  * ```Text Usecase
    Find 13 months children who are completely immunised
    ```
    ```javascript Recommended way
    'use strict';
    ({params, imports}) => {        
       return params.db.objects('Individual')
            .filtered(`voided = false and SUBQUERY(enrolments, $enrolment, $enrolment.program.name = 'Child' and $enrolment.programExitDateTime = null and $enrolment.voided = false and SUBQUERY(checklists, $checklist, SUBQUERY(items, $item, ($item.detail.concept.name = 'BCG' OR $item.detail.concept.name = 'Polio 0' OR $item.detail.concept.name = 'Polio 1' OR $item.detail.concept.name = 'Polio 2' OR $item.detail.concept.name = 'Polio 3' OR $item.detail.concept.name = 'Pentavalent 1' OR $item.detail.concept.name = 'Pentavalent 2' OR $item.detail.concept.name = 'Pentavalent 3' OR $item.detail.concept.name = 'Measles 1' OR $item.detail.concept.name = 'Measles 2' OR $item.detail.concept.name = 'FIPV 1' OR $item.detail.concept.name = 'FIPV 2' OR $item.detail.concept.name = 'Rota 1' OR $item.detail.concept.name = 'Rota 2') and $item.completionDate <> nil).@count = 14).@count > 0).@count > 0`)
            .filter(individual => individual.getAgeInMonths() >= 13)     
    };
    ```
    ```javascript Not recommended way
    'use strict';
    ({params, imports}) => {
        const isChildGettingImmunised = (enrolment) => {
            if (enrolment.hasChecklist) {
                const vaccineToCheck = ['BCG', 'Polio 0', 'Polio 1', 'Polio 2', 'Polio 3', 'Pentavalent 1', 'Pentavalent 2', 'Pentavalent 3', 'Measles 1', 'Measles 2', 'FIPV 1', 'FIPV 2', 'Rota 1', 'Rota 2'];
                const checklist = _.head(enrolment.getChecklists());
                return _.chain(checklist.items)
                    .filter(({detail}) => _.includes(vaccineToCheck, detail.concept.name))
                    .every(({completionDate}) => !_.isNil(completionDate))
                    .value();
            }
            return false;
        };

        return params.db.objects('Individual')
            .filtered(`SUBQUERY(enrolments, $enrolment, $enrolment.program.name = 'Child' and $enrolment.programExitDateTime = null and $enrolment.voided = false).@count > 0`)
            .filter((individual) => individual.voided === false && individual.getAgeInMonths() >= 13 && _.some(individual.enrolments, enrolment => enrolment.program.name === 'Child' && isChildGettingImmunised(enrolment)))
    };
    ```
    ```Text How optimized
    Moving to realm query since no of children with age < 13 months were less
    ```
* In most cases, filtering as much as possible using realm queries (for cases like voided checks) and then doing JS filtering on top of it if needed, would be appropriate. (refer the below code example)

  * ```Text Usecase
    Find dead children using concept value captured in encounter cancel or program exit form.
    ```
    ```javascript Recommended way
    'use strict';
    ({params, imports}) => { 
       const moment = imports.moment;

       const isChildDead = (enrolment) => {
          const exitObservation = enrolment.findExitObservation('29238876-fbd8-4f39-b749-edb66024e25e');
          if(!_.isNil(exitObservation) && _.isEqual(exitObservation.getValueWrapper().getValue(), "cbb0969c-c7fe-4ce4-b8a2-670c4e3c5039"))
            return true;
          
          const encounters = enrolment.getEncounters(false);
          const sortedEncounters = _.sortBy(encounters, (encounter) => {
          return _.isNil(encounter.cancelDateTime)? moment().diff(encounter.encounterDateTime) : 
          moment().diff(encounter.cancelDateTime)}); 
          const latestEncounter = _.head(sortedEncounters);
          if(_.isNil(latestEncounter)) return false; 
           
          const cancelObservation = latestEncounter.findCancelEncounterObservation('0066a0f7-c087-40f4-ae44-a3e931967767');
          if(_.isNil(cancelObservation)) return false;
          return _.isEqual(cancelObservation.getValueWrapper().getValue(), "cbb0969c-c7fe-4ce4-b8a2-670c4e3c5039")
        };

    return params.db.objects('Individual')
            .filtered(`voided = false`)
            .filter(individual => _.some(individual.enrolments, enrolment => enrolment.program.name === 'Child' && isChildDead(enrolment)));
    }
    ```
    ```javascript Not recommended way
    'use strict';
    ({params, imports}) => {

    return params.db.objects('Individual')
            .filtered(`subquery(enrolments, $enrolment, $enrolment.program.name == "Child" and subquery(programExitObservations, $exitObservation, $exitObservation.concept.uuid ==  "29238876-fbd8-4f39-b749-edb66024e25e" and ( $exitObservation.valueJSON ==  '{"answer":"cbb0969c-c7fe-4ce4-b8a2-670c4e3c5039"}')  ).@count > 0 ).@count > 0 OR subquery(enrolments.encounters, $encounter, $encounter.voided == false and subquery(cancelObservations, $cancelObservation, $cancelObservation.concept.uuid ==  "0066a0f7-c087-40f4-ae44-a3e931967767" and ( $cancelObservation.valueJSON ==  '{"answer":"cbb0969c-c7fe-4ce4-b8a2-670c4e3c5039"}')  ).@count > 0 ).@count > 0`)
            .filter(ind => ind.voided == false);
    };
    ```
    ```Text How optimized
    Moving to JS since realm query iterates through all encounters which can be avoided in JS
    In this cases since the intention is to find if child is dead it can be assumed to be captured in the last encounter or in program exit form based on the domain knowledge

    ```

Also check - [https://avni.readme.io/docs/writing-rules#using-paramsdb-object-when-writing-rules](https://avni.readme.io/docs/writing-rules#using-paramsdb-object-when-writing-rules)

#### DEPRECATED. Use Concept UUIDs instead of their names for comparison

Please check - `Filter based on a custom observation value expression` pattern above.

Though not much performance improvement, using concept uuids(for comparing with concept answers), instead of getting its readable values did provide minor improvement(in seconds) when need to iterate through thousands of rows. (refer below code example)

* ```Text Usecase
  Find children with congential abnormality based on values of certain concepts
  ```
  ```javascript Recommended way
  'use strict';
  ({params, imports}) => {
      const isChildCongenitalAnamoly = (enrolment) => {
         const _ = imports.lodash;
      
         const encounter = enrolment.lastFulfilledEncounter('Child PNC'); 
         if(_.isNil(encounter)) return false; 
         
         const obs1 = encounter.findObservation("Is the infant's mouth cleft pallet seen?");
         const condition2 = obs1 ? obs1.getValueWrapper().getValue() === '3a9fe9a1-a866-47ed-b75c-c0071ea22d97' : false;
           
         const obs2 = encounter.findObservation('Is there visible tumor on back or on head of infant?');
         const condition3 = obs2 ? obs2.getValueWrapper().getValue() === '3a9fe9a1-a866-47ed-b75c-c0071ea22d97' : false;
           
         const obs3 = encounter.findObservation("Is foam coming from infant's mouth continuously?");
         const condition4 = obs3 ? obs3.getValueWrapper().getValue() === '3a9fe9a1-a866-47ed-b75c-c0071ea22d97' : false;
                    
           return condition2 || condition3 || condition4;
      };
      
      const isChildCongenitalAnamolyReg = (individual) => {
           const obs = individual.findObservation('Has any congenital abnormality?');
           return obs ? obs.getValueWrapper().getValue() === '3a9fe9a1-a866-47ed-b75c-c0071ea22d97' : false;
      };
      
      return params.db.objects('Individual')
          .filtered(`voided = false and SUBQUERY(enrolments, $enrolment, $enrolment.program.name = 'Child' and $enrolment.programExitDateTime = null and $enrolment.voided = false).@count > 0`)
          .filter((individual) => (isChildCongenitalAnamolyReg(individual) || 
              _.some(individual.enrolments, enrolment => enrolment.program.name === 'Child' && _.isNil(enrolment.programExitDateTime) && !enrolment.voided && isChildCongenitalAnamoly(enrolment) )) )
  };
  ```
  ```javascript Not recommended way
  'use strict';
  ({params, imports}) => {
      const isChildCongenitalAnamoly = (enrolment) => {
           
           const obs1 = enrolment.findLatestObservationInEntireEnrolment("Is the infant's mouth cleft pallet seen?");
           const condition2 = obs1 ? obs1.getReadableValue() === 'Yes' : false;
           
       const obs2 = enrolment.findLatestObservationInEntireEnrolment('Is there visible tumor on back or on head of infant?');
           const condition3 = obs2 ? obs2.getReadableValue() === 'Yes' : false;
           
           const obs3 = enrolment.findLatestObservationInEntireEnrolment("Is foam coming from infant's mouth continuously?");
           const condition4 = obs3 ? obs3.getReadableValue() === 'Yes' : false;
                    
           return condition2 || condition3 || condition4;
      };
      
      const isChildCongenitalAnamolyReg = (individual) => {
           const obs = individual.getObservationReadableValue('Has any congenital abnormality?');
           return obs ? obs === 'Yes' : false;
      };
      
      return params.db.objects('Individual')
          .filtered(`SUBQUERY(enrolments, $enrolment, $enrolment.program.name = 'Child' and $enrolment.programExitDateTime = null and $enrolment.voided = false).@count > 0`)
          .filter((individual) => individual.voided === false && (isChildCongenitalAnamolyReg(individual) || 
              _.some(individual.enrolments, enrolment => enrolment.program.name === 'Child' && isChildCongenitalAnamoly(enrolment) )) )
  };
  ```
  ```Text How optimized
  Use concept uuid instead of readableValue to compare and check for value only in specific encounter type where the concept was used
  ```

## Nested Report Cards

Frequently there are cases where across report cards very similar logic is used and only a value used for comparison, changes. Eg: in one of our partner organisations, we load 'Total SAM children' and 'Total MAM children'. For rendering each takes around 20-30s. And hence the dashboard nos doesn't load until both the report card results are calculated and it makes the user to wait for a minute. If the logic is combined, we can render the results in 30s since it would need only retrieval from db and iterating once.\
The above kind of scenarios also lead to code duplication across report cards and when some requirement changes, then the change needs to be done in both.

In-order to handle such scenarios, we recommend using the Nested Report Card. This is a non-standard report card, which has the ability to show upto a maximum of **9** report cards, based on a single Query's response.

The query can return an object with "reportCards" property, which holds within it an array of objets with properties, ` { cardName: 'nested-i', cardColor: '#123456', textColor: '#654321', primaryValue: '20', secondaryValue: '(5%)',  lineListFunction: () => {/*Do something*/} }`. DB instance is passed using the params and useful libraries like lodash and moment are available in the imports parameter of the function. 

```javascript Nested Report Card Query Format
'use strict';
({params, imports}) => {
    /*
    Business logic
    */
    return {reportCards: \[
        {
            cardName: 'nested-i',
            cardColor: '#123456',
            textColor: '#654321',
            primaryValue: '20',
            secondaryValue: '(5%)',
            lineListFunction: () => {
                /*Do something*/
            }
        },
        {
            cardName: 'nested-i+1',
            cardColor: '#123456',
            textColor: '#654321',
            primaryValue: '20',
            secondaryValue: '(5%)',
            lineListFunction: () => {
                /*Do something*/
            }
        }
    ]
	}
};
```
```Text Mandatory Fields
- primaryValue
- secondaryValue
- lineListFunction
```
```Text Optional fields
- cardName
- cardColor
- textColor
```

```javascript Sample Nested Report card Query
// Documentation - https://docs.mongodb.com/realm-legacy/docs/javascript/latest/index.html#queries

'use strict';
({params, imports}) => {
const _ = imports.lodash;
const moment = imports.moment;

const substanceUseDue = (enrolment) => {
    const substanceUseEnc = enrolment.scheduledEncountersOfType('Record Substance use details');
    
    const substanceUse = substanceUseEnc
    .filter((e) => moment().isSameOrAfter(moment(e.earliestVisitDateTime)) && e.cancelDateTime === null && e.encounterDateTime === null );
    
    return substanceUse.length > 0 ? true : false;
    
    };
const indList = params.db.objects('Individual')
        .filtered(`SUBQUERY(enrolments, $enrolment, $enrolment.program.name = 'Substance use' and $enrolment.programExitDateTime = null and $enrolment.voided = false and SUBQUERY($enrolment.encounters, $encounter, $encounter.encounterType.name = 'Record Substance use details' and $encounter.voided = false ).@count > 0 and voided = false).@count > 0`)
        .filter((individual) => _.some(individual.enrolments, enrolment => substanceUseDue(enrolment)
        )); 
        
const includingVoidedLength = indList.length;
const excludingVoidedLength = 6;  
const llf1 = () => { return params.db.objects('Individual')
        .filtered(`SUBQUERY(enrolments, $enrolment, $enrolment.program.name = 'Substance use' and $enrolment.programExitDateTime = null and $enrolment.voided = false and SUBQUERY($enrolment.encounters, $encounter, $encounter.encounterType.name = 'Record Substance use details' and $encounter.voided = false ).@count > 0 and voided = false).@count > 0`)
        .filter((individual) => _.some(individual.enrolments, enrolment => substanceUseDue(enrolment)
        ));    
        };
           

return {reportCards: [{
      cardName: 'nested 1',
      textColor: '#bb34ff',
      primaryValue: includingVoidedLength,   
      secondaryValue: null,
      lineListFunction: llf1
  },
  {
      cardName: 'nested 2',
      cardColor: '#ff34ff',
      primaryValue: excludingVoidedLength,   
      secondaryValue: null,
      lineListFunction: () => {return params.db.objects('Individual')
        .filtered(`SUBQUERY(enrolments, $enrolment, $enrolment.program.name = 'Substance use' and $enrolment.programExitDateTime = null and $enrolment.voided = false and SUBQUERY($enrolment.encounters, $encounter, $encounter.encounterType.name = 'Record Substance use details' and $encounter.voided = false ).@count > 0 and voided = false).@count > 0`)
        .filter((individual) => individual.voided === false  && _.some(individual.enrolments, enrolment => substanceUseDue(enrolment)
        ));}
  }]}
};
```

### Screenshot of Nested Custom Dashboard Report Card Edit screen on Avni Webapp

![image](https://files.readme.io/ecdd996-Screenshot_2024-01-25_at_5.15.20_PM.png)

### Screenshot of Nested Report Cards in Custom Dashboard in Avni Client

![image](https://files.readme.io/dca68e5-Screenshot_2024-01-25_at_5.19.04_PM.png)

![]()

Note: If there is a mismatch between the count of nested report cards configured and the length of reportCards property returned by the query response, then we show an appropriate error message on all Nested Report Cards corresponding to the Custom Report Card.

![image](https://files.readme.io/82d8ca0-Screenshot_2024-01-25_at_5.23.56_PM.png)

## Default Dashboard and Report Cards

Starting in release 10.0, any newly created organisation will have a default dashboard created with the following sections, standard cards and filters.

Default Dashboard (Filters: 'Subject Type' and 'As On Date')

1. Visit Details Section
   1. Scheduled Visits Card
   2. Overdue Visits Card
2. Recent Statistics Section
   1. Recent Registrations Card (Recent duration filter configured as - 1 day)
   2. Recent Enrolments Card (Recent duration filter configured as - 1 day)
   3. Recent Visits Card (Recent duration filter configured as - 1 day)
3. Registration Overview Section
   1. Total Card

This default dashboard will also be assigned as Primary dashboard on the 'Everyone' user group.

## Reference screen-shots of Avni-Client Custom Dashboard with Approvals ReportCards and Location filter

![image](https://files.readme.io/e35888a-Screenshot_2023-12-12_at_12.46.46_PM.png)
  Default state of Approvals Report Cards without any filter applied](https://files.readme.io/18fb944-Subject-list-field-app.png)

***

![Custom Dashboards filter page](https://files.readme.io/576efec-Screenshot_2023-12-12_at_12.47.01_PM.png)

***

![State of Approvals Report Cards after the Location filter was applied](https://files.readme.io/c5ac6f6-Screenshot_2023-12-12_at_12.47.25_PM.png)

***


`Dashboard` created here will be shown in the field app.
You can add multiple `Sections` to a dashboard.
`Sections` will be shown in the same order as added here from the app-designer.
`Sections` can have multiple `Cards`, either in `Tile` or `List` format.
Within a `Section`, `Cards` will be shown in the same order as added here.

Collapse all the `Sections` for changing their order.


Card contains the actual query that gets executed. Right now query should return a list of individual object.

## Related Topics

<!-- Add links to related documentation -->


---
<!-- Source: 07-mobile-app-features/quick-form-edit.md -->

# Quick Form Edit and Jump to Summary

## TL;DR

This feature allows users to jump directly to any page in the form and then quickly save the form skipping the middle questions. This will save a lot of time as now users don't have to go through all the pages.\
There is no configuration required for the quick form edit feature however, one need ...

## Overview

This feature allows users to jump directly to any page in the form and then quickly save the form skipping the middle questions. This will save a lot of time as now users don't have to go through all the pages.\
There is no configuration required for the quick form edit feature however, one need to enable jump to summary feature

## Enabling jump to summary

In the admin app go to "Organisation Details" and enable the "Show summary button" option. 

![Enabling Jump to summary feature](https://files.readme.io/19f3021-Jump_to_summary.png)

After enabling the "jump to summary feature", sync the field app. The user will see the Summary button at the top right corner in the form.

![Quick form edit in action](https://files.readme.io/aea853d-quick-form-edit1.gif)

**Note**: This feature is only supported in the mobile application.

## Related Topics

<!-- Add links to related documentation -->


================================================================================
# Section: Troubleshooting
================================================================================


---
<!-- Source: 08-troubleshooting/README.md -->

# Troubleshooting Common Implementation Issues

Guides for diagnosing and fixing common issues encountered during Avni implementation: form problems, rules debugging, visit scheduling, data imports, and more.

## Contents

### 1. [Troubleshooting Form Configuration Issues](form-configuration-issues.md)
form issues  form troubleshooting  missing fields  form not loading

### 2. [Debugging JavaScript Rules](rules-debugging.md)
rules debugging  rule errors  rule not working  JavaScript debugging

### 3. [Troubleshooting Visit Scheduling Issues](visit-scheduling-issues.md)
visit scheduling  scheduling issues  visits not appearing  schedule debugging

### 4. [Troubleshooting Data Import Issues](data-import-troubleshooting.md)
import errors  upload failures  CSV errors  data import issues

### 5. [Handling Duplicate Data](duplicate-data-handling.md)
duplicate data  duplicate subjects  duplicate entries  deduplication

### 6. [Testing and Verification SQL Queries](testing-verification-queries.md)
testing  verification  SQL queries  data verification

### 7. [Common Issues Quick Reference](common-issues-quick-fixes.md)
quick fixes  common issues  FAQ  quick reference


---
<!-- Source: 08-troubleshooting/common-issues-quick-fixes.md -->

# Common Issues Quick Reference

## TL;DR

<!-- TODO: Add 2-3 sentence summary of Common Issues Quick Reference -->

## Overview

**What:** <!-- TODO: One-sentence description -->

**When to use:** <!-- TODO: Scenarios -->

**Prerequisites:** <!-- TODO: What to know first -->

## Form Quick Fixes

<!-- TODO: Add content for form-quick-fixes -->

## Rules Quick Fixes

<!-- TODO: Add content for rules-quick-fixes -->

## Sync Quick Fixes

<!-- TODO: Add content for sync-quick-fixes -->

## Related Topics

<!-- TODO: Add links to related documentation -->


---
<!-- Source: 08-troubleshooting/data-import-troubleshooting.md -->

# Troubleshooting Data Import Issues

## TL;DR

<!-- TODO: Add 2-3 sentence summary of Troubleshooting Data Import Issues -->

## Overview

**What:** <!-- TODO: One-sentence description -->

**When to use:** <!-- TODO: Scenarios -->

**Prerequisites:** <!-- TODO: What to know first -->

## Common Csv Errors

<!-- TODO: Add content for common-csv-errors -->

## Validation Failures

<!-- TODO: Add content for validation-failures -->

## Diagnostic Steps

<!-- TODO: Add content for diagnostic-steps -->

## Related Topics

<!-- TODO: Add links to related documentation -->


---
<!-- Source: 08-troubleshooting/duplicate-data-handling.md -->

# Handling Duplicate Data

## TL;DR

<!-- TODO: Add 2-3 sentence summary of Handling Duplicate Data -->

## Overview

**What:** <!-- TODO: One-sentence description -->

**When to use:** <!-- TODO: Scenarios -->

**Prerequisites:** <!-- TODO: What to know first -->

## Finding Duplicates

<!-- TODO: Add content for finding-duplicates -->

## Resolving Duplicates

<!-- TODO: Add content for resolving-duplicates -->

## Prevention

<!-- TODO: Add content for prevention -->

## Related Topics

<!-- TODO: Add links to related documentation -->


---
<!-- Source: 08-troubleshooting/form-configuration-issues.md -->

# Troubleshooting Form Configuration Issues

## TL;DR

<!-- TODO: Add 2-3 sentence summary of Troubleshooting Form Configuration Issues -->

## Overview

**What:** <!-- TODO: One-sentence description -->

**When to use:** <!-- TODO: Scenarios -->

**Prerequisites:** <!-- TODO: What to know first -->

## Issue Missing Fields

<!-- TODO: Add content for issue-missing-fields -->

## Issue Form Not Loading

<!-- TODO: Add content for issue-form-not-loading -->

## Issue Skip Logic

<!-- TODO: Add content for issue-skip-logic -->

## Diagnostic Steps

<!-- TODO: Add content for diagnostic-steps -->

## Related Topics

<!-- TODO: Add links to related documentation -->


---
<!-- Source: 08-troubleshooting/rules-debugging.md -->

# Debugging JavaScript Rules

## TL;DR

<!-- TODO: Add 2-3 sentence summary of Debugging JavaScript Rules -->

## Overview

**What:** <!-- TODO: One-sentence description -->

**When to use:** <!-- TODO: Scenarios -->

**Prerequisites:** <!-- TODO: What to know first -->

## Common Rule Errors

<!-- TODO: Add content for common-rule-errors -->

## Debugging Checklist

<!-- TODO: Add content for debugging-checklist -->

## Rule Failure Logs

<!-- TODO: Add content for rule-failure-logs -->

## Related Topics

<!-- TODO: Add links to related documentation -->


---
<!-- Source: 08-troubleshooting/testing-verification-queries.md -->

# Testing and Verification SQL Queries

## TL;DR

<!-- TODO: Add 2-3 sentence summary of Testing and Verification SQL Queries -->

## Overview

**What:** <!-- TODO: One-sentence description -->

**When to use:** <!-- TODO: Scenarios -->

**Prerequisites:** <!-- TODO: What to know first -->

## Subject Queries

<!-- TODO: Add content for subject-queries -->

## Encounter Queries

<!-- TODO: Add content for encounter-queries -->

## Program Queries

<!-- TODO: Add content for program-queries -->

## Related Topics

<!-- TODO: Add links to related documentation -->


---
<!-- Source: 08-troubleshooting/visit-scheduling-issues.md -->

# Troubleshooting Visit Scheduling Issues

## TL;DR

<!-- TODO: Add 2-3 sentence summary of Troubleshooting Visit Scheduling Issues -->

## Overview

**What:** <!-- TODO: One-sentence description -->

**When to use:** <!-- TODO: Scenarios -->

**Prerequisites:** <!-- TODO: What to know first -->

## Visits Not Appearing

<!-- TODO: Add content for visits-not-appearing -->

## Wrong Dates

<!-- TODO: Add content for wrong-dates -->

## Diagnostic Sql

<!-- TODO: Add content for diagnostic-sql -->

## Related Topics

<!-- TODO: Add links to related documentation -->


================================================================================
# Section: Implementation Guides
================================================================================


---
<!-- Source: 09-implementation-guides/README.md -->

# Implementation Guides and Examples

Real-world implementation examples and step-by-step guides for common Avni use cases: health tracking, nutrition programs, and education monitoring.

## Contents

### 1. [Implementation Example: Maternal Health Tracking](maternal-health-example.md)
maternal health  health tracking  ANC  pregnancy tracking

### 2. [Implementation Example: Child Nutrition Program](child-nutrition-example.md)
child nutrition  nutrition tracking  growth monitoring  implementation example

### 3. [Implementation Example: Education Monitoring](education-monitoring-example.md)
education  classroom monitoring  school tracking  implementation example

### 4. [Implementation Checklist](implementation-checklist.md)
checklist  implementation steps  setup checklist  go-live checklist


---
<!-- Source: 09-implementation-guides/child-nutrition-example.md -->

# Implementation Example: Child Nutrition Program

## TL;DR

author: Anjali Bhagabati 
description: >-  
featuredpost: false 
featuredimage:
tags:
- Health
---

## Overview

author: Anjali Bhagabati 
description: >-  
featuredpost: false 
featuredimage:
tags:
- Health
---


    <img src="/img/2025-05-28-bridging-the-nutrition-gap-apf-odisha/why-child-nutrition-matters.png">


Child nutrition is a vital indicator of a nation’s health and development. While India has made significant strides in
improving maternal and child health over the last decade, there is still a pressing need to address persistent gaps,
especially in underserved rural communities.

One of the most [impactful periods in a child’s life is the first **1,000
days.**](https://azimpremjifoundation.org/what-we-do/health/creche-initiative/) Nutrition during this window plays a
pivotal role in shaping the child’s cognitive development, immunity, and long-term health outcomes.


  <h2 style="margin: 0 0 8px 0; font-size: 1.25rem;">
    🎥 Video Case Study: Azim Premji Foundation | Community Nutrition Program (CNP)
  </h2>
  <a href="https://www.youtube.com/watch?v=sfB9QyFoWW8&list=PLEy8ff0CKDBkFhqQ95itFuEJMf38HwLBx" 
     target="_blank" 
     rel="noopener noreferrer"
     style="color: #007acc; text-decoration: underline;">
    Watch on YouTube
  </a>


### APF Odisha Nutrition Initiative: Focused Care from Pregnancy to Early Childhood

The **Azim Premji Foundation’s Odisha Nutrition Initiative** addresses these challenges with a focused intervention that
spans from pregnancy through the first five years of a child's life. The initiative targets maternal and child nutrition
through community-level engagement, regular monitoring, and technology-driven support systems.


    <img src="/img/2025-05-28-bridging-the-nutrition-gap-apf-odisha/program-overview.png">


### Why Technology Was Essential

Frontline health workers in rural and tribal areas often operate under challenging conditions, including:

* Inconsistent or no internet connectivity
* Limited access to timely health data
* Manual, paper-based reporting systems

The solution required a digital platform that could:

* Be usable offline in remote areas with poor connectivity.
* Customizable for local health workflows.
* Supporting real-time data collection and reporting.
* Be **easy to use** for health workers with a very basic level of training.

### The Solution: Avni – Open-Source Technology for Social Impact

[**Avni**](https://avniproject.org/) is a powerful, open-source platform for field service delivery. It is designed to
enable digital data collection, decision support, and real-time reporting for community health programs. With offline
functionality and modular workflows,it is ideal for nonprofits, government partners, and social enterprises aiming for
deep impact.

Built and maintained by the [**Samanvay Foundation**,](https://www.samanvayfoundation.org/) Avni is currently being
actively used by multiple NGO across India.

### How APF Odisha Is Using Avni

[The Azim Premji Foundation integrated Avni](https://www.youtube.com/watch?v=sfB9QyFoWW8&list=PLEy8ff0CKDBkFhqQ95itFuEJMf38HwLBx&index=5)
into its Pregnancy and Child Program in Odisha, particularly in underserved rural communities. The deployment focuses on
improving early identification of at-risk cases, enhancing field supervision, and enabling data-driven program
management.

#### 1\. Pregnancy Program: Proactive Maternal Care

* Registration & Lifecycle Tracking: Every pregnant woman is registered in the Avni app and monitored through antenatal,
  delivery, and postnatal stages.

* Risk Identification: The app flags high-risk pregnancies, triggering rapid follow-up by Poshan Sathi and Quick
  Response Team (QRT) personnel.

* Timely Reminders: Health workers and supervisors receive automated alerts for critical visits (ANC and PNC), ensuring
  no woman misses essential care.

#### 2\. Child Program: Nutrition Surveillance and Support

* Growth Monitoring: Children under five are tracked monthly for weight, height, and developmental milestones, using WHO
  growth charts.

* Malnutrition Detection: Children identified with Severe Acute Malnutrition (SAM) or Moderate Acute Malnutrition (MAM)
  are prioritized for intervention.

* NRC Referrals & Follow-up: Severely affected children are referred to Nutrition Rehabilitation Centres (NRCs) directly
  through the app. Their recovery and follow-up are digitally tracked post-discharge.

#### 3\. TIMS: Training and Information Management System

The Training and Information Management System (TIMS) is a custom-built module within Avni for APF Odisha. It allows:

* Field staff to request training support based on real-time challenges

* Program leads to track training needs and conduct targeted upskilling

#### 4\. Supervisor Monitoring

Supervisors log visits to Anganwadi Centres and Village Health Nutrition Days (VSHNDs) within Avni. This ensures
real-time visibility for program managers into field operations and quality checks.

#### 5\. Comprehensive Reporting

Avni offers dashboards and downloadable reports to help APF and its partners evaluate program impact, identify issues,
and make data-driven decisions. Reports are built on an innovative BI tool \- Superset


      <img src="/img/2025-05-28-bridging-the-nutrition-gap-apf-odisha/offline-dashboard.gif">


      <img src="/img/2025-05-28-bridging-the-nutrition-gap-apf-odisha/individual-dashboard-child.gif">


      <img src="/img/2025-05-28-bridging-the-nutrition-gap-apf-odisha/individual-dashboard.gif">


    <img src="/img/2025-05-28-bridging-the-nutrition-gap-apf-odisha/reports.png">

## **Program Reach and Impact**

Through the Avni platform, the Odisha Nutrition Initiative has achieved significant scale:

* **300** frontline workers actively using the app

* **79,000** children tracked

* **22,000** pregnant women enrolled

* **7,357** households counselled on dietary diversity and Infant and Young Child Feeding (IYCF) practices

* **1,275** children with low Weight-for-Height (WFH) referred to CMAM

* **3,793** high-risk pregnancies linked to institutional deliveries and timely ANC

The APF-Avni collaboration in Odisha shows how **simple, scalable tech** can strengthen public health systems by
empowering field workers, improving data quality, and ensuring that no high-risk case is missed. This approach sets a
benchmark for sustainable, tech-driven healthcare delivery in rural India.


<i>“Avni plays a pivotal role in strengthening the Community Nutrition Program by bridging the gap between field-level data
collection and real-time decision-making. Its offline-first design is especially effective in remote tribal areas with
limited connectivity. By enabling frontline workers to capture key data on maternal and child health and service
delivery during home visits, growth monitoring sessions, and VHSNDs, AVNI facilitates the timely identification and
follow-up of High-Risk Pregnancies (HRP) and undernourished children.” </i> \- **Ramesh Sahu, Program Manager**


If you're interested in adopting a similar approach or want to learn more about how the Avni platform can support your initiatives:


👉 <a href="https://calendly.com/avnisupport-samanvayfoundation/product-demo-and-discussion?embed_domain=avniproject.org&embed_type=PopupText" target="_blank" rel="noopener noreferrer">
Schedule a call with us
</a>


📬 <a href="https://avniproject.us17.list-manage.com/subscribe?u=5f3876f49a7603817af2856b9&id=c9fdedc9e7" target="_blank" rel="noopener noreferrer">
Subscribe to our newsletter to stay updated on new case studies, features, and implementation stories.
</a>


Let’s work together to scale impactful solutions for better health outcomes.

## Related Topics

<!-- Add links to related documentation -->


---
<!-- Source: 09-implementation-guides/education-monitoring-example.md -->

# Implementation Example: Education Monitoring

## TL;DR

author: The Avni Team
description:
featuredpost: false
featuredimage: /img/2024-09-19-Scaling-Rural-Education/CInI-1.png
tags:
  - Education
  - Case Study
---

## Overview

author: The Avni Team
description:
featuredpost: false
featuredimage: /img/2024-09-19-Scaling-Rural-Education/CInI-1.png
tags:
  - Education
  - Case Study
---


In the heart of rural India, education is getting a fresh makeover. It’s not just about reading and writing anymore; it’s about giving children the skills they need for life. The Collectives for Integrated Livelihood Initiatives (CInI), part of Tata Trusts, is leading this change, reaching over 250,000 students in rural and tribal areas in Odisha and Jharkhand. They blend traditional learning with practical experiences to help these children build a brighter future.


    <img src="/img/2024-09-19-Scaling-Rural-Education/CInI-1.png">

## CInI’s Vision: Empowering Through Education

CInI, started in 2007, aims to improve the lives of tribal households in Central India. Their education program is unique, combining book learning with hands-on activities. Here’s what they’re doing:

- **Systems Strengthening**: Collaborating with departments of Education to establish itself as a resource for community strengthening and Foundational Literacy and Numeracy.
- **Making School Environments Vibrant**: Making classrooms visually engaging and fun through creating print rich environment, developing kitchen gardens to teach kids about responsibility and sustainable living, engaging children through libraries, and integrating technology.
- **Academic Enrichment**: Focus on improving Foundational Literacy and Numeracy through academic interventions and teacher support.
- **Community Engagement**: Involve SMCs, Panchayati Raj Institutions (PRIs) and parents in children’s education and school development through a strong model of engagement. 
- **Continuous Assessments**: Helping students understand key concepts and find areas where they need more help.

CInI focuses on timely interventions to continuously improve the classroom environment and overall quality of education. It's amazing to see how these initiatives are shaping a self-sustaining future for these kids!


    <img src="/img/2024-09-19-Scaling-Rural-Education/CInI-2.png">

## Avni’s Role in Enhancing Education Outcomes

CInI recognised the need for efficient data collection to monitor and improve its education initiatives. The challenge was to streamline the process and make use of data to track progress in real time. Avni has become an integral tool in addressing this need, offering a user-friendly, low-code mechanism for field data collection. Our platform supports CInI in tracking various aspects of their programs, including:

- **Professional Development and Classroom Practices**: Training for teachers and headmasters, and monitoring updated classroom practices.
- **Student Assessments and Readiness**: Evaluating language, math, and science skills, and readiness for school.
- **School and Library Management**: Involvement of school management committees and profiling library activities.
- **On-Site Support and Monitoring**: Providing demo classes, on-site support for teachers, and monitoring classroom quality and student attendance.
- **Early Childhood and FLN (Foundational Learning and Numeracy) Programs**: Observing Anganwadis, monitoring Early Childhood Care and Education programs, and the FLN program.

By enabling real-time data collection and analysis, Avni allows us to make informed, data-driven decisions, ultimately enhancing education outcomes.

## Impact of Digital Adoption on the Program

The digital shift brought several benefits to CInI’s education program:

- **Streamlined Data Collection**: Avni enables real-time data entry through mobile devices, ensuring that information about student attendance, assessments, and classroom conditions is captured efficiently.
- **Data Accuracy**: Custom-designed digital forms with single and multi-select options reduce manual errors, providing more reliable insights.
- **Automated Scheduling and Follow-ups**: Avni’s platform automates visit schedules and follow-ups for coordinators, ensuring consistent monitoring across schools and Anganwadis.

Here are few clips of the CInI program in the Avni app:


    <img src="/img/2024-09-19-Scaling-Rural-Education/CInI-3.gif">

## The People Behind the Data: User Personas

Here are some key personas using Avni in the field:

- **Field Coordinators**: Responsible for visiting schools and Anganwadis, Field Coordinators use Avni to schedule visits, track progress, and report on any issues or improvements needed.
- **Cluster Coordinators**: Overseeing several field coordinators, Cluster Coordinators monitor the overall progress of multiple schools and Anganwadis within their designated clusters, ensuring that reports are timely and accurate.
- **State Coordinators**: At a higher level, State Coordinators manage the education program across several districts. They use Avni to analyse field data, assess overall program performance, and provide strategic input to improve the education initiatives in their region.

## The Journey So Far

As of July 2024, Avni is being used in three districts of Odisha and eight districts of Jharkhand. The platform supports over 2,500 schools, 4,500 school teachers, 490 Anganwadis, and 520 Anganwadi Workers, each of whom is now empowered to capture and act on data like never before.


    <img src="/img/2024-09-19-Scaling-Rural-Education/CInI-4.png">


CInI and its more than 150 users are working on the ground to elevate the quality of education. By prioritising robust assessments, Academic Enrichment has recorded an average of 30%  improvement in language and in math. CInI has successfully set up more than 1200 libraries in the schools and Anganwadis so far.

## Related Topics

<!-- Add links to related documentation -->


---
<!-- Source: 09-implementation-guides/implementation-checklist.md -->

# Implementation Checklist

## TL;DR

<!-- TODO: Add 2-3 sentence summary of Implementation Checklist -->

## Overview

**What:** <!-- TODO: One-sentence description -->

**When to use:** <!-- TODO: Scenarios -->

**Prerequisites:** <!-- TODO: What to know first -->

## Planning Checklist

<!-- TODO: Add content for planning-checklist -->

## Setup Checklist

<!-- TODO: Add content for setup-checklist -->

## Development Checklist

<!-- TODO: Add content for development-checklist -->

## Testing Checklist

<!-- TODO: Add content for testing-checklist -->

## Deployment Checklist

<!-- TODO: Add content for deployment-checklist -->

## Related Topics

<!-- TODO: Add links to related documentation -->


---
<!-- Source: 09-implementation-guides/maternal-health-example.md -->

# Implementation Example: Maternal Health Tracking

## TL;DR

featuredstudy: false
tags:
  - Health
  - Case Study
---
There are parts of India where the road connectivity from the villages to the nearest block headquarter is quite poor. One such place (tehsil, i.e.

## Overview

featuredstudy: false
tags:
  - Health
  - Case Study
---
There are parts of India where the road connectivity from the villages to the nearest block headquarter is quite poor. One such place (tehsil, i.e. block or sub-district) is <a href="https://www.mapsofindia.com/villages/maharashtra/gadchiroli/bhamragad/" target="_blank" rel="noopener noreferrer">Bhamraghad</a>. <a href="http://www.lokbiradariprakalp.org/" target="_blank" rel="noopener noreferrer">Lokbiradari Prakalp</a> (LBP), in village Hemalkasa, is the literal lifeline of this and neighbouring blocks, because it has a hospital (do go to the home page of Lokbiradari Prakalp and see the photos to get the feel of the place and the hospital).

For many months of the year, getting to the hospital from the villages in the same block can be quite difficult. One may need to wade through knee/waist height water for a couple of hours, to reach the hospital. For certain illnesses seeing the doctor is the only option. But in many conditions like fever, headache, diarrhoea, vomiting, acidity, scabies, etc - going or taking someone to the hospital, losing one day of employment is not feasible. Ordinarily, in the public health system, there is nearby <a href="http://nrhmmeghalaya.nic.in/sub-centres-scs" target="_blank" rel="noopener noreferrer">subcenter</a> with a trained nurse whom one can go to. But these subcenters are only partially operational - leaving people with fewer options.

To resolve this problem LBP along with the village representatives, decided to run health centres for every 6 villages. These health centres to have medicines, and a few other basic facilities like weighing machine, BP machine, etc. These pharmacies were to be run by a selected person from one of these villages - called arogyadoots or community health workers (CHWs).

Overall the CHWs were responsible for:

1. categorise the complaint into one or more of 16 types
2. compute the quantity, form and number of doses of the medicine based on age, weight, gender & complaints
3. making referral in some cases instead of dispensing the medicines
4. note down the details for monitoring purpose

2 & 3 above are error-prone and monitoring of the work from the paper records was difficult. There was a need for a solution that could do 2,3 & 4; from a mobile device, offline. Also, consolidate all this data in a central place for analysis.

- - -

While many data collection products allow for forms with user-defined fields, skip logic etc. We wanted to allow for the insertion of programmable logic in various parts of the workflow. This programmable logic being specific only to that implementation. This ability differentiates Avni from other products. Avni allows for JavaScript-based rules, a language that has the most number of programmers - hence it is easy to find them.

This was the first use-case of Avni (then called OpenCHS). Avni provided a simple mobile form which on completion did 2 & 3 based on rules configured for this implementation. On every interaction with the patient, the CHW would fill one form with 8–10 questions (there were other form questions like BP, Temperature, Pallor, Pedal Edema, Skin Condition, etc for later analysis).

This field app has been in use for the last three years now, by 6 health workers covering 30 villages of a total of 15,000 population. The health workers have almost no connectivity in the field. They travel to LBP once a month, for monthly discussions and at this point, they sync the data with the server. (This is an extremely low resource setup where in the villages the Internet has not reached, in most villages in India now, the Internet is of low quality but present. In such cases the data can be synchronised regularly.) At the time of writing, this is the only implementation of Avni that runs on the server on-premise. We made that decision because the Internet connectivity even from the hospital is not reliable.

![](/img/lbp-case-study-1-.png "Deployment of Avni at Lok Biradari Prakalp")

- - -

The software-based approach allowed LBP to change the prescription logic, medicines, for some of the complaints.

Currently, LBP plans to roll out another program, for maternal and child health - which has been configured and tested, as of now.

_ps: the health program has been described in more detail on LBP's website here._

- - -

**Credit for icons**

"designed by - https://www.flaticon.com/authors/roundicons, https://www.flaticon.com/authors/pixel-buddha, https://www.flaticon.com/authors/freepik, https://www.flaticon.com/authors/eucalyp - from Flaticon"


---
templateKey: case-study
title: Empowering Vision Care Project Chashma’s Transformation with Avni Platform
date: 2024-05-22T20:30:00.000Z
author: The Avni Team
description:
featuredpost: false
featuredimage:
tags:
  - Health
  - Case Study
---

## Executive Summary

Sarva Mangal Family Trust (SMFT), a non-profit organization, in collaboration with Bhansali Trust, also a non-profit organization working in healthcare, initiated Project Chashma with the ambitious goal of delivering eye care services to 20 million individuals within five years through partnerships with grassroots NGOs. However, the project encountered operational inefficiencies, especially in data management, during its initial stages, hindering its scalability and effectiveness. With the adoption of an open-source data collection and case management platform, Avni, these challenges were addressed, leading to streamlined data management and enhanced overall operational efficiency.

## The Challenges

Bhansali Trust’s expertise in organizing eye care camps, especially for cataract surgeries across diverse Indian regions, positioned them well to lead Project Chashma. Beginning with remote villages in North Gujarat, the project aimed to deliver comprehensive eye care services, encompassing patient registration, eye examinations & consultation, eyeglass distribution, patient referrals & follow-up for eye ailment treatment, and impact monitoring. However, as the project scaled, it encountered significant operational challenges:

- **Crowd Management and Data Collection**: The influx of patients led to overcrowded camps, making patient registration and data collection challenging. Manual data entry, due to its slow pace and susceptibility to errors, significantly hampered the project’s ability to effectively serve the community.
- **Data Management**: The manual data entry process resulted in inaccuracies and inefficiencies, causing a cumbersome transition to digital records.
- **Process Inefficiencies**: The initial setup lacked a streamlined process for patient flow and data collection, resulting in delays and a compromised patient experience.
- **Reporting & Evaluation**: The absence of automated reporting delayed insights and impeded the project’s ability to adapt and enhance its operations.
- **Impact Assessment**: Manual processes hindered timely and precise evaluation of the project’s impact, limiting the ability to make data-driven adjustments.
- **Routine Follow-up**: The project required a system for ongoing patient follow-ups to ensure the sustained impact of the treatments administered.

To overcome these challenges and streamline processes, the Trust sought a digital solution tailored for remote village settings where network connectivity is limited. A customized offline mobile application was developed on the Avni platform for data collection and real-time monitoring at different stages of the process.

## Implementation

In response, the project team revamped the patient flow and data collection processes, integrating the Avni platform for its robust offline capabilities and comprehensive data management tools.

Avni is an open-source platform for on-field service delivery and data collection. Designed for the development sector, Avni strengthens field capacity for non-profits and governments across sectors like health, water, education, and social welfare.


    <img src="/img/2024-05-22-Empowering-vision-care-Chashma-tech4dev/avni-block-diagram.png">**Avni Block Diagram**


        <img src="/img/2024-05-22-Empowering-vision-care-Chashma-tech4dev/dashboard-patient-registration.png">**Avni Mobile App Dashboard & Patient Registration**


        <img src="/img/2024-05-22-Empowering-vision-care-Chashma-tech4dev/dashboard-patient-registration.png">**Avni Mobile App Dashboard & Patient Registration**


        <img src="/img/2024-05-22-Empowering-vision-care-Chashma-tech4dev/participation-gender-age-group.png">**Patients Participation in the Eye-camp by Gender & Age-Group**


        <img src="/img/2024-05-22-Empowering-vision-care-Chashma-tech4dev/percentage-of-student-need-eyeglasses.png">**Patients Participation and Percentage of Adults and Students Need Eyeglasses**

## Impact

The strategic enhancements facilitated by the Avni digital solution resulted in notable improvements in operational efficiency throughout the project:

- **Token System for Crowd Management**: Introducing a token system improved patient flow and organization at the camps, mitigating overcrowding and streamlining the registration process.
- **Digital Data Collection**: The offline data collection feature of Avni streamlined and expedited the data collection process, ensuring consistent and precise patient records. This facilitated a more reliable assessment of eye care needs and interventions.
- **Automated Reporting**: The customizable reports and analytics features of Avni facilitated timely and automated impact assessments, reducing the need for manual labor and enabling a more profound understanding of the project’s effectiveness.
- **Enhanced Impact Assessment**: The integration of real-time data collection and analysis capabilities enabled the project to accurately measure its impact, facilitating prompt adjustments to better meet community needs. Additionally, real-time data access and user-friendly dashboards enhanced transparency and collaboration, enabling informed decision-making at all organizational levels.
- **Improved Patient Outcomes**: By leveraging efficient monitoring and routine follow-up capabilities of the solution, the project ensured that patients received timely and appropriate care, thereby enhancing its overall impact on community health.
- **Staff Training and Upskilling**: Focused training sessions equipped staff with the skills needed to effectively utilize the Avni platform, facilitating a seamless transition to digital data management.

The Avni platform not only resolved the project’s immediate data management challenges but also established a scalable model for future expansion, with the potential for adoption by other grassroots organizations. With real-time access to data and enhanced process efficiencies, the project was able to effectively serve a larger population, marking a significant advancement in its mission.

## Conclusion

The integration of the Avni platform into Project Chashma’s operations has been transformative, addressing critical challenges in crowd management, data collection, staff upskilling, and impact assessment. The improvements in process efficiency and data management capabilities have not only bolstered the project’s effectiveness but have also set a new standard for leveraging technology in nonprofit initiatives. Project Chashma’s experience underscores the potential of digital tools to enhance service delivery and expand impact, serving as a valuable blueprint for other NGOs aiming to scale their efforts in underserved communities.


*Tech4Dev has published this insightful article detailing the transformative impact of the Avni platform on Project Chashma, led by Sarva Mangal Family Trust (SMFT) and Bhansali Trust. The article tells how Avni's offline capabilities and robust data management tools have improved patient registration, eye exams, eyeglass distribution, follow-up treatments, and overall project impact assessment, setting a new benchmark for technology in non-profit initiatives.*


---
templateKey: case-study
title: Scaling Rural Education - How Schools And Anganwadis Are Building Lifelong Skills Beyond the Classroom
date: 2024-09-19T20:30:00.000Z
author: The Avni Team
description:
featuredpost: false
featuredimage: /img/2024-09-19-Scaling-Rural-Education/CInI-1.png
tags:
  - Education
  - Case Study
---


In the heart of rural India, education is getting a fresh makeover. It’s not just about reading and writing anymore; it’s about giving children the skills they need for life. The Collectives for Integrated Livelihood Initiatives (CInI), part of Tata Trusts, is leading this change, reaching over 250,000 students in rural and tribal areas in Odisha and Jharkhand. They blend traditional learning with practical experiences to help these children build a brighter future.


    <img src="/img/2024-09-19-Scaling-Rural-Education/CInI-1.png">

## CInI’s Vision: Empowering Through Education

CInI, started in 2007, aims to improve the lives of tribal households in Central India. Their education program is unique, combining book learning with hands-on activities. Here’s what they’re doing:

- **Systems Strengthening**: Collaborating with departments of Education to establish itself as a resource for community strengthening and Foundational Literacy and Numeracy.
- **Making School Environments Vibrant**: Making classrooms visually engaging and fun through creating print rich environment, developing kitchen gardens to teach kids about responsibility and sustainable living, engaging children through libraries, and integrating technology.
- **Academic Enrichment**: Focus on improving Foundational Literacy and Numeracy through academic interventions and teacher support.
- **Community Engagement**: Involve SMCs, Panchayati Raj Institutions (PRIs) and parents in children’s education and school development through a strong model of engagement. 
- **Continuous Assessments**: Helping students understand key concepts and find areas where they need more help.

CInI focuses on timely interventions to continuously improve the classroom environment and overall quality of education. It's amazing to see how these initiatives are shaping a self-sustaining future for these kids!


    <img src="/img/2024-09-19-Scaling-Rural-Education/CInI-2.png">

## Avni’s Role in Enhancing Education Outcomes

CInI recognised the need for efficient data collection to monitor and improve its education initiatives. The challenge was to streamline the process and make use of data to track progress in real time. Avni has become an integral tool in addressing this need, offering a user-friendly, low-code mechanism for field data collection. Our platform supports CInI in tracking various aspects of their programs, including:

- **Professional Development and Classroom Practices**: Training for teachers and headmasters, and monitoring updated classroom practices.
- **Student Assessments and Readiness**: Evaluating language, math, and science skills, and readiness for school.
- **School and Library Management**: Involvement of school management committees and profiling library activities.
- **On-Site Support and Monitoring**: Providing demo classes, on-site support for teachers, and monitoring classroom quality and student attendance.
- **Early Childhood and FLN (Foundational Learning and Numeracy) Programs**: Observing Anganwadis, monitoring Early Childhood Care and Education programs, and the FLN program.

By enabling real-time data collection and analysis, Avni allows us to make informed, data-driven decisions, ultimately enhancing education outcomes.

## Impact of Digital Adoption on the Program

The digital shift brought several benefits to CInI’s education program:

- **Streamlined Data Collection**: Avni enables real-time data entry through mobile devices, ensuring that information about student attendance, assessments, and classroom conditions is captured efficiently.
- **Data Accuracy**: Custom-designed digital forms with single and multi-select options reduce manual errors, providing more reliable insights.
- **Automated Scheduling and Follow-ups**: Avni’s platform automates visit schedules and follow-ups for coordinators, ensuring consistent monitoring across schools and Anganwadis.

Here are few clips of the CInI program in the Avni app:


    <img src="/img/2024-09-19-Scaling-Rural-Education/CInI-3.gif">

## The People Behind the Data: User Personas

Here are some key personas using Avni in the field:

- **Field Coordinators**: Responsible for visiting schools and Anganwadis, Field Coordinators use Avni to schedule visits, track progress, and report on any issues or improvements needed.
- **Cluster Coordinators**: Overseeing several field coordinators, Cluster Coordinators monitor the overall progress of multiple schools and Anganwadis within their designated clusters, ensuring that reports are timely and accurate.

## Frequently Asked Questions

### Q: What types of data fields are supported in Avni?

Concept DataType - Description
Numeric concepts - Numeric concepts are used to capture numbers. When creating a numeric concept, you can define normal ranges and absolute ranges. In the field application, if an observation for a concept collected goes beyond the normal range, then it is highlighted in red. Values above the absolute range are not allowed. For instance for concept: Blood Pressure (Systolic), you can choose a Numeric concept with ranges.

Coded concepts (and NA concepts) - Coded concepts are those that have a fixed set of answers. For instance for Blood Group you would choose a coded concept with values: A+, B+, AB+, etc.

These answers are also defined as concepts of NA datatype.

ID datatype - A concept of Id datatype is used to store autogenerated ids. See Creating identifiers for more information on creating autogenerated ids. For instance PatientIDs, TestIDs, etc.

Media concepts (Image, Video and Audio) - Images and videos can be captured using Image and Video concept datatypes. For audio recording, Audio datatype can be used.

Text (and Notes) concepts - The Text data type helps capture one-line text while the Notes datatype is used to capture longer form text.

Date and time concepts - There are different datatypes that can be used to capture date and time.
*Date** - A simple date with no time
*Time** - Just the time of day, with no date
*DateTime** - To store both date and time in a single observation
*Duration** - To capture durations such as 4 weeks, 2 days etc.
Location concepts - Location concepts can be used to capture locations based on the location types configured in your implementation.
Location concepts have 3 attributes:
- Within Catchment - Denotes whether the location to be captured would be within the catchment already assigned to your field workers. This attribute defaults to true and is mandatory.
- Lowest Level(s) - Denotes the lowest location type(s) you intend to capture via form elements using this concept. This attribute is mandatory.
- Highest Level - Denotes the highest location type that you would like to capture via form elements using this concept. This attribute is optional.
Subject concepts - Subject concepts can be used to link to other subjects. Each Subject concept can map to a single subject type. Any form element using this concept can capture one or multiple subjects of the specified subject type.
Phone Number concepts - For capturing the phone number. It comes with a 10 digit validation. OTP verification can be enabled by turning on the "Switch on Verification" option. Avni uses msg91 for OTP messages, so msg91 Auth key and Template need to be step up using the admin app.
Group Affiliation concepts - Whenever automatic addition of a subject to a group is required Group Affiliation concept can be used. It provides the list of all the group subjects in the form and choosing any group will add that subject to that group when the form is saved.
Encounter - Encounter concepts can be used to link an encounter to any form. Each Encounter concept can map to a single encounter type. It should also provide the scope to search that encounter. Also, name identifiers can be constructed by specifying the concepts used in the encounter form. Any form element using this concept can capture one or multiple encounters of the specified encounter type.

### Q: What’s the difference between subject, program, and encounter?

A Subject is the base entity for which data is collected. A subject can be a person, a household, a class, or even non-human entities like a waterbody or a toilet.

A Program is used to monitor a subject over a defined period.

Every program has an enrolment form (entry point) and an exit form (exit point).

Example: Pregnancy can be a program, with ANC and Delivery as program encounters. The enrolment form may capture one-time details like LMP and EDD.

In addition, subjects can have general encounters that are not tied to a program.

Example: Monitoring a waterbody daily without any enrolment or exit.

### Q: How do I design a workflow for maternal health tracking?

Maternal Health / Pregnancy Workflow in Avni
1. Create the Subject

Type: Person

Purpose: Represents the pregnant woman whose health is being tracked.

2. Registration Form

Contains: Basic personal and demographic details.

Captured once at the time of creating the subject.

3. Configure the Program

Program Name: Pregnancy / Maternal Health

Program Components:

Enrolment Form

Captures one-time pregnancy details:

Last Menstrual Period (LMP)

Expected Delivery Date (EDD)

Height, weight

Previous pregnancy details

ANC (Antenatal Care) Forms

Scheduled automatically based on LMP date.

Tracks visits, vitals, investigations, and interventions during pregnancy.

Delivery Form

Captures delivery details, mode of delivery, complications, birth outcomes.

PNC (Postnatal Care) Forms

Scheduled after delivery.

Tracks maternal and newborn health.

Exit Form

Marks the completion of the program for that subject.

4. Scheduling

All ANC and PNC visits are scheduled based on the LMP or delivery date.

Reminders and follow-ups can be set automatically.

5. Data Flow

Subject created → registration form filled

Subject enrolled into Pregnancy Program → enrolment form captures one-time pregnancy details

ANC visits tracked and scheduled automatically

Delivery recorded → triggers PNC scheduling

PNC visits tracked

Exit form completes the program
This structure ensures complete lifecycle tracking of maternal health, from registration to postnatal follow-up, with automated scheduling based on pregnancy dates.

### Q: How do I configure a multi-step service delivery workflow?

Configuring Multi-Step Service Delivery in Avni
1. Independent Services

If the services are independent of each other, Avni allows multiple program enrolments for a subject at the same time.

Example: A person can be enrolled in both:

Pregnancy Program

Mental Health Program

Each program runs independently, with its own forms, schedules, and follow-ups.

2. Dependent Services / Multi-Step Workflow

If the service delivery steps are dependent on each other, you can configure them within the same program:

Use assessment forms scheduled at predefined intervals.

Add logic rules to trigger specific forms based on previous data or conditions.

Example:

Step 1: Initial assessment

Step 2: Trigger counseling form if certain risk indicators are recorded in Step 1

Step 3: Follow-up visit forms automatically scheduled based on Step 2 outcomes

### Q: How do I configure a one-time survey vs. ongoing case?

1. One-Time Survey

Can be captured:

Within the subject registration form itself

Or as a general encounter outside any program

Ideal for surveys or data collection that happens only once per subject.

2. Ongoing Case

Best managed using a program in Avni.

Programs allow you to:

Track the enrolment of the subject

Capture multiple encounters over time (e.g., ANC visits, monitoring forms)

Record exit of the case along with exit reasons (e.g., completed, migrated, dropped out)

Suitable for scenarios requiring longitudinal tracking and multiple touchpoints.

### Q: What’s the best way to model school → student tracking?

In Avni, registering a school as a subject can be avoided if no specific information needs to be captured against it. Instead, the school can be configured as a location, and classes and students can be registered under the same school location. Classes can be set up as group subjects, and students as person subject types, assigned to their respective classes. Forms can then be configured for any subject or class where data needs to be captured—for example, classrooms can have daily attendance forms scheduled, which users can fill out directly from the app, enabling efficient tracking of students within the school.

### Q: How do I write a rule to calculate BMI in Avni?

// SAMPLE RULE EXAMPLE: Calculate BMI from Height and Weight
'use strict';
({ params, imports }) => {
  const programEnrolment = params.entity;        // Current program enrolment
  const formElement = params.formElement;        // The form element this rule is linked to
  
  // Fetch observations for Height and Weight (update names as per your form)
  let height = programEnrolment.findObservation("Height of women");
  let weight = programEnrolment.findObservation("Weight of women");
  
  height = height && height.getValue();
  weight = weight && weight.getValue();

  let value = '';
  
  // If both height and weight are valid numbers, calculate BMI
  if (_.isFinite(weight) && _.isFinite(height)) {
    value = ruleServiceLibraryInterfaceForSharingModules
              .common
              .calculateBMI(weight, height);
  }

  // Return the BMI value into the current form element
  return new imports.rulesConfig.FormElementStatus(formElement.uuid, true, value);  
};

Replace "Height of women" and "Weight of women" with the exact observation names in your form.

calculateBMI is already available in the shared rule service library, so no need to manually code the math.

This rule is from the Pregnancy Program Enrolment form

### Q: Can I integrate Avni with SMS or WhatsApp alerts?

**Answer:** Avni provides comprehensive communication capabilities through SMS and WhatsApp integrations:

### SMS Integration (MSG91)
- Password reset OTP and user credential sharing
- Phone number verification for beneficiaries
- Multi-language support with secure authentication

### WhatsApp Integration (Glific)
- Trigger WhatsApp messages on events (registration, enrollment, visits)
- Bulk and individual messaging capabilities

**Use cases:** Health camp reminders, ANC visit alerts, motivational content, field worker notifications

**Setup:** Organizations need MSG91 and Glific accounts configured in Avni.

### Q: Answer: yes we can configure cascading drop-downs of Locations or Coded Concepts.

### Location Concepts
Yes, for locations, we can do it through Location concepts:

- **Location concept type:** Supports hierarchical location selection
- **Configuration attributes:**
  - **Within Catchment:** Whether locations must be within assigned catchments
  - **Lowest Level(s):** The most granular location types to capture
  - **Highest Level:** The broadest location type to capture

- **Implementation:** Location concepts automatically provide cascading selection based on your configured location hierarchy (state → district → village)
- **Catchment control:** Can restrict selections to locations within field workers' assigned areas or across the entire Location heirarchy of the organisation.


### Coded Concept Hierarchies
Coded concepts can be structured in multiple levels with parent-child relationships:

- **Level 1:** Primary categories (e.g., "Health Services")
- **Level 2:** Sub-categories (e.g., "Maternal Health", "Child Health")  
- **Level 3:** Specific services (e.g., "ANC Visit", "PNC Visit", "Immunization")
We can configure FormElementRules to show / hide Answer Concepts at lower levels based on the selection of higher level concepts.

### Q: Can I create dynamic labels based on other field values?

Yes, you can create dynamic labels based on other fields by adding a rule to the field, either manually or by using the Rule Builder. For detailed steps, refer to the Avni documentation on ReadMe
 or reach out to our support team for assistance.

## Related Topics

<!-- Add links to related documentation -->


================================================================================
# Section: Reference
================================================================================


---
<!-- Source: 10-reference/README.md -->

# Reference Materials

Reference materials including frequently asked questions, API endpoints for configuration, and version compatibility information.

## Contents

### 1. [Frequently Asked Questions - Implementation](faq-implementation.md)
FAQ  frequently asked questions  common questions  implementation questions

### 2. [API Endpoints for Configuration](api-endpoints.md)
API  endpoints  REST API  configuration API

### 3. [Version Compatibility Guide](version-compatibility.md)
version  compatibility  release notes  feature availability


---
<!-- Source: 10-reference/api-endpoints.md -->

# API Endpoints for Configuration

## TL;DR

<!-- TODO: Add 2-3 sentence summary of API Endpoints for Configuration -->

## Overview

**What:** <!-- TODO: One-sentence description -->

**When to use:** <!-- TODO: Scenarios -->

**Prerequisites:** <!-- TODO: What to know first -->

## Common Endpoints

<!-- TODO: Add content for common-endpoints -->

## Related Topics

<!-- TODO: Add links to related documentation -->


---
<!-- Source: 10-reference/faq-implementation.md -->

# Frequently Asked Questions - Implementation

## TL;DR

Subject Types can be created through the App Designer.1. Go to App Designer > Subject Types > Add New Subject Type

## How do I create a new subject type in Avni?

Subject Types can be created through the App Designer.1. Go to App Designer > Subject Types > Add New Subject Type

## How do I add or remove a new field to an existing form?

Fields can be added to forms through the App Designer. You can reach the form through different means.
1. Go to App Designer > Forms > Select the form
2. Go to App Designer > Subject Types, Programs or Encounter Types > Select the form you need to edit
3. Navigate to the section/page you wish to add the field to. If required, add a new section/page As you hover over the left portion, you will see a + button. Click on it to add a new field.
Each Form field has a few components.
1. Question - This is what shows up in your form
2. Concept - This is the internal name of the field. It is also shown in patient dashboards, reports etc. Normally, we keep the name of the concept to be the same as the question. Remember that there can only be one concept with a certain name in the entire system. Also, a concept can be used only once in a form. Based on the data type of the concept, you will have a few questions to answer to configure it correctly.
3. Rule - There are three rules that you can configure for a question -
1. Show/Hide question - This is used to show or hide the question based on a certain condition.
2. Validation Rule - Based on conditions, you might show an error to the user
3. Value Rule - Based on conditions, you might set an answer value
The rules section is available by clicking on "RULE" section on the left side of the question

## What types of data fields are supported in Avni?

Concept DataType - Description
Numeric concepts - Numeric concepts are used to capture numbers. When creating a numeric concept, you can define normal ranges and absolute ranges. In the field application, if an observation for a concept collected goes beyond the normal range, then it is highlighted in red. Values above the absolute range are not allowed. For instance for concept: Blood Pressure (Systolic), you can choose a Numeric concept with ranges.

Coded concepts (and NA concepts) - Coded concepts are those that have a fixed set of answers. For instance for Blood Group you would choose a coded concept with values: A+, B+, AB+, etc.

These answers are also defined as concepts of NA datatype.

ID datatype - A concept of Id datatype is used to store autogenerated ids. See Creating identifiers for more information on creating autogenerated ids. For instance PatientIDs, TestIDs, etc.

Media concepts (Image, Video and Audio) - Images and videos can be captured using Image and Video concept datatypes. For audio recording, Audio datatype can be used.

Text (and Notes) concepts - The Text data type helps capture one-line text while the Notes datatype is used to capture longer form text.

Date and time concepts - There are different datatypes that can be used to capture date and time.
*Date** - A simple date with no time
*Time** - Just the time of day, with no date
*DateTime** - To store both date and time in a single observation
*Duration** - To capture durations such as 4 weeks, 2 days etc.
Location concepts - Location concepts can be used to capture locations based on the location types configured in your implementation.
Location concepts have 3 attributes:
- Within Catchment - Denotes whether the location to be captured would be within the catchment already assigned to your field workers. This attribute defaults to true and is mandatory.
- Lowest Level(s) - Denotes the lowest location type(s) you intend to capture via form elements using this concept. This attribute is mandatory.
- Highest Level - Denotes the highest location type that you would like to capture via form elements using this concept. This attribute is optional.
Subject concepts - Subject concepts can be used to link to other subjects. Each Subject concept can map to a single subject type. Any form element using this concept can capture one or multiple subjects of the specified subject type.
Phone Number concepts - For capturing the phone number. It comes with a 10 digit validation. OTP verification can be enabled by turning on the "Switch on Verification" option. Avni uses msg91 for OTP messages, so msg91 Auth key and Template need to be step up using the admin app.
Group Affiliation concepts - Whenever automatic addition of a subject to a group is required Group Affiliation concept can be used. It provides the list of all the group subjects in the form and choosing any group will add that subject to that group when the form is saved.
Encounter - Encounter concepts can be used to link an encounter to any form. Each Encounter concept can map to a single encounter type. It should also provide the scope to search that encounter. Also, name identifiers can be constructed by specifying the concepts used in the encounter form. Any form element using this concept can capture one or multiple encounters of the specified encounter type.

## How can I configure skip logic between form fields?

Skip logic is implemented through rules in Avni. Every field on the Form Designer has a "Rule" section. You can configure skip logic by adding the logic and then clicking on "Show/Hide question".

## Can I do regex validations in Avni?

Yes. Regular expression validations are available for Text concepts in Avni. When you choose a text concept for a question, you get to fill in two other fields - "Validation Regex" and "Validation Description Key". These allow you to enter the regex, and a description of the error message to show when the text does not match the regular expression

## Can I make a form available only to specific user groups?

Yes. You can make a form available only to specific user groups by adding the group(s) to the form's "User Group" section. The User Group section is available on the Admin section.

## How do I configure a program with multiple stages?

Consider what data you need to collect in each stage of the program. Every stage is a different encounter type, and ia associated with a form. Encounter Type rules can be configured to ensure that only forms that are relevant at any point are shown in the app

## How do I make a question appear only if another answer is “Yes”?

This can be achieved by adding skip logic rule on the form fields

## Can Avni support multi-language forms?

Yes. Avni can be rolled out in multiple languages at once. To have your app in multiple languages,
1. Set up your language in Admin -> Languages
2. Go to Translations and download translations. Make changes in the zip file as appropriate and upload the translations back into the system
3. Usually an external tool like lokalise is used to add translations to the downloaded zip file

## How do I mark a field as mandatory?

In the form designer, go to the field you want to mark as mandatory. Check the box, and it will be shown as mandatory.
Remember that a field is mandatory only if it is visible. If you have created a visibility rule through which your form field is not visible, then the mandatory field on it will not be respected.

## Can I attach media (photos/audio) to a form in Avni?

Yes. Media concepts (image, video and audio) can be used to capture photos, videos, and audio in Avni. Choose the right data type to capture the media that you need

## How do I configure a follow-up encounter?

You can create a follow-up by creating a new encounter type. If you want it to be scheduled at a particular point in time, it can be done through the Visit Schedule Rule. You can find the Visit Schedule rule in the "Rules" section of a form. You can navigate to the form either through the "Forms" section of the App Designer or through the "Encounter Types"/"Programs"/"Subject Types" section of the Admin section.

## Can I edit a form after it has been deployed?

Yes. You can edit a form after it has been deployed by going to the form either through the "Forms" section of the App Designer or through the "Encounter Types"/"Programs"/"Subject Types" section of the Admin section. Any changes you make will be available to users once they sync the app.
Older filled forms will still have any questions you delete, but they cannot be modified anymore.

## How do I duplicate an existing form configuration?

In the Forms section, a form has a "Clone form" option. This can be used to duplicate an existing form.

## How can I make a numeric field accept only integers?

By applying a validation rule on that particular numeric field

## How do I configure a calculated field in Avni?

For a calculated field, a javacript snippet needs to written, sharing sample -

use strict';
({params, imports}) => {
    const programEncounter = params.entity;
    const individual = programEncounter.programEnrolment.individual;
    const moment = imports.moment;
    const formElement = params.formElement;
    const _ = imports.lodash;
    let visibility = true;
    let value = null;
    let answersToSkip = [];
    let validationErrors = [];

    const totalParticipants = individual.getGroupSubjects();

    const participants = programEncounter.getObservationReadableValue("d81c0be9-77fb-4673-af36-4b28773a6378");

    if(participants && participants.length > 0) value = totalParticipants.length - participants.length;
    else value = totalParticipants.length;

    return new imports.rulesConfig.FormElementStatus(formElement.uuid, visibility, value, answersToSkip, validationErrors);
};

## Can I limit form access based on user roles?

Yes, form access can be configured on basis of the user's role. Under Webapp >> User groups >> Select the user group >> Permissions
Under permissions tab there will be different permissions for each entity in Avni, based on requirement it can be configured

## What’s the difference between subject, program, and encounter?

A Subject is the base entity for which data is collected. A subject can be a person, a household, a class, or even non-human entities like a waterbody or a toilet.

A Program is used to monitor a subject over a defined period.

Every program has an enrolment form (entry point) and an exit form (exit point).

Example: Pregnancy can be a program, with ANC and Delivery as program encounters. The enrolment form may capture one-time details like LMP and EDD.

In addition, subjects can have general encounters that are not tied to a program.

Example: Monitoring a waterbody daily without any enrolment or exit.

## How do I design a workflow for maternal health tracking?

Maternal Health / Pregnancy Workflow in Avni
1. Create the Subject

Type: Person

Purpose: Represents the pregnant woman whose health is being tracked.

2. Registration Form

Contains: Basic personal and demographic details.

Captured once at the time of creating the subject.

3. Configure the Program

Program Name: Pregnancy / Maternal Health

Program Components:

Enrolment Form

Captures one-time pregnancy details:

Last Menstrual Period (LMP)

Expected Delivery Date (EDD)

Height, weight

Previous pregnancy details

ANC (Antenatal Care) Forms

Scheduled automatically based on LMP date.

Tracks visits, vitals, investigations, and interventions during pregnancy.

Delivery Form

Captures delivery details, mode of delivery, complications, birth outcomes.

PNC (Postnatal Care) Forms

Scheduled after delivery.

Tracks maternal and newborn health.

Exit Form

Marks the completion of the program for that subject.

4. Scheduling

All ANC and PNC visits are scheduled based on the LMP or delivery date.

Reminders and follow-ups can be set automatically.

5. Data Flow

Subject created → registration form filled

Subject enrolled into Pregnancy Program → enrolment form captures one-time pregnancy details

ANC visits tracked and scheduled automatically

Delivery recorded → triggers PNC scheduling

PNC visits tracked

Exit form completes the program
This structure ensures complete lifecycle tracking of maternal health, from registration to postnatal follow-up, with automated scheduling based on pregnancy dates.

## How can I model household → individual relationships?

Modeling Household → Individual Relationships in Avni
1. Define Relationships

Navigate to: Webapp → App Designer → Relationships → Define

Here you can define the types of relationships that exist between individuals in a household.

Examples: Mother, Father, Daughter, Son

You can also specify which gender each relationship applies to.

2. Configure Relationship Types

Go to: Webapp → App Designer → Relationship Types → Add New

Create a relationship and its reverse.

Example:

Mother → Son → reverse is Son → Mother

Mother → Daughter → reverse is Daughter → Mother

Father → Son → reverse is Son → Father

Father → Daughter → reverse is Daughter → Father

3. Usage

Once defined, these relationships can be assigned to individuals within a household.

This enables tracking of household members, family hierarchies, and dependent relationships.

## How do I track recurring visits for a subject?

Recurring visits for a subject can be tracked by configuring the Visit Schedule Rule under the subject registration form in Webapp → App Designer. You can use the drop-down rule designer to set fixed-frequency visits for any form. For more complex or custom scheduling, a JavaScript rule can be written. Sample rules are available in the README documentation

## How do I set up a longitudinal data collection workflow?

Setting Up a Longitudinal Data Collection Workflow in Avni

Understand Longitudinal Data Collection

Avni is designed for longitudinal data collection, allowing you to capture data for a subject (the on-ground entity) over time, at predefined intervals and frequencies.

This ensures structured, continuous tracking of any subject, such as a person, household, or facility.

Configure Data Collection

Define your subjects and forms in Webapp → App Designer.

Set up visit schedules, program encounters, or recurring forms to capture data at the required frequency.

Export Longitudinal Data

Navigate to Webapp → Longitudinal Export.

You can download the data in a format that maintains the chronological order of observations for each subject.

This gives you a ready-to-analyze dataset showing how data for a subject changes over time.

## What’s the best way to handle referrals between workers?

Handling Referrals Between Workers in Avni

Set Up User Roles

Navigate to Webapp → User Groups.

Create different roles or user groups based on responsibilities.

Assign appropriate permissions to each group and add the respective users.

Schedule Referral Visits

Using the scheduling feature, you can assign referral visits to the appropriate worker.

These visits appear in the assigned user’s task list for follow-up.

Use Offline Report Cards

Configure offline report cards to highlight records that require referrals.

The responsible user can track and act on these referrals even when offline.

## How can I manage cases that get closed and reopened?

Managing Cases that Get Closed and Reopened in Avni

Cases Configured as Programs

When a subject is enrolled in a program, it can be exited (closed) using the Program Exit feature.

Reopening Cases

If a case needs to be reopened, you can undo the program exit.

This makes the subject/case available again for data recording and collection.

## How do I configure a multi-step service delivery workflow?

Configuring Multi-Step Service Delivery in Avni
1. Independent Services

If the services are independent of each other, Avni allows multiple program enrolments for a subject at the same time.

Example: A person can be enrolled in both:

Pregnancy Program

Mental Health Program

Each program runs independently, with its own forms, schedules, and follow-ups.

2. Dependent Services / Multi-Step Workflow

If the service delivery steps are dependent on each other, you can configure them within the same program:

Use assessment forms scheduled at predefined intervals.

Add logic rules to trigger specific forms based on previous data or conditions.

Example:

Step 1: Initial assessment

Step 2: Trigger counseling form if certain risk indicators are recorded in Step 1

Step 3: Follow-up visit forms automatically scheduled based on Step 2 outcomes

## Can I link a child record to a household subject?

Linking a Child Record to a Household Subject in Avni

Yes, you can link a child (or any individual) to a household subject in Avni.

Avni provides a built-in feature to:

Add members to a household

Designate the head of the household

Additionally, you can define relationships between household members to make the mapping clearer

## How do I manage subjects across multiple programs?

Managing Subjects Across Multiple Programs in Avni

Avni allows a single subject to be enrolled in multiple programs simultaneously.

There is no extra setup required to manage this.

Each program runs independently, with its own forms, schedules, and follow-ups, allowing flexible tracking of different services for the same subject.

This makes it easy to monitor multiple aspects of a subject’s data without conflicts or additional management overhead.

## How can I model seasonal data collection (e.g., crops)?

Modeling Seasonal Data Collection (e.g., Crops) in Avni

1.Schedule Forms at Predefined Times

In Avni, forms can be scheduled to appear at specific times of the year using predefined scheduling rules or logic.

This allows you to capture seasonal crop information at the right time for each subject (e.g., farm, field).

2. Use Conditional Logic for Fields

If the same form is used across seasons, you can hide or show fields dynamically based on:

Season

Crop type

Other user input or data logic

This ensures that only relevant information is captured during each season.

Multiple approaches in Avni allow flexible and accurate collection of seasonal data without creating separate forms for each season.

## How do I configure a one-time survey vs. ongoing case?

1. One-Time Survey

Can be captured:

Within the subject registration form itself

Or as a general encounter outside any program

Ideal for surveys or data collection that happens only once per subject.

2. Ongoing Case

Best managed using a program in Avni.

Programs allow you to:

Track the enrolment of the subject

Capture multiple encounters over time (e.g., ANC visits, monitoring forms)

Record exit of the case along with exit reasons (e.g., completed, migrated, dropped out)

Suitable for scenarios requiring longitudinal tracking and multiple touchpoints.

## How do I manage data across multiple locations?

In Avni, data can be collected against a specific location, and users (data entry personnel) can be assigned access to a predefined set of locations. This ensures that each user records data only for the locations they are responsible for. Additionally, MIS reports can be configured with location filters, allowing supervisors and managers to analyze and monitor data across multiple locations efficiently. This setup makes it easy to manage data collection, access control, and reporting for projects spread over different geographic areas.

## Can I assign subjects to specific users or teams?

Yes, Avni allows you to assign subjects to specific users or teams using the subject assignment feature. This can be configured under Webapp → App Designer → Subject Types → Select Subject, where the toggle “Sync by direct assignment” enables syncing of subjects directly assigned to users. The actual assignment of subjects can then be easily performed from Webapp → Assignment, ensuring that users or teams only access the subjects they are responsible for.

## How do I record both baseline and follow-up data?

Baseline data is typically collected at the start of a program, while follow-up data is recorded at subsequent visits. In Avni, both baseline and follow-up data collection can be easily configured using form visit scheduling, allowing you to define when each form should be filled for a subject, ensuring structured and timely data capture throughout the program.

## What’s the best way to model school → student tracking?

In Avni, registering a school as a subject can be avoided if no specific information needs to be captured against it. Instead, the school can be configured as a location, and classes and students can be registered under the same school location. Classes can be set up as group subjects, and students as person subject types, assigned to their respective classes. Forms can then be configured for any subject or class where data needs to be captured—for example, classrooms can have daily attendance forms scheduled, which users can fill out directly from the app, enabling efficient tracking of students within the school.

## How do I manage multiple identifiers for the same subject?

Avni does support identifiers, and multiple identifiers can be created and used for the same subject. However, since Avni is primarily an offline data collection tool, there are certain corner cases where duplicate identifiers may get assigned—for example, when the same user enters data on two devices or when the web-based data entry app is used. In such situations, it can become difficult to support and debug issues. Therefore, we generally do not recommend using multiple identifiers unless they are strictly distributed or tracked on the ground, where duplication risks are minimized.

## How can I record GPS location data with each encounter?

Avni provides the ability to capture GPS location data with each form submission. This can be enabled for any user by going to Webapp → Admin → Users, selecting the desired user, and toggling “Track Location” to true. Once enabled, the GPS coordinates will automatically be recorded whenever that user fills out a form, ensuring location tracking for each encounter.

## How do I set up case closure criteria?

If a case is managed as a program in Avni, users can decide when it should be closed based on their training and then complete the exit form with the correct exit information. Alternatively, closure criteria can be built into the workflow by assessing the data entered in each form and guiding the user to exit the program when predefined conditions are met. With some customization, the user flow within forms can also be structured to prompt or direct users toward program closure at the right time, ensuring consistency in case management.

## Can I link data from one form into another?

Yes, in Avni you can link data from one form into another. This is done using form element rules with JavaScript, which allow you to fetch data from previous forms and use it within the current form. Once fetched, the data can also be processed further based on your requirements, enabling seamless continuity across different forms.

## How do I write a rule to calculate BMI in Avni?

// SAMPLE RULE EXAMPLE: Calculate BMI from Height and Weight
'use strict';
({ params, imports }) => {
  const programEnrolment = params.entity;        // Current program enrolment
  const formElement = params.formElement;        // The form element this rule is linked to
  
  // Fetch observations for Height and Weight (update names as per your form)
  let height = programEnrolment.findObservation("Height of women");
  let weight = programEnrolment.findObservation("Weight of women");
  
  height = height && height.getValue();
  weight = weight && weight.getValue();

  let value = '';
  
  // If both height and weight are valid numbers, calculate BMI
  if (_.isFinite(weight) && _.isFinite(height)) {
    value = ruleServiceLibraryInterfaceForSharingModules
              .common
              .calculateBMI(weight, height);
  }

  // Return the BMI value into the current form element
  return new imports.rulesConfig.FormElementStatus(formElement.uuid, true, value);  
};

Replace "Height of women" and "Weight of women" with the exact observation names in your form.

calculateBMI is already available in the shared rule service library, so no need to manually code the math.

This rule is from the Pregnancy Program Enrolment form

## Can I prevent form submission if a rule fails?

No, Avni does not allow you to block form submission if a rule fails. Instead, when a rule fails, it creates an entry in the rule failure table, which helps developers or implementors identify and debug the issue. This ensures that data collection is not disrupted in the field, while still allowing backend teams to track and resolve rule-related errors.

## How do I create a rule to send an alert for high blood pressure?

Avni does not provide an in-app alert or notification feature. However, abnormal values like high blood pressure can still be highlighted during data entry. For example, while configuring a numeric field (such as BP Diastolic) in the App Designer, you can set thresholds (e.g., High Normal = 80). If a user enters a value above this, it will automatically be highlighted in red to indicate an abnormal condition. Additionally, these abnormal values can be included in decisions within the form, and the resulting decision outcomes can be displayed in the program summary of that individual, making it easier to track and review cases of high blood pressure. Furthermore, an offline report card can be configured to list and navigate to such cases, allowing field teams to easily identify and follow up on individuals with high BP.

## How do I check if a subject is under 5 years old in a rule?

Within a rule it can be easily accessed from the drop down avaiable. Or else in case you want to customise the rule further it can written in javascript like this- individual.getAgeInYears() < 5

## Can rules trigger notifications for supervisors?

No, Avni does not have a built-in notification or alert triggering system. However, this need can be addressed by configuring an offline report card on the supervisor’s app dashboard. The report card can be designed to display highlighted cases—such as abnormal conditions or referrals—that supervisors need to track. This way, instead of receiving notifications, supervisors can regularly review the dashboard to monitor the cases that require their attention.

## How do I create a rule for conditional program enrollment?

In Avni, conditional program enrollment can be handled using the Enrolment Eligibility Check Rule available under program configuration. You can add a custom rule here to define the eligibility criteria for a subject. When an individual does not meet the defined conditions, the option to enroll them in that program will not appear on their profile.

## Can I use JavaScript libraries inside Avni rules?

There are a few Javascript libraries that are present by default in the Avni rules. This include lodash and momentjs. 

Security restrictions limit the addition of other Javascript libraries within the rules

## How do I write a rule to auto-populate a field?

//Sample rule to autopopulate the height of child from his previously filled encounter - 
'use strict';
({params, imports}) => {
  const programEncounter = params.entity;
  const moment = imports.moment;
  const formElement = params.formElement;
  const _ = imports.lodash;
  let visibility = true;
  let value = null;
  let answersToSkip = [];
  let validationErrors = [];

  let obs = programEncounter.programEnrolment.findLatestObservationFromEncounters('Height', programEncounter);
  
   if(obs)
  {
  value=obs.getReadableValue();
  }
    
    
  return new imports.rulesConfig.FormElementStatus(formElement.uuid, visibility, value, answersToSkip, validationErrors);
};

OR it can be easily achieved via rule designer

## How do I validate a phone number with a regex rule?

A phone number is typically added as a Text concept with a validation rule. There are different regex rules that you can write. Some examples are

^[0-9]{10}$ - 10 digits only
((\+*)((0[ -]*)*|((91 )*))((\d{12})+|(\d{10})+))|\d{5}([- ]*)\d{6} - All different kinds of phone numbers

## How do I enforce that visits happen within 30 days?

You can add two dates when you schedule a visit. 
Due Date - The earliest date on which a visit is expected to happen
Overdue Date - The latest date by when a visit is expected to happen

Visits that are due and overdue can be shown on the app on the dashboard, and on reports. This allows users to understand which visits are due to be completed, and which ones have gone past the due date

## Can I access previous encounter data in a rule?

Yes, sample rule to fetch height from a previous encounter is -
'use strict';
({params, imports}) => {
  const programEncounter = params.entity;
  const moment = imports.moment;
  const formElement = params.formElement;
  const _ = imports.lodash;
  let visibility = true;
  let value = null;
  let answersToSkip = [];
  let validationErrors = [];

  let obs = programEncounter.programEnrolment.findLatestObservationFromEncounters('Height', programEncounter);
  
   if(obs)
  {
  value=obs.getReadableValue();
  }
    
    
  return new imports.rulesConfig.FormElementStatus(formElement.uuid, visibility, value, answersToSkip, validationErrors);
}; OR it can be easily achieved via rule designer

## How do I create a rule that prevents duplicate registration?

Under subject config on webapp there is a toggle for Unique names -  If active then user can't register a subject with duplicate names within their catchment

## How can I trigger a follow-up form automatically?

This can achieved via a visit scheduling rule of the form from the form after which the next followup should be scheduled. It can be configured via webapp >> app designer >> form >> Visit scheduling rule

## Can I write a rule to calculate gestational age?

Sample rule to calculate - "use strict";
({params, imports}) => {
    const programEncounter = params.entity;
    const formElement = params.formElement;
    
 let edd = programEncounter.programEnrolment
 .getObservationReadableValueInEntireEnrolment('Estimated Date of Delivery', programEncounter);
let dateOfDelivery = programEncounter.getObservationReadableValue('Date of delivery');
 
    
 const value = imports.motherCalculations
      .gestationalAgeForEDD(edd,dateOfDelivery);
      
 return new imports.rulesConfig.FormElementStatus(formElement.uuid, true, value);
};

## How do I enforce minimum and maximum age limits?

You can add a validation rule in the registration form to through a validation if the age limit is not matched. Until validation error is not resolved the registration couldn't be saved

## How do I use rules for referral workflows?

For referral workflows, multiple rules can be used -- Decision rules, program Summary rules and Custom offline report cards

## How do I debug a failing rule in Avni?

If a rule fails in the avni app, its entry will be available on Web app >> App designer >> Rule failures >> Find the rule failure with individual uuid or the timestamp, it will have further details of the rule failure which can be used to debug the issue and fix it accordingly

## Can I export all my rules for review?

No, only rules alone cant be exported. Reviewing code is easy on the webapp interface itself.

## Can I use Avni offline for a whole week?

Yes, Avni can be used fully offline for a week or even longer, since data is stored locally on the device. The only thing to keep in mind is that offline use works reliably as long as another user is not using the app for the same set of individuals or doing data entry for the same records during that period. Once you reconnect to the internet, all pending data will sync back to the server.

## How do I change the app language?

You can change the app language directly from the Avni mobile app. Just open the app, go to More, tap on your username at the top, and then select from the available languages. Once selected, the app will switch to the chosen language immediately.

## How do I search for a subject in the field app?

On the field app home screen, you’ll see a search icon at the top right. Tap on it, select the subject type you want to look for, and then enter the subject details (like name, ID, or other identifiers). After clicking the submit button, the app will display a list of matching records.

## Can I update a subject’s information after registration?

Yes, Avni allows to edit the registration information.

## How do I record a missed visit?

Avni allows to do data entry for the back dates, just select the date on top of the visit while filling the form

## What happens if I accidentally delete a record?

There is no feature to delete a record from the Avni mobile app. So a field user wont be able to do so. Avni allows to void the record which can be reverted by undo void

## How do I know if my data is synced?

You can check sync status from the sync button on the home screen (top right corner). If your data is fully synced, there will be no numbers showing on the sync icon. If numbers are visible, it means there are pending activities waiting to be synced.

## Can I see my past encounters for a subject?

Yes, you can. On the subject profile or the program profile, all completed encounters are displayed, allowing you to review past data entries.

## How do I mark a subject as inactive?

You can simply void the subject

## How do I transfer a subject to another worker?

Webapp >> Assignments >> Search the subject and update the user detail for assignment

## Can I edit a submitted form?

Yes, until unless you have the permission, you can edit the forms easily in Avni

## How do I log out and log back in without losing data?

Logging out wont loose data, once u login back without any other action on the app, the data will sync

## What should I do if the app crashes?

Raise an urgent support ticket with proper details on the Freshdesk link provided by Avni team

## How do I handle duplicate subjects in the app?

In case there are duplicate subjects registered then void one of them.

## Can I use Avni on multiple devices?

Yes, but avoid using Avni app with same login details on different devices

## How do I install Avni updates?

Similar to other apps, on Google play store>> Avni >> Install updates

## What should I check before starting field data collection?

Make sure after login the sync was successfull 100%

## How do I export data from Avni to Excel?

You can download data from Webapp >> Longitudinal export >> It will give you a csv file

## Can I schedule automatic data exports?

No, currently there is no automatic data export. Avni has its won backups running so nothing to worry

## Can I generate PDF reports from Avni?

added to git

## How do I get aggregated data by location?

added to git

## Can I query Avni directly with SQL?

added to git

## How do I filter data exports by date?

added to git

## How do I schedule custom reports?

added to git

## What is the structure of Avni’s database?

added to git

## How do I create a dropdown field with predefined options?

In Avni single select or mutliselect fields can be created from Webapp >> App Designer>> Form >> New form element >> New concept >> Select Coded datatype >> Add predefined options as answers. Then mark the field if can be single select or multi select

## How do I migrate data from another system into Avni?

Avni provides comprehensive bulk data upload functionality through the Admin web console:

- **Supported uploads:**
  - Subjects (individuals/entities)
  - Program enrollments 
  - Program encounters
  - General encounters
  - Locations and catchments
  - Users and their catchments

- **Process:** Download sample CSV templates from the Admin interface, fill with your data, and upload
- **Validation:** Basic level of form validations and rules executions are done during upload - mandatory fields are enforced, hidden fields are ignored based on form element rules
- **Automated processing:** Visit schedules and decisions are automatically created based on your configured logic

## Can I integrate Avni with SMS or WhatsApp alerts?

**Answer:** Avni provides comprehensive communication capabilities through SMS and WhatsApp integrations:

### SMS Integration (MSG91)
- Password reset OTP and user credential sharing
- Phone number verification for beneficiaries
- Multi-language support with secure authentication

### WhatsApp Integration (Glific)
- Trigger WhatsApp messages on events (registration, enrollment, visits)
- Bulk and individual messaging capabilities

**Use cases:** Health camp reminders, ANC visit alerts, motivational content, field worker notifications

**Setup:** Organizations need MSG91 and Glific accounts configured in Avni.

## How do I monitor API usage and limits?

Avni does not support API monitoring. Avni does provide RESTful External APIs which can be leveraged to fetch data from Avni or Push data to Avni, API docs for which are available [here](https://avniproject.github.io/docs/).

## Answer: yes we can configure cascading drop-downs of Locations or Coded Concepts.

### Location Concepts
Yes, for locations, we can do it through Location concepts:

- **Location concept type:** Supports hierarchical location selection
- **Configuration attributes:**
  - **Within Catchment:** Whether locations must be within assigned catchments
  - **Lowest Level(s):** The most granular location types to capture
  - **Highest Level:** The broadest location type to capture

- **Implementation:** Location concepts automatically provide cascading selection based on your configured location hierarchy (state → district → village)
- **Catchment control:** Can restrict selections to locations within field workers' assigned areas or across the entire Location heirarchy of the organisation.


### Coded Concept Hierarchies
Coded concepts can be structured in multiple levels with parent-child relationships:

- **Level 1:** Primary categories (e.g., "Health Services")
- **Level 2:** Sub-categories (e.g., "Maternal Health", "Child Health")  
- **Level 3:** Specific services (e.g., "ANC Visit", "PNC Visit", "Immunization")
We can configure FormElementRules to show / hide Answer Concepts at lower levels based on the selection of higher level concepts.

## How do I copy a question from one form to another?

**Answer:** Questions in Avni are based on **Concepts**, which are reusable across forms:

- **Concept reuse:** Once a concept is created, it can be used in multiple forms
- **Form element creation:** Add the same concept to different forms as form elements
- **Consistency:** Using the same concept ensures data consistency across forms
- **UUID-based:** Concepts use UUIDs internally, so the same concept can have different display names via translations

The documentation emphasizes that concepts should be considered "programming keywords" representing ideas that can be reused across multiple forms.

## Can I hide a field from data collectors but keep it for admins?

**Answer:** No in Avni Forms, we cannot hide a field from data collectors but keep it for admins. What you see in the form is what gets stored. You may additionally create Read-Only Form Elements or Configure Decision Concepts which are auto-generated based on the form data.

## How do I configure default language for a form?

**Answer:** Avni supports user language preferences that determine the language used throughout the Avni Mobile App, including forms, report cards, menu items, and button text. Avni does not have form-specific default language configuration.

### Translation System

- **Translation framework:** Avni supports multiple languages for all user-facing content
- **Language-specific translations:** Create translations for each supported language
- **Default language:** Configure the primary language for your organization
- **Form element translations:** All form elements can have language-specific display text

## Can I restrict date fields to future dates only?

Yes, through FormElement / FormElementGroup Rules, we can implement validation to restrict date fields to future dates only.

## How do I enable GPS capture in registration forms?

There is a User level "Track Location" setting that needs to be enabled for Geographical coordinates to be captured. Switches on location tracking on the Field App during first time create of Subject or Encounter.

## Can I create a calculated field based on two numeric inputs?

Yes, we can auto-calculate values based on other form elements. 
Example: Calculate BMI from height and weight, or compute totals from multiple numeric fields.

## How do I make a field appear only during new subject registration?

We do not recommend this approach, rather based on Business need, recommend setting up a Program or Encounter form that should be used to capture change in subject's status post registration.

## How can I reorder questions in a form?

You can move questions up or down when designing the form in the Avni web app. Just drag and drop them into the order you want.

## Can I create a checkbox list where multiple options are allowed?

Yes. Avni lets you create a question with multi-select options. 
While creating the question, select

Date type = Coded
Type = Multiselect
This will let users tick more than one option for that question.

## Can I make a field read-only after first entry?

Yes. It can be done by writing a rule stating that after the first value is entered and form saved, this question should not be editable again.

## How do I enforce that one field must be filled if another is empty?

This is also possible with rules. You can write a validation rule: if Field A is empty, then Field B must be filled (i.e. generate validation error if both are empty).

## How can I store multiple phone numbers?

You can add this as a question group. While adding the question in the form, add this as a question group and add the queston as Contact Number 1, Contact Number 2 ...

## Can I use QR codes for subject IDs in Avni?

No, not currently

## How do I configure automatic case closure after 6 months?

No. Avni does not support automatic case closure based on time. Once the program reaches the end, the user must manually exit the beneficiary from the program by clicking the Exit button available next to the program enrollment form.

## Can I configure a form to appear only once per program stage?

Yes. It can be done by writing a rule stating that after a certain period or after filling in some other encounter, this form should not appear again.

## How do I make a yes/no field mandatory?

Yes. It can be done by setting Concept type = Coded, Data type = Single Select (Yes/No), and marking it as Required.

## Can I pre-fill information from previous visits?

Yes. It can be done by writing a rule. For more details, kindly refer to avni readme for rule details

## How do I add an image upload field?

In Avni, there are two concepts for handling images: Image and ImageV2, where the main difference is that ImageV2 also captures the location of the image. To configure this, navigate to WebApp → App Designer → Form, create a new form element, and add a new concept with the data type set as either Image or ImageV2. You can then select whether it should be Single Select or Multi Select, and save the element. Additionally, if more specific image dimensions are required, you can define the width and height within the form element settings.

## Can I create dynamic labels based on other field values?

Yes, you can create dynamic labels based on other fields by adding a rule to the field, either manually or by using the Rule Builder. For detailed steps, refer to the Avni documentation on ReadMe
 or reach out to our support team for assistance.

## How do I enable conditional skip logic across sections?

You can implement conditional skip logic either by manually writing a rule or by using the Rule Builder. To do this, go to App Designer, then create a new form or open an existing form. You will find the Rule option next to Details, where you can define the skip logic as needed.

## Can I configure reminders for upcoming encounters?

Currently, there is no feature available for reminders, but users can track upcoming encounters by adding a dashboard card for it to the dashboard.

## How do I configure a repeatable group of fields?

To create a repeatable group of fields, go to WebApp → App Designer → Form, create a new form element, and add a new concept with the data type set to Question Group. This allows you to add multiple fields under it. You will find a checkbox labeled Repeatable — enable it to configure the group as repeatable.

## Can I set a numeric field to allow decimals only?

Go to WebApp → App Designer → Form, create a new form element, and add a new concept with the data type set to Numeric. You will need to manually write a rule to ensure the system only accepts decimal values. To learn how to create this rule, refer to the Avni documentation or reach out to our support team for assistance.

## How do I configure a program where only supervisors can enroll subjects?

Go to Admin → User Groups, create a new group named Supervisor, and add all users who need supervisor access to this group. Then, click on Permissions, select the program, and toggle the Enrollment option to enable it. This ensures that only users in the Supervisor group can enroll program.
Note:
Make sure to disable (untoggle) the enrollment option for all other user groups so that only supervisors have this permission.

## Can I create a read-only dashboard for workers in Avni?

Yes, this can be done by enabling the View Only permission for the respective user groups.

## How do I configure a field that stores household GPS plus notes?

Go to App Designer → Create a new form or open an existing form, then create a new form element and add a new concept with the data type set to Location. This will allow you to capture and record the GPS coordinates.

## Can I configure gender-specific forms in Avni?

Yes we can do my adding the rule in the form

## How do I set default answers for checkboxes?

Webapp>> App Designer >> Form >> Coded concep field >> form element rule of the field >> The rule designer allows to select action of displaying "Value" with some conditions. Generate and save the rule

## How do I configure case assignment based on location?

By default, Avni assigns cases based on location. Each user is linked to a catchment. And each catchment is a set of locations

## How do I model a program for chronic disease management?

1. Create a Subject Type

Go to Webapp → App Designer → Subject Types → Create New.

Give it a name like Person or Individual.

Select Person from the subject type dropdown.

On save, a default registration form is created.

This form already includes first name, last name, age, gender, and location. You can add more fields as needed.

2.Create a Program

Go to Webapp → App Designer → Programs → Create New.

Name it Chronic Disease.

On save, Avni automatically creates an Enrolment Form and an Exit Form.

3 Create Encounters

Go to Webapp → App Designer → Encounters → Create New.

Select your program (Chronic Disease).

Give the encounter a name.

Avni automatically creates and maps the form for this encounter.

Customize Forms

Go to Forms and edit the Registration, Enrolment, Exit, and Encounter forms.

Add fields, rules, and logic as per your requirements.

## Can I design workflows for both subjects and facilities?

Yes. In Avni, you can register subjects and enter data against them. Under subject creation, you also have User as a type of subject. This means you can create a subject type for users or facilities and then do data collection and monitoring for them as well.

## How do I create a workflow for nutrition tracking?

1. Create a Subject Type

Go to Webapp → App Designer → Subject Types → Create New.

Name it Person or Individual.

Select Person from the dropdown.

On save, a default registration form is created with fields like name, age, gender, and location. Add child-specific fields if needed.

2.Create a Program

Go to Webapp → App Designer → Programs → Create New.

If the program name is set to Child, Avni automatically generates growth charts for enrolled children.

On save, the Enrolment Form and Exit Form are created automatically.

3.Create Encounters

Go to Webapp → App Designer → Encounters → Create New.

Select the Nutrition Tracking (or Child) program.

Give the encounter a name (e.g., Monthly Nutrition Check).

A form for this encounter is created and mapped automatically.

4.Customize Forms

Go to Forms and edit the Registration, Enrolment, Exit, and Encounter forms.

If the program is for children, make sure to include Height and Weight concepts in the forms—these are required for growth chart generation.

You can also add other nutrition-related fields (e.g., dietary intake, supplementation) and set rules or logic as needed.

## Can I model relationships like teacher → student → guardian?

Yes. You can create separate subject types for Teacher, Student, and Guardian. Then, by using the subject type concept in the forms, you can link them together. For example, a Teacher can be added in the Student form (or vice versa), and a Guardian can also be linked to the Student.

You can further enhance this by:

Using summary rules to show the linked values (e.g., Teacher or Guardian name) at the top of a profile.

If you click on the Teacher’s name in a Student’s profile, it will take you directly to the Teacher’s profile.

## Can I assign a subject to multiple programs at once?

Yes, a subject can be enrolled in multiple programs at a time

## How do I create a workflow for tracking immunizations?

Create a program named Child. Then add a checklist rule at the form level rules and vaccine details in the checklist JSON. The JSON contains information about vaccines and their schedules. Sample rule code and a sample JSON are available in the Avni README documentation.

## Can I design a program that ends after a specific milestone?

Yes. This can be achieved in multiple ways:

1.Train users to monitor the condition during each follow-up and exit the program when the milestone is reached.

2.Use a decision rule to highlight when a condition is met, and show it as a counselling point to exit the program.

3.Apply a worklist updation rule to prompt exit on the next button. A sample worklist updation rule is available in the Avni README documentation.

## Can I track household-level interventions as well as individuals?

Yes. Avni is designed to support interventions at both the household and individual level. You can also map individuals to households, so data is linked and tracked together.

## How do I configure seasonal visits (e.g., annual surveys)?

Avni supports scheduling visits in advance using the visit schedule rule. By configuring the rule logic, you can set up seasonal or recurring visits—such as annual surveys, quarterly check-ins, or any other periodic follow-up.

## Can I link subjects across different user groups?

Yes. Subject assignment can be done for multiple users, even if th

## How do I model temporary migration of subjects?

Migration of subjects is not supported in the mobile app. However, within a catchment, users can update the subject’s address to reflect their temporary location.

## Can I track dropout cases and reasons?

Yes. Dropouts and their reasons can be captured in program exit forms. You can then track exit cases through the mobile app, custom reports, or using the longitudinal export.

## Can I design workflows that include supervisor approvals?

Yes. Avni provides an out-of-the-box approval mechanism. Permissions for approving or rejecting entities can be given to specific users through user groups. To include an entity in the approval workflow, simply enable the approval setting while creating the entity in the App Designer.

## How do I configure different visit schedules for children and adults?

This can be done by adding an age-based condition in the visit schedule rule designer. That way, children and adults can each have their own visit schedules.

## How can I model data for disaster relief beneficiaries?

You can model disaster relief beneficiaries in Avni by:

1.Creating a Subject Type – e.g., Individual or Household, depending on whether relief is tracked per person or per family.

2.Designing Registration Forms – include fields like name, age, gender, address, disaster-affected status, and relief needs.

3.Creating a Program – e.g., Disaster Relief Support. On save, an enrolment and exit form are created automatically.

4. Adding Encounters – e.g., Relief Distribution, Shelter Support, Medical Check-up.

5. Customizing Forms – capture details such as type of relief provided, date, follow-up needs, or referrals.

6. Using Rules (optional) – to highlight vulnerable groups (children, elderly, disabled) or track milestones like completion of relief support.

## Can I set up workflows that branch based on eligibility?

Yes. Eligibility checks can be added in the visit schedule rule designer. Based on these conditions, workflows can branch—for example, scheduling different visits or follow-ups only if the subject meets certain criteria.

## How do I manage subjects who belong to multiple households?

While this is not a usual situation, Avni does not prevent you from adding the same member to multiple households. Go to a household on the app and add any member that you want

## Can I configure Avni to track both individuals and groups?

Avni considers individuals and groups as subject types. A group subject type is a subject type that allows you to add members. This can be used to model households, classrooms and much more. 

Create two different subject types, one for the individual and another for the group. Register them separately and add members to the group subject type

## Can I create a single program with multiple enrollment points?

Yes, you can create a single program with multiple enrollments. To do this, go to App Designer → Create or edit a program, then look for the "Allow Multiple Enrollments" option. Enable it to allow the system to support multiple enrollments for that program.

## How do I configure workflows for child growth monitoring?

Yes, this is possible, but your administrator needs to set it up first.

Why it's possible:

Avni has built-in features specifically designed for tracking child growth
The system can automatically calculate growth charts and detect malnutrition
It can remind you when children need their next check-up
How you can use it:

Ask your supervisor or IT administrator to set up the "Child Growth Monitoring" program for you
Once set up, you'll see a "Child Program" option in your mobile app
When you register a new child, fill in their weight, height, and age
The app will automatically show you if the child's growth is normal or needs attention
The app will tell you when to schedule the next visit for each child

## Can I model a workflow where visits reduce over time?

Yes, this works automatically once your program is set up.

Why it's possible:

Avni is smart enough to know that older children need fewer check-ups than babies
The system can automatically adjust visit schedules based on the child's age
This helps you focus more time on children who need it most
How it works for you:

When you enroll a baby (0-2 years), the app will schedule monthly visits
For toddlers (2-5 years), it will automatically change to every 3 months
For older children, visits become less frequent (maybe once a year)
You don't need to remember this - the app will show you the correct schedule
Your dashboard will always show you who needs a visit and when

## How do I check if my app has the latest forms?

Yes, you can easily check and update your forms.

Why it's possible:

Avni automatically keeps your forms up to date
The app shows you when new forms are available
You can update forms even when you have poor internet connection
How you can do it:

Open your Avni app
Look for a "Sync" button (usually at the top or in settings)
Tap "Sync" - this will check for new forms and updates
If you see "Last synced: [recent date/time]" then your forms are current
If sync hasn't happened recently, try:
Make sure you have internet connection
Pull down on the main screen to refresh
Go to Settings and tap "Force Sync"
The app will show you if any forms were updated

## Can I work in two different programs at the same time?

Yes, you can switch between different health programs easily.

Why it's possible:

Many health workers handle multiple programs (like child health AND maternal health)
Avni lets you switch between programs without closing the app
Each program has its own forms and people to track
How you can do it:

On your main screen, look for a program selector (might say "Child Health" or "Maternal Care")
Tap on it to see all programs you're assigned to
Select the program you want to work on
The app will show you only the people and forms for that program
To switch programs, just tap the program selector again and choose a different one
Your work in each program is kept separate - no mixing up of data

## How do I find all subjects assigned to me?

Yes, your app shows you exactly who you're responsible for.

Why it's possible:

Avni knows which areas and people you're assigned to work with
The app filters to show only your assigned people
You can search and sort to find people quickly
How you can do it:


To find someone specific:
Use the search box at the top
Type their name or ID number
To filter your list:
Look for filter options (might show "All", "Due for visit", "Overdue")
Select the filter you want
The app organizes people by:
Who needs a visit today
Who is overdue for a visit
Who you've recently visited

## Can I register a new subject without network?

Yes, you can register new people even without internet.

Why it's possible:

Avni works offline - it saves everything on your phone first
When you get internet connection later, it uploads the data automatically
This is very helpful when working in remote areas
How you can do it:

Open your Avni app (works even without internet bars)
Tap "Register" or "Add New Person"
Fill out the registration form completely
Tap "Save" - the information is stored on your phone
You'll see the person added to your list immediately
When you get internet connection:
The app will automatically upload the new registration
You'll see a sync notification
The person's data is now safely stored on the server

## How do I sync partially completed forms?

Yes, your partially filled information is automatically saved.

Why it's possible:

Avni automatically saves what you've filled in as you type
If you leave a form incomplete, your information stays there when you come back
Only completely finished forms get sent to the server
How it works:

Start filling out a form for someone
If you can't complete it right now, just go back or close the form
Your filled information is automatically saved on your phone
Later, go back to that person's profile
Tap on the incomplete form - you'll see all your previous answers are still there
Continue filling from where you left off
Only when you complete the entire form and submit it will it sync to the server
Incomplete forms stay only on your phone until you finish them

## What happens if two users register the same subject?

Yes, the system will catch this and help fix it.

Why it's handled:

Sometimes two health workers might register the same person by mistake
Avni is smart enough to detect when this might happen
The system helps merge duplicate records safely
How it works:

Before registering someone new, always search first:
Use the search box to look for their name
Check if they're already in the system
If you accidentally register someone who already exists:
The system will notice during sync
Your supervisor will get a notification about possible duplicates
Your administrator can then:
Compare the two records
Merge them into one correct record
Keep all the important information from both
Always search before registering to avoid this problem

## How do I mark a subject as deceased?

Yes, you can update someone's status when they pass away.

Why it's possible:

Unfortunately, this sometimes happens in health programs
Avni needs to know so it stops scheduling visits for that person
All their previous health records are kept for reporting
How you can do it:

Find the person in your subject list
Tap on their name to open their profile
Look for "Update Status" or "Mark as Deceased" option
Tap on it and confirm the action
Fill in the date if asked
Save the changes
The person will:
No longer appear in your active visit list
Stop getting scheduled for future visits
Their historical data remains for reports

## Can I view my assigned workload for the week?

Yes, your app shows you exactly what work you need to do each day.

Why it's possible:

Avni creates a personalized schedule for each health worker
It shows you who to visit and when
You can plan your week and track your progress.

You'll see:
People who need visits today (usually highlighted)
People due for visits this week
Overdue visits (often shown in red)
For each day, you can see:
How many people to visit
Their names and locations
What type of visit (check-up, follow-up, etc.)
As you complete visits, they'll be marked as done
Your progress for the week is shown as completed vs. remaining tasks

## How do I reset my password in the field app?

After login >> home dashboard>> More >> Change password

## How do I identify subjects with overdue visits?

By default dashboard displays card to show overdue and due visits both for the subject selected

## How do I update subject address information?

By editing subject registration form

## Can I work offline for multiple programs simultaneously?

Yes, within same login you can do data entry for multiple programs

## How do I capture signatures in the Avni app?

Avni supports upload of signatures as files. However, direct signature using a stylus or finger on the mobile application does not exist

## Can I search for subjects by multiple fields (name + phone)?

Yes. On the App Designer, there are two options - the ability to design the exact fields that you can search subjects by, and also decide which fields should be present in the search result fields. 

To set this up, go to App Designer -> Search Fields. Configure fields that are relevant to each subject typs. Go to Search Result Fields -> Add the fields you would want to see there. 

Remember that search result fields only show registration fields, and not all questions on every form

## How do I report an error from the field app?

If you have a paid account, you can use the ticketing system that you have to raise the issue. If not, join the community Discord channel at https://discord.gg/4pcgcQW8pk. The community is pretty friendly, you should be able to find your answer

## Can I update my app without losing offline data?

App updates from the PlayStore work seamlessly. Remember not to delete or uninstall your app. If you do so, you will lose all unsynced data

## How do I check which data has not yet synced?

On the Avni app, the top right button is the sync button. If there is data that has not yet synced to the server, it will show a badge with the number of items left to sync. If you don't see a badge, the data is in sync with the server. 

The app does not specifically show which items have not yet been synced

## Can I pause form filling and return later?

To achieve this, there is a feature called "Drafts". On your Admin-> Organisation Details, enable Draft Save option. It will automatically save the form, but will not be sent to the server until you finally save the details

## How do I use Avni with multiple languages at once?

There are a few options to achieve this. 

If there are multiple users, and a user needs to work on a specific language, you will first need to set up that language and add translations to it. A user can go to their profile on the "More" menu of the home screen of the app, and choose the language of their choice. 

You can also add your question in multiple languages within the question itself to achieve this if you want both languages to show up at once

## Can I hide sensitive information from field workers?

Since the data comes from field users, it is best not to collect sensitive information if it does not directly help with the programme. If it directly helps, then the field users will need to use them, therefore there is little value in hiding it from them. 


If you consider one form in your application to be sensitive, and want to prevent a cadre of workers from accessing it, you can achieve this using User Groups and Permissions. These options are available in the Admin section

## How do I ensure GPS accuracy during data collection?

On Android:
Settings → Location → Mode → High accuracy (uses GPS + WiFi + mobile networks).

Ask users to wait a few seconds outdoors before capturing, so the GPS can “lock on” to satellites.

Ensure permissions for location services are granted to the Avni app.

Cheaper phones may only give ±20–50m accuracy. Higher-end phones can get within 3–5m. If precision is critical (e.g., mapping households), budget for better devices.

## Can I undo the last change in a filled form?

You can go to the form and edit it back to what you want. A direct "Undo" option does not exist on Avni

## When I sign in to Avni, it says catchment not set up. What are catchments, and how do I set them up?

Avni works on the basis of catchments, where a user needs to be assigned a group of locations (called catchment). This ringfences the data on their phones to just the area they work in, reducing data usage and storage, preventing accidental changes, improving performance. 

In order to work on the Avni field app, you first need to set up 
1. Locations
2. Catchments

Once you set up a catchment, you should assign the catchment to the user through the Users section on the Admin screens

## Is my data stored encrypted on the phone?

Avni has been designed for people with relatively low mobile phone literacy and areas with patchy internet availability. The security measures have been designed to ensure they are able to use the app. As a result, the app does not ask for a login if you have not explicitly logged out. 

Security features of the mobile phone is expected to keep the data private with the owner of the phone

If you prefer, or if you are at a place where your phone might be used by others, we recommend you logout of the app before handing over the phone to others.

## I signed out from Avni and am now at the field. The app is taking me to the sign-in screen. What can I do?

Unfortunately, signing in requires internet connection and cannot be performed offline

## Can I set up two factor authentication on Avni?

At this point, 2 factor authentication is unavailable on Avni

## Can I do push notifications on Avni?

Avni is designed to work in offline settings where the app is a primary work app. Any information to the user can be conveyed by directly showing it on the app. 

The Broadcasts feature helps with any broadcasts, and Whatsapp broadcasts can be used to send Whatsapp messages to a user if required.

## How secure is the data on the cloud?

Data going to the cloud is encrypted. In the cloud databases, data is stored encrypted

## Who are Avni's competitors?

Avni is open source tool that provides similar to commcare, ODK

## How is Avni better than the competitors products /services?

Avni stands out for advanced case management features, customizable decision support algorithms, multi-language support, offline capabilities, full control over data, and a high level of security/privacy. It is fully open-source, making it more flexible and cost-effective compared to many proprietary competitors like CommCare.

## What is the difference between self service, assisted self service and Samanvay managed ?

Self Service: User independently configures and customizes the platform.

Assisted Self Service: Avni provides guidance and support, but the application is primarily built by the user.

Samanvay Managed Service: End-to-end solution where Avni sets up, customizes, and manages the platform for the organization.

## Can I add multiple languages to the app?

Yes , multiple languages can be added to the app and as per need toggle  between different languages

## Will I get data collected on real-time basis to visuale and analyse

Data will available near to real time basis as offine data needs to be synced by users. Auto sync is available that happens every 1 hour but it depends on moinle phone sand app setting

## Is Avni free of cost? if not what are charges

No, it is an open source with 3 different options . More details https://avniproject.org/pricing

## Related Topics

<!-- Add links to related documentation -->


---
<!-- Source: 10-reference/version-compatibility.md -->

# Version Compatibility Guide

## TL;DR

<!-- TODO: Add 2-3 sentence summary of Version Compatibility Guide -->

## Overview

**What:** <!-- TODO: One-sentence description -->

**When to use:** <!-- TODO: Scenarios -->

**Prerequisites:** <!-- TODO: What to know first -->

## Feature Availability

<!-- TODO: Add content for feature-availability -->

## Related Topics

<!-- TODO: Add links to related documentation -->