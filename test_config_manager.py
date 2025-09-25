#!/usr/bin/env python3
"""
Comprehensive Test Suite for Avni Configuration Manager

This test suite validates the clean_config_manager.py functionality with various scenarios:
1. Basic location hierarchy creation
2. Complex multi-level hierarchies
3. Subject types and programs
4. Encounter types (both general and program-specific)
5. Error handling and edge cases
6. Progressive creation with existing entities
7. Data validation and transformation

Usage:
    python test_config_manager.py --auth-token <token> --base-url <url>
"""

import sys
import json
import argparse
import uuid
from datetime import datetime
from typing import Dict, List, Any, Tuple

# Import the configuration manager
from clean_config_manager import main as config_manager_main

class AvniConfigTestSuite:
    """Comprehensive test suite for Avni Configuration Manager"""
    
    def __init__(self, auth_token: str, base_url: str, user_name: str = None, implementation_name: str = None):
        self.auth_token = auth_token
        self.base_url = base_url
        self.user_name = user_name
        self.implementation_name = implementation_name or "test-suite"
        self.test_results = []
        self.total_tests = 0
        self.passed_tests = 0
        self.failed_tests = 0
        
    def log_test_result(self, test_name: str, passed: bool, message: str, details: Dict = None):
        """Log test result"""
        self.total_tests += 1
        if passed:
            self.passed_tests += 1
            status = "✅ PASS"
        else:
            self.failed_tests += 1
            status = "❌ FAIL"
            
        result = {
            'test_name': test_name,
            'status': status,
            'passed': passed,
            'message': message,
            'details': details or {},
            'timestamp': datetime.now().isoformat()
        }
        self.test_results.append(result)
        print(f"{status}: {test_name} - {message}")
        
    def generate_uuid(self) -> str:
        """Generate a UUID for test entities"""
        return str(uuid.uuid4())
        
    def create_test_config_basic_hierarchy(self) -> Dict:
        """Test Case 1: Basic Location Hierarchy with Unique Names"""
        timestamp = str(int(datetime.now().timestamp()))
        return {
            "addressLevelTypes": [
                {
                    "name": f"Test State {timestamp}",
                    "uuid": self.generate_uuid(),
                    "level": 1.0,
                    "voided": False
                },
                {
                    "name": f"Test District {timestamp}", 
                    "uuid": self.generate_uuid(),
                    "level": 2.0,
                    "voided": False
                }
            ],
            "locations": [
                {
                    "name": f"Test State Location {timestamp}",
                    "uuid": self.generate_uuid(),
                    "level": 1.0,
                    "type": f"Test State {timestamp}",
                    "addressLevelTypeUUID": None,  # Will be set dynamically
                    "voided": False
                },
                {
                    "name": f"Test District A {timestamp}",
                    "uuid": self.generate_uuid(),
                    "level": 2.0,
                    "type": f"Test District {timestamp}", 
                    "addressLevelTypeUUID": None,  # Will be set dynamically
                    "voided": False
                },
                {
                    "name": f"Test District B {timestamp}",
                    "uuid": self.generate_uuid(),
                    "level": 2.0,
                    "type": f"Test District {timestamp}",
                    "addressLevelTypeUUID": None,  # Will be set dynamically
                    "voided": False
                }
            ],
            "subjectTypes": [],
            "programs": [],
            "encounterTypes": []
        }
        
    def create_test_config_comprehensive(self) -> Dict:
        """Test Case 2: Comprehensive Configuration (Your Original Prompt)"""
        # Generate UUIDs for address level types
        state_uuid = self.generate_uuid()
        district_uuid = self.generate_uuid()
        block_uuid = self.generate_uuid()
        
        # Generate UUIDs for locations
        karnataka_uuid = self.generate_uuid()
        maharashtra_uuid = self.generate_uuid()
        odisha_uuid = self.generate_uuid()
        bengaluru_uuid = self.generate_uuid()
        mysore_uuid = self.generate_uuid()
        mumbai_uuid = self.generate_uuid()
        pune_uuid = self.generate_uuid()
        bhubaneswar_uuid = self.generate_uuid()
        khordha_uuid = self.generate_uuid()
        
        # Generate UUIDs for subject types
        person_uuid = self.generate_uuid()
        household_uuid = self.generate_uuid()
        health_worker_uuid = self.generate_uuid()
        
        # Generate UUIDs for programs
        maternal_health_uuid = self.generate_uuid()
        nutrition_uuid = self.generate_uuid()
        community_health_uuid = self.generate_uuid()
        
        return {
            "addressLevelTypes": [
                {
                    "name": "State",
                    "uuid": state_uuid,
                    "level": 1.0,
                    "voided": False
                },
                {
                    "name": "District",
                    "uuid": district_uuid,
                    "level": 2.0,
                    "voided": False
                },
                {
                    "name": "Block",
                    "uuid": block_uuid,
                    "level": 3.0,
                    "voided": False
                }
            ],
            "locations": [
                # States
                {
                    "name": "Karnataka",
                    "uuid": karnataka_uuid,
                    "level": 1.0,
                    "type": "State",
                    "addressLevelTypeUUID": state_uuid,
                    "voided": False
                },
                {
                    "name": "Maharashtra", 
                    "uuid": maharashtra_uuid,
                    "level": 1.0,
                    "type": "State",
                    "addressLevelTypeUUID": state_uuid,
                    "voided": False
                },
                {
                    "name": "Odisha",
                    "uuid": odisha_uuid,
                    "level": 1.0,
                    "type": "State",
                    "addressLevelTypeUUID": state_uuid,
                    "voided": False
                },
                # Districts
                {
                    "name": "Bengaluru",
                    "uuid": bengaluru_uuid,
                    "level": 2.0,
                    "type": "District",
                    "addressLevelTypeUUID": district_uuid,
                    "parentLocationUUID": karnataka_uuid,
                    "voided": False
                },
                {
                    "name": "Mysore",
                    "uuid": mysore_uuid,
                    "level": 2.0,
                    "type": "District",
                    "addressLevelTypeUUID": district_uuid,
                    "parentLocationUUID": karnataka_uuid,
                    "voided": False
                },
                {
                    "name": "Mumbai",
                    "uuid": mumbai_uuid,
                    "level": 2.0,
                    "type": "District",
                    "addressLevelTypeUUID": district_uuid,
                    "parentLocationUUID": maharashtra_uuid,
                    "voided": False
                },
                {
                    "name": "Pune",
                    "uuid": pune_uuid,
                    "level": 2.0,
                    "type": "District",
                    "addressLevelTypeUUID": district_uuid,
                    "parentLocationUUID": maharashtra_uuid,
                    "voided": False
                },
                {
                    "name": "Bhubaneswar",
                    "uuid": bhubaneswar_uuid,
                    "level": 2.0,
                    "type": "District",
                    "addressLevelTypeUUID": district_uuid,
                    "parentLocationUUID": odisha_uuid,
                    "voided": False
                },
                # Block
                {
                    "name": "Khordha",
                    "uuid": khordha_uuid,
                    "level": 3.0,
                    "type": "Block",
                    "addressLevelTypeUUID": block_uuid,
                    "parentLocationUUID": bhubaneswar_uuid,
                    "voided": False
                }
            ],
            "subjectTypes": [
                {
                    "name": "Person",
                    "uuid": person_uuid,
                    "group": False,
                    "household": False,
                    "active": True,
                    "type": "Person",
                    "allowEmptyLocation": True,
                    "allowMiddleName": False,
                    "lastNameOptional": False,
                    "allowProfilePicture": False,
                    "uniqueName": False,
                    "directlyAssignable": False,
                    "shouldSyncByLocation": False,
                    "syncRegistrationConcept1Usable": False,
                    "syncRegistrationConcept2Usable": False,
                    "voided": False,
                    "registrationFormUuid": self.generate_uuid()
                },
                {
                    "name": "Household",
                    "uuid": household_uuid,
                    "group": True,
                    "household": True,
                    "active": True,
                    "type": "PersonGroup",
                    "allowEmptyLocation": True,
                    "allowMiddleName": False,
                    "lastNameOptional": False,
                    "allowProfilePicture": False,
                    "uniqueName": False,
                    "directlyAssignable": False,
                    "shouldSyncByLocation": False,
                    "syncRegistrationConcept1Usable": False,
                    "syncRegistrationConcept2Usable": False,
                    "voided": False,
                    "registrationFormUuid": self.generate_uuid()
                },
                {
                    "name": "Health Worker",
                    "uuid": health_worker_uuid,
                    "group": False,
                    "household": False,
                    "active": True,
                    "type": "User",
                    "allowEmptyLocation": True,
                    "allowMiddleName": False,
                    "lastNameOptional": False,
                    "allowProfilePicture": False,
                    "uniqueName": False,
                    "directlyAssignable": False,
                    "shouldSyncByLocation": False,
                    "syncRegistrationConcept1Usable": False,
                    "syncRegistrationConcept2Usable": False,
                    "voided": False,
                    "registrationFormUuid": self.generate_uuid()
                }
            ],
            "programs": [
                {
                    "name": "Maternal Health Program",
                    "uuid": maternal_health_uuid,
                    "colour": "#FF6B6B",
                    "voided": False,
                    "active": True,
                    "manualEligibilityCheckRequired": False,
                    "showGrowthChart": True,
                    "allowMultipleEnrolments": False,
                    "subjectTypeUuid": person_uuid,
                    "programEnrolmentFormUuid": self.generate_uuid(),
                    "programExitFormUuid": self.generate_uuid()
                },
                {
                    "name": "Nutrition Program",
                    "uuid": nutrition_uuid,
                    "colour": "#4ECDC4",
                    "voided": False,
                    "active": True,
                    "manualEligibilityCheckRequired": False,
                    "showGrowthChart": True,
                    "allowMultipleEnrolments": False,
                    "subjectTypeUuid": person_uuid,
                    "programEnrolmentFormUuid": self.generate_uuid(),
                    "programExitFormUuid": self.generate_uuid()
                },
                {
                    "name": "Community Health Program",
                    "uuid": community_health_uuid,
                    "colour": "#45B7D1",
                    "voided": False,
                    "active": True,
                    "manualEligibilityCheckRequired": False,
                    "showGrowthChart": False,
                    "allowMultipleEnrolments": True,
                    "subjectTypeUuid": household_uuid,
                    "programEnrolmentFormUuid": self.generate_uuid(),
                    "programExitFormUuid": self.generate_uuid()
                }
            ],
            "encounterTypes": [
                # General encounters (no program)
                {
                    "name": "General Health Checkup",
                    "uuid": self.generate_uuid(),
                    "active": True,
                    "isImmutable": False,
                    "voided": False,
                    "subjectTypeUuid": person_uuid
                },
                {
                    "name": "Home Visit",
                    "uuid": self.generate_uuid(),
                    "active": True,
                    "isImmutable": False,
                    "voided": False,
                    "subjectTypeUuid": household_uuid
                },
                # Program encounters
                {
                    "name": "Antenatal Care Visit",
                    "uuid": self.generate_uuid(),
                    "active": True,
                    "isImmutable": False,
                    "voided": False,
                    "subjectTypeUuid": person_uuid,
                    "programUuid": maternal_health_uuid
                },
                {
                    "name": "Nutrition Counseling",
                    "uuid": self.generate_uuid(),
                    "active": True,
                    "isImmutable": False,
                    "voided": False,
                    "subjectTypeUuid": person_uuid,
                    "programUuid": nutrition_uuid
                }
            ]
        }
        
    def create_test_config_edge_cases(self) -> Dict:
        """Test Case 3: Edge Cases and Data Validation"""
        return {
            "addressLevelTypes": [
                {
                    "name": "Custom Region",
                    "uuid": self.generate_uuid(),
                    "level": 1.0,
                    "voided": "false"  # String instead of boolean (should be converted)
                }
            ],
            "locations": [
                {
                    "name": "Test Location",
                    "uuid": self.generate_uuid(),
                    "level": 1.0,
                    "type": "Custom Region",
                    "addressLevelTypeUUID": None,  # Will be set
                    "voided": "false",  # String instead of boolean
                    "gpsCoordinates": {"x": 77.5946, "y": 12.9716},  # Bangalore coordinates
                    "locationProperties": {"population": 8500000}
                }
            ],
            "subjectTypes": [],
            "programs": [],
            "encounterTypes": []
        }
        
    def run_config_test(self, test_name: str, config: Dict) -> Tuple[bool, Dict]:
        """Run a configuration test"""
        try:
            # Call the configuration manager with new signature
            result = config_manager_main(
                auth_token=self.auth_token,
                org_type='trial',  # Explicitly set to 'trial' for all tests to bypass Production/UAT restrictions
                config=config,
                user_name=self.user_name,
                org_name=self.implementation_name,
                base_url=self.base_url
            )
            
            # Analyze the result
            if result and isinstance(result, dict):
                # The result is nested under 'configResult'
                config_result = result.get('configResult', result)
                total = config_result.get('summary', {}).get('total', 0)
                successful = config_result.get('summary', {}).get('successful', 0)
                failed = config_result.get('summary', {}).get('failed', 0)
                skipped = config_result.get('summary', {}).get('skipped', 0)
                
                # Consider test passed if at least some entities were processed successfully
                # and no critical errors occurred
                passed = (
                    config_result.get('result') in ['success', 'partial_success'] and
                    (successful > 0 or skipped > 0) and
                    (failed == 0 or failed < total)  # Allow some failures but prefer none
                )
                
                # Special case: if all entities already exist, that's also a success
                if config_result.get('status') == 'all_entities_already_exist':
                    passed = True
                
                message = f"Total: {total}, Success: {successful}, Failed: {failed}, Skipped: {skipped}"
                return passed, result
            else:
                return False, {'error': 'Invalid response from configuration manager'}
                
        except Exception as e:
            return False, {'error': str(e), 'exception_type': type(e).__name__}
            
    def test_basic_hierarchy(self):
        """Test Case 1: Basic Location Hierarchy"""
        config = self.create_test_config_basic_hierarchy()
        
        # Set address level type UUIDs dynamically
        state_uuid = config['addressLevelTypes'][0]['uuid']
        district_uuid = config['addressLevelTypes'][1]['uuid']
        
        config['locations'][0]['addressLevelTypeUUID'] = state_uuid
        config['locations'][1]['addressLevelTypeUUID'] = district_uuid
        config['locations'][2]['addressLevelTypeUUID'] = district_uuid
        
        # Set parent relationship for districts
        state_location_uuid = config['locations'][0]['uuid']
        config['locations'][1]['parentLocationUUID'] = state_location_uuid
        config['locations'][2]['parentLocationUUID'] = state_location_uuid
        
        passed, result = self.run_config_test("Basic Location Hierarchy", config)
        self.log_test_result(
            "test_basic_hierarchy",
            passed,
            "Basic location hierarchy with State and District levels",
            result
        )
        
    def test_comprehensive_config(self):
        """Test Case 2: Comprehensive Configuration"""
        config = self.create_test_config_comprehensive()
        passed, result = self.run_config_test("Comprehensive Configuration", config)
        self.log_test_result(
            "test_comprehensive_config",
            passed,
            "Complete configuration with locations, subjects, programs, and encounters",
            result
        )
        
    def test_edge_cases(self):
        """Test Case 3: Edge Cases and Data Validation"""
        config = self.create_test_config_edge_cases()
        
        # Set address level type UUID
        region_uuid = config['addressLevelTypes'][0]['uuid']
        config['locations'][0]['addressLevelTypeUUID'] = region_uuid
        
        passed, result = self.run_config_test("Edge Cases", config)
        self.log_test_result(
            "test_edge_cases",
            passed,
            "Edge cases with string booleans and custom data",
            result
        )
        
    def test_empty_config(self):
        """Test Case 4: Empty Configuration"""
        config = {
            "addressLevelTypes": [],
            "locations": [],
            "subjectTypes": [],
            "programs": [],
            "encounterTypes": []
        }
        
        passed, result = self.run_config_test("Empty Configuration", config)
        # Empty config should be handled gracefully
        expected_passed = result.get('result') == 'success' and result.get('status') == 'no_entities_to_process'
        self.log_test_result(
            "test_empty_config",
            expected_passed,
            "Empty configuration should be handled gracefully",
            result
        )
        
    def test_invalid_data(self):
        """Test Case 5: Invalid Data Handling"""
        config = {
            "addressLevelTypes": [
                {
                    "name": "",  # Empty name should cause validation error
                    "uuid": "invalid-uuid",  # Invalid UUID format
                    "level": "not-a-number",  # Invalid level type
                    "voided": "maybe"  # Invalid boolean value
                }
            ],
            "locations": [],
            "subjectTypes": [],
            "programs": [],
            "encounterTypes": []
        }
        
        passed, result = self.run_config_test("Invalid Data", config)
        # This should fail gracefully with proper error handling
        expected_passed = result.get('result') in ['partial_success', 'failure'] and 'error' in str(result).lower()
        self.log_test_result(
            "test_invalid_data",
            expected_passed,
            "Invalid data should be handled with proper error messages",
            result
        )
        
    def test_compliance_validation(self):
        """Test Case 6: Assistant Prompt Compliance Validation"""
        # Test missing required keys
        invalid_config = {
            "addressLevelTypes": []
            # Missing required keys: locations, subjectTypes, programs, encounterTypes
        }
        
        passed, result = self.run_config_test("Compliance Validation - Missing Keys", invalid_config)
        # This should fail due to missing required keys
        expected_to_fail = not passed
        self.log_test_result(
            "test_compliance_missing_keys",
            expected_to_fail,
            "Configuration with missing required keys should fail validation",
            result
        )
        
        # Test invalid subject type
        invalid_subject_config = {
            "addressLevelTypes": [],
            "locations": [],
            "subjectTypes": [
                {
                    "name": "Test Subject",
                    "uuid": str(uuid.uuid4()),
                    "type": "InvalidType"  # Invalid: not in allowed enum
                }
            ],
            "programs": [],
            "encounterTypes": []
        }
        
        passed, result = self.run_config_test("Compliance Validation - Invalid Subject Type", invalid_subject_config)
        expected_to_fail = not passed
        self.log_test_result(
            "test_compliance_invalid_subject_type",
            expected_to_fail,
            "Configuration with invalid subject type should fail validation",
            result
        )
        
        # Test valid compliant configuration
        compliant_config = {
            "addressLevelTypes": [
                {
                    "name": "Test State",
                    "uuid": str(uuid.uuid4()),
                    "level": 1.0,
                    "voided": False
                }
            ],
            "locations": [
                {
                    "name": "Test Location",
                    "uuid": str(uuid.uuid4()),
                    "level": 1.0,
                    "type": "Test State",
                    "addressLevelTypeUUID": str(uuid.uuid4()),
                    "voided": False
                }
            ],
            "subjectTypes": [
                {
                    "name": "Person",
                    "uuid": str(uuid.uuid4()),
                    "type": "Person",
                    "group": False,
                    "household": False,
                    "active": True
                }
            ],
            "programs": [
                {
                    "name": "Test Program",
                    "uuid": str(uuid.uuid4()),
                    "colour": "#FF5733",
                    "subjectTypeUuid": str(uuid.uuid4()),
                    "active": True,
                    "voided": False
                }
            ],
            "encounterTypes": [
                {
                    "name": "Test Encounter",
                    "uuid": str(uuid.uuid4()),
                    "subjectTypeUuid": str(uuid.uuid4()),
                    "active": True,
                    "voided": False
                }
            ]
        }
        
        passed, result = self.run_config_test("Compliance Validation - Valid Config", compliant_config)
        self.log_test_result(
            "test_compliance_valid_config",
            passed,
            "Valid compliant configuration should pass validation",
            result
        )
        
    def run_all_tests(self):
        """Run all test cases"""
        print("🚀 Starting Avni Configuration Manager Test Suite")
        print(f"📍 Base URL: {self.base_url}")
        print(f"🔑 Auth Token: {'*' * 20}...{self.auth_token[-10:]}")
        print("=" * 80)
        
        # Run individual tests
        self.test_basic_hierarchy()
        self.test_comprehensive_config()
        self.test_edge_cases()
        self.test_empty_config()
        self.test_invalid_data()
        self.test_compliance_validation()
        
        # Print summary
        self.print_test_summary()
        
    def print_test_summary(self):
        """Print comprehensive test summary"""
        print("\n" + "=" * 80)
        print("📊 TEST SUITE SUMMARY")
        print("=" * 80)
        print(f"Total Tests: {self.total_tests}")
        print(f"✅ Passed: {self.passed_tests}")
        print(f"❌ Failed: {self.failed_tests}")
        print(f"📈 Success Rate: {(self.passed_tests/self.total_tests*100):.1f}%")
        
        if self.failed_tests > 0:
            print("\n🔍 FAILED TESTS:")
            for result in self.test_results:
                if not result['passed']:
                    print(f"  ❌ {result['test_name']}: {result['message']}")
                    if result['details'].get('error'):
                        print(f"     Error: {result['details']['error']}")
        
        print("\n📋 DETAILED RESULTS:")
        for result in self.test_results:
            print(f"  {result['status']} {result['test_name']}")
            print(f"    Message: {result['message']}")
            if result['details']:
                summary = result['details'].get('summary', {})
                if summary:
                    print(f"    Summary: {summary}")
            print()
            
        # Save detailed results to file
        with open('test_results.json', 'w') as f:
            json.dump(self.test_results, f, indent=2)
        print("💾 Detailed results saved to test_results.json")


