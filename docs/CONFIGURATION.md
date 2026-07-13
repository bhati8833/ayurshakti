<!-- generated-by: gsd-doc-writer -->
# Configuration — ayurshakti.shop

Central configuration reference for the ayurshakti.shop project. All settings, credentials, and environment variables are documented here.

---

## 1. Profile Configuration

**File:** `config/profile.json`

The central profile file contains site metadata, author info, contact details, brand voice, and script paths. It is loaded by all Python scripts via `scripts/lib/profile.py`.

### Top-Level Keys

`config/profile.json` is a single JSON object with these top-level keys:

| Key | Type | Description |
|-----|------|-------------|
| `site` | object | Site metadata: name, domain, url, sitemap, llms, title, description, keywords, language, timezone, blogger_id |
| `author` | object | Author identity: name, title, bio, short_bio, photo, social links |
| `contact` | object | Public contact: email, phone, address |
| `brand` | object | Brand voice: tagline, voice, audience, topics |
| `scripts` | object | Script registry mapping logical names (`dir`, `bing_sitemap`, `social_post`, `schedule_posts`, `pubmed_cite`, `approval_queue`, `schedule_config`, etc.) to filenames under `scripts/` |

### Site

| Variable | Value | Required |
|----------|-------|----------|
| `name` | `AyurShakti` | Yes |
| `domain` | `ayurshakti.shop` | Yes |
| `url` | `https://www.ayurshakti.shop` | Yes |
| `sitemap` | `https://www.ayurshakti.shop/sitemap.xml` | Yes |
| `llms` | `https://llms.ayurshakti.shop/llms.txt` | Yes |
| `title` | `AyurShakti — Ayurvedic Health & Pet Wellness` | Yes |
| `description` | Site meta description (evidence-based Ayurveda for human & pet health) | Yes |
| `keywords` | `["ayurveda","pet health","natural remedies","herbal medicine","dog health","cat health", ...]` | Yes |
| `language` | `en` | Yes |
| `timezone` | `America/New_York` | Yes |
| `blogger_id` | `5016036252143286656` | Yes |

### Author

| Variable | Value | Required |
|----------|-------|----------|
| `name` | `Suresh Bhati` | Yes |
| `title` | `Ayurvedic Researcher & Health Writer` | Yes |
| `bio` | Full bio string | Yes |
| `social.twitter` | `https://x.com/ayurshakti_` | No |
| `social.bluesky` | `https://bsky.app/profile/ayurshakti.bsky.social` | No |
| `social.pinterest` | `https://www.pinterest.com/ayurshakti_shop/` | No |
| `social.quora` | `https://www.quora.com/profile/Ayurshakti` | No |
| `social.reddit` | `https://www.reddit.com/user/ayurshakti/` | No |
| `social.medium` | `https://medium.com/@ayurshakti` | No |
| `short_bio` | `Ayurvedic researcher sharing evidence-based natural health wisdom for humans and pets.` | No |
| `photo` | (empty) | No |

### Contact

| Variable | Value | Required |
|----------|-------|----------|
| `email` | `contact@ayurshakti.shop` | Yes |
| `phone` | (empty) | No |
| `address` | (empty) | No |

### Brand

| Variable | Value |
|----------|-------|
| `tagline` | `Ancient Wisdom for Modern Wellness` |
| `voice` | `Authoritative yet warm, evidence-based Ayurveda` |
| `audience` | `["India", "United States", "United Kingdom", "Canada", "Australia"]` |
| `topics` | `["Ayurveda", "Pet Health", "Natural Remedies", "Herbal Medicine", "Dog Care", "Cat Care"]` |

---

## 2. Environment Variables

No `.env` files are committed to the repository. The `.gitignore` excludes `.env`, `.env.local`, and `.env.production`.

All secrets and credentials are stored as individual files in the `secrets/` directory (gitignored). See **Section 3** below for the full secrets inventory.

### Per-Environment Overrides

