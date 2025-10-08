"""
Authentication API routes
Handles user registration, login, and authentication
"""
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime, timezone
from core.database import get_database
from services.auth_service import auth_service
from services.audit_service import audit_logger, AuditActionType
from models.user_models import User, UserCreate, UserLogin, UserResponse, TokenResponse
from middleware.rate_limiting import rate_limit

router = APIRouter(prefix="/auth", tags=["authentication"])
security = HTTPBearer()

@router.post("/register", response_model=TokenResponse)
@rate_limit(requests_per_hour=10)  # Limit registration attempts
async def register_user(
    user_data: UserCreate,
    db=Depends(get_database)
):
    """Register a new user account"""
    
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
    
    # Serialize datetime for MongoDB
    user_dict = user.model_dump()
    user_dict['created_at'] = user_dict['created_at'].isoformat()
    await db.users.insert_one(user_dict)
    
    # Create user profile
    from models.user_models import UserProfile
    profile = UserProfile(user_id=user.id)
    profile_dict = profile.model_dump()
    profile_dict['created_at'] = profile_dict['created_at'].isoformat()
    profile_dict['updated_at'] = profile_dict['updated_at'].isoformat()
    await db.user_profiles.insert_one(profile_dict)
    
    # Generate token
    token = auth_service.create_access_token(
        data={"sub": user.id, "email": user.email}
    )
    
    # Log registration
    await audit_logger.log_action(
        action_type=AuditActionType.USER_REGISTER,
        user_id=user.id,
        user_email=user.email,
        resource_type="user_account",
        resource_id=user.id,
        metadata={"registration_method": "email"},
        legal_basis="Contract performance"
    )
    
    return TokenResponse(
        access_token=token,
        user=UserResponse(
            id=user.id,
            email=user.email,
            full_name=user.full_name,
            is_admin=user.is_admin
        )
    )

@router.post("/login", response_model=TokenResponse)
@rate_limit(requests_per_hour=30)  # Limit login attempts
async def login_user(
    credentials: UserLogin,
    db=Depends(get_database)
):
    """Login with email and password"""
    
    user = await db.users.find_one({"email": credentials.email}, {"_id": 0})
    
    if not user or not auth_service.verify_password(credentials.password, user["hashed_password"]):
        # Log failed login attempt
        await audit_logger.log_action(
            action_type=AuditActionType.USER_LOGIN,
            user_email=credentials.email,
            resource_type="authentication",
            metadata={"status": "failed", "reason": "invalid_credentials"},
            legal_basis="Security monitoring"
        )
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    
    # Update last login
    await db.users.update_one(
        {"email": credentials.email},
        {"$set": {"last_login": datetime.now(timezone.utc).isoformat()}}
    )
    
    # Generate token
    token = auth_service.create_access_token(
        data={"sub": user["id"], "email": user["email"]}
    )
    
    # Log successful login
    await audit_logger.log_action(
        action_type=AuditActionType.USER_LOGIN,
        user_id=user["id"],
        user_email=user["email"],
        resource_type="authentication",
        metadata={"status": "success"},
        legal_basis="Contract performance"
    )
    
    return TokenResponse(
        access_token=token,
        user=UserResponse(
            id=user["id"],
            email=user["email"],
            full_name=user["full_name"],
            is_admin=user.get("is_admin", False)
        )
    )

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: dict = Depends(auth_service.get_current_user)
):
    """Get current user information"""
    
    # Log data access
    await audit_logger.log_action(
        action_type=AuditActionType.DATA_READ,
        user_id=current_user["id"],
        user_email=current_user["email"],
        resource_type="user_profile",
        resource_id=current_user["id"],
        legal_basis="Contract performance"
    )
    
    return UserResponse(
        id=current_user["id"],
        email=current_user["email"],
        full_name=current_user["full_name"],
        is_admin=current_user.get("is_admin", False)
    )

