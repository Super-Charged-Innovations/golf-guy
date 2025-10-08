"""
S3 File Storage Service for Golf Guy Platform
Handles secure file uploads, management, and GDPR-compliant storage
"""
import boto3
from botocore.exceptions import ClientError, NoCredentialsError
from fastapi import UploadFile, HTTPException
import os
import uuid
import mimetypes
from typing import Optional, List, Dict
from datetime import datetime, timedelta
import hashlib
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class S3FileStorageService:
    """
    S3-based file storage service with security and GDPR compliance
    """
    
    def __init__(self):
        self.aws_access_key = os.environ.get('AWS_ACCESS_KEY_ID')
        self.aws_secret_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
        self.bucket_name = os.environ.get('S3_BUCKET_NAME', 'golfguy-platform-storage')
        self.region = os.environ.get('AWS_REGION', 'eu-north-1')  # European region for GDPR compliance
        
        # Initialize S3 client
        self._s3_client = None
        
        # File configuration
        self.max_file_size = 50 * 1024 * 1024  # 50MB max file size
        self.allowed_extensions = {
            'images': ['.jpg', '.jpeg', '.png', '.webp', '.gif'],
            'documents': ['.pdf', '.doc', '.docx', '.txt'],
            'videos': ['.mp4', '.mov', '.avi', '.webm']
        }
        
        # Storage categories with prefixes
        self.storage_categories = {
            'destination-images': 'destinations/images/',
            'user-profiles': 'users/profiles/',
            'kyc-documents': 'users/kyc/',
            'admin-content': 'admin/content/',
            'gdpr-exports': 'gdpr/exports/',
            'generated-reports': 'reports/'
        }
    
    @property
    def s3_client(self):
        """Lazy initialization of S3 client"""
        if self._s3_client is None:
            if not self.aws_access_key or not self.aws_secret_key:
                raise HTTPException(
                    status_code=500,
                    detail="AWS credentials not configured"
                )
            
            self._s3_client = boto3.client(
                's3',
                aws_access_key_id=self.aws_access_key,
                aws_secret_access_key=self.aws_secret_key,
                region_name=self.region
            )
        return self._s3_client
    
    def _validate_file(self, file: UploadFile, category: str) -> Dict:
        """Validate uploaded file against security and size requirements"""
        
        # Check file size
        if hasattr(file.file, 'seek') and hasattr(file.file, 'tell'):
            file.file.seek(0, 2)  # Seek to end
            file_size = file.file.tell()
            file.file.seek(0)  # Reset to beginning
            
            if file_size > self.max_file_size:
                raise HTTPException(
                    status_code=413,
                    detail=f"File size {file_size} exceeds maximum {self.max_file_size} bytes"
                )
        
        # Check file extension
        file_ext = Path(file.filename).suffix.lower()
        
        allowed_extensions = []
        for ext_list in self.allowed_extensions.values():
            allowed_extensions.extend(ext_list)
        
        if file_ext not in allowed_extensions:
            raise HTTPException(
                status_code=400,
                detail=f"File extension {file_ext} not allowed"
            )
        
        # Determine MIME type
        mime_type, _ = mimetypes.guess_type(file.filename)
        if not mime_type:
            mime_type = 'application/octet-stream'
        
        return {
            'file_size': file_size if 'file_size' in locals() else 0,
            'file_extension': file_ext,
            'mime_type': mime_type,
            'original_filename': file.filename
        }
    
    def _generate_file_key(self, category: str, user_id: Optional[str] = None, 
                          original_filename: str = None) -> str:
        """Generate secure file key with UUID and timestamp"""
        
        # Get category prefix
        prefix = self.storage_categories.get(category, 'misc/')
        
        # Add user ID for user-specific content
        if user_id and category in ['user-profiles', 'kyc-documents', 'gdpr-exports']:
            prefix += f"{user_id}/"
        
        # Generate unique filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        unique_id = str(uuid.uuid4())[:8]
        
        # Preserve original extension
        file_ext = Path(original_filename).suffix.lower() if original_filename else ''
        
        filename = f"{timestamp}_{unique_id}{file_ext}"
        
        return f"{prefix}{filename}"
    
    async def upload_file(self, file: UploadFile, category: str, 
                         user_id: Optional[str] = None, 
                         metadata: Optional[Dict] = None) -> Dict:
        """
        Upload file to S3 with security validation and metadata
        
        Args:
            file: FastAPI UploadFile object
            category: Storage category (e.g., 'destination-images', 'user-profiles')
            user_id: Optional user ID for user-specific files
            metadata: Optional metadata to store with file
            
        Returns:
            Dict with file information including S3 URL
        """
        
        try:
            # Validate file
            file_info = self._validate_file(file, category)
            
            # Generate file key
            file_key = self._generate_file_key(category, user_id, file.filename)
            
            # Prepare metadata
            upload_metadata = {
                'category': category,
                'uploaded_at': datetime.now().isoformat(),
                'original_filename': file.filename,
                'file_size': str(file_info['file_size']),
                'uploader_id': user_id or 'anonymous'
            }
            
            if metadata:
                upload_metadata.update(metadata)
            
            # Upload to S3
            self.s3_client.upload_fileobj(
                file.file,
                self.bucket_name,
                file_key,
                ExtraArgs={
                    'ContentType': file_info['mime_type'],
                    'Metadata': upload_metadata,
                    'ServerSideEncryption': 'AES256',  # Encrypt at rest
                    'CacheControl': 'max-age=31536000',  # 1 year cache for static assets
                }
            )
            
            # Generate file URL
            file_url = f"https://{self.bucket_name}.s3.{self.region}.amazonaws.com/{file_key}"
            
            logger.info(f"File uploaded successfully: {file_key}")
            
            return {
                'file_key': file_key,
                'file_url': file_url,
                'file_size': file_info['file_size'],
                'mime_type': file_info['mime_type'],
                'original_filename': file.filename,
                'category': category,
                'uploaded_at': datetime.now().isoformat()
            }
            
        except ClientError as e:
            logger.error(f"AWS S3 error during file upload: {str(e)}")
            raise HTTPException(status_code=500, detail=f"File upload failed: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error during file upload: {str(e)}")
            raise HTTPException(status_code=500, detail="File upload failed")
    
    def generate_presigned_url(self, file_key: str, expiration: int = 3600) -> str:
        """
        Generate presigned URL for secure file access
        
        Args:
            file_key: S3 file key
            expiration: URL expiration time in seconds (default 1 hour)
            
        Returns:
            Presigned URL string
        """
        
        try:
            url = self.s3_client.generate_presigned_url(
                'get_object',
                Params={'Bucket': self.bucket_name, 'Key': file_key},
                ExpiresIn=expiration
            )
            return url
        except ClientError as e:
            logger.error(f"Error generating presigned URL: {str(e)}")
            raise HTTPException(status_code=500, detail="Failed to generate file access URL")
    
    def delete_file(self, file_key: str, user_id: Optional[str] = None) -> bool:
        """
        Delete file from S3 (GDPR compliance - right to be forgotten)
        
        Args:
            file_key: S3 file key to delete
            user_id: Optional user ID for permission check
            
        Returns:
            True if successful
        """
        
        try:
            # Additional security check for user-specific files
            if user_id and ('users/' in file_key and user_id not in file_key):
                raise HTTPException(status_code=403, detail="Not authorized to delete this file")
            
            self.s3_client.delete_object(Bucket=self.bucket_name, Key=file_key)
            logger.info(f"File deleted successfully: {file_key}")
            return True
            
        except ClientError as e:
            logger.error(f"Error deleting file: {str(e)}")
            raise HTTPException(status_code=500, detail="File deletion failed")
    
    def list_files(self, prefix: str, user_id: Optional[str] = None) -> List[Dict]:
        """
        List files with optional prefix filtering
        
        Args:
            prefix: S3 key prefix to filter by
            user_id: Optional user ID for user-specific files
            
        Returns:
            List of file information dictionaries
        """
        
        try:
            # Add user ID to prefix for user-specific files
            if user_id and prefix.startswith('users/'):
                prefix = f"{prefix}{user_id}/"
            
            response = self.s3_client.list_objects_v2(
                Bucket=self.bucket_name,
                Prefix=prefix,
                MaxKeys=1000
            )
            
            files = []
            for obj in response.get('Contents', []):
                # Get file metadata
                metadata_response = self.s3_client.head_object(
                    Bucket=self.bucket_name,
                    Key=obj['Key']
                )
                
                files.append({
                    'file_key': obj['Key'],
                    'file_size': obj['Size'],
                    'last_modified': obj['LastModified'].isoformat(),
                    'metadata': metadata_response.get('Metadata', {}),
                    'content_type': metadata_response.get('ContentType', 'unknown')
                })
            
            return files
            
        except ClientError as e:
            logger.error(f"Error listing files: {str(e)}")
            raise HTTPException(status_code=500, detail="Failed to list files")
    
    def get_file_info(self, file_key: str) -> Dict:
        """Get metadata and information about a specific file"""
        
        try:
            response = self.s3_client.head_object(Bucket=self.bucket_name, Key=file_key)
            
            return {
                'file_key': file_key,
                'file_size': response['ContentLength'],
                'last_modified': response['LastModified'].isoformat(),
                'content_type': response.get('ContentType', 'unknown'),
                'metadata': response.get('Metadata', {}),
                'server_side_encryption': response.get('ServerSideEncryption', 'None')
            }
            
        except ClientError as e:
            if e.response['Error']['Code'] == 'NoSuchKey':
                raise HTTPException(status_code=404, detail="File not found")
            else:
                logger.error(f"Error getting file info: {str(e)}")
                raise HTTPException(status_code=500, detail="Failed to get file information")
    
    async def cleanup_user_files(self, user_id: str) -> int:
        """
        Delete all files associated with a user (GDPR right to be forgotten)
        
        Args:
            user_id: User ID to cleanup files for
            
        Returns:
            Number of files deleted
        """
        
        deleted_count = 0
        
        # Categories that contain user-specific files
        user_categories = ['user-profiles', 'kyc-documents', 'gdpr-exports']
        
        for category in user_categories:
            prefix = f"{self.storage_categories[category]}{user_id}/"
            
            try:
                # List all user files in this category
                files = self.list_files(prefix, user_id)
                
                # Delete each file
                for file_info in files:
                    if self.delete_file(file_info['file_key'], user_id):
                        deleted_count += 1
                        
            except Exception as e:
                logger.error(f"Error cleaning up user files in {category}: {str(e)}")
        
        logger.info(f"Cleaned up {deleted_count} files for user {user_id}")
        return deleted_count

# Initialize the service
s3_service = S3FileStorageService()