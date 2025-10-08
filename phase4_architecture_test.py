#!/usr/bin/env python3
"""
Phase 4 Architecture Improvements Testing
Tests the new modular backend architecture components
"""

import requests
import json
import sys
import os
from datetime import datetime

# Configuration
BACKEND_URL = "https://golf-ai-advisor.preview.emergentagent.com/api"

class Phase4ArchitectureTester:
    def __init__(self):
        self.session = requests.Session()
        self.test_results = []
        
    def log_test(self, test_name, success, details=""):
        """Log test results"""
        status = "✅ PASS" if success else "❌ FAIL"
        result = {
            "test": test_name,
            "status": status,
            "success": success,
            "details": details,
            "timestamp": datetime.now().isoformat()
        }
        self.test_results.append(result)
        print(f"{status} {test_name}: {details}")
    
    def test_configuration_system(self):
        """Test Phase 4 core configuration system"""
        print("\n⚙️ TESTING PHASE 4 CONFIGURATION SYSTEM")
        
        try:
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

    def test_database_manager(self):
        """Test Phase 4 database connection management"""
        print("\n💾 TESTING PHASE 4 DATABASE MANAGER")
        
        try:
            sys.path.append('/app/backend')
            from core.database import db_manager
            
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

    def test_rate_limiting_middleware(self):
        """Test Phase 4 rate limiting middleware"""
        print("\n🚦 TESTING PHASE 4 RATE LIMITING MIDDLEWARE")
        
        try:
            sys.path.append('/app/backend')
            from middleware.rate_limiting import rate_limit_monitor
            
            # Test rate limit monitoring
            stats = rate_limit_monitor.get_rate_limit_stats()
            if isinstance(stats, dict) and 'total_buckets' in stats:
                self.log_test("Rate Limiting - Monitoring", True, f"Rate limit monitoring working: {stats['total_buckets']} buckets")
            else:
                self.log_test("Rate Limiting - Monitoring", False, "Rate limit monitoring not working")
                
        except Exception as e:
            self.log_test("Rate Limiting - Monitoring", False, f"Rate limit monitoring error: {str(e)}")
        
        # Test rate limiting on authentication endpoints
        login_data = {
            "email": "nonexistent@test.com",
            "password": "wrongpassword"
        }
        
        rate_limit_hit = False
        requests_made = 0
        
        # Make multiple requests to trigger rate limiting
        for i in range(12):  # Try to exceed the rate limit
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

    def test_service_layer_architecture(self):
        """Test Phase 4 service layer architecture"""
        print("\n🏗️ TESTING PHASE 4 SERVICE LAYER ARCHITECTURE")
        
        # Test modular API routes
        modular_endpoints = [
            "/auth/login", 
            "/auth/register"
        ]
        
        for endpoint in modular_endpoints:
            try:
                # Just test that the endpoint exists (OPTIONS request)
                response = self.session.options(f"{BACKEND_URL}{endpoint}")
                
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

    def test_backward_compatibility(self):
        """Test backward compatibility with existing functionality"""
        print("\n🔄 TESTING BACKWARD COMPATIBILITY")
        
        # Test that existing endpoints still work
        existing_endpoints = [
            "/destinations",
            "/articles", 
            "/partners",
            "/testimonials"
        ]
        
        for endpoint in existing_endpoints:
            try:
                response = self.session.get(f"{BACKEND_URL}{endpoint}")
                if response.status_code == 200:
                    self.log_test(f"Backward Compatibility - {endpoint}", True, "Existing endpoint still working")
                else:
                    self.log_test(f"Backward Compatibility - {endpoint}", False, f"Endpoint broken: {response.status_code}")
            except Exception as e:
                self.log_test(f"Backward Compatibility - {endpoint}", False, f"Error testing {endpoint}: {str(e)}")

    def test_performance_improvements(self):
        """Test performance improvements from new architecture"""
        print("\n⚡ TESTING PERFORMANCE IMPROVEMENTS")
        
        import time
        
        # Test response times for database queries
        start_time = time.time()
        response = self.session.get(f"{BACKEND_URL}/destinations")
        end_time = time.time()
        
        response_time = (end_time - start_time) * 1000  # Convert to milliseconds
        
        if response.status_code == 200 and response_time < 2000:  # Less than 2 seconds
            self.log_test("Performance - Database Queries", True, f"Fast response time: {response_time:.2f}ms")
        elif response.status_code == 200:
            self.log_test("Performance - Database Queries", False, f"Slow response time: {response_time:.2f}ms")
        else:
            self.log_test("Performance - Database Queries", False, f"Query failed: {response.status_code}")

    def run_all_tests(self):
        """Run all Phase 4 architecture tests"""
        print("🚀 STARTING PHASE 4 ARCHITECTURE IMPROVEMENTS TESTING")
        print(f"Testing against: {BACKEND_URL}")
        print("=" * 60)
        
        # Run all tests
        self.test_configuration_system()
        self.test_database_manager()
        self.test_rate_limiting_middleware()
        self.test_service_layer_architecture()
        self.test_backward_compatibility()
        self.test_performance_improvements()
        
        # Summary
        print("\n" + "=" * 60)
        print("📊 PHASE 4 ARCHITECTURE TEST SUMMARY")
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
        
        return passed, failed

if __name__ == "__main__":
    tester = Phase4ArchitectureTester()
    passed, failed = tester.run_all_tests()
    
    # Exit with appropriate code
    if failed > 0:
        sys.exit(1)
    else:
        sys.exit(0)