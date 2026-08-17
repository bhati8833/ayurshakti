# Overview — ayurshakti.shop

## Lightweight Architecture (GitHub + Cloudflare + Firebase)

```
Developer / AI Agent ──► GitHub (Git Push) ──► GitHub Actions ──► Firebase Hosting ──► Cloudflare DNS ──► Readers
                                                    (Static CDN)       (Security/SSL)
```

| Layer | Provider | Role |
|-------|----------|------|
| **Version Control** | GitHub | Code & Markdown repository (`bhati8833/ayurshakti.shop`) |
| **CI/CD Build** | GitHub Actions | Automatic `npm run build` and deployment trigger |
| **Hosting & Storage** | Firebase Hosting | Ultra-fast SSG static hosting (`ayur-shakti`) for account `vle.bhati@gmail.com` |
| **DNS & SSL Edge** | Cloudflare | DNS management, DDoS protection, Brotli compression, edge SSL |
| **Domain** | Namecheap | Domain registration (`ayurshakti.shop`) |
| **Framework** | Next.js 14 | React, TypeScript, Tailwind CSS, Motion (`output: 'export'`) |
| **Analytics** | Google Analytics GA4 | Traffic tracking (`G-1KKZFZB7ML`) |
| **SEO** | GSC & Bing | Search Console & Bing IndexNow |
| **AI Crawlers** | Cloudflare Worker | `llms.txt` serving (`llms.ayurshakti.shop`) |

## Key Identifiers

| Identifier | Value |
|------|-------|
| Firebase Account | `vle.bhati@gmail.com` |
| Firebase Project ID | `ayur-shakti` |
| GA4 Property ID | `533609055` |
| Cloudflare Zone ID | `f63c29bc9532dc008cd45e2db084ee4e` |

## Local Development Hardware & Processing Batching

| Spec | Value | Operational Rule |
|------|-------|------------------|
| **CPU** | Intel Core i5-1035G1 (4C/8T @ 1.00GHz - 3.60GHz) | Add minor sleep delays in loops to prevent throttling |
| **RAM** | 8 GB (7.3 GiB usable, ~4.5 GiB available) | Keep parallel script execution within memory limits |
| **Disk** | 109 GB SSD (84% used, ~18 GB free) | Keep `.next/` and build outputs clean |
| **Batching** | 25–50 items / micro-batch | Process content/markdown files in chunks of 25–50 |

