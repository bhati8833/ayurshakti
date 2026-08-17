import json
import os
import re
import urllib.parse
import urllib.request

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# 1. Load temp_post.json
with open(os.path.join(SCRIPT_DIR, "temp_post.json")) as f:
    post_data = json.load(f)

html = post_data["content"]

# 2. Fix the HTML

# Bold text: **text** -> <strong>text</strong>
html = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html)

# Links: [text](/link) -> <a href="\2">\1</a>
html = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>', html)

# Table fix
html = html.replace("<p>|------|------|-------------|</p>\n", "")
html = html.replace("<p>|------|------|-------------|</p>", "")

# Unwrapped <li> elements -> wrap in <ul>
# Find consecutive <li>...</li> blocks
html = re.sub(r'(?:<li>.*?</li>\n*)+', lambda m: f'<ul>\n{m.group(0)}</ul>\n', html)

# Fix script tag with <p> wrapped
html = html.replace('<p></script></p>', '</script>')
html = html.replace('<p><script type="application/ld+json"></p>', '<script type="application/ld+json">')
html = html.replace('<p><script type="application/ld+json">\n<p>{', '<script type="application/ld+json">\n{')

match = re.search(r'(<script type="application/ld+json">.*?</script>)', html, re.DOTALL)
if match:
    old_script = match.group(1)
    new_script = old_script.replace('<p>', '').replace('</p>', '')
    html = html.replace(old_script, new_script)

post_data["content"] = html

# Save back to temp_post.json just in case
with open(os.path.join(SCRIPT_DIR, "temp_post_fixed.json"), "w") as f:
    json.dump(post_data, f, indent=2)

# 3. Update Blogger API
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
    post_id = post_data["id"]
    api_url = f"https://www.googleapis.com/blogger/v3/blogs/{blog_id}/posts/{post_id}"

    body = json.dumps({
        "title": post_data["title"],
        "content": html,
        "labels": post_data.get("labels", []),
        "status": "LIVE"
    }).encode("utf-8")

    req = urllib.request.Request(
        api_url,
        data=body,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        },
        method="PUT"
    )

    resp = urllib.request.urlopen(req)
    result = json.loads(resp.read())
    print("Post updated successfully!")
    print(f"URL: {result.get('url')}")
except Exception as e:
    print(f"Error updating post: {e}")
