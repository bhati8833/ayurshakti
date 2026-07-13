# Analytics & SEO — ayurshakti.shop

> **OpenCode Required Skills:**
> Before executing tasks in this document, load the following skills from the OpenCode library (Home Directory):
> - `seo-keyword-strategist`
> - `seo-aeo-keyword-research`
> - `competitive-landscape`

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

**Measurement Protocol (server-side events):**
```bash
curl -X POST "https://www.google-analytics.com/mp/collect?measurement_id=G-1KKZFZB7ML&api_secret=YOUR_MP_SECRET" \
  -d '{"client_id":"123.456","events":[{"name":"page_view","params":{"page_title":"Home","page_location":"/"}}]}'
```

## Google Search Console

| Parameter | Value |
|-----------|-------|
| Site | `sc-domain:ayurshakti.shop` (domain property) |
| Service Account Access | ✅ `siteFullUser` |
| Data Status | No data yet (new site) |

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

## Service Account Token (for above APIs)

Use `secrets/ayurshakti-501603-a1a6ff0396df.json` to generate JWT-based tokens:

```python
import json, time, base64, urllib.request
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding

with open("secrets/ayurshakti-501603-a1a6ff0396df.json") as f:
    data = json.load(f)
key = serialization.load_pem_private_key(data["private_key"].encode(), password=None)

now = int(time.time())
claim = json.dumps({"iss": data["client_email"],
    "scope": "https://www.googleapis.com/auth/analytics.readonly https://www.googleapis.com/auth/webmasters",
    "aud": "https://oauth2.googleapis.com/token", "exp": now + 3600, "iat": now})
header = base64.urlsafe_b64encode(json.dumps({"alg":"RS256","typ":"JWT"}).encode()).rstrip(b"=").decode()
payload = base64.urlsafe_b64encode(claim.encode()).rstrip(b"=").decode()
unsigned = f"{header}.{payload}"
sig = base64.urlsafe_b64encode(key.sign(unsigned.encode(), padding.PKCS1v15(), hashes.SHA256())).rstrip(b"=").decode()
jwt = f"{unsigned}.{sig}"

req = urllib.request.Request("https://oauth2.googleapis.com/token",
    data=urllib.parse.urlencode({"grant_type":"urn:ietf:params:oauth:grant-type:jwt-bearer","assertion":jwt}).encode(),
    headers={"Content-Type":"application/x-www-form-urlencoded"})
token = json.loads(urllib.request.urlopen(req).read())["access_token"]

---

## PageSpeed Insights API

| Field | Value |
|-------|-------|
| **Base URL** | `https://pagespeedonline.googleapis.com/v5/runPagespeed` |
| **Auth** | API Key only (querystring) |
| **Quota** | 25,000 req/day free |
| **Rate Limit** | 240 req/min |

### Usage — Weekly Speed Audit

```bash
curl "https://pagespeedonline.googleapis.com/v5/runPagespeed?url=https://www.ayurshakti.shop/&strategy=mobile&key=YOUR_BLOGGER_API_KEY"
```

### Python Function

```python
import requests

def check_speed(url, strategy="mobile"):
    r = requests.get("https://pagespeedonline.googleapis.com/v5/runPagespeed", params={
        "url": url,
        "strategy": strategy,
        "key": "YOUR_BLOGGER_API_KEY"  # see secrets/
    })
    data = r.json()
    cats = data["lighthouseResult"]["categories"]
    return {
        "url": url,
        "performance": int(cats["performance"]["score"] * 100),
        "accessibility": int(cats["accessibility"]["score"] * 100),
        "seo": int(cats["seo"]["score"] * 100),
        "best_practices": int(cats["best-practices"]["score"] * 100),
    }
```

### Threshold Alerts

| Score | Label | Action |
|:-----:|-------|--------|
| 90-100 | ✅ Fast | No action needed |
| 50-89 | ⚠️ Needs Work | Investigate LCP/TBT/CLS |
| 0-49 | ❌ Slow | Optimize images, JS, fonts |

---

## Web Search Indexing API

| Field | Value |
|-------|-------|
| **Base URL** | `https://indexing.googleapis.com/v3/urlNotifications:publish` |
| **Auth** | OAuth or Service Account (API Key NOT supported) |
| **Scope** | `https://www.googleapis.com/auth/indexing` |
| **Quota** | 200 URLs/day free |
| **Rate Limit** | 1 req/sec (burst: 5/sec) |

### Purpose

Jab bhi naya article schedule/publish ho, Google ko immediately notify karo. Isse:

- Naye articles **hours mein index** ho jate hain (instead of weeks)
- Google ko signal milta hai "yeh site active hai"
- Better crawl budget for ayurshakti.shop

### Usage — Notify Google on New Post

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

### Integration — After Scheduler Runs

```python
# In schedule-posts.py, after successful post:
if result.get("id"):
    post_url = f"https://www.ayurshakti.shop/{result.get('url') or result['id']}"
    notify_index(post_url)
    log(f"🔔 Indexing API notified for: {post_url}")
```

### Error Handling

| HTTP | Meaning | Action |
|:----:|---------|--------|
| 200 | Success | Log `notified` |
| 429 | Rate limited | Wait + retry with backoff |
| 403 | Not verified in GSC | Check Search Console ownership |
| 400 | Invalid URL | Check URL format (no trailing slash issues) |

> See [`docs/03-gcp-apis.md`](03-gcp-apis.md) for full quota + T&C

---

## Email UTM Tracking

Email marketing campaigns ke liye UTM params auto-tagged hote hain. Apps Script (`docs/15-email-marketing-system.md`) se bheje gaye emails mein yeh tracking hoti hai:

