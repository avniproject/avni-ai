"""
Test Subject interface for the Judge Framework
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Any
from .result_models import TestConfiguration


class TestSubject(ABC):
    """
    Abstract interface for test subjects - what we're testing.
    Each implementation represents a different type of test artifact.
    """

    def __init__(self, test_data: Dict[str, Any], config: TestConfiguration):
        self.test_data = test_data
        self.config = config

    @abstractmethod
    def get_test_identifier(self) -> str:
        """Get unique identifier for this test subject"""
        pass

    @abstractmethod
    def get_test_input(self) -> Dict[str, Any]:
        """Get input data that will be passed to the test executor"""
        pass

    @abstractmethod
    def get_expected_behavior(self) -> str:
        """Get description of expected behavior for evaluation"""
        pass

    @abstractmethod
    def get_evaluation_context(self) -> Dict[str, Any]:
        """Get additional context needed for evaluation"""
        pass

    def get_test_metadata(self) -> Dict[str, Any]:
        """Get metadata about this test subject"""
        return {
            "test_type": self.__class__.__name__,
            "identifier": self.get_test_identifier(),
            "config_workflow": self.config.workflow_name,
        }


class TestSubjectFactory(ABC):
    """
    Factory interface for creating test subjects from various sources
    """

    @abstractmethod
    def create_from_static_data(
        self, static_case: Dict[str, Any], config: TestConfiguration
    ) -> "TestSubject":
        """Create test subject from static test case data"""
        pass

    @abstractmethod
    def create_from_ai_generation(
        self, ai_prompt: str, config: TestConfiguration
    ) -> "TestSubject":
        """Create test subject from AI-generated test case"""
        pass

    @abstractmethod
    def get_generation_prompt_template(self) -> str:
        """Get the prompt template for AI test generation"""
        pass


class TestSubjectGenerator:
    """
    Utility class for generating test subjects using mixed approach
    (static cases + AI-generated cases)
    """

    def __init__(self, factory: TestSubjectFactory):
        self.factory = factory

    def generate_test_suite(
        self, config: TestConfiguration, num_ai_cases: int = 0
    ) -> List[TestSubject]:
        """
        Generate a complete test suite combining static and AI-generated cases
        """
        test_subjects = []

        # Add static test cases
        for static_case in config.static_test_cases:
            subject = self.factory.create_from_static_data(static_case, config)
            test_subjects.append(subject)

        # Add AI-generated test cases if enabled
        if config.ai_generation_enabled and num_ai_cases > 0:
            ai_subjects = self._generate_ai_cases(config, num_ai_cases)
            test_subjects.extend(ai_subjects)

        return test_subjects

    def _generate_ai_cases(
        self, config: TestConfiguration, num_cases: int
    ) -> List[TestSubject]:
        """Generate AI-powered test cases"""
        import openai

        ai_subjects = []
        generation_prompt = self.factory.get_generation_prompt_template()

        for i in range(num_cases):
            try:
                response = openai.chat.completions.create(
                    model=config.openai_model,
                    messages=[{"role": "system", "content": generation_prompt}],
                    temperature=config.openai_temperature,
                    max_tokens=800,
                )

                ai_case_content = response.choices[0].message.content.strip()

                # Parse AI response into test case format
                # This assumes AI returns JSON, can be customized per factory
                import json

                ai_case_data = json.loads(ai_case_content)

                subject = self.factory.create_from_ai_generation(ai_case_data, config)
                ai_subjects.append(subject)

            except Exception as e:
                print(f"Failed to generate AI test case {i + 1}: {e}")
                # Continue with other cases even if one fails
                continue

        return ai_subjects
