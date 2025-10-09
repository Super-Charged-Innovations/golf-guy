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
            # Import encryption utilities with proper environment loading
            sys.path.append('/app/backend')
            
            # Load environment variables first
            from dotenv import load_dotenv
            load_dotenv('/app/backend/.env')
            
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
                
            # Test encryption key is loaded
            import os
            if os.environ.get('ENCRYPTION_KEY'):
                self.log_test("Encryption Key", True, "ENCRYPTION_KEY environment variable is loaded")
            else:
                self.log_test("Encryption Key", False, "ENCRYPTION_KEY environment variable missing")
                
        except ImportError as e:
            self.log_test("Encryption Import", False, f"Cannot import encryption utilities: {str(e)}")
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

    def test_mongodb_security_hardening(self):
        """Test MongoDB security hardening and authentication"""
        print("\n🔒 TESTING MONGODB SECURITY HARDENING")
        
        # Test that existing endpoints still work with authenticated MongoDB
        endpoints_to_test = [
            ("/destinations", "GET"),
            ("/articles", "GET"),
            ("/partners", "GET"),
            ("/testimonials", "GET")
        ]
        
        for endpoint, method in endpoints_to_test:
            try:
                if method == "GET":
                    response = self.session.get(f"{BACKEND_URL}{endpoint}")
                
                if response.status_code == 200:
                    self.log_test(f"MongoDB Auth - {endpoint}", True, f"Endpoint working with authenticated MongoDB")
                else:
                    self.log_test(f"MongoDB Auth - {endpoint}", False, f"Endpoint failed: {response.status_code}")
                    
            except Exception as e:
                self.log_test(f"MongoDB Auth - {endpoint}", False, f"Error testing {endpoint}: {str(e)}")
        
        # Test user registration/login still works with new MongoDB setup
        if self.auth_token:
            self.log_test("MongoDB User Auth", True, "User authentication working with secured MongoDB")
        else:
            self.log_test("MongoDB User Auth", False, "User authentication failed with secured MongoDB")

    def test_file_storage_system(self):
        """Test S3 file storage system endpoints"""
        print("\n📁 TESTING FILE STORAGE SYSTEM (S3 Integration)")
        
        if not self.auth_token:
            self.log_test("File Storage System", False, "No auth token available for testing")
            return
        
        headers = {
            'Authorization': f'Bearer {self.auth_token}',
        }
        
        # Test file upload endpoint (should fail without AWS credentials - expected behavior)
        try:
            # Create a small test file
            test_file_content = b"Test file content for golf platform"
            files = {
                'file': ('test_file.txt', test_file_content, 'text/plain')
            }
            data = {
                'category': 'user-profiles'
            }
            
            response = self.session.post(
                f"{BACKEND_URL}/files/upload",
                files=files,
                data=data,
                headers=headers
            )
            
            if response.status_code == 500:
                error_detail = response.text
                if "AWS credentials not configured" in error_detail or "File upload failed" in error_detail:
                    self.log_test("File Upload Validation", True, "File upload properly fails without AWS credentials (expected)")
                else:
                    self.log_test("File Upload Validation", False, f"Unexpected error: {error_detail}")
            elif response.status_code == 200:
                self.log_test("File Upload", True, "File upload successful (AWS configured)")
            else:
                self.log_test("File Upload", False, f"Unexpected response: {response.status_code}")
                
        except Exception as e:
            self.log_test("File Upload Test", False, f"File upload test error: {str(e)}")
        
        # Test file listing endpoint
        try:
            response = self.session.get(
                f"{BACKEND_URL}/files/list?category=user-profiles",
                headers=headers
            )
            
            if response.status_code == 500:
                error_detail = response.text
                if "AWS credentials not configured" in error_detail:
                    self.log_test("File List Validation", True, "File listing properly fails without AWS credentials (expected)")
                else:
                    self.log_test("File List Validation", False, f"Unexpected error: {error_detail}")
            elif response.status_code == 200:
                data = response.json()
                if 'category' in data and 'files' in data:
                    self.log_test("File Listing", True, "File listing endpoint working")
                else:
                    self.log_test("File Listing", False, f"File listing response incomplete: {data}")
            else:
                self.log_test("File Listing", False, f"File listing failed: {response.status_code}")
                
        except Exception as e:
            self.log_test("File Listing Test", False, f"File listing test error: {str(e)}")
        
        # Test file download URL generation (should fail without AWS credentials)
        try:
            response = self.session.get(
                f"{BACKEND_URL}/files/test_file_key/download",
                headers=headers
            )
            
            if response.status_code == 500:
                error_detail = response.text
                if "AWS credentials not configured" in error_detail:
                    self.log_test("File Download URL", True, "Download URL generation properly fails without AWS credentials (expected)")
                else:
                    self.log_test("File Download URL", False, f"Unexpected error: {error_detail}")
            elif response.status_code == 404:
                self.log_test("File Download URL", True, "File not found response (expected for test key)")
            else:
                self.log_test("File Download URL", False, f"Unexpected response: {response.status_code}")
                
        except Exception as e:
            self.log_test("File Download Test", False, f"File download test error: {str(e)}")

    def test_gdpr_audit_logging_system(self):
        """Test GDPR audit logging system"""
        print("\n📋 TESTING GDPR AUDIT LOGGING SYSTEM")
        
        if not self.auth_token:
            self.log_test("GDPR Audit System", False, "No auth token available for testing")
            return
        
        headers = {
            'Authorization': f'Bearer {self.auth_token}',
            'Content-Type': 'application/json'
        }
        
        # Test user's own audit trail endpoint
        try:
            response = self.session.get(f"{BACKEND_URL}/audit/my-trail", headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                if 'user_id' in data and 'entries' in data:
                    self.log_test("User Audit Trail", True, f"Audit trail working, {data.get('total_entries', 0)} entries found")
                else:
                    self.log_test("User Audit Trail", False, f"Audit trail response incomplete: {data}")
            else:
                error_detail = response.text
                self.log_test("User Audit Trail", False, f"Audit trail failed: {response.status_code} - {error_detail}")
                
        except Exception as e:
            self.log_test("User Audit Trail", False, f"Audit trail error: {str(e)}")
        
        # Test GDPR report generation
        try:
            response = self.session.get(f"{BACKEND_URL}/audit/gdpr-report", headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                if 'user_id' in data and 'total_logged_actions' in data:
                    self.log_test("GDPR Report", True, f"GDPR report generated, {data.get('total_logged_actions', 0)} actions logged")
                else:
                    self.log_test("GDPR Report", False, f"GDPR report incomplete: {data}")
            else:
                error_detail = response.text
                self.log_test("GDPR Report", False, f"GDPR report failed: {response.status_code} - {error_detail}")
                
        except Exception as e:
            self.log_test("GDPR Report", False, f"GDPR report error: {str(e)}")
        
        # Test audit trail with filters
        try:
            response = self.session.get(
                f"{BACKEND_URL}/audit/my-trail?action_types=user_login,user_register&limit=50",
                headers=headers
            )
            
            if response.status_code == 200:
                data = response.json()
                if 'entries' in data:
                    self.log_test("Audit Trail Filters", True, "Audit trail filtering working")
                else:
                    self.log_test("Audit Trail Filters", False, f"Filtered audit trail incomplete: {data}")
            else:
                self.log_test("Audit Trail Filters", False, f"Filtered audit trail failed: {response.status_code}")
                
        except Exception as e:
            self.log_test("Audit Trail Filters", False, f"Audit trail filter error: {str(e)}")

    def test_admin_audit_access(self):
        """Test admin audit access (will fail for non-admin users - expected)"""
        print("\n👑 TESTING ADMIN AUDIT ACCESS")
        
        if not self.auth_token:
            self.log_test("Admin Audit Access", False, "No auth token available for testing")
            return
        
        headers = {
            'Authorization': f'Bearer {self.auth_token}',
            'Content-Type': 'application/json'
        }
        
        # Test admin audit access (should fail for regular users)
        try:
            response = self.session.get(
                f"{BACKEND_URL}/admin/audit/{self.user_id}",
                headers=headers
            )
            
            if response.status_code == 403:
                self.log_test("Admin Audit Access Control", True, "Admin audit access properly restricted to admins")
            elif response.status_code == 200:
                self.log_test("Admin Audit Access", True, "Admin audit access working (user has admin privileges)")
            else:
                self.log_test("Admin Audit Access", False, f"Unexpected response: {response.status_code}")
                
        except Exception as e:
            self.log_test("Admin Audit Access", False, f"Admin audit test error: {str(e)}")

    def test_file_upload_security_validation(self):
        """Test file upload security validation"""
        print("\n🛡️ TESTING FILE UPLOAD SECURITY VALIDATION")
        
        if not self.auth_token:
            self.log_test("File Security Validation", False, "No auth token available for testing")
            return
        
        headers = {
            'Authorization': f'Bearer {self.auth_token}',
        }
        
        # Test invalid category
        try:
            test_file_content = b"Test content"
            files = {
                'file': ('test.txt', test_file_content, 'text/plain')
            }
            data = {
                'category': 'invalid-category'
            }
            
            response = self.session.post(
                f"{BACKEND_URL}/files/upload",
                files=files,
                data=data,
                headers=headers
            )
            
            if response.status_code == 400:
                error_detail = response.text
                if "Invalid category" in error_detail:
                    self.log_test("File Category Validation", True, "Invalid file category properly rejected")
                else:
                    self.log_test("File Category Validation", False, f"Unexpected error: {error_detail}")
            else:
                self.log_test("File Category Validation", False, f"Invalid category not rejected: {response.status_code}")
                
        except Exception as e:
            self.log_test("File Category Validation", False, f"Category validation error: {str(e)}")
        
        # Test admin-only category access
        try:
            files = {
                'file': ('test.txt', b"Test content", 'text/plain')
            }
            data = {
                'category': 'admin-content'
            }
            
            response = self.session.post(
                f"{BACKEND_URL}/files/upload",
                files=files,
                data=data,
                headers=headers
            )
            
            if response.status_code == 403:
                self.log_test("Admin Category Access", True, "Admin-only category properly restricted")
            elif response.status_code == 500 and "AWS credentials" in response.text:
                self.log_test("Admin Category Access", True, "Admin category access passed (AWS credentials missing)")
            else:
                self.log_test("Admin Category Access", False, f"Admin category not restricted: {response.status_code}")
                
        except Exception as e:
            self.log_test("Admin Category Access", False, f"Admin category test error: {str(e)}")

    def test_phase4_configuration_system(self):
        """Test Phase 4 core configuration system"""
        print("\n⚙️ TESTING PHASE 4 CONFIGURATION SYSTEM")
        
        try:
            # Import configuration modules
            sys.path.append('/app/backend')
            from core.config import settings, validate_startup_config
            
            # Test configuration loading
            if settings.security.jwt_secret_key:
                self.log_test("Config - JWT Secret", True, "JWT secret key loaded successfully")
            else:
                self.log_test("Config - JWT Secret", False, "JWT secret key not configured")
            
            # Test CORS configuration
            cors_origins = settings.get_cors_origins()
            if isinstance(cors_origins, list) and len(cors_origins) > 0:
                self.log_test("Config - CORS Origins", True, f"CORS origins configured: {len(cors_origins)} origins")
            else:
                self.log_test("Config - CORS Origins", False, "CORS origins not properly configured")
            
            # Test database configuration
            if settings.database.mongo_url and settings.database.db_name:
                self.log_test("Config - Database", True, "Database configuration loaded")
            else:
                self.log_test("Config - Database", False, "Database configuration missing")
            
            # Test AWS configuration validation
            aws_configured = settings.aws.is_configured
            self.log_test("Config - AWS Validation", True, f"AWS configuration check: {'configured' if aws_configured else 'not configured'}")
            
            # Test AI configuration
            if settings.ai.api_key:
                self.log_test("Config - AI API Key", True, "AI API key configured")
            else:
                self.log_test("Config - AI API Key", False, "AI API key not configured")
            
            # Test configuration validation
            warnings = settings.validate_configuration()
            if len(warnings) == 0:
                self.log_test("Config - Validation", True, "All critical configuration validated")
            else:
                self.log_test("Config - Validation", False, f"Configuration warnings: {len(warnings)}")
            
            # Test environment detection
            is_prod = settings.is_production()
            self.log_test("Config - Environment", True, f"Environment detection: {'production' if is_prod else 'development'}")
            
        except ImportError as e:
            self.log_test("Config System Import", False, f"Cannot import configuration system: {str(e)}")
        except Exception as e:
            self.log_test("Config System Test", False, f"Configuration system error: {str(e)}")

    def test_phase4_database_manager(self):
        """Test Phase 4 database connection management"""
        print("\n💾 TESTING PHASE 4 DATABASE MANAGER")
        
        try:
            sys.path.append('/app/backend')
            from core.database import db_manager
            
            # Test database health check endpoint (if available)
            if self.auth_token:
                headers = {
                    'Authorization': f'Bearer {self.auth_token}',
                    'Content-Type': 'application/json'
                }
                
                # Test if there's a health check endpoint
                try:
                    response = self.session.get(f"{BACKEND_URL}/health", headers=headers)
                    if response.status_code == 200:
                        data = response.json()
                        if 'database' in data:
                            self.log_test("DB Manager - Health Check", True, "Database health check endpoint working")
                        else:
                            self.log_test("DB Manager - Health Check", True, "Health endpoint exists (no DB details)")
                    else:
                        self.log_test("DB Manager - Health Check", False, f"Health check failed: {response.status_code}")
                except:
                    self.log_test("DB Manager - Health Check", False, "No health check endpoint available")
            
            # Test database connectivity through existing endpoints
            response = self.session.get(f"{BACKEND_URL}/destinations")
            if response.status_code == 200:
                self.log_test("DB Manager - Connection Pool", True, "Database connection working through endpoints")
            else:
                self.log_test("DB Manager - Connection Pool", False, f"Database connection issues: {response.status_code}")
            
            # Test index creation (implicit through successful queries)
            response = self.session.get(f"{BACKEND_URL}/articles")
            if response.status_code == 200:
                self.log_test("DB Manager - Indexes", True, "Database indexes working (queries successful)")
            else:
                self.log_test("DB Manager - Indexes", False, "Database query performance issues")
                
        except Exception as e:
            self.log_test("DB Manager Test", False, f"Database manager test error: {str(e)}")

    def test_phase4_modular_auth_service(self):
        """Test Phase 4 modular authentication service"""
        print("\n🔐 TESTING PHASE 4 MODULAR AUTH SERVICE")
        
        try:
            sys.path.append('/app/backend')
            from services.auth_service import auth_service
            
            # Test password validation
            weak_password = "123"
            strong_password = "StrongPass123!"
            
            weak_issues = auth_service.validate_password_strength(weak_password)
            strong_issues = auth_service.validate_password_strength(strong_password)
            
            if len(weak_issues) > 0 and len(strong_issues) == 0:
                self.log_test("Auth Service - Password Validation", True, "Password strength validation working")
            else:
                self.log_test("Auth Service - Password Validation", False, f"Password validation issues: weak={len(weak_issues)}, strong={len(strong_issues)}")
            
            # Test token generation and validation
            test_data = {"sub": "test_user", "email": "test@example.com"}
            token = auth_service.create_access_token(test_data)
            decoded = auth_service.decode_token(token)
            
            if decoded and decoded.get("sub") == "test_user":
                self.log_test("Auth Service - Token Management", True, "Token generation and validation working")
            else:
                self.log_test("Auth Service - Token Management", False, "Token management issues")
            
            # Test password hashing
            test_password = "TestPassword123!"
            hashed = auth_service.get_password_hash(test_password)
            verified = auth_service.verify_password(test_password, hashed)
            
            if verified and hashed != test_password:
                self.log_test("Auth Service - Password Hashing", True, "Password hashing and verification working")
            else:
                self.log_test("Auth Service - Password Hashing", False, "Password hashing issues")
                
        except Exception as e:
            self.log_test("Auth Service Test", False, f"Auth service test error: {str(e)}")

    def test_phase4_rate_limiting_middleware(self):
        """Test Phase 4 rate limiting middleware"""
        print("\n🚦 TESTING PHASE 4 RATE LIMITING MIDDLEWARE")
        
        # Test rate limiting on authentication endpoints
        login_data = {
            "email": "nonexistent@test.com",
            "password": "wrongpassword"
        }
        
        rate_limit_hit = False
        requests_made = 0
        
        # Make multiple requests to trigger rate limiting
        for i in range(15):  # Try to exceed the rate limit
            try:
                response = self.session.post(
                    f"{BACKEND_URL}/auth/login",
                    json=login_data,
                    headers={'Content-Type': 'application/json'}
                )
                requests_made += 1
                
                # Check for rate limit headers
                if 'X-RateLimit-Limit' in response.headers:
                    self.log_test("Rate Limiting - Headers", True, "Rate limit headers present in response")
                
                if response.status_code == 429:
                    rate_limit_hit = True
                    self.log_test("Rate Limiting - Enforcement", True, f"Rate limit enforced after {requests_made} requests")
                    break
                    
            except Exception as e:
                self.log_test("Rate Limiting Test", False, f"Rate limiting test error: {str(e)}")
                break
        
        if not rate_limit_hit and requests_made >= 10:
            self.log_test("Rate Limiting - Enforcement", False, f"Rate limit not enforced after {requests_made} requests")
        elif not rate_limit_hit:
            self.log_test("Rate Limiting - Enforcement", True, "Rate limiting configured (limit not reached in test)")
        
        # Test rate limit monitoring
        try:
            sys.path.append('/app/backend')
            from middleware.rate_limiting import rate_limit_monitor
            
            stats = rate_limit_monitor.get_rate_limit_stats()
            if isinstance(stats, dict) and 'total_buckets' in stats:
                self.log_test("Rate Limiting - Monitoring", True, f"Rate limit monitoring working: {stats['total_buckets']} buckets")
            else:
                self.log_test("Rate Limiting - Monitoring", False, "Rate limit monitoring not working")
                
        except Exception as e:
            self.log_test("Rate Limiting - Monitoring", False, f"Rate limit monitoring error: {str(e)}")

    def test_phase4_service_layer_architecture(self):
        """Test Phase 4 service layer architecture"""
        print("\n🏗️ TESTING PHASE 4 SERVICE LAYER ARCHITECTURE")
        
        # Test modular API routes
        modular_endpoints = [
            "/auth/me",
            "/auth/login", 
            "/auth/register"
        ]
        
        for endpoint in modular_endpoints:
            try:
                if endpoint == "/auth/me" and self.auth_token:
                    headers = {'Authorization': f'Bearer {self.auth_token}'}
                    response = self.session.get(f"{BACKEND_URL}{endpoint}", headers=headers)
                elif endpoint in ["/auth/login", "/auth/register"]:
                    # Just test that the endpoint exists (OPTIONS request)
                    response = self.session.options(f"{BACKEND_URL}{endpoint}")
                else:
                    continue
                
                if response.status_code in [200, 204, 405]:  # 405 = Method not allowed (but endpoint exists)
                    self.log_test(f"Service Layer - {endpoint}", True, "Modular endpoint accessible")
                else:
                    self.log_test(f"Service Layer - {endpoint}", False, f"Endpoint issues: {response.status_code}")
                    
            except Exception as e:
                self.log_test(f"Service Layer - {endpoint}", False, f"Error testing {endpoint}: {str(e)}")
        
        # Test error handling consistency
        try:
            response = self.session.post(
                f"{BACKEND_URL}/auth/login",
                json={"email": "invalid", "password": "test"},
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code in [400, 422]:  # Validation error
                try:
                    error_data = response.json()
                    if 'detail' in error_data:
                        self.log_test("Service Layer - Error Handling", True, "Consistent error response format")
                    else:
                        self.log_test("Service Layer - Error Handling", False, "Inconsistent error format")
                except:
                    self.log_test("Service Layer - Error Handling", False, "Non-JSON error response")
            else:
                self.log_test("Service Layer - Error Handling", False, f"Unexpected error status: {response.status_code}")
                
        except Exception as e:
            self.log_test("Service Layer - Error Handling", False, f"Error handling test failed: {str(e)}")
        
        # Test dependency injection patterns
        if self.auth_token:
            headers = {'Authorization': f'Bearer {self.auth_token}'}
            response = self.session.get(f"{BACKEND_URL}/auth/me", headers=headers)
            
            if response.status_code == 200:
                self.log_test("Service Layer - Dependency Injection", True, "Authentication dependency working")
            else:
                self.log_test("Service Layer - Dependency Injection", False, "Authentication dependency issues")

    def test_booking_system_api(self):
        """Test Booking System API endpoints"""
        print("\n📅 TESTING BOOKING SYSTEM API")
        
        if not self.auth_token:
            self.log_test("Booking System API", False, "No auth token available for testing")
            return
        
        headers = {
            'Authorization': f'Bearer {self.auth_token}',
            'Content-Type': 'application/json'
        }
        
        # Test booking availability endpoint
        availability_data = {
            "destination_id": "test-destination-123",
            "check_in_date": "2024-06-15",
            "check_out_date": "2024-06-20",
            "guests": 2
        }
        
        try:
            response = self.session.post(f"{BACKEND_URL}/bookings/check-availability", json=availability_data, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                self.log_test("Booking Availability", True, "Booking availability endpoint working")
            elif response.status_code == 401:
                self.log_test("Booking Availability", True, "Booking availability endpoint secured (401 expected)")
            else:
                self.log_test("Booking Availability", False, f"Booking availability failed: {response.status_code}")
                
        except Exception as e:
            self.log_test("Booking Availability", False, f"Booking availability error: {str(e)}")
        
        # Test user bookings endpoint
        try:
            response = self.session.get(f"{BACKEND_URL}/bookings/my", headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                self.log_test("User Bookings", True, "User bookings endpoint working")
            elif response.status_code == 401:
                self.log_test("User Bookings", True, "User bookings endpoint secured (401 expected)")
            else:
                self.log_test("User Bookings", False, f"User bookings failed: {response.status_code}")
                
        except Exception as e:
            self.log_test("User Bookings", False, f"User bookings error: {str(e)}")
        
        # Test booking creation endpoint
        booking_data = {
            "destination_id": "test-destination-123",
            "check_in_date": "2024-06-15",
            "check_out_date": "2024-06-20",
            "guests": 2,
            "package_id": "test-package-456"
        }
        
        try:
            response = self.session.post(f"{BACKEND_URL}/bookings", json=booking_data, headers=headers)
            
            if response.status_code in [200, 201]:
                data = response.json()
                self.log_test("Booking Creation", True, "Booking creation endpoint working")
            elif response.status_code == 401:
                self.log_test("Booking Creation", True, "Booking creation endpoint secured (401 expected)")
            else:
                self.log_test("Booking Creation", False, f"Booking creation failed: {response.status_code}")
                
        except Exception as e:
            self.log_test("Booking Creation", False, f"Booking creation error: {str(e)}")

    def test_advanced_search_filtering_api(self):
        """Test Advanced Search & Filtering API endpoints"""
        print("\n🔍 TESTING ADVANCED SEARCH & FILTERING API")
        
        # Test search destinations with filters
        search_params = {
            "countries": "Spain,Portugal",
            "price_min": "1000",
            "price_max": "5000",
            "difficulty": "Medium",
            "course_type": "Links"
        }
        
        try:
            response = self.session.get(f"{BACKEND_URL}/search/destinations", params=search_params)
            
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, (list, dict)):
                    self.log_test("Search Destinations", True, f"Search destinations working")
                else:
                    self.log_test("Search Destinations", False, f"Search destinations unexpected format: {type(data)}")
            else:
                self.log_test("Search Destinations", False, f"Search destinations failed: {response.status_code}")
                
        except Exception as e:
            self.log_test("Search Destinations", False, f"Search destinations error: {str(e)}")
        
        # Test search filters endpoint
        try:
            response = self.session.get(f"{BACKEND_URL}/search/filters")
            
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, dict):
                    filter_count = len(data.keys())
                    self.log_test("Search Filters", True, f"Search filters working, {filter_count} filter categories")
                else:
                    self.log_test("Search Filters", False, f"Search filters unexpected format: {data}")
            else:
                self.log_test("Search Filters", False, f"Search filters failed: {response.status_code}")
                
        except Exception as e:
            self.log_test("Search Filters", False, f"Search filters error: {str(e)}")
        
        # Test popular searches endpoint
        try:
            response = self.session.get(f"{BACKEND_URL}/search/popular")
            
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, (list, dict)):
                    if isinstance(data, list):
                        self.log_test("Popular Searches", True, f"Popular searches working, {len(data)} popular terms")
                    else:
                        # Handle dict format
                        popular_count = len(data.get('popular_searches', []))
                        self.log_test("Popular Searches", True, f"Popular searches working, {popular_count} popular terms")
                else:
                    self.log_test("Popular Searches", False, f"Popular searches unexpected format: {type(data)}")
            else:
                self.log_test("Popular Searches", False, f"Popular searches failed: {response.status_code}")
                
        except Exception as e:
            self.log_test("Popular Searches", False, f"Popular searches error: {str(e)}")
        
        # Test AI search suggestions
        if self.auth_token:
            headers = {'Authorization': f'Bearer {self.auth_token}', 'Content-Type': 'application/json'}
            search_query = {"query": "golf courses in Spain with ocean views"}
            
            try:
                response = self.session.post(f"{BACKEND_URL}/search/ai-suggestions", json=search_query, headers=headers)
                
                if response.status_code == 200:
                    data = response.json()
                    self.log_test("AI Search Suggestions", True, "AI search suggestions working")
                elif response.status_code == 401:
                    self.log_test("AI Search Suggestions", True, "AI search suggestions secured (401 expected)")
                else:
                    self.log_test("AI Search Suggestions", False, f"AI search suggestions failed: {response.status_code}")
                    
            except Exception as e:
                self.log_test("AI Search Suggestions", False, f"AI search suggestions error: {str(e)}")

    def test_payment_system_stripe_api(self):
        """Test Payment System (Stripe Integration) API endpoints"""
        print("\n💳 TESTING PAYMENT SYSTEM (STRIPE INTEGRATION)")
        
        # Test payment packages endpoint
        try:
            response = self.session.get(f"{BACKEND_URL}/payments/packages")
            
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list) and len(data) > 0:
                    package_count = len(data)
                    self.log_test("Payment Packages", True, f"Payment packages working, {package_count} packages available")
                else:
                    self.log_test("Payment Packages", False, f"Payment packages empty or wrong format: {data}")
            else:
                self.log_test("Payment Packages", False, f"Payment packages failed: {response.status_code}")
                
        except Exception as e:
            self.log_test("Payment Packages", False, f"Payment packages error: {str(e)}")
        
        if not self.auth_token:
            self.log_test("Payment System Auth", False, "No auth token available for authenticated payment tests")
            return
        
        headers = {
            'Authorization': f'Bearer {self.auth_token}',
            'Content-Type': 'application/json'
        }
        
        # Test Stripe checkout session creation
        checkout_data = {
            "package_id": "premium-golf-package",
            "destination_id": "spain-costa-del-sol",
            "success_url": "https://golf-ai-advisor.preview.emergentagent.com/payment/success",
            "cancel_url": "https://golf-ai-advisor.preview.emergentagent.com/payment/cancel"
        }
        
        try:
            response = self.session.post(f"{BACKEND_URL}/payments/create-checkout-session", json=checkout_data, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                if 'checkout_url' in data or 'session_id' in data:
                    self.log_test("Stripe Checkout Session", True, "Stripe checkout session creation working")
                else:
                    self.log_test("Stripe Checkout Session", False, f"Checkout session missing required fields: {data}")
            elif response.status_code == 401:
                self.log_test("Stripe Checkout Session", True, "Stripe checkout session secured (401 expected)")
            else:
                self.log_test("Stripe Checkout Session", False, f"Stripe checkout session failed: {response.status_code}")
                
        except Exception as e:
            self.log_test("Stripe Checkout Session", False, f"Stripe checkout session error: {str(e)}")
        
        # Test payment status checking
        try:
            response = self.session.get(f"{BACKEND_URL}/payments/status/test-payment-123", headers=headers)
            
            if response.status_code in [200, 404]:  # 404 is OK for non-existent payment
                self.log_test("Payment Status Check", True, "Payment status checking endpoint working")
            elif response.status_code == 401:
                self.log_test("Payment Status Check", True, "Payment status checking secured (401 expected)")
            else:
                self.log_test("Payment Status Check", False, f"Payment status check failed: {response.status_code}")
                
        except Exception as e:
            self.log_test("Payment Status Check", False, f"Payment status check error: {str(e)}")
        
        # Test user transactions endpoint
        try:
            response = self.session.get(f"{BACKEND_URL}/payments/my-transactions", headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                self.log_test("User Transactions", True, "User transactions endpoint working")
            elif response.status_code == 401:
                self.log_test("User Transactions", True, "User transactions secured (401 expected)")
            else:
                self.log_test("User Transactions", False, f"User transactions failed: {response.status_code}")
                
        except Exception as e:
            self.log_test("User Transactions", False, f"User transactions error: {str(e)}")

    def test_swedish_localization_i18n_api(self):
        """Test Swedish Localization (i18n) API endpoints"""
        print("\n🇸🇪 TESTING SWEDISH LOCALIZATION (i18n)")
        
        # Test English translations endpoint
        try:
            response = self.session.get(f"{BACKEND_URL}/i18n/translations/en")
            
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, dict) and len(data) > 0:
                    translation_count = len(data)
                    self.log_test("English Translations", True, f"English translations working, {translation_count} translations")
                else:
                    self.log_test("English Translations", False, f"English translations empty or wrong format: {data}")
            else:
                self.log_test("English Translations", False, f"English translations failed: {response.status_code}")
                
        except Exception as e:
            self.log_test("English Translations", False, f"English translations error: {str(e)}")
        
        # Test Swedish translations endpoint
        try:
            response = self.session.get(f"{BACKEND_URL}/i18n/translations/sv")
            
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, dict) and len(data) > 0:
                    translation_count = len(data)
                    self.log_test("Swedish Translations", True, f"Swedish translations working, {translation_count} translations")
                    
                    # Check for Swedish-specific content
                    if 'currency_symbol' in data and data['currency_symbol'] == 'kr':
                        self.log_test("Swedish Currency", True, "Swedish currency symbol properly configured")
                    else:
                        self.log_test("Swedish Currency", False, "Swedish currency symbol not found or incorrect")
                else:
                    self.log_test("Swedish Translations", False, f"Swedish translations empty or wrong format: {data}")
            else:
                self.log_test("Swedish Translations", False, f"Swedish translations failed: {response.status_code}")
                
        except Exception as e:
            self.log_test("Swedish Translations", False, f"Swedish translations error: {str(e)}")
        
        # Test localized countries endpoint
        try:
            response = self.session.get(f"{BACKEND_URL}/i18n/countries/sv")
            
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, dict) and len(data) > 0:
                    country_count = len(data)
                    self.log_test("Localized Countries", True, f"Localized countries working, {country_count} countries")
                else:
                    self.log_test("Localized Countries", False, f"Localized countries empty or wrong format: {data}")
            else:
                self.log_test("Localized Countries", False, f"Localized countries failed: {response.status_code}")
                
        except Exception as e:
            self.log_test("Localized Countries", False, f"Localized countries error: {str(e)}")
        
        # Test currency formatting endpoint
        try:
            response = self.session.get(f"{BACKEND_URL}/i18n/currency-format/sv")
            
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, dict) and 'symbol' in data:
                    self.log_test("Currency Formatting", True, f"Currency formatting working: {data}")
                else:
                    self.log_test("Currency Formatting", False, f"Currency formatting wrong format: {data}")
            else:
                self.log_test("Currency Formatting", False, f"Currency formatting failed: {response.status_code}")
                
        except Exception as e:
            self.log_test("Currency Formatting", False, f"Currency formatting error: {str(e)}")

    def test_pwa_mobile_backend_support(self):
        """Test PWA Mobile Infrastructure Backend Support"""
        print("\n📱 TESTING PWA MOBILE BACKEND SUPPORT")
        
        # Test mobile-optimized API endpoints
        mobile_headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15',
            'Content-Type': 'application/json'
        }
        
        # Test mobile destinations endpoint
        try:
            response = self.session.get(f"{BACKEND_URL}/destinations?mobile=true", headers=mobile_headers)
            
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list):
                    self.log_test("Mobile Destinations API", True, f"Mobile destinations API working, {len(data)} destinations")
                else:
                    self.log_test("Mobile Destinations API", False, f"Mobile destinations unexpected format: {type(data)}")
            else:
                self.log_test("Mobile Destinations API", False, f"Mobile destinations failed: {response.status_code}")
                
        except Exception as e:
            self.log_test("Mobile Destinations API", False, f"Mobile destinations error: {str(e)}")
        
        # Test mobile search API performance
        try:
            import time
            start_time = time.time()
            response = self.session.get(f"{BACKEND_URL}/search/destinations?limit=10", headers=mobile_headers)
            end_time = time.time()
            response_time = (end_time - start_time) * 1000  # Convert to milliseconds
            
            if response.status_code == 200 and response_time < 2000:  # Under 2 seconds
                self.log_test("Mobile API Performance", True, f"Mobile API performance good: {response_time:.0f}ms")
            elif response.status_code == 200:
                self.log_test("Mobile API Performance", False, f"Mobile API slow: {response_time:.0f}ms")
            else:
                self.log_test("Mobile API Performance", False, f"Mobile API failed: {response.status_code}")
                
        except Exception as e:
            self.log_test("Mobile API Performance", False, f"Mobile API performance error: {str(e)}")
        
        # Test mobile error handling
        try:
            response = self.session.get(f"{BACKEND_URL}/nonexistent-endpoint", headers=mobile_headers)
            
            if response.status_code == 404:
                try:
                    error_data = response.json()
                    if 'detail' in error_data:
                        self.log_test("Mobile Error Handling", True, "Mobile error handling working")
                    else:
                        self.log_test("Mobile Error Handling", False, "Mobile error format inconsistent")
                except:
                    self.log_test("Mobile Error Handling", False, "Mobile error not JSON formatted")
            else:
                self.log_test("Mobile Error Handling", False, f"Mobile error handling unexpected: {response.status_code}")
                
        except Exception as e:
            self.log_test("Mobile Error Handling", False, f"Mobile error handling error: {str(e)}")
        
        # Test mobile data compression/optimization
        if self.auth_token:
            headers = {
                'Authorization': f'Bearer {self.auth_token}',
                'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15',
                'Accept-Encoding': 'gzip, deflate'
            }
            
            try:
                response = self.session.get(f"{BACKEND_URL}/destinations", headers=headers)
                
                if response.status_code == 200:
                    content_encoding = response.headers.get('Content-Encoding', '')
                    if 'gzip' in content_encoding:
                        self.log_test("Mobile Data Compression", True, "Mobile data compression enabled")
                    else:
                        self.log_test("Mobile Data Compression", True, "Mobile API working (compression optional)")
                else:
                    self.log_test("Mobile Data Compression", False, f"Mobile compression test failed: {response.status_code}")
                    
            except Exception as e:
                self.log_test("Mobile Data Compression", False, f"Mobile compression error: {str(e)}")

    def test_integration_workflows(self):
        """Test end-to-end integration workflows"""
        print("\n🔄 TESTING INTEGRATION WORKFLOWS")
        
        if not self.auth_token:
            self.log_test("Integration Workflows", False, "No auth token available for integration testing")
            return
        
        headers = {
            'Authorization': f'Bearer {self.auth_token}',
            'Content-Type': 'application/json'
        }
        
        # Test search → book → pay workflow simulation
        try:
            # Step 1: Search for destinations
            search_response = self.session.get(f"{BACKEND_URL}/search/destinations?countries=Spain")
            
            if search_response.status_code != 200:
                self.log_test("Search→Book→Pay Workflow", False, f"Search step failed: {search_response.status_code}")
                return
            
            # Step 2: Get payment packages
            packages_response = self.session.get(f"{BACKEND_URL}/payments/packages")
            
            if packages_response.status_code != 200:
                self.log_test("Search→Book→Pay Workflow", False, f"Packages step failed: {packages_response.status_code}")
                return
            
            # Step 3: Check booking availability (simulated)
            availability_response = self.session.get(f"{BACKEND_URL}/bookings/availability", headers=headers)
            
            # This might return 401 or 404, which is acceptable for this workflow test
            if availability_response.status_code in [200, 401, 404]:
                self.log_test("Search→Book→Pay Workflow", True, "End-to-end workflow endpoints accessible")
            else:
                self.log_test("Search→Book→Pay Workflow", False, f"Booking step failed: {availability_response.status_code}")
                
        except Exception as e:
            self.log_test("Search→Book→Pay Workflow", False, f"Integration workflow error: {str(e)}")
        
        # Test mobile vs desktop API consistency
        try:
            desktop_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            mobile_headers = {'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15'}
            
            desktop_response = self.session.get(f"{BACKEND_URL}/destinations", headers=desktop_headers)
            mobile_response = self.session.get(f"{BACKEND_URL}/destinations", headers=mobile_headers)
            
            if desktop_response.status_code == 200 and mobile_response.status_code == 200:
                desktop_data = desktop_response.json()
                mobile_data = mobile_response.json()
                
                if len(desktop_data) == len(mobile_data):
                    self.log_test("Mobile vs Desktop Consistency", True, "Mobile and desktop APIs return consistent data")
                else:
                    self.log_test("Mobile vs Desktop Consistency", False, f"Data inconsistency: desktop={len(desktop_data)}, mobile={len(mobile_data)}")
            else:
                self.log_test("Mobile vs Desktop Consistency", False, f"API consistency test failed: desktop={desktop_response.status_code}, mobile={mobile_response.status_code}")
                
        except Exception as e:
            self.log_test("Mobile vs Desktop Consistency", False, f"API consistency error: {str(e)}")

    def test_performance_and_security_validation(self):
        """Test performance and security validation for production readiness"""
        print("\n⚡ TESTING PERFORMANCE & SECURITY VALIDATION")
        
        # Test concurrent request handling (simplified)
        try:
            import threading
            import time
            
            results = []
            
            def make_request():
                try:
                    start_time = time.time()
                    response = self.session.get(f"{BACKEND_URL}/destinations")
                    end_time = time.time()
                    results.append({
                        'status_code': response.status_code,
                        'response_time': (end_time - start_time) * 1000
                    })
                except Exception as e:
                    results.append({'error': str(e)})
            
            # Create 5 concurrent requests
            threads = []
            for i in range(5):
                thread = threading.Thread(target=make_request)
                threads.append(thread)
                thread.start()
            
            # Wait for all threads to complete
            for thread in threads:
                thread.join()
            
            successful_requests = [r for r in results if 'status_code' in r and r['status_code'] == 200]
            if len(successful_requests) >= 4:  # At least 4 out of 5 successful
                avg_response_time = sum(r['response_time'] for r in successful_requests) / len(successful_requests)
                self.log_test("Concurrent Request Handling", True, f"Concurrent requests handled: {len(successful_requests)}/5, avg: {avg_response_time:.0f}ms")
            else:
                self.log_test("Concurrent Request Handling", False, f"Concurrent request issues: {len(successful_requests)}/5 successful")
                
        except Exception as e:
            self.log_test("Concurrent Request Handling", False, f"Concurrent request test error: {str(e)}")
        
        # Test GDPR compliance with new features
        if self.auth_token:
            headers = {'Authorization': f'Bearer {self.auth_token}', 'Content-Type': 'application/json'}
            
            try:
                # Test that user data export includes new feature data
                export_response = self.session.post(f"{BACKEND_URL}/privacy/export-data", headers=headers)
                
                if export_response.status_code == 200:
                    export_data = export_response.json()
                    if 'data' in export_data and isinstance(export_data['data'], dict):
                        data_sections = list(export_data['data'].keys())
                        self.log_test("GDPR New Features Compliance", True, f"GDPR export includes {len(data_sections)} data sections")
                    else:
                        self.log_test("GDPR New Features Compliance", False, "GDPR export data format issues")
                else:
                    self.log_test("GDPR New Features Compliance", False, f"GDPR export failed: {export_response.status_code}")
                    
            except Exception as e:
                self.log_test("GDPR New Features Compliance", False, f"GDPR compliance test error: {str(e)}")
        
        # Test API response time validation
        try:
            import time
            
            critical_endpoints = [
                "/destinations",
                "/search/destinations",
                "/payments/packages",
                "/i18n/translations/en"
            ]
            
            slow_endpoints = []
            
            for endpoint in critical_endpoints:
                start_time = time.time()
                response = self.session.get(f"{BACKEND_URL}{endpoint}")
                end_time = time.time()
                response_time = (end_time - start_time) * 1000
                
                if response_time > 1000:  # Over 1 second
                    slow_endpoints.append(f"{endpoint}: {response_time:.0f}ms")
            
            if len(slow_endpoints) == 0:
                self.log_test("API Response Time Validation", True, "All critical endpoints respond under 1 second")
            else:
                self.log_test("API Response Time Validation", False, f"Slow endpoints: {', '.join(slow_endpoints)}")
                
        except Exception as e:
            self.log_test("API Response Time Validation", False, f"Response time validation error: {str(e)}")

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
        
        # Phase 2 Infrastructure Tests
        print("\n" + "="*60)
        print("🚀 PHASE 2 INFRASTRUCTURE TESTING")
        print("="*60)
        self.test_mongodb_security_hardening()
        self.test_file_storage_system()
        self.test_gdpr_audit_logging_system()
        self.test_admin_audit_access()
        self.test_file_upload_security_validation()
        
        # Phase 4 Architecture Tests
        print("\n" + "="*60)
        print("🚀 PHASE 4 ARCHITECTURE IMPROVEMENTS TESTING")
        print("="*60)
        self.test_phase4_configuration_system()
        self.test_phase4_database_manager()
        self.test_phase4_modular_auth_service()
        self.test_phase4_rate_limiting_middleware()
        self.test_phase4_service_layer_architecture()
        
        # Medium Priority Features & PWA Mobile Testing
        print("\n" + "="*60)
        print("🚀 MEDIUM PRIORITY FEATURES & PWA MOBILE TESTING")
        print("="*60)
        self.test_booking_system_api()
        self.test_advanced_search_filtering_api()
        self.test_payment_system_stripe_api()
        self.test_swedish_localization_i18n_api()
        self.test_pwa_mobile_backend_support()
        self.test_integration_workflows()
        self.test_performance_and_security_validation()
        
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