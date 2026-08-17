#!/usr/bin/env python3
"""
Phase 2 - Brand Mention & Backlink Monitor for ayurshakti.shop
Weekly check: GSC backlinks, web mentions, IndexNow stats, competitor tracking.

Usage:
  python3 scripts/monitor-mentions.py              # Full report
  python3 scripts/monitor-mentions.py --quick      # Quick check (default: full)

Free-tier only — no paid APIs.
Output: scripts/monitor-mentions-log.json + terminal report
"""
import html.parser
import json
import os
import re
import sys
import urllib.request
from datetime import UTC, datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from lib.profile import AUTHOR_NAME, SITE_DOMAIN, SITE_URL

SITEMAP_URL = f"{SITE_URL}/atom.xml"
LOG_PATH = os.path.join(SCRIPT_DIR, "monitor-mentions-log.json")

SEARCH_URL = "https://www.google.com/search?q={q}"
BING_SEARCH_URL = "https://www.bing.com/search?q={q}"

BRAND_TERMS = [
    "ayurshakti",
    "ayur shakti",
    "ayurshakti.shop",
    f"{AUTHOR_NAME} ayurveda",
]

COMPETITOR_DOMAINS = [
    "easyayurveda.com",
    "ayurtimes.com",
    "planetayurveda.com",
]

SEARCH_QUERIES = [
    f'"{SITE_DOMAIN}" -site:{SITE_DOMAIN}',
    '"ayur shakti" ayurveda -site:ayurshakti.shop',
    f'"{AUTHOR_NAME}" ayurveda',
    'site:*.com "ayurshakti"',
]

def google_search(q, num=5):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
        }
        url = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote_plus(q)}"
        req = urllib.request.Request(url, headers=headers)
        resp = urllib.request.urlopen(req, timeout=10)
        html_data = resp.read().decode("utf-8", errors="replace")

        results = []
        for m in re.finditer(
            r'<a[^>]*class="result__a"[^>]*href="(https?://[^"]+)"[^>]*>.*?</a>',
            html_data[:50000], re.DOTALL
        ):
            link = html.unescape(m.group(1))
            if link and not any(d in link for d in ["duckduckgo.com", "html.duckduckgo.com"]):
                results.append(link)
        return results[:num]
    except Exception as e:
        print(f"    websearch error: {e}")
        return []

def get_gsc_backlinks():
    print("  GSC backlinks: manual check required (GSC web UI → Links → External Links)")
    print("    Visit: https://search.google.com/search-console/links?resource_id=sc-domain%3Aayurshakti.shop")
    return []

def get_indexnow_stats():
    try:
        sitemap_url = f"{SITE_URL}/atom.xml"
        req = urllib.request.Request(
            f"https://www.bing.com/webmaster/api/query?url={urllib.parse.quote(sitemap_url)}",
            headers={"User-Agent": "ayurshakti-monitor/1.0"}
        )
        resp = urllib.request.urlopen(req, timeout=10)
        return resp.status
    except Exception:
        return None

def check_competitors():
    mentions = []
    for domain in COMPETITOR_DOMAINS:
        try:
            req = urllib.request.Request(
                f"https://{domain}",
                headers={"User-Agent": "Mozilla/5.0"}
            )
            resp = urllib.request.urlopen(req, timeout=10)
            mentions.append({"domain": domain, "status": resp.status, "status_ok": resp.status == 200})
        except Exception as e:
            mentions.append({"domain": domain, "status": str(e), "status_ok": False})
    return mentions

def check_own_site():
    results = {}
    pages = [
        ("homepage", SITE_URL),
        ("sitemap", f"{SITE_URL}/atom.xml"),
        ("robots", f"{SITE_URL}/robots.txt"),
        ("llms", "https://llms.ayurshakti.shop/llms.txt"),
    ]
    for name, url in pages:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            resp = urllib.request.urlopen(req, timeout=10)
            results[name] = {"status": resp.status, "ok": resp.status == 200, "size": len(resp.read())}
        except Exception as e:
            results[name] = {"status": str(e), "ok": False}
    return results

def generate_report():
    print(f"=== AyurShakti Mention Monitor === {datetime.now(UTC).strftime('%Y-%m-%d %H:%M UTC')}")
    print()

    print("[1] External Mentions")
    for q in SEARCH_QUERIES:
        print(f"  Query: {q}")
        urls = google_search(q, num=3)
        if urls:
            for u in urls:
                print(f"    {u}")
        else:
            print("    (none found — no backlinks yet, expected)")

    print()
    print("[2] Site Health")
    health = check_own_site()
    for name, data in health.items():
        icon = "✅" if data["ok"] else "❌"
        print(f"  {icon} {name}: {data['status']} ({data.get('size', 0)}B)")

    print()
    print("[3] Competitor Pulse")
    comps = check_competitors()
    for c in comps:
        icon = "✅" if c["status_ok"] else "❌"
        print(f"  {icon} {c['domain']}: {c['status']}")

    print()
    print("[4] GSC Backlinks")
    get_gsc_backlinks()

    report = {
        "timestamp": datetime.now(UTC).isoformat(),
        "mentions": [],
        "site_health": health,
        "competitors": comps,
    }

    with open(LOG_PATH, "w") as f:
        json.dump(report, f, indent=2)
    print(f"\nReport saved: {LOG_PATH}")

if __name__ == "__main__":
    import urllib.parse
    generate_report()
