#!/usr/bin/env python3
"""
AyurShakti Legacy Metadata Scrubbing Engine
Author: Suresh Bhati
Description:
  Scrubs scraped web clutter, repetitive metadata, filler bylines, 
  and duplicate paragraphs across all content markdown files.
"""

import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTENT_DIR = ROOT / "content"

def scrub_content_string(text: str) -> str:
    """Scrub raw legacy meta clutter from content body text."""
    # 1. Remove Author / Source: by ...
    text = re.sub(r"^\s*\*\*Author\s*/\s*Source:\*\*\s*by\s*.*$", "", text, flags=re.MULTILINE | re.IGNORECASE)
    
    # 2. Remove Total Chapters/Sections: XX
    text = re.sub(r"^\s*\*\*Total\s+Chapters/Sections:\*\*\s*\d+$", "", text, flags=re.MULTILINE | re.IGNORECASE)
    text = re.sub(r"Total\s+Chapters/Sections:\s*\d+", "", text, flags=re.IGNORECASE)

    # 3. Remove scraped scholar bylines e.g. "by Laxmi Maji | 2021 | 143,541 words"
    text = re.sub(r"^\s*by\s+[A-Za-z\s.]+\|\s*\d{4}\s*\|\s*[\d,]+\s*words\s*$", "", text, flags=re.MULTILINE | re.IGNORECASE)
    text = re.sub(r".*?\|\s*\d{4}\s*\|\s*[\d,]+\s*words.*", "", text, flags=re.IGNORECASE)

    # 4. Remove filler scraped intro sentences e.g. "This page relates ‘...’ found in the study on diseases..."
    text = re.sub(
        r"^\s*This page relates [‘'\"].*?[’'\"] found in the study on diseases and remedies found in the Atharvaveda and Charaka-samhita\..*?taken up for study\.\s*$",
        "",
        text,
        flags=re.MULTILINE | re.DOTALL | re.IGNORECASE
    )
    text = re.sub(
        r"This page relates [‘'\"].*?[’'\"] found in the study on diseases and remedies found in the Atharvaveda and Charaka-samhita\..*?for study\.",
        "",
        text,
        flags=re.IGNORECASE
    )

    # 5. Remove Go directly to: Footnotes
    text = re.sub(r"^\s*Go\s+directly\s+to:\s*\n?\s*Footnotes\.*$", "", text, flags=re.MULTILINE | re.IGNORECASE)
    text = re.sub(r"Go\s+directly\s+to:\s*.*?Footnotes\.*", "", text, flags=re.IGNORECASE)

    # 6. Remove Footnotes and references: \n [back to top]
    text = re.sub(r"^\s*Footnotes\s+and\s+references:\s*\n?\s*\[back to top\]\s*$", "", text, flags=re.MULTILINE | re.IGNORECASE)
    text = re.sub(r"^\s*\[back to top\]\s*$", "", text, flags=re.MULTILINE | re.IGNORECASE)

    # 7. Remove scholar signatures at the end like "(Laxmi Maji)\nResearch Scholar"
    text = re.sub(r"^\s*\([A-Za-z\s.]+\)\s*\n?\s*Research\s+Scholar\s*$", "", text, flags=re.MULTILINE | re.IGNORECASE)

    # 8. Remove standalone book title repetitions above headings (e.g. "Atharvaveda and Charaka Samhita")
    text = re.sub(r"^\s*Atharvaveda and Charaka Samhita\s*$", "", text, flags=re.MULTILINE)

    # 9. Deduplicate consecutive identical paragraphs
    paragraphs = text.split("\n\n")
    cleaned_paragraphs = []
    for p in paragraphs:
        p_strip = p.strip()
        if not p_strip:
            continue
        # If identical to previous paragraph, skip duplicate
        if cleaned_paragraphs and cleaned_paragraphs[-1].strip() == p_strip:
            continue
        cleaned_paragraphs.append(p)

    cleaned_text = "\n\n".join(cleaned_paragraphs)

    # 10. Clean up excessive blank lines
    cleaned_text = re.sub(r"\n{3,}", "\n\n", cleaned_text)
    return cleaned_text.strip()

def process_file(file_path: Path) -> bool:
    """Scrub a single markdown file."""
    try:
        content = file_path.read_text(encoding="utf-8")
        cleaned = scrub_content_string(content)
        if cleaned != content:
            file_path.write_text(cleaned, encoding="utf-8")
            return True
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
    return False

def main():
    print("🧹 Starting Comprehensive Legacy Metadata Scrubbing...")
    modified_count = 0
    total_count = 0

    for md_file in CONTENT_DIR.rglob("*.md"):
        total_count += 1
        if process_file(md_file):
            modified_count += 1

    print(f"✅ Cleaned {modified_count} of {total_count} markdown files.")

if __name__ == "__main__":
    main()
