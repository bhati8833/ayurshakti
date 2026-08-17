#!/usr/bin/env python3
"""
Internal Linking Engine for Herb Profiles
Creates min 3 links per profile based on:
1. Same dosha action (Vata/Pitta/Kapha shamak)
2. Same therapeutic condition
3. Same botanical family
4. Formula relationships
"""
import json
import re
from pathlib import Path
from collections import defaultdict

ROOT = Path("/home/shiva/ayurshakti.shop")

with open(ROOT / "data" / "herb_index.json") as f:
    HERB_INDEX = json.load(f)

with open(ROOT / "data" / "herb_synonyms.json") as f:
    SYNONYMS = json.load(f)

# Build relationship maps
def build_relationship_maps():
    """Build maps for internal linking"""
    
    # Family map
    family_map = defaultdict(list)
    for slug, data in HERB_INDEX.items():
        family = data.get("family", "")
        if family and family not in ["Polyherbal", "Mineral"]:
            family_map[family].append(slug)
    
    # Dosha action map (from dosha_karma text)
    dosha_map = defaultdict(list)
    for slug, data in HERB_INDEX.items():
        dosha_karma = data.get("dosha_karma", "").lower()
        if "vata" in dosha_karma and ("shamak" in dosha_karma or "pacif" in dosha_karma):
            dosha_map["Vata"].append(slug)
        if "pitta" in dosha_karma and ("shamak" in dosha_karma or "pacif" in dosha_karma):
            dosha_map["Pitta"].append(slug)
        if "kapha" in dosha_karma and ("shamak" in dosha_karma or "pacif" in dosha_karma):
            dosha_map["Kapha"].append(slug)
    
    # Condition map (from therapeutic_uses)
    condition_keywords = {
        "stress": ["stress", "anxiety", "cortisol", "adaptogen", "nervous"],
        "sleep": ["sleep", "insomnia", "sedat", "gaba"],
        "digestion": ["digest", "agni", "gut", "constipation", "diarrhea", "appetite"],
        "immunity": ["immun", "viral", "fever", "infection"],
        "joints": ["joint", "arthrit", "inflammation", "pain", "swelling"],
        "skin": ["skin", "acne", "eczema", "dermatitis", "wound"],
        "respiratory": ["cough", "asthma", "bronchit", "lung", "breath"],
        "heart": ["heart", "cardio", "blood pressure", "circulation"],
        "liver": ["liver", "hepatic", "jaundice", "detox"],
        "kidney": ["kidney", "renal", "urinary", "diuretic"],
        "reproductive": ["reproduct", "fertility", "libido", "menstrual", "pcs", "hormone"],
        "cognitive": ["memory", "cognitive", "brain", "neuro", "focus", "concentration"],
        "metabolic": ["diabetes", "blood sugar", "glucose", "metabolic", "weight"],
        "detox": ["detox", "cleanse", "ama", "purif"],
    }
    
    condition_map = defaultdict(list)
    for slug, data in HERB_INDEX.items():
        uses = " ".join(data.get("therapeutic_uses", [])).lower()
        for condition, keywords in condition_keywords.items():
            if any(kw in uses for kw in keywords):
                condition_map[condition].append(slug)
    
    return {
        "family": family_map,
        "dosha": dosha_map,
        "condition": condition_map
    }

RELATIONSHIPS = build_relationship_maps()

