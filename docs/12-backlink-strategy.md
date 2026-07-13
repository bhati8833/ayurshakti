# Backlink Strategy & SEO Architecture — ayurshakti.shop

> **OpenCode Required Skills:**
> Before executing tasks in this document, load the following skills from the OpenCode library (Home Directory):
> - `marketing-psychology`
> - `competitive-landscape`
> - `seo-keyword-strategist`

> **SEO Component: Off-Page Optimization**
> Part of the ayurshakti.shop SEO ecosystem. Complements on-page (docs/08, docs/09) and technical SEO.

## Architecture Overview

```
BACKLINK SYSTEM
│
├─ PHASE 1: AI AGENT (Browser Automation)
│   ├─ Quora ──── answers with links
│   ├─ Reddit ─── r/Ayurveda participation
│   ├─ Medium ─── article republish
│   ├─ Pinterest ─ pin images with URL
│   └─ Web 2.0 ── profile backlinks
│
├─ PHASE 2: API AUTO (Scripts & Tools)
│   ├─ notify-ping.py ─── 15+ ping services
│   ├─ IndexNow ───────── already running ✅
│   ├─ shoutrrr ───────── social auto-post
│   ├─ GSC / GA4 ──────── performance monitoring
│   ├─ monitor-mentions ─ brand mention alerts
│   └─ directory-submit ─ business listings
│
└─ PHASE 3: MANUAL HIGH-VALUE
    ├─ HARO ─── journalist query responses
    ├─ Guest Post ── DR 40+ health sites
    ├─ Niche Edit ── existing article link insert
    ├─ Broken Link ── dead link replacement
    └─ Skyscraper ── better content → steal backlinks
```

---

## Phase 1: AI Agent (Web-Enabled Automation)

Browser automation ke through AI agent yeh platforms handle karega. Agent form fill karega, content submit karega, accounts manage karega.

### 1A. Quora Backlinks

| Detail | Spec |
|--------|------|
| **Link Type** | Do-Follow in answers + No-Follow in profile |
| **DA** | 93 |
| **Method** | Agent search relevant questions → write answer → link to article |
| **Rate** | 5 answers/week |
| **Tool** | `agent-browser` skill (uses `secrets/cookies-quora.txt`) |

**Workflow:**
```
agent-browser → navigate quora.com → search "ayurveda [topic]" questions
→ filter recent + unanswered → write 200-word answer
→ link to ayurshakti.shop article → submit
```

### 1B. Reddit Backlinks

| Detail | Spec |
|--------|------|
| **Link Type** | No-Follow in posts + Do-Follow in wiki/profile (with age) |
| **DA** | 92 |
| **Method** | Participate in r/Ayurveda, r/herbalism, r/NaturalHealth |
| **Rate** | 3-5 comments + 1 post/week |
| **Tool** | `agent-browser` skill (uses `secrets/cookies-reddit.txt`) |

**Workflow:**
```
agent-browser → reddit.com → login → browse r/Ayurveda
→ find relevant discussion → natural mention + link
→ OR create text post: "I wrote about [topic] on my blog"
```

### 1C. Medium Backlinks

| Detail | Spec |
|--------|------|
| **Link Type** | Do-Follow (in article body) |
| **DA** | 94 |
| **Method** | Republish condensed version of article with canonical link |
| **Rate** | 2 articles/week |
| **Tool** | `agent-browser` skill (uses `secrets/cookies-medium.txt`) |

**Workflow:**
```
Take article → create 800-word condensed version
→ add "Originally published at ayurshakti.shop" with do-follow link
→ publish on Medium → cross-post to relevant publications
```

### 1D. Pinterest Backlinks

| Detail | Spec |
|--------|------|
| **Link Type** | No-Follow |
| **DA** | 92 |
| **Method** | Create infographic → pin with article URL |
| **Rate** | 5 pins/week |
| **Tool** | API Script (`secrets/pinterest-creds.json`) |

### 1E. Web 2.0 Profile Backlinks

| Platform | Link Type | Action | Priority |
|----------|-----------|--------|----------|
| **Tumblr** (DA 86) | Do-Follow | Create blog → cross-post articles | HIGH |
| **Google Business** (DA 96) | No-Follow | Complete profile → website link | HIGH |
| **Justdial** (DA 59) | Do-Follow | Business listing → website | MEDIUM |
| **Indiamart** (DA 63) | No-Follow | Business listing | MEDIUM |
| **LinkedIn Company** (DA 98) | No-Follow | Company page → website in bio | HIGH |

---

## Phase 2: API Auto (Scripts & Tools)

