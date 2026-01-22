# Appendices

---

## Appendix A: Codebase Reference

### Key Files for Rule Generation
- `@/Users/himeshr/IdeaProjects/avni-ai/dify/assistant_prompt.md` - Main assistant prompt
- `@/Users/himeshr/IdeaProjects/avni-ai/src/services/config_processor.py` - Config processing logic
- `@/Users/himeshr/IdeaProjects/avni-ai/src/tools/` - Tool implementations

### Key Files for Form Creation
- `@/Users/himeshr/IdeaProjects/avni-ai/src/tools/app_designer/` - App designer tools
- `@/Users/himeshr/IdeaProjects/avni-ai/AvniFormElementValidatorPrompt.md` - Form validation reference
- `@/Users/himeshr/IdeaProjects/avni-ai/src/services/tool_registry.py` - Tool registration

### Testing Framework
- `@/Users/himeshr/IdeaProjects/avni-ai/tests/judge_framework/` - LLM-as-judge testing
- `@/Users/himeshr/IdeaProjects/avni-ai/tests/` - Unit tests

---

## Appendix B: Sample CSV Schema (Draft)

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