There are **no** `.env.development`, `.env.production`, or `.env.test` files, and no `NODE_ENV`-conditional config loading in the codebase. All environment-specific behavior is controlled by the single committed `config/profile.json` plus gitignored files in `secrets/`:

- **Local / development:** scripts read `config/profile.json` and load credentials directly from `secrets/` files at runtime.
- **Production deployment:** DNS, SSL, Cloudflare Workers, Email Routing, and Bot Management (`bot_management.is_robots_txt_managed = false`) are configured entirely in the Cloudflare dashboard — not in repo files. The Blogger-hosted site serves its `robots.txt` via the `ayurshakti-robots` Cloudflare Worker (see Section 4).
- **Switching targets:** change `site.url`, `site.domain`, and `blogger_id` in `config/profile.json`, and update the corresponding `secrets/` credential files.

---

## 3. Secrets Directory

**Directory:** `secrets/` (gitignored — contains actual credential values)

The following files are expected to exist in the `secrets/` directory:

| File | Service | Contents |
|------|---------|----------|
| `ayurshakti-501603-a1a6ff0396df.json` | GCP IAM | Service account private key + client email |
| `blogger-oauth-tokens.json` | Google OAuth | OAuth client_id, client_secret, refresh_token |
| `client_secret_641160040343-...json` | Google OAuth | OAuth web client ID + secret |
| `blogger-api-key.txt` | Blogger API | Restricted API key (read-only public data) |
| `cloudflare-api-token.txt` | Cloudflare | Zone-level API Bearer token (Token B) |
| `cloudflare-workers-token.txt` | Cloudflare | Account-level Workers & Pages API token (Token A) |
| `cloudflare-global-key.txt` | Cloudflare | Global API Key (full access, fallback) |
| `cloudflare-zone-id.txt` | Cloudflare | Zone ID for ayurshakti.shop |
| `cloudflare-account-id.txt` | Cloudflare | Account ID |
| `cloudflare-email.txt` | Cloudflare | Account email (`vle.bhati@gmail.com`) |
| `ga4-mp-secret.txt` | GA4 | Measurement Protocol secret (server-side events) |
| `bing-api-key.txt` | Bing | Bing API key |
| `bing-client-credentials.json` | Bing | Bing Webmaster OAuth credentials (client ID + secret) |
| `x-creds.json` | X/Twitter | Developer API keys and tokens |
| `pinterest-creds.json` | Pinterest | Pinterest API App ID and access token |
| `bluesky-creds.json` | Bluesky | Bluesky API credentials |
| `bluesky-creds.json.template` | Bluesky | Template file (no actual secrets) |
| `github-images-token.json` | GitHub | GitHub access token for the `bhati8833/ayurshakti-images` image repo |
| `cookies-reddit.txt` | Reddit | Login session cookies |
| `cookies-quora.txt` | Quora | Login session cookies |
| `cookies-medium.txt` | Medium | Login session cookies |
| `cookies-pinterest.txt` | Pinterest | Login session cookies |
| `cookies-x.txt` | X/Twitter | Login session cookies |
| `blogger_cookies.txt` | Blogger | Login session cookies for Blogger dashboard |
| `seznam-api-key.txt` | Seznam | Seznam Webmaster API key |

> **Security:** All `secrets/` files are listed in `.gitignore` and never committed. AI agents must load credential values from these files at runtime — never hardcode them.

---

## 4. Cloudflare

### Zone Info

| Parameter | Value | Source |
|-----------|-------|--------|
| Zone ID | `f63c29bc9532dc008cd45e2db084ee4e` | `secrets/cloudflare-zone-id.txt` |
| Account ID | `7d34fa428747bddab0f82baf07479bc6` | `secrets/cloudflare-account-id.txt` |
| Plan | Free | Cloudflare dashboard |
| Status | Active | Cloudflare dashboard <!-- VERIFY: confirm zone is still active in Cloudflare dashboard --> |

