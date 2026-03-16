---
title: Setting Up Locations via CSV Upload
category: organization-setup
audience: implementer
difficulty: intermediate
priority: high
keywords:
- locations
- CSV upload
- bulk upload
- location types
- lineage
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
- address-hierarchy.md
- catchment-configuration.md
estimated_reading_time: 10 minutes
version: '1.0'
---
# Setting Up Locations via CSV Upload

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

<!-- CHUNK: overview -->
## Overview

In Avni, Locations refer to geographical entities which could be a State, Village, Schools, Hospital, etc.. where an organisation provides services. It plays an important role in identifying the “Where” aspect of the data being captured / service that was provided. Locations are also used to group together Avni entities (Subjects, Encounters, GroupSubjects) based on their Geographical proximity, using the Catchments. This simplifies the assignment of Avni entities in the Geographical area of influence of a Field-Worker to him/her as a single composite entity rather than individually allocating each entity to the User.

Avni **“Upload\- Locations”** functionality, allows Avni Admin Users to perform following actions in **bulk**

* Create new locations   
* Update name, GPS coordinates and other properties for existing locations  
* Modify the parent location for an existing location and there-after reflect the change in lineage for it and all its children

This is achieved by means of uploading a CSV(Comma-separated Values) file of a specific format. Please read through the rest of the document to learn more about initializing Location Types and setting up large amounts of Locations for each of those types for specific Location Type Hierarchy.
<!-- END CHUNK -->

<!-- CHUNK: steps-to-create-location-types-hierarchy -->
## Steps to create Location Types Hierarchy

### Navigation to the Bulk Uploads screen

* Login to Avni Web Console 

