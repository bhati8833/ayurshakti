#!/usr/bin/env python3
"""
Generate herb profile markdown from herb_index.json
- Conditional sections (only render if data exists)
- Idempotency: skip if status: Published in existing frontmatter
- Triphala/Dashmool exclusion: don't list formula components as ingredients
- Outputs to content/herbs_draft/
"""
import json
import os
import re
from pathlib import Path
from datetime import datetime
from collections import defaultdict

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

def is_combination_component(herb_slug: str) -> bool:
    return herb_slug.lower() in COMPONENT_TO_FORMULA

def get_combination_formula(herb_slug: str) -> str:
    return COMPONENT_TO_FORMULA.get(herb_slug.lower(), "")

def load_existing_frontmatter(slug: str):
    """Load existing frontmatter if file exists"""
    f = HERBS_DIR / f"{slug}.md"
    if f.exists():
        content = f.read_text(encoding="utf-8")
        if content.startswith("---"):
            parts = content.split("---", 2)
            if len(parts) >= 3:
                try:
                    import yaml
                    return yaml.safe_load(parts[1])
                except:
                    pass
    return None

def should_skip_generation(slug: str) -> bool:
    """Idempotency check: skip if already Published"""
    fm = load_existing_frontmatter(slug)
    if fm and fm.get("status") == "Published":
        print(f"  ⏭️  Skipping {slug}: already Published")
        return True
    return False

def filter_ingredient_list(ingredients: list, current_herb: str) -> list:
    """Remove combination formula components from ingredient lists"""
    if not ingredients:
        return []
    filtered = []
    for ing in ingredients:
        ing_lower = ing.lower().strip()
        # Check if this ingredient is a component herb
        is_component = False
        for formula, components in COMBINATION_FORMULAS.items():
            if ing_lower in [c.lower() for c in components]:
                is_component = True
                break
        if not is_component:
            filtered.append(ing)
    return filtered

# ============================================================
# INTERNAL LINKING ENGINE
# ============================================================
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

def build_relationship_maps():
    """Build maps for internal linking across all herbs"""
    family_map = defaultdict(list)
    dosha_map = defaultdict(list)
    condition_map = defaultdict(list)
    
    for slug, data in HERB_INDEX.items():
        # Family map
        family = data.get("family", "")
        if family and family not in ["Polyherbal", "Mineral"]:
            family_map[family].append(slug)
        
        # Dosha map
        dosha_karma = data.get("dosha_karma", "").lower()
        if "vata" in dosha_karma and ("shamak" in dosha_karma or "pacif" in dosha_karma):
            dosha_map["Vata"].append(slug)
        if "pitta" in dosha_karma and ("shamak" in dosha_karma or "pacif" in dosha_karma):
            dosha_map["Pitta"].append(slug)
        if "kapha" in dosha_karma and ("shamak" in dosha_karma or "pacif" in dosha_karma):
            dosha_map["Kapha"].append(slug)
        
        # Condition map
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
    
    return links[:5]

def build_internal_links_section(slug: str, min_links: int = 2) -> str:
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

def format_section(title: str, content: str, level: int = 2) -> str:
    """Format a section if content exists"""
    if not content or not content.strip():
        return ""
    h = "#" * level
    return f"\n{h} {title}\n\n{content.strip()}\n"

def build_nomenclature_table(data: dict) -> str:
    """Build Section 1: Botanical & Multilingual Nomenclature"""
    rows = []
    if data.get("botanical_name"):
        rows.append(("**Botanical Name**", f"*{data['botanical_name']}*"))
    if data.get("family"):
        rows.append(("**Family**", data["family"]))
    if data.get("all_sanskrit_names"):
        rows.append(("**Sanskrit Names**", ", ".join(data["all_sanskrit_names"])))
    if data.get("hindi_names"):
        rows.append(("**Hindi Name**", ", ".join(data["hindi_names"])))
    if data.get("english_names"):
        rows.append(("**English Names**", ", ".join(data["english_names"])))
    if data.get("tamil_names"):
        rows.append(("**Tamil Name**", ", ".join(data["tamil_names"])))
    if data.get("telugu_names"):
        rows.append(("**Telugu Name**", ", ".join(data["telugu_names"])))
    if data.get("arabic_names"):
        rows.append(("**Arabic Name**", ", ".join(data["arabic_names"])))
    if data.get("chinese_names"):
        rows.append(("**Chinese Name**", ", ".join(data["chinese_names"])))
    
    if not rows:
        return ""
    
    table = "| Parameter | Details |\n| :--- | :--- |\n"
    for param, detail in rows:
        table += f"| {param} | {detail} |\n"
    return table

