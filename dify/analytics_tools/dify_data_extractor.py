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
import os

# =============================================================================
# CONFIGURATION - UPDATE THESE VALUES OR SET ENVIRONMENT VARIABLES
# =============================================================================

import os

# Authentication tokens (update these with your actual values or set environment variables)
# To get fresh tokens:
# 1. Log into Dify at https://cloud.dify.ai
# 2. Open Developer Tools (F12) > Network tab
# 3. Perform an action (e.g., view apps)
# 4. Find a request to /console/api/apps
# 5. Copy the headers: X-CSRF-Token, Cookie, and Baggage
CSRF_TOKEN = os.getenv("DIFY_CSRF_TOKEN", "your_csrf_token_here")
COOKIES = os.getenv("DIFY_COOKIES", "your_cookies_here")
BAGGAGE = os.getenv("DIFY_BAGGAGE", "your_baggage_here")

# Date range for conversation retrieval
START_DATE = None  # Set to None to fetch all conversations
END_DATE = None

# Output settings
OUTPUT_FORMAT = "csv"  # Options: "csv", "json", "both" - set to csv only
OUTPUT_DIR = "../.."  # Directory to save files (relative to analytics_tools)
ADD_TIMESTAMP = True  # Add timestamp to filenames

# Request settings
DELAY_BETWEEN_REQUESTS = 1.0  # Seconds to wait between requests
MAX_RETRIES = 3  # Maximum number of retries on failure
RETRY_DELAY = 2  # Seconds to wait before retrying

# =============================================================================
# END CONFIGURATION
# =============================================================================


def make_request_with_retry(url: str, headers: dict, params: dict = None, max_retries: int = MAX_RETRIES, retry_delay: float = RETRY_DELAY) -> requests.Response:
    """
    Make a GET request with retry logic
    
    Args:
        url: The URL to request
        headers: Request headers
        params: Query parameters
        max_retries: Maximum number of retries
        retry_delay: Delay between retries in seconds
    
    Returns:
        Response object
    
    Raises:
        requests.exceptions.RequestException: If all retries fail
    """
    for attempt in range(max_retries + 1):
        try:
            response = requests.get(url, headers=headers, params=params, timeout=30)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            if attempt < max_retries:
                print(f"Request failed (attempt {attempt + 1}/{max_retries + 1}): {e}")
                time.sleep(retry_delay)
            else:
                raise e


