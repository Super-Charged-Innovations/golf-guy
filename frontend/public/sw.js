// Golf Guy PWA Service Worker
// Handles offline functionality, caching, and push notifications

const CACHE_NAME = 'golf-guy-v2.0.0';
const OFFLINE_URL = '/offline.html';

// Assets to cache for offline functionality
const STATIC_ASSETS = [
  '/',
  '/destinations',
  '/about',
  '/contact',
  OFFLINE_URL,
  // Core styles and scripts
  '/static/css/main.css',
  '/static/js/main.js',
  // Essential images
  '/icons/icon-192x192.png',
  '/icons/icon-512x512.png'
];

// API endpoints to cache responses
const CACHEABLE_API_PATTERNS = [
  /\/api\/destinations$/,
  /\/api\/articles$/,
  /\/api\/i18n\/translations/
];

self.addEventListener('install', (event) => {
  console.log('Golf Guy SW: Install event');
  
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => {
        console.log('Golf Guy SW: Caching static assets');
        return cache.addAll(STATIC_ASSETS);
      })
      .catch((error) => {
        console.error('Golf Guy SW: Error during install:', error);
      })
  );
  
  // Force activation of new service worker
  self.skipWaiting();
});

self.addEventListener('activate', (event) => {
  console.log('Golf Guy SW: Activate event');
  
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames
          .filter((name) => name !== CACHE_NAME)
          .map((name) => {
            console.log('Golf Guy SW: Deleting old cache:', name);
            return caches.delete(name);
          })
      );
    }).then(() => {
      // Ensure SW controls all tabs immediately
      return self.clients.claim();
    })
  );
});

self.addEventListener('fetch', (event) => {
  // Skip non-GET requests and chrome extensions
  if (event.request.method !== 'GET' || event.request.url.startsWith('chrome-extension://')) {
    return;
  }

  const url = new URL(event.request.url);
  
  // Handle different types of requests
  if (url.pathname.startsWith('/api/')) {
    // API requests - cache strategy
    event.respondWith(handleApiRequest(event.request));
  } else {
    // Static assets and pages - cache first strategy
    event.respondWith(handleStaticRequest(event.request));
  }
});

async function handleApiRequest(request) {
  const url = new URL(request.url);
  
  // Check if this API endpoint should be cached
  const shouldCache = CACHEABLE_API_PATTERNS.some(pattern => 
    pattern.test(url.pathname)
  );
  
  if (!shouldCache) {
    // For non-cacheable API requests (like POST, auth), just fetch
    try {
      return await fetch(request);
    } catch (error) {
      console.log('Golf Guy SW: API request failed, returning error');
      return new Response(
        JSON.stringify({ 
          error: 'Network unavailable', 
          message: 'Please check your connection and try again',
          offline: true 
        }),
        { 
          status: 503,
          headers: { 'Content-Type': 'application/json' }
        }
      );
    }
  }
  
  // For cacheable API requests, use network first with cache fallback
  try {
    const response = await fetch(request);
    
    // Cache successful responses
    if (response.status === 200) {
      const cache = await caches.open(CACHE_NAME);
      await cache.put(request, response.clone());
    }
    
    return response;
  } catch (error) {
    // Network failed, try cache
    const cachedResponse = await caches.match(request);
    if (cachedResponse) {
      console.log('Golf Guy SW: Serving cached API response');
      return cachedResponse;
    }
    
    // No cache available, return error
    return new Response(
      JSON.stringify({ 
        error: 'Data unavailable offline',
        message: 'This content requires an internet connection',
        offline: true 
      }),
      { 
        status: 503,
        headers: { 'Content-Type': 'application/json' }
      }
    );
  }
}

async function handleStaticRequest(request) {
  // Cache first strategy for static assets
  const cachedResponse = await caches.match(request);
  
  if (cachedResponse) {
    console.log('Golf Guy SW: Serving from cache:', request.url);
    return cachedResponse;
  }
  
  try {
    const response = await fetch(request);
    
    // Cache successful responses
    if (response.status === 200) {
      const cache = await caches.open(CACHE_NAME);
      await cache.put(request, response.clone());
    }
    
    return response;
  } catch (error) {
    console.log('Golf Guy SW: Network failed, serving offline page');
    
    // For navigation requests, serve offline page
    if (request.mode === 'navigate') {
      const cache = await caches.open(CACHE_NAME);
      return cache.match(OFFLINE_URL);
    }
    
    // For other requests, return generic error
    return new Response('Offline', { status: 503 });
  }
}

// Handle background sync for offline actions
self.addEventListener('sync', (event) => {
  console.log('Golf Guy SW: Background sync:', event.tag);
  
  if (event.tag === 'background-sync-bookings') {
    event.waitUntil(syncOfflineBookings());
  }
  
  if (event.tag === 'background-sync-inquiries') {
    event.waitUntil(syncOfflineInquiries());
  }
});

async function syncOfflineBookings() {
  console.log('Golf Guy SW: Syncing offline bookings');
  
  try {
    // Get offline bookings from IndexedDB (if implemented)
    // Send them to server when connection is restored
    // This would integrate with booking system
  } catch (error) {
    console.error('Golf Guy SW: Error syncing bookings:', error);
  }
}

async function syncOfflineInquiries() {
  console.log('Golf Guy SW: Syncing offline inquiries');
  
  try {
    // Get offline inquiries from IndexedDB
    // Send them to server when connection is restored
  } catch (error) {
    console.error('Golf Guy SW: Error syncing inquiries:', error);
  }
}

// Handle push notifications (for booking confirmations, etc.)
self.addEventListener('push', (event) => {
  console.log('Golf Guy SW: Push notification received');
  
  let data = {};
  if (event.data) {
    try {
      data = event.data.json();
    } catch (error) {
      data = { message: event.data.text() };
    }
  }
  
  const title = data.title || 'Golf Guy';
  const options = {
    body: data.message || 'You have a new golf notification',
    icon: '/icons/icon-192x192.png',
    badge: '/icons/badge-72x72.png',
    vibrate: [100, 50, 100],
    data: {
      dateOfArrival: Date.now(),
      primaryKey: data.id || '1',
      url: data.url || '/'
    },
    actions: data.actions || [
      {
        action: 'view',
        title: 'View Details'
      },
      {
        action: 'close',
        title: 'Dismiss'
      }
    ]
  };
  
  event.waitUntil(
    self.registration.showNotification(title, options)
  );
});

// Handle notification clicks
self.addEventListener('notificationclick', (event) => {
  console.log('Golf Guy SW: Notification clicked');
  
  event.notification.close();
  
  const urlToOpen = event.notification.data.url || '/';
  
  event.waitUntil(
    clients.matchAll({
      type: 'window',
      includeUncontrolled: true
    }).then((windowClients) => {
      // Check if app is already open
      const existingClient = windowClients.find(client => 
        client.url.includes(urlToOpen)
      );
      
      if (existingClient) {
        return existingClient.focus();
      } else if (windowClients.length > 0) {
        return windowClients[0].navigate(urlToOpen).then(client => client.focus());
      } else {
        return clients.openWindow(urlToOpen);
      }
    })
  );
});

// Handle app updates
self.addEventListener('message', (event) => {
  if (event.data && event.data.type === 'SKIP_WAITING') {
    console.log('Golf Guy SW: Skipping waiting');
    self.skipWaiting();
  }
});

console.log('Golf Guy Service Worker loaded successfully');