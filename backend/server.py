"""
Golf Guy Platform - Main FastAPI Application
Modular architecture with proper separation of concerns
"""
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

# Core modules
from core.config import settings, validate_startup_config
from core.database import db_manager

# API routes
from api.auth.routes import router as auth_router

# Legacy imports for existing routes (to be modularized)
from fastapi import APIRouter, HTTPException, Query, Depends, Header, UploadFile, File, Form
from fastapi.responses import PlainTextResponse, StreamingResponse
from pydantic import BaseModel, Field, ConfigDict, EmailStr
from typing import List, Optional, Dict, Any
import uuid
from datetime import datetime, timezone, timedelta
import io
import csv

# Services
from services.auth_service import auth_service, require_auth, require_admin
from ai_service import ai_service
from s3_service import s3_service
from services.audit_service import audit_logger, AuditActionType

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management"""
    
    # Startup
    logger.info("Starting Golf Guy Platform API")
    
    # Validate configuration
    config_valid = validate_startup_config()
    if not config_valid:
        logger.warning("Configuration validation found issues")
    
    # Initialize database connection
    try:
        await db_manager.connect()
        logger.info("Database connection established")
    except Exception as e:
        logger.error(f"Failed to connect to database: {e}")
        raise
    
    # Log startup completion
    logger.info(f"Golf Guy Platform API v{settings.app.version} started successfully")
    
    yield
    
    # Shutdown
    logger.info("Shutting down Golf Guy Platform API")
    await db_manager.disconnect()

# Create FastAPI application with lifespan management
app = FastAPI(
    title=settings.app.app_name,
    version=settings.app.version,
    description="Production-grade golf travel platform with AI recommendations and GDPR compliance",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.get_cors_origins(),
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(auth_router, prefix="/api")

# Create API router for legacy routes (to be gradually moved to modules)
api_router = APIRouter(prefix="/api")

# Get database dependency (using new architecture)
async def get_db():
    return await db_manager.connect()

# ===== EXISTING MODELS (TO BE MOVED TO MODELS MODULE) =====

# SEO Model
class SEO(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    canonical: Optional[str] = None

# Package Model for Destinations
class Package(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    duration_nights: int
    duration_days: int
    price: int
    currency: str = "SEK"
    inclusions: List[str] = []
    exclusions: List[str] = []
    description: Optional[str] = None
    available: bool = True

# Course Details Model
class CourseDetails(BaseModel):
    par: Optional[int] = None
    holes: Optional[int] = None
    length_meters: Optional[int] = None
    difficulty: Optional[str] = None  # Easy, Medium, Hard, Championship
    designer: Optional[str] = None
    year_established: Optional[int] = None
    course_type: Optional[str] = None  # Links, Parkland, Desert, Mountain, etc.

# Resort Amenities Model
class ResortAmenities(BaseModel):
    spa: bool = False
    restaurants: int = 0
    pools: int = 0
    gym: bool = False
    kids_club: bool = False
    conference_facilities: bool = False
    beach_access: bool = False
    additional: List[str] = []

# Destination Models
class Destination(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    slug: str
    country: str
    region: Optional[str] = None
    short_desc: str
    long_desc: str
    
    # Categorization
    destination_type: str = "golf_course"  # golf_course, golf_resort, both
    
    # Pricing
    price_from: int
    price_to: int
    currency: str = "SEK"
    
    # Media
    images: List[str] = []
    video_url: Optional[str] = None
    
    # Details
    highlights: List[str] = []
    courses: List[CourseDetails] = []  # Multiple courses at one destination
    amenities: Optional[ResortAmenities] = None
    packages: List[Package] = []
    
    # Location details
    location_coordinates: Optional[Dict[str, float]] = None  # lat, lng
    climate: Optional[str] = None
    best_time_to_visit: Optional[str] = None
    
    # Logistics
    nearest_airport: Optional[str] = None
    transfer_time: Optional[str] = None
    
    # Status
    featured: bool = False
    published: bool = True
    
    # SEO
    seo: Optional[SEO] = None
    
    # Timestamps
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class DestinationCreate(BaseModel):
    name: str
    slug: str
    country: str
    region: Optional[str] = None
    short_desc: str
    long_desc: str
    destination_type: str = "golf_course"
    price_from: int
    price_to: int
    currency: str = "SEK"
    images: List[str] = []
    video_url: Optional[str] = None
    highlights: List[str] = []
    courses: List[CourseDetails] = []
    amenities: Optional[ResortAmenities] = None
    packages: List[Package] = []
    location_coordinates: Optional[Dict[str, float]] = None
    climate: Optional[str] = None
    best_time_to_visit: Optional[str] = None
    nearest_airport: Optional[str] = None
    transfer_time: Optional[str] = None
    featured: bool = False
    published: bool = True
    seo: Optional[SEO] = None

class DestinationUpdate(BaseModel):
    name: Optional[str] = None
    slug: Optional[str] = None
    country: Optional[str] = None
    region: Optional[str] = None
    short_desc: Optional[str] = None
    long_desc: Optional[str] = None
    destination_type: Optional[str] = None
    price_from: Optional[int] = None
    price_to: Optional[int] = None
    currency: Optional[str] = None
    images: Optional[List[str]] = None
    video_url: Optional[str] = None
    highlights: Optional[List[str]] = None
    courses: Optional[List[CourseDetails]] = None
    amenities: Optional[ResortAmenities] = None
    packages: Optional[List[Package]] = None
    location_coordinates: Optional[Dict[str, float]] = None
    climate: Optional[str] = None
    best_time_to_visit: Optional[str] = None
    nearest_airport: Optional[str] = None
    transfer_time: Optional[str] = None
    featured: Optional[bool] = None
    published: Optional[bool] = None
    seo: Optional[SEO] = None

# Article Models
class Article(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    slug: str
    content: str
    excerpt: Optional[str] = None
    category: Optional[str] = None
    author: Optional[str] = None
    publish_date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    featured_until: Optional[datetime] = None
    destination_ids: List[str] = []
    image: Optional[str] = None
    published: bool = True
    seo: Optional[SEO] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class ArticleCreate(BaseModel):
    title: str
    slug: str
    content: str
    excerpt: Optional[str] = None
    category: Optional[str] = None
    author: Optional[str] = None
    publish_date: Optional[datetime] = None
    featured_until: Optional[datetime] = None
    destination_ids: Optional[List[str]] = None
    image: Optional[str] = None
    published: Optional[bool] = None
    seo: Optional[SEO] = None

class ArticleUpdate(BaseModel):
    title: Optional[str] = None
    slug: Optional[str] = None
    content: Optional[str] = None
    excerpt: Optional[str] = None
    category: Optional[str] = None
    author: Optional[str] = None
    publish_date: Optional[datetime] = None
    featured_until: Optional[datetime] = None
    destination_ids: Optional[List[str]] = None
    image: Optional[str] = None
    published: Optional[bool] = None
    seo: Optional[SEO] = None

# Continue with rest of existing models...
# (Continuing with the existing model definitions to maintain compatibility)

# ===== HELPER FUNCTIONS =====

def serialize_datetime(doc: dict) -> dict:
    """Convert datetime objects to ISO strings for MongoDB storage"""
    if not doc:
        return doc
    for key, value in doc.items():
        if isinstance(value, datetime):
            doc[key] = value.isoformat()
        elif isinstance(value, list):
            doc[key] = [serialize_datetime(item) if isinstance(item, dict) else item for item in value]
        elif isinstance(value, dict):
            doc[key] = serialize_datetime(value)
    return doc

def deserialize_datetime(doc: dict, fields: List[str]) -> dict:
    """Convert ISO string timestamps back to datetime objects"""
    if not doc:
        return doc
    for field in fields:
        if field in doc and isinstance(doc[field], str):
            try:
                doc[field] = datetime.fromisoformat(doc[field])
            except:
                pass
    return doc

# ===== API ROUTES =====

@api_router.get("/")
async def root():
    """API root endpoint with system information"""
    return {
        "message": settings.app.app_name,
        "version": settings.app.version,
        "environment": settings.app.environment,
        "status": "operational"
    }

@api_router.get("/health")
async def health_check():
    """Comprehensive health check endpoint"""
    
    # Database health check
    db_health = await db_manager.health_check()
    
    # Configuration validation
    config_warnings = settings.validate_configuration()
    
    return {
        "status": "healthy" if db_health["status"] == "healthy" else "degraded",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "version": settings.app.version,
        "environment": settings.app.environment,
        "database": db_health,
        "configuration": {
            "aws_configured": settings.aws.is_configured,
            "ai_configured": bool(settings.ai.api_key),
            "cache_enabled": settings.cache.enable_caching,
            "warnings_count": len(config_warnings)
        }
    }

# User Profile Routes (using new auth dependencies)
@api_router.get("/profile")
async def get_user_profile(
    current_user: dict = Depends(require_auth),
    db = Depends(get_db)
):
    """Get user profile and preferences"""
    
    profile = await db.user_profiles.find_one({"user_id": current_user["id"]}, {"_id": 0})
    
    if not profile:
        # Create default profile if it doesn't exist
        from models.user_models import UserProfile
        profile = UserProfile(user_id=current_user["id"])
        profile_dict = profile.model_dump()
        profile_dict = serialize_datetime(profile_dict)
        await db.user_profiles.insert_one(profile_dict)
        
        # Log profile creation
        await audit_logger.log_action(
            action_type=AuditActionType.DATA_CREATE,
            user_id=current_user["id"],
            user_email=current_user["email"],
            resource_type="user_profile",
            resource_id=current_user["id"],
            legal_basis="Contract performance"
        )
        
        profile = profile_dict
    
    # Deserialize datetime fields
    profile = deserialize_datetime(profile, ["created_at", "updated_at"])
    
    # Log profile access
    await audit_logger.log_action(
        action_type=AuditActionType.DATA_READ,
        user_id=current_user["id"],
        user_email=current_user["email"],
        resource_type="user_profile",
        resource_id=current_user["id"],
        legal_basis="Contract performance"
    )
    
    return profile

# Add all other existing routes here...
# (The rest of the routes would be added here to maintain compatibility)

# Include the API router
app.include_router(api_router)

# Add system monitoring endpoints
@app.get("/api/admin/system/stats")
async def get_system_stats(
    current_user: dict = Depends(require_admin),
    db = Depends(get_db)
):
    """Get comprehensive system statistics (Admin only)"""
    
    # Database statistics
    db_stats = await db_manager.get_collection_stats()
    
    # Configuration status
    config_warnings = settings.validate_configuration()
    
    return {
        "system_info": {
            "version": settings.app.version,
            "environment": settings.app.environment,
            "uptime": "Not implemented yet",
        },
        "database": db_stats,
        "configuration": {
            "warnings": config_warnings,
            "aws_configured": settings.aws.is_configured,
            "ai_configured": bool(settings.ai.api_key),
        }
    }

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": f"Welcome to {settings.app.app_name}",
        "version": settings.app.version,
        "status": "operational"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "server:app", 
        host="0.0.0.0", 
        port=8001, 
        reload=settings.is_development()
    )