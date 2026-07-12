# Architecture Patterns

**Domain:** Multi-platform search engine indexing + AI crawler optimization for ayurshakti.shop Blogger site
**Researched:** 2026-07-12

## Recommended Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        AYURSHAKTI.SHOP INDEXING PIPELINE                      │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌──────────────┐     ┌──────────────────┐     ┌────────────────────────┐  │
│  │  SCHEDULER   │────▶│  ARTICLE PUBLISH │────▶│  INDEXING ORCHESTRATOR │  │
│  │ schedule-    │     │  (Blogger API)   │     │  (new unified script)  │  │
│  │ posts.py     │     └──────────────────┘     └───────────┬────────────┘  │
│  └──────────────┘                                          │               │
│         │                                                   │               │
│         │                    ┌──────────────────────────────┼────────────┐  │
│         │                    ▼                              ▼            ▼  │
│         │            ┌────────────────┐            ┌─────────────┐ ┌─────────┐
│         │            │  IndexNow      │            │  Yandex     │ │ Seznam  │
│         │            │  (Bing/Yandex/ │            │  Webmaster  │ │ Webmaster│
│         │            │   Seznam)      │            │  API        │ │ API     │
│         │            │  api.indexnow. │            │  reporter.  │ │ reporter.│
│         │            │  org/indexnow  │            │  seznam.cz  │ │ seznam.cz│
│         │            └───────┬────────┘            └──────┬──────┘ └────┬────┘  │
│         │                    │                            │            │        │
│         │                    ▼                            ▼            ▼        │
│         │            ┌─────────────────────────────────────────────────────┐   │
│         │            │         UNIFIED PIPELINE STATUS TRACKING            │   │
│         │            │  (data/tracking/pipeline-status.json — extended)    │   │
│         │            │  stages: scheduled → published → pinged(indexnow)   │   │
│         │            │               → pinged(yandex) → pinged(seznam)     │   │
│         │            │               → ai_crawled                          │   │
│         │            └─────────────────────────────────────────────────────┘   │
│         │                                                                    │
│         ▼                                                                    │
│  ┌──────────────────┐     ┌────────────────────────────────────────────┐   │
│  │  CLOUDFLARE EDGE │     │         AI CRAWLER ANALYTICS LAYER         │   │
│  │  llms-worker.js  │────▶│  Cloudflare Worker logs → KV counters      │   │
│  │  (serves llms.txt)│     │  + periodic export to data/tracking/      │   │
│  └──────────────────┘     │  ai-crawler-analytics.json                  │   │
│                           └────────────────────────────────────────────┘   │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Component Boundaries

| Component | Responsibility | Communicates With |
|-----------|---------------|-------------------|
| `schedule-posts.py` | Picks approved articles, schedules on Blogger, triggers indexing | `lib.auth`, `lib.tracking`, `indexing-orchestrator.py` (new) |
| `indexing-orchestrator.py` (NEW) | Single entry point for all indexing submissions | IndexNow API, Yandex Webmaster API, Seznam Webmaster API, `lib.tracking` |
| `bing-sitemap-submit.py` (DEPRECATED) | ~~Submits to IndexNow~~ → **Refactor as IndexNow client lib** | `lib.tracking` (for pipeline status) |
| `seznam-api.py` (EXTEND) | Query Seznam indexing status, request reindex | `lib.tracking` (for status updates) |
| `yandex-api.py` (NEW) | Query Yandex indexing status, submit via IndexNow (same key) | `lib.tracking` |
| `llms-worker.js` (EXTEND) | Serve llms.txt + log AI crawler requests to Cloudflare KV | Cloudflare KV, periodic export script |
| `ai-crawler-analytics.py` (NEW) | Export Cloudflare KV logs → local JSON for reporting | `data/tracking/ai-crawler-analytics.json` |
| `analytics-report.py` (EXTEND) | Add indexing status + AI crawler metrics to daily report | `lib.tracking`, `data/tracking/*` |

---

## Patterns to Follow

