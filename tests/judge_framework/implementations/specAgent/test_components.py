"""
Component validation tests for Spec Agent implementation.

Quick tests to verify all components are working correctly.
"""

import json
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent.parent
sys.path.insert(0, str(project_root))


def test_entities_loading():
    """Test that entities can be loaded from file."""
    print("Testing entities loading...")

    entities_file = project_root / "tests/resources/scoping/entities_summary.json"

    if not entities_file.exists():
        print(f"❌ Entities file not found: {entities_file}")
        return False

    with open(entities_file, "r") as f:
        data = json.load(f)

    # Extract actual_value
    if "conditions" in data and len(data["conditions"]) > 0:
        entities = data["conditions"][0].get("actual_value", {})
    else:
        entities = data

    # Validate structure
    expected_keys = [
        "subject_types",
        "programs",
        "encounter_types",
        "address_levels",
        "forms",
    ]
    for key in expected_keys:
        if key not in entities:
            print(f"❌ Missing key in entities: {key}")
            return False

    print("✅ Entities loaded successfully")
    print(f"   - Subject Types: {len(entities['subject_types'])}")
    print(f"   - Programs: {len(entities['programs'])}")
    print(f"   - Encounter Types: {len(entities['encounter_types'])}")
    print(f"   - Forms: {len(entities['forms'])}")

    return True


