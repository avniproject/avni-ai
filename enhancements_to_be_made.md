### General design to separate the flow into requirements gathering stage and bundle generation stage

1. Input: XLS(Scoping / srs / modelling),PDF/Images (Forms), , XLS / csv / pdf   (Existing org data sheets)  
2. Data extraction using LLM extractor node, to generate entities JSONL  
3. COnvert into YAML/MARKDOWN Spec without technicalities for initial Scoping/modelling  
   	\- Validate homogeneous content usable for spec driven dev or flag immediately.  
   	\- COnvert into YAML/MARKDOWN spec based on reference data, some llm prompt and deterministic end-points.  
   	\- Store the YAML/MARKDOWN SPEC and drive rest of the flow based on it.)

Inputs

- Do not trigger the workflow unless all info is provided by the user  
- Reduce the cost downstream  
- If the files are uploaded later then have callbacks  
- Decouple conversation and scoping \-  from bundle generation  
- Ensure that the spec is defined before generating the bundle  
- Ensure that flow processes new files uploaded in every new prompts and appends to entityJsonl  
- Extend the Dify entity extractor prompt to also extract a forms and concepts from the spec document.

Validations

- Deterministic validation   
- Adequacy of info \- clarification questions based on schema or context  
- Same schema or context to check for uploaded file content

Before giving to bundle generator

- Give to pydantic validators the content  
- Have Request schema and Response Schema  
- Validate the request being sent to LLM schema to match request format  
- Validate the llm response to match format Response Schema  
- Have ability to make immediate corrections based on validator response in the same loop, to have fault tolerance : Send error and previous response, do this iteratively(Max 3 tries) till validation successful  
- 
