# Spec Agent Testing - Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Step 1: Set Environment Variables

```bash
export DIFY_API_KEY="your_dify_api_key_here"
export DIFY_API_BASE_URL="https://api.dify.ai/v1"
export AVNI_MCP_SERVER_URL="http://localhost:8023"
export AVNI_AUTH_TOKEN="your_avni_auth_token"  # Optional
```

### Step 2: Run Component Validation (Optional)

```bash
# Verify all components work
uv run python tests/judge_framework/implementations/specAgent/test_components.py
```

Expected output: `✅ All component tests passed!`

### Step 3: Run Spec Agent Tests

```bash
# Run all 6 test scenarios
uv run python tests/judge_framework/examples/run_spec_agent_tests.py
```

## 📊 What You'll See

### Test Execution
```
Starting Spec Agent tests
Loaded 6 test scenarios
Created 6 test subjects
Executing tests...

Test 1/6: happy_path_full_entities
  ✓ Executing test...
  ✓ Evaluating results...
  
Test 2/6: empty_entities_should_ask_for_docs
  ✓ Executing test...
  ✓ Evaluating results...
...
```

### Conversation Monitoring
```
============================================================
Conversation Monitoring Summary
============================================================

Test: happy_path_full_entities
============================================================
Conversation: abc123...
============================================================

📦 Entities Cached: True
   Entity Counts:
   - subject_types: 2
   - programs: 2
   - encounter_types: 7
   - forms: 9

🔧 Tool Calls: 2
   1. generate_spec - success
   2. validate_spec - success

📝 Spec Generated: True
```

### Test Report
```
============================================================
SPEC AGENT TEST REPORT
============================================================

Overall Statistics:
- Total Tests: 6
- Passed: 5
- Failed: 1
- Success Rate: 83.3%

Metric Averages:
- Tool Call Correctness: 85.2%
- Spec Validity: 91.7%
- Entity Coverage: 78.3%
- Conversation Flow: 72.5%
```

## 🎯 Common Test Scenarios

### Run Specific Scenarios

Edit `tests/judge_framework/test_suites/specAgent/spec_agent_test_scenarios.json` to comment out scenarios you don't want to run.

### Fail-Fast Mode (Stop on First Failure)

```bash
uv run python tests/judge_framework/examples/run_spec_agent_tests.py --fail-fast
```

### JSON Output (For CI/CD)

```bash
uv run python tests/judge_framework/examples/run_spec_agent_tests.py --output-format json > results.json
```

### Disable Monitoring (Faster)

```bash
uv run python tests/judge_framework/examples/run_spec_agent_tests.py --no-monitor
```

## 🔍 Debug a Failing Test

### 1. Check Conversation State

```bash
# Get conversation ID from test output, then:
curl https://staging-ai.avniproject.org/debug/conversation/{conversation_id} | jq
```

### 2. Export Debug Snapshot

```python
from tests.judge_framework.implementations.specAgent.monitoring import ConversationMonitor

monitor = ConversationMonitor("https://staging-ai.avniproject.org/")
monitor.export_debug_snapshot("conversation_id", "debug_snapshot.json")
```

### 3. View Detailed Logs

Add logging to see what's happening:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📝 Customize Test Scenarios

### Add a New Scenario

Edit `tests/judge_framework/test_suites/specAgent/spec_agent_test_scenarios.json`:

```json
{
  "scenario": "my_custom_test",
  "description": "Tests a specific behavior",
  "entities_filter": "full",
  "conversation_vars": {
    "org_name": "My Org",
    "query": "Generate the spec please."
  },
  "expected_behavior": {
    "should_call_generate_spec": true
  }
}
```

### Adjust Thresholds

Edit `tests/judge_framework/examples/configs/spec_agent_config.py`:

```python
config.evaluation_config.success_thresholds = {
    "tool_call_correctness": 90.0,  # Stricter
    "spec_validity": 95.0,
    "entity_coverage": 80.0,
    "conversation_flow": 70.0,
}
```

## 🐛 Troubleshooting

### "DIFY_API_KEY not set"
```bash
export DIFY_API_KEY="your_key"
```

### "Connection refused to staging-ai.avniproject.org"
Check that the staging server is running and accessible. Contact the team if the staging environment is down.

### "No module named 'requests'"
Install dependencies:
```bash
uv sync
```

### Agent Not Calling generate_spec
1. Check if entities are being injected
2. Review Spec Agent prompt in Dify YAML
3. Monitor conversation state for debugging

### Tests Taking Too Long
Use `--no-monitor` flag to skip conversation monitoring:
```bash
uv run python tests/judge_framework/examples/run_spec_agent_tests.py --no-monitor
```

## 📚 Next Steps

1. **Review Results**: Check the test report for failures
2. **Debug Issues**: Use monitoring tools to inspect conversation state
3. **Adjust Scenarios**: Modify test scenarios based on findings
4. **Iterate**: Re-run tests after fixing issues
5. **Integrate**: Add to CI/CD pipeline once stable

## 🔗 Useful Links

- **Full Documentation**: `tests/judge_framework/implementations/specAgent/README.md`
- **V3 Testing Guide**: `tests/judge_framework/implementations/specAgent/V3_TESTING_GUIDE.md`
- **Test Scenarios**: `tests/judge_framework/test_suites/specAgent/spec_agent_test_scenarios.json`
- **Configuration**: `tests/judge_framework/examples/configs/spec_agent_config.py`

## 💡 Tips

- Start with component validation to ensure everything is set up correctly
- Use monitoring to understand what the agent is doing
- Adjust thresholds based on your quality requirements
- Export debug snapshots for detailed analysis
- Run fail-fast mode when debugging specific issues

---

**Ready to test?** Run the command and watch your Spec Agent get evaluated! 🚀
