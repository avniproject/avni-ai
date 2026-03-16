---
title: Migrating Subjects Between Locations
category: data-management
audience: implementer
difficulty: intermediate
priority: medium
keywords:
- subject migration
- move subject
- location change
- migrate location
last_updated: '2026-03-16'
task_types:
- tutorial
features:
- subjects
- locations
technical_level:
- procedural
implementation_phase:
- maintenance
complexity: moderate
retrieval_boost: 1.0
related_topics:
- ../02-organization-setup/address-hierarchy.md
estimated_reading_time: 1 minutes
version: '1.0'
---
# Migrating Subjects Between Locations

<!-- CHUNK: tldr -->
## TL;DR

[https://editor.swagger.io/?url=https://raw.githubusercontent.com/avniproject/avni-server/master/avni-server-api/src/main/resources/api/external-api.yaml](https://editor.swagger.io/?url=https://raw.githubusercontent.com/avniproject/avni-server/master/avni-server-api/src/main/resources/api/externa...
<!-- END CHUNK -->

<!-- CHUNK: please-refer-to-api-doc -->
## Please refer to API Doc

[https://editor.swagger.io/?url=https://raw.githubusercontent.com/avniproject/avni-server/master/avni-server-api/src/main/resources/api/external-api.yaml](https://editor.swagger.io/?url=https://raw.githubusercontent.com/avniproject/avni-server/master/avni-server-api/src/main/resources/api/external-api.yaml)
<!-- END CHUNK -->

<!-- CHUNK: documentation-deprecated -->
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
<!-- END CHUNK -->

<!-- CHUNK: related-topics -->
## Related Topics

<!-- Add links to related documentation -->
<!-- END CHUNK -->