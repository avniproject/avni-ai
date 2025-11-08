You are an expert Avni form designer and domain consultant.
Your task is to validate the form provided by the user based on the given context.
You should:
Check whether the form's questions are relevant, complete, and logically structured.
Identify any issues or inconsistencies (e.g., missing questions, redundant fields, unclear wording).
Suggest improvements — including edits, removals, or additions to the questions — that would make the form more effective for its intended purpose.
Explain your reasoning briefly and clearly for each suggestion.

IMPORTANT: Only report actual issues. If the form is well-designed and follows proper Avni patterns, simply state "✅ This form appears to be well-structured and follows proper Avni design patterns. No issues identified."

Do not force yourself to find problems where none exist. Focus on genuine issues that would impact form functionality, user experience, or data quality.

CRITICAL: When reporting issues, be SPECIFIC. Provide exact field names, UUIDs, or line references. 
❌ BAD: "Some field names are inconsistent" 
✅ GOOD: "Field 'Patient Name' (UUID: abc-123) has inconsistent casing"

❌ BAD: "Several fields are marked as non-editable"
✅ GOOD: "Fields 'Age' and 'Gender' have editable=false which may restrict necessary user input"

**ABSOLUTE RULES:**
1. NEVER mention fields with "voided": true - treat them as if they don't exist
2. NEVER report organisation ID as an issue - it's never a problem
3. SingleSelect type with Numeric dataType is VALID - do not flag this

Return your answer as a structured list of:
⚠️ Issues found and  💡 Suggested improvements

If no issues are found, respond with: "✅ Form validation complete - no issues identified."

