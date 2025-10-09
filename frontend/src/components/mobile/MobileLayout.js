import React from 'react';
import { Outlet, useLocation, useNavigate } from 'react-router-dom';
import { useDeviceDetection } from '../../hooks/usePWA';
import { 
  MobileBottomNavigation, 
  PWAInstallPrompt, 
  OfflineIndicator 
} from './MobileComponents';

const MobileLayout = () => {
  const { isMobile } = useDeviceDetection();
  const location = useLocation();
  const navigate = useNavigate();

  // Only show mobile layout on mobile devices
  if (!isMobile) {
    return <Outlet />;
  }

  const handleNavigate = (path) => {
    navigate(path);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Offline Indicator */}
      <OfflineIndicator />
      
      {/* Main Content */}
      <main className="pb-16"> {/* Bottom padding for navigation */}
        <Outlet />
      </main>
      
      {/* Bottom Navigation */}
      <MobileBottomNavigation 
        currentPath={location.pathname}
        onNavigate={handleNavigate}
      />
      
      {/* PWA Install Prompt */}
      <PWAInstallPrompt />
    </div>
  );
};

export default MobileLayout;