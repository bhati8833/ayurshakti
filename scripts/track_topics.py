import json

md_path = "/home/shiva/ayurshakti.shop/docs/bulk-topic-research.md"
json_path = "/home/shiva/ayurshakti.shop/data/tracking/article-registry.json"

with open(md_path, encoding='utf-8') as f:
    content = f.read()

# Fix the structure
content = content.replace("## Category B: Pet Health — High Priority (12 Topics)", "## Category B: Pet Health — High Priority (13 Topics)")
content = content.replace("### 13. Natural Joint Pain", "### 1. Natural Joint Pain")
content = content.replace("### 14. Natural Allergy", "### 2. Natural Allergy")
content = content.replace("### 26. Urinary Tract", "### 11. Urinary Tract")
content = content.replace("### 27. Home Dental Care", "### 12. Home Dental Care")
content = content.replace("### 28. Seasonal Dog Care", "### 13. Seasonal Dog Care")

with open(md_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Fixed structure in bulk-topic-research.md")

# Now extract topics and keywords
topics = []
lines = content.split('\n')
current_title = None

for line in lines:
    if line.startswith("### ") and not line.startswith("### Publish in this order"):
        current_title = line.split(" ", 2)[2].strip()
    elif line.startswith("- **Target Keyword:**"):
        kw = line.replace("- **Target Keyword:**", "").strip()
        if current_title:
            topics.append({"title": current_title, "target_keyword": kw})
            current_title = None

print(f"Extracted {len(topics)} topics from md file.")

# Add to article-registry.json
with open(json_path, encoding='utf-8') as f:
    data = json.load(f)

existing_titles = [a.get("title", "").lower() for a in data.get("articles", [])]
added_count = 0

for t in topics:
    # Very basic check, could be improved if needed, but titles are fairly unique
    found = False
    for ext in existing_titles:
        if t["title"].lower() in ext or ext in t["title"].lower():
            found = True
            break
    
    if not found:
        data["articles"].append({
            "title": t["title"],
            "target_keyword": t["target_keyword"],
            "status": "Draft",
            "image": {
                "status": "Pending"
            }
        })
        existing_titles.append(t["title"].lower())
        added_count += 1

with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2)

print(f"Added {added_count} new topics as Draft to article-registry.json")
