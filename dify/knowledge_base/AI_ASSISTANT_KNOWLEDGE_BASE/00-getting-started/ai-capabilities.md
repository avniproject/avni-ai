---
title: "Avni AI Assistant Capabilities"
category: "getting-started"
audience: "implementer"
difficulty: "beginner"
priority: "critical"
keywords:
  - ai assistant
  - capabilities
  - what can ai do
  - ai limitations
  - help
last_updated: "2026-03-16"
task_types:
  - reference
features:
  - forms
  - rules
  - subjects
  - programs
  - encounters
  - locations
technical_level:
  - conceptual
implementation_phase:
  - planning
  - setup
  - development
complexity: "simple"
retrieval_boost: 2.0
version: "1.0"
---

# Avni AI Assistant Capabilities

<!-- CHUNK: capabilities-overview -->
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

<!-- END CHUNK -->

<!-- CHUNK: capabilities-limitations -->
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

<!-- END CHUNK -->

<!-- CHUNK: how-to-use -->
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

<!-- END CHUNK -->

<!-- CHUNK: example-queries -->
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

<!-- END CHUNK -->
