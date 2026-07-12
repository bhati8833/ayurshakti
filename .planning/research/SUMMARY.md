# Project Research Summary

**Project:** ayurshakti.shop — Ayurvedic Health Blog on Blogger with AdSense Monetization
**Domain:** YMYL Health/Wellness Content × Multi-Platform Search Indexing × Zero-Budget Automation
**Researched:** 2026-07-12
**Confidence:** HIGH

## Executive Summary

ayurshakti.shop is a new-domain Ayurvedic health blog on Google Blogger targeting AdSense monetization. The project faces a dual challenge: **YMYL compliance** (health content requires E-E-A-T signals, named authorship, medical disclaimers, 20+ articles minimum) and **technical distribution automation** (broken scheduler, multi-platform search indexing via IndexNow, AI crawler optimization via llms.txt). Research shows that in 2026, health blogs fail AdSense review primarily due to missing legal pages, anonymous AI content, and premature application with insufficient article volume — not technical SEO gaps.

The recommended approach is a **strictly sequenced four-phase roadmap**: Phase 0 establishes the non-negotiable compliance foundation (5 legal pages, author bio, disclaimer template, scheduler fix). Phase 1 builds content volume (30 articles in topic clusters with PubMed citations) while fixing the broken automation pipeline. Phase 2 activates multi-source traffic distribution (Pinterest, Quora/Reddit, email, social auto-posting). Phase 3 reaches 50+ articles and applies for AdSense only after a full E-E-A-T audit. Key risks are mitigated by: mandatory human editing gate before publish, long-tail keyword strategy, IndexNow for instant multi-engine indexing, and Cloudflare Worker edge-served llms.txt for AI crawler control.

---

## Key Findings

### Recommended Stack

The existing Python 3.11+ / Blogger API / Cloudflare Workers stack is solid and should not change. **Three new additions** enable multi-platform indexing and AI crawler optimization:

**Core technologies:**
- `bing-webmaster-tools==1.2.0` (Python SDK) — Only maintained async Python client for Bing Webmaster Tools API v2; covers SubmitUrl, GetCrawlIssues, GetQueryData; built on aiohttp + Pydantic
- `yandex-webmaster-api==0.0.3` — Only Python wrapper for Yandex Webmaster API v4; requires OAuth 2.0 Authorization Code flow; covers hosts, sitemaps, recrawl quota, search queries
- `index-now==0.3.0` — Only maintained Python client for IndexNow protocol; single POST to `api.indexnow.org` notifies Bing, Yandex, Seznam, Naver, Yep simultaneously; supports 10k URL batches
- `robots.txt` + `llms.txt` via Cloudflare Workers — Zero-dependency static files served at edge; `llms.txt` is the emerging AI crawler standard (read by GPTBot, ClaudeBot, PerplexityBot); `robots.txt` blocks training crawlers (GPTBot, ClaudeBot, CCBot, Bytespider) while allowing search/indexing bots (OAI-SearchBot, ChatGPT-User, PerplexityBot)

**Seznam strategy:** No custom API client — Seznam has no public REST API. Use IndexNow (Seznam participates) + sitemap.xml + robots.txt allowing `SeznamBot`.

---

### Expected Features

**Must have (table stakes — 16 features, non-negotiable for AdSense):**
- TS-01: 50+ published articles (800-1500+ words) — Current: 11, need ~39 more at 5-7/week
- TS-02: 5 legal pages (About, Contact, Privacy, Medical Disclaimer, Terms) — Only Privacy exists
- TS-03: Medical disclaimer on every article — Add to Blogger template footer
- TS-04/05: HTTPS + mobile-responsive + PageSpeed >80 — Cloudflare CDN active, verify
- TS-06: Clear navigation + 4-6 Ayurveda categories — Organize existing + planned content
- TS-07/08: GSC + GA4 + Bing Webmaster Tools + IndexNow — GSC/GA4 done, Bing/IndexNow pending
- TS-09: XML sitemap to all engines — Blogger auto-generates atom.xml, submit to GSC/Bing/Yandex
- TS-10: Author bio with credentials on every article — September 2025 Perspective Update mandate
- TS-11: Article-level last-updated date visible — Add to Blogger template
- TS-12: JSON-LD schema (Article, FAQ, HowTo, MedicalWebPage) — Partially done, verify + expand
- TS-13: Social sharing buttons — Add to template
- TS-14: Internal linking system — "Related Posts" + manual cross-links
- TS-15: Email subscription (Google Sheets + Apps Script) — Infrastructure exists, add signup form
- TS-16: Post scheduling consistency (Mon/Wed/Fri) — **Blocker: scheduler broken (Pitfall M1)**