### Pattern 1: Unified Indexing Orchestrator
**What:** Single script that submits to IndexNow (covers Bing, Yandex, Seznam, Naver) AND queries platform-specific webmaster APIs for status.
**When:** Any new article publish, content update, or manual reindex request.
**Example:**
```python
# scripts/indexing-orchestrator.py
#!/usr/bin/env python3
"""
Unified indexing submission + status tracking for all platforms.
Replaces bing-sitemap-submit.py and extends seznam-api.py.
"""
import json
import os
import sys
import urllib.request
from dataclasses import dataclass
from typing import Optional

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from lib.profile import SITE_URL, SITEMAP_URL
from lib.tracking import update_pipeline_status, load_json, save_json
from lib.utils import setup_logger

logger = setup_logger("indexing-orchestrator", log_file=os.path.join(
    os.path.dirname(SCRIPT_DIR), "data", "tracking", "indexing.log"
))

INDEXNOW_ENDPOINT = "https://api.indexnow.org/indexnow"
INDEXNOW_KEY_FILE = os.path.join(os.path.dirname(SCRIPT_DIR), "secrets", "indexnow-key.txt")

@dataclass
class IndexResult:
    platform: str          # "indexnow" | "yandex" | "seznam"
    success: bool
    status_code: Optional[int]
    details: dict

def load_indexnow_key() -> str:
    with open(INDEXNOW_KEY_FILE) as f:
        return f.read().strip()

def submit_to_indexnow(url: str, key: str) -> IndexResult:
    """Submit single URL to IndexNow (shared endpoint for Bing/Yandex/Seznam/Naver)."""
    host = SITE_URL.replace("https://", "").replace("/", "")
    key_location = f"{SITE_URL}/{key}.txt"
    
    payload = {
        "host": host,
        "key": key,
        "keyLocation": key_location,
        "urlList": [url]
    }
    
    req = urllib.request.Request(
        INDEXNOW_ENDPOINT,
        data=json.dumps(payload).encode(),
        headers={
            "Content-Type": "application/json; charset=utf-8",
            "User-Agent": "ayurshakti-indexing/1.0"
        },
        method="POST"
    )
    
    try:
        resp = urllib.request.urlopen(req, timeout=15)
        return IndexResult("indexnow", True, resp.status, {"response": resp.read().decode()})
    except urllib.error.HTTPError as e:
        return IndexResult("indexnow", False, e.code, {"error": e.read().decode()})
    except Exception as e:
        return IndexResult("indexnow", False, None, {"error": str(e)})

def submit_batch_to_indexnow(urls: list[str], key: str) -> IndexResult:
    """Submit up to 10,000 URLs in one POST."""
    host = SITE_URL.replace("https://", "").replace("/", "")
    key_location = f"{SITE_URL}/{key}.txt"
    
    payload = {"host": host, "key": key, "keyLocation": key_location, "urlList": urls}
    
    req = urllib.request.Request(
        INDEXNOW_ENDPOINT,
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json; charset=utf-8", "User-Agent": "ayurshakti-indexing/1.0"},
        method="POST"
    )
    try:
        resp = urllib.request.urlopen(req, timeout=30)
        return IndexResult("indexnow", True, resp.status, {"submitted": len(urls)})
    except Exception as e:
        return IndexResult("indexnow", False, None, {"error": str(e)})

def check_indexnow_status(url: str, key: str) -> dict:
    """Query Bing Webmaster Tools IndexNow insights (requires BWT API - separate OAuth)."""
    # For now, rely on pipeline status tracking; BWT API requires separate auth
    return {"platform": "indexnow", "url": url, "status": "submitted"}

def check_seznam_status(url: str) -> dict:
    """Query Seznam Webmaster API for document indexing status."""
    # Use existing seznam-api.py functions
    from scripts.seznam_api import get_document_info
    try:
        return get_document_info(url=url)
    except Exception as e:
        return {"platform": "seznam", "url": url, "error": str(e)}

def check_yandex_status(url: str) -> dict:
    """Query Yandex Webmaster API for indexing status."""
    # Yandex uses IndexNow for submissions; status via Yandex Webmaster API
    # Requires separate OAuth token - implement when key available
    return {"platform": "yandex", "url": url, "status": "pending_api_key"}

def orchestrate_indexing(url: str, title: str = "") -> dict:
    """Main entry point: submit to all platforms, update pipeline status."""
    key = load_indexnow_key()
    results = {}
    
    # 1. IndexNow (covers Bing + Yandex + Seznam + Naver)
    result = submit_to_indexnow(url, key)
    results["indexnow"] = result.__dict__
    update_pipeline_status(url, "pinged", "completed" if result.success else "failed", {
        "service": "indexnow",
        "status_code": result.status_code,
        "title": title
    })
    
    # 2. Seznam-specific status check (uses same IndexNow submission but separate API for insights)
    results["seznam_status"] = check_seznam_status(url)
    
    # 3. Yandex status (when API key available)
    results["yandex_status"] = check_yandex_status(url)
    
    return results

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Unified indexing orchestrator")
    parser.add_argument("--url", required=True, help="Article URL to submit")
    parser.add_argument("--title", default="", help="Article title for tracking")
    parser.add_argument("--batch", nargs="+", help="Batch submit multiple URLs")
    args = parser.parse_args()
    
    if args.batch:
        key = load_indexnow_key()
        result = submit_batch_to_indexnow(args.batch, key)
        print(json.dumps(result.__dict__, indent=2))
    else:
        result = orchestrate_indexing(args.url, args.title)
        print(json.dumps(result, indent=2))
```