def test_test_subject_creation():
    """Test that test subjects can be created."""
    print("\nTesting test subject creation...")

    try:
        from tests.judge_framework.implementations.specAgent import (
            SpecAgentTestSubjectFactory,
        )
        from tests.judge_framework.interfaces.result_models import (
            TestConfiguration,
            DifyConfig,
            EvaluationConfig,
            TestGenerationConfig,
        )

        entities_file = str(
            project_root / "tests/resources/scoping/entities_summary.json"
        )

        # Create factory
        factory = SpecAgentTestSubjectFactory(entities_file)

        # Create test configuration
        config = TestConfiguration(
            dify_config=DifyConfig(
                api_key="test", base_url="http://test", workflow_name="Test Workflow"
            ),
            evaluation_config=EvaluationConfig(
                evaluation_metrics=["test"], success_thresholds={"test": 80.0}
            ),
            generation_config=TestGenerationConfig(
                static_test_cases=[], ai_generation_enabled=False
            ),
        )

        # Create test subject
        test_case = {
            "scenario": "test_scenario",
            "entities_filter": "full",
            "conversation_vars": {"org_name": "Test"},
            "expected_behavior": {},
        }

        subject = factory.create_from_static_data(test_case, config)

        print(f"✅ Test subject created: {subject.get_test_identifier()}")

        # Validate test input
        test_input = subject.get_test_input()
        if "query" not in test_input or "inputs" not in test_input:
            print("❌ Invalid test input structure")
            return False

        print(f"   - Query: {test_input['query'][:50]}...")
        print(f"   - Inputs keys: {list(test_input['inputs'].keys())}")

        return True

    except Exception as e:
        print(f"❌ Failed to create test subject: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_scenarios_loading():
    """Test that test scenarios can be loaded."""
    print("\nTesting scenarios loading...")

    scenarios_file = (
        project_root
        / "tests/judge_framework/test_suites/specAgent/spec_agent_test_scenarios.json"
    )

    if not scenarios_file.exists():
        print(f"❌ Scenarios file not found: {scenarios_file}")
        return False

    with open(scenarios_file, "r") as f:
        data = json.load(f)

    scenarios = data.get("test_scenarios", [])

    if not scenarios:
        print("❌ No scenarios found in file")
        return False

    print(f"✅ Loaded {len(scenarios)} test scenarios")
    for scenario in scenarios:
        print(f"   - {scenario['scenario']}: {scenario['description'][:50]}...")

    return True


def test_executor_creation():
    """Test that executor can be created."""
    print("\nTesting executor creation...")

    try:
        from tests.judge_framework.implementations.specAgent import SpecAgentExecutor
        from tests.judge_framework.interfaces.result_models import (
            TestConfiguration,
            DifyConfig,
            EvaluationConfig,
            TestGenerationConfig,
        )

        config = TestConfiguration(
            dify_config=DifyConfig(
                api_key="test", base_url="http://test", workflow_name="Test Workflow"
            ),
            evaluation_config=EvaluationConfig(
                evaluation_metrics=["test"], success_thresholds={"test": 80.0}
            ),
            generation_config=TestGenerationConfig(
                static_test_cases=[], ai_generation_enabled=False
            ),
        )

        executor = SpecAgentExecutor(config)

        print("✅ Executor created successfully")
        metadata = executor.get_executor_metadata()
        print(f"   - Type: {metadata['executor_type']}")
        print(
            f"   - Supports variable injection: {metadata['supports_variable_injection']}"
        )

        return True

    except Exception as e:
        print(f"❌ Failed to create executor: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_judge_creation():
    """Test that judge can be created."""
    print("\nTesting judge creation...")

    try:
        from tests.judge_framework.implementations.specAgent import SpecAgentJudge
        from tests.judge_framework.interfaces.result_models import (
            TestConfiguration,
            DifyConfig,
            EvaluationConfig,
            TestGenerationConfig,
        )

        config = TestConfiguration(
            dify_config=DifyConfig(
                api_key="test", base_url="http://test", workflow_name="Test Workflow"
            ),
            evaluation_config=EvaluationConfig(
                evaluation_metrics=["tool_call_correctness", "spec_validity"],
                success_thresholds={"tool_call_correctness": 80.0},
            ),
            generation_config=TestGenerationConfig(
                static_test_cases=[], ai_generation_enabled=False
            ),
        )

        judge = SpecAgentJudge(config)

        print("✅ Judge created successfully")

        # Test evaluation with mock data
        test_input = {
            "test_scenario": "test",
            "entities": {"subject_types": [{"name": "Test"}]},
            "expected_behavior": {},
        }

        test_output = {
            "success": True,
            "conversation_id": "test123",
            "agent_response": "SPEC_APPROVED\nsubject_types:\n  - name: Test",
            "spec_yaml": "subject_types:\n  - name: Test",
            "tool_calls": [{"tool": "generate_spec", "status": "success"}],
        }

        result = judge.evaluate(test_input, test_output)

        print("   - Evaluation completed")
        print(f"   - Overall score: {result.scores.get('overall', 0):.1f}")
        print(f"   - Passed: {result.success}")

        return True

    except Exception as e:
        print(f"❌ Failed to create/test judge: {e}")
        import traceback

        traceback.print_exc()
        return False


def test_monitoring_tools():
    """Test that monitoring tools can be created."""
    print("\nTesting monitoring tools...")

    try:
        from tests.judge_framework.implementations.specAgent.monitoring import (
            ConversationMonitor,
        )

        monitor = ConversationMonitor("http://localhost:8023")

        print("✅ Monitoring tools created successfully")
        print(f"   - Base URL: {monitor.base_url}")

        return True

    except Exception as e:
        print(f"❌ Failed to create monitoring tools: {e}")
        import traceback

        traceback.print_exc()
        return False


def main():
    """Run all component tests."""
    print("=" * 60)
    print("Spec Agent Component Validation Tests")
    print("=" * 60)

    tests = [
        test_entities_loading,
        test_scenarios_loading,
        test_test_subject_creation,
        test_executor_creation,
        test_judge_creation,
        test_monitoring_tools,
    ]

    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
            import traceback

            traceback.print_exc()
            results.append(False)

    print("\n" + "=" * 60)
    print("Test Results Summary")
    print("=" * 60)

    passed = sum(results)
    total = len(results)

    print(f"Passed: {passed}/{total}")

    if passed == total:
        print("✅ All component tests passed!")
        return 0
    else:
        print(f"❌ {total - passed} test(s) failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
