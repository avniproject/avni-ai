"""
Main testing system that orchestrates the entire testing process.
"""

import datetime
from typing import List
from models import ConversationResult
from prompts import SCENARIO_NAMES
from ai_tester import AITester
from tests.dify.common.dify_client import DifyClient
from ai_reviewer import AIReviewer
from analytics import StatisticsCalculator, ReportGenerator


class TestingSystem:
    """Enhanced testing system with AI reviewer and comprehensive analytics"""

    def __init__(self, dify_api_key: str):
        self.tester = AITester()
        self.dify_client = DifyClient(dify_api_key)
        self.conversation_id = ""
        self.reviewer = AIReviewer()
        self.results: List[ConversationResult] = []
        self.scenarios = SCENARIO_NAMES

    def run_single_conversation(
        self, scenario_index: int, cycle: int
    ) -> ConversationResult:
        """Run a single conversation and get it reviewed"""
        # Reset the conversation for each new test
        self.conversation_id = ""

        chat_history = []
        scenario = self.scenarios[scenario_index]

        print(f"  Testing {scenario} (Cycle {cycle})")

        # Initial tester message
        next_message = self.tester.generate_message([], scenario_index)

        # Run 8 iterations of a conversation
        for iteration in range(8):
            print(f"    Iteration {iteration + 1}/8")

            # Get assistant response via Dify
            response = self.dify_client.send_message(
                query=next_message,
                conversation_id=self.conversation_id,
            )

            if response["success"]:
                self.conversation_id = response["conversation_id"]
                ai_response = response["answer"]
            else:
                print(f"Dify API error: {response.get('error', 'Unknown error')}")
                ai_response = "Sorry, I encountered an error."

            # Record this exchange in our local history for the reviewer
            chat_history.append({"role": "user", "content": next_message})
            chat_history.append({"role": "assistant", "content": ai_response})

            if iteration < 7:
                # Generate next tester message - flip roles for tester's perspective
                # From tester's view: assistant messages are "user" inputs, tester messages are "assistant" responses
                tester_history = []
                for msg in chat_history:
                    if msg["role"] == "user":  # Tester's previous message
                        tester_history.append(
                            {"role": "assistant", "content": msg["content"]}
                        )
                    elif (
                        msg["role"] == "assistant"
                    ):  # Dify's response becomes input to tester
                        tester_history.append(
                            {"role": "user", "content": msg["content"]}
                        )

                next_message = self.tester.generate_message(
                    tester_history, scenario_index
                )

        # Get AI reviewer analysis
        print("    Analyzing conversation...")
        analysis = self.reviewer.analyze_conversation(chat_history, scenario)

        return ConversationResult(
            cycle=cycle,
            scenario=scenario,
            scenario_index=scenario_index,
            conversation=chat_history,
            reviewer_analysis=analysis,
            timestamp=datetime.datetime.now().isoformat(),
        )

    def run_full_test_cycles(self, num_cycles: int = 5) -> None:
        """Run full test cycles across all scenarios"""
        print(
            f"Starting {num_cycles} test cycles across {len(self.scenarios)} scenarios"
        )
        print(f"Total conversations: {num_cycles * len(self.scenarios)}")

        for cycle in range(1, num_cycles + 1):
            print(f"\n CYCLE {cycle}/{num_cycles}")

            for scenario_index in range(len(self.scenarios)):
                result = self.run_single_conversation(scenario_index, cycle)
                self.results.append(result)

        print(f"\n Completed all {num_cycles} cycles!")

    def generate_and_print_report(self) -> None:
        """Calculate statistics and print comprehensive report"""
        print("\n Calculating comprehensive statistics...")
        statistics = StatisticsCalculator.calculate_statistics(self.results)

        print("\n COMPREHENSIVE TEST REPORT")
        report = ReportGenerator.generate_report(statistics, self.results)
        print(report)
