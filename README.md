# AyurShakti — ayurshakti.shop

High-performance, static Ayurvedic health and pet wellness platform built with Next.js 14, hosted on Firebase Hosting (Edge CDN), with Cloudflare DNS and an automated SEO & social syndication engine.

| Field | Value |
|-------|-------|
| **Framework** | Next.js 14 (TypeScript, Tailwind CSS, Motion) |
| **Hosting** | Firebase Hosting (`output: 'export'`) |
| **Domain** | `ayurshakti.shop` / `www.ayurshakti.shop` |
| **Registrar / DNS** | Namecheap → Cloudflare DNS |
| **Owner / Author** | Suresh Bhati ([contact@ayurshakti.shop](mailto:contact@ayurshakti.shop)) |
| **GCP Project** | `ayurshakti-501603` |
| **GA4 Property** | `G-1KKZFZB7ML` (ID: `533609055`) |
| **Content** | Ayurveda, Botanical Profiles, Pet Health, Glossary, Canonical Texts |
| **Languages** | English, Hindi (Hinglish) |
| **SEO / Indexing** | GCP Indexing API, Search Console, Bing Webmaster / IndexNow |
| **Social** | Bluesky, X/Twitter, Pinterest (API) · LinkedIn, Medium, Moltbook (browser agent) |

---

## Technical Stack & Architecture

```
GitHub Repo (Source) ──► npm run build (Next.js export) ──► Firebase Hosting (Edge CDN)
                                                                   │
                                                                   ▼
                                                         Cloudflare DNS / Proxy
```

- **Image Management:** Repository-based asset storage served via `resources.ayurshakti.shop` and local `/public/` static paths.
- **Dynamic Features:** Interactive Dosha quiz, interactive glossary, PubMed citation integration, and client-side calculators.

---

## Key Commands

```bash
# Build Next.js static export
npm run build

# Push changes to GitHub to trigger automated CI/CD deployment
git add .
git commit -m "Site update"
git push origin master

# Submit sitemap to Bing + IndexNow
python3 scripts/bing-sitemap-submit.py

# Ping search engines post-publish
python3 scripts/notify-ping.py

# Social syndication
python3 scripts/social-post.py --url URL --title "Title"

# Fetch PubMed citations
python3 scripts/pubmed-cite.py 'ashwagandha cortisol study' 3
```

---

## Document Index (`docs/`)

All technical documentation is sequentially numbered in `docs/`:

| File | Purpose |
|------|---------|
| `docs/00-startup.md` | **Session startup script** — mandatory agent entry point. |
| `docs/01-overview.md` | **Project overview** — modern stack details and identity. |
| `docs/02-architecture.md` | **System architecture** — Next.js static build & deployment flow. |
| `docs/03-configuration.md` | **Configuration** — complete infrastructure settings. |
| `docs/04-credentials.md` | **Credentials reference** — secret locations and environment mapping. |
| `docs/05-firebase-hosting.md` | **Firebase hosting** — static SSG CDN & GitHub CI/CD pipeline. |
| `docs/06-cloudflare.md` | **Cloudflare** — DNS, Workers, edge caching, WAF, SSL settings. |
| `docs/07-resource-hosting.md` | **Resource hosting** — GitHub image hosting & Cloudflare resource proxy. |
| `docs/08-gcp-apis.md` | **GCP APIs** — Indexing, Analytics, Search Console, PageSpeed. |
| `docs/09-analytics-seo.md` | **Analytics & SEO** — GA4, GSC, Indexing API, Bing IndexNow. |
| `docs/10-indexing-research.md` | **Indexing research** — SEO technical requirements & Google indexing strategy. |
| `docs/11-ai-agent-guide.md` | **AI agent guide** — task routing, skills, Next.js build workflow. |
| `docs/12-topic-research-rule.md` | **Topic research** — keyword strategy and botanical profiles. |
| `docs/13-article-writing-rule.md` | **Article writing** — human-touch rules, SEO quality checklist. |
| `docs/14-article-approval-scheduler.md` | **Approval & scheduler** — static build & Indexing API pipeline. |
| `docs/15-content-tracking-system.md` | **Content tracking** — tracking static publication status. |
| `docs/16-backlink-strategy.md` | **Backlink strategy** — automation & outreach strategy. |
| `docs/17-image-generation-guide.md` | **Image generation** — AI image prompts and optimization. |
| `docs/18-email-marketing-system.md` | **Email marketing** — Next.js form embeds + Google Apps Script. |
| `docs/19-moltbook-playbook.md` | **Moltbook playbook** — AI browser agent social interactions. |
| `docs/20-traffic-growth-strategy.md` | **Traffic growth** — indexing foundation and performance tuning. |
