#!/usr/bin/env python3
"""
scripts/modernize_canonical_library.py
AyurShakti Canonical Text Library Modernization Engine.

Converts multi-chapter monolithic canonical text files into:
1. A Volume Index Hub Page (Master Overview & Chapter Directory)
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

# English Title Mapping for Known Volumes & Chapters
ENGLISH_VOLUME_TITLES = {
    "sushruta_samhita_volume_5_kalpasthana": {
        "volume_title": "Ayurvedic Toxicology and Agada Tantra: Sushruta Samhita Kalpasthana Complete Guide",
        "volume_slug": "ayurvedic-toxicology-and-agada-tantra-sushruta-samhita-kalpasthana",
        "description": "Comprehensive classical Ayurvedic guide to toxicology (Kalpasthana), emergency snakebite antidotes, plant & mineral toxins, rabies management, and sonic detoxification.",
        "chapters": {
            1: {
                "title": "Ayurvedic Food Safety and Poison Detection: Sushruta Samhita Kalpasthana Chapter 1",
                "slug": "ayurvedic-food-safety-and-poison-detection-sushruta-samhita-kalpasthana-ch1",
                "topic": "Royal food protection, detection of poisoned drinks, food safety protocols, and immediate resuscitation methods."
            },
            2: {
                "title": "Plant and Mineral Toxicology Guide: Sushruta Samhita Kalpasthana Chapter 2",
                "slug": "plant-and-mineral-toxicology-guide-sushruta-samhita-kalpasthana-ch2",
                "topic": "Classification of immobile (Sthavara) vegetable and mineral poisons, botanical toxins, and systemic antidote formulations."
            },
            3: {
                "title": "Animal Venom Classification and Air Purification: Sushruta Samhita Kalpasthana Chapter 3",
                "slug": "animal-venom-classification-and-air-purification-sushruta-samhita-kalpasthana-ch3",
                "topic": "Classification of animal (Jangama) toxins, venomous bites, and environmental air/water decontamination techniques."
            },
            4: {
                "title": "Venomous Snakes and Bite Symptoms: Sushruta Samhita Kalpasthana Chapter 4",
                "slug": "venomous-snakes-and-bite-symptoms-sushruta-samhita-kalpasthana-ch4",
                "topic": "Taxonomy of venomous serpents (Hooded, Spotted, Striped), physiological bite stages, and clinical prognosis."
            },
            5: {
                "title": "Emergency Snakebite Antidotes and Protocols: Sushruta Samhita Kalpasthana Chapter 5",
                "slug": "emergency-snakebite-antidotes-and-protocols-sushruta-samhita-kalpasthana-ch5",
                "topic": "Classical anti-venomous Agadas, emergency tourniquet & suction protocols, and resuscitation formulations (Ajeya Ghrita)."
            },
            6: {
                "title": "Ayurvedic Management of Rabies and Hydrophobia: Sushruta Samhita Kalpasthana Chapter 6",
                "slug": "ayurvedic-management-of-rabies-and-hydrophobia-sushruta-samhita-kalpasthana-ch6",
                "topic": "Rodent venom, rabid animal bites (Alarka Visha), clinical symptoms of hydrophobia, and cauterization therapies."
            },
            7: {
                "title": "Sonic Detoxification Therapy and Master Antidotes: Sushruta Samhita Kalpasthana Chapter 7",
                "slug": "sonic-detoxification-therapy-and-master-antidotes-sushruta-samhita-kalpasthana-ch7",
                "topic": "Therapeutic anti-venomous sound drums (Dundubhi Svaniya), Kshara-agada, Kalyanaka Ghrita, and Mahasugandhi Agada."
            },
            8: {
                "title": "Medical Management of Insect and Spider Venom: Sushruta Samhita Kalpasthana Chapter 8",
                "slug": "medical-management-of-insect-and-spider-venom-sushruta-samhita-kalpasthana-ch8",
                "topic": "Insects, scorpions, and venomous spider (Luta) bites, staging of necrotic tissue lesions, and specific antidote pastes."
            }
        }
    }
}

def clean_scraped_boilerplate(text: str) -> str:
    """Purge 5-line scraped paragraphs, word counts, and legacy header noise."""
    if not text:
        return ""
    
    # Remove scraped metadata lines
    text = re.sub(r'^\s*\*\*Author\s*/\s*Source:\*\*\s*by\s*.*$', '', text, flags=re.M | re.I)
    text = re.sub(r'^\s*\*\*Total\s+Chapters/Sections:\*\*\s*\d+$', '', text, flags=re.M | re.I)
    text = re.sub(r'Total\s+Chapters/Sections:\s*\d+', '', text, flags=re.I)
    text = re.sub(r'by\s+[A-Za-z\s.]+\|\s*\d{4}\s*\|\s*[\d,]+\s*words', '', text, flags=re.I)
    
    # Remove repetitive volume intro paragraph block
    text = re.sub(r'Sushruta Samhita, Volume \d+:.*?\n', '', text, flags=re.I)
    text = re.sub(r'This current book, the Kalpa-sthana.*?various other subjects\.', '', text, flags=re.S | re.I)
    text = re.sub(r'The Sushruta Samhita is the most representative work.*?medicine\.', '', text, flags=re.S | re.I)
    text = re.sub(r'Susruta-samhita is recognized as\.\.\.', '', text, flags=re.I)
    text = re.sub(r'This page relates [‘\'"].*?[’\'"] found in the study on diseases.*?for study\.', '', text, flags=re.S | re.I)
    
    # Clean whitespace
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()

def convert_to_h3_subheadings(text: str) -> str:
    """Convert unformatted recipe & symptom headers like 'Ajeya-Ghrita:—' into '### Ajeya-Ghrita' for TOC."""
    lines = text.split('\n')
    new_lines = []
    
    for line in lines:
        # Match pattern like 'Ajeya-Ghrita:—' or 'Symptoms of bite:—' or 'Insects of Vataja Temperament:—'
        m = re.match(r'^\s*([A-Z0-9][a-zA-Z0-9\s\,\-\(\)\/]+):\s*[\—\-–]\s*$', line)
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
            "q": f"What are the main medical topics covered in {chapter_title}?",
            "a": f"This chapter focuses on {topic_desc}, providing detailed classical Ayurvedic protocols, symptom staging, and therapeutic interventions."
        },
        {
            "q": "Who is the primary classical authority for these Ayurvedic medical teachings?",
            "a": "These classical medical discourses originate from Acharya Sushruta and Sage Dhanvantari in the Sushruta Samhita, edited and formatted for modern clinical E-E-A-T reference by Suresh Bhati."
        },
        {
            "q": "How are the formulations in this chapter applied in clinical practice?",
            "a": "The classical formulations (Agadas, Ghritas, and plasters) described are administered externally as pastes or internally as decoctions under expert Ayurvedic supervision according to patient Dosha constitution."
        },
        {
            "q": "Are emergency toxicological measures detailed in this text?",
            "a": "Yes, Sushruta Samhita provides immediate emergency resuscitation protocols, tourniquet application, blood purification, and specific antidotes for environmental and biological toxins."
        },
        {
            "q": "Where can I find the complete index of Sushruta Samhita Kalpasthana chapters?",
            "a": "The complete index and navigation for all chapters of Kalpasthana are accessible on the AyurShakti Canonical Texts directory."
        }
    ]
    
    # Build Markdown FAQ
    faq_md = "\n\n---\n\n## Frequently Asked Questions (FAQ)\n\n"
    for item in qas:
        faq_md += f"### {item['q']}\n{item['a']}\n\n"
        
    # Build JSON-LD Schema
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
    print(f"\n[+] Processing canonical file: {filepath}")
    filename_base = os.path.basename(filepath).replace('.md', '')
    
    with open(filepath, 'r', encoding='utf-8') as f:
        raw_content = f.read()

    # Determine volume key
    vol_key = None
    for k in ENGLISH_VOLUME_TITLES:
        if k in filename_base:
            vol_key = k
            break
            
    vol_config = ENGLISH_VOLUME_TITLES.get(vol_key)
    
    # Split raw content by H2 headings
    sections = re.split(r'\n(?=##\s*)', raw_content)
    
    # Group sections into Volume Intro vs Chapters
    intro_sections = []
    chapter_map = {}
    
    for sec in sections:
        sec_clean = sec.strip()
        if not sec_clean:
            continue
            
        first_line = sec_clean.split('\n')[0]
        
        # Check if it's a chapter
        ch_match = re.search(r'Chapter\s+([IVXLCDM\d]+)', first_line, re.I)
        if ch_match:
            ch_str = ch_match.group(1).upper()
            # Convert roman numeral to integer
            roman_dict = {'I': 1, 'II': 2, 'III': 3, 'IV': 4, 'V': 5, 'VI': 6, 'VII': 7, 'VIII': 8, 'IX': 9, 'X': 10}
            ch_num = roman_dict.get(ch_str) if ch_str in roman_dict else int(ch_str) if ch_str.isdigit() else 1
            chapter_map[ch_num] = sec_clean
        elif any(x in first_line.lower() for x in ['introduction', 'preface', 'title page', 'acknowledg']):
            intro_sections.append(sec_clean)
            
    sorted_ch_nums = sorted(chapter_map.keys())
    print(f"    Found {len(sorted_ch_nums)} chapters: {sorted_ch_nums}")
    
    # -------------------------------------------------------------
    # 1. CREATE VOLUME MASTER HUB PAGE
    # -------------------------------------------------------------
    vol_title = vol_config["volume_title"] if vol_config else f"Ayurvedic Guide: {filename_base.replace('_', ' ').title()}"
    vol_slug = vol_config["volume_slug"] if vol_config else filename_base.replace('_', '-')
    vol_desc = vol_config["description"] if vol_config else "Classical Ayurvedic research monograph and canonical text guide."
    
    hub_frontmatter = f"""---