def build_taseer_section(data: dict) -> str:
    """Build Section 2: Ayurvedic Energy Profile (Taseer)"""
    parts = []
    if data.get("rasa"):
        parts.append(f"- **Rasa (Taste):** {data['rasa']}")
    if data.get("guna"):
        parts.append(f"- **Guna (Qualities):** {data['guna']}")
    if data.get("virya"):
        parts.append(f"- **Virya (Taseer / Potency):** {data['virya']}")
    if data.get("vipaka"):
        parts.append(f"- **Vipaka (Post-Digestive Effect):** {data['vipaka']}")
    if data.get("dosha_karma"):
        parts.append(f"- **Dosha Karma (Dosha Impact):** {data['dosha_karma']}")
    if not parts:
        return ""
    return "\n".join(parts)

def build_phytochemical_section(data: dict) -> str:
    """Build Section 3: Phytochemical Composition"""
    items = data.get("phytochemicals", [])
    if not items:
        return ""
    return "\n".join([f"- {item}" for item in items])

def build_clinical_uses(data: dict) -> str:
    """Build Section 4: Primary Clinical Use Cases"""
    items = data.get("therapeutic_uses", [])
    if not items:
        return ""
    return "\n".join([f"{i+1}. {item}" for i, item in enumerate(items)])

def build_formulations_section(data: dict) -> str:
    """Build Section 5: Classical Formulations & Dosage"""
    formulations = data.get("formulations", [])
    if not formulations:
        return ""
    filtered = filter_ingredient_list(formulations, data.get("slug", ""))
    if not filtered:
        return ""
    return "\n".join([f"- **{f}**" for f in filtered])

def build_classical_refs(data: dict) -> str:
    """Build Section: Classical References"""
    refs = data.get("classical_refs", [])
    if not refs:
        return ""
    lines = []
    for ref in refs:
        source = ref.get("source", "")
        chapter = ref.get("chapter", "")
        file = ref.get("file", "")
        context = ref.get("context", "")
        line = f"- **{source}**"
        if chapter:
            line += f", Chapter {chapter}"
        if file:
            line += f" ({file})"
        if context:
            line += f" — {context}"
        lines.append(line)
    return "\n".join(lines)

def build_research_refs(data: dict) -> str:
    """Build Section: Modern Research"""
    refs = data.get("research_refs", [])
    if not refs:
        return ""
    lines = []
    for ref in refs:
        title = ref.get("title", "")
        file = ref.get("file", "")
        lines.append(f"- {title} ({file})")
    return "\n".join(lines)

def build_dosage_section(data: dict) -> str:
    """Build Section: Dosage from existing profile or extracted"""
    if data.get("existing_profile", {}).get("content"):
        # Extract dosage from existing content
        content = data["existing_profile"]["content"]
        dosage_match = re.search(r'(?i)(dosage|posology|administration).*?(?=\n##|\n---|\Z)', content, re.DOTALL)
        if dosage_match:
            return dosage_match.group(0).strip()
    return ""

def build_tldr(data: dict, slug: str) -> str:
    """Build TL;DR block - 2-3 sentence direct answer"""
    botanical = data.get("botanical_name", slug.replace("-", " ").title())
    sanskrit = data.get("all_sanskrit_names", [None])[0]
    category = data.get("family", "Ayurvedic herb")
    
    if data.get("is_combination"):
        components = ", ".join(data.get("components", []))
        return f"""> **TL;DR:** {botanical} ({sanskrit}) is a classical Ayurvedic polyherbal formulation combining {components}. It is traditionally used for {category.lower()} and balancing doshas. Consult a qualified practitioner for personalized dosage."""
    
    # For single herbs - generate based on available data
    uses = data.get("therapeutic_uses", [])
    if uses:
        primary_use = uses[0].lower()
        return f"""> **TL;DR:** {botanical} ({sanskrit}) is a {category} herb traditionally used for {primary_use}. It works by balancing Vata, Pitta, and Kapha doshas. Always consult a qualified Ayurvedic practitioner before use."""
    
    return f"""> **TL;DR:** {botanical} ({sanskrit}) is a {category} herb in classical Ayurvedic medicine. It is valued for its therapeutic properties and dosha-balancing effects. Consult a qualified practitioner for personalized guidance."""


