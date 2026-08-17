#!/usr/bin/env python3
"""
AyurShakti AI Phrase Auto-Fixer
Author: Suresh Bhati
Description: Replaces forbidden AI phrases with clean, scholarly Ayurvedic prose.
"""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTENT_DIR = ROOT / "content"

REPLACEMENTS = [
    (r"\bIn conclusion\b", "In summary"),
    (r"\bin conclusion\b", "in summary"),
    (r"\brevolves around\b", "focuses on"),
    (r"\bRevolves around\b", "Focuses on"),
    (r"\bdelve into\b", "examine"),
    (r"\bDelve into\b", "Examine"),
    (r"\btreasure trove\b", "comprehensive archive"),
    (r"\bTreasure trove\b", "Comprehensive archive"),
    (r"\bharness the power of\b", "utilize the therapeutic efficacy of"),
    (r"\bunlock the secrets?\b", "discover the principles"),
    (r"\bit'?s worth noting\b", "notably"),
    (r"\bwithout further ado\b", "proceeding to the analysis"),
    (r"\bgame-changer\b", "significant development"),
]

def fix_file(file_path: Path) -> bool:
    content = file_path.read_text(encoding="utf-8")
    original = content

    for pat, repl in REPLACEMENTS:
        content = re.sub(pat, repl, content)

    if content != original:
        file_path.write_text(content, encoding="utf-8")
        return True
    return False

def main():
    print("🔧 Fixing remaining AI phrases...")
    fixed = 0
    for md in CONTENT_DIR.rglob("*.md"):
        if fix_file(md):
            fixed += 1
    print(f"✅ Auto-fixed {fixed} files.")

if __name__ == "__main__":
    main()