def main():
    """Main function to run the test suite"""
    parser = argparse.ArgumentParser(description='Avni Configuration Manager Test Suite')
    parser.add_argument('--auth-token', required=True, help='Avni authentication token')
    parser.add_argument('--base-url', required=True, help='Avni base URL (e.g., https://staging.avniproject.org)')
    parser.add_argument('--user-name', help='User name for API calls (e.g., noopur@copilot)')
    parser.add_argument('--implementation-name', help='Implementation name for cookies (e.g., copilot)', default='test-suite')
    parser.add_argument('--test-case', help='Run specific test case only', 
                       choices=['basic', 'comprehensive', 'edge', 'empty', 'invalid', 'compliance', 'all'],
                       default='all')
    
    args = parser.parse_args()
    
    # Prompt for user name if not provided
    user_name = args.user_name
    if not user_name:
        user_name = input("Enter your Avni user name (e.g., noopur@copilot): ").strip()
    
    # Create and run test suite
    test_suite = AvniConfigTestSuite(args.auth_token, args.base_url, user_name, args.implementation_name)
    
    if args.test_case == 'all':
        test_suite.run_all_tests()
    elif args.test_case == 'basic':
        test_suite.test_basic_hierarchy()
        test_suite.print_test_summary()
    elif args.test_case == 'comprehensive':
        test_suite.test_comprehensive_config()
        test_suite.print_test_summary()
    elif args.test_case == 'edge':
        test_suite.test_edge_cases()
        test_suite.print_test_summary()
    elif args.test_case == 'empty':
        test_suite.test_empty_config()
        test_suite.print_test_summary()
    elif args.test_case == 'invalid':
        test_suite.test_invalid_data()
        test_suite.print_test_summary()
    elif args.test_case == 'compliance':
        test_suite.test_compliance_validation()
        test_suite.print_test_summary()


if __name__ == "__main__":
    main()
