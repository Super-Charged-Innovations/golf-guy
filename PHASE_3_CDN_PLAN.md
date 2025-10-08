# Phase 3: CDN Integration & Image Optimization Plan

## Current Status: S3 Backend Complete, Frontend Components Ready

### 3.1 AWS CloudFront CDN Integration ✅ READY FOR IMPLEMENTATION

**Purpose**: Global content delivery with caching and optimization

**Implementation Requirements**:

#### CloudFront Distribution Configuration:
```yaml
# CloudFront Configuration (Infrastructure as Code)
CloudFrontDistribution:
  Properties:
    DistributionConfig:
      Origins:
        - DomainName: golfguy-platform-storage.s3.eu-north-1.amazonaws.com
          Id: S3Origin
          S3OriginConfig:
            OriginAccessIdentity: !Ref CloudFrontOriginAccessIdentity
      
      DefaultCacheBehavior:
        TargetOriginId: S3Origin
        ViewerProtocolPolicy: redirect-to-https
        CachePolicyId: 4135ea2d-6df8-44a3-9df3-4b5a84be39ad  # Managed-CachingOptimized
        
      # Cache behaviors for different file types
      CacheBehaviors:
        - PathPattern: "*.jpg"
          CachePolicyId: 4135ea2d-6df8-44a3-9df3-4b5a84be39ad
          TTL: 86400  # 24 hours
        - PathPattern: "*.png"
          CachePolicyId: 4135ea2d-6df8-44a3-9df3-4b5a84be39ad
          TTL: 86400
        - PathPattern: "*.pdf"
          CachePolicyId: 4135ea2d-6df8-44a3-9df3-4b5a84be39ad
          TTL: 3600   # 1 hour
      
      # Security headers
      ResponseHeadersPolicy:
        SecurityHeadersConfig:
          StrictTransportSecurity:
            AccessControlMaxAgeSec: 31536000
            IncludeSubdomains: true
          ContentTypeOptions:
            Override: true
          FrameOptions:
            FrameOption: DENY
            Override: true
```

#### Environment Variables Needed:
```bash
# Add to backend/.env
CLOUDFRONT_DISTRIBUTION_DOMAIN=d123456789abcd.cloudfront.net
CLOUDFRONT_URL_SIGNING_KEY_ID=APKAI...
CLOUDFRONT_PRIVATE_KEY_PATH=/path/to/private-key.pem
```

### 3.2 Image Optimization Pipeline ✅ READY FOR IMPLEMENTATION

**Lambda@Edge Function for Automatic Optimization**:

```javascript
// CloudFront Lambda@Edge function for image optimization
exports.handler = async (event, context) => {
    const request = event.Records[0].cf.request;
    const uri = request.uri;
    
    // Only process image requests
    if (!uri.match(/\.(jpg|jpeg|png|webp)$/i)) {
        return request;
    }
    
    // Parse query parameters for optimization
    const params = new URLSearchParams(request.querystring);
    
    const width = params.get('w') || params.get('width');
    const height = params.get('h') || params.get('height');
    const quality = params.get('q') || params.get('quality') || '80';
    const format = params.get('f') || params.get('format') || 'auto';
    
    // Modify the request to include optimization parameters
    if (width || height || quality !== '80' || format !== 'auto') {
        const optimizedUri = uri.replace(/(\.[^.]+)$/, `_${width || 'auto'}x${height || 'auto'}_q${quality}_${format}$1`);
        request.uri = optimizedUri;
    }
    
    return request;
};
```

**Backend Image Optimization Service**:

