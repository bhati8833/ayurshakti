<!-- generated-by: gsd-doc-writer -->
# AyurShakti — ayurshakti.shop

Ayurvedic health and pet wellness blog hosted on Google Blogger, managed via Python automation scripts, with cloud infrastructure on Cloudflare DNS and a Google Sheets–based email marketing system.

<!-- VERIFY: live site availability, DNS records, and external service URLs (ayurshakti.shop, moltbook.com, etc.) cannot be verified from the repository alone -->

| Field | Value |
|-------|-------|
| **Platform** | Google Blogger |
| **Domain** | ayurshakti.shop |
| **Registrar** | Namecheap → Cloudflare DNS |
| **DNS** | Cloudflare (Free Plan) |
| **Owner** | Suresh Bhati ([contact@ayurshakti.shop](mailto:contact@ayurshakti.shop)) |
| **Blog ID** | `944859273218738540` |
| **GCP Project** | `ayurshakti-501603` |
| **GA4 Property** | `G-1KKZFZB7ML` (ID: `533609055`) |
| **Content** | Ayurveda, Herbal Remedies, Pet Health, Diet & Nutrition |
| **Languages** | English, Hindi (Hinglish) |
| **SEO/Webmaster** | Google Search Console, Bing Webmaster, Yandex Webmaster, Seznam Webmaster |
| **Social** | Bluesky, X/Twitter, Pinterest (API) · LinkedIn, Medium, Moltbook (browser agent) |

---

## Installation

The project is version-controlled with **git** and uses a Python virtual environment. It requires **Python ≥ 3.12** (Node.js ≥ 18 is only needed for Cloudflare Wrangler / llms-worker deployments).

```bash
# From an existing checkout:
cd /home/shiva/ayurshakti.shop

# Install Python dependencies (pinned via requirements.txt / pyproject.toml)
python3 -m pip install -r requirements.txt
```

Dependencies: `requests`, `markdown`, `cryptography`, `python-dotenv`.

> **Secrets:** Actual keys/tokens live in `secrets/` (gitignored). Never hardcode them. See `docs/06-credentials.md`.

---

## Quick Start

1. Install dependencies (see Installation).
2. Create the `secrets/` directory and add your credential files — see `docs/06-credentials.md`. Never commit secrets.
3. Submit the sitemap to Bing + IndexNow (pings Bing, Yandex, Seznam):
   ```bash
   python3 scripts/bing-sitemap-submit.py
   ```
4. Assign/update category labels on all posts so menu pages display correctly:
   ```bash
   python3 assign_categories.py
   ```
5. Schedule approved articles (auto-picks 2 from the queue every 12h, skips items without labels):
   ```bash
   python3 scripts/schedule-posts.py
   ```

---

## Document Index

All documentation lives in `docs/` as modular Markdown files. Start with `00-startup.md` on every new session.

