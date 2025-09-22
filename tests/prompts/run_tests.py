"""
Main entry point for the Avni AI Assistant testing system.
"""

import os
import openai
from testing_system import TestingSystem


def main():
    """Main function to run the enhanced testing system"""
    # Set up API keys
    openai.api_key = os.getenv("OPENAI_API_KEY")
    dify_api_key = os.getenv("DIFY_API_KEY")

    if not openai.api_key:
        print("Error: OpenAI API key not set.")
        return

    if not dify_api_key or dify_api_key == "app-your-dify-key-here":
        print("Error: DIFY_API_KEY environment variable not set.")
        print("Please set your Dify API key to run this script.")
        return

    print("Starting Enhanced Avni AI Assistant Testing System")

    # Create and run testing system with Dify API key
    testing_system = TestingSystem(dify_api_key)

    # Run test cycles
    testing_system.run_full_test_cycles(num_cycles=2)

    # Generate and print comprehensive report
    testing_system.generate_and_print_report()


if __name__ == "__main__":
    main()