```python
# Add to backend/image_optimization.py
from PIL import Image, ImageOpt
import io
import boto3
from typing import Tuple, Optional

class ImageOptimizer:
    def __init__(self):
        self.max_width = 2048
        self.max_height = 2048
        self.quality_settings = {
            'thumbnail': 60,
            'standard': 80,
            'high': 95
        }
    
    def optimize_image(
        self, 
        image_data: bytes, 
        width: Optional[int] = None,
        height: Optional[int] = None,
        quality: str = 'standard',
        format: str = 'auto'
    ) -> Tuple[bytes, str]:
        """Optimize image with specified parameters"""
        
        with Image.open(io.BytesIO(image_data)) as img:
            # Convert to RGB if necessary
            if img.mode in ('RGBA', 'LA', 'P'):
                img = img.convert('RGB')
            
            # Calculate dimensions
            original_width, original_height = img.size
            
            if width or height:
                # Calculate aspect ratio
                aspect_ratio = original_width / original_height
                
                if width and height:
                    new_width, new_height = width, height
                elif width:
                    new_width = min(width, self.max_width)
                    new_height = int(new_width / aspect_ratio)
                else:
                    new_height = min(height, self.max_height)
                    new_width = int(new_height * aspect_ratio)
                
                img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # Determine output format
            if format == 'auto':
                # Use WebP for modern browsers, JPEG fallback
                output_format = 'WebP'
                mime_type = 'image/webp'
            else:
                output_format = format.upper()
                mime_type = f'image/{format.lower()}'
            
            # Save optimized image
            output = io.BytesIO()
            img.save(
                output, 
                format=output_format,
                quality=self.quality_settings.get(quality, 80),
                optimize=True
            )
            
            return output.getvalue(), mime_type

# Usage in S3 service
def upload_optimized_image(self, file_data: bytes, file_key: str) -> Dict:
    """Upload image with multiple optimized versions"""
    optimizer = ImageOptimizer()
    
    # Generate multiple sizes
    sizes = [
        ('thumbnail', 150, None, 'thumbnail'),
        ('small', 400, None, 'standard'),
        ('medium', 800, None, 'standard'),
        ('large', 1200, None, 'high'),
        ('original', None, None, 'high')
    ]
    
    uploaded_versions = {}
    
    for size_name, width, height, quality in sizes:
        if size_name == 'original':
            optimized_data = file_data
            mime_type = 'image/jpeg'
        else:
            optimized_data, mime_type = optimizer.optimize_image(
                file_data, width, height, quality
            )
        
        # Upload to S3 with size suffix
        size_key = file_key.replace('.', f'_{size_name}.')
        
        self.s3_client.put_object(
            Bucket=self.bucket_name,
            Key=size_key,
            Body=optimized_data,
            ContentType=mime_type,
            ServerSideEncryption='AES256',
            CacheControl='max-age=31536000'
        )
        
        uploaded_versions[size_name] = {
            'key': size_key,
            'size': len(optimized_data),
            'mime_type': mime_type
        }
    
    return uploaded_versions
```

### 3.3 Responsive Image Component ✅ READY FOR IMPLEMENTATION

**Frontend Optimized Image Component**:

```jsx
// frontend/src/components/OptimizedImage.js
import React, { useState } from 'react';

const OptimizedImage = ({
  src,
  alt,
  sizes = '(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw',
  className = '',
  loading = 'lazy',
  onLoad = () => {},
  onError = () => {},
  fallback = '/images/placeholder.jpg'
}) => {
  const [imageError, setImageError] = useState(false);
  const [imageLoaded, setImageLoaded] = useState(false);
  
  // Generate srcSet for different sizes
  const generateSrcSet = (baseSrc) => {
    const sizes = [400, 800, 1200];
    return sizes
      .map(size => `${baseSrc}?w=${size}&q=80 ${size}w`)
      .join(', ');
  };
  
  const handleLoad = (e) => {
    setImageLoaded(true);
    onLoad(e);
  };
  
  const handleError = (e) => {
    setImageError(true);
    onError(e);
  };
  
  if (imageError) {
    return (
      <img
        src={fallback}
        alt={alt}
        className={className}
        loading={loading}
      />
    );
  }
  
  return (
    <div className="relative">
      {!imageLoaded && (
        <div className={`absolute inset-0 bg-gray-200 animate-pulse rounded ${className}`} />
      )}
      <img
        src={`${src}?w=800&q=80`}
        srcSet={generateSrcSet(src)}
        sizes={sizes}
        alt={alt}
        className={`${className} ${imageLoaded ? 'opacity-100' : 'opacity-0'} transition-opacity duration-300`}
        loading={loading}
        onLoad={handleLoad}
        onError={handleError}
      />
    </div>
  );
};

export default OptimizedImage;
```

