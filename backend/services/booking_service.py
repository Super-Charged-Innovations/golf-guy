"""
Booking Service
Handles golf course booking logic, availability checking, and reservation management
"""
import asyncio
from typing import List, Optional, Dict, Any
from datetime import datetime, timezone, date, time, timedelta
import logging
from core.database import get_database
from models.booking_models import (
    Booking, BookingCreate, BookingUpdate, BookingStatus, PaymentStatus,
    TimeSlot, AvailabilityRequest, AvailabilityResponse, BookingStats,
    ExternalBookingProvider, BookingItem
)
from services.audit_service import audit_logger, AuditActionType

logger = logging.getLogger(__name__)

class BookingService:
    """Service for managing golf bookings and availability"""
    
    def __init__(self):
        self.booking_providers = {}  # External booking provider integrations
        self.availability_cache = {}  # Cache for availability data
        
    async def check_availability(
        self, 
        request: AvailabilityRequest,
        db = None
    ) -> AvailabilityResponse:
        """
        Check availability for a destination on specific date
        """
        if not db:
            db = await get_database()
        
        try:
            # Get destination info
            destination = await db.destinations.find_one(
                {"id": request.destination_id}, 
                {"_id": 0}
            )
            
            if not destination:
                raise ValueError(f"Destination {request.destination_id} not found")
            
            # Generate available time slots (in real implementation, this would
            # integrate with golf course booking systems)
            available_slots = await self._generate_available_slots(
                request.destination_id,
                request.date,
                request.players,
                destination
            )
            
            # Check existing bookings to reduce availability
            booked_slots = await self._get_booked_slots(
                request.destination_id, 
                request.date,
                db
            )
            
            # Update availability based on existing bookings
            updated_slots = self._update_slot_availability(available_slots, booked_slots)
            
            # Get weather information (mock for now)
            weather_info = await self._get_weather_forecast(
                destination.get('location_coordinates'),
                request.date
            )
            
            return AvailabilityResponse(
                destination_id=request.destination_id,
                destination_name=destination['name'],
                date=request.date,
                available_slots=updated_slots,
                weather_info=weather_info,
                special_offers=self._get_special_offers(destination, request.date)
            )
            
        except Exception as e:
            logger.error(f"Error checking availability: {str(e)}")
            raise
    
    async def _generate_available_slots(
        self, 
        destination_id: str, 
        booking_date: date,
        players: int,
        destination: Dict
    ) -> List[TimeSlot]:
        """Generate available time slots for a destination"""
        
        slots = []
        
        # Standard golf course hours (7:00 AM to 6:00 PM)
        start_hour = 7
        end_hour = 18
        slot_interval = 15  # 15-minute intervals
        
        # Base price calculation based on destination
        base_price = destination.get('price_from', 500)  # SEK
        
        # Course information
        courses = destination.get('courses', [])
        course_name = courses[0].get('course_name', 'Main Course') if courses else 'Golf Course'
        
        current_time = time(start_hour, 0)
        end_time = time(end_hour, 0)
        
        while current_time < end_time:
            # Calculate dynamic pricing (peak hours cost more)
            price_multiplier = 1.0
            if 10 <= current_time.hour <= 15:  # Peak hours
                price_multiplier = 1.3
            elif current_time.hour < 9 or current_time.hour > 16:  # Off-peak
                price_multiplier = 0.8
            
            # Weekend pricing
            if booking_date.weekday() >= 5:  # Saturday/Sunday
                price_multiplier *= 1.2
            
            slot_price = int(base_price * price_multiplier)
            
            # Available slots (in real system, this would come from course management system)
            available_spots = 4  # Standard foursome
            
            slot = TimeSlot(
                destination_id=destination_id,
                date=booking_date,
                time=current_time,
                available_slots=available_spots,
                total_slots=available_spots,
                price_per_player=slot_price,
                currency="SEK",
                course_name=course_name,
                special_conditions=self._get_slot_conditions(current_time, booking_date)
            )
            
            slots.append(slot)
            
            # Move to next slot
            current_datetime = datetime.combine(booking_date, current_time)
            next_datetime = current_datetime + timedelta(minutes=slot_interval)
            current_time = next_datetime.time()
        
        return slots
    
    async def _get_booked_slots(
        self, 
        destination_id: str, 
        booking_date: date,
        db
    ) -> List[Dict]:
        """Get existing bookings for a destination and date"""
        
        bookings = await db.bookings.find({
            "items.destination_id": destination_id,
            "items.date": booking_date.isoformat(),
            "status": {"$in": [BookingStatus.CONFIRMED, BookingStatus.PENDING]}
        }, {"_id": 0}).to_list(None)
        
        booked_slots = []
        for booking in bookings:
            for item in booking.get('items', []):
                if item['destination_id'] == destination_id:
                    booked_slots.append({
                        'time': item['time'],
                        'players': len(item.get('players', []))
                    })
        
        return booked_slots
    
    def _update_slot_availability(
        self, 
        available_slots: List[TimeSlot], 
        booked_slots: List[Dict]
    ) -> List[TimeSlot]:
        """Update slot availability based on existing bookings"""
        
        # Create a mapping of booked times
        booked_by_time = {}
        for booking in booked_slots:
            time_str = booking['time']
            players = booking['players']
            if time_str not in booked_by_time:
                booked_by_time[time_str] = 0
            booked_by_time[time_str] += players
        
        # Update available slots
        updated_slots = []
        for slot in available_slots:
            time_str = slot.time.strftime('%H:%M:%S')
            booked_players = booked_by_time.get(time_str, 0)
            slot.available_slots = max(0, slot.total_slots - booked_players)
            
            # Only include slots with availability
            if slot.available_slots > 0:
                updated_slots.append(slot)
        
        return updated_slots
    
    def _get_slot_conditions(self, slot_time: time, booking_date: date) -> List[str]:
        """Get special conditions for a time slot"""
        conditions = []
        
        # Early morning conditions
        if slot_time.hour < 8:
            conditions.append("Early morning - dew on course")
        
        # Peak hour conditions
        if 10 <= slot_time.hour <= 15:
            conditions.append("Peak hours - premium pricing")
        
        # Weekend conditions
        if booking_date.weekday() >= 5:
            conditions.append("Weekend rates apply")
        
        return conditions
    
    async def _get_weather_forecast(
        self, 
        coordinates: Optional[Dict], 
        booking_date: date
    ) -> Optional[Dict]:
        """Get weather forecast for the location (mock implementation)"""
        
        # In real implementation, this would call weather API
        # Mock weather data
        return {
            "temperature": "18°C",
            "condition": "Partly cloudy",
            "wind": "Light breeze",
            "precipitation": "10%",
            "visibility": "Good"
        }
    
    def _get_special_offers(self, destination: Dict, booking_date: date) -> List[str]:
        """Get special offers for the destination and date"""
        offers = []
        
        # Weekday offers
        if booking_date.weekday() < 5:
            offers.append("Weekday Special: 15% off for bookings before 10 AM")
        
        # Group offers
        offers.append("Group Discount: Book 4+ players and save 10%")
        
        # Seasonal offers
        month = booking_date.month
        if month in [11, 12, 1, 2]:  # Winter months
            offers.append("Winter Golf: Special rates for brave players")
        
        return offers
    
    async def create_booking(
        self, 
        booking_data: BookingCreate,
        user_id: Optional[str] = None,
        db = None
    ) -> Booking:
        """Create a new booking"""
        
        if not db:
            db = await get_database()
        
        try:
            # Validate availability for all items
            for item in booking_data.items:
                availability = await self.check_availability(
                    AvailabilityRequest(
                        destination_id=item.destination_id,
                        date=item.date,
                        players=len(item.players)
                    ),
                    db
                )
                
                # Check if requested time is available
                requested_time = item.time
                available_slot = None
                for slot in availability.available_slots:
                    if slot.time == requested_time and slot.available_slots >= len(item.players):
                        available_slot = slot
                        break
                
                if not available_slot:
                    raise ValueError(f"Requested time {requested_time} not available for {item.destination_name}")
            
            # Calculate total amount
            total_amount = sum(item.total_price for item in booking_data.items)
            
            # Create booking object
            booking = Booking(
                user_id=user_id,
                customer_name=booking_data.customer_name,
                customer_email=booking_data.customer_email,
                customer_phone=booking_data.customer_phone,
                customer_country=booking_data.customer_country,
                items=booking_data.items,
                total_amount=total_amount,
                payment_method=booking_data.payment_method,
                status=BookingStatus.PENDING
            )
            
            # Store in database
            booking_dict = booking.model_dump()
            # Convert datetime fields to ISO strings
            booking_dict['created_at'] = booking_dict['created_at'].isoformat()
            booking_dict['updated_at'] = booking_dict['updated_at'].isoformat()
            
            # Convert dates and times in items
            for item in booking_dict['items']:
                if isinstance(item['date'], date):
                    item['date'] = item['date'].isoformat()
                if isinstance(item['time'], time):
                    item['time'] = item['time'].strftime('%H:%M:%S')
            
            await db.bookings.insert_one(booking_dict)
            
            # Log booking creation
            await audit_logger.log_action(
                action_type=AuditActionType.DATA_CREATE,
                user_id=user_id,
                user_email=booking_data.customer_email,
                resource_type="booking",
                resource_id=booking.id,
                metadata={
                    "booking_reference": booking.booking_reference,
                    "total_amount": total_amount,
                    "items_count": len(booking_data.items)
                },
                legal_basis="Contract performance"
            )
            
            logger.info(f"Booking created: {booking.booking_reference}")
            return booking
            
        except Exception as e:
            logger.error(f"Error creating booking: {str(e)}")
            raise
    
    async def get_booking(self, booking_id: str, db = None) -> Optional[Booking]:
        """Get booking by ID"""
        if not db:
            db = await get_database()
        
        booking_data = await db.bookings.find_one({"id": booking_id}, {"_id": 0})
        if not booking_data:
            return None
        
        # Convert ISO strings back to datetime objects
        if booking_data.get('created_at'):
            booking_data['created_at'] = datetime.fromisoformat(booking_data['created_at'])
        if booking_data.get('updated_at'):
            booking_data['updated_at'] = datetime.fromisoformat(booking_data['updated_at'])
        
        return Booking(**booking_data)
    
    async def update_booking(
        self, 
        booking_id: str, 
        update_data: BookingUpdate,
        db = None
    ) -> Optional[Booking]:
        """Update booking status and details"""
        if not db:
            db = await get_database()
        
        update_fields = {
            k: v for k, v in update_data.model_dump().items() 
            if v is not None
        }
        update_fields['updated_at'] = datetime.now(timezone.utc).isoformat()
        
        result = await db.bookings.update_one(
            {"id": booking_id},
            {"$set": update_fields}
        )
        
        if result.modified_count > 0:
            return await self.get_booking(booking_id, db)
        return None
    
    async def cancel_booking(
        self, 
        booking_id: str, 
        reason: str = "Customer request",
        db = None
    ) -> bool:
        """Cancel a booking"""
        if not db:
            db = await get_database()
        
        update_data = BookingUpdate(
            status=BookingStatus.CANCELLED,
            cancellation_reason=reason
        )
        
        result = await self.update_booking(booking_id, update_data, db)
        return result is not None
    
    async def get_user_bookings(
        self, 
        user_id: str,
        status: Optional[BookingStatus] = None,
        db = None
    ) -> List[Booking]:
        """Get all bookings for a user"""
        if not db:
            db = await get_database()
        
        query = {"user_id": user_id}
        if status:
            query["status"] = status
        
        bookings_data = await db.bookings.find(query, {"_id": 0}).to_list(None)
        
        bookings = []
        for booking_data in bookings_data:
            # Convert datetime fields
            if booking_data.get('created_at'):
                booking_data['created_at'] = datetime.fromisoformat(booking_data['created_at'])
            if booking_data.get('updated_at'):
                booking_data['updated_at'] = datetime.fromisoformat(booking_data['updated_at'])
            
            bookings.append(Booking(**booking_data))
        
        return bookings

# Global booking service instance
booking_service = BookingService()