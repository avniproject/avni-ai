# AI Architecture Evaluation Notes

## Problems with Current Approach (avni-ai + Dify)

### Version Control
- Prompts live in two places: `dify/*.md` files in repo AND Dify UI. Changes in one don't sync to the other.

### Conversation Continuity
- Each chat starts from the beginning — no session resumption across conversations (you can't continue from a particular node).

### Dify Platform Limitations
- Human-in-the-loop node cannot be placed inside a loop (open GitHub issue, no fix timeline).
- Python sandbox has no access to external libraries (openpyxl, etc.) — forced us to move parsing to server-side API.
- Code nodes intermittently fail to execute before answer nodes (bundle generation flow bug).
- Structured output from LLM must be a JSON object, not an array — forced restructuring of our entity format.
- File uploads are only available on the first message — subsequent turns don't carry the file, requiring conversation variable workarounds.

---

## Problems in avni-ai-platform

### SRS Parsing
- Completely deterministic — `srs_parser.py` (2,023 lines) and `canonical_srs_parser.py` (963 lines) rely on exact column header matching.
- Silently skips entire sheets if headers don't match expected patterns
- Cannot handle spelling mistakes, renamed columns, or non-standard layouts.
- Misses fields like `lowest_address_level` — only extracts `name` and `type` from subject types.
- **Need**: LLM-based extraction that interprets the document regardless of format (our `extraction_llm_prompt.md` approach).

### Data Models
- `SRSData` uses primitives: `subjectTypes: list[dict[str, Any]]`, `encounterTypes: list[str]` (just names, no metadata).
- No typed contracts matching avni-server's actual contracts.

### UUID Generation
- Uses UUID v5 wheras avni-server uses UUID v4

### Bundle Validation
- `server_contract_validator.py` and `bundle_validator.py` exist but are never called from the generation pipeline.

### In-Memory State
- `_pending_actions`, `_bundle_pending`, `_srs_state`, `_org_contexts` are all in-memory dicts — lost on server restart.
- Only conversation history is persisted to PostgreSQL.

### Intent Routing
- Keyword-based classification misroutes knowledge questions containing action keywords (e.g., "what is a bundle?" routes to bundle generation instead of knowledge/RAG).
- Claude LLM fallback exists but rarely triggers because keyword threshold is too low (0.25).

### LLM Enrichment
- Fails silently — if LLM returns malformed JSON, all field enrichments are dropped with no user feedback.

---

## Requirements for Target Architecture

### Must Have
- Single codebase with all prompts, flows, and logic version controlled in git.
- LLM-based entity extraction from specification documents (handles any format).
- Typed contract models matching avni-server's contracts (SubjectTypeContract, ProgramContract, etc.).
- Human-in-the-loop confirmation/correction loop with no framework limitations.
- Conversation history persisted to database (survives restarts).
- Bundle validation against avni-server contracts before export.
- Direct bundle upload to avni-server via `/api/importMetaData`.
- Testable end-to-end (no external orchestration dependency for tests).

### Must Retain (from existing Avni AI Assistant)
- RAG-based Q&A using Avni knowledge base.
- Intent routing (RAG, config CRUD, bundle generation, out-of-scope).
- Chat interface integrated with Avni webapp.
- Config CRUD via Assistant LLM (existing Prod flow capability).

### Should Have
- LLM field enrichment (infer allowNegative, allowDecimal, ranges from field names).
- Multi-provider LLM support with failover.
- Observability/tracing for LLM calls (LangFuse or similar).
- Asset lifecycle (generate, store, retrieve, update, bundle, upload) with session persistence.
- Content safety (input filtering, output guards).

### Extensibility (Future)
- AI-powered translations automation.
- Image data extraction into form fields.
- Voice capture and transcript mapping.
- New LLM provider integration without code restructuring.

---

## Approach: Fix avni-ai-platform + Migrate

### What avni-ai-platform already provides
- Chat with SSE streaming + PostgreSQL conversation history
- Intent routing (keyword + LLM, 7 intent types)
- RAG with pgvector embeddings
- Bundle generation (handles concepts, forms, rules, groups, privileges)
- LLM Reasoner for field enrichment (60+ deterministic rules + LLM fallback)
- Skip logic generator
- Human-in-the-loop via `POST /chat/confirm` (no framework limitations)
- Multi-provider LLM client (Ollama, Groq, Cerebras, Gemini, OpenAI, Anthropic)
- React frontend with chat, bundle review, spreadsheet editor
- Content filtering and output guards
- 438 tests

### What to port from avni-ai
- LLM extraction prompt approach (replaces deterministic parser as primary path)
- Typed contract models matching avni-server (`SubjectTypeContract`, `ProgramContract`, `EncounterTypeContract`, `AddressLevelTypeContract`, `FormMappingContract`)
- Ambiguity checker logic
- UUID v4 generation (replace their arbitrary UUID v5)
- MongoDB asset store for bundle session persistence
- Direct bundle upload to avni-server (`bundle_uploader.py`)
- Dify knowledge base content → avni-ai-platform's RAG knowledge base

### What to fix in avni-ai-platform
- Wire `server_contract_validator` into bundle generation pipeline
- Move `_pending_actions` and other in-memory state to PostgreSQL
- Fix intent router keyword threshold (misroutes knowledge questions)
- Resolve `__SELF_PREV__` marker in skip logic generation
- Add error feedback for silent LLM enrichment failures
- Add error feedback for silently skipped parser sheets
- Add LangFuse (open-source, self-hosted) for LLM call tracing and observability — instrument existing `claude_client.py` calls without introducing LangChain

### What to deprecate
- Dify entirely (all flows migrated to avni-ai-platform)
- avni-ai as a standalone service (bundle logic merged into avni-ai-platform)
- avni-skills `generate_bundle_v2.js` (superseded by avni-ai-platform's generator)