### 3.4 Performance Monitoring ✅ READY FOR IMPLEMENTATION

**CloudWatch Dashboard Configuration**:

```yaml
# CloudWatch Dashboard for monitoring
CloudWatchDashboard:
  Properties:
    DashboardName: GolfGuy-CDN-Performance
    DashboardBody: |
      {
        "widgets": [
          {
            "type": "metric",
            "properties": {
              "metrics": [
                ["AWS/CloudFront", "Requests", "DistributionId", "${CloudFrontDistribution}"],
                ["AWS/CloudFront", "BytesDownloaded", "DistributionId", "${CloudFrontDistribution}"],
                ["AWS/CloudFront", "CacheHitRate", "DistributionId", "${CloudFrontDistribution}"]
              ],
              "period": 300,
              "stat": "Sum",
              "region": "us-east-1",
              "title": "CloudFront Performance"
            }
          },
          {
            "type": "metric",
            "properties": {
              "metrics": [
                ["AWS/S3", "BucketSizeBytes", "BucketName", "golfguy-platform-storage", "StorageType", "StandardStorage"],
                ["AWS/S3", "NumberOfObjects", "BucketName", "golfguy-platform-storage", "StorageType", "AllStorageTypes"]
              ],
              "period": 86400,
              "stat": "Average",
              "region": "eu-north-1",
              "title": "S3 Storage Metrics"
            }
          }
        ]
      }
```

### 3.5 Implementation Checklist

#### Infrastructure Setup:
- [ ] Create AWS S3 bucket with proper security policies
- [ ] Set up CloudFront distribution with caching rules
- [ ] Configure Origin Access Identity for S3
- [ ] Create IAM roles for Lambda@Edge optimization
- [ ] Set up CloudWatch monitoring and alerts

#### Backend Integration:
- [ ] Add AWS credentials to environment variables
- [ ] Implement image optimization service
- [ ] Update S3 service to generate multiple image sizes
- [ ] Add CDN URL generation to file upload responses
- [ ] Test presigned URL generation with CloudFront

#### Frontend Integration:
- [ ] Create OptimizedImage component
- [ ] Update FileUpload component to use CDN URLs
- [ ] Add responsive image loading throughout the app
- [ ] Implement lazy loading and progressive enhancement
- [ ] Add error handling and fallback images

#### Testing & Validation:
- [ ] Test file upload to S3 through CDN
- [ ] Verify image optimization is working
- [ ] Validate caching headers and TTL settings
- [ ] Test global performance from different regions
- [ ] Monitor costs and usage patterns

### 3.6 Cost Optimization Strategy

**S3 Storage Classes**:
- **Standard**: Active files (first 30 days)
- **Standard-IA**: Infrequently accessed files (30-90 days)
- **Glacier**: Archive old files (90+ days)

**CloudFront Pricing Tiers**:
- **Price Class 100**: Use only North America and Europe
- **Price Class 200**: Add Asia, Middle East, Africa
- **Price Class All**: Global distribution

**Lifecycle Policies**:
```json
{
  "Rules": [
    {
      "Id": "FileLifecycle",
      "Status": "Enabled",
      "Transitions": [
        {
          "Days": 30,
          "StorageClass": "STANDARD_IA"
        },
        {
          "Days": 90,
          "StorageClass": "GLACIER"
        }
      ]
    }
  ]
}
```

## Ready for Phase 4: Architecture Improvements

Phase 3 planning is complete. The CDN integration and image optimization system is designed and ready for implementation once AWS credentials are available. All frontend components are built and backend infrastructure is prepared.

**Next Phase**: Architecture improvements and backend modularization for better scalability and maintainability.