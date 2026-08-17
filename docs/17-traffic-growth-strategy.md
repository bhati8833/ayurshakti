# Traffic Growth Strategy — ayurshakti.shop

## 1. What the two reports actually are

### Google Analytics 4 (GA4) — *what users do on the site*
GA4 measures **on-site behavior**. The API (`analyticsdata.googleapis.com/v1beta`) returns metrics per date.

### Google Search Console (GSC) — *how Google sees the site*
GSC measures **search visibility**. The API (`webmasters/v3/.../searchAnalytics`) returns per-query performance.

---

## 2. The Bottleneck (SEO & Indexing Foundation)

1. Confirm `sc-domain:ayurshakti.shop` ownership in GSC (DNS verified via Cloudflare).
2. Submit `https://www.ayurshakti.shop/sitemap.xml` in GSC → Sitemaps.
3. Wire the **Indexing API** into publish flow so every new post pings Google (`docs/05-analytics-seo.md`).
4. Keep `scripts/bing-sitemap-submit.py` running post-publish (covers Bing + Yandex + Seznam via IndexNow).
5. Verify Next.js head meta tags and JSON-LD structured data on all static exports.

---

## 3. Technical SEO & Performance

- Target Mobile PageSpeed Performance ≥ 90 on Next.js pages.
- Optimize images in `/public/images/` with WebP and clean metadata.
- Monitor static output performance on Firebase Hosting CDN edge nodes.

---

## 4. Prioritized Action Plan

| Priority | Task | Owner script / doc | Target |
|----------|------|--------------------|--------|
| P0 | Confirm GSC ownership + submit sitemap | GSC UI | impressions > 0 |
| P0 | Indexing API on every publish | `05-analytics-seo.md` | index in hours |
| P1 | Audit GA4 bounce (filter bots/owner) | GA4 UI | realistic bounce |
| P1 | Long-tail bilingual posts (clusters) | topic + write pipeline | 30 indexed |
| P2 | Mobile PageSpeed ≥ 90 on top pages | PageSpeed API | perf ≥ 90 |