<context>
{{#context#}}
</context>

# Avni Forms Knowledge Base

This document contains comprehensive information about Avni form structures, including both correct production forms and examples of incorrect forms for validation purposes.

## Table of Contents
1. [Production Forms (Correct Examples)](#production-forms-correct-examples)
2. [Example Forms (Examples of What To Do and What Not To Do)](#example-forms-examples-of-what-to-do-and-what-not-to-do)
3. [Key Patterns and Best Practices](#key-patterns-and-best-practices)
4. [Common Mistakes to Avoid](#common-mistakes-to-avoid)

## Production Forms (Correct Examples)

Common form types include: Individual Registration, Pregnancy Enrolment, ANC, Delivery, Child Enrolment, Growth Monitoring, PNC Encounter, Eligible Couple Followup, Program Exit, and various Encounter Cancellation forms. These demonstrate proper Avni patterns with correct organisation IDs, proper subject references, and appropriate business logic.

## Example Forms (Examples of What To Do and What Not To Do)

### 1. Individual Registration (Wrong Example)
- **Type**: IndividualProfile
- **UUID**: 76ab20e6-88c5-413b-ae7b-c58c474e8700
- **Issues Identified**:
  - **Incorrect Subject Type Reference**: Different subject type UUIDs
  - **Poor Form Structure**: Single "Basic questions" group instead of organized sections
  - **Missing Validation**: No mandatory field enforcement or validation rules
  - **Incomplete Relationships**: Subject relationships not properly configured

#### Specific Critical Issues:

1. **Name Field in Registration Form** ❌
```json
{
  "name": "Name",
  "uuid": "37dcbe2b-27be-47a3-a42e-099ac95f1028",
  "concept": {
    "name": "Name",
    "dataType": "Text"
  },
  "type": "SingleSelect"
}
```
**Problem**: Name field should NOT be included in registration forms because it's automatically added by default on the first page.
**Solution**: Remove name field entirely from form definition.

2. **Relatives Field in Registration** ❌
```json
{
  "name": "Relatives",
  "concept": {
    "dataType": "Subject",
    "keyValues": [{"key": "subjectTypeUUID", "value": "e1e13801-d608-4c63-925d-94846d222d02"}]
  }
}
```
**Problem**: Individual registration should not include relatives field.
**Solution**: Create a separate household subject type instead. Use household registration for family relationships.

3. **Child Details as Repeatable Group** ❌
```json
{
  "name": "Child details (repeatable question group)"
}
```
**Problem**: Children should not be modeled as repeatable question groups.
**Solution**: Create children as separate subject types and link them via relationships.

4. **Inconsistent Mandatory Field Declaration** ❌
```json
{
  "name": "Do you have a ration card? (Mandatory for food supplies)",
  "mandatory": false
}
```
**Problem**: Field name indicates it's mandatory but `mandatory` is set to `false`.
**Solution**: Either remove "(Mandatory...)" from name and keep `mandatory: false`, or set `mandatory: true`.

### 2. Program Enrolment (Wrong Example)
- **Type**: ProgramEnrolment
- **UUID**: bb7f2149-7e09-41c2-8479-b4e277bd15ce
- **Issues Identified**:
  - **Inappropriate Purpose**: Emergency health assessment not suitable for program enrolment
  - **Missing Program Context**: Lacks proper program-specific enrolment data
  - **No Integration Logic**: Missing visit scheduling and workflow integration

#### Specific Critical Issues:

5. **Non-Unique Generic Coded Answers** ❌
When using coded concepts, generic answers like "Other", "None of the above", "All of the above" should be unique across the system.
**Problem**: Multiple forms creating separate "Other" concepts instead of reusing existing ones.
**Solution**: Use standardized UUIDs for common generic answers.

6. **Dependent Fields Without Visibility Rules** ❌
```json
{
  "name": "Do you want additional aid?",
  "mandatory": false
}
```
**Problem**: Dependent fields should have visibility rules and be non-mandatory.
**Solution**: ✅ This example actually shows correct implementation with visibility rules.

7. **Proper Numeric Concept Configuration** ✅
```json
{
  "name": "Temperature",
  "concept": {
    "dataType": "Numeric",
    "lowAbsolute": 95.0,
    "highAbsolute": 108.0,
    "lowNormal": 97.0,
    "highNormal": 100.0
  }
}
```
Temperature and saturation fields correctly include proper validation ranges.

8. **Phone Number Without Validation** ❌
```json
{
  "name": "Phone Number",
  "concept": {
    "dataType": "Text"
  }
}
```
**Problem**: Phone numbers marked as text without validation.
**Solution**: Add regex validation for 10-digit phone numbers: `^[6-9]\\d{9}$`

9. **Incorrect Data Type for Numeric Fields** ❌
```json
{
  "name": "How many days since the patient is ill?",
  "concept": {
    "name": "Days",
    "dataType": "Text"
  }
}
```
**Problem**: Days should be numeric, not text.
**Solution**: Use `"dataType": "Numeric"` with appropriate validation ranges.

10. **Wrong Field Type for Yes/No Questions** ❌
```json
{
  "name": "was patient handed over ors?",
  "concept": {
    "name": "yesno",
    "dataType": "Coded",
    "answers": [
      {"name": "yes", "order": 0.0},
      {"name": "no", "order": 1.0}
    ]
  },
  "type": "MultiSelect"
}
```
**Problem**: Yes/No questions should use `SingleSelect`, not `MultiSelect`.
**Solution**: Change `"type": "SingleSelect"` for binary choice questions.

---

## Complete JSON Examples

### Individual Registration (Wrong Example) - Complete JSON

```json
{
  "name": "Individual Registration",
  "uuid": "76ab20e6-88c5-413b-ae7b-c58c474e8700",
  "formType": "IndividualProfile",
  "formElementGroups": [
    {
      "uuid": "061b81bd-a096-4f27-bb6f-b1da97aa8ed7",
      "name": "Basic questions",
      "displayOrder": 1.0,
      "formElements": [
        {
          "name": "Name",
          "uuid": "37dcbe2b-27be-47a3-a42e-099ac95f1028",
          "keyValues": [],
          "concept": {
            "name": "Name",
            "uuid": "5715495c-687f-432e-b9a9-624252b8a42f",
            "dataType": "Text",
            "id": 315500,
            "active": true,
            "media": []
          },
          "displayOrder": 1.0,
          "type": "SingleSelect",
          "organisationId": 676,
          "mandatory": false
        },
        {
          "name": "Relatives",
          "uuid": "a18e242c-e6a9-4092-a9ba-cd2b220e2252",
          "keyValues": [],
          "concept": {
            "name": "Relatives",
            "uuid": "031462a3-b564-4187-852f-5411989e36aa",
            "dataType": "Subject",
            "id": 315501,
            "active": true,
            "keyValues": [
              {
                "key": "subjectTypeUUID",
                "value": "e1e13801-d608-4c63-925d-94846d222d02"
              }
            ],
            "media": []
          },
          "displayOrder": 2.0,
          "type": "SingleSelect",
          "organisationId": 676,
          "mandatory": false
        },
        {
          "name": "Child details",
          "uuid": "4a0364e2-9b08-4dc4-a932-532e76e3f705",
          "keyValues": [
            {
              "key": "repeatable",
              "value": true
            }
          ],
          "concept": {
            "name": "Child details",
            "uuid": "655ef651-debf-4977-9d37-243ab97844cc",
            "dataType": "QuestionGroup",
            "id": 315503,
            "active": true,
            "media": []
          },
          "displayOrder": 3.0,
          "type": "SingleSelect",
          "organisationId": 676,
          "mandatory": false
        },
        {
          "name": "Some coded questions",
          "uuid": "994774da-e80e-43d0-b3e5-e21c4c271add",
          "keyValues": [],
          "concept": {
            "name": "questions",
            "uuid": "7d553fd2-e33d-4a1e-b590-ed2eb33837f3",
            "dataType": "Coded",
            "answers": [
              {
                "name": "a",
                "uuid": "a7e24eb1-0bce-4348-87b5-8c1681d596b0",
                "order": 0.0
              },
              {
                "name": "b",
                "uuid": "e022cd38-5e45-473f-b4b6-d239a542d488",
                "order": 1.0
              },
              {
                "name": "None of the above",
                "uuid": "b6ad2a63-9c57-4b81-ac2e-39663534f004",
                "order": 4.0
              },
              {
                "name": "c",
                "uuid": "263b65c5-914b-4492-ac15-41d33234c7d3",
                "order": 2.0
              },
              {
                "name": "Other",
                "uuid": "67975595-5ebb-47d7-9999-e92d47e5add7",
                "order": 3.0
              }
            ],
            "id": 315508,
            "active": true,
            "media": []
          },
          "displayOrder": 5.0,
          "type": "SingleSelect",
          "organisationId": 676,
          "mandatory": false
        },
        {
          "name": "Do you have a ration card? (Mandatory for food supplies)",
          "uuid": "f49075d5-267e-4112-9390-793d8f69eba2",
          "keyValues": [],
          "concept": {
            "name": "RationCardPossesion",
            "uuid": "aa75ddcd-cfd1-4ca3-a19e-0a8e2138d4c9",
            "dataType": "Coded",
            "answers": [
              {
                "name": "no",
                "uuid": "6d12dbd0-5557-49d1-a302-c9b54fe5a00b",
                "order": 1.0
              },
              {
                "name": "yes",
                "uuid": "5d02c3b9-fdce-4a36-959d-9fd4a5c45db3",
                "order": 0.0
              }
            ],
            "id": 315511,
            "active": true,
            "media": []
          },
          "displayOrder": 6.0,
          "type": "SingleSelect",
          "organisationId": 676,
          "mandatory": false
        },
        {
          "name": "Do you want additional aid?",
          "uuid": "812cc21d-7e14-47c1-9130-cf48d7c97aed",
          "keyValues": [],
          "concept": {
            "name": "Aid",
            "uuid": "519e9489-aea6-45e9-a34f-8641aaeca88e",
            "dataType": "Coded",
            "answers": [
              {
                "name": "yeah",
                "uuid": "a4f36a0e-dcf5-4bc3-8793-e396beb5b6e7",
                "order": 0.0
              },
              {
                "name": "no",
                "uuid": "6d12dbd0-5557-49d1-a302-c9b54fe5a00b",
                "order": 1.0
              }
            ],
            "id": 315513,
            "active": true,
            "media": []
          },
          "displayOrder": 7.0,
          "type": "SingleSelect",
          "rule": "'use strict';\n({params, imports}) => {\n  const individual = params.entity;\n  const moment = imports.moment;\n  const formElement = params.formElement;\n  const _ = imports.lodash;\n  let visibility = true;\n  let value = null;\n  let answersToSkip = [];\n  let validationErrors = [];\n  \n  const condition11 = new imports.rulesConfig.RuleCondition({individual, formElement}).when.valueInRegistration(\"aa75ddcd-cfd1-4ca3-a19e-0a8e2138d4c9\").containsAnswerConceptName(\"6d12dbd0-5557-49d1-a302-c9b54fe5a00b\").matches();\n  \n  visibility = !(condition11 );\n  \n  return new imports.rulesConfig.FormElementStatus(formElement.uuid, visibility, value, answersToSkip, validationErrors);\n};",
          "declarativeRule": [
            {
              "actions": [
                {
                  "actionType": "hideFormElement"
                }
              ],
              "conditions": [
                {
                  "compoundRule": {
                    "rules": [
                      {
                        "lhs": {
                          "type": "concept",
                          "scope": "registration",
                          "conceptName": "RationCardPossesion",
                          "conceptUuid": "aa75ddcd-cfd1-4ca3-a19e-0a8e2138d4c9",
                          "conceptDataType": "Coded"
                        },
                        "rhs": {
                          "type": "answerConcept",
                          "answerConceptNames": ["no"],
                          "answerConceptUuids": ["6d12dbd0-5557-49d1-a302-c9b54fe5a00b"]
                        },
                        "operator": "containsAnswerConceptName"
                      }
                    ],
                    "conjunction": "or"
                  }
                }
              ]
            }
          ],
          "organisationId": 676,
          "mandatory": false
        }
      ],
      "organisationId": 676,
      "timed": false,
      "display": "Basic questions"
    }
  ],
  "organisationId": 676,
  "subjectType": {
    "id": 1789,
    "uuid": "e1e13801-d608-4c63-925d-94846d222d02",
    "name": "Individual",
    "type": "Individual",
    "organisationId": 676
  },
  "decisionRule": "",
  "visitScheduleRule": "",
  "validationRule": "",
  "checklistsRule": ""
}
```

### Program Enrolment (Wrong Example) - Complete JSON

```json
{
  "name": "Program Enrolment",
  "uuid": "bb7f2149-7e09-41c2-8479-b4e277bd15ce",
  "formType": "ProgramEnrolment",
  "formElementGroups": [
    {
      "uuid": "eba1a69e-cf97-4d6c-864d-720336782961",
      "name": "Emergency Health Check",
      "displayOrder": 1.0,
      "formElements": [
        {
          "name": "What is the body temp?",
          "uuid": "4e2a73f4-f498-4a9a-ae51-84434e6d2cca",
          "keyValues": [],
          "concept": {
            "name": "Temp",
            "uuid": "ee3c1cb0-a6a6-448a-81a9-9219b8be92ab",
            "dataType": "Numeric",
            "lowAbsolute": 90.0,
            "highAbsolute": 106.0,
            "lowNormal": 96.8,
            "highNormal": 99.0,
            "unit": "Fahrenheit",
            "id": 315514,
            "active": true,
            "media": []
          },
          "displayOrder": 1.0,
          "type": "SingleSelect",
          "organisationId": 676,
          "mandatory": false
        },
        {
          "name": "What is blood oxygen saturation?",
          "uuid": "c86b5858-d118-48e6-a320-cb53d0c844ac",
          "keyValues": [],
          "concept": {
            "name": "BOS",
            "uuid": "f003fc44-f78e-4cee-bb27-21d7112d56a8",
            "dataType": "Numeric",
            "lowAbsolute": 0.0,
            "highAbsolute": 100.0,
            "lowNormal": 95.0,
            "highNormal": 100.0,
            "unit": "Percentage",
            "id": 315515,
            "active": true,
            "media": []
          },
          "displayOrder": 2.0,
          "type": "SingleSelect",
          "organisationId": 676,
          "mandatory": false
        },
        {
          "name": "What is the mobile number of attendant?",
          "uuid": "aafa0212-cfec-4836-b9c2-e694505a2a62",
          "keyValues": [],
          "concept": {
            "name": "Phone number",
            "uuid": "32cb8cb5-4c2e-425a-8c4c-f3cd124b41c2",
            "dataType": "Text",
            "id": 315516,
            "active": true,
            "media": []
          },
          "displayOrder": 3.0,
          "type": "SingleSelect",
          "organisationId": 676,
          "mandatory": false
        },
        {
          "name": "was patient handed over ors?",
          "uuid": "5193ac10-5854-4ac2-b3e7-9eec149aaf44",
          "keyValues": [],
          "concept": {
            "name": "yesno",
            "uuid": "89b8ff2b-96c2-449f-83ff-c243bacc86a8",
            "dataType": "Coded",
            "answers": [
              {
                "name": "yes",
                "uuid": "5d02c3b9-fdce-4a36-959d-9fd4a5c45db3",
                "order": 0.0
              },
              {
                "name": "no",
                "uuid": "6d12dbd0-5557-49d1-a302-c9b54fe5a00b",
                "order": 1.0
              }
            ],
            "id": 315518,
            "active": true,
            "media": []
          },
          "displayOrder": 4.0,
          "type": "MultiSelect",
          "organisationId": 676,
          "mandatory": false
        },
        {
          "name": "How many days since the patient is ill?",
          "uuid": "11559c89-712f-4720-a240-05040cada0eb",
          "keyValues": [],
          "concept": {
            "name": "Days",
            "uuid": "90aececf-46f8-40f3-a605-d4dd2d126340",
            "dataType": "Text",
            "id": 315519,
            "active": true,
            "media": []
          },
          "displayOrder": 5.0,
          "type": "SingleSelect",
          "organisationId": 676,
          "mandatory": false
        },
        {
          "name": "Aadhar Number",
          "uuid": "eaa920a6-7529-401e-bc29-a781ef72c0de",
          "keyValues": [],
          "concept": {
            "name": "Aadhar",
            "uuid": "df4166df-20bd-4177-b3e5-30291a525ef1",
            "dataType": "Text",
            "id": 315517,
            "active": true,
            "media": []
          },
          "displayOrder": 6.0,
          "type": "SingleSelect",
          "organisationId": 676,
          "voided": true,
          "mandatory": false
        }
      ],
      "organisationId": 676,
      "timed": false,
      "display": "Emergency Health Check"
    }
  ],
  "organisationId": 676,
  "decisionRule": "",
  "visitScheduleRule": "",
  "validationRule": "",
  "checklistsRule": ""
}
```

## Key Patterns and Best Practices

### 1. Consistent Architecture
- All forms follow standard Avni structure: `formElementGroups` → `formElements` → `concept`
- Each element has unique UUID for stable references
- Proper subject type references using correct UUIDs

### 2. Key Validation Rules
- **Text dataType with SingleSelect type**: VALID pattern for text fields with dropdown UI
- **ExcludedAnswers**: Use in keyValues to hide specific answers from users (answers still exist in concept but won't display)
- **Answer Ordering**: Order values can be non-sequential (1.0, 3.0, 7.0) - reflects priority, not sequence
- **Mandatory Fields**: Cancellation forms should typically have mandatory cancel reason
- **Conditional Logic**: Fields can have visibility rules based on other field values

## Common Mistakes to Avoid

### Critical Issues to Flag:
1. **Name fields in registration forms** - Always wrong (auto-added by system)
2. **MultiSelect for Yes/No questions** - Should be SingleSelect  
3. **Text dataType for numeric fields** (Days, Age) - Should be Numeric dataType (but SingleSelect type with Numeric dataType is valid)
4. **Missing phone validation** - Phone numbers need regex: `^[6-9]\\d{9}$`
5. **Relatives in individual registration** - Use household subject types instead
6. **Children as repeatable groups** - Should be separate subject types
7. **Inconsistent mandatory declarations** - Field name vs actual mandatory setting


## What NOT to Flag as Issues

**Do NOT report these as problems - they are valid Avni patterns:**

### ✅ Valid Patterns Often Mistaken as Errors:

1. **Voided Fields**: Fields with `"voided": true` are INTENTIONALLY disabled. COMPLETELY IGNORE voided fields - do not report them as issues. Do not analyze voided fields for mandatory settings, data types, or any other attributes.

2. **SingleSelect with Numeric DataType**: This is VALID - numeric fields can use SingleSelect type for dropdown UI. Do not flag this as an issue.

3. **Organisation ID**: Never report organisation ID as a problem. Any organisation ID value is valid for its deployment context.

4. **ExcludedAnswers with Present Answers**: If answers exist in the concept's answer list BUT are also listed in `"ExcludedAnswers"` keyValues, this is CORRECT - the excluded answers will be hidden from users

5. **Non-Sequential Answer Ordering**: Answer order values like 1.0, 3.0, 5.0, 7.0, 9.0 are perfectly valid - order reflects priority/logic, not sequential numbering

6. **Text DataType with SingleSelect Type**: This is a VALID combination for text input fields that use dropdown/selection UI but store text values

7. **Program-Specific Answer Filtering**: Cancellation forms commonly exclude certain reasons that don't apply to that specific encounter type - this is intentional design

8. **Complex Visit Scheduling Logic**: Encounter cancellation forms often have sophisticated rescheduling rules based on cancellation reasons - this is expected functionality

9. **Conditional Field Visibility**: Fields that only appear when certain conditions are met (like "Other reason" when "Other" is selected) are correct implementations

10. **Mandatory Fields in Cancellation Forms**: Cancel reason fields should typically be mandatory to ensure proper tracking

**CRITICAL: Any field with `"voided": true` should be completely IGNORED during validation. Do not mention voided fields in your analysis.**

### ⚠️ Focus Validation On These Real Issues Instead:
- Missing validation rules where needed
- Missing mandatory field markers
- Improper subject type references  
- Missing phone number regex validation
- Wrong data types for numeric fields
- Children modeled as repeatable groups instead of subjects
- Name fields in registration forms
- Relatives fields in individual registration

This knowledge base should help validate new forms against established patterns and identify potential issues before deployment.