### Nameservers

| Provider | Nameservers |
|----------|-------------|
| Cloudflare | `betty.ns.cloudflare.com`, `sri.ns.cloudflare.com` |
| Registrar | Namecheap (points to Cloudflare NS) |

### DNS Records

<!-- VERIFY: confirm current DNS records in Cloudflare dashboard -->

| Type | Name | Content | Proxy | TTL |
|------|------|---------|-------|-----|
| A | `@` | `216.239.32.21` | DNS only | 3600 |
| A | `@` | `216.239.34.21` | DNS only | 3600 |
| A | `@` | `216.239.36.21` | DNS only | 3600 |
| A | `@` | `216.239.38.21` | DNS only | 3600 |
| CNAME | `www` | `ghs.google.com` | DNS only | Auto |
| CNAME | `resources` | `ayurshakti-images.pages.dev` | Proxied | Auto |
| CNAME | `llms` | `llms-txt.ayurshakti.workers.dev` | Proxied | Auto |
| MX | `@` | `route{1,2,3}.mx.cloudflare.net` | DNS only | Auto |
| TXT | `@` | SPF record, Pinterest verification | DNS only | 3600 |
| TXT | `cf2024-1._domainkey` | DKIM key for email signing | DNS only | Auto |
| TXT | `_dmarc` | DMARC policy (`p=none`) | DNS only | Auto |

### API Tokens

Two-token architecture with non-overlapping permissions:

| Token | File | Scope | Permissions |
|-------|------|-------|-------------|
| **Token A** (Workers & Pages) | `secrets/cloudflare-workers-token.txt` | Account | Workers Scripts:Edit, Pages:Edit, KV:Edit, R2:Edit, D1:Edit, AI:Edit |
| **Token B** (Zone Admin) | `secrets/cloudflare-api-token.txt` | Zone `ayurshakti.shop` | DNS:Edit, Cache Purge, SSL:Edit, WAF:Edit, Transform Rules:Edit, Email Routing:Edit |
| **Global Key** (Fallback) | `secrets/cloudflare-global-key.txt` | Full | Complete API access |

### Workers

| Worker | Route | Purpose | Source |
|--------|-------|---------|--------|
| **llms-txt** | `llms.ayurshakti.shop/*` | Serves `llms.txt` for AI crawlers | `scripts/llms-worker.js` |
| **ayurshakti-images** | `resources.ayurshakti.shop/*` | Static asset hosting via Cloudflare Pages | `blog_images/wrangler.toml` |
| **ayurshakti-robots** | `ayurshakti.shop/robots.txt` + `www.ayurshakti.shop/robots.txt` | Serves site `robots.txt` (Blogger API cannot set it) | `robots-worker/worker.js` |

### robots.txt Deployment (IMPORTANT)

Blogger's API **cannot** write the custom `robots.txt`, and the `www` record is grey-clouded by default — so a **Cloudflare Worker** (`ayurshakti-robots`) serves it instead.

- The `www.ayurshakti.shop` DNS record is **proxied (orange-cloud)** so the Worker route intercepts `/robots.txt`.
- Cloudflare Bot Management **managed robots.txt is DISABLED** (`is_robots_txt_managed: false`) so it doesn't override the Worker.
- Yandex/Seznam/AI-optimized rules live in the repo file **`robots.txt`**.

**To update robots.txt:**
1. Edit `robots.txt` in repo root.
2. `cd robots-worker && python3 inject.py` (injects content into `worker.js`).
3. `CLOUDFLARE_API_TOKEN=$(cat ../secrets/cloudflare-workers-token.txt) npx wrangler deploy`
4. Verify: `curl -s https://www.ayurshakti.shop/robots.txt` matches local.

### Email Routing

Cloudflare Email Routing forwards `contact@ayurshakti.shop` to the Gmail account configured in `secrets/cloudflare-email.txt` (`vle.bhati@gmail.com`). <!-- VERIFY: confirm email routing rules in Cloudflare dashboard -->

