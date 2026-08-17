#!/usr/bin/env python3
"""
refine_all_silos.py - Multi-Silo Programmatic Content Sanitizer for AyurShakti.shop
-----------------------------------------------------------------------------------
Sanitizes markdown content across Canonical Texts, Samhitas, and Research silos.
Follows strict hardware-safe batching (50 files per chunk with micro-pauses).
"""

import os
import re
import sys
import time

BATCH_SIZE = 50
MICRO_PAUSE = 0.2  # 200ms CPU cooling pause per batch

# Directories to process
CANONICAL_DIR = "content/canonical_texts"
SAMHITAS_DIR = "content/samhitas"
RESEARCH_DIR = "content/research"


def sanitize_canonical_text(content: str) -> str:
    """Refines Canonical Text markdown formatting, removes legacy clutter and broken list breaks."""

    # 1. Strip legacy repeated introductory blocks
    # e.g., "Agriculture and Animal husbandry in the Puranas\n\nThis page relates..."
    content = re.sub(
        r"(?i)Agriculture and Animal husbandry in the Puranas\s*\n\nThis page relates [^\n]+\n\n",
        "",
        content,
    )
    content = re.sub(r"-\s*Sub-Contents:\s*\(\+\s*/\s*-\)\s*\n?", "", content)

    # 2. Strip GL_NOTE legacy raw markers like GL_NOTE:413781:}
    content = re.sub(r"GL_NOTE:\d+:?\}?", "", content)

    # 3. Clean heading section numbers: e.g. "## 45. Chapter 3 - " -> "## Chapter 3 - "
    content = re.sub(r"^(#{2,4})\s*\d+[\.\s]+", r"\1 ", content, flags=re.MULTILINE)

    # 4. Fix single-word vertical list spacing
    # Converts sequences of single-word lines separated by empty lines into clean inline text
    # e.g., "wheat,\n\nsesame,\n\nblack gram," -> "wheat, sesame, black gram"
    def fix_separated_list(match):
        raw_block = match.group(0)
        items = [line.strip() for line in raw_block.split("\n\n") if line.strip()]
        if len(items) >= 3 and all(len(item.split()) <= 4 for item in items):
            return "\n\n" + ", ".join(items) + "\n\n"
        return raw_block

    # Pattern targeting 3+ consecutive single-word lines separated by double newlines
    content = re.sub(
        r"(\n[A-Za-zāīūṛḷēōṁḥṅñṭḍṇśṣ0-9\s,\-\'\"\(\)]+\n){3,}",
        fix_separated_list,
        content,
    )

    # 5. Format raw footnote references e.g. "[20]:\n\nvratārhaṇaṃ..." into shloka/footnote blockquote
    def format_footnote(match):
        num = match.group(1)
        text = match.group(2).strip()
        if re.search(r"[āīūṛḷēōṁḥṅñṭḍṇśṣ/]", text):  # Contains IAST/Sanskrit shloka
            return f'\n\n<blockquote className="ayur-shloka">\n<strong>[{num}]</strong> {text}\n</blockquote>\n\n'
        return f'\n\n<div className="footnote-card"><strong>[{num}]</strong> {text}</div>\n\n'

    content = re.sub(
        r"\n\[(\d+)\]:\s*\n+([^\n]+(?:\n[^\n]+)*?)(?=\n\n|\n\[\d+\]:|\n---|\Z)",
        format_footnote,
        content,
    )

    # 6. Ensure clean spacing around horizontal rules
    content = re.sub(r"\n{3,}---", "\n\n---", content)
    content = re.sub(r"---\n{3,}", "---\n\n", content)

    return content


def sanitize_samhita_text(content: str) -> str:
    """Refines Samhita chapter markdown, removes title duplications and formats shlokas."""

    # 1. Format Sanskrit shlokas into ayur-shloka callout box if not already wrapped
    # Matches lines with IAST transliteration or Devanagari ending with // or |
    def wrap_shloka(match):
        block = match.group(0).strip()
        if "ayur-shloka" in block:
            return block
        return f'\n\n<blockquote className="ayur-shloka">\n{block}\n</blockquote>\n\n'

    content = re.sub(
        r"(\n(?:[^\n]+[āīūṛḷēōṁḥṅñṭḍṇśṣ|\/]{2,}[^\n]*\n?)+)",
        wrap_shloka,
        content,
    )

    # 2. De-duplicate repeated section headings if identical
    lines = content.split("\n")
    cleaned_lines = []
    prev_h = None
    for line in lines:
        if line.startswith("#"):
            if line == prev_h:
                continue
            prev_h = line
        cleaned_lines.append(line)

    return "\n".join(cleaned_lines)


def sanitize_research_text(content: str) -> str:
    """Refines Research monograph markdown, strips PDF scan page artifacts."""

    # 1. Strip raw Roman numeral page artifacts on isolated lines (e.g., "ii", "iii", "iv")
    content = re.sub(
        r"\n\s*(?:[ivxlcdm]+|\d{1,3})\s*\n(?=\n)", "\n", content, flags=re.IGNORECASE
    )

    # 2. Clean heading section numbers
    content = re.sub(r"^(#{2,4})\s*\d+[\.\s]+", r"\1 ", content, flags=re.MULTILINE)

    return content


def process_directory(dir_path: str, mode: str):
    """Processes a directory of markdown files in 50-file micro-batches with pauses."""
    if not os.path.exists(dir_path):
        print(f"Directory {dir_path} not found. Skipping.")
        return

    md_files = []
    for root, _, files in os.walk(dir_path):
        for f in files:
            if f.endswith(".md") and f != "index.md":
                md_files.append(os.path.join(root, f))

    total = len(md_files)
    print(f"[{mode.upper()}] Starting processing for {total} files in {dir_path}...")

    processed = 0
    for i in range(0, total, BATCH_SIZE):
        batch = md_files[i : i + BATCH_SIZE]
        for file_path in batch:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    raw_text = f.read()

                if mode == "canonical":
                    cleaned_text = sanitize_canonical_text(raw_text)
                elif mode == "samhita":
                    cleaned_text = sanitize_samhita_text(raw_text)
                elif mode == "research":
                    cleaned_text = sanitize_research_text(raw_text)
                else:
                    cleaned_text = raw_text

                if cleaned_text != raw_text:
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(cleaned_text)

                processed += 1
            except Exception as e:
                print(f"Error processing {file_path}: {e}")

        # Hardware safety micro-pause to release CPU & RAM threshold
        print(
            f"  Batch {i//BATCH_SIZE + 1}/{(total + BATCH_SIZE - 1)//BATCH_SIZE} complete ({processed}/{total} files). Micro-pause {MICRO_PAUSE}s..."
        )
        time.sleep(MICRO_PAUSE)

    print(f"[{mode.upper()}] Successfully processed {processed}/{total} files.\n")


def main():
    start_time = time.time()
    print("=================================================================")
    print("AyurShakti Multi-Silo Content Sanitizer (Hardware-Safe Execution)")
    print("=================================================================\n")

    process_directory(CANONICAL_DIR, "canonical")
    process_directory(SAMHITAS_DIR, "samhita")
    process_directory(RESEARCH_DIR, "research")

    elapsed = time.time() - start_time
    print(
        f"All silos successfully sanitized in {elapsed:.2f} seconds with zero system overload!"
    )


if __name__ == "__main__":
    main()
