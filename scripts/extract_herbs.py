#!/usr/bin/env python3
"""
Extract herb data from all content sources.
Filters out combination formula components (Triphala, Trikatu, Dashmool, etc.)
Outputs: data/herb_index.json with structured data per herb
"""
import json
import os
import re
from pathlib import Path
from collections import defaultdict

ROOT = Path("/home/shiva/ayurshakti.shop")
CONTENT_DIR = ROOT / "content"

# Load synonyms
with open(ROOT / "data" / "herb_synonyms.json") as f:
    SYNONYMS = json.load(f)

COMBINATION_FORMULAS = SYNONYMS.get("combination_formulas", {})
COMPONENT_TO_FORMULA = {}
for formula, components in COMBINATION_FORMULAS.items():
    for comp in components:
        COMPONENT_TO_FORMULA[comp.lower()] = formula

def normalize_herb_name(name: str) -> str:
    return re.sub(r'[^a-z0-9]', '', name.lower().strip())

def is_combination_component(herb_slug: str) -> bool:
    return herb_slug.lower() in COMPONENT_TO_FORMULA

def get_combination_formula(herb_slug: str) -> str:
    return COMPONENT_TO_FORMULA.get(herb_slug.lower(), "")

def empty_herb_dict():
    return {
        "classical_refs": [],
        "formulations": [],
        "therapeutic_uses": [],
        "dosage_mentions": [],
        "clinical_studies": [],
        "phytochemicals": [],
        "research_refs": [],
        "glossary_definition": "",
        "sanskrit_names": set()
    }

def load_existing_profiles():
    profiles = {}
    herbs_dir = ROOT / "content" / "herbs"
    for f in herbs_dir.glob("*.md"):
        content = f.read_text(encoding="utf-8")
        if content.startswith("---"):
            parts = content.split("---", 2)
            if len(parts) >= 3:
                try:
                    import yaml
                    frontmatter = yaml.safe_load(parts[1])
                    slug = f.stem
                    profiles[slug] = {"frontmatter": frontmatter, "content": parts[2]}
                except:
                    pass
    return profiles

def extract_from_samhitas():
    herbs = defaultdict(empty_herb_dict)
    samhita_dirs = [
        CONTENT_DIR / "samhitas" / "charaka-samhita",
        CONTENT_DIR / "samhitas" / "sushruta-samhita"
    ]
    for samhita_dir in samhita_dirs:
        if not samhita_dir.exists():
            continue
        for f in samhita_dir.glob("*.md"):
            content = f.read_text(encoding="utf-8", errors="ignore")
            chapter_match = re.search(r'chapter[- ]?(\d+)', f.stem, re.IGNORECASE)
            chapter = chapter_match.group(1) if chapter_match else "unknown"
            book = samhita_dir.name.replace("-samhita", "").capitalize()
            for sanskrit, slug in SYNONYMS.get("by_sanskrit", {}).items():
                if is_combination_component(slug):
                    continue
                pattern = r'\b' + re.escape(sanskrit) + r'\b'
                if re.search(pattern, content, re.IGNORECASE):
                    herbs[slug]["classical_refs"].append({
                        "source": f"{book} Samhita",
                        "chapter": chapter,
                        "file": f.name,
                        "context": "mentioned in classical text"
                    })
                    herbs[slug]["sanskrit_names"].add(sanskrit)
    return herbs

def extract_from_canonical_texts():
    herbs = defaultdict(empty_herb_dict)
    canonical_dir = CONTENT_DIR / "canonical_texts"
    if not canonical_dir.exists():
        return herbs
    for f in canonical_dir.glob("*.md"):
        content = f.read_text(encoding="utf-8", errors="ignore")
        title = f.stem.replace("_", " ").title()
        for sanskrit, slug in SYNONYMS.get("by_sanskrit", {}).items():
            if is_combination_component(slug):
                continue
            pattern = r'\b' + re.escape(sanskrit) + r'\b'
            if re.search(pattern, content, re.IGNORECASE):
                herbs[slug]["classical_refs"].append({
                    "source": "Classical Text",
                    "text": title,
                    "file": f.name,
                    "context": "mentioned in classical text"
                })
                herbs[slug]["sanskrit_names"].add(sanskrit)
                formulation_patterns = [
                    rf'{re.escape(sanskrit)}.*?(churna|kwath|arishta|ghrita|taila|rasa|vati|guggulu|lehya)',
                    rf'(churna|kwath|arishta|ghrita|taila|rasa|vati|guggulu|lehya).*?{re.escape(sanskrit)}'
                ]
                for pat in formulation_patterns:
                    matches = re.findall(pat, content, re.IGNORECASE)
                    if matches:
                        for m in matches:
                            herbs[slug]["formulations"].append(m if isinstance(m, str) else " ".join(m))
    return herbs

