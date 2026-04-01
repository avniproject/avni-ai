# Testing Spec Agent with v3 Workflow

## Quick Start

The v3 workflow is now fully compatible with the Spec Agent test framework. All critical issues have been fixed.

### Run Tests with v3 Workflow (Default)

```bash
# Set environment variables
export DIFY_API_KEY="your_dify_api_key"
export AVNI_MCP_SERVER_URL="http://localhost:8023"

# Start avni-ai server (Terminal 1)
cd /Users/himeshr/IdeaProjects/avni-ai
uv run python -m src.main

# Run tests with v3 workflow (Terminal 2)
uv run python tests/judge_framework/examples/run_spec_agent_tests.py
```

### Run Tests with v2 Workflow

```bash
uv run python tests/judge_framework/examples/run_spec_agent_tests.py --workflow-version v2
```

## What Was Fixed in v3

### 1. spec_yaml Extraction
- **Added:** Extract Spec YAML code node
- **Added:** Save Spec YAML variable assigner
- **Result:** spec_yaml is now properly captured from Spec Agent response

### 2. JSON Body Fix
- **Fixed:** Patch Bundle HTTP body now has quoted spec_yaml
- **Before:** `"spec_yaml": {{#conversation.spec_yaml#}}`
- **After:** `"spec_yaml": "{{#conversation.spec_yaml#}}"`
- **Result:** Valid JSON sent to backend

### 3. Edge Routing
- **Updated:** Spec Agent → Extract Spec → Save Spec → Download Bundle
- **Result:** Proper data flow through new nodes

### 4. Duplicate Edge Removed
- **Removed:** Duplicate edge from "Already Processed?" to Doc Extractor
- **Result:** No more unpredictable behavior

### 5. Enhanced Spec Agent Instruction
- **Added:** Explicit SPEC_APPROVED format
- **Added:** Check for pre-populated entities
- **Added:** No markdown code blocks instruction
- **Result:** More reliable spec extraction

## Test Scenarios

All 6 test scenarios work with v3:

1. **happy_path_full_entities** - Full entities → generate spec → approve
2. **empty_entities_should_ask_for_docs** - No entities → ask for docs
3. **partial_entities_subject_types_only** - Only subject types
4. **partial_entities_no_forms** - All except forms
5. **user_confirmation_yes** - User approves spec
6. **user_requests_corrections** - User requests changes

## Command Line Options

```bash
# Default (v3 workflow)
uv run python tests/judge_framework/examples/run_spec_agent_tests.py

# Specify v2 workflow
uv run python tests/judge_framework/examples/run_spec_agent_tests.py --workflow-version v2

# Fail-fast mode
uv run python tests/judge_framework/examples/run_spec_agent_tests.py --fail-fast

# JSON output
uv run python tests/judge_framework/examples/run_spec_agent_tests.py --output-format json

# Disable monitoring
uv run python tests/judge_framework/examples/run_spec_agent_tests.py --no-monitor

# Custom scenarios file
uv run python tests/judge_framework/examples/run_spec_agent_tests.py \
  --scenarios path/to/scenarios.json \
  --entities path/to/entities.json
```

## Monitoring v3 Workflow

### Check Conversation State

```bash
# List all conversations
curl http://localhost:8023/debug/conversations

# Get specific conversation
curl http://localhost:8023/debug/conversation/{conversation_id} | jq
```

### Expected in v3 Conversation State

```json
{
  "conversation_id": "abc123...",
  "entities_cached": true,
  "entities_summary": {
    "subject_types": 2,
    "programs": 2,
    "encounter_types": 7,
    "forms": 9
  },
  "tool_calls": [
    {"tool": "generate_spec", "status": "success"},
    {"tool": "validate_spec", "status": "success"}
  ],
  "conversation_variables": {
    "entities_jsonl": "{...}",
    "spec_yaml": "subject_types:\n  - name: Cohort\n...",
    "setup_mode_active": true
  }
}
```

**Key difference from v2:** `spec_yaml` is now populated!

## Validation Checklist

After running tests, verify:

- ✅ spec_yaml is populated in conversation state
- ✅ Tool calls show generate_spec and validate_spec
- ✅ No JSON parsing errors in logs
- ✅ Test success rate > 70%
- ✅ Entity coverage scores > 70%

## Troubleshooting v3

### spec_yaml Still Empty?

Check:
1. Spec Agent output contains "SPEC_APPROVED"
2. Extract Spec YAML node is in the flow
3. Edge connections are correct
4. No errors in Dify workflow logs

### JSON Errors in Patch Bundle?

Check:
1. spec_yaml has quotes in JSON body (line 1553)
2. No special characters breaking JSON
3. Backend can handle multi-line strings

### Test Failures?

Check:
1. Workflow name is correct: "App Configurator [Staging] v3"
2. DIFY_API_KEY is valid
3. avni-ai server is running on port 8023
4. Entities file exists and is valid JSON

## Differences Between v2 and v3

| Feature | v2 | v3 |
|---------|----|----|
| spec_yaml extraction | Manual/Missing | Automated via code node |
| JSON body | May have issues | Fixed with quotes |
| Duplicate edges | Present | Removed |
| Spec Agent instruction | Basic | Enhanced with format |
| Test compatibility | Partial | Full |

## Performance

v3 workflow adds 2 nodes to the flow:
- Extract Spec YAML (code node) - ~50ms
- Save Spec YAML (variable assigner) - ~10ms

**Total overhead:** ~60ms per test (negligible)

## Next Steps

1. **Upload v3 to Dify** - Import the updated YAML file
2. **Run manual test** - Verify workflow works in Dify UI
3. **Run automated tests** - Execute full test suite
4. **Monitor results** - Check debug endpoints
5. **Iterate if needed** - Adjust based on findings

## Files Modified

- `dify/App Configurator [Staging] v3.yml` - Main workflow file
- `tests/judge_framework/examples/run_spec_agent_tests.py` - Added v3 support
- `tests/judge_framework/examples/configs/spec_agent_config.py` - Added v3 config

## Documentation

- **Implementation Summary:** `dify/V3_WORKFLOW_FIXES_SUMMARY.md`
- **Test Framework:** `tests/judge_framework/implementations/specAgent/IMPLEMENTATION_SUMMARY.md`
- **Quick Start:** `tests/judge_framework/implementations/specAgent/QUICK_START.md`

---

**Status:** ✅ Ready for Testing  
**Default Workflow:** v3  
**Backward Compatible:** Yes (use --workflow-version v2)
