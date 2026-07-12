# Technology Stack

**Project:** ayurshakti.shop — Multi-Platform Search Engine Indexing & AI Crawler Optimization
**Researched:** 2026-07-12
**Milestone Context:** Subsequent milestone — Adding Bing, Yandex, Seznam, IndexNow, and AI crawler optimization to existing Blogger + Cloudflare + Python automation stack

---

## Recommended Stack

### Core Framework (Existing — Do Not Change)

| Technology | Version | Purpose | Why |
|------------|---------|---------|-----|
| Python | 3.11+ | Core automation runtime | Already in `scripts/lib/`, battle-tested |
| Google APIs Client Library | `google-api-python-client` ≥ 2.100 | Blogger v3, GA4, Search Console, Indexing | Official, maintained, used in existing scripts |
| google-auth | ≥ 2.23 | OAuth 2.0 / Service Account auth | Required by Google APIs |
| requests | ≥ 2.31 | HTTP client for all non-Google APIs | Universal, zero-config, in stdlib-adjacent |
| python-dotenv | ≥ 1.0 | Secrets management via `.env` | Already used, keeps keys out of repo |

---

### NEW: Multi-Platform Search Engine Indexing

#### Bing Webmaster Tools API v2
| Technology | Version | Purpose | Why |
|------------|---------|---------|-----|
| `bing-webmaster-tools` | 1.2.0 | Async Python client for Bing WMT API | **Only maintained Python SDK**; covers all endpoints (SubmitUrl, GetCrawlIssues, GetQueryData, GetSitemaps, GetSiteInfo); built on aiohttp + Pydantic; MIT license; Python 3.9+ |
| Base URL | `https://ssl.bing.com/webmaster/api.svc/json/` | REST JSON endpoint | Official Microsoft endpoint |
| Auth | API Key (query param `apikey`) or OAuth 2.0 Bearer | Simple key for automation; OAuth for multi-user | API key from Bing Webmaster Tools → Settings → API Access |
| Rate Limits | Undocumented; observed ~1,200 QPM per site (similar to GSC) | Respect with exponential backoff | No official published limits; implement conservative client-side throttle |

**Integration Point:** Add `BingWebmasterClient` class in `scripts/lib/indexing/bing_client.py` wrapping the SDK. Reuse existing `scripts/lib/auth.py` pattern for API key loading from `.env`.

#### Yandex Webmaster API v4
| Technology | Version | Purpose | Why |
|------------|---------|---------|-----|
| `yandex-webmaster-api` | 0.0.3 | Python wrapper for Yandex Webmaster v4 | **Only Python library**; covers hosts, sitemaps, reindexing (recrawl), search queries, diagnostics, backlinks; MIT; Python ≥3.8 |
| Base URL | `https://api.webmaster.yandex.net/v4/user/{user_id}/hosts/{host_id}/` | REST API | Official Yandex endpoint |
| Auth | OAuth 2.0 (Authorization Code flow) | Required; no API key option | Register app at `https://oauth.yandex.ru/client/new`; scopes: `webmaster:hostinfo`, `webmaster:verify`, `webmaster:recrawl` |
| Rate Limits | Per-endpoint; recrawl quota checked via `/recrawl/quota/` | Use `/recrawl/quota/` before bulk submissions | Quota typically 100–1,000 URLs/day depending on site quality |

**Integration Point:** Add `YandexWebmasterClient` in `scripts/lib/indexing/yandex_client.py`. OAuth token refresh logic fits existing `scripts/lib/auth.py` token store pattern (reuse `TokenStore` class).

