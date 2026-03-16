---
title: Custom Fields in Search Results
category: mobile-app-features
audience: implementer
difficulty: intermediate
priority: medium
keywords:
- custom search
- search results
- search fields
- custom fields
last_updated: '2026-03-16'
task_types:
- configuration
features:
- subjects
technical_level:
- procedural
implementation_phase:
- development
complexity: simple
retrieval_boost: 1.0
related_topics:
- dashboard-filters.md
estimated_reading_time: 1 minutes
version: '1.0'
---
# Custom Fields in Search Results

<!-- CHUNK: tldr -->
## TL;DR

Avni app has the capability to setup [custom search filters](https://avni.readme.io/docs/my-dashboard-and-search-filters), but the results do not show any of these fields. Using this feature one can add additional fields to the search result.
<!-- END CHUNK -->

<!-- CHUNK: overview -->
## Overview

Avni app has the capability to setup [custom search filters](https://avni.readme.io/docs/my-dashboard-and-search-filters), but the results do not show any of these fields. Using this feature one can add additional fields to the search result.
<!-- END CHUNK -->

<!-- CHUNK: setting-up-custom-fields-in-search-results -->
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
<!-- END CHUNK -->

<!-- CHUNK: related-topics -->
## Related Topics

<!-- Add links to related documentation -->
<!-- END CHUNK -->