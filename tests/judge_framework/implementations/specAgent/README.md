# Spec Agent Testing Implementation

Automated testing framework for the Dify App Configurator Spec Agent using the judge framework.

## Overview

This implementation tests the Spec Agent's ability to:
- Generate YAML specs from extracted entities
- Call appropriate tools (generate_spec, validate_spec)
- Handle different entity states (full, partial, empty)
- Follow expected conversation workflows
- Ask for user confirmation

## Quick Start

### 1. Set Environment Variables

```bash
export DIFY_API_KEY="your_dify_api_key"
export DIFY_API_BASE_URL="https://api.dify.ai/v1"
export AVNI_MCP_SERVER_URL="https://staging-ai.avniproject.org/"
export AVNI_AUTH_TOKEN="your_avni_token"  # Optional for some tests
```

### 2. Run Tests

```bash
# Run all test scenarios
python tests/judge_framework/examples/run_spec_agent_tests.py

# Run with fail-fast (stop on first failure)
python tests/judge_framework/examples/run_spec_agent_tests.py --fail-fast

# Output as JSON
python tests/judge_framework/examples/run_spec_agent_tests.py --output-format json

# Disable conversation monitoring
python tests/judge_framework/examples/run_spec_agent_tests.py --no-monitor
```

### 3. Monitor Conversation State

The framework automatically monitors conversation state on the avni-ai server. You can also query manually:

```bash
# Get conversation state
curl https://staging-ai.avniproject.org/debug/conversation/{conversation_id}

# List all conversations
curl https://staging-ai.avniproject.org/debug/conversations

# Clear conversation state
curl -X DELETE https://staging-ai.avniproject.org/debug/conversation/{conversation_id}
```

## Architecture

### Components

1. **SpecAgentTestSubject** (`spec_agent_subject.py`)
   - Loads entities from Durga India scoping documents
   - Creates test cases with different entity combinations
   - Supports conversation variable injection

2. **SpecAgentExecutor** (`spec_agent_executor.py`)
   - Executes Dify conversations with variable injection
   - Extracts generated specs from responses
   - Tracks tool calls made by agent

3. **SpecAgentJudge** (`spec_agent_judge.py`)
   - Evaluates spec generation quality
   - Validates YAML structure
   - Checks entity coverage
   - Assesses conversation flow

4. **ConversationMonitor** (`monitoring.py`)
   - Queries avni-ai server for conversation state
   - Inspects cached entities and tool calls
   - Exports debug snapshots

### Test Scenarios

Located in `tests/judge_framework/test_suites/specAgent/spec_agent_test_scenarios.json`:

1. **happy_path_full_entities**: Full entities → generate spec → user approves
2. **empty_entities_should_ask_for_docs**: No entities → agent asks for documents
3. **partial_entities_subject_types_only**: Only subject types loaded
4. **partial_entities_no_forms**: All entities except forms
5. **user_confirmation_yes**: User approves generated spec
6. **user_requests_corrections**: User requests changes

## Evaluation Criteria

### 1. Tool Call Correctness (30% weight)
- Did agent call `generate_spec` with conversation_id?
- Did agent call `validate_spec`?
- Were tools called in correct order?

**Thresholds:**
- 100%: Called both generate_spec and validate_spec
- 80%: Called generate_spec only
- 0%: Did not call generate_spec

### 2. Spec Validity (30% weight)
- Is the generated YAML valid?
- Does it have expected structure?
- Are required keys present?

**Thresholds:**
- 100%: Valid YAML with all expected keys
- 60-100%: Valid YAML with some expected keys
- 0%: Invalid YAML or no spec generated

### 3. Entity Coverage (25% weight)
- Are all input entities present in the spec?
- Are entity names preserved correctly?
- Are relationships maintained?

**Thresholds:**
- 100%: All entities covered
- 70-99%: Most entities covered
- 0%: No entities or cannot evaluate

### 4. Conversation Flow (15% weight)
- Did agent output SPEC_APPROVED marker?
- Did agent ask for user confirmation?
- Did agent provide summary/details?

**Thresholds:**
- 100%: All flow markers present
- 50-80%: Some flow markers present
- 0%: No expected flow markers

## Test Data

### Entities
Pre-extracted from Durga India scoping documents:
- **Location**: `tests/resources/scoping/entities_summary.json`
- **Contents**:
  - 2 subject types (Cohort, Participant)
  - 2 programs (Work With Men, Work With Women)
  - 7 encounter types
  - 2 address levels (State, City)
  - 6 forms with detailed fields

