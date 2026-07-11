#!/usr/bin/env python3
"""
Social Auto-Poster for ayurshakti.shop
Posts to Bluesky, X/Twitter, Pinterest APIs. Queues LinkedIn for browser agent.
Integrates with tracking system (article-registry.json, api-usage-log.json, pipeline-status.json).

Usage:
  python3 scripts/social-post.py --url ARTICLE_URL --title "Article Title"
"""

import base64
import hashlib
import hmac
import json
import os
import random
import sys
import time
from datetime import UTC, datetime
from urllib.parse import quote_plus, urlparse

import requests
from requests.auth import AuthBase

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from lib.profile import SITE_NAME
from lib.tracking import (
    check_api_usage,
    increment_api_usage,
    update_article_registry,
    update_pipeline_status,
    load_json,
    save_json,
)

SECRETS_DIR = os.path.normpath(os.path.join(SCRIPT_DIR, "..", "secrets"))
TRACKING_DIR = os.path.normpath(os.path.join(SCRIPT_DIR, "..", "data", "tracking"))
SITE_HANDLE = "ayurshakti.bsky.social"

ARTICLE_REGISTRY_PATH = os.path.join(TRACKING_DIR, "article-registry.json")
API_LOG_PATH = os.path.join(TRACKING_DIR, "api-usage-log.json")


# --- OAuth 1.0a for X/Twitter ---

class TwitterOAuth1(AuthBase):
    def __init__(self, consumer_key, consumer_secret, access_token, access_token_secret):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_token = access_token
        self.access_token_secret = access_token_secret

    def __call__(self, r):
        timestamp = str(int(time.time()))
        nonce = str(random.randint(0, 10**10))
        params = {
            "oauth_consumer_key": self.consumer_key,
            "oauth_nonce": nonce,
            "oauth_signature_method": "HMAC-SHA1",
            "oauth_timestamp": timestamp,
            "oauth_token": self.access_token,
            "oauth_version": "1.0"
        }
        parsed = urlparse(r.url)
        base_url = f"{parsed.scheme}://{parsed.hostname}{parsed.path}"
        param_str = "&".join(
            f"{quote_plus(k)}={quote_plus(v)}"
            for k, v in sorted(params.items())
        )
        sig_base = f"{r.method}&{quote_plus(base_url)}&{quote_plus(param_str)}"
        signing_key = f"{quote_plus(self.consumer_secret)}&{quote_plus(self.access_token_secret)}"
        signature = base64.b64encode(
            hmac.new(signing_key.encode(), sig_base.encode(), hashlib.sha1).digest()
        ).decode()
        params["oauth_signature"] = signature
        auth_header = "OAuth " + ", ".join(
            f'{k}="{quote_plus(v)}"' for k, v in params.items()
        )
        r.headers["Authorization"] = auth_header
        return r


# --- Platform posters ---

def post_bluesky(url, title):
    if not check_api_usage("bluesky_api"):
        return False
    creds_path = os.path.join(SECRETS_DIR, "bluesky-creds.json")
    if not os.path.exists(creds_path):
        print("  Bluesky: creds not found")
        return False
    try:
        with open(creds_path) as f:
            creds = json.load(f)
        identifier = creds.get("identifier", SITE_HANDLE)
        password = creds.get("password", "")
        if not password:
            print("  Bluesky: password empty")
            return False

        resp = requests.post(
            "https://bsky.social/xrpc/com.atproto.server.createSession",
            json={"identifier": identifier, "password": password},
            timeout=15
        )
        resp.raise_for_status()
        session = resp.json()
        token = session["accessJwt"]
        did = session["did"]

        text = f"{title}\n\n{url}"
        facet_uri = {
            "$type": "app.bsky.richtext.facet",
            "features": [{"$type": "app.bsky.richtext.facet#link", "uri": url}],
            "index": {"byteStart": len(text) - len(url), "byteEnd": len(text)}
        }
        resp2 = requests.post(
            "https://bsky.social/xrpc/com.atproto.repo.createRecord",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "repo": did, "collection": "app.bsky.feed.post",
                "record": {
                    "$type": "app.bsky.feed.post",
                    "text": text,
                    "createdAt": datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%S.000Z"),
                    "facets": [facet_uri]
                }
            },
            timeout=15
        )
        resp2.raise_for_status()
        print("  Bluesky: posted")
        increment_api_usage("bluesky_api")
        return True
    except Exception as e:
        print(f"  Bluesky: failed ({e})")
        return False


