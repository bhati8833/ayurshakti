#!/usr/bin/env python3
"""
Update all Blogger post image URLs to use new /img/ path structure.
Old: https://resources.ayurshakti.shop/filename.jpg
New: https://resources.ayurshakti.shop/img/filename.jpg
"""
import json
import os
import re
import sys
import urllib.request
from urllib.parse import urlencode

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def get_access_token():
    path = os.path.join(BASE, "secrets", "blogger-oauth-tokens.json")
    with open(path) as f:
        s = json.load(f)
    data = {
        "client_id": s["client_id"],
        "client_secret": s["client_secret"],
        "refresh_token": s["refresh_token"],
        "grant_type": "refresh_token"
    }
    req = urllib.request.Request(s["token_uri"], data=urlencode(data).encode(), method="POST")
    return json.loads(urllib.request.urlopen(req).read())["access_token"]
def fix_img_paths(content):
    return re.sub(
        r'src="https://resources\.ayurshakti\.shop/(?!img/)([^"]+)"',
        r'src="https://resources.ayurshakti.shop/img/\1"',
        content
    )
def fix_href_paths(content):
    return re.sub(
        r'href="https://resources\.ayurshakti\.shop/(?!img/)(?!key/)(?!pdf/)([^"]+)"',
        r'href="https://resources.ayurshakti.shop/img/\1"',
        content
    )

try:
    token = get_access_token()
    with open(os.path.join(BASE, "scripts", "schedule-config.json")) as f:
        blog_id = json.load(f)["blog_id"]

    posts = []
    page_token = None
    while True:
        url = f"https://www.googleapis.com/blogger/v3/blogs/{blog_id}/posts?maxResults=50"
        if page_token:
            url += f"&pageToken={page_token}"
        req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
        data = json.loads(urllib.request.urlopen(req).read())
        posts.extend(data.get("items", []))
        page_token = data.get("nextPageToken")
        if not page_token:
            break

    print(f"Total posts: {len(posts)}\n")
    updated = 0
    for p in posts:
        content = p.get("content", "")
        old_content = content
        content = fix_img_paths(content)
        content = fix_href_paths(content)
        if content != old_content:
            print(f"Updating: {p['title']}")
            body = json.dumps({"title": p["title"], "content": content}).encode("utf-8")
            update_url = f"https://www.googleapis.com/blogger/v3/blogs/{blog_id}/posts/{p['id']}"
            update_req = urllib.request.Request(
                update_url, data=body,
                headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
                method="PUT"
            )
            urllib.request.urlopen(update_req)
            print("  ✅ Updated\n")
            updated += 1
        else:
            print(f"Skipped (no changes): {p['title']}")

    print(f"\nDone. Updated {updated} posts")
except Exception as e:
    print(f"Error: {e}", file=sys.stderr)
    import traceback
    traceback.print_exc()
    sys.exit(1)