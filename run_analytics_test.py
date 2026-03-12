import os
import sys
import pandas as pd
import importlib.util

# Set project root
PROJECT_ROOT = r"c:\Users\prasa\Downloads\avni-ai\avni-ai"

# Insert project root into sys.path
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Import analytics module directly by file path
analytics_module_path = os.path.join(PROJECT_ROOT, "dify", "analytics_tools", "analytics.py")
analytics_spec = importlib.util.spec_from_file_location("analytics", analytics_module_path)
analytics_module = importlib.util.module_from_spec(analytics_spec)
analytics_spec.loader.exec_module(analytics_module)

analyze_real_data = analytics_module.analyze_real_data
export_factual_report_csv = analytics_module.export_factual_report_csv

# Run analysis on real data file
if __name__ == "__main__":
    csv_file = os.path.join(PROJECT_ROOT, "messages_20260225_154435.csv")
    print(f"Analyzing: {csv_file}")
    
    if os.path.exists(csv_file):
        result = analyze_real_data(csv_file)
        print("\n=== Summary ===")
        for key, value in result["summary"].items():
            print(f"  {key}: {value}")
        
        # Print other key metrics
        if "cost_stats" in result:
            print("\n=== Cost Stats ===")
            print(f"  Total Cost: ${result['cost_stats'].get('total_cost', 'N/A')}")
            print("\n=== Cost by Environment ===")
            for env, cost in result["cost_stats"].get("cost_by_environment", {}).items():
                print(f"  {env}: ${cost}")
        
        if "exact_duplicates" in result and result["exact_duplicates"]:
            print("\n=== Exact Duplicates (Top 5) ===")
            for query, count in sorted(result["exact_duplicates"].items(), key=lambda x: x[1], reverse=True)[:5]:
                print(f"  '{query}': {count}")
    else:
        print(f"File not found: {csv_file}")
