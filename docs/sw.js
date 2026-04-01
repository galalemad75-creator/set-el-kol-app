/* ==========================================================
   Service Worker — ست الكل | Set El Kol
   Caches app shell + recent recipes for offline support
   ========================================================== */

const CACHE_NAME = 'setelkol-v3b';
const SHELL_ASSETS = [
  '/',
  '/index.html',
  '/icon-192.png',
  '/icon-512.png',
  '/manifest.json'
];

const API_CACHE = 'setelkol-api-v1';
const API_DOMAIN = 'www.themealdb.com';
const MAX_API_ENTRIES = 50;

// ========== INSTALL ==========
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => cache.addAll(SHELL_ASSETS))
  );
  self.skipWaiting();
});

// ========== ACTIVATE ==========
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(keys =>
      Promise.all(
        keys
          .filter(key => key !== CACHE_NAME && key !== API_CACHE)
          .map(key => caches.delete(key))
      )
    )
  );
  self.clients.claim();
});

// ========== FETCH ==========
self.addEventListener('fetch', event => {
  const { request } = event;
  const url = new URL(request.url);

  // API requests: network-first, cache fallback
  if (url.hostname === API_DOMAIN) {
    event.respondWith(networkFirst(request));
    return;
  }

  // Shell assets: cache-first
  if (request.method === 'GET') {
    event.respondWith(cacheFirst(request));
    return;
  }
});

// ========== STRATEGIES ==========

async function cacheFirst(request) {
  const cached = await caches.match(request);
  if (cached) return cached;
  try {
    const response = await fetch(request);
    if (response.ok) {
      const cache = await caches.open(CACHE_NAME);
      cache.put(request, response.clone());
    }
    return response;
  } catch (e) {
    // Offline fallback for navigation
    if (request.mode === 'navigate') {
      return caches.match('/index.html');
    }
    throw e;
  }
}

async function networkFirst(request) {
  try {
    const response = await fetch(request);
    if (response.ok) {
      const cache = await caches.open(API_CACHE);
      cache.put(request, response.clone());
      trimCache(API_CACHE, MAX_API_ENTRIES);
    }
    return response;
  } catch (e) {
    const cached = await caches.match(request);
    if (cached) return cached;
    throw e;
  }
}

// ========== CACHE MANAGEMENT ==========
async function trimCache(name, maxEntries) {
  const cache = await caches.open(name);
  const keys = await cache.keys();
  if (keys.length > maxEntries) {
    // Delete oldest entries
    for (let i = 0; i < keys.length - maxEntries; i++) {
      await cache.delete(keys[i]);
    }
  }
}
