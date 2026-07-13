# Credentials Reference — ayurshakti.shop

> ⚠️ **SECURITY NOTICE:** Actual credential values are NEVER hardcoded in docs.
> - Actual values → `secrets/` directory (gitignored)
> - This file → only shows **where** to find each credential
> - AI agents → load from `secrets/` files, don't hardcode in chat

## Secrets Directory Structure

| File | Contains | Created By |
|------|----------|-----------|
| `secrets/ayurshakti-501603-a1a6ff0396df.json` | GCP service account private key + client email | GCP IAM download |
| `secrets/blogger-oauth-tokens.json` | OAuth client_id, client_secret, refresh_token | OAuth flow (see `docs/04-blogger-api.md`) |
| `secrets/client_secret_641160040343-....json` | OAuth web client ID + secret | GCP Credentials download |
| `secrets/blogger-api-key.txt` | Blogger REST API key (restricted) | GCP API Keys dashboard |
| `secrets/cloudflare-api-token.txt` | Cloudflare API Bearer token | Cloudflare dashboard |
| `secrets/cloudflare-global-key.txt` | Cloudflare Global API Key | Cloudflare dashboard |
| `secrets/ga4-mp-secret.txt` | GA4 Measurement Protocol secret | GA4 admin → Data Streams |
| `secrets/cookies-*.txt` | Social media login cookies (reddit, quora, medium) | Extracted via browser extension |
| `secrets/x-creds.json` | Twitter (X) Developer API Keys and Tokens | Twitter Developer Portal |
| `secrets/pinterest-creds.json` | Pinterest API App ID and Access Token | Pinterest Developer Portal |
| `secrets/github-images-token.json` | GitHub Access Token for Image Repo | User provided |

## Credential Quick Reference

| # | Service | Credential Name | Where's the Value? | Used In |
|---|---------|----------------|-------------------|---------|
| 1 | Cloudflare | API Token | `secrets/cloudflare-api-token.txt` | `docs/02-cloudflare.md` |
| 2 | Cloudflare | Global API Key | `secrets/cloudflare-global-key.txt` | `docs/02-cloudflare.md` |
| 3 | Cloudflare | Zone ID | `docs/02-cloudflare.md` (actual in secrets/) | DNS API calls |
| 4 | Cloudflare | Account ID | `docs/02-cloudflare.md` (actual in secrets/) | Account-level API |
| 5 | Bing | API Key | `secrets/bing-client-credentials.json` | `docs/09` Bing SEO / IndexNow submission |
| 6 | Bing | Client ID | `secrets/bing-client-credentials.json` | Bing Webmaster auth |
| 7 | Bing | Client Secret | `secrets/bing-client-credentials.json` | Bing Webmaster auth |
| 5 | GCP | Project ID: `ayurshakti-501603` | `docs/03-gcp-apis.md` | All GCP APIs |
| 6 | GCP | Project Number: `641160040343` | `docs/03-gcp-apis.md` | GCP billing/IDs |
| 7 | Blogger | API Key (restricted) | `secrets/blogger-api-key.txt` | `docs/04-blogger-api.md` |
| 8 | Blogger | API Key (old — REVOKED) | N/A — deleted from GCP | Legacy |
| 9 | Google OAuth | Client ID | `secrets/client_secret_*.json` | `docs/04-blogger-api.md` |
| 10 | Google OAuth | Client Secret | `secrets/client_secret_*.json` | `docs/04-blogger-api.md` |
| 11 | Google OAuth | Refresh Token | `secrets/blogger-oauth-tokens.json` | `docs/04-blogger-api.md` |
| 12 | GCP IAM | Service Account Email | `secrets/ayurshakti-501603-*.json` | SA auth (see `docs/05`) |
| 13 | GCP IAM | Service Account Private Key | `secrets/ayurshakti-501603-*.json` | JWT token generation |
| 14 | Google | Blog ID: `944859273218738540` | `docs/04-blogger-api.md` | All Blogger API calls |
| 15 | GA4 | Property ID: `533609055` | `docs/05-analytics-seo.md` | Analytics API |
| 16 | GA4 | Measurement ID: `G-1KKZFZB7ML` | `docs/05-analytics-seo.md` | MP/analytics API |
| 17 | GA4 | Measurement Protocol Secret | `secrets/ga4-mp-secret.txt` | `docs/05-analytics-seo.md` |
| 18 | GSC | Site: `sc-domain:ayurshakti.shop` | `docs/05-analytics-seo.md` | Search Console API |
| 19 | PageSpeed | API Key (same as Blogger key) | `secrets/blogger-api-key.txt` | `docs/05-analytics-seo.md` |
| 20 | Indexing API | Auth via SA | `secrets/ayurshakti-501603-*.json` | `docs/05-analytics-seo.md` |
| 21 | Social Logins | Cookies for Reddit, Quora, etc. | `secrets/cookies-*.txt` | `docs/12-backlink-strategy.md` |
| 22 | Twitter API | OAuth tokens/keys | `secrets/x-creds.json` | `docs/12-backlink-strategy.md` |
| 23 | Pinterest API | App ID and Access Token | `secrets/pinterest-creds.json` | `docs/12-backlink-strategy.md` |
| 24 | GitHub API | Access Token (Image Hosting) | `secrets/github-images-token.json` | Image Generation / Publishing |

## Email Account

- **Contact & Primary Sending:** contact@ayurshakti.shop (Cloudflare Email Routing → Gmail)
- **Google Account Login:** vle.bhati@gmail.com (App Password via `~/.config/opencode-mail.conf`)
- **Owner:** Suresh Bhati (contact@ayurshakti.shop)
> **CRITICAL RULE:** For ALL email sending and reading via AI agents, use the identity `Suresh Bhati` and the email `contact@ayurshakti.shop`. The `vle.bhati@gmail.com` email should ONLY be used for SMTP/IMAP authentication if strictly required, but NEVER as the sender or public-facing email.
>
> **Setup Requirement:** For Gmail to allow sending as `contact@ayurshakti.shop`, you MUST add it in Gmail Settings -> "Accounts and Import" -> "Send mail as" using `smtp.gmail.com` and the App Password. Otherwise, Gmail will rewrite the From address to `vle.bhati@gmail.com`.

## JSON Files

| File | Contains | Source |
|------|----------|--------|
| `secrets/ayurshakti-501603-a1a6ff0396df.json` | Service account private key + client email | GCP IAM download |
| `secrets/blogger-oauth-tokens.json` | OAuth refresh token | Generated via OAuth flow |
| `secrets/client_secret_641160040343-...json` | OAuth web client ID + secret | GCP Credentials download |
