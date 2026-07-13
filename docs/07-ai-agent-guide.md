# AI Agent Guide — ayurshakti.shop

## First File to Read

**START HERE:** `README.md` (project root) — has the document index.
Then read this file for agent-specific instructions.

## Doc Reading Sequence (Priority)

| Order | File | When to Read |
|-------|------|-------------|
| 1 | `README.md` | Always — entry point |
| 2 | `docs/07-ai-agent-guide.md` | Always — agent instructions |
| 3 | `docs/01-overview.md` | First time / new task |
| 4 | `docs/04-blogger-api.md` | Content ops tasks |
| 5 | `docs/02-cloudflare.md` | DNS / infra tasks |
| 6 | `docs/05-analytics-seo.md` | SEO / reporting tasks |
| 7 | `docs/06-credentials.md` | Reference — lookup only |
| 8 | `docs/03-gcp-apis.md` | GCP / API management tasks |

## Available MCP Tools (OpenCode)

These tools are available to AI agents in this environment.

### Meta Ads & Marketing
- `meta-marketing_create_campaign` — Create ad campaigns (OUTCOME_AWARENESS, OUTCOME_TRAFFIC, etc.)
- `meta-marketing_create_adset` — Create ad sets with targeting, budget
- `meta-marketing_create_adcreative` — Create ad creatives (image/video)
- `meta-marketing_create_ad` — Create ads linked to creatives
- `meta-marketing_list_campaigns/adsets/ads` — List all ad objects
- `meta-marketing_get_account_insights` — Performance reports

### Web Browser Automation
- `browser_puppeteer_navigate/fill/click/screenshot/evaluate` — Full browser control

### Email (contact@ayurshakti.shop)
- `email_send_email` — Send from contact@ayurshakti.shop (via Gmail)
- `email_list_emails/read_email/search_emails` — Read/search inbox
- Forwarded from Cloudflare Email Routing → Gmail (IMAP)
- **Setup needed:** Gmail App Password (see below)

### Web Search & Fetch
- `websearch` — Real-time web search with crawling
- `webfetch` — Fetch URL content

### Stock Trading (Zerodha Kite)
- `zerodha-kite_*` — 20+ tools: place/modify/cancel orders, GTT, holdings, LTP, search

## Backlink Strategy (SEO Off-Page)

See `docs/12-backlink-strategy.md` for full architecture. Summary:

| Phase | Type | Tools | When |
|-------|------|-------|------|
| **Phase 1** | AI Agent (Browser) | `agent-browser` skill — Quora, Reddit, Medium, Pinterest | Week 1 onwards |
| **Phase 2** | API Auto (Scripts) | `notify-ping.py`, `bing-sitemap-submit.py`, Shoutrrr Docker | Week 1-2 |
| **Phase 3** | Manual High-Value | HARO, Guest Post, Broken Link, Skyscraper | Week 2+ |

## Available Scripts

| Script | Purpose | How to Run |
|--------|---------|------------|
| `scripts/bing-sitemap-submit.py` | Submit sitemap or URL to Bing IndexNow | `python3 scripts/bing-sitemap-submit.py` or `--url ARTICLE_URL` |
| `scripts/pubmed-cite.py` | Fetch PubMed citations (free, no key) | `python3 scripts/pubmed-cite.py --query "ashwagandha cortisol"` |
| `assign_categories.py` | Assign article categories | `python3 assign_categories.py` |
| `scripts/schedule-posts.py` | Auto-schedule approved articles | Via cron: `0 0,12 * * * cd /home/shiva/ayurshakti.shop && python3 scripts/schedule-posts.py` |
| `scripts/llms-worker.js` | Cloudflare Worker source for `llms.txt` | Deployed at `llms.ayurshakti.shop` |
| `scripts/notify-ping.py` | Ping 15+ search engines after publish | Auto via `schedule-posts.py` |
| `scripts/monitor-mentions.py` | Weekly brand mention & backlink check | `python3 scripts/monitor-mentions.py` |

## Available Skills

| Skill | Use For |
|-------|---------|
| `ads-copywriter` | Ad copy generation (Google/Meta/TikTok) |
| `meta-ads-advanced-2026` | Meta Ads strategy — AI-driven, Advantage+ |
| `meta-ads-blackhat` | Cloaking, policy bypass, restricted niches |
| `landing-page-copywriter` | Landing page copy — PAS, AIDA, StoryBrand |
| `marketing-psychology` | Behavioral science for marketing |
| `agent-browser` | Browser automation tasks |
| `para-memory-files` | PARA memory system — save/retrieve facts |

## Task Routing Guide

