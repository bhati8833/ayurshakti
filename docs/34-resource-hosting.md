# 34-Resource-Hosting — AyurShakti.shop

## Architecture Overview

```
blog_images/  (local project directory)
    ↓ git push
GitHub Repo: bhati8833/ayurshakti-images
    ↓ auto-deploy
Cloudflare Pages: resources.ayurshakti.shop
```

## GitHub Repo Structure

```
/
├── img/                → All images (.jpg, .png)
│   ├── favicon/        → Browser favicons (favicon.ico, icon-192.png, etc.)
│   ├── logo.png        → Site logo
│   ├── *.jpg           → Blog header images
│   └── *.png           → AI-generated illustrations
├── key/                → Verification keys
│   └── indexnow-key.txt → Bing IndexNow API key
├── pdf/                → Downloadable PDFs
│   └── lead-magnet.pdf → Email lead magnet
└── wrangler.toml       → Cloudflare Workers config
```

## CDN URL Reference

| Category | URL Pattern |
|---|---|
| Blog Images | `https://resources.ayurshakti.shop/img/{filename}` |
| Logo | `https://resources.ayurshakti.shop/img/logo.png` |
| Favicon | `https://resources.ayurshakti.shop/img/favicon/{filename}` |
| PDFs | `https://resources.ayurshakti.shop/pdf/{filename}` |
| IndexNow Key | `https://resources.ayurshakti.shop/key/indexnow-key.txt` |

## Deploy Methods

### Method 1: Git Push (Auto-deploy)
```bash
cd blog_images
git add img/your-new-image.jpg
git commit -m "Add image for article X"
git push origin main
# Cloudflare Pages auto-rebuilds (~30-60s)
```

### Method 2: Wrangler CLI (Instant)
```bash
cd blog_images
CLOUDFLARE_API_TOKEN=$(cat ../secrets/cloudflare-api-token.txt) npx wrangler deploy
```

## Auth

| Credential | File | Purpose |
|---|---|---|
| GitHub Token | `secrets/github-images-token.json` | `git push` manual image uploads |
| CF API Token | `secrets/cloudflare-api-token.txt` | Wrangler deploy, Page Rules |
| CF Global Key | `secrets/cloudflare-global-key.txt` | DNS, Cache Purge (fallback) |

## Important Notes

- `www.ayurshakti.shop` is **DNS-only** (not proxied) — Cloudflare cannot serve Page Rules or Workers on the www domain. This is required for Blogger CNAME (`ghs.google.com`).
- `resources.ayurshakti.shop` is **proxied** (AAAA `100::`) — Cloudflare Pages handles all traffic.
- Images are only served under `/img/` prefix — old root-level paths (e.g. `/logo.png`) return 404.
- All existing Blogger posts have been updated in July 2026 to use the new `/img/` paths.