![](https://files.readme.io/35932d9141d5744753f1730b6b5a4aa04a4b755a9fd18c25586ca98b58639177-image.png)

* Go to **Admin** app

![](https://files.readme.io/b51402bda3d8cf3a6aefd515b8e19cecc2c0200c5c557ae973cb38d3fa4e172e-image.png)

* Click on the **“Location Types”** section

![](https://files.readme.io/b846e3e44e146727fc20ad58b6c881cb8d2a96ac3dcdac90ae90f84b1fc81d2f-image.png)

### Create Location Types Hierarchy

When we start with creation of Location types, we do so from the highest Location type to the lowest in descending order of its level within the Location Hierarchy.

For example, to set up a Location Hierarchy of State(3) \-\> District(2) \-\> City(1), you would repeat the below process 3 times, first for “State”, then “District” and finally for “City”.

#### Create Location Type

1. Click on “CREATE” button on the top right corner, in “Location Types” screen  
2. Initialize “Name” field, to an appropriate String value starting with Upper-case Alphabet  
3. Initialize the “Level” field to appropriate Numeric value, which would be lower than its “Parent” Location Type’s “Level” value. Ex: “2.0”, “3”, “4.5”  
4. Associate “Parent” Location Type, as long as this isn’t the Highest Location type in its hierarchy  
5. Save the Location type, by clicking on the “SAVE” button

![](https://files.readme.io/2c1cb4ff350002b55cb86e570dc8f22baf8f5c5a1738bf1575def95eb6a7e1a3-image.png)

#### About Multiple Location Type Hierarchies within a single organization

Avni allows for an organization to have more than one Location hierarchy. The hierarchies could be linked at a specific location type or otherwise.

##### Example for Multiple Hierarchy joined at a common location type

![](https://files.readme.io/785775716ea75efb92621f34ebf17f014cb5f1b5a478a2c4e7d1ffff90e26b2a-image.png)

##### Example for Multiple Hierarchies not linked with each other

![](https://files.readme.io/4c530ae55ff631715c497aef020ef6591e2189c5df01b3bc034a34797acc6bc4-image.png)

### Review Location Types Hierarchy

Do a quick review of the Location Types Hierarchy, to ensure that its created as per requirement.

![](https://files.readme.io/6fccd280624ae8da4252f2bf7b3bb2bdb4950fabd5f7132f2820cc4849d6b628-image.png)
<!-- END CHUNK -->

<!-- CHUNK: steps-to-create-form-of-type-locations-optional -->
## Steps to create Form of type Locations (Optional)

For your organization, if there is a need to specify additional details as part of each Location, then Avni allows you to configure a “Location” type Form, which can be configured to store those additional details as Observations for each Location. This is an optional feature to be done only if such need arises.

* Navigate to the App Designer app

  ![](https://files.readme.io/45b6cf059a148183cb5597b2e09a93dc6d705c9af4eb09f99df0c9cdbd246050-image.png)
* Click on Forms in the left side tab, to open up the Forms section.  
* Create a new Form of type “Locations” by clicking on the “CREATE” button on the Top-Right corner of the screen.  

  ![](https://files.readme.io/2ad5b18293dfb28f217f3a87bd633dccb766d962a56c68f2c3fdb4b1611e6237-image.png)
* Setup the Locations type Form in the same way as you do for any other Avni Entity Data collection Forms. See below sample screenshot for reference.

  ![](https://files.readme.io/b5c2e8c75e8660ff5eaa3fba63826e1b2898aab32cf942beeec47d8cba11dd19-image.png)
<!-- END CHUNK -->

<!-- CHUNK: csv-format -->
## Steps to create Locations via CSV upload

### Prerequisites

* **Ensure Location Types Hierarchy already exists**\
  In order to start with the locations upload in the Avni app, organisation needs to have Location Types created in the requisite hierarchical order.  
* **Ensure Location Form if needed, has already been configured**\
  If your organisation needs additional properties to be set during Location creation, then ensure that you have configured a form of type “Locations” in the aforementioned manner 

### Navigation to the Bulk Uploads screen

* Login to Avni Web Console

![](https://files.readme.io/93db597e0607f374895d82942c940eca42ff9954f008e28fb2933b459a2bc280-image.png)

* Go to **Admin** app

![](https://files.readme.io/a0bfd4fcaa19d3275985307bdc624b89237c508ee94eb2a9f6a992c0f3d30348-image.png)

* Click on the **“Upload”** section

![](https://files.readme.io/81b9a7ec02dcba7ee588ceb2c4a6a508e9346610ef43e9b29c2c30ba0fb6b8fa-image.png)

### Download sample CSV file

In the Avni “Admin” app, “Upload” section, we provide the users with an option to download a sample file, which would give you a rough example for coming up with the required “Locations” upload CSV file.

The locations upload file format is different for the “Create” and “Edit” modes, therefore choose the appropriate mode and apply the same, when uploading the file later as well.

If your organization has multiple Location hierarchies, then you would have to select the specific location hierarchy for which you need the sample file. This is applicable only for “Create” mode.\
Finally, click on the “Download Sample” button, to get the sample file.

![](https://files.readme.io/31cbacad108b87cdd4a90ad196fbd4b879761676b333fe0cdfbd7baa6814f30c-image.png)

#### Sample Locations upload csv file screenshot

As part of the sample Locations csv file downloaded, you’ll have following information available to you for quick reference:

* All Headers configurable for the selected Mode and Location hierarchy  
* Descriptor row with guidance and examples on what values should be specified for each of the columns

1. **Create** mode

   ![](https://files.readme.io/00dc42970a69fea2eac1a114935cb3b2cbefe588aa540a5147cd51e7bdc930bc-image.png)
2. **Edit** mode

   ![](https://files.readme.io/42250968ba2ed5feec3e8da58e4c0521e1aa8bbe1418530de90a3f61a4eaf71f-image.png)

### Compose Locations upload CSV file

1. ### "Create" Mode

#### Headers Row

The first row of your upload file should contain Location types, arranged in descending order of their Level, in the selected Location Hierarchy from Left to Right, as comma-separated values.\
Refer Sample Locations Upload documents available [here](https://docs.google.com/spreadsheets/d/1R3l_tRUKZ7_WoZa4QIRctecFqJZoB2jdltyKUPMSD0Q/edit?usp=sharing) for Location Hierarchy of: Block(3) \-\> GP(2) \-\> Village/Hamlet(1). This is followed by “GPS Coordinates” and other Location properties name as column names.

![](https://files.readme.io/1a1dff92a0cb11f31704ee8f6d87ac78013ae49e56e8b878dc8657bb96762ece-image.png)

#### Descriptor Row

The second row of your upload file can optionally be a descriptor row, retained as is from the sample location upload file downloaded earlier. Avni would ignore the row, if its starting text matches the Sample file Descriptor row content’s starting text.

#### Data Rows

Entries provided in each of the address-level-type columns would be created as individual locations. (For example, the “Jawhar” block, “Sarsun” GP, and “Dehere” village will be created as a unique location with the appropriate location lineage, as specified during upload.)\
If the Parent locations already exists during a new location creation, then they are not re-created and are just used as is to build the location lineage.

#### GPS Coordinates

In-case, user would like to set the GPS Coordinates for locations during upload, then they would need to additionally specify values in the "GPS coordinates" column. The value for this column should be of the Format “\<Decimal number\>,\<Decimal number\>”.\
Ex: “123.456789,234.567890”, “12.34,45.67”, “13,77”

#### Additional Location Properties

Avni allows an organisation to configure Forms of Type “FormType.Location” for enabling inclusion of additional properties for each Location. These Forms are made up of the same building blocks of Pages and Questions like Forms of other types.

In-order to configure Location properties, you would need to specify the Concept “name” as the Column Header and specify the value for each of the locations in the corresponding columnar position.

![](https://files.readme.io/d779bbd3674a887c54b1f320d9e7cceb881b841f3360697f9d450c0bbf2795d1-image.png)

2. ### “Edit” Mode

This mode is to be used to perform bulk updates to locations. The type of updates allowed are as follows:

* Update name of existing locations  
* Update GPS coordinates and other properties for existing locations  
* Modify the parent location for an existing location and there-after reflect the change in lineage for it and all its children

#### Headers Row

The first row of your upload file, would usually contain following data as columns headers:

1. Location with full hierarchy  
2. New location name  
3. Parent location with full hierarchy  
4. GPS coordinates  
5. Multiple Location Properties name  

Refer Sample Locations Upload documents available [here](https://docs.google.com/spreadsheets/d/1EFpeMuQe-BEGvghUAeQWsLumfJ88B2Iv8w-lVqzQX4c/edit?usp=sharing).

![](https://files.readme.io/9d903fe0c5fe2d9d8fc93622312ef7e23efbc3fd6c2d811ade340d362c37db39-image.png)

#### Data Rows

Entries provided for the columns listed below would be used as specified here:

* Location with full hierarchy (Mandatory): Used to identify the specific location to be modified  
* New location name (Optional):  Used to specify the new title value for a location  
* Parent location with full hierarchy (Optional):  Used to identify the new parent location to move this location to. Ex: Move “Vil B” to “PHC C, Sub C” from “PHC B, Sub B”  
* GPS coordinates (Optional):  Used to update the GPS coordinates. Format:  “\<Double\>,\<Double\>”. Ex: “123.456789,234.567890”  
* Values for multiple Location Properties columns that are part of the Form of type “FormType.Location”. These again are optional.

#### Edit Row validations

1. If the “Location with full hierarchy” does not exist during location updation, then the update operation fails for that row.  
2. Atleast one among the following columns should have a valid value for the updation operation to be performed successfully for that row:  
   * New location name  
   * Parent location with full hierarchy  
   * GPS coordinates  

### Upload the CSV file

Project team then downloads the sheet in the CSV format. Navigate to the “**Upload”** tab of the Admin section, and perform the following steps to upload the file:

* Select the “Type” to be “Locations”   
* Specify the file to be uploaded using the “CHOOSE FILE” option  
* Select the appropriate “Mod&#x65;**”** of CSV Upload  
  * Create: For creating new locations  
  * Edit: For updating existing location’s Name, Parent, GPS coordinates or other properties  
* Choose appropriate “Location Hierarchy” (Applicable only for “Create” mode)  
* Click on the “Upload” button

![](https://files.readme.io/225211b913de07fb56c6a7676b1b6c88a78aecc2c92f97833c646b304b8ce6c4-image.png)
<!-- END CHUNK -->

<!-- CHUNK: monitoring-progress-of-the-upload -->
## Monitoring Progress of the Upload

Avni provides users with an easy way to monitor the progress of the CSV file uploads. In the same “Upload” tab of the Admin section, the bottom-half contains a list of all uploads triggered by users of the organization.

![](https://files.readme.io/ac1a32f7738e8035e5ad076005a218693044cfc7f00348d080bdd3a3e50d2d22-image.png)The “Status” column will indicate the overall status of the specific upload activity. With other columns like “Rows/File read” , “Rows/File completed” and “Rows/File skipped” indicating the Granular row-level progress of the file processing.

The final “Failure” column, will consist of Hyperlinks to Download an Error Information file, which would be present, only upon Erroneous completion of the upload activity.

![](https://files.readme.io/f38defc143785372fa7b8963c14e555d89eaa5feebe009aa7d55a20a40445bbf-image.png)
<!-- END CHUNK -->

<!-- CHUNK: verification-of-uploaded-content -->
## Verification of Uploaded content

On successful upload of a file, the Project team can verify from the Locations tab in the “Admin” application, whether the uploaded content was indeed processed successfully as per requirement. Search for the newly created Locations and click on the same to view its details, to confirm that its created with exact configuration as intended.

![](https://files.readme.io/8457449146f1308efc4d6a9e690368dd3818a1ac9d78f329004771e7422d4fb7-image.png)
<!-- END CHUNK -->

<!-- CHUNK: related-topics -->
## Related Topics

<!-- Add links to related documentation -->
<!-- END CHUNK -->