# Credentials Reference — ayurshakti.shop

> ⚠️ **SECURITY NOTICE:** Actual credential values are NEVER hardcoded in docs.
> - Actual values → `secrets/` directory (gitignored)
> - This file → only shows **where** to find each credential
> - AI agents → load from `secrets/` files, don't hardcode in chat

---

## Secrets Directory Structure

| File | Contains | Created By |
|------|----------|-----------|
| `secrets/ayurshakti-501603-a1a6ff0396df.json` | GCP service account private key + client email | GCP IAM download |
| `secrets/client_secret_641160040343-....json` | OAuth web client ID + secret | GCP Credentials download |
| `secrets/cloudflare-api-token.txt` | Cloudflare API Bearer token | Cloudflare dashboard |
| `secrets/cloudflare-global-key.txt` | Cloudflare Global API Key | Cloudflare dashboard |
| `secrets/ga4-mp-secret.txt` | GA4 Measurement Protocol secret | GA4 admin → Data Streams |
| `secrets/bing-client-credentials.json` | Bing Webmaster API credentials | Bing Webmaster Portal |
| `secrets/cookies-*.txt` | Social media login cookies (reddit, quora, medium) | Extracted via browser extension |
| `secrets/x-creds.json` | Twitter (X) Developer API Keys and Tokens | Twitter Developer Portal |
| `secrets/pinterest-creds.json` | Pinterest API App ID and Access Token | Pinterest Developer Portal |
| `secrets/github-images-token.json` | GitHub Access Token for Image Repo | User provided |

---

## Credential Quick Reference

| # | Service | Credential Name | Where's the Value? | Used In |
|---|---------|----------------|-------------------|---------|
| 1 | **Cloudflare** | API Token | `secrets/cloudflare-api-token.txt` | `docs/02-cloudflare.md` |
| 2 | **Cloudflare** | Global API Key | `secrets/cloudflare-global-key.txt` | `docs/02-cloudflare.md` |
| 3 | **Cloudflare** | Zone ID | `docs/02-cloudflare.md` | DNS API calls |
| 4 | **Cloudflare** | Account ID | `docs/02-cloudflare.md` | Account API |
| 5 | **Bing** | API Key & Credentials | `secrets/bing-client-credentials.json` | IndexNow / Bing submission |
| 6 | **GCP** | Project ID (`ayurshakti-501603`) | `docs/03-gcp-apis.md` | All GCP APIs |
| 7 | **GCP IAM** | Service Account Email & Key | `secrets/ayurshakti-501603-*.json` | Web Search Indexing & GSC |
| 8 | **GA4** | Property ID (`533609055`) | `docs/05-analytics-seo.md` | Analytics API |
| 9 | **GA4** | Measurement ID (`G-1KKZFZB7ML`) | `docs/05-analytics-seo.md` | Analytics tracking |
| 10 | **GSC** | Site (`sc-domain:ayurshakti.shop`) | `docs/05-analytics-seo.md` | Search Console API |
| 11 | **GitHub** | Access Token (Image Hosting) | `secrets/github-images-token.json` | `docs/34-resource-hosting.md` |
| 12 | **Socials** | Twitter (X) & Pinterest Credentials | `secrets/x-creds.json` & `secrets/pinterest-creds.json` | Social syndication |

---

## Email Account & Identity

- **Contact & Primary Sending:** contact@ayurshakti.shop (Cloudflare Email Routing → Gmail)
- **Google Account Login:** vle.bhati@gmail.com (Firebase / GCP Owner)
- **Author Identity:** Suresh Bhati (contact@ayurshakti.shop)
