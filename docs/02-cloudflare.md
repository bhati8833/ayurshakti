# Cloudflare — ayurshakti.shop

## Zone Info

| Parameter | Value |
|-----------|-------|
| Zone ID | `f63c29bc9532dc008cd45e2db084ee4e` (`secrets/cloudflare-zone-id.txt`) |
| Account ID | `7d34fa428747bddab0f82baf07479bc6` (`secrets/cloudflare-account-id.txt`) |
| Status | Active |
| Plan | Free |

## Authentication

### Token Architecture — Two Token System

We maintain two API tokens with **non-overlapping permission sets** for security:

### Token A: Workers & Pages (Account-Level)
**File:** `secrets/cloudflare-workers-token.txt`
**Token Name:** `icy-bird-ef23`

**Used for:** Wrangler deploys, Workers scripts, Pages management.

```bash
# Wrangler deploy
cd blog_images
CLOUDFLARE_API_TOKEN=$(cat ../secrets/cloudflare-workers-token.txt) npx wrangler deploy

# Workers API
curl -H "Authorization: Bearer $TOKEN" \
  "https://api.cloudflare.com/client/v4/accounts/ACCOUNT_ID/workers/scripts"

# Pages API
curl -H "Authorization: Bearer $TOKEN" \
  "https://api.cloudflare.com/client/v4/accounts/ACCOUNT_ID/pages/projects"
```

**Permissions:**
- Account: Workers Scripts:Edit, Cloudflare Pages:Edit, Workers KV:Edit, Workers R2:Edit, D1:Edit, Queues:Edit, AI Gateway:Edit, Workers AI:Edit, Vectorize:Edit, Hyperdrive:Edit, etc.

### Token B: Zone Admin (Zone-Level)
**File:** `secrets/cloudflare-api-token.txt`
**Token Name:** `spcific_cf_token`

**Permissions:** Zone-level full access.

```bash
# All zone operations — DNS, Cache, SSL, WAF, Transform Rules, etc.
curl -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
  "https://api.cloudflare.com/client/v4/zones/YOUR_ZONE_ID"
```

**Permissions:**
- Zone (ayurshakti.shop): DNS:Edit, Cache Purge:Purge, Zone Settings:Edit, Analytics:Read, Firewall Services:Edit, SSL and Certificates:Edit, Transform Rules:Edit, Email Routing Rules:Edit, Bot Management:Edit, Custom Pages:Edit, Load Balancers:Edit

### Method 3: Global API Key (Fallback — Full Access)

**File:** `secrets/cloudflare-global-key.txt`

```bash
curl -H "X-Auth-Email: vle.bhati@gmail.com" \
  -H "X-Auth-Key: YOUR_CLOUDFLARE_GLOBAL_KEY" \
  "https://api.cloudflare.com/client/v4/zones/YOUR_ZONE_ID"
```

Global Key has **full access** — can do everything. Use only when Token A/Token B don't cover some operation.

### Token Usage Quick Reference

| Operation | Token A (workers) | Token B (zone) | Global Key |
|---|---|---|---|
| Wrangler deploy | ✅ | ❌ | ❌ |
| Workers scripts | ✅ | ❌ | ✅ |
| Pages projects | ✅ | ❌ | ✅ |
| DNS records | ❌ | ✅ | ✅ |
| Cache Purge | ❌ | ✅ | ✅ |
| Zone Settings | ❌ | ✅ | ✅ |
| SSL/Certs | ❌ | ✅ | ✅ |
| Page Rules | ❌ | ✅ | ✅ |
| WAF Firewall | ❌ | ✅ | ✅ |
| Transform Rules | ❌ | ✅ | ✅ |
| Email Routing | ❌ | ✅ | ✅ |
| Bot Management | ❌ | ✅ | ✅ |
| Load Balancers | ❌ | ✅ | ✅ |

## Nameservers

| Cloudflare NS | Status |
|---|---|
| `betty.ns.cloudflare.com` | Active (from Namecheap) |
| `sri.ns.cloudflare.com` | Active (from Namecheap) |

## DNS Records

| Type | Name | Content | Proxy | TTL |
|------|------|---------|-------|-----|
| A | `@` | `216.239.32.21` | DNS only | 3600 |
| A | `@` | `216.239.34.21` | DNS only | 3600 |
| A | `@` | `216.239.36.21` | DNS only | 3600 |
| A | `@` | `216.239.38.21` | DNS only | 3600 |
| CNAME | `www` | `ghs.google.com` | DNS only | Auto |
| CNAME | `f6bqezndsqmb` | `gv-nodx2qf3ujm32g.dv.googlehosted.com` | DNS only | 3600 |
| CNAME | `resources` | `ayurshakti-images.pages.dev` | Proxied | Auto |
| CNAME | `llms` | `llms-txt.ayurshakti.workers.dev` | Proxied | Auto |
| TXT | `@` | `pinterest-site-verification=...` | DNS only | 3600 |
| MX | `@` | `route{1,2,3}.mx.cloudflare.net` | DNS only | Auto |
| TXT | `@` | `v=spf1 include:_spf.mx.cloudflare.net...` | DNS only | Auto |
| TXT | `cf2024-1._domainkey` | DKIM key for email signing | DNS only | Auto |
| TXT | `_dmarc` | `v=DMARC1; p=none;` | DNS only | Auto |

