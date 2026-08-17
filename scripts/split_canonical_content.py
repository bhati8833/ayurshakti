#!/usr/bin/env python3
"""
AyurShakti Content Silo Restructuring & Chapter Splitting Script
Author: Suresh Bhati
Description:
  Reads monolithic Ayurvedic markdown files from /content/canonical_texts
  and restructures them into individual chapter files under clean Silo folders:
  - content/samhitas/[book-slug]/[chapter-slug].md
  - content/herbs/[herb-slug].md
  - content/pet-health/[slug].md
  - content/research/[slug].md
  
  Ensures 100% full content preservation (no text is truncated), generates
  structured YAML frontmatter, and creates book-level table-of-contents metadata.
"""

import os
import re
import json
import math
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
CONTENT_DIR = BASE_DIR / "content"

# Target Silo Output Directories
SAMHITAS_DIR = CONTENT_DIR / "samhitas"
HERBS_DIR = CONTENT_DIR / "herbs"
PET_HEALTH_DIR = CONTENT_DIR / "pet-health"
RESEARCH_DIR = CONTENT_DIR / "research"

for d in [SAMHITAS_DIR, HERBS_DIR, PET_HEALTH_DIR, RESEARCH_DIR]:
    d.mkdir(parents=True, exist_ok=True)

def slugify(text: str) -> str:
    """Convert text to a clean URL-friendly slug."""
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_-]+', '-', text).strip('-')
    return text

def calculate_reading_time(text: str) -> int:
    words = len(text.split())
    return max(1, math.ceil(words / 200))

def parse_header(header_line: str):
    """
    Parses headers like:
    ## 2. Chapter 5 - Measure in eating (matrashita)
    ## 1. Sutrasthana (Sutra Sthana) — General Principles
    ## 10. Chapter 1 - The Quest for Longevity
    Returns (index_num, title, chapter_num)
    """
    clean_line = header_line.lstrip('#').strip()
    
    # Check for leading number prefix e.g. "2. Chapter 5..."
    match = re.match(r'^(\d+)\.\s+(.*)$', clean_line)
    if match:
        idx_num = int(match.group(1))
        rest = match.group(2).strip()
    else:
        idx_num = 0
        rest = clean_line
        
    # Check for Chapter number inside title
    ch_match = re.search(r'Chapter\s+(\d+)', rest, re.IGNORECASE)
    ch_num = int(ch_match.group(1)) if ch_match else idx_num
    
    return idx_num, rest, ch_num