class DifyDataExtractor:
    def __init__(self, csrf_token: str, cookies: str, baggage: str):
        """
        Initialize the extractor with authentication headers

        Args:
            csrf_token: X-CSRF-Token value
            cookies: Cookie header value
            baggage: Baggage header value
        """
        # Strip whitespace from tokens
        csrf_token = csrf_token.strip() if csrf_token else ""
        cookies = cookies.strip() if cookies else ""
        baggage = baggage.strip() if baggage else ""
        
        if not csrf_token or csrf_token == "your_csrf_token_here":
            raise ValueError("CSRF_TOKEN is not set. Please set the DIFY_CSRF_TOKEN environment variable or update the config.")
        if not cookies or cookies == "your_cookies_here":
            raise ValueError("COOKIES is not set. Please set the DIFY_COOKIES environment variable or update the config.")
        
        self.base_url = "https://cloud.dify.ai/console/api"
        self.headers = {
            "accept": "application/json",
            "accept-language": "en-GB,en;q=0.7",
            "content-type": "application/json",
            "x-csrf-token": csrf_token,
            "Cookie": cookies,
        }
        if baggage and baggage != "your_baggage_here":
            self.headers["baggage"] = baggage

    def validate_tokens(self) -> bool:
        """
        Validate authentication tokens by making a test request

        Returns:
            True if tokens are valid, False otherwise
        """
        try:
            response = make_request_with_retry(f"{self.base_url}/apps", self.headers, max_retries=1, retry_delay=0)
            return response.status_code == 200
        except:
            return False

    def get_all_apps(self) -> List[Dict[str, Any]]:
        """
        Get all apps from Dify

        Returns:
            List of app data
        """
        url = f"{self.base_url}/apps"
        try:
            response = make_request_with_retry(url, self.headers)
            data = response.json()
            return data.get("data", [])
        except requests.exceptions.RequestException as e:
            print(f"Error fetching apps: {e}")
            if hasattr(e, 'response') and e.response:
                print(f"Response status: {e.response.status_code}")
                print(f"Response text: {e.response.text}")
            return []

    def get_all_conversations(
        self, app_id: str, start_date: str = None, end_date: str = None
    ) -> List[Dict[str, Any]]:
        """
        Get all conversations from all pages for a specific app

        Args:
            app_id: The app ID
            start_date: Start date in format "YYYY-MM-DD HH:MM" (optional)
            end_date: End date in format "YYYY-MM-DD HH:MM" (optional)

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
                "app_id": app_id,
                "page": page,
                "limit": limit,
                "sort_by": "-created_at",
                "annotation_status": "all",
            }
            if start_date:
                params["start"] = start_date
            if end_date:
                params["end"] = end_date

            try:
                response = make_request_with_retry(url, self.headers, params=params)
                data = response.json()

                conversations = data.get("data", [])

                if not conversations:
                    print(f"No more conversations found on page {page}")
                    break

                print(f"Found {len(conversations)} conversations on page {page}")

                for item in conversations:
                    conversation = {
                        "app_id": app_id,
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
                if hasattr(e, 'response') and e.response:
                    print(f"Response status: {e.response.status_code}")
                    print(f"Response text: {e.response.text}")
                break

        print(f"Total conversations fetched: {len(all_conversations)}")
        return all_conversations

    def get_all_chat_messages(self, app_id: str, conversation_id: str) -> List[Dict[str, Any]]:
        """
        Get all chat messages for a specific conversation in a specific app

        Args:
            app_id: The app ID
            conversation_id: The conversation ID

        Returns:
            List of all message data for the conversation
        """
        all_messages = []
        page = 1
        limit = 100  # Use larger page size for efficiency

        while True:
            url = f"{self.base_url}/chat-messages"
            params = {"app_id": app_id, "conversation_id": conversation_id, "limit": limit, "page": page}

            try:
                response = make_request_with_retry(url, self.headers, params=params)
                data = response.json()

                messages = data.get("data", [])

                if not messages:
                    break

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

                # Check if there are more pages
                has_more = data.get("has_more", False)
                if not has_more:
                    break

                page += 1

                # Add delay between requests
                if DELAY_BETWEEN_REQUESTS > 0:
                    time.sleep(DELAY_BETWEEN_REQUESTS)

            except requests.exceptions.RequestException as e:
                print(f"Error fetching messages for conversation {conversation_id}: {e}")
                if hasattr(e, 'response') and e.response:
                    print(f"Response status: {e.response.status_code}")
                    print(f"Response text: {e.response.text}")
                break

        return all_messages

    def extract_all_data(
        self, start_date: str = None, end_date: str = None, delay: float = 0.5
    ) -> Dict[str, List[Dict[str, Any]]]:
        """
        Extract all data from both endpoints for all apps

        Args:
            start_date: Start date for conversations (optional)
            end_date: End date for conversations (optional)
            delay: Delay between requests in seconds

        Returns:
            Dictionary containing conversations and messages data
        """
        print("Starting data extraction...")
        if start_date and end_date:
            print(f"Date range: {start_date} to {end_date}")
        else:
            print("Fetching all conversations (no date filter)")

        # Get all apps
        apps = self.get_all_apps()
        if not apps:
            print("No apps found")
            return {"conversations": [], "messages": []}

        print(f"Found {len(apps)} apps")

        all_conversations = []
        all_messages = []

        for app in apps:
            app_id = app.get("id")
            app_name = app.get("name", "Unknown")
            print(f"\nProcessing app: {app_name} ({app_id})")

            # Get conversations for this app
            conversations = self.get_all_conversations(app_id, start_date, end_date)
            all_conversations.extend(conversations)

            if not conversations:
                print(f"No conversations found for app {app_name}")
                continue

            print(f"Fetching messages for {len(conversations)} conversations in app {app_name}...")

            for i, conv in enumerate(conversations):
                conv_id = conv["id"]
                print(f"Processing conversation {i + 1}/{len(conversations)}: {conv_id}")

                messages = self.get_all_chat_messages(app_id, conv_id)
                all_messages.extend(messages)

                print(f"  Found {len(messages)} messages")

                # Add delay between requests
                if delay > 0 and i < len(conversations) - 1:
                    time.sleep(delay)

        print("\nExtraction completed!")
        print(f"Total conversations: {len(all_conversations)}")
        print(f"Total messages: {len(all_messages)}")

        return {"conversations": all_conversations, "messages": all_messages}

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

    try:
        # Create extractor instance
        extractor = DifyDataExtractor(CSRF_TOKEN, COOKIES, BAGGAGE)
        
        # Validate tokens
        print("Validating authentication tokens...")
        if not extractor.validate_tokens():
            print("ERROR: Authentication tokens are invalid or expired.")
            print("Please update the tokens:")
            print("1. Log into Dify at https://cloud.dify.ai")
            print("2. Open Developer Tools (F12) > Network tab")
            print("3. Perform an action (e.g., view apps)")
            print("4. Find a request to /console/api/apps")
            print("5. Copy the headers: X-CSRF-Token, Cookie, and Baggage")
            print("6. Set environment variables: DIFY_CSRF_TOKEN, DIFY_COOKIES, DIFY_BAGGAGE")
            print("   Or update the config values in the script.")
            return
        
        print("Tokens validated successfully.")
        
        # Extract all data
        data = extractor.extract_all_data(delay=DELAY_BETWEEN_REQUESTS)

        # Save data as CSV only
        print("\nSaving data as CSV files...")

        extractor.save_to_csv(data, OUTPUT_DIR, ADD_TIMESTAMP)

        print("\nData extraction completed successfully!")
        print(f"Total conversations: {len(data['conversations'])}")
        print(f"Total messages: {len(data['messages'])}")
    
    except ValueError as e:
        print(f"Configuration error: {e}")
        print("Please set the required environment variables or update the config values.")


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
    start_date = args.start_date if args.start_date is not None else START_DATE
    end_date = args.end_date if args.end_date is not None else END_DATE
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
