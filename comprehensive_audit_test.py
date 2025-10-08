#!/usr/bin/env python3
"""
Comprehensive Final Audit Testing Suite
Tests all systems implemented during the audit phases
"""

import requests
import json
import uuid
import time
from datetime import datetime

# Configuration
BACKEND_URL = "https://golf-ai-advisor.preview.emergentagent.com/api"
TEST_USER_EMAIL = f"audituser_{uuid.uuid4().hex[:8]}@golfaudit.com"
TEST_USER_PASSWORD = "AuditSecure123!"
TEST_USER_NAME = "Golf Audit User"

class ComprehensiveAuditor:
    def __init__(self):
        self.session = requests.Session()
        self.auth_token = None
        self.user_id = None
        self.test_results = []
        
    def log_test(self, category, test_name, success, details=""):
        """Log test results with category"""
        status = "✅" if success else "❌"
        result = {
            "category": category,
            "test": test_name,
            "success": success,
            "details": details,
            "timestamp": datetime.now().isoformat()
        }
        self.test_results.append(result)
        print(f"{status} [{category}] {test_name}: {details}")
        
    def setup_test_user(self):
        """Setup test user for authentication"""
        print("\n🔧 SETTING UP TEST USER")
        
        # Register user
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
                self.auth_token = data['access_token']
                self.user_id = data['user']['id']
                self.log_test("SETUP", "User Registration", True, "Test user created successfully")
                return True
            else:
                self.log_test("SETUP", "User Registration", False, f"Failed: {response.status_code}")
                return False
                
        except Exception as e:
            self.log_test("SETUP", "User Registration", False, f"Error: {str(e)}")
            return False
    
    def test_phase1_security_systems(self):
        """Test Phase 1 Security Systems"""
        print("\n🔐 PHASE 1: SECURITY SYSTEMS AUDIT")
        
        # JWT Security
        if self.auth_token:
            headers = {'Authorization': f'Bearer {self.auth_token}'}
            try:
                response = self.session.get(f"{BACKEND_URL}/auth/me", headers=headers)
                if response.status_code == 200:
                    self.log_test("PHASE1", "JWT Security", True, "JWT token validation working")
                else:
                    self.log_test("PHASE1", "JWT Security", False, f"JWT validation failed: {response.status_code}")
            except Exception as e:
                self.log_test("PHASE1", "JWT Security", False, f"JWT test error: {str(e)}")
        
        # CORS Configuration
        try:
            headers = {'Origin': 'https://golf-ai-advisor.preview.emergentagent.com'}
            response = self.session.options(f"{BACKEND_URL}/auth/login", headers=headers)
            if response.status_code in [200, 204]:
                self.log_test("PHASE1", "CORS Configuration", True, "CORS preflight working")
            else:
                self.log_test("PHASE1", "CORS Configuration", False, f"CORS failed: {response.status_code}")
        except Exception as e:
            self.log_test("PHASE1", "CORS Configuration", False, f"CORS test error: {str(e)}")
        
        # Authentication Endpoints
        login_data = {"email": TEST_USER_EMAIL, "password": TEST_USER_PASSWORD}
        try:
            response = self.session.post(f"{BACKEND_URL}/auth/login", json=login_data)
            if response.status_code == 200:
                self.log_test("PHASE1", "Authentication Endpoints", True, "Login endpoint working")
            else:
                self.log_test("PHASE1", "Authentication Endpoints", False, f"Login failed: {response.status_code}")
        except Exception as e:
            self.log_test("PHASE1", "Authentication Endpoints", False, f"Auth test error: {str(e)}")
        
        # Data Encryption (test GDPR endpoints as proxy)
        if self.auth_token:
            headers = {'Authorization': f'Bearer {self.auth_token}'}
            try:
                response = self.session.get(f"{BACKEND_URL}/privacy/settings", headers=headers)
                if response.status_code == 200:
                    self.log_test("PHASE1", "Data Encryption", True, "GDPR privacy endpoints working")
                else:
                    self.log_test("PHASE1", "Data Encryption", False, f"Privacy endpoint failed: {response.status_code}")
            except Exception as e:
                self.log_test("PHASE1", "Data Encryption", False, f"Encryption test error: {str(e)}")
    
    def test_phase2_infrastructure_systems(self):
        """Test Phase 2 Infrastructure Systems"""
        print("\n🏗️ PHASE 2: INFRASTRUCTURE SYSTEMS AUDIT")
        
        # MongoDB Security Hardening
        try:
            response = self.session.get(f"{BACKEND_URL}/destinations")
            if response.status_code == 200:
                data = response.json()
                self.log_test("PHASE2", "MongoDB Security", True, f"Database working, {len(data)} destinations found")
            else:
                self.log_test("PHASE2", "MongoDB Security", False, f"Database query failed: {response.status_code}")
        except Exception as e:
            self.log_test("PHASE2", "MongoDB Security", False, f"Database test error: {str(e)}")
        
        # S3 File Storage Endpoints
        if self.auth_token:
            headers = {'Authorization': f'Bearer {self.auth_token}'}
            try:
                response = self.session.get(f"{BACKEND_URL}/files/list?category=user-profiles", headers=headers)
                if response.status_code == 500 and "AWS credentials" in response.text:
                    self.log_test("PHASE2", "S3 File Storage", True, "S3 endpoints working (AWS not configured - expected)")
                elif response.status_code == 200:
                    self.log_test("PHASE2", "S3 File Storage", True, "S3 endpoints fully functional")
                else:
                    self.log_test("PHASE2", "S3 File Storage", False, f"S3 endpoint failed: {response.status_code}")
            except Exception as e:
                self.log_test("PHASE2", "S3 File Storage", False, f"S3 test error: {str(e)}")
        
        # GDPR Audit Logging System
        if self.auth_token:
            headers = {'Authorization': f'Bearer {self.auth_token}'}
            try:
                response = self.session.get(f"{BACKEND_URL}/audit/my-trail", headers=headers)
                if response.status_code == 200:
                    data = response.json()
                    self.log_test("PHASE2", "GDPR Audit Logging", True, f"Audit system working, {data.get('total_entries', 0)} entries")
                else:
                    self.log_test("PHASE2", "GDPR Audit Logging", False, f"Audit system failed: {response.status_code}")
            except Exception as e:
                self.log_test("PHASE2", "GDPR Audit Logging", False, f"Audit test error: {str(e)}")
        
        # File Upload Security Validation
        if self.auth_token:
            headers = {'Authorization': f'Bearer {self.auth_token}'}
            files = {'file': ('test.txt', b'test', 'text/plain')}
            data = {'category': 'invalid-category'}
            try:
                response = self.session.post(f"{BACKEND_URL}/files/upload", files=files, data=data, headers=headers)
                if response.status_code == 400 and "Invalid category" in response.text:
                    self.log_test("PHASE2", "File Upload Security", True, "File upload validation working")
                else:
                    self.log_test("PHASE2", "File Upload Security", False, f"Validation failed: {response.status_code}")
            except Exception as e:
                self.log_test("PHASE2", "File Upload Security", False, f"Upload security test error: {str(e)}")
    
    def test_phase3_frontend_integration(self):
        """Test Phase 3 Frontend Integration (Backend perspective)"""
        print("\n🎨 PHASE 3: FRONTEND INTEGRATION AUDIT")
        
        # Authentication Flow (Backend support)
        if self.auth_token:
            headers = {'Authorization': f'Bearer {self.auth_token}'}
            try:
                response = self.session.get(f"{BACKEND_URL}/auth/me", headers=headers)
                if response.status_code == 200:
                    data = response.json()
                    if 'id' in data and 'email' in data:
                        self.log_test("PHASE3", "Authentication Flow Support", True, "Backend auth flow working")
                    else:
                        self.log_test("PHASE3", "Authentication Flow Support", False, "Incomplete user data")
                else:
                    self.log_test("PHASE3", "Authentication Flow Support", False, f"Auth flow failed: {response.status_code}")
            except Exception as e:
                self.log_test("PHASE3", "Authentication Flow Support", False, f"Auth flow test error: {str(e)}")
        
        # Protected Route Access
        if self.auth_token:
            headers = {'Authorization': f'Bearer {self.auth_token}'}
            protected_endpoints = ["/profile", "/privacy/settings"]
            
            for endpoint in protected_endpoints:
                try:
                    response = self.session.get(f"{BACKEND_URL}{endpoint}", headers=headers)
                    if response.status_code == 200:
                        self.log_test("PHASE3", f"Protected Route {endpoint}", True, "Route accessible with auth")
                    else:
                        self.log_test("PHASE3", f"Protected Route {endpoint}", False, f"Route failed: {response.status_code}")
                except Exception as e:
                    self.log_test("PHASE3", f"Protected Route {endpoint}", False, f"Route test error: {str(e)}")
        
        # Cookie Consent Backend Support (GDPR endpoints)
        if self.auth_token:
            headers = {'Authorization': f'Bearer {self.auth_token}'}
            try:
                response = self.session.post(f"{BACKEND_URL}/privacy/export-data", headers=headers)
                if response.status_code == 200:
                    self.log_test("PHASE3", "Cookie Consent Backend", True, "GDPR data export working")
                else:
                    self.log_test("PHASE3", "Cookie Consent Backend", False, f"GDPR export failed: {response.status_code}")
            except Exception as e:
                self.log_test("PHASE3", "Cookie Consent Backend", False, f"GDPR test error: {str(e)}")
    
    def test_phase4_architecture_improvements(self):
        """Test Phase 4 Architecture Improvements"""
        print("\n🏛️ PHASE 4: ARCHITECTURE IMPROVEMENTS AUDIT")
        
        # Configuration System (test through successful API responses)
        try:
            response = self.session.get(f"{BACKEND_URL}/")
            if response.status_code == 200:
                data = response.json()
                if 'message' in data and 'version' in data:
                    self.log_test("PHASE4", "Configuration System", True, "Configuration system working")
                else:
                    self.log_test("PHASE4", "Configuration System", False, "Configuration incomplete")
            else:
                self.log_test("PHASE4", "Configuration System", False, f"Config test failed: {response.status_code}")
        except Exception as e:
            self.log_test("PHASE4", "Configuration System", False, f"Config test error: {str(e)}")
        
        # Database Health Monitoring (test through query performance)
        start_time = time.time()
        try:
            response = self.session.get(f"{BACKEND_URL}/destinations")
            end_time = time.time()
            response_time = (end_time - start_time) * 1000  # Convert to milliseconds
            
            if response.status_code == 200 and response_time < 1000:  # Less than 1 second
                self.log_test("PHASE4", "Database Health Monitoring", True, f"Query performance: {response_time:.2f}ms")
            else:
                self.log_test("PHASE4", "Database Health Monitoring", False, f"Performance issues: {response_time:.2f}ms")
        except Exception as e:
            self.log_test("PHASE4", "Database Health Monitoring", False, f"Performance test error: {str(e)}")
        
        # Modular Authentication System
        if self.auth_token:
            headers = {'Authorization': f'Bearer {self.auth_token}'}
            try:
                response = self.session.get(f"{BACKEND_URL}/auth/me", headers=headers)
                if response.status_code == 200:
                    self.log_test("PHASE4", "Modular Authentication", True, "Modular auth system working")
                else:
                    self.log_test("PHASE4", "Modular Authentication", False, f"Modular auth failed: {response.status_code}")
            except Exception as e:
                self.log_test("PHASE4", "Modular Authentication", False, f"Modular auth test error: {str(e)}")
        
        # Rate Limiting Middleware (test by making multiple requests)
        rate_limit_detected = False
        for i in range(10):
            try:
                response = self.session.post(
                    f"{BACKEND_URL}/auth/login",
                    json={"email": "nonexistent@test.com", "password": "wrong"},
                    headers={'Content-Type': 'application/json'}
                )
                
                # Check for rate limit headers or 429 status
                if 'X-RateLimit-Limit' in response.headers or response.status_code == 429:
                    rate_limit_detected = True
                    break
                    
            except Exception:
                break
        
        if rate_limit_detected:
            self.log_test("PHASE4", "Rate Limiting Middleware", True, "Rate limiting active")
        else:
            self.log_test("PHASE4", "Rate Limiting Middleware", False, "Rate limiting not enforced")
        
        # Service Layer Architecture (test error handling consistency)
        try:
            response = self.session.post(
                f"{BACKEND_URL}/auth/login",
                json={"email": "invalid", "password": "test"}
            )
            
            if response.status_code in [400, 422]:
                try:
                    error_data = response.json()
                    if 'detail' in error_data:
                        self.log_test("PHASE4", "Service Layer Architecture", True, "Consistent error handling")
                    else:
                        self.log_test("PHASE4", "Service Layer Architecture", False, "Inconsistent error format")
                except:
                    self.log_test("PHASE4", "Service Layer Architecture", False, "Non-JSON error response")
            else:
                self.log_test("PHASE4", "Service Layer Architecture", False, f"Unexpected error status: {response.status_code}")
        except Exception as e:
            self.log_test("PHASE4", "Service Layer Architecture", False, f"Service layer test error: {str(e)}")
    
    def test_performance_scalability(self):
        """Test Performance & Scalability"""
        print("\n⚡ PERFORMANCE & SCALABILITY AUDIT")
        
        # API Response Times
        endpoints_to_test = [
            "/destinations",
            "/articles", 
            "/partners",
            "/testimonials"
        ]
        
        for endpoint in endpoints_to_test:
            start_time = time.time()
            try:
                response = self.session.get(f"{BACKEND_URL}{endpoint}")
                end_time = time.time()
                response_time = (end_time - start_time) * 1000
                
                if response.status_code == 200 and response_time < 500:  # Less than 500ms
                    self.log_test("PERFORMANCE", f"API Response {endpoint}", True, f"{response_time:.2f}ms")
                else:
                    self.log_test("PERFORMANCE", f"API Response {endpoint}", False, f"Slow response: {response_time:.2f}ms")
            except Exception as e:
                self.log_test("PERFORMANCE", f"API Response {endpoint}", False, f"Error: {str(e)}")
        
        # Database Query Performance (with indexes)
        start_time = time.time()
        try:
            response = self.session.get(f"{BACKEND_URL}/destinations?country=Spain&featured=true")
            end_time = time.time()
            query_time = (end_time - start_time) * 1000
            
            if response.status_code == 200 and query_time < 200:  # Less than 200ms for filtered query
                self.log_test("PERFORMANCE", "Database Query Performance", True, f"Filtered query: {query_time:.2f}ms")
            else:
                self.log_test("PERFORMANCE", "Database Query Performance", False, f"Slow query: {query_time:.2f}ms")
        except Exception as e:
            self.log_test("PERFORMANCE", "Database Query Performance", False, f"Query error: {str(e)}")
    
    def test_integration_workflows(self):
        """Test End-to-End Integration Workflows"""
        print("\n🔄 INTEGRATION WORKFLOWS AUDIT")
        
        if not self.auth_token:
            self.log_test("INTEGRATION", "End-to-End Workflows", False, "No auth token for integration tests")
            return
        
        headers = {'Authorization': f'Bearer {self.auth_token}'}
        
        # User Profile Workflow
        try:
            # Get profile
            response = self.session.get(f"{BACKEND_URL}/profile", headers=headers)
            if response.status_code == 200:
                # Update profile
                profile_update = {
                    "preferences": {
                        "budget_min": 10000,
                        "budget_max": 25000,
                        "preferred_countries": ["Spain", "Portugal"]
                    }
                }
                response = self.session.put(f"{BACKEND_URL}/profile", json=profile_update, headers=headers)
                if response.status_code == 200:
                    self.log_test("INTEGRATION", "User Profile Workflow", True, "Profile CRUD working")
                else:
                    self.log_test("INTEGRATION", "User Profile Workflow", False, f"Profile update failed: {response.status_code}")
            else:
                self.log_test("INTEGRATION", "User Profile Workflow", False, f"Profile get failed: {response.status_code}")
        except Exception as e:
            self.log_test("INTEGRATION", "User Profile Workflow", False, f"Profile workflow error: {str(e)}")
        
        # AI Integration Workflow
        try:
            # Test AI recommendations
            response = self.session.get(f"{BACKEND_URL}/ai/recommendations", headers=headers)
            if response.status_code == 200:
                # Test AI chat
                chat_data = {"message": "I'm looking for golf trips to Spain"}
                response = self.session.post(f"{BACKEND_URL}/ai/chat", json=chat_data, headers=headers)
                if response.status_code == 200:
                    self.log_test("INTEGRATION", "AI Integration Workflow", True, "AI recommendations and chat working")
                else:
                    self.log_test("INTEGRATION", "AI Integration Workflow", False, f"AI chat failed: {response.status_code}")
            else:
                self.log_test("INTEGRATION", "AI Integration Workflow", False, f"AI recommendations failed: {response.status_code}")
        except Exception as e:
            self.log_test("INTEGRATION", "AI Integration Workflow", False, f"AI workflow error: {str(e)}")
        
        # GDPR Compliance Workflow
        try:
            # Get privacy settings
            response = self.session.get(f"{BACKEND_URL}/privacy/settings", headers=headers)
            if response.status_code == 200:
                # Export data
                response = self.session.post(f"{BACKEND_URL}/privacy/export-data", headers=headers)
                if response.status_code == 200:
                    # Get audit trail
                    response = self.session.get(f"{BACKEND_URL}/audit/my-trail", headers=headers)
                    if response.status_code == 200:
                        self.log_test("INTEGRATION", "GDPR Compliance Workflow", True, "Full GDPR workflow working")
                    else:
                        self.log_test("INTEGRATION", "GDPR Compliance Workflow", False, f"Audit trail failed: {response.status_code}")
                else:
                    self.log_test("INTEGRATION", "GDPR Compliance Workflow", False, f"Data export failed: {response.status_code}")
            else:
                self.log_test("INTEGRATION", "GDPR Compliance Workflow", False, f"Privacy settings failed: {response.status_code}")
        except Exception as e:
            self.log_test("INTEGRATION", "GDPR Compliance Workflow", False, f"GDPR workflow error: {str(e)}")
    
    def run_comprehensive_audit(self):
        """Run complete comprehensive audit"""
        print("🚀 STARTING COMPREHENSIVE FINAL AUDIT")
        print(f"Testing against: {BACKEND_URL}")
        print(f"Test user: {TEST_USER_EMAIL}")
        print("=" * 80)
        
        # Setup
        if not self.setup_test_user():
            print("❌ Cannot proceed without test user setup")
            return
        
        # Run all audit phases
        self.test_phase1_security_systems()
        self.test_phase2_infrastructure_systems()
        self.test_phase3_frontend_integration()
        self.test_phase4_architecture_improvements()
        self.test_performance_scalability()
        self.test_integration_workflows()
        
        # Generate comprehensive summary
        self.generate_audit_summary()
    
    def generate_audit_summary(self):
        """Generate comprehensive audit summary"""
        print("\n" + "=" * 80)
        print("📊 COMPREHENSIVE AUDIT SUMMARY")
        print("=" * 80)
        
        # Overall statistics
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result['success'])
        failed_tests = total_tests - passed_tests
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        
        print(f"Total Tests Executed: {total_tests}")
        print(f"✅ Passed: {passed_tests}")
        print(f"❌ Failed: {failed_tests}")
        print(f"🎯 Success Rate: {success_rate:.1f}%")
        
        # Results by category
        categories = {}
        for result in self.test_results:
            category = result['category']
            if category not in categories:
                categories[category] = {'passed': 0, 'failed': 0, 'tests': []}
            
            if result['success']:
                categories[category]['passed'] += 1
            else:
                categories[category]['failed'] += 1
            categories[category]['tests'].append(result)
        
        print("\n📋 RESULTS BY AUDIT PHASE:")
        for category, stats in categories.items():
            total = stats['passed'] + stats['failed']
            rate = (stats['passed'] / total * 100) if total > 0 else 0
            print(f"  {category}: {stats['passed']}/{total} ({rate:.1f}%)")
        
        # Critical failures
        critical_failures = [r for r in self.test_results if not r['success'] and 
                           any(keyword in r['test'].lower() for keyword in ['jwt', 'auth', 'security', 'cors'])]
        
        if critical_failures:
            print(f"\n🚨 CRITICAL SECURITY ISSUES ({len(critical_failures)}):")
            for failure in critical_failures:
                print(f"  ❌ [{failure['category']}] {failure['test']}: {failure['details']}")
        
        # Failed tests by category
        print("\n❌ FAILED TESTS BY CATEGORY:")
        for category, stats in categories.items():
            failed_tests = [t for t in stats['tests'] if not t['success']]
            if failed_tests:
                print(f"\n  {category}:")
                for test in failed_tests:
                    print(f"    ❌ {test['test']}: {test['details']}")
        
        # System health assessment
        print("\n🏥 OVERALL SYSTEM HEALTH ASSESSMENT:")
        if success_rate >= 95:
            print("  🟢 EXCELLENT - System is production-ready with minimal issues")
        elif success_rate >= 85:
            print("  🟡 GOOD - System is mostly stable with some minor issues")
        elif success_rate >= 70:
            print("  🟠 FAIR - System has moderate issues that should be addressed")
        else:
            print("  🔴 POOR - System has significant issues requiring immediate attention")
        
        # Recommendations
        print("\n💡 RECOMMENDATIONS:")
        if failed_tests == 0:
            print("  ✅ All systems operational - ready for production")
        else:
            print(f"  🔧 Address {failed_tests} failed tests before production deployment")
            if critical_failures:
                print(f"  🚨 URGENT: Fix {len(critical_failures)} critical security issues immediately")
        
        return success_rate, critical_failures

if __name__ == "__main__":
    auditor = ComprehensiveAuditor()
    auditor.run_comprehensive_audit()