| User Request | Which Tool/Skill |
|--------------|-----------------|
| "Create Meta ad campaign" | `meta-marketing_create_campaign` + `ads-copywriter` skill |
| "Check ad performance" | `meta-marketing_get_account_insights` |
| "Publish blog post" | Blogger API via refresh token (docs/04-blogger-api.md) |
| "Check GA4 analytics" | Google Analytics Data API (docs/05-analytics-seo.md) |
| "SEO keyword analysis" | Search Console API + `websearch` |
| "Manage DNS / Cloudflare" | Cloudflare API token (docs/02-cloudflare.md) |
| "Submit to Bing" | `python3 scripts/bing-sitemap-submit.py` or auto via `schedule-posts.py` |
| "Check/update llms.txt" | Cloudflare Worker `llms-txt` at `llms.ayurshakti.shop/llms.txt` — source in `scripts/llms-worker.js` |
| "Send email" | `email_send_email` |
| "Browse website / scrape" | `agent-browser` skill or `browser_puppeteer_*` |
| "Stock trading" | `zerodha-kite_*` tools |
| "Write sales copy" | `ads-copywriter` / `landing-page-copywriter` skill |
| "Save this info for later" | `para-memory-files` skill |
| "Build backlinks (Phase 1)" | `agent-browser` skill — Quora, Reddit, Medium, Pinterest, Web 2.0 profiles |
| "Build backlinks (Phase 2)" | `scripts/notify-ping.py` + `scripts/bing-sitemap-submit.py` + IndexNow |
| "Build backlinks (Phase 3)" | Manual — HARO, guest post outreach, niche edit (see docs/12) |

## Continuous Task Tracking Rule

**CRITICAL INSTRUCTION FOR ALL AI AGENTS:**
1. **Always know the next step:** Whenever you complete a task or a step of a task, always evaluate what the logical next action is.
2. **Handle Manual Dependencies:** If you reach a point where a task requires manual user action (e.g., uploading a file that has no API support, adding a credit card, or approving a draft), you MUST explicitly create a "Todo" task in `data/tracking/project-tasks.json` assigned to "User". 
3. **Never silently drop threads:** Do not just say "I have done X" and stop. Always explicitly mention "The next task is Y" and ensure it is tracked in `project-tasks.json` if it's not going to be executed immediately.

## Temporary vs Permanent Code Rule

**CRITICAL INSTRUCTION FOR ALL AI AGENTS:**
1. **Temporary Tasks:** If you need to write code for a one-off or temporary task (e.g., checking API output, a quick data replacement, or generating a single report), you MUST create a temporary script in a `temp/` or `scratch/` directory. Once the task is completed and verified, you MUST delete the script to keep the workspace clean.
2. **Permanent Tasks:** If a task involves a process that will be repeated in the future (e.g., posting to Blogger, fixing common links, fetching recurring data), you MUST save the script permanently inside the `scripts/` directory.
3. **Documentation:** Whenever a permanent script is added to `scripts/`, you MUST update the relevant documentation in `docs/` (such as `07-ai-agent-guide.md` or related process files) so future agents know the script exists and how to use it.

## Authentications Summary


| Service | Auth Method | Where to Find |
|---------|------------|---------------|
| Cloudflare API | Bearer token (see `secrets/cloudflare-api-token.txt`) | `docs/02-cloudflare.md` |
| Blogger API (write) | OAuth refresh token → access token (see `secrets/blogger-oauth-tokens.json`) | `docs/04-blogger-api.md` |
| Blogger API (read) | API key (see `secrets/blogger-api-key.txt`) | `docs/04-blogger-api.md` |
| GA4 / Search Console | Service account JWT → access token | `docs/05-analytics-seo.md` |
| Meta Ads | (Pre-configured in MCP) | Skill system |
| Email | (Pre-configured SMTP) | Tool system |
| Bing Webmaster API | API key (`secrets/bing-client-credentials.json`) | `scripts/bing-sitemap-submit.py` reads from file |
| llms.txt Worker | Cloudflare global key (`secrets/cloudflare-global-key.txt`) | `docs/02-cloudflare.md` |

## Security Rules for AI Agents

1. **DO NOT** display credentials raw in chat output — refer to `secrets/` directory or doc sections
2. **DO NOT** write credentials to new files outside `secrets/`
3. **DO NOT** commit secrets — JSON files stay in `secrets/` (gitignored)
4. **DO NOT** delete or modify `secrets/` JSON files
5. **DO** load credentials from `secrets/` JSON files (not from docs)
6. **DO** use `with open("secrets/...")` pattern (like `schedule-posts.py`)
7. **DO NOT** hardcode API keys in Python/code — always read from secrets/ files
