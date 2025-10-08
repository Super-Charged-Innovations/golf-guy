import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useAuth } from '../contexts/AuthContext';
import { useNavigate, Link } from 'react-router-dom';
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from '../components/ui/card';
import { Button } from '../components/ui/button';
import { Badge } from '../components/ui/badge';
import { Avatar, AvatarFallback } from '../components/ui/avatar';
import { 
  User, 
  TrendingUp, 
  MapPin, 
  MessageSquare, 
  Settings,
  Sparkles,
  Calendar,
  Phone,
  Mail,
  ArrowRight,
  Loader2
} from 'lucide-react';
import { useScrollAnimation } from '../hooks/useScrollAnimation';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

export default function ClientDashboard() {
  const { user, token, isAuthenticated, loading: authLoading } = useAuth();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [profile, setProfile] = useState(null);
  const [tierStatus, setTierStatus] = useState(null);
  const [inquiries, setInquiries] = useState([]);
  const [recommendations, setRecommendations] = useState([]);

  useEffect(() => {
    if (!isAuthenticated) {
      navigate('/login');
      return;
    }
    loadDashboardData();
  }, [isAuthenticated]);

  const loadDashboardData = async () => {
    try {
      const [profileRes, tierRes, inquiriesRes] = await Promise.all([
        axios.get(`${API}/profile`, {
          headers: { Authorization: `Bearer ${token}` }
        }),
        axios.get(`${API}/profile/tier-status`, {
          headers: { Authorization: `Bearer ${token}` }
        }),
        axios.get(`${API}/inquiries`, {
          headers: { Authorization: `Bearer ${token}` }
        }).catch(() => ({ data: [] }))
      ]);

      setProfile(profileRes.data);
      setTierStatus(tierRes.data);
      setInquiries(inquiriesRes.data.slice(0, 3)); // Last 3 inquiries
    } catch (error) {
      console.error('Failed to load dashboard:', error);
    } finally {
      setLoading(false);
    }
  };

  const getTierColor = (tier) => {
    switch(tier) {
      case 0: return 'bg-amber-100 text-amber-700 border-amber-300';
      case 1: return 'bg-blue-100 text-blue-700 border-blue-300';
      case 2: return 'bg-emerald-100 text-emerald-700 border-emerald-300';
      case 3: return 'bg-purple-100 text-purple-700 border-purple-300';
      default: return 'bg-gray-100 text-gray-700 border-gray-300';
    }
  };

  const getTierIcon = (tier) => {
    if (tier === 3) return <Sparkles className="h-5 w-5" />;
    return <TrendingUp className="h-5 w-5" />;
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-emerald-50/30 to-white py-8">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
          {/* Header Skeleton */}
          <div className="mb-8 flex items-center justify-between">
            <div className="space-y-2">
              <div className="h-8 w-64 bg-gray-200 rounded animate-pulse" />
              <div className="h-4 w-48 bg-gray-200 rounded animate-pulse" />
            </div>
            <div className="h-16 w-16 rounded-full bg-gray-200 animate-pulse" />
          </div>
          
          {/* Stats Cards Skeleton */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
            {[1, 2, 3].map((i) => (
              <div key={i} className="p-6 border rounded-lg bg-white">
                <div className="flex items-center justify-between mb-4">
                  <div className="h-12 w-12 rounded-full bg-gray-200 animate-pulse" />
                  <div className="h-6 w-16 bg-gray-200 rounded animate-pulse" />
                </div>
                <div className="h-8 w-20 bg-gray-200 rounded animate-pulse mb-2" />
                <div className="h-4 w-32 bg-gray-200 rounded animate-pulse" />
              </div>
            ))}
          </div>
          
          {/* Content Skeleton */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <div className="lg:col-span-2 space-y-6">
              <div className="p-6 border rounded-lg bg-white h-48 animate-pulse" />
            </div>
            <div className="space-y-6">
              <div className="p-6 border rounded-lg bg-white h-64 animate-pulse" />
            </div>
          </div>
        </div>
      </div>
    );
  }

  const initials = user?.full_name
    ?.split(' ')
    .map(n => n[0])
    .join('')
    .toUpperCase() || 'U';

  const completionPercentage = tierStatus?.tier ? (tierStatus.tier / 3) * 100 : 0;

  return (
    <div className="min-h-screen bg-gradient-to-b from-emerald-50/30 to-white py-8">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="mb-8 animate-fade-in-up">
          <div className="flex items-center justify-between mb-2">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">
                Welcome back, {user?.full_name?.split(' ')[0]}!
              </h1>
              <p className="text-gray-600 mt-1">Here's your golf travel overview</p>
            </div>
            <Avatar className="h-16 w-16 border-4 border-emerald-200 shadow-lg">
              <AvatarFallback className="bg-gradient-to-br from-emerald-400 to-emerald-600 text-white text-xl font-bold">
                {initials}
              </AvatarFallback>
            </Avatar>
          </div>
        </div>

        {/* Quick Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          {/* Profile Status */}
          <DashboardCard delay={0}>
            <div className="flex items-center justify-between mb-4">
              <div className="p-3 rounded-full bg-emerald-100">
                <User className="h-6 w-6 text-emerald-600" />
              </div>
              <Badge variant="outline" className="text-xs">
                Profile
              </Badge>
            </div>
            <h3 className="text-2xl font-bold text-gray-900 mb-1">{completionPercentage.toFixed(0)}%</h3>
            <p className="text-sm text-gray-600">Profile Complete</p>
            <div className="mt-3 bg-gray-200 rounded-full h-2 overflow-hidden">
              <div 
                className="bg-gradient-to-r from-emerald-500 to-emerald-600 h-full transition-all duration-500"
                style={{ width: `${completionPercentage}%` }}
              ></div>
            </div>
          </DashboardCard>

          {/* Tier Status */}
          <DashboardCard delay={100}>
            <div className="flex items-center justify-between mb-4">
              <div className={`p-3 rounded-full ${getTierColor(tierStatus?.tier)}`}>
                {getTierIcon(tierStatus?.tier)}
              </div>
              <Badge 
                className={tierStatus?.tier === 3 ? 'bg-purple-600 text-white' : ''}
                variant={tierStatus?.tier === 0 ? 'outline' : 'default'}
              >
                {tierStatus?.tier === 0 ? 'Getting Started' : `Tier ${tierStatus?.tier}`}
              </Badge>
            </div>
            <h3 className="text-2xl font-bold text-gray-900 mb-1">
              {tierStatus?.tier === 3 ? 'VIP Member' : tierStatus?.tier === 0 ? 'New User' : `Tier ${tierStatus?.tier}`}
            </h3>
            <p className="text-sm text-gray-600 line-clamp-2">{tierStatus?.message}</p>
          </DashboardCard>

          {/* Inquiries */}
          <DashboardCard delay={200}>
            <div className="flex items-center justify-between mb-4">
              <div className="p-3 rounded-full bg-blue-100">
                <MessageSquare className="h-6 w-6 text-blue-600" />
              </div>
              <Badge variant="outline" className="text-xs">
                Recent
              </Badge>
            </div>
            <h3 className="text-2xl font-bold text-gray-900 mb-1">{inquiries.length}</h3>
            <p className="text-sm text-gray-600">Travel Inquiries</p>
          </DashboardCard>
        </div>

        {/* Main Content Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Left Column - Profile Summary */}
          <div className="lg:col-span-2 space-y-6">
            {/* Quick Actions */}
            <Card className="animate-fade-in-up animate-delay-300 border-emerald-100">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Sparkles className="h-5 w-5 text-emerald-600" />
                  Quick Actions
                </CardTitle>
                <CardDescription>Manage your golf travel experience</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  <Link to="/profile">
                    <Button 
                      variant="outline" 
                      className="w-full justify-start border-emerald-200 hover:bg-emerald-50 hover:border-emerald-400 transition-all"
                    >
                      <Settings className="h-4 w-4 mr-2" />
                      Update Profile
                    </Button>
                  </Link>
                  
                  <Link to="/destinations">
                    <Button 
                      variant="outline" 
                      className="w-full justify-start border-emerald-200 hover:bg-emerald-50 hover:border-emerald-400 transition-all"
                    >
                      <MapPin className="h-4 w-4 mr-2" />
                      Browse Destinations
                    </Button>
                  </Link>
                  
                  <Link to="/contact">
                    <Button 
                      variant="outline" 
                      className="w-full justify-start border-emerald-200 hover:bg-emerald-50 hover:border-emerald-400 transition-all"
                    >
                      <Phone className="h-4 w-4 mr-2" />
                      Contact Agent
                    </Button>
                  </Link>
                  
                  <Button 
                    variant="outline" 
                    className="w-full justify-start border-emerald-200 hover:bg-emerald-50 hover:border-emerald-400 transition-all"
                    onClick={() => {
                      const chatButton = document.querySelector('[data-testid="ai-chat-button"]');
                      if (chatButton) chatButton.click();
                    }}
                  >
                    <MessageSquare className="h-4 w-4 mr-2" />
                    Chat with Alex
                  </Button>

                  <Link to="/privacy">
                    <Button 
                      variant="outline" 
                      className="w-full justify-start border-blue-200 hover:bg-blue-50 hover:border-blue-400 transition-all col-span-2"
                    >
                      <svg className="h-4 w-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                      </svg>
                      Privacy & Data
                    </Button>
                  </Link>
                </div>
              </CardContent>
            </Card>

            {/* Recent Inquiries */}
            <Card className="animate-fade-in-up animate-delay-400 border-emerald-100">
              <CardHeader>
                <CardTitle>Recent Inquiries</CardTitle>
                <CardDescription>Your latest travel requests</CardDescription>
              </CardHeader>
              <CardContent>
                {inquiries.length > 0 ? (
                  <>
                    <div className="space-y-4">
                      {inquiries.map((inquiry, index) => (
                        <div 
                          key={inquiry.id || index} 
                          className="flex items-center justify-between p-4 rounded-lg border border-gray-200 hover:border-emerald-200 hover:bg-emerald-50/30 transition-all cursor-pointer"
                          onClick={() => navigate('/contact')}
                          role="button"
                          tabIndex={0}
                        >
                          <div className="flex-1">
                            <div className="flex items-center gap-2 mb-1">
                              <MapPin className="h-4 w-4 text-emerald-600" />
                              <span className="font-medium text-gray-900">
                                {inquiry.destination_name || 'General Inquiry'}
                              </span>
                            </div>
                            <p className="text-sm text-gray-600">
                              {inquiry.message?.substring(0, 80)}...
                            </p>
                            <p className="text-xs text-gray-500 mt-1">
                              {new Date(inquiry.created_at).toLocaleDateString()}
                            </p>
                          </div>
                          <Badge variant="outline" className="ml-4">
                            {inquiry.status || 'Pending'}
                          </Badge>
                        </div>
                      ))}
                    </div>
                    <Link to="/contact">
                      <Button variant="ghost" className="w-full mt-4 text-emerald-600 hover:text-emerald-700 hover:bg-emerald-50">
                        Make New Inquiry
                        <ArrowRight className="ml-2 h-4 w-4" />
                      </Button>
                    </Link>
                  </>
                ) : (
                  <div className="text-center py-12">
                    <div className="inline-flex p-4 rounded-full bg-gray-100 mb-4">
                      <MessageSquare className="h-8 w-8 text-gray-400" />
                    </div>
                    <h3 className="text-lg font-medium text-gray-900 mb-2">No inquiries yet</h3>
                    <p className="text-sm text-gray-600 mb-6 max-w-sm mx-auto">
                      Start planning your dream golf vacation by making your first travel inquiry
                    </p>
                    <Link to="/contact">
                      <Button className="bg-emerald-600 hover:bg-emerald-700">
                        <Mail className="h-4 w-4 mr-2" />
                        Make Your First Inquiry
                      </Button>
                    </Link>
                  </div>
                )}
              </CardContent>
            </Card>
          </div>

          {/* Right Column - Profile Details */}
          <div className="space-y-6">
            {/* Account Details */}
            <Card className="animate-fade-in-up animate-delay-300 border-emerald-100">
              <CardHeader>
                <CardTitle className="text-base">Account Details</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <div className="flex items-center gap-2 text-sm text-gray-600 mb-1">
                    <User className="h-4 w-4" />
                    <span>Full Name</span>
                  </div>
                  <p className="font-medium text-gray-900">{user?.full_name}</p>
                </div>
                
                <div>
                  <div className="flex items-center gap-2 text-sm text-gray-600 mb-1">
                    <Mail className="h-4 w-4" />
                    <span>Email</span>
                  </div>
                  <p className="font-medium text-gray-900">{user?.email}</p>
                </div>

                {profile?.preferences?.phone_number && (
                  <div>
                    <div className="flex items-center gap-2 text-sm text-gray-600 mb-1">
                      <Phone className="h-4 w-4" />
                      <span>Phone</span>
                    </div>
                    <p className="font-medium text-gray-900">{profile.preferences.phone_number}</p>
                  </div>
                )}

                {profile?.preferences?.travel_frequency && (
                  <div>
                    <div className="flex items-center gap-2 text-sm text-gray-600 mb-1">
                      <Calendar className="h-4 w-4" />
                      <span>Travel Frequency</span>
                    </div>
                    <p className="font-medium text-gray-900">{profile.preferences.travel_frequency}</p>
                  </div>
                )}
              </CardContent>
            </Card>

            {/* Travel Preferences */}
            {profile?.preferences && (
              <Card className="animate-fade-in-up animate-delay-400 border-emerald-100">
                <CardHeader>
                  <CardTitle className="text-base">Travel Preferences</CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  {profile.preferences.preferred_countries?.length > 0 && (
                    <div>
                      <p className="text-sm text-gray-600 mb-2">Preferred Destinations</p>
                      <div className="flex flex-wrap gap-2">
                        {profile.preferences.preferred_countries.slice(0, 4).map((country, index) => (
                          <Badge key={index} variant="outline" className="border-emerald-200 text-emerald-700">
                            {country}
                          </Badge>
                        ))}
                      </div>
                    </div>
                  )}

                  {profile.preferences.budget_min && profile.preferences.budget_max && (
                    <div>
                      <p className="text-sm text-gray-600 mb-1">Budget Range</p>
                      <p className="font-medium text-gray-900">
                        {profile.preferences.budget_min.toLocaleString()} - {profile.preferences.budget_max.toLocaleString()} SEK
                      </p>
                    </div>
                  )}

                  {profile.preferences.playing_level && (
                    <div>
                      <p className="text-sm text-gray-600 mb-1">Playing Level</p>
                      <Badge className="bg-emerald-100 text-emerald-700 border-0">
                        {profile.preferences.playing_level}
                      </Badge>
                    </div>
                  )}
                </CardContent>
              </Card>
            )}

            {/* CTA Card */}
            {tierStatus?.tier === 0 && (
              <Card className="animate-fade-in-up animate-delay-500 border-2 border-emerald-200 bg-gradient-to-br from-emerald-50 to-white">
                <CardContent className="pt-6">
                  <div className="text-center">
                    <div className="inline-flex p-3 rounded-full bg-emerald-100 mb-4">
                      <TrendingUp className="h-6 w-6 text-emerald-600" />
                    </div>
                    <h3 className="font-bold text-gray-900 mb-2">Complete Your Profile</h3>
                    <p className="text-sm text-gray-600 mb-4">
                      Unlock personalized recommendations and better rates!
                    </p>
                    <Link to="/profile">
                      <Button className="w-full bg-emerald-600 hover:bg-emerald-700">
                        Complete Now
                        <ArrowRight className="ml-2 h-4 w-4" />
                      </Button>
                    </Link>
                  </div>
                </CardContent>
              </Card>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

// Animated Card Component
function DashboardCard({ children, delay = 0 }) {
  const [ref, isVisible] = useScrollAnimation({ threshold: 0.1 });

  return (
    <div
      ref={ref}
      className={`transition-all duration-700 ${
        isVisible 
          ? 'opacity-100 translate-y-0' 
          : 'opacity-0 translate-y-4'
      }`}
      style={{ transitionDelay: `${delay}ms` }}
    >
      <Card className="card-hover border-emerald-100 h-full">
        <CardContent className="pt-6">
          {children}
        </CardContent>
      </Card>
    </div>
  );
}
