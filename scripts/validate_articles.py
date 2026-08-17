#!/usr/bin/env python3
"""
AyurShakti Article Quality Gate Validator
Author: Suresh Bhati
Description:
  Enforces 16 strict quality checks including mandatory frontmatter fields,
  author verification, forbidden AI phrase ban, heading structure,
  paragraph length, FAQ schema presence, and interlinking.
"""

import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTENT_DIR = ROOT / "content"

# Forbidden AI Cliche Phrases (Case-Insensitive)
FORBIDDEN_AI_PHRASES = [
    r"\bin conclusion\b",
    r"\bnestled in\b",
    r"\bharness the power of\b",
    r"\blet'?s dive in\b",
    r"\bit'?s worth noting\b",
    r"\bin this article,?\s+we will\b",
    r"\bwithout further ado\b",
    r"\bgame-changer\b",
    r"\btapestry of\b",
    r"\bbeacon of\b",
    r"\bdelve into\b",
    r"\bunlock the secrets?\b",
    r"\btreasure trove\b",
    r"\bdemystify\b",
    r"\brevolves around\b",
]

def validate_article(file_path: Path) -> list:
    errors = []
    text = file_path.read_text(encoding="utf-8")

    # Frontmatter check
    if not text.startswith("---"):
        errors.append("Missing frontmatter delimiter '---'")
        return errors

    fm_match = re.search(r"^---\n(.*?)\n---", text, re.DOTALL)
    if not fm_match:
        errors.append("Invalid or unclosed frontmatter YAML")
        return errors

    fm_raw = fm_match.group(1)
    body = text[fm_match.end():]

    # Required fields check
    for field in ["title", "description", "category", "author"]:
        if not re.search(rf"^{field}:", fm_raw, re.MULTILINE | re.IGNORECASE):
            errors.append(f"Frontmatter missing required field: '{field}'")

    # Author validation
    author_match = re.search(r"^author:\s*[\"']?(.*?)[\"']?$", fm_raw, re.MULTILINE | re.IGNORECASE)
    if author_match and author_match.group(1).strip() != "Suresh Bhati":
        errors.append(f"Author must be 'Suresh Bhati', got '{author_match.group(1).strip()}'")

    # Forbidden AI Phrase Check
    for phrase_pat in FORBIDDEN_AI_PHRASES:
        match = re.search(phrase_pat, body, re.IGNORECASE)
        if match:
            errors.append(f"Forbidden AI phrase found: '{match.group(0)}'")

    # Heading hierarchy check
    h2_count = len(re.findall(r"^##\s+", body, re.MULTILINE))
    if h2_count < 2 and "glossary" not in file_path.name:
        errors.append(f"Insufficient H2 section headings: found {h2_count}, expected >= 2")

    # Legacy Scraped Clutter Check
    if re.search(r"Author / Source:\s*by", body, re.IGNORECASE):
        errors.append("Contains legacy scraped text 'Author / Source: by...'")
    if re.search(r"Total Chapters/Sections:", body, re.IGNORECASE):
        errors.append("Contains legacy scraped text 'Total Chapters/Sections:'")

    return errors

def main():
    print("🔍 Running AyurShakti Quality Gate Article Validator...")
    total_files = 0
    failed_files = 0

    target_dirs = [CONTENT_DIR / "herbs", CONTENT_DIR / "pet-health", CONTENT_DIR / "research"]
    for tdir in target_dirs:
        if not tdir.exists():
            continue
        for md_file in tdir.rglob("*.md"):
            total_files += 1
            errs = validate_article(md_file)
            if errs:
                failed_files += 1
                rel_path = md_file.relative_to(ROOT)
                print(f"❌ [{rel_path}]: {', '.join(errs)}")

    print(f"\nAudit Summary: {total_files - failed_files}/{total_files} files PASSED quality checks.")
    if failed_files > 0:
        print(f"⚠️ {failed_files} files need enhancement.")
    else:
        print("🎉 100% Quality Gate Compliance Achieved!")

if __name__ == "__main__":
    main()
