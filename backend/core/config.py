"""
Core configuration module for Golf Guy Platform
Centralizes all configuration management and environment variables
"""
import os
from pathlib import Path
from typing import Optional
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load environment variables
ROOT_DIR = Path(__file__).parent.parent
load_dotenv(ROOT_DIR / '.env')

class DatabaseSettings(BaseSettings):
    """Database configuration settings"""
    mongo_url: str = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
    db_name: str = os.environ.get('DB_NAME', 'golftrip')
    
    class Config:
        env_prefix = 'DB_'

class SecuritySettings(BaseSettings):
    """Security and authentication settings"""
    jwt_secret_key: str = os.environ.get('JWT_SECRET_KEY', '')
    encryption_key: str = os.environ.get('ENCRYPTION_KEY', '')
    cors_origins: str = os.environ.get('CORS_ORIGINS', '*')
    
    @property
    def cors_origins_list(self) -> list:
        """Convert CORS origins string to list"""
        return [origin.strip() for origin in self.cors_origins.split(',')]
    
    class Config:
        env_prefix = 'SECURITY_'

class AWSSettings(BaseSettings):
    """AWS S3 and CloudFront settings"""
    aws_access_key_id: Optional[str] = os.environ.get('AWS_ACCESS_KEY_ID')
    aws_secret_access_key: Optional[str] = os.environ.get('AWS_SECRET_ACCESS_KEY')
    s3_bucket_name: str = os.environ.get('S3_BUCKET_NAME', 'golfguy-platform-storage')
    aws_region: str = os.environ.get('AWS_REGION', 'eu-north-1')
    cloudfront_domain: Optional[str] = os.environ.get('CLOUDFRONT_DISTRIBUTION_DOMAIN')
    
    @property
    def is_configured(self) -> bool:
        """Check if AWS credentials are properly configured"""
        return bool(self.aws_access_key_id and self.aws_secret_access_key)
    
    class Config:
        env_prefix = 'AWS_'

class AISettings(BaseSettings):
    """AI service configuration"""
    emergent_llm_key: Optional[str] = os.environ.get('EMERGENT_LLM_KEY')
    openai_api_key: Optional[str] = os.environ.get('OPENAI_API_KEY')  # Fallback
    
    @property
    def api_key(self) -> str:
        """Get the appropriate API key for AI services"""
        return self.emergent_llm_key or self.openai_api_key or ''
    
    class Config:
        env_prefix = 'AI_'

class AppSettings(BaseSettings):
    """Application-wide settings"""
    app_name: str = "Golf Guy Platform API"
    version: str = "2.0.0"
    debug: bool = os.environ.get('DEBUG', 'False').lower() == 'true'
    environment: str = os.environ.get('ENVIRONMENT', 'production')
    
    # Rate limiting settings
    rate_limit_requests: int = int(os.environ.get('RATE_LIMIT_REQUESTS', '100'))
    rate_limit_window: int = int(os.environ.get('RATE_LIMIT_WINDOW', '3600'))  # 1 hour
    
    # File upload settings
    max_file_size: int = int(os.environ.get('MAX_FILE_SIZE', '52428800'))  # 50MB
    allowed_file_extensions: str = os.environ.get(
        'ALLOWED_FILE_EXTENSIONS', 
        '.jpg,.jpeg,.png,.webp,.pdf,.doc,.docx,.txt,.mp4,.mov,.avi'
    )
    
    @property
    def allowed_extensions_list(self) -> list:
        """Convert allowed extensions string to list"""
        return [ext.strip() for ext in self.allowed_file_extensions.split(',')]
    
    class Config:
        env_prefix = 'APP_'

class CacheSettings(BaseSettings):
    """Caching configuration"""
    redis_url: Optional[str] = os.environ.get('REDIS_URL')
    cache_ttl: int = int(os.environ.get('CACHE_TTL', '3600'))  # 1 hour default
    enable_caching: bool = os.environ.get('ENABLE_CACHING', 'True').lower() == 'true'
    
    class Config:
        env_prefix = 'CACHE_'

class Settings:
    """Main settings container"""
    
    def __init__(self):
        self.database = DatabaseSettings()
        self.security = SecuritySettings()
        self.aws = AWSSettings()
        self.ai = AISettings()
        self.app = AppSettings()
        self.cache = CacheSettings()
    
    def get_cors_origins(self) -> list:
        """Get CORS origins for FastAPI"""
        return self.security.cors_origins_list
    
    def is_production(self) -> bool:
        """Check if running in production environment"""
        return self.app.environment.lower() == 'production'
    
    def is_development(self) -> bool:
        """Check if running in development environment"""
        return self.app.environment.lower() in ['development', 'dev']
    
    def validate_configuration(self) -> list:
        """Validate critical configuration and return warnings"""
        warnings = []
        
        # Critical settings validation
        if not self.security.jwt_secret_key:
            warnings.append("JWT_SECRET_KEY not configured - authentication will fail")
        
        if not self.security.encryption_key:
            warnings.append("ENCRYPTION_KEY not configured - data encryption will fail")
        
        if self.security.cors_origins == '*' and self.is_production():
            warnings.append("CORS is set to wildcard (*) in production - security risk")
        
        if not self.ai.api_key:
            warnings.append("No AI API key configured - AI features will be disabled")
        
        # Optional settings warnings
        if not self.aws.is_configured:
            warnings.append("AWS credentials not configured - file storage will be disabled")
        
        if not self.cache.redis_url and self.cache.enable_caching:
            warnings.append("Redis URL not configured - caching will be disabled")
        
        return warnings

# Global settings instance
settings = Settings()

# Configuration validation on startup
def validate_startup_config():
    """Validate configuration on application startup"""
    warnings = settings.validate_configuration()
    
    if warnings:
        import logging
        logger = logging.getLogger(__name__)
        logger.warning("Configuration warnings detected:")
        for warning in warnings:
            logger.warning(f"  - {warning}")
    
    return len(warnings) == 0

# Export commonly used settings
DATABASE_URL = settings.database.mongo_url
DB_NAME = settings.database.db_name
JWT_SECRET = settings.security.jwt_secret_key
CORS_ORIGINS = settings.get_cors_origins()
AWS_CONFIGURED = settings.aws.is_configured
AI_API_KEY = settings.ai.api_key