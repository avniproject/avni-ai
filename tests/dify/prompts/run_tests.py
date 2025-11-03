"""
Main entry point for the Avni AI Assistant testing system.
"""

import os
import sys
import openai
from .testing_system import TestingSystem
from dotenv import load_dotenv

from ..common.utils import validate_all_env_variables

load_dotenv()


def main():
    """Main function to run the enhanced testing system"""
    if not validate_all_env_variables():
        sys.exit(1)

    # Set up API keys
    openai.api_key = os.getenv("OPENAI_API_KEY")
    dify_api_key = os.getenv("DIFY_API_KEY")

    print("Starting Enhanced Avni AI Assistant Testing System")

    testing_system = TestingSystem(dify_api_key)

    # Run test cycles
    testing_system.run_full_test_cycles(num_cycles=5)

    # Generate and print comprehensive report
    testing_system.generate_and_print_report()


if __name__ == "__main__":
    main()