**Important:** `www.ayurshakti.shop` is DNS-only (unproxied) — required for Google Sites/Blogger CNAME compatibility. This means Page Rules and Workers cannot be applied to the www domain.

## Workers

**llms-txt Worker:**
- Route: `llms.ayurshakti.shop/*` → `llms-txt` script
- Serves `llms.txt` for AI crawler knowledge retrieval
- Source: `scripts/llms-worker.js`
- Access: `https://llms.ayurshakti.shop/llms.txt`

**ayurshakti-images Worker (via Wrangler):**
- Deployed to `https://ayurshakti-images.ayurshakti.workers.dev`
- Cloudflare Pages auto-deploys from GitHub at `resources.ayurshakti.shop`
- Serves static assets from the GitHub repo `bhati8833/ayurshakti-images`

## Resource Hosting Architecture

### GitHub Repo Structure (`bhati8833/ayurshakti-images`)

```
/                    → index.html, wrangler.toml
/img/                → All .jpg, .png images (including favicon/)
/key/                 → indexnow-key.txt (Bing IndexNow verification)
/pdf/                → PDF assets (.pdf files)
```

### CDN URL Format

| Asset Type | URL Format | Example |
|---|---|---|
| Images | `https://resources.ayurshakti.shop/img/{filename}` | `/img/logo.png`, `/img/favicon/favicon.ico` |
| PDFs | `https://resources.ayurshakti.shop/pdf/{filename}` | `/pdf/lead-magnet.pdf` |
| Keys | `https://resources.ayurshakti.shop/key/{filename}` | `/key/indexnow-key.txt` |

### Deploy Flow

```bash
# 1. Generate image → saves to blog_images/img/
# Manually generate image per docs/13-image-generation-guide.md

# 2. Commit & push to GitHub (auto-triggers Cloudflare Pages rebuild)
cd blog_images
git add -A && git commit -m "Add image" && git push

# 3. OR deploy via Wrangler (bypasses GH Pages wait)
CLOUDFLARE_API_TOKEN=$(cat ../secrets/cloudflare-api-token.txt) npx wrangler deploy
```

## Useful Commands

```bash
# List DNS records (requires Global Key or zone-level token)
curl -X GET "https://api.cloudflare.com/client/v4/zones/YOUR_ZONE_ID/dns_records" \
  -H "X-Auth-Email: vle.bhati@gmail.com" \
  -H "X-Auth-Key: YOUR_GLOBAL_KEY"

# Create DNS record
curl -X POST "https://api.cloudflare.com/client/v4/zones/YOUR_ZONE_ID/dns_records" \
  -H "X-Auth-Email: vle.bhati@gmail.com" \
  -H "X-Auth-Key: YOUR_GLOBAL_KEY" \
  -H "Content-Type: application/json" \
  -d '{"type":"A","name":"www","content":"1.2.3.4","ttl":3600,"proxied":false}'

# Purge cache (Global Key required)
curl -X POST "https://api.cloudflare.com/client/v4/zones/YOUR_ZONE_ID/purge_cache" \
  -H "X-Auth-Email: vle.bhati@gmail.com" \
  -H "X-Auth-Key: YOUR_GLOBAL_KEY" \
  -d '{"purge_everything":true}'

# List Workers routes (API Token works)
curl -X GET "https://api.cloudflare.com/client/v4/zones/YOUR_ZONE_ID/workers/routes" \
  -H "Authorization: Bearer YOUR_API_TOKEN"

# Create Page Rule (API Token works for this)
curl -X POST "https://api.cloudflare.com/client/v4/zones/YOUR_ZONE_ID/pagerules" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"targets":[{"target":"url","constraint":{"operator":"matches","value":"*example.com/key*"}}], "actions":[{"id":"forwarding_url","value":{"url":"https://other.com/key","status_code":301}}], "status":"active"}'

# Deploy assets via Wrangler
cd blog_images
CLOUDFLARE_API_TOKEN=$(cat ../secrets/cloudflare-api-token.txt) npx wrangler deploy

# List Workers scripts
curl -X GET "https://api.cloudflare.com/client/v4/accounts/YOUR_ACCOUNT_ID/workers/scripts" \
  -H "Authorization: Bearer YOUR_API_TOKEN"
```

## Notes

- **www domain is DNS-only** — Cloudflare cannot intercept traffic to `www.ayurshakti.shop`. Page Rules, Workers, and WAF rules on this domain will NOT work.
- **resources subdomain is proxied** — Cloudflare serves the GitHub repo via Cloudflare Pages, proxying through the AAAA `100::` record.
- **llms subdomain is proxied** — Worker route active for serving `llms.txt`.
