#!/usr/bin/env python3
"""
Bing IndexNow Submitter for ayurshakti.shop
Uses IndexNow API (supported by Bing, Yandex, Seznam)
Usage:
  python3 scripts/bing-sitemap-submit.py                    # Submit sitemap URL
  python3 scripts/bing-sitemap-submit.py --url ARTICLE_URL  # Submit single article
"""
import json
import os
import sys
import urllib.request

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from lib.profile import SITE_URL, SITEMAP_URL
from lib.tracking import update_pipeline_status

SECRETS_DIR = os.path.join(SCRIPT_DIR, "..", "secrets")

def get_api_key():
    path = os.path.join(SECRETS_DIR, "bing-client-credentials.json")
    with open(path) as f:
        return json.load(f)["api_key"]

def submit_to_indexnow(api_key, url_to_submit):
    payload = {
        "host": "www.ayurshakti.shop",
        "key": api_key,
        "keyLocation": f"{SITE_URL}/indexnow-key.txt",
        "urlList": [url_to_submit]
    }
    req = urllib.request.Request(
        "https://api.indexnow.org/indexnow",
        data=json.dumps(payload).encode(),
        headers={
            "Content-Type": "application/json; charset=utf-8",
            "User-Agent": "ayurshakti-bing-submit/1.0"
        },
        method="POST"
    )
    try:
        resp = urllib.request.urlopen(req, timeout=15)
        print(f"Submitted to IndexNow: {url_to_submit}")
        print(f"   Response: {resp.status}")
        # Update pipeline status
        update_pipeline_status(url_to_submit, 'pinged', 'completed', {
            'service': 'indexnow',
            'status_code': resp.status
        })
        return True
    except Exception as e:
        print(f"Submission failed: {e}")
        update_pipeline_status(url_to_submit, 'pinged', 'failed', {
            'service': 'indexnow',
            'error': str(e)
        })
        return False

if __name__ == "__main__":
    api_key = get_api_key()
    if "--url" in sys.argv:
        idx = sys.argv.index("--url") + 1
        if idx < len(sys.argv):
            submit_to_indexnow(api_key, sys.argv[idx])
    else:
        submit_to_indexnow(api_key, SITEMAP_URL)
