# Architecture — ayurshakti.shop

**Updated:** August 2026 | **Source:** Next.js Static Architecture

---

## System Overview

AyurShakti.shop is a modern, high-performance static website built with **Next.js 14** (React, TypeScript, Tailwind CSS, Motion) exported as static HTML/CSS/JS (`output: 'export'`) and hosted on **Firebase Hosting** with **Cloudflare** for edge security & DNS, and **GitHub** for version control and image hosting.

```
┌──────────────────────────────────────────────────────────────────────────────────┐
│                           END USERS & AI CRAWLERS                                │
│                    Browser | GPTBot | ClaudeBot | Perplexity                     │
└────────────────────────────┬─────────────────────────────────────────────────────┘
                             │ HTTPS
┌────────────────────────────▼─────────────────────────────────────────────────────┐
│                         CLOUDFLARE CDN + EDGE                                     │
│       ┌──────────────────────┬───────────────────────┬──────────────────────┐     │
│       │  DNS + SSL + Cache   │  Workers (llms.txt)   │  Edge Protection     │     │
│       └──────────┬───────────┴───────────────────────┴──────────────────────┘     │
│                  │                                                               │
│       ┌──────────▼───────────┐                                                   │
│       │  FIREBASE HOSTING    │ (Edge Static CDN)                                 │
│       │  out/ directory      │                                                   │
│       │  Pre-rendered Pages  │                                                   │
│       └──────────────────────┘                                                   │
└──────────────────────────────────────────────────────────────────────────────────┘
                             ▲
                             │ Automatic Deploy
┌────────────────────────────┴─────────────────────────────────────────────────────┐
│                      GITHUB ACTIONS & SOURCE CONTROL                             │
│       bhati8833/ayurshakti.shop ──► `npm run build` ──► Firebase Deploy          │
└──────────────────────────────────────────────────────────────────────────────────┘
```

---

## Technical Stack & Layers

| Layer | Technology | Role & Details |
| :--- | :--- | :--- |
| **Framework** | **Next.js 14** | React 18, TypeScript, Tailwind CSS, Motion (`output: 'export'`) |
| **Static Host** | **Firebase Hosting** | Static Edge CDN serving `out/` export folder (`ayur-shakti`) |
| **DNS & Edge CDN** | **Cloudflare** | DNSSEC, WAF, DDoS protection, edge caching, Brotli compression |
| **Source & Images** | **GitHub** | Code repo (`ayurshakti.shop`) & GitHub asset storage (`resources.ayurshakti.shop`) |
| **SEO & Indexing** | **GSC & Indexing API** | Google Search Console, Bing IndexNow, GCP Web Search Indexing API |
| **Analytics** | **GA4** | Google Analytics 4 tracking (`G-1KKZFZB7ML`) |

---

## 📊 Free Tier Limits Summary

- **Firebase Hosting**: 10 GB storage, 360 MB/day bandwidth (Cloudflare absorbs >90% of requests).
- **Cloudflare**: Unlimited unmetered bandwidth, 100k Workers/day, 5 custom WAF rules.
- **GitHub**: Unlimited public repo storage, 2,000 GitHub Actions build minutes/month.

---

## 🛠️ Automated CI/CD & Deploy Workflow

```bash
# 1. Local Development
npm run dev

# 2. Static Build Verification
npm run build

# 3. Deploy to Firebase Hosting
firebase deploy --only hosting
```
