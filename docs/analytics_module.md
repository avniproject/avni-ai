# Analytics Module Documentation

## Overview

The analytics module (`dify/analytics_tools/analytics.py`) provides functionality for analyzing conversation data from CSV files and generating comprehensive reports. It processes message data to extract insights about usage patterns, performance metrics, costs, and more.

## Module Location

```
dify/analytics_tools/analytics.py
```

## Functions

### 1. `analyze_real_data(csv_file: str = "messages_20260225_154435.csv") -> dict`

Analyzes conversation data from a CSV file and returns a comprehensive dictionary of metrics.

#### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `csv_file` | str | `"messages_20260225_154435.csv"` | Path to the CSV file containing message data |

#### Expected CSV Columns

The input CSV should contain the following columns:
- `conversation_id`: Unique identifier for each conversation
- `user_name`: Name of the user
- `org_name`: Organization name
- `org_type`: Organization type (e.g., "prod", "dev")
- `created_at`: Unix timestamp
- `query`: User query text
- `answer`: System answer text
- `provider_response_latency`: Response time in seconds
- `prompt_tokens`: Number of prompt tokens used
- `completion_tokens`: Number of completion tokens used
- `total_tokens`: Total tokens used
- `total_price`: Total cost in USD

#### Returns

A dictionary containing the following sections:

| Key | Description |
|-----|-------------|
| `summary` | Overall statistics (total messages, conversations, users, organizations, date range) |
| `environment_distribution` | Count of messages by organization type |
| `top_organizations` | Top 10 organizations by message count |
| `top_users` | Top 10 users by message count |
| `hourly_distribution` | Message count by hour of day |
| `daily_distribution` | Message count by day of week |
| `conversation_stats` | Average, median, max conversation length |
| `text_stats` | Average/max query and answer lengths |
| `performance_stats` | Response time statistics |
| `token_stats` | Token usage metrics |
| `cost_stats` | Cost analysis including cost by environment |
| `exact_duplicates` | Queries that appear multiple times |

#### Example Usage

```python
from dify.analytics_tools.analytics import analyze_real_data

# Analyze a CSV file
result = analyze_real_data("messages.csv")

# Access specific metrics
print(f"Total messages: {result['summary']['total_messages']}")
print(f"Total cost: {result['cost_stats']['total_cost']}")
```

---

### 2. `export_factual_report_csv(data: dict, output_file: str = None) -> str`

Exports the analytics data to a formatted CSV file.

#### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `data` | dict | Required | Dictionary returned by `analyze_real_data()` |
| `output_file` | str | `None` | Output file path. If None, generates timestamped filename |

#### Returns

- `str`: Path to the created CSV file

#### Output Sections

The exported CSV contains the following sections:
1. **SUMMARY METRICS** - Overall statistics
2. **ENVIRONMENT DISTRIBUTION** - Messages by org type
3. **TOP 10 ORGANIZATIONS** - Top organizations by usage
4. **TOP 10 USERS** - Top users by message count
5. **HOURLY USAGE PATTERNS** - Messages per hour
6. **DAILY USAGE PATTERNS** - Messages per day of week
7. **CONVERSATION ANALYSIS** - Conversation length statistics
8. **TEXT ANALYSIS** - Query/answer length metrics
9. **PERFORMANCE METRICS** - Response time data
10. **TOKEN USAGE** - Token consumption metrics
11. **COST ANALYSIS** - Overall cost metrics
12. **COST BY ENVIRONMENT** - Cost breakdown by org type
13. **DUPLICATE QUERIES** - Repeated queries

#### Example Usage

```python
from dify.analytics_tools.analytics import analyze_real_data, export_factual_report_csv

# Generate analytics
data = analyze_real_data("messages.csv")

# Export to CSV
output_path = export_factual_report_csv(data, "report.csv")
print(f"Report saved to: {output_path}")
```

---

## Test Suite

The test suite is located at `tests/test_analytics.py` and includes the following tests:

### Test Functions

| Test Name | Description |
|-----------|-------------|
| `test_basic_analysis` | Verifies output contains expected keys and calculates statistics correctly |
| `test_determinism` | Ensures multiple runs produce identical results |
| `test_empty_input_raises` | Verifies exception is raised for empty CSV |
| `test_missing_columns_error` | Verifies KeyError is raised for missing required columns |
| `test_export_report_creates_file` | Validates CSV export produces expected sections |

### Running Tests

```bash
# Run all analytics tests
pytest tests/test_analytics.py -v

# Run a specific test
pytest tests/test_analytics.py::test_basic_analysis -v
```

---

## Data Flow

```
CSV File (messages.csv)
        |
        v
+-------------------+
| analyze_real_data |
+-------------------+
        |
        v
   Dictionary with
   all metrics
        |
        +-------------------+
        |                   |
        v                   v
+-------------------+  +----------------------+
| Export to CSV     |  | Direct access to     |
| (optional)       |  | metrics via dict     |
+-------------------+  +----------------------+
```

---

## Error Handling

| Scenario | Behavior |
|----------|----------|
| Empty CSV file | Raises Exception |
| Missing required columns | Raises KeyError |
| Invalid data types | May cause unexpected results |

---

## Dependencies

- `pandas`: For CSV reading and data manipulation
- `datetime`: For timestamp handling
- `csv`: For CSV export

## Example Output

### Summary Section
```python
{
    'summary': {
        'total_messages': 150,
        'total_conversations': 45,
        'unique_users': 30,
        'unique_organizations': 5,
        'date_range_days': 30,
        'messages_per_day': 5.0
    },
    'cost_stats': {
        'total_cost': 0.50,
        'avg_cost_per_message': 0.003,
        'cost_by_environment': {'prod': 0.40, 'dev': 0.10}
    }
}
```

---

## CLI Usage

The module can also be run directly:

```bash
python dify/analytics_tools/analytics.py
```

This will generate a timestamped CSV report (`complete_analytics_YYYYMMDD_HHMMSS.csv`) in the current directory.

