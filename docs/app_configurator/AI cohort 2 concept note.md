**1\.  Problem Statement**

**Last year around 40-50% of Avni's incoming revenue came from SaaS subscriptions. To grow this share and reach more NGOs — especially those with smaller budgets — Avni needs to reduce the cost of client onboarding and app configuration. The process today is manual, time-intensive, and dependent on skilled team members, making it difficult to scale.**

**2\.  Current Process & Pain Points**

**2.1  End-to-end current workflow**

| How it works today Step 1 — Requirement gathering:  Delivery Manager (DM) collects requirements from client calls, Excel sheets, and PDFs. Step 2 — Specification:  DM maps requirements to Avni domain model and produces Scoping, Forms & Modelling documents.  (1.5 – 2 days) Step 3 — Estimation & contract:  Mapped documents used to estimate cost with the implementation team; contract signed. Step 4 — App configuration:  Implementation team configures app; clarifies requirements with client as needed. Step 5 — UAT:  Client tests app, shares feedback; engineer incorporates changes within scope. Step 6 — Go live:  Field-user training begins; app used on the ground. |
| :---- |

**2.2  Pain points**

* Manual work of filling forms and the modelling document — time-consuming and error-prone.  
* Too many form fields to be filled in specification document with self-evident answers. Example: 'Number of children delivered' cannot be negative or a decimal — yet must be explicitly specified today.  
* Currently AI aided generation of forms is dependent on a team member since it requires setup and not integrated with Avni product. Post generation corrections are to be made to make it work as expected.  
* AI aided rule generation is not reliable.

**3\.  Proposed Solution**

**Two-phase implementation plan**

| Phase | What it delivers | Estimated Timelines |
| :---- | :---- | :---- |
| **Phase 1** | Scoping, Forms & Modelling documents  →   (AI assistance in Avni web app)  \-\> Avni app Automate app configuration from structured specification documents. | March end |
| **Phase 2** | Raw requirements (PDFs / Excels / call notes)  →  (AI assistance in Avni web app) \-\> Scoping, Forms & Modelling documents Automate mapping of unstructured inputs to Avni domain model and structured spec. | April end |

**Once both phases are complete, the feature will serve two distinct user types:**

| User Persona | Org Category | Behaviour / Flow | Notes |
| :---- | :---- | :---- | :---- |
| **Internal team / users with Avni domain knowledge** | UAT & Self-service org | Upload requirements (spreadsheet, PDF, plain text)  →  Review Specifications sheet  →  Download Avni app to try out with username and password | Specifications sheet shared with user to finalise scope and sign contract with client |
| **Users without Avni domain knowledge** | Trial org | Upload requirements (spreadsheet, PDF, plain text)  →  Directions to download Avni app to try out with username and password | Specification sheet generated internally; not shared with user |

**4\.  Success Measurement**

**Before vs. after targets**

| Task | Current State | Target State | Scope Note |
| :---- | :---- | :---- | :---- |
| **Requirements → Specification documents** | 1.5 – 2 days | \~0.5 day | Calls still needed; AI automates document creation |
| **Specification documents → Avni app** | 100% of current effort | 30% reduction in effort | Field visit, report cards (DB migration in progress) and PM work are out of scope for this reduction |

**5\.  Solution Design**

In addition to above we would like to explore AI solutions for requirements raised from clients like extraction of data from image and filling it.

### Solution Design (Technical)

---

#### 5.1  User Experience Flow

The user interacts with a **conversational chat interface inside Avni Webapp**. The flow differs by phase:

**Phase 1 — Structured spec → Avni app:**
1. User uploads a structured specification spreadsheet (Excel/CSV) in the chat
2. AI acknowledges receipt, parses the file, and shows a summary: *"Found 2 subject types, 3 programs, 14 encounter types, 18 forms…"*
3. AI generates the full app configuration and applies it to the user's organisation
4. User is told to sync their mobile app or browse App Designer to see the result
5. User can ask follow-up corrections in chat: *"Rename program X to Y"*, *"Add a field 'Blood Group' to ANC form"* — AI updates and re-applies

**Phase 2 — Unstructured requirements → Structured spec → Avni app:**
1. User uploads raw requirements (PDFs, call notes, free-text Excel)
2. AI uses an LLM to interpret requirements, asks clarifying questions, and produces a structured specification spreadsheet
3. For internal users: the generated spec is shown for review/edit before applying
4. For trial org users: spec is applied directly; user gets app to try out

---

#### 5.2  High-Level Architecture

