import os
import sys
import pandas as pd
import tempfile
import pytest
import importlib.util

# Get project root
PROJECT_ROOT = r"c:\Users\prasa\Downloads\avni-ai\avni-ai"

# Insert project root at the beginning of sys.path
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Remove tests/dify from path if present - it shadows the real dify module
tests_dir = os.path.join(PROJECT_ROOT, "tests")
if tests_dir in sys.path:
    sys.path.remove(tests_dir)

# Also clear any cached dify modules from tests/dify
for mod in list(sys.modules.keys()):
    if mod.startswith('tests.dify') or (mod == 'dify' and 'analytics_tools' not in str(sys.modules.get(mod, ''))):
        try:
            del sys.modules[mod]
        except:
            pass

# Debug: print path info when run directly
if __name__ == "__main__":
    print(f"Project root: {PROJECT_ROOT}")
    print(f"sys.path: {sys.path[:3]}")

# Import analytics module directly by file path
analytics_module_path = os.path.join(PROJECT_ROOT, "dify", "analytics_tools", "analytics.py")
analytics_spec = importlib.util.spec_from_file_location("analytics", analytics_module_path)
analytics_module = importlib.util.module_from_spec(analytics_spec)
analytics_spec.loader.exec_module(analytics_module)

analyze_real_data = analytics_module.analyze_real_data
export_factual_report_csv = analytics_module.export_factual_report_csv


def _make_sample_csv(path):
    # a small data set covering most of the branches in analyze_real_data
    df = pd.DataFrame(
        {
            "conversation_id": [1, 1, 2],
            "user_name": ["Alice", "Alice", "Bob"],
            "org_name": ["OrgA", "OrgA", "OrgB"],
            "org_type": ["prod", "prod", "dev"],
            "created_at": [1609459200, 1609459260, 1609545600],  # two messages on day 1, one on day 2
            "query": ["hi", "hi", "hello"],
            "answer": ["hey", "hey", "hey"],
            "provider_response_latency": [0.1, 0.2, 0.3],
            "prompt_tokens": [10, 10, 20],
            "completion_tokens": [20, 20, 30],
            "total_tokens": [30, 30, 50],
            "total_price": [0.01, 0.01, 0.02],
        }
    )
    df.to_csv(path, index=False)


def test_basic_analysis(tmp_path):
    """Verify that the output dictionary contains all expected keys and
    calculates simple statistics correctly."""
    csv_path = str(tmp_path / "sample.csv")
    _make_sample_csv(csv_path)

    result = analyze_real_data(csv_path)

    # summary
    assert result["summary"]["total_messages"] == 3
    assert result["summary"]["total_conversations"] == 2
    assert result["summary"]["unique_users"] == 2
    assert result["summary"]["unique_organizations"] == 2

    # duplicates
    assert result["exact_duplicates"].get("hi") == 2

    # cost by environment should have both prod and dev
    assert set(result["cost_stats"]["cost_by_environment"].keys()) == {"prod", "dev"}


def test_determinism(tmp_path):
    """Running analysis multiple times on the same file should produce
    identical results.  This captures a baseline so we notice when the
    implementation changes and causes test instability."""
    csv_path = tmp_path / "sample.csv"
    _make_sample_csv(csv_path)

    baseline = analyze_real_data(str(csv_path))
    second = analyze_real_data(str(csv_path))
    assert baseline == second


def test_empty_input_raises(tmp_path):
    """An empty CSV should complain rather than silently produce garbage.
    This is one of the error patterns we want to guard against."""
    empty = tmp_path / "empty.csv"
    # create an empty file with headers only
    pd.DataFrame(columns=["conversation_id"]).to_csv(empty, index=False)

    with pytest.raises(Exception):
        analyze_real_data(str(empty))


def test_missing_columns_error(tmp_path):
    """If required columns are missing the function currently blows up;
    the test ensures we notice if that behaviour changes in the future."""
    bad = tmp_path / "bad.csv"
    pd.DataFrame({"foo": [1, 2, 3]}).to_csv(bad, index=False)

    with pytest.raises(KeyError):
        analyze_real_data(str(bad))


def test_export_report_creates_file(tmp_path):
    """Export produces a CSV with a few well-known sections."""
    csv_path = tmp_path / "sample.csv"
    _make_sample_csv(csv_path)
    data = analyze_real_data(str(csv_path))

    output = tmp_path / "out.csv"
    returned = export_factual_report_csv(data, output_file=str(output))

    assert os.path.exists(returned)
    text = open(returned, "r", encoding="utf-8").read()
    assert "SUMMARY METRICS" in text
    assert "ENVIRONMENT DISTRIBUTION" in text
    assert "TOP 10 ORGANIZATIONS" in text


# Run analysis on real data file when executed directly
if __name__ == "__main__":
    csv_file = os.path.join(PROJECT_ROOT, "messages_20260225_154435.csv")
    print(f"Analyzing: {csv_file}")
    
    if os.path.exists(csv_file):
        result = analyze_real_data(csv_file)
        print("\nSummary:")
        for key, value in result["summary"].items():
            print(f"  {key}: {value}")
    else:
        print("File not found")

