import React, { useState, useEffect } from 'react';
import { Button } from './ui/button';
import { Card } from './ui/card';
import { Switch } from './ui/switch';
import { X, Cookie, Settings, Shield, BarChart3 } from 'lucide-react';

const CookieConsent = () => {
  const [isVisible, setIsVisible] = useState(false);
  const [showDetails, setShowDetails] = useState(false);
  const [preferences, setPreferences] = useState({
    necessary: true, // Always required
    functional: false,
    analytics: false,
    marketing: false
  });

  useEffect(() => {
    // Check if user has already made a consent decision
    const consent = localStorage.getItem('cookie-consent');
    if (!consent) {
      // Delay showing banner slightly for better UX
      const timer = setTimeout(() => {
        setIsVisible(true);
      }, 1500);
      return () => clearTimeout(timer);
    }
  }, []);

  const handleAcceptAll = () => {
    const allAccepted = {
      necessary: true,
      functional: true,
      analytics: true,
      marketing: true,
      timestamp: new Date().toISOString()
    };
    localStorage.setItem('cookie-consent', JSON.stringify(allAccepted));
    setIsVisible(false);
    
    // Initialize analytics and marketing cookies if accepted
    if (window.gtag) {
      window.gtag('consent', 'update', {
        analytics_storage: 'granted',
        ad_storage: 'granted'
      });
    }
  };

  const handleRejectAll = () => {
    const onlyNecessary = {
      necessary: true,
      functional: false,
      analytics: false,
      marketing: false,
      timestamp: new Date().toISOString()
    };
    localStorage.setItem('cookie-consent', JSON.stringify(onlyNecessary));
    setIsVisible(false);
  };

  const handleSavePreferences = () => {
    const consent = {
      ...preferences,
      timestamp: new Date().toISOString()
    };
    localStorage.setItem('cookie-consent', JSON.stringify(consent));
    setIsVisible(false);
    
    // Update consent based on user preferences
    if (window.gtag) {
      window.gtag('consent', 'update', {
        analytics_storage: preferences.analytics ? 'granted' : 'denied',
        ad_storage: preferences.marketing ? 'granted' : 'denied'
      });
    }
  };

  const togglePreference = (key) => {
    if (key === 'necessary') return; // Can't toggle necessary cookies
    setPreferences(prev => ({
      ...prev,
      [key]: !prev[key]
    }));
  };

  if (!isVisible) return null;

  return (
    <div className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-end justify-center p-4">
      <Card className="w-full max-w-4xl bg-white shadow-2xl border-0 animate-in slide-in-from-bottom-4">
        <div className="p-6">
          {/* Header */}
          <div className="flex items-start justify-between mb-4">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 bg-emerald-100 rounded-full flex items-center justify-center">
                <Cookie className="w-5 h-5 text-emerald-600" />
              </div>
              <div>
                <h2 className="text-xl font-bold text-gray-900">
                  Cookie & Privacy Settings
                </h2>
                <p className="text-sm text-gray-600">
                  We respect your privacy and are committed to transparency
                </p>
              </div>
            </div>
            <Button
              variant="ghost"
              size="sm"
              onClick={() => setIsVisible(false)}
              className="text-gray-400 hover:text-gray-600"
            >
              <X className="w-4 h-4" />
            </Button>
          </div>

          {/* Main Content */}
          {!showDetails ? (
            <div className="space-y-4">
              <p className="text-gray-700 leading-relaxed">
                We use cookies and similar technologies to enhance your browsing experience, 
                provide personalized content and ads, and analyze our traffic. Some cookies 
                are necessary for our website to function properly, while others help us 
                understand how you interact with our platform to improve your experience.
              </p>
              
              <div className="flex flex-wrap gap-3">
                <Button 
                  onClick={handleAcceptAll}
                  className="bg-emerald-600 hover:bg-emerald-700 text-white"
                >
                  Accept All Cookies
                </Button>
                <Button 
                  variant="outline" 
                  onClick={handleRejectAll}
                  className="border-gray-300 text-gray-700 hover:bg-gray-50"
                >
                  Reject All
                </Button>
                <Button 
                  variant="outline"
                  onClick={() => setShowDetails(true)}
                  className="border-emerald-600 text-emerald-600 hover:bg-emerald-50"
                >
                  <Settings className="w-4 h-4 mr-2" />
                  Customize
                </Button>
              </div>

              <div className="text-xs text-gray-500 space-x-4">
                <a href="/privacy-policy" className="hover:text-emerald-600 underline">
                  Privacy Policy
                </a>
                <a href="/cookie-policy" className="hover:text-emerald-600 underline">
                  Cookie Policy
                </a>
                <a href="/terms" className="hover:text-emerald-600 underline">
                  Terms of Service
                </a>
              </div>
            </div>
          ) : (
            <div className="space-y-6">
              <div className="grid gap-4">
                {/* Necessary Cookies */}
                <div className="flex items-start justify-between p-4 bg-gray-50 rounded-lg">
                  <div className="flex items-start gap-3 flex-1">
                    <Shield className="w-5 h-5 text-green-600 mt-1" />
                    <div className="flex-1">
                      <h3 className="font-semibold text-gray-900 mb-1">
                        Necessary Cookies
                      </h3>
                      <p className="text-sm text-gray-600 mb-2">
                        Essential for the website to function. These cookies enable core 
                        functionality such as security, network management, and accessibility.
                      </p>
                      <div className="text-xs text-gray-500">
                        Examples: Authentication, session management, form submissions
                      </div>
                    </div>
                  </div>
                  <div className="ml-4">
                    <Switch 
                      checked={true} 
                      disabled={true}
                      className="data-[state=checked]:bg-green-600"
                    />
                    <div className="text-xs text-gray-500 mt-1">Always Active</div>
                  </div>
                </div>

                {/* Functional Cookies */}
                <div className="flex items-start justify-between p-4 border rounded-lg">
                  <div className="flex items-start gap-3 flex-1">
                    <Settings className="w-5 h-5 text-blue-600 mt-1" />
                    <div className="flex-1">
                      <h3 className="font-semibold text-gray-900 mb-1">
                        Functional Cookies
                      </h3>
                      <p className="text-sm text-gray-600 mb-2">
                        Help us provide enhanced functionality and personalization, 
                        such as language preferences and chat widgets.
                      </p>
                      <div className="text-xs text-gray-500">
                        Examples: Language settings, AI chat preferences, user interface customization
                      </div>
                    </div>
                  </div>
                  <div className="ml-4">
                    <Switch 
                      checked={preferences.functional}
                      onCheckedChange={() => togglePreference('functional')}
                      className="data-[state=checked]:bg-emerald-600"
                    />
                  </div>
                </div>

                {/* Analytics Cookies */}
                <div className="flex items-start justify-between p-4 border rounded-lg">
                  <div className="flex items-start gap-3 flex-1">
                    <BarChart3 className="w-5 h-5 text-orange-600 mt-1" />
                    <div className="flex-1">
                      <h3 className="font-semibold text-gray-900 mb-1">
                        Analytics Cookies
                      </h3>
                      <p className="text-sm text-gray-600 mb-2">
                        Help us understand how visitors interact with our website 
                        by collecting and reporting information anonymously.
                      </p>
                      <div className="text-xs text-gray-500">
                        Examples: Google Analytics, page views, user behavior tracking
                      </div>
                    </div>
                  </div>
                  <div className="ml-4">
                    <Switch 
                      checked={preferences.analytics}
                      onCheckedChange={() => togglePreference('analytics')}
                      className="data-[state=checked]:bg-emerald-600"
                    />
                  </div>
                </div>

                {/* Marketing Cookies */}
                <div className="flex items-start justify-between p-4 border rounded-lg">
                  <div className="flex items-start gap-3 flex-1">
                    <Cookie className="w-5 h-5 text-purple-600 mt-1" />
                    <div className="flex-1">
                      <h3 className="font-semibold text-gray-900 mb-1">
                        Marketing Cookies
                      </h3>
                      <p className="text-sm text-gray-600 mb-2">
                        Used to track visitors across websites and display ads 
                        that are relevant and engaging for individual users.
                      </p>
                      <div className="text-xs text-gray-500">
                        Examples: Ad targeting, social media pixels, conversion tracking
                      </div>
                    </div>
                  </div>
                  <div className="ml-4">
                    <Switch 
                      checked={preferences.marketing}
                      onCheckedChange={() => togglePreference('marketing')}
                      className="data-[state=checked]:bg-emerald-600"
                    />
                  </div>
                </div>
              </div>

              <div className="flex flex-wrap gap-3 pt-4 border-t">
                <Button 
                  onClick={handleSavePreferences}
                  className="bg-emerald-600 hover:bg-emerald-700 text-white"
                >
                  Save Preferences
                </Button>
                <Button 
                  variant="outline"
                  onClick={() => setShowDetails(false)}
                  className="border-gray-300 text-gray-700 hover:bg-gray-50"
                >
                  Back
                </Button>
                <Button 
                  variant="ghost"
                  onClick={handleAcceptAll}
                  className="text-emerald-600 hover:text-emerald-700 hover:bg-emerald-50"
                >
                  Accept All
                </Button>
              </div>
            </div>
          )}
        </div>
      </Card>
    </div>
  );
};

export default CookieConsent;