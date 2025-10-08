from fastapi import FastAPI, APIRouter, HTTPException, Query, Depends, Header, UploadFile, File, Form, Request
from fastapi.responses import PlainTextResponse, StreamingResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict, EmailStr
from typing import List, Optional, Dict, Any
import uuid
from datetime import datetime, timezone, timedelta
import io
import csv
from auth_service import auth_service
from ai_service import ai_service
from s3_service import s3_service
from audit_service import audit_logger, AuditActionType

# Rate limiting middleware
class RateLimiter:
    """Simple rate limiter for authentication endpoints"""
    def __init__(self):
        self.attempts = {}
        self.max_attempts = 10
        self.window = 3600  # 1 hour
    
    def is_allowed(self, key: str) -> bool:
        """Check if request is allowed"""
        import time
        current_time = time.time()
        
        if key not in self.attempts:
            self.attempts[key] = []
        
        # Clean old attempts
        self.attempts[key] = [t for t in self.attempts[key] if current_time - t < self.window]
        
        # Check if under limit
        if len(self.attempts[key]) < self.max_attempts:
            self.attempts[key].append(current_time)
            return True
        return False

rate_limiter = RateLimiter()


ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ.get('DB_NAME', 'golftrip')]

# Create the main app without a prefix
app = FastAPI()

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")


# ===== Models =====

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
    destination_ids: List[str] = []
    image: Optional[str] = None
    published: bool = True
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

