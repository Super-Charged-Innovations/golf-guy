import React, { useState } from 'react';
import { useDeviceDetection, usePWA } from '../../hooks/usePWA';
import { Button } from '../ui/button';
import { Card } from '../ui/card';
import { Badge } from '../ui/badge';
import { 
  Download, 
  Smartphone, 
  Wifi,
  WifiOff,
  Star,
  Clock,
  Users,
  MapPin,
  DollarSign
} from 'lucide-react';

const MobileDestinationCard = ({ destination, onBook = () => {}, onFavorite = () => {} }) => {
  const [isFavorite, setIsFavorite] = useState(false);
  
  const handleFavorite = () => {
    setIsFavorite(!isFavorite);
    onFavorite(destination.id, !isFavorite);
  };

  return (
    <Card className="w-full bg-white shadow-lg border-0 overflow-hidden">
      {/* Image */}
      <div className="relative h-48">
        <img 
          src={destination.images?.[0] || '/placeholder-golf.jpg'}
          alt={destination.name}
          className="w-full h-full object-cover"
        />
        
        {/* Favorite Button */}
        <button
          onClick={handleFavorite}
          className={`absolute top-3 right-3 w-10 h-10 rounded-full flex items-center justify-center transition-colors ${
            isFavorite 
              ? 'bg-red-500 text-white' 
              : 'bg-white/80 text-gray-600 hover:bg-white'
          }`}
        >
          <Star className={`w-5 h-5 ${isFavorite ? 'fill-current' : ''}`} />
        </button>
        
        {/* Featured Badge */}
        {destination.featured && (
          <Badge className="absolute top-3 left-3 bg-emerald-600 text-white">
            Featured
          </Badge>
        )}
        
        {/* Price Tag */}
        <div className="absolute bottom-3 left-3 bg-black/70 text-white px-3 py-1 rounded-full text-sm font-medium">
          From {destination.price_from} SEK
        </div>
      </div>
      
      {/* Content */}
      <div className="p-4">
        <div className="flex items-start justify-between mb-2">
          <h3 className="font-bold text-lg text-gray-900 line-clamp-2 flex-1">
            {destination.name}
          </h3>
        </div>
        
        {/* Location */}
        <div className="flex items-center text-gray-600 mb-2">
          <MapPin className="w-4 h-4 mr-1" />
          <span className="text-sm">
            {destination.region ? `${destination.region}, ` : ''}{destination.country}
          </span>
        </div>
        
        {/* Description */}
        <p className="text-gray-600 text-sm line-clamp-2 mb-3">
          {destination.short_desc}
        </p>
        
        {/* Highlights */}
        <div className="flex flex-wrap gap-1 mb-4">
          {destination.highlights?.slice(0, 2).map((highlight, index) => (
            <Badge key={index} variant="outline" className="text-xs">
              {highlight}
            </Badge>
          ))}
          {destination.highlights?.length > 2 && (
            <Badge variant="outline" className="text-xs">
              +{destination.highlights.length - 2} more
            </Badge>
          )}
        </div>
        
        {/* Action Buttons */}
        <div className="flex gap-2">
          <Button 
            className="flex-1 bg-emerald-600 hover:bg-emerald-700 text-white h-12"
            onClick={() => onBook(destination)}
          >
            Book Now
          </Button>
          <Button 
            variant="outline"
            className="px-4 h-12 border-emerald-600 text-emerald-600 hover:bg-emerald-50"
            onClick={() => window.location.href = `/destinations/${destination.slug}`}
          >
            Details
          </Button>
        </div>
      </div>
    </Card>
  );
};

const MobileSearchBar = ({ onSearch, onFiltersToggle, searchQuery, setSearchQuery }) => {
  return (
    <div className="bg-white shadow-sm border-b sticky top-0 z-40">
      <div className="p-4">
        <div className="flex gap-2">
          <div className="flex-1 relative">
            <input
              type="text"
              placeholder="Search golf destinations..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && onSearch()}
              className="w-full h-12 px-4 pr-12 border border-gray-300 rounded-xl focus:ring-2 focus:ring-emerald-500 focus:border-transparent"
            />
            <button
              onClick={onSearch}
              className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-emerald-600"
            >
              🔍
            </button>
          </div>
          <Button
            variant="outline"
            onClick={onFiltersToggle}
            className="h-12 px-4 border-gray-300"
          >
            Filters
          </Button>
        </div>
      </div>
    </div>
  );
};

const MobileBottomNavigation = ({ currentPath, onNavigate }) => {
  const navItems = [
    { path: '/', icon: '🏠', label: 'Home' },
    { path: '/destinations', icon: '⛳', label: 'Golf' },
    { path: '/search', icon: '🔍', label: 'Search' },
    { path: '/dashboard', icon: '📊', label: 'Bookings' },
    { path: '/profile', icon: '👤', label: 'Profile' }
  ];

  return (
    <div className="fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 z-50">
      <div className="flex">
        {navItems.map((item) => (
          <button
            key={item.path}
            onClick={() => onNavigate(item.path)}
            className={`flex-1 py-3 px-2 text-center transition-colors ${
              currentPath === item.path 
                ? 'text-emerald-600 bg-emerald-50' 
                : 'text-gray-600 hover:text-gray-900'
            }`}
          >
            <div className="text-lg mb-1">{item.icon}</div>
            <div className="text-xs font-medium">{item.label}</div>
          </button>
        ))}
      </div>
    </div>
  );
};