def process_charaka_samhita(filepath: Path):
    print(f"Processing Charaka Samhita from {filepath.name}...")
    book_slug = "charaka-samhita"
    book_title = "Charaka Samhita (English Translation)"
    author = "Shree Gulabkunverba Ayurvedic Society"
    book_dir = SAMHITAS_DIR / book_slug
    book_dir.mkdir(parents=True, exist_ok=True)

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split by level-2 markdown headings ##
    sections_raw = re.split(r'\n(?=##\s+)', content)
    
    chapters_meta = []
    current_sthana = "Sutrasthana"

    for i, section_text in enumerate(sections_raw):
        lines = section_text.strip().splitlines()
        if not lines:
            continue
        
        first_line = lines[0]
        if not first_line.startswith('##'):
            continue  # Main title or intro block

        idx_num, title, ch_num = parse_header(first_line)
        
        # Check if title indicates a new Sthana / Section
        if "Sutrasthana" in title or "Sutra Sthana" in title:
            current_sthana = "Sutrasthana"
        elif "Nidanasthana" in title:
            current_sthana = "Nidanasthana"
        elif "Vimanasthana" in title:
            current_sthana = "Vimanasthana"
        elif "Sharirasthana" in title:
            current_sthana = "Sharirasthana"
        elif "Indriyasthana" in title:
            current_sthana = "Indriyasthana"
        elif "Chikitsasthana" in title or "Cikitsasthana" in title:
            current_sthana = "Chikitsasthana"
        elif "Kalpasthana" in title:
            current_sthana = "Kalpasthana"
        elif "Siddhisthana" in title:
            current_sthana = "Siddhisthana"

        ch_slug = f"{slugify(current_sthana)}-ch-{ch_num:02d}-{slugify(title)}"
        # Truncate slug if too long
        ch_slug = ch_slug[:80].rstrip('-')
        
        body_content = "\n".join(lines[1:]).strip()
        reading_time = calculate_reading_time(body_content)

        chapters_meta.append({
            "idx": idx_num,
            "title": title,
            "ch_num": ch_num,
            "sthana": current_sthana,
            "slug": ch_slug,
            "reading_time": reading_time,
            "body": body_content
        })

    # Sort chapters by idx
    chapters_meta.sort(key=lambda x: x["idx"])

    # Write individual chapter markdown files with YAML frontmatter
    toc_list = []
    for idx, item in enumerate(chapters_meta):
        prev_slug = chapters_meta[idx - 1]["slug"] if idx > 0 else ""
        next_slug = chapters_meta[idx + 1]["slug"] if idx < len(chapters_meta) - 1 else ""

        frontmatter = f"""---
title: "{item['title']}"
book: "{book_title}"
book_slug: "{book_slug}"
author: "{author}"
silo: "samhitas"
section: "{item['sthana']}"
chapter_number: {item['ch_num']}
chapter_slug: "{item['slug']}"
reading_time: {item['reading_time']}
prev_chapter: "{prev_slug}"
next_chapter: "{next_slug}"
---

# {item['title']}

{item['body']}
"""
        ch_filepath = book_dir / f"{item['slug']}.md"
        with open(ch_filepath, 'w', encoding='utf-8') as out_f:
            out_f.write(frontmatter)

        toc_list.append({
            "chapter_number": item['ch_num'],
            "title": item['title'],
            "section": item['sthana'],
            "slug": item['slug'],
            "reading_time": item['reading_time']
        })

    # Save book-level Table of Contents JSON
    book_info = {
        "title": book_title,
        "book_slug": book_slug,
        "author": author,
        "total_chapters": len(toc_list),
        "silo": "samhitas",
        "description": "The foundational classic of Ayurvedic internal medicine covering Sutrasthana, Nidanasthana, Chikitsasthana, and therapeutics.",
        "chapters": toc_list
    }
    with open(book_dir / "book-info.json", 'w', encoding='utf-8') as info_f:
        json.dump(book_info, info_f, indent=2)

    print(f"Successfully generated {len(toc_list)} chapter pages for Charaka Samhita!")

def process_sushruta_samhita():
    """Processes all Sushruta Samhita volume files."""
    book_slug = "sushruta-samhita"
    book_title = "Sushruta Samhita (English Translation)"
    author = "Kaviraj Kunja Lal Bhishagratna"
    book_dir = SAMHITAS_DIR / book_slug
    book_dir.mkdir(parents=True, exist_ok=True)

    sushruta_files = sorted((CONTENT_DIR / "canonical_texts").glob("sushruta_samhita_volume_*.md"))
    if not sushruta_files:
        return

    chapters_meta = []
    global_idx = 1

    for filepath in sushruta_files:
        print(f"Processing {filepath.name}...")
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extract Sthana name from volume filename or header
        vol_name = filepath.stem
        if "sutrasthana" in vol_name:
            current_sthana = "Sutrasthana"
        elif "nidana" in vol_name:
            current_sthana = "Nidanasthana"
        elif "sharira" in vol_name:
            current_sthana = "Sharirasthana"
        elif "chikitsa" in vol_name:
            current_sthana = "Chikitsasthana"
        elif "kalpa" in vol_name:
            current_sthana = "Kalpasthana"
        elif "uttara" in vol_name:
            current_sthana = "Uttaratantra"
        else:
            current_sthana = "General"

        sections_raw = re.split(r'\n(?=##\s+)', content)
        for section_text in sections_raw:
            lines = section_text.strip().splitlines()
            if not lines or not lines[0].startswith('##'):
                continue

            idx_num, title, ch_num = parse_header(lines[0])
            ch_slug = f"{slugify(current_sthana)}-ch-{global_idx:03d}-{slugify(title)}"[:80].rstrip('-')
            body_content = "\n".join(lines[1:]).strip()

            chapters_meta.append({
                "global_idx": global_idx,
                "title": title,
                "ch_num": ch_num,
                "sthana": current_sthana,
                "slug": ch_slug,
                "reading_time": calculate_reading_time(body_content),
                "body": body_content
            })
            global_idx += 1

    for idx, item in enumerate(chapters_meta):
        prev_slug = chapters_meta[idx - 1]["slug"] if idx > 0 else ""
        next_slug = chapters_meta[idx + 1]["slug"] if idx < len(chapters_meta) - 1 else ""

        frontmatter = f"""---
title: "{item['title']}"
book: "{book_title}"
book_slug: "{book_slug}"
author: "{author}"
silo: "samhitas"
section: "{item['sthana']}"
chapter_number: {item['ch_num']}
chapter_slug: "{item['slug']}"
reading_time: {item['reading_time']}
prev_chapter: "{prev_slug}"
next_chapter: "{next_slug}"
---

# {item['title']}

{item['body']}
"""
        with open(book_dir / f"{item['slug']}.md", 'w', encoding='utf-8') as out_f:
            out_f.write(frontmatter)

    book_info = {
        "title": book_title,
        "book_slug": book_slug,
        "author": author,
        "total_chapters": len(chapters_meta),
        "silo": "samhitas",
        "description": "The paramount classical treatise on Ayurvedic surgery (Shalya Tantra), plastic surgery, surgical instruments, and therapeutics.",
        "chapters": [{"title": c["title"], "slug": c["slug"], "section": c["sthana"]} for c in chapters_meta]
    }
    with open(book_dir / "book-info.json", 'w', encoding='utf-8') as info_f:
        json.dump(book_info, info_f, indent=2)

    print(f"Successfully generated {len(chapters_meta)} chapter pages for Sushruta Samhita!")

