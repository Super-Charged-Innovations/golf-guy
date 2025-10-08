"""
Rate limiting middleware for API protection
Implements token bucket algorithm with Redis backend
"""
import time
import hashlib
from functools import wraps
from typing import Optional, Dict, Any
from fastapi import HTTPException, Request
from core.config import settings
import logging

logger = logging.getLogger(__name__)

# In-memory rate limiting (fallback when Redis is not available)
class InMemoryRateLimiter:
    """Simple in-memory rate limiter using token bucket algorithm"""
    
    def __init__(self):
        self.buckets: Dict[str, Dict] = {}
        self.cleanup_interval = 3600  # Clean old entries every hour
        self.last_cleanup = time.time()
    
    def _cleanup_old_entries(self):
        """Remove old entries to prevent memory leaks"""
        current_time = time.time()
        if current_time - self.last_cleanup > self.cleanup_interval:
            cutoff_time = current_time - 3600  # Remove entries older than 1 hour
            self.buckets = {
                key: value for key, value in self.buckets.items()
                if value.get('last_refill', 0) > cutoff_time
            }
            self.last_cleanup = current_time
    
    def is_allowed(
        self, 
        key: str, 
        max_requests: int, 
        window_seconds: int = 3600
    ) -> tuple[bool, Dict[str, Any]]:
        """
        Check if request is allowed using token bucket algorithm
        
        Args:
            key: Unique identifier for the rate limit bucket
            max_requests: Maximum requests allowed in the window
            window_seconds: Time window in seconds
            
        Returns:
            (is_allowed, info_dict)
        """
        current_time = time.time()
        
        # Clean up old entries periodically
        self._cleanup_old_entries()
        
        if key not in self.buckets:
            self.buckets[key] = {
                'tokens': max_requests,
                'last_refill': current_time,
                'total_requests': 0
            }
        
        bucket = self.buckets[key]
        
        # Calculate tokens to add based on elapsed time
        time_elapsed = current_time - bucket['last_refill']
        tokens_to_add = (time_elapsed / window_seconds) * max_requests
        
        # Refill bucket (but don't exceed max_requests)
        bucket['tokens'] = min(max_requests, bucket['tokens'] + tokens_to_add)
        bucket['last_refill'] = current_time
        
        # Check if we can consume a token
        if bucket['tokens'] >= 1:
            bucket['tokens'] -= 1
            bucket['total_requests'] += 1
            
            return True, {
                'requests_remaining': int(bucket['tokens']),
                'reset_time': current_time + window_seconds,
                'total_requests': bucket['total_requests']
            }
        else:
            return False, {
                'requests_remaining': 0,
                'reset_time': bucket['last_refill'] + window_seconds,
                'total_requests': bucket['total_requests']
            }

# Global rate limiter instance
rate_limiter = InMemoryRateLimiter()

# Redis rate limiter (future implementation)
class RedisRateLimiter:
    """Redis-based distributed rate limiter"""
    
    def __init__(self, redis_client):
        self.redis = redis_client
    
    async def is_allowed(
        self, 
        key: str, 
        max_requests: int, 
        window_seconds: int = 3600
    ) -> tuple[bool, Dict[str, Any]]:
        """Redis-based rate limiting implementation"""
        # TODO: Implement Redis-based rate limiting
        # This would use Redis sliding window or token bucket
        pass

def get_client_identifier(request: Request) -> str:
    """Generate unique client identifier for rate limiting"""
    
    # Try to get user ID from token if available
    auth_header = request.headers.get("authorization", "")
    if auth_header.startswith("Bearer "):
        token = auth_header.split(" ")[1]
        # You could decode the token here to get user ID
        # For now, we'll use the token hash
        user_hash = hashlib.md5(token.encode()).hexdigest()[:16]
        return f"user:{user_hash}"
    
    # Fallback to IP address
    forwarded_for = request.headers.get("x-forwarded-for")
    if forwarded_for:
        client_ip = forwarded_for.split(",")[0].strip()
    else:
        client_ip = request.client.host if request.client else "unknown"
    
    return f"ip:{client_ip}"

