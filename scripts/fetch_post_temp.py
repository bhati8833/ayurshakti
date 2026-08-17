import json
import os
import urllib.parse
import urllib.request

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

def get_access_token():
    secrets_path = os.path.join(SCRIPT_DIR, "..", "secrets", "blogger-oauth-tokens.json")
    with open(secrets_path) as f:
        s = json.load(f)
    data = {
        "client_id": s["client_id"],
        "client_secret": s["client_secret"],
        "refresh_token": s["refresh_token"],
        "grant_type": "refresh_token"
    }
    req = urllib.request.Request(s["token_uri"], data=urllib.parse.urlencode(data).encode(), method="POST")
    resp = json.loads(urllib.request.urlopen(req).read())
    return resp["access_token"]

try:
    token = get_access_token()
    blog_id = "944859273218738540"
    path = "/2026/07/ayurvedic-remedies-for-pcos-natural.html"
    url = f"https://www.googleapis.com/blogger/v3/blogs/{blog_id}/posts/bypath?path={urllib.parse.quote(path)}"
    
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
    resp = urllib.request.urlopen(req)
    post_data = json.loads(resp.read())
    
    with open(os.path.join(SCRIPT_DIR, "temp_post.json"), "w") as f:
        json.dump(post_data, f, indent=2)
    print("Success")
except Exception as e:
    print(f"Error: {e}")