Server-side scripts jo automatically chalenge. No manual intervention.

### 2A. Ping Services (`scripts/notify-ping.py`)

**Purpose:** Har article publish ke baad 15+ search engines/services ko notify kare.

| Service | Endpoint | Protocol |
|---------|----------|----------|
| Google Blog Search | `http://blogsearch.google.com/ping` | HTTP GET |
| Ping-O-Matic | `http://rpc.pingomatic.com/` | XML-RPC |
| Bing Webmaster | `https://www.bing.com/webmaster/ping.aspx` | HTTP GET |
| Weblogs.com | `http://rpc.weblogs.com/ping` | XML-RPC |
| FeedBurner | `http://ping.feedburner.com` | HTTP GET |
| Blogflux | `http://rpc.blogflux.com/ping` | XML-RPC |
| Feedster | `http://api.feedster.com/ping` | HTTP GET |
| Blogdigger | `http://www.blogdigger.com/ping` | HTTP GET |
| BlogRoll | `http://rpc.blogrolling.com/ping` | XML-RPC |
| IceRocket | `http://rpc.icerocket.com/ping` | XML-RPC |
| PingMyBlog | `http://pingmyblog.com/ping` | HTTP GET |
| BlogBot | `http://blogbot.com/rpc/ping` | XML-RPC |
| Pingoat | `http://pingoat.com/goat/Rpc` | XML-RPC |
| MyBlogLog | `http://www.mybloglog.com/rpc/ping` | XML-RPC |
| Technorati | `http://rpc.technorati.com/rpc/ping` | XML-RPC |

**Integration:** `schedule-posts.py` publish ke baad auto-call karega.

### 2B. IndexNow (Already Running ✅)

| Engine | Status | Script |
|--------|--------|--------|
| Bing | ✅ | `scripts/bing-sitemap-submit.py` |
| Yandex | ✅ | Same script |
| Naver | ✅ | Same script |
| Seznam | ✅ | Same script |
| Yep | ✅ | Same script |
| Internet Archive | ✅ | Same script |
| Amazonbot | ✅ | Same script |

### 2C. Social Auto-Post (`scripts/social-post.py`) ✅

**Implemented:** Bluesky API (direct) + agent-browser queue for X/LinkedIn
**Docker alternative avoided** (daemon not running on server)

| Detail | Spec |
|--------|------|
| **Bluesky** | ✅ Direct API via `atproto` (username + app password) |
| **X (Twitter)** | ✅ Direct API via Free Tier (`secrets/x-creds.json`) |
| **LinkedIn** | 🔄 Queued in `agent-pending-posts.json` → agent browser posts |
| **Pinterest** | ✅ Direct API via Personal Access Token (`secrets/pinterest-creds.json`) |
| **Setup** | `secrets/bluesky-creds.json`, `secrets/x-creds.json`, `secrets/pinterest-creds.json`, + `secrets/cookies-*.txt` for browsers |
| **Integration** | `schedule-posts.py` publish ke baad auto-call karega ✅ |
| **Post frequency** | 1 post/article → Bluesky + queued for X/LinkedIn/Pinterest |

### 2D. Monitor-Mentions (`scripts/monitor-mentions.py`) ✅

**Purpose:** Weekly check karega ki kisi ne ayurshakti.shop ko mention kiya ya nahi.

| Method | Mechanism | Status |
|--------|-----------|--------|
| **Web Search** | DuckDuckGo HTML API — find "ayurshakti" mentions on other sites | ✅ |
| **Competitor Pulse** | Check competitor sites are up (EasyAyurveda, AyurTimes, PlanetAyurveda) | ✅ |
| **Site Health** | Check own site + sitemap + robots.txt + llms.txt all return 200 | ✅ |
| **GSC Backlinks** | Manual link printed in report → open GSC web UI | 🔄 |
| **IndexNow Stats** | Confirm Bing still accepting submissions | ✅ |

**Cron:** `0 10 * * 0` (every Sunday 10am) ✅

### 2E. Directory Submission (Agent + API Hybrid)

| Directory | DA | Method | Backlink |
|-----------|-----|--------|----------|
| Google Business | 96 | Agent browser | No-Follow |
| Justdial | 59 | Agent browser | Do-Follow |
| Indiamart | 63 | Agent browser | No-Follow |
| Sulekha | 55 | Agent browser | Do-Follow |
| Practo (if relevant) | 68 | Agent browser | Do-Follow |
| LinkedIn Company | 98 | Manual once | No-Follow |
| Crunchbase | 91 | Manual once | Do-Follow |

---

## Phase 3: Manual High-Value

