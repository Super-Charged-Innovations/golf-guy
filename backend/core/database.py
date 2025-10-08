"""
Database connection and management module
Provides centralized database access with connection pooling and monitoring
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from typing import Optional, Dict, Any
import logging
from datetime import datetime, timezone
from core.config import settings

logger = logging.getLogger(__name__)

class DatabaseManager:
    """
    Centralized database management with connection pooling and health monitoring
    """
    
    def __init__(self):
        self._client: Optional[AsyncIOMotorClient] = None
        self._db: Optional[AsyncIOMotorDatabase] = None
        self._connection_pool_size = 10
        self._max_pool_size = 100
        self._connection_timeout = 10000  # 10 seconds
        
    async def connect(self) -> AsyncIOMotorDatabase:
        """
        Establish database connection with connection pooling
        """
        if self._client is None:
            try:
                self._client = AsyncIOMotorClient(
                    settings.database.mongo_url,
                    maxPoolSize=self._max_pool_size,
                    minPoolSize=self._connection_pool_size,
                    serverSelectionTimeoutMS=self._connection_timeout,
                    connectTimeoutMS=self._connection_timeout,
                    socketTimeoutMS=self._connection_timeout,
                    retryWrites=True,
                    w='majority'  # Write concern for data durability
                )
                
                # Test the connection
                await self._client.admin.command('ping')
                logger.info("Connected to MongoDB successfully")
                
                self._db = self._client[settings.database.db_name]
                
                # Create indexes on startup
                await self._create_indexes()
                
            except Exception as e:
                logger.error(f"Failed to connect to MongoDB: {str(e)}")
                raise
        
        return self._db
    
    async def disconnect(self):
        """Close database connection"""
        if self._client:
            self._client.close()
            logger.info("Disconnected from MongoDB")
    
    async def _create_indexes(self):
        """Create database indexes for optimal performance"""
        try:
            db = self._db
            
            # User collection indexes
            await db.users.create_index("email", unique=True)
            await db.users.create_index("created_at")
            await db.users.create_index("is_admin")
            
            # User profiles indexes
            await db.user_profiles.create_index("user_id", unique=True)
            await db.user_profiles.create_index("tier")
            await db.user_profiles.create_index("kyc_completed")
            
            # Destinations indexes
            await db.destinations.create_index("slug", unique=True)
            await db.destinations.create_index("country")
            await db.destinations.create_index("featured")
            await db.destinations.create_index("published")
            await db.destinations.create_index([("name", "text"), ("short_desc", "text"), ("long_desc", "text")])
            
            # Articles indexes
            await db.articles.create_index("slug", unique=True)
            await db.articles.create_index("category")
            await db.articles.create_index("published")
            await db.articles.create_index("publish_date")
            await db.articles.create_index([("title", "text"), ("content", "text")])
            
            # Inquiries indexes
            await db.inquiries.create_index("email")
            await db.inquiries.create_index("status")
            await db.inquiries.create_index("created_at")
            await db.inquiries.create_index("destination_id")
            
            # Audit logs indexes with TTL
            await db.audit_logs.create_index("user_id")
            await db.audit_logs.create_index("action_type")
            await db.audit_logs.create_index("timestamp")
            await db.audit_logs.create_index("resource_type")
            await db.audit_logs.create_index("expires_at", expireAfterSeconds=0)  # TTL index
            
            # Hero carousel indexes
            await db.hero_carousel.create_index("order")
            await db.hero_carousel.create_index("active")
            
            # Testimonials indexes
            await db.testimonials.create_index("destination_id")
            await db.testimonials.create_index("published")
            await db.testimonials.create_index("rating")
            
            # Partners indexes
            await db.partners.create_index("type")
            await db.partners.create_index("active")
            await db.partners.create_index("order")
            
            # GDPR-related indexes
            await db.consent_records.create_index("user_id")
            await db.consent_records.create_index("consent_type")
            await db.consent_records.create_index("timestamp")
            
            await db.data_export_requests.create_index("user_id")
            await db.data_export_requests.create_index("status")
            await db.data_export_requests.create_index("requested_at")
            
            await db.data_deletion_requests.create_index("user_id")
            await db.data_deletion_requests.create_index("status")
            await db.data_deletion_requests.create_index("requested_at")
            
            await db.privacy_settings.create_index("user_id", unique=True)
            
            logger.info("Database indexes created successfully")
            
        except Exception as e:
            logger.error(f"Failed to create database indexes: {str(e)}")
            # Don't raise here as the app should still work without indexes
    
    async def health_check(self) -> Dict[str, Any]:
        """
        Perform database health check
        """
        try:
            if not self._client:
                return {
                    "status": "disconnected",
                    "error": "No database connection"
                }
            
            # Test database connectivity
            start_time = datetime.now()
            await self._client.admin.command('ping')
            response_time = (datetime.now() - start_time).total_seconds() * 1000
            
            # Get database statistics
            db_stats = await self._db.command('dbStats')
            server_status = await self._client.admin.command('serverStatus')
            
            # Check connection pool status
            pool_stats = {
                "current_connections": server_status.get('connections', {}).get('current', 0),
                "available_connections": server_status.get('connections', {}).get('available', 0),
                "total_created": server_status.get('connections', {}).get('totalCreated', 0)
            }
            
            return {
                "status": "healthy",
                "response_time_ms": round(response_time, 2),
                "database_size_mb": round(db_stats.get('dataSize', 0) / (1024 * 1024), 2),
                "collections_count": db_stats.get('collections', 0),
                "indexes_count": db_stats.get('indexes', 0),
                "connection_pool": pool_stats,
                "server_version": server_status.get('version', 'unknown'),
                "uptime_seconds": server_status.get('uptime', 0)
            }
            
        except Exception as e:
            logger.error(f"Database health check failed: {str(e)}")
            return {
                "status": "unhealthy",
                "error": str(e)
            }
    
    async def get_collection_stats(self) -> Dict[str, Any]:
        """Get statistics for all collections"""
        try:
            collections = await self._db.list_collection_names()
            stats = {}
            
            for collection_name in collections:
                collection_stats = await self._db.command('collStats', collection_name)
                stats[collection_name] = {
                    "document_count": collection_stats.get('count', 0),
                    "size_mb": round(collection_stats.get('size', 0) / (1024 * 1024), 2),
                    "avg_document_size": collection_stats.get('avgObjSize', 0),
                    "index_count": collection_stats.get('nindexes', 0)
                }
            
            return stats
            
        except Exception as e:
            logger.error(f"Failed to get collection stats: {str(e)}")
            return {}
    
    async def cleanup_expired_data(self) -> Dict[str, int]:
        """Clean up expired data across collections"""
        cleanup_results = {}
        current_time = datetime.now(timezone.utc)
        
        try:
            # Cleanup expired audit logs (if TTL index fails)
            result = await self._db.audit_logs.delete_many({
                "expires_at": {"$lt": current_time}
            })
            cleanup_results["audit_logs"] = result.deleted_count
            
            # Cleanup old temporary data
            # Add more cleanup operations as needed
            
            logger.info(f"Data cleanup completed: {cleanup_results}")
            return cleanup_results
            
        except Exception as e:
            logger.error(f"Data cleanup failed: {str(e)}")
            return {}

# Global database manager instance
db_manager = DatabaseManager()

# Dependency for FastAPI to get database
async def get_database() -> AsyncIOMotorDatabase:
    """FastAPI dependency to get database connection"""
    return await db_manager.connect()

# Export commonly used database access
async def get_db():
    """Simple database getter for direct usage"""
    return await db_manager.connect()