---
title: Multi-Language Forms and Translation Management
category: concepts-and-forms
audience: implementer
difficulty: intermediate
priority: medium
keywords:
- translation
- multi-language
- localization
- language support
- translation management
last_updated: '2026-03-16'
task_types:
- configuration
- tutorial
features:
- forms
technical_level:
- procedural
implementation_phase:
- development
complexity: moderate
retrieval_boost: 1.0
related_topics:
- form-structure.md
estimated_reading_time: 8 minutes
version: '1.0'
---
# Multi-Language Forms and Translation Management

<!-- CHUNK: tldr -->
## TL;DR

Since Avni is widely used for Data-collection by field workers, it is most likely to have a need for the Forms to be read and filled-up in their native language. For example, field workers providing health-care services in the remote villages of Gujarat would be most comfortable performing data-c...
<!-- END CHUNK -->

<!-- CHUNK: overview -->
## Overview

Since Avni is widely used for Data-collection by field workers, it is most likely to have a need for the Forms to be read and filled-up in their native language. For example, field workers providing health-care services in the remote villages of Gujarat would be most comfortable performing data-collection in Gujarathi, as opposed to English or Hindi.\
For this reason, Avni supports translation of data-collections forms to native language of the user(field worker) in the Avni "client" mobile application and "Data-Entry" Web application.
<!-- END CHUNK -->

<!-- CHUNK: supported-languages -->
## Supported Languages

Avni currently supports Translation capabilities from English to following languages:

* Hindi  
* Marathi  
* Gujarathi  
* Tamil  
* Kannada  
* Bengali  
* Telugu  
* Odia  
* Malayalam  
* Punjabi  
* Sanskrit  
* Urdu  
* Assamese

We additionally have some default translations already available for a few of the above languages, that would make it easier for an organisation to get started on its “Translations” journey. The languages that have some baked-in translations in Avni are as follows:

* Hindi  
* Marathi  
* Gujarathi  
* Tamil  
* Kannada
<!-- END CHUNK -->

<!-- CHUNK: prerequisites -->
## Prerequisites

In-order to set up translation for any of the aforementioned languages, the organisation should have enabled the language in the Languages section of the Organisation config.

### Steps to enable Languages for the Organisation

