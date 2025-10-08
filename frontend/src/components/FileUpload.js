import React, { useState, useRef, useCallback } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { Card, CardHeader, CardTitle, CardContent } from './ui/card';
import { Button } from './ui/button';
import { Progress } from './ui/progress';
import { Alert, AlertDescription } from './ui/alert';
import { Badge } from './ui/badge';
import { 
  Upload, 
  X, 
  File, 
  Image, 
  Video, 
  FileText,
  Check,
  AlertCircle,
  Download,
  Trash2,
  Eye
} from 'lucide-react';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

// File type icons
const getFileIcon = (fileName, size = 'w-4 h-4') => {
  const extension = fileName.split('.').pop()?.toLowerCase();
  
  if (['jpg', 'jpeg', 'png', 'gif', 'webp'].includes(extension)) {
    return <Image className={`${size} text-green-600`} />;
  } else if (['mp4', 'mov', 'avi', 'webm'].includes(extension)) {
    return <Video className={`${size} text-purple-600`} />;
  } else if (['pdf', 'doc', 'docx', 'txt'].includes(extension)) {
    return <FileText className={`${size} text-blue-600`} />;
  }
  return <File className={`${size} text-gray-600`} />;
};

// File size formatter
const formatFileSize = (bytes) => {
  if (bytes === 0) return '0 Bytes';
  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
};

