// Golf Guy PWA Service Worker v2.0
// Enhanced for browser compatibility (Vivaldi, Samsung Internet, Chrome, Safari)

const CACHE_NAME = 'golf-guy-v2.0.0';
const OFFLINE_URL = '/offline.html';

// Critical assets for PWA functionality
const ESSENTIAL_ASSETS = [
  '/',
  '/destinations',
  '/offline.html',
  '/manifest.json'
];

// Optional assets for better offline experience
const OPTIONAL_ASSETS = [
  '/about',
  '/contact',
  '/static/css/main.css',
  '/logo192.png',
  '/logo512.png'
];

self.addEventListener('install', (event) => {
  console.log('[Golf Guy SW] Installing service worker version 2.0');
  
  event.waitUntil(
    caches.open(CACHE_NAME).then(async (cache) => {
      console.log('[Golf Guy SW] Caching essential assets');
      
      try {
        // Cache essential assets first
        await cache.addAll(ESSENTIAL_ASSETS);
        console.log('[Golf Guy SW] Essential assets cached successfully');
        
        // Cache optional assets (don't fail if these fail)
        for (const asset of OPTIONAL_ASSETS) {
          try {
            await cache.add(asset);
          } catch (error) {
            console.log(`[Golf Guy SW] Optional asset failed: ${asset}`);
          }
        }
        
      } catch (error) {
        console.error('[Golf Guy SW] Caching failed:', error);
      }
    })
  );
  
  // Activate immediately
  self.skipWaiting();
});

self.addEventListener('activate', (event) => {
  console.log('[Golf Guy SW] Activating service worker');
  
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames
          .filter((name) => name !== CACHE_NAME)
          .map((name) => {
            console.log('[Golf Guy SW] Deleting old cache:', name);
            return caches.delete(name);
          })
      );
    }).then(() => {
      console.log('[Golf Guy SW] Service worker activated and ready');
      return self.clients.claim();
    })
  );
});

self.addEventListener('fetch', (event) => {
  // Skip non-GET requests and browser extension requests
  if (event.request.method !== 'GET' || 
      event.request.url.includes('chrome-extension://') ||
      event.request.url.includes('browser-extension://')) {
    return;
  }

  event.respondWith(handleRequest(event.request));
});

async function handleRequest(request) {
  const url = new URL(request.url);
  
  // For navigation requests, try network first, then cache, then offline page
  if (request.mode === 'navigate') {
    try {
      const response = await fetch(request);
      if (response.status === 200) {
        // Cache the successful response
        const cache = await caches.open(CACHE_NAME);
        await cache.put(request, response.clone());
        return response;
      }
    } catch (error) {
      console.log('[Golf Guy SW] Network failed for navigation, trying cache');
    }
    
    // Try cache
    const cachedResponse = await caches.match(request);
    if (cachedResponse) {
      return cachedResponse;
    }
    
    // Return offline page
    return caches.match(OFFLINE_URL);
  }
  
  // For other requests, try cache first, then network
  const cachedResponse = await caches.match(request);
  if (cachedResponse) {
    return cachedResponse;
  }
  
  try {
    const response = await fetch(request);
    if (response.status === 200) {
      const cache = await caches.open(CACHE_NAME);
      await cache.put(request, response.clone());
    }
    return response;
  } catch (error) {
    // Return generic offline response for failed requests
    if (request.destination === 'document') {
      return caches.match(OFFLINE_URL);
    }
    return new Response('Offline', { status: 503 });
  }
}

// Enhanced PWA install criteria checking
self.addEventListener('message', (event) => {
  console.log('[Golf Guy SW] Received message:', event.data);
  
  if (event.data && event.data.type === 'SKIP_WAITING') {
    console.log('[Golf Guy SW] Skipping waiting, activating immediately');
    self.skipWaiting();
  }
  
  if (event.data && event.data.type === 'GET_VERSION') {
    event.ports[0].postMessage({ version: CACHE_NAME });
  }
});

console.log('[Golf Guy SW] Service Worker v2.0 loaded and ready for enhanced PWA experience');