# App Configurator Testing with Judge Framework Integration

Integrate AI App Configurator testing into the existing judge_framework using staging environment (https://staging.avniproject.org, org: app_config_test_1) with the Dify workflow and enable rapid SSH-based deployment for iteration.

## Overview

This plan adapts the existing judge_framework pattern (used for form validation and conversation testing) to test the App Configurator bundle generation workflow. It includes:
1. Bundle module implementation (spec_parser, bundle_generator, etc.)
2. Judge framework integration for automated testing
3. Local MongoDB Docker setup for asset store
4. SSH-based quick deployment to staging
5. Both unit tests and end-to-end Dify workflow tests

## Architecture

```
Test Flow:
  Test Subject (SRS Excel) 
    → Executor (Dify App Config Workflow OR Direct Python Module)
    → Judge (LLM evaluates bundle correctness)
    → Analytics (Success rates, error analysis)

Deployment Flow:
  Local Dev → Git Push → SSH to Staging → Git Pull → Restart Service
```

## Phase 1: Bundle Module Implementation

### 1.1 Core Bundle Files
**Directory**: `src/tools/bundle/`

Files to create (per `RevisedImplementationPlan.md`):

**`__init__.py`**
```python
from .spec_parser import SpecParser
from .ambiguity_checker import AmbiguityChecker
from .bundle_generator import BundleGenerator
from .asset_store import AssetStore
from .bundle_uploader import BundleUploader
from .uuid_registry import UUIDRegistry
```

**`spec_parser.py`**
- Parse Excel/CSV SRS files
- Extract Modelling sheet → entities JSONL
- Extract Form sheets (columns A-Q) → forms JSONL
- Use openpyxl for Excel reading
- Return structured JSONL format

**`ambiguity_checker.py`**
- Validate JSONL completeness
- Check for missing mandatory fields
- Detect unknown data types
- Flag inconsistencies (e.g., program without subject)
- Return ambiguity report with issues/warnings

**`bundle_generator.py`**
- JSONL → Avni bundle JSON (deterministic)
- Generate: subjectTypes, programs, encounterTypes, concepts, forms, formMappings
- Use stable UUID generation (UUID5 based on names)
- Create cancellation forms automatically
- Add keyValues for metadata

**`asset_store.py`**
- MongoDB async operations using Motor
- Session CRUD: create, find, update, resume
- Store JSONL, bundle JSON, ambiguity reports
- Version tracking and upload history
- Schema matches `RevisedImplementationPlan.md` section 5

**`bundle_uploader.py`**
- Assemble Metadata ZIP from bundle JSON
- POST to `/api/importMetaData` endpoint
- Handle upload response and errors
- Update session with upload status

**`uuid_registry.py`**
- Port 143 standard UUIDs from existing registry
- Deterministic UUID5 generation for new entities
- Namespace-based UUID generation

### 1.2 Handler Implementation
**File**: `src/handlers/bundle_handler.py`

FastAPI endpoints:
```python
@app.post("/generate-bundle-async")
async def generate_bundle_async(file: UploadFile, org: str)

@app.get("/bundle-status/{session_id}")
async def get_bundle_status(session_id: str)

@app.post("/bundle-confirm-entities")
async def confirm_entities(session_id: str, confirmed: bool)

@app.post("/bundle-confirm-forms")
async def confirm_forms(session_id: str, confirmed: bool)

@app.post("/bundle-upload")
async def upload_bundle(session_id: str)
```

### 1.3 MongoDB Models
**File**: `src/models/bundle_session.py`

Pydantic models:
- `BundleSession` - Main session document
- `EntityJSONL` - Entity representation
- `FormJSONL` - Form field representation
- `AmbiguityReport` - Validation results
- `UploadHistory` - Upload tracking

## Phase 2: Local Infrastructure Setup

### 2.1 Docker Compose for MongoDB
**File**: `docker-compose.bundle-test.yml`

```yaml
version: '3.8'
services:
  mongodb:
    image: mongo:7.0
    container_name: avni-bundle-mongodb
    ports:
      - "27017:27017"
    environment:
      MONGO_INITDB_DATABASE: avni_ai_test
    volumes:
      - mongodb_data:/data/db
    healthcheck:
      test: echo 'db.runCommand("ping").ok' | mongosh localhost:27017/test --quiet
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  mongodb_data:
```

### 2.2 Environment Configuration
**File**: `.env.bundle_test`

```env
# MongoDB
MONGODB_URL=mongodb://localhost:27017
MONGODB_DATABASE=avni_ai_test

# Staging Avni Server
AVNI_BASE_URL=https://staging.avniproject.org
AVNI_AUTH_TOKEN=<from_app_config_test_1_org>
AVNI_TEST_ORG=app_config_test_1
AVNI_TEST_USER=himeshr@app_config_test_1

# Dify App Config Workflow
DIFY_API_BASE_URL=https://api.dify.ai/v1
DIFY_BUNDLE_API_KEY=<available_from_user>  # API key is available
DIFY_BUNDLE_WORKFLOW_NAME=App Config [Staging] Assistant
DIFY_BUNDLE_WORKFLOW_URL=https://cloud.dify.ai/app/4a9a9f37-f391-41a1-a964-9d73e36f1444/workflow

# OpenAI (for judge evaluation)
OPENAI_API_KEY=<existing_key>

# Judge Framework
JUDGE_FRAMEWORK_DEFAULT_MODEL=gpt-4o
JUDGE_FRAMEWORK_DEFAULT_TEMPERATURE=0.1
```

**Setup Instructions**:
1. Copy `.env.bundle_test` to `.env` or load it for testing
2. Add Dify API key (available from user)
3. Get auth token from app_config_test_1 org on staging
4. Verify MongoDB is running locally

### 2.3 Makefile Targets
**File**: `Makefile` (update)

```makefile
# Start MongoDB for bundle testing
start-bundle-mongodb:
	docker-compose -f docker-compose.bundle-test.yml up -d
	@echo "Waiting for MongoDB to be ready..."
	@sleep 5

# Stop MongoDB
stop-bundle-mongodb:
	docker-compose -f docker-compose.bundle-test.yml down

# Run bundle unit tests
test-bundle-unit:
	uv run pytest tests/bundle/unit/ -v -m unit

# Run bundle integration tests (requires MongoDB)
test-bundle-integration: start-bundle-mongodb
	uv run pytest tests/bundle/integration/ -v -m integration
	make stop-bundle-mongodb

# Run bundle Dify workflow tests
test-bundle-dify:
	uv run pytest tests/bundle/judge_framework/ -v -m dify

# Run all bundle tests
test-bundle-all: test-bundle-unit test-bundle-integration test-bundle-dify
```

## Phase 3: Judge Framework Integration

### 3.1 Bundle Test Subject
**File**: `tests/judge_framework/implementations/bundleGeneration/bundle_generation_subject.py`

```python
class BundleGenerationTestSubject(TestSubject):
    """Test subject for bundle generation from SRS Excel"""
    
    def __init__(self, srs_file_path: str, expected_output: dict, config: TestConfiguration):
        self.srs_file_path = srs_file_path
        self.expected_output = expected_output
        self.config = config
    
    def get_test_identifier(self) -> str:
        return f"bundle_{Path(self.srs_file_path).stem}"
    
    def get_test_input(self) -> Dict[str, Any]:
        return {
            "srs_file": self.srs_file_path,
            "org": "app_config_test_1",
            "user": "himeshr@app_config_test_1"
        }
    
    def get_expected_behavior(self) -> str:
        return self.expected_output.get("expected_behavior", "")
    
    def get_evaluation_context(self) -> Dict[str, Any]:
        return {
            "expected_entities": self.expected_output.get("entities", []),
            "expected_forms": self.expected_output.get("forms", []),
            "expected_concepts": self.expected_output.get("concepts", [])
        }
```

### 3.2 Bundle Test Executor (Dual Mode)
**File**: `tests/judge_framework/implementations/bundleGeneration/bundle_generation_executor.py`

Two execution modes:

**Mode 1: Direct Python Module Testing**
```python
class DirectBundleExecutor(TestExecutor):
    """Execute bundle generation directly via Python modules"""
    
    async def execute(self, test_input: Dict[str, Any]) -> Dict[str, Any]:
        # 1. Parse SRS → JSONL
        parser = SpecParser()
        jsonl = await parser.parse(test_input["srs_file"])
        
        # 2. Check ambiguity
        checker = AmbiguityChecker()
        ambiguity_report = checker.check(jsonl)
        
        # 3. Generate bundle
        generator = BundleGenerator()
        bundle = generator.generate(jsonl)
        
        return {
            "jsonl": jsonl,
            "ambiguity_report": ambiguity_report,
            "bundle": bundle
        }
```

**Mode 2: Dify Workflow Testing**
```python
class DifyBundleExecutor(TestExecutor):
    """Execute bundle generation via Dify workflow"""
    
    async def execute(self, test_input: Dict[str, Any]) -> Dict[str, Any]:
        # Upload SRS file to Dify workflow
        # Monitor conversation flow
        # Extract final bundle output
        # Return results
```

### 3.3 Bundle Judge Strategy
**File**: `tests/judge_framework/implementations/bundleGeneration/bundle_generation_judge.py`

```python
class BundleGenerationJudge(JudgeStrategy):
    """LLM-as-judge for bundle generation correctness"""
    
    def evaluate(self, test_input, test_output) -> EvaluationResult:
        # Evaluation criteria:
        # 1. Entity completeness (all entities from SRS present)
        # 2. Form structure correctness (fields, data types, mandatory)
        # 3. Concept generation (correct types, options)
        # 4. UUID consistency (stable across runs)
        # 5. Relationship integrity (program→subject, encounter→program)
        # 6. Ambiguity handling (flagged correctly)
        
        # Use GPT-4o to evaluate
        prompt = self._build_evaluation_prompt(test_input, test_output)
        evaluation = self.openai_client.chat.completions.create(...)
        
        return EvaluationResult(
            test_identifier=test_input["test_identifier"],
            success=evaluation["success"],
            scores={
                "entity_completeness": evaluation["entity_score"],
                "form_correctness": evaluation["form_score"],
                "concept_accuracy": evaluation["concept_score"],
                "relationship_integrity": evaluation["relationship_score"]
            }
        )
```

### 3.4 Bundle Test Configuration
**File**: `tests/judge_framework/examples/configs/bundle_generation_config.py`

```python
def create_bundle_generation_test_config() -> TestConfiguration:
    dify_config = DifyConfig(
        api_key=os.getenv("DIFY_BUNDLE_API_KEY"),
        base_url=os.getenv("DIFY_API_BASE_URL"),
        workflow_name="App Config [Staging] Assistant",
        test_user="himeshr@app_config_test_1",
        timeout_seconds=180  # Bundle generation can take longer
    )
    
    evaluation_config = EvaluationConfig(
        evaluation_metrics=[
            "entity_completeness",
            "form_correctness", 
            "concept_accuracy",
            "relationship_integrity",
            "ambiguity_detection"
        ],
        success_thresholds={
            "entity_completeness": 90.0,
            "form_correctness": 85.0,
            "concept_accuracy": 85.0,
            "relationship_integrity": 90.0
        },
        openai_model="gpt-4o",
        openai_temperature=0.1
    )
    
    # Static test cases from existing SRS files
    static_test_cases = load_srs_test_cases()
    
    generation_config = TestGenerationConfig(
        static_test_cases=static_test_cases,
        ai_generation_enabled=False,  # Use real SRS files only
        num_ai_cases=0
    )
    
    return TestConfiguration(
        dify_config=dify_config,
        evaluation_config=evaluation_config,
        generation_config=generation_config,
        max_iterations=1  # Bundle generation is single-turn
    )
```

### 3.5 Bundle Test Runner
**File**: `tests/judge_framework/examples/run_bundle_generation_tests.py`

```python
#!/usr/bin/env python3
"""
Run bundle generation tests using judge framework
"""

from tests.judge_framework.orchestrator import JudgeOrchestrator
from tests.judge_framework.implementations.bundleGeneration import (
    BundleGenerationSubjectFactory,
    DirectBundleExecutor,  # or DifyBundleExecutor
    BundleGenerationJudge
)
from tests.judge_framework.examples.configs.bundle_generation_config import (
    create_bundle_generation_test_config
)
from tests.judge_framework.analytics.reporting import ReportGenerator

def main():
    config = create_bundle_generation_test_config()
    
    # Choose executor mode
    executor = DirectBundleExecutor(config)  # For module testing
    # executor = DifyBundleExecutor(config)  # For Dify workflow testing
    
    judge = BundleGenerationJudge(config)
    factory = BundleGenerationSubjectFactory()
    
    orchestrator = JudgeOrchestrator(executor, judge)
    
    # Run test suite
    results = orchestrator.run_test_suite(factory, config, fail_fast=False)
    
    # Generate reports
    report_gen = ReportGenerator()
    report_gen.generate_console_report(results)
    report_gen.generate_json_report(results, "reports/bundleGeneration/")
    report_gen.generate_csv_report(results, "reports/bundleGeneration/")
    
    return 0 if results.success_rate >= 80.0 else 1

if __name__ == "__main__":
    exit(main())
```

## Phase 4: Test Data and Fixtures

### 4.1 Download SRS Files from Google Sheets
**Source**: https://docs.google.com/spreadsheets/d/1cEod2MbMtRvAcupArC4nZaHIYB2HHUrIIbOZR0uGRz8/edit?gid=262841117#gid=262841117

**Script**: `scripts/download_srs_samples.py`
```python
#!/usr/bin/env python3
"""Download SRS samples from Google Sheets and convert to test fixtures"""

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from pathlib import Path

GOOGLE_SHEET_ID = "1cEod2MbMtRvAcupArC4nZaHIYB2HHUrIIbOZR0uGRz8"
OUTPUT_DIR = Path("tests/fixtures/bundle/srs_samples")

def download_srs_sheets():
    """Download all sheets from Google Spreadsheet"""
    # Authenticate with Google Sheets API
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
    client = gspread.authorize(creds)
    
    # Open spreadsheet
    sheet = client.open_by_key(GOOGLE_SHEET_ID)
    
    # Download each worksheet
    for worksheet in sheet.worksheets():
        df = pd.DataFrame(worksheet.get_all_records())
        output_file = OUTPUT_DIR / f"{worksheet.title}.xlsx"
        df.to_excel(output_file, index=False)
        print(f"Downloaded: {worksheet.title} → {output_file}")

if __name__ == "__main__":
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    download_srs_sheets()
```

**Alternative**: Manual download as Excel files and place in `tests/fixtures/bundle/srs_samples/`

### 4.2 Test Fixtures Directory Structure
```
tests/fixtures/bundle/
├── srs_samples/           # Downloaded from Google Sheets
│   ├── pregnancy_program.xlsx
│   ├── health_screening.xlsx
│   └── multi_program_complex.xlsx
├── expected_outputs/      # Expected results for each SRS
│   ├── pregnancy_program/
│   │   ├── entities.jsonl
│   │   ├── forms.jsonl
│   │   ├── ambiguity_report.json
│   │   └── bundle_json/
│   │       ├── subjectTypes.json
│   │       ├── programs.json
│   │       └── forms.json
│   └── ...
└── test_cases.json       # Test case metadata
```

### 4.3 Test Case Metadata
**File**: `tests/fixtures/bundle/test_cases.json`

```json
[
  {
    "test_id": "pregnancy_program_basic",
    "srs_file": "srs_samples/pregnancy_program.xlsx",
    "google_sheet_url": "https://docs.google.com/spreadsheets/d/1cEod2MbMtRvAcupArC4nZaHIYB2HHUrIIbOZR0uGRz8",
    "description": "Basic pregnancy program with ANC encounters",
    "expected_output": {
      "entities": ["Individual", "Pregnancy", "ANC"],
      "forms": ["ANC Form", "Pregnancy Enrollment"],
      "concepts": ["BP Systolic", "BP Diastolic", "Weight"],
      "expected_behavior": "Should create complete pregnancy program with vital signs"
    },
    "complexity": "simple"
  },
  {
    "test_id": "health_screening_complete",
    "srs_file": "srs_samples/health_screening.xlsx",
    "google_sheet_url": "https://docs.google.com/spreadsheets/d/1cEod2MbMtRvAcupArC4nZaHIYB2HHUrIIbOZR0uGRz8",
    "description": "Complete health screening with skip logic",
    "expected_output": {
      "entities": ["Individual", "Health Screening", "Follow-up"],
      "forms": ["Screening Form", "Follow-up Form"],
      "concepts": ["Diabetes", "Hypertension", "BMI"],
      "expected_behavior": "Should handle conditional fields and skip logic"
    },
    "complexity": "medium"
  }
]
```

## Phase 5: Unit Tests

### 5.1 Unit Test Structure
**Directory**: `tests/bundle/unit/`

```
tests/bundle/unit/
├── __init__.py
├── conftest.py              # Shared fixtures
├── test_spec_parser.py      # Excel parsing tests
├── test_ambiguity_checker.py # Validation tests
├── test_bundle_generator.py  # JSON generation tests
├── test_asset_store.py       # MongoDB tests (with mongomock)
├── test_uuid_registry.py     # UUID determinism tests
└── test_bundle_uploader.py   # Upload logic tests
```

### 5.2 Sample Unit Test
**File**: `tests/bundle/unit/test_spec_parser.py`

```python
import pytest
from src.tools.bundle.spec_parser import SpecParser

class TestSpecParser:
    @pytest.fixture
    def parser(self):
        return SpecParser()
    
    @pytest.mark.unit
    async def test_parse_modelling_sheet(self, parser):
        """Test parsing Modelling sheet to entities JSONL"""
        srs_file = "tests/fixtures/bundle/srs_samples/pregnancy_program.xlsx"
        jsonl = await parser.parse(srs_file)
        
        entities = [row for row in jsonl if row["type"] in ["subject_type", "program", "encounter_type"]]
        
        assert len(entities) > 0
        assert any(e["name"] == "Individual" for e in entities)
        assert any(e["name"] == "Pregnancy" for e in entities)
    
    @pytest.mark.unit
    async def test_parse_form_sheet(self, parser):
        """Test parsing form sheet to fields JSONL"""
        srs_file = "tests/fixtures/bundle/srs_samples/pregnancy_program.xlsx"
        jsonl = await parser.parse(srs_file)
        
        fields = [row for row in jsonl if row["type"] == "field"]
        
        assert len(fields) > 0
        assert all("form" in f for f in fields)
        assert all("data_type" in f for f in fields)
```

### 5.3 MongoDB Mock Tests
**File**: `tests/bundle/unit/test_asset_store.py`

```python
import pytest
from mongomock_motor import AsyncMongoMockClient
from src.tools.bundle.asset_store import AssetStore

class TestAssetStore:
    @pytest.fixture
    async def asset_store(self):
        client = AsyncMongoMockClient()
        db = client["test_db"]
        return AssetStore(db)
    
    @pytest.mark.unit
    async def test_create_session(self, asset_store):
        """Test session creation"""
        session_id = await asset_store.create_session("test_org")
        
        assert session_id is not None
        session = await asset_store.get_session(session_id)
        assert session["org"] == "test_org"
        assert session["status"] == "created"
```

## Phase 6: Integration Tests

### 6.1 Integration Test Structure
**Directory**: `tests/bundle/integration/`

```
tests/bundle/integration/
├── __init__.py
├── conftest.py                    # MongoDB Docker fixtures
├── test_end_to_end_minimal.py     # Simple SRS → bundle
├── test_end_to_end_complex.py     # Complex SRS with skip logic
├── test_session_resume.py         # Session persistence
├── test_ambiguity_handling.py     # Missing data scenarios
└── test_upload_to_staging.py      # Upload to staging server
```

### 6.2 Sample Integration Test
**File**: `tests/bundle/integration/test_end_to_end_minimal.py`

```python
import pytest
from src.tools.bundle.spec_parser import SpecParser
from src.tools.bundle.ambiguity_checker import AmbiguityChecker
from src.tools.bundle.bundle_generator import BundleGenerator
from src.tools.bundle.asset_store import AssetStore

@pytest.mark.integration
async def test_minimal_pregnancy_program_end_to_end(mongodb_client):
    """Test complete flow: SRS → JSONL → Bundle JSON"""
    
    # 1. Parse SRS
    parser = SpecParser()
    jsonl = await parser.parse("tests/fixtures/bundle/srs_samples/pregnancy_program.xlsx")
    
    # 2. Check ambiguity
    checker = AmbiguityChecker()
    report = checker.check(jsonl)
    assert len(report["issues"]) == 0  # Should have no blocking issues
    
    # 3. Generate bundle
    generator = BundleGenerator()
    bundle = generator.generate(jsonl)
    
    # 4. Verify bundle structure
    assert "subjectTypes" in bundle
    assert "programs" in bundle
    assert "encounterTypes" in bundle
    assert "forms" in bundle
    
    # 5. Store in MongoDB
    asset_store = AssetStore(mongodb_client["avni_ai_test"])
    session_id = await asset_store.create_session("app_config_test_1")
    await asset_store.store_jsonl(session_id, "entities", jsonl)
    await asset_store.store_asset(session_id, "bundle", bundle)
    
    # 6. Verify persistence
    retrieved_bundle = await asset_store.get_asset(session_id, "bundle")
    assert retrieved_bundle == bundle
```

## Phase 7: SSH-Based Quick Deployment

### 7.1 Staging Server Setup
**Server**: avni-staging (from avni-server repo)
**Location**: https://staging.avniproject.org
**Service**: avni-ai (FastAPI service)

**Prerequisites**:
1. SSH access to avni-staging server
2. avni-ai service configured on staging
3. Git repository access from staging server

### 7.2 Deployment Script
**File**: `scripts/deploy_to_staging_ssh.sh`

```bash
#!/bin/bash
# Quick deployment to staging via SSH

set -e

# Configuration (update with actual staging server details)
STAGING_HOST="avni-staging.server.com"  # Update with actual hostname
STAGING_USER="ubuntu"
STAGING_PATH="/opt/avni-ai"
SERVICE_NAME="avni-ai"

echo "🚀 Deploying to staging via SSH..."

# 1. Push local changes
echo "📤 Pushing to git..."
git add .
git commit -m "Bundle configurator updates" || true
git push origin main

# 2. SSH to staging and update
echo "🔗 Connecting to staging server..."
ssh ${STAGING_USER}@${STAGING_HOST} << 'EOF'
    cd /opt/avni-ai
    
    echo "📥 Pulling latest code..."
    git fetch origin
    git reset --hard origin/main
    
    echo "📦 Installing dependencies..."
    uv sync
    
    echo "🔄 Restarting service..."
    sudo systemctl restart avni-ai
    
    echo "✅ Deployment complete!"
    
    echo "📊 Service status:"
    sudo systemctl status avni-ai --no-pager -l
EOF

echo "🎉 Staging deployment complete!"
echo "🔗 Check logs: ssh ${STAGING_USER}@${STAGING_HOST} 'sudo journalctl -u avni-ai -f'"
```

**Note**: Update `STAGING_HOST` with the actual hostname from avni-server repo's staging configuration

### 7.2 Quick Test Script
**File**: `scripts/test_staging_bundle.sh`

```bash
#!/bin/bash
# Quick test of bundle generation on staging

STAGING_URL="https://staging-mcp.avniproject.org"
TEST_SRS="tests/fixtures/bundle/srs_samples/pregnancy_program.xlsx"

echo "🧪 Testing bundle generation on staging..."

# Upload SRS file and trigger bundle generation
curl -X POST "${STAGING_URL}/generate-bundle-async" \
  -F "file=@${TEST_SRS}" \
  -F "org=app_config_test_1" \
  | jq .

echo "✅ Test request sent!"
```

### 7.3 Makefile Deployment Targets
**File**: `Makefile` (update)

```makefile
# Deploy to staging via SSH
deploy-staging-ssh:
	./scripts/deploy_to_staging_ssh.sh

# Test staging deployment
test-staging-bundle:
	./scripts/test_staging_bundle.sh

# Quick iteration: deploy + test
quick-deploy: deploy-staging-ssh
	sleep 10
	make test-staging-bundle
```

## Phase 8: CI/CD Integration

### 8.1 Update CircleCI
**File**: `.circleci/config.yml` (add job)

```yaml
bundle_tests:
  docker:
    - image: cimg/python:3.13
    - image: mongo:7.0
  steps:
    - checkout
    - run:
        name: Install uv
        command: |
          curl -LsSf https://astral.sh/uv/install.sh | sh
          echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$BASH_ENV"
    - run:
        name: Install dependencies
        command: uv sync --group test
    - run:
        name: Run bundle unit tests
        command: uv run pytest tests/bundle/unit/ -v -m unit --cov=src/tools/bundle
    - run:
        name: Run bundle integration tests
        command: uv run pytest tests/bundle/integration/ -v -m integration
        environment:
          MONGODB_URL: mongodb://localhost:27017
    - store_test_results:
        path: test-results
    - store_artifacts:
        path: htmlcov
        destination: bundle-coverage
```

### 8.2 Update Workflow
**File**: `.circleci/config.yml` (update workflow)

```yaml
workflows:
  version: 2
  build-test-deploy:
    jobs:
      - build
      - test
      - bundle_tests  # Add bundle tests
      - staging_approve:
          type: approval
          requires:
            - test
            - bundle_tests  # Require bundle tests to pass
```

## Phase 9: Documentation

### 9.1 Bundle Testing Guide
**File**: `docs/app_configurator/BUNDLE_TESTING.md`

Sections:
- Running bundle tests locally
- Using judge_framework for bundle testing
- Creating new test cases
- Debugging bundle generation
- MongoDB session inspection
- Interpreting test results

### 9.2 Quick Start Guide
**File**: `docs/app_configurator/QUICK_START.md`

```markdown
# Quick Start: Bundle Generation Testing

## Local Development

1. Start MongoDB:
   ```bash
   make start-bundle-mongodb
   ```

2. Run unit tests:
   ```bash
   make test-bundle-unit
   ```

3. Run integration tests:
   ```bash
   make test-bundle-integration
   ```

4. Run Dify workflow tests:
   ```bash
   make test-bundle-dify
   ```

## Staging Deployment

1. Deploy to staging:
   ```bash
   make deploy-staging-ssh
   ```

2. Test on staging:
   ```bash
   make test-staging-bundle
   ```

## Adding New Test Cases

1. Add SRS file to `tests/fixtures/bundle/srs_samples/`
2. Create expected outputs in `tests/fixtures/bundle/expected_outputs/`
3. Update `test_cases.json`
4. Run tests
```

## Implementation Order

### Week 0: Initial Setup (1-2 days)
- **Setup Tasks**:
  - Download SRS files from Google Sheets (https://docs.google.com/spreadsheets/d/1cEod2MbMtRvAcupArC4nZaHIYB2HHUrIIbOZR0uGRz8)
  - Set up `.env.bundle_test` with Dify API key and staging credentials
  - Configure SSH access to avni-staging server
  - Start MongoDB Docker container
  - Create test fixtures directory structure

### Week 1: Core Bundle Modules
- **Day 1-2**: Implement `spec_parser.py` and `ambiguity_checker.py`
- **Day 3-4**: Implement `bundle_generator.py` and `uuid_registry.py`
- **Day 5**: Implement `asset_store.py` with MongoDB

### Week 2: Testing Infrastructure
- **Day 6-7**: Set up MongoDB Docker, write unit tests
- **Day 8-9**: Create judge_framework integration (subject, executor, judge)
- **Day 10**: Write integration tests

### Week 3: Deployment and Polish
- **Day 11-12**: SSH deployment scripts, test on staging
- **Day 13-14**: Dify workflow testing, end-to-end validation
- **Day 15**: Documentation, CI/CD integration

## Success Criteria

- ✅ All bundle modules implemented and tested
- ✅ Unit test coverage >80% for bundle modules
- ✅ Integration tests pass with local MongoDB
- ✅ Judge framework successfully evaluates bundle generation
- ✅ SSH deployment works to staging environment
- ✅ End-to-end test: SRS upload → bundle generation → upload to staging
- ✅ CI/CD pipeline includes bundle tests
- ✅ Documentation complete

## Environment Setup Checklist

- [ ] MongoDB Docker running locally
- [ ] `.env.bundle_test` configured with staging credentials
- [x] Dify API key available (confirmed by user)
- [ ] SSH access to avni-staging server configured (from avni-server repo)
- [x] Test organization `app_config_test_1` accessible on staging
- [x] SRS files location confirmed (Google Sheets: https://docs.google.com/spreadsheets/d/1cEod2MbMtRvAcupArC4nZaHIYB2HHUrIIbOZR0uGRz8)
- [ ] Download SRS files from Google Sheets to fixtures
- [ ] Judge framework dependencies installed
- [ ] Google Sheets API credentials (if using automated download)

## Testing Strategy

### Unit Tests (Fast, No External Dependencies)
- Spec parser logic
- Ambiguity checker rules
- Bundle generator templates
- UUID determinism
- MongoDB operations (with mongomock)

### Integration Tests (Requires MongoDB Docker)
- End-to-end SRS → bundle flow
- Session persistence and resume
- Ambiguity handling scenarios
- Upload to staging server

### Judge Framework Tests (Requires Dify + Staging)
- Dify workflow end-to-end
- LLM evaluation of bundle correctness
- Comparison against expected outputs
- Error categorization and reporting

## Dependencies

**Python Packages** (add to `pyproject.toml`):
```toml
dependencies = [
    # Existing...
    "openpyxl>=3.1.0",      # Excel parsing
    "motor>=3.3.0",         # Async MongoDB
    "mongomock-motor>=0.0.21",  # MongoDB mocking for tests
    "gspread>=5.12.0",      # Google Sheets API (for SRS download)
    "oauth2client>=4.1.3",  # Google Sheets authentication
]
```

**System Requirements**:
- Docker Desktop (for MongoDB)
- SSH access to avni-staging server (from avni-server repo)
- Dify API key (available)
- Staging Avni server credentials (app_config_test_1 org)
- Google Sheets API credentials (optional, for automated SRS download)

## Risks and Mitigations

| Risk | Mitigation |
|------|------------|
| No existing SRS files found | Create minimal sample files based on spec |
| MongoDB connection issues | Provide detailed Docker setup instructions |
| Staging server access problems | Document SSH key setup process |
| Dify API rate limits | Implement exponential backoff and retry logic |
| Bundle upload failures | Add comprehensive error handling and logging |
| Test data maintenance | Version control expected outputs with SRS files |

## Next Steps After Implementation

1. **Expand Test Coverage**: Add more complex SRS scenarios
2. **Performance Testing**: Benchmark large SRS file processing
3. **Error Recovery**: Test partial failures and rollback
4. **Multi-org Testing**: Test with different organizations
5. **Monitoring**: Add Prometheus metrics for bundle generation
6. **User Acceptance**: Run with real client SRS files