const PWAInstallPrompt = () => {
  const { canInstall, installApp, isInstalled } = usePWA();
  const [showPrompt, setShowPrompt] = useState(false);

  useEffect(() => {
    // Show install prompt after user has browsed for a bit
    if (canInstall && !isInstalled) {
      const timer = setTimeout(() => {
        setShowPrompt(true);
      }, 30000); // Show after 30 seconds

      return () => clearTimeout(timer);
    }
  }, [canInstall, isInstalled]);

  const handleInstall = async () => {
    const success = await installApp();
    if (success) {
      setShowPrompt(false);
    }
  };

  if (!showPrompt || isInstalled) {
    return null;
  }

  return (
    <div className="fixed bottom-20 left-4 right-4 z-50">
      <Card className="bg-emerald-600 text-white border-0 shadow-2xl">
        <div className="p-4">
          <div className="flex items-start gap-3">
            <div className="w-12 h-12 bg-white/20 rounded-xl flex items-center justify-center flex-shrink-0">
              <Download className="w-6 h-6" />
            </div>
            
            <div className="flex-1 min-w-0">
              <h3 className="font-bold text-lg mb-1">Install Golf Guy App</h3>
              <p className="text-emerald-100 text-sm mb-3">
                Get faster access, offline browsing, and exclusive mobile features!
              </p>
              
              <div className="flex gap-2">
                <Button
                  onClick={handleInstall}
                  className="bg-white text-emerald-600 hover:bg-gray-100 font-medium"
                  size="sm"
                >
                  <Smartphone className="w-4 h-4 mr-2" />
                  Install
                </Button>
                <Button
                  onClick={() => setShowPrompt(false)}
                  variant="ghost"
                  className="text-white hover:bg-white/10"
                  size="sm"
                >
                  Later
                </Button>
              </div>
            </div>
          </div>
        </div>
      </Card>
    </div>
  );
};

const OfflineIndicator = () => {
  const [isOnline, setIsOnline] = useState(navigator.onLine);

  useEffect(() => {
    const handleOnline = () => setIsOnline(true);
    const handleOffline = () => setIsOnline(false);

    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);

    return () => {
      window.removeEventListener('online', handleOnline);
      window.removeEventListener('offline', handleOffline);
    };
  }, []);

  if (isOnline) return null;

  return (
    <div className="fixed top-0 left-0 right-0 bg-amber-500 text-white text-center py-2 px-4 z-50">
      <div className="flex items-center justify-center gap-2">
        <WifiOff className="w-4 h-4" />
        <span className="text-sm font-medium">You're offline - limited features available</span>
      </div>
    </div>
  );
};

const MobileBookingCard = ({ booking, onViewDetails, onCancel }) => {
  const statusColors = {
    pending: 'bg-amber-100 text-amber-800',
    confirmed: 'bg-green-100 text-green-800', 
    cancelled: 'bg-red-100 text-red-800',
    completed: 'bg-blue-100 text-blue-800'
  };

  return (
    <Card className="w-full border border-gray-200 hover:shadow-md transition-shadow">
      <div className="p-4">
        {/* Header */}
        <div className="flex items-center justify-between mb-3">
          <Badge className={statusColors[booking.status] || statusColors.pending}>
            {booking.status.charAt(0).toUpperCase() + booking.status.slice(1)}
          </Badge>
          <span className="text-xs text-gray-500">
            #{booking.booking_reference}
          </span>
        </div>
        
        {/* Booking Details */}
        <div className="space-y-2 mb-4">
          <h3 className="font-semibold text-gray-900">
            {booking.items?.[0]?.destination_name || 'Golf Booking'}
          </h3>
          
          <div className="flex items-center text-gray-600 text-sm">
            <Clock className="w-4 h-4 mr-2" />
            <span>
              {new Date(booking.items?.[0]?.date).toLocaleDateString()} at{' '}
              {booking.items?.[0]?.time}
            </span>
          </div>
          
          <div className="flex items-center text-gray-600 text-sm">
            <Users className="w-4 h-4 mr-2" />
            <span>{booking.items?.[0]?.players?.length || 1} players</span>
          </div>
          
          <div className="flex items-center text-gray-900 text-sm font-medium">
            <DollarSign className="w-4 h-4 mr-2" />
            <span>{booking.total_amount} {booking.currency}</span>
          </div>
        </div>
        
        {/* Actions */}
        <div className="flex gap-2">
          <Button
            onClick={() => onViewDetails(booking)}
            variant="outline"
            size="sm"
            className="flex-1"
          >
            View Details
          </Button>
          {booking.status === 'confirmed' && (
            <Button
              onClick={() => onCancel(booking)}
              variant="outline"
              size="sm"
              className="text-red-600 hover:text-red-700 hover:bg-red-50"
            >
              Cancel
            </Button>
          )}
        </div>
      </div>
    </Card>
  );
};

export {
  MobileDestinationCard,
  MobileSearchBar,
  MobileBottomNavigation,
  PWAInstallPrompt,
  OfflineIndicator,
  MobileBookingCard
};