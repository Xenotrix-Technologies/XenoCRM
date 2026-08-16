const CACHE_NAME = 'xenocrm-static-v3.0';
const OFFLINE_URL = '/offline/';

// Safe static assets ONLY - NO authenticated HTML views, NO private ERP data, NO APIs!
const STATIC_ASSETS = [
  '/static/pwa/manifest.json?v=3.0',
  '/static/pwa/pwa-init.js',
  '/static/css/main.css',
  '/static/css/form_styles.css',
  '/static/css/invoices.css',
  '/static/js/nav.js',
  '/static/pwa/icons/icon-192.png?v=3.0',
  '/static/pwa/icons/icon-512.png?v=3.0',
  '/static/pwa/icons/icon-maskable-192.png?v=3.0',
  '/static/pwa/icons/icon-maskable-512.png?v=3.0',
  '/static/pwa/icons/apple-touch-icon.png?v=3.0',
  '/static/pwa/icons/favicon.ico?v=3.0',
  OFFLINE_URL
];

// Install Event - Pre-cache safe app shell & offline assets
self.addEventListener('install', (event) => {
  self.skipWaiting();
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      console.log('[XenoCRM SW] Pre-caching static assets and offline fallback v3.0');
      return cache.addAll(STATIC_ASSETS).catch((err) => {
        console.warn('[XenoCRM SW] Pre-cache error (ignored for non-critical files):', err);
      });
    })
  );
});

// Activate Event - Clean up stale caches and notify clients
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
  if (request.mode === 'navigate' || (request.headers.get('accept') && request.headers.get('accept').includes('text/html'))) {
    event.respondWith(
      fetch(request).catch(() => {
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

  // 3. Manifest & PWA Icon Updates -> Network First to reflect brand/icon updates instantly
  if (url.pathname.includes('manifest.json') || url.pathname.includes('/pwa/icons/')) {
    event.respondWith(
      fetch(request).then((networkResponse) => {
        if (networkResponse && networkResponse.status === 200) {
          const responseToCache = networkResponse.clone();
          caches.open(CACHE_NAME).then((cache) => cache.put(request, responseToCache));
        }
        return networkResponse;
      }).catch(() => caches.match(request))
    );
    return;
  }

  // 4. Static Assets (CSS, JS, Web Fonts, Images)
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
          fetch(request).then((networkResponse) => {
            if (networkResponse && networkResponse.status === 200) {
              caches.open(CACHE_NAME).then((cache) => cache.put(request, networkResponse));
            }
          }).catch(() => {});
          return cachedResponse;
        }

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