Tumhe khud karna hoga (ya AI agent ko specific instructions dekar). Highest impact.

### 3A. HARO (Help a Reporter)

| Detail | Spec |
|--------|------|
| **URL** | `https://www.helpareporter.com/` |
| **Cost** | Free tier (basic queries) |
| **Method** | Signup → daily emails → relevant queries → pitch answer |
| **Success Rate** | 5-10% (out of 10 pitches, 1 gets published) |
| **Backlink Type** | Do-Follow from high-DR news sites (DR 70+) |
| **Time** | 15 min/day |
| **Tool** | Agent browser can read queries, but response must be personal |

**Workflow:**
```
Daily: Open HARO → filter "Health / Wellness" queries
→ find match → write expert quote (100 words)
→ include "Suresh Bhati, Ayurvedic researcher at ayurshakti.shop"
→ submit → wait for journalist to publish
```

### 3B. Guest Post Outreach

| Detail | Spec |
|--------|------|
| **Target Sites** | EasyAyurveda (42), AyurTimes (45), PlanetAyurveda (50), Health blogs |
| **Method** | Email outreach → offer unique article → include backlink |
| **Pitch Template** | "I've written for [site]. Here's a unique article idea for your audience..." |
| **Rate** | 2 outreach/week |
| **Success Rate** | 20-30% |
| **Backlink Type** | Do-Follow in author bio or article body |

**Target Sites (DR sorted):**

| Site | DR | Topic Fit | Outreach Email |
|------|-----|-----------|---------------|
| planetayurveda.com | 50 | Exact match | contact@planetayurveda.com |
| ayurtimes.com | 45 | Exact match | info@ayurtimes.com |
| easyayurveda.com | 42 | Exact match | easyayurveda@gmail.com |
| ayurhealthline.com | 38 | Ayurveda | contact@ayurhealthline.com |
| bimbima.com | 35 | Ayurveda | admin@bimbima.com |

### 3C. Niche Edit Backlinks

| Detail | Spec |
|--------|------|
| **Method** | Find existing articles that mention a topic but not your site |
| **Action** | Email site owner: "I noticed your article on [topic] — I have a detailed guide at ayurshakti.shop that adds value" |
| **Rate** | 1-2 outreach/week |
| **Success Rate** | 15-25% |
| **Tool** | Search `"keyword" + "according to research" + "studies show"` for opportunities |

### 3D. Broken Link Building

| Detail | Spec |
|--------|------|
| **Method** | Find broken links on health sites → offer your article as replacement |
| **Tool** | Check My Links (Chrome extension) or `brokenlinkcheck.com` |
| **Target** | Resource pages, "Best Ayurveda blogs" lists |
| **Rate** | 1 outreach/day |
| **Success Rate** | 10-20% |

**Workflow:**
```
Find: "site:*.com "best ayurveda blogs" OR "ayurveda resources""
→ Check each page for broken links
→ If broken link matches your content → email webmaster
→ "Found broken link on your page. I have a relevant article at ayurshakti.shop"
```

### 3E. Email Outreach via Newsletter

| Detail | Spec |
|--------|------|
| **Method** | Email newsletter se existing subscribers ko blog articles bhejna |
| **Tool** | Google Sheets + Apps Script (`docs/15-email-marketing-system.md`) |
| **Link Type** | Direct traffic (no SEO value but high conversion) |
| **Rate** | Weekly newsletter + welcome sequence on signup |
| **UTM Tracking** | `utm_source=email&utm_medium=newsletter&utm_campaign=weekly-{date}` |
| **GA4 Integration** | Email traffic visible in GA4 Acquisition reports |

**Workflow:**
```
Visitor → Signup form (Blogger sidebar) → Google Sheet → Apps Script
  → Welcome email with lead magnet → Weekly newsletter with blog links
  → Click → GA4 tracked → Return visitor → Better SEO signals
```

**Why Email Supports SEO:**
- Return visitor rate badhta hai (Google ranking signal)
- Direct traffic share increases (positive site quality signal)
- Article engagement (time on site, scroll depth) improves
- Social sharing from engaged readers

### 3F. Skyscraper Technique

| Detail | Spec |
|--------|------|
| **Method** | Find top-performing Ayurveda content → create 10x better → ask sites linking to old one to link to yours |
| **Tool** | BuzzSumo free tier OR `websearch` for "most shared ayurveda articles" |
| **Rate** | 1/month |
| **Success Rate** | 15-20% |

---

## Implementation Priority Matrix

