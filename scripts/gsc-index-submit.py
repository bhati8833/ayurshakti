#!/usr/bin/env python3
"""
Google Search Console indexing for ayurshakti.shop

Primary : Google Indexing API (instant ping on publish)
          -> indexing.googleapis.com/v3/urlNotifications:publish
Secondary: GSC sitemap submission via Webmaster API (automates TASK-013)

Auth: service account (secrets/ayurshakti-501603-*.json) with the
      https://www.googleapis.com/auth/indexing scope.

Usage:
  python3 scripts/gsc-index-submit.py                   # submit sitemap.xml to GSC
  python3 scripts/gsc-index-submit.py --url ARTICLE_URL  # ping a single URL
"""
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from lib.profile import SITE_URL, SITEMAP_URL
from lib.tracking import update_pipeline_status

SECRETS_DIR = os.path.normpath(os.path.join(SCRIPT_DIR, "..", "secrets"))
SA_KEY_PATH = os.path.join(SECRETS_DIR, "ayurshakti-501603-a1a6ff0396df.json")
SCOPES = [
    "https://www.googleapis.com/auth/indexing",
    "https://www.googleapis.com/auth/webmasters",
]
GSC_SITE = "sc-domain:ayurshakti.shop"
INDEXING_URL = "https://indexing.googleapis.com/v3/urlNotifications:publish"
GSC_SITEMAP_API = (
    "https://www.googleapis.com/webmasters/v3/sites/{site}/sitemaps/{feed}"
)


def _get_token():
    from google.oauth2 import service_account
    from google.auth.transport.requests import Request

    creds = service_account.Credentials.from_service_account_file(
        SA_KEY_PATH, scopes=SCOPES
    )
    creds.refresh(Request())
    return creds.token


def notify_index(url, max_retries=3):
    """Ping Google Indexing API for a single URL. Returns bool success."""
    try:
        token = _get_token()
    except Exception as e:
        print(f"  Google Indexing API: auth failed ({e})")
        return False

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    payload = json.dumps({"url": url, "type": "URL_UPDATED"}).encode()
    last_body = ""
    for attempt in range(max_retries):
        req = urllib.request.Request(
            INDEXING_URL, data=payload, headers=headers, method="POST"
        )
        try:
            resp = urllib.request.urlopen(req, timeout=20)
            print(f"  Google Indexing API: OK ({resp.status}) {url}")
            update_pipeline_status(
                url, "indexing", "completed",
                {"service": "google", "status_code": resp.status},
            )
            return True
        except urllib.error.HTTPError as e:
            last_body = e.read().decode()[:300]
            if e.code == 429:
                wait = 2 ** attempt
                print(f"  Google Indexing API: 429 rate limited, retry in {wait}s")
                time.sleep(wait)
                continue
            if e.code == 403:
                print(f"  Google Indexing API: 403 NOT VERIFIED in GSC "
                      f"({GSC_SITE}). Check ownership. {last_body}")
                break
            print(f"  Google Indexing API: FAILED ({e.code}) {last_body}")
            break
    update_pipeline_status(
        url, "indexing", "failed",
        {"service": "google", "error": last_body or "exhausted retries"},
    )
    return False


def submit_sitemap():
    """Submit sitemap.xml to GSC via Webmaster API. Returns bool success."""
    try:
        token = _get_token()
    except Exception as e:
        print(f"  GSC sitemap submit: auth failed ({e})")
        return False

    site = urllib.parse.quote(GSC_SITE, safe="")
    feed = urllib.parse.quote(SITEMAP_URL, safe="")
    url = GSC_SITEMAP_API.format(site=site, feed=feed)
    req = urllib.request.Request(
        url, data=b"", headers={"Authorization": f"Bearer {token}"}, method="PUT"
    )
    try:
        resp = urllib.request.urlopen(req, timeout=20)
        print(f"  GSC sitemap submitted: OK ({resp.status}) {SITEMAP_URL}")
        return True
    except urllib.error.HTTPError as e:
        body = e.read().decode()[:300]
        print(f"  GSC sitemap submit: FAILED ({e.code}) {body}")
        return False


if __name__ == "__main__":
    if "--url" in sys.argv:
        idx = sys.argv.index("--url") + 1
        if idx < len(sys.argv):
            ok = notify_index(sys.argv[idx])
            sys.exit(0 if ok else 1)
    else:
        ok = submit_sitemap()
        sys.exit(0 if ok else 1)