# HeroCarousel Models
class HeroCarousel(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    subtitle: str
    kicker: Optional[str] = None
    image: str
    destination_id: Optional[str] = None
    cta_text: str = "Start Inquiry"
    cta_url: str = "/contact"
    order: int = 0
    active: bool = True
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class HeroCarouselCreate(BaseModel):
    title: str
    subtitle: str
    kicker: Optional[str] = None
    image: str
    destination_id: Optional[str] = None
    cta_text: str = "Start Inquiry"
    cta_url: str = "/contact"
    order: int = 0
    active: bool = True

class HeroCarouselUpdate(BaseModel):
    title: Optional[str] = None
    subtitle: Optional[str] = None
    kicker: Optional[str] = None
    image: Optional[str] = None
    destination_id: Optional[str] = None
    cta_text: Optional[str] = None
    cta_url: Optional[str] = None
    order: Optional[int] = None
    active: Optional[bool] = None

# Testimonial Models
class Testimonial(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    rating: int  # 1-5
    content: str
    destination_id: Optional[str] = None
    trip_date: Optional[str] = None
    published: bool = True
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class TestimonialCreate(BaseModel):
    name: str
    rating: int
    content: str
    destination_id: Optional[str] = None
    trip_date: Optional[str] = None
    published: bool = True

class TestimonialUpdate(BaseModel):
    name: Optional[str] = None
    rating: Optional[int] = None
    content: Optional[str] = None
    destination_id: Optional[str] = None
    trip_date: Optional[str] = None
    published: Optional[bool] = None

# Partner Models
class Partner(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    type: str  # e.g., "insurance", "charity", "course"
    logo: str
    description: Optional[str] = None
    url: Optional[str] = None
    order: int = 0
    active: bool = True

class PartnerCreate(BaseModel):
    name: str
    type: str
    logo: str
    description: Optional[str] = None
    url: Optional[str] = None
    order: int = 0
    active: bool = True

class PartnerUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[str] = None
    logo: Optional[str] = None
    description: Optional[str] = None
    url: Optional[str] = None
    order: Optional[int] = None
    active: Optional[bool] = None

# Inquiry Models
class InquiryNote(BaseModel):
    text: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class Inquiry(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    email: EmailStr
    phone: Optional[str] = None
    destination_id: Optional[str] = None
    destination_name: Optional[str] = None
    dates: Optional[str] = None
    group_size: Optional[int] = None
    budget: Optional[str] = None
    message: Optional[str] = None
    status: str = "new"  # new, in_progress, responded, closed
    notes: List[InquiryNote] = []
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class InquiryCreate(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    destination_id: Optional[str] = None
    destination_name: Optional[str] = None
    dates: Optional[str] = None
    group_size: Optional[int] = None
    budget: Optional[str] = None
    message: Optional[str] = None

class InquiryUpdate(BaseModel):
    status: Optional[str] = None
    notes: Optional[List[InquiryNote]] = None

class InquiryAddNote(BaseModel):
    text: str

# Settings Models
class Setting(BaseModel):
    model_config = ConfigDict(extra="ignore")
    key: str
    value: Any

class SettingUpdate(BaseModel):
    value: Any

# User & Authentication Models
class User(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    email: EmailStr
    hashed_password: str
    full_name: str
    is_active: bool = True
    is_admin: bool = False
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    last_login: Optional[datetime] = None

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: str
    email: EmailStr
    full_name: str
    is_admin: bool

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

# User Profile & AI Portfolio Models
class UserPreferences(BaseModel):
    # Basic preferences (required for Tier 1)
    budget_min: int = 0
    budget_max: int = 50000
    preferred_countries: List[str] = []
    playing_level: str = "Intermediate"  # Beginner, Intermediate, Advanced, Professional
    accommodation_preference: str = "Any"  # Luxury, Mid-range, Budget, Any
    trip_duration_days: Optional[int] = None
    group_size: Optional[int] = None
    
    # Additional KYC info (for Tier 2-3)
    phone_number: Optional[str] = None
    travel_frequency: Optional[str] = None  # "First-time", "Annual", "Frequent"
    preferred_travel_months: List[str] = []
    dietary_requirements: Optional[str] = None
    special_requests: Optional[str] = None
    previous_golf_destinations: List[str] = []
    handicap: Optional[int] = None

class ConversationMessage(BaseModel):
    role: str  # user or assistant
    content: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class UserProfile(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    preferences: UserPreferences = Field(default_factory=UserPreferences)
    conversation_summary: str = ""
    conversation_history: List[Dict] = []  # Temporary storage, cleared after summarization
    past_inquiries: List[str] = []  # List of inquiry IDs
    kyc_notes: str = ""  # AI-generated KYC summary
    kyc_completed: bool = False  # Whether user has completed KYC
    tier: int = 0  # 0 = No KYC, 1-3 = Based on information completeness
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class UserProfileUpdate(BaseModel):
    preferences: Optional[UserPreferences] = None
    kyc_notes: Optional[str] = None

# GDPR Compliance Models
class ConsentRecord(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    consent_type: str  # marketing, analytics, cookies, data_processing
    granted: bool
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class DataExportRequest(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    email: str
    status: str = "pending"  # pending, processing, completed, failed
    export_data: Optional[Dict] = None
    requested_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    completed_at: Optional[datetime] = None

class DataDeletionRequest(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    email: str
    reason: Optional[str] = None
    status: str = "pending"  # pending, approved, processing, completed
    requested_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    completed_at: Optional[datetime] = None

class PrivacySettings(BaseModel):
    user_id: str
    marketing_emails: bool = False
    analytics_tracking: bool = True
    cookie_consent: bool = False
    data_sharing: bool = False
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

# AI Chat Models
class ChatMessage(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str
    conversation_id: Optional[str] = None

# AI Content Generation Models
class DestinationAIRequest(BaseModel):
    course_name: str
    location: str
    additional_info: Optional[str] = None

class RecommendationResponse(BaseModel):
    recommendations: List[Dict]

# File Upload Models
class FileUploadResponse(BaseModel):
    file_key: str
    file_url: str
    file_size: int
    mime_type: str
    original_filename: str
    category: str
    uploaded_at: str

class FileInfoResponse(BaseModel):
    file_key: str
    file_size: int
    last_modified: str
    content_type: str
    metadata: Dict
    server_side_encryption: str

class PresignedUrlResponse(BaseModel):
    presigned_url: str
    expires_in: int


# ===== Helper Functions =====

def calculate_user_tier(profile: UserProfile) -> int:
    """Calculate user tier based on KYC and profile completeness"""
    if not profile.kyc_completed:
        return 0
    
    prefs = profile.preferences
    score = 0
    
    # Tier 1 requirements (basic info)
    if prefs.budget_min and prefs.budget_max:
        score += 1
    if prefs.preferred_countries:
        score += 1
    if prefs.playing_level:
        score += 1
    if prefs.accommodation_preference and prefs.accommodation_preference != "Any":
        score += 1
    
    # Tier 2 requirements (enhanced info)
    if prefs.trip_duration_days:
        score += 1
    if prefs.group_size:
        score += 1
    if prefs.phone_number:
        score += 1
    if prefs.travel_frequency:
        score += 1
    
    # Tier 3 requirements (comprehensive info)
    if prefs.preferred_travel_months:
        score += 1
    if prefs.previous_golf_destinations:
        score += 1
    if prefs.handicap is not None:
        score += 1
    if profile.past_inquiries:
        score += 1
    
    # Determine tier
    if score <= 4:
        return 1
    elif score <= 8:
        return 2
    else:
        return 3

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


# ===== Authentication Dependency =====

security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Dependency to get current authenticated user"""
    token = credentials.credentials
    payload = auth_service.decode_token(token)
    
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token payload")
    
    # Fetch user from database
    user = await db.users.find_one({"id": user_id}, {"_id": 0})
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    
    deserialize_datetime(user, ["created_at", "last_login"])
    return user


# ===== Routes =====

@api_router.get("/")
async def root():
    return {"message": "Golf Guy Platform API", "version": "1.0.0"}

# Authentication Routes
@api_router.post("/auth/register", response_model=TokenResponse)
async def register(user_data: UserCreate, request: Request = None):
    """Register a new user with rate limiting"""
    
    # Apply rate limiting
    client_ip = request.client.host if request and request.client else "unknown"
    rate_key = f"register:{client_ip}"
    if not rate_limiter.is_allowed(rate_key):
        raise HTTPException(status_code=429, detail="Too many registration attempts. Please try again later.")
    
    # Check if user already exists
    existing_user = await db.users.find_one({"email": user_data.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create user
    user = User(
        email=user_data.email,
        hashed_password=auth_service.get_password_hash(user_data.password),
        full_name=user_data.full_name
    )
    
    user_dict = user.model_dump()
    user_dict = serialize_datetime(user_dict)
    await db.users.insert_one(user_dict)
    
    # Create user profile
    profile = UserProfile(user_id=user.id)
    profile_dict = profile.model_dump()
    profile_dict = serialize_datetime(profile_dict)
    await db.user_profiles.insert_one(profile_dict)
    
    # Generate token
    token = auth_service.create_access_token(data={"sub": user.id, "email": user.email})
    
    return TokenResponse(
        access_token=token,
        user=UserResponse(
            id=user.id,
            email=user.email,
            full_name=user.full_name,
            is_admin=user.is_admin
        )
    )

@api_router.post("/auth/login", response_model=TokenResponse)
async def login(credentials: UserLogin, request: Request = None):
    """Login with email and password with rate limiting"""
    
    # Apply rate limiting
    client_ip = request.client.host if request and request.client else "unknown"
    rate_key = f"login:{credentials.email}:{client_ip}"
    if not rate_limiter.is_allowed(rate_key):
        raise HTTPException(status_code=429, detail="Too many login attempts. Please try again later.")
    
    user = await db.users.find_one({"email": credentials.email}, {"_id": 0})
    
    if not user or not auth_service.verify_password(credentials.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    
    # Update last login
    await db.users.update_one(
        {"id": user["id"]},
        {"$set": {"last_login": datetime.now(timezone.utc).isoformat()}}
    )
    
    # Generate token
    token = auth_service.create_access_token(data={"sub": user["id"], "email": user["email"]})
    
    return TokenResponse(
        access_token=token,
        user=UserResponse(
            id=user["id"],
            email=user["email"],
            full_name=user["full_name"],
            is_admin=user.get("is_admin", False)
        )
    )

@api_router.get("/auth/me", response_model=UserResponse)
async def get_current_user_info(current_user: dict = Depends(get_current_user)):
    """Get current user information"""
    return UserResponse(
        id=current_user["id"],
        email=current_user["email"],
        full_name=current_user["full_name"],
        is_admin=current_user.get("is_admin", False)
    )

# User Profile Routes
@api_router.get("/profile", response_model=UserProfile)
async def get_user_profile(current_user: dict = Depends(get_current_user)):
    """Get user profile and preferences"""
    profile = await db.user_profiles.find_one({"user_id": current_user["id"]}, {"_id": 0})
    
    if not profile:
        # Create profile if doesn't exist
        profile = UserProfile(user_id=current_user["id"])
        profile_dict = profile.model_dump()
        profile_dict = serialize_datetime(profile_dict)
        await db.user_profiles.insert_one(profile_dict)
        return profile
    
    deserialize_datetime(profile, ["created_at", "updated_at"])
    return profile

@api_router.put("/profile", response_model=UserProfile)
async def update_user_profile(
    profile_update: UserProfileUpdate,
    current_user: dict = Depends(get_current_user)
):
    """Update user profile and preferences"""
    update_data = {k: v for k, v in profile_update.model_dump().items() if v is not None}
    update_data["updated_at"] = datetime.now(timezone.utc)
    update_data = serialize_datetime(update_data)
    
    await db.user_profiles.update_one(
        {"user_id": current_user["id"]},
        {"$set": update_data}
    )
    
    profile = await db.user_profiles.find_one({"user_id": current_user["id"]}, {"_id": 0})
    deserialize_datetime(profile, ["created_at", "updated_at"])
    return profile

@api_router.post("/profile/complete-kyc")
async def complete_kyc(
    current_user: dict = Depends(get_current_user)
):
    """Mark KYC as completed and calculate tier"""
    profile = await db.user_profiles.find_one({"user_id": current_user["id"]}, {"_id": 0})
    
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    # Convert to UserProfile model
    profile_obj = UserProfile(**profile)
    profile_obj.kyc_completed = True
    
    # Calculate tier
    tier = calculate_user_tier(profile_obj)
    
    # Update database
    await db.user_profiles.update_one(
        {"user_id": current_user["id"]},
        {
            "$set": {
                "kyc_completed": True,
                "tier": tier,
                "updated_at": datetime.now(timezone.utc)
            }
        }
    )
    
    return {"message": "KYC completed", "tier": tier}

@api_router.get("/profile/tier-status")
async def get_tier_status(current_user: dict = Depends(get_current_user)):
    """Get user tier and KYC status"""
    profile = await db.user_profiles.find_one({"user_id": current_user["id"]}, {"_id": 0})
    
    if not profile:
        return {
            "tier": 0,
            "kyc_completed": False,
            "message": "Hey! Fill out your profile for the most accurate details and best available rates"
        }
    
    tier = profile.get("tier", 0)
    kyc_completed = profile.get("kyc_completed", False)
    
    tier_messages = {
        0: "Hey! Fill out your KYC form for the most accurate details and best available rates",
        1: "Basic profile complete! Add more details to unlock better rates",
        2: "Enhanced profile! You're getting great rates",
        3: "VIP status! You have access to our best rates and exclusive offers"
    }
    
    return {
        "tier": tier,
        "kyc_completed": kyc_completed,
        "message": tier_messages.get(tier, tier_messages[0])
    }

# GDPR Compliance Routes
@api_router.get("/privacy/settings")
async def get_privacy_settings(current_user: dict = Depends(get_current_user)):
    """Get user's privacy settings"""
    settings = await db.privacy_settings.find_one({"user_id": current_user["id"]}, {"_id": 0})
    
    if not settings:
        # Return default settings
        return {
            "user_id": current_user["id"],
            "marketing_emails": False,
            "analytics_tracking": True,
            "cookie_consent": False,
            "data_sharing": False,
            "updated_at": datetime.now(timezone.utc).isoformat()
        }
    
    deserialize_datetime(settings, ["updated_at"])
    return settings

@api_router.put("/privacy/settings")
async def update_privacy_settings(
    settings: PrivacySettings,
    current_user: dict = Depends(get_current_user)
):
    """Update user's privacy settings (GDPR compliance)"""
    settings.user_id = current_user["id"]
    settings.updated_at = datetime.now(timezone.utc)
    
    await db.privacy_settings.update_one(
        {"user_id": current_user["id"]},
        {"$set": serialize_datetime(settings.model_dump())},
        upsert=True
    )
    
    # Log consent change
    consent_log = {
        "id": str(uuid.uuid4()),
        "user_id": current_user["id"],
        "settings_update": settings.model_dump(),
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
    await db.consent_logs.insert_one(serialize_datetime(consent_log))
    
    return {"message": "Privacy settings updated successfully"}

@api_router.post("/privacy/export-data")
async def request_data_export(current_user: dict = Depends(get_current_user)):
    """Request data export (GDPR Article 20 - Right to data portability)"""
    
    # Collect all user data
    user_data = {
        "user": await db.users.find_one({"id": current_user["id"]}, {"_id": 0, "password": 0}),
        "profile": await db.user_profiles.find_one({"user_id": current_user["id"]}, {"_id": 0}),
        "inquiries": await db.inquiries.find({"email": current_user["email"]}, {"_id": 0}).to_list(1000),
        "privacy_settings": await db.privacy_settings.find_one({"user_id": current_user["id"]}, {"_id": 0}),
        "export_date": datetime.now(timezone.utc).isoformat()
    }
    
    # Create export request record
    export_request = DataExportRequest(
        user_id=current_user["id"],
        email=current_user["email"],
        status="completed",
        export_data=user_data,
        completed_at=datetime.now(timezone.utc)
    )
    
    await db.data_export_requests.insert_one(serialize_datetime(export_request.model_dump()))
    
    return {
        "message": "Data export completed",
        "data": user_data,
        "export_id": export_request.id
    }

@api_router.post("/privacy/delete-account")
async def request_account_deletion(
    reason: Optional[str] = None,
    current_user: dict = Depends(get_current_user)
):
    """Request account deletion (GDPR Article 17 - Right to be forgotten)"""
    
    # Create deletion request
    deletion_request = DataDeletionRequest(
        user_id=current_user["id"],
        email=current_user["email"],
        reason=reason,
        status="pending"
    )
    
    await db.data_deletion_requests.insert_one(serialize_datetime(deletion_request.model_dump()))
    
    return {
        "message": "Account deletion request received. We will process this within 30 days as required by GDPR.",
        "request_id": deletion_request.id,
        "note": "You can cancel this request within 7 days by contacting support."
    }

@api_router.delete("/privacy/delete-account/confirm/{request_id}")
async def confirm_account_deletion(
    request_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Permanently delete user account and data (Admin or user after review period)"""
    
    request = await db.data_deletion_requests.find_one({"id": request_id, "user_id": current_user["id"]})
    
    if not request:
        raise HTTPException(status_code=404, detail="Deletion request not found")
    
    if request["status"] != "pending":
        raise HTTPException(status_code=400, detail="Request already processed")
    
    # Anonymize user data (GDPR compliance - retain for legal purposes but anonymize)
    from encryption_utils import anonymize_email
    
    anonymized_email = anonymize_email(current_user["email"])
    
    # Update user to anonymized state
    await db.users.update_one(
        {"id": current_user["id"]},
        {
            "$set": {
                "email": anonymized_email,
                "full_name": "Deleted User",
                "deleted_at": datetime.now(timezone.utc).isoformat()
            }
        }
    )
    
    # Delete or anonymize profile
    await db.user_profiles.delete_one({"user_id": current_user["id"]})
    
    # Anonymize inquiries (keep for business records but remove PII)
    await db.inquiries.update_many(
        {"email": current_user["email"]},
        {
            "$set": {
                "email": anonymized_email,
                "name": "Deleted User",
                "phone": "[DELETED]"
            }
        }
    )
    
    # Update deletion request
    await db.data_deletion_requests.update_one(
        {"id": request_id},
        {
            "$set": {
                "status": "completed",
                "completed_at": datetime.now(timezone.utc).isoformat()
            }
        }
    )
    
    return {"message": "Account successfully deleted"}

# AI Chat Routes
@api_router.post("/ai/chat", response_model=ChatResponse)
async def chat_with_ai(
    chat_message: ChatMessage,
    current_user: dict = Depends(get_current_user)
):
    """Chat with AI assistant"""
    # Get user profile for context
    profile = await db.user_profiles.find_one({"user_id": current_user["id"]}, {"_id": 0})
    if not profile:
        profile = {"preferences": {}, "conversation_summary": "", "conversation_history": []}
    
    # Get available destinations for context
    destinations = await db.destinations.find({"published": True}, {"_id": 0}).to_list(100)
    
    # Get conversation history
    conversation_history = profile.get("conversation_history", [])
    
    # Chat with AI
    response = await ai_service.chat_with_context(
        user_message=chat_message.message,
        user_profile={
            "name": current_user.get("full_name", "Guest"),
            **profile.get("preferences", {})
        },
        conversation_history=conversation_history,
        available_destinations=destinations
    )
    
    # Append to conversation history
    conversation_history.append({
        "role": "user",
        "content": chat_message.message,
        "timestamp": datetime.now(timezone.utc).isoformat()
    })
    conversation_history.append({
        "role": "assistant",
        "content": response,
        "timestamp": datetime.now(timezone.utc).isoformat()
    })
    
    # Update profile with new conversation history
    await db.user_profiles.update_one(
        {"user_id": current_user["id"]},
        {"$set": {"conversation_history": conversation_history}}
    )
    
    # If conversation is long (>20 messages), summarize and clear
    if len(conversation_history) > 20:
        summary = await ai_service.summarize_conversation(conversation_history)
        await db.user_profiles.update_one(
            {"user_id": current_user["id"]},
            {
                "$set": {
                    "conversation_summary": summary,
                    "conversation_history": []
                }
            }
        )
    
    return ChatResponse(response=response)

# AI Recommendations Route
@api_router.get("/ai/recommendations", response_model=RecommendationResponse)
async def get_ai_recommendations(current_user: dict = Depends(get_current_user)):
    """Get personalized AI recommendations based on user tier"""
    # Get user profile
    profile = await db.user_profiles.find_one({"user_id": current_user["id"]}, {"_id": 0})
    if not profile:
        profile = {"preferences": {}, "conversation_summary": "", "tier": 0, "kyc_completed": False}
    
    tier = profile.get("tier", 0)
    kyc_completed = profile.get("kyc_completed", False)
    
    # If tier 0 (no KYC), return message to complete profile
    if tier == 0 or not kyc_completed:
        return RecommendationResponse(recommendations=[{
            "destination_name": "Complete Your Profile",
            "reason": "Fill out your KYC form to unlock personalized recommendations and best available rates!",
            "match_score": 0,
            "highlight": "🌟 Get started now",
            "is_kyc_prompt": True
        }])
    
    # Get all destinations
    destinations = await db.destinations.find({"published": True}, {"_id": 0}).to_list(1000)
    
    # Get recent additions (last 30 days)
    thirty_days_ago = datetime.now(timezone.utc) - timedelta(days=30)
    recent = await db.destinations.find({
        "published": True,
        "created_at": {"$gte": thirty_days_ago.isoformat()}
    }, {"_id": 0}).to_list(100)
    
    # Generate recommendations with tier context
    recommendations = await ai_service.generate_recommendations(
        user_profile={
            "name": current_user.get("full_name", "Guest"),
            **profile.get("preferences", {}),
            "conversation_summary": profile.get("conversation_summary", ""),
            "past_inquiries": profile.get("past_inquiries", []),
            "tier": tier
        },
        available_destinations=destinations,
        recent_additions=recent
    )
    
    return RecommendationResponse(recommendations=recommendations)

# File Upload & Storage Routes
@api_router.post("/files/upload", response_model=FileUploadResponse)
async def upload_file(
    file: UploadFile = File(...),
    category: str = Form(...),
    current_user: dict = Depends(get_current_user)
):
    """Upload file to S3 storage with security validation"""
    
    # Validate category
    allowed_categories = [
        'destination-images', 'user-profiles', 'kyc-documents', 
        'admin-content', 'gdpr-exports', 'generated-reports'
    ]
    
    if category not in allowed_categories:
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid category. Allowed: {', '.join(allowed_categories)}"
        )
    
    # Admin-only categories
    admin_categories = ['admin-content', 'destination-images']
    if category in admin_categories and not current_user.get("is_admin", False):
        raise HTTPException(status_code=403, detail="Admin access required for this category")
    
    try:
        result = await s3_service.upload_file(
            file=file,
            category=category,
            user_id=current_user["id"],
            metadata={
                'uploaded_by': current_user["email"],
                'user_name': current_user.get("full_name", "Unknown")
            }
        )
        return FileUploadResponse(**result)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

@api_router.get("/files/{file_key}/info", response_model=FileInfoResponse)
async def get_file_info(
    file_key: str,
    current_user: dict = Depends(get_current_user)
):
    """Get file information and metadata"""
    
    # Check if user can access this file (basic security check)
    if 'users/' in file_key and current_user["id"] not in file_key:
        if not current_user.get("is_admin", False):
            raise HTTPException(status_code=403, detail="Access denied")
    
    try:
        info = s3_service.get_file_info(file_key)
        return FileInfoResponse(**info)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get file info: {str(e)}")

@api_router.get("/files/{file_key}/download", response_model=PresignedUrlResponse)
async def get_download_url(
    file_key: str,
    expiration: int = Query(default=3600, description="URL expiration in seconds"),
    current_user: dict = Depends(get_current_user)
):
    """Generate presigned URL for secure file download"""
    
    # Validate expiration (max 7 days)
    if expiration > 604800:
        expiration = 604800
    
    # Check if user can access this file
    if 'users/' in file_key and current_user["id"] not in file_key:
        if not current_user.get("is_admin", False):
            raise HTTPException(status_code=403, detail="Access denied")
    
    try:
        presigned_url = s3_service.generate_presigned_url(file_key, expiration)
        return PresignedUrlResponse(
            presigned_url=presigned_url,
            expires_in=expiration
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate download URL: {str(e)}")

@api_router.delete("/files/{file_key}")
async def delete_file(
    file_key: str,
    current_user: dict = Depends(get_current_user)
):
    """Delete file from storage (with permission checks)"""
    
    # Check if user can delete this file
    if 'users/' in file_key and current_user["id"] not in file_key:
        if not current_user.get("is_admin", False):
            raise HTTPException(status_code=403, detail="Access denied")
    
    try:
        success = s3_service.delete_file(file_key, current_user["id"])
        if success:
            return {"message": "File deleted successfully", "file_key": file_key}
        else:
            raise HTTPException(status_code=500, detail="File deletion failed")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete file: {str(e)}")

@api_router.get("/files/list")
async def list_user_files(
    category: str = Query(..., description="File category to list"),
    current_user: dict = Depends(get_current_user)
):
    """List user's files by category"""
    
    # Admin can list any category, users only their own files
    if not current_user.get("is_admin", False):
        user_categories = ['user-profiles', 'kyc-documents', 'gdpr-exports']
        if category not in user_categories:
            raise HTTPException(
                status_code=403, 
                detail="Access denied to this file category"
            )
    
    try:
        prefix = s3_service.storage_categories.get(category, '')
        files = s3_service.list_files(prefix, current_user["id"])
        return {
            "category": category,
            "total_files": len(files),
            "files": files
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to list files: {str(e)}")

# GDPR Audit & Compliance Routes
@api_router.get("/audit/my-trail")
async def get_my_audit_trail(
    start_date: Optional[str] = Query(None, description="Start date (ISO format)"),
    end_date: Optional[str] = Query(None, description="End date (ISO format)"),
    action_types: Optional[str] = Query(None, description="Comma-separated action types"),
    limit: int = Query(100, description="Maximum entries to return"),
    current_user: dict = Depends(get_current_user)
):
    """Get user's own audit trail (GDPR Article 15 - Right of Access)"""
    
    # Parse date filters
    start_dt = None
    end_dt = None
    if start_date:
        try:
            start_dt = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
        except:
            raise HTTPException(status_code=400, detail="Invalid start_date format")
    
    if end_date:
        try:
            end_dt = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
        except:
            raise HTTPException(status_code=400, detail="Invalid end_date format")
    
    # Parse action types
    action_type_list = None
    if action_types:
        action_type_list = [AuditActionType(t.strip()) for t in action_types.split(',')]
    
    try:
        entries = await audit_logger.get_user_audit_trail(
            user_id=current_user["id"],
            start_date=start_dt,
            end_date=end_dt,
            action_types=action_type_list,
            limit=min(limit, 1000)  # Cap at 1000 for performance
        )
        
        return {
            "user_id": current_user["id"],
            "total_entries": len(entries),
            "entries": entries
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get audit trail: {str(e)}")

@api_router.get("/audit/gdpr-report")
async def get_gdpr_report(
    current_user: dict = Depends(get_current_user)
):
    """Generate comprehensive GDPR data processing report for user"""
    
    try:
        report = await audit_logger.generate_gdpr_report(current_user["id"])
        
        # Log the GDPR report generation
        await audit_logger.log_action(
            action_type=AuditActionType.GDPR_DATA_REQUEST,
            user_id=current_user["id"],
            user_email=current_user["email"],
            resource_type="gdpr_report",
            resource_id=current_user["id"],
            metadata={"report_type": "comprehensive_audit"},
            legal_basis="Article 15 - Right of Access"
        )
        
        return report
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate GDPR report: {str(e)}")

@api_router.get("/admin/audit/{user_id}")
async def get_user_audit_trail_admin(
    user_id: str,
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    limit: int = Query(100),
    current_user: dict = Depends(get_current_user)
):
    """Get audit trail for any user (Admin only)"""
    
    if not current_user.get("is_admin", False):
        raise HTTPException(status_code=403, detail="Admin access required")
    
    # Log admin access to user audit trail
    await audit_logger.log_action(
        action_type=AuditActionType.ADMIN_ACCESS,
        user_id=current_user["id"],
        user_email=current_user["email"],
        resource_type="user_audit_trail",
        resource_id=user_id,
        metadata={"accessed_user_id": user_id},
        legal_basis="Legitimate interest - Security monitoring"
    )
    
    # Parse dates
    start_dt = None
    end_dt = None
    if start_date:
        try:
            start_dt = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
        except:
            raise HTTPException(status_code=400, detail="Invalid start_date format")
    
    if end_date:
        try:
            end_dt = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
        except:
            raise HTTPException(status_code=400, detail="Invalid end_date format")
    
    try:
        entries = await audit_logger.get_user_audit_trail(
            user_id=user_id,
            start_date=start_dt,
            end_date=end_dt,
            limit=min(limit, 1000)
        )
        
        return {
            "user_id": user_id,
            "accessed_by": current_user["email"],
            "total_entries": len(entries),
            "entries": entries
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get user audit trail: {str(e)}")

# AI Content Generation (Admin only)
@api_router.post("/ai/generate-destination")
async def generate_destination_content(
    request: DestinationAIRequest,
    current_user: dict = Depends(get_current_user)
):
    """AI Auto-fill destination content (Admin only)"""
    if not current_user.get("is_admin", False):
        raise HTTPException(status_code=403, detail="Admin access required")
    
    content = await ai_service.generate_destination_content(
        course_name=request.course_name,
        location=request.location,
        additional_info=request.additional_info
    )
    
    return content

# Destinations
@api_router.get("/destinations", response_model=List[Destination])
async def get_destinations(
    country: Optional[str] = None,
    featured: Optional[bool] = None,
    published: Optional[bool] = True
):
    query = {}
    if country:
        query["country"] = country
    if featured is not None:
        query["featured"] = featured
    if published is not None:
        query["published"] = published
    
    destinations = await db.destinations.find(query, {"_id": 0}).to_list(1000)
    for dest in destinations:
        deserialize_datetime(dest, ["created_at", "updated_at"])
    return destinations

@api_router.get("/destinations/{slug}", response_model=Destination)
async def get_destination(slug: str):
    dest = await db.destinations.find_one({"slug": slug}, {"_id": 0})
    if not dest:
        raise HTTPException(status_code=404, detail="Destination not found")
    deserialize_datetime(dest, ["created_at", "updated_at"])
    return dest

@api_router.post("/destinations", response_model=Destination)
async def create_destination(destination: DestinationCreate):
    dest_obj = Destination(**destination.model_dump())
    doc = dest_obj.model_dump()
    doc = serialize_datetime(doc)
    await db.destinations.insert_one(doc)
    return dest_obj

@api_router.put("/destinations/{dest_id}", response_model=Destination)
async def update_destination(dest_id: str, destination: DestinationUpdate):
    update_data = {k: v for k, v in destination.model_dump().items() if v is not None}
    update_data["updated_at"] = datetime.now(timezone.utc)
    update_data = serialize_datetime(update_data)
    
    result = await db.destinations.update_one(
        {"id": dest_id},
        {"$set": update_data}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Destination not found")
    
    dest = await db.destinations.find_one({"id": dest_id}, {"_id": 0})
    deserialize_datetime(dest, ["created_at", "updated_at"])
    return dest

@api_router.delete("/destinations/{dest_id}")
async def delete_destination(dest_id: str):
    result = await db.destinations.delete_one({"id": dest_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Destination not found")
    return {"message": "Destination deleted"}

# Articles
@api_router.get("/articles", response_model=List[Article])
async def get_articles(
    category: Optional[str] = None,
    published: Optional[bool] = True,
    featured: Optional[bool] = None
):
    query = {}
    if category:
        query["category"] = category
    if published is not None:
        query["published"] = published
    if featured:
        # Featured articles have featured_until date in the future
        query["featured_until"] = {"$gt": datetime.now(timezone.utc).isoformat()}
    
    articles = await db.articles.find(query, {"_id": 0}).sort("publish_date", -1).to_list(1000)
    for article in articles:
        deserialize_datetime(article, ["publish_date", "featured_until", "created_at", "updated_at"])
    return articles

@api_router.get("/articles/{slug}", response_model=Article)
async def get_article(slug: str):
    article = await db.articles.find_one({"slug": slug}, {"_id": 0})
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    deserialize_datetime(article, ["publish_date", "featured_until", "created_at", "updated_at"])
    return article

@api_router.post("/articles", response_model=Article)
async def create_article(article: ArticleCreate):
    article_obj = Article(**article.model_dump())
    doc = article_obj.model_dump()
    doc = serialize_datetime(doc)
    await db.articles.insert_one(doc)
    return article_obj

@api_router.put("/articles/{article_id}", response_model=Article)
async def update_article(article_id: str, article: ArticleUpdate):
    update_data = {k: v for k, v in article.model_dump().items() if v is not None}
    update_data["updated_at"] = datetime.now(timezone.utc)
    update_data = serialize_datetime(update_data)
    
    result = await db.articles.update_one(
        {"id": article_id},
        {"$set": update_data}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Article not found")
    
    article = await db.articles.find_one({"id": article_id}, {"_id": 0})
    deserialize_datetime(article, ["publish_date", "featured_until", "created_at", "updated_at"])
    return article

@api_router.delete("/articles/{article_id}")
async def delete_article(article_id: str):
    result = await db.articles.delete_one({"id": article_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Article not found")
    return {"message": "Article deleted"}

# Hero Carousel
@api_router.get("/hero", response_model=List[HeroCarousel])
async def get_hero_slides(active: Optional[bool] = True):
    query = {}
    if active is not None:
        query["active"] = active
    
    slides = await db.hero_carousel.find(query, {"_id": 0}).sort("order", 1).to_list(100)
    for slide in slides:
        deserialize_datetime(slide, ["created_at"])
    return slides

@api_router.post("/hero", response_model=HeroCarousel)
async def create_hero_slide(slide: HeroCarouselCreate):
    slide_obj = HeroCarousel(**slide.model_dump())
    doc = slide_obj.model_dump()
    doc = serialize_datetime(doc)
    await db.hero_carousel.insert_one(doc)
    return slide_obj

@api_router.put("/hero/{slide_id}", response_model=HeroCarousel)
async def update_hero_slide(slide_id: str, slide: HeroCarouselUpdate):
    update_data = {k: v for k, v in slide.model_dump().items() if v is not None}
    update_data = serialize_datetime(update_data)
    
    result = await db.hero_carousel.update_one(
        {"id": slide_id},
        {"$set": update_data}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Hero slide not found")
    
    slide = await db.hero_carousel.find_one({"id": slide_id}, {"_id": 0})
    deserialize_datetime(slide, ["created_at"])
    return slide

@api_router.delete("/hero/{slide_id}")
async def delete_hero_slide(slide_id: str):
    result = await db.hero_carousel.delete_one({"id": slide_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Hero slide not found")
    return {"message": "Hero slide deleted"}

# Testimonials
@api_router.get("/testimonials", response_model=List[Testimonial])
async def get_testimonials(published: Optional[bool] = True):
    query = {}
    if published is not None:
        query["published"] = published
    
    testimonials = await db.testimonials.find(query, {"_id": 0}).sort("created_at", -1).to_list(1000)
    for testimonial in testimonials:
        deserialize_datetime(testimonial, ["created_at"])
    return testimonials

@api_router.post("/testimonials", response_model=Testimonial)
async def create_testimonial(testimonial: TestimonialCreate):
    testimonial_obj = Testimonial(**testimonial.model_dump())
    doc = testimonial_obj.model_dump()
    doc = serialize_datetime(doc)
    await db.testimonials.insert_one(doc)
    return testimonial_obj

@api_router.put("/testimonials/{testimonial_id}", response_model=Testimonial)
async def update_testimonial(testimonial_id: str, testimonial: TestimonialUpdate):
    update_data = {k: v for k, v in testimonial.model_dump().items() if v is not None}
    update_data = serialize_datetime(update_data)
    
    result = await db.testimonials.update_one(
        {"id": testimonial_id},
        {"$set": update_data}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Testimonial not found")
    
    testimonial = await db.testimonials.find_one({"id": testimonial_id}, {"_id": 0})
    deserialize_datetime(testimonial, ["created_at"])
    return testimonial

@api_router.delete("/testimonials/{testimonial_id}")
async def delete_testimonial(testimonial_id: str):
    result = await db.testimonials.delete_one({"id": testimonial_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Testimonial not found")
    return {"message": "Testimonial deleted"}

# Partners
@api_router.get("/partners", response_model=List[Partner])
async def get_partners(active: Optional[bool] = True):
    query = {}
    if active is not None:
        query["active"] = active
    
    partners = await db.partners.find(query, {"_id": 0}).sort("order", 1).to_list(1000)
    return partners

@api_router.post("/partners", response_model=Partner)
async def create_partner(partner: PartnerCreate):
    partner_obj = Partner(**partner.model_dump())
    doc = partner_obj.model_dump()
    await db.partners.insert_one(doc)
    return partner_obj

@api_router.put("/partners/{partner_id}", response_model=Partner)
async def update_partner(partner_id: str, partner: PartnerUpdate):
    update_data = {k: v for k, v in partner.model_dump().items() if v is not None}
    
    result = await db.partners.update_one(
        {"id": partner_id},
        {"$set": update_data}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Partner not found")
    
    partner = await db.partners.find_one({"id": partner_id}, {"_id": 0})
    return partner

@api_router.delete("/partners/{partner_id}")
async def delete_partner(partner_id: str):
    result = await db.partners.delete_one({"id": partner_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Partner not found")
    return {"message": "Partner deleted"}

# Inquiries
@api_router.get("/inquiries", response_model=List[Inquiry])
async def get_inquiries(
    status: Optional[str] = None,
    current_user: dict = Depends(get_current_user)
):
    """Get user's own inquiries or all inquiries if admin"""
    query = {}
    
    # Non-admin users can only see their own inquiries
    if not current_user.get("is_admin", False):
        query["email"] = current_user.get("email")
    
    if status:
        query["status"] = status
    
    inquiries = await db.inquiries.find(query, {"_id": 0}).sort("created_at", -1).to_list(1000)
    for inquiry in inquiries:
        deserialize_datetime(inquiry, ["created_at", "updated_at"])
        for note in inquiry.get("notes", []):
            if isinstance(note, dict) and "created_at" in note:
                deserialize_datetime(note, ["created_at"])
    return inquiries

@api_router.get("/inquiries/{inquiry_id}", response_model=Inquiry)
async def get_inquiry(inquiry_id: str):
    inquiry = await db.inquiries.find_one({"id": inquiry_id}, {"_id": 0})
    if not inquiry:
        raise HTTPException(status_code=404, detail="Inquiry not found")
    deserialize_datetime(inquiry, ["created_at", "updated_at"])
    for note in inquiry.get("notes", []):
        if isinstance(note, dict) and "created_at" in note:
            deserialize_datetime(note, ["created_at"])
    return inquiry

@api_router.post("/inquiries", response_model=Inquiry)
async def create_inquiry(inquiry: InquiryCreate):
    inquiry_obj = Inquiry(**inquiry.model_dump())
    doc = inquiry_obj.model_dump()
    doc = serialize_datetime(doc)
    await db.inquiries.insert_one(doc)
    return inquiry_obj

@api_router.put("/inquiries/{inquiry_id}", response_model=Inquiry)
async def update_inquiry_status(inquiry_id: str, inquiry: InquiryUpdate):
    update_data = {k: v for k, v in inquiry.model_dump().items() if v is not None}
    update_data["updated_at"] = datetime.now(timezone.utc)
    update_data = serialize_datetime(update_data)
    
    result = await db.inquiries.update_one(
        {"id": inquiry_id},
        {"$set": update_data}
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Inquiry not found")
    
    inquiry = await db.inquiries.find_one({"id": inquiry_id}, {"_id": 0})
    deserialize_datetime(inquiry, ["created_at", "updated_at"])
    for note in inquiry.get("notes", []):
        if isinstance(note, dict) and "created_at" in note:
            deserialize_datetime(note, ["created_at"])
    return inquiry

@api_router.post("/inquiries/{inquiry_id}/notes", response_model=Inquiry)
async def add_inquiry_note(inquiry_id: str, note_data: InquiryAddNote):
    note = InquiryNote(text=note_data.text)
    note_dict = note.model_dump()
    note_dict = serialize_datetime(note_dict)
    
    result = await db.inquiries.update_one(
        {"id": inquiry_id},
        {
            "$push": {"notes": note_dict},
            "$set": {"updated_at": datetime.now(timezone.utc).isoformat()}
        }
    )
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Inquiry not found")
    
    inquiry = await db.inquiries.find_one({"id": inquiry_id}, {"_id": 0})
    deserialize_datetime(inquiry, ["created_at", "updated_at"])
    for note in inquiry.get("notes", []):
        if isinstance(note, dict) and "created_at" in note:
            deserialize_datetime(note, ["created_at"])
    return inquiry

@api_router.get("/inquiries/export/csv")
async def export_inquiries_csv():
    inquiries = await db.inquiries.find({}, {"_id": 0}).sort("created_at", -1).to_list(10000)
    
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=[
        "id", "name", "email", "phone", "destination_name", "dates", 
        "group_size", "budget", "message", "status", "created_at"
    ])
    writer.writeheader()
    
    for inquiry in inquiries:
        writer.writerow({
            "id": inquiry.get("id", ""),
            "name": inquiry.get("name", ""),
            "email": inquiry.get("email", ""),
            "phone": inquiry.get("phone", ""),
            "destination_name": inquiry.get("destination_name", ""),
            "dates": inquiry.get("dates", ""),
            "group_size": inquiry.get("group_size", ""),
            "budget": inquiry.get("budget", ""),
            "message": inquiry.get("message", ""),
            "status": inquiry.get("status", ""),
            "created_at": inquiry.get("created_at", "")
        })
    
    output.seek(0)
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=inquiries.csv"}
    )

# Instagram Mock
@api_router.get("/instagram/latest")
async def get_instagram_posts():
    # Mock Instagram posts
    return [
        {
            "id": "1",
            "caption": "Experience the stunning fairways of Costa del Sol 🏌️‍♂️",
            "media_url": "https://images.unsplash.com/photo-1683836018144-6e5f398102de?w=400",
            "permalink": "https://instagram.com/p/mock1",
            "timestamp": datetime.now(timezone.utc).isoformat()
        },
        {
            "id": "2",
            "caption": "Sunset rounds at Portugal's finest courses ⛳",
            "media_url": "https://images.unsplash.com/photo-1602798416092-03afbccf616a?w=400",
            "permalink": "https://instagram.com/p/mock2",
            "timestamp": (datetime.now(timezone.utc) - timedelta(days=2)).isoformat()
        },
        {
            "id": "3",
            "caption": "Turkish golf paradise awaits 🌴",
            "media_url": "https://images.unsplash.com/photo-1668890966028-889d8f67f2b1?w=400",
            "permalink": "https://instagram.com/p/mock3",
            "timestamp": (datetime.now(timezone.utc) - timedelta(days=5)).isoformat()
        }
    ]

# Settings
@api_router.get("/settings/{key}", response_model=Setting)
async def get_setting(key: str):
    setting = await db.settings.find_one({"key": key}, {"_id": 0})
    if not setting:
        raise HTTPException(status_code=404, detail="Setting not found")
    return setting

@api_router.put("/settings/{key}", response_model=Setting)
async def update_setting(key: str, setting: SettingUpdate):
    result = await db.settings.update_one(
        {"key": key},
        {"$set": {"value": setting.value}},
        upsert=True
    )
    
    setting = await db.settings.find_one({"key": key}, {"_id": 0})
    return setting

# SEO - Sitemap
@api_router.get("/sitemap.xml", response_class=PlainTextResponse)
async def get_sitemap():
    base_url = "https://golf-ai-advisor.preview.emergentagent.com"
    
    # Static pages
    urls = [
        f"<url><loc>{base_url}/</loc><priority>1.0</priority></url>",
        f"<url><loc>{base_url}/destinations</loc><priority>0.9</priority></url>",
        f"<url><loc>{base_url}/articles</loc><priority>0.9</priority></url>",
        f"<url><loc>{base_url}/about</loc><priority>0.7</priority></url>",
        f"<url><loc>{base_url}/contact</loc><priority>0.8</priority></url>",
    ]
    
    # Dynamic destination pages
    destinations = await db.destinations.find({"published": True}, {"_id": 0, "slug": 1}).to_list(1000)
    for dest in destinations:
        urls.append(f"<url><loc>{base_url}/destinations/{dest['slug']}</loc><priority>0.8</priority></url>")
    
    # Dynamic article pages
    articles = await db.articles.find({"published": True}, {"_id": 0, "slug": 1}).to_list(1000)
    for article in articles:
        urls.append(f"<url><loc>{base_url}/articles/{article['slug']}</loc><priority>0.7</priority></url>")
    
    sitemap = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{"".join(urls)}
</urlset>"""
    
    return sitemap

# SEO - Robots
@api_router.get("/robots.txt", response_class=PlainTextResponse)
async def get_robots():
    return """User-agent: *
Allow: /
Sitemap: https://golf-ai-advisor.preview.emergentagent.com/api/sitemap.xml"""

# Seed Data
@api_router.post("/seed")
async def seed_database():
    """Populate database with sample data for demonstration"""
    
    # Clear existing data
    await db.destinations.delete_many({})
    await db.articles.delete_many({})
    await db.hero_carousel.delete_many({})
    await db.partners.delete_many({})
    await db.testimonials.delete_many({})
    
    # Clear users for fresh start (optional - comment out in production)
    # await db.users.delete_many({})
    # await db.user_profiles.delete_many({})
    
    # Seed Destinations
    destinations_data = [
        {
            "name": "Costa del Sol Golf Collection",
            "slug": "costa-del-sol",
            "country": "Spain",
            "region": "Andalusia",
            "short_desc": "Experience world-class golf on Spain's stunning southern coast",
            "long_desc": "Costa del Sol offers over 70 championship golf courses with year-round sunshine. Play legendary courses like Valderrama and enjoy Mediterranean luxury resorts with spa facilities, gourmet dining, and pristine beaches.",
            "price_from": 12500,
            "price_to": 28000,
            "currency": "SEK",
            "images": [
                "https://images.unsplash.com/photo-1683836018144-6e5f398102de?w=800",
                "https://images.unsplash.com/photo-1602798416092-03afbccf616a?w=800",
                "https://images.unsplash.com/photo-1668890966028-889d8f67f2b1?w=800"
            ],
            "highlights": ["70+ courses", "Year-round sunshine", "Championship venues", "Luxury resorts"],
            "featured": True,
            "published": True,
            "seo": {"title": "Costa del Sol Golf Holidays | Spain Golf Trips", "description": "Book your Costa del Sol golf holiday. 70+ courses, year-round sunshine, championship golf.", "canonical": "/destinations/costa-del-sol"}
        },
        {
            "name": "Algarve Golf Paradise",
            "slug": "algarve",
            "country": "Portugal",
            "region": "Algarve",
            "short_desc": "Portugal's premier golf destination with dramatic coastal courses",
            "long_desc": "The Algarve boasts 40+ world-class golf courses set against stunning Atlantic cliffs and golden beaches. Enjoy excellent value, superb cuisine, and warm Portuguese hospitality at award-winning resorts.",
            "price_from": 9800,
            "price_to": 22000,
            "currency": "SEK",
            "images": [
                "https://images.unsplash.com/photo-1605144884288-49eb7f9bb447?w=800",
                "https://images.unsplash.com/photo-1587174486073-ae5e5cff23aa?w=800"
            ],
            "highlights": ["40+ courses", "Dramatic cliffs", "Excellent value", "Award-winning resorts"],
            "featured": True,
            "published": True,
            "seo": {"title": "Algarve Golf Holidays Portugal | Golf Breaks", "description": "Algarve golf holidays with 40+ courses. Coastal golf paradise with great value.", "canonical": "/destinations/algarve"}
        },
        {
            "name": "Turkish Riviera Golf",
            "slug": "turkish-riviera",
            "country": "Turkey",
            "region": "Antalya",
            "short_desc": "Exceptional golf with all-inclusive luxury and ancient history",
            "long_desc": "Belek is Turkey's golf coast with stunning championship courses designed by legends like Nick Faldo and Colin Montgomerie. Enjoy all-inclusive 5-star resorts, pristine beaches, and explore ancient ruins between rounds.",
            "price_from": 11500,
            "price_to": 24000,
            "currency": "SEK",
            "images": [
                "https://images.unsplash.com/photo-1527004013197-933c4bb611b3?w=800"
            ],
            "highlights": ["Championship courses", "All-inclusive resorts", "Ancient history", "5-star luxury"],
            "featured": True,
            "published": True,
            "seo": {"title": "Turkey Golf Holidays | Belek Golf Breaks", "description": "Turkish Riviera golf with championship courses and all-inclusive luxury.", "canonical": "/destinations/turkish-riviera"}
        },
        {
            "name": "Scottish Highlands Golf",
            "slug": "scottish-highlands",
            "country": "Scotland",
            "region": "Highlands",
            "short_desc": "Play golf's ancient home with legendary links courses",
            "long_desc": "Experience authentic Scottish golf on historic links courses where the game was born. From St Andrews to Royal Dornoch, enjoy challenging coastal golf, whisky tastings, and Highland hospitality.",
            "price_from": 18000,
            "price_to": 35000,
            "currency": "SEK",
            "images": [
                "https://images.unsplash.com/photo-1587174486073-ae5e5cff23aa?w=800"
            ],
            "highlights": ["Historic links", "St Andrews", "Whisky tours", "Authentic experience"],
            "featured": True,
            "published": True,
            "seo": {"title": "Scotland Golf Holidays | Scottish Links Golf", "description": "Play Scotland's legendary links courses. St Andrews, Royal Dornoch & more.", "canonical": "/destinations/scottish-highlands"}
        },
        {
            "name": "Dubai Golf Experience",
            "slug": "dubai",
            "country": "UAE",
            "region": "Dubai",
            "short_desc": "Luxury desert golf with world-class hospitality",
            "long_desc": "Dubai offers championship golf courses amid stunning desert landscapes. Play Emirates Golf Club, address any course by Faldo or Norman, and enjoy ultra-luxury hotels, shopping, and dining.",
            "price_from": 22000,
            "price_to": 45000,
            "currency": "SEK",
            "images": [
                "https://images.unsplash.com/photo-1512453979798-5ea266f8880c?w=800"
            ],
            "highlights": ["Desert golf", "Ultra-luxury", "World-class dining", "Shopping paradise"],
            "featured": False,
            "published": True,
            "seo": {"title": "Dubai Golf Holidays | Luxury Golf UAE", "description": "Dubai golf holidays with championship desert courses and luxury hotels.", "canonical": "/destinations/dubai"}
        },
        {
            "name": "Mauritius Golf Island",
            "slug": "mauritius",
            "country": "Mauritius",
            "region": "Indian Ocean",
            "short_desc": "Tropical island paradise with stunning oceanfront golf",
            "long_desc": "Mauritius combines world-class golf with pristine beaches and crystal-clear waters. Play championship courses with Indian Ocean views, stay at luxury resorts, and enjoy Creole culture and cuisine.",
            "price_from": 28000,
            "price_to": 55000,
            "currency": "SEK",
            "images": [
                "https://images.unsplash.com/photo-1589895920112-b05c070f8273?w=800"
            ],
            "highlights": ["Ocean views", "Beach resorts", "Creole cuisine", "Tropical paradise"],
            "featured": False,
            "published": True,
            "seo": {"title": "Mauritius Golf Holidays | Indian Ocean Golf", "description": "Mauritius golf with ocean views and luxury beach resorts.", "canonical": "/destinations/mauritius"}
        },
        {
            "name": "Provence Golf & Wine",
            "slug": "provence",
            "country": "France",
            "region": "Provence",
            "short_desc": "Combine championship golf with French cuisine and wine",
            "long_desc": "Provence offers beautiful golf courses set among vineyards and lavender fields. Enjoy Michelin-star dining, world-class wine tours, and charming villages between rounds of golf.",
            "price_from": 16500,
            "price_to": 32000,
            "currency": "SEK",
            "images": [
                "https://images.unsplash.com/photo-1558973909-82e7cba37c2f?w=800"
            ],
            "highlights": ["Wine country", "Michelin dining", "Charming villages", "Lavender fields"],
            "featured": False,
            "published": True,
            "seo": {"title": "Provence Golf Holidays France | Wine & Golf", "description": "Provence golf with wine tours and French cuisine.", "canonical": "/destinations/provence"}
        },
        {
            "name": "Morocco Golf Adventure",
            "slug": "morocco",
            "country": "Morocco",
            "region": "Marrakech",
            "short_desc": "Exotic golf with stunning Atlas Mountain backdrops",
            "long_desc": "Morocco offers unique golf experiences with Atlas Mountain views. Play championship courses, explore vibrant souks, relax in traditional riads, and discover the magic of Marrakech.",
            "price_from": 13500,
            "price_to": 26000,
            "currency": "SEK",
            "images": [
                "https://images.unsplash.com/photo-1537984822441-cff330075342?w=800"
            ],
            "highlights": ["Atlas views", "Marrakech culture", "Exotic riads", "Adventure tours"],
            "featured": False,
            "published": True,
            "seo": {"title": "Morocco Golf Holidays | Marrakech Golf Trips", "description": "Morocco golf with Atlas Mountain views and Marrakech culture.", "canonical": "/destinations/morocco"}
        },
        {
            "name": "Irish Links Experience",
            "slug": "ireland",
            "country": "Ireland",
            "region": "West Coast",
            "short_desc": "Dramatic coastal links with legendary Irish hospitality",
            "long_desc": "Ireland's wild Atlantic coast offers some of the world's finest links golf. Play Ballybunion, Lahinch, and Doonbeg, then enjoy Irish pubs, traditional music, and warm hospitality.",
            "price_from": 17000,
            "price_to": 34000,
            "currency": "SEK",
            "images": [
                "https://images.unsplash.com/photo-1574192324001-ee41e18ed679?w=800"
            ],
            "highlights": ["Dramatic links", "Irish pubs", "Atlantic coast", "Traditional music"],
            "featured": False,
            "published": True,
            "seo": {"title": "Ireland Golf Holidays | Irish Links Golf", "description": "Irish links golf with dramatic coastal courses and warm hospitality.", "canonical": "/destinations/ireland"}
        },
        {
            "name": "Thailand Golf Escape",
            "slug": "thailand",
            "country": "Thailand",
            "region": "Phuket & Bangkok",
            "short_desc": "Tropical golf with exceptional value and Thai hospitality",
            "long_desc": "Thailand offers outstanding golf courses at incredible value. Play championship courses in Phuket or Bangkok, enjoy luxury spa resorts, Thai cuisine, and explore temples and beaches.",
            "price_from": 14500,
            "price_to": 27000,
            "currency": "SEK",
            "images": [
                "https://images.unsplash.com/photo-1552465011-b4e21bf6e79a?w=800"
            ],
            "highlights": ["Great value", "Spa resorts", "Thai cuisine", "Temple tours"],
            "featured": False,
            "published": True,
            "seo": {"title": "Thailand Golf Holidays | Phuket Golf Trips", "description": "Thailand golf with exceptional value and luxury resorts.", "canonical": "/destinations/thailand"}
        }
    ]
    
    for dest_data in destinations_data:
        dest_obj = Destination(**dest_data)
        doc = dest_obj.model_dump()
        doc = serialize_datetime(doc)
        await db.destinations.insert_one(doc)
    
    # Seed Articles
    articles_data = [
        {
            "title": "Top 10 Golf Courses in Spain for 2025",
            "slug": "top-10-golf-courses-spain-2025",
            "content": "Spain continues to be one of Europe's premier golf destinations. Here are our top picks for 2025...",
            "excerpt": "Discover the best golf courses Spain has to offer in 2025",
            "category": "Destinations",
            "author": "Golf Guy Editorial",
            "publish_date": datetime.now(timezone.utc),
            "featured_until": datetime.now(timezone.utc) + timedelta(days=30),
            "destination_ids": [],
            "image": "https://images.unsplash.com/photo-1683836018144-6e5f398102de?w=800",
            "published": True,
            "seo": {"title": "Top 10 Golf Courses in Spain 2025", "description": "Best golf courses in Spain for your 2025 golf holiday", "canonical": "/articles/top-10-golf-courses-spain-2025"}
        },
        {
            "title": "Algarve Golf Trip Report: 7 Days of Portuguese Paradise",
            "slug": "algarve-trip-report",
            "content": "Just returned from an incredible week playing golf in the Algarve. Here's our complete guide...",
            "excerpt": "A detailed trip report from a week of golf in Portugal's Algarve",
            "category": "Travel Reports",
            "author": "Mike Anderson",
            "publish_date": datetime.now(timezone.utc) - timedelta(days=5),
            "featured_until": datetime.now(timezone.utc) + timedelta(days=25),
            "destination_ids": [],
            "image": "https://images.unsplash.com/photo-1605144884288-49eb7f9bb447?w=800",
            "published": True,
            "seo": {"title": "Algarve Golf Trip Report", "description": "Complete trip report from 7 days of golf in Portugal's Algarve", "canonical": "/articles/algarve-trip-report"}
        },
        {
            "title": "Why Turkey Should Be Your Next Golf Destination",
            "slug": "why-turkey-golf-destination",
            "content": "Turkey's golf scene has exploded in recent years. Here's why Belek should be on your radar...",
            "excerpt": "Discover why Turkey is becoming a top golf destination",
            "category": "Destinations",
            "author": "Golf Guy Editorial",
            "publish_date": datetime.now(timezone.utc) - timedelta(days=12),
            "featured_until": datetime.now(timezone.utc) + timedelta(days=18),
            "destination_ids": [],
            "image": "https://images.unsplash.com/photo-1527004013197-933c4bb611b3?w=800",
            "published": True,
            "seo": {"title": "Why Turkey for Golf Holidays", "description": "Why Turkey should be your next golf destination", "canonical": "/articles/why-turkey-golf-destination"}
        },
        {
            "title": "Planning Your First Golf Trip: Complete Guide",
            "slug": "planning-first-golf-trip",
            "content": "Planning your first golf trip can seem overwhelming. We break down everything you need to know...",
            "excerpt": "Everything you need to know to plan your first golf vacation",
            "category": "Guides",
            "author": "Golf Guy Editorial",
            "publish_date": datetime.now(timezone.utc) - timedelta(days=20),
            "featured_until": None,
            "destination_ids": [],
            "image": "https://images.unsplash.com/photo-1587174486073-ae5e5cff23aa?w=800",
            "published": True,
            "seo": {"title": "Planning Your First Golf Trip Guide", "description": "Complete guide to planning your first golf vacation", "canonical": "/articles/planning-first-golf-trip"}
        },
        {
            "title": "Best Time to Visit Costa del Sol for Golf",
            "slug": "best-time-costa-del-sol",
            "content": "Wondering when to book your Costa del Sol golf trip? Here's our month-by-month breakdown...",
            "excerpt": "Month-by-month guide to the best time for golf in Costa del Sol",
            "category": "Guides",
            "author": "Golf Guy Editorial",
            "publish_date": datetime.now(timezone.utc) - timedelta(days=30),
            "featured_until": None,
            "destination_ids": [],
            "image": "https://images.unsplash.com/photo-1602798416092-03afbccf616a?w=800",
            "published": True,
            "seo": {"title": "Best Time for Costa del Sol Golf", "description": "When to visit Costa del Sol for the best golf experience", "canonical": "/articles/best-time-costa-del-sol"}
        }
    ]
    
    for article_data in articles_data:
        article_obj = Article(**article_data)
        doc = article_obj.model_dump()
        doc = serialize_datetime(doc)
        await db.articles.insert_one(doc)
    
    # Seed Hero Carousel
    hero_data = [
        {
            "title": "Discover Your Perfect Golf Escape",
            "subtitle": "From Spanish sunshine to Scottish links, we create unforgettable golf experiences",
            "kicker": "PREMIUM GOLF HOLIDAYS",
            "image": "https://images.unsplash.com/photo-1683836018144-6e5f398102de?w=1600",
            "destination_id": None,
            "cta_text": "Start Planning",
            "cta_url": "/contact",
            "order": 1,
            "active": True
        },
        {
            "title": "Costa del Sol Awaits",
            "subtitle": "70+ championship courses on Spain's stunning Mediterranean coast",
            "kicker": "SPAIN COLLECTION",
            "image": "https://images.unsplash.com/photo-1602798416092-03afbccf616a?w=1600",
            "destination_id": None,
            "cta_text": "View Packages",
            "cta_url": "/destinations/costa-del-sol",
            "order": 2,
            "active": True
        },
        {
            "title": "Algarve Golf Paradise",
            "subtitle": "Portugal's premier destination with dramatic coastal courses",
            "kicker": "PORTUGAL FEATURED",
            "image": "https://images.unsplash.com/photo-1605144884288-49eb7f9bb447?w=1600",
            "destination_id": None,
            "cta_text": "Explore Algarve",
            "cta_url": "/destinations/algarve",
            "order": 3,
            "active": True
        },
        {
            "title": "Turkish Riviera Luxury",
            "subtitle": "Championship golf with all-inclusive 5-star resorts",
            "kicker": "EXCEPTIONAL VALUE",
            "image": "https://images.unsplash.com/photo-1527004013197-933c4bb611b3?w=1600",
            "destination_id": None,
            "cta_text": "Discover Turkey",
            "cta_url": "/destinations/turkish-riviera",
            "order": 4,
            "active": True
        },
        {
            "title": "Scottish Links Tradition",
            "subtitle": "Play where golf began on historic championship links",
            "kicker": "AUTHENTIC SCOTLAND",
            "image": "https://images.unsplash.com/photo-1587174486073-ae5e5cff23aa?w=1600",
            "destination_id": None,
            "cta_text": "View Scotland",
            "cta_url": "/destinations/scottish-highlands",
            "order": 5,
            "active": True
        },
        {
            "title": "Custom Golf Experiences",
            "subtitle": "Tell us your dream trip and we'll make it happen",
            "kicker": "TAILORED FOR YOU",
            "image": "https://images.unsplash.com/photo-1668890966028-889d8f67f2b1?w=1600",
            "destination_id": None,
            "cta_text": "Get Custom Quote",
            "cta_url": "/contact",
            "order": 6,
            "active": True
        }
    ]
    
    for hero in hero_data:
        hero_obj = HeroCarousel(**hero)
        doc = hero_obj.model_dump()
        doc = serialize_datetime(doc)
        await db.hero_carousel.insert_one(doc)
    
    # Seed Partners
    partners_data = [
        {
            "name": "Eastern DGolf",
            "type": "insurance",
            "logo": "https://via.placeholder.com/150x60/2D5016/FFFFFF?text=Eastern+DGolf",
            "description": "Official travel insurance and guarantee partner",
            "url": "https://easterndgolf.com",
            "order": 1,
            "active": True
        },
        {
            "name": "Golf Foundation",
            "type": "charity",
            "logo": "https://via.placeholder.com/150x60/C8A951/FFFFFF?text=Golf+Foundation",
            "description": "Supporting youth golf development",
            "url": "https://golffoundation.org",
            "order": 2,
            "active": True
        },
        {
            "name": "IAGTO",
            "type": "membership",
            "logo": "https://via.placeholder.com/150x60/1E5B8C/FFFFFF?text=IAGTO",
            "description": "International Association of Golf Tour Operators member",
            "url": "https://iagto.com",
            "order": 3,
            "active": True
        }
    ]
    
    for partner_data in partners_data:
        partner_obj = Partner(**partner_data)
        doc = partner_obj.model_dump()
        await db.partners.insert_one(doc)
    
    # Seed Testimonials
    testimonials_data = [
        {
            "name": "Erik Johansson",
            "rating": 5,
            "content": "Absolutely fantastic experience! Golf Guy organized our Costa del Sol trip perfectly. Every detail was taken care of, from tee times to accommodation. Will definitely book again!",
            "destination_id": None,
            "trip_date": "October 2024",
            "published": True
        },
        {
            "name": "Anna Bergström",
            "rating": 5,
            "content": "The Algarve package exceeded all expectations. Beautiful courses, amazing weather, and excellent value. The team's knowledge and service were outstanding.",
            "destination_id": None,
            "trip_date": "September 2024",
            "published": True
        },
        {
            "name": "Lars Andersson",
            "rating": 5,
            "content": "Just returned from Turkey and what a trip! Championship courses, luxury resort, all-inclusive - perfect combination. Thank you Golf Guy for an unforgettable experience.",
            "destination_id": None,
            "trip_date": "November 2024",
            "published": True
        }
    ]
    
    for testimonial_data in testimonials_data:
        testimonial_obj = Testimonial(**testimonial_data)
        doc = testimonial_obj.model_dump()
        doc = serialize_datetime(doc)
        await db.testimonials.insert_one(doc)
    
    return {
        "message": "Database seeded successfully",
        "destinations": len(destinations_data),
        "articles": len(articles_data),
        "hero_slides": len(hero_data),
        "partners": len(partners_data),
        "testimonials": len(testimonials_data)
    }

# Seed Mock Users for Testing
@api_router.post("/seed-users")
async def seed_mock_users():
    """Create mock user profiles for admin testing"""
    
    mock_users_data = [
        {
            "email": "budget.golfer@test.com",
            "password": "password123",
            "full_name": "Budget Bob",
            "preferences": {
                "budget_min": 5000,
                "budget_max": 15000,
                "preferred_countries": ["Spain", "Portugal"],
                "playing_level": "Beginner",
                "accommodation_preference": "Budget",
                "trip_duration_days": 7,
                "group_size": 2
            },
            "conversation_summary": "Looking for affordable golf vacations in Spain or Portugal. Prefers value-for-money packages with basic accommodations."
        },
        {
            "email": "luxury.player@test.com",
            "password": "password123",
            "full_name": "Luxury Linda",
            "preferences": {
                "budget_min": 25000,
                "budget_max": 50000,
                "preferred_countries": ["Scotland", "Ireland", "France"],
                "playing_level": "Advanced",
                "accommodation_preference": "Luxury",
                "trip_duration_days": 10,
                "group_size": 4
            },
            "conversation_summary": "Interested in premium golf experiences with luxury resort stays. Enjoys historic courses and fine dining. Budget not a concern."
        },
        {
            "email": "family.vacation@test.com",
            "password": "password123",
            "full_name": "Family Frank",
            "preferences": {
                "budget_min": 15000,
                "budget_max": 30000,
                "preferred_countries": ["Turkey", "Morocco", "UAE"],
                "playing_level": "Intermediate",
                "accommodation_preference": "Mid-range",
                "trip_duration_days": 7,
                "group_size": 4
            },
            "conversation_summary": "Planning family golf vacation. Needs kid-friendly resorts with multiple amenities. Wife doesn't play golf, so resort activities important."
        },
        {
            "email": "corporate.group@test.com",
            "password": "password123",
            "full_name": "Corporate Carl",
            "preferences": {
                "budget_min": 20000,
                "budget_max": 40000,
                "preferred_countries": ["Spain", "Portugal", "Mauritius"],
                "playing_level": "Professional",
                "accommodation_preference": "Luxury",
                "trip_duration_days": 5,
                "group_size": 12
            },
            "conversation_summary": "Organizing corporate golf retreat. Needs conference facilities, premium courses, and team-building activities. Group of 12 executives."
        },
        {
            "email": "admin@golfguy.com",
            "password": "admin123",
            "full_name": "Admin User",
            "is_admin": True,
            "preferences": {
                "budget_min": 0,
                "budget_max": 100000,
                "preferred_countries": [],
                "playing_level": "Advanced",
                "accommodation_preference": "Any",
                "trip_duration_days": 7,
                "group_size": 1
            },
            "conversation_summary": "Admin account for testing and platform management."
        }
    ]
    
    created_users = []
    
    for user_data in mock_users_data:
        # Check if user exists
        existing = await db.users.find_one({"email": user_data["email"]})
        if existing:
            continue
        
        # Create user
        user = User(
            email=user_data["email"],
            hashed_password=auth_service.get_password_hash(user_data["password"]),
            full_name=user_data["full_name"],
            is_admin=user_data.get("is_admin", False)
        )
        
        user_dict = user.model_dump()
        user_dict = serialize_datetime(user_dict)
        await db.users.insert_one(user_dict)
        
        # Create user profile
        profile = UserProfile(
            user_id=user.id,
            preferences=UserPreferences(**user_data["preferences"]),
            conversation_summary=user_data["conversation_summary"]
        )
        
        profile_dict = profile.model_dump()
        profile_dict = serialize_datetime(profile_dict)
        await db.user_profiles.insert_one(profile_dict)
        
        created_users.append({
            "email": user.email,
            "full_name": user.full_name,
            "is_admin": user.is_admin
        })
    
    return {
        "message": "Mock users created successfully",
        "users": created_users,
        "count": len(created_users),
        "note": "Login with any email above using password: 'password123' (admin password: 'admin123')"
    }


# Include the router in the main app
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()