| # | File | Description |
|---|------|-------------|
| 0 | `docs/00-startup.md` | **Session startup script** — AI agents must run this on every new session. Checks tracking data, presents an action menu. |
| 1 | `docs/01-overview.md` | **Project overview** — architecture diagram, key IDs, service account info. |
| 2 | `docs/02-cloudflare.md` | **Cloudflare** — zone info, two-token auth system, DNS records, Workers, cache purge, API commands. |
| 3 | `docs/03-gcp-apis.md` | **GCP APIs** — 6 enabled APIs (Blogger, Analytics, Search Console, PageSpeed, Indexing, API Keys), authentication, Python examples. |
| 4 | `docs/04-blogger-api.md` | **Blogger API v3** — 3 auth methods (API Key, OAuth, Service Account), endpoint cheatsheet, CRUD examples. |
| 5 | `docs/05-analytics-seo.md` | **Analytics & SEO** — GA4, Search Console, Bing/Yandex/Seznam Webmaster, Measurement Protocol, AMP, page speed. |
| 6 | `docs/06-credentials.md` | **Credentials reference** — every secret file, its source, and where it lives. |
| 7 | `docs/07-ai-agent-guide.md` | **AI agent guide** — MCP plugins, skills, doc reading order, agent rules. |
| 8 | `docs/08-topic-research-rule.md` | **Topic research rule** — 18-section guide for AI: keyword research, geography filters, seasonal calendar, competitor radar, content clusters, KPIs. |
| 9 | `docs/09-article-writing-rule.md` | **Article writing rule** — writing skills, human-touch checklist, SEO/AEO rules, brand voice, 16/16 checklist with category label gate. |
| — | `docs/office-hours-design.md` | **Office hours design** — growth + zero-investment monetization strategy. |
| 11 | `docs/11-article-approval-scheduler.md` | **Approval & scheduler** — 10/10 checklist, `approval-queue.json` format, EST time slots with ±15min jitter. |
| 12 | `docs/12-backlink-strategy.md` | **Backlink strategy** — Quora, Reddit, Medium, Pinterest automation; manual outreach; priority matrix. |
| 13 | `docs/13-image-generation-guide.md` | **Image generation guide** — manual workflow, prompt format, style guide, request queue. |
| 14 | `docs/14-content-tracking-system.md` | **Content tracking** — `article-registry.json`, `api-usage-log.json`, pre-flight checks. |
| 15 | `docs/15-email-marketing-system.md` | **Email marketing** — Google Sheets + Apps Script, welcome sequence, newsletter, lead magnet, UTM tracking. |
| — | `docs/34-resource-hosting.md` | **Resource hosting** — Cloudflare Pages + GitHub for images, PDFs, static assets. |
| — | `docs/bulk-topic-research.md` | **Bulk topic research** — SEO gap analysis and topic lists across human health and pet health categories. |
| — | `docs/ARCHITECTURE.md` | **Architecture** — system overview, component diagram, data flow, key abstractions. |
| — | `docs/CONFIGURATION.md` | **Configuration** — profile, secrets, Cloudflare, GCP, Blogger, GA4, Bing/Yandex/Seznam, email, scheduler. |

---

## Quick Commands

> **Security:** Actual keys reside in `secrets/` (gitignored). Never hardcode them. See `docs/06-credentials.md` for reference.

### Blogger API

```bash
# Get blog info (read-only, API key)
curl "https://www.googleapis.com/blogger/v3/blogs/944859273218738540?key=YOUR_BLOGGER_API_KEY"

# Get OAuth access token from refresh token
curl -X POST "https://oauth2.googleapis.com/token" \
  -d "client_id=YOUR_CLIENT_ID&client_secret=YOUR_CLIENT_SECRET&refresh_token=YOUR_REFRESH_TOKEN&grant_type=refresh_token"

# List all posts
curl -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  "https://www.googleapis.com/blogger/v3/blogs/944859273218738540/posts"

# Search posts
curl "https://www.googleapis.com/blogger/v3/blogs/944859273218738540/posts/search?q=ashwagandha&key=YOUR_API_KEY"
```

### Cloudflare

```bash
# List DNS records
curl -H "Authorization: Bearer YOUR_CLOUDFLARE_API_TOKEN" \
  "https://api.cloudflare.com/client/v4/zones/YOUR_ZONE_ID/dns_records"

# Purge cache
curl -X POST "https://api.cloudflare.com/client/v4/zones/YOUR_ZONE_ID/purge_cache" \
  -H "Authorization: Bearer YOUR_CLOUDFLARE_API_TOKEN" \
  -d '{"purge_everything": true}'

# Check llms.txt (AI crawler knowledge)
curl -s https://llms.ayurshakti.shop/llms.txt
```

### GA4 Analytics

```bash
curl -X POST "https://analyticsdata.googleapis.com/v1beta/properties/533609055:runReport" \
  -H "Authorization: Bearer {TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "dateRanges":[{"startDate":"7daysAgo","endDate":"today"}],
    "metrics":[{"name":"activeUsers"},{"name":"screenPageViews"}]
  }'
```

### Python Scripts

