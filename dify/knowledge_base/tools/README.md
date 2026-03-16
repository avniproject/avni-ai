# Avni AI Assistant Knowledge Base - Optimization Tools

This directory contains tools for maintaining and optimizing the Avni AI Assistant knowledge base for LLM embeddings and RAG (Retrieval-Augmented Generation).

## Tools Overview

### 1. validate_metadata.py

Validates that all markdown files have proper YAML frontmatter with required fields.

**Usage:**
```bash
python validate_metadata.py ../AI_ASSISTANT_KNOWLEDGE_BASE
```

**What it checks:**
- Presence of YAML frontmatter
- Required fields (title, category, audience, difficulty, priority, keywords, last_updated)
- Valid values for priority, difficulty, and audience
- Keywords is a non-empty list

**Output:**
- ✅ Valid files
- ❌ Invalid files with specific error messages
- ⚠️ Files without metadata

**Exit codes:**
- 0: All files valid
- 1: Some files invalid or missing metadata

---

### 2. analyze_chunks.py

Analyzes chunk sizes in markdown files to ensure optimal embedding quality.

**Usage:**
```bash
python analyze_chunks.py ../AI_ASSISTANT_KNOWLEDGE_BASE
```

**What it checks:**
- Presence of chunk markers (`<!-- CHUNK: id -->` ... `<!-- END CHUNK -->`)
- Word count per chunk (target: 200-600 words)
- Chunk size distribution

**Output:**
- ✅ Good size (200-600 words)
- ⚠️ Too short (<200 words)
- ⚠️ Too long (>600 words)
- Quality score (% of chunks in optimal range)

**Recommendations:**
- Target: 300-500 words per chunk
- Each chunk should contain one complete concept
- Add context so chunks are self-contained

---

### 3. METADATA_TEMPLATE.md

Complete template for creating new knowledge base files with proper metadata and structure.

**What it includes:**
- Full YAML frontmatter schema with all fields
- Chunk structure examples
- Content organization patterns
- Writing guidelines for authors

**How to use:**
1. Copy template to new file
2. Fill in metadata fields
3. Replace placeholder content
4. Add chunk markers
5. Validate with `validate_metadata.py`

---

## LLM Optimization Guidelines

### Metadata Best Practices

**Required Fields:**
- `title`: Descriptive, context-rich title
- `category`: Directory name (getting-started, core-concepts, etc.)
- `audience`: implementer (primary), admin, developer, all
- `difficulty`: beginner, intermediate, advanced
- `priority`: critical, high, medium, low
- `keywords`: Array of search terms (minimum 3)
- `last_updated`: YYYY-MM-DD format

**Priority Levels:**
- **Critical (boost: 2.0x)**: Core concepts, essential for any implementation
- **High (boost: 1.5x)**: Common tasks, frequently used features
- **Medium (boost: 1.0x)**: Advanced features, less common scenarios
- **Low (boost: 0.5x)**: Reference information, rarely used

**Semantic Tags:**
- `task_types`: configuration, troubleshooting, reference, tutorial, example, best-practice
- `features`: forms, rules, subjects, programs, encounters, locations, users, dashboards
- `technical_level`: conceptual, procedural, reference, troubleshooting
- `implementation_phase`: planning, setup, development, testing, deployment, maintenance
- `complexity`: simple, moderate, complex

### Chunking Strategy

**Optimal chunk size:** 300-500 words
- **Minimum:** 200 words (or embedding loses context)
- **Maximum:** 600 words (or embedding dilutes relevance)

**Chunk naming:**
- Use descriptive IDs: `overview`, `step-by-step-guide`, `code-example`
- Include topic: `faq-how-to-add-field`, `antipattern-skip-logic`
- Not generic: `section1`, `part2`, `content`

**Chunk boundaries:**
- One complete concept per chunk
- Self-contained (readable in isolation)
- Include necessary context
- Clear semantic boundaries

### Content Structure

**Every file should have:**
1. **TL;DR chunk** - 2-3 sentence summary
2. **Overview chunk** - What, when to use, prerequisites
3. **Main content chunks** - Organized by topic
4. **FAQ chunk** - Common questions (if applicable)
5. **Related topics chunk** - Cross-references

**Heading guidelines:**
- Context-rich: "Configuring Skip Logic for Conditional Form Fields"
- Not generic: "Configuration"
- Include key search terms
- Self-contained meaning

### RAG Optimization

**Query patterns:**
Add common questions users ask:
```yaml
query_patterns:
  - "how to schedule visits"
  - "visit not appearing"
  - "schedule next visit after enrollment"
```

