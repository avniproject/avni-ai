---
# METADATA TEMPLATE FOR AVNI AI ASSISTANT KNOWLEDGE BASE
# Copy this template to the top of each new markdown file
# Fill in all required fields and relevant optional fields

# ============================================================================
# REQUIRED FIELDS (Must be present in every file)
# ============================================================================

title: "[Descriptive Title - What this document covers]"
category: "[Directory name: getting-started, core-concepts, organization-setup, etc.]"
audience: "implementer"  # Options: implementer, admin, developer, all
difficulty: "beginner"   # Options: beginner, intermediate, advanced
priority: "high"         # Options: critical, high, medium, low
keywords:                # Array of search terms (minimum 3)
  - keyword1
  - keyword2
  - keyword3
last_updated: "2026-03-16"  # Format: YYYY-MM-DD

# ============================================================================
# OPTIONAL FIELDS (Add as relevant)
# ============================================================================

subcategory: "[Subdirectory or specific topic area]"

# Task classification
task_types:              # What kind of tasks does this help with?
  - configuration       # Setting up features
  - troubleshooting     # Solving problems
  - reference           # Looking up information
  - tutorial            # Learning step-by-step
  - example             # Seeing real implementations
  - best-practice       # Understanding recommended approaches

# Feature coverage
features:                # Which Avni features are covered?
  - forms
  - rules
  - subjects
  - programs
  - encounters
  - locations
  - users
  - dashboards
  - concepts

# Technical depth
technical_level:         # How is content presented?
  - conceptual          # High-level understanding
  - procedural          # Step-by-step how-to
  - reference           # Detailed specifications
  - troubleshooting     # Problem-solving

# Implementation phase
implementation_phase:    # When in the project lifecycle?
  - planning            # Before starting
  - setup               # Initial configuration
  - development         # Building implementation
  - testing             # Validation
  - deployment          # Going live
  - maintenance         # Ongoing support

# Complexity indicator
complexity: "moderate"   # Options: simple, moderate, complex

# Search optimization
query_patterns:          # Common questions this answers
  - "how to [action]"
  - "why is [problem]"
  - "[feature] not working"

answer_types:            # What kind of answers provided?
  - how-to
  - troubleshooting
  - reference
  - explanation
  - example

# Retrieval optimization
retrieval_boost: 1.0     # Boost factor: critical=2.0, high=1.5, medium=1.0, low=0.5

# Relationships
related_topics:          # Links to related documents (relative paths)
  - ../category/related-file.md
  - ./another-related-file.md

prerequisites:           # What should be read first?
  - ../category/prerequisite-file.md

# User experience
estimated_reading_time: "5 minutes"

# Version control
version: "1.0"

# Synonym mapping (for better semantic search)
synonyms:
  term1: [synonym1, synonym2, synonym3]
  term2: [synonym1, synonym2]

# Retrieval strategy
retrieval_strategy:
  quick_answer_chunks:   # Chunk IDs for quick answers
    - tldr
    - faq-main-question
  detailed_chunks:       # Chunk IDs for detailed explanations
    - overview
    - step-by-step-guide
    - code-example
  comprehensive_chunks:  # All chunks for full context
    - all

---

# [Document Title]

<!-- CHUNK: tldr -->
## TL;DR

[2-3 sentence summary of the entire document. What is this about? What will you learn? What can you do after reading?]

<!-- END CHUNK -->

<!-- CHUNK: overview -->
## Overview

**What:** [One-sentence description of what this document covers]

**When to use:** [Specific scenarios where this information is needed]

**Prerequisites:** [What you should know before reading this]

<!-- END CHUNK -->

<!-- CHUNK: key-concepts -->
## Key Concepts

### [Concept 1 Name]

**Definition:** [Clear, concise definition]

**Purpose:** [Why this concept exists and what problem it solves]

**Example:** [Concrete, relatable example]

### [Concept 2 Name]

[Same structure as above]

<!-- END CHUNK -->

<!-- CHUNK: step-by-step-guide -->
## Step-by-Step Guide

### Step 1: [Action to Take]

**Goal:** [What this step achieves]

**Instructions:**
1. [Specific action with details]
2. [Specific action with details]
3. [Specific action with details]

