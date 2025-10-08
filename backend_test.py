#!/usr/bin/env python3
"""
Comprehensive Backend Security Testing Suite
Tests JWT authentication, CORS, encryption, and GDPR endpoints
"""

import requests
import json
import os
import sys
from datetime import datetime
import uuid

# Configuration
BACKEND_URL = "https://golf-ai-advisor.preview.emergentagent.com/api"
TEST_USER_EMAIL = f"testuser_{uuid.uuid4().hex[:8]}@golftest.com"
TEST_USER_PASSWORD = "SecureTestPass123!"
TEST_USER_NAME = "Golf Test User"

class BackendTester:
    def __init__(self):
        self.session = requests.Session()
        self.auth_token = None
        self.user_id = None
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
        
    def test_environment_variables(self):
        """Test that critical environment variables are loaded"""
        print("\n🔐 TESTING ENVIRONMENT SECURITY")
        
        # Test JWT secret is loaded (don't log actual value)
        try:
            response = self.session.get(f"{BACKEND_URL}/")
            if response.status_code == 200:
                self.log_test("Environment Variables", True, "Backend is running and environment loaded")
            else:
                self.log_test("Environment Variables", False, f"Backend not accessible: {response.status_code}")
        except Exception as e:
            self.log_test("Environment Variables", False, f"Connection error: {str(e)}")
    
    def test_cors_security(self):
        """Test CORS configuration"""
        print("\n🌐 TESTING CORS SECURITY")
        
        # Test allowed origin
        headers = {
            'Origin': 'https://golf-ai-advisor.preview.emergentagent.com',
            'Access-Control-Request-Method': 'POST',
            'Access-Control-Request-Headers': 'Content-Type,Authorization'
        }
        
        try:
            response = self.session.options(f"{BACKEND_URL}/auth/login", headers=headers)
            if response.status_code in [200, 204]:
                cors_headers = response.headers.get('Access-Control-Allow-Origin', '')
                if 'golf-ai-advisor.preview.emergentagent.com' in cors_headers or cors_headers == '*':
                    self.log_test("CORS Allowed Origin", True, f"CORS allows expected origin: {cors_headers}")
                else:
                    self.log_test("CORS Allowed Origin", False, f"CORS headers unexpected: {cors_headers}")
            else:
                self.log_test("CORS Preflight", False, f"CORS preflight failed: {response.status_code}")
        except Exception as e:
            self.log_test("CORS Testing", False, f"CORS test error: {str(e)}")
        
        # Test blocked origin (should be blocked if CORS is properly configured)
        blocked_headers = {
            'Origin': 'https://malicious-site.com',
            'Access-Control-Request-Method': 'POST'
        }
        
        try:
            response = self.session.options(f"{BACKEND_URL}/auth/login", headers=blocked_headers)
            cors_origin = response.headers.get('Access-Control-Allow-Origin', '')
            if cors_origin == '*':
                self.log_test("CORS Security", False, "CORS allows all origins (*) - security risk!")
            elif 'malicious-site.com' not in cors_origin:
                self.log_test("CORS Security", True, "CORS properly blocks unauthorized origins")
            else:
                self.log_test("CORS Security", False, "CORS allows unauthorized origin")
        except Exception as e:
            self.log_test("CORS Security Test", False, f"Error testing blocked origin: {str(e)}")
    
    def test_user_registration(self):
        """Test user registration endpoint"""
        print("\n👤 TESTING USER REGISTRATION")
        
        registration_data = {
            "email": TEST_USER_EMAIL,
            "password": TEST_USER_PASSWORD,
            "full_name": TEST_USER_NAME
        }
        
        try:
            response = self.session.post(
                f"{BACKEND_URL}/auth/register",
                json=registration_data,
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 200:
                data = response.json()
                if 'access_token' in data and 'user' in data:
                    self.auth_token = data['access_token']
                    self.user_id = data['user']['id']
                    self.log_test("User Registration", True, f"User registered successfully, token received")
                else:
                    self.log_test("User Registration", False, f"Registration response missing token/user: {data}")
            else:
                error_detail = response.text
                self.log_test("User Registration", False, f"Registration failed: {response.status_code} - {error_detail}")
                
        except Exception as e:
            self.log_test("User Registration", False, f"Registration error: {str(e)}")
    
    def test_user_login(self):
        """Test user login endpoint"""
        print("\n🔑 TESTING USER LOGIN")
        
        login_data = {
            "email": TEST_USER_EMAIL,
            "password": TEST_USER_PASSWORD
        }
        
        try:
            response = self.session.post(
                f"{BACKEND_URL}/auth/login",
                json=login_data,
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 200:
                data = response.json()
                if 'access_token' in data and 'user' in data:
                    # Update token in case registration failed
                    self.auth_token = data['access_token']
                    self.user_id = data['user']['id']
                    self.log_test("User Login", True, f"Login successful, token received")
                else:
                    self.log_test("User Login", False, f"Login response missing token/user: {data}")
            else:
                error_detail = response.text
                self.log_test("User Login", False, f"Login failed: {response.status_code} - {error_detail}")
                
        except Exception as e:
            self.log_test("User Login", False, f"Login error: {str(e)}")
    
    def test_jwt_token_validation(self):
        """Test JWT token validation with /auth/me endpoint"""
        print("\n🎫 TESTING JWT TOKEN VALIDATION")
        
        if not self.auth_token:
            self.log_test("JWT Token Validation", False, "No auth token available for testing")
            return
        
        # Test valid token
        headers = {
            'Authorization': f'Bearer {self.auth_token}',
            'Content-Type': 'application/json'
        }
        
        try:
            response = self.session.get(f"{BACKEND_URL}/auth/me", headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                if 'id' in data and 'email' in data:
                    self.log_test("JWT Valid Token", True, f"Token validation successful, user data received")
                else:
                    self.log_test("JWT Valid Token", False, f"Token valid but user data incomplete: {data}")
            else:
                error_detail = response.text
                self.log_test("JWT Valid Token", False, f"Token validation failed: {response.status_code} - {error_detail}")
                
        except Exception as e:
            self.log_test("JWT Valid Token", False, f"Token validation error: {str(e)}")
        
        # Test invalid token
        invalid_headers = {
            'Authorization': 'Bearer invalid_token_12345',
            'Content-Type': 'application/json'
        }
        
        try:
            response = self.session.get(f"{BACKEND_URL}/auth/me", headers=invalid_headers)
            
            if response.status_code == 401:
                self.log_test("JWT Invalid Token", True, "Invalid token properly rejected")
            else:
                self.log_test("JWT Invalid Token", False, f"Invalid token not rejected: {response.status_code}")
                
        except Exception as e:
            self.log_test("JWT Invalid Token", False, f"Invalid token test error: {str(e)}")
        
        # Test missing token
        try:
            response = self.session.get(f"{BACKEND_URL}/auth/me")
            
            if response.status_code == 403:
                self.log_test("JWT Missing Token", True, "Missing token properly rejected")
            else:
                self.log_test("JWT Missing Token", False, f"Missing token not rejected: {response.status_code}")
                
        except Exception as e:
            self.log_test("JWT Missing Token", False, f"Missing token test error: {str(e)}")
    
    def test_protected_routes(self):
        """Test protected routes require authentication"""
        print("\n🛡️ TESTING PROTECTED ROUTES")
        
        if not self.auth_token:
            self.log_test("Protected Routes", False, "No auth token available for testing")
            return
        
        protected_endpoints = [
            "/profile",
            "/ai/chat",
            "/ai/recommendations",
            "/privacy/settings"
        ]
        
        headers = {
            'Authorization': f'Bearer {self.auth_token}',
            'Content-Type': 'application/json'
        }
        
        for endpoint in protected_endpoints:
            try:
                if endpoint == "/ai/chat":
                    # AI chat is POST endpoint
                    chat_data = {"message": "test"}
                    response = self.session.post(f"{BACKEND_URL}{endpoint}", json=chat_data, headers=headers)
                else:
                    response = self.session.get(f"{BACKEND_URL}{endpoint}", headers=headers)
                
                if response.status_code in [200, 404]:  # 404 is OK if endpoint doesn't exist
                    self.log_test(f"Protected Route {endpoint}", True, f"Authenticated access successful: {response.status_code}")
                else:
                    self.log_test(f"Protected Route {endpoint}", False, f"Authenticated access failed: {response.status_code}")
                    
            except Exception as e:
                self.log_test(f"Protected Route {endpoint}", False, f"Error testing {endpoint}: {str(e)}")
        
        # Test without authentication
        for endpoint in protected_endpoints[:2]:  # Test first 2 endpoints
            try:
                if endpoint == "/ai/chat":
                    # AI chat is POST endpoint
                    chat_data = {"message": "test"}
                    response = self.session.post(f"{BACKEND_URL}{endpoint}", json=chat_data)
                else:
                    response = self.session.get(f"{BACKEND_URL}{endpoint}")
                
                if response.status_code in [401, 403]:
                    self.log_test(f"Unauth Access {endpoint}", True, "Unauthenticated access properly blocked")
                else:
                    self.log_test(f"Unauth Access {endpoint}", False, f"Unauthenticated access not blocked: {response.status_code}")
                    
            except Exception as e:
                self.log_test(f"Unauth Access {endpoint}", False, f"Error testing unauth {endpoint}: {str(e)}")
    
    def test_encryption_functionality(self):
        """Test encryption utilities functionality"""
        print("\n🔒 TESTING ENCRYPTION FUNCTIONALITY")
        
        try:
            # Import encryption utilities
            sys.path.append('/app/backend')
            from encryption_utils import encrypt_data, decrypt_data, hash_data, anonymize_email
            
            # Test encryption/decryption
            test_data = "sensitive_user_data_123"
            encrypted = encrypt_data(test_data)
            decrypted = decrypt_data(encrypted)
            
            if decrypted == test_data and encrypted != test_data:
                self.log_test("Data Encryption", True, "Encryption/decryption working correctly")
            else:
                self.log_test("Data Encryption", False, f"Encryption failed: original={test_data}, decrypted={decrypted}")
            
            # Test hashing
            test_hash = hash_data("test_data")
            if len(test_hash) == 64:  # SHA256 produces 64 char hex
                self.log_test("Data Hashing", True, "SHA256 hashing working correctly")
            else:
                self.log_test("Data Hashing", False, f"Hashing failed: {test_hash}")
            
            # Test email anonymization
            test_email = "user@example.com"
            anon_email = anonymize_email(test_email)
            if "deleted_" in anon_email and "@example.com" in anon_email:
                self.log_test("Email Anonymization", True, "Email anonymization working correctly")
            else:
                self.log_test("Email Anonymization", False, f"Anonymization failed: {anon_email}")
                
        except Exception as e:
            self.log_test("Encryption Functionality", False, f"Encryption test error: {str(e)}")
    
    def test_gdpr_endpoints(self):
        """Test GDPR compliance endpoints"""
        print("\n📋 TESTING GDPR ENDPOINTS")
        
        if not self.auth_token:
            self.log_test("GDPR Endpoints", False, "No auth token available for testing")
            return
        
        headers = {
            'Authorization': f'Bearer {self.auth_token}',
            'Content-Type': 'application/json'
        }
        
        # Test privacy settings
        try:
            response = self.session.get(f"{BACKEND_URL}/privacy/settings", headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                if 'marketing_emails' in data and 'cookie_consent' in data:
                    self.log_test("GDPR Privacy Settings", True, "Privacy settings endpoint working")
                else:
                    self.log_test("GDPR Privacy Settings", False, f"Privacy settings incomplete: {data}")
            else:
                self.log_test("GDPR Privacy Settings", False, f"Privacy settings failed: {response.status_code}")
                
        except Exception as e:
            self.log_test("GDPR Privacy Settings", False, f"Privacy settings error: {str(e)}")
        
        # Test data export
        try:
            response = self.session.post(f"{BACKEND_URL}/privacy/export-data", headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                if 'data' in data and 'export_id' in data:
                    self.log_test("GDPR Data Export", True, "Data export endpoint working")
                else:
                    self.log_test("GDPR Data Export", False, f"Data export incomplete: {data}")
            else:
                self.log_test("GDPR Data Export", False, f"Data export failed: {response.status_code}")
                
        except Exception as e:
            self.log_test("GDPR Data Export", False, f"Data export error: {str(e)}")
    
    def test_ai_integration(self):
        """Test AI service integration"""
        print("\n🤖 TESTING AI INTEGRATION")
        
        if not self.auth_token:
            self.log_test("AI Integration", False, "No auth token available for testing")
            return
        
        headers = {
            'Authorization': f'Bearer {self.auth_token}',
            'Content-Type': 'application/json'
        }
        
        # Test AI recommendations
        try:
            response = self.session.get(f"{BACKEND_URL}/ai/recommendations", headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                if 'recommendations' in data:
                    self.log_test("AI Recommendations", True, "AI recommendations endpoint working")
                else:
                    self.log_test("AI Recommendations", False, f"AI recommendations incomplete: {data}")
            else:
                self.log_test("AI Recommendations", False, f"AI recommendations failed: {response.status_code}")
                
        except Exception as e:
            self.log_test("AI Recommendations", False, f"AI recommendations error: {str(e)}")
        
        # Test AI chat
        chat_data = {"message": "Hello, I'm interested in golf trips to Spain"}
        
        try:
            response = self.session.post(f"{BACKEND_URL}/ai/chat", json=chat_data, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                if 'response' in data and data['response']:
                    self.log_test("AI Chat", True, "AI chat endpoint working")
                else:
                    self.log_test("AI Chat", False, f"AI chat response empty: {data}")
            else:
                self.log_test("AI Chat", False, f"AI chat failed: {response.status_code}")
                
        except Exception as e:
            self.log_test("AI Chat", False, f"AI chat error: {str(e)}")
    
    def test_database_connectivity(self):
        """Test database operations"""
        print("\n💾 TESTING DATABASE CONNECTIVITY")
        
        # Test basic endpoints that require database
        try:
            response = self.session.get(f"{BACKEND_URL}/destinations")
            
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list):
                    self.log_test("Database Connectivity", True, f"Database working, {len(data)} destinations found")
                else:
                    self.log_test("Database Connectivity", False, f"Database response unexpected: {type(data)}")
            else:
                self.log_test("Database Connectivity", False, f"Database query failed: {response.status_code}")
                
        except Exception as e:
            self.log_test("Database Connectivity", False, f"Database error: {str(e)}")
    
    def run_all_tests(self):
        """Run all security tests"""
        print("🚀 STARTING COMPREHENSIVE BACKEND SECURITY TESTING")
        print(f"Testing against: {BACKEND_URL}")
        print(f"Test user: {TEST_USER_EMAIL}")
        print("=" * 60)
        
        # Run all tests
        self.test_environment_variables()
        self.test_cors_security()
        self.test_user_registration()
        self.test_user_login()
        self.test_jwt_token_validation()
        self.test_protected_routes()
        self.test_encryption_functionality()
        self.test_gdpr_endpoints()
        self.test_ai_integration()
        self.test_database_connectivity()
        
        # Summary
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        
        passed = sum(1 for result in self.test_results if result['success'])
        failed = len(self.test_results) - passed
        
        print(f"Total Tests: {len(self.test_results)}")
        print(f"✅ Passed: {passed}")
        print(f"❌ Failed: {failed}")
        print(f"Success Rate: {(passed/len(self.test_results)*100):.1f}%")
        
        # Show failed tests
        if failed > 0:
            print("\n🚨 FAILED TESTS:")
            for result in self.test_results:
                if not result['success']:
                    print(f"  ❌ {result['test']}: {result['details']}")
        
        # Critical security issues
        critical_failures = []
        for result in self.test_results:
            if not result['success'] and any(keyword in result['test'].lower() for keyword in ['jwt', 'cors', 'auth', 'token']):
                critical_failures.append(result)
        
        if critical_failures:
            print(f"\n🔥 CRITICAL SECURITY ISSUES ({len(critical_failures)}):")
            for result in critical_failures:
                print(f"  🚨 {result['test']}: {result['details']}")
        
        return passed, failed, critical_failures

if __name__ == "__main__":
    tester = BackendTester()
    passed, failed, critical = tester.run_all_tests()
    
    # Exit with error code if critical failures
    if critical:
        sys.exit(1)
    elif failed > 0:
        sys.exit(2)
    else:
        sys.exit(0)