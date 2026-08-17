#!/usr/bin/env python3
"""
Bing submission for ayurshakti.shop

Primary : Bing Webmaster URL Submission API v2 (SubmitUrlbatch) using the API key.
Secondary: IndexNow (api.indexnow.org) -> Bing, Yandex, Seznam.
Fallback : Web-based ping (bing.com/webmaster/ping.aspx).

Usage:
  python3 scripts/bing-sitemap-submit.py                  # Submit sitemap URL
  python3 scripts/bing-sitemap-submit.py --url ARTICLE_URL  # Submit single article
"""
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from lib.profile import SITE_URL, SITEMAP_URL, SITE_DOMAIN
from lib.tracking import update_pipeline_status

SECRETS_DIR = os.path.join(SCRIPT_DIR, "..", "secrets")


def get_api_key():
    txt = os.path.join(SECRETS_DIR, "bing-api-key.txt")
    if os.path.exists(txt):
        with open(txt) as f:
            key = f.read().strip()
            if key:
                return key
    json_path = os.path.join(SECRETS_DIR, "bing-client-credentials.json")
    if os.path.exists(json_path):
        with open(json_path) as f:
            return json.load(f).get("api_key", "").strip()
    raise FileNotFoundError("Bing API key not found (secrets/bing-api-key.txt)")


def _http_post(url, payload, headers):
    data = json.dumps(payload).encode()
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    try:
        resp = urllib.request.urlopen(req, timeout=20)
        return resp.status, resp.read().decode()
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()
    except Exception as e:  # network / timeout
        return None, str(e)


def submit_via_webmaster_api(api_key, url_list):
    """Bing Webmaster Tools URL Submission API (json protocol)."""
    payload = {"siteUrl": SITE_URL.rstrip("/"), "urlList": url_list}
    endpoint = (
        "https://ssl.bing.com/webmaster/api.svc/json/SubmitUrlbatch"
        f"?apikey={urllib.parse.quote(api_key)}"
    )
    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "User-Agent": "ayurshakti-bing/1.0",
    }
    status, body = _http_post(endpoint, payload, headers)
    ok = status in (200, 204)
    print(f"  Bing Webmaster API: {'OK' if ok else 'FAILED'} "
          f"(status={status}) {body[:200]}")
    return ok, status


def submit_via_indexnow(api_key, url_list):
    """IndexNow protocol -> Bing, Yandex, Seznam."""
    payload = {
        "host": SITE_DOMAIN,
        "key": api_key,
        "keyLocation": f"{SITE_URL.rstrip('/')}/indexnow-key.txt",
        "urlList": url_list,
    }
    endpoint = "https://api.indexnow.org/indexnow"
    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "User-Agent": "ayurshakti-indexnow/1.0",
    }
    status, body = _http_post(endpoint, payload, headers)
    ok = status in (200, 202)
    print(f"  IndexNow: {'OK' if ok else 'FAILED'} "
          f"(status={status}) {body[:200]}")
    return ok, status


def submit_via_ping(url_to_submit):
    """Web-based fallback: notify Bing via the ping endpoint."""
    endpoint = (
        "https://www.bing.com/webmaster/ping.aspx?siteMap="
        f"{urllib.parse.quote(url_to_submit, safe='')}"
    )
    try:
        resp = urllib.request.urlopen(endpoint, timeout=20)
        ok = resp.status in (200, 204)
        print(f"  Bing ping.aspx: {'OK' if ok else 'FAILED'} "
              f"(status={resp.status})")
        return ok, resp.status
    except urllib.error.HTTPError as e:
        print(f"  Bing ping.aspx: FAILED (status={e.code})")
        return False, e.code
    except Exception as e:
        print(f"  Bing ping.aspx: FAILED ({e})")
        return False, None


def submit(url_to_submit):
    api_key = get_api_key()
    url_list = [url_to_submit]
    is_sitemap = url_to_submit.rstrip("/").endswith("sitemap.xml")

    # 1) Bing Webmaster URL Submission API (primary, Bing only).
    ok, status = submit_via_webmaster_api(api_key, url_list)

    # 2) IndexNow (covers Bing + Yandex + Seznam). Skip key-verification
    #    noise for sitemaps; IndexNow only accepts individual URLs.
    if not is_sitemap:
        in_ok, _ = submit_via_indexnow(api_key, url_list)
        ok = ok or in_ok

    # 3) Web-based ping fallback for the sitemap.
    if is_sitemap and not ok:
        ping_ok, _ = submit_via_ping(url_to_submit)
        ok = ok or ping_ok

    update_pipeline_status(
        url_to_submit, "pinged", "completed" if ok else "failed",
        {"service": "bing", "url": url_to_submit, "status_code": status},
    )
    return ok


if __name__ == "__main__":
    api_key = get_api_key()
    if "--url" in sys.argv:
        idx = sys.argv.index("--url") + 1
        if idx < len(sys.argv):
            ok = submit(sys.argv[idx])
            sys.exit(0 if ok else 1)
    else:
        ok = submit(SITEMAP_URL)
        sys.exit(0 if ok else 1)
