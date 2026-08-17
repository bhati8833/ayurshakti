import json
import os
import re
import urllib.request
from urllib.parse import urlencode

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

image_mapping = {
    "ashwagandha_dogs": "ashwagandha_dogs_1783327381866.png",
    "ashwagandha_men_vitality": "ashwagandha_men_vitality_1783327271819.png",
    "ayurveda_dogs": "ayurveda_dogs_guide_1783327360341.png",
    "pcos": "ayurvedic-remedies-for-pcos-natural-hormonal-balance-guide.jpg",
    "brahmi": "brahmi_brain_health_1783327145301.png",
    "calming_chews": "calming_chews_dogs_1783327342587.png",
    "coconut_oil": "coconut_oil_dogs_1783327211632.png",
    "dog_anxiety": "dog_anxiety_night_1783327233851.png",
    "shatavari": "shatavari_women_health_1783327190602.png",
    "digestion": "the-complete-guide-to-ayurvedic-digestion.jpg",
    "triphala": "triphala_dogs_1783327285010.png",
    "turmeric": "turmeric_dogs_1783327299925.png"
}

title_to_key = [
    ("digestion", "digestion"),
    ("pcos", "pcos"),
    ("shatavari", "shatavari"),
    ("ashwagandha.*men|men.*ashwagandha", "ashwagandha_men_vitality"),
    ("ashwagandha.*dog|dog.*ashwagandha", "ashwagandha_dogs"),
    ("brahmi", "brahmi"),
    ("calming", "calming_chews"),
    ("coconut", "coconut_oil"),
    ("anxiety|night", "dog_anxiety"),
    ("triphala", "triphala"),
    ("turmeric", "turmeric"),
    ("ayurveda.*dog|dog.*ayurveda.*beginner", "ayurveda_dogs"),
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

def replace_hostname(content):
    return content.replace("images.ayurshakti.shop", "resources.ayurshakti.shop")

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

        content = replace_hostname(content)

        imgs = re.findall(r'src="([^"]+)"', content)
        new_filename = find_new_filename(p["title"])

        for img in imgs:
            if not new_filename:
                continue
            local_domain = "resources.ayurshakti.shop"
            if local_domain in img:
                continue
            new_url = f"https://{local_domain}/{new_filename}"
            content = content.replace(img, new_url)

        if content != old_content:
            print(f"Updating: {p['title']}")
            print(f"  Images: {len(imgs)} replaced → {new_filename}")
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

    if updated == 0:
        print("\nNo posts needed updating.")
    else:
        print(f"\nDone. Updated {updated} posts")

except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
