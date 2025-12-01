#!/usr/bin/env python3
"""
Dify Data Extractor
===================

A script to extract conversation and message data from Dify API.

Usage:
1. Update the configuration values below
2. Run: python3 dify_data_extractor.py
"""

import requests
import csv
import json
from datetime import datetime
import argparse
from typing import List, Dict, Any
import time

# =============================================================================
# CONFIGURATION - UPDATE THESE VALUES
# =============================================================================

# Authentication tokens (update these with your actual values)
CSRF_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NjQxNTkyNDIsInN1YiI6ImIyODlmZmMwLTNmNTYtNDYxOS05OTE5LTVlYjIxYzFkNjk2YyJ9.JbtKlDG6KS8PlgsHdO3cqjNstFOWF0OJqM5uQdNXJII"

COOKIES = "cookieyes-consent=consentid:THl1cnRLYVhpZ1dJVUxsMDhpSklMN3JEbTRSUDIzUU8,consent:no,action:,necessary:yes,functional:no,analytics:no,performance:no,advertisement:no,other:no; __Host-csrf_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NjQxNTkyNDIsInN1YiI6ImIyODlmZmMwLTNmNTYtNDYxOS05OTE5LTVlYjIxYzFkNjk2YyJ9.JbtKlDG6KS8PlgsHdO3cqjNstFOWF0OJqM5uQdNXJII; __Host-access_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiYjI4OWZmYzAtM2Y1Ni00NjE5LTk5MTktNWViMjFjMWQ2OTZjIiwiZXhwIjoxNzY0MTU5MjQyLCJpc3MiOiJDTE9VRCIsInN1YiI6IkNvbnNvbGUgQVBJIFBhc3Nwb3J0In0.JeyVq3234-FFS5ZuRrLYMGVhNBvIFbHp59LOdinYVdM; __Host-refresh_token=828209a515330d6528b645c10d47e90f2ba69b77c749ea2ab6b3afb26759080dbb0b9ac21b0f0af9f31b9294f278bef1223f1b8dcbe61d36a82a87d0a5beb379"

BAGGAGE = "sentry-environment=production,sentry-public_key=c0bcc0e36783694f41e4fb1e6a3efea9,sentry-trace_id=2a09ba8e279f44678d71c11831bab59c,sentry-sample_rate=0.1,sentry-sampled=false"

# Date range for conversation retrieval
START_DATE = "2025-08-19 00:00"
END_DATE = "2025-11-26 23:59"

# Output settings
OUTPUT_FORMAT = "csv"  # Options: "csv", "json", "both" - set to csv only
OUTPUT_DIR = "."  # Directory to save files
ADD_TIMESTAMP = True  # Add timestamp to filenames

# Request settings
DELAY_BETWEEN_REQUESTS = 0.5  # Seconds to wait between requests

# =============================================================================
# END CONFIGURATION
# =============================================================================