### Pattern 2: Pipeline Status Extension for Multi-Platform Indexing
**What:** Extend `lib/tracking.py` pipeline stages to track each platform separately.
**When:** Every article publish triggers multi-platform indexing.
**Example:**
```python
# In lib/tracking.py - extend VALID_STAGES
VALID_STAGES = (
    "scheduled", 
    "published", 
    "social-posted", 
    "pinged",           # legacy - keep for backward compat
    "pinged-indexnow",  # NEW - IndexNow (Bing/Yandex/Seznam/Naver)
    "pinged-seznam",    # NEW - Seznam Webmaster API status
    "pinged-yandex",    # NEW - Yandex Webmaster API status  
    "ai-crawled"        # NEW - AI crawler detection
)
```

### Pattern 3: Cloudflare Worker AI Crawler Logging
**What:** Extend `llms-worker.js` to log AI crawler requests to Cloudflare KV with counters.
**When:** Every request to `/llms.txt` or any page by known AI user agents.
**Example:**
```javascript
// scripts/llms-worker.js (extended)
export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const ua = request.headers.get('user-agent') || '';
    
    // AI crawler detection
    const AI_BOTS = [
      'GPTBot', 'OAI-SearchBot', 'ChatGPT-User',
      'ClaudeBot', 'anthropic-ai', 'Claude-Web',
      'PerplexityBot', 'Perplexity-User',
      'Google-Extended', 'GoogleOther',
      'Applebot-Extended', 'CCBot', 'Bytespider',
      'Meta-ExternalAgent', 'PetalBot', 'DuckAssistBot'
    ];
    
    const matchedBot = AI_BOTS.find(bot => ua.includes(bot));
    
    if (matchedBot) {
      // Log to Cloudflare KV for analytics
      const key = `ai_crawler:${matchedBot}:${new Date().toISOString().split('T')[0]}`;
      const current = await env.AI_CRAWLER_KV.get(key, { type: 'json' }) || { count: 0, urls: [] };
      current.count++;
      current.urls.push(url.pathname);
      // Keep last 100 URLs per day per bot
      if (current.urls.length > 100) current.urls = current.urls.slice(-100);
      await env.AI_CRAWLER_KV.put(key, JSON.stringify(current), { expirationTtl: 86400 * 30 });
      
      // Also log to console for wrangler tail / real-time debugging
      console.log(JSON.stringify({
        type: 'ai_crawler',
        bot: matchedBot,
        url: request.url,
        ip: request.headers.get('CF-Connecting-IP'),
        ts: new Date().toISOString()
      }));
    }
    
    // Serve llms.txt
    if (url.pathname === "/llms.txt") {
      return new Response(llmsContent, {
        headers: {
          "content-type": "text/plain; charset=utf-8",
          "cache-control": "public, max-age=86400"
        }
      });
    }
    
    return new Response("Not Found", { status: 404 });
  }
};

const llmsContent = `...`; // existing content
```

