# Avni AutoSetup Training Curriculum

---

# PHASE 1: Rule Generation (Weeks 1-10)

---

### Week 1: Onboarding & Foundation

| Day | Activity | Duration | Expected Output |
|-----|----------|----------|-----------------|
| 1-2 | **Avni Platform Introduction** | 8 hrs | Interns can navigate Avni web app, understand subject types, programs, encounters |
| 2-3 | **Codebase Walkthrough** | 8 hrs | Understand `src/` structure, MCP server, Dify workflows, tool registry |
| 3-4 | **Development Environment Setup** | 4 hrs | Local server running, can execute `uv run pytest` |
| 4-5 | **LLM/AI Fundamentals** | 8 hrs | Understand prompt engineering, function calling, RAG concepts |
| 5 | **First PR: Documentation Fix** | 4 hrs | Merged PR to README or inline comments |

**Deliverables:**
- [ ] Each intern has working local environment
- [ ] Each intern completes Avni trial org setup manually
- [ ] Written summary of codebase architecture (1 page each)

---

### Week 2: Deep Dive - Existing Rule Generation & Avni Rules

| Day | Activity | Duration | Expected Output |
|-----|----------|----------|-----------------|
| 1-2 | **Study existing rule generation** | 8 hrs | Document current visit scheduling rule capabilities |
| 2-3 | **Analyze Dify workflows** | 6 hrs | Map `assistant_prompt.md` and `orchestrator_prompt.md` flow |
| 3-4 | **Study Avni rules documentation** | 6 hrs | Understand JavaScript rule structure in Avni |
| 4-5 | **Identify rule patterns** | 8 hrs | Catalog 10+ common rule patterns from existing implementations |
| 5 | **Present findings** | 4 hrs | Presentation to mentor on gaps and opportunities |

**Deliverables:**
- [ ] Rule pattern catalog document
- [ ] Gap analysis: current vs. needed rule types
- [ ] Proposed rule expansion roadmap

---

### Week 3-4: Enhanced Visit Scheduling Rules

| Week | Focus | Expected Output |
|------|-------|----------------|
| 3 | **Complex scheduling patterns** | Multi-condition scheduling, recurring visits, conditional scheduling |
| 3 | **Edge cases & error handling** | Handle missing data, invalid dates, conflicting schedules |
| 4 | **Testing & validation** | 10+ test cases for scheduling scenarios |
| 4 | **Deploy to staging** | Scheduling rules working on staging environment |

**Deliverables:**
- [ ] Enhanced `src/tools/rules/visit_scheduling.py`
- [ ] Support for complex multi-condition schedules
- [ ] Deployed and tested on staging

---

### Week 5-6: Decision Rules

| Week | Focus | Expected Output |
|------|-------|----------------|
| 5 | **Decision rule requirements** | Document 5+ decision rule use cases (risk classification, recommendations) |
| 5 | **Design decision rule prompt** | Prompt template for LLM to generate decision rules |
| 6 | **Implement decision rule tool** | New tool in `src/tools/rules/` for decision rule generation |
| 6 | **Testing & integration** | Unit tests, Dify workflow integration |

**Deliverables:**
- [ ] `src/tools/rules/decision_rules.py` implemented
- [ ] Decision rules for: risk classification, recommendations, alerts
- [ ] 5+ test cases, deployed to staging

---

### Week 7-8: Eligibility Rules (Program & Encounter)

| Week | Focus | Expected Output |
|------|-------|----------------|
| 7 | **Program eligibility rules** | Rules determining if subject can enroll in a program |
| 7 | **Encounter eligibility rules** | Rules determining if encounter can be performed |
| 8 | **Complex eligibility conditions** | Multi-field, cross-entity eligibility checks |
| 8 | **Testing & integration** | Unit tests, Dify workflow integration |

**Deliverables:**
- [ ] `src/tools/rules/eligibility_rules.py` implemented
- [ ] Program eligibility and encounter eligibility supported
- [ ] 5+ test cases, deployed to staging

---

### Week 9: Edit Rules

| Day | Activity | Duration | Expected Output |
|-----|----------|----------|-----------------|
| 1-2 | **Edit rule requirements** | 8 hrs | Document when/how data edits should be restricted |
| 2-3 | **Design edit rule prompt** | 8 hrs | Prompt template for edit rule generation |
| 3-4 | **Implement edit rule tool** | 10 hrs | New tool for edit rule generation |
| 4-5 | **Testing & integration** | 6 hrs | Unit tests, Dify workflow integration |

**Deliverables:**
- [ ] `src/tools/rules/edit_rules.py` implemented
- [ ] Edit restrictions based on time, status, role
- [ ] 5+ test cases, deployed to staging

---

### Week 10: Phase 1 Consolidation & Pilot

| Day | Activity | Duration | Expected Output |
|-----|----------|----------|-----------------|
| 1-2 | **Consolidate all rule types** | 8 hrs | Unified rule generation interface |
| 2-3 | **Pilot with Launchpad 2 member** | 8 hrs | Real user test of rule generation |
| 3-4 | **Bug fixes from pilot** | 8 hrs | Address issues found in pilot |
| 4-5 | **Documentation & demo** | 6 hrs | Technical docs, demo to stakeholders |
| 5 | **Phase 1 retrospective** | 2 hrs | Lessons learned, Phase 2 prep |

**Deliverables:**
- [ ] All 5 rule types working: Visit Scheduling, Decision, Eligibility (Program + Encounter), Edit
- [ ] Pilot completed with Launchpad 2 member
- [ ] Phase 1 completion report

