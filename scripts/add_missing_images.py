import json
import os
import re
import urllib.request
from urllib.parse import urlencode

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

image_mapping = {
    "calming_cbd": "dog_calming_cbd_free_1783832454358.png",
    "digestive_issues": "dog_digestive_issues_1783832463737.png",
    "flea_tick": "dog_flea_tick_1783832478299.png",
    "gut_agni": "ayurveda_agni_gut_1783832487475.png",
    "joint_pain": "dog_joint_pain_1783832497693.png",
    "ear_infections": "dog_ear_infections_1783832509536.png",
    "pcos": "ayurvedic-remedies-for-pcos-natural-hormonal-balance-guide.jpg",
    "allergy_relief": "dog_allergy_relief_1783832518988.png",
    "giloy": "giloy_immunity_1783832530138.png",
    "gut_health_7": "ayurvedic_gut_health_v3_1783605434349.png"
}

title_to_key = [
    ("calming.*cbd", "calming_cbd"),
    ("digestive issues", "digestive_issues"),
    ("flea.*tick", "flea_tick"),
    ("gut health.*agni", "gut_agni"),
    ("joint pain", "joint_pain"),
    ("ear infections", "ear_infections"),
    ("pcos", "pcos"),
    ("allergy relief", "allergy_relief"),
    ("giloy", "giloy"),
    ("gut health.*7 natural ways", "gut_health_7")
]

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

def find_new_filename(title):
    title_lower = title.lower()
    for pattern, key in title_to_key:
        if re.search(pattern, title_lower):
            return image_mapping[key]
    return None

try:
    token = get_access_token()
    with open(os.path.join(BASE, "scripts", "schedule-config.json")) as f:
        blog_id = json.load(f)["blog_id"]

    posts = []
    page_token = None
    while True:
        url = f"https://www.googleapis.com/blogger/v3/blogs/{blog_id}/posts?maxResults=50&status=LIVE&status=SCHEDULED&status=DRAFT"
        if page_token:
            url += f"&pageToken={page_token}"
        req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
        data = json.loads(urllib.request.urlopen(req).read())
        posts.extend(data.get("items", []))
        page_token = data.get("nextPageToken")
        if not page_token:
            break

    print(f"Total posts retrieved: {len(posts)}\n")

    updated = 0
    for p in posts:
        new_filename = find_new_filename(p["title"])
        if not new_filename:
            continue

        content = p.get("content", "")
        old_content = content
        
        # Check if the image is already there
        img_url = f"https://resources.ayurshakti.shop/img/{new_filename}"
        if img_url in content:
            print(f"Skipped (already has image): {p['title']}")
            continue
            
        # Prepend image
        content = f'<div class="separator" style="clear: both; text-align: center;"><img src="{img_url}" alt="{p["title"]}" border="0" /></div><br/>\n' + content

        if content != old_content:
            print(f"Updating: {p['title']} with {new_filename}")
            body = json.dumps({
                "title": p["title"],
                "content": content
            }).encode("utf-8")
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

    if updated == 0:
        print("\nNo posts needed updating.")
    else:
        print(f"\nDone. Updated {updated} posts")

except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
