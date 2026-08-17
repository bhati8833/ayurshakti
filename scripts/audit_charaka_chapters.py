#!/usr/bin/env python3
"""
Comprehensive Audit & Tracking Script for Charaka Samhita Chapters
Reads all chapters in content/samhitas/charaka-samhita/ and generates detailed JSON tracking data
covering unused text debris, heading structure recommendations, rich content gaps, SEO tags/keywords/meta, and schema requirements.
"""

import os
import json
import re

CONTENT_DIR = "/home/shiva/ayurshakti.shop/content/samhitas/charaka-samhita"
BOOK_INFO_PATH = os.path.join(CONTENT_DIR, "book-info.json")
TRACKING_OUTPUT_PATH = "/home/shiva/ayurshakti.shop/data/tracking/charaka_audit_tracking.json"
PROJECT_TASKS_PATH = "/home/shiva/ayurshakti.shop/data/tracking/project-tasks.json"

LEGACY_DEBRIS_PATTERNS = [
    (r'Total\s+Chapters/Sections:\s*\d+', "Total Chapters/Sections count marker"),
    (r'Go\s+directly\s+to:\s*Footnotes', "Legacy navigation link 'Go directly to: Footnotes'"),
    (r'Footnotes\s+and\s+references:\s*\[back to top\]', "Legacy link 'Footnotes and references: [back to top]'"),
    (r'\[back to top\]', "Legacy link '[back to top]'"),
    (r'Atharvaveda and Charaka Samhita', "Legacy redundant header 'Atharvaveda and Charaka Samhita'"),
    (r'Research Scholar', "Legacy scholar metadata line"),
    (r'This page relates.*study on diseases', "Legacy research paper disclaimer line"),
    (r'by\s+.*\|\s*\d{4}\s*\|\s*[\d,]+\s*words', "Legacy word count byline")
]

def audit_chapter(file_path, meta):
    with open(file_path, "r", encoding="utf-8") as f:
        raw_text = f.read()

    # Frontmatter extraction
    fm_match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", raw_text, re.DOTALL)
    fm_raw = fm_match.group(1) if fm_match else ""
    body = fm_match.group(2) if fm_match else raw_text

    # 1. Unused Text Debris Check
    debris_found = []
    for pattern, label in LEGACY_DEBRIS_PATTERNS:
        if re.search(pattern, raw_text, re.IGNORECASE):
            debris_found.append(label)

    # 2. Heading Structure Analysis
    h1_count = len(re.findall(r"^#\s+(.+)$", body, re.MULTILINE))
    h2_matches = re.findall(r"^##\s+(.+)$", body, re.MULTILINE)
    h3_matches = re.findall(r"^###\s+(.+)$", body, re.MULTILINE)
    h4_matches = re.findall(r"^####\s+(.+)$", body, re.MULTILINE)

    bold_as_headings = len(re.findall(r"^\*\*[^*]+\*\*\s*$", body, re.MULTILINE))

    heading_issues = []
    if h1_count > 1:
        heading_issues.append(f"Multiple H1 tags found ({h1_count}). Should have exactly 1 main title H1.")
    elif h1_count == 0:
        heading_issues.append("Missing H1 title in markdown body.")

    if len(h2_matches) < 2:
        heading_issues.append(f"Low H2 section count ({len(h2_matches)} H2s). Needs clear sub-sections (Overview, Sanskrit Verses, Therapeutics, Clinical Applications).")

    if bold_as_headings > 3:
        heading_issues.append(f"Found {bold_as_headings} pseudo-headings formatted as bold text instead of proper Markdown H2/H3/H4 tags.")

    # 3. Rich Content Analysis
    shloka_boxes = len(re.findall(r'<div class="ayur-shloka">', body)) + len(re.findall(r'```sanskrit', body))
    shloka_verses = len(re.findall(r'[\u0900-\u097F]', body))  # Devanagari script presence

    has_clinical_summary = "glass-summary" in body or "Clinical Executive Summary" in body
    has_takeaways = "takeaways-card" in body or "Key Takeaways" in body
    has_dosage_box = "dosage-box" in body or "Therapeutic Dosage" in body

    rich_content_gaps = []
    if shloka_verses > 0 and shloka_boxes == 0:
        rich_content_gaps.append("Devanagari Sanskrit text detected but NOT styled inside a premium '.ayur-shloka' callout box.")
    elif shloka_verses == 0:
        rich_content_gaps.append("Missing original Devanagari Sanskrit Shloka verses for classical authenticity.")

    if not has_clinical_summary:
        rich_content_gaps.append("Missing '.glass-summary' Clinical Executive Summary block at the top of the chapter.")

    if not has_takeaways:
        rich_content_gaps.append("Missing '.takeaways-card' for quick practitioner reference.")

    # 4. SEO & Schema Analysis
    chapter_title = meta.get("title", "Charaka Samhita Chapter")
    section = meta.get("section", "Sutrasthana")
    chap_num = meta.get("chapter_number", 1)

    suggested_meta_description = f"Read unabridged Charaka Samhita {section} Chapter {chap_num} ({chapter_title}). Classical Sanskrit verses, English translation, and Ayurvedic therapeutic principles by Suresh Bhati."
    if len(suggested_meta_description) > 160:
        suggested_meta_description = suggested_meta_description[:157] + "..."

    keywords = [
        "charaka samhita",
        f"charaka samhita {section.lower()}",
        f"charaka samhita chapter {chap_num}",
        chapter_title.lower(),
        "ayurvedic canonical text",
        "sanskrit medical manuscript",
        "suresh bhati ayurveda"
    ]

    tags = ["Charaka Samhita", section, "Canonical Text", "Ayurvedic Therapeutics", "Sanskrit Manuscripts"]

    recommended_heading_hierarchy = [
        f"H1: {chapter_title} — Charaka Samhita {section} Chapter {chap_num}",
        f"H2: 1. Classical Executive Summary & Scope",
        f"H2: 2. Authenticated Sanskrit Shloka & Verse Analysis",
        f"H2: 3. Core Ayurvedic Principles & Pathophysiology",
        f"H2: 4. Therapeutic Protocols & Botanical Formulations",
        f"H2: 5. Clinical Practitioner Takeaways & Dosha Guidelines",
        f"H2: 6. Canonical Citations & Cross-References"
    ]

    return {
        "chapter_slug": meta.get("slug", os.path.basename(file_path).replace('.md', '')),
        "title": chapter_title,
        "section": section,
        "chapter_number": chap_num,
        "reading_time_min": meta.get("reading_time", 5),
        "file_path": file_path,
        "word_count": len(body.split()),
        "unused_text_debris": debris_found,
        "heading_issues": heading_issues,
        "recommended_heading_hierarchy": recommended_heading_hierarchy,
        "rich_content_gaps": rich_content_gaps,
        "seo": {
            "title_tag": f"{chapter_title} | Charaka Samhita {section} | AyurShakti",
            "meta_description": suggested_meta_description,
            "target_keywords": keywords,
            "tags": tags,
            "schema": {
                "@context": "https://schema.org",
                "@type": "MedicalWebPage",
                "isPartOf": {
                    "@type": "Book",
                    "name": "Charaka Samhita",
                    "author": "Maharshi Charaka / Shree Gulabkunverba Society"
                },
                "author": "Suresh Bhati"
            }
        },
        "status": "Needs Quality Enhancement" if (debris_found or heading_issues or rich_content_gaps) else "Compliant"
    }

