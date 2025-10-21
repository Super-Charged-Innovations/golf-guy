#!/usr/bin/env python3
"""
Test Demo User Login Functionality
Tests the newly created demo users with proper schema including full_name, is_active, and is_admin fields
"""

import requests
import json
from datetime import datetime

# Configuration
BACKEND_URL = "https://golf-travel-app.preview.emergentagent.com/api"

# Demo user credentials
ADMIN_USER = {
    "email": "admin@dgolf.se",
    "password": "Admin123!"
}

STANDARD_USER = {
    "email": "user@dgolf.se",
    "password": "User123!"
}

class DemoUserTester:
    def __init__(self):
        self.session = requests.Session()
        self.test_results = []
        
    def log_test(self, test_name, success, details="", response_data=None):
        """Log test results"""
        status = "✅ PASS" if success else "❌ FAIL"
        result = {
            "test": test_name,
            "status": status,
            "success": success,
            "details": details,
            "response_data": response_data,
            "timestamp": datetime.now().isoformat()
        }
        self.test_results.append(result)
        print(f"{status} {test_name}: {details}")
        if not success and response_data:
            print(f"   Response: {json.dumps(response_data, indent=2)}")
    
    def test_admin_login(self):
        """Test admin user login"""
        print("\n👑 TESTING ADMIN USER LOGIN")
        print(f"   Email: {ADMIN_USER['email']}")
        
        try:
            response = self.session.post(
                f"{BACKEND_URL}/auth/login",
                json=ADMIN_USER,
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Check for access_token
                if 'access_token' not in data:
                    self.log_test("Admin Login - Token", False, "access_token missing from response", data)
                    return None
                
                # Check for user object
                if 'user' not in data:
                    self.log_test("Admin Login - User Object", False, "user object missing from response", data)
                    return None
                
                user = data['user']
                
                # Verify full_name field
                if 'full_name' not in user:
                    self.log_test("Admin Login - full_name Field", False, "full_name field missing from user object", user)
                    return None
                
                if user['full_name'] != "Admin User":
                    self.log_test("Admin Login - full_name Value", False, f"Expected 'Admin User', got '{user['full_name']}'", user)
                else:
                    self.log_test("Admin Login - full_name Value", True, f"full_name correctly set to '{user['full_name']}'")
                
                # Verify is_admin field
                if 'is_admin' not in user:
                    self.log_test("Admin Login - is_admin Field", False, "is_admin field missing from user object", user)
                    return None
                
                if user['is_admin'] != True:
                    self.log_test("Admin Login - is_admin Value", False, f"Expected True, got {user['is_admin']}", user)
                else:
                    self.log_test("Admin Login - is_admin Value", True, "is_admin correctly set to True")
                
                # Verify email
                if user.get('email') != ADMIN_USER['email']:
                    self.log_test("Admin Login - Email", False, f"Email mismatch: {user.get('email')}", user)
                else:
                    self.log_test("Admin Login - Email", True, f"Email correct: {user['email']}")
                
                # Verify id field exists
                if 'id' not in user:
                    self.log_test("Admin Login - ID Field", False, "id field missing from user object", user)
                else:
                    self.log_test("Admin Login - ID Field", True, f"User ID: {user['id']}")
                
                self.log_test("Admin Login - Overall", True, "Admin login successful with all required fields")
                return data['access_token']
                
            else:
                error_detail = response.text
                self.log_test("Admin Login - Overall", False, f"Login failed with status {response.status_code}: {error_detail}")
                return None
                
        except Exception as e:
            self.log_test("Admin Login - Overall", False, f"Exception occurred: {str(e)}")
            return None
    
    def test_standard_user_login(self):
        """Test standard user login"""
        print("\n👤 TESTING STANDARD USER LOGIN")
        print(f"   Email: {STANDARD_USER['email']}")
        
        try:
            response = self.session.post(
                f"{BACKEND_URL}/auth/login",
                json=STANDARD_USER,
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Check for access_token
                if 'access_token' not in data:
                    self.log_test("Standard User Login - Token", False, "access_token missing from response", data)
                    return None
                
                # Check for user object
                if 'user' not in data:
                    self.log_test("Standard User Login - User Object", False, "user object missing from response", data)
                    return None
                
                user = data['user']
                
                # Verify full_name field
                if 'full_name' not in user:
                    self.log_test("Standard User Login - full_name Field", False, "full_name field missing from user object", user)
                    return None
                
                if user['full_name'] != "Standard User":
                    self.log_test("Standard User Login - full_name Value", False, f"Expected 'Standard User', got '{user['full_name']}'", user)
                else:
                    self.log_test("Standard User Login - full_name Value", True, f"full_name correctly set to '{user['full_name']}'")
                
                # Verify is_admin field
                if 'is_admin' not in user:
                    self.log_test("Standard User Login - is_admin Field", False, "is_admin field missing from user object", user)
                    return None
                
                if user['is_admin'] != False:
                    self.log_test("Standard User Login - is_admin Value", False, f"Expected False, got {user['is_admin']}", user)
                else:
                    self.log_test("Standard User Login - is_admin Value", True, "is_admin correctly set to False")
                
                # Verify email
                if user.get('email') != STANDARD_USER['email']:
                    self.log_test("Standard User Login - Email", False, f"Email mismatch: {user.get('email')}", user)
                else:
                    self.log_test("Standard User Login - Email", True, f"Email correct: {user['email']}")
                
                # Verify id field exists
                if 'id' not in user:
                    self.log_test("Standard User Login - ID Field", False, "id field missing from user object", user)
                else:
                    self.log_test("Standard User Login - ID Field", True, f"User ID: {user['id']}")
                
                self.log_test("Standard User Login - Overall", True, "Standard user login successful with all required fields")
                return data['access_token']
                
            else:
                error_detail = response.text
                self.log_test("Standard User Login - Overall", False, f"Login failed with status {response.status_code}: {error_detail}")
                return None
                
        except Exception as e:
            self.log_test("Standard User Login - Overall", False, f"Exception occurred: {str(e)}")
            return None
    
    def test_invalid_credentials(self):
        """Test login with invalid credentials"""
        print("\n🔒 TESTING INVALID CREDENTIALS")
        
        invalid_login = {
            "email": "admin@dgolf.se",
            "password": "WrongPassword123!"
        }
        
        try:
            response = self.session.post(
                f"{BACKEND_URL}/auth/login",
                json=invalid_login,
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 401:
                self.log_test("Invalid Credentials", True, "Invalid credentials properly rejected with 401 status")
            else:
                self.log_test("Invalid Credentials", False, f"Expected 401, got {response.status_code}")
                
        except Exception as e:
            self.log_test("Invalid Credentials", False, f"Exception occurred: {str(e)}")
    
    def test_authenticated_endpoint(self, token, user_type):
        """Test authenticated endpoint with token"""
        print(f"\n🔐 TESTING AUTHENTICATED ENDPOINT ({user_type})")
        
        if not token:
            self.log_test(f"Auth Endpoint - {user_type}", False, "No token available for testing")
            return
        
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        
        try:
            response = self.session.get(f"{BACKEND_URL}/auth/me", headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                
                # Verify all required fields are present
                required_fields = ['id', 'email', 'full_name', 'is_admin']
                missing_fields = [field for field in required_fields if field not in data]
                
                if missing_fields:
                    self.log_test(f"Auth Endpoint - {user_type} Fields", False, f"Missing fields: {missing_fields}", data)
                else:
                    self.log_test(f"Auth Endpoint - {user_type} Fields", True, "All required fields present")
                
                # Verify full_name is not empty
                if not data.get('full_name'):
                    self.log_test(f"Auth Endpoint - {user_type} full_name", False, "full_name is empty", data)
                else:
                    self.log_test(f"Auth Endpoint - {user_type} full_name", True, f"full_name: {data['full_name']}")
                
                # Verify is_admin is boolean
                if not isinstance(data.get('is_admin'), bool):
                    self.log_test(f"Auth Endpoint - {user_type} is_admin Type", False, f"is_admin is not boolean: {type(data.get('is_admin'))}", data)
                else:
                    self.log_test(f"Auth Endpoint - {user_type} is_admin Type", True, f"is_admin: {data['is_admin']}")
                
                self.log_test(f"Auth Endpoint - {user_type} Overall", True, "Authenticated endpoint working correctly")
                
            else:
                error_detail = response.text
                self.log_test(f"Auth Endpoint - {user_type} Overall", False, f"Request failed with status {response.status_code}: {error_detail}")
                
        except Exception as e:
            self.log_test(f"Auth Endpoint - {user_type} Overall", False, f"Exception occurred: {str(e)}")
    
    def print_summary(self):
        """Print test summary"""
        print("\n" + "="*80)
        print("TEST SUMMARY")
        print("="*80)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result['success'])
        failed_tests = total_tests - passed_tests
        
        print(f"\nTotal Tests: {total_tests}")
        print(f"Passed: {passed_tests} ✅")
        print(f"Failed: {failed_tests} ❌")
        print(f"Success Rate: {(passed_tests/total_tests*100):.1f}%")
        
        if failed_tests > 0:
            print("\n" + "="*80)
            print("FAILED TESTS:")
            print("="*80)
            for result in self.test_results:
                if not result['success']:
                    print(f"\n❌ {result['test']}")
                    print(f"   Details: {result['details']}")
                    if result['response_data']:
                        print(f"   Response: {json.dumps(result['response_data'], indent=2)}")
        
        print("\n" + "="*80)
        
        return failed_tests == 0

def main():
    """Main test execution"""
    print("="*80)
    print("DEMO USER LOGIN FUNCTIONALITY TEST")
    print("="*80)
    print(f"Backend URL: {BACKEND_URL}")
    print(f"Test Time: {datetime.now().isoformat()}")
    
    tester = DemoUserTester()
    
    # Test admin login
    admin_token = tester.test_admin_login()
    
    # Test standard user login
    standard_token = tester.test_standard_user_login()
    
    # Test invalid credentials
    tester.test_invalid_credentials()
    
    # Test authenticated endpoints
    if admin_token:
        tester.test_authenticated_endpoint(admin_token, "Admin User")
    
    if standard_token:
        tester.test_authenticated_endpoint(standard_token, "Standard User")
    
    # Print summary
    all_passed = tester.print_summary()
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    exit(main())
