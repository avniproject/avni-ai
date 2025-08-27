# 📋 Project Plan: Avni Assistant (Phase-wise)

## **Phase 1: Bundle Matcher + Guided Chat**
**Goal**: Assist users by suggesting prebuilt bundles through chat.  

### Work Items
1. **Conversation Framework**
   - Set up Orchestration Layer (basic routing to Tier 1 vs Tier 2 LLM).  
   - Implement session memory (short-term storage).  
   - Implement conversation logging (request/response).  

2. **Bundle Matcher**
   - Define metadata schema for bundles (tags, domain, config summary, prerequisites).  
   - Build bundle library (store metadata + JSON definitions).  
   - Implement similarity matching (semantic embeddings of user request vs bundle metadata).  
   - Return ranked suggestions with descriptions.  

3. **UI/UX**
   - Chat interface (guided wizard + freeform chat).  
   - Bundle suggestion flow (show top matches, allow “tell me more” or “apply later”).  

---

## **Phase 2: Knowledge Base + RAG**
**Goal**: Provide grounded answers using Avni documentation + examples.  

### Work Items
1. **Knowledge Base Setup**
   - Collect Avni docs, FAQs, config examples.  
   - Convert to chunked text format (Markdown/JSON).  
   - Index into vector DB (FAISS/Pinecone/Weaviate).  

2. **RAG Pipeline**
   - Integrate retriever in orchestration.  
   - Implement context injection (retrieved docs into LLM prompt).  
   - Fine-tune prompts to ensure strict grounding.  

3. **Memory Enhancements**
   - Add long-term memory (conversation embeddings).  
   - Implement semantic recall for repeated users.  

4. **UX Enhancements**
   - Highlight sourced docs in responses (“Based on Avni docs → …”).  
   - Provide citations/links for transparency.  

---

## **Phase 3: API Adapter + Audit Logs**
**Goal**: Allow assistant to apply changes in Avni after confirmation.  

### Work Items
1. **API Adapter**
   - Build secure adapter for Avni API.  
   - Define supported actions (create entity, update form, apply bundle).  
   - Implement payload validation.  

2. **Confirmation & Guardrails**
   - Add “propose → confirm → execute” workflow.  
   - Preview config changes before applying.  
   - Allow rollback if needed.  

3. **Audit Logs**
   - Schema for storing before/after states, user confirmation, execution status.  
   - Write to durable store separate from conversation logs.  
   - Build admin dashboard to review audit history.  

4. **Safety**
   - Permission checks (only authorized users can apply changes).  
   - Rate limits + error handling.  

---

## **Ongoing Work Across Phases**
- Continuous improvement of orchestration (better intent detection, tier routing).  
- Fine-tuning LLM prompts based on logs.  
- Bundle library expansion.  
- User feedback loop (thumbs up/down on responses).  
