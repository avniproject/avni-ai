# Judge Framework - Reusable LLM-as-Judge Testing System

A modular, extensible framework for testing AI interactions using LLM-as-judge methodology. Originally designed for Avni healthcare system testing, now reusable across multiple domains.

## 🎯 Purpose

The Judge Framework provides a standardized way to:
- Test LLM chat conversations with Dify workflows
- Validate form element configurations  
- Evaluate visit scheduling rules
- Generate comprehensive analytics and reports

## 🏗️ Architecture

### Core Components

- **TestSubject**: What we're testing (conversations, forms, rules)
- **TestExecutor**: How we run the tests (Dify workflows, validation engines)
- **JudgeStrategy**: Evaluation logic and scoring criteria
- **JudgeOrchestrator**: Coordinates the testing workflow
- **Analytics**: Statistics calculation and multi-format reporting

### Design Patterns

- **Strategy Pattern**: Pluggable conversation generation and evaluation
- **Template Method**: Standardized test execution workflow
- **Factory Pattern**: Flexible test subject creation
- **Observer Pattern**: Progress reporting and monitoring

## 🚀 Quick Start

### 1. Environment Setup

```bash
# Set required environment variables
export OPENAI_API_KEY="your_openai_key"
export DIFY_API_KEY="your_dify_key"
export DIFY_API_BASE_URL="https://api.dify.ai/v1"
export AVNI_AUTH_TOKEN="your_avni_token"
export AVNI_MCP_SERVER_URL="your_mcp_url"
```

### 2. Run Conversation Tests

```bash
cd tests/judge_framework/examples
python run_conversation_tests.py --output-format all
```

### 3. View Results

- Console report: Displayed in terminal
- JSON report: `conversation_test_report.json`
- CSV report: `conversation_test_report.csv`

## 📁 Directory Structure

```
judge_framework/
├── interfaces/           # Core abstractions and contracts
│   ├── test_subject.py   # Test subject interface and factory
│   ├── test_executor.py  # Test execution interface
│   ├── judge_strategy.py # Evaluation strategy interface
│   ├── result_models.py  # Configuration and result models
│   └── conversation_strategy.py # Conversation generation strategies
├── orchestrator.py       # Main test coordination logic
├── analytics/           # Statistics and reporting
│   ├── statistics.py    # Statistical calculations
│   └── reporting.py     # Multi-format report generation
├── implementations/     # Concrete implementations
│   └── conversation/    # Chat conversation testing
└── examples/           # Usage examples and configurations
    ├── configs/        # Configuration files
    ├── run_conversation_tests.py
    └── MIGRATION.md    # Migration guide from old system
```

## 🔧 Configuration

The framework uses modular configuration:

```python
from judge_framework.interfaces.result_models import TestConfiguration, DifyConfig, EvaluationConfig, TestGenerationConfig

config = TestConfiguration(
    dify_config=DifyConfig(
        api_key="your_key",
        base_url="https://api.dify.ai/v1",
        workflow_name="your_workflow"
    ),
    evaluation_config=EvaluationConfig(
        evaluation_metrics=["accuracy", "completeness", "consistency"],
        success_thresholds={"accuracy": 75.0, "completeness": 80.0}
    ),
    generation_config=TestGenerationConfig(
        static_test_cases=[...],
        ai_generation_enabled=True,
        num_ai_cases=5
    )
)
```

## 📊 Supported Test Types

### 1. Conversation Testing ✅
Tests multi-turn AI conversations with Dify workflows:
- Configurable conversation strategies (AI, rule-based)
- Existing prompt integration
- Conversation flow analysis

### 2. Form Validation Testing 🚧
Tests Avni form element validation:
- Validation rule correctness
- Edge case handling
- User experience assessment

### 3. Scheduling Rules Testing 🚧
Tests visit scheduling logic:
- Rule correctness validation
- Performance analysis
- Compliance checking

## 📈 Analytics & Reporting

### Report Formats
- **Console**: Human-readable terminal output
- **JSON**: Machine-readable structured data
- **CSV**: Data analysis spreadsheet format

### Metrics
- Success rates and error analysis
- Score distributions and statistics
- Performance trends and comparisons
- Detailed error categorization

## 🔄 Migration from Old System

See `examples/MIGRATION.md` for detailed migration guide from the original `TestingSystem`.

### Key Benefits
- **Extensibility**: Easy to add new test types
- **Better Analytics**: Multiple report formats and detailed statistics
- **Modular Configuration**: Separate concerns for different components
- **Robust Error Handling**: Configurable failure modes and detailed error tracking

## 🧪 Extending the Framework

### Adding New Test Types

1. **Create Test Subject**:
```python
class MyTestSubject(TestSubject):
    def get_test_identifier(self) -> str:
        return "my_test"
    
    def get_test_input(self) -> Dict[str, Any]:
        return {"test_data": "..."}
```

2. **Create Test Executor**:
```python
class MyTestExecutor(TestExecutor):
    def execute(self, test_input: Dict[str, Any]) -> Dict[str, Any]:
        # Your test execution logic
        return {"result": "..."}
```

3. **Create Judge Strategy**:
```python
class MyJudgeStrategy(JudgeStrategy):
    def evaluate(self, test_input, test_output) -> EvaluationResult:
        # Your evaluation logic
        return result
```

4. **Create Factory**:
```python
class MyTestSubjectFactory(TestSubjectFactory):
    def create_from_static_data(self, static_case, config):
        return MyTestSubject(static_case, config)
```

## 🛠️ Development

### Running Tests
```bash
# Run conversation tests
python examples/run_conversation_tests.py

# Run with specific options
python examples/run_conversation_tests.py --fail-fast --output-format json
```

### Adding New Features
1. Follow the interface contracts in `interfaces/`
2. Add implementations in `implementations/`
3. Create example configurations in `examples/configs/`
4. Update documentation

## 📝 Requirements

- Python 3.8+
- OpenAI API key
- Dify API key and workflow URL
- Avni authentication tokens (for healthcare testing)

## 🤝 Contributing

1. Follow the existing architecture patterns
2. Add comprehensive tests for new features
3. Update documentation and examples
4. Maintain backward compatibility where possible

## 📄 License

This framework is part of the Avni project and follows the same licensing terms.