**Expected result:** [What you should see after completing this step]

**Troubleshooting:** [Common issues and quick fixes]

### Step 2: [Next Action]

[Same structure as above]

<!-- END CHUNK -->

<!-- CHUNK: code-example -->
## Code Example

**Scenario:** [What this example demonstrates]

```javascript
// [Well-commented code showing the concept in action]
function exampleFunction() {
  // Step 1: [What this does]
  const value = getValue();
  
  // Step 2: [What this does]
  return processValue(value);
}
```

**Explanation:**
- Line 1-2: [What these lines do]
- Line 3-4: [What these lines do]

**When to use:** [Situations where this pattern applies]

<!-- END CHUNK -->

<!-- CHUNK: faq-main-question -->
## FAQ: [Common Question]

**Q: [Exact question users ask]**

**A:** [Direct, actionable answer]

[Step-by-step if needed]

**Related:** [Links to detailed documentation]

<!-- END CHUNK -->

<!-- CHUNK: common-issues -->
## Common Issues

### Issue: [Problem Description]

**Symptoms:** [What you see when this problem occurs]

**Cause:** [Why this happens]

**Solution:**
1. [Step to fix]
2. [Step to fix]
3. [Step to fix]

**Prevention:** [How to avoid this in the future]

<!-- END CHUNK -->

<!-- CHUNK: antipattern -->
## ❌ Common Mistake: [What People Do Wrong]

**What people try:**
```javascript
// WRONG: [Description of incorrect approach]
const wrong = doItThisWay();
```

**Why it fails:**
- [Reason 1]
- [Reason 2]

**✅ Correct approach:**
```javascript
// RIGHT: [Description of correct approach]
const correct = doItThisWay();
```

**Key differences:**
1. [Difference 1]
2. [Difference 2]

<!-- END CHUNK -->

<!-- CHUNK: related-topics -->
## Related Topics

- **[Related Topic 1](link)** - [How it relates to this topic]
- **[Related Topic 2](link)** - [How it relates to this topic]
- **[Related Topic 3](link)** - [How it relates to this topic]

<!-- END CHUNK -->

<!-- CHUNK: quick-reference -->
## Quick Reference

| Item | Value | Notes |
|------|-------|-------|
| [Key concept] | [Value/Setting] | [When to use] |
| [Key concept] | [Value/Setting] | [When to use] |

**Common commands:**
```bash
# [Description]
command --option value
```

<!-- END CHUNK -->

<!-- CHUNK: best-practices -->
## Best Practices

1. **[Practice 1]** - [Why this is important]
2. **[Practice 2]** - [Why this is important]
3. **[Practice 3]** - [Why this is important]

**Avoid:**
- ❌ [Anti-pattern 1]
- ❌ [Anti-pattern 2]

<!-- END CHUNK -->

---

## NOTES FOR CONTENT AUTHORS

### Chunk Size Guidelines
- **Target:** 300-500 words per chunk
- **Minimum:** 200 words (or chunk is too small for good embeddings)
- **Maximum:** 600 words (or chunk is too large and dilutes relevance)

### Chunk Naming
- Use descriptive IDs: `overview`, `step-by-step-guide`, `code-example`
- Not generic: `section1`, `part2`, `content`
- Include topic: `faq-how-to-add-field`, `antipattern-skip-logic`

### Heading Guidelines
- **Context-rich:** "Configuring Skip Logic for Conditional Form Fields"
- **Not generic:** "Configuration"
- Include key terms that users search for
- Make headings self-contained (readable in isolation)

### Priority Levels
- **Critical:** Core concepts required for any implementation
- **High:** Common implementation tasks, frequently used features
- **Medium:** Advanced features, less common scenarios
- **Low:** Reference information, rarely used features

### Retrieval Boost
- **2.0x:** Critical content (always retrieve first)
- **1.5x:** High priority content (common tasks)
- **1.0x:** Medium priority (default)
- **0.5x:** Low priority (reference only)

### Writing Style
- Use active voice
- Be specific and concrete
- Include examples
- State prerequisites explicitly
- Link to related topics
- Add troubleshooting for common issues
