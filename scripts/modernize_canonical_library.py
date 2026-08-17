#!/usr/bin/env python3
"""
scripts/modernize_canonical_library.py
AyurShakti Comprehensive Canonical Text Library Modernization Engine.

Transforms all monolithic canonical text files into:
1. Volume Index Hub Pages (Master Overview & Chapter Directory)
2. Dedicated Chapter Pages with:
   - Pure International Medical English Titles & Slugs
   - Strict H1/H2/H3 Heading Hierarchy (for dynamic Sticky TOC)
   - Top E-E-A-T Clinical Executive Summary (TL;DR)
   - Inter-chapter Navigation (Prev / Next Chapter links)
   - Bottom 5-Question FAQ section
   - Embedded JSON-LD MedicalWebPage & FAQPage Schema
   - Clean YAML frontmatter (Author: Suresh Bhati)
"""

import os
import sys
import re
import glob
import json
import argparse
from typing import List, Dict, Tuple

# Volume Title & Slug Standardizer Dictionary
VOLUME_MAP = {
    "sushruta_samhita_volume_1_sutrasthana": {
        "title": "Sushruta Samhita Sutrasthana: Fundamental Principles of Ayurvedic Surgery and Medicine",
        "slug": "sushruta-samhita-sutrasthana-fundamental-principles",
        "category": "Sutrasthana",
        "desc": "Classical foundational handbook of Ayurvedic surgery, surgical tools, wound care, pharmacology, and medical ethics."
    },
    "sushruta_samhita_volume_2_nidanasthana": {
        "title": "Sushruta Samhita Nidanasthana: Diagnostic Pathology and Clinical Etiology Guide",
        "slug": "sushruta-samhita-nidanasthana-diagnostic-pathology",
        "category": "Nidanasthana",
        "desc": "Classical Ayurvedic pathology guide detailing etiology, signs, and diagnosis of surgical and systemic diseases."
    },
    "sushruta_samhita_volume_3_sharirasthana": {
        "title": "Sushruta Samhita Sharirasthana: Human Anatomy, Embryology and Marma Science",
        "slug": "sushruta-samhita-sharirasthana-anatomy-and-embryology",
        "category": "Sharirasthana",
        "desc": "Ancient Indian anatomical treatise covering embryology, vital organs, cadaver dissection, and Marma vital points."
    },
    "sushruta_samhita_volume_4_cikitsasthana": {
        "title": "Sushruta Samhita Cikitsasthana: Surgical Therapeutics and Clinical Operations",
        "slug": "sushruta-samhita-cikitsasthana-surgical-therapeutics",
        "category": "Cikitsasthana",
        "desc": "Comprehensive surgical treatment manual covering post-operative recovery, wound management, and rejuvenation."
    },
    "sushruta_samhita_volume_5_kalpasthana": {
        "title": "Ayurvedic Toxicology and Agada Tantra: Sushruta Samhita Kalpasthana Complete Guide",
        "slug": "ayurvedic-toxicology-and-agada-tantra-sushruta-samhita-kalpasthana",
        "category": "Kalpasthana",
        "desc": "Classical Ayurvedic guide to toxicology (Kalpasthana), emergency snakebite antidotes, plant & mineral toxins, rabies management, and sonic detoxification."
    },
    "sushruta_samhita_volume_6_uttara_tantra": {
        "title": "Sushruta Samhita Uttara Tantra: Ophthalmology, ENT, Pediatrics and Internal Medicine",
        "slug": "sushruta-samhita-uttara-tantra-ophthalmology-ent-pediatrics",
        "category": "Uttara Tantra",
        "desc": "Master clinical supplement detailing cataract surgery, eye diseases, ENT protocols, pediatrics, and internal medicine."
    },
    "charaka_samhita_english_translation": {
        "title": "Charaka Samhita Complete Translation: Fundamental Concepts of Internal Medicine",
        "slug": "charaka-samhita-complete-translation-internal-medicine",
        "category": "Charaka Samhita",
        "desc": "The quintessential classical text of Ayurvedic internal medicine, Panchakarma, diagnosis, and longevity."
    },
    "rasa_jala_nidhi_vol_1": {
        "title": "Rasa Jala Nidhi Volume 1: Mercury Purification and Alchemy Science",
        "slug": "rasa-jala-nidhi-vol-1-mercury-purification-alchemy",
        "category": "Rasa Shastra",
        "desc": "Classical treatise on iatrochemistry, mercury processing (Parada), laboratory apparatus, and alchemical initiations."
    },
    "rasa_jala_nidhi_vol_2": {
        "title": "Rasa Jala Nidhi Volume 2: Minerals, Gems and Uparasa Pharmacology",
        "slug": "rasa-jala-nidhi-vol-2-minerals-gems-uparasa",
        "category": "Rasa Shastra",
        "desc": "Detailed guide on mineral processing, Uparasa, gems, metals, and therapeutic metallic Bhasma preparations."
    },
    "rasa_jala_nidhi_vol_3": {
        "title": "Rasa Jala Nidhi Volume 3: Metals, Gems and Mineral Processing",
        "slug": "rasa-jala-nidhi-vol-3-metals-gems-processing",
        "category": "Rasa Shastra",
        "desc": "Comprehensive handbook on precious metals, gold, silver, copper, and mineral alchemy in Ayurvedic pharmacology."
    },
    "rasa_jala_nidhi_vol_4": {
        "title": "Rasa Jala Nidhi Volume 4: Iatrochemistry and Therapeutic Formulations",
        "slug": "rasa-jala-nidhi-vol-4-iatrochemistry-therapeutics",
        "category": "Rasa Shastra",
        "desc": "Master clinical formulation text detailing mercury-based therapeutics for systemic diseases."
    },
    "rasa_jala_nidhi_vol_5": {
        "title": "Rasa Jala Nidhi Volume 5: Treatment of Complex Chronic Afflictions",
        "slug": "rasa-jala-nidhi-vol-5-treatment-complex-chronic-diseases",
        "category": "Rasa Shastra",
        "desc": "Clinical guide for managing severe chronic conditions using purified mineral and herbometallic formulations."
    },
    "vrikshayurveda_and_environmental_philosophy": {
        "title": "Vrikshayurveda and Environmental Philosophy: Ancient Plant Science and Botany",
        "slug": "vrikshayurveda-environmental-philosophy-ancient-botany",
        "category": "Vrikshayurveda",
        "desc": "Classical Indian agricultural and botanical science manual detailing tree nursing, soil care, and plant pathology."
    },
    "marma_sastra_and_ayurveda": {
        "title": "Marma Sastra and Ayurvedic Science: Vital Energy Points and Clinical Practice",
        "slug": "marma-sastra-ayurveda-vital-points-guide",
        "category": "Marma Science",
        "desc": "Clinical monograph on 107 Marma vital points, trauma management, and therapeutic pressure points."
    },
    "surgery_in_ancient_india": {
        "title": "Ancient Indian Surgical Science: Historical Methods and Techniques",
        "slug": "ancient-indian-surgical-science-historical-methods",
        "category": "Ayurvedic Surgery",
        "desc": "Academic investigation into surgical instruments, rhinoplasty, lithotomy, and operative techniques in ancient India."
    }
}

