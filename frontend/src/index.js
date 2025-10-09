import React from "react";
import ReactDOM from "react-dom/client";
import "@/index.css";
import App from "@/App";

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
);

// Register service worker for PWA functionality with enhanced browser support
if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('/sw.js', {
      scope: '/',
      updateViaCache: 'none'
    })
    .then((registration) => {
      console.log('PWA: Service Worker registered successfully:', registration.scope);
      
      // Check for updates periodically
      setInterval(() => {
        registration.update();
      }, 60000); // Check every minute
      
      // Listen for new service worker
      registration.addEventListener('updatefound', () => {
        const newWorker = registration.installing;
        if (newWorker) {
          newWorker.addEventListener('statechange', () => {
            if (newWorker.state === 'installed') {
              console.log('PWA: New version available');
              if (navigator.serviceWorker.controller) {
                // Show update notification
                if (confirm('New version of Golf Guy is available! Update now?')) {
                  newWorker.postMessage({ type: 'SKIP_WAITING' });
                  window.location.reload();
                }
              }
            }
          });
        }
      });
    })
    .catch((error) => {
      console.error('PWA: Service Worker registration failed:', error);
    });
  });

  // Enhanced PWA detection and debugging
  navigator.serviceWorker.ready.then((registration) => {
    console.log('PWA: Service Worker is ready');
    
    // Force install prompt check (browser-specific)
    if (window.navigator.userAgent.includes('Samsung') || 
        window.navigator.userAgent.includes('Vivaldi')) {
      console.log('PWA: Detected Samsung Internet/Vivaldi - triggering enhanced install check');
      
      // Dispatch custom event to trigger install prompt
      setTimeout(() => {
        if (!window.matchMedia('(display-mode: standalone)').matches) {
          console.log('PWA: Attempting to trigger install prompt for Samsung/Vivaldi');
          window.dispatchEvent(new Event('pwa-install-available'));
        }
      }, 5000);
    }
  });
}

// Enhanced PWA install prompt for specific browsers
window.addEventListener('pwa-install-available', () => {
  console.log('PWA: Custom install event triggered');
  
  // Show custom install instruction for browsers that don't support beforeinstallprompt
  const installInstructions = document.createElement('div');
  installInstructions.innerHTML = `
    <div style="
      position: fixed; 
      bottom: 20px; 
      left: 20px; 
      right: 20px; 
      background: #10b981; 
      color: white; 
      padding: 16px; 
      border-radius: 12px; 
      box-shadow: 0 8px 32px rgba(0,0,0,0.3);
      z-index: 1000;
      font-family: -apple-system, BlinkMacSystemFont, sans-serif;
    ">
      <div style="display: flex; align-items: center; gap: 12px;">
        <div style="font-size: 24px;">📱</div>
        <div style="flex: 1;">
          <div style="font-weight: bold; margin-bottom: 4px;">Install Golf Guy App</div>
          <div style="font-size: 14px; opacity: 0.9;">
            Tap your browser menu (⋮) and select "Add to Home screen" or "Install app"
          </div>
        </div>
        <button onclick="this.parentElement.parentElement.remove()" style="
          background: rgba(255,255,255,0.2); 
          border: none; 
          color: white; 
          padding: 8px; 
          border-radius: 6px;
          cursor: pointer;
        ">✕</button>
      </div>
    </div>
  `;
  
  document.body.appendChild(installInstructions);
  
  // Auto-remove after 30 seconds
  setTimeout(() => {
    if (installInstructions.parentNode) {
      installInstructions.remove();
    }
  }, 30000);
});

// Check PWA installation criteria
function checkPWAInstallability() {
  const criteria = {
    https: location.protocol === 'https:',
    manifest: document.querySelector('link[rel="manifest"]') !== null,
    serviceWorker: 'serviceWorker' in navigator,
    standalone: !window.matchMedia('(display-mode: standalone)').matches
  };
  
  console.log('PWA Installability Criteria:', criteria);
  
  const allMet = Object.values(criteria).every(Boolean);
  console.log('PWA: All criteria met:', allMet);
  
  return criteria;
}

// Run PWA check after page load
window.addEventListener('load', () => {
  setTimeout(() => {
    checkPWAInstallability();
  }, 2000);
});