**Answer types:**
Classify what kind of answers provided:
```yaml
answer_types:
  - how-to
  - troubleshooting
  - reference
  - explanation
```

**Retrieval strategy:**
Define which chunks for different query depths:
```yaml
retrieval_strategy:
  quick_answer_chunks: [tldr, faq-main-question]
  detailed_chunks: [overview, step-by-step-guide, code-example]
  comprehensive_chunks: [all]
```

---

## Workflow for New Content

### 1. Create File from Template

```bash
cp tools/METADATA_TEMPLATE.md new-topic.md
```

### 2. Fill in Metadata

- Complete all required fields
- Add relevant optional fields
- Set appropriate priority and boost
- Add semantic tags

### 3. Write Content

- Follow structure template
- Add chunk markers
- Use context-rich headings
- Include examples and anti-patterns
- Add Q&A sections

### 4. Validate

```bash
# Check metadata
python tools/validate_metadata.py .

# Check chunk sizes
python tools/analyze_chunks.py .
```

### 5. Refine

- Adjust chunk sizes if needed
- Add missing metadata
- Improve headings
- Add cross-references

---

## Maintenance Tasks

### Weekly
- [ ] Validate metadata on new files
- [ ] Check chunk sizes on new content
- [ ] Update `last_updated` dates on modified files

### Monthly
- [ ] Review retrieval analytics
- [ ] Update priority scores based on usage
- [ ] Add new query patterns to metadata
- [ ] Refine chunk boundaries if needed

### Quarterly
- [ ] Re-evaluate embedding model
- [ ] Benchmark retrieval quality
- [ ] Update semantic tags
- [ ] Refresh related_topics links

### Annual
- [ ] Complete metadata audit
- [ ] Restructure if needed
- [ ] Version bump for major changes

---

## Quality Metrics

### Target Metrics

**Retrieval Quality:**
- Precision@5: >80%
- Recall@10: >90%
- MRR (Mean Reciprocal Rank): >0.7
- NDCG: >0.8

**Content Quality:**
- Metadata completeness: 100%
- Chunks in optimal range: >80%
- Files with chunk markers: >90%

**Maintenance:**
- Files updated in last 6 months: >50%
- Broken links: 0
- Duplicate content: <5%

---

## Troubleshooting

### Validation fails with "Missing frontmatter"

**Solution:** Add YAML frontmatter at the start of file:
```yaml
---
title: "Your Title"
category: "category-name"
# ... other fields
---
```

### Chunk size warnings

**Too short (<200 words):**
- Combine with related chunks
- Add more context and examples
- Expand explanations

**Too long (>600 words):**
- Split into multiple chunks
- Each chunk should cover one concept
- Use clear semantic boundaries

### Metadata validation errors

**Invalid priority/difficulty/audience:**
- Check spelling and case
- Use only allowed values
- See METADATA_TEMPLATE.md for valid options

---

## Examples

### Good Metadata Example

```yaml
---
title: "Visit Schedule Rules - Complete Guide"
category: "javascript-rules"
subcategory: "visit-schedule-rules"
audience: "implementer"
difficulty: "intermediate"
priority: "high"
keywords:
  - visit schedule
  - program encounter
  - scheduling logic
  - earliest visit date
task_types:
  - configuration
  - tutorial
  - example
features:
  - rules
  - programs
  - encounters
technical_level:
  - procedural
  - reference
implementation_phase:
  - development
  - testing
complexity: "moderate"
query_patterns:
  - "how to schedule visits"
  - "visit not appearing"
retrieval_boost: 1.5
related_topics:
  - ../javascript-rules/helper-functions.md
  - ../troubleshooting/visit-scheduling-issues.md
last_updated: "2026-03-16"
version: "1.0"
---
```

### Good Chunk Example

```markdown
<!-- CHUNK: validation-rule-age-range -->
## Validation Rule: Age Range Check

**Context:** JavaScript validation rule for Avni forms to ensure age is within acceptable range.

**Use case:** Maternal health programs where age must be 15-49 years.

**Code:**
```javascript
const ValidationRules = {
  'ageRange': function(individual, form) {
    const age = individual.getAgeInYears();
    if (age < 15 || age > 49) {
      return ValidationResult.failure(
        'age',
        'Age must be between 15 and 49 years'
      );
    }
    return ValidationResult.success();
  }
};
```

**When to use:** Any program with age restrictions.

<!-- END CHUNK -->
```

---

## Support

For questions or issues with these tools:
1. Check this README
2. Review METADATA_TEMPLATE.md
3. Ask the AI Assistant
4. Contact the knowledge base maintainer

---

**Last Updated:** 2026-03-16
**Version:** 1.0
