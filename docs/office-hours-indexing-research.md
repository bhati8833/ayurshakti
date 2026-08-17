# Indexing & Demand Research — ayurshakti.shop

## 1. Current Situation & Technical Overview

| Metric | Value |
|--------|-------|
| **Domain** | `ayurshakti.shop` / `www.ayurshakti.shop` |
| **Hosting** | Firebase Hosting (Edge CDN) |
| **Build Engine** | Next.js 14 (`output: 'export'`) |
| **Search Indexing API** | Active (`indexing.googleapis.com/v3`) |

---

## 2. Root Cause & Solution Strategy

### 2A. Static Export Technical Standards

1. **Clean Canonical URLs** — Handled via Next.js metadata API (`metadataBase` & canonical tag).
2. **Dynamic Sitemap** — Standardized at `https://www.ayurshakti.shop/sitemap.xml`.
3. **Structured Data** — JSON-LD (Article, FAQPage, HowTo) embedded directly into HTML output.

### 2B. Content Quality & E-E-A-T

Google requires high-quality, authoritative content:
- **E-E-A-T Signals** — Author byline (Suresh Bhati), medical disclaimer, PubMed citations.
- **Topical Authority** — Deep botanical and Ayurvedic condition clusters.
- **Fast Edge Delivery** — Firebase Hosting + Cloudflare CDN.

---

## 3. Demand Analysis & Action Plan

### P0 — Immediate Indexing Notification
- Submit new URLs via `Indexing API` (`scripts/bing-sitemap-submit.py` & GCP Indexing API).
- Submit `sitemap.xml` directly in Google Search Console & Bing Webmaster Tools.

### P1 — Content Quality & Multi-Platform Syndication
- Ensure all articles pass the 16/16 Quality Gate before static deployment.
- Syndicate content to Bluesky, Pinterest, and Medium.
