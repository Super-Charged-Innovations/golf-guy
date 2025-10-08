import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { Card, CardHeader, CardTitle, CardContent } from './ui/card';
import { Button } from './ui/button';
import { Badge } from './ui/badge';
import { Alert, AlertDescription } from './ui/alert';
import { Input } from './ui/input';
import { Label } from './ui/label';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from './ui/select';
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from './ui/dialog';
import { 
  Files,
  Search,
  Filter,
  Download,
  Trash2,
  Eye,
  Calendar,
  HardDrive,
  Image,
  FileText,
  Video,
  AlertCircle,
  RefreshCw,
  Upload
} from 'lucide-react';
import axios from 'axios';
import { formatDistanceToNow } from 'date-fns';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

// File type icons (reuse from FileUpload)
const getFileIcon = (fileName, size = 'w-5 h-5') => {
  const extension = fileName.split('.').pop()?.toLowerCase();
  
  if (['jpg', 'jpeg', 'png', 'gif', 'webp'].includes(extension)) {
    return <Image className={`${size} text-green-600`} />;
  } else if (['mp4', 'mov', 'avi', 'webm'].includes(extension)) {
    return <Video className={`${size} text-purple-600`} />;
  } else if (['pdf', 'doc', 'docx', 'txt'].includes(extension)) {
    return <FileText className={`${size} text-blue-600`} />;
  }
  return <Files className={`${size} text-gray-600`} />;
};

// Format file size
const formatFileSize = (bytes) => {
  if (!bytes || bytes === 0) return '0 Bytes';
  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
};

