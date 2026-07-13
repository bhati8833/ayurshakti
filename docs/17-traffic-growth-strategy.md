# Traffic Growth Strategy — ayurshakti.shop

> **Status snapshot (pulled 2026-07-13, GA4 last 30d):**
> 42 users · 57 sessions · 475 pageviews · 0% returning · GSC 0 impressions/clicks.
> The site is live but **not yet indexed/ranking** — that is the #1 bottleneck.

This document explains what the two Google reports mean, how the API pulls them
(see `scripts/analytics-report.py`), and the prioritized strategy to grow traffic
from ~40 users/month toward sustained organic growth.

---

## 1. What the two reports actually are

### Google Analytics 4 (GA4) — *what users do on the site*
GA4 measures **on-site behavior**. The API (`analyticsdata.googleapis.com/v1beta`)
returns metrics per date:

| Metric | Meaning | Our 30d |
|--------|---------|---------|
| `activeUsers` / `totalUsers` | Unique people who visited | 42 |
| `newUsers` | First-time visitors | 42 (100%) |
| `sessions` | Visit count (user can have many) | 57 |
| `screenPageViews` | Total page loads | 475 |
| `averageSessionDuration` | Avg time per visit | 474s (~8 min) |
| `bounceRate` | Single-page-no-interaction sessions | 0.7%* |

\* A 0.7% bounce is not realistic for human traffic — it usually means
measurement is catching bot/self/automation hits or the engagement signal is
misconfigured. **Flag for audit** (see §5).

### Google Search Console (GSC) — *how Google sees the site*
GSC measures **search visibility**. The API (`webmasters/v3/.../searchAnalytics`)
returns per-query performance:

| Field | Meaning | Our 30d |
|-------|---------|---------|
| `impressions` | Times a page showed in Google results | 0 |
| `clicks` | Times a result was clicked | 0 |
| `ctr` | clicks / impressions | n/a |
| `position` | Avg ranking | n/a |

**Reading the two together:** GA4 says people who land stay (good engagement),
GSC says nobody is *finding* us via search (no index/ranking). Fix discovery
first; engagement is already a strength to preserve.

---

## 2. The bottleneck (do this before anything else)

GSC = 0 impressions means Google has not indexed the site meaningfully.
No amount of content helps until the site is in the index.

**Action — indexing foundation (Week 1):**
1. Confirm `sc-domain:ayurshakti.shop` ownership in GSC (DNS verified via Cloudflare — likely OK).
2. Submit `https://www.ayurshakti.shop/sitemap.xml` in GSC → Sitemaps.
3. Wire the **Indexing API** into publish flow so every new post pings Google
   (`docs/05-analytics-seo.md` §Web Search Indexing API). Add a call in
   `scripts/schedule-posts.py` after a successful post (already half-planned there).
4. Keep `scripts/bing-sitemap-submit.py` running post-publish (covers Bing +
   Yandex + Seznam via IndexNow).
5. Verify the Blogger theme serves real `<head>` meta tags (Seznam/Yandex need
   static HTML, not JS-injected).

**Success metric:** GSC impressions climb from 0 → 100+ within 2–3 weeks.

---

## 3. Content engine (the compound growth lever)

The repo already has a content pipeline (topic research → write → approval queue
→ scheduler). Tune it for *search demand*, not just volume.

**Action — search-first content (ongoing):**
- Target **long-tail, low-competition** Ayurveda/Hindi queries (e.g. "giloy
  kaise khaye", "pet ke liye ashwagandha"). Use `docs/08-topic-research-rule.md`.
- Publish in **both English + Hinglish** — Hindi queries have less competition
  and the site is already bilingual.
- Build **topical clusters**: 1 pillar post + 3–4 supporting posts linking to it.
  Internal linking is the cheapest ranking signal you control.
- Keep the existing ~2-posts/12h auto-schedule; consistency signals "active site"
  to Google (improves crawl budget).

**Success metric:** 30+ indexed posts, avg position < 50 for target queries.

---

## 4. Technical SEO (don't lose the rankings you earn)

**Action (Week 2–3):**
- Run `pagespeedonline.googleapis.com/v5/runPagespeed` on mobile for top pages.
  Target Performance ≥ 90. Blogger + Cloudflare usually passes; optimize images
  (the repo already generates/resizes blog images — keep it strict).
- Fix CWV: LCP (hero image lazy/resize), CLS (set image dimensions), TBT (defer
  third-party scripts).
- Add `robots.txt` + XML sitemap to Cloudflare cache; ensure no `noindex` leaks.

---

## 5. Measurement & the bounce-rate flag

The 0.7% bounce is a measurement red flag. Before trusting any GA4 number:
- Check `secrets/ga4-mp-secret.txt` Measurement Protocol events aren't double-
  counting or firing on non-interactive hits.
- Filter internal/owner IPs via a GA4 **traffic filter** (data-stream settings).
- Confirm the GA4 tag is on every Blogger page (theme `<head>`).

**Weekly ritual** (automate it):
```bash
python3 scripts/analytics-report.py --days 7 --save     # track trend
python3 scripts/analytics-report.py --days 7 --strategy # print recommendations
```
Watch the columns move: impressions 0→↑, clicks 0→↑, returning users 0%→↑.

---

## 6. Distribution (amplify, don't rely on)

Organic search is the goal, but the existing social auto-posters buy time and
backlinks while SEO ramps:
- `scripts/social-post.py` → X, Pinterest, Bluesky, Medium, Moltbook.
- Pinterest + Medium are surprisingly strong organic referrers for health content.
- Every shared post should carry UTM tags (already defined in `docs/05-analytics-seo.md`
  §Email UTM Tracking) so GA4 shows which channel drives *real* users.

---

## 7. Prioritized action plan

| Priority | Task | Owner script / doc | Target |
|----------|------|--------------------|--------|
| P0 | Confirm GSC ownership + submit sitemap | GSC UI | impressions > 0 |
| P0 | Indexing API on every publish | `schedule-posts.py` + `05-analytics-seo.md` | index in hours |
| P1 | Audit GA4 bounce (filter bots/owner) | `ga4-mp-secret.txt`, GA4 UI | realistic bounce |
| P1 | 30 long-tail bilingual posts (clusters) | topic + write pipeline | 30 indexed |
| P2 | Mobile PageSpeed ≥ 90 on top pages | PageSpeed API | perf ≥ 90 |
| P2 | Internal linking across clusters | writing rule | lower position |
| P3 | Weekly `--strategy` report review | `analytics-report.py` | trend tracking |

**Bottom line:** You already have the API plumbing and the content engine. The
gap is **indexing + measurement hygiene**. Close P0/P1 this week and traffic
becomes a content-volume function, not a mystery.
