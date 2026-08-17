# Credentials Reference — ayurshakti.shop

> ⚠️ **SECURITY NOTICE:** Actual credential values are NEVER hardcoded in docs.
> - Actual values → `secrets/` directory (gitignored)
> - GitHub secrets → repository settings (encrypted)
> - AI agents → load from `secrets/` files or environment

---

## Secrets Directory & GitHub Secrets

| Secret Name / File | Service | Contains / Used For | Where Stored |
|-------------------|---------|---------------------|--------------|
| `FIREBASE_TOKEN` | Firebase Hosting | CLI Deploy Token for `vle.bhati@gmail.com` (`ayur-shakti` project) | GitHub Secrets (`FIREBASE_TOKEN`) & `~/.config/configstore/firebase-tools.json` |
| `ayurshakti-501603-a1a6ff0396df.json` | GCP IAM | Service account private key + email for Indexing API & GSC (`ayurshakti-501603`) | `secrets/ayurshakti-501603-a1a6ff0396df.json` |
| `client_secret_641160040343-....json` | GCP OAuth | OAuth web client ID + secret | `secrets/` |
| `cloudflare-api-token.txt` | Cloudflare | API Bearer token | `secrets/cloudflare-api-token.txt` |
| `cloudflare-global-key.txt` | Cloudflare | Global API Key | `secrets/cloudflare-global-key.txt` |
| `ga4-mp-secret.txt` | GA4 | Measurement Protocol secret | `secrets/ga4-mp-secret.txt` |
| `bing-client-credentials.json` | Bing Webmaster | API credentials for IndexNow | `secrets/bing-client-credentials.json` |
| `github-images-token.json` | GitHub | Access token for image repository (`resources.ayurshakti.shop`) | `secrets/github-images-token.json` |
| `x-creds.json` & `pinterest-creds.json` | Social APIs | API Keys and Tokens for Twitter/X and Pinterest | `secrets/` |

---

## Service & Project Mapping

| # | Service | Identifier / Project | Used In |
|---|---------|----------------------|---------|
| 1 | **Firebase Hosting** | Project `ayur-shakti` | Static site hosting & Edge CDN (`npm run build` static export) |
| 2 | **GitHub Actions** | Repository `bhati8833/ayurshakti` | CI/CD automated build & deploy pipeline (`.github/workflows/firebase-deploy.yml`) |
| 3 | **GCP Indexing API** | Project `ayurshakti-501603` | Google Search Indexing API calls (`scripts/gsc-index-submit.py`) |
| 4 | **GA4 Analytics** | Property `533609055` (`G-1KKZFZB7ML`) | Client & Measurement Protocol tracking |
| 5 | **Cloudflare DNS** | Zone `ayurshakti.shop` | Domain DNS, SSL, WAF, Edge Caching |

---

## Email Account & Identity

- **Contact & Primary Sending:** `contact@ayurshakti.shop` (Cloudflare Email Routing → Gmail)
- **Google Account Owner:** `vle.bhati@gmail.com` (Firebase `ayur-shakti` owner)
- **Author Identity:** Suresh Bhati ([contact@ayurshakti.shop](mailto:contact@ayurshakti.shop))
