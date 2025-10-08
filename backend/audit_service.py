"""
GDPR-Compliant Audit Logging System
Tracks all data access, modifications, and user actions for compliance purposes
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime, timezone
from typing import Optional, Dict, Any, List
from enum import Enum
import logging
import json
import os
from pydantic import BaseModel

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AuditActionType(str, Enum):
    """Audit action types for GDPR compliance"""
    
    # Data Access Actions
    DATA_READ = "data_read"
    DATA_EXPORT = "data_export"
    DATA_VIEW = "data_view"
    
    # Data Modification Actions
    DATA_CREATE = "data_create"
    DATA_UPDATE = "data_update"
    DATA_DELETE = "data_delete"
    
    # User Authentication Actions
    USER_LOGIN = "user_login"
    USER_LOGOUT = "user_logout"
    USER_REGISTER = "user_register"
    
    # Consent Management Actions
    CONSENT_GIVEN = "consent_given"
    CONSENT_WITHDRAWN = "consent_withdrawn"
    CONSENT_UPDATED = "consent_updated"
    
    # Privacy Rights Actions
    GDPR_DATA_REQUEST = "gdpr_data_request"
    GDPR_DELETE_REQUEST = "gdpr_delete_request"
    GDPR_RECTIFICATION = "gdpr_rectification"
    
    # File Operations
    FILE_UPLOAD = "file_upload"
    FILE_DOWNLOAD = "file_download"
    FILE_DELETE = "file_delete"
    
    # Admin Actions
    ADMIN_ACCESS = "admin_access"
    USER_IMPERSONATION = "user_impersonation"
    SYSTEM_CONFIGURATION = "system_configuration"

class AuditLogEntry(BaseModel):
    """Audit log entry model"""
    id: str
    timestamp: datetime
    action_type: AuditActionType
    user_id: Optional[str] = None
    user_email: Optional[str] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    resource_type: Optional[str] = None  # e.g., "user_profile", "destination", "inquiry"
    resource_id: Optional[str] = None
    data_before: Optional[Dict] = None  # For updates/deletes
    data_after: Optional[Dict] = None   # For creates/updates
    metadata: Dict[str, Any] = {}
    legal_basis: Optional[str] = None   # GDPR legal basis
    retention_period_days: int = 2555   # 7 years default for audit logs

class AuditLogger:
    """GDPR-compliant audit logging service"""
    
    def __init__(self):
        self.mongo_url = os.environ.get('MONGO_URL')
        self.db_name = os.environ.get('DB_NAME', 'golftrip')
        self._client = None
        self._db = None
        
        # Configure retention periods (in days)
        self.retention_periods = {
            # Data access logs - 7 years for financial/legal compliance
            AuditActionType.DATA_READ: 2555,
            AuditActionType.DATA_EXPORT: 2555,
            AuditActionType.GDPR_DATA_REQUEST: 2555,
            
            # Authentication logs - 1 year
            AuditActionType.USER_LOGIN: 365,
            AuditActionType.USER_LOGOUT: 365,
            AuditActionType.USER_REGISTER: 2555,  # User registration kept longer
            
            # Data modifications - 7 years
            AuditActionType.DATA_CREATE: 2555,
            AuditActionType.DATA_UPDATE: 2555,
            AuditActionType.DATA_DELETE: 2555,
            
            # Consent management - 3 years after consent withdrawal
            AuditActionType.CONSENT_GIVEN: 1095,
            AuditActionType.CONSENT_WITHDRAWN: 1095,
            AuditActionType.CONSENT_UPDATED: 1095,
            
            # File operations - 3 years
            AuditActionType.FILE_UPLOAD: 1095,
            AuditActionType.FILE_DOWNLOAD: 1095,
            AuditActionType.FILE_DELETE: 1095,
            
            # Admin actions - 7 years
            AuditActionType.ADMIN_ACCESS: 2555,
            AuditActionType.USER_IMPERSONATION: 2555,
            AuditActionType.SYSTEM_CONFIGURATION: 2555,
        }
    
    @property
    async def db(self):
        """Lazy initialization of database connection"""
        if self._client is None:
            self._client = AsyncIOMotorClient(self.mongo_url)
            self._db = self._client[self.db_name]
        return self._db
    
    async def log_action(
        self,
        action_type: AuditActionType,
        user_id: Optional[str] = None,
        user_email: Optional[str] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        resource_type: Optional[str] = None,
        resource_id: Optional[str] = None,
        data_before: Optional[Dict] = None,
        data_after: Optional[Dict] = None,
        metadata: Optional[Dict] = None,
        legal_basis: Optional[str] = None
    ) -> str:
        """
        Log an audit event for GDPR compliance
        
        Args:
            action_type: Type of action being audited
            user_id: ID of user performing action
            user_email: Email of user performing action  
            ip_address: IP address of request
            user_agent: Browser user agent
            resource_type: Type of resource being accessed/modified
            resource_id: ID of specific resource
            data_before: Data state before modification
            data_after: Data state after modification
            metadata: Additional context information
            legal_basis: GDPR legal basis for processing
            
        Returns:
            Audit log entry ID
        """
        
        try:
            db = await self.db
            
            # Generate unique audit entry ID
            import uuid
            audit_id = str(uuid.uuid4())
            
            # Sanitize sensitive data before logging
            sanitized_before = self._sanitize_data(data_before) if data_before else None
            sanitized_after = self._sanitize_data(data_after) if data_after else None
            
            # Create audit entry
            audit_entry = AuditLogEntry(
                id=audit_id,
                timestamp=datetime.now(timezone.utc),
                action_type=action_type,
                user_id=user_id,
                user_email=user_email,
                ip_address=ip_address,
                user_agent=user_agent,
                resource_type=resource_type,
                resource_id=resource_id,
                data_before=sanitized_before,
                data_after=sanitized_after,
                metadata=metadata or {},
                legal_basis=legal_basis,
                retention_period_days=self.retention_periods.get(action_type, 2555)
            )
            
            # Calculate expiration date for automatic cleanup
            from datetime import timedelta
            expiration_date = datetime.now(timezone.utc) + timedelta(
                days=audit_entry.retention_period_days
            )
            
            # Store in database with TTL index for automatic deletion
            audit_dict = audit_entry.model_dump()
            audit_dict['expires_at'] = expiration_date
            
            await db.audit_logs.insert_one(audit_dict)
            
            logger.info(f"Audit log created: {action_type} by user {user_id} on {resource_type}/{resource_id}")
            
            return audit_id
            
        except Exception as e:
            logger.error(f"Failed to create audit log: {str(e)}")
            # Don't raise exception to avoid breaking main application flow
            return ""
    
    def _sanitize_data(self, data: Dict) -> Dict:
        """Remove or hash sensitive data before logging"""
        if not data:
            return data
        
        sanitized = data.copy()
        
        # Fields to completely remove from audit logs
        remove_fields = [
            'password', 'hashed_password', 'token', 'api_key',
            'credit_card', 'ssn', 'passport_number'
        ]
        
        # Fields to hash instead of storing plaintext
        hash_fields = [
            'email', 'phone_number', 'ip_address'
        ]
        
        for field in remove_fields:
            if field in sanitized:
                sanitized[field] = "[REDACTED]"
        
        for field in hash_fields:
            if field in sanitized and sanitized[field]:
                import hashlib
                sanitized[field] = hashlib.sha256(str(sanitized[field]).encode()).hexdigest()[:16]
        
        return sanitized
    
    async def get_user_audit_trail(
        self, 
        user_id: str, 
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        action_types: Optional[List[AuditActionType]] = None,
        limit: int = 1000
    ) -> List[Dict]:
        """
        Get audit trail for a specific user (GDPR Article 15 - Right of Access)
        
        Args:
            user_id: User ID to get audit trail for
            start_date: Optional start date filter
            end_date: Optional end date filter
            action_types: Optional list of action types to filter
            limit: Maximum number of entries to return
            
        Returns:
            List of audit log entries
        """
        
        try:
            db = await self.db
            
            # Build query
            query = {"user_id": user_id}
            
            if start_date or end_date:
                query["timestamp"] = {}
                if start_date:
                    query["timestamp"]["$gte"] = start_date
                if end_date:
                    query["timestamp"]["$lte"] = end_date
            
            if action_types:
                query["action_type"] = {"$in": [str(action) for action in action_types]}
            
            # Execute query
            cursor = db.audit_logs.find(query, {"_id": 0}).sort("timestamp", -1).limit(limit)
            entries = await cursor.to_list(length=None)
            
            return entries
            
        except Exception as e:
            logger.error(f"Failed to get user audit trail: {str(e)}")
            return []
    
    async def get_resource_audit_trail(
        self,
        resource_type: str,
        resource_id: str,
        limit: int = 100
    ) -> List[Dict]:
        """Get audit trail for a specific resource"""
        
        try:
            db = await self.db
            
            query = {
                "resource_type": resource_type,
                "resource_id": resource_id
            }
            
            cursor = db.audit_logs.find(query, {"_id": 0}).sort("timestamp", -1).limit(limit)
            entries = await cursor.to_list(length=None)
            
            return entries
            
        except Exception as e:
            logger.error(f"Failed to get resource audit trail: {str(e)}")
            return []
    
    async def cleanup_expired_logs(self) -> int:
        """Clean up expired audit logs (run as scheduled task)"""
        
        try:
            db = await self.db
            
            # MongoDB TTL index should handle this automatically,
            # but we can also do manual cleanup
            current_time = datetime.now(timezone.utc)
            
            result = await db.audit_logs.delete_many({
                "expires_at": {"$lt": current_time}
            })
            
            deleted_count = result.deleted_count
            if deleted_count > 0:
                logger.info(f"Cleaned up {deleted_count} expired audit log entries")
            
            return deleted_count
            
        except Exception as e:
            logger.error(f"Failed to cleanup expired audit logs: {str(e)}")
            return 0
    
    async def generate_gdpr_report(self, user_id: str) -> Dict:
        """
        Generate comprehensive GDPR data processing report for a user
        
        Args:
            user_id: User ID to generate report for
            
        Returns:
            Comprehensive audit report
        """
        
        try:
            # Get all audit entries for user
            all_entries = await self.get_user_audit_trail(user_id, limit=10000)
            
            # Analyze audit data
            report = {
                "user_id": user_id,
                "report_generated_at": datetime.now(timezone.utc).isoformat(),
                "total_logged_actions": len(all_entries),
                "date_range": {
                    "first_action": None,
                    "last_action": None
                },
                "action_summary": {},
                "data_access_summary": {
                    "total_data_reads": 0,
                    "total_data_exports": 0,
                    "total_file_downloads": 0
                },
                "data_modification_summary": {
                    "total_creates": 0,
                    "total_updates": 0,
                    "total_deletes": 0
                },
                "consent_history": [],
                "gdpr_requests": []
            }
            
            if all_entries:
                # Date range
                report["date_range"]["first_action"] = all_entries[-1]["timestamp"]
                report["date_range"]["last_action"] = all_entries[0]["timestamp"]
                
                # Analyze actions
                for entry in all_entries:
                    action_type = entry["action_type"]
                    
                    # Count action types
                    if action_type not in report["action_summary"]:
                        report["action_summary"][action_type] = 0
                    report["action_summary"][action_type] += 1
                    
                    # Data access tracking
                    if action_type in ["data_read", "data_view"]:
                        report["data_access_summary"]["total_data_reads"] += 1
                    elif action_type == "data_export":
                        report["data_access_summary"]["total_data_exports"] += 1
                    elif action_type == "file_download":
                        report["data_access_summary"]["total_file_downloads"] += 1
                    
                    # Data modification tracking
                    if action_type == "data_create":
                        report["data_modification_summary"]["total_creates"] += 1
                    elif action_type == "data_update":
                        report["data_modification_summary"]["total_updates"] += 1
                    elif action_type == "data_delete":
                        report["data_modification_summary"]["total_deletes"] += 1
                    
                    # Consent tracking
                    if "consent" in action_type:
                        report["consent_history"].append({
                            "action": action_type,
                            "timestamp": entry["timestamp"],
                            "details": entry.get("metadata", {})
                        })
                    
                    # GDPR requests
                    if "gdpr" in action_type:
                        report["gdpr_requests"].append({
                            "request_type": action_type,
                            "timestamp": entry["timestamp"],
                            "status": entry.get("metadata", {}).get("status", "unknown")
                        })
            
            return report
            
        except Exception as e:
            logger.error(f"Failed to generate GDPR report: {str(e)}")
            return {}

# Initialize audit logger
audit_logger = AuditLogger()