```bash
# Submit sitemap to Bing + IndexNow (Bing, Yandex, Seznam)
python3 scripts/bing-sitemap-submit.py

# Schedule approved articles (auto-picks 2 from queue, skips items without labels)
python3 scripts/schedule-posts.py

# Ping 15+ search engines on new publish
python3 scripts/notify-ping.py

# Post to Bluesky / X / Pinterest; queue LinkedIn, Medium, Moltbook for browser agent
python3 scripts/social-post.py

# Weekly brand mention monitoring
python3 scripts/monitor-mentions.py

# Fetch PubMed citations for articles
python3 scripts/pubmed-cite.py

# Check Seznam Webmaster indexing status
python3 scripts/seznam-api.py status

# Assign/update labels on all Blogger posts (v2.0 with herb sub-label auto-detection)
python3 assign_categories.py           # Fix all posts
python3 assign_categories.py --dry-run  # Preview only
python3 assign_categories.py --id POST_ID  # Fix single post
```

---

## Usage Examples

**1. Submit a single article URL to search engines via IndexNow (Bing, Yandex, Seznam):**

```bash
python3 scripts/bing-sitemap-submit.py --url https://www.ayurshakti.shop/2026/07/my-article.html
```

**2. Syndicate a published article to social platforms:**

```bash
python3 scripts/social-post.py --url https://www.ayurshakti.shop/2026/07/my-article.html --title "My Article Title"
```

Posts to **Bluesky**, **X/Twitter**, and **Pinterest** directly; queues **LinkedIn**, **Medium**, and **Moltbook** for the browser agent.

**3. Check Seznam Webmaster indexing status:**

```bash
python3 scripts/seznam-api.py status
```

**4. Publish an approved article at the optimal EST window:**

```bash
python3 scripts/schedule-posts.py
```

Picks 2 random approved articles from `scripts/approval-queue.json` (only 10/10 checklist passed AND non-empty labels array) and schedules them at EST morning (8–10am) or evening (6–8pm) slots with ±15 min jitter, then triggers IndexNow, ping, and social syndication.

> **Label validation:** The scheduler skips queue items with empty or missing labels. Run `python3 assign_categories.py` first to ensure articles have correct category labels — otherwise they won't publish and menu category pages stay empty. See checklist item #0 in `docs/09-article-writing-rule.md`.

---

## Folder Structure

