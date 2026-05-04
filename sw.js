// Network-first HTML loader.
//
// GitHub Pages serves every response with Cache-Control: max-age=600 and
// won't let us override that header. For static-URL HTML pages (the index
// and the locandina) that means returning visitors keep seeing a cached
// copy for up to 10 minutes after a deploy. This service worker bypasses
// the HTTP cache for HTML navigations by re-fetching with cache: "no-store".
//
// Non-HTML requests (CSS/JS/images/SVG) pass through untouched — the
// browser cache still applies, and cache-bust.py's ?v=<hash> stamps make
// each deploy's asset URLs unique so freshness is preserved that way.

self.addEventListener("install", (event) => {
  self.skipWaiting();
});

self.addEventListener("activate", (event) => {
  event.waitUntil(self.clients.claim());
});

self.addEventListener("fetch", (event) => {
  const req = event.request;
  if (req.method !== "GET") return;
  if (new URL(req.url).origin !== self.location.origin) return;

  const accept = req.headers.get("accept") || "";
  const isHtml = req.mode === "navigate" || accept.includes("text/html");
  if (!isHtml) return;

  event.respondWith(fetch(req, { cache: "no-store" }));
});