@router.post("/logout")
async def logout_user(
    current_user: dict = Depends(auth_service.get_current_user)
):
    """Logout user (client-side token removal)"""
    
    # Log logout
    await audit_logger.log_action(
        action_type=AuditActionType.USER_LOGOUT,
        user_id=current_user["id"],
        user_email=current_user["email"],
        resource_type="authentication",
        legal_basis="Contract performance"
    )
    
    return {"message": "Successfully logged out"}

@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    current_user: dict = Depends(auth_service.get_current_user)
):
    """Refresh user access token"""
    
    # Generate new token
    new_token = auth_service.create_access_token(
        data={"sub": current_user["id"], "email": current_user["email"]}
    )
    
    # Log token refresh
    await audit_logger.log_action(
        action_type=AuditActionType.USER_LOGIN,
        user_id=current_user["id"],
        user_email=current_user["email"],
        resource_type="authentication",
        metadata={"action": "token_refresh"},
        legal_basis="Contract performance"
    )
    
    return TokenResponse(
        access_token=new_token,
        user=UserResponse(
            id=current_user["id"],
            email=current_user["email"],
            full_name=current_user["full_name"],
            is_admin=current_user.get("is_admin", False)
        )
    )

# Password reset functionality
class PasswordResetRequest(BaseModel):
    email: EmailStr

class PasswordReset(BaseModel):
    email: EmailStr
    reset_token: str
    new_password: str

@router.post("/password-reset-request")
@rate_limit(requests_per_hour=5)  # Very limited for security
async def request_password_reset(
    request: PasswordResetRequest,
    db=Depends(get_database)
):
    """Request password reset (generates reset token)"""
    
    user = await db.users.find_one({"email": request.email}, {"_id": 0})
    
    if not user:
        # Don't reveal if email exists for security
        return {"message": "If the email exists, a reset link has been sent"}
    
    # Generate password reset token (valid for 1 hour)
    reset_token = auth_service.create_access_token(
        data={"sub": user["id"], "type": "password_reset"},
        expires_delta_hours=1
    )
    
    # In production, send this token via email
    # For now, we'll store it in database for demo
    await db.password_reset_tokens.insert_one({
        "user_id": user["id"],
        "token": reset_token,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "used": False
    })
    
    # Log password reset request
    await audit_logger.log_action(
        action_type=AuditActionType.GDPR_DATA_REQUEST,
        user_id=user["id"],
        user_email=user["email"],
        resource_type="password_reset",
        metadata={"request_type": "password_reset"},
        legal_basis="Contract performance"
    )
    
    return {"message": "If the email exists, a reset link has been sent"}

@router.post("/password-reset")
async def reset_password(
    reset_data: PasswordReset,
    db=Depends(get_database)
):
    """Reset password using reset token"""
    
    # Verify reset token
    token_payload = auth_service.decode_token(reset_data.reset_token)
    if not token_payload or token_payload.get("type") != "password_reset":
        raise HTTPException(status_code=400, detail="Invalid or expired reset token")
    
    user_id = token_payload.get("sub")
    
    # Check if token has been used
    reset_token_record = await db.password_reset_tokens.find_one({
        "user_id": user_id,
        "token": reset_data.reset_token,
        "used": False
    })
    
    if not reset_token_record:
        raise HTTPException(status_code=400, detail="Reset token has already been used or is invalid")
    
    # Update password
    new_password_hash = auth_service.get_password_hash(reset_data.new_password)
    await db.users.update_one(
        {"id": user_id},
        {"$set": {"hashed_password": new_password_hash}}
    )
    
    # Mark token as used
    await db.password_reset_tokens.update_one(
        {"_id": reset_token_record["_id"]},
        {"$set": {"used": True}}
    )
    
    # Log password reset
    await audit_logger.log_action(
        action_type=AuditActionType.DATA_UPDATE,
        user_id=user_id,
        user_email=reset_data.email,
        resource_type="user_credentials",
        resource_id=user_id,
        metadata={"action": "password_reset_completed"},
        legal_basis="Contract performance"
    )
    
    return {"message": "Password has been reset successfully"}