```
┌──────────────────────────────────────────────────────┐
│                   Avni Webapp (React)                │
│         Chat UI with file upload + text input        │
└──────────────────┬───────────────────────────────────┘
                   │  chat message + file
                   ▼
┌──────────────────────────────────────────────────────┐
│              Dify Orchestrator (Advanced Chat)       │
│                                                      │
│  ┌─────────────┐  ┌──────────────┐  ┌────────────┐   │
│  │ Intent      │  │ RAG /        │  │ FILE_SETUP │   │
│  │ Classifier  │→ │ Assistant    │  │ Router     │   │
│  │ (LLM)       │  │ (LLM + KB)   │  │            │   │
│  └─────────────┘  └──────────────┘  └─────┬──────┘   │
└───────────────────────────────────────────┼──────────┘
                                            │  HTTP tool call
                                            ▼
┌─────────────────────────────────────────────────────┐
│              avni-ai Service (Python/FastAPI)       │
│                                                     │
│  ┌────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │ Spec       │  │ Bundle       │  │ Asset        │ │
│  │ Parser     │→ │ Generator    │→ │ Store        │ │
│  │            │  │              │  │              │ │
│  └────────────┘  └──────────────┘  └──────┬───────┘ │
│                                           │         │
│  ┌────────────┐  ┌──────────────┐         │         │
│  │ LLM        │  │ Bundle       │ ←───────┘         │
│  │ Reasoner   │  │ Uploader     │                   │
│  │ (OpenAI)   │  │              │                   │
│  └────────────┘  └──────┬───────┘                   │
└─────────────────────────┼───────────────────────────┘
                          │  Metadata ZIP upload
                          ▼
┌──────────────────────────────────────────────────────┐
│              avni-server (Spring Boot)               │
│         Existing bulk import endpoint                │
│         UUID-based upsert (create or update)         │
└──────────────────────────────────────────────────────┘
```

---

#### 5.3  Where AI / LLM Is Used vs. Where It Isn't

A key design choice is **separating deterministic work from AI-driven work**. Not everything needs an LLM — structured spec parsing is rule-based, while interpretation and correction require intelligence.

| Step | AI / LLM? | Rationale |
|------|-----------|-----------|
| **Intent classification** (file upload vs. question vs. config change) | Yes — LLM | Natural language understanding needed |
| **Spec parsing** (reading Excel columns, extracting field names/types) | No — deterministic | Columns A–Q have fixed semantics; rule-based parser is reliable and fast |
| **Inferring missing properties** (e.g. "Number of children" → cannot be negative, cannot be decimal) | Yes — LLM | Domain reasoning about field semantics; reduces spec burden on user |
| **Bundle JSON generation** (producing config files) | No — deterministic | Exact JSON schemas required; template-based generation is reliable |
| **Validation & gap detection** (missing cancellation forms, incomplete mappings) | No — deterministic | Known rules about what a complete bundle looks like |
| **Visit schedule rule generation** | Hybrid | Pattern matching for common frequencies (deterministic); LLM for ambiguous specs |
| **Skip logic / conditional display rules** | Hybrid | Simple conditions are parsed deterministically from column Q; complex natural-language conditions use LLM |
| **Unstructured requirement → structured spec** (Phase 2) | Yes — LLM | Core AI value: interpreting PDFs, call notes, free-text into Avni domain model |
| **Conversational corrections** ("rename X to Y", "add field Z") | Yes — LLM | Natural language understanding + tool calling to update assets |

---

#### 5.4  AI Pipeline Detail

**Phase 1 pipeline (structured spec → app):**

```
Upload Excel/CSV
       │
       ▼
  ┌─────────────────┐
  │  Spec Parser    │  ← Deterministic: openpyxl reads sheets,
  │  (rule-based)   │    maps columns to structured data
  └────────┬────────┘
           │ parsed entities, fields, options, conditions
           ▼
  ┌─────────────────┐
  │  LLM Reasoner   │  ← AI: infers missing properties
  │  (OpenAI)       │    (negative/decimal/future-date flags,
  │                 │     normal ranges, field grouping hints)
  └────────┬────────┘
           │ enriched spec
           ▼
  ┌─────────────────┐
  │  Bundle         │  ← Deterministic: generates JSON config
  │  Generator      │    files with stable UUIDs, validation
  └────────┬────────┘
           │ JSON assets
           ▼
  ┌─────────────────┐
  │  Asset Store    │  ← Persist, version, allow updates
  └────────┬────────┘
           │
           ▼
  ┌─────────────────┐
  │  Bundle Uploader│  ← ZIP + upload to avni-server
  └─────────────────┘
```

The **LLM Reasoner** step is critical — it addresses the pain point that *"too many form fields have self-evident answers."* For example, given a field named "Number of children delivered" with data type "Numeric", the LLM infers:
- `allowNegativeValue: false` (count cannot be negative)
- `allowDecimalValue: false` (count must be integer)
- `lowAbsolute: 0, highAbsolute: 15` (reasonable range)