title: "{vol_title}"
description: "{vol_desc}"
author: "Suresh Bhati"
category: "Canonical Texts"
publishedDate: "2026-08-17"
status: "Published"
labels: ["Ayurveda", "Sushruta Samhita", "Kalpasthana", "Toxicology", "Agada Tantra"]
isCanonicalText: true
---

> **Clinical Executive Summary (Volume Overview)**: {vol_desc} Formatted for modern global E-E-A-T research reference.

## Volume Chapter Directory

"""
    for ch_num in sorted_ch_nums:
        if vol_config and ch_num in vol_config["chapters"]:
            ch_info = vol_config["chapters"][ch_num]
            ch_t = ch_info["title"]
            ch_s = ch_info["slug"]
            ch_d = ch_info["topic"]
        else:
            ch_t = f"Chapter {ch_num}"
            ch_s = f"{vol_slug}-ch{ch_num}"
            ch_d = "Classical Ayurvedic medical chapter."
            
        hub_frontmatter += f"### {ch_num}. [{ch_t}](/articles/{ch_s})\n**Overview**: {ch_d}\n\n"

    # Append cleaned introductory sections
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
    total_chs = len(sorted_ch_nums)
    
    for idx, ch_num in enumerate(sorted_ch_nums):
        if vol_config and ch_num in vol_config["chapters"]:
            ch_info = vol_config["chapters"][ch_num]
            ch_title = ch_info["title"]
            ch_slug = ch_info["slug"]
            ch_topic = ch_info["topic"]
        else:
            ch_title = f"Chapter {ch_num}: {filename_base.replace('_', ' ').title()}"
            ch_slug = f"{vol_slug}-ch{ch_num}"
            ch_topic = "Detailed classical Ayurvedic medical chapter."
            
        # Determine Prev and Next chapters
        prev_slug = vol_config["chapters"][sorted_ch_nums[idx-1]]["slug"] if idx > 0 and vol_config else (f"{vol_slug}-ch{sorted_ch_nums[idx-1]}" if idx > 0 else "")
        prev_title = vol_config["chapters"][sorted_ch_nums[idx-1]]["title"] if idx > 0 and vol_config else (f"Chapter {sorted_ch_nums[idx-1]}" if idx > 0 else "")
        
        next_slug = vol_config["chapters"][sorted_ch_nums[idx+1]]["slug"] if idx < total_chs - 1 and vol_config else (f"{vol_slug}-ch{sorted_ch_nums[idx+1]}" if idx < total_chs - 1 else "")
        next_title = vol_config["chapters"][sorted_ch_nums[idx+1]]["title"] if idx < total_chs - 1 and vol_config else (f"Chapter {sorted_ch_nums[idx+1]}" if idx < total_chs - 1 else "")
        
        # Clean section content
        raw_sec = chapter_map[ch_num]
        cleaned_sec = clean_scraped_boilerplate(raw_sec)
        formatted_sec = convert_to_h3_subheadings(cleaned_sec)
        
        # Build Navigation Markdown
        nav_md = "\n\n---\n\n<div className=\"flex justify-between items-center my-6 p-4 bg-emerald-950/20 rounded-xl border border-emerald-500/20\">\n"
        if prev_slug:
            nav_md += f"  <a href=\"/articles/{prev_slug}\" className=\"text-emerald-400 hover:underline flex items-center font-medium\">← {prev_title}</a>\n"
        else:
            nav_md += f"  <a href=\"/articles/{vol_slug}\" className=\"text-emerald-400 hover:underline font-medium\">← Volume Index</a>\n"
            
        nav_md += f"  <a href=\"/articles/{vol_slug}\" className=\"text-slate-400 hover:text-emerald-400 text-sm font-medium\">Volume Index</a>\n"
        
        if next_slug:
            nav_md += f"  <a href=\"/articles/{next_slug}\" className=\"text-emerald-400 hover:underline flex items-center font-medium\">{next_title} →</a>\n"
        else:
            nav_md += f"  <a href=\"/articles/{vol_slug}\" className=\"text-emerald-400 hover:underline font-medium\">Volume Index →</a>\n"
        nav_md += "</div>\n\n"

        # Build FAQ & Schema
        faq_md, schema_script = build_faq_and_schema(ch_title, ch_topic, ch_slug)
        
        # Frontmatter
        ch_frontmatter = f"""---
