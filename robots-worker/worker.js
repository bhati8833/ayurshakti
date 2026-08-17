// ayurshakti-robots worker
// Scoped ONLY to ayurshakti.shop/robots.txt and www.ayurshakti.shop/robots.txt
// All other traffic passes untouched to Blogger (no route match).

const ROBOTS_TXT = `# robots.txt for ayurshakti.shop
# Optimized for Yandex, Seznam, Google, Bing, and AI crawlers
# Last updated: 2026-07-11

# ============================================================
# DEFAULT RULES - All crawlers
# ============================================================
User-agent: *
Allow: /

# Block search/filter/utility pages (no SEO value)
Disallow: /search
Disallow: /search/
Disallow: /search?q=*
Disallow: *?q=*
Disallow: /feeds/
Disallow: /feeds/posts/default
Disallow: /feeds/posts/default?*
Disallow: /blogger/
Disallow: /blogger/*
Disallow: /*?format=*
Disallow: /*?m=*
Disallow: /*?amp=*
Disallow: /comment*
Disallow: /*/comment*
Disallow: /*#comment
Disallow: /view-source:*
Disallow: /*.atom
Disallow: /*.xml$
Disallow: /*?redirect=*
Disallow: /*.json$

# ============================================================
# YANDEX-SPECIFIC RULES
# ============================================================
User-agent: Yandex
Allow: /
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
Disallow: /*.xml$

# Yandex-specific: Clean-param for UTM/tracking parameters
# Ignores these URL parameters when indexing (prevents duplicates)
Clean-param: utm_source&utm_medium&utm_campaign&utm_content&utm_term / 
Clean-param: ref / 
Clean-param: fbclid / 
Clean-param: gclid / 
Clean-param: mc_cid / 
Clean-param: mc_eid / 
Clean-param: _ga / 
Clean-param: _gl /

# Crawl-delay for Yandex (seconds between requests)
# Default is conservative; adjust if server load is an issue
Crawl-delay: 2

# ============================================================
# SEZNAM-SPECIFIC RULES
# ============================================================
User-agent: SeznamBot
Allow: /
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
Disallow: /*.xml$

# Request-rate for Seznam (requests per time unit)
# Format: Request-rate: requests/time (s=seconds, m=minutes, h=hours, d=days)
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
Disallow: /search
Disallow: /feeds/
Disallow: /blogger/
Disallow: /*?q=*
Disallow: /*?m=*
Disallow: /*?amp=*
Disallow: /comment*
Disallow: /*/comment*

# ============================================================
# SITEMAPS - Use XML sitemap (not Atom feed)
# ============================================================
Sitemap: https://www.ayurshakti.shop/sitemap.xml

# llms.txt for AI knowledge retrieval
Sitemap: https://www.ayurshakti.shop/llms.txt

# Image sitemap (if available)
# Sitemap: https://www.ayurshakti.shop/sitemap-images.xml

# ============================================================
# HOST DIRECTIVE (Yandex) - Preferred domain
# ============================================================
Host: www.ayurshakti.shop`;

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
    // Fallback (should never trigger since route is scoped to /robots.txt)
    return fetch(request);
  },
};