def build_faq_section(data: dict, slug: str) -> tuple:
    """Build FAQ section with 5 Q&A pairs and FAQPage JSON-LD schema"""
    botanical = data.get("botanical_name", slug.replace("-", " ").title())
    sanskrit = data.get("all_sanskrit_names", [None])[0] or slug.title()
    category = data.get("family", "Ayurvedic herb")
    is_combo = data.get("is_combination", False)
    is_component = data.get("is_formula_component", False)
    formula = data.get("part_of_formula", "").title() if is_component else ""
    
    # Generate 5 FAQs based on herb type
    if is_combo:
        faqs = [
            {
                "q": f"What is {sanskrit} ({botanical})?",
                "a": f"{sanskrit} is a classical Ayurvedic polyherbal formulation traditionally used in {data.get('family', 'Ayurvedic medicine').lower()}. It combines multiple herbs for synergistic therapeutic effects."
            },
            {
                "q": f"What are the ingredients in {sanskrit}?",
                "a": f"{sanskrit} contains: {', '.join(data.get('components', []))}. These herbs work synergistically for enhanced therapeutic benefit."
            },
            {
                "q": f"What are the benefits of {sanskrit}?",
                "a": f"Traditionally used for {data.get('family', 'dosha balancing').lower()}. It helps balance Vata, Pitta, and Kapha doshas and supports overall wellness."
            },
            {
                "q": f"How to take {sanskrit}?",
                "a": "Dosage varies by individual constitution and condition. Typically taken as churna (powder), kwath (decoction), or tablet form. Consult an Ayurvedic practitioner for personalized dosage."
            },
            {
                "q": f"Are there any side effects of {sanskrit}?",
                "a": "Generally safe when taken as directed. May cause mild digestive upset in sensitive individuals. Pregnant/nursing women and those on medications should consult a healthcare provider before use."
            }
        ]
    elif is_component:
        faqs = [
            {
                "q": f"What is {sanskrit} ({botanical})?",
                "a": f"{sanskrit} is a {category} herb in classical Ayurvedic medicine. It is also a key component of the {formula} formulation."
            },
            {
                "q": f"What are the main benefits of {sanskrit}?",
                "a": f"Traditionally used for {data.get('therapeutic_uses', ['general wellness'])[0].lower() if data.get('therapeutic_uses') else 'dosha balancing'}. Supports overall health and dosha balance."
            },
            {
                "q": f"How is {sanskrit} used in {formula}?",
                "a": f"In {formula}, {sanskrit} works synergistically with other herbs to enhance the formulation's therapeutic effect on {data.get('family', 'dosha balance').lower()}."
            },
            {
                "q": f"How to take {sanskrit}?",
                "a": "Available as churna (powder), kwath (decoction), or capsule. Typical dosage: 3-6g powder or 15-30ml decoction twice daily. Consult practitioner for personalized guidance."
            },
            {
                "q": f"Any precautions for {sanskrit}?",
                "a": "Generally safe. Pregnant/nursing women, those with medical conditions, or on medications should consult an Ayurvedic practitioner before use."
            }
        ]
    else:
        uses = data.get("therapeutic_uses", ["general wellness"])
        primary_use = uses[0].lower() if uses else "dosha balancing"
        faqs = [
            {
                "q": f"What is {sanskrit} ({botanical})?",
                "a": f"{sanskrit} is a {category} herb in classical Ayurvedic medicine. It is valued for its {primary_use} properties and ability to balance doshas."
            },
            {
                "q": f"What are the benefits of {sanskrit}?",
                "a": f"Traditionally used for {primary_use}. It helps balance Vata, Pitta, and Kapha doshas. {'. '.join(uses[:2]) if uses else 'Supports overall wellness and vitality.'}"
            },
            {
                "q": f"How to use {sanskrit}?",
                "a": "Available as powder (churna), decoction (kwath), tablet, or capsule. Typical dosage: 3-6g powder or 15-30ml decoction twice daily with warm water or as directed by practitioner."
            },
            {
                "q": f"Can {sanskrit} be taken daily?",
                "a": "Yes, many Ayurvedic herbs are taken daily as rasayana (rejuvenative). However, cycling (e.g., 6 weeks on, 2 weeks off) is often recommended. Consult an Ayurvedic practitioner for your constitution."
            },
            {
                "q": f"Any side effects or interactions of {sanskrit}?",
                "a": "Generally safe at recommended doses. May interact with certain medications (blood thinners, diabetes meds, sedatives). Pregnant/nursing women and those with medical conditions should consult a healthcare provider before use."
            }
        ]
    
    # Build FAQ markdown
    faq_md = "\n## ❓ 9. Frequently Asked Questions\n\n"
    for i, faq in enumerate(faqs, 1):
        faq_md += f"### Q{i}: {faq['q']}\n\n**A:** {faq['a']}\n\n"
    
    # Build FAQPage JSON-LD schema
    schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": faq["q"],
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": faq["a"]
                }
            }
            for faq in faqs
        ]
    }
    
    schema_script = f'\n<script type="application/ld+json">\n{json.dumps(schema, indent=2, ensure_ascii=False)}\n</script>\n'
    
    return faq_md, schema_script


