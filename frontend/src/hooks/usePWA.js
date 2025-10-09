import { useState, useEffect } from 'react';

export const useDeviceDetection = () => {
  const [device, setDevice] = useState({
    isMobile: false,
    isTablet: false,
    isDesktop: false,
    isTouchDevice: false,
    userAgent: '',
    screenWidth: 0,
    screenHeight: 0
  });

  useEffect(() => {
    const detectDevice = () => {
      const userAgent = navigator.userAgent || '';
      const screenWidth = window.innerWidth;
      const screenHeight = window.innerHeight;
      
      // Mobile detection
      const mobileRegex = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i;
      const isMobileUA = mobileRegex.test(userAgent);
      const isMobileWidth = screenWidth <= 768;
      
      // Tablet detection
      const isTabletWidth = screenWidth > 768 && screenWidth <= 1024;
      const isTabletUA = /iPad|Android(?=.*Mobile)/i.test(userAgent);
      
      // Touch device detection
      const isTouchDevice = 'ontouchstart' in window || navigator.maxTouchPoints > 0;
      
      setDevice({
        isMobile: isMobileUA || isMobileWidth,
        isTablet: isTabletUA || isTabletWidth,
        isDesktop: screenWidth > 1024,
        isTouchDevice,
        userAgent,
        screenWidth,
        screenHeight
      });
    };

    detectDevice();
    
    // Listen for resize events
    const handleResize = () => detectDevice();
    window.addEventListener('resize', handleResize);
    
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  return device;
};

export const usePWA = () => {
  const [pwaSupport, setPwaSupport] = useState({
    isSupported: false,
    isInstalled: false,
    canInstall: false,
    deferredPrompt: null
  });

  useEffect(() => {
    // Check if PWA is supported
    const isSupported = 'serviceWorker' in navigator && 'PushManager' in window;
    
    // Check if app is installed (running in standalone mode)
    const isInstalled = window.matchMedia('(display-mode: standalone)').matches ||
                       window.navigator.standalone === true;

    setPwaSupport(prev => ({
      ...prev,
      isSupported,
      isInstalled
    }));

    // Handle install prompt
    let deferredPrompt = null;
    
    const handleBeforeInstallPrompt = (e) => {
      console.log('PWA: Install prompt available');
      e.preventDefault(); // Prevent automatic prompt
      deferredPrompt = e;
      
      setPwaSupport(prev => ({
        ...prev,
        canInstall: true,
        deferredPrompt: e
      }));
    };

    const handleAppInstalled = () => {
      console.log('PWA: App installed successfully');
      setPwaSupport(prev => ({
        ...prev,
        isInstalled: true,
        canInstall: false,
        deferredPrompt: null
      }));
    };

    window.addEventListener('beforeinstallprompt', handleBeforeInstallPrompt);
    window.addEventListener('appinstalled', handleAppInstalled);

    // Register service worker
    if (isSupported && !isInstalled) {
      registerServiceWorker();
    }

    return () => {
      window.removeEventListener('beforeinstallprompt', handleBeforeInstallPrompt);
      window.removeEventListener('appinstalled', handleAppInstalled);
    };
  }, []);

  const installApp = async () => {
    const { deferredPrompt } = pwaSupport;
    
    if (!deferredPrompt) {
      console.log('PWA: No install prompt available');
      return false;
    }

    try {
      // Show the install prompt
      deferredPrompt.prompt();
      
      // Wait for user response
      const { outcome } = await deferredPrompt.userChoice;
      
      console.log(`PWA: Install prompt result: ${outcome}`);
      
      // Clear the deferred prompt
      setPwaSupport(prev => ({
        ...prev,
        deferredPrompt: null,
        canInstall: false
      }));
      
      return outcome === 'accepted';
    } catch (error) {
      console.error('PWA: Install error:', error);
      return false;
    }
  };

  return { ...pwaSupport, installApp };
};

const registerServiceWorker = async () => {
  try {
    const registration = await navigator.serviceWorker.register('/sw.js', {
      scope: '/',
      updateViaCache: 'none'
    });
    
    console.log('PWA: Service worker registered:', registration.scope);
    
    // Handle updates
    registration.addEventListener('updatefound', () => {
      const newWorker = registration.installing;
      
      if (newWorker) {
        newWorker.addEventListener('statechange', () => {
          if (newWorker.state === 'installed' && navigator.serviceWorker.controller) {
            console.log('PWA: New content available - refresh to update');
            
            // Optionally show update notification
            if (window.confirm('New version available! Refresh to update?')) {
              newWorker.postMessage({ type: 'SKIP_WAITING' });
              window.location.reload();
            }
          }
        });
      }
    });
    
    return registration;
  } catch (error) {
    console.error('PWA: Service worker registration failed:', error);
    return null;
  }
};

export const useOnlineStatus = () => {
  const [isOnline, setIsOnline] = useState(navigator.onLine);

  useEffect(() => {
    const handleOnline = () => {
      console.log('Network: Back online');
      setIsOnline(true);
    };
    
    const handleOffline = () => {
      console.log('Network: Gone offline');  
      setIsOnline(false);
    };

    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);

    return () => {
      window.removeEventListener('online', handleOnline);
      window.removeEventListener('offline', handleOffline);
    };
  }, []);

  return isOnline;
};

export default { useDeviceDetection, usePWA, useOnlineStatus };