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

def extract_section(content, section_title):
    """Extract a section from markdown content"""
    pattern = rf'##\s+{re.escape(section_title)}.*?(?=\n##\s+|\Z)'
    match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(0).strip()
    return None

def extract_taseer(content):
    """Extract Taseer section data"""
    section = extract_section(content, r"🔥 2\. Ayurvedic Energy Profile")
    if not section:
        return {}
    
    data = {}
    # Extract rasa, guna, virya, vipaka, dosha_karma
    rasa_match = re.search(r'\*\*Rasa \(Taste\):\*\*\s*(.+)', section)
    if rasa_match:
        data["rasa"] = rasa_match.group(1).strip()
    
    guna_match = re.search(r'\*\*Guna \(Qualities\):\*\*\s*(.+)', section)
    if guna_match:
        data["guna"] = guna_match.group(1).strip()
    
    virya_match = re.search(r'\*\*Virya \(Taseer.*?\):\*\*\s*(.+)', section)
    if virya_match:
        data["virya"] = virya_match.group(1).strip()
    
    vipaka_match = re.search(r'\*\*Vipaka \(Post-Digestive Effect\):\*\*\s*(.+)', section)
    if vipaka_match:
        data["vipaka"] = vipaka_match.group(1).strip()
    
    dosha_match = re.search(r'\*\*Dosha Karma \(Dosha Impact\):\*\*\s*(.+)', section, re.DOTALL)
    if dosha_match:
        data["dosha_karma"] = dosha_match.group(1).strip()
    
    return data

def extract_phytochemical(content):
    """Extract phytochemical section"""
    section = extract_section(content, r"🧪 3\. Phytochemical")
    if section:
        # Clean up bullet points
        items = re.findall(r'[-•]\s*(.+)', section)
        return [item.strip() for item in items if item.strip()]
    return []

def extract_clinical(content):
    """Extract clinical uses section"""
    section = extract_section(content, r"💡 4\. Primary Clinical Use")
    if section:
        items = re.findall(r'[-•\d.]\s*(.+)', section)
        return [item.strip() for item in items if item.strip()]
    return []

def extract_formulations(content):
    """Extract formulations section"""
    section = extract_section(content, r"💊 5\. Classical Formulations")
    if section:
        items = re.findall(r'[-•]\s*(.+)', section)
        return [item.strip() for item in items if item.strip()]
    return []

def main():
    PUBLISHED_HERBS = [
        "ashwagandha", "shatavari", "giloy", "brahmi", "tulsi",
        "turmeric", "amalaki", "haritaki", "bibhitaki", "triphala"
    ]
    
    for slug in PUBLISHED_HERBS:
        backup_file = Path("/home/shiva/ayurshakti.shop/content/herbs_backup") / f"{slug}.md"
        if not backup_file.exists():
            print(f"  ⚠️  No backup for {slug}")
            continue
        
        content = backup_file.read_text(encoding="utf-8")
        
        if slug in HERB_INDEX:
            # Extract rich data
            taseer = extract_taseer(content)
            phytochemicals = extract_phytochemical(content)
            clinical = extract_clinical(content)
            formulations = extract_formulations(content)
            
            # Merge into index
            HERB_INDEX[slug].update(taseer)
            if phytochemicals:
                HERB_INDEX[slug]["phytochemicals"] = phytochemicals
            if clinical:
                HERB_INDEX[slug]["therapeutic_uses"] = clinical
            if formulations:
                HERB_INDEX[slug]["formulations"] = formulations
            
            print(f"  ✅ Enriched {slug}: taseer={len(taseer)}, phyto={len(phytochemicals)}, clinical={len(clinical)}, formulations={len(formulations)}")
    
    # Save updated index
    with open("/home/shiva/ayurshakti.shop/data/herb_index.json", "w") as f:
        json.dump(HERB_INDEX, f, indent=2, ensure_ascii=False)
    
    print("\n✅ herb_index.json updated with rich content")

if __name__ == "__main__":
    main()