def get_internal_links(slug: str, max_links: int = 5) -> list:
    """Get relevant internal links for a herb"""
    links = []
    added = set()
    
    data = HERB_INDEX.get(slug, {})
    if not data:
        return []
    
    # 1. Formula relationships (highest priority)
    if data.get("is_combination"):
        for comp in data.get("components", []):
            if comp != slug and comp in HERB_INDEX:
                title = HERB_INDEX[comp].get("all_sanskrit_names", [comp.title()])[0]
                links.append({
                    "slug": comp,
                    "title": title,
                    "anchor": f"{title} (component herb)",
                    "reason": "formula_component"
                })
                added.add(comp)
    elif data.get("is_formula_component"):
        formula = data.get("part_of_formula", "").lower()
        if formula in ["triphala", "dashmool"]:
            for comp in SYNONYMS.get("combination_formulas", {}).get(formula, []):
                if comp != slug and comp in HERB_INDEX:
                    title = HERB_INDEX[comp].get("all_sanskrit_names", [comp.title()])[0]
                    links.append({
                        "slug": comp,
                        "title": title,
                        "anchor": f"{title} (sister herb in {formula.title()})",
                        "reason": "formula_sibling"
                    })
                    added.add(comp)
    
    # 2. Same family
    family = data.get("family", "")
    if family and family not in ["Polyherbal", "Mineral"]:
        for sib in RELATIONSHIPS["family"].get(family, []):
            if sib != slug and sib not in added:
                title = HERB_INDEX[sib].get("all_sanskrit_names", [sib.title()])[0]
                links.append({
                    "slug": sib,
                    "title": title,
                    "anchor": f"{title} (same {family} family)",
                    "reason": "same_family"
                })
                added.add(sib)
                if len(links) >= 5:
                    break
    
    # 3. Same dosha action
    for dosha in ["Vata", "Pitta", "Kapha"]:
        if len(links) >= 5:
            break
        for sib in RELATIONSHIPS["dosha"].get(dosha, []):
            if sib != slug and sib not in added:
                title = HERB_INDEX[sib].get("all_sanskrit_names", [sib.title()])[0]
                links.append({
                    "slug": sib,
                    "title": title,
                    "anchor": f"{title} ({dosha}-balancing)",
                    "reason": f"same_dosha_{dosha.lower()}"
                })
                added.add(sib)
                if len(links) >= 5:
                    break
    
    # 4. Same condition
    for condition, herbs in RELATIONSHIPS["condition"].items():
        if len(links) >= 5:
            break
        if slug in herbs:
            for sib in herbs:
                if sib != slug and sib not in added:
                    title = HERB_INDEX[sib].get("all_sanskrit_names", [sib.title()])[0]
                    links.append({
                        "slug": sib,
                        "title": title,
                        "anchor": f"{title} (for {condition})",
                        "reason": f"same_condition_{condition}"
                    })
                    added.add(sib)
                    if len(links) >= 5:
                        break
    
    # Return top max_links
    return links[:max_links]

def build_internal_links_section(slug: str, min_links: int = 3) -> str:
    """Build the internal links section markdown"""
    links = get_internal_links(slug, max_links=5)
    
    if len(links) < min_links:
        return ""
    
    # Group by reason for better presentation
    formula_links = [l for l in links if l["reason"].startswith("formula")]
    family_links = [l for l in links if l["reason"] == "same_family"]
    dosha_links = [l for l in links if l["reason"].startswith("same_dosha")]
    condition_links = [l for l in links if l["reason"].startswith("same_condition")]
    
    md = "\n## 🔗 Related Botanical Profiles & Formulations\n\n"
    
    if formula_links:
        md += "**Formula Relationships:**\n"
        for l in formula_links:
            md += f"- [{l['anchor']}](/herbs/{l['slug']})\n"
        md += "\n"
    
    if family_links:
        md += "**Same Botanical Family:**\n"
        for l in family_links:
            md += f"- [{l['anchor']}](/herbs/{l['slug']})\n"
        md += "\n"
    
    if dosha_links:
        md += "**Same Dosha Action:**\n"
        for l in dosha_links:
            md += f"- [{l['anchor']}](/herbs/{l['slug']})\n"
        md += "\n"
    
    if condition_links:
        md += "**Similar Therapeutic Uses:**\n"
        for l in condition_links:
            md += f"- [{l['anchor']}](/herbs/{l['slug']})\n"
        md += "\n"
    
    return md

# Test
if __name__ == "__main__":
    with open("/home/shiva/ayurshakti.shop/data/herb_index.json") as f:
        HERB_INDEX = json.load(f)
    
    # Test a few
    for slug in ["ashwagandha", "arjuna", "guggulu", "triphala", "dashmool"]:
        links = get_internal_links(slug, max_links=5)
        print(f"\n{slug}: {len(links)} links")
        for l in links:
            print(f"  - {l['slug']}: {l['anchor']} ({l['reason']})")
