import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useAuth } from '../contexts/AuthContext';
import { useNavigate } from 'react-router-dom';
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { Label } from '../components/ui/label';
import { Switch } from '../components/ui/switch';
import { Alert, AlertDescription } from '../components/ui/alert';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription, DialogFooter } from '../components/ui/dialog';
import { Textarea } from '../components/ui/textarea';
import { toast } from 'sonner';
import { 
  Shield, 
  Download, 
  Trash2, 
  AlertTriangle,
  CheckCircle2,
  Lock,
  Eye,
  Mail,
  BarChart,
  Cookie,
  Users,
  Loader2
} from 'lucide-react';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

export default function PrivacySettings() {
  const { isAuthenticated, token, logout } = useAuth();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [settings, setSettings] = useState({
    marketing_emails: false,
    analytics_tracking: true,
    cookie_consent: false,
    data_sharing: false
  });
  
  const [showExportDialog, setShowExportDialog] = useState(false);
  const [showDeleteDialog, setShowDeleteDialog] = useState(false);
  const [deleteReason, setDeleteReason] = useState('');
  const [exportData, setExportData] = useState(null);

  useEffect(() => {
    if (!isAuthenticated) {
      navigate('/login');
      return;
    }
    loadPrivacySettings();
  }, [isAuthenticated]);

  const loadPrivacySettings = async () => {
    try {
      const response = await axios.get(`${API}/privacy/settings`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setSettings(response.data);
    } catch (error) {
      console.error('Failed to load privacy settings:', error);
      toast.error('Failed to load privacy settings');
    } finally {
      setLoading(false);
    }
  };

  const handleSettingChange = (key, value) => {
    setSettings(prev => ({ ...prev, [key]: value }));
  };

  const handleSaveSettings = async () => {
    setSaving(true);
    try {
      await axios.put(
        `${API}/privacy/settings`,
        settings,
        { headers: { Authorization: `Bearer ${token}` } }
      );
      toast.success('Privacy settings updated successfully');
    } catch (error) {
      console.error('Failed to save settings:', error);
      toast.error('Failed to save privacy settings');
    } finally {
      setSaving(false);
    }
  };

  const handleDataExport = async () => {
    try {
      const response = await axios.post(
        `${API}/privacy/export-data`,
        {},
        { headers: { Authorization: `Bearer ${token}` } }
      );
      setExportData(response.data.data);
      
      // Create downloadable JSON file
      const dataStr = JSON.stringify(response.data.data, null, 2);
      const dataBlob = new Blob([dataStr], { type: 'application/json' });
      const url = URL.createObjectURL(dataBlob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `golf-guy-data-export-${new Date().toISOString().split('T')[0]}.json`;
      link.click();
      
      toast.success('Your data has been exported successfully');
      setShowExportDialog(false);
    } catch (error) {
      console.error('Failed to export data:', error);
      toast.error('Failed to export data');
    }
  };

  const handleDeleteAccount = async () => {
    try {
      await axios.post(
        `${API}/privacy/delete-account`,
        { reason: deleteReason },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      
      toast.success('Account deletion request submitted. You will be logged out.');
      setTimeout(() => {
        logout();
        navigate('/');
      }, 2000);
    } catch (error) {
      console.error('Failed to request deletion:', error);
      toast.error('Failed to request account deletion');
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-b from-emerald-50/30 to-white">
        <Loader2 className="h-12 w-12 animate-spin text-emerald-600" />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-emerald-50/30 to-white py-12">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="mb-8 animate-fade-in-up">
          <div className="flex items-center gap-3 mb-2">
            <div className="p-3 rounded-full bg-emerald-100">
              <Shield className="h-6 w-6 text-emerald-600" />
            </div>
            <div>
              <h1 className="text-3xl font-bold text-gray-900">Privacy & Data</h1>
              <p className="text-gray-600">Manage your privacy preferences and data</p>
            </div>
          </div>
        </div>

        {/* GDPR Notice */}
        <Alert className="mb-6 border-blue-200 bg-blue-50 animate-fade-in-up animate-delay-100">
          <Lock className="h-4 w-4 text-blue-600" />
          <AlertDescription className="text-sm text-blue-900">
            We comply with GDPR and Swedish data protection laws. Your data is encrypted and stored securely. 
            You have the right to access, export, and delete your personal data at any time.
          </AlertDescription>
        </Alert>

        {/* Privacy Controls */}
        <Card className="mb-6 animate-fade-in-up animate-delay-200 border-emerald-100">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Eye className="h-5 w-5 text-emerald-600" />
              Privacy Controls
            </CardTitle>
            <CardDescription>
              Control how your data is used and shared
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">
            {/* Marketing Emails */}
            <div 
              className="flex items-center justify-between p-4 rounded-lg border border-gray-200 hover:border-emerald-300 hover:bg-emerald-50/30 transition-all cursor-pointer group"
              onClick={() => handleSettingChange('marketing_emails', !settings.marketing_emails)}
              role="button"
              tabIndex={0}
              onKeyDown={(e) => {
                if (e.key === 'Enter' || e.key === ' ') {
                  e.preventDefault();
                  handleSettingChange('marketing_emails', !settings.marketing_emails);
                }
              }}
            >
              <div className="flex items-start gap-3 flex-1 pointer-events-none">
                <Mail className="h-5 w-5 text-emerald-600 mt-1 group-hover:scale-110 transition-transform" />
                <div>
                  <Label className="text-base font-medium cursor-pointer">Marketing Emails</Label>
                  <p className="text-sm text-gray-600 mt-1">
                    Receive promotional emails, special offers, and travel inspiration
                  </p>
                </div>
              </div>
              <Switch
                checked={settings.marketing_emails}
                onCheckedChange={(checked) => handleSettingChange('marketing_emails', checked)}
                onClick={(e) => e.stopPropagation()}
                className="pointer-events-auto"
              />
            </div>

            {/* Analytics Tracking */}
            <div 
              className="flex items-center justify-between p-4 rounded-lg border border-gray-200 hover:border-emerald-300 hover:bg-emerald-50/30 transition-all cursor-pointer group"
              onClick={() => handleSettingChange('analytics_tracking', !settings.analytics_tracking)}
              role="button"
              tabIndex={0}
              onKeyDown={(e) => {
                if (e.key === 'Enter' || e.key === ' ') {
                  e.preventDefault();
                  handleSettingChange('analytics_tracking', !settings.analytics_tracking);
                }
              }}
            >
              <div className="flex items-start gap-3 flex-1 pointer-events-none">
                <BarChart className="h-5 w-5 text-emerald-600 mt-1 group-hover:scale-110 transition-transform" />
                <div>
                  <Label className="text-base font-medium cursor-pointer">Analytics Tracking</Label>
                  <p className="text-sm text-gray-600 mt-1">
                    Help us improve by allowing anonymous usage analytics
                  </p>
                </div>
              </div>
              <Switch
                checked={settings.analytics_tracking}
                onCheckedChange={(checked) => handleSettingChange('analytics_tracking', checked)}
                onClick={(e) => e.stopPropagation()}
                className="pointer-events-auto"
              />
            </div>

            {/* Cookie Consent */}
            <div 
              className="flex items-center justify-between p-4 rounded-lg border border-gray-200 hover:border-emerald-300 hover:bg-emerald-50/30 transition-all cursor-pointer group"
              onClick={() => handleSettingChange('cookie_consent', !settings.cookie_consent)}
              role="button"
              tabIndex={0}
              onKeyDown={(e) => {
                if (e.key === 'Enter' || e.key === ' ') {
                  e.preventDefault();
                  handleSettingChange('cookie_consent', !settings.cookie_consent);
                }
              }}
            >
              <div className="flex items-start gap-3 flex-1 pointer-events-none">
                <Cookie className="h-5 w-5 text-emerald-600 mt-1 group-hover:scale-110 transition-transform" />
                <div>
                  <Label className="text-base font-medium cursor-pointer">Cookie Consent</Label>
                  <p className="text-sm text-gray-600 mt-1">
                    Allow non-essential cookies for enhanced functionality
                  </p>
                </div>
              </div>
              <Switch
                checked={settings.cookie_consent}
                onCheckedChange={(checked) => handleSettingChange('cookie_consent', checked)}
                onClick={(e) => e.stopPropagation()}
                className="pointer-events-auto"
              />
            </div>

            {/* Data Sharing */}
            <div 
              className="flex items-center justify-between p-4 rounded-lg border border-gray-200 hover:border-emerald-300 hover:bg-emerald-50/30 transition-all cursor-pointer group"
              onClick={() => handleSettingChange('data_sharing', !settings.data_sharing)}
              role="button"
              tabIndex={0}
              onKeyDown={(e) => {
                if (e.key === 'Enter' || e.key === ' ') {
                  e.preventDefault();
                  handleSettingChange('data_sharing', !settings.data_sharing);
                }
              }}
            >
              <div className="flex items-start gap-3 flex-1 pointer-events-none">
                <Users className="h-5 w-5 text-emerald-600 mt-1 group-hover:scale-110 transition-transform" />
                <div>
                  <Label className="text-base font-medium cursor-pointer">Data Sharing with Partners</Label>
                  <p className="text-sm text-gray-600 mt-1">
                    Share data with trusted golf course and hotel partners for bookings
                  </p>
                </div>
              </div>
              <Switch
                checked={settings.data_sharing}
                onCheckedChange={(checked) => handleSettingChange('data_sharing', checked)}
                onClick={(e) => e.stopPropagation()}
                className="pointer-events-auto"
              />
            </div>

            <div className="pt-4">
              <Button 
                onClick={handleSaveSettings}
                disabled={saving}
                className="w-full bg-emerald-600 hover:bg-emerald-700"
              >
                {saving ? (
                  <>
                    <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                    Saving...
                  </>
                ) : (
                  <>
                    <CheckCircle2 className="h-4 w-4 mr-2" />
                    Save Privacy Settings
                  </>
                )}
              </Button>
            </div>
          </CardContent>
        </Card>

        {/* GDPR Rights */}
        <Card className="animate-fade-in-up animate-delay-300 border-emerald-100">
          <CardHeader>
            <CardTitle>Your GDPR Rights</CardTitle>
            <CardDescription>
              Under EU and Swedish law, you have specific rights regarding your personal data
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            {/* Data Export */}
            <div className="p-4 rounded-lg border border-gray-200 hover:border-emerald-200 transition-colors">
              <div className="flex items-start justify-between mb-2">
                <div className="flex items-start gap-3">
                  <Download className="h-5 w-5 text-blue-600 mt-1" />
                  <div>
                    <h3 className="font-medium">Export Your Data</h3>
                    <p className="text-sm text-gray-600 mt-1">
                      Download all your personal data in JSON format (GDPR Article 20)
                    </p>
                  </div>
                </div>
              </div>
              <Button 
                variant="outline"
                onClick={() => setShowExportDialog(true)}
                className="mt-3 border-blue-200 text-blue-700 hover:bg-blue-50"
              >
                <Download className="h-4 w-4 mr-2" />
                Request Data Export
              </Button>
            </div>

            {/* Account Deletion */}
            <div className="p-4 rounded-lg border border-red-200 bg-red-50/30">
              <div className="flex items-start justify-between mb-2">
                <div className="flex items-start gap-3">
                  <Trash2 className="h-5 w-5 text-red-600 mt-1" />
                  <div>
                    <h3 className="font-medium text-red-900">Delete Your Account</h3>
                    <p className="text-sm text-red-700 mt-1">
                      Permanently delete your account and all associated data (GDPR Article 17)
                    </p>
                  </div>
                </div>
              </div>
              <Button 
                variant="outline"
                onClick={() => setShowDeleteDialog(true)}
                className="mt-3 border-red-300 text-red-700 hover:bg-red-100"
              >
                <Trash2 className="h-4 w-4 mr-2" />
                Request Account Deletion
              </Button>
            </div>
          </CardContent>
        </Card>

        {/* Export Dialog */}
        <Dialog open={showExportDialog} onOpenChange={setShowExportDialog}>
          <DialogContent>
            <DialogHeader>
              <DialogTitle>Export Your Data</DialogTitle>
              <DialogDescription>
                We'll generate a complete export of your personal data in JSON format. 
                This includes your profile, preferences, inquiries, and privacy settings.
              </DialogDescription>
            </DialogHeader>
            <Alert className="border-blue-200 bg-blue-50">
              <Lock className="h-4 w-4 text-blue-600" />
              <AlertDescription className="text-sm text-blue-900">
                Your data export will be encrypted and only accessible by you.
              </AlertDescription>
            </Alert>
            <DialogFooter>
              <Button variant="outline" onClick={() => setShowExportDialog(false)}>
                Cancel
              </Button>
              <Button onClick={handleDataExport} className="bg-blue-600 hover:bg-blue-700">
                <Download className="h-4 w-4 mr-2" />
                Download My Data
              </Button>
            </DialogFooter>
          </DialogContent>
        </Dialog>

        {/* Delete Dialog */}
        <Dialog open={showDeleteDialog} onOpenChange={setShowDeleteDialog}>
          <DialogContent>
            <DialogHeader>
              <DialogTitle className="flex items-center gap-2 text-red-900">
                <AlertTriangle className="h-5 w-5" />
                Delete Account
              </DialogTitle>
              <DialogDescription>
                This action cannot be undone. Your account and all associated data will be permanently deleted 
                after a 7-day review period, in compliance with GDPR requirements.
              </DialogDescription>
            </DialogHeader>
            <div className="space-y-4">
              <Alert className="border-red-200 bg-red-50">
                <AlertTriangle className="h-4 w-4 text-red-600" />
                <AlertDescription className="text-sm text-red-900">
                  <strong>Warning:</strong> This will delete:
                  <ul className="list-disc list-inside mt-2 space-y-1">
                    <li>Your profile and preferences</li>
                    <li>Travel history and inquiries</li>
                    <li>Saved destinations and recommendations</li>
                    <li>All account data</li>
                  </ul>
                </AlertDescription>
              </Alert>
              <div>
                <Label>Reason for deletion (optional)</Label>
                <Textarea
                  value={deleteReason}
                  onChange={(e) => setDeleteReason(e.target.value)}
                  placeholder="Help us improve by sharing why you're leaving..."
                  rows={3}
                  className="mt-2"
                />
              </div>
            </div>
            <DialogFooter>
              <Button variant="outline" onClick={() => setShowDeleteDialog(false)}>
                Cancel
              </Button>
              <Button 
                onClick={handleDeleteAccount}
                className="bg-red-600 hover:bg-red-700 text-white"
              >
                <Trash2 className="h-4 w-4 mr-2" />
                Request Deletion
              </Button>
            </DialogFooter>
          </DialogContent>
        </Dialog>
      </div>
    </div>
  );
}
