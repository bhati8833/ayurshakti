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
| **DNS & Edge** | Cloudflare | DNS records, SSL/TLS (Full Strict), WAF rules, Bot Management |
| **Image Asset Hosting** | GitHub / Cloudflare | `blog_images/` & `/public/images/` served via `resources.ayurshakti.shop` |

---

## 3. Secrets Directory

**Directory:** `secrets/` (gitignored — contains actual private credential values)

| File | Service | Purpose |
| :--- | :--- | :--- |
| `secrets/ayurshakti-501603-a1a6ff0396df.json` | GCP IAM | Service account private key for Search Console & Indexing API |
| `secrets/cloudflare-api-token.txt` | Cloudflare | API Token for DNS and Cache Management |
| `secrets/cloudflare-workers-token.txt` | Cloudflare | API Token for Workers & Pages |
| `secrets/github-images-token.json` | GitHub | GitHub access token for image hosting repository |
| `secrets/x-creds.json` | X / Twitter | Developer API credentials |
| `secrets/pinterest-creds.json` | Pinterest | Pinterest API App token |

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
# Build static site output
npm run build

# Deploy static bundle to Firebase Hosting
firebase deploy --only hosting

# Force deployment
firebase deploy --only hosting --force
```