def generate_herb_profile(slug: str, data: dict) -> str:
    """Generate complete herb profile markdown"""
    
    # Get display title
    title = data.get("botanical_name", slug.replace("-", " ").title())
    if data.get("all_sanskrit_names"):
        sanskrit = data["all_sanskrit_names"][0]
        title = f"{sanskrit} ({data.get('botanical_name', '')})"
    
    # Category
    category = "Herb Profiles"
    if data.get("is_combination"):
        category = "Classical Formulations"
    elif data.get("is_formula_component"):
        category = "Herb Profiles"
    
    # Labels
    labels = ["Herb Profiles"]
    if data.get("all_sanskrit_names"):
        labels.append(data["all_sanskrit_names"][0])
    if data.get("is_combination"):
        labels.append("Classical Formulation")
    elif data.get("is_formula_component"):
        formula = data.get("part_of_formula", "").title()
        labels.append(f"Component of {formula}")
    
    # Description for SEO
    desc_parts = []
    if data.get("botanical_name"):
        desc_parts.append(f"Complete botanical profile of {data['botanical_name']}")
    if data.get("family"):
        desc_parts.append(f"featuring scientific taxonomy, multilingual names")
    if data.get("all_sanskrit_names"):
        desc_parts.append(f"Ayurvedic Taseer (Virya)")
    if data.get("is_combination"):
        desc_parts.append(f"Classical polyherbal formulation with {len(data.get('components', []))} ingredients")
    description = ". ".join(desc_parts) + "."
    
    # Frontmatter
    fm = {
        "title": title,
        "category": category,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "status": "Draft",
        "description": description,
        "labels": labels
    }
    
    # Build sections - Force minimum 5 H2 sections for SEO
    sections = []
    
    # Section 1: Nomenclature (ALWAYS - required)
    nomenclature = build_nomenclature_table(data)
    if nomenclature:
        sections.append(format_section("🌿 1. Botanical & Multilingual Nomenclature", nomenclature))
    else:
        sections.append(format_section("🌿 1. Botanical & Multilingual Nomenclature", 
            "*Botanical name and multilingual nomenclature data being compiled.*"))
    
    # Section 2: Taseer (Ayurvedic Energy Profile) - ALWAYS
    taseer = build_taseer_section(data)
    if taseer:
        sections.append(format_section("🔥 2. Ayurvedic Energy Profile (Taseer & Dravyaguna)", taseer))
    else:
        placeholder = "*Rasa, Guna, Virya, Vipaka, and Dosha Karma data being compiled from classical texts.*"
        sections.append(format_section("🔥 2. Ayurvedic Energy Profile (Taseer & Dravyaguna)", placeholder))
    
    # Section 3: Phytochemical - ALWAYS
    phyto = build_phytochemical_section(data)
    if phyto:
        sections.append(format_section("🧪 3. Phytochemical & Nutritional Composition", phyto))
    else:
        placeholder = "*Key phytochemical constituents and nutritional profile being documented from classical and modern research.*"
        sections.append(format_section("🧪 3. Phytochemical & Nutritional Composition", placeholder))
    
    # Section 4: Clinical Uses - ALWAYS
    clinical = build_clinical_uses(data)
    if clinical:
        sections.append(format_section("💡 4. Primary Clinical Use Cases", clinical))
    else:
        placeholder = "*Traditional therapeutic indications and clinical applications being compiled from Samhita references and modern studies.*"
        sections.append(format_section("💡 4. Primary Clinical Use Cases", placeholder))
    
    # Section 5: Formulations - ALWAYS
    form = build_formulations_section(data)
    if form:
        sections.append(format_section("💊 5. Classical Formulations & Dosage", form))
    else:
        placeholder = "*Classical formulations (churna, kwath, arishta, ghrita) and dosage guidelines being documented from Samhita references.*"
        sections.append(format_section("💊 5. Classical Formulations & Dosage", placeholder))
    
    # Section 6: Classical References (conditional but recommended)
    classical = build_classical_refs(data)
    if classical:
        sections.append(format_section("📜 6. Classical References", classical))
    
    # Section 7: Modern Research (conditional but recommended)
    research = build_research_refs(data)
    if research:
        sections.append(format_section("🔬 7. Modern Research Summary", research))
    
    # Section 8: Internal Links (NEW - Internal Linking Engine)
    internal_links = build_internal_links_section(slug, min_links=3)
    if internal_links:
        sections.append(internal_links)
    else:
        # Fallback to old related herbs logic
        related = []
        if data.get("is_combination"):
            for comp in data.get("components", []):
                related.append(f"- [{comp.title()}](/herbs/{comp})")
        elif data.get("is_formula_component"):
            formula = data.get("part_of_formula", "").title()
            related.append(f"- Part of **{formula}** formulation")
            for comp in COMBINATION_FORMULAS.get(formula.lower(), []):
                if comp != slug:
                    related.append(f"- Sister herb: [{comp.title()}](/herbs/{comp})")
        
        if related:
            sections.append(format_section("🔗 Related Botanical Profiles & Formulations", "\n".join(related)))
    
    # Build FAQ section + schema
    faq_md, faq_schema = build_faq_section(data, slug)
    sections.append(faq_md)
    
    # Assemble
    body = "".join(sections)
    
    # Build TL;DR
    tldr = build_tldr(data, slug)
    
    # Add disclaimer
    disclaimer = "\n---\n\n> **⚠️ Medical Disclaimer:** The information on this website is for informational and educational purposes only. It is not a substitute for professional medical advice, diagnosis, or treatment. Always consult a qualified healthcare provider before starting any supplement, herb, or Ayurvedic treatment, especially if you are pregnant, nursing, have a medical condition, or are taking prescription medications."
    
    # Final markdown
    md = f"""---
title: "{title}"
category: "{category}"
date: "{datetime.now().strftime('%Y-%m-%d')}"
status: "Draft"
description: "{description}"
labels: {json.dumps(labels)}
---

# {title}

{tldr}

{body}
{faq_schema}
{disclaimer}
"""
    return md

def main():
    DRAFT_DIR.mkdir(parents=True, exist_ok=True)
    
    with open(INDEX_FILE) as f:
        herb_index = json.load(f)
    
    print(f"Generating profiles for {len(herb_index)} herbs...")
    generated = 0
    skipped = 0
    
    for slug, data in herb_index.items():
        data["slug"] = slug
        
        if should_skip_generation(slug):
            skipped += 1
            continue
        
        md = generate_herb_profile(slug, data)
        
        output_file = DRAFT_DIR / f"{slug}.md"
        output_file.write_text(md, encoding="utf-8")
        generated += 1
        print(f"  ✅ Generated: {slug}.md")
    
    print(f"\n📊 Summary:")
    print(f"  Generated: {generated}")
    print(f"  Skipped (Published): {skipped}")
    print(f"  Output dir: {DRAFT_DIR}")

if __name__ == "__main__":
    main()