**Should have (differentiators — 10 features, competitive advantage):**
- D-01: PubMed-cited evidence-based content — Inline citations with hyperlinks to studies
- D-02: AI crawler optimization (llms.txt) — **Already deployed via Cloudflare Worker**
- D-03: Multi-platform auto-distribution pipeline — X, Bluesky, Pinterest, LinkedIn, Medium from single trigger
- D-04: Topic cluster architecture — 4-5 deep clusters (Digestive Health, Skin & Hair, Stress & Sleep, Pet Wellness, Immunity)
- D-05: Quora + Reddit automated backlink generation — Strategic answers with blog links
- D-06: Pinterest SEO-optimized pin generation — Visual search with 2-3 year pin shelf life
- D-07: Bilingual content (English + Hindi Hinglish) — Capture vernacular search traffic
- D-08: Monthly content freshness audit — 90-day review cycle, update citations/dates
- D-09: Google Discover optimization — 1200px+ images, Discover-friendly headlines
- D-10: Pet Wellness sub-niche — Under-served, high shareability, topic cluster opportunity

**Defer (v2+ — anti-features to explicitly avoid):**
- A-01 to A-12: No unsubstantiated medical claims, no diagnosing/prescribing, no "miracle cure" language, no unmoderated comments, no health affiliate links, no aggressive ad density, no auto-play ads, no AI-spun content, no pirated images, no undisclosed sponsored posts, no clickbait, no Blogger native sidebar ads

---

### Architecture Approach

**Unified Indexing Orchestrator Pattern** — Single entry point (`indexing-orchestrator.py`) replaces fragmented per-engine scripts. On article publish: Blogger API → IndexNow bulk POST (notifies Bing/Yandex/Seznam/Naver) → platform-specific status queries (Seznam Webmaster API, Yandex Webmaster API when key available) → granular pipeline status updates (`pinged-indexnow`, `pinged-seznam`, `pinged-yandex`, `ai-crawled`).

**Pipeline Status Extension** — Extend `lib/tracking.py` VALID_STAGES to track each platform separately with success/failure details per article.

**Cloudflare Worker AI Crawler Logging** — Extend `llms-worker.js` to detect AI user-agents (GPTBot, ClaudeBot, PerplexityBot, etc.), increment KV counters per bot per day, log to console for real-time debugging. Daily cron exports KV → `data/tracking/ai-crawler-analytics.json`.

**Periodic Analytics Export** — Python script (`ai-crawler-analytics.py`) pulls Cloudflare KV via `wrangler` CLI, merges into local JSON, feeds `analytics-report.py`.

**Major components:**
1. `indexing-orchestrator.py` (NEW) — Unified submission + status tracking for all platforms
2. `llms-worker.js` (EXTEND) — Edge serve llms.txt + AI crawler detection/logging to KV
3. `ai-crawler-analytics.py` (NEW) — Daily KV export → local tracking JSON
4. `analytics-report.py` (EXTEND) — Add indexing success rates + AI crawler metrics to daily report
5. `schedule-posts.py` (FIX) — Post ID bug fix, dry-run mode, calls orchestrator post-publish

---

### Critical Pitfalls

1. **C1: YMYL Health Content Without E-E-A-T Signals** — AdSense rejection #1 for health blogs. No author bylines, no credentials, anonymous AI content = "unaccountable publisher." **Prevention:** Named author on every post, author bio page with experience, PubMed citations for every health claim, prominent medical disclaimer, AI transparency footer.

2. **C2: Unedited AI Content That Reads Like Generic Output** — March 2026 Core Update penalized sites with >40% unedited AI content (55%+ traffic loss). **Prevention:** Mandatory human editing gate (AI draft → human adds unique insight/local example/personal story), vary article structure, original AI-generated images, max 5-7 articles/week, transparency footer.