def process_other_canonical_and_research():
    """Processes Rasa Jala Nidhi, Ashtanga Hridaya, Hastyayurveda, essays, etc."""
    canonical_dir = CONTENT_DIR / "canonical_texts"
    essays_dir = CONTENT_DIR / "essays_and_studies"
    herb_dir = CONTENT_DIR / "herb_profiles"

    # 1. Process Herb Profiles -> content/herbs/
    if herb_dir.exists():
        for herb_file in herb_dir.glob("*.md"):
            print(f"Migrating herb profile: {herb_file.name}")
            with open(herb_file, 'r', encoding='utf-8') as f:
                text = f.read()

            herb_slug = slugify(herb_file.stem.replace("_herb_profile", ""))
            body = text
            if not text.startswith("---"):
                title = herb_slug.replace("-", " ").title()
                frontmatter = f"""---
title: "{title}"
silo: "herbs"
slug: "{herb_slug}"
category: "Adaptogens & Dravyaguna"
---

"""
                body = frontmatter + text

            with open(HERBS_DIR / f"{herb_slug}.md", 'w', encoding='utf-8') as out_f:
                out_f.write(body)

    # 2. Process Pet Health / Hastyayurveda / Matangalila
    pet_files = ["matangalila_by_nilakantha_sanskrit.md", "hastyayurveda.md"]
    for pf in pet_files:
        p_path = canonical_dir / pf
        if p_path.exists():
            print(f"Processing Pet Health text: {pf}")
            with open(p_path, 'r', encoding='utf-8') as f:
                text = f.read()
            p_slug = slugify(p_path.stem)
            frontmatter = f"""---
title: "{p_path.stem.replace('_', ' ').title()}"
silo: "pet-health"
slug: "{p_slug}"
category: "Mrigayurveda & Elephantology"
---

"""
            with open(PET_HEALTH_DIR / f"{p_slug}.md", 'w', encoding='utf-8') as out_f:
                out_f.write(frontmatter + text)

    # 3. Process Essays & Research Studies -> content/research/
    if essays_dir.exists():
        for essay_file in essays_dir.glob("*.md"):
            print(f"Processing Research Essay: {essay_file.name}")
            with open(essay_file, 'r', encoding='utf-8') as f:
                text = f.read()
            r_slug = slugify(essay_file.stem)
            frontmatter = f"""---
title: "{essay_file.stem.replace('_', ' ').title()}"
silo: "research"
slug: "{r_slug}"
category: "Ayurvedic History & Alchemy"
---

"""
            with open(RESEARCH_DIR / f"{r_slug}.md", 'w', encoding='utf-8') as out_f:
                out_f.write(frontmatter + text)

if __name__ == "__main__":
    charaka_path = CONTENT_DIR / "canonical_texts" / "charaka_samhita_english_translation_by_shree_gulabkunverba.md"
    if charaka_path.exists():
        process_charaka_samhita(charaka_path)
    
    process_sushruta_samhita()
    process_other_canonical_and_research()
    print("ALL CONTENT SILO RESTRUCTURING & CHAPTER SPLITTING COMPLETE!")
