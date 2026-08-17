# 35-Firebase-Hosting — Free Tier Limits & Site Deployment Guide

## Overview

AyurShakti.shop utilizes a modern, zero-cost, high-performance static architecture combining **Firebase Hosting (Spark Plan)**, **Cloudflare (Free Plan)**, and **GitHub (Free Plan)**.

```
┌──────────────────┐
│  GitHub Repo     │ ──► GitHub Actions CI/CD (`npm run build`)
└──────────────────┘             │
                                 ▼ auto-deploy
                       ┌───────────────────┐
                       │ Firebase Hosting  │ (Static SSG Edge CDN)
                       └───────────────────┘
                                 ▲
                                 │ CNAME Proxy / Edge SSL & Cache
                       ┌───────────────────┐
                       │   Cloudflare DNS  │ (DDoS + WAF + Edge Caching)
                       └───────────────────┘
                                 │
                                 ▼
                       [ Site Visitors / Readers ]
```

---

## 📊 Platform Free Tier Limits & Specifications

### 1. Firebase Hosting (Spark Plan - 100% Free)
| Feature / Resource | Free Tier Limit | Details & Strategy for AyurShakti |
| :--- | :--- | :--- |
| **Storage Capacity** | **10 GB** | Total static files size (`out/` export directory). Fits thousands of pre-rendered pages easily. |
| **Data Transfer / Bandwidth** | **360 MB / day** (~10.8 GB / mo) | Direct origin bandwidth limit. *Cloudflare Edge Caching absorbs >90% of requests*, preventing Firebase limit breaches. |
| **Custom Domains & SSL** | **Unlimited** | Free automatic SSL certificate via Let's Encrypt with auto-renewal. Custom domain mapping (`ayurshakti.shop`). |
| **Sites per Project** | **Up to 36 sites** | Allows running staging environments, preview builds, or subdomains on the same `ayur-shakti` project. |
| **Deployments History** | **Recent 10 rollbacks** | Allows instant rollbacks to previous builds via Firebase Console. |

### 2. Cloudflare (Free Plan)
| Feature / Resource | Free Tier Limit | Details & Strategy for AyurShakti |
| :--- | :--- | :--- |
| **Bandwidth & Requests** | **Unlimited / Unmetered** | Cloudflare caches static assets globally across 270+ edge locations at no cost. |
| **DNSSEC & DNS Queries** | **Unlimited** | Ultra-fast global DNS resolution with built-in DNSSEC security. |
| **WAF Custom Rules** | **5 Active Rules** | Block malicious bots, scrapers, or country-specific spam threats. |
| **Rate Limiting** | **1 Free Rule** | Prevent abuse or brute-force requests on public endpoints. |
| **Cloudflare Workers** | **100,000 requests / day** | Serves edge-side logic like dynamic `llms.txt` generation (`llms.ayurshakti.shop`). |

### 3. GitHub (Free Tier)
| Feature / Resource | Free Tier Limit | Details & Strategy for AyurShakti |
| :--- | :--- | :--- |
| **Repository Storage** | **1 GB - 5 GB (recommended)** | Codebase & static Markdown content repository (`bhati8833/ayurshakti.shop`). |
| **GitHub Actions CI/CD** | **2,000 minutes / month** | Automatically builds Next.js (`npm run build`) and deploys to Firebase Hosting on `git push main`. |
| **GitHub Image Hosting** | **Unlimited via Repo / Raw CDN** | Blog images hosted in public repository or dedicated media repository, served via raw CDN (`raw.githubusercontent.com`) or Cloudflare resource proxy. |

---

## 🌐 Supported Website Types & Deployment Compatibility

### ✅ Fully Supported (100% Free on Firebase + Cloudflare)
1. **Static Site Generators (SSG)**:
   - **Next.js**: Pre-rendered HTML (`output: 'export'`) — **Used by AyurShakti.shop**
   - **Astro / Hugo / Gatsby / Nuxt (SSG)**
   - **Vite (React, Vue, Svelte, Vanilla)**
2. **Single Page Applications (SPAs)**:
   - React, Vue, Angular, Svelte SPAs (client-side routing handled by rewrites in `firebase.json`).
3. **Content Platforms & Websites**:
   - Blogs, canonical knowledge centers, digital glossaries.
   - Documentation sites, portfolios, brand landing pages, product marketing sites.
   - E-commerce frontend storefronts connecting to headless APIs (Shopify, Stripe, Snipcart).

### ❌ Not Supported (Requires Server / Paid Cloud Upgrades)
- **Dynamic Node.js SSR Servers**: Next.js Server Components requiring runtime Node server (e.g. `next start` without static export).
- **Server Database Runtime**: Running MySQL / Postgres database directly on the web host (requires external managed DB like Supabase, PlanetScale, or Firebase Firestore).
- **Dynamic File Uploads to Host Filesystem**: Static hosting cannot save user file uploads to disk (requires Firebase Storage bucket or AWS S3).

---

## ⚙️ Project Configuration Files

### `firebase.json`
```json
{
  "hosting": {
    "public": "out",
    "ignore": [
      "firebase.json",
      "**/.*",
      "**/node_modules/**"
    ],
    "cleanUrls": true,
    "trailingSlash": false
  }
}
```

### `.firebaserc`
```json
{
  "projects": {
    "default": "ayur-shakti"
  }
}
```

---

## 🚀 Key Deployment Commands

```bash
# 1. Clean build output and generate static files
npm run build

# 2. Manual Firebase Hosting deployment
firebase deploy --only hosting

# 3. Forced deployment (bypasses stale session locks)
firebase deploy --only hosting --force
```
