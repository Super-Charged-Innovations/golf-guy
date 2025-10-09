"""
Payment Service using Stripe integration
Handles golf booking payments with security and compliance
"""
import os
import logging
from typing import Optional, Dict, Any, List
from datetime import datetime, timezone
from fastapi import HTTPException, Request
from pydantic import BaseModel
from emergentintegrations.payments.stripe.checkout import (
    StripeCheckout, CheckoutSessionResponse, CheckoutStatusResponse, CheckoutSessionRequest
)
from core.database import get_database
from services.audit_service import audit_logger, AuditActionType

logger = logging.getLogger(__name__)

class PaymentTransaction(BaseModel):
    """Payment transaction record"""
    id: str
    session_id: str
    user_id: Optional[str] = None
    user_email: Optional[str] = None
    booking_id: Optional[str] = None
    package_type: str
    amount: float
    currency: str = "SEK"
    payment_status: str = "pending"  # pending, paid, failed, cancelled, expired
    stripe_status: Optional[str] = None
    metadata: Dict[str, Any] = {}
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime] = None

class PaymentPackage(BaseModel):
    """Predefined payment packages for security"""
    id: str
    name: str
    description: str
    amount: float
    currency: str = "SEK"
    features: List[str] = []
    popular: bool = False
    booking_type: str = "round"  # round, package, lesson

