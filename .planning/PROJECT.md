# AyurShakti — ayurshakti.shop

## What This Is

An Ayurvedic health and pet wellness content blog hosted on Google Blogger, monetized via AdSense. Content is produced at high volume (5-7 articles/week) using AI-assisted writing, auto-scheduled via Python scripts, and distributed across multiple traffic channels — Google Search, Bing, social media (Bluesky, X/Twitter, Pinterest, LinkedIn, Medium, Quora, Reddit), and AI crawler ecosystems.

## Core Value

Generate consistent AdSense revenue through high-traffic, multi-source organic content distribution.

## Business Context

- **Customer**: Health-conscious readers interested in Ayurveda, natural remedies, and holistic pet care (India, US, UK, Canada, Australia)
- **Revenue model**: Google AdSense display ads
- **Success metric**: Monthly AdSense revenue (traffic → RPM → earnings)
- **Strategy notes**: Zero paid tools — all infrastructure uses free tiers (Blogger, Cloudflare, GitHub Pages, free APIs)

## Requirements

### Validated

Existing infrastructure and capabilities already built:

- ✓ Google Blogger CMS with custom domain (ayurshakti.shop) — existing
- ✓ Cloudflare DNS + CDN + Pages (resources.ayurshakti.shop for images/assets) — existing
- ✓ Cloudflare Email Routing (contact@ → Gmail) — existing
- ✓ Python automation scripts: scheduler, social poster, ping notifier, PubMed fetcher — existing
- ✓ Social media API integrations: Bluesky, X/Twitter (OAuth 1.0a), Pinterest (v5) — existing
- ✓ Social media cookies: Reddit, Quora, Medium — existing
- ✓ Google APIs integrated: Blogger v3, GA4, Search Console, PageSpeed, Indexing — existing
- ✓ llms.txt Cloudflare Worker for AI crawler access — existing
- ✓ Email marketing via Google Sheets + Apps Script — existing
- ✓ JSON-based tracking system (article-registry, api-usage, tasks) — existing
- ✓ PubMed citation integration for evidence-based content — existing
- ✓ Blogger theme with schema markup (fixed OG tags, JSON-LD) — existing

### Active

- [ ] **TRAFF-01**: Multi-platform indexing — Google Search Console, Bing Webmaster, Yandex, IndexNow properly configured and verified
- [ ] **TRAFF-02**: Fix auto-scheduler (schedule-posts.py) — resolve "Invalid post id" 400 error, get automated publishing working
- [ ] **TRAFF-03**: Clear social posting backlog — distribute all existing published articles to Bluesky, X/Twitter, Pinterest
- [ ] **TRAFF-04**: Set up automated social distribution pipeline — every new publish auto-posts to all platforms
- [ ] **TRAFF-05**: AI-friendly optimization — llms.txt, GPTBot/ClaudeBot/Perplexity crawler indexing, structured data for AI consumption
- [ ] **TRAFF-06**: High-volume content pipeline — research → write → approve → schedule (5-7 articles/week) using AI agent automation
- [ ] **TRAFF-07**: Backlink strategy execution — Quora, Reddit, Medium, Pinterest automated backlink generation
- [ ] **TRAFF-08**: Multi-source traffic analytics — track traffic sources (organic, social, AI, direct) and optimize channel mix
- [ ] **EARN-01**: Apply for Google AdSense — after sufficient traffic and quality content established
- [ ] **EARN-02**: Ad placement optimization — test ad positions for max RPM without harming UX
- [ ] **INFRA-01**: Fix technical debt in scripts — extract duplicated OAuth to shared lib, add requirements.txt, add package.json
- [ ] **INFRA-02**: Ping services cleanup — remove defunct services, add timeout tuning, log real failures
- [ ] **INFRA-03**: Log rotation and monitoring — auto-rotate scheduler logs, add basic uptime monitoring

### Out of Scope

- Paid tools or services — everything must be free/open-source
- Custom CMS migration — Blogger is the permanent platform
- Mobile app development
- Paid advertising (Google Ads, Facebook Ads)
- Video content creation (YouTube)

## Context

- **Domain**: New domain, no AdSense application yet
- **Traffic**: Minimal/unknown — analytics need verification
- **Existing articles**: 11 published, ~22 drafts ready to write
- **Automation status**: Scripts exist but have known bugs (scheduler 400 error, social backlog of 10 articles)
- **Infrastructure**: All free tiers — Blogger unlimited posts, Cloudflare free plan, GitHub free, free APIs only
- **AI agent**: AI agent handles content writing, script fixes, and automation orchestration
- **Competition**: Health/wellness niche is competitive but high RPM for AdSense

## Constraints

- **Budget**: Zero — only domain registration cost. No paid tools, services, or APIs
- **Platform**: Google Blogger — limited compared to self-hosted CMS (no plugins, limited customization)
- **API Limits**: Blogger API 10k req/day, GA4 200k req/day, free tier limits on all services
- **Time**: AI agent-driven — user reviews and approves, AI does writing and automation
- **Compliance**: Health content needs disclaimers, no medical claims, AdSense policies must be followed

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Zero paid tools | Minimize costs, maximize ROI | — Pending |
| Blogger + Cloudflare only | Free, reliable, no maintenance | ✓ Good |
| AI agent writes + automates | Scale content without hiring writers | — Pending |
| Multi-source traffic strategy | Don't depend on one source (Google only) | — Pending |
| Fix automation before scaling | Broken scheduler blocks everything | — Pending |

## Evolution

This document evolves at phase transitions and milestone boundaries.

**After each phase transition** (via `/gsd-transition`):
1. Requirements invalidated? → Move to Out of Scope with reason
2. Requirements validated? → Move to Validated with phase reference
3. New requirements emerged? → Add to Active
4. Decisions to log? → Add to Key Decisions
5. "What This Is" still accurate? → Update if drifted

---
*Last updated: 2026-07-11 after initialization*