### Pattern 4: Periodic Analytics Export Script
**What:** Python script runs via cron to pull Cloudflare KV analytics → local JSON for reporting.
**When:** Daily cron (e.g., 03:00 EST) via `schedule-config.json` or separate cron.
**Example:**
```python
# scripts/ai-crawler-analytics.py
#!/usr/bin/env python3
"""Export Cloudflare KV AI crawler logs to local tracking JSON."""
import os, sys, json, subprocess
from datetime import datetime, timezone

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from lib.tracking import TRACKING_DIR, load_json, save_json

ANALYTICS_PATH = os.path.join(TRACKING_DIR, "ai-crawler-analytics.json")

def export_from_cloudflare():
    """Use wrangler to fetch KV data. Requires CLOUDFLARE_API_TOKEN in env."""
    # List all keys with prefix ai_crawler:
    result = subprocess.run(
        ["wrangler", "kv:key", "list", "--binding", "AI_CRAWLER_KV", "--prefix", "ai_crawler:"],
        capture_output=True, text=True, timeout=60
    )
    if result.returncode != 0:
        return {"error": result.stderr}
    
    keys = json.loads(result.stdout)
    analytics = {"exported_at": datetime.now(timezone.utc).isoformat(), "bots": {}}
    
    for key_info in keys:
        key = key_info["name"]
        # Fetch value
        val_result = subprocess.run(
            ["wrangler", "kv:key", "get", "--binding", "AI_CRAWLER_KV", key],
            capture_output=True, text=True, timeout=30
        )
        if val_result.returncode == 0:
            try:
                data = json.loads(val_result.stdout)
                # Parse key: ai_crawler:GPTBot:2026-07-12
                parts = key.split(":")
                if len(parts) == 3:
                    bot = parts[1]
                    date = parts[2]
                    analytics["bots"].setdefault(bot, {})[date] = data
            except json.JSONDecodeError:
                pass
    
    return analytics

def main():
    analytics = export_from_cloudflare()
    # Merge with existing history
    history = load_json(ANALYTICS_PATH, {"exports": []})
    history.setdefault("exports", []).append(analytics)
    # Keep last 90 exports
    if len(history["exports"]) > 90:
        history["exports"] = history["exports"][-90:]
    save_json(ANALYTICS_PATH, history)
    print(json.dumps(analytics, indent=2))

if __name__ == "__main__":
    main()
```

---

## Anti-Patterns to Avoid

### Anti-Pattern 1: Separate Scripts Per Search Engine
**What:** Maintaining `bing-submit.py`, `yandex-submit.py`, `seznam-submit.py` independently.
**Why bad:** IndexNow is a *shared protocol* — one POST to `api.indexnow.org` notifies all participating engines. Duplicate submissions waste quota and create inconsistent state.
**Instead:** Single `indexing-orchestrator.py` submits to IndexNow endpoint once; platform-specific status queries are separate read-only operations.

### Anti-Pattern 2: Hardcoding API Keys in Scripts
**What:** `api_key = "xxx"` directly in Python files.
**Why bad:** Keys rotate, secrets leak in git history, different environments need different keys.
**Instead:** All secrets in `secrets/` directory (gitignored), loaded via `lib.profile` or direct file read. Use `indexnow-key.txt` for IndexNow, `yandex-api-key.txt` for Yandex Webmaster API.

### Anti-Pattern 3: Losing Pipeline Visibility After Scheduler
**What:** `schedule-posts.py` calls `bing-sitemap-submit.py` via subprocess but doesn't track per-platform success/failure in pipeline status.
**Why bad:** Can't answer "was this article indexed by Yandex?" without checking logs manually.
**Instead:** `indexing-orchestrator.py` updates `pipeline-status.json` with granular stages (`pinged-indexnow`, `pinged-seznam`, `pinged-yandex`, `ai-crawled`).

### Anti-Pattern 4: Relying Only on GA4/GSC for AI Crawler Visibility
**What:** Assuming Google Analytics shows GPTBot/ClaudeBot traffic.
**Why bad:** AI crawlers don't execute JavaScript → invisible to GA4. Must use server logs or Cloudflare Workers.
**Instead:** Cloudflare Worker logs to KV → daily export → merged into `analytics-report.py` output.

---