class DifyDataExtractor:
    def __init__(self, csrf_token: str, cookies: str, baggage: str):
        """
        Initialize the extractor with authentication headers

        Args:
            csrf_token: X-CSRF-Token value
            cookies: Cookie header value
            baggage: Baggage header value
        """
        self.base_url = "https://cloud.dify.ai/console/api/apps/31143de1-fbca-4692-9897-badc6a40daff"
        self.headers = {
            "accept": "*/*",
            "accept-language": "en-GB,en;q=0.7",
            "baggage": baggage,
            "content-type": "application/json",
            "x-csrf-token": csrf_token,
            "Cookie": cookies,
        }

    def get_all_conversations(
        self, start_date: str, end_date: str
    ) -> List[Dict[str, Any]]:
        """
        Get all conversations from all pages

        Args:
            start_date: Start date in format "YYYY-MM-DD HH:MM"
            end_date: End date in format "YYYY-MM-DD HH:MM"

        Returns:
            List of all conversation data
        """
        all_conversations = []
        page = 1
        limit = 100  # Use larger page size for efficiency

        while True:
            print(f"Fetching conversations page {page}...")

            url = f"{self.base_url}/chat-conversations"
            params = {
                "page": page,
                "limit": limit,
                "start": start_date,
                "end": end_date,
                "sort_by": "-created_at",
                "annotation_status": "all",
            }

            try:
                response = requests.get(url, headers=self.headers, params=params)
                response.raise_for_status()
                data = response.json()

                conversations = data.get("data", [])

                if not conversations:
                    print(f"No more conversations found on page {page}")
                    break

                print(f"Found {len(conversations)} conversations on page {page}")

                for item in conversations:
                    conversation = {
                        "id": item.get("id"),
                        "from_end_user_id": item.get("from_end_user_id"),
                        "name": item.get("name"),
                        "summary": item.get("summary"),
                        "message_count": item.get("message_count"),
                        "user_feedback_stats": json.dumps(
                            item.get("user_feedback_stats", {})
                        ),
                        "admin_feedback_stats": json.dumps(
                            item.get("admin_feedback_stats", {})
                        ),
                        "status_count": json.dumps(item.get("status_count", {})),
                        "status": item.get("status"),
                        "from_source": item.get("from_source"),
                        "created_at": item.get("created_at"),
                        "updated_at": item.get("updated_at"),
                    }
                    all_conversations.append(conversation)

                # Check if there are more pages
                has_more = data.get("has_more", False)
                if not has_more:
                    print("Reached last page of conversations")
                    break

                page += 1

                # Add delay between requests
                if DELAY_BETWEEN_REQUESTS > 0:
                    time.sleep(DELAY_BETWEEN_REQUESTS)

            except requests.exceptions.RequestException as e:
                print(f"Error fetching conversations page {page}: {e}")
                break

        print(f"Total conversations fetched: {len(all_conversations)}")
        return all_conversations

    def get_all_chat_messages(self, conversation_id: str) -> List[Dict[str, Any]]:
        """
        Get all chat messages for a specific conversation

        Args:
            conversation_id: The conversation ID

        Returns:
            List of all message data for the conversation
        """
        all_messages = []
        limit = 100  # Use larger page size for efficiency

        url = f"{self.base_url}/chat-messages"
        params = {"conversation_id": conversation_id, "limit": limit}

        try:
            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            data = response.json()

            messages = data.get("data", [])

            for item in messages:
                inputs = item.get("inputs", {}) or {}
                metadata = item.get("metadata", {}) or {}
                usage = metadata.get("usage", {}) or {}

                message = {
                    "conversation_id": conversation_id,
                    "message_id": item.get("id"),
                    "org_name": inputs.get("org_name"),
                    "org_type": inputs.get("org_type"),
                    "user_name": inputs.get("user_name"),
                    "query": item.get("query"),
                    "answer": item.get("answer"),
                    "message_tokens": item.get("message_tokens"),
                    "answer_tokens": item.get("answer_tokens"),
                    "provider_response_latency": item.get("provider_response_latency"),
                    "from_source": item.get("from_source"),
                    "from_end_user_id": item.get("from_end_user_id"),
                    "status": item.get("status"),
                    "created_at": item.get("created_at"),
                    "prompt_tokens": usage.get("prompt_tokens"),
                    "completion_tokens": usage.get("completion_tokens"),
                    "total_tokens": usage.get("total_tokens"),
                    "total_price": usage.get("total_price"),
                    "currency": usage.get("currency"),
                    "latency": usage.get("latency"),
                    "time_to_first_token": usage.get("time_to_first_token"),
                    "time_to_generate": usage.get("time_to_generate"),
                }
                all_messages.append(message)

        except requests.exceptions.RequestException as e:
            print(f"Error fetching messages for conversation {conversation_id}: {e}")

        return all_messages

    def extract_all_data(
        self, start_date: str, end_date: str, delay: float = 0.5
    ) -> Dict[str, List[Dict[str, Any]]]:
        """
        Extract all data from both endpoints

        Args:
            start_date: Start date for conversations
            end_date: End date for conversations
            delay: Delay between requests in seconds

        Returns:
            Dictionary containing conversations and messages data
        """
        print("Starting data extraction...")
        print(f"Date range: {start_date} to {end_date}")

        # Get all conversations
        conversations = self.get_all_conversations(start_date, end_date)

        if not conversations:
            print("No conversations found")
            return {"conversations": [], "messages": []}

        print(f"\nFetching messages for {len(conversations)} conversations...")

        all_messages = []
        for i, conv in enumerate(conversations):
            conv_id = conv["id"]
            print(f"Processing conversation {i + 1}/{len(conversations)}: {conv_id}")

            messages = self.get_all_chat_messages(conv_id)
            all_messages.extend(messages)

            print(f"  Found {len(messages)} messages")

            # Add delay between requests
            if delay > 0 and i < len(conversations) - 1:
                time.sleep(delay)

        print("\nExtraction completed!")
        print(f"Total conversations: {len(conversations)}")
        print(f"Total messages: {len(all_messages)}")

        return {"conversations": conversations, "messages": all_messages}

    def save_to_csv(
        self,
        data: Dict[str, List[Dict[str, Any]]],
        output_dir: str = ".",
        timestamp: bool = True,
    ):
        """
        Save extracted data to CSV files

        Args:
            data: Dictionary containing conversations and messages
            output_dir: Directory to save files
            timestamp: Whether to add timestamp to filenames
        """
        timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S") if timestamp else ""

        # Save conversations
        conv_filename = (
            f"conversations_{timestamp_str}.csv"
            if timestamp_str
            else "conversations.csv"
        )
        conv_filepath = f"{output_dir}/{conv_filename}"

        if data["conversations"]:
            with open(conv_filepath, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=data["conversations"][0].keys())
                writer.writeheader()
                writer.writerows(data["conversations"])
            print(f"Conversations saved to: {conv_filepath}")

        # Save messages
        msg_filename = (
            f"messages_{timestamp_str}.csv" if timestamp_str else "messages.csv"
        )
        msg_filepath = f"{output_dir}/{msg_filename}"

        if data["messages"]:
            with open(msg_filepath, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=data["messages"][0].keys())
                writer.writeheader()
                writer.writerows(data["messages"])
            print(f"Messages saved to: {msg_filepath}")

    def save_to_json(
        self,
        data: Dict[str, List[Dict[str, Any]]],
        output_dir: str = ".",
        timestamp: bool = True,
    ):
        """
        Save extracted data to JSON files

        Args:
            data: Dictionary containing conversations and messages
            output_dir: Directory to save files
            timestamp: Whether to add timestamp to filenames
        """
        timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S") if timestamp else ""
        filename = (
            f"dify_data_{timestamp_str}.json" if timestamp_str else "dify_data.json"
        )
        filepath = f"{output_dir}/{filename}"

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        print(f"All data saved to JSON: {filepath}")


