import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useAuth } from '../contexts/AuthContext';
import { useNavigate } from 'react-router-dom';
import { Button } from '../components/ui/button';
import { Input } from '../components/ui/input';
import { Label } from '../components/ui/label';
import { Textarea } from '../components/ui/textarea';
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '../components/ui/card';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '../components/ui/select';
import { Badge } from '../components/ui/badge';
import { toast } from 'sonner';
import FileUpload from '../components/FileUpload';
import { 
  User, 
  DollarSign, 
  Globe, 
  TrendingUp, 
  Calendar,
  Users as UsersIcon,
  Utensils,
  Award,
  CheckCircle2,
  Loader2,
  FileText
} from 'lucide-react';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const COUNTRIES = [
  'Spain', 'Portugal', 'Scotland', 'Ireland', 'England', 'France', 
  'Italy', 'Turkey', 'Morocco', 'Dubai', 'Thailand', 'Mauritius', 'South Africa'
];

const TRAVEL_MONTHS = [
  'January', 'February', 'March', 'April', 'May', 'June',
  'July', 'August', 'September', 'October', 'November', 'December'
];

export default function ProfileKYC() {
  const { isAuthenticated, token, user } = useAuth();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [tierStatus, setTierStatus] = useState(null);
  const [formData, setFormData] = useState({
    // Basic Info (Tier 1)
    budget_min: 0,
    budget_max: 50000,
    preferred_countries: [],
    playing_level: 'Intermediate',
    accommodation_preference: 'Any',
    trip_duration_days: null,
    group_size: null,
    
    // Enhanced Info (Tier 2)
    phone_number: '',
    travel_frequency: '',
    preferred_travel_months: [],
    
    // Advanced Info (Tier 3)
    dietary_requirements: '',
    special_requests: '',
    previous_golf_destinations: [],
    handicap: null
  });

  useEffect(() => {
    if (!isAuthenticated) {
      navigate('/login');
      return;
    }
    loadProfile();
  }, [isAuthenticated]);

  const loadProfile = async () => {
    try {
      const [profileRes, tierRes] = await Promise.all([
        axios.get(`${API}/profile`, {
          headers: { Authorization: `Bearer ${token}` }
        }),
        axios.get(`${API}/profile/tier-status`, {
          headers: { Authorization: `Bearer ${token}` }
        })
      ]);

      const profile = profileRes.data;
      const prefs = profile.preferences || {};
      
      setFormData({
        budget_min: prefs.budget_min || 0,
        budget_max: prefs.budget_max || 50000,
        preferred_countries: prefs.preferred_countries || [],
        playing_level: prefs.playing_level || 'Intermediate',
        accommodation_preference: prefs.accommodation_preference || 'Any',
        trip_duration_days: prefs.trip_duration_days || null,
        group_size: prefs.group_size || null,
        phone_number: prefs.phone_number || '',
        travel_frequency: prefs.travel_frequency || '',
        preferred_travel_months: prefs.preferred_travel_months || [],
        dietary_requirements: prefs.dietary_requirements || '',
        special_requests: prefs.special_requests || '',
        previous_golf_destinations: prefs.previous_golf_destinations || [],
        handicap: prefs.handicap || null
      });

      setTierStatus(tierRes.data);
    } catch (error) {
      console.error('Failed to load profile:', error);
      toast.error('Failed to load profile');
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSaving(true);

    try {
      // Update profile
      await axios.put(
        `${API}/profile`,
        { preferences: formData },
        { headers: { Authorization: `Bearer ${token}` } }
      );

      // Complete KYC and calculate tier
      const tierRes = await axios.post(
        `${API}/profile/complete-kyc`,
        {},
        { headers: { Authorization: `Bearer ${token}` } }
      );

      setTierStatus({
        tier: tierRes.data.tier,
        kyc_completed: true,
        message: getTierMessage(tierRes.data.tier)
      });

      toast.success(`Profile updated! You're now Tier ${tierRes.data.tier}`);
    } catch (error) {
      console.error('Failed to save profile:', error);
      toast.error('Failed to save profile');
    } finally {
      setSaving(false);
    }
  };

  const getTierMessage = (tier) => {
    const messages = {
      0: "Complete your profile to get started",
      1: "Basic profile complete! Add more details to unlock better rates",
      2: "Enhanced profile! You're getting great rates",
      3: "VIP status! You have access to our best rates and exclusive offers"
    };
    return messages[tier] || messages[0];
  };

  const toggleCountry = (country) => {
    setFormData(prev => ({
      ...prev,
      preferred_countries: prev.preferred_countries.includes(country)
        ? prev.preferred_countries.filter(c => c !== country)
        : [...prev.preferred_countries, country]
    }));
  };

  const toggleMonth = (month) => {
    setFormData(prev => ({
      ...prev,
      preferred_travel_months: prev.preferred_travel_months.includes(month)
        ? prev.preferred_travel_months.filter(m => m !== month)
        : [...prev.preferred_travel_months, month]
    }));
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <Loader2 className="h-8 w-8 animate-spin text-emerald-600" />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-emerald-50/30 to-white py-12">
      <div className="max-w-4xl mx-auto px-4">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Your Golf Travel Profile</h1>
          <p className="text-gray-600">Complete your profile to unlock personalized recommendations and better rates</p>
        </div>

        {/* Tier Status Card */}
        {tierStatus && (
          <Card className={`mb-8 border-2 ${
            tierStatus.tier === 0 ? 'border-amber-300 bg-amber-50' :
            tierStatus.tier === 1 ? 'border-blue-300 bg-blue-50' :
            tierStatus.tier === 2 ? 'border-emerald-300 bg-emerald-50' :
            'border-purple-300 bg-purple-50'
          }`}>
            <CardContent className="pt-6">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-4">
                  <div className={`h-16 w-16 rounded-full flex items-center justify-center ${
                    tierStatus.tier === 0 ? 'bg-amber-200' :
                    tierStatus.tier === 1 ? 'bg-blue-200' :
                    tierStatus.tier === 2 ? 'bg-emerald-200' :
                    'bg-purple-200'
                  }`}>
                    <TrendingUp className={`h-8 w-8 ${
                      tierStatus.tier === 0 ? 'text-amber-700' :
                      tierStatus.tier === 1 ? 'text-blue-700' :
                      tierStatus.tier === 2 ? 'text-emerald-700' :
                      'text-purple-700'
                    }`} />
                  </div>
                  <div>
                    <div className="flex items-center gap-2 mb-1">
                      <h3 className="text-2xl font-bold">
                        {tierStatus.tier === 0 ? 'Getting Started' : `Tier ${tierStatus.tier}`}
                      </h3>
                      {tierStatus.tier === 3 && (
                        <Badge className="bg-purple-600">VIP</Badge>
                      )}
                    </div>
                    <p className="text-sm text-gray-600">{tierStatus.message}</p>
                  </div>
                </div>
                
                {/* Progress Indicator */}
                <div className="hidden md:flex items-center gap-2">
                  {[0, 1, 2, 3].map(tier => (
                    <div
                      key={tier}
                      className={`h-3 w-3 rounded-full ${
                        tier <= tierStatus.tier ? 'bg-emerald-500' : 'bg-gray-300'
                      }`}
                    />
                  ))}
                </div>
              </div>
            </CardContent>
          </Card>
        )}

        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Basic Information - Tier 1 */}
          <Card>
            <CardHeader>
              <div className="flex items-center gap-2">
                <User className="h-5 w-5 text-emerald-600" />
                <CardTitle>Basic Information</CardTitle>
              </div>
              <CardDescription>Essential details to get started (Required for Tier 1)</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              {/* Budget Range */}
              <div className="space-y-2">
                <Label>Budget Range (SEK)</Label>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <Label className="text-xs text-gray-500">Minimum</Label>
                    <Input
                      type="number"
                      value={formData.budget_min}
                      onChange={(e) => setFormData({...formData, budget_min: parseInt(e.target.value) || 0})}
                      placeholder="e.g., 10000"
                    />
                  </div>
                  <div>
                    <Label className="text-xs text-gray-500">Maximum</Label>
                    <Input
                      type="number"
                      value={formData.budget_max}
                      onChange={(e) => setFormData({...formData, budget_max: parseInt(e.target.value) || 0})}
                      placeholder="e.g., 50000"
                    />
                  </div>
                </div>
              </div>

              {/* Preferred Countries */}
              <div className="space-y-2">
                <Label>Preferred Destinations</Label>
                <div className="flex flex-wrap gap-2">
                  {COUNTRIES.map(country => (
                    <Badge
                      key={country}
                      variant={formData.preferred_countries.includes(country) ? 'default' : 'outline'}
                      className="cursor-pointer"
                      onClick={() => toggleCountry(country)}
                    >
                      {country}
                    </Badge>
                  ))}
                </div>
              </div>

              {/* Playing Level */}
              <div className="space-y-2">
                <Label>Playing Level</Label>
                <Select
                  value={formData.playing_level}
                  onValueChange={(value) => setFormData({...formData, playing_level: value})}
                >
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="Beginner">Beginner</SelectItem>
                    <SelectItem value="Intermediate">Intermediate</SelectItem>
                    <SelectItem value="Advanced">Advanced</SelectItem>
                    <SelectItem value="Professional">Professional</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              {/* Accommodation Preference */}
              <div className="space-y-2">
                <Label>Accommodation Preference</Label>
                <Select
                  value={formData.accommodation_preference}
                  onValueChange={(value) => setFormData({...formData, accommodation_preference: value})}
                >
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="Luxury">Luxury Resort</SelectItem>
                    <SelectItem value="Mid-range">Mid-range Hotel</SelectItem>
                    <SelectItem value="Budget">Budget-Friendly</SelectItem>
                    <SelectItem value="Any">Any</SelectItem>
                  </SelectContent>
                </Select>
              </div>
            </CardContent>
          </Card>

          {/* Enhanced Information - Tier 2 */}
          <Card>
            <CardHeader>
              <div className="flex items-center gap-2">
                <Calendar className="h-5 w-5 text-blue-600" />
                <CardTitle>Travel Preferences</CardTitle>
              </div>
              <CardDescription>Additional details for better recommendations (Tier 2)</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label>Trip Duration (Days)</Label>
                  <Input
                    type="number"
                    value={formData.trip_duration_days || ''}
                    onChange={(e) => setFormData({...formData, trip_duration_days: parseInt(e.target.value) || null})}
                    placeholder="e.g., 7"
                  />
                </div>

                <div className="space-y-2">
                  <Label>Group Size</Label>
                  <Input
                    type="number"
                    value={formData.group_size || ''}
                    onChange={(e) => setFormData({...formData, group_size: parseInt(e.target.value) || null})}
                    placeholder="e.g., 4"
                  />
                </div>
              </div>

              <div className="space-y-2">
                <Label>Phone Number</Label>
                <Input
                  type="tel"
                  value={formData.phone_number}
                  onChange={(e) => setFormData({...formData, phone_number: e.target.value})}
                  placeholder="+46 70 123 45 67"
                />
              </div>

              <div className="space-y-2">
                <Label>Travel Frequency</Label>
                <Select
                  value={formData.travel_frequency}
                  onValueChange={(value) => setFormData({...formData, travel_frequency: value})}
                >
                  <SelectTrigger>
                    <SelectValue placeholder="Select frequency" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="First-time">First-time Golf Traveler</SelectItem>
                    <SelectItem value="Annual">Once a Year</SelectItem>
                    <SelectItem value="Frequent">Multiple Times a Year</SelectItem>
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <Label>Preferred Travel Months</Label>
                <div className="flex flex-wrap gap-2">
                  {TRAVEL_MONTHS.map(month => (
                    <Badge
                      key={month}
                      variant={formData.preferred_travel_months.includes(month) ? 'default' : 'outline'}
                      className="cursor-pointer"
                      onClick={() => toggleMonth(month)}
                    >
                      {month.substring(0, 3)}
                    </Badge>
                  ))}
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Advanced Information - Tier 3 */}
          <Card>
            <CardHeader>
              <div className="flex items-center gap-2">
                <Award className="h-5 w-5 text-purple-600" />
                <CardTitle>VIP Details</CardTitle>
              </div>
              <CardDescription>Complete your profile for VIP status and exclusive offers (Tier 3)</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <Label>Golf Handicap (Optional)</Label>
                <Input
                  type="number"
                  value={formData.handicap || ''}
                  onChange={(e) => setFormData({...formData, handicap: parseInt(e.target.value) || null})}
                  placeholder="e.g., 15"
                />
              </div>

              <div className="space-y-2">
                <Label>Dietary Requirements</Label>
                <Textarea
                  value={formData.dietary_requirements}
                  onChange={(e) => setFormData({...formData, dietary_requirements: e.target.value})}
                  placeholder="e.g., Vegetarian, Gluten-free, etc."
                  rows={2}
                />
              </div>

              <div className="space-y-2">
                <Label>Special Requests or Preferences</Label>
                <Textarea
                  value={formData.special_requests}
                  onChange={(e) => setFormData({...formData, special_requests: e.target.value})}
                  placeholder="Any special requirements or preferences we should know about?"
                  rows={3}
                />
              </div>

              <div className="space-y-2">
                <Label>Previous Golf Destinations (Comma separated)</Label>
                <Input
                  value={formData.previous_golf_destinations.join(', ')}
                  onChange={(e) => setFormData({
                    ...formData, 
                    previous_golf_destinations: e.target.value.split(',').map(s => s.trim()).filter(Boolean)
                  })}
                  placeholder="e.g., St Andrews, Algarve, Costa del Sol"
                />
              </div>
            </CardContent>
          </Card>

          {/* KYC Document Upload */}
          <Card className="mb-8">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <FileText className="w-5 h-5" />
                KYC Documents
              </CardTitle>
              <CardDescription>
                Upload identity documents to verify your profile and unlock higher tiers with better rates and exclusive offers.
                Accepted: ID cards, passports, driver's licenses (PDF, JPG, PNG)
              </CardDescription>
            </CardHeader>
            <CardContent>
              <FileUpload 
                category="kyc-documents"
                maxFiles={3}
                maxSizeBytes={10 * 1024 * 1024} // 10MB
                allowedExtensions={['.pdf', '.jpg', '.jpeg', '.png']}
                onUploadComplete={(fileData) => {
                  toast.success(`Document "${fileData.original_filename}" uploaded successfully`);
                  // Optionally refresh tier status after upload
                  fetchTierStatus();
                }}
                className="border-0 shadow-none p-0"
              />
            </CardContent>
          </Card>

          {/* Submit Button */}
          <div className="flex justify-end gap-4">
            <Button
              type="button"
              variant="outline"
              onClick={() => navigate('/')}
              disabled={saving}
            >
              Cancel
            </Button>
            <Button
              type="submit"
              disabled={saving}
              className="bg-emerald-600 hover:bg-emerald-700"
            >
              {saving ? (
                <>
                  <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                  Saving...
                </>
              ) : (
                <>
                  <CheckCircle2 className="h-4 w-4 mr-2" />
                  Save Profile
                </>
              )}
            </Button>
          </div>
        </form>
      </div>
    </div>
  );
}
