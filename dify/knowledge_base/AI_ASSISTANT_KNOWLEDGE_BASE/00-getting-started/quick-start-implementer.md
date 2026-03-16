---
title: "Quick Start Guide for Avni Implementers"
category: "getting-started"
audience: "implementer"
difficulty: "beginner"
priority: "critical"
keywords:
  - quick start
  - getting started
  - implementer guide
  - first steps
  - setup guide
last_updated: "2026-03-16"
task_types:
  - tutorial
  - configuration
features:
  - forms
  - subjects
  - programs
  - concepts
technical_level:
  - procedural
implementation_phase:
  - planning
  - setup
complexity: "simple"
query_patterns:
  - "how to get started with avni"
  - "first steps for implementer"
  - "avni setup guide"
  - "begin avni implementation"
answer_types:
  - how-to
  - tutorial
retrieval_boost: 2.0
related_topics:
  - About the AI Assistant.md
estimated_reading_time: "15 minutes"
version: "1.0"
---

# Quick Start Guide for Avni Implementers

<!-- CHUNK: tldr -->
## TL;DR

This guide walks you through the essential steps to start implementing on Avni. You'll learn to create organizations, define subject types, build forms, and write basic rules. Estimated time: 2-3 hours for a basic setup.

**Core workflow:** Organization → Locations → Subject Types → Forms → Programs → Rules

<!-- END CHUNK -->

<!-- CHUNK: overview -->
## Overview

**What:** A step-by-step guide to get your first Avni implementation running.

**When to use:** You're starting a new Avni implementation and need to understand the basic setup flow.

**Prerequisites:** 
- Access to Avni admin portal
- Understanding of your program requirements (who you're tracking, what data you need)
- Basic familiarity with forms and data collection

**What you'll build:** A simple maternal health tracking system with beneficiary registration and ANC visit forms.

<!-- END CHUNK -->

<!-- CHUNK: step1-organization -->
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

<!-- END CHUNK -->

<!-- CHUNK: step2-locations -->
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

<!-- END CHUNK -->

<!-- CHUNK: step3-concepts -->
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

<!-- END CHUNK -->

<!-- CHUNK: step4-subject-type -->
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

<!-- END CHUNK -->

<!-- CHUNK: step5-registration-form -->
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

<!-- END CHUNK -->

<!-- CHUNK: step6-program -->
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

<!-- END CHUNK -->

<!-- CHUNK: step7-encounter-type -->
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

<!-- END CHUNK -->

<!-- CHUNK: step8-basic-rule -->
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

<!-- END CHUNK -->

<!-- CHUNK: step9-test -->
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

<!-- END CHUNK -->

<!-- CHUNK: next-steps -->
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

<!-- END CHUNK -->

<!-- CHUNK: faq-quick-start -->
## FAQ

**Q: How long does initial setup take?**

A: Basic setup (organization, locations, one subject type, one form): 2-3 hours. Full implementation with rules and testing: 1-2 weeks.

**Q: Can I change things after going live?**

A: Yes! You can add fields, modify forms, update rules. Users need to sync to get changes.

**Q: What if I make a mistake?**

A: Most configuration can be edited. Data can be voided (soft delete). Test thoroughly before going live.

**Q: Do I need to know programming?**

A: Basic setup: No. Advanced rules: Yes, JavaScript knowledge helps.

<!-- END CHUNK -->

<!-- CHUNK: common-issues-quick-start -->
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

<!-- END CHUNK -->

<!-- CHUNK: resources -->
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

<!-- END CHUNK -->
