---
title: Address Hierarchy Setup in Avni
category: organization-setup
audience: implementer
difficulty: intermediate
priority: high
keywords:
- address hierarchy
- location types
- locations
- hierarchy setup
last_updated: '2026-03-16'
task_types:
- configuration
- tutorial
features:
- locations
technical_level:
- procedural
implementation_phase:
- setup
complexity: moderate
retrieval_boost: 1.5
related_topics:
- location-setup-csv.md
- catchment-configuration.md
estimated_reading_time: 1 minutes
version: '1.0'
---
# Address Hierarchy Setup in Avni

<!-- CHUNK: tldr -->
## TL;DR

Below is a list of definitions that are essential for understanding this document.
<!-- END CHUNK -->

<!-- CHUNK: definitions -->
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
<!-- END CHUNK -->

<!-- CHUNK: related-topics -->
## Related Topics

<!-- Add links to related documentation -->
<!-- END CHUNK -->