| Campaign | utm_source | utm_medium | utm_campaign | utm_content |
|----------|------------|------------|--------------|-------------|
| Welcome | email | email | welcome | lead-magnet |
| Newsletter | email | newsletter | weekly-{YYYY-MM-DD} | article-{1..3} |
| Custom | email | broadcast | {custom_name} | {content_name} |

GA4 mein yeh traffic "email" source ke under ayega. Dashboard check karo for click-through rates.

---

## Bing Webmaster Tools API

| Field | Value |
|-------|-------|
| **Base URL** | `https://ssl.bing.com/webmaster/api.svc/json/SubmitUrlbatch` |
| **Auth** | API Key (`secrets/bing-client-credentials.json`) |
| **Requirement**| **MANDATORY SITEMAP SUBMISSION** due to June 2026 Bing Index Update |

### Usage — Auto-Submit Sitemap & URLs

**MANDATORY:** After every new post publication or update, the sitemap must be submitted to Bing to ensure rapid indexing.

```bash
# Submit sitemap to Bing
python3 scripts/bing-sitemap-submit.py

# Submit individual URL via IndexNow
python3 scripts/bing-sitemap-submit.py --url https://www.ayurshakti.shop/your-new-post
```

---

## Yandex Webmaster

| Field | Value |
|-------|-------|
| **Verification** | Meta tag: `<meta name="yandex-verification" content="a4f4553babbc2e32" />` |
| **API Key** | **Not provided** — Yandex does not offer API key for sitemap submission |
| **Sitemap** | `https://www.ayurshakti.shop/sitemap.xml` (submit manually in Webmaster UI) |
| **IndexNow** | Supported via `api.indexnow.org` — uses Bing API key |
| **Documentation** | https://yandex.com/support/webmaster/en/service/info.html |

### Key Points

**No API Access**: Yandex Webmaster does **not** provide programmatic API access for sitemap/URL submission. Verification is done via:
1. Meta tag in HTML `<head>` (preferred for Blogger)
2. DNS TXT record
3. HTML file upload
4. WHOIS email

**IndexNow Support**: Yandex supports IndexNow protocol. The existing `scripts/bing-sitemap-submit.py` submits to `api.indexnow.org` which covers **Bing, Yandex, and Seznam** simultaneously using the Bing API key.

**Manual Sitemap Submission**: After verification in Yandex Webmaster UI:
1. Go to Indexing → Sitemap files
2. Add `https://www.ayurshakti.shop/sitemap.xml`
3. Submit

---

## Seznam Webmaster

| Field | Value |
|-------|-------|
| **Verification** | Meta tag: `<meta name="seznam-wmt" content="8BYbml7huX76KfxLSl4lpsZlA7atVBfI" />` |
| **API Key** | stored in `secrets/seznam-api-key.txt` (do not commit the key) |
| **API Base URL** | `https://reporter.seznam.cz/wm/api` |
| **API Docs** | https://reporter.seznam.cz/wm/web/dokumentace |
| **Sitemap** | `https://www.ayurshakti.shop/sitemap.xml` |
| **IndexNow** | Supported via `api.indexnow.org` — uses Bing API key |

### API Endpoints (Bearer token + session cookie auth)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/web` | GET | Site overview (counts by category) |
| `/web/documents` | GET | Page counts + sample URLs (max 1000) |
| `/web/documents-history` | GET | Historical daily counts |
| `/web/document` | GET | Specific URL details |
| `/web/document/reindex` | POST | Request reindex (write key, 500/day) |
| `/web/database-info` | GET | Database version |
| `/sites` | GET | List configured domains |

### Rate Limits

| Limit | Value |
|-------|-------|
| Requests/second | 5 |
| Requests/minute | 100 |
| Reindex/day | 500 |

### Usage

```bash
# Get site status
python3 scripts/seznam-api.py status

# Get indexed pages sample
python3 scripts/seznam-api.py documents --limit 100

# Get historical data (30 days)
python3 scripts/seznam-api.py history --days 30

# Get specific URL info
python3 scripts/seznam-api.py document --document https://www.ayurshakti.shop/some-post

# Request reindex (requires write-enabled key)
python3 scripts/seznam-api.py reindex --document https://www.ayurshakti.shop/some-post

# List all configured sites
python3 scripts/seznam-api.py sites
```

### Important Notes

**Verification**: Meta tag must be in static HTML source (not injected via JS). Blogger theme XML is the correct place.

**API Authentication**: The API key is stored in `secrets/seznam-api-key.txt` (generated in Seznam Webmaster UI → API → Access Keys). Requires **session cookie** from login at `https://reporter.seznam.cz/wm/` — Bearer token alone is not sufficient.

**IndexNow**: Seznam supports IndexNow protocol. The existing `scripts/bing-sitemap-submit.py` submits to `api.indexnow.org` which covers Bing, Yandex, and Seznam simultaneously.

### IndexNow Protocol (Seznam Official)

Seznam supports IndexNow at `https://search.seznam.cz/indexnow`:

**GET (single URL)**:
```
GET https://search.seznam.cz/indexnow?url=<URL>&key=<KEY>&keyLocation=<KEY_URL>
```

**POST (bulk - max 10,000 URLs)**:
```json
POST https://search.seznam.cz/indexnow
Content-Type: application/json
{
  "host": "www.ayurshakti.shop",
  "key": "<INDEXNOW_KEY>",
  "keyLocation": "https://www.ayurshakti.shop/<KEY>.txt",
  "urlList": ["https://www.ayurshakti.shop/url1", "..."]
}
```

**Key Requirements**:
- UTF-8 encoding
- 8-128 characters, alphanumeric + hyphen
- Plain text file (no HTML/BOM)
- Place at root: `https://www.ayurshakti.shop/<KEY>.txt`

**Response Codes**: 200=OK, 403=Bad key, 422=Invalid params, 429=Rate limited
```
