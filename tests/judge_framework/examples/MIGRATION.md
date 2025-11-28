# Migration Guide: From TestingSystem to Judge Framework

This guide shows how to migrate from the original `TestingSystem` to the new reusable `JudgeFramework`.

## Overview

The new Judge Framework provides:
- **Modular configuration** with separate components for Dify, evaluation, and test generation
- **Strategy pattern** for pluggable conversation generation and evaluation
- **Unified analytics** with multiple report formats
- **Extensibility** for form validation and scheduling rule testing

## Side-by-Side Comparison

### Old Approach (TestingSystem)

```python
from tests.dify.prompts.testing_system import TestingSystem

# Initialize system
testing_system = TestingSystem(dify_api_key)

# Run tests
testing_system.run_full_test_cycles(num_cycles=5)

# Generate report
testing_system.generate_and_print_report()
```

### New Approach (Judge Framework)

```python
from tests.judge_framework.orchestrator import JudgeOrchestrator
from tests.judge_framework.examples.configs.conversation_config import create_conversation_test_config
from tests.judge_framework.implementations.conversation import (
    ConversationTestSubjectFactory,
    ConversationExecutorWrapper, 
    ConversationJudgeStrategyWrapper
)

# Create configuration
config = create_conversation_test_config()

# Set up components
test_subject_factory = ConversationTestSubjectFactory(tester_prompts)
executor = ConversationExecutorWrapper(config=config, scenario_prompts=tester_prompts)
judge_strategy = ConversationJudgeStrategyWrapper(config)

# Create orchestrator
orchestrator = JudgeOrchestrator(executor, judge_strategy)

# Run tests
suite_result = orchestrator.run_test_suite(test_subject_factory, config)

# Generate reports
statistics = StatisticsCalculator.calculate_suite_statistics(suite_result)
report = ReportGenerator.generate_console_report(suite_result, statistics)
```

## Key Changes

### 1. Configuration Structure

**Before:**
```python
# Monolithic configuration
testing_system = TestingSystem(dify_api_key)
```

**After:**
```python
# Modular configuration
config = TestConfiguration(
    dify_config=DifyConfig(api_key="...", base_url="...", workflow_name="..."),
    evaluation_config=EvaluationConfig(evaluation_metrics=[...], success_thresholds={...}),
    generation_config=TestGenerationConfig(static_test_cases=[...], ai_generation_enabled=True)
)
```

### 2. Test Execution

**Before:**
```python
# Fixed 8-iteration conversations
testing_system.run_single_conversation(scenario_index, cycle)
```

**After:**
```python
# Configurable execution with pluggable strategies
suite_result = orchestrator.run_test_suite(
    test_subject_factory=test_subject_factory,
    config=config,
    fail_fast=False  # Optional early termination
)
```

### 3. Evaluation

**Before:**
```python
# Fixed evaluation metrics (configuration_correctness, consistency, communication_quality)
analysis = reviewer.analyze_conversation(chat_history, scenario)
```

**After:**
```python
# Configurable evaluation metrics
result = judge_strategy.evaluate(test_input, test_output)
# Metrics defined in config.evaluation_config.evaluation_metrics
```

### 4. Reporting

**Before:**
```python
# Console-only reporting
testing_system.generate_and_print_report()
```

**After:**
```python
# Multiple formats
console_report = ReportGenerator.generate_console_report(suite_result, statistics)
json_report = ReportGenerator.generate_json_report(suite_result, statistics)
csv_report = ReportGenerator.generate_csv_report(suite_result)
```

## Migration Steps

### Step 1: Update Environment Configuration

Replace single API key configuration with modular config:

```python
# Old .env
DIFY_API_KEY=your_api_key
OPENAI_API_KEY=your_openai_key

# New .env (same variables, but used differently)
DIFY_API_KEY=your_api_key
DIFY_API_BASE_URL=https://api.dify.ai/v1
OPENAI_API_KEY=your_openai_key
AVNI_AUTH_TOKEN=your_avni_token
AVNI_MCP_SERVER_URL=your_mcp_url
```

### Step 2: Replace Test Execution Code

```python
# Remove old imports
# from tests.dify.prompts.testing_system import TestingSystem

# Add new imports
from tests.judge_framework.orchestrator import JudgeOrchestrator
from tests.judge_framework.examples.configs.conversation_config import create_conversation_test_config
from tests.judge_framework.implementations.conversation import (
    ConversationTestSubjectFactory,
    ConversationExecutorWrapper,
    ConversationJudgeStrategyWrapper
)
```

### Step 3: Update Test Execution Logic

```python
# Old approach
def main():
    testing_system = TestingSystem(dify_api_key)
    testing_system.run_full_test_cycles(num_cycles=5)
    testing_system.generate_and_print_report()

# New approach
def main():
    config = create_conversation_test_config()
    
    # Set up components
    scenario_names, tester_prompts = load_conversation_prompts()
    test_subject_factory = ConversationTestSubjectFactory(tester_prompts)
    executor = ConversationExecutorWrapper(config=config, scenario_prompts=tester_prompts)
    judge_strategy = ConversationJudgeStrategyWrapper(config)
    
    # Run tests
    orchestrator = JudgeOrchestrator(executor, judge_strategy)
    suite_result = orchestrator.run_test_suite(test_subject_factory, config, fail_fast=False)
    
    # Generate reports
    statistics = StatisticsCalculator.calculate_suite_statistics(suite_result)
    report = ReportGenerator.generate_console_report(suite_result, statistics)
    print(report)
```

## Benefits of Migration

### 1. **Extensibility**
- Easy to add new test types (forms, scheduling rules)
- Pluggable evaluation strategies
- Configurable metrics per use case

### 2. **Better Analytics**
- Multiple report formats (console, JSON, CSV)
- Detailed statistics and error analysis
- Test suite comparison capabilities

### 3. **Improved Configuration**
- Separate concerns (Dify, evaluation, generation)
- Environment-specific configurations
- Multiple workflow support with different API keys

### 4. **Robust Error Handling**
- Continue on failure by default
- Configurable fail-fast behavior
- Detailed error categorization

## Backward Compatibility

The new framework wraps existing components, so:
- Existing prompts and scenarios work unchanged
- Original evaluation logic is preserved
- Migration can be gradual

## Testing the Migration

1. Run the old system and save results
2. Run the new system with equivalent configuration
3. Compare results using the new comparison functionality:

```python
from tests.judge_framework.analytics.statistics import StatisticsCalculator

# Compare old vs new results
comparison = StatisticsCalculator.compare_test_suites([old_suite_result, new_suite_result])
print(ReportGenerator.generate_comparison_report([old_suite_result, new_suite_result], comparison))
```

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure Python path includes project root
2. **Missing Environment Variables**: Check all required variables in .env
3. **Configuration Errors**: Validate configuration objects before use

### Getting Help

- Check the example scripts in `examples/` directory
- Review the interface documentation in `interfaces/`
- Compare with working conversation example in `run_conversation_tests.py`
