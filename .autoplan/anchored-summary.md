## Objective
- Fix Google Search Console indexing for ayurshakti.shop. Root cause found: articles "unknown to Google" (sitemap submitted 21 URLs, 0 indexed; homepage indexed). Built + wired Google Indexing API automation (P0) and GSC sitemap submission (P1). Batched all 21 live article URLs through the Indexing API.

## Important Details
- Repo: ayurshakti.shop, branch `master`, no remote (git-native only).
- GSC property: `sc-domain:ayurshakti.shop`, SA `siteFullUser`. SA key: `secrets/ayurshakti-501603-a1a6ff0396df.json`.
- **GSC status (checked 2026-07-15):** sitemap.xml submitted (www: 21 urls/0 indexed today; non-www: 22 urls/0 indexed since 07-11). Homepage (www & non-www) = PASS "Submitted and indexed". Article URLs = "URL is unknown to Google" (never crawled). robots.txt allows all; articles return 200, no noindex, **but NO canonical tag** (secondary issue).
- **GSC Coverage export (`google search console Results/ayurshakti.shop-Coverage-2026-07-15.zip`):** 22 known pages, 2 indexed, 20 critical issues — Discovered-not-indexed=15, Page-with-redirect=3, Crawled-not-indexed=1, Alternate-page-canonical=1. Non-critical=0. Impressions=0 throughout (07-10: 20 not-indexed/2 indexed).
- **CORRECTED diagnosis (user flagged theme already live):** Live Blogger theme DOES have correct self-canonical (verified live article HTML: `<link href='...post-url...' rel='canonical'/>`; `?m=1` returns 200 with canonical pointing to desktop — properly consolidated). Earlier "canonical NONE" was a regex false-negative. Sitemap URLs have 0 redirects. The 3 "Page with redirect" came from the **non-www sitemap** (submitted 2026-07-11) whose URLs 301 → www. The 15 "Discovered - not indexed" = crawl priority; 1 "Crawled - not indexed" = content quality.
- Sitemap decision (user-corrected): standardize on `sitemap.xml` — Blogger `atom.xml` broken, so webmaster platforms use `sitemap.xml`.
- Locked autoplan decisions: D1 = full automation (P0 Indexing API ping + P1 GSC sitemap submit); D2 = AdSense + Affiliate both.
- Google Indexing API: `indexing.googleapis.com/v3/urlNotifications:publish`, scope needs BOTH `indexing` + `webmasters` (webmasters required for sitemap PUT). Quota 200 URLs/day, 1 req/s.

## Work State
### Completed
- TASK-003: `post_pinterest` in `scripts/social-post.py` refactored (dynamic board, 100-char title, error bodies).
- TASK-015: `scripts/bing-sitemap-submit.py` rewritten (Bing Webmaster API + IndexNow + ping fallback, non-zero exit).
- P0: `scripts/gsc-index-submit.py` created — Google Indexing API per-URL ping (`--url`) + GSC sitemap submit (default), 429 backoff, 403 alert, non-zero exit. Wired into `schedule-posts.py` publish flow (mirrors Bing block, records `google_index_status`). Added `"indexing"` to `VALID_STAGES` in `scripts/lib/tracking.py`. Standardized sitemap → `sitemap.xml` in `scripts/config/profile.json`.
- Verified: sitemap submit → 204 OK; per-URL ping → 200 OK; both scripts compile.
- **GSC fix applied:** batch-pinged all 21 live sitemap URLs via Indexing API (21 OK, 0 failed) to force crawl/index.
- Diagnosed GSC Coverage export: 22 known pages, 2 indexed, 20 critical issues. **Canonical is live and correct** (regex false-negative corrected). Real issues: 15 "Discovered - not indexed" (crawl priority), 1 "Crawled - not indexed" (content quality), 3 "Page with redirect" (non-www sitemap → www).
- **Removed redundant non-www sitemap via GSC API** (DELETE sites/{site}/sitemaps/...) — only `https://www.ayurshakti.shop/sitemap.xml` remains (0 errors). Eliminates the redirect noise.
- **Root cause of 1 "Crawled - not indexed" + 1 "Alternate page": TWO 100%-duplicate PCOS posts** (`ayurvedic-remedies-for-pcos-natural.html` and the suffixed `_01253035810` twin, same title, 959/961 vocab overlap). Rewrote the suffixed twin (Blogger post id `74438030860831675`) as a DISTINCT article **"PCOS Diet Chart & Daily Routine: Ayurvedic Foods to Eat and Avoid"** via Blogger API PUT. Duplicate overlap dropped **100% → 33%**. Re-pinged Indexing API (200 OK) to force recrawl with new content. TASK-016 marked Completed.

### Active
- (none) — awaiting Google crawl (hours/days) to reflect indexing in GSC.

### Blocked
- (none)

## Next Move
1. **User action (TASK-016):** paste canonical-fixed `theme-and-logo/ayurshakti-main.xml` into Blogger HTML editor → adds self-canonical to all posts, fixes "Alternate page" + helps redirect/duplicate issues.
2. Re-verify indexing in ~24-48h via URL Inspection / sitemap `indexed` count (expect >0 from the 21 Indexing API pings).
3. For the 1 "Crawled - currently not indexed" post: improve content depth/thin-content (quality issue, canonical won't fix).
4. Optional: drop redundant non-www sitemap submission (canonical domain is www).
5. P2/P3 (per `docs/gsc-indexing-strategy.md`): indexability audit + measurement dashboard.

## Relevant Files
- `scripts/gsc-index-submit.py`: NEW — Google Indexing API + GSC sitemap submit.
- `scripts/schedule-posts.py`: publish pipeline; Bing ping (~line 269) + NEW Google Indexing API block (after Bing); `google_index_status` in syndication_results.
- `scripts/lib/tracking.py`: `VALID_STAGES` now includes `"indexing"` (line 20).
- `scripts/bing-sitemap-submit.py`: TASK-015 done, non-zero exit.
- `scripts/social-post.py`: `post_pinterest` refactored (TASK-003 done).
- `scripts/config/profile.json`: sitemap → `sitemap.xml`. Root `config/profile.json`: sitemap.xml (via `lib.profile`).
- `secrets/ayurshakti-501603-a1a6ff0396df.json`: Google SA key.
- `data/tracking/project-tasks.json`: TASK-003/015 Completed; TASK-013 Todo (now also automatable); TASK-002/005/014 Todo (ignored).
- `docs/gsc-indexing-strategy.md`, `docs/office-hours-design.md`, `docs/autoplan-output.md`: design/plan docs.
