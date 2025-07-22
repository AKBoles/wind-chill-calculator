const CACHE_NAME = "weather-utility-pro-v2";
const urlsToCache = [
  "/",
  "/static/manifest.json",
  "/static/service-worker.js",
  "/static/icons/icon-192.png",
  "/static/icons/icon-512.png"
];

// Install the service worker and cache resources
self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      console.log("Caching app shell");
      return cache.addAll(urlsToCache);
    })
  );
  // Force the waiting service worker to become the active service worker
  self.skipWaiting();
});

// Fetch files from the cache first, then network
self.addEventListener("fetch", (event) => {
  // Skip cross-origin requests
  if (!event.request.url.startsWith(self.location.origin)) {
    return;
  }

  event.respondWith(
    caches.match(event.request).then((response) => {
      // Return cached version or fetch from network
      if (response) {
        return response;
      }
      
      return fetch(event.request).then((response) => {
        // Don't cache non-successful responses
        if (!response || response.status !== 200 || response.type !== 'basic') {
          return response;
        }

        // Clone the response as it can only be consumed once
        const responseToCache = response.clone();

        caches.open(CACHE_NAME).then((cache) => {
          cache.put(event.request, responseToCache);
        });

        return response;
      }).catch(() => {
        // Return a fallback response for navigation requests
        if (event.request.mode === 'navigate') {
          return caches.match('/');
        }
      });
    })
  );
});

// Activate the new service worker and clear old caches
self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames
          .filter((name) => name !== CACHE_NAME)
          .map((name) => {
            console.log("Deleting old cache:", name);
            return caches.delete(name);
          })
      );
    })
  );
  // Ensure the new service worker takes control immediately
  self.clients.claim();
});

// Handle background sync for future enhancements
self.addEventListener('sync', (event) => {
  console.log('Background sync triggered');
});

// Handle push notifications for future weather alerts
self.addEventListener('push', (event) => {
  if (event.data) {
    const data = event.data.json();
    const options = {
      body: data.body,
      icon: '/static/icons/icon-192.png',
      badge: '/static/icons/icon-192.png',
      tag: 'weather-alert'
    };
    
    event.waitUntil(
      self.registration.showNotification(data.title, options)
    );
  }
});
