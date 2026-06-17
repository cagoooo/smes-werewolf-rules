/* 石門國小狼人殺規則站 Service Worker — 版本控管 + 更新通知 */
const BUILD_VERSION = '2026.06.17-8';        // 每次部署改它（或跑 scripts/bump-version.ps1）
const CACHE = 'wolf-' + BUILD_VERSION;
const PRECACHE = [
  './', './index.html', './favicon.svg', './favicon.ico', './apple-touch-icon.png',
  './manifest.webmanifest',
  './assets/icon-192.png', './assets/icon-512.png',
  './assets/icon-192-maskable.png', './assets/icon-512-maskable.png'
];

self.addEventListener('install', (e) => {
  // 不自動 skipWaiting → 讓新 SW 進 waiting，由使用者在通知列決定何時套用
  e.waitUntil(caches.open(CACHE).then(c =>
    Promise.allSettled(PRECACHE.map(u => c.add(u).catch(() => {})))));
});

self.addEventListener('activate', (e) => {
  e.waitUntil((async () => {
    const keys = await caches.keys();
    await Promise.all(keys.filter(k => k.startsWith('wolf-') && k !== CACHE).map(k => caches.delete(k)));
    await self.clients.claim();
    (await self.clients.matchAll({ type: 'window' }))
      .forEach(c => c.postMessage({ type: 'SW_ACTIVATED', version: BUILD_VERSION }));
  })());
});

self.addEventListener('message', (e) => {
  if (e.data && e.data.type === 'SKIP_WAITING') self.skipWaiting();
});

self.addEventListener('fetch', (e) => {
  const req = e.request;
  if (req.method !== 'GET') return;
  let url; try { url = new URL(req.url); } catch { return; }
  if (url.origin !== self.location.origin) return;
  if (url.pathname.endsWith('version.json')) {           // 版本檔永遠拿最新
    e.respondWith(fetch(req).catch(() => caches.match(req))); return;
  }
  if (req.mode === 'navigate' || (req.headers.get('accept') || '').includes('text/html')) {
    e.respondWith(fetch(req).then(res => {                // HTML network-first
      const copy = res.clone(); caches.open(CACHE).then(c => c.put(req, copy)); return res;
    }).catch(() => caches.match(req).then(r => r || caches.match('./index.html')))); return;
  }
  e.respondWith(caches.match(req).then(cached => {         // 其他資源 cache-first + 背景更新
    const net = fetch(req).then(res => {
      if (res && res.status === 200 && res.type === 'basic') {
        const copy = res.clone(); caches.open(CACHE).then(c => c.put(req, copy));
      } return res;
    }).catch(() => cached);
    return cached || net;
  }));
});
