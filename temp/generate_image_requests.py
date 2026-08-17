import json

registry_path = "data/tracking/article-registry.json"
requests_path = "data/tracking/manual-image-requests.txt"

with open(registry_path, "r") as f:
    registry = json.load(f)

drafts = [a for a in registry.get("articles", []) if a.get("status") == "Draft" and a.get("image", {}).get("status") == "Pending"]

new_requests = ""

for draft in drafts:
    title = draft.get("title")
    keyword = draft.get("target_keyword", "")
    
    description = f"A premium, minimalist aesthetic image representing {keyword or title}. Style: Soft golden lighting, peaceful atmosphere, vibrant colors, clean and premium look, 16:9 aspect ratio. No text, no human faces."
    
    new_requests += f"Article Title: {title}\n"
    new_requests += f"Description: {description}\n\n"
    new_requests += "Image URL Link: \n"
    new_requests += "Image Quantity: 1\n"
    new_requests += "Status: Pending\n"
    new_requests += "--------------------------------------------------\n\n"

with open(requests_path, "a") as f:
    f.write(new_requests)

print(f"Added {len(drafts)} image requests to {requests_path}")