---

## 5. Google Cloud Platform

### Project

| Parameter | Value |
|-----------|-------|
| Project ID | `ayurshakti-501603` |
| Project Number | `641160040343` |
| Owner Email | `contact@ayurshakti.shop` |

### Enabled APIs

| API | Purpose | Auth Methods |
|-----|---------|--------------|
| Blogger API v3 | Blog post CRUD, pages, comments | API Key (read) / OAuth (write) |
| Google Analytics Data API | Traffic analytics, user behavior | OAuth / Service Account |
| Google Search Console API | Keyword research, SEO performance | OAuth / Service Account |
| PageSpeed Insights API | Lighthouse performance audits | API Key only |
| Web Search Indexing API | Instant Google indexing notifications | OAuth / Service Account |
| API Keys API | Create/restrict API keys | OAuth only |

### Service Account

| Parameter | Value |
|-----------|-------|
| Email | `blogger-service-account@ayurshakti-501603.iam.gserviceaccount.com` |
| Key File | `secrets/ayurshakti-501603-a1a6ff0396df.json` |
| GA4 Access | Viewer role |
| GSC Access | siteFullUser |

### OAuth 2.0 Client

| Parameter | Value |
|-----------|-------|
| Client Secret File | `secrets/client_secret_641160040343-...json` |
| Auth URI | `https://accounts.google.com/o/oauth2/auth` |
| Token URI | `https://oauth2.googleapis.com/token` |
| Redirect URIs | `http://localhost:8080` |
| Consent Screen | Testing mode (`vle.bhati@gmail.com` as test user) <!-- VERIFY: confirm consent screen status in GCP console --> |

### API Quotas (Free Tier)

| API | Daily Quota | Rate Limit |
|-----|-------------|------------|
| Blogger API v3 | 10,000 req/day | 100 req/100s |
| Analytics Data API | 200,000 req/day | 60 req/min |
| Search Console API | 2,000 queries/day | 1 query/s |
| PageSpeed Insights API | 25,000 req/day | 240 req/min |
| Web Search Indexing API | 200 URLs/day | 1 req/s (burst 5/s) |

All quotas reset at midnight Pacific Time. Overages return `429 Too Many Requests`.

---

## 6. Blogger

| Parameter | Value | Source |
|-----------|-------|--------|
| Blog ID | `944859273218738540` | `scripts/schedule-config.json` |
| Blog Name | `ayurshakti` | Blogger dashboard |
| URL | `https://www.ayurshakti.shop/` | — |
| Platform | Google Blogger | — |

### Authentication Methods

| Method | Capability | Credential Source |
|--------|-----------|-------------------|
| **API Key** (restricted) | Read-only (public data) | `secrets/blogger-api-key.txt` |
| **OAuth Refresh Token** | Read + Write (recommended) | `secrets/blogger-oauth-tokens.json` |
| **Service Account** | Read-only (via JWT) | `secrets/ayurshakti-501603-a1a6ff0396df.json` |

> **Blog ID discrepancy:** `config/profile.json` contains `blogger_id: "5016036252143286656"`, while `scripts/schedule-config.json` and all operational docs use `944859273218738540`. The latter is the active Blog ID used in API calls. <!-- VERIFY: confirm both IDs in Blogger dashboard; the profile.json value may be a different resource ID -->

---

## 7. Google Analytics (GA4) & Search Console

### GA4

| Parameter | Value | Source |
|-----------|-------|--------|
| Property Name | `san-hini-1` | GA4 dashboard |
| Property ID | `533609055` | GA4 admin |
| Measurement ID | `G-1KKZFZB7ML` | GA4 data streams |
| Measurement Protocol Secret | (see file) | `secrets/ga4-mp-secret.txt` |
| Timezone | `Asia/Calcutta` | GA4 property settings |
| Currency | `INR` | GA4 property settings |

### Google Search Console