## Scalability Considerations

| Concern | At 100 articles | At 1,000 articles | At 10,000 articles |
|---------|-----------------|-------------------|---------------------|
| **IndexNow batch size** | Single URL POST per article | Batch 50-100 URLs per scheduler run | Batch 10,000 URLs (max per request), multiple batches |
| **Pipeline status JSON** | ~50 KB | ~500 KB | ~5 MB — consider splitting by month or SQLite |
| **AI crawler KV keys** | ~30 keys/day (3 bots × 10 pages) | ~300 keys/day | ~3,000 keys/day — TTL 30 days keeps it bounded |
| **Seznam/Yandex API calls** | 1-2 per article | 10-20 per day | Rate limit awareness — cache status 24h |
| **Analytics report generation** | <1 sec | ~5 sec | ~30 sec — add `--incremental` flag |

**Batch IndexNow Submission Strategy:**
```python
# In schedule-posts.py, after scheduling N articles:
urls_to_submit = [f"https://www.ayurshakti.shop/{p['url']}" for p in scheduled_posts]
if urls_to_submit:
    result = submit_batch_to_indexnow(urls_to_submit, key)
    # Single API call notifies all engines for all articles
```

---

## Data Flow Summary

### 1. Article Publish → Indexing Submission
```
schedule-posts.py 
  → publishes to Blogger (GET article URL)
  → calls indexing-orchestrator.py --url <URL> --title "<title>"
  → indexing-orchestrator.py:
      → POST to api.indexnow.org/indexnow (single call for all engines)
      → update_pipeline_status(url, "pinged-indexnow", "completed/failed", details)
      → query Seznam Webmaster API for document status
      → update_pipeline_status(url, "pinged-seznam", "completed/failed", details)
      → (when Yandex API key available) query Yandex Webmaster API
      → update_pipeline_status(url, "pinged-yandex", ...)
  → schedule-posts.py continues: ping services, social post, analytics
```

### 2. Indexing Status Monitoring (Daily/On-Demand)
```
analytics-report.py --days 7 --save
  → fetches GA4 + GSC (existing)
  → loads pipeline-status.json
  → computes indexing success rate per platform
  → loads ai-crawler-analytics.json (from KV export)
  → prints unified report with AI crawler activity
  → saves to analytics-history.json
```

### 3. AI Crawler Analytics Collection
```
User requests any page → Cloudflare Worker (llms-worker.js or main worker)
  → detects AI user-agent (GPTBot, ClaudeBot, PerplexityBot, etc.)
  → increments KV counter: ai_crawler:{bot}:{date} → {count, urls[]}
  → logs to console (wrangler tail)
  
Daily cron (03:00 EST):
  → ai-crawler-analytics.py exports KV → data/tracking/ai-crawler-analytics.json
  → analytics-report.py includes AI crawler summary
```

### 4. llms.txt Serving (Edge)
```
GET /llms.txt → Cloudflare Worker (llms-worker.js)
  → Returns static llms.txt content (cached at edge, 24h TTL)
  → Logs AI crawler UA if detected
  → No origin hit — purely edge-served
```

---

## Sources

- [IndexNow Official Documentation](https://www.indexnow.org/documentation) — Protocol spec, endpoints, response codes
- [Bing IndexNow API Documentation](https://www.bing.com/webmasters/help/indexnow-0z209wby) — Bing-specific endpoints, limits, dashboard
- [Yandex IndexNow Reference](https://yandex.com/support/webmaster/en/indexnow/reference) — Key verification, API request format
- [Seznam Webmaster API](https://reporter.seznam.cz/wm/) — Document status, reindex, history endpoints
- [Cloudflare AI Crawl Control](https://developers.cloudflare.com/ai-crawl-control/) — Bot Management, WAF rules for AI crawlers
- [Monitor AI Crawler Server Logs](https://www.citeflow.io/blog/monitor-ai-crawler-server-logs) — User agent reference, log analysis patterns
- [llms.txt Proposal](https://answer.ai/blog/llms-txt-proposal) — Standard specification, adoption metrics
- [IndexNow Bulk Submitter](https://indexnowtool.com/tools/bulk-url-submitter) — 10,000 URL limit, POST structure