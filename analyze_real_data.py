#!/usr/bin/env python3
"""
Analyze the real messages CSV file and generate a report.
This script analyzes the actual data from messages_20260225_154435.csv
"""

import os
import sys

# Add project root to path
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from dify.analytics_tools.analytics import analyze_real_data, export_factual_report_csv


def main():
    # Path to the actual data file
    csv_file = os.path.join(PROJECT_ROOT, "messages_20260225_154435.csv")
    
    print(f"Analyzing file: {csv_file}")
    print("=" * 60)
    
    # Check if file exists
    if not os.path.exists(csv_file):
        print(f"ERROR: File not found: {csv_file}")
        return
    
    # Analyze the data
    result = analyze_real_data(csv_file)
    
    # Print summary
    print("\n📊 ANALYTICS SUMMARY")
    print("=" * 60)
    
    summary = result["summary"]
    print(f"\nMessages Summary:")
    print(f"  - Total Messages: {summary['total_messages']}")
    print(f"  - Total Conversations: {summary['total_conversations']}")
    print(f"  - Unique Users: {summary['unique_users']}")
    print(f"  - Unique Organizations: {summary['unique_organizations']}")
    print(f"  - Date Range: {summary['date_range_days']} days")
    print(f"  - Messages per Day: {summary['messages_per_day']:.2f}")
    
    print(f"\n💰 Cost Analysis:")
    cost = result["cost_stats"]
    print(f"  - Total Cost: ${cost['total_cost']:.6f}")
    print(f"  - Avg Cost per Message: ${cost['avg_cost_per_message']:.6f}")
    print(f"  - Cost by Environment:")
    for env, cost_val in cost['cost_by_environment'].items():
        print(f"      {env}: ${cost_val:.6f}")
    
    print(f"\n🔤 Token Usage:")
    tokens = result["token_stats"]
    print(f"  - Total Prompt Tokens: {tokens['total_prompt_tokens']}")
    print(f"  - Total Completion Tokens: {tokens['total_completion_tokens']}")
    print(f"  - Total Tokens: {tokens['total_tokens']}")
    print(f"  - Avg Tokens per Message: {tokens['avg_tokens_per_message']:.2f}")
    
    print(f"\n⚡ Performance:")
    perf = result["performance_stats"]
    print(f"  - Avg Response Time: {perf['avg_response_time']:.3f}s")
    print(f"  - Median Response Time: {perf['median_response_time']:.3f}s")
    print(f"  - Min Response Time: {perf['min_response_time']:.3f}s")
    print(f"  - Max Response Time: {perf['max_response_time']:.3f}s")
    
    print(f"\n🏢 Top Organizations:")
    for org, count in list(result["top_organizations"].items())[:5]:
        print(f"  - {org}: {count} messages")
    
    print(f"\n👤 Top Users:")
    for user, count in list(result["top_users"].items())[:5]:
        print(f"  - {user}: {count} messages")
    
    if result["exact_duplicates"]:
        print(f"\n🔄 Duplicate Queries:")
        for query, count in result["exact_duplicates"].items():
            print(f"  - '{query}': {count} times")
    
    # Export to CSV
    output_file = os.path.join(PROJECT_ROOT, "analytics_report.csv")
    export_path = export_factual_report_csv(result, output_file=output_file)
    print(f"\n✅ Report exported to: {export_path}")
    
    print("\n" + "=" * 60)
    print("Analysis complete!")


if __name__ == "__main__":
    main()
