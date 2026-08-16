const CACHE_NAME = 'xenocrm-static-v1.0';
const OFFLINE_URL = '/offline/';

// Safe static assets ONLY - NO authenticated HTML views, NO private ERP data, NO APIs!
const STATIC_ASSETS = [
  '/static/pwa/manifest.json',
  '/static/pwa/pwa-init.js',
  '/static/css/main.css',
  '/static/css/form_styles.css',
  '/static/css/invoices.css',
  '/static/js/nav.js',
  '/static/pwa/icons/icon-192.png',
  '/static/pwa/icons/icon-512.png',
  '/static/pwa/icons/icon-maskable-192.png',
  '/static/pwa/icons/icon-maskable-512.png',
  '/static/pwa/icons/apple-touch-icon.png',
  '/static/pwa/icons/favicon.ico',
  OFFLINE_URL
];

// Install Event - Pre-cache safe app shell & offline assets
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      console.log('[XenoCRM SW] Pre-caching static assets and offline fallback');
      return cache.addAll(STATIC_ASSETS).catch((err) => {
        console.warn('[XenoCRM SW] Pre-cache error (ignored for non-critical files):', err);
      });
    }).then(() => self.skipWaiting())
  );
});

// Activate Event - Clean up stale caches
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cacheName) => {
          if (cacheName !== CACHE_NAME) {
            console.log('[XenoCRM SW] Deleting obsolete cache:', cacheName);
            return caches.delete(cacheName);
          }
        })
      );
    }).then(() => self.clients.claim())
  );
});

// Fetch Event - Secure Caching Strategy
self.addEventListener('fetch', (event) => {
  const request = event.request;
  const url = new URL(request.url);

  // 1. NON-GET Requests (POST, PUT, DELETE, etc.) -> ALWAYS direct network call
  if (request.method !== 'GET') {
    return;
  }

  // 2. HTML Navigation Requests (ERP Pages, Views, Reports, APIs)
  // SECURITY REQUIREMENT: Never cache private authenticated HTML data!
  if (request.mode === 'navigate' || (request.headers.get('accept') && request.headers.get('accept').includes('text/html'))) {
    event.respondWith(
      fetch(request).catch(() => {
        // Network failed (Offline) -> Serve pre-cached safe Offline Fallback Page
        console.log('[XenoCRM SW] Offline navigation fallback for:', request.url);
        return caches.match(OFFLINE_URL).then((offlineResponse) => {
          return offlineResponse || new Response(
            '<html><body style="font-family:sans-serif;padding:2rem;text-align:center;"><h2>Offline</h2><p>Network connection unavailable. Please check your internet connection.</p></body></html>',
            { headers: { 'Content-Type': 'text/html' } }
          );
        });
      })
    );
    return;
  }

  // 3. Static Assets (CSS, JS, Web Fonts, PWA Icons, Images)
  if (
    url.pathname.startsWith('/static/') ||
    url.hostname.includes('cdn.jsdelivr.net') ||
    url.hostname.includes('cdn.tailwindcss.com') ||
    url.hostname.includes('unpkg.com') ||
    url.hostname.includes('fonts.googleapis.com') ||
    url.hostname.includes('fonts.gstatic.com')
  ) {
    event.respondWith(
      caches.match(request).then((cachedResponse) => {
        if (cachedResponse) {
          // Return cached static asset immediately & update cache in background
          fetch(request).then((networkResponse) => {
            if (networkResponse && networkResponse.status === 200) {
              caches.open(CACHE_NAME).then((cache) => cache.put(request, networkResponse));
            }
          }).catch(() => {/* Ignore network error for background revalidation */});
          return cachedResponse;
        }

        // Asset not in cache -> Fetch from network & cache it safely
        return fetch(request).then((networkResponse) => {
          if (networkResponse && networkResponse.status === 200 && networkResponse.type === 'basic') {
            const responseToCache = networkResponse.clone();
            caches.open(CACHE_NAME).then((cache) => cache.put(request, responseToCache));
          }
          return networkResponse;
        }).catch((err) => {
          console.warn('[XenoCRM SW] Failed to fetch static asset:', request.url, err);
        });
      })
    );
    return;
  }

  // 4. Default: Network first fallback
  event.respondWith(
    fetch(request).catch(() => caches.match(request))
  );
});

// Skip waiting message listener for PWA auto-updates
self.addEventListener('message', (event) => {
  if (event.data && event.data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }
});