3. **C3: Missing Mandatory Pages (About, Contact, Privacy, Disclaimer, Terms)** — Instant AdSense rejection. Privacy Policy must mention AdSense cookies + AI crawlers. **Prevention:** Create all 5 pages in Phase 0, link in footer, update Privacy Policy to 2026 standards.

4. **C4: Applying for AdSense Too Early (<20 articles)** — #1 rejection reason. Each rejection adds 2-4 week cooldown. **Prevention:** Hard gate at 20+ high-quality articles (1000-2000 words each), 2+ months active publishing, consistent organic traffic before applying.

5. **C5: No Medical Disclaimer on Health Content** — Hard rejection signal (Policy 8). Legal liability risk. **Prevention:** Standardized disclaimer template in theme, auto-append to every health article, avoid definitive claims ("cures") → use "may help," "traditionally used for."

---

## Implications for Roadmap

Based on research, suggested phase structure:

### Phase 0: Foundation & Compliance (Week 1-2)
**Rationale:** All critical pitfalls (C1, C3, C5) are foundation-level. Legal pages, disclaimers, author attribution, and technical verification must exist BEFORE any content push or SEO effort. The broken scheduler (M1) must be fixed to enable Phase 1.
**Delivers:**
- 5 legal pages live (About, Contact, Privacy, Medical Disclaimer, Terms)
- Medical disclaimer template in Blogger theme (auto-appends to all posts)
- Author bio page + per-article author box with credentials
- Scheduler bug fixed (post ID issue), dry-run mode verified for 1 week
- Technical foundation verified: HTTPS, mobile, PageSpeed, schema markup
- Current 11 articles audited for medical claims violations (A-01 to A-04)
**Addresses:** TS-02, TS-03, TS-04, TS-05, TS-06, TS-10, TS-11, TS-12, AD-01 to AD-06, A-01 to A-04
**Avoids:** C1, C3, C5, M1, M3, M5

### Phase 1: Fix Automation + Content Pipeline (Week 3-8)
**Rationale:** Content volume (TS-01) is the AdSense gate. Must fix automation first (M1), then produce 30+ articles using topic clusters (D-04) with PubMed citations (D-01) and human editing gate (C2 prevention). Long-tail keyword strategy (M2 prevention) built into topic selection.
**Delivers:**
- `indexing-orchestrator.py` deployed (IndexNow + Seznam/Yandex status)
- `llms-worker.js` extended with AI crawler KV logging
- Scheduler reliably publishing 5-7 articles/week (Mon/Wed/Fri)
- 30+ articles published across 4-5 topic clusters
- Every article: PubMed citations, internal links (2-3), medical disclaimer, author attribution, JSON-LD schema
- GSC + Bing + IndexNow verified per article
**Addresses:** TS-01, TS-07, TS-08, TS-09, TS-12, TS-14, D-01, D-02, D-04
**Avoids:** C2, C4, M1, M2, M5, m1, m4, m5, m6
**Uses:** `bing-webmaster-tools`, `yandex-webmaster-api`, `index-now`, Cloudflare Workers KV

### Phase 2: Multi-Source Traffic Distribution (Week 9-12)
**Rationale:** Single-source Google dependency (M6) is fatal. Distribution channels have technical blockers (cookie auth M7, Pinterest SEO M4). Must activate BEFORE AdSense application to show multi-source traffic credibility.
**Delivers:**
- Auto-distribution pipeline: Blogger publish → X + Bluesky + Pinterest + LinkedIn + Medium
- Pinterest Rich Pins configured, 3-5 pin designs/article, keyword-optimized descriptions
- Quora/Reddit automated answer posting (browser automation for cookie-based platforms)
- Email subscription form in sidebar/footer, Google Sheets capture working
- `ai-crawler-analytics.py` daily cron exporting Cloudflare KV → local analytics
- `analytics-report.py` includes indexing success rates + AI crawler activity
**Addresses:** D-03, D-05, D-06, TS-15, D-02 (maintain), TS-08
**Avoids:** M4, M6, M7
**Implements:** Architecture components 2, 3, 4, 5

