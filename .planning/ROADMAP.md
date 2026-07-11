# Roadmap: ayurshakti.shop

## Overview

An Ayurveda health + pet wellness blog on Google Blogger, monetized via Google AdSense. The project follows a strict **horizontal layer** structure — each phase completes fully before the next begins. Foundation (legal/compliance) → Automation (fix broken pipeline) → Content (50+ articles) → Indexing/SEO → Traffic Distribution → Analytics → AdSense/Monetization → Infrastructure Cleanup. Zero budget, all free tiers, AI agent-driven with human review.

## Phases

- [ ] **Phase 0: Foundation** - Legal pages, medical disclaimers, technical baseline
- [ ] **Phase 1: Automation Fix** - Fix broken scheduler, extract shared OAuth lib, script cleanup
- [ ] **Phase 2: Content Engine** - 50+ articles across 4-5 topic clusters, consistent publishing cadence
- [ ] **Phase 3: Indexing & SEO Infrastructure** - IndexNow, Google Indexing API, AI crawler optimization
- [ ] **Phase 4: Traffic Distribution** - Social auto-distribution, backlink pipeline, owned channels
- [ ] **Phase 5: Analytics & Monitoring** - GA4 verification, multi-source dashboard, credential health
- [ ] **Phase 6: AdSense & Monetization** - Pre-application audit, apply, optimize ad placement
- [ ] **Phase 7: Infrastructure Cleanup** - Code quality, credential migration, monitoring

## Phase Details

### Phase 0: Foundation

**Goal**: Legal compliance, medical disclaimers, and technical foundation verified — site meets AdSense YMYL prerequisites
**Depends on**: Nothing (starting point)
**Requirements**: R-001, R-002, R-003, R-004, R-005, R-006, R-007, R-008, R-009, R-010, R-011, R-012, R-013, R-014, R-015
**Success Criteria** (what must be TRUE):

1. All 5 legal pages (About Us, Contact Us, Medical Disclaimer, Terms of Service, Privacy Policy) exist on the live site and are linked in the footer
2. Standardized medical disclaimer appears on every health article (via theme template)
3. All 12 published articles audited and rewritten to use "may help"/"traditionally used" language — no definitive medical claims remain
4. Author name + bio box with credentials visible at the bottom of every article
5. HTTPS verified, mobile-responsive confirmed, PageSpeed >80 on mobile + desktop, ads.txt configured

**Risk**: CRITICAL — AdSense guaranteed rejection + legal liability without this layer. Missing any single legal page triggers instant rejection. Health claims without disclaimers = permanent AdSense ban risk.
**Resource**: 2 weeks, ~8-10 AI hours/week (page creation, theme template edits, article auditing)
**Plans**: 1 plan
**UI hint**: yes

Plans:

- [ ] 00-PLAN.md — Legal pages, author profile, technical verification, article audit

---

### Phase 1: Automation Fix

**Goal**: Broken scheduler repaired, social poster debugged, script infrastructure standardized
**Depends on**: Phase 0
**Requirements**: R-016, R-017, R-018, R-019, R-020, R-021, R-022, R-023
**Success Criteria** (what must be TRUE):

1. `schedule-posts.py` successfully publishes articles via Blogger API with zero 400 errors — verified by 1 week of manual dry-runs
2. `--dry-run` mode outputs expected schedule without making any API calls
3. Duplicated OAuth logic extracted into `scripts/lib/auth.py` and consumed by all API scripts
4. `requirements.txt` with all Python deps pinned and committed to repo
5. Scheduler logs auto-rotate at 5MB max, keep 5 rotations

**Risk**: CRITICAL — broken scheduler blocks the ENTIRE content pipeline and social distribution. No articles can be published, no content reaches search engines or social media.
**Resource**: 2 weeks, ~15-20 AI hours/week (debugging heavy — root cause of 400 error, testing)
**Plans**: 5/6 plans executed
**UI hint**: no

Plans:

- [x] 01-01-PLAN.md — Fix scheduler 400 error (PUT→POST) and add --dry-run mode (R-016, R-017)
- [x] 01-02-PLAN.md — Extract shared lib modules: auth.py, tracking.py, utils.py (R-020)
- [x] 01-03-PLAN.md — Create requirements.txt + pyproject.toml; clean notify-ping.py to 3 services (R-021, D-10)
- [x] 01-04-PLAN.md — Add subprocess error logging and log rotation (5MB/5 files) (R-018, R-022)
- [x] 01-05-PLAN.md — Add pipeline status dashboard JSON tracking (R-023)
- [ ] 01-06-PLAN.md — Migrate all scripts to shared libs; 1-week dry-run verification (R-020, R-019)

---

### Phase 2: Content Engine

**Goal**: 50+ published articles across 4-5 topic clusters at consistent Mon/Wed/Fri cadence
**Depends on**: Phase 1
**Requirements**: R-024, R-025, R-026, R-027, R-028, R-029, R-030, R-031, R-032, R-033, R-034, R-035, R-036, R-037, R-038
**Success Criteria** (what must be TRUE):

1. 50+ articles published on ayurshakti.shop mapped to 4-5 Ayurveda topic clusters (Digestive Health, Skin & Hair, Stress & Sleep, Pet Wellness, Immunity)
2. Every article contains PubMed citations hyperlinked to actual studies, minimum 1000-2000 words, and at least one 1200px+ featured image
3. Articles publish automatically on Mon/Wed/Fri schedule (±15min jitter) with no manual intervention
4. Every article links to 2-3 existing related articles and passes the 10/10 pre-publish checklist before going live
5. Human editing step adds a unique example, local knowledge, or personal story to every article before publishing

**Risk**: MODERATE — content quality can degrade at volume if AI writing becomes templated. AdSense may reject if articles lack authentic E-E-A-T signals. Losing the "human touch" requirement creates generic content.
**Resource**: 8-10 weeks, ~10-15 AI hours/week (writing heavy — 5-7 articles/week)
**Plans**: TBD
**UI hint**: no

---

### Phase 3: Indexing & SEO Infrastructure

**Goal**: Push-based indexing operational for all major search engines; AI crawler optimization in place
**Depends on**: Phase 2
**Requirements**: R-039, R-040, R-041, R-042, R-043, R-044, R-045, R-046, R-047, R-048
**Success Criteria** (what must be TRUE):

1. IndexNow protocol submits every new article URL to Bing/Yandex/Seznam within 5 minutes of publish
2. Google Indexing API notifies Google of every new/updated article at publish time
3. Custom robots.txt served via Cloudflare correctly allows OAI-SearchBot, Claude-SearchBot, and PerplexityBot while blocking training bots
4. `llms.txt` at `llms.ayurshakti.shop` auto-updates with each new article URL, sorted by priority
5. All published URLs verified as indexed in Google Search Console and Bing Webmaster Tools

**Risk**: HIGH — without this layer, content is invisible to search engines. Articles may take weeks/months to appear in Google/Bing. AI crawlers (ChatGPT Search, Perplexity) cannot cite content they cannot find.
**Resource**: 2 weeks, ~8-10 AI hours/week (configuration, testing, verification scripts)
**Plans**: TBD
**UI hint**: no

---

### Phase 4: Traffic Distribution

**Goal**: Automated social distribution pipeline active across all platforms; backlink generation running
**Depends on**: Phase 3
**Requirements**: R-049, R-050, R-051, R-052, R-053, R-054, R-055, R-056, R-057, R-058, R-059, R-060
**Success Criteria** (what must be TRUE):

1. Every new article auto-posts to X/Twitter, Bluesky, and Pinterest within 30 minutes of publish
2. All 12 existing backlog articles distributed to all social platforms (no "zero social post" articles remain)
3. Quora answer automation and Reddit post automation scheduled and posting on a regular cadence with blog links
4. Pinterest Rich Pins validated and working; 3-5 keyword-optimized pin designs per article
5. Email subscription form visible on site sidebar or footer, and social sharing buttons appear on every article

