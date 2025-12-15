## Scripts Overview

### 1. `dify_data_extractor.py`
**Purpose**: Extract conversation and message data from Dify API

**What it does**:
- Fetches all conversations within a date range
- Gets all messages for each conversation  
- Exports data to CSV formats
- Handles pagination automatically

### 2. `clean_csv.py`
**Purpose**: Clean extracted data by removing test/internal users

**What it does**:
- Removes messages from specified test users
- Removes messages from test organizations
- Creates a cleaned CSV file for analysis

### 3. `analytics.py`
**Purpose**: Generate factual analytics from cleaned conversation data

**What it does**:
- Provides objective metrics only
- Shows usage patterns by time, organization, environment
- Analyzes performance, costs, and token usage
- Exports structured analytics report

## Quick Start

### Step 1: Extract Data from Dify
```bash
cd dify/analytics_tools

# Update the configuration at the top of dify_data_extractor.py:
# - CSRF_TOKEN
# - COOKIES  
# - BAGGAGE
# - START_DATE / END_DATE
# Go to Logs and annotations on the Dify UI and look for chat-conversations network request to find the values for these variables.

uv run python dify_data_extractor.py
```

**Output**: `messages_YYYYMMDD_HHMMSS.csv` and `conversations_YYYYMMDD_HHMMSS.csv`

### Step 2: Clean the Data
```bash
uv run python clean_csv.py
```

**Output**: `messages_cleaned.csv`

### Step 3: Generate Analytics
```bash
uv run python analytics.py
```

**Output**: `complete_analytics_YYYYMMDD_HHMMSS.csv`