| Phase | Item | Impact | Effort | Timeline | Do When |
|-------|------|--------|--------|----------|---------|
| P1 | Quora answers | ⭐⭐⭐ | Low | Week 1 | Agent ready hai, start immediately |
| P1 | Reddit participation | ⭐⭐⭐ | Low | Week 1 | Agent ready hai |
| P1 | Pinterest pins | ⭐⭐ | Low | Week 1 | Infographic banao phir pin karo |
| P1 | Medium republish | ⭐⭐⭐ | Medium | Week 2 | Article ke saath |
| P2 | notify-ping.py | ⭐⭐ | Low | Week 1 | ✅ Done, 15+ ping services |
| P2 | social-post.py | ⭐⭐⭐ | Low | Week 1 | ✅ Done, Bluesky API + agent queue |
| P2 | monitor-mentions.py | ⭐⭐ | Low | Week 1 | ✅ Done, weekly cron |
| P2 | Directory listing | ⭐ | Low | Week 2 | Agent browser 1-time |
| P3 | HARO signup | ⭐⭐⭐⭐⭐ | Low | Week 1 | Aaj hi karo |
| P3 | Guest post outreach | ⭐⭐⭐⭐ | Medium | Week 2-3 | 5 target sites |
| P3 | Niche edit | ⭐⭐⭐⭐ | Medium | Week 3-4 | Research first |
| P3 | Broken link | ⭐⭐⭐⭐ | Medium | Week 3-4 | Ongoing |
| P3 | Skyscraper | ⭐⭐⭐⭐⭐ | High | Month 2-3 | After 30+ articles |

---

## Auto-Pipeline (Post-Publish)

Every article publish triggers this automated pipeline:

```
schedule-posts.py
  ├─ 1. Blogger API → Publish article
  ├─ 2. bing-sitemap-submit.py → IndexNow (7 engines) ✅
  ├─ 3. notify-ping.py → 15+ ping services ✅
  └─ 4. social-post.py → Bluesky direct + X/LinkedIn/Pinterest queue ✅
```

Weekly (Sunday 10am):
```
monitor-mentions.py
  ├─ Web search for backlinks/mentions
  ├─ Site health check (sitemap, robots, llms, homepage)
  ├─ Competitor pulse check
  └─ GSC link report reminder
```

---

## Tooling Summary

### Open Source Tools (Free, Self-Host)

| Tool | Purpose | License | Deploy |
|------|---------|---------|--------|
| [Shoutrrr](https://github.com/coollabsio/shoutrrr) | Social media scheduler | Apache 2.0 | Docker |
| [Open-Dispatch](https://github.com/Matthew-Selvam/Open-Dispatch) | Social API | MIT | Docker |
| [PostPilot](https://github.com/stukenov/postpilot) | Headless browser auto-post | MIT | Python + Playwright |
| [LetMePost.dev](https://github.com/letmepost/letmepost.dev) | Social API proxy | Apache 2.0 | Docker |
| [Pingmap.dev](https://pingmap.dev/) | IndexNow auto-submit | SaaS free tier | Cloud (free) |

### Our Scripts

| Script | Phase | Purpose | File |
|--------|-------|---------|------|
| `bing-sitemap-submit.py` | P2 | IndexNow submission | ✅ Done |
| `notify-ping.py` | P2 | 15+ ping services | ✅ Done |
| `social-post.py` | P2 | Bluesky API + agent queue for X/LinkedIn | ✅ Done |
| `monitor-mentions.py` | P2 | Weekly brand mention & backlink monitoring | ✅ Done |
| `schedule-posts.py` | Core | Auto-publish to Blogger | ✅ Done |

---

## Success Metrics

Track these monthly:

| Metric | Month 1 | Month 2 | Month 3 | Month 4+ |
|--------|---------|---------|---------|----------|
| **Total Backlinks** | 10-20 | 30-50 | 60-100 | 150+ |
| **Referring Domains** | 5-10 | 15-25 | 30-50 | 60+ |
| **Domain Rating (DR)** | 5-10 | 10-20 | 20-30 | 30-40 |
| **GSC Organic Clicks/Day** | 0-5 | 5-20 | 20-50 | 50-100 |
| **HARO Mentions** | 1-2 | 3-5 | 5-10 | 10+ |

---

## Version History

| Date | Changes |
|------|---------|
| 2026-07-07 | Initial doc created — Phase 1/2/3 full architecture |
| 2026-07-07 | Phase 2 implemented: `social-post.py` (Bluesky API + agent queue), `monitor-mentions.py` (weekly cron). Updated ping services list + auto-pipeline section. |
|------|---------|
| 2026-07-07 | Initial creation — Full Phase 1/2/3 backlink architecture with tools, scripts, and priority matrix |
