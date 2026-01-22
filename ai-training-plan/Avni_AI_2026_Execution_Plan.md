# Avni AutoSetup With AI in 2026 Execution Plan

## Program Overview

| Attribute | Details |
|-----------|---------|
| **Duration** | 5 months (January - May 2026) |
| **Team** | 1 Senior Developer (Mentor) + 2 Junior Developers (Full-time Interns) |
| **Primary Goal** | Expand rule generation coverage → Enable form creation from CSV |
| **Success Metric** | Percentage of setup done correctly (target: ≥75% accuracy on pilot configurations) |
| **Pilot Group** | Avni Launchpad "2" and "3" cohort members |
| **Validation Method** | Manual review by mentor and pilot users |

---

## Strategic Approach

### Progression Path
Phase 1: Rule Generation     |  Phase 2: Form Creation    
-----------------------------|-----------------------------
Enhance visit scheduling     |  CSV/Spreadsheet parsing   
Add Decision Rules           |  Forms,Pages generation   
Add Form Element Rules       |  Questions and Concepts generation    

### Current Baseline
- ✅ RAG-based chat assistant with Avni documentation
- ✅ Configuration creation (addressLevelTypes, locations, catchments, subjectTypes, programs, encounterTypes)
- ✅ Form element validation (Basic, needs to evolve to cover Pages and whole form context)
- ✅ Mid-complexity visit scheduling rule generation
- ❌ Complex rule generation (Questions skip logic, validation rules, decision rules, Eligibility and Edit-Rules)
- ❌ Form creation from structured input

---

## Training Curriculum

See [Training Curriculum](docs/training_curriculum.md) for detailed weekly breakdown of Phase 1 (Rule Generation) and Phase 2 (Form Creation).

---

## Technical Milestones

See [Technical Milestones & Success Criteria](docs/technical_milestones.md) for detailed milestone definitions and success metrics.

---

## Resource Requirements

### Technical Resources
- Staging environment access (`staging.avniproject.org`)
- OpenAI API key (existing)
- Dify workflow access
- GitHub repository access

### Documentation Resources
- Avni documentation (existing knowledge base)
- Sample forms from existing implementations
- Launchpad 2 & 3 member contacts for pilot coordination

### Time Allocation
- **Mentor:** ~10 hrs/week (code review, guidance, unblocking)
- **Interns:** 40 hrs/week each (full-time)

---

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Phase 2 dependency on Phase 1 | High | High | Ensure Phase 1 rule tools are stable before Week 16 integration |
| Avni Form API complexity | Medium | High | Early API exploration in Week 11, mentor support |
| LLM output inconsistency | High | Medium | Robust validation, fallback to templates, judge framework tests |
| Intern learning curve | Medium | Medium | Structured curriculum, pair programming, weekly checkpoints |
| Scope creep | Medium | High | Strict milestone gates at Week 4, 8, 10, 15, 18, 20 |
| Staging environment issues | Low | Medium | Early access verification in Week 1, backup test approach |
| Pilot user availability | Medium | Medium | Coordinate with Launchpad 2 & 3 early, have backup pilot users |
| Rule complexity exceeds LLM capability | Medium | High | Start with simpler rules, escalate complex cases to manual |

---

## Weekly Mentor Checkpoints

### Phase 1: Rule Generation (Weeks 1-10)

| Week | Checkpoint Focus |
|------|------------------|
| 1-2 | Environment setup verified, codebase understanding confirmed, Avni learning, Prompt engineering, Dify ramp up |
| 3 | Rule pattern catalog reviewed, gap analysis approved |
| 4 | Visit scheduling enhancement - code review |
| 4 | **Milestone 1:** Enhanced visit scheduling deployed to staging |
| 5 | Decision rules - design review |
| 6 | Decision rules - code review, deployed to staging |
| 7 | Eligibility rules - design review |
| 8 | **Milestone 2:** Decision & eligibility rules deployed to staging |
| 9 | Edit rules - code review |
| 10 | **Phase 1 Gate:** All 5 rule types working, pilot completed, demo |

### Phase 2: Form Creation (Weeks 11-20)

| Week | Checkpoint Focus |
|------|------------------|
| 11 | Form API study complete, CSV/Excel schema approved |
| 12 | Page structure - code review |
| 13 | Question groups - code review |
| 14 | Concept creation - code review |
| 15 | **Milestone 4:** Form structure generation working |
| 16 | Form API integration tested on staging |
| 17 | **Milestone 5:** Complete form creation working |
| 18 | Polish & Edge Cases |
| 19 | Pilot feedback reviewed, bug priorities set |
| 20 | **Phase 2 Gate:** All deliverables complete, final demo |
---
