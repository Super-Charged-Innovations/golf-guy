import React, { useState, useEffect } from 'react';
import { X, Download, Menu, Smartphone, Info } from 'lucide-react';

const BrowserInstallGuide = () => {
  const [showGuide, setShowGuide] = useState(false);
  const [browserType, setBrowserType] = useState('');
  const [isStandalone, setIsStandalone] = useState(false);

  useEffect(() => {
    // Check if already installed
    const standalone = window.matchMedia('(display-mode: standalone)').matches || 
                     window.navigator.standalone === true;
    setIsStandalone(standalone);

    if (standalone) return; // Don't show if already installed

    // Detect browser type
    const userAgent = navigator.userAgent.toLowerCase();
    let browser = '';
    
    if (userAgent.includes('vivaldi')) {
      browser = 'vivaldi';
    } else if (userAgent.includes('samsungbrowser') || userAgent.includes('samsung')) {
      browser = 'samsung';
    } else if (userAgent.includes('chrome') && !userAgent.includes('edg')) {
      browser = 'chrome';
    } else if (userAgent.includes('firefox')) {
      browser = 'firefox';
    } else if (userAgent.includes('safari') && !userAgent.includes('chrome')) {
      browser = 'safari';
    } else if (userAgent.includes('edge') || userAgent.includes('edg')) {
      browser = 'edge';
    } else {
      browser = 'generic';
    }
    
    setBrowserType(browser);
    console.log(`PWA: Detected browser: ${browser}`);
    console.log(`PWA: User agent: ${navigator.userAgent}`);

    // Show install guide after user has browsed for a bit (mobile only)
    if (window.innerWidth <= 768) {
      const timer = setTimeout(() => {
        const lastDismissed = localStorage.getItem('pwa-install-dismissed');
        const daysSinceDismiss = lastDismissed ? 
          (Date.now() - parseInt(lastDismissed)) / (1000 * 60 * 60 * 24) : 999;
        
        if (daysSinceDismiss > 7) { // Show every 7 days
          setShowGuide(true);
        }
      }, 8000); // Show after 8 seconds

      return () => clearTimeout(timer);
    }
  }, []);

  const getInstallInstructions = (browser) => {
    const instructions = {
      vivaldi: {
        title: "Install Golf Guy on Vivaldi",
        steps: [
          "1. Tap the menu button (⋮) in the top-right corner",
          "2. Look for 'Add to Home screen' or 'Install app'",
          "3. Tap 'Install' or 'Add' to confirm",
          "4. Find Golf Guy app icon on your home screen"
        ]
      },
      samsung: {
        title: "Install Golf Guy on Samsung Internet",
        steps: [
          "1. Tap the menu button (☰) at the bottom",
          "2. Select 'Add page to' then 'Home screen'", 
          "3. Edit the name if needed and tap 'Add'",
          "4. Golf Guy app will appear on your home screen"
        ]
      },
      chrome: {
        title: "Install Golf Guy on Chrome",
        steps: [
          "1. Tap the menu button (⋮) in the top-right",
          "2. Select 'Add to Home screen' or 'Install app'",
          "3. Confirm by tapping 'Install'",
          "4. Golf Guy app will be installed"
        ]
      },
      firefox: {
        title: "Install Golf Guy on Firefox",
        steps: [
          "1. Tap the menu button (☰)",
          "2. Select 'Page' then 'Add to Home Screen'",
          "3. Edit the name and tap 'Add'",
          "4. Find Golf Guy on your home screen"
        ]
      },
      safari: {
        title: "Install Golf Guy on Safari",
        steps: [
          "1. Tap the Share button (📤) at the bottom",
          "2. Scroll down and tap 'Add to Home Screen'",
          "3. Edit the name if needed",
          "4. Tap 'Add' to install Golf Guy"
        ]
      },
      generic: {
        title: "Install Golf Guy App",
        steps: [
          "1. Look for your browser's menu button",
          "2. Find 'Add to Home screen' or 'Install app' option",
          "3. Follow the prompts to install",
          "4. Enjoy Golf Guy as a native app!"
        ]
      }
    };
    
    return instructions[browser] || instructions.generic;
  };

  const handleDismiss = () => {
    setShowGuide(false);
    localStorage.setItem('pwa-install-dismissed', Date.now().toString());
  };

  const handleShowInstructions = () => {
    setShowGuide(true);
  };

  if (isStandalone) {
    return null; // Already installed
  }

  // Floating install button (always visible on mobile)
  if (window.innerWidth <= 768 && !showGuide) {
    return (
      <button
        onClick={handleShowInstructions}
        className="fixed bottom-24 right-4 w-14 h-14 bg-emerald-600 text-white rounded-full shadow-lg flex items-center justify-center hover:bg-emerald-700 transition-all z-40 md:hidden"
        title="Install Golf Guy App"
      >
        <Download className="w-6 h-6" />
      </button>
    );
  }

  if (!showGuide) return null;

  const instructions = getInstallInstructions(browserType);

  return (
    <div className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4">
      <div className="bg-white rounded-xl max-w-md w-full shadow-2xl">
        <div className="p-6">
          {/* Header */}
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-3">
              <div className="w-12 h-12 bg-emerald-100 rounded-xl flex items-center justify-center">
                <Download className="w-6 h-6 text-emerald-600" />
              </div>
              <div>
                <h3 className="text-lg font-bold text-gray-900">
                  {instructions.title}
                </h3>
                <p className="text-sm text-gray-600">
                  Get the full app experience
                </p>
              </div>
            </div>
            <button
              onClick={handleDismiss}
              className="text-gray-400 hover:text-gray-600"
            >
              <X className="w-5 h-5" />
            </button>
          </div>

          {/* Benefits */}
          <div className="bg-emerald-50 rounded-lg p-3 mb-4">
            <h4 className="font-semibold text-emerald-800 mb-2">App Benefits:</h4>
            <div className="grid grid-cols-2 gap-2 text-sm text-emerald-700">
              <div className="flex items-center gap-1">
                <span>⚡</span> Faster loading
              </div>
              <div className="flex items-center gap-1">
                <span>📱</span> App icon
              </div>
              <div className="flex items-center gap-1">
                <span>🔄</span> Offline access
              </div>
              <div className="flex items-center gap-1">
                <span>🔔</span> Push notifications
              </div>
            </div>
          </div>

          {/* Installation Steps */}
          <div className="space-y-3 mb-4">
            <h4 className="font-semibold text-gray-900">Installation Steps:</h4>
            {instructions.steps.map((step, index) => (
              <div key={index} className="flex gap-3">
                <div className="w-6 h-6 bg-emerald-600 text-white rounded-full flex items-center justify-center text-sm font-medium flex-shrink-0">
                  {index + 1}
                </div>
                <p className="text-sm text-gray-700 pt-1">{step}</p>
              </div>
            ))}
          </div>

          {/* Browser-specific tips */}
          <div className="bg-amber-50 rounded-lg p-3 mb-4">
            <div className="flex items-start gap-2">
              <Info className="w-4 h-4 text-amber-600 mt-0.5 flex-shrink-0" />
              <div className="text-sm">
                <span className="font-medium text-amber-800">Tip:</span>
                <span className="text-amber-700 ml-1">
                  {browserType === 'vivaldi' && "Vivaldi supports PWA installation through the menu."}
                  {browserType === 'samsung' && "Samsung Internet has excellent PWA support."}
                  {browserType === 'chrome' && "Chrome will show an automatic install banner."}
                  {browserType === 'firefox' && "Firefox supports bookmarking to home screen."}
                  {browserType === 'safari' && "Safari requires the Share button method."}
                  {browserType === 'generic' && "Most modern browsers support app installation."}
                </span>
              </div>
            </div>
          </div>

          {/* Action buttons */}
          <div className="flex gap-3">
            <button
              onClick={handleDismiss}
              className="flex-1 bg-emerald-600 text-white py-3 px-4 rounded-lg font-medium hover:bg-emerald-700 transition-colors"
            >
              I'll install it now
            </button>
            <button
              onClick={handleDismiss}
              className="px-4 py-3 text-gray-600 hover:text-gray-800 transition-colors"
            >
              Maybe later
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default BrowserInstallGuide;