def clean_heading_text(heading: str) -> str:
    """Clean raw markdown heading into a Pure International English Title."""
    h = re.sub(r'^##\s*', '', heading).strip()
    h = re.sub(r'^[#\s]+', '', h)
    # Strip leading digits and dots like '1. ', '2. 3. ', 'Chapter I - ', 'Part 1 - '
    h = re.sub(r'^\d+\.\s*', '', h)
    h = re.sub(r'^\d+\.\s*\d+\.\s*', '', h)
    h = re.sub(r'^(?:Chapter|Canto|Part|Vol|Volume)\s+[IVXLCDM\d]+[\s\:\-\–]*', '', h, flags=re.I)
    h = re.sub(r'^(?:Chapter|Canto|Part|Vol|Volume)\s+\d+[\s\:\-\–]*', '', h, flags=re.I)
    h = re.sub(r'\bby\s+[A-Za-z\s.]+', '', h, flags=re.I)
    h = h.replace('"', "'").replace('\n', ' ').strip(' :-–—.')
    return h if h else "General Discourse"

def slugify(text: str) -> str:
    """Generate clean URL slug."""
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    text = re.sub(r'[\s-]+', '-', text).strip('-')
    return text[:80]

def clean_scraped_boilerplate(text: str) -> str:
    """Purge scraped paragraphs, word counts, and legacy header noise."""
    if not text:
        return ""
    text = re.sub(r'^\s*\*\*Author\s*/\s*Source:\*\*\s*by\s*.*$', '', text, flags=re.M | re.I)
    text = re.sub(r'^\s*\*\*Total\s+Chapters/Sections:\*\*\s*\d+$', '', text, flags=re.M | re.I)
    text = re.sub(r'Total\s+Chapters/Sections:\s*\d+', '', text, flags=re.I)
    text = re.sub(r'by\s+[A-Za-z\s.]+\|\s*\d{4}\s*\|\s*[\d,]+\s*words', '', text, flags=re.I)
    text = re.sub(r'Sushruta Samhita, Volume \d+:.*?\n', '', text, flags=re.I)
    text = re.sub(r'This current book, the Kalpa-sthana.*?various other subjects\.', '', text, flags=re.S | re.I)
    text = re.sub(r'The Sushruta Samhita is the most representative work.*?medicine\.', '', text, flags=re.S | re.I)
    text = re.sub(r'Susruta-samhita is recognized as\.\.\.', '', text, flags=re.I)
    text = re.sub(r'This page relates [‘\'"].*?[’\'"] found in the study on diseases.*?for study\.', '', text, flags=re.S | re.I)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()

