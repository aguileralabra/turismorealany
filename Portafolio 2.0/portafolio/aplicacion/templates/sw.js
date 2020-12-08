const OFFLINE = 'Turismo Real'
const CACHE_NAME = 'vl_cache_reservas';
const URLS_TO_CACHE = [
                    'static/img/deparmen5.jpg',
                    'static/img/deparment2.jpg',
                    'static/img/deparment3.jpg',
                    'static/img/departamento7.jpg',
                    'static/img/departamento8.jpg',
                    'static/img/family.jpg',
                    'static/img/logo-xd.png',
                    'static/img/logo.PNG',
                    'static/swInstall.js',
                    'static/manifest.json',
                    '/sw.js',
                      ]
self.addEventListener('install', e => {
  e.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        return cache.addAll(URLS_TO_CACHE)
          .then (() => self.skipWaiting())
      })
  )
})
self.addEventListener('activate', e => {
  const cacheWhiteList = [CACHE_NAME]
  e.waitUntil(
    caches.keys()
      .then(cacheNames => {
        return Promise.all(
          cacheNames.map(cacheName => {
            if (cacheWhiteList.indexOf(cacheName) === -1) {
              return caches.delete(cacheName)
            }
          })
        )
      })
      .then(() => self.clients.claim())
  )
})
self.addEventListener("fetch", function(event) {
  event.respondWith(
    fetch(event.request).catch(function() {
      return caches.match(event.request).then(function(response) {
        return response || caches.match(OFFLINE);
      });
    })
  );
});