#### Seznam Webmaster (Czech Republic)
| Technology | Version | Purpose | Why |
|------------|---------|---------|-----|
| **No public Python SDK** | — | — | Seznam does not publish a public REST API; only API key retrieval from `https://reporter.seznam.cz/wm/` |
| Auth | API Key (project key from reporter.seznam.cz) | Simple key-based | Used by Czech SEO tools (Collabim, Semor, Rocketoo) |
| Endpoints | Undocumented internal API | No official public docs | Reverse-engineered by Czech tools; unstable for direct use |
| **Recommendation** | **Do not build custom client** | Use sitemap + robots.txt + IndexNow instead | Seznam participates in IndexNow; submitting via IndexNow covers Seznam indexing without fragile API dependency |

**Integration Point:** No new code. Ensure sitemap.xml is accessible, robots.txt allows `SeznamBot`, and IndexNow submissions include Seznam endpoint (`https://search.seznam.cz/indexnow`).

---

### NEW: IndexNow Protocol
| Technology | Version | Purpose | Why |
|------------|---------|---------|-----|
| `index-now` | 0.3.0 (jakob-bagterp/index-now-for-python) | Python client for IndexNow bulk + single submission | **Only maintained Python lib**; supports bulk (10k URLs), sitemap extraction, key generation, multiple search engine endpoints; MIT; Python 3.9+ |
| Shared Endpoint | `https://api.indexnow.org/indexnow` | Cross-engine submission (Bing, Yandex, Seznam, Yep, Naver) | One POST notifies all participating engines |
| Per-Engine Endpoints | `https://<engine>/indexnow` | Direct submission if needed | Bing: `bing.com`, Yandex: `yandex.com`, Seznam: `search.seznam.cz`, Yep: `indexnow.yep.com` |
| Key Format | 8–128 hex chars; hosted at `/{key}.txt` on domain root | Domain ownership proof | Must return 200, exact key match, no newline, `text/plain` |
| Rate Limits | 10,000 URLs per POST; 429 on excess → exponential backoff (60s, 5m, 30m) | Protocol spec | Implement `Retry-After` handling; batch large sitemaps |

**Integration Point:** Add `IndexNowClient` in `scripts/lib/indexing/indexnow_client.py`. Reuse `scripts/lib/sitemap.py` for URL extraction. Schedule via existing Cloudflare Worker cron or Python script triggered post-publish.

---

### NEW: AI Crawler Optimization

| Technology | Version | Purpose | Why |
|------------|---------|---------|-----|
| **No new Python dependencies** | — | robots.txt + llms.txt are static files | Zero runtime cost; served by Blogger/Cloudflare |
| `robots.txt` | Standard | Per-bot allow/block directives | Supported by all major AI crawlers |
| `llms.txt` | Emerging standard (2024–2025) | AI content usage policy + curated link index | Placed at domain root; read by GPTBot, ClaudeBot, PerplexityBot, etc. |
| Cloudflare Workers | Existing | Edge rewrite/serve of `robots.txt` and `llms.txt` | Already in stack; no origin hit |

**Crawler User-Agent Tokens (2025–2026):**

| Crawler | Operator | Purpose | Recommended Directive |
|---------|----------|---------|----------------------|
| `GPTBot` | OpenAI | Model training | `Disallow: /` (block training) |
| `OAI-SearchBot` | OpenAI | ChatGPT Search indexing | `Allow: /` (allow citations) |
| `ChatGPT-User` | OpenAI | Real-time user fetch | `Allow: /` |
| `ClaudeBot` | Anthropic | Model training | `Disallow: /` |
| `Claude-SearchBot` | Anthropic | Claude Search indexing | `Allow: /` |
| `Claude-User` | Anthropic | Real-time user fetch | `Allow: /` |
| `PerplexityBot` | Perplexity | Answer engine indexing | `Allow: /` |
| `Google-Extended` | Google | Gemini training opt-out | `Disallow: /` (does not affect Search) |
| `CCBot` | Common Crawl | Third-party training corpus | `Disallow: /` |
| `Bytespider` | ByteDance | TikTok/Doubao training | `Disallow: /` |
| `anthropic-ai` | Anthropic | Legacy training crawler | `Disallow: /` |

