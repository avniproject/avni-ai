---
title: Mobile App Configuration Settings
category: mobile-app-features
audience: implementer
difficulty: intermediate
priority: medium
keywords:
- app configuration
- mobile settings
- app menu
- application menu
last_updated: '2026-03-16'
task_types:
- configuration
- reference
features:
- dashboards
technical_level:
- procedural
implementation_phase:
- development
complexity: moderate
retrieval_boost: 1.0
related_topics:
- offline-dashboards.md
estimated_reading_time: 1 minutes
version: '1.0'
---
# Mobile App Configuration Settings

<!-- CHUNK: tldr -->
## TL;DR

The customizable "Application menu" feature helps you add a new menu item that will show up on the "More" option of the Android app.
<!-- END CHUNK -->

<!-- CHUNK: overview -->
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
<!-- END CHUNK -->

<!-- CHUNK: related-topics -->
## Related Topics

<!-- Add links to related documentation -->
<!-- END CHUNK -->