def main():
    print("Loading Charaka Samhita book info...")
    with open(BOOK_INFO_PATH, "r", encoding="utf-8") as f:
        book_info = json.load(f)

    chapters_meta = book_info.get("chapters", [])
    print(f"Total chapters cataloged in book-info.json: {len(chapters_meta)}")

    audit_results = []

    # Map by slug
    files_in_dir = [f for f in os.listdir(CONTENT_DIR) if f.endswith(".md") and f != "index.md"]
    print(f"Total markdown chapter files in directory: {len(files_in_dir)}")

    for idx, item in enumerate(chapters_meta):
        slug = item.get("slug")
        file_name = f"{slug}.md"
        file_path = os.path.join(CONTENT_DIR, file_name)

        if not os.path.exists(file_path):
            # Try fuzzy match
            matching = [f for f in files_in_dir if slug in f or f.startswith(f"{item.get('section', '').lower()}-ch-{item.get('chapter_number', 0):02d}")]
            if matching:
                file_path = os.path.join(CONTENT_DIR, matching[0])
            else:
                continue

        res = audit_chapter(file_path, item)
        res["id"] = f"CHARAKA-CH-{idx+1:03d}"
        audit_results.append(res)

    print(f"Successfully audited {len(audit_results)} chapters.")

    # Save detailed audit JSON
    os.makedirs(os.path.dirname(TRACKING_OUTPUT_PATH), exist_ok=True)
    with open(TRACKING_OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump({
            "book": "Charaka Samhita",
            "total_chapters_audited": len(audit_results),
            "generated_at": "2026-08-17T21:35:00Z",
            "author_attribution": "Suresh Bhati",
            "chapters": audit_results
        }, f, indent=2)
    print(f"Saved full audit output to {TRACKING_OUTPUT_PATH}")

    # Now update project-tasks.json - REMOVE ALL OLD TASKS as requested by user
    sections = set(c["section"] for c in audit_results)
    new_tasks = []

    # Task for Global Heading & CSS Fixes
    new_tasks.append({
        "id": "TASK-CHARAKA-000",
        "title": "Define Base Global CSS Headings (H1, H2, H3, H4) & Interlink Double-Box Fix",
        "description": "Define base HTML heading styles (H1, H2, H3, H4) with Playfair font and proper line-height in globals.css. Fix interlinker regex so nested tooltip cards & double border boxes never render.",
        "status": "Todo",
        "assignee": "AI",
        "priority": "Critical",
        "tags": ["css", "headings", "interlinking", "bug-fix"],
        "dependencies": []
    })

    for sec in sorted(list(sections)):
        sec_chapters = [c for c in audit_results if c["section"] == sec]
        new_tasks.append({
            "id": f"TASK-CHARAKA-{sec.upper()}",
            "title": f"Refine & Rich-Enhance Charaka Samhita {sec} ({len(sec_chapters)} Chapters)",
            "description": f"Sanitize legacy debris, rewrite headings to H1-H4 hierarchy, format Sanskrit Shlokas into .ayur-shloka boxes, add .glass-summary executive summaries, and verify metadata/schema for all {len(sec_chapters)} chapters in {sec}.",
            "status": "Todo",
            "assignee": "AI",
            "priority": "High",
            "tags": ["charaka-samhita", sec.lower(), "content-enhancement", "seo"],
            "dependencies": ["TASK-CHARAKA-000"]
        })

    with open(PROJECT_TASKS_PATH, "w", encoding="utf-8") as f:
        json.dump({"tasks": new_tasks}, f, indent=2)

    print(f"Updated {PROJECT_TASKS_PATH} with {len(new_tasks)} clean Charaka Samhita tracking tasks (old tracking removed).")

if __name__ == "__main__":
    main()