| Parameter | Value |
|-----------|-------|
| Site Property | `sc-domain:ayurshakti.shop` (domain property) |
| Service Account | Added as Full User <!-- VERIFY: confirm service account has siteFullUser role in GSC --> |
| Data Status | New site — no data yet |

---

## 8. Bing Webmaster Tools

| Parameter | Value | Source |
|-----------|-------|--------|
| API Key | (see file) | `secrets/bing-api-key.txt` |
| Client Credentials | (see file) | `secrets/bing-client-credentials.json` |
| Script | `scripts/bing-sitemap-submit.py` | Sitemap/IndexNow submission |

Bing URL submission via IndexNow is mandatory for rapid indexing after the June 2026 Bing Index Update.

---

## 9. Yandex Webmaster

| Parameter | Value | Source |
|-----------|-------|--------|
| Verification Method | Meta tag / DNS TXT | Yandex Webmaster UI |
| Meta Tag | `<meta name="yandex-verification" content="a4f4553babbc2e32" />` | Added to `theme-and-logo/ayurshakti-main.xml` |
| API Key | **Not provided** | Yandex does not offer API key for sitemap submission |
| Sitemap | `https://www.ayurshakti.shop/sitemap.xml` | Submit manually in Webmaster UI |
| IndexNow | Supported via `api.indexnow.org` | Uses Bing API key |

### Yandex Webmaster Setup

1. Add site at https://webmaster.yandex.com
2. Verify via meta tag (recommended): `<meta name="yandex-verification" content="a4f4553babbc2e32" />` in Blogger theme `<head>`
3. Submit sitemap: Indexing → Sitemap files → Add `https://www.ayurshakti.shop/sitemap.xml`
4. DNS TXT record (alternative): `yandex-verification = a4f4553babbc2e32`

### Important Notes

**No API Key**: Yandex Webmaster does **not** provide an API key for programmatic sitemap/URL submission (unlike Bing/Google). Verification is done via:
1. Meta tag in HTML `<head>` (preferred for Blogger)
2. DNS TXT record
3. HTML file upload
4. WHOIS email

**IndexNow Support**: Yandex supports IndexNow protocol. Use the same `scripts/bing-sitemap-submit.py` with the Bing API key to submit URLs to Yandex simultaneously.

**Manual Sitemap Submission**: After verification, submit `https://www.ayurshakti.shop/sitemap.xml` in Yandex Webmaster UI → Indexing → Sitemap files.