### Conversation Variables
Templates in `tests/judge_framework/test_suites/specAgent/conversation_variable_templates.json`:
- `default`: Basic setup
- `with_full_entities`: Full entity injection
- `spec_already_generated`: Follow-up scenarios
- `empty_state`: No entities loaded

## Monitoring & Debugging

### Server-Side Endpoints

**GET /debug/conversation/{conversation_id}**
```json
{
  "conversation_id": "...",
  "entities_cached": true,
  "entities_summary": {
    "subject_types": 2,
    "programs": 2,
    "encounter_types": 7,
    "forms": 6
  },
  "tool_calls": [
    {"tool": "generate_spec", "status": "success"},
    {"tool": "validate_spec", "status": "success"}
  ],
  "conversation_variables": {
    "entities_jsonl": "...",
    "spec_yaml": "..."
  }
}
```

**GET /debug/conversations**
Lists all cached conversations with summaries.

**DELETE /debug/conversation/{conversation_id}**
Clears cached state for a conversation.

### Client-Side Tools

```python
from tests.judge_framework.implementations.specAgent.monitoring import ConversationMonitor

monitor = ConversationMonitor("http://localhost:8023")

# Get conversation state
state = monitor.get_conversation_state(conversation_id)

# Print summary
monitor.print_conversation_summary(conversation_id)

# Export debug snapshot
monitor.export_debug_snapshot(conversation_id, "debug_snapshot.json")
```

## Configuration

### Default Configuration
```python
from tests.judge_framework.examples.configs.spec_agent_config import get_spec_agent_config

config = get_spec_agent_config()
```

### Strict Configuration (Production)
```python
from tests.judge_framework.examples.configs.spec_agent_config import get_strict_config

config = get_strict_config()  # Higher thresholds
```

### Lenient Configuration (Development)
```python
from tests.judge_framework.examples.configs.spec_agent_config import get_lenient_config

config = get_lenient_config()  # Lower thresholds for debugging
```

## Adding New Test Scenarios

1. Edit `tests/judge_framework/test_suites/specAgent/spec_agent_test_scenarios.json`
2. Add new scenario with:
   - `scenario`: Unique identifier
   - `description`: What the test does
   - `entities_filter`: Which entities to use (full, empty, partial_*)
   - `conversation_vars`: Variables to inject
   - `expected_behavior`: What agent should do

Example:
```json
{
  "scenario": "my_new_test",
  "description": "Tests something specific",
  "entities_filter": "full",
  "conversation_vars": {
    "org_name": "Test Org",
    "query": "Generate the spec."
  },
  "expected_behavior": {
    "should_call_generate_spec": true
  }
}
```

## Troubleshooting

### Agent Not Calling generate_spec

**Check:**
1. Are entities properly injected? Monitor conversation state
2. Is the Spec Agent prompt correct in Dify YAML?
3. Are conversation variables being passed correctly?

**Debug:**
```bash
# Check conversation state
curl http://localhost:8023/debug/conversation/{conversation_id}

# Run with monitoring enabled
python tests/judge_framework/examples/run_spec_agent_tests.py
```

### Invalid YAML Generated

**Check:**
1. Is the spec extraction working? Check `spec_yaml` in test output
2. Are there markdown code blocks interfering?
3. Is the agent outputting SPEC_APPROVED marker?

**Debug:**
```python
# In spec_agent_executor.py, add logging
logger.info(f"Raw response: {agent_response}")
logger.info(f"Extracted spec: {spec_yaml}")
```

### Low Entity Coverage

**Check:**
1. Are entity names matching between input and spec?
2. Is the spec parser handling all entity types?
3. Are there typos in entity names?

**Debug:**
```python
# In spec_agent_judge.py, add detailed logging
logger.info(f"Input entities: {input_names}")
logger.info(f"Spec entities: {spec_names}")
logger.info(f"Covered: {input_names & spec_names}")
```

## Integration with CI/CD

```yaml
# .github/workflows/spec-agent-tests.yml
name: Spec Agent Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run Spec Agent tests
        env:
          DIFY_API_KEY: ${{ secrets.DIFY_API_KEY }}
          AVNI_MCP_SERVER_URL: ${{ secrets.AVNI_MCP_SERVER_URL }}
        run: |
          python tests/judge_framework/examples/run_spec_agent_tests.py --fail-fast
```

## Future Enhancements

- [ ] Multi-turn conversation testing (corrections flow)
- [ ] Performance benchmarking (response time, token usage)
- [ ] Spec quality scoring (beyond structure validation)
- [ ] Automated spec correction testing
- [ ] Integration with full end-to-end flow testing
- [ ] Support for multiple scoping documents
- [ ] Parallel test execution
- [ ] Historical test result tracking
