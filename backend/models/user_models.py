"""
User-related data models
Defines all user, profile, and authentication models
"""
from pydantic import BaseModel, Field, ConfigDict, EmailStr
from typing import List, Optional, Dict, Any
from datetime import datetime, timezone
import uuid

# Base User Models
class User(BaseModel):
    """User account model"""
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
    """User creation model"""
    email: EmailStr
    password: str
    full_name: str

class UserLogin(BaseModel):
    """User login model"""
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    """User response model (no sensitive data)"""
    id: str
    email: EmailStr
    full_name: str
    is_admin: bool

class TokenResponse(BaseModel):
    """Authentication token response"""
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

# User Profile Models
class UserPreferences(BaseModel):
    """User travel preferences for recommendations"""
    
    # Basic preferences (Tier 1)
    budget_min: int = 0
    budget_max: int = 50000
    preferred_countries: List[str] = []
    playing_level: str = "Intermediate"  # Beginner, Intermediate, Advanced, Professional
    accommodation_preference: str = "Any"  # Luxury, Mid-range, Budget, Any
    trip_duration_days: Optional[int] = None
    group_size: Optional[int] = None
    
    # Enhanced KYC info (Tier 2-3)
    phone_number: Optional[str] = None
    travel_frequency: Optional[str] = None  # "First-time", "Annual", "Frequent"
    preferred_travel_months: List[str] = []
    dietary_requirements: Optional[str] = None
    special_requests: Optional[str] = None
    previous_golf_destinations: List[str] = []
    handicap: Optional[int] = None

class ConversationMessage(BaseModel):
    """AI conversation message"""
    role: str  # user or assistant
    content: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class UserProfile(BaseModel):
    """Complete user profile with preferences and AI data"""
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    preferences: UserPreferences = Field(default_factory=UserPreferences)
    conversation_summary: str = ""
    conversation_history: List[Dict] = []  # Temporary storage
    past_inquiries: List[str] = []  # Inquiry IDs
    kyc_notes: str = ""  # AI-generated KYC summary
    kyc_completed: bool = False
    tier: int = 0  # 0-3 based on profile completeness
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class UserProfileUpdate(BaseModel):
    """User profile update model"""
    preferences: Optional[UserPreferences] = None
    kyc_notes: Optional[str] = None

# GDPR Compliance Models
class ConsentRecord(BaseModel):
    """User consent record for GDPR compliance"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    consent_type: str  # marketing, analytics, cookies, data_processing
    granted: bool
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class DataExportRequest(BaseModel):
    """GDPR data export request"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    email: str
    status: str = "pending"  # pending, processing, completed, failed
    export_data: Optional[Dict] = None
    requested_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    completed_at: Optional[datetime] = None

class DataDeletionRequest(BaseModel):
    """GDPR data deletion request"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    email: str
    reason: Optional[str] = None
    status: str = "pending"  # pending, approved, processing, completed
    requested_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    completed_at: Optional[datetime] = None

class PrivacySettings(BaseModel):
    """User privacy settings"""
    user_id: str
    marketing_emails: bool = False
    analytics_tracking: bool = True
    cookie_consent: bool = False
    data_sharing: bool = False
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

# Utility Models
class UserTierStatus(BaseModel):
    """User tier status response"""
    user_id: str
    tier: int
    tier_name: str
    tier_description: str
    requirements_met: int
    total_requirements: int
    next_tier_requirements: List[str]
    benefits: List[str]

def calculate_user_tier(profile: UserProfile) -> int:
    """Calculate user tier based on profile completeness"""
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

def get_tier_info(tier: int) -> Dict[str, Any]:
    """Get tier information and benefits"""
    tier_info = {
        0: {
            "name": "New Member",
            "description": "Complete your profile to unlock personalized recommendations",
            "benefits": ["Basic destination browsing", "General recommendations"],
            "requirements": ["Complete KYC verification"]
        },
        1: {
            "name": "Explorer",
            "description": "Basic profile complete with travel preferences",
            "benefits": [
                "Personalized recommendations", 
                "Basic trip planning", 
                "Email support"
            ],
            "requirements": [
                "Set budget range", 
                "Choose preferred countries", 
                "Set playing level"
            ]
        },
        2: {
            "name": "Enthusiast",
            "description": "Enhanced profile with detailed travel preferences",
            "benefits": [
                "Priority recommendations",
                "Advanced filtering",
                "Phone support",
                "Early access to deals"
            ],
            "requirements": [
                "Add trip duration",
                "Set group size",
                "Provide phone number",
                "Set travel frequency"
            ]
        },
        3: {
            "name": "VIP Golfer",
            "description": "Complete profile with comprehensive travel history",
            "benefits": [
                "VIP recommendations",
                "Exclusive deals",
                "Personal travel consultant",
                "Priority booking",
                "Complimentary upgrades"
            ],
            "requirements": [
                "Set preferred travel months",
                "Add golf destinations history",
                "Provide handicap",
                "Complete at least one inquiry"
            ]
        }
    }
    
    return tier_info.get(tier, tier_info[0])