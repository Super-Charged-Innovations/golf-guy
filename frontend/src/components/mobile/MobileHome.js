import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useDeviceDetection } from '../../hooks/usePWA';
import { useAuth } from '../../contexts/AuthContext';
import { Card } from '../ui/card';
import { Button } from '../ui/button';
import { Input } from '../ui/input';
import { Badge } from '../ui/badge';
import { 
  MobileDestinationCard, 
  MobileSearchBar 
} from './MobileComponents';
import {
  Search,
  Star,
  MapPin,
  TrendingUp,
  Zap,
  Calendar,
  Award
} from 'lucide-react';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const MobileHome = () => {
  const { isMobile } = useDeviceDetection();
  
  // Early return BEFORE any other hooks
  if (!isMobile) {
    return null; // Desktop version handled by regular Home component
  }

  const navigate = useNavigate();
  const { user } = useAuth();
  const [searchQuery, setSearchQuery] = useState('');
  const [featuredDestinations, setFeaturedDestinations] = useState([]);
  const [popularSearches, setPopularSearches] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadHomeData();
  }, []);

  const loadHomeData = async () => {
    try {
      // Load featured destinations
      const destResponse = await axios.get(`${API}/destinations?featured=true&limit=6`);
      setFeaturedDestinations(destResponse.data || []);
      
      // Load popular searches
      const searchResponse = await axios.get(`${API}/search/popular`);
      setPopularSearches(searchResponse.data.popular_searches?.slice(0, 5) || []);
      
    } catch (error) {
      console.error('Error loading home data:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = () => {
    if (searchQuery.trim()) {
      navigate(`/destinations?q=${encodeURIComponent(searchQuery)}`);
    }
  };

  const handleQuickSearch = (query) => {
    navigate(`/destinations?q=${encodeURIComponent(query)}`);
  };

  const handleBookDestination = (destination) => {
    navigate(`/booking?destination=${destination.id}`);
  };

  const handleFavoriteDestination = async (destinationId, isFavorite) => {
    // TODO: Implement favorites functionality
    console.log('Favorite destination:', destinationId, isFavorite);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Hero Section */}
      <div className="bg-gradient-to-br from-emerald-600 to-emerald-800 text-white">
        <div className="p-6 pb-8">
          {/* Welcome Message */}
          <div className="mb-6">
            <h1 className="text-2xl font-bold mb-2">
              {user ? `Welcome back, ${user.full_name.split(' ')[0]}!` : 'Discover Golf'}
            </h1>
            <p className="text-emerald-100 text-sm">
              Find your perfect golf destination with AI-powered recommendations
            </p>
          </div>
          
          {/* Quick Search */}
          <div className="relative mb-4">
            <input
              type="text"
              placeholder="Where would you like to play?"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
              className="w-full h-12 px-4 pr-12 bg-white text-gray-900 rounded-xl border-0 focus:ring-2 focus:ring-white"
            />
            <button
              onClick={handleSearch}
              className="absolute right-3 top-1/2 transform -translate-y-1/2 text-emerald-600 hover:text-emerald-700"
            >
              <Search className="w-5 h-5" />
            </button>
          </div>
          
          {/* Quick Action Buttons */}
          <div className="grid grid-cols-3 gap-3">
            <Button
              variant="secondary"
              size="sm"
              onClick={() => navigate('/destinations?featured=true')}
              className="bg-white/20 text-white border-white/30 hover:bg-white/30"
            >
              <Star className="w-4 h-4 mr-1" />
              Featured
            </Button>
            <Button
              variant="secondary"
              size="sm"
              onClick={() => navigate('/destinations?sort=price_asc')}
              className="bg-white/20 text-white border-white/30 hover:bg-white/30"
            >
              <TrendingUp className="w-4 h-4 mr-1" />
              Best Value
            </Button>
            <Button
              variant="secondary"
              size="sm"
              onClick={() => navigate('/dashboard')}
              className="bg-white/20 text-white border-white/30 hover:bg-white/30"
            >
              <Calendar className="w-4 h-4 mr-1" />
              {user ? 'My Trips' : 'Plan Trip'}
            </Button>
          </div>
        </div>
      </div>

      {/* Popular Searches */}
      {popularSearches.length > 0 && (
        <div className="p-4">
          <h2 className="text-lg font-bold text-gray-900 mb-3 flex items-center">
            <Zap className="w-5 h-5 mr-2 text-emerald-600" />
            Popular Searches
          </h2>
          
          <div className="flex gap-2 overflow-x-auto pb-2">
            {popularSearches.map((search, index) => (
              <button
                key={index}
                onClick={() => handleQuickSearch(search.query)}
                className="flex-shrink-0 bg-white px-4 py-2 rounded-xl border border-gray-200 text-sm font-medium text-gray-700 hover:border-emerald-500 hover:text-emerald-600 transition-colors"
              >
                {search.query}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Featured Destinations */}
      <div className="p-4">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-lg font-bold text-gray-900 flex items-center">
            <Award className="w-5 h-5 mr-2 text-emerald-600" />
            Featured Destinations
          </h2>
          <Button
            variant="ghost"
            size="sm"
            onClick={() => navigate('/destinations')}
            className="text-emerald-600"
          >
            View All
          </Button>
        </div>

        {loading ? (
          <div className="grid gap-4">
            {[...Array(3)].map((_, index) => (
              <Card key={index} className="h-64 bg-gray-200 animate-pulse rounded-xl" />
            ))}
          </div>
        ) : (
          <div className="grid gap-4">
            {featuredDestinations.map((destination) => (
              <MobileDestinationCard
                key={destination.id}
                destination={destination}
                onBook={handleBookDestination}
                onFavorite={handleFavoriteDestination}
              />
            ))}
          </div>
        )}
      </div>

      {/* Quick Stats (if user is authenticated) */}
      {user && (
        <div className="p-4">
          <Card className="bg-gradient-to-r from-emerald-500 to-emerald-600 text-white">
            <div className="p-4">
              <h3 className="font-bold mb-3">Your Golf Journey</h3>
              <div className="grid grid-cols-3 gap-4 text-center">
                <div>
                  <div className="text-2xl font-bold">0</div>
                  <div className="text-xs text-emerald-100">Bookings</div>
                </div>
                <div>
                  <div className="text-2xl font-bold">0</div>
                  <div className="text-xs text-emerald-100">Countries</div>
                </div>
                <div>
                  <div className="text-2xl font-bold">0</div>
                  <div className="text-xs text-emerald-100">Rounds</div>
                </div>
              </div>
              
              <Button
                className="w-full mt-4 bg-white text-emerald-600 hover:bg-gray-100"
                size="sm"
                onClick={() => navigate('/dashboard')}
              >
                View Dashboard
              </Button>
            </div>
          </Card>
        </div>
      )}

      {/* Bottom Padding for Navigation */}
      <div className="h-20" />
    </div>
  );
};

export default MobileHome;