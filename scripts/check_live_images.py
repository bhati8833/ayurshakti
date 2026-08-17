import json
import re
import urllib.request

with open('/home/shiva/ayurshakti.shop/secrets/blogger-api-token.json') as f:
    token = json.load(f)["access_token"]
with open('/home/shiva/ayurshakti.shop/scripts/schedule-config.json') as f:
    blog_id = json.load(f)["blog_id"]

url = f"https://www.googleapis.com/blogger/v3/blogs/{blog_id}/posts?maxResults=50"
req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
try:
    resp = urllib.request.urlopen(req)
    data = json.loads(resp.read())
    for p in data.get('items', []):
        content = p.get('content', '')
        # find img src
        imgs = re.findall(r'<img[^>]+src="([^"]+)"', content)
        print(f"Post ID: {p['id']}, Title: {p['title']}")
        for img in imgs:
            print(f"  Image: {img}")
except Exception as e:
    print(e)
