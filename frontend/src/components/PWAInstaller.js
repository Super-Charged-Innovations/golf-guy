import React, { useState, useEffect } from 'react';
import { X, Download, Smartphone, Star } from 'lucide-react';

const PWAInstaller = () => {
  const [deferredPrompt, setDeferredPrompt] = useState(null);
  const [showInstallPrompt, setShowInstallPrompt] = useState(false);
  const [isInstalled, setIsInstalled] = useState(false);
  const [isIOS, setIsIOS] = useState(false);
  const [browserInfo, setBrowserInfo] = useState('');

  useEffect(() => {
    // Detect iOS devices
    const iOS = /iPad|iPhone|iPod/.test(navigator.userAgent);
    const standalone = window.navigator.standalone;
    setIsIOS(iOS);
    setIsInstalled(standalone || window.matchMedia('(display-mode: standalone)').matches);
    
    // Get browser info for debugging
    setBrowserInfo(navigator.userAgent);
    
    console.log('PWA Debug Info:', {
      userAgent: navigator.userAgent,
      isIOS: iOS,
      standalone: standalone,
      displayMode: window.matchMedia('(display-mode: standalone)').matches
    });

    // Handle beforeinstallprompt event
    const handleBeforeInstallPrompt = (e) => {
      console.log('PWA: beforeinstallprompt event triggered');
      e.preventDefault();
      setDeferredPrompt(e);
      
      // Show install prompt after a delay (browser requirement)
      setTimeout(() => {
        if (!isInstalled) {
          setShowInstallPrompt(true);
          console.log('PWA: Showing install prompt');
        }
      }, 3000); // 3 second delay
    };

    const handleAppInstalled = () => {
      console.log('PWA: App installed successfully');
      setIsInstalled(true);
      setShowInstallPrompt(false);
      setDeferredPrompt(null);
    };

    // Add event listeners
    window.addEventListener('beforeinstallprompt', handleBeforeInstallPrompt);
    window.addEventListener('appinstalled', handleAppInstalled);

    // For debugging - force show install prompt after 10 seconds on mobile
    const debugTimer = setTimeout(() => {
      if (!isInstalled && (window.innerWidth <= 768) && !iOS) {
        console.log('PWA: Debug - showing install prompt for mobile browser');
        setShowInstallPrompt(true);
      }
    }, 10000);

    return () => {
      window.removeEventListener('beforeinstallprompt', handleBeforeInstallPrompt);
      window.removeEventListener('appinstalled', handleAppInstalled);
      clearTimeout(debugTimer);
    };
  }, [isInstalled]);

  const handleInstall = async () => {
    if (!deferredPrompt) {
      console.log('PWA: No deferred prompt available');
      return;
    }

    try {
      console.log('PWA: Triggering install prompt');
      deferredPrompt.prompt();
      
      const { outcome } = await deferredPrompt.userChoice;
      console.log(`PWA: Install outcome: ${outcome}`);
      
      if (outcome === 'accepted') {
        setIsInstalled(true);
        console.log('PWA: User accepted installation');
      }
      
      setDeferredPrompt(null);
      setShowInstallPrompt(false);
      
    } catch (error) {
      console.error('PWA: Install error:', error);
    }
  };

  const handleDismiss = () => {
    setShowInstallPrompt(false);
    // Show again after 24 hours
    localStorage.setItem('pwa-dismissed', Date.now().toString());
  };

  // Don't show if already installed
  if (isInstalled) {
    return null;
  }

  // iOS Install Instructions
  if (isIOS && !isInstalled) {
    return (
      <div className="fixed bottom-4 left-4 right-4 z-50">
        <Card className="bg-blue-600 text-white border-0 shadow-2xl">
          <div className="p-4">
            <div className="flex items-start gap-3">
              <div className="w-12 h-12 bg-white/20 rounded-xl flex items-center justify-center flex-shrink-0">
                <Download className="w-6 h-6" />
              </div>
              
              <div className="flex-1 min-w-0">
                <h3 className="font-bold text-lg mb-1">Install Golf Guy App</h3>
                <p className="text-blue-100 text-sm mb-3">
                  Tap the Share button <span className="bg-white/20 px-2 py-1 rounded text-xs">📤</span> and select "Add to Home Screen" 
                </p>
                
                <div className="flex gap-2">
                  <Button
                    onClick={handleDismiss}
                    variant="ghost"
                    className="text-white hover:bg-white/10"
                    size="sm"
                  >
                    Got it
                  </Button>
                </div>
              </div>
              
              <button
                onClick={handleDismiss}
                className="text-blue-200 hover:text-white"
              >
                <X className="w-5 h-5" />
              </button>
            </div>
          </div>
        </Card>
      </div>
    );
  }

  // Android/Desktop Install Prompt
  if (showInstallPrompt || deferredPrompt) {
    return (
      <div className="fixed bottom-20 md:bottom-4 left-4 right-4 z-50">
        <div className="bg-emerald-600 text-white border-0 shadow-2xl rounded-xl p-4">
          <div className="flex items-start gap-3">
            <div className="w-12 h-12 bg-white/20 rounded-xl flex items-center justify-center flex-shrink-0">
              <Download className="w-6 h-6" />
            </div>
            
            <div className="flex-1 min-w-0">
              <h3 className="font-bold text-lg mb-1">Install Golf Guy App</h3>
              <p className="text-emerald-100 text-sm mb-3">
                Get faster access, work offline, and enjoy a native app experience!
              </p>
              
              <div className="flex flex-wrap gap-2 mb-3 text-xs">
                <span className="bg-white/20 px-2 py-1 rounded">⚡ Faster loading</span>
                <span className="bg-white/20 px-2 py-1 rounded">📱 App icon</span>
                <span className="bg-white/20 px-2 py-1 rounded">🔄 Offline access</span>
              </div>
              
              <div className="flex gap-2">
                <button
                  onClick={handleInstall}
                  className="bg-white text-emerald-600 hover:bg-gray-100 font-medium px-4 py-2 rounded-lg text-sm flex items-center"
                >
                  <Smartphone className="w-4 h-4 mr-2" />
                  Install Now
                </button>
                <button
                  onClick={handleDismiss}
                  className="text-white hover:bg-white/10 px-4 py-2 rounded-lg text-sm"
                >
                  Later
                </button>
              </div>
            </div>
            
            <button
              onClick={handleDismiss}
              className="text-emerald-200 hover:text-white"
            >
              <X className="w-5 h-5" />
            </button>
          </div>
        </div>
      </div>
    );
  }

  // Debug info (only in development)
  if (process.env.NODE_ENV === 'development') {
    return (
      <div className="fixed top-20 right-4 z-50">
        <Card className="bg-gray-800 text-white text-xs p-2 max-w-xs">
          <div>PWA Debug:</div>
          <div>Prompt: {deferredPrompt ? 'Ready' : 'Not available'}</div>
          <div>Installed: {isInstalled ? 'Yes' : 'No'}</div>
          <div>iOS: {isIOS ? 'Yes' : 'No'}</div>
          <div>Width: {window.innerWidth}px</div>
        </Card>
      </div>
    );
  }

  return null;
};

export default PWAInstaller;