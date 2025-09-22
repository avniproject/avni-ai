"""
Data models for the Avni AI Assistant testing system.
"""

from dataclasses import dataclass
from typing import Dict, List, Any


@dataclass
class ConversationResult:
    """Data class to store conversation results and analysis"""

    cycle: int
    scenario: str
    scenario_index: int
    conversation: List[Dict[str, str]]
    reviewer_analysis: Dict[str, Any]
    timestamp: str


@dataclass
class TestStatistics:
    """Data class to store comprehensive test statistics"""

    total_cycles: int
    scenarios_tested: List[str]
    accuracy_by_scenario: Dict[str, float]
    consistency_scores: Dict[str, List[float]]
    error_categories: Dict[str, int]