def rate_limit(
    requests_per_hour: int = 100,
    requests_per_minute: Optional[int] = None,
    custom_key_func: Optional[callable] = None
):
    """
    Rate limiting decorator for FastAPI routes
    
    Args:
        requests_per_hour: Maximum requests per hour
        requests_per_minute: Maximum requests per minute (optional)
        custom_key_func: Custom function to generate rate limit key
    """
    
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Extract request object from arguments
            request = None
            for arg in args:
                if isinstance(arg, Request):
                    request = arg
                    break
            
            # Look for request in kwargs
            if not request:
                for value in kwargs.values():
                    if isinstance(value, Request):
                        request = value
                        break
            
            # Skip rate limiting if no request object found
            if not request:
                logger.warning("Rate limiting skipped - no request object found")
                return await func(*args, **kwargs)
            
            # Generate rate limit key
            if custom_key_func:
                client_key = custom_key_func(request)
            else:
                client_key = get_client_identifier(request)
            
            # Check hourly rate limit
            hourly_key = f"hourly:{func.__name__}:{client_key}"
            allowed, info = rate_limiter.is_allowed(
                hourly_key, 
                requests_per_hour, 
                3600  # 1 hour
            )
            
            if not allowed:
                raise HTTPException(
                    status_code=429,
                    detail="Too many requests. Please try again later.",
                    headers={
                        "X-RateLimit-Limit": str(requests_per_hour),
                        "X-RateLimit-Remaining": "0",
                        "X-RateLimit-Reset": str(int(info['reset_time']))
                    }
                )
            
            # Check minute rate limit if specified
            if requests_per_minute:
                minute_key = f"minute:{func.__name__}:{client_key}"
                allowed_minute, info_minute = rate_limiter.is_allowed(
                    minute_key,
                    requests_per_minute,
                    60  # 1 minute
                )
                
                if not allowed_minute:
                    raise HTTPException(
                        status_code=429,
                        detail="Too many requests per minute. Please slow down.",
                        headers={
                            "X-RateLimit-Limit": str(requests_per_minute),
                            "X-RateLimit-Remaining": "0",
                            "X-RateLimit-Reset": str(int(info_minute['reset_time']))
                        }
                    )
            
            # Add rate limit headers to response
            try:
                response = await func(*args, **kwargs)
                
                # Add headers if response object supports it
                if hasattr(response, 'headers'):
                    response.headers["X-RateLimit-Limit"] = str(requests_per_hour)
                    response.headers["X-RateLimit-Remaining"] = str(info['requests_remaining'])
                    response.headers["X-RateLimit-Reset"] = str(int(info['reset_time']))
                
                return response
                
            except Exception as e:
                # Log rate limit violations for monitoring
                if isinstance(e, HTTPException) and e.status_code != 429:
                    logger.info(f"Rate limited request from {client_key} to {func.__name__}")
                raise
        
        return wrapper
    return decorator

# Common rate limit configurations
class RateLimits:
    """Predefined rate limit configurations"""
    
    # Authentication endpoints (strict)
    AUTH_STRICT = {"requests_per_hour": 10, "requests_per_minute": 2}
    AUTH_MODERATE = {"requests_per_hour": 30, "requests_per_minute": 5}
    
    # API endpoints (general)
    API_GENERAL = {"requests_per_hour": 100}
    API_HEAVY = {"requests_per_hour": 50}  # For resource-intensive endpoints
    
    # File operations
    FILE_UPLOAD = {"requests_per_hour": 20, "requests_per_minute": 3}
    FILE_DOWNLOAD = {"requests_per_hour": 200}
    
    # Public endpoints
    PUBLIC_GENERAL = {"requests_per_hour": 1000}
    PUBLIC_SEARCH = {"requests_per_hour": 500}

# Specialized rate limiting functions
def auth_rate_limit():
    """Rate limit for authentication endpoints"""
    return rate_limit(**RateLimits.AUTH_STRICT)

def api_rate_limit():
    """Standard rate limit for API endpoints"""
    return rate_limit(**RateLimits.API_GENERAL)

def file_upload_rate_limit():
    """Rate limit for file upload endpoints"""
    return rate_limit(**RateLimits.FILE_UPLOAD)

def admin_rate_limit():
    """Rate limit for admin endpoints (more permissive)"""
    return rate_limit(requests_per_hour=500)

# Rate limit monitoring
class RateLimitMonitor:
    """Monitor and analyze rate limiting patterns"""
    
    @staticmethod
    def get_rate_limit_stats() -> Dict[str, Any]:
        """Get rate limiting statistics"""
        current_time = time.time()
        
        stats = {
            "total_buckets": len(rate_limiter.buckets),
            "active_buckets": 0,
            "top_consumers": [],
            "bucket_details": {}
        }
        
        # Analyze bucket data
        bucket_data = []
        for key, bucket in rate_limiter.buckets.items():
            if current_time - bucket['last_refill'] < 3600:  # Active in last hour
                stats["active_buckets"] += 1
                bucket_data.append({
                    "key": key,
                    "total_requests": bucket['total_requests'],
                    "tokens_remaining": bucket['tokens'],
                    "last_activity": bucket['last_refill']
                })
        
        # Sort by request count to find top consumers
        bucket_data.sort(key=lambda x: x['total_requests'], reverse=True)
        stats["top_consumers"] = bucket_data[:10]
        
        return stats
    
    @staticmethod
    def clear_rate_limit_data():
        """Clear all rate limit data (admin function)"""
        rate_limiter.buckets.clear()
        logger.info("Rate limit data cleared")

# Export the monitor
rate_limit_monitor = RateLimitMonitor()