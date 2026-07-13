# Google Cloud Platform — APIs

## Project

| Parameter | Value |
|-----------|-------|
| Project ID | `ayurshakti-501603` |
| Project Number | `641160040343` |
| Owner Email | `contact@ayurshakti.shop` |

## Enabled APIs

| # | API | Status | Purpose |
|---|-----|--------|---------|
| 1 | API Keys API | ✅ ENABLED | Create/restrict/rotate API keys programmatically |
| 2 | Blogger API v3 | ✅ ENABLED | CRUD posts, pages, comments |
| 3 | Google Analytics Data API | ✅ ENABLED | Traffic analytics, user behavior |
| 4 | Google Search Console API | ✅ ENABLED | Keyword research, SEO performance |
| 5 | PageSpeed Insights API | ✅ ENABLED | Site speed monitoring, Lighthouse scores |
| 6 | Web Search Indexing API | ✅ ENABLED | Instant Google indexing on new/scheduled posts |

---

## 1. API Keys API

| Field | Value |
|-------|-------|
| **Full Name** | Google API Keys API |
| **Base URL** | `https://apikeys.googleapis.com/v2/` |
| **Auth** | OAuth 2.0 (cannot use API key to manage API keys) |
| **Scope** | `https://www.googleapis.com/auth/cloud-platform` |
| **Daily Quota** | N/A (part of GCP generic quotas) |
| **Rate Limit** | 60 req/min per project |
| **Use Case** | Create new restricted keys, rotate old keys, list all keys |