def convert_to_h3_subheadings(text: str) -> str:
    """Convert unformatted recipe & symptom headers into H3 subheadings for sticky TOC."""
    lines = text.split('\n')
    new_lines = []
    for line in lines:
        m = re.match(r'^\s*([A-Z0-9][a-zA-Z0-9\s\,\-\(\)\/]{3,60}):\s*[\—\-–]\s*$', line)
        if m:
            heading_title = m.group(1).strip()
            new_lines.append(f'\n### {heading_title}\n')
        else:
            new_lines.append(line)
    return '\n'.join(new_lines)

def build_faq_and_schema(chapter_title: str, topic_desc: str, slug: str) -> tuple[str, str]:
    """Build 5-Question FAQ section and JSON-LD FAQPage & MedicalWebPage Schema."""
    qas = [
        {
            "q": f"What are the primary medical concepts explained in {chapter_title}?",
            "a": f"This chapter covers {topic_desc}, offering authoritative classical Ayurvedic principles, therapeutic procedures, and clinical formulations."
        },
        {
            "q": "What is the classical authority and origin of these medical teachings?",
            "a": "These teachings originate from classical Sanskrit Samhitas and ancient scholar manuscripts, curated and structured for modern E-E-A-T clinical reference by Suresh Bhati."
        },
        {
            "q": "How are the therapeutic remedies in this chapter utilized in clinical practice?",
            "a": "Remedies described in this text are customized based on individual Dosha constitution, severe pathology staging, and professional Ayurvedic medical guidance."
        },
        {
            "q": "Does this text outline preventive and curative healthcare measures?",
            "a": "Yes, it provides comprehensive preventive daily routines (Dinacharya), dietary rules, herbal formulations, and therapeutic interventions."
        },
        {
            "q": "Where can I view the complete directory of canonical Ayurvedic chapters?",
            "a": "The full library index and chapter directories are accessible on the AyurShakti Canonical Texts portal."
        }
    ]
    
    faq_md = "\n\n---\n\n## Frequently Asked Questions (FAQ)\n\n"
    for item in qas:
        faq_md += f"### {item['q']}\n{item['a']}\n\n"
        
    json_ld = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "MedicalWebPage",
                "@id": f"https://ayurshakti.shop/articles/{slug}#webpage",
                "url": f"https://ayurshakti.shop/articles/{slug}",
                "name": chapter_title,
                "description": topic_desc,
                "author": {
                    "@type": "Person",
                    "name": "Suresh Bhati",
                    "url": "https://ayurshakti.shop/about"
                },
                "publisher": {
                    "@type": "Organization",
                    "name": "AyurShakti",
                    "url": "https://ayurshakti.shop"
                }
            },
            {
                "@type": "FAQPage",
                "@id": f"https://ayurshakti.shop/articles/{slug}#faq",
                "mainEntity": [
                    {
                        "@type": "Question",
                        "name": item["q"],
                        "acceptedAnswer": {
                            "@type": "Answer",
                            "text": item["a"]
                        }
                    } for item in qas
                ]
            }
        ]
    }
    
    schema_script = f'\n\n<script type="application/ld+json">\n{json.dumps(json_ld, indent=2)}\n</script>\n'
    return faq_md, schema_script

