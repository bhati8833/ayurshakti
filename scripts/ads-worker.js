// Cloudflare Worker: ads.txt for ayurshakti.shop
// Serves ads.txt at root path — Blogger cannot serve root files
// Route: ayurshakti.shop/ads.txt -> this Worker
export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.pathname === "/ads.txt") {
      return new Response(adsTxtContent, {
        headers: {
          "content-type": "text/plain; charset=utf-8",
          "cache-control": "public, max-age=86400"
        }
      });
    }
    return new Response("Not Found", { status: 404 });
  }
};

// Placeholder: replace pub-XXXXXXXXXXXXXX with actual AdSense publisher ID after approval (Phase 6)
const adsTxtContent = `google.com, pub-XXXXXXXXXXXXXXXX, DIRECT, f08c47fec0942fa0`;