### Phase 3: Scale to AdSense Readiness (Week 13-16)
**Rationale:** AdSense requires 50+ articles (C4), all policy pages (C3), and demonstrable E-E-A-T (C1). This phase reaches volume threshold and runs full pre-application audit.
**Delivers:**
- 50+ articles published (cumulative)
- Full E-E-A-T audit: every article has author bio, citations, disclaimer, freshness date
- First content freshness audit (D-08) — review/update declining articles
- Google Discover optimization (D-09) — image/headline standards applied
- Ads.txt served via Cloudflare Worker (M8 prevention)
- AdSense application submitted with complete checklist
**Addresses:** TS-01 (target), AD-01 to AD-06, AD-08, AD-09, AD-10, D-08, D-09
**Avoids:** C4, C1 (re-verification), M8, m3, m8

### Phase 4: Monetization & Expansion (Week 17+)
**Rationale:** Post-approval, focus shifts to revenue optimization and traffic scaling.
**Delivers:**
- AdSense code installed, ad placement optimized (1-2 above fold, 1-2 in content)
- RPM monitoring, Tier-1 traffic growth strategies
- Bilingual content experiment (D-07) — Hindi/Hinglish cluster
- Pet Wellness sub-niche expansion (D-10)
- Ongoing quarterly content audits, cookie health monitoring (M7)
**Addresses:** AD-07, D-07, D-10
**Implements:** Log rotation (m7), credential expiry alerts

---

### Phase Ordering Rationale

- **Foundation first (Phase 0):** All critical AdSense rejection triggers (C1, C3, C5) are compliance issues that must exist before content scales. Fixing scheduler (M1) unblocks everything downstream.
- **Content before distribution (Phase 1 → 2):** No content = nothing to distribute. Topic clusters (D-04) guide article creation; PubMed citations (D-01) build E-E-A-T during production, not after.
- **Distribution before AdSense (Phase 2 → 3):** AdSense reviewers favor sites with traffic diversity (M6). Multi-source traffic must be operational before application.
- **Volume gate before application (Phase 3):** Hard 20+ article minimum (C4), 50+ target. Rushing application wastes months in cooldowns.
- **Architecture enables phases:** `indexing-orchestrator.py` (Phase 1) feeds status to `analytics-report.py` (Phase 2). `llms-worker.js` KV logging (Phase 1) feeds `ai-crawler-analytics.py` (Phase 2).

---

### Research Flags

**Phases likely needing deeper research during planning (`/gsd-plan-phase --research-phase`):**
- **Phase 0:** Legal/compliance review for medical disclaimer language — health niche has specific regulatory requirements (FDA, FTC, state laws). Need attorney review or validated template.
- **Phase 1:** Blogger API edge cases for scheduler fix — the "Invalid post id" 400 error needs root cause analysis (Pitfall M1). Also: IndexNow key generation/hosting verification on Blogger subdomain.
- **Phase 2:** Social platform OAuth migration — Reddit, Quora, Medium currently use cookie auth (M7). Need research on official APIs vs. browser automation reliability. Pinterest Rich Pins validation on Blogger.
- **Phase 3:** AdSense application timing strategy — optimal site age (3-6 months), traffic thresholds, rejection appeal process, ads.txt deployment on Blogger via Cloudflare Worker.

**Phases with standard patterns (skip research-phase):**
- **Phase 1 (core content production):** Well-documented patterns — PubMed API integration exists, topic cluster SEO is standard, human editing gate is process not tech.
- **Phase 4 (monetization optimization):** Standard AdSense placement optimization, A/B testing patterns well-established.

---

## Confidence Assessment

| Area | Confidence | Notes |
|------|------------|-------|
| Stack | HIGH | Official SDK docs (Bing, Yandex, IndexNow), Cloudflare Workers well-documented, existing Python stack battle-tested |
| Features | HIGH | 20+ 2026 sources across AdSense guides, YMYL/E-E-A-T docs, health niche case studies. Consistent consensus on table stakes. |
| Architecture | HIGH | Patterns derived from existing codebase (`schedule-posts.py`, `lib/tracking.py`, `llms-worker.js`) + IndexNow protocol spec. No speculative components. |
| Pitfalls | HIGH | Project-specific findings (CONCERNS.md, PROJECT.md) + 15+ 2026 AdSense/SEO sources. Critical pitfalls validated against actual project state. |

**Overall confidence:** HIGH

### Gaps to Address