def main():
    """Main execution function"""
    print("Dify Data Extractor")
    print("==================")
    print()

    # Create extractor instance
    extractor = DifyDataExtractor(CSRF_TOKEN, COOKIES, BAGGAGE)

    # Extract all data
    data = extractor.extract_all_data(
        start_date=START_DATE, end_date=END_DATE, delay=DELAY_BETWEEN_REQUESTS
    )

    # Save data as CSV only
    print("\nSaving data as CSV files...")

    extractor.save_to_csv(data, OUTPUT_DIR, ADD_TIMESTAMP)

    print("\nData extraction completed successfully!")
    print(f"Total conversations: {len(data['conversations'])}")
    print(f"Total messages: {len(data['messages'])}")


def main_with_args():
    """Command line interface"""
    parser = argparse.ArgumentParser(description="Extract data from Dify API")
    parser.add_argument("--csrf-token", help="X-CSRF-Token value")
    parser.add_argument("--cookies", help="Cookie header value")
    parser.add_argument("--baggage", help="Baggage header value")
    parser.add_argument("--start-date", help="Start date (YYYY-MM-DD HH:MM)")
    parser.add_argument("--end-date", help="End date (YYYY-MM-DD HH:MM)")
    parser.add_argument("--output-dir", default=".", help="Output directory")
    parser.add_argument(
        "--format",
        choices=["csv", "json", "both"],
        default="both",
        help="Output format",
    )
    parser.add_argument(
        "--delay", type=float, default=0.5, help="Delay between requests in seconds"
    )
    parser.add_argument(
        "--no-timestamp", action="store_true", help="Do not add timestamp to filenames"
    )

    args = parser.parse_args()

    # Use command line args if provided, otherwise use config values
    csrf_token = args.csrf_token or CSRF_TOKEN
    cookies = args.cookies or COOKIES
    baggage = args.baggage or BAGGAGE
    start_date = args.start_date or START_DATE
    end_date = args.end_date or END_DATE
    output_dir = args.output_dir
    output_format = args.format
    delay = args.delay
    add_timestamp = not args.no_timestamp

    # Create extractor instance
    extractor = DifyDataExtractor(csrf_token, cookies, baggage)

    # Extract data
    data = extractor.extract_all_data(start_date, end_date, delay)

    # Save data
    if output_format in ["csv", "both"]:
        extractor.save_to_csv(data, output_dir, add_timestamp)

    if output_format in ["json", "both"]:
        extractor.save_to_json(data, output_dir, add_timestamp)

    print("\nExtraction completed successfully!")
    print(f"Total conversations: {len(data['conversations'])}")
    print(f"Total messages: {len(data['messages'])}")


if __name__ == "__main__":
    import sys

    # If command line arguments are provided, use CLI mode
    if len(sys.argv) > 1:
        main_with_args()
    else:
        # Otherwise use config values from top of file
        main()