const FileUpload = ({ 
  category = 'user-profiles',
  maxFiles = 5,
  maxSizeBytes = 50 * 1024 * 1024, // 50MB
  allowedExtensions = ['.jpg', '.jpeg', '.png', '.webp', '.pdf', '.doc', '.docx'],
  onUploadComplete = () => {},
  className = ''
}) => {
  const { token } = useAuth();
  const fileInputRef = useRef();
  
  const [dragActive, setDragActive] = useState(false);
  const [files, setFiles] = useState([]);
  const [uploadProgress, setUploadProgress] = useState({});
  const [errors, setErrors] = useState([]);

  // File validation
  const validateFile = (file) => {
    const errors = [];
    
    // Size check
    if (file.size > maxSizeBytes) {
      errors.push(`File "${file.name}" exceeds maximum size of ${formatFileSize(maxSizeBytes)}`);
    }
    
    // Extension check
    const extension = '.' + file.name.split('.').pop()?.toLowerCase();
    if (!allowedExtensions.includes(extension)) {
      errors.push(`File "${file.name}" has unsupported extension. Allowed: ${allowedExtensions.join(', ')}`);
    }
    
    return errors;
  };

  // Handle file selection
  const handleFiles = useCallback((selectedFiles) => {
    const fileArray = Array.from(selectedFiles);
    const newErrors = [];
    const validFiles = [];
    
    // Validate each file
    fileArray.forEach(file => {
      const fileErrors = validateFile(file);
      if (fileErrors.length > 0) {
        newErrors.push(...fileErrors);
      } else {
        validFiles.push({
          file,
          id: Math.random().toString(36).substr(2, 9),
          status: 'ready', // ready, uploading, completed, error
          progress: 0,
          uploadedData: null
        });
      }
    });
    
    // Check total file count
    if (files.length + validFiles.length > maxFiles) {
      newErrors.push(`Maximum ${maxFiles} files allowed`);
      return;
    }
    
    setErrors(newErrors);
    if (validFiles.length > 0) {
      setFiles(prev => [...prev, ...validFiles]);
    }
  }, [files.length, maxFiles, maxSizeBytes, allowedExtensions]);

  // Drag and drop handlers
  const handleDrag = useCallback((e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  }, []);

  const handleDrop = useCallback((e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFiles(e.dataTransfer.files);
    }
  }, [handleFiles]);

  // File input change
  const handleInputChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      handleFiles(e.target.files);
    }
  };

  // Upload single file
  const uploadFile = async (fileObj) => {
    const formData = new FormData();
    formData.append('file', fileObj.file);
    formData.append('category', category);
    
    try {
      setFiles(prev => prev.map(f => 
        f.id === fileObj.id 
          ? { ...f, status: 'uploading', progress: 0 }
          : f
      ));
      
      const response = await axios.post(`${API}/files/upload`, formData, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'multipart/form-data'
        },
        onUploadProgress: (progressEvent) => {
          const progress = Math.round((progressEvent.loaded * 100) / progressEvent.total);
          setFiles(prev => prev.map(f => 
            f.id === fileObj.id 
              ? { ...f, progress }
              : f
          ));
        }
      });
      
      // Update file status
      setFiles(prev => prev.map(f => 
        f.id === fileObj.id 
          ? { 
              ...f, 
              status: 'completed', 
              progress: 100,
              uploadedData: response.data 
            }
          : f
      ));
      
      onUploadComplete(response.data);
      
    } catch (error) {
      console.error('Upload error:', error);
      setFiles(prev => prev.map(f => 
        f.id === fileObj.id 
          ? { ...f, status: 'error', progress: 0 }
          : f
      ));
      
      const errorMessage = error.response?.data?.detail || 'Upload failed';
      setErrors(prev => [...prev, `Upload failed for "${fileObj.file.name}": ${errorMessage}`]);
    }
  };

  // Upload all files
  const uploadAllFiles = async () => {
    const readyFiles = files.filter(f => f.status === 'ready');
    
    for (const file of readyFiles) {
      await uploadFile(file);
    }
  };

  // Remove file
  const removeFile = (fileId) => {
    setFiles(prev => prev.filter(f => f.id !== fileId));
  };

  // Clear errors
  const clearErrors = () => {
    setErrors([]);
  };

  return (
    <Card className={className}>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Upload className="w-5 h-5" />
          File Upload
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        
        {/* Upload Area */}
        <div
          className={`
            border-2 border-dashed rounded-lg p-8 text-center transition-colors
            ${dragActive 
              ? 'border-emerald-500 bg-emerald-50' 
              : 'border-gray-300 hover:border-gray-400'
            }
          `}
          onDragEnter={handleDrag}
          onDragLeave={handleDrag}
          onDragOver={handleDrag}
          onDrop={handleDrop}
        >
          <Upload className="w-12 h-12 text-gray-400 mx-auto mb-4" />
          <p className="text-lg font-medium text-gray-900 mb-2">
            Drop files here or click to upload
          </p>
          <p className="text-sm text-gray-500 mb-4">
            Supports: {allowedExtensions.join(', ')} (Max {formatFileSize(maxSizeBytes)})
          </p>
          <Button
            type="button"
            variant="outline"
            onClick={() => fileInputRef.current?.click()}
          >
            Choose Files
          </Button>
          <input
            ref={fileInputRef}
            type="file"
            multiple
            className="hidden"
            accept={allowedExtensions.join(',')}
            onChange={handleInputChange}
          />
        </div>

        {/* Error Messages */}
        {errors.length > 0 && (
          <Alert variant="destructive">
            <AlertCircle className="h-4 w-4" />
            <AlertDescription>
              <div className="space-y-1">
                {errors.map((error, index) => (
                  <div key={index}>{error}</div>
                ))}
              </div>
              <Button 
                variant="ghost" 
                size="sm" 
                className="mt-2"
                onClick={clearErrors}
              >
                Dismiss
              </Button>
            </AlertDescription>
          </Alert>
        )}

        {/* File List */}
        {files.length > 0 && (
          <div className="space-y-2">
            <div className="flex items-center justify-between">
              <h4 className="font-medium">Files ({files.length}/{maxFiles})</h4>
              <Button
                onClick={uploadAllFiles}
                disabled={files.filter(f => f.status === 'ready').length === 0}
                size="sm"
                className="bg-emerald-600 hover:bg-emerald-700"
              >
                Upload All
              </Button>
            </div>
            
            <div className="space-y-2">
              {files.map((fileObj) => (
                <div
                  key={fileObj.id}
                  className="flex items-center gap-3 p-3 bg-gray-50 rounded-lg"
                >
                  {/* File Icon */}
                  {getFileIcon(fileObj.file.name)}
                  
                  {/* File Info */}
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium text-gray-900 truncate">
                      {fileObj.file.name}
                    </p>
                    <p className="text-xs text-gray-500">
                      {formatFileSize(fileObj.file.size)}
                    </p>
                    
                    {/* Progress Bar */}
                    {fileObj.status === 'uploading' && (
                      <Progress value={fileObj.progress} className="h-2 mt-1" />
                    )}
                  </div>
                  
                  {/* Status Badge */}
                  <div className="flex items-center gap-2">
                    {fileObj.status === 'ready' && (
                      <Badge variant="outline">Ready</Badge>
                    )}
                    {fileObj.status === 'uploading' && (
                      <Badge variant="secondary">
                        Uploading {fileObj.progress}%
                      </Badge>
                    )}
                    {fileObj.status === 'completed' && (
                      <Badge variant="default" className="bg-green-100 text-green-800">
                        <Check className="w-3 h-3 mr-1" />
                        Complete
                      </Badge>
                    )}
                    {fileObj.status === 'error' && (
                      <Badge variant="destructive">
                        <AlertCircle className="w-3 h-3 mr-1" />
                        Error
                      </Badge>
                    )}
                    
                    {/* Action Buttons */}
                    {fileObj.status === 'completed' && fileObj.uploadedData && (
                      <div className="flex gap-1">
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() => window.open(fileObj.uploadedData.file_url, '_blank')}
                          title="View file"
                        >
                          <Eye className="w-4 h-4" />
                        </Button>
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() => {
                            const link = document.createElement('a');
                            link.href = fileObj.uploadedData.file_url;
                            link.download = fileObj.uploadedData.original_filename;
                            document.body.appendChild(link);
                            link.click();
                            document.body.removeChild(link);
                          }}
                          title="Download file"
                        >
                          <Download className="w-4 h-4" />
                        </Button>
                      </div>
                    )}
                    
                    {/* Remove Button */}
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => removeFile(fileObj.id)}
                      title="Remove file"
                    >
                      <X className="w-4 h-4" />
                    </Button>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </CardContent>
    </Card>
  );
};

export default FileUpload;