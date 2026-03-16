---
title: "Avni AI Assistant Knowledge Base - Implementer Guide"
category: "navigation"
audience: "implementer"
difficulty: "beginner"
priority: "critical"
keywords:
  - knowledge base
  - navigation
  - table of contents
  - index
  - implementer guide
last_updated: "2026-03-16"
task_types:
  - reference
technical_level:
  - conceptual
implementation_phase:
  - planning
  - setup
  - development
  - testing
  - deployment
  - maintenance
complexity: "simple"
retrieval_boost: 2.0
version: "2.0"
---

# Avni AI Assistant Knowledge Base

**For Implementers** | Version 2.0 | Last Updated: March 16, 2026

<!-- CHUNK: welcome -->
## Welcome

This knowledge base helps Avni implementers configure and troubleshoot Avni implementations. It covers JavaScript rules, form configuration, concept management, organization setup, and implementation patterns.

**What's new in v2.0:**
- ✅ Reorganized into 10 focused categories
- ✅ 68 topic-specific files (vs 5 monolithic files)
- ✅ Implementer-focused content (96% relevant)
- ✅ LLM-optimized with metadata and semantic chunks
- ✅ Troubleshooting guides from 90,000+ support tickets
- ✅ Clear navigation and cross-references

<!-- END CHUNK -->

<!-- CHUNK: quick-navigation -->
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

<!-- END CHUNK -->

<!-- CHUNK: knowledge-base-structure -->
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

<!-- END CHUNK -->

<!-- CHUNK: how-to-use -->
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

<!-- END CHUNK -->

<!-- CHUNK: ai-assistant-tips -->
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

<!-- END CHUNK -->

<!-- CHUNK: whats-changed -->
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

<!-- END CHUNK -->

<!-- CHUNK: migration-guide -->
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

<!-- END CHUNK -->

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