This eliminates ~40% of manual spec-filling work.

**Phase 2 pipeline (unstructured → structured spec → app):**

```
Upload PDF / Excel / plain text
       │
       ▼
  ┌─────────────────┐
  │  Document       │  ← AI: extracts text from PDFs,
  │  Extractor      │    tables from Excel, structures
  │  (LLM + tools)  │    free-text into sections
  └────────┬────────┘
           │ raw extracted content
           ▼
  ┌─────────────────┐
  │  Domain Mapper  │  ← AI: maps requirements to Avni
  │  (LLM + RAG)    │    domain model (subject types,
  │                 │    programs, forms, fields) using
  │                 │    Avni knowledge base as context
  └────────┬────────┘
           │ draft structured spec
           ▼
  ┌─────────────────┐
  │  Clarification  │  ← AI: asks user targeted questions
  │  Dialog (LLM)   │    for ambiguous requirements
  └────────┬────────┘
           │ finalised spec
           ▼
     Phase 1 pipeline (above)
```

---

#### 5.5  Asset Lifecycle

Every generated config file is an **asset** — stored, retrievable, updatable, and re-uploadable. This enables iterative refinement without starting from scratch.

```
  Upload spec  ──→  Generate assets  ──→  Store  ──→  Upload to server
       ↑                                    │  ↑
       │              ┌─────────────────────┘  │
       │              ▼                        │
       └──── User correction via chat  ──→  Update asset
```

**Asset operations:**

| Operation | Description |
|-----------|-------------|
| **Generate** | Parse spec → produce JSON config files |
| **Store** | Persist per organisation/session on filesystem |
| **Retrieve** | Read back for inspection or LLM context |
| **Update** | Modify specific assets (via chat correction or re-parse) |
| **Bundle** | Assemble all assets into a Metadata ZIP |
| **Upload** | Push ZIP to avni-server (full bundle or incremental) |

Deterministic UUIDs (based on entity names) ensure **idempotent re-uploads** — the same spec always produces the same UUIDs, so re-uploading updates entities rather than duplicating them.

---

#### 5.6  Phased Delivery (aligned to stories)

Each phase builds on the assets produced by the previous one:

| Phase | Story | What it does | AI involvement |
|-------|-------|-------------|----------------|
| **1** | #1706 | **Entities from spec** — parse Modelling sheet, generate subject types, programs, encounter types, address level types; upload to server | Spec parsing is deterministic; LLM infers program eligibility rules |
| **2** | #1704 | **Forms & concepts from spec** — parse form sheets (columns A–Q), generate deduplicated concepts + form structures + form mappings; upload | Deterministic parsing + LLM infers missing field properties (negative/decimal/range) |
| **3** | #1705 | **Visit schedule rules** — parse frequency column, generate scheduling rules on forms; update assets and re-upload | Pattern matching + LLM for ambiguous schedule descriptions |
| **4** | #1707 | **Conditional display rules** — parse "when to show" column, generate skip logic; update form assets and re-upload | Deterministic for simple conditions; LLM for natural-language conditions |

Each phase produces incremental assets that are added to the store. At any point, a full bundle can be assembled and uploaded.

---

#### 5.7  Key Design Decisions

| Decision | Rationale |
|----------|-----------|
| **Bundle upload, not individual API calls** | Avni-server's Metadata ZIP import is the production-proven path; handles ordering, upsert, and validation internally |
| **Deterministic generation + LLM enrichment** (not pure LLM generation) | Config JSON requires exact schemas — LLM hallucinations in JSON structure would cause upload failures; LLM adds value in reasoning about field semantics |
| **Python port of srs-bundle-generator** (not Node.js subprocess) | Single runtime, easier debugging, same deployment unit as avni-ai service |
| **Asset store with session persistence** | Enables iterative refinement; user can correct via chat without regenerating everything |
| **Dify as orchestration layer** | Reuses existing chat infrastructure; intent routing separates file-setup from Q&A flows |

---

#### 5.8  System Components Summary

```
avni-ai service (new modules):
  ├── Spec Parser          — reads Excel/CSV, extracts structured data
  ├── LLM Reasoner         — infers missing field properties, interprets ambiguous specs
  ├── Bundle Generator      — produces Avni config JSON files (deterministic)
  ├── Asset Store           — persists/retrieves/updates generated configs
  ├── Bundle Uploader       — assembles ZIP, uploads to avni-server
  └── UUID Registry         — standard UUIDs + deterministic generation for stability

Dify (modified):
  ├── Intent classifier     — routes file uploads to FILE_SETUP path
  └── FILE_SETUP workflow   — orchestrates parse → generate → upload cycle

Avni Webapp (modified):
  └── Chat UI               — file upload enabled (.xlsx, .csv, .pdf)
```