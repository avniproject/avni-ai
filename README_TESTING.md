# Avni Configuration Manager Test Suite

This comprehensive test suite validates the `clean_config_manager.py` functionality with various scenarios including location hierarchies, subject types, programs, and encounter types.

## 🚀 Quick Start

### 1. Update Credentials

Edit `run_tests.py` and replace the placeholder values:

```python
AUTH_TOKEN = "your-actual-auth-token-here"
BASE_URL = "https://staging.avniproject.org"  # or your production URL
```

**Note:** The test suite automatically uses `org_type: 'trial'` to bypass Production/UAT restrictions in the configuration manager.

### 2. Run All Tests

```bash
python run_tests.py
```

### 3. Run Specific Test Cases

```bash
# Run comprehensive test (matches your original prompt)
python test_config_manager.py --auth-token "your-token" --base-url "https://staging.avniproject.org" --test-case comprehensive

# Run basic hierarchy test
python test_config_manager.py --auth-token "your-token" --base-url "https://staging.avniproject.org" --test-case basic

# Run edge cases test
python test_config_manager.py --auth-token "your-token" --base-url "https://staging.avniproject.org" --test-case edge
```

## 📋 Test Cases

### 1. **Basic Location Hierarchy** (`test_basic_hierarchy`)
- **Purpose**: Tests simple State → District hierarchy
- **Entities**: 2 AddressLevelTypes, 3 Locations
- **Validates**: Basic location creation and parent-child relationships

### 2. **Comprehensive Configuration** (`test_comprehensive_config`)
- **Purpose**: Tests your complete original prompt requirements
- **Entities**: 
  - 3 AddressLevelTypes (State, District, Block)
  - 9 Locations (Karnataka, Maharashtra, Odisha + their districts/blocks)
  - 3 Subject Types (Person, Household, Health Worker)
  - 3 Programs (Maternal Health, Nutrition, Community Health)
  - 4 Encounter Types (2 general, 2 program-specific)
- **Validates**: Complete workflow with all entity types and relationships

### 3. **Edge Cases** (`test_edge_cases`)
- **Purpose**: Tests data validation and type conversion
- **Entities**: Custom AddressLevelTypes with string booleans
- **Validates**: String-to-boolean conversion, GPS coordinates, custom properties

### 4. **Empty Configuration** (`test_empty_config`)
- **Purpose**: Tests graceful handling of empty configurations
- **Entities**: All empty arrays
- **Validates**: No-op scenario handling

### 5. **Invalid Data** (`test_invalid_data`)
- **Purpose**: Tests error handling with malformed data
- **Entities**: Invalid UUIDs, empty names, wrong data types
- **Validates**: Error handling and validation

## 🎯 Test Validation Criteria

### ✅ Success Criteria
- **Complete Success**: All entities created successfully
- **Partial Success**: Some entities created, some skipped (already exist)
- **Graceful Failures**: Proper error messages for invalid data

### ❌ Failure Criteria
- **API Errors**: Constraint violations, authentication failures
- **Data Transformation Issues**: Incorrect data types, missing required fields
- **Relationship Errors**: Broken parent-child references

## 📊 Expected Results

### Comprehensive Test Expected Output:
```
✅ PASS: test_comprehensive_config - Total: 19, Success: 19, Failed: 0, Skipped: 0
```

**Breakdown:**
- 3 AddressLevelTypes (may be skipped if already exist)
- 9 Locations with proper hierarchy
- 3 Subject Types
- 3 Programs linked to subject types
- 4 Encounter Types (2 general, 2 program-specific)

### Key Validations:
1. **Location Hierarchy**: Districts properly linked to States, Blocks to Districts
2. **Subject Types**: Proper type classification (Person, PersonGroup, User)
3. **Programs**: Correct subject type references and UUIDs
4. **Encounters**: Proper program linkage for program encounters

## 🛡️ Safety Features

### Organization Type Protection
The configuration manager includes built-in safety to prevent accidental modifications:

- **Production/UAT Organizations**: Automatically blocked from configuration changes
- **Trial Organizations**: Allowed to proceed with configuration changes
- **Test Suite**: Explicitly uses `'trial'` org_type to bypass restrictions

```python
# Configuration manager blocks Production/UAT
if org_type in ['Production', 'UAT']:
    return {
        'configResult': {
            'result': 'error',
            'status': 'production_uat_blocked',
            'message': 'Configuration creation not supported for Production/UAT organizations'
        }
    }

# Test suite explicitly uses 'trial'
test_input = {
    'config': config,
    'auth_token': self.auth_token,
    'org_type': 'trial'  # Bypasses Production/UAT restrictions
}
```

## 🔧 Configuration Structure

The test creates configurations matching this structure:

```
Location Hierarchy:
├── State (Level 1)
│   ├── Karnataka
│   ├── Maharashtra  
│   └── Odisha
├── District (Level 2)
│   ├── Bengaluru → Karnataka
│   ├── Mysore → Karnataka
│   ├── Mumbai → Maharashtra
│   ├── Pune → Maharashtra
│   └── Bhubaneswar → Odisha
└── Block (Level 3)
    └── Khordha → Bhubaneswar

Subject Types:
├── Person (Individual tracking)
├── Household (Family units)
└── Health Worker (Field staff)

Programs:
├── Maternal Health Program → Person
├── Nutrition Program → Person
└── Community Health Program → Household

Encounters:
├── General Health Checkup → Person (no program)
├── Home Visit → Household (no program)
├── Antenatal Care Visit → Person + Maternal Health Program
└── Nutrition Counseling → Person + Nutrition Program
```

## 📁 Output Files

- **`test_results.json`**: Detailed test results with timestamps and error details
- **Console Output**: Real-time test progress and summary

## 🐛 Troubleshooting

### Common Issues:

1. **Authentication Errors**
   ```
   Status 401: Invalid auth token
   ```
   **Solution**: Verify your auth token is current and valid

2. **Constraint Violations**
   ```
   Status 409: address_level_type_name_organisation_id_unique
   ```
   **Solution**: This indicates the bug we fixed - entities already exist

3. **Network Errors**
   ```
   Connection timeout
   ```
   **Solution**: Check base URL and network connectivity

### Debug Mode:
Add debug logging by modifying the test to print detailed API responses:

```python
print(f"API Response: {json.dumps(result, indent=2)}")
```

## 🎯 Success Metrics

- **Coverage**: Tests all major entity types and relationships
- **Validation**: Verifies data transformation and API compliance  
- **Error Handling**: Confirms graceful failure modes
- **Performance**: Measures creation time and success rates

Run the tests and share the results to validate that all the fixes we implemented are working correctly! 🚀
