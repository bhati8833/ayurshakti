# Configuration — ayurshakti.shop

Central configuration reference for the AyurShakti project. All settings, platform configurations, and environment credentials are documented here.

---

## 1. Profile Configuration

**File:** `config/profile.json`

Contains site metadata, author identity, contact details, brand voice, and script paths.

```json
{
  "site": {
    "name": "AyurShakti",
    "domain": "ayurshakti.shop",
    "url": "https://www.ayurshakti.shop",
    "sitemap": "https://www.ayurshakti.shop/sitemap.xml",
    "llms": "https://llms.ayurshakti.shop/llms.txt",
    "title": "AyurShakti — Ayurvedic Health & Pet Wellness",
    "description": "Evidence-based Ayurveda for human & pet health.",
    "language": "en",
    "timezone": "America/New_York"
  },
  "author": {
    "name": "Suresh Bhati",
    "title": "Ayurvedic Researcher & Health Writer",
    "contact_email": "contact@ayurshakti.shop"
  }
}
```

---

## 2. Platform Infrastructure Configuration

| Component | Platform | Configuration File / Dashboard |
| :--- | :--- | :--- |
| **Framework** | Next.js 14 SSG | `next.config.mjs` (`output: 'export'`), `tailwind.config.ts`, `tsconfig.json` |
| **Hosting** | Firebase Hosting | `firebase.json` (`public: "out"`, `cleanUrls: true`), `.firebaserc` (`ayur-shakti`) |
| **CI/CD Build** | GitHub Actions | `.github/workflows/firebase-deploy.yml` (`FIREBASE_TOKEN` secret) |
| **DNS & Edge** | Cloudflare | DNS records, SSL/TLS (Full Strict), WAF rules, Bot Management |
| **Image Asset Hosting** | GitHub / Cloudflare | `blog_images/` & `/public/images/` served via `resources.ayurshakti.shop` |

---

## 3. Secrets & Tokens Reference

| Token / Secret | Platform / Scope | Purpose | Stored In |
| :--- | :--- | :--- | :--- |
| `FIREBASE_TOKEN` | Firebase Hosting | Deployment authentication for project `ayur-shakti` (`vle.bhati@gmail.com`) | GitHub Secrets (`FIREBASE_TOKEN`) & CLI config |
| `ayurshakti-501603-a1a6ff0396df.json` | GCP IAM | Service account private key for GCP Search Indexing API & Search Console | `secrets/ayurshakti-501603-a1a6ff0396df.json` |
| `cloudflare-api-token.txt` | Cloudflare | API Token for DNS and Cache Management | `secrets/cloudflare-api-token.txt` |
| `cloudflare-workers-token.txt` | Cloudflare | API Token for Workers & Pages | `secrets/cloudflare-workers-token.txt` |
| `github-images-token.json` | GitHub | GitHub access token for image hosting repository (`resources.ayurshakti.shop`) | `secrets/github-images-token.json` |
| `x-creds.json` | X / Twitter | Developer API credentials | `secrets/x-creds.json` |
| `pinterest-creds.json` | Pinterest | Pinterest API App token | `secrets/pinterest-creds.json` |

---

## 4. Cloudflare Edge Settings

| DNS Record | Type | Target / Content | Proxy Status |
| :--- | :--- | :--- | :--- |
| `@` | CNAME / A | `ayur-shakti.web.app` (Firebase Hosting) | Proxied (Orange Cloud) |
| `www` | CNAME | `ayurshakti.shop` | Proxied (Orange Cloud) |
| `resources` | CNAME | GitHub raw CDN / Cloudflare Pages | Proxied (Orange Cloud) |
| `llms` | CNAME | Cloudflare Worker (`llms-worker.js`) | Proxied (Orange Cloud) |

---

## 5. Deployment Commands

```bash
# Build static site output locally
npm run build

# Push changes to GitHub to trigger automated CI/CD deployment to Firebase Hosting
git add .
git commit -m "Deployment update"
git push origin master
```