class PaymentService:
    """Service for handling payments via Stripe"""
    
    def __init__(self):
        self.stripe_api_key = os.environ.get('STRIPE_API_KEY')
        if not self.stripe_api_key:
            logger.warning("STRIPE_API_KEY not configured - payments will be disabled")
        
        # Predefined packages for security (NEVER accept amounts from frontend)
        self.GOLF_PACKAGES = {
            "single_round": PaymentPackage(
                id="single_round",
                name="Single Round",
                description="18 holes of golf with cart",
                amount=850.0,
                currency="SEK",
                features=["18 holes", "Golf cart", "Scorecard"],
                popular=False,
                booking_type="round"
            ),
            "premium_round": PaymentPackage(
                id="premium_round", 
                name="Premium Round",
                description="18 holes with premium amenities",
                amount=1250.0,
                currency="SEK",
                features=["18 holes", "Golf cart", "Caddie service", "Refreshments"],
                popular=True,
                booking_type="round"
            ),
            "golf_lesson": PaymentPackage(
                id="golf_lesson",
                name="Golf Lesson",
                description="1-hour private golf lesson",
                amount=650.0,
                currency="SEK",
                features=["1-hour lesson", "Professional instructor", "Equipment provided"],
                popular=False,
                booking_type="lesson"
            ),
            "weekend_package": PaymentPackage(
                id="weekend_package",
                name="Weekend Golf Package",
                description="2 days of golf with accommodation",
                amount=2850.0,
                currency="SEK",
                features=["2 rounds of golf", "2 nights accommodation", "Breakfast", "Golf cart"],
                popular=True,
                booking_type="package"
            ),
            "luxury_package": PaymentPackage(
                id="luxury_package",
                name="Luxury Golf Experience",
                description="3-day luxury golf package",
                amount=5500.0,
                currency="SEK",
                features=[
                    "3 rounds on championship courses", 
                    "3 nights luxury accommodation",
                    "All meals included",
                    "Spa access",
                    "Airport transfers"
                ],
                popular=False,
                booking_type="package"
            )
        }
    
    def get_available_packages(self) -> List[PaymentPackage]:
        """Get all available payment packages"""
        return list(self.GOLF_PACKAGES.values())
    
    def get_package(self, package_id: str) -> Optional[PaymentPackage]:
        """Get specific payment package"""
        return self.GOLF_PACKAGES.get(package_id)
    
    async def create_checkout_session(
        self,
        package_id: str,
        origin_url: str,
        user_id: Optional[str] = None,
        user_email: Optional[str] = None,
        booking_id: Optional[str] = None,
        quantity: int = 1,
        metadata: Optional[Dict] = None
    ) -> CheckoutSessionResponse:
        """
        Create Stripe checkout session for golf package
        """
        
        if not self.stripe_api_key:
            raise HTTPException(status_code=500, detail="Payment system not configured")
        
        # Validate package
        package = self.get_package(package_id)
        if not package:
            raise HTTPException(status_code=400, detail=f"Invalid package: {package_id}")
        
        try:
            # Calculate total amount (server-side only for security)
            total_amount = package.amount * quantity
            
            # Create dynamic URLs using provided origin
            success_url = f"{origin_url}/booking/success?session_id={{CHECKOUT_SESSION_ID}}"
            cancel_url = f"{origin_url}/booking/cancel"
            
            # Prepare metadata
            session_metadata = {
                "package_id": package_id,
                "package_name": package.name,
                "quantity": str(quantity),
                "user_id": user_id or "guest",
                "booking_id": booking_id or "",
                "source": "golf_platform"
            }
            
            if metadata:
                session_metadata.update(metadata)
            
            # Initialize Stripe checkout
            stripe_checkout = StripeCheckout(
                api_key=self.stripe_api_key,
                webhook_url=f"{origin_url}/api/webhook/stripe"  # Will be called by Stripe
            )
            
            # Create checkout session request
            checkout_request = CheckoutSessionRequest(
                amount=total_amount,
                currency=package.currency.lower(),
                success_url=success_url,
                cancel_url=cancel_url,
                metadata=session_metadata
            )
            
            # Create session with Stripe
            session = await stripe_checkout.create_checkout_session(checkout_request)
            
            # Create payment transaction record
            db = await get_database()
            
            import uuid
            transaction_id = str(uuid.uuid4())
            
            transaction = PaymentTransaction(
                id=transaction_id,
                session_id=session.session_id,
                user_id=user_id,
                user_email=user_email,
                booking_id=booking_id,
                package_type=package_id,
                amount=total_amount,
                currency=package.currency,
                payment_status="pending",
                metadata=session_metadata,
                created_at=datetime.now(timezone.utc),
                updated_at=datetime.now(timezone.utc)
            )
            
            # Store transaction in database
            transaction_dict = transaction.model_dump()
            transaction_dict['created_at'] = transaction_dict['created_at'].isoformat()
            transaction_dict['updated_at'] = transaction_dict['updated_at'].isoformat()
            
            await db.payment_transactions.insert_one(transaction_dict)
            
            # Log payment initiation
            await audit_logger.log_action(
                action_type=AuditActionType.DATA_CREATE,
                user_id=user_id,
                user_email=user_email,
                resource_type="payment_transaction",
                resource_id=transaction_id,
                metadata={
                    "session_id": session.session_id,
                    "package_id": package_id,
                    "amount": total_amount,
                    "currency": package.currency
                },
                legal_basis="Contract performance"
            )
            
            logger.info(f"Payment session created: {session.session_id} for {total_amount} {package.currency}")
            
            return session
            
        except Exception as e:
            logger.error(f"Error creating checkout session: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Payment session creation failed: {str(e)}")
    
    async def get_payment_status(self, session_id: str) -> CheckoutStatusResponse:
        """Get payment status from Stripe and update local records"""
        
        if not self.stripe_api_key:
            raise HTTPException(status_code=500, detail="Payment system not configured")
        
        try:
            # Get status from Stripe
            stripe_checkout = StripeCheckout(
                api_key=self.stripe_api_key,
                webhook_url=""  # Not needed for status check
            )
            
            status = await stripe_checkout.get_checkout_status(session_id)
            
            # Update local transaction record
            await self._update_transaction_status(session_id, status)
            
            return status
            
        except Exception as e:
            logger.error(f"Error getting payment status: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Payment status check failed: {str(e)}")
    
    async def _update_transaction_status(
        self, 
        session_id: str, 
        status: CheckoutStatusResponse
    ) -> bool:
        """Update local payment transaction status"""
        
        try:
            db = await get_database()
            
            # Find existing transaction
            transaction = await db.payment_transactions.find_one(
                {"session_id": session_id},
                {"_id": 0}
            )
            
            if not transaction:
                logger.warning(f"No transaction found for session: {session_id}")
                return False
            
            # Prevent duplicate processing
            if transaction.get('payment_status') == 'paid':
                logger.info(f"Transaction already processed: {session_id}")
                return True
            
            # Update transaction status
            update_data = {
                "stripe_status": status.status,
                "payment_status": status.payment_status,
                "updated_at": datetime.now(timezone.utc).isoformat()
            }
            
            # Mark as completed if payment successful
            if status.payment_status == 'paid':
                update_data["completed_at"] = datetime.now(timezone.utc).isoformat()
                
                # Update booking status if booking_id exists
                booking_id = transaction.get('booking_id')
                if booking_id:
                    await db.bookings.update_one(
                        {"id": booking_id},
                        {"$set": {
                            "payment_status": "captured",
                            "status": "confirmed",
                            "payment_id": session_id,
                            "updated_at": datetime.now(timezone.utc).isoformat()
                        }}
                    )
                    
                    # Log booking confirmation
                    await audit_logger.log_action(
                        action_type=AuditActionType.DATA_UPDATE,
                        user_id=transaction.get('user_id'),
                        user_email=transaction.get('user_email'),
                        resource_type="booking",
                        resource_id=booking_id,
                        metadata={
                            "action": "payment_confirmed",
                            "amount": status.amount_total,
                            "session_id": session_id
                        },
                        legal_basis="Contract performance"
                    )
            
            # Update transaction
            result = await db.payment_transactions.update_one(
                {"session_id": session_id},
                {"$set": update_data}
            )
            
            # Log payment status update
            await audit_logger.log_action(
                action_type=AuditActionType.DATA_UPDATE,
                user_id=transaction.get('user_id'),
                user_email=transaction.get('user_email'),
                resource_type="payment_transaction",
                resource_id=transaction['id'],
                metadata={
                    "previous_status": transaction.get('payment_status'),
                    "new_status": status.payment_status,
                    "session_id": session_id
                },
                legal_basis="Contract performance"
            )
            
            return result.modified_count > 0
            
        except Exception as e:
            logger.error(f"Error updating transaction status: {str(e)}")
            return False
    
    async def handle_stripe_webhook(self, webhook_body: bytes, signature: str) -> Dict[str, Any]:
        """Handle Stripe webhook for payment events"""
        
        if not self.stripe_api_key:
            raise HTTPException(status_code=500, detail="Payment system not configured")
        
        try:
            # Initialize Stripe checkout for webhook handling
            stripe_checkout = StripeCheckout(
                api_key=self.stripe_api_key,
                webhook_url=""  # Not needed for webhook handling
            )
            
            # Process webhook
            webhook_response = await stripe_checkout.handle_webhook(webhook_body, signature)
            
            logger.info(f"Webhook processed: {webhook_response.event_type} for session {webhook_response.session_id}")
            
            # Update transaction based on webhook
            if webhook_response.session_id:
                # Get the latest status and update our records
                status = await self.get_payment_status(webhook_response.session_id)
                
                return {
                    "processed": True,
                    "event_type": webhook_response.event_type,
                    "session_id": webhook_response.session_id,
                    "payment_status": webhook_response.payment_status
                }
            
            return {"processed": True, "event_type": webhook_response.event_type}
            
        except Exception as e:
            logger.error(f"Error handling webhook: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Webhook processing failed: {str(e)}")
    
    async def get_user_transactions(
        self, 
        user_id: str,
        status: Optional[str] = None
    ) -> List[Dict]:
        """Get user's payment transactions"""
        
        try:
            db = await get_database()
            
            query = {"user_id": user_id}
            if status:
                query["payment_status"] = status
            
            transactions = await db.payment_transactions.find(
                query, 
                {"_id": 0}
            ).sort("created_at", -1).to_list(None)
            
            return transactions
            
        except Exception as e:
            logger.error(f"Error getting user transactions: {str(e)}")
            return []

# Global payment service instance
payment_service = PaymentService()