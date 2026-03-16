---
title: Bulk Data Upload (v2)
category: data-management
audience: implementer
difficulty: intermediate
priority: high
keywords:
- bulk upload
- data upload
- CSV upload
- data migration
- bulk import
last_updated: '2026-03-16'
task_types:
- tutorial
- configuration
features:
- subjects
- encounters
- programs
technical_level:
- procedural
implementation_phase:
- deployment
- maintenance
complexity: moderate
retrieval_boost: 1.5
related_topics:
- data-import-validation.md
estimated_reading_time: 6 minutes
version: '1.0'
---
# Bulk Data Upload (v2)

<!-- CHUNK: tldr -->
## TL;DR

* Prepare data in bulk, review, and upload. * Migrating away from an existing implementation, and need to seed with existing data.
<!-- END CHUNK -->

<!-- CHUNK: purpose -->
## Purpose

* Prepare data in bulk, review, and upload.
* Migrating away from an existing implementation, and need to seed with existing data.
* Your organization has a separate component where data is collected outside Avni, but you still need this data to be present with field workers using Avni.
<!-- END CHUNK -->

<!-- CHUNK: upload-types -->
## Using the Admin app to upload data

The Admin app of the web console has an upload option. Currently, this supports the following. Essentially for each form present in you organisation there is a corresponding upload option in the dropdown, with a sample file.

* Upload subjects
* Upload program enrolment (excluding exit information and observations)
* Upload program encounters (excluding cancel information and observations)
* Upload encounters (excluding cancel information and observations)
* [Upload locations](location-and-catchment-in-avni)
* Upload users and catchments
* Upload metadata zip file downloaded from a different implementation
<!-- END CHUNK -->

<!-- CHUNK: sample-file -->
## Sample file