### T&C / Restrictions
- API keys must be **restricted** (by HTTP referrer, IP, or API) before production use
- Unrestricted keys are a **security risk** — anyone with the key can call the API
- Use **API restrictions** to limit which APIs a key can call
- Use **HTTP referrer restrictions** for browser-side keys (e.g. `*.ayurshakti.shop/*`)
- Use **IP restrictions** for server-side keys (e.g. server's public IP or `127.0.0.1` for local)

### Example: List API Keys

```bash
curl -X GET "https://apikeys.googleapis.com/v2/projects/ayurshakti-501603/locations/global/keys" \
  -H "Authorization: Bearer {ACCESS_TOKEN}"
```

### Our Keys

| Key Name | Key Value | Restricted To | Used For |
|----------|-----------|---------------|----------|
| Blogger API Key | `YOUR_BLOGGER_API_KEY` (see `secrets/`) | Blogger API v3 + HTTP referrer `*.ayurshakti.shop/*` | Read-only blog data (slider, posts) |
| Blogger API Key (old) | `OLD_KEY_UNRESTRICTED` (see `secrets/` — **REVOKED**) | ❌ Unrestricted — **TO DELETE** | Legacy |

---

## 2. Blogger API v3

| Field | Value |
|-------|-------|
| **Full Name** | Blogger API v3 |
| **Base URL** | `https://www.googleapis.com/blogger/v3/` |
| **Auth (Read)** | API Key (public data only) |
| **Auth (Write)** | OAuth 2.0 (refresh token) or Service Account (if invited) |
| **Scope** | `https://www.googleapis.com/auth/blogger` |
| **Daily Quota** | 10,000 requests/day (free) |
| **Rate Limit** | 100 req / 100 sec per user |
| **Use Case** | Create, read, update, delete posts, pages, comments |

### T&C / Restrictions
- Content must comply with Google's Terms of Service (no spam, no illegal content)
- API key can only **read public content** — no private posts
- OAuth required for **write operations** (create/update/delete)
- Service Account needs to be **invited as blog author** before it can write
- Rate limits apply per user — exceeding returns `403` with `rateLimitExceeded`
- Respect `Retry-After` headers on 429/403 responses
- Blog content must adhere to Blogger Content Policy

### Local Reference
Full CRUD docs, endpoints, Python examples → [`docs/04-blogger-api.md`](04-blogger-api.md)

---

## 3. Google Analytics Data API

| Field | Value |
|-------|-------|
| **Full Name** | Google Analytics Data API (GA4) |
| **Base URL** | `https://analyticsdata.googleapis.com/v1beta/` |
| **Auth** | OAuth 2.0 or Service Account |
| **Scope** | `https://www.googleapis.com/auth/analytics.readonly` |
| **Daily Quota** | 200,000 requests/day (free) |
| **Rate Limit** | 60 req/min per property per project |
| **Use Case** | Pull active users, page views, sessions, traffic sources per article |

### T&C / Restrictions
- Data can be exported but **cannot be re-sold** or shared with third parties
- Must maintain Google Analytics **privacy policy** disclosure on site
- Cannot use data to identify individual users (aggregate only)
- Service Account needs **Viewer role** in GA4 property
- Minimum reporting interval: 1 hour (real-time limited)

### Local Reference
Full docs, endpoints, Python examples → [`docs/05-analytics-seo.md`](05-analytics-seo.md)

---

## 4. Google Search Console API

| Field | Value |
|-------|-------|
| **Full Name** | Google Search Console API |
| **Base URL** | `https://www.googleapis.com/webmasters/v3/` |
| **Auth** | OAuth 2.0 or Service Account |
| **Scope** | `https://www.googleapis.com/auth/webmasters.readonly` |
| **Daily Quota** | 2,000 queries/day (free) |
| **Rate Limit** | 1 query/sec per site |
| **Use Case** | Track keyword rankings, clicks, impressions, average position |

### T&C / Restrictions
- You can only access **verified sites** under your Search Console account
- Service Account needs to be added as **Full User** or **Restricted User** in GSC
- Query data is **sampled** for large datasets (>5,000 rows per day)
- Cannot access historical data beyond **16 months**
- Rate limit is **per site** — separate queries to different sites don't conflict
- Data is **not real-time** — typically 2-3 day delay

### Local Reference
Full docs, endpoints, Python examples → [`docs/05-analytics-seo.md`](05-analytics-seo.md)

---

## 5. PageSpeed Insights API

| Field | Value |
|-------|-------|
| **Full Name** | PageSpeed Insights API |
| **Base URL** | `https://pagespeedonline.googleapis.com/v5/` |
| **Auth** | API Key only (no OAuth needed) |
| **Scope** | N/A (uses API Key) |
| **Daily Quota** | 25,000 requests/day (free) |
| **Rate Limit** | 240 req/min |
| **Use Case** | Weekly Lighthouse audits — performance, accessibility, SEO, best practices |

### T&C / Restrictions
- Can only audit URLs you **own or have permission** to test
- Data is cached for **30 seconds** for same URL — repeated calls within 30s return same result
- Strategy options: `desktop` or `mobile` (default: mobile)
- Response includes **Lighthouse scores** (0-100) and **lab data** (FCP, LCP, TTI, TBT, CLS)
- Free tier is sufficient for single-site monitoring (25k/day = one audit every ~3.5 seconds)
- No need for OAuth — just pass API key as query parameter

### Endpoint

```
GET https://pagespeedonline.googleapis.com/v5/runPagespeed
  ?url=https://www.ayurshakti.shop/
  &strategy=mobile
  &key=YOUR_BLOGGER_API_KEY  # see secrets/
```

### Response Fields

```json
{
  "lighthouseResult": {
    "categories": {
      "performance": {"score": 0.85},
      "accessibility": {"score": 0.92},
      "best-practices": {"score": 0.90},
      "seo": {"score": 0.95}
    },
    "audits": {
      "largest-contentful-paint": {"numericValue": 2500},
      "total-blocking-time": {"numericValue": 150},
      "cumulative-layout-shift": {"numericValue": 0.05}
    }
  }
}
```

### Quota Monitoring

In GCP Console → `APIs & Services → Quotas` → search `PageSpeed Insights API`

---

## 6. Web Search Indexing API

| Field | Value |
|-------|-------|
| **Full Name** | Web Search Indexing API |
| **Base URL** | `https://indexing.googleapis.com/v3/` |
| **Auth** | OAuth or Service Account (requires Search Console ownership) |
| **Scope** | `https://www.googleapis.com/auth/indexing` |
| **Daily Quota** | 200 URL notifications/day (free) |
| **Rate Limit** | 1 req/sec (burst: 5/sec) |
| **Use Case** | Notify Google immediately when new article is published/scheduled |

### T&C / Restrictions
- **CRITICAL:** You can only submit URLs for **sites you own/verified** in Google Search Console
- Only submit **actual, accessible URLs** — submitting non-existent pages gets your quota cut
- Do **not** submit duplicate URLs or spam — Google can **revoke access** permanently
- Two notification types:
  - `URL_UPDATED` — New or updated content (use for new articles)
  - `URL_DELETED` — Removed content
- Processing is **not instant** — Google puts in crawl queue, usually within hours
- Quota is **shared across all URLs** for the site — 200/day total
- Must use **Service Account** (recommended) or OAuth — API Key does NOT work

### Auth Setup (Service Account)

```python
import google.auth
from google.auth.transport.requests import Request
from google.oauth2 import service_account

SCOPES = ["https://www.googleapis.com/auth/indexing"]
creds = service_account.Credentials.from_service_account_file(
    "secrets/ayurshakti-501603-a1a6ff0396df.json", scopes=SCOPES)
creds.refresh(Request())
```

**Important:** Service Account email (`blogger-service-account@...`) must be added as **Owner** in Search Console for the site property `sc-domain:ayurshakti.shop`

### Endpoint

```
POST https://indexing.googleapis.com/v3/urlNotifications:publish
Authorization: Bearer {ACCESS_TOKEN}
Content-Type: application/json

{
  "url": "https://www.ayurshakti.shop/2026/07/article-name.html",
  "type": "URL_UPDATED"
}
```

### Batch Check Status

```
GET https://indexing.googleapis.com/v3/urlNotifications/metadata?url=https://www.ayurshakti.shop/2026/07/article-name.html
```

### Integration with Scheduler

After every scheduled/published post, call Indexing API automatically:
```
Scheduler runs → Blogge API (create post) → SUCESS → Indexing API (notify URL)
```

### Quota Monitoring

- Check remaining quota: `Quota Check` tab in GCP Console → `Web Search Indexing API`
- Track usage in `data/tracking/indexing-log.json`
- 200/day = 100 articles/day × 2 calls (create + update) sufficient for current scale

---

## OAuth 2.0 Client

| Parameter | Value |
|-----------|-------|
| Client ID | `YOUR_CLIENT_ID` (see `secrets/client_secret_*.json`) |
| Client Secret | `YOUR_CLIENT_SECRET` (see `secrets/client_secret_*.json`) |
| Auth URI | `https://accounts.google.com/o/oauth2/auth` |
| Token URI | `https://oauth2.googleapis.com/token` |
| Redirect URIs | `http://localhost:8080` |
| File | `secrets/client_secret_641160040343-....json` |
| Consent Screen | Testing mode (vle.bhati@gmail.com = test user) |

> To regenerate refresh token, see `docs/04-blogger-api.md`

## Quota Summary Table

| API | Daily Free Quota | Rate Limit | Auth Method | Cost |
|-----|:----------------:|:----------:|:-----------:|:----:|
| API Keys API | N/A | 60 req/min | OAuth | Free |
| Blogger API v3 | 10,000 req/day | 100 req/100s | Key / OAuth | Free |
| Analytics Data API | 200,000 req/day | 60 req/min | OAuth / SA | Free |
| Search Console API | 2,000 queries/day | 1 qps | OAuth / SA | Free |
| PageSpeed Insights API | 25,000 req/day | 240 req/min | API Key | Free |
| Web Search Indexing API | 200 URLs/day | 1 req/s | OAuth / SA | Free |

> All quotas reset at **midnight Pacific Time**. Overages return `429 Too Many Requests`.

## Google T&C — Common Rules Across All APIs

1. **Attribution:** APIs are provided "as is" — no uptime SLA for free tier
2. **No Re-Selling:** Data obtained via APIs cannot be re-sold or redistributed
3. **Rate Limits:** Must implement exponential backoff on `429` / `503` responses
4. **Proper Use:** Only access data you have permission to access
5. **Security:** API keys must be restricted. OAuth tokens must not be hardcoded
6. **Content Policy:** Blog content must follow Google's content policies (no spam, no deceptive content)
7. **Quota Monitoring:** Unexpected quota consumption must be investigated immediately
