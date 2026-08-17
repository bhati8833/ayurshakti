#!/usr/bin/env python3
"""
AyurShakti Label Assigner v2.0
Fixes/updates labels on ALL Blogger posts based on article title keywords.
Also syncs labels to article-registry.json.

Usage:
    python3 assign_categories.py              # Fix all posts
    python3 assign_categories.py --dry-run     # Preview only
    python3 assign_categories.py --id POST_ID  # Fix single post
"""
import json, os, sys, time, requests

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TRACKING_DIR = os.path.join(SCRIPT_DIR, "data", "tracking")
REGISTRY_PATH = os.path.join(TRACKING_DIR, "article-registry.json")
SECRETS_PATH = os.path.join(SCRIPT_DIR, "secrets", "blogger-oauth-tokens.json")
BLOG_ID = "944859273218738540"

def get_labels_from_title(title):
    title_lower = title.lower()
    labels = []

    # Individual herb sub-labels (for menu sub-category links like /search/label/Ashwagandha)
    herb_names = {
        'ashwagandha': 'Ashwagandha', 'triphala': 'Triphala', 'turmeric': 'Turmeric',
        'brahmi': 'Brahmi', 'shilajit': 'Shilajit', 'giloy': 'Giloy',
        'shatavari': 'Shatavari', 'tulsi': 'Tulsi',
    }
    matched_herbs = [name for kw, name in herb_names.items() if kw in title_lower]
    labels.extend(matched_herbs)

    # Main category: Ayurvedic Herbs (if article mentions a specific herb or is herb-related)
    if matched_herbs or any(kw in title_lower for kw in ['herb', 'supplement']):
        labels.append('Ayurvedic Herbs')
    if any(kw in title_lower for kw in ['brain', 'memory', 'cogniti', 'mental', 'focus']):
        labels.append('Brain Health')
    if any(kw in title_lower for kw in ['women', 'pcos', 'female', 'hormonal balance', 'shatavari']):
        labels.append("Women's Health")
    if any(kw in title_lower for kw in ['men', 'male', 'testosterone', 'vitality']):
        labels.append("Men's Health")
    if any(kw in title_lower for kw in ['dog', 'puppy', 'canine', 'pet', 'flea', 'tick', 'ear infection']):
        labels.append('Dog Health')
    remedy_keywords = ['gut health', 'digest', 'allergy', 'itchy', 'joint pain', 'arthritis',
                       'flea', 'tick', 'ear infection', 'anxiety', 'calming', 'sleep']
    if any(kw in title_lower for kw in remedy_keywords):
        labels.append('Natural Remedies')
    return labels

def get_blogger_token():
    creds = json.load(open(SECRETS_PATH))
    r = requests.post('https://oauth2.googleapis.com/token', data={
        'client_id': creds['client_id'],
        'client_secret': creds['client_secret'],
        'refresh_token': creds['refresh_token'],
        'grant_type': 'refresh_token'
    }, timeout=15)
    r.raise_for_status()
    return r.json()['access_token']

def sync_to_registry(post_id, title, labels):
    os.makedirs(TRACKING_DIR, exist_ok=True)
    reg = json.load(open(REGISTRY_PATH)) if os.path.exists(REGISTRY_PATH) else {"articles": []}
    found = False
    for art in reg["articles"]:
        if art.get("id") == post_id or art.get("title") == title:
            art["labels"] = labels
            art["id"] = post_id
            found = True
            break
    if not found:
        reg["articles"].append({"id": post_id, "title": title, "labels": labels, "status": "Published"})
    json.dump(reg, open(REGISTRY_PATH, "w"), indent=2)

def main():
    dry_run = "--dry-run" in sys.argv
    single_id = None
    for i, a in enumerate(sys.argv):
        if a == "--id" and i + 1 < len(sys.argv):
            single_id = sys.argv[i + 1]

    token = get_blogger_token()
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    # Fetch posts
    all_posts = []
    page_token = None
    while True:
        url = f"https://www.googleapis.com/blogger/v3/blogs/{BLOG_ID}/posts/?maxResults=50"
        if page_token:
            url += f"&pageToken={page_token}"
        r2 = requests.get(url, headers=headers, timeout=15)
        data = r2.json()
        for p in data.get("items", []):
            if single_id and str(p["id"]) != single_id:
                continue
            all_posts.append(p)
        page_token = data.get("nextPageToken")
        if not page_token or single_id:
            break

    print(f"Found {len(all_posts)} post(s) to process")
    for post in all_posts:
        pid = post["id"]
        title = post["title"]
        existing = post.get("labels", [])
        new_labels = get_labels_from_title(title)

        if not new_labels:
            print(f"  ⚠️  No labels matched for: {title[:50]}")
            continue

        if set(new_labels) == set(existing):
            print(f"  ✅ Already correct: {title[:50]} → {new_labels}")
            sync_to_registry(pid, title, new_labels)
            continue

        print(f"  {'🔍 DRY-RUN' if dry_run else '🔄'} Updating: {title[:50]}")
        print(f"     Old: {existing} | New: {new_labels}")

        if dry_run:
            continue

        resp = requests.patch(
            f"https://www.googleapis.com/blogger/v3/blogs/{BLOG_ID}/posts/{pid}",
            headers=headers, json={"labels": new_labels}, timeout=15
        )
        if resp.status_code == 200:
            print(f"     ✅ Done")
            sync_to_registry(pid, title, new_labels)
        else:
            print(f"     ❌ Failed: {resp.status_code} {resp.text[:100]}")
        time.sleep(0.5)

    print("\n✅ Complete!")

if __name__ == "__main__":
    main()