**Risk**: MODERATE — social accounts could be rate-limited or suspended if posting frequency is too aggressive. Cookie-based auth for Quora/Reddit expires silently (30-90 days) causing broken pipeline with no alerts.
**Resource**: 4 weeks, ~12-15 AI hours/week (API integrations, automation building, backfill posting)
**Plans**: TBD
**UI hint**: yes

---

### Phase 5: Analytics & Monitoring

**Goal**: Multi-source traffic visibility established; credential health monitoring active
**Depends on**: Phase 4
**Requirements**: R-061, R-062, R-063, R-064, R-065, R-066
**Success Criteria** (what must be TRUE):

1. GA4 data verifiably flowing with correct source/medium attribution for organic, social, AI crawler, and direct traffic
2. Multi-source traffic dashboard shows breakdown by channel (Google organic, Bing, social platforms, AI referrals, direct)
3. Cookie expiry dates tracked with alerts configured to notify before expiration
4. Credential health monitoring detects failed auth and sends alert within 24 hours
5. Quarterly content freshness audit cycle defined with checklist and documented in project docs

**Risk**: LOW — all functionality deferred deliberately; no blocking issues. Analytics only adds value once content pipeline and distribution are running.
**Resource**: 1 week, ~6-8 AI hours/week (configuration, script building, dashboard setup)
**Plans**: TBD
**UI hint**: yes

---

### Phase 6: AdSense & Monetization

**Goal**: AdSense approved and ad placement optimized for maximum revenue
**Depends on**: Phase 5
**Requirements**: R-067, R-068, R-069, R-070, R-071, R-072, R-073, R-074
**Success Criteria** (what must be TRUE):

1. Full E-E-A-T audit passed — every article checked for author attribution, medical disclaimer, citations, and original content
2. AdSense application submitted only after: 20+ articles, site age >= 3 months, ALL legal pages live and linked, multi-source traffic confirmed
3. Multi-source traffic NOT 100% Google organic — at least 2 other channels contribute visits
4. AdSense code installed on site AFTER approval is granted (never before)
5. Ad placement optimized: 1-2 ads above the fold, 1-2 in-content, 1 near article end — with no ads near navigation or clickable elements

**Risk**: CRITICAL — applying too early = rejection with 2-4 week cooldown. Health niche has highest AdSense scrutiny. Installing AdSense code before approval = policy violation.
**Resource**: 1-2 weeks active + ongoing, ~5-8 AI hours/week (audit, application, placement testing)
**Plans**: TBD
**UI hint**: yes

---

### Phase 7: Infrastructure Cleanup

**Goal**: Technical debt resolved, credential management improved, monitoring robust
**Depends on**: Phase 6
**Requirements**: R-075, R-076, R-077, R-078
**Success Criteria** (what must be TRUE):

1. Defunct ping services removed from `notify-ping.py`; timeouts tuned to 5s per service
2. Scheduler logs auto-rotate at 5MB/5 rotations; basic uptime monitoring active
3. Cookie-based auth migrated to API tokens wherever platform support exists
4. `package.json` added for any Node.js dependencies (llms-worker.js and others)

**Risk**: LOW — all cleanup, no blocking issues. Deliberately deferred as lowest-priority work.
**Resource**: 1 week, ~5-6 AI hours/week (script refactoring, cleanup)
**Plans**: TBD
**UI hint**: no

---

## Progress

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 0. Foundation | 0/1 | Planning | - |
| 1. Automation Fix | 5/6 | In Progress|  |
| 2. Content Engine | 0/0 | Not started | - |
| 3. Indexing & SEO | 0/0 | Not started | - |
| 4. Traffic Distribution | 0/0 | Not started | - |
| 5. Analytics & Monitoring | 0/0 | Not started | - |
| 6. AdSense & Monetization | 0/0 | Not started | - |
| 7. Infrastructure Cleanup | 0/0 | Not started | - |
