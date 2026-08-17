#!/usr/bin/env python3
"""
Extract rich content from backed up originals and merge into herb_index.json
"""
import json
import re
from pathlib import Path

ROOT = Path("/home/shiva/ayurshakti.shop")
BACKUP_DIR = ROOT / "content" / "herbs_backup"
INDEX_FILE = ROOT / "data" / "herb_index.json"

with open(INDEX_FILE) as f:
    HERB_INDEX = json.load(f)

def extract_section(content, start_marker, end_marker=None):
    """Extract a section from markdown content between markers"""
    start_idx = content.find(start_marker)
    if start_idx == -1:
        return None
    start_idx = content.find('\n', start_idx) + 1
    if end_marker:
        end_idx = content.find(end_marker, start_idx)
        if end_idx == -1:
            end_idx = len(content)
    else:
        end_idx = len(content)
    return content[start_idx:end_idx].strip()

def extract_taseer(content):
    """Extract Taseer section data"""
    section = extract_section(content, "## 🔥 2. Ayurvedic Energy Profile", "## 🧪")
    if not section:
        return {}
    
    data = {}
    # Extract using more flexible regex
    patterns = {
        "rasa": r'\*\*Rasa \(Taste\):\*\*\s*\*([^*]+)\*',
        "guna": r'\*\*Guna \(Qualities\):\*\*\s*\*([^*]+)\*',
        "virya": r'\*\*Virya \(Taseer / Potency\):\*\*\s*\*\*([^*]+)\*\*',
        "vipaka": r'\*\*Vipaka \(Post-Digestive Effect\):\*\*\s*\*([^*]+)\*',
    }
    
    for key, pattern in patterns.items():
        match = re.search(pattern, section)
        if match:
            data[key] = match.group(1).strip()
    
    # Dosha Karma - capture everything after the heading
    dosha_match = re.search(r'\*\*Dosha Karma \(Dosha Impact\):\*\*\s*(.+?)(?:\n\n|\Z)', section, re.DOTALL)
    if dosha_match:
        data["dosha_karma"] = dosha_match.group(1).strip()
    
    return data

def extract_phytochemical(content):
    section = extract_section(content, "## 🧪 3. Phytochemical", "## 💡")
    if not section:
        return []
    items = re.findall(r'[-•]\s*\*\*([^*]+)\*\*:\s*(.+?)(?=\n[-•]|\n\n|\Z)', section, re.DOTALL)
    result = []
    for name, desc in items:
        result.append(f"**{name.strip()}**: {desc.strip()}")
    return result

def extract_clinical(content):
    section = extract_section(content, "## 💡 4. Primary Clinical Use", "## 💊")
    if not section:
        return []
    # Remove numbering and extract items
    items = re.findall(r'(?:\d+\.|[-•])\s*(.+?)(?=\n\d+\.|\n[-•]|\n\n|\Z)', section, re.DOTALL)
    return [item.strip() for item in items if item.strip()]

def extract_formulations(content):
    section = extract_section(content, "## 💊 5. Classical Formulations", "## 📜")
    if not section:
        return []
    items = re.findall(r'[-•]\s*(.+?)(?=\n[-•]|\n\n|\Z)', section, re.DOTALL)
    return [item.strip() for item in items if item.strip()]

def main():
    PUBLISHED_HERBS = [
        "ashwagandha", "shatavari", "giloy", "brahmi", "tulsi",
        "turmeric", "amalaki", "haritaki", "bibhitaki", "triphala"
    ]
    
    with open("/home/shiva/ayurshakti.shop/data/herb_index.json") as f:
        HERB_INDEX = json.load(f)
    
    for slug in PUBLISHED_HERBS:
        backup_file = Path("/home/shiva/ayurshakti.shop/content/herbs_backup") / f"{slug}.md"
        if not backup_file.exists():
            print(f"  ⚠️  No backup for {slug}")
            continue
        
        content = backup_file.read_text(encoding="utf-8")
        
        if slug in HERB_INDEX:
            taseer = extract_taseer(content)
            phytochemicals = extract_phytochemical(content)
            clinical = extract_clinical(content)
            formulations = extract_formulations(content)
            
            HERB_INDEX[slug].update(taseer)
            if phytochemicals:
                HERB_INDEX[slug]["phytochemicals"] = phytochemicals
            if clinical:
                HERB_INDEX[slug]["therapeutic_uses"] = clinical
            if formulations:
                HERB_INDEX[slug]["formulations"] = formulations
            
            print(f"  ✅ Enriched {slug}: taseer={len(taseer)}, phyto={len(phytochemicals)}, clinical={len(clinical)}, formulations={len(formulations)}")
    
    with open("/home/shiva/ayurshakti.shop/data/herb_index.json", "w") as f:
        json.dump(HERB_INDEX, f, indent=2, ensure_ascii=False)
    
    print("\n✅ herb_index.json updated with rich content")

if __name__ == "__main__":
    main()