```
ayurshakti.shop/
├── README.md                     ← This file — entry point
├── requirements.txt              ← Pinned Python dependencies
├── pyproject.toml               ← Project metadata, ruff/pytest config
├── robots.txt                    ← Site robots rules (served via Cloudflare Worker)
├── config/
│   └── profile.json              ← Central profile (site, author, contact, brand)
├── data/
│   └── tracking/
│       ├── article-registry.json ← Master list of published/draft articles
│       ├── api-usage-log.json    ← API rate limit tracker
│       ├── project-tasks.json     ← Todo tasks for AI / User
│       ├── indexing-log.json      ← Search engine indexing submissions
│       ├── pipeline-status.json   ← Content pipeline state
│       └── manual-image-requests.txt ← Pending image generation requests
├── docs/                         ← All documentation (modular .md)
│   ├── 00-startup.md
│   ├── 01-overview.md
│   ├── ...
│   ├── ARCHITECTURE.md
│   ├── CONFIGURATION.md
│   └── bulk-topic-research.md
├── scripts/
│   ├── lib/
│   │   ├── profile.py            ← Profile loader (imported by all Python scripts)
│   │   ├── auth.py               ← OAuth / token helpers
│   │   ├── tracking.py           ← Tracking-file read/write helpers
│   │   └── utils.py              ← Shared utilities
│   ├── config/
│   │   └── profile.json          ← Script-specific config mirror
│   ├── bing-sitemap-submit.py    ← IndexNow URL submission (Bing, Yandex, Seznam)
│   ├── schedule-posts.py         ← Auto-scheduler (picks 2 from queue every 12h)
│   ├── notify-ping.py            ← Pings 15+ search engines on publish
│   ├── social-post.py            ← Bluesky/X/Pinterest + queue LinkedIn/Medium/Moltbook
│   ├── monitor-mentions.py       ← Weekly brand mention check
│   ├── pubmed-cite.py            ← Fetch PubMed citations (free, no API key)
│   ├── seznam-api.py             ← Seznam Webmaster API client
│   ├── track_topics.py           ← Topic tracking / research helper
│   ├── check_live_images.py      ← Verify live image assets on CDN
│   ├── fetch_post_temp.py        ← Fetch a post draft temp file
│   ├── update_images_blogger.py  ← Rewrite post image URLs to CDN
│   ├── update_img_paths.py       ← Bulk image path migration
│   ├── fix_post.py               ← Post fix utilities
│   ├── llms-worker.js            ← Cloudflare Worker: llms.txt
│   ├── ads-worker.js             ← Cloudflare Worker: ad/placement logic
│   ├── fetch-profiles.js         ← Puppeteer: extract social profile usernames
│   ├── email-apps-script-code.js ← Google Apps Script for email marketing
│   ├── approval-queue.json       ← Articles awaiting scheduling
│   ├── schedule-config.json      ← Scheduler configuration
│   ├── agent-pending-posts.json  ← Posts queued for the browser agent
│   └── schedule-log.json         ← Scheduler run log
├── robots-worker/                ← Cloudflare Worker serving robots.txt
│   ├── worker.js
│   ├── inject.py
│   └── wrangler.toml
├── secrets/                      ← GITIGNORED — API keys, tokens, credentials
│   ├── blogger-oauth-tokens.json
│   ├── blogger-api-key.txt
│   ├── cloudflare-api-token.txt
│   ├── cloudflare-workers-token.txt
│   ├── cloudflare-global-key.txt
│   ├── cloudflare-zone-id.txt
│   ├── cloudflare-account-id.txt
│   ├── ayurshakti-501603-*.json
│   ├── ga4-mp-secret.txt
│   ├── bing-api-key.txt
│   ├── seznam-api-key.txt
│   ├── x-creds.json
│   ├── pinterest-creds.json
│   ├── bluesky-creds.json
│   └── cookies-*.txt             ← Session cookies (reddit, quora, medium, moltbook, etc.)
├── assets/                       ← Static assets
├── blog_images/                  ← Generated blog images + Cloudflare Pages config
├── theme-and-logo/
│   ├── ayurshakti-main.xml       ← Blogger theme XML
│   └── Logo.png                  ← Site logo files
├── drafts/                       ← Draft articles in progress
├── temp/                         ← Temp files
├── node_modules/                 ← NPM dependencies (Wrangler/Workers)
├── .gitignore
└── assign_categories.py          ← Label assigner v2.0 — auto-detects herb sub-labels from article titles for Blogger menu pages
```

---

## How To Use This Repo

1. **New session?** Read and execute `docs/00-startup.md` first — it checks tracking data and presents an action menu.
2. **Writing articles?** Follow `docs/09-article-writing-rule.md`. Register drafts in `data/tracking/article-registry.json`. Ensure articles pass the **16/16 checklist** including **checklist item #0** — correct category labels with herb sub-labels for menu pages. Without labels, category pages stay empty.
3. **Researching topics?** Use `docs/08-topic-research-rule.md` for keyword research, clustering, and gap analysis.
4. **Publishing?** Submit articles to the approval queue (`scripts/approval-queue.json`) with valid `labels` array — the scheduler rejects items with empty labels. The auto-scheduler (`docs/11-article-approval-scheduler.md`) handles timing. Run `assign_categories.py` to fix labels on all posts if needed.
5. **Email marketing?** See `docs/15-email-marketing-system.md` for the Apps Script workflow.
6. **Backlinks & outreach?** Execute strategies in `docs/12-backlink-strategy.md`.
7. **SEO/Webmaster?** Submit to Google Search Console, Bing, Yandex, and Seznam (see `docs/05-analytics-seo.md` and `docs/CONFIGURATION.md`).
8. **Category management?** Run `python3 assign_categories.py` to assign/update labels on all published posts. The script auto-detects categories from post titles and assigns herb sub-labels for individual herbs (e.g., Ashwagandha, Brahmi, Giloy, Triphala, Turmeric, Shatavari) so menu pages display correctly. Without proper labels, category page navigation stays empty.

See `docs/07-ai-agent-guide.md` for AI agent–specific instructions including available MCP tools and skills.
