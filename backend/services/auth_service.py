"""
Authentication Service
Centralized authentication and token management
"""
from datetime import datetime, timedelta, timezone
from typing import Optional
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from passlib.context import CryptContext
from jose import JWTError, jwt
from core.config import settings
from core.database import get_database

class AuthenticationService:
    """Authentication service for user management and token handling"""
    
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.security = HTTPBearer()
        self.algorithm = "HS256"
        self.access_token_expire_hours = 24
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a plain password against its hash"""
        return self.pwd_context.verify(plain_password, hashed_password)
    
    def get_password_hash(self, password: str) -> str:
        """Generate password hash"""
        return self.pwd_context.hash(password)
    
    def create_access_token(
        self, 
        data: dict, 
        expires_delta_hours: Optional[int] = None
    ) -> str:
        """Create JWT access token"""
        to_encode = data.copy()
        
        if expires_delta_hours:
            expire = datetime.now(timezone.utc) + timedelta(hours=expires_delta_hours)
        else:
            expire = datetime.now(timezone.utc) + timedelta(hours=self.access_token_expire_hours)
        
        to_encode.update({
            "exp": expire,
            "iat": datetime.now(timezone.utc),
            "type": "access_token"
        })
        
        encoded_jwt = jwt.encode(to_encode, settings.security.jwt_secret_key, algorithm=self.algorithm)
        return encoded_jwt
    
    def decode_token(self, token: str) -> Optional[dict]:
        """Decode and verify JWT token"""
        try:
            payload = jwt.decode(
                token, 
                settings.security.jwt_secret_key, 
                algorithms=[self.algorithm]
            )
            
            # Check token type
            if payload.get("type") != "access_token":
                return None
            
            # Check expiration
            exp = payload.get("exp")
            if exp and datetime.fromtimestamp(exp, tz=timezone.utc) < datetime.now(timezone.utc):
                return None
            
            return payload
            
        except JWTError:
            return None
    
    async def get_current_user(
        self, 
        credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
        db = Depends(get_database)
    ):
        """Dependency to get current authenticated user"""
        
        token = credentials.credentials
        payload = self.decode_token(token)
        
        if not payload:
            raise HTTPException(
                status_code=401, 
                detail="Invalid or expired token",
                headers={"WWW-Authenticate": "Bearer"}
            )
        
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=401, 
                detail="Invalid token payload",
                headers={"WWW-Authenticate": "Bearer"}
            )
        
        # Fetch user from database
        user = await db.users.find_one({"id": user_id}, {"_id": 0})
        if not user:
            raise HTTPException(
                status_code=401, 
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"}
            )
        
        # Check if user is active
        if not user.get("is_active", True):
            raise HTTPException(
                status_code=401, 
                detail="User account is disabled",
                headers={"WWW-Authenticate": "Bearer"}
            )
        
        # Deserialize datetime fields
        if user.get("created_at") and isinstance(user["created_at"], str):
            user["created_at"] = datetime.fromisoformat(user["created_at"])
        if user.get("last_login") and isinstance(user["last_login"], str):
            user["last_login"] = datetime.fromisoformat(user["last_login"])
        
        return user
    
    async def get_current_admin(
        self, 
        current_user: dict = Depends(lambda: auth_service.get_current_user)
    ):
        """Dependency to ensure current user is an admin"""
        
        if not current_user.get("is_admin", False):
            raise HTTPException(
                status_code=403, 
                detail="Admin access required"
            )
        
        return current_user
    
    def validate_password_strength(self, password: str) -> list:
        """Validate password strength and return list of issues"""
        issues = []
        
        if len(password) < 8:
            issues.append("Password must be at least 8 characters long")
        
        if not any(c.isupper() for c in password):
            issues.append("Password must contain at least one uppercase letter")
        
        if not any(c.islower() for c in password):
            issues.append("Password must contain at least one lowercase letter")
        
        if not any(c.isdigit() for c in password):
            issues.append("Password must contain at least one number")
        
        # Check for special characters
        special_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        if not any(c in special_chars for c in password):
            issues.append("Password must contain at least one special character")
        
        return issues
    
    async def is_email_taken(self, email: str, db) -> bool:
        """Check if email is already registered"""
        user = await db.users.find_one({"email": email})
        return user is not None
    
    async def get_user_by_email(self, email: str, db) -> Optional[dict]:
        """Get user by email address"""
        return await db.users.find_one({"email": email}, {"_id": 0})
    
    async def get_user_by_id(self, user_id: str, db) -> Optional[dict]:
        """Get user by ID"""
        user = await db.users.find_one({"id": user_id}, {"_id": 0})
        if user:
            # Deserialize datetime fields
            if user.get("created_at") and isinstance(user["created_at"], str):
                user["created_at"] = datetime.fromisoformat(user["created_at"])
            if user.get("last_login") and isinstance(user["last_login"], str):
                user["last_login"] = datetime.fromisoformat(user["last_login"])
        return user
    
    def generate_user_token_data(self, user: dict) -> dict:
        """Generate token data for a user"""
        return {
            "sub": user["id"],
            "email": user["email"],
            "is_admin": user.get("is_admin", False),
            "full_name": user.get("full_name", "")
        }

# Global authentication service instance
auth_service = AuthenticationService()

# Convenience dependencies
async def require_auth(current_user: dict = Depends(auth_service.get_current_user)):
    """Dependency that requires authentication"""
    return current_user

async def require_admin(current_user: dict = Depends(auth_service.get_current_admin)):
    """Dependency that requires admin privileges"""
    return current_user

# Optional authentication (for public endpoints that benefit from user context)
async def optional_auth(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(HTTPBearer(auto_error=False)),
    db = Depends(get_database)
) -> Optional[dict]:
    """Optional authentication dependency - returns None if not authenticated"""
    
    if not credentials:
        return None
    
    try:
        payload = auth_service.decode_token(credentials.credentials)
        if not payload:
            return None
        
        user_id = payload.get("sub")
        if not user_id:
            return None
        
        user = await db.users.find_one({"id": user_id}, {"_id": 0})
        if not user or not user.get("is_active", True):
            return None
        
        return user
        
    except Exception:
        return None