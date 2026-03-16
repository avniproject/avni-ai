---
title: "Offline Sync Basics - How Avni Works Offline"
category: "core-concepts"
audience: "implementer"
difficulty: "beginner"
priority: "high"
keywords:
  - offline
  - sync
  - synchronization
  - mobile app
  - connectivity
  - catchment
last_updated: "2026-03-16"
task_types:
  - reference
features:
  - all
technical_level:
  - conceptual
implementation_phase:
  - planning
  - deployment
complexity: "simple"
retrieval_boost: 1.5
related_topics:
  - ../02-organization-setup/catchment-configuration.md
  - ../02-organization-setup/user-management.md
estimated_reading_time: "6 minutes"
version: "1.0"
---

# Offline Sync Basics

<!-- CHUNK: tldr -->
## TL;DR

Avni's mobile app works completely offline, storing data locally. When internet is available, it syncs changes bidirectionally - uploading new data and downloading updates. Sync is catchment-based, so users only get data for their assigned locations.

<!-- END CHUNK -->

<!-- CHUNK: overview -->
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

<!-- END CHUNK -->

<!-- CHUNK: how-offline-works -->
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

<!-- END CHUNK -->

<!-- CHUNK: sync-process -->
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

<!-- END CHUNK -->

<!-- CHUNK: catchment-based-sync -->
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

<!-- END CHUNK -->

<!-- CHUNK: sync-scenarios -->
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

<!-- END CHUNK -->

<!-- CHUNK: conflict-resolution -->
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

<!-- END CHUNK -->

<!-- CHUNK: troubleshooting-sync -->
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

<!-- END CHUNK -->

<!-- CHUNK: best-practices -->
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

<!-- END CHUNK -->

---

**Navigation:**  
[← Back: Data Model](data-model.md) | [Next: Organization Setup →](../02-organization-setup/README.md)
