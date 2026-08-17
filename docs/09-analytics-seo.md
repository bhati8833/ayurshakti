# Analytics & SEO — ayurshakti.shop

## Google Analytics (GA4)

| Parameter | Value |
|-----------|-------|
| Property Name | `san-hini-1` |
| Property ID | `533609055` |
| Measurement ID | `G-1KKZFZB7ML` |
| Measurement Protocol Secret | `YOUR_MP_SECRET` (see `secrets/ga4-mp-secret.txt`) |
| Service Account Access | ✅ Viewer |
| Timezone | Asia/Calcutta |
| Currency | INR |

**GA4 Report Example:**
```bash
curl -X POST "https://analyticsdata.googleapis.com/v1beta/properties/533609055:runReport" \
  -H "Authorization: Bearer {TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "dateRanges":[{"startDate":"2026-07-05","endDate":"2026-07-06"}],
    "metrics":[{"name":"activeUsers"},{"name":"screenPageViews"},{"name":"sessions"}]
  }'
```

---

## Google Search Console

| Parameter | Value |
|-----------|-------|
| Site | `sc-domain:ayurshakti.shop` (domain property) |
| Service Account Access | ✅ `siteFullUser` |
| Data Status | Active |

**Keyword Query:**
```bash
curl -X POST "https://www.googleapis.com/webmasters/v3/sites/sc-domain%3Aayurshakti.shop/searchAnalytics/query" \
  -H "Authorization: Bearer {TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "startDate":"2026-07-01",
    "endDate":"2026-07-06",
    "dimensions":["query"],
    "rowLimit":10
  }'
```

---

## PageSpeed Insights API

| Field | Value |
|-------|-------|
| **Base URL** | `https://pagespeedonline.googleapis.com/v5/runPagespeed` |
| **Auth** | API Key |
| **Quota** | 25,000 req/day free |
| **Rate Limit** | 240 req/min |

```bash
curl "https://pagespeedonline.googleapis.com/v5/runPagespeed?url=https://www.ayurshakti.shop/&strategy=mobile&key=YOUR_API_KEY"
```

---

## Web Search Indexing API

| Field | Value |
|-------|-------|
| **Base URL** | `https://indexing.googleapis.com/v3/urlNotifications:publish` |
| **Auth** | OAuth or Service Account |
| **Scope** | `https://www.googleapis.com/auth/indexing` |
| **Quota** | 200 URLs/day free |

```python
from google.oauth2 import service_account
from google.auth.transport.requests import Request
import requests

SCOPES = ["https://www.googleapis.com/auth/indexing"]
creds = service_account.Credentials.from_service_account_file(
    "secrets/ayurshakti-501603-a1a6ff0396df.json", scopes=SCOPES)
creds.refresh(Request())

def notify_index(url):
    r = requests.post(
        "https://indexing.googleapis.com/v3/urlNotifications:publish",
        headers={"Authorization": f"Bearer {creds.token}"},
        json={"url": url, "type": "URL_UPDATED"}
    )
    return r.status_code == 200
```

---

## Bing Webmaster Tools & IndexNow API

```bash
# Submit sitemap to Bing
python3 scripts/bing-sitemap-submit.py

# Submit individual URL via IndexNow
python3 scripts/bing-sitemap-submit.py --url https://www.ayurshakti.shop/articles/ashwagandha-benefits
```
