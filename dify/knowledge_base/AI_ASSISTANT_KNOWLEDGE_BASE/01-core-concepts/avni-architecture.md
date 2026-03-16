---
title: "Avni Architecture Overview"
category: "core-concepts"
audience: "implementer"
difficulty: "beginner"
priority: "high"
keywords:
  - architecture
  - components
  - field app
  - server
  - multitenancy
last_updated: "2026-03-16"
task_types:
  - reference
features:
  - all
technical_level:
  - conceptual
implementation_phase:
  - planning
complexity: "simple"
retrieval_boost: 1.5
related_topics:
  - domain-model.md
  - offline-sync-basics.md
estimated_reading_time: "8 minutes"
version: "1.0"
---

# Avni Architecture Overview

<!-- CHUNK: tldr -->
## TL;DR

Avni is a multi-tenant platform with mobile field apps that work offline, a web-based admin interface for configuration, and a central server for data storage and synchronization. The architecture supports multiple organizations on shared infrastructure while maintaining complete data isolation.

<!-- END CHUNK -->

<!-- CHUNK: overview -->
## Overview

**What:** Understanding Avni's component architecture and how they interact.

**When to use:** Planning your implementation, understanding system capabilities, troubleshooting issues.

**Key components:**
- Field App (Android) - Offline data collection
- Admin Web App - Configuration and management
- Avni Server - Central data storage
- Rules Server - JavaScript rule execution
- ETL Server - Reporting data preparation

<!-- END CHUNK -->

<!-- CHUNK: components -->
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

<!-- END CHUNK -->

<!-- CHUNK: multitenancy -->
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

<!-- END CHUNK -->

<!-- CHUNK: data-flow -->
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

<!-- END CHUNK -->

<!-- CHUNK: deployment -->
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

<!-- END CHUNK -->

<!-- CHUNK: related-concepts -->
## Related Concepts

**For deeper understanding:**
- [Domain Model](domain-model.md) - How entities relate
- [Offline Sync](offline-sync-basics.md) - How sync works
- [Data Model](data-model.md) - How data is structured

**For implementation:**
- [Organization Setup](../02-organization-setup/README.md) - Setting up your org
- [User Management](../02-organization-setup/user-management.md) - Managing users

<!-- END CHUNK -->

---

**Navigation:**  
[← Back to Core Concepts](README.md) | [Next: Domain Model →](domain-model.md)