**llms.txt Template (place at `https://ayurshakti.shop/llms.txt`):**
```
# AI Crawler permissions
User-agent: GPTBot
Disallow: /

User-agent: OAI-SearchBot
Allow: /

User-agent: ChatGPT-User
Allow: /

User-agent: ClaudeBot
Disallow: /

User-agent: Claude-SearchBot
Allow: /

User-agent: Claude-User
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: Google-Extended
Disallow: /

User-agent: CCBot
Disallow: /

User-agent: Bytespider
Disallow: /

User-agent: anthropic-ai
Disallow: /

# curated index
Links:
- https://ayurshakti.shop/  (Home - Ayurveda wellness blog)
- https://ayurshakti.shop/sitemap.xml  (Full sitemap)
- https://ayurshakti.shop/category/ayurveda/  (Core content)
- https://ayurshakti.shop/category/herbs/  (Herb guides)
- https://ayurshakti.shop/category/recipes/  (Ayurvedic recipes)
```

---

## Alternatives Considered

| Category | Recommended | Alternative | Why Not |
|----------|-------------|-------------|---------|
| Bing SDK | `bing-webmaster-tools` (merj) | Direct REST calls via `requests` | SDK handles retries, rate limiting, Pydantic models, async — less boilerplate |
| Yandex SDK | `yandex-webmaster-api` (bzdvdn) | Direct REST calls | Only library covering v4 endpoints; OAuth flow non-trivial to reimplement |
| Seznam | **IndexNow + sitemap** | Custom API reverse-engineering | No public API; fragile; IndexNow is official participation |
| IndexNow | `index-now` (jakob-bagterp) | Manual `requests.post()` | Library handles batching, key validation, sitemap parsing, multi-engine endpoints |
| AI Crawler Control | `robots.txt` + `llms.txt` | Meta tags / HTTP headers | `robots.txt` is the standard all crawlers check; `llms.txt` emerging standard for AI-specific policy |
| Python HTTP | `requests` (sync) + `aiohttp` (via SDKs) | `httpx` | Existing codebase uses `requests`; SDKs bring their own async clients; no need to standardize yet |

---

## Installation

```bash
# Core (already present)
pip install google-api-python-client google-auth python-dotenv requests

# NEW: Multi-platform indexing
pip install bing-webmaster-tools==1.2.0
pip install yandex-webmaster-api==0.0.3
pip install index-now==0.3.0

# Dev dependencies
pip install -D pytest pytest-asyncio pytest-mock black ruff mypy
```

**Requirements.txt additions:**
```
bing-webmaster-tools==1.2.0
yandex-webmaster-api==0.0.3
index-now==0.3.0
```

---

## Sources

- **Bing Webmaster Tools API**: https://github.com/merj/bing-webmaster-tools (README, PyPI, source)
- **Bing API Docs**: https://learn.microsoft.com/en-us/bingwebmaster/
- **Yandex Webmaster API v4**: https://yandex.com/dev/webmaster/doc/en/concepts/getting-started
- **Yandex Python SDK**: https://pypi.org/project/yandex-webmaster-api/ (v0.0.3, 2024-03-12)
- **IndexNow Protocol**: https://www.indexnow.org/documentation, https://www.indexnow.org/faq
- **IndexNow Python**: https://github.com/jakob-bagterp/index-now-for-python
- **Seznam Webmaster**: https://reporter.seznam.cz/wm/, Collabim integration docs
- **AI Crawlers 2026**: Contently (2026-05-06), BestSEO.sg (2026-05-06), Pixis (2026-06-09), Verlua (2026-05-14), IndexDoctor (2026-04-19)
- **llms.txt**: https://www.ingeniousnetsoft.com/what-is-llms-txt-file-and-what-does-it-do (2026-04-28), ai-robots-txt GitHub org
- **Google Search Console API**: https://developers.google.com/webmaster-tools/v1/ (v3, current as of 2024-07-23)