- **Medical disclaimer legal review:** No attorney-reviewed disclaimer template. Risk: regulatory non-compliance. *Handle:* Source validated template from health law resource or budget for legal review in Phase 0.
- **Blogger ads.txt deployment:** Blogger doesn't support custom root files. Cloudflare Worker rewrite needed but exact implementation untested. *Handle:* Prototype Worker route in Phase 0, verify `ayurshakti.shop/ads.txt` serves correctly.
- **Cookie auth migration timeline:** Reddit/Quora/Medium have no official posting APIs. Browser automation (Puppeteer) adds complexity. *Handle:* Phase 2 research spike — evaluate `browser-use` or `puppeteer` reliability vs. maintaining cookie refresh process.
- **AdSense approval timeline variance:** 6-8 week estimate to 50 articles assumes fixed scheduler + consistent 5-7/week output. Real-world may stretch to 10-12 weeks. *Handle:* Build buffer into Phase 3; don't schedule AdSense application until 50 articles actually published.
- **Tier-1 traffic acquisition:** Health niche RPM $8-20 requires US/UK/CA/AU traffic. Indian traffic RPM $0.50-2. Current strategy relies on long-tail SEO + Pinterest. *Handle:* Phase 2 monitor GA4 geo breakdown; if Tier-1 < 30%, add targeted content for US/UK search intent.

---

## Sources

### Primary (HIGH confidence)
- **IndexNow Protocol** — https://www.indexnow.org/documentation — Protocol spec, endpoints, 10k URL batch limits, key verification
- **Bing Webmaster Tools API** — https://learn.microsoft.com/en-us/bingwebmaster/ — Official Microsoft docs, API endpoints, rate limit guidance
- **Yandex Webmaster API v4** — https://yandex.com/dev/webmaster/doc/en/concepts/getting-started — OAuth flow, host verification, recrawl quota endpoints
- **Google AdSense Program Policies 2026** — https://support.google.com/adsense — Official policies, YMYL requirements, approval criteria
- **Google Search Quality Rater Guidelines (2025)** — E-E-A-T framework, YMYL classification, health content standards
- **llms.txt Proposal** — https://answer.ai/blog/llms-txt-proposal — Standard specification, adoption by AI crawlers

### Secondary (MEDIUM confidence)
- **bing-webmaster-tools SDK** — https://github.com/merj/bing-webmaster-tools — README, PyPI, source code review (v1.2.0)
- **yandex-webmaster-api SDK** — https://pypi.org/project/yandex-webmaster-api/ — v0.0.3 (2024-03-12), only Python v4 wrapper
- **index-now Python SDK** — https://github.com/jakob-bagterp/index-now-for-python — v0.3.0, bulk submission, sitemap parsing
- **2026 AdSense Approval Guides** — BlogerHub, DigitalTechnest, SahilDubey, Webtimize, Bloggerscope — Consistent 15-25 article threshold, legal page requirements
- **YMYL Health Content Guides 2026** — Tygart Media, Blueprint Media, Search Engine Land — September 2025 Perspective Update details
- **Pinterest SEO 2026** — BloggersPassion, Automateed, SorinBlogger — Rich Pins, pin longevity, keyword optimization
- **Project-specific audits** — PROJECT.md, CONCERNS.md — Current state: 11 articles, broken scheduler, empty indexing log, deployed llms.txt

### Tertiary (LOW confidence — needs validation)
- **Seznam Webmaster API** — https://reporter.seznam.cz/wm/ — No public docs; reverse-engineered by Czech tools (Collabim, Semor). IndexNow participation confirmed but API stability unknown.
- **AI Crawler User-Agent Lists 2026** — Contently, BestSEO.sg, Pixis, Verlua, IndexDoctor (Apr-Jun 2026) — Crawler tokens may change; monitor ai-robots-txt GitHub org for updates.
- **Health Niche RPM Benchmarks** — QuickBlogTools, EarnifyHub, Adstimate — $8-20 RPM for US traffic, $0.50-2 for India. Actuals vary by seasonality and AdSense category.
- **Blogger Platform E-E-A-T Limitations** — Community knowledge; no official Google statement comparing Blogger vs WordPress for YMYL.

---

*Research completed: 2026-07-12*
*Ready for roadmap: yes*