def extract_from_research():
    herbs = defaultdict(empty_herb_dict)
    research_dirs = [
        CONTENT_DIR / "research",
        CONTENT_DIR / "essays_and_studies"
    ]
    for research_dir in research_dirs:
        if not research_dir.exists():
            continue
        for f in research_dir.glob("*.md"):
            content = f.read_text(encoding="utf-8", errors="ignore")
            title = f.stem.replace("_", " ").title()
            for sanskrit, slug in SYNONYMS.get("by_sanskrit", {}).items():
                if is_combination_component(slug):
                    continue
                pattern = r'\b' + re.escape(sanskrit) + r'\b'
                if re.search(pattern, content, re.IGNORECASE):
                    herbs[slug]["research_refs"].append({
                        "title": title,
                        "file": f.name,
                        "context": "mentioned in research"
                    })
    return herbs

def extract_from_glossary():
    herbs = defaultdict(empty_herb_dict)
    glossary_dir = CONTENT_DIR / "glossary"
    if not glossary_dir.exists():
        return herbs
    for f in glossary_dir.glob("glossary_*.json"):
        try:
            with open(f) as fp:
                data = json.load(fp)
                for term in data.get("terms", []):
                    if isinstance(term, dict) and "term" in term:
                        t = term["term"].lower().strip()
                        for sanskrit, slug in SYNONYMS.get("by_sanskrit", {}).items():
                            if is_combination_component(slug):
                                continue
                            if normalize_herb_name(t) == normalize_herb_name(sanskrit):
                                herbs[slug]["glossary_definition"] = term.get("definition", "")
        except:
            pass
    return herbs

def dedupe_list(lst):
    """Deduplicate list handling both hashable and unhashable items"""
    if not lst:
        return lst
    seen = set()
    result = []
    for x in lst:
        try:
            if x not in seen:
                seen.add(x)
                result.append(x)
        except TypeError:
            # Unhashable (dict/list) - use JSON string
            key = json.dumps(x, sort_keys=True) if isinstance(x, (dict, list)) else str(x)
            if key not in seen:
                seen.add(key)
                result.append(x)
    return result

def merge_extractions(*extractions):
    merged = defaultdict(empty_herb_dict)
    for ext in extractions:
        for slug, data in ext.items():
            for key, value in data.items():
                if key == "sanskrit_names":
                    merged[slug][key].update(value)
                elif isinstance(value, list):
                    merged[slug][key].extend(value)
                elif isinstance(value, str) and value:
                    merged[slug][key] = value
    for slug in merged:
        merged[slug]["sanskrit_names"] = list(merged[slug]["sanskrit_names"])
        for key in merged[slug]:
            if isinstance(merged[slug][key], list):
                merged[slug][key] = dedupe_list(merged[slug][key])
    return merged

def enrich_with_ground_truth(merged):
    existing = load_existing_profiles()
    for slug, data in merged.items():
        if slug in SYNONYMS["by_slug"]:
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
            data["combination_formula"] = get_combination_formula(slug)
            data["is_formula_component"] = True
    return merged

def main():
    print("Extracting herb data from all sources...")
    samhita_data = extract_from_samhitas()
    print(f"  Samhitas: {len(samhita_data)} herbs")
    canonical_data = extract_from_canonical_texts()
    print(f"  Canonical texts: {len(canonical_data)} herbs")
    research_data = extract_from_research()
    print(f"  Research: {len(research_data)} herbs")
    glossary_data = extract_from_glossary()
    print(f"  Glossary: {len(glossary_data)} herbs")
    merged = merge_extractions(samhita_data, canonical_data, research_data, glossary_data)
    print(f"  Merged: {len(merged)} unique herbs")
    enriched = enrich_with_ground_truth(merged)
    final_index = {}
    for slug, data in enriched.items():
        if is_combination_component(slug):
            data["is_formula_component"] = True
            data["part_of_formula"] = get_combination_formula(slug)
        final_index[slug] = data
    for formula, components in COMBINATION_FORMULAS.items():
        if formula not in final_index:
            final_index[formula] = {
                "is_combination": True,
                "components": components,
                "botanical_name": f"{formula.title()} (polyherbal formulation)",
                "family": "Polyherbal",
                "combination_formula": formula
            }
    output = ROOT / "data" / "herb_index.json"
    with open(output, "w") as f:
        json.dump(final_index, f, indent=2, ensure_ascii=False, default=str)
    print(f"\nHerb index saved to {output}")
    print(f"   Total profiles: {len(final_index)}")
    print(f"   Combination formulas: {len(COMBINATION_FORMULAS)}")
    print(f"   Formula components flagged: {sum(1 for v in final_index.values() if v.get('is_formula_component'))}")

if __name__ == "__main__":
    main()
