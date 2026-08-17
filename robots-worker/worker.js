// ayurshakti-robots worker
// Scoped ONLY to ayurshakti.shop/robots.txt and www.ayurshakti.shop/robots.txt

const ROBOTS_TXT = `# robots.txt for ayurshakti.shop
# Optimized for Yandex, Seznam, Google, Bing, and AI crawlers
# Last updated: 2026-08-17

# ============================================================
# DEFAULT RULES - All crawlers
# ============================================================
User-agent: *
Allow: /
Allow: /_next/
Allow: /sitemap.xml
Allow: /llms.txt

# Block search/filter/utility pages (no SEO value)
Disallow: /search
Disallow: /search/
Disallow: /search?*
Disallow: /*?q=*
Disallow: /feeds/
Disallow: /blogger/
Disallow: /*?format=*
Disallow: /*?m=*
Disallow: /*?amp=*
Disallow: /comment*
Disallow: /*/comment*
Disallow: /*#comment
Disallow: /view-source:*
Disallow: /*.atom
Disallow: /*?redirect=*

# ============================================================
# YANDEX-SPECIFIC RULES
# ============================================================
User-agent: Yandex
Allow: /
Allow: /sitemap.xml
Disallow: /search
Disallow: /search/
Disallow: /feeds/
Disallow: /blogger/
Disallow: /*?q=*
Disallow: /*?m=*
Disallow: /*?amp=*
Disallow: /comment*
Disallow: /*/comment*
Disallow: /*#comment
Disallow: /view-source:*
Disallow: /*.atom

# Yandex-specific: Clean-param for UTM/tracking parameters
Clean-param: utm_source&utm_medium&utm_campaign&utm_content&utm_term / 
Clean-param: ref / 
Clean-param: fbclid / 
Clean-param: gclid / 
Clean-param: mc_cid / 
Clean-param: mc_eid / 
Clean-param: _ga / 
Clean-param: _gl /

Crawl-delay: 2

# ============================================================
# SEZNAM-SPECIFIC RULES
# ============================================================
User-agent: SeznamBot
Allow: /
Allow: /sitemap.xml
Disallow: /search
Disallow: /search/
Disallow: /feeds/
Disallow: /blogger/
Disallow: /*?q=*
Disallow: /*?m=*
Disallow: /*?amp=*
Disallow: /comment*
Disallow: /*/comment*
Disallow: /*#comment
Disallow: /view-source:*
Disallow: /*.atom

Request-rate: 100/1m

# ============================================================
# AI CRAWLERS - Allow for content discovery & training
# ============================================================
User-agent: GPTBot
Allow: /

User-agent: ChatGPT-User
Allow: /

User-agent: Claude-Web
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: CCBot
Allow: /

User-agent: Google-Extended
Allow: /

User-agent: AppleBot
Allow: /

User-agent: anthropic-ai
Allow: /

User-agent: omgili
Allow: /

User-agent: PetalBot
Allow: /

User-agent: YouBot
Allow: /

User-agent: Meta-ExternalAgent
Allow: /

User-agent: BingPreview
Allow: /

# ============================================================
# MAJOR SEARCH ENGINES
# ============================================================
User-agent: Googlebot
Allow: /
Allow: /sitemap.xml
Disallow: /search
Disallow: /feeds/
Disallow: /blogger/
Disallow: /*?q=*
Disallow: /*?m=*
Disallow: /*?amp=*
Disallow: /comment*
Disallow: /*/comment*

User-agent: Bingbot
Allow: /
Allow: /sitemap.xml
Disallow: /search
Disallow: /feeds/
Disallow: /blogger/
Disallow: /*?q=*
Disallow: /*?m=*
Disallow: /*?amp=*
Disallow: /comment*
Disallow: /*/comment*

User-agent: DuckDuckBot
Allow: /
Allow: /sitemap.xml
Disallow: /search
Disallow: /feeds/
Disallow: /blogger/
Disallow: /*?q=*
Disallow: /*?m=*
Disallow: /*?amp=*
Disallow: /comment*
Disallow: /*/comment*

User-agent: Baiduspider
Allow: /
Allow: /sitemap.xml
Disallow: /search
Disallow: /feeds/
Disallow: /blogger/
Disallow: /*?q=*
Disallow: /*?m=*
Disallow: /*?amp=*
Disallow: /comment*
Disallow: /*/comment*

# ============================================================
# SITEMAPS
# ============================================================
Sitemap: https://ayurshakti.shop/sitemap.xml

# llms.txt for AI knowledge retrieval
Sitemap: https://ayurshakti.shop/llms.txt

# ============================================================
# HOST DIRECTIVE (Yandex) - Preferred domain
# ============================================================
Host: ayurshakti.shop`;

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    if (url.pathname === "/robots.txt") {
      return new Response(ROBOTS_TXT, {
        status: 200,
        headers: {
          "Content-Type": "text/plain; charset=utf-8",
          "Cache-Control": "public, max-age=86400",
        },
      });
    }
    return fetch(request);
  },
};
