---
title: "Organization Creation in Avni"
category: "organization-setup"
audience: "implementer"
difficulty: "beginner"
priority: "critical"
keywords:
  - organization creation
  - setup
  - admin
  - new org
last_updated: "2026-03-16"
task_types:
  - configuration
  - tutorial
technical_level:
  - procedural
implementation_phase:
  - setup
complexity: "simple"
retrieval_boost: 2.0
related_topics:
  - address-hierarchy.md
  - user-management.md
estimated_reading_time: "10 minutes"
version: "1.0"
---

# Organization Creation

<!-- CHUNK: tldr -->
## TL;DR

Organization creation is typically done by Avni team. You'll receive admin credentials to configure your organization. Setup involves creating admin users, uploading configuration bundles, and setting up address hierarchy. Time: ~2 hours for basic setup.

<!-- END CHUNK -->

<!-- CHUNK: overview -->
## Overview

**What:** Creating a new Avni organization (tenant) on the platform.

**Who does it:** Usually Avni team (requires super admin access).

**What you do:** Configure the organization after creation (users, locations, forms).

**Prerequisites:**
- Organization name and details
- Configuration bundle (forms, programs)
- Admin user details

<!-- END CHUNK -->

<!-- CHUNK: creation-steps -->
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

<!-- END CHUNK -->

<!-- CHUNK: post-creation -->
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

<!-- END CHUNK -->

<!-- CHUNK: common-issues -->
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

<!-- END CHUNK -->

<!-- CHUNK: checklist -->
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

<!-- END CHUNK -->

---

**Navigation:**  
[← Back to Organization Setup](README.md) | [Next: Address Hierarchy →](address-hierarchy.md)