const FileManager = ({ 
  allowedCategories = ['user-profiles', 'kyc-documents'],
  showUploadButton = true,
  className = ''
}) => {
  const { token, user } = useAuth();
  
  const [files, setFiles] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [selectedCategory, setSelectedCategory] = useState(allowedCategories[0] || '');
  const [searchTerm, setSearchTerm] = useState('');
  const [sortBy, setSortBy] = useState('date_desc');
  
  // Available categories based on user permissions
  const categories = {
    'user-profiles': { label: 'Profile Images', icon: <Image className="w-4 h-4" /> },
    'kyc-documents': { label: 'KYC Documents', icon: <FileText className="w-4 h-4" /> },
    'gdpr-exports': { label: 'Data Exports', icon: <Download className="w-4 h-4" /> },
    'destination-images': { label: 'Destination Media', icon: <Image className="w-4 h-4" />, adminOnly: true },
    'admin-content': { label: 'Admin Content', icon: <Files className="w-4 h-4" />, adminOnly: true }
  };

  // Filter categories based on user permissions
  const availableCategories = Object.entries(categories).filter(([key, category]) => {
    if (category.adminOnly && !user?.is_admin) return false;
    return allowedCategories.includes(key);
  });

  // Load files for selected category
  const loadFiles = async (category = selectedCategory) => {
    if (!category) return;
    
    setLoading(true);
    setError('');
    
    try {
      const response = await axios.get(`${API}/files/list`, {
        params: { category },
        headers: { Authorization: `Bearer ${token}` }
      });
      
      setFiles(response.data.files || []);
    } catch (err) {
      console.error('Error loading files:', err);
      setError(err.response?.data?.detail || 'Failed to load files');
    } finally {
      setLoading(false);
    }
  };

  // Delete file
  const deleteFile = async (fileKey, fileName) => {
    if (!confirm(`Are you sure you want to delete "${fileName}"? This action cannot be undone.`)) {
      return;
    }
    
    try {
      await axios.delete(`${API}/files/${encodeURIComponent(fileKey)}`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      
      // Reload files
      loadFiles();
    } catch (err) {
      console.error('Error deleting file:', err);
      setError(err.response?.data?.detail || 'Failed to delete file');
    }
  };

  // Generate download URL
  const downloadFile = async (fileKey, fileName) => {
    try {
      const response = await axios.get(`${API}/files/${encodeURIComponent(fileKey)}/download`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      
      // Open presigned URL in new tab
      window.open(response.data.presigned_url, '_blank');
    } catch (err) {
      console.error('Error generating download URL:', err);
      setError(err.response?.data?.detail || 'Failed to generate download link');
    }
  };

  // Filter and sort files
  const filteredFiles = files
    .filter(file => {
      if (!searchTerm) return true;
      const fileName = file.metadata?.original_filename || file.file_key;
      return fileName.toLowerCase().includes(searchTerm.toLowerCase());
    })
    .sort((a, b) => {
      switch (sortBy) {
        case 'name_asc':
          return (a.metadata?.original_filename || a.file_key).localeCompare(
            b.metadata?.original_filename || b.file_key
          );
        case 'name_desc':
          return (b.metadata?.original_filename || b.file_key).localeCompare(
            a.metadata?.original_filename || a.file_key
          );
        case 'size_asc':
          return a.file_size - b.file_size;
        case 'size_desc':
          return b.file_size - a.file_size;
        case 'date_asc':
          return new Date(a.last_modified) - new Date(b.last_modified);
        case 'date_desc':
        default:
          return new Date(b.last_modified) - new Date(a.last_modified);
      }
    });

  // Load files when category changes
  useEffect(() => {
    if (selectedCategory) {
      loadFiles(selectedCategory);
    }
  }, [selectedCategory]);

  // Initial load
  useEffect(() => {
    if (availableCategories.length > 0 && !selectedCategory) {
      setSelectedCategory(availableCategories[0][0]);
    }
  }, [availableCategories.length]);

  return (
    <Card className={className}>
      <CardHeader>
        <div className="flex items-center justify-between">
          <CardTitle className="flex items-center gap-2">
            <Files className="w-5 h-5" />
            File Manager
          </CardTitle>
          <div className="flex items-center gap-2">
            <Button
              variant="outline"
              size="sm"
              onClick={() => loadFiles()}
              disabled={loading}
            >
              <RefreshCw className={`w-4 h-4 mr-2 ${loading ? 'animate-spin' : ''}`} />
              Refresh
            </Button>
            {showUploadButton && (
              <Dialog>
                <DialogTrigger asChild>
                  <Button size="sm" className="bg-emerald-600 hover:bg-emerald-700">
                    <Upload className="w-4 h-4 mr-2" />
                    Upload
                  </Button>
                </DialogTrigger>
                <DialogContent className="max-w-2xl">
                  <DialogHeader>
                    <DialogTitle>Upload Files</DialogTitle>
                  </DialogHeader>
                  {/* FileUpload component would be imported and used here */}
                  <div className="p-4 border-2 border-dashed border-gray-300 rounded-lg text-center">
                    <p className="text-gray-500">FileUpload component would go here</p>
                    <p className="text-sm text-gray-400 mt-1">
                      Category: {categories[selectedCategory]?.label}
                    </p>
                  </div>
                </DialogContent>
              </Dialog>
            )}
          </div>
        </div>
      </CardHeader>
      
      <CardContent className="space-y-6">
        {/* Category Selection and Filters */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <Label htmlFor="category">Category</Label>
            <Select value={selectedCategory} onValueChange={setSelectedCategory}>
              <SelectTrigger>
                <SelectValue placeholder="Select category" />
              </SelectTrigger>
              <SelectContent>
                {availableCategories.map(([key, category]) => (
                  <SelectItem key={key} value={key}>
                    <div className="flex items-center gap-2">
                      {category.icon}
                      {category.label}
                    </div>
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
          
          <div>
            <Label htmlFor="search">Search Files</Label>
            <div className="relative">
              <Search className="absolute left-3 top-3 w-4 h-4 text-gray-400" />
              <Input
                id="search"
                placeholder="Search by filename..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="pl-10"
              />
            </div>
          </div>
          
          <div>
            <Label htmlFor="sort">Sort By</Label>
            <Select value={sortBy} onValueChange={setSortBy}>
              <SelectTrigger>
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="date_desc">Date (Newest First)</SelectItem>
                <SelectItem value="date_asc">Date (Oldest First)</SelectItem>
                <SelectItem value="name_asc">Name (A-Z)</SelectItem>
                <SelectItem value="name_desc">Name (Z-A)</SelectItem>
                <SelectItem value="size_asc">Size (Smallest First)</SelectItem>
                <SelectItem value="size_desc">Size (Largest First)</SelectItem>
              </SelectContent>
            </Select>
          </div>
        </div>

        {/* Error Alert */}
        {error && (
          <Alert variant="destructive">
            <AlertCircle className="h-4 w-4" />
            <AlertDescription>{error}</AlertDescription>
          </Alert>
        )}

        {/* Files List */}
        <div className="space-y-2">
          {loading ? (
            <div className="flex items-center justify-center p-8">
              <RefreshCw className="w-6 h-6 animate-spin text-gray-400 mr-2" />
              <span className="text-gray-500">Loading files...</span>
            </div>
          ) : filteredFiles.length === 0 ? (
            <div className="text-center p-8 text-gray-500">
              <Files className="w-12 h-12 mx-auto mb-4 text-gray-300" />
              <p className="text-lg font-medium">No files found</p>
              <p className="text-sm">
                {searchTerm 
                  ? 'Try adjusting your search terms' 
                  : 'Upload some files to get started'
                }
              </p>
            </div>
          ) : (
            <div className="space-y-2">
              <div className="flex items-center gap-2 text-sm text-gray-600 pb-2 border-b">
                <HardDrive className="w-4 h-4" />
                <span>{filteredFiles.length} files</span>
                <span>•</span>
                <span>
                  {formatFileSize(filteredFiles.reduce((sum, file) => sum + (file.file_size || 0), 0))} total
                </span>
              </div>
              
              {filteredFiles.map((file) => {
                const fileName = file.metadata?.original_filename || file.file_key.split('/').pop();
                const uploadDate = new Date(file.last_modified);
                
                return (
                  <div key={file.file_key} className="flex items-center gap-4 p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors">
                    {/* File Icon */}
                    <div className="flex-shrink-0">
                      {getFileIcon(fileName)}
                    </div>
                    
                    {/* File Info */}
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-2">
                        <p className="font-medium text-gray-900 truncate">
                          {fileName}
                        </p>
                        {file.metadata?.category && (
                          <Badge variant="outline" className="text-xs">
                            {categories[file.metadata.category]?.label || file.metadata.category}
                          </Badge>
                        )}
                      </div>
                      
                      <div className="flex items-center gap-4 mt-1 text-sm text-gray-500">
                        <span className="flex items-center gap-1">
                          <HardDrive className="w-3 h-3" />
                          {formatFileSize(file.file_size)}
                        </span>
                        <span className="flex items-center gap-1">
                          <Calendar className="w-3 h-3" />
                          {formatDistanceToNow(uploadDate, { addSuffix: true })}
                        </span>
                        {file.content_type && (
                          <span className="text-xs text-gray-400">
                            {file.content_type}
                          </span>
                        )}
                      </div>
                    </div>
                    
                    {/* Action Buttons */}
                    <div className="flex items-center gap-2">
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => downloadFile(file.file_key, fileName)}
                        title="Download file"
                      >
                        <Download className="w-4 h-4" />
                      </Button>
                      
                      <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => deleteFile(file.file_key, fileName)}
                        title="Delete file"
                        className="text-red-600 hover:text-red-700 hover:bg-red-50"
                      >
                        <Trash2 className="w-4 h-4" />
                      </Button>
                    </div>
                  </div>
                );
              })}
            </div>
          )}
        </div>
      </CardContent>
    </Card>
  );
};

export default FileManager;