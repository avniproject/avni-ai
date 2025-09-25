#!/usr/bin/env python3
"""
Simple Test Runner for Avni Configuration Manager

This script provides an easy way to run tests with your credentials.
"""

import os
import sys
from test_config_manager import AvniConfigTestSuite

def main():
    """Run tests with your credentials"""
    
    # TODO: Replace these with your actual values
    AUTH_TOKEN = "eyJraWQiOiJlQWdKblRMcnJyNVRKUFB6eGtLbWIzNStFUnFjcllPYmNZam5EdUtoWElvPSIsImFsZyI6IlJTMjU2In0.eyJzdWIiOiIxYWZmMmRiYy03OThhLTQ0MjgtOGE3YS02MTJhZTVjM2RkMDkiLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiaXNzIjoiaHR0cHM6XC9cL2NvZ25pdG8taWRwLmFwLXNvdXRoLTEuYW1hem9uYXdzLmNvbVwvYXAtc291dGgtMV9oV0VPdmpaVUgiLCJwaG9uZV9udW1iZXJfdmVyaWZpZWQiOnRydWUsImNvZ25pdG86dXNlcm5hbWUiOiJoaW1lc2hSIiwiY3VzdG9tOnVzZXJVVUlEIjoiNGEyZjQ2OGUtZDNjMS00NDUyLWI3MWYtOTY4N2M1MmM5ZTYwIiwiYXVkIjoiN2Ric3JnZzU2bXB0cjR1ZTFnNjVudjNzODYiLCJldmVudF9pZCI6ImFiYWYxYzYwLTY3YjMtNDMzZi04NmNkLWY4YTgyMzMwNjNlNyIsInRva2VuX3VzZSI6ImlkIiwiYXV0aF90aW1lIjoxNzU4NTQyMzM0LCJwaG9uZV9udW1iZXIiOiIrOTE5NzQxMDgzNzU1IiwiZXhwIjoxNzU4ODEwMDE3LCJpYXQiOjE3NTg4MDY0MTcsImVtYWlsIjoiaGltZXNobEBzYW1hbnZheWZvdW5kYXRpb24ub3JnIn0.H93wmK8713wtQ4Act2K-AHgpCfXpUJPPs8lKMgdOHYinKpbcImwiTYiEly59seLmcmrXgi43MP2UmMVR3ld0FKZ8Tpff-u4blcVlXSRyrVzVY7b-BOzOJaI3_JNJaWXiQwOMJlEJOwxhVSz9ODAI5V0ocLFoeYwYiDnvFkiVTxsPh9etfUVk_cPtWlnXZsnCIHnvmYNtE95hiqUZ23R83u_QJ7q_36TCQMM19DNHrtO811VukLZ5ACgx9n1LwHYzd2JJ52GmILgi49cAar_Lqsbcw27FBK8KWONevU4AsWy7NqfhtqGwaj9RiWNVR-h1NlyfMdSFGqeY7j7oOFXigw"
    BASE_URL = "https://staging.avniproject.org"  # or your production URL
    USER_NAME = "himeshR"  # Replace with your Avni username
    ORG_NAME = "test-suite"  # Replace with your organization name if different
    
    # Validate credentials
    if AUTH_TOKEN == "your-auth-token-here":
        print("❌ Please update AUTH_TOKEN in run_tests.py with your actual token")
        print("💡 You can get your token from the Avni web application")
        return
        
    if not BASE_URL.startswith("https://"):
        print("❌ Please provide a valid BASE_URL (should start with https://)")
        return
    
    print("🧪 Running Avni Configuration Manager Tests")
    print(f"🌐 Base URL: {BASE_URL}")
    print(f"👤 User: {USER_NAME}")
    print(f"🏢 Organization: {ORG_NAME}")
    print(f"🔐 Token: {'*' * 20}...{AUTH_TOKEN[-10:]}")
    
    # Create and run test suite
    test_suite = AvniConfigTestSuite(AUTH_TOKEN, BASE_URL, USER_NAME, ORG_NAME)
    test_suite.run_all_tests()

if __name__ == "__main__":
    main()
