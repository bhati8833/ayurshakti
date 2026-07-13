# Overview — ayurshakti.shop

## Architecture

```
User ──► ayurshakti.shop ──► Cloudflare DNS ──► Google Blogger ──► Readers
                              (DNS only)
                              │
                              ├─ llms.ayurshakti.shop ──► Cloudflare Worker (llms-txt) ──► AI crawlers
                              │
                              └─ Email (contact@) ──► Cloudflare Email ──► Gmail ──► Apps Script ──► Google Sheet
                                      └─ Subscribers ──► Welcome Email ──► Newsletter ──► Traffic back to site
```

| Layer | Provider | Role |
|-------|----------|------|
| Domain | Namecheap | Registration |
| DNS | Cloudflare | Nameservers, DNS records |
| Hosting | Google Blogger | Content, pages, posts |
| Analytics | Google Analytics GA4 | Traffic tracking |
| SEO | Google Search Console | Keyword performance |
| Bing SEO | Bing Webmaster Tools | Bing indexation, sitemap submission |
| AI Crawlers | Cloudflare Worker (`llms-txt`) | `llms.txt` serve for GPTBot, Claude, Perplexity |
| Email Marketing | Google Sheets + Apps Script | Subscriber management, newsletter, lead magnets |

## Key Facts

| Fact | Value |
|------|-------|
| Blog ID | `944859273218738540` |
| GA4 Property ID | `533609055` |
| GA4 Measurement ID | `G-1KKZFZB7ML` |
| GCP Project ID | `ayurshakti-501603` |
| GCP Project Number | `641160040343` |
| Cloudflare Zone ID | `f63c29bc9532dc008cd45e2db084ee4e` |

## Service Account

| Field | Value |
|-------|-------|
| Email | `blogger-service-account@ayurshakti-501603.iam.gserviceaccount.com` |
| Key File | `secrets/ayurshakti-501603-a1a6ff0396df.json` |
| Permissions | Search Console: siteFullUser, GA4: Viewer |

## Refresh Token

| Field | Value |
|-------|-------|
| Token | `YOUR_REFRESH_TOKEN` (see `secrets/blogger-oauth-tokens.json`) |
| File | `secrets/blogger-oauth-tokens.json` |
| Expiry | Never |

## API Key (Restricted)

| Field | Value |
|-------|-------|
| Key | `YOUR_BLOGGER_API_KEY` (see `secrets/blogger-api-key.txt`) |
| Restrictions | Blogger API v3, *.ayurshakti.shop/* |