---

# PHASE 2: Form Creation (Weeks 11-20)

---

### Week 11: Form Creation Foundation

| Day | Activity | Duration | Expected Output |
|-----|----------|----------|-----------------|
| 1-2 | **Study Avni form API** | 8 hrs | Document form creation API endpoints, form structure |
| 2-3 | **Define CSV/Excel schema** | 8 hrs | Standard format for form definition input |
| 3-4 | **Implement parser** | 8 hrs | Python module to parse CSV/Excel into structured data |
| 4-5 | **Map to Avni form schema** | 6 hrs | Transformation logic from input to Avni JSON |
| 5 | **Unit tests** | 2 hrs | Test parsing with sample files |

**Deliverables:**
- [ ] CSV/Excel schema specification document
- [ ] `src/services/form_parser.py` implemented
- [ ] 3+ sample input files for testing

---

### Week 12-13: Pages and Question Groups

| Week | Focus | Expected Output |
|------|-------|----------------|
| 12 | **Form page structure** | Create form pages/sections from input |
| 12 | **Question group handling** | Support for nested question groups |
| 13 | **Display order & layout** | Proper ordering of pages, groups, questions |
| 13 | **Testing & validation** | Unit tests for page/group generation |

**Deliverables:**
- [ ] Form pages creation working
- [ ] Question groups with proper nesting
- [ ] Display order correctly applied

---

### Week 14-15: Question Generation

| Week | Focus | Expected Output |
|------|-------|----------------|
| 14 | **Concept creation** | Auto-create concepts for new form fields |
| 14 | **Data type mapping** | Map input types to Avni concept dataTypes |
| 15 | **Coded answers** | Handle SingleSelect/MultiSelect with answer options |
| 15 | **Special field types** | Location, Subject, Duration, PhoneNumber, etc. |

**Deliverables:**
- [ ] `src/tools/app_designer/forms.py` implemented
- [ ] All Avni data types supported
- [ ] Concept creation integrated

---

### Week 16: Form API Integration

| Day | Activity | Duration | Expected Output |
|-----|----------|----------|-----------------|
| 1-2 | **Form creation API calls** | 8 hrs | Implement Avni API calls for form creation |
| 2-3 | **Error handling & validation** | 8 hrs | Robust error handling, validation before API calls |
| 3-4 | **Update config processor** | 8 hrs | Extend `config_processor.py` for form operations |
| 4-5 | **Dify workflow integration** | 6 hrs | Add form creation to assistant workflow |
| 5 | **Testing on staging** | 2 hrs | Test form creation on staging environment |

**Deliverables:**
- [ ] Form creation working end-to-end
- [ ] Forms created via input visible in Avni App Designer
- [ ] Error messages clear and actionable

---

### Week 17: Complete Form Creation

| Day | Activity | Duration | Expected Output |
|-----|----------|----------|-----------------|
| 1-2 | **Handle edge cases** | 8 hrs | Empty rows, special characters, duplicate names |
| 2-3 | **Form update capability** | 8 hrs | Update existing forms, not just create |
| 3-4 | **Multi-form support** | 8 hrs | Create multiple forms from single input file |
| 4-5 | **User feedback integration** | 6 hrs | Clear progress messages during form creation |
| 5 | **Testing** | 2 hrs | Comprehensive edge case testing |

**Deliverables:**
- [ ] Edge cases handled gracefully
- [ ] Form update capability
- [ ] Multi-form creation supported

---

### Week 18: Polish & Documentation

| Day | Activity | Duration | Expected Output |
|-----|----------|----------|-----------------|
| 1-2 | **Form creation polish** | 8 hrs | Refine form creation workflow, improve UX |
| 2-3 | **Documentation** | 8 hrs | Technical docs, API docs, user guide |
| 3-4 | **Testing & validation** | 8 hrs | Comprehensive testing of form creation |
| 4-5 | **Prepare for pilot** | 6 hrs | Sample forms, pilot materials ready |
| 5 | **Internal demo** | 2 hrs | Demo form creation capabilities |

---

### Week 19: Pilot with Launchpad 2 & 3

| Day | Activity | Duration | Expected Output |
|-----|----------|----------|-----------------|
| 1-2 | **Pilot with Launchpad 2 member** | 8 hrs | Real user test, collect feedback |
| 2-3 | **Bug fixes from pilot 1** | 8 hrs | Address issues found |
| 3-4 | **Pilot with Launchpad 3 member** | 8 hrs | Second user test |
| 4-5 | **Feedback consolidation** | 8 hrs | Document all feedback, prioritize fixes |
| 5 | **Testing** | 2 hrs | Validate fixes from pilot feedback |

**Deliverables:**
- [ ] 2 pilot sessions completed (Launchpad 2 + 3)
- [ ] Feedback log with prioritized issues

---

### Week 20: Finalization & Handover

| Day | Activity | Duration | Expected Output |
|-----|----------|----------|-----------------|
| 1-2 | **Critical bug fixes** | 8 hrs | Fix high-priority issues from pilots |
| 2-3 | **Final documentation** | 8 hrs | Complete documentation package |
| 3-4 | **Judge framework tests** | 8 hrs | Add test cases for form creation |
| 4-5 | **Final demo & presentation** | 6 hrs | Demo to stakeholders, present results |
| 5 | **Retrospective & handover** | 2 hrs | Lessons learned, future roadmap |

**Deliverables:**
- [ ] All critical bugs fixed
- [ ] Complete documentation package
- [ ] Final presentation deck
- [ ] Retrospective document
