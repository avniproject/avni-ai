"""
Debug script to test a single Spec Agent scenario with detailed logging.
"""

import json
import logging
import os
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent))

from tests.judge_framework.implementations.specAgent import (
    SpecAgentTestSubjectFactory,
    SpecAgentExecutor,
)
from tests.judge_framework.examples.run_spec_agent_tests import (
    create_test_configuration,
)

# Set up detailed logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)


def main():
    """Run a single test with detailed logging."""
    # Create config
    config = create_test_configuration()

    # Load entities
    entities_file = Path(__file__).parent.parent.parent.parent / "resources" / "scoping" / "entities_summary.json"
    
    logger.info(f"Loading entities from: {entities_file}")
    
    # Create factory
    factory = SpecAgentTestSubjectFactory(str(entities_file))
    
    # Create a simple test case
    test_case = {
        "scenario": "debug_test",
        "description": "Debug test with full entities",
        "entities_filter": "full",
        "conversation_vars": {
            "org_name": "Durga India",
            "user_name": "Test User",
            "setup_mode_active": True,
            "spec_yaml": "",
            "query": "I've uploaded the scoping documents. Please generate the spec.",
        },
        "expected_behavior": {
            "should_call_generate_spec": True,
            "should_call_validate_spec": True,
        },
    }
    
    # Create test subject
    logger.info("Creating test subject...")
    subject = factory.create_from_static_data(test_case, config)
    
    # Get test input
    test_input = subject.get_test_input()
    
    logger.info("=" * 80)
    logger.info("TEST INPUT DETAILS")
    logger.info("=" * 80)
    logger.info(f"Query: {test_input['query']}")
    logger.info(f"\nInputs keys: {list(test_input['inputs'].keys())}")
    
    # Log entities_jsonl length
    entities_jsonl = test_input['inputs'].get('entities_jsonl', '')
    logger.info(f"\nentities_jsonl length: {len(entities_jsonl)} chars")
    logger.info(f"entities_jsonl preview (first 200 chars):\n{entities_jsonl[:200]}")
    
    # Log other important inputs
    logger.info(f"\nsetup_mode_active: {test_input['inputs'].get('setup_mode_active')}")
    logger.info(f"avni_mcp_server_url: {test_input['inputs'].get('avni_mcp_server_url')}")
    logger.info(f"org_name: {test_input['inputs'].get('org_name')}")
    
    # Execute test
    logger.info("\n" + "=" * 80)
    logger.info("EXECUTING TEST")
    logger.info("=" * 80)
    
    executor = SpecAgentExecutor(config)
    result = executor.execute(test_input)
    
    logger.info("\n" + "=" * 80)
    logger.info("TEST RESULT")
    logger.info("=" * 80)
    logger.info(f"Success: {result.get('success')}")
    logger.info(f"Conversation ID: {result.get('conversation_id')}")
    logger.info(f"Tool calls: {len(result.get('tool_calls', []))}")
    logger.info(f"Agent response length: {len(result.get('agent_response', ''))} chars")
    logger.info(f"\nAgent response preview (first 500 chars):\n{result.get('agent_response', '')[:500]}")
    
    if result.get('tool_calls'):
        logger.info(f"\nTool calls made:")
        for i, call in enumerate(result.get('tool_calls', []), 1):
            logger.info(f"  {i}. {call.get('name', 'unknown')}")
    else:
        logger.warning("\n⚠️  NO TOOL CALLS MADE - Agent did not call generate_spec or validate_spec!")
    
    if result.get('error'):
        logger.error(f"\nError: {result.get('error')}")
    
    return 0 if result.get('success') else 1


if __name__ == "__main__":
    sys.exit(main())