title: "{ch_title}"
description: "{ch_topic}"
author: "Suresh Bhati"
category: "Canonical Texts"
publishedDate: "2026-08-17"
status: "Published"
labels: ["Ayurveda", "Sushruta Samhita", "Kalpasthana", "Toxicology", "Agada Tantra", "Chapter {ch_num}"]
isCanonicalText: true
---

> **Clinical Executive Summary (E-E-A-T Overview)**: {ch_topic} Formatted with classical Sanskrit attributions and modern international clinical commentary by Suresh Bhati.

{formatted_sec}

{nav_md}

{faq_md}

{schema_script}
"""
        ch_filepath = os.path.join('content', 'canonical_texts', f"{ch_slug}.md")
        with open(ch_filepath, 'w', encoding='utf-8') as f:
            f.write(ch_frontmatter.strip())
            
        print(f"    [✓] Created Chapter Page: {ch_filepath}")

def main():
    parser = argparse.ArgumentParser(description="AyurShakti Canonical Library Modernization Engine")
    parser.add_argument("--file", help="Specific canonical markdown file to process")
    args = parser.parse_args()
    
    if args.file:
        files = [args.file]
    else:
        files = glob.glob('content/canonical_texts/sushruta_samhita_volume_5_kalpasthana*.md')
        
    print(f"Starting Canonical Modernization on {len(files)} file(s)...")
    for f in files:
        process_file(f)
        
    print("\n[✔] Pilot Canonical Modernization completed successfully!")

if __name__ == "__main__":
    main()