def post_x(url, title):
    if not check_api_usage("x_api"):
        return False
    creds_path = os.path.join(SECRETS_DIR, "x-creds.json")
    if not os.path.exists(creds_path):
        print("  X: creds not found")
        return False
    try:
        with open(creds_path) as f:
            creds = json.load(f)
        auth = TwitterOAuth1(
            creds["consumer_key"], creds["consumer_secret"],
            creds["access_token"], creds["access_token_secret"]
        )
        text = f"{title}\n\n{url}"
        resp = requests.post(
            "https://api.twitter.com/2/tweets",
            auth=auth,
            json={"text": text},
            timeout=15
        )
        resp.raise_for_status()
        print("  X (Twitter): posted")
        increment_api_usage("x_api")
        return True
    except Exception as e:
        print(f"  X (Twitter): failed ({e})")
        return False


def post_pinterest(url, title):
    if not check_api_usage("pinterest_api"):
        return False
    creds_path = os.path.join(SECRETS_DIR, "pinterest-creds.json")
    if not os.path.exists(creds_path):
        print("  Pinterest: creds not found")
        return False
    try:
        with open(creds_path) as f:
            creds = json.load(f)
        access_token = creds.get("access_token", "")
        if not access_token:
            print("  Pinterest: access_token empty")
            return False

        board_id = os.environ.get("PINTEREST_BOARD_ID", "944982003002747285")
        resp = requests.post(
            "https://api.pinterest.com/v5/pins",
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            },
            json={
                "title": title,
                "description": f"{title}\n\nVisit: {url}",
                "link": url,
                "alt_text": title[:500],
                "board_id": board_id
            },
            timeout=15
        )
        resp.raise_for_status()
        print("  Pinterest: posted")
        increment_api_usage("pinterest_api")
        return True
    except Exception as e:
        print(f"  Pinterest: failed ({e})")
        return False


def signal_agent(platform, url, title):
    log_path = os.path.join(SCRIPT_DIR, "agent-pending-posts.json")
    pending = []
    if os.path.exists(log_path):
        try:
            with open(log_path) as f:
                pending = json.load(f)
        except (json.JSONDecodeError, Exception):
            pending = []
    pending.append({
        "platform": platform, "url": url,
        "title": title,
        "timestamp": datetime.now(UTC).isoformat()
    })
    with open(log_path, "w") as f:
        json.dump(pending, f, indent=2)
    print(f"  {platform}: queued in agent-pending-posts.json")


def post_all(url, title):
    print(f"Social posting: {title}")
    results = {}
    results["bluesky"] = post_bluesky(url, title)
    results["x"] = post_x(url, title)
    results["pinterest"] = post_pinterest(url, title)
    signal_agent("LinkedIn", url, title)
    signal_agent("Medium", url, title)

    # Update pipeline status for social-posted stage
    any_success = any(results.values())
    platform_details = {}
    for platform, success in results.items():
        if success:
            platform_details[platform] = {"status": "completed"}
        else:
            platform_details[platform] = {"status": "failed"}

    update_pipeline_status(url, 'social-posted', 'completed' if any_success else 'failed', {
        'platforms': platform_details,
        'title': title
    })

    for platform, success in results.items():
        if success:
            update_article_registry({"id": url, "title": title, "url": url}, "Published", None)
    return results


if __name__ == "__main__":
    url = None
    title = None
    for i, arg in enumerate(sys.argv):
        if arg == "--url" and i + 1 < len(sys.argv):
            url = sys.argv[i + 1]
        if arg == "--title" and i + 1 < len(sys.argv):
            title = sys.argv[i + 1]
    if not url:
        print("Usage: python3 scripts/social-post.py --url URL --title TITLE")
        sys.exit(1)
    post_all(url, title or f"New article at {SITE_NAME}")
