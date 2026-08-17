# Google Cloud Platform — APIs

## Project Summary

| Parameter | Value |
|-----------|-------|
| **Project ID** | `ayurshakti-501603` |
| **Project Number** | `641160040343` |
| **Owner Email** | `contact@ayurshakti.shop` |

---

## Enabled GCP APIs

| # | API | Status | Purpose |
|---|-----|--------|---------|
| 1 | **Web Search Indexing API** | ✅ ENABLED | Instant Google indexing on new & updated static URLs |
| 2 | **Google Search Console API** | ✅ ENABLED | Keyword performance, search queries, click tracking |
| 3 | **Google Analytics Data API (GA4)** | ✅ ENABLED | Traffic analytics, real-time pageviews, active readers |
| 4 | **PageSpeed Insights API** | ✅ ENABLED | Automated Lighthouse performance audits |
| 5 | **API Keys API** | ✅ ENABLED | Manage API keys & restrictions programmatically |

---

## 1. Web Search Indexing API

| Field | Value |
|-------|-------|
| **Full Name** | Web Search Indexing API |
| **Base URL** | `https://indexing.googleapis.com/v3/` |
| **Auth** | OAuth 2.0 or Service Account (Search Console Owner) |
| **Scope** | `https://www.googleapis.com/auth/indexing` |
| **Daily Quota** | **200 URL notifications / day** (free) |
| **Rate Limit** | 1 req/sec (burst: 5/sec) |
| **Use Case** | Notify Google immediately when new static Next.js articles are published to Firebase Hosting |

### Usage Example
```python
import google.auth
from google.auth.transport.requests import Request
from google.oauth2 import service_account
import requests

SCOPES = ["https://www.googleapis.com/auth/indexing"]
creds = service_account.Credentials.from_service_account_file(
    "secrets/ayurshakti-501603-a1a6ff0396df.json", scopes=SCOPES)
creds.refresh(Request())

url = "https://www.ayurshakti.shop/articles/ashwagandha-benefits"
response = requests.post(
    "https://indexing.googleapis.com/v3/urlNotifications:publish",
    headers={"Authorization": f"Bearer {creds.token}"},
    json={"url": url, "type": "URL_UPDATED"}
)
print("Indexing result:", response.status_code)
```

---

## 2. Google Search Console API

| Field | Value |
|-------|-------|
| **Full Name** | Google Search Console API |
| **Base URL** | `https://www.googleapis.com/webmasters/v3/` |
| **Auth** | Service Account or OAuth 2.0 |
| **Scope** | `https://www.googleapis.com/auth/webmasters.readonly` |
| **Daily Quota** | **2,000 queries / day** (free) |
| **Rate Limit** | 1 query/sec per site |
| **Use Case** | Track keyword rankings, impressions, CTR, and indexing coverage for `sc-domain:ayurshakti.shop` |

---

## 3. Google Analytics Data API (GA4)

| Field | Value |
|-------|-------|
| **Full Name** | Google Analytics Data API (GA4) |
| **Base URL** | `https://analyticsdata.googleapis.com/v1beta/` |
| **Auth** | Service Account or OAuth 2.0 |
| **Scope** | `https://www.googleapis.com/auth/analytics.readonly` |
| **Daily Quota** | **200,000 requests / day** (free) |
| **Use Case** | Fetch traffic stats, session duration, and top performing Ayurvedic articles |

---

## 4. PageSpeed Insights API

| Field | Value |
|-------|-------|
| **Full Name** | PageSpeed Insights API |
| **Base URL** | `https://pagespeedonline.googleapis.com/v5/` |
| **Auth** | API Key |
| **Daily Quota** | **25,000 requests / day** (free) |
| **Use Case** | Monitor Lighthouse Mobile & Desktop scores for Firebase Hosting deployments |

```bash
curl "https://pagespeedonline.googleapis.com/v5/runPagespeed?url=https://www.ayurshakti.shop/&strategy=mobile&key=YOUR_API_KEY"
```

---

## Quota & Reset Summary

- **Reset Time**: Quotas reset daily at midnight Pacific Time (00:00 PT).
- **Cost**: All enabled GCP APIs operate 100% within free usage tiers.