**robots.txt**: Yandex-specific rules are in the repo `robots.txt` (served via Blogger's custom robots.txt editor — Settings → Search preferences → Custom robots.txt):
- `Sitemap: https://www.ayurshakti.shop/sitemap.xml` (XML sitemap — **not** the Atom feed)

NOTE: Blogger's custom robots.txt editor only accepts standard REP directives (User-agent, Allow, Disallow, Sitemap). Yandex-specific extensions (`Clean-param`, `Crawl-delay`, `Host`) are NOT supported and are intentionally omitted.

Yandex robots.txt requirements: max 500 KB, root location, HTTP 200, standard REP directives only (Blogger does not support the `Clean-param`/`Crawl-delay`/`Host` extensions).

---

## 10. Seznam Webmaster

| Parameter | Value | Source |
|-----------|-------|--------|
| Verification Method | Meta tag | Blogger theme `<head>` |
| Meta Tag | `<meta name="seznam-wmt" content="ThtQuvsJGBn0D8Zwafe17h8vAGV9mAIt" />` | Added to `theme-and-logo/ayurshakti-main.xml` |
| API Key | Stored in `secrets/seznam-api-key.txt` (do not commit the key) | `secrets/seznam-api-key.txt` |
| API Base URL | `https://reporter.seznam.cz/wm/api` | Seznam Webmaster API |
| API Docs | `https://reporter.seznam.cz/wm/web/dokumentace` | Official documentation |
| Sitemap | `https://www.ayurshakti.shop/sitemap.xml` | Submit in Webmaster UI |
| IndexNow | Supported via `search.seznam.cz/indexnow` & `api.indexnow.org` | Uses Bing API key |

### API Endpoints (Bearer token + session cookie auth)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/web` | GET | Site overview (counts by category) |
| `/web/documents` | GET | Page counts + sample URLs (max 1000) |
| `/web/documents-history` | GET | Historical daily counts |
| `/web/document` | GET | Specific URL details |
| `/web/document/reindex` | POST | Request reindex (write key, 500/day) |
| `/web/database-info` | GET | Database version <!-- VERIFY: not yet implemented in seznam-api.py — endpoint exists on Seznam API but needs a script wrapper --> |
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

### Important Notes

**Verification**: Meta tag must be in static HTML source (not injected via JS). Blogger theme XML is the correct place.

**API Authentication**: The API key is stored in `secrets/seznam-api-key.txt` (generated in Seznam Webmaster UI → API → Access Keys). Requires **session cookie** from login at `https://reporter.seznam.cz/wm/` — Bearer token alone is not sufficient.

**IndexNow**: Seznam supports IndexNow protocol. The existing `scripts/bing-sitemap-submit.py` submits to `api.indexnow.org` which covers Bing, Yandex, and Seznam simultaneously.

**robots.txt**: Seznam-specific rules are in the repo `robots.txt` (served via Blogger's custom robots.txt editor — Settings → Search preferences → Custom robots.txt):
- The `User-agent: SeznamBot` block contains only `Allow: /` (no Disallow set; Blogger does not support per-bot Disallow beyond the `*` block)
- `Request-rate` is NOT supported by Blogger's robots.txt editor and is omitted
- `Sitemap: https://www.ayurshakti.shop/sitemap.xml`

Seznam robots.txt directives: `User-agent`, `Disallow`, `Allow`, `Sitemap` (case-insensitive names, case-sensitive paths). `Request-rate`, `Crawl-delay`, and `Host` are not supported by Blogger's robots.txt editor.

---

## 11. Email System

### Email Identity

| Parameter | Value |
|-----------|-------|
| From Address | `contact@ayurshakti.shop` |
| SMTP Auth Account | `vle.bhati@gmail.com` (App Password) |
| Routing | Cloudflare Email Routing → Gmail |

### Google Sheets (Subscriber Database)

| Parameter | Value |
|-----------|-------|
| Spreadsheet ID | `1-8SFDK23ZXMGKmBfdXpY-wNkwTGWZfTUTy9JJPZAZas` |
| Sheet Name | `AyurShakti Email List` |
| Apps Script File | `scripts/email-apps-script-code.js` |

### Sheet Columns

| Column | Position | Type | Purpose |
|--------|----------|------|---------|
| `timestamp` | A | Auto | Form submission time |
| `name` | B | String | Subscriber first name |
| `email` | C | String | Subscriber email (unique) |
| `source` | D | String | Signup location (sidebar, popup, post-footer, lead-magnet) |
| `lead_sent` | E | TRUE/FALSE | Welcome email delivered? |
| `unsubscribed` | F | TRUE/FALSE | Opt-out status |
| `unsubscribed_at` | G | Date | When they opted out |
| `last_newsletter_sent` | H | Date | Last newsletter date |
| `bounce_count` | I | Number | Failed delivery count |

### Apps Script Config (edit in `scripts/email-apps-script-code.js`)

| Parameter | Value |
|-----------|-------|
| `MAX_DAILY_EMAILS` | `80` |
| `UNSUBSCRIBE_BOUNCE_LIMIT` | `3` |
| `LEAD_MAGNET_URL` | `https://resources.ayurshakti.shop/pdfs/lead-magnet.pdf` |

---

## 12. Label Taxonomy

The site uses a two-tier label system for Blogger posts: **menu category labels** (top-level navigation) and **herb sub-labels** (for the "All Herbs" sub-menu). Labels are critical for site navigation — without correct labels, articles don't appear on their category pages.

### Label Assignment

Labels are assigned programmatically by `assign_categories.py` based on article title keyword matching, and can also be manually set in the article's `labels` array in `approval-queue.json`. Every article must have at least one menu category label before it can be scheduled (the scheduler skips articles with empty labels).

### Menu Category Labels (Top-Level)

These correspond to the site's main navigation menu. Each article should have **at least one** category label:

| Label | Trigger Keywords | Example Articles |
|-------|-----------------|-----------------|
| `Ayurvedic Herbs` | Any herb name match + `herb`, `supplement` | Ashwagandha, Brahmi, Triphala, Turmeric guides |
| `Dog Health` | `dog`, `puppy`, `canine`, `pet`, `flea`, `tick`, `ear infection` | Coconut Oil for Dogs, Triphala for Dogs, Dog Anxiety |
| `Women's Health` | `women`, `pcos`, `female`, `hormonal balance` | PCOS Remedies, Shatavari for Women |
| `Men's Health` | `men`, `male`, `testosterone`, `vitality` | Ashwagandha for Men, Brain Health |
| `Natural Remedies` | `gut health`, `digest`, `allergy`, `itchy`, `joint pain`, `arthritis`, `anxiety`, `calming`, `sleep` | Calming Chews, Joint Pain Relief, Sleep Remedies |
| `Brain Health` | `brain`, `memory`, `cogniti`, `mental`, `focus` | Brahmi Benefits, Cognitive Enhancement |

> **Note:** An article can have multiple category labels (e.g., an Ashwagandha article about men's health and stress gets `["Ashwagandha", "Ayurvedic Herbs", "Men's Health", "Natural Remedies"]`). The scheduler deduplicates categories when picking 2 articles per run to avoid publishing two articles from the same category in one day.

### Herb Sub-Labels (For "All Herbs" Menu)

When an article is about a specific herb, include the **individual herb name** as a sub-label. These power the "All Herbs" dropdown menu links (each herb name becomes a Blogger label search URL like `/search/label/Ashwagandha`):

| Herb Sub-Label | Keyword Match |
|----------------|---------------|
| `Ashwagandha` | Title contains "ashwagandha" |
| `Brahmi` | Title contains "brahmi" |
| `Triphala` | Title contains "triphala" |
| `Turmeric` | Title contains "turmeric" |
| `Giloy` | Title contains "giloy" |
| `Shatavari` | Title contains "shatavari" |
| `Shilajit` | Title contains "shilajit" |
| `Tulsi` | Title contains "tulsi" |

### Rule: New Herbs

Future articles about herbs not in the above list should still get the herb name as a sub-label (e.g., an article about "Neem" should include `"Neem"` in the `labels` array). Add the new herb to `assign_categories.py` so automated label assignment includes it. <!-- VERIFY: confirm the theme "All Herbs" menu includes the new herb sub-label after adding -->

### Validation

During the 16/16 pre-publish checklist (see `docs/09-article-writing-rule.md`), item #0 verifies:
- Article has correct menu category label(s)
- If herb-specific, includes the individual herb name as a sub-label
- Without correct labels, the category page stays empty — **this blocks scheduling**

### Label Source Code

The label assignment logic and the canonical herb name list live in:

| File | Purpose |
|------|---------|
| `assign_categories.py` | Keyword-to-label mapping + Blogger API update script |
| `scripts/approval-queue.json` | Per-article `labels` array (set before scheduling) |
| `data/tracking/article-registry.json` | Master registry with `labels` per published article |

---

## 13. Scheduler Configuration

**File:** `scripts/schedule-config.json`

| Variable | Value | Description |
|----------|-------|-------------|
| `target_timezone` | `America/New_York` | Scheduling timezone |
| `posts_per_day` | `2` | Maximum posts per day |
| `jitter_minutes` | `15` | Random minute offset within window |
| `gap_between_posts_hours` | `10` | Minimum hours between posts |
| `weekend_schedule` | `true` | Posts also on weekends |
| `max_daily_posts` | `2` | Hard limit |
| `blog_id` | `944859273218738540` | Blogger blog ID for API calls |
| `ga4_enabled` | `false` | GA4 measurement protocol disabled |

### Schedule Windows

| Slot | Hours (EST) | Label |
|------|-------------|-------|
| Morning | 08:00–10:00 | Morning (8-10am EST) |
| Evening | 18:00–20:00 | Evening (6-8pm EST) |

---

## 14. Social Media APIs

| Platform | Credential File | Auth Method |
|----------|----------------|-------------|
| X/Twitter | `secrets/x-creds.json` | OAuth 1.0a (consumer key + access token) |
| Pinterest | `secrets/pinterest-creds.json` | OAuth 2.0 (App ID + access token) |
| Bluesky | `secrets/bluesky-creds.json` | API password |
| Reddit | `secrets/cookies-reddit.txt` | Browser session cookie |
| Quora | `secrets/cookies-quora.txt` | Browser session cookie |
| Medium | `secrets/cookies-medium.txt` | Browser session cookie |

Social posting is handled by `scripts/social-post.py`.

---

## 15. Image Hosting

| Parameter | Value |
|-----------|-------|
| CDN Domain | `resources.ayurshakti.shop` |
| GitHub Repo | `bhati8833/ayurshakti-images` |
| Wrangler Config | `blog_images/wrangler.toml` |
| Deployment | Cloudflare Pages (auto-deploy from GitHub) + Wrangler CLI |
| Image URL Pattern | `https://resources.ayurshakti.shop/img/{filename}` |
| PDF URL Pattern | `https://resources.ayurshakti.shop/pdf/{filename}` |

---

## 16. Data Tracking Files

| File | Purpose |
|------|---------|
| `data/tracking/article-registry.json` | Master registry of all articles (status, dates, metadata) |
| `data/tracking/api-usage-log.json` | API rate limit and quota usage logs |
| `data/tracking/project-tasks.json` | Task management (Todo items for AI and User) |

---

## 17. Required vs Optional Settings

### Required (startup fails if missing)

| Setting | Validation |
|---------|-----------|
| `config/profile.json` | Must exist — loaded by `scripts/lib/profile.py` on import. Missing file raises `FileNotFoundError`. |
| All `secrets/` credential files | Scripts load directly from these files at runtime. Missing files cause HTTP 401/403 errors. |

### Optional (defaults in source code)

| Setting | Default | Defined In |
|---------|---------|------------|
| `ga4_enabled` | `false` | `scripts/schedule-config.json` |
| `jitter_minutes` | `15` | `scripts/schedule-config.json` |
| `posts_per_day` | `2` | `scripts/schedule-config.json` |
| `MAX_DAILY_EMAILS` | `80` | `scripts/email-apps-script-code.js` |
| `UNSUBSCRIBE_BOUNCE_LIMIT` | `3` | `scripts/email-apps-script-code.js` |

---

## 18. Python Dependencies

The project declares dependencies in both `requirements.txt` and `pyproject.toml`. Python scripts use standard library modules plus the following third-party packages:

| Package | Used In | Purpose |
|---------|---------|---------|
| `requests` (third-party) | Multiple scripts | HTTP API calls |
| `markdown` (third-party) | `scripts/schedule-posts.py` | Markdown-to-HTML conversion |
| `cryptography` (third-party) | Credential handling scripts | Encryption/decryption of secrets |
| `python-dotenv` (third-party) | Config loading scripts | Load environment variables from `.env` |

Install with:

```bash
pip install -r requirements.txt
```

### Node.js (for Wrangler)

| Tool | Used For |
|------|----------|
| `npx wrangler` | Cloudflare Workers deployment (from `blog_images/`) |
| `node_modules` | Present in project root (simple-icons dependency) |
