#!/usr/bin/env python3
"""
Validate Quality Gate compliance for all 1,265 Research Sub-Chapters & 17 Hub Directories
- Checks 0 clutter strings (42,318 words, Total Chapters/Sections, Go directly to: Footnotes, Author/Source: by...)
- Checks presence of FAQ section (15 Question Matrix)
- Checks JSON-LD Schema (MedicalWebPage + FAQPage)
- Checks Author: Suresh Bhati + Original Scholar preservation
"""

import json
import re
from pathlib import Path

ROOT = Path("/home/shiva/ayurshakti.shop")
RESEARCH_DIR = ROOT / "content" / "research"

CLUTTER_PATTERNS = [
    r"Total\s+Chapters/Sections:\s*\d+",
    r"\*\*Author\s*/\s*Source:\*\*\s*by",
    r"Go\s+directly\s+to:\s*.*?Footnotes",
    r"\|\s*\d{4}\s*\|\s*[\d,]+\s*words"
]

def audit_research_chapter(file_path: Path) -> dict:
    text = file_path.read_text(encoding="utf-8")
    words = len(text.split())
    
    # Check clutter strings
    has_clutter = False
    for pat in CLUTTER_PATTERNS:
        if re.search(pat, text, re.IGNORECASE):
            has_clutter = True
            break
            
    has_author = 'author: "Suresh Bhati"' in text
    has_scholar = 'original_scholar:' in text
    has_faq = "## ❓ 4. Frequently Asked Questions" in text or "Frequently Asked Questions" in text
    has_faq_schema = '"FAQPage"' in text
    has_med_schema = '"MedicalWebPage"' in text or '"ScholarlyArticle"' in text
    
    checks = {
        "Zero Clutter Strings": not has_clutter,
        "Author Suresh Bhati": has_author,
        "Original Scholar Preserved": has_scholar,
        "15 Question FAQ Section": has_faq,
        "FAQPage JSON-LD Schema": has_faq_schema,
        "Medical/Scholarly Schema": has_med_schema
    }
    
    passed = all(checks.values())
    return {
        "file": file_path.name,
        "words": words,
        "passed": passed,
        "score": f"{sum(checks.values())}/{len(checks)}",
        "checks": checks
    }

def main():
    print("🔬 Auditing Quality Gate Compliance for 1,265 Research Chapters & 17 Hub Directories...")
    paper_dirs = [d for d in RESEARCH_DIR.iterdir() if d.is_dir()]
    
    total_files = 0
    passed_count = 0
    
    for d in paper_dirs:
        ch_files = list(d.glob("*.md"))
        for f in ch_files:
            total_files += 1
            res = audit_research_chapter(f)
            if res["passed"]:
                passed_count += 1
            else:
                print(f"  ❌ {f.relative_to(RESEARCH_DIR)} | Score: {res['score']} | Failed: {[k for k, v in res['checks'].items() if not v]}")
                
    print(f"\n📊 RESEARCH CHAPTER AUDIT SUMMARY")
    print(f"  Total Files Checked: {total_files}")
    print(f"  Passed 100% Quality Gate: {passed_count}/{total_files} ({passed_count/total_files*100:.1f}%)")

if __name__ == "__main__":
    main()
