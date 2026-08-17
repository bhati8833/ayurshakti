#!/usr/bin/env python3
"""
Improved extraction using glossary as primary source + all content
"""
import json
import re
from pathlib import Path
from collections import defaultdict

ROOT = Path("/home/shiva/ayurshakti.shop")
CONTENT_DIR = ROOT / "content"

with open(ROOT / "data" / "herb_synonyms.json") as f:
    SYNONYMS = json.load(f)

COMBINATION_FORMULAS = SYNONYMS.get("combination_formulas", {})
COMPONENT_TO_FORMULA = {}
for formula, components in COMBINATION_FORMULAS.items():
    for comp in components:
        COMPONENT_TO_FORMULA[comp.lower()] = formula

def is_combination_component(herb_slug: str) -> bool:
    return herb_slug.lower() in COMPONENT_TO_FORMULA

def get_combination_formula(herb_slug: str) -> str:
    return COMPONENT_TO_FORMULA.get(herb_slug.lower(), "")

# Build comprehensive Sanskrit name list from glossary
def load_all_sanskrit_terms():
    """Load all terms from glossary JSON files"""
    terms = {}
    glossary_dir = CONTENT_DIR / "glossary"
    for f in glossary_dir.glob("glossary_*.json"):
        try:
            with open(f) as fp:
                data = json.load(fp)
                for term in data.get("terms", []):
                    if isinstance(term, dict) and "term" in term:
                        t = term["term"]
                        terms[t.lower()] = term.get("definition", "")
        except:
            pass
    return terms

GLOSSARY_TERMS = load_all_sanskrit_terms()
print(f"Loaded {len(GLOSSARY_TERMS)} glossary terms")

# Match glossary terms to known herbs
def match_glossary_to_herbs():
    """Find which glossary terms correspond to our herb list"""
    herb_terms = {}
    for slug, syn in SYNONYMS.get("by_slug", {}).items():
        if slug in ["triphala", "dashmool"]:  # Skip combination formulas themselves
            continue
        names = set()
        names.update(syn.get("sanskrit", []))
        names.update(syn.get("hindi", []))
        names.update(syn.get("english", []))
        names.add(slug)
        
        matched_terms = []
        for name in names:
            norm = name.lower().strip()
            # Find glossary terms that match or contain this name
            for gterm, gdef in GLOSSARY_TERMS.items():
                if norm in gterm or gterm in norm:
                    if len(gterm) > 3:  # Avoid too short matches
                        matched_terms.append((gterm, gdef))
        if matched_terms:
            herb_terms[slug] = matched_terms[:5]  # Top 5 matches
    return herb_terms

HERB_GLOSSARY_MAP = match_glossary_to_herbs()
print(f"Matched glossary terms for {len(HERB_GLOSSARY_MAP)} herbs")

def extract_from_all_content():
    """Single pass through all content files"""
    herbs = defaultdict(lambda: {
        "classical_refs": [],
        "formulations": [],
        "therapeutic_uses": [],
        "dosage_mentions": [],
        "clinical_studies": [],
        "phytochemicals": [],
        "research_refs": [],
        "glossary_definitions": [],
        "sanskrit_names": set(),
        "content_files": []
    })
    
    # All content directories
    content_dirs = [
        CONTENT_DIR / "samhitas",
        CONTENT_DIR / "canonical_texts",
        CONTENT_DIR / "research",
        CONTENT_DIR / "essays_and_studies",
        CONTENT_DIR / "other_works",
        CONTENT_DIR / "herbs",
        CONTENT_DIR / "herb_profiles",
        CONTENT_DIR / "pet-health",
    ]
    
    all_files = []
    for d in content_dirs:
        if d.exists():
            all_files.extend(d.rglob("*.md"))
    
    print(f"Scanning {len(all_files)} content files...")
    
    # For each herb, search all files
    for slug, syn in SYNONYMS.get("by_slug", {}).items():
        if slug in ["triphala", "dashmool"]:  # Skip formulas themselves
            continue
            
        # Build search terms
        search_terms = set()
        search_terms.update(syn.get("sanskrit", []))
        search_terms.update(syn.get("hindi", []))
        search_terms.update(syn.get("english", []))
        search_terms.add(slug)
        
        # Add glossary-matched terms
        if slug in HERB_GLOSSARY_MAP:
            for gterm, gdef in HERB_GLOSSARY_MAP[slug]:
                search_terms.add(gterm)
        
        # Search each file
        for f in all_files:
            try:
                content = f.read_text(encoding="utf-8", errors="ignore")
                found = False
                for term in search_terms:
                    if len(term) < 3:
                        continue
                    pattern = r'\b' + re.escape(term) + r'\b'
                    if re.search(pattern, content, re.IGNORECASE):
                        found = True
                        herbs[slug]["content_files"].append(str(f.relative_to(ROOT)))
                        herbs[slug]["sanskrit_names"].add(term)
                        
                        # Categorize by directory
                        rel = f.relative_to(CONTENT_DIR)
                        if "samhitas" in str(rel):
                            herbs[slug]["classical_refs"].append({
                                "source": "Samhita",
                                "file": str(rel),
                                "context": f"mentioned as {term}"
                            })
                        elif "canonical" in str(rel) or "other_works" in str(rel):
                            herbs[slug]["classical_refs"].append({
                                "source": "Classical Text",
                                "file": str(rel),
                                "context": f"mentioned as {term}"
                            })
                        elif "research" in str(rel) or "essays" in str(rel):
                            herbs[slug]["research_refs"].append({
                                "title": f.stem.replace("_", " ").title(),
                                "file": str(rel),
                                "context": f"mentioned as {term}"
                            })
                        elif "herbs" in str(rel) or "herb_profiles" in str(rel):
                            herbs[slug]["content_files"].append(str(rel))
                if found:
                    break  # Found in this file, move to next file
            except:
                pass
    
    return herbs

