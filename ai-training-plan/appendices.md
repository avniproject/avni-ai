# Appendices

---
## Appendix A: Reference websites

- [Avni Website](https://avniproject.org)
- [Avni Documentation](https://avni.readme.io/docs/implementers-concept-guide-introduction)

- [Avni Staging](https://staging.avniproject.org/)
- [Dify Platform](https://dify.ai/)
- [Cloud Dify](https://cloud.dify.ai/)

## Appendix B: Codebase Reference

### Key Files for Rule Generation
- `avni-ai/dify/assistant_prompt.md` - Main assistant prompt
- `avni-ai/src/services/config_processor.py` - Config processing logic
- `avni-ai/src/tools/` - Tool implementations

### Key Files for Form Creation
- `avni-ai/src/tools/app_designer/` - App designer tools
- `avni-ai/AvniFormElementValidatorPrompt.md` - Form validation reference
- `avni-ai/src/services/tool_registry.py` - Tool registration

### Testing Framework
- `avni-ai/tests/judge_framework/` - LLM-as-judge testing
- `avni-ai/tests/` - Unit tests

---

## Appendix C: Sample CSV Schema (Draft)

```csv
page,group,field_name,data_type,mandatory,display_order,options
Basic Details,Personal Info,First Name,Text,true,1,
Basic Details,Personal Info,Last Name,Text,true,2,
Basic Details,Personal Info,Age,Numeric,true,3,
Basic Details,Personal Info,Gender,Coded:SingleSelect,true,4,Male|Female|Other
Health Info,Pregnancy,Is Pregnant,Coded:SingleSelect,false,5,Yes|No
Health Info,Pregnancy,Expected Delivery Date,Date,false,6,
Health Info,Pregnancy,Last Menstrual Period,Date,false,7,
Health Info,Vitals,Weight,Numeric,true,8,
Health Info,Vitals,Height,Numeric,true,9,
Health Info,Vitals,Blood Pressure Systolic,Numeric,false,10,
Health Info,Vitals,Blood Pressure Diastolic,Numeric,false,11,
Health Info,Risk Assessment,High Risk,Coded:SingleSelect,false,12,Yes|No
Health Info,Risk Assessment,Risk Factors,Coded:MultiSelect,false,13,Diabetes|Hypertension|Anemia|Previous Complications|Other
Health Info,Risk Assessment,Risk Factors - Other,Text,false,14,
```

### CSV Schema Column Definitions

| Column | Description | Required |
|--------|-------------|----------|
| `page` | Form page/section name | Yes |
| `group` | Question group within page | Yes |
| `field_name` | Display name of the field | Yes |
| `data_type` | Avni data type (Text, Numeric, Date, Coded:SingleSelect, Coded:MultiSelect, etc.) | Yes |
| `mandatory` | Whether field is required (true/false) | Yes |
| `display_order` | Order of field in form | Yes |
| `options` | Pipe-separated options for Coded fields | No |
