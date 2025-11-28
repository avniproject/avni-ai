"""
Result models and configuration classes for the Judge Framework
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
from abc import ABC, abstractmethod
import datetime


@dataclass
class DifyConfig:
    """Configuration for Dify workflow integration"""
    api_key: str
    base_url: str
    workflow_name: str
    test_user: str = "automated_tester"
    timeout_seconds: int = 120


@dataclass
class EvaluationConfig:
    """Configuration for evaluation criteria and scoring"""
    evaluation_metrics: List[str] = field(default_factory=list)
    success_thresholds: Dict[str, float] = field(default_factory=dict)
    openai_model: str = "gpt-4o"
    openai_temperature: float = 0.1
    include_detailed_analysis: bool = True


@dataclass
class TestGenerationConfig:
    """Configuration for test data generation"""
    static_test_cases: List[Dict[str, Any]] = field(default_factory=list)
    ai_generation_enabled: bool = True
    ai_generation_prompt: str = ""
    num_ai_cases: int = 0


@dataclass
class TestConfiguration:
    """Main configuration that composes all sub-configurations"""
    
    # Component configurations
    dify_config: DifyConfig
    evaluation_config: EvaluationConfig
    generation_config: TestGenerationConfig
    
    # Test execution settings
    max_iterations: int = 8
    
    # Reporting configuration
    custom_report_sections: List[str] = field(default_factory=list)
    
    # Convenience methods for backward compatibility
    @property
    def dify_api_key(self) -> str:
        return self.dify_config.api_key
    
    @property
    def dify_base_url(self) -> str:
        return self.dify_config.base_url
    
    @property
    def workflow_name(self) -> str:
        return self.dify_config.workflow_name
    
    @property
    def evaluation_metrics(self) -> List[str]:
        return self.evaluation_config.evaluation_metrics
    
    @property
    def success_thresholds(self) -> Dict[str, float]:
        return self.evaluation_config.success_thresholds
    
    @property
    def openai_model(self) -> str:
        return self.evaluation_config.openai_model
    
    @property
    def openai_temperature(self) -> float:
        return self.evaluation_config.openai_temperature
    
    @property
    def static_test_cases(self) -> List[Dict[str, Any]]:
        return self.generation_config.static_test_cases
    
    @property
    def ai_generation_enabled(self) -> bool:
        return self.generation_config.ai_generation_enabled
    
    @property
    def test_user(self) -> str:
        return self.dify_config.test_user
    
    @property
    def timeout_seconds(self) -> int:
        return self.dify_config.timeout_seconds


@dataclass 
class EvaluationResult:
    """Standardized result from any judge evaluation"""
    
    # Basic result info
    test_identifier: str
    test_type: str
    success: bool
    timestamp: str = field(default_factory=lambda: datetime.datetime.now().isoformat())
    
    # Scoring (configurable metrics)
    scores: Dict[str, float] = field(default_factory=dict)
    
    # Detailed information
    details: Dict[str, Any] = field(default_factory=dict)
    error_categories: List[str] = field(default_factory=list)
    error_message: Optional[str] = None
    
    # Test execution metadata
    execution_metadata: Dict[str, Any] = field(default_factory=dict)
    
    # Optional raw data for debugging
    raw_input: Optional[Dict[str, Any]] = None
    raw_output: Optional[Dict[str, Any]] = None


@dataclass
class TestSuiteResult:
    """Aggregated results for a complete test suite"""
    
    test_type: str
    total_tests: int
    successful_tests: int
    failed_tests: int
    success_rate: float
    
    # Individual results
    individual_results: List[EvaluationResult] = field(default_factory=list)
    
    # Aggregated statistics
    average_scores: Dict[str, float] = field(default_factory=dict)
    score_distributions: Dict[str, Dict[str, int]] = field(default_factory=list)
    
    # Error analysis
    error_summary: Dict[str, int] = field(default_factory=dict)
    common_errors: List[str] = field(default_factory=list)
    
    # Metadata
    start_time: str = ""
    end_time: str = ""
    configuration_hash: str = ""


class BaseTestSubject(ABC):
    """Abstract base for test subjects"""
    
    def __init__(self, test_data: Dict[str, Any], config: TestConfiguration):
        self.test_data = test_data
        self.config = config
    
    @abstractmethod
    def get_test_identifier(self) -> str:
        """Get unique identifier for this test"""
        pass
    
    @abstractmethod
    def get_test_input(self) -> Dict[str, Any]:
        """Get input data for test execution"""
        pass
    
    @abstractmethod
    def get_expected_behavior(self) -> str:
        """Get description of expected behavior for evaluation"""
        pass


class TestSuite:
    """Collection of test subjects with metadata"""
    
    def __init__(self, test_type: str, config: TestConfiguration):
        self.test_type = test_type
        self.config = config
        self.test_subjects: List[BaseTestSubject] = []
        self.metadata: Dict[str, Any] = {}
    
    def add_test_subject(self, subject: BaseTestSubject):
        """Add a test subject to the suite"""
        self.test_subjects.append(subject)
    
    def get_test_subjects(self) -> List[BaseTestSubject]:
        """Get all test subjects in the suite"""
        return self.test_subjects
    
    def get_suite_summary(self) -> Dict[str, Any]:
        """Get summary of the test suite"""
        return {
            "test_type": self.test_type,
            "total_tests": len(self.test_subjects),
            "configuration": {
                "workflow": self.config.workflow_name,
                "metrics": self.config.evaluation_metrics,
                "static_cases": len(self.config.static_test_cases),
                "ai_generation": self.config.ai_generation_enabled
            },
            "metadata": self.metadata
        }