def enrich_with_known_data(herbs):
    """Add botanical info, existing profiles, formula flags"""
    existing = {}
    herbs_dir = CONTENT_DIR / "herbs"
    for f in herbs_dir.glob("*.md"):
        content = f.read_text(encoding="utf-8")
        if content.startswith("---"):
            parts = content.split("---", 2)
            if len(parts) >= 3:
                try:
                    import yaml
                    fm = yaml.safe_load(parts[1])
                    existing[f.stem] = {"frontmatter": fm, "content": parts[2]}
                except:
                    pass
    
    for slug, data in herbs.items():
        if slug in SYNONYMS.get("by_slug", {}):
            syn = SYNONYMS["by_slug"][slug]
            data["botanical_name"] = syn.get("botanical", "")
            data["family"] = syn.get("family", "")
            data["all_sanskrit_names"] = syn.get("sanskrit", [])
            data["hindi_names"] = syn.get("hindi", [])
            data["english_names"] = syn.get("english", [])
            data["tamil_names"] = syn.get("tamil", [])
            data["telugu_names"] = syn.get("telugu", [])
            data["arabic_names"] = syn.get("arabic", [])
            data["chinese_names"] = syn.get("chinese", [])
            data["is_combination"] = syn.get("is_combination", False)
            data["components"] = syn.get("components", [])
        
        if slug in existing:
            data["existing_profile"] = existing[slug]["frontmatter"]
            data["existing_content"] = existing[slug]["content"]
        
        if is_combination_component(slug):
            data["is_formula_component"] = True
            data["part_of_formula"] = get_combination_formula(slug)
        
        # Deduplicate
        data["sanskrit_names"] = list(data["sanskrit_names"])
        data["content_files"] = list(set(data["content_files"]))
        for key in ["classical_refs", "formulations", "research_refs", "glossary_definitions"]:
            seen = set()
            unique = []
            for item in data.get(key, []):
                k = json.dumps(item, sort_keys=True) if isinstance(item, dict) else str(item)
                if k not in seen:
                    seen.add(k)
                    unique.append(item)
            data[key] = unique
    
    return herbs

def main():
    print("Extracting herbs from all content...")
    herbs = extract_from_all_content()
    print(f"Found {len(herbs)} herbs with content matches")
    
    herbs = enrich_with_known_data(herbs)
    
    # Add combination formulas
    for formula, components in COMBINATION_FORMULAS.items():
        if formula not in herbs:
            herbs[formula] = {
                "is_combination": True,
                "components": components,
                "botanical_name": f"{formula.title()} (polyherbal formulation)",
                "family": "Polyherbal",
                "combination_formula": formula
            }
    
    output = ROOT / "data" / "herb_index.json"
    with open(output, "w") as f:
        json.dump(herbs, f, indent=2, ensure_ascii=False, default=str)
    
    print(f"\nHerb index saved: {len(herbs)} profiles")
    print(f"  Formula components flagged: {sum(1 for v in herbs.values() if v.get('is_formula_component'))}")
    print(f"  Has classical refs: {sum(1 for v in herbs.values() if v.get('classical_refs'))}")
    print(f"  Has research refs: {sum(1 for v in herbs.values() if v.get('research_refs'))}")
    print(f"  Has existing profile: {sum(1 for v in herbs.values() if v.get('existing_profile'))}")

if __name__ == "__main__":
    main()
