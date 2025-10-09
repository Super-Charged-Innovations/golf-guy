"""
Booking System Models
Core booking functionality for golf course reservations
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Dict, Any
from datetime import datetime, timezone, date, time
import uuid
from enum import Enum

class BookingStatus(str, Enum):
    """Booking status enumeration"""
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    COMPLETED = "completed"
    NO_SHOW = "no_show"

class PaymentStatus(str, Enum):
    """Payment status enumeration"""
    PENDING = "pending"
    AUTHORIZED = "authorized"
    CAPTURED = "captured"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"
    FAILED = "failed"

class BookingType(str, Enum):
    """Types of golf bookings"""
    ROUND = "round"           # Single round of golf
    PACKAGE = "package"       # Multi-day package
    LESSON = "lesson"         # Golf lesson
    TOURNAMENT = "tournament" # Tournament entry

class PlayerInfo(BaseModel):
    """Individual player information"""
    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    handicap: Optional[int] = None
    special_requirements: Optional[str] = None

class TimeSlot(BaseModel):
    """Available time slot for booking"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    destination_id: str
    date: date
    time: time
    available_slots: int
    total_slots: int
    price_per_player: int
    currency: str = "SEK"
    course_name: Optional[str] = None
    special_conditions: List[str] = []
    weather_forecast: Optional[str] = None

class BookingItem(BaseModel):
    """Individual booking item (can have multiple in one booking)"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    destination_id: str
    destination_name: str
    booking_type: BookingType
    date: date
    time: time
    duration_hours: int = 4  # Default golf round duration
    players: List[PlayerInfo]
    course_name: Optional[str] = None
    package_id: Optional[str] = None  # If booking a package
    price_per_player: int
    total_price: int
    currency: str = "SEK"
    special_requests: Optional[str] = None
    equipment_rental: List[str] = []  # Golf club rental, cart, etc.

class Booking(BaseModel):
    """Complete booking with payment and customer info"""
    model_config = ConfigDict(extra="ignore")
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: Optional[str] = None  # None for guest bookings
    booking_reference: str = Field(default_factory=lambda: f"GG{str(uuid.uuid4())[:8].upper()}")
    
    # Customer Information
    customer_name: str
    customer_email: str
    customer_phone: str
    customer_country: str = "Sweden"
    
    # Booking Details
    items: List[BookingItem]
    total_amount: int
    currency: str = "SEK"
    booking_date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    # Status
    status: BookingStatus = BookingStatus.PENDING
    payment_status: PaymentStatus = PaymentStatus.PENDING
    
    # Payment Information
    payment_method: Optional[str] = None  # stripe, paypal, klarna
    payment_id: Optional[str] = None      # External payment provider ID
    payment_details: Optional[Dict] = None
    
    # Additional Information
    source: str = "website"  # website, mobile, admin
    cancellation_reason: Optional[str] = None
    admin_notes: Optional[str] = None
    
    # Timestamps
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    confirmed_at: Optional[datetime] = None
    cancelled_at: Optional[datetime] = None

class BookingCreate(BaseModel):
    """Create new booking request"""
    customer_name: str
    customer_email: str
    customer_phone: str
    customer_country: str = "Sweden"
    items: List[BookingItem]
    payment_method: str = "stripe"
    special_requests: Optional[str] = None
    marketing_consent: bool = False

class BookingUpdate(BaseModel):
    """Update booking request"""
    status: Optional[BookingStatus] = None
    payment_status: Optional[PaymentStatus] = None
    customer_phone: Optional[str] = None
    special_requests: Optional[str] = None
    admin_notes: Optional[str] = None

class AvailabilityRequest(BaseModel):
    """Request to check availability"""
    destination_id: str
    date: date
    players: int = 1
    preferred_times: Optional[List[time]] = None

class AvailabilityResponse(BaseModel):
    """Available time slots response"""
    destination_id: str
    destination_name: str
    date: date
    available_slots: List[TimeSlot]
    fully_booked_times: List[time] = []
    weather_info: Optional[Dict] = None
    special_offers: List[str] = []

# Booking Analytics Models
class BookingStats(BaseModel):
    """Booking statistics for analytics"""
    total_bookings: int
    confirmed_bookings: int
    pending_bookings: int
    cancelled_bookings: int
    total_revenue: int
    currency: str = "SEK"
    average_booking_value: float
    popular_destinations: List[Dict]
    booking_trends: Dict

# Integration Models for External Booking APIs
class ExternalBookingProvider(BaseModel):
    """External golf course booking provider configuration"""
    provider_id: str
    provider_name: str
    api_endpoint: str
    api_key: str
    supported_destinations: List[str]
    booking_fee_percentage: float = 0.0
    cancellation_policy: str
    active: bool = True

class ExternalBookingRequest(BaseModel):
    """Request to external booking provider"""
    provider_id: str
    destination_id: str
    customer_info: Dict
    booking_details: Dict
    
class ExternalBookingResponse(BaseModel):
    """Response from external booking provider"""
    provider_id: str
    external_booking_id: str
    status: str
    confirmation_code: Optional[str] = None
    booking_details: Dict
    cancellation_policy: Optional[str] = None