#!/usr/bin/env python3
"""
Phase 2 - Ping Service Notifier for ayurshakti.shop
Notifies 3 active search engines & blog aggregators about new content.
Auto-called by schedule-posts.py after each publish.

Usage:
  python3 scripts/notify-ping.py                    # Ping sitemap URL
  python3 scripts/notify-ping.py --url ARTICLE_URL  # Ping specific article
  python3 scripts/notify-ping.py --dry-run          # Preview without pinging
"""
import json
import os
import sys
import urllib.parse
import urllib.request
import xmlrpc.client

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(SCRIPT_DIR, "lib"))
from lib.profile import SITE_NAME, SITE_URL, SITEMAP_URL
from lib.tracking import update_pipeline_status
from lib.utils import dry_run_check, setup_logger

# Only 3 active ping services (per D-10, R-075)
PING_SERVICES = [
    {
        "name": "IndexNow (Bing/Yandex/Seznam)",
        "url": "https://api.indexnow.org/indexnow",
        "type": "post",
    },
    {
        "name": "Ping-O-Matic",
        "url": "http://rpc.pingomatic.com/",
        "type": "xmlrpc",
    },
    {
        "name": "Weblogs.com",
        "url": "http://rpc.weblogs.com/ping",
        "type": "xmlrpc",
    },
]

# 5 second timeout for all requests
TIMEOUT = 5

logger = setup_logger("notify-ping")


def ping_post(service_name, url, article_url):
    """Ping IndexNow via POST with JSON payload."""
    try:
        # IndexNow requires key and host - using a placeholder key location
        key_location = f"https://{SITE_URL.replace('https://', '').replace('/', '')}/key.txt"
        payload = {
            "host": SITE_URL.replace("https://", "").replace("/", ""),
            "key": "ayurshakti-key",  # In production, load from config/secrets
            "keyLocation": key_location,
            "urlList": [article_url],
        }
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            url,
            data=data,
            headers={
                "User-Agent": "ayurshakti-ping/1.0",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        resp = urllib.request.urlopen(req, timeout=TIMEOUT)
        return resp.status in (200, 202)
    except Exception as e:
        logger.warning(f"  ❌ {service_name} failed: {e}")
        return False


def ping_xmlrpc(service_name, url):
    """Ping via XML-RPC (Ping-O-Matic, Weblogs.com)."""
    try:
        proxy = xmlrpc.client.ServerProxy(url, allow_none=True, verbose=False)
        proxy.weblogUpdates.ping(SITE_NAME, SITE_URL)
        return True
    except Exception as e:
        logger.warning(f"  ❌ {service_name} failed: {e}")
        return False


def notify(url_to_ping):
    """Ping all active services with the given URL."""
    success = 0
    failed = 0

    for svc in PING_SERVICES:
        try:
            if svc["type"] == "post":
                ok = ping_post(svc["name"], svc["url"], url_to_ping)
            else:
                ok = ping_xmlrpc(svc["name"], svc["url"])

            if ok:
                logger.info(f"  ✅ {svc['name']}: OK")
                success += 1
            else:
                failed += 1
        except Exception as e:
            logger.warning(f"  ❌ {svc['name']} error: {e}")
            failed += 1

    # Update pipeline status for pinged stage
    update_pipeline_status(url_to_ping, 'pinged', 'completed' if success > 0 else 'failed', {
        'services_success': success,
        'services_failed': failed
    })

    return success, failed


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Ping search engines and aggregators")
    parser.add_argument(
        "--url", default=SITEMAP_URL, help="Article URL to ping (default: sitemap)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview actions without making API calls",
    )
    args = parser.parse_args()

    # Dry-run check (also checks sys.argv via utils.dry_run_check)
    if dry_run_check(f"ping {len(PING_SERVICES)} services with {args.url}"):
        logger.info("  Services that would be pinged:")
        for svc in PING_SERVICES:
            logger.info(f"    - {svc['name']} ({svc['type'].upper()})")
        sys.exit(0)

    logger.info(f"Pinging {len(PING_SERVICES)} services with: {args.url}")
    s, f = notify(args.url)
    logger.info(f"  Success: {s}, Failed: {f}")