Sample files are available in the interface. Download the file, fill in values and then upload. The file is in a [CSV](https://www.howtogeek.com/348960/what-is-a-csv-file-and-how-do-i-open-it/) format.\
Sample file acts as an up-to-date documentation on the following.

* fields
* whether they are mandatory for upload
* possible values
* format of the value

> 📘 Since above has already been documented and maintain in the sample file these are not documented here again, please refer to it as a reference documentation.
<!-- END CHUNK -->

<!-- CHUNK: mandatory-fields-in-the-form -->
## Mandatory fields in the form

The mandatory fields in the form element are not applicable when uploading the data via CSV files - since we have seen when made mandatory especially for the legacy data, the users are force to upload some junk information (this may be added in the future).
<!-- END CHUNK -->

<!-- CHUNK: rules -->
## Rules

No rules are run as part of CSV upload. This implies that:

* field values created automatically via form element rules will not get created (such columns are present in the sample hence can be uploaded manually)
* observations created by decision rules will not be created automatically (such columns are present in the sample hence can be uploaded manually)
* Validation rule is not applied
* Edit rule is not applied

> 📘 Avni currently doesn't have a robust framework to run these rules on the server side. This may be added in future, if we observe that users need these.
<!-- END CHUNK -->

<!-- CHUNK: identifiers -->
## Identifiers

The primary purpose of these identifiers is for the users to be able to link different CSV file types upload data to each  other - in the same way as foreign key linkages between different records. These linkages can be created using identifiers of user's choosing. Lets try to understand this via an example. Lets assume there are three forms.

* Woman Registration (Subject)
* Pregnancy Program Enrolment (Program Enrolment)
  * links to woman
* Ante Natal Visit Form (Program Encounter)
  * links to pregnancy program


  <thead>
    <tr>
      <th>
        Form
      </th>

      <th>
        Columns
      </th>

      <th>
        Description
      </th>
    </tr>
  </thead>

  <tbody>
    <tr>
      <td>
        Woman Registration
      </td>

      <td>
        Id from previous system
      </td>

      <td>
        Any unique identifier that you may want to use. Note that you can make this up if you don't already have one. e.g. WOMAN-100001, WOMAN-100002
      </td>
    </tr>

    <tr>
      <td>
        Pregnancy Program Enrolment
      </td>

      <td>
        Id from previous system
      </td>

      <td>
        Any unique identifier that you may want to use. It should unique for all program enrolments. They can be same as woman registration id, but we recommend you use something like e.g. WOMAN-100001-01, WOMAN-100001-02 so that you can use multiple enrolments for the same woman.  

        It is possible that at the time of preparing this data, you are don't plan to upload woman registration via CSV and it is already present in Avni. In such a case you should use the Avni UUID value of the woman registration in this field.
      </td>
    </tr>

    <tr>
      <td>
        Pregnancy Program Enrolment
      </td>

      <td>
        Subject Id from previous system
      </td>

      <td>
        This should be used to match the pregnancy enrolment record woman registration record. Hence, for our example used so far, this field would have values like - WOMAN-100001, WOMAN-100002
      </td>
    </tr>

    <tr>
      <td>
        Ante Natal Visit Form
      </td>

      <td>
        Id from previous system
      </td>

      <td>
        You can leave this blank, if you intention is to create new records only and not edit them.
      </td>
    </tr>

    <tr>
      <td>
        Ante Natal Visit Form
      </td>

      <td>
        Program Enrolment Id
      </td>

      <td>
        This should be used to match the program ante natal visit form record with woman registration record. Hence, for our example used so far, this field would have values like - WOMAN-100001-01, WOMAN-100002-01  

        It is possible that at the time of preparing this data, you are don't plan to upload pregnancy enrolment data via CSV and it is already present in Avni. In such a case you should use the Avni UUID value of the woman registration in this field.
      </td>
    </tr>
  </tbody>


> 📘 The identifiers used above, for Id from previous system, are saved in Avni but is not visible in Avni after uploading, it is used only for matching records during CSV upload.
<!-- END CHUNK -->

<!-- CHUNK: scheduling-a-visit-and-upload-visit-details -->
## Scheduling a visit and Upload visit details

Please note that sample file for uploading visit details and scheduling a visit are different. These two options allow for  either creating a scheduled encounter/visit or completed encounter/visit. Note that scheduling a visit and then uploading the visit details for the same visit is not supported (as that is similar to edit).

![image](https://files.readme.io/30f7062dbe6572554955d88df13530e6e45c5a4cd5986fd81499661a294f78a2-image.png)
<!-- END CHUNK -->

<!-- CHUNK: important-notes-gotchas -->
## Important Notes / Gotchas

* **Limited Concept Support in CSV Upload**: Not all concepts are supported when uploading data via CSV. Specifically, the following are not supported:
  * GroupAffiliation
  * Id
  * File
* **Id Confusion**: The identifiers (used in Id from previous system) are different from Id elements in the form, if you have them.
* **Form Data Editing**: Editing previously submitted form data is not currently supported through the CSV upload process.
<!-- END CHUNK -->

<!-- CHUNK: questions -->
## Questions

### What if I have a comma in my observation value?

* Wrap your value in quotes.

### Why are decision concepts not appearing the sample file

If you are using decision concepts in the rule but not linked those concepts then this will happen.

### Is the order of values important?

* No. Columns can be in any order.

### How do I upload images?

* For images, use a url that the avni server can download. Ensure that
  * The images are a direct download link (not a redirect to a page that uses javascript to download)
  * The image urls end with the image type. eg: [https://somedomain.com/images/abc.png](https://somedomain.com/images/abc.png)


You can upload users, subjects, enrolments and encounters in bulk in this screen. Metadata zip files that have been downloaded from another organisation can also be uploaded in this screen.

All files except the metadata zip are supposed to be in a [CSV](https://en.wikipedia.org/wiki/Comma-separated_values) format. If you use Microsoft Excel, it has an option to save your spreadsheet in CSV format.

Use the **Download Sample** option to download a sample file. More details about the sample file are available [here](https://avni.readme.io/docs/upload-data)
<!-- END CHUNK -->

<!-- CHUNK: related-topics -->
## Related Topics

<!-- Add links to related documentation -->
<!-- END CHUNK -->