#!/usr/bin/env python3
"""
Force regenerate the 10 already-published herbs with new template
"""
import json
import shutil
from pathlib import Path
from datetime import datetime

ROOT = Path("/home/shiva/ayurshakti.shop")
DRAFT_DIR = ROOT / "content" / "herbs_draft"
HERBS_DIR = ROOT / "content" / "herbs"
INDEX_FILE = ROOT / "data" / "herb_index.json"

with open(INDEX_FILE) as f:
    HERB_INDEX = json.load(f)

with open(ROOT / "data" / "herb_synonyms.json") as f:
    SYNONYMS = json.load(f)

COMBINATION_FORMULAS = SYNONYMS.get("combination_formulas", {})
COMPONENT_TO_FORMULA = {}
for formula, components in COMBINATION_FORMULAS.items():
    for comp in components:
        COMPONENT_TO_FORMULA[comp.lower()] = formula

# Import the generation functions from the main script
import sys
sys.path.insert(0, str(ROOT / "scripts"))
from generate_herb_profile import (
    generate_herb_profile, 
    load_existing_frontmatter,
    should_skip_generation,
    filter_ingredient_list
)

# The 10 published herbs to regenerate
PUBLISHED_HERBS = [
    "ashwagandha", "shatavari", "giloy", "brahmi", "tulsi",
    "turmeric", "amalaki", "haritaki", "bibhitaki", "triphala"
]

def main():
    # Backup originals first
    backup_dir = ROOT / "content" / "herbs_backup"
    backup_dir.mkdir(exist_ok=True)
    
    for slug in PUBLISHED_HERBS:
        src = HERBS_DIR / f"{slug}.md"
        if src.exists():
            dst = backup_dir / f"{slug}.md"
            shutil.copy2(src, dst)
            print(f"  📦 Backed up: {slug}.md")
    
    print(f"\n🔄 Regenerating {len(PUBLISHED_HERBS)} published herbs...")
    
    for slug in PUBLISHED_HERBS:
        if slug not in HERB_INDEX:
            print(f"  ⚠️  {slug} not in herb_index.json, skipping")
            continue
        
        data = HERB_INDEX[slug]
        data["slug"] = slug
        
        # Force generation (bypass skip check)
        md = generate_herb_profile(slug, data)
        
        # Fix status to Published for these herbs
        md = md.replace('status: "Draft"', 'status: "Published"')
        
        # Write to herbs/ directory (overwrite published)
        output_file = HERBS_DIR / f"{slug}.md"
        output_file.write_text(md, encoding="utf-8")
        print(f"  ✅ Regenerated: {slug}.md")
    
    print(f"\n✅ Done! Originals backed up to {backup_dir}")

if __name__ == "__main__":
    main()