def process_file(filepath: str):
    if not os.path.exists(filepath):
        return
    filename = os.path.basename(filepath)
    # Skip already generated chapter files
    if any(x in filename for x in ['-ch1.md', '-ch2.md', '-ch3.md', '-ch4.md', '-ch5.md', '-ch6.md', '-ch7.md', '-ch8.md']) or filename == 'ayurvedic-toxicology-and-agada-tantra-sushruta-samhita-kalpasthana.md':
        return

    print(f"\n[+] Modernizing Monolithic Text: {filename}")
    filename_base = filename.replace('.md', '')
    
    with open(filepath, 'r', encoding='utf-8') as f:
        raw_content = f.read()

    # Find volume metadata
    vol_info = None
    for key, info in VOLUME_MAP.items():
        if key in filename_base:
            vol_info = info
            break
            
    if not vol_info:
        clean_name = re.sub(r'_by_.*$', '', filename_base).replace('_', ' ').title()
        vol_info = {
            "title": f"{clean_name}: Comprehensive Classical Ayurvedic Research Monograph",
            "slug": slugify(clean_name),
            "category": "Canonical Texts",
            "desc": f"Classical Ayurvedic research monograph and medical treatise on {clean_name}."
        }
        
    vol_title = vol_info["title"]
    vol_slug = vol_info["slug"]
    vol_desc = vol_info["desc"]
    
    sections = re.split(r'\n(?=##\s*)', raw_content)
    intro_sections = []
    chapter_list = []
    
    for sec in sections:
        sec_clean = sec.strip()
        if not sec_clean:
            continue
        first_line = sec_clean.split('\n')[0]
        if any(x in first_line.lower() for x in ['preface', 'intro', 'title page', 'acknowledg', 'abstract', 'synopsis', 'plate']):
            intro_sections.append(sec_clean)
        else:
            chapter_list.append(sec_clean)
            
    # If no chapters found, treat whole file as 1 major chapter
    if not chapter_list:
        chapter_list = [raw_content]
        
    # Cap excessive sub-chunks to maximum 50 quality chapters to prevent RAM thrashing
    if len(chapter_list) > 50:
        print(f"    Notice: Consolidating {len(chapter_list)} micro-sections into 30 structured major chapters.")
        chunk_size = len(chapter_list) // 30 + 1
        consolidated = []
        for i in range(0, len(chapter_list), chunk_size):
            chunk_group = chapter_list[i:i+chunk_size]
            first_h2 = chunk_group[0].split('\n')[0]
            group_body = "\n\n".join(chunk_group)
            consolidated.append(group_body)
        chapter_list = consolidated

    print(f"    Generated {len(chapter_list)} chapter sections.")
    
    # -------------------------------------------------------------
    # 1. CREATE VOLUME MASTER HUB PAGE
    # -------------------------------------------------------------
    hub_frontmatter = f"""---
title: "{vol_title}"
description: "{vol_desc}"
author: "Suresh Bhati"
category: "{vol_info.get('category', 'Canonical Texts')}"
publishedDate: "2026-08-17"
status: "Published"
labels: ["Ayurveda", "Canonical Texts", "Suresh Bhati", "{vol_info.get('category', 'Research')}"]
isCanonicalText: true
---

> **Clinical Executive Summary (Volume Overview)**: {vol_desc} Formatted for modern global E-E-A-T research reference.

## Volume Chapter Directory

"""
    chapter_meta = []
    for idx, sec in enumerate(chapter_list, start=1):
        first_line = sec.split('\n')[0]
        topic = clean_heading_text(first_line)
        ch_title = f"{topic}: {vol_title.split(':')[0]} Chapter {idx}".replace('"', "'").replace('\n', ' ')
        ch_slug = f"{vol_slug}-ch{idx}"
        ch_desc = f"Detailed classical discussion on {topic} within {vol_title.split(':')[0]}.".replace('"', "'").replace('\n', ' ')
        chapter_meta.append({
            "num": idx,
            "title": ch_title,
            "slug": ch_slug,
            "topic": topic,
            "desc": ch_desc,
            "raw_sec": sec
        })
        hub_frontmatter += f"### {idx}. [{ch_title}](/articles/{ch_slug})\n**Overview**: {ch_desc}\n\n"

    hub_body = "\n\n---\n\n## Volume Background & Preface\n\n"
    for intro in intro_sections:
        cleaned = clean_scraped_boilerplate(intro)
        if cleaned:
            hub_body += cleaned + "\n\n"
            
    hub_filepath = os.path.join('content', 'canonical_texts', f"{vol_slug}.md")
    with open(hub_filepath, 'w', encoding='utf-8') as f:
        f.write(hub_frontmatter + hub_body)
    print(f"    [✓] Created Volume Hub Page: {hub_filepath}")
    
    # -------------------------------------------------------------
    # 2. CREATE DEDICATED CHAPTER PAGES
    # -------------------------------------------------------------
    total_chs = len(chapter_meta)
    
    for idx, ch in enumerate(chapter_meta):
        ch_title = ch["title"].replace('"', "'").replace('\n', ' ')
        ch_slug = ch["slug"]
        ch_topic = ch["topic"]
        ch_desc = ch["desc"].replace('"', "'").replace('\n', ' ')
        
        prev_ch = chapter_meta[idx-1] if idx > 0 else None
        next_ch = chapter_meta[idx+1] if idx < total_chs - 1 else None
        
        cleaned_sec = clean_scraped_boilerplate(ch["raw_sec"])
        formatted_sec = convert_to_h3_subheadings(cleaned_sec)
        
        nav_md = "\n\n---\n\n<div className=\"flex justify-between items-center my-6 p-4 bg-emerald-950/20 rounded-xl border border-emerald-500/20\">\n"
        if prev_ch:
            nav_md += f"  <a href=\"/articles/{prev_ch['slug']}\" className=\"text-emerald-400 hover:underline flex items-center font-medium\">← {prev_ch['title']}</a>\n"
        else:
            nav_md += f"  <a href=\"/articles/{vol_slug}\" className=\"text-emerald-400 hover:underline font-medium\">← Volume Index</a>\n"
            
        nav_md += f"  <a href=\"/articles/{vol_slug}\" className=\"text-slate-400 hover:text-emerald-400 text-sm font-medium\">Volume Index</a>\n"
        
        if next_ch:
            nav_md += f"  <a href=\"/articles/{next_ch['slug']}\" className=\"text-emerald-400 hover:underline flex items-center font-medium\">{next_ch['title']} →</a>\n"
        else:
            nav_md += f"  <a href=\"/articles/{vol_slug}\" className=\"text-emerald-400 hover:underline font-medium\">Volume Index →</a>\n"
        nav_md += "</div>\n\n"

        faq_md, schema_script = build_faq_and_schema(ch_title, ch_desc, ch_slug)
        
        ch_frontmatter = f"""---
title: "{ch_title}"
description: "{ch_desc}"
author: "Suresh Bhati"
category: "{vol_info.get('category', 'Canonical Texts')}"
publishedDate: "2026-08-17"
status: "Published"
labels: ["Ayurveda", "Canonical Texts", "{vol_info.get('category', 'Research')}", "Chapter {ch['num']}"]
isCanonicalText: true
---

> **Clinical Executive Summary (E-E-A-T Overview)**: {ch_desc} Formatted with classical Sanskrit attributions and modern international clinical commentary by Suresh Bhati.

{formatted_sec}

{nav_md}

{faq_md}

{schema_script}
"""
        ch_filepath = os.path.join('content', 'canonical_texts', f"{ch_slug}.md")
        with open(ch_filepath, 'w', encoding='utf-8') as f:
            f.write(ch_frontmatter.strip())
            
    # Purge old monolithic file to avoid duplicates
    if os.path.exists(filepath) and filepath != hub_filepath:
        os.remove(filepath)
        print(f"    [✔] Removed monolithic legacy source file: {filename}")

def main():
    parser = argparse.ArgumentParser(description="AyurShakti Comprehensive Canonical Library Modernization Engine")
    parser.add_argument("--file", help="Specific canonical markdown file to process")
    args = parser.parse_args()
    
    if args.file:
        files = [args.file]
    else:
        files = sorted(glob.glob('content/canonical_texts/*_by_*.md') + glob.glob('content/canonical_texts/*_sanskrit.md'))
        
    print(f"Starting Canonical Modernization across {len(files)} monolithic text volume(s)...")
    for f in files:
        process_file(f)
        
    print("\n[✔] ALL Canonical Text Modernization completed successfully!")

if __name__ == "__main__":
    main()