1. Navigate to the “Admin” application

   ![](https://files.readme.io/7bf088b321b670a88c9b73d86ed5d50999afb0ea9553067a0c3483c38e53c7b8-image.png)
2. Select the “Languages” section in the left-tab  
3. Add all the languages that are to be made available to the translation framework, using the drop-down and then click on “Save” button

   ![](https://files.readme.io/0dd7d20b674af9c7257ea0b6e3566e31a8f12dc66b8372251c4e8f305210398d-image.png)
<!-- END CHUNK -->

<!-- CHUNK: steps-involved-in-the-translation-process -->
## Steps involved in the translation process

Avni allows the management of translations using the Admin web interface. Below are the steps to translate the content of the app from English to the preferred language

### Navigation to ‘Translations’ module

Login to Avni Web Console and go to the ‘Translations’ module. 

![](https://files.readme.io/ebee37b87a4225d75c86d2c0ff612fcb9bd2ca653fd70d3e95a557ddb9c0a697-image.png)


### Downloading Translation Keys from Avni

* From the “Translations Dashboard”,download the keys after choosing the desired platform. Platforms are:  
  * Web  
  * Android  
* In general, most organisations need translations only for their field users who perform data-collection using their mobile devices. In such cases, the platform of interest is “Android” (Mobile).  
* If additionally, your organisation also wants translations to be done for the Data-Entry App, then also download the keys for the “Web” platform. 

![](https://files.readme.io/9a5030ec956f7983bf2edff00650c0a2d00367fee775375ecafb49957a8e4a6c-image.png)


* For each platform selection download, the app will download a zip file containing one JSON file per language available in the organisation config.   
* The JSON file will contain keys for both the standard platform app as well as those specific to your implementation, covering all labels in the app, form fields, location names and any other concepts created in the implementation.  
* The file will also contain existing translated values, if any. This is useful when you have to update the translations after a while, as you will already have all previously uploaded translations available for retention or modifications as needed  
* IMPORTANT Note: When organisations do not want Locations to be part of translations, then they need to bundle export without locations, import those into a temporary org and export translations from that temporary organisation. This was required for one of our organisations since they had a very large number of locations (More than 100,000) and hence were in need to translate other things before locations.

### Setting up a project in Translation Management System (TMS)

* The JSON files can be edited with any tool that the implementer is comfortable with, to come up with translated values for the target language.  
* But for most use cases, we would have multiple translators involved and/or a lot of keys are to be translated. In such cases, we highly recommend using an external translation management system (TMS) like [Lokalise](https://lokalise.com/) which provides a sophisticated editor for performing translations. The TMS provides the ability to import/export JSON files and supports a variety of use cases related to translations.  
* Avni has an enterprise-free plan for Lokalise. If you would like to use Lokalise, please request the Avni team to create your account and project to get started.

#### Creating an implementation project in Lokalise

This is an optional step, required only if the implementation project does not already exist. 

1. In the Project section, a new project needs to be created as shown in the screenshot below.   

   ![](https://files.readme.io/cde8ae8c4f81316f321973918c3717b138e529eb0c1bac0e8c305f1c74e4fb98-image.png)

   ![](https://files.readme.io/46fc019a73c69cd626060e89701fba69edf2894fdad9ccb112a85fd58cb08fd3-image.png)

   

2. While creating the project, provide the Project name, Base language (Which will be english always), and target language in which translations are needed.

   ![](https://files.readme.io/3b1d13d3c4ee9db1eb2f247b44fb36b44f98063d143c684a8c620aae8f1d4d96-image.png)

#### Uploading Translation keys to Lokalise

Once the project is ready in TMS and you have downloaded the translation ZIP file(s), log in to [Lokalise](https://app.lokalise.com/projects) with Samanvay's official email address, if not already done.

* Unzip the downloaded translation zip file  

* Before uploading the JSON, please make sure that null values are removed from the json files

  ![](https://files.readme.io/db2521a87f4b27a65fbac3b98fdf384aaf6024f21dd04d864bb95df03bceff93-image.png)

* In your project, navigate to the ‘Upload’ section and import the JSON file from the unzipped folder of the previously downloaded Translations zip file.

  ![](https://files.readme.io/7d26a129395f40bc2e2bbca4a770a27cf61fa0258d5129fd75a95538a51536d6-image.png)

* In the translation zip file that is downloaded, go to the local folder and select the English json file  

* Once the JSON file has been uploaded successfully, you will see the ‘Ready for Import’ message.

  ![](https://files.readme.io/6a0496a0ba800eb383d5b8f8978defe60bbaf01130868d8e2de18ab6f4324fbe-image.png)

* Go to the ‘editor’ section and verify the keys available for the translation.

  ![](https://files.readme.io/775e3003e6a87eade2045a7acf5b844ea1d1f60efac77cd4f74370fc3572c1b0-image.png)

  

#### Inviting Contributors to the project

Next, Navigate to the ‘Contributors’ section to send out invites to other people

![](https://files.readme.io/0903aa35f4aa3b0b7cc8ec50506511d0e99f0dd8b624eeaf5c403d816b204d3c-image.png)


Perform below mentioned tasks to invite users to collaborate on the project

* Role should be selected as ‘Translator’   
* “Reference language” should have the base language (Usually English) and  
* “Contributable language” should have target language

![](https://files.readme.io/c3a2ff0b427c727aea29a09ff339a6c7a7219079cf034cd76a114b956f0c3ec8-image.png)


### Guide for translating keys using Lokalise

* All invitees will receive an Email invite from Lokalise with instructions to login and access the project.

  ![](https://files.readme.io/0f9fcf8ad025f5dd50c754a3736618988e51eced350063df791a20145073c8fb-image.png)

* Once logged in, available projects will be shown in the projects tab/ home screen. you can click on the project name to access the translation items.

  ![](https://files.readme.io/29a4f970e6de4969a115870182c25584f55b1fc1a65eaa09a46b2786fc9317f6-image.png)

* The project would display the editor page by default, and the list of keys should be visible at the bottom.

  ![](https://files.readme.io/e0ab4bd3396825a5df93f6cd6f2e39997d51e8a82b9d33c9ff65d10c9f9e7e25-image.png)

* You can select the Bilingual option shown in the screenshot below and search the question or required field names to be translated.

  ![](https://files.readme.io/0de7bfccf120d85d1154466d2ae52a542f12b0ef10eddf0f133b228d3e6a49cf-image.png)

* After giving the keywords in the search bar, you can see the results below which show questions and field names on the left side. against which you need to provide the Kannada translation and save the response.

  ![](https://files.readme.io/914ab3acbc6c6d25788f872ceecca5160f1420ad85d29afc3ff45d3e240d5d16-image.png)

* Additional notes  
  * Keep the required forms handy while you start the translation process, you can refer to the questions from respective and update the values in Lokalise.  
  * In case of questions, the box on the left side might show "empty" and the question would be visible above that in blue fonts. you can provide the appropriate translation against that on the right-hand side box.

#### Translating Keys with Dynamic string having placeholders

Consider the following “Android” Platform keys, which are examples for Dynamic strings with placeholders:

| numberAboveHiAbsolute | "Should be \{\{limit}}, or less than \{\{limit}}" |
| :-------------------- | :------------------------------------------------ |
| enrolmentSavedMsg     | "\{\{programName}} Enrolment Saved"               |

In-order to translate them to Hindi, you would have to specify following in the translated json file:

| numberAboveHiAbsolute | "\{\{limit}} के बराबर या \{\{limit}} से कम" |
| :-------------------- | :------------------------------------------ |
| enrolmentSavedMsg     | "\{\{programName}} एनरोलमेण्ट सेव हुआ"      |

As shown above, ensure that you retain the string placeholder content within “\{\{” and “}}” as is in native english. Ex: “\{\{limit}}”, "\{\{programName}}”

### Uploading Translations

After completing translation for all the required keys, questions and forms you can download the translated values JSON file of the target language.

* Go to the “Downloads” section of the project  

  ![](https://files.readme.io/934b5c2b87ce2127c6983e5f97739abd5aa4381c3c0c884f7d53a040f9c4d8a1-image.png)
* As seen above, select the ‘Don’t Export’ option for the “Empty Translations” field, so as to export only the translated fields.  
* Click on “Build and Download” option to download the Translated values ZIP file

  ![](https://files.readme.io/ae74952cda34852fe4c7d78933624066f83514681cf5fe52ec8d17b53e911303-image.png)
* Please note that the downloaded ZIP file would contain the JSON file of the base language (English) and targeted language JSON.

  ![](https://files.readme.io/f61d4ac05c7f32ff80ce10f556145a89b11b3ef9f0a43ee2509c4515d31c321c-image.png)
* Now the JSON file of the translation language needs to be uploaded into the Avni. Navigate to the “Translations Dashboard“. Using its “Upload Translations” functionality, upload the JSON file, after choosing an appropriate language. Be careful about choosing the target language, it should be same as the language of the translated values.

  ![](https://files.readme.io/1cc8a1416150da1c1961d5b82bb4508b387a4be7a71d4679ad68f4778ce47301-image.png)
* On successful upload of the translated values, you should see a change in the value of the “Keys with translations” column for the corresponding Language, in the “Translations Dashboard”.
<!-- END CHUNK -->

<!-- CHUNK: using-the-avni-client-application-in-user-s-native -->
## **Using the Avni client application in User’s native Language**

On the Avni client app, users would need to sync their devices in-order to get the new translations.

If the default language for the User hasn’t been set to his/her desired native language, then the user should be able to switch to it, by navigating to the “More” menu and clicking on the “Edit Settings” button at the top, and selecting the language in which he/she wants to see the app content.

![image](https://files.readme.io/28964f670ac61932780ce5d1a5d3c2553a005e392960a59852aacc0c130b57b9-image.png)

![image](https://files.readme.io/aed7f494a90af456f84dc6caa5ec5c80c32e9f469b61ec7295d60a7deaa86503-image.png)


After adding [languages](#/admin/language) you will be able to download/upload the translation file for all the different languages.

Learn more about [translation management](https://avni.readme.io/docs/translation-management).
<!-- END CHUNK -->

<!-- CHUNK: related-topics -->
## Related Topics

<!-- Add links to related documentation -->
<!-- END CHUNK -->