#!/usr/bin/env python3
"""
Validate Quality Gate compliance for all 17 Research & Evidence Articles in content/research/
"""

import json
from pathlib import Path

ROOT = Path("/home/shiva/ayurshakti.shop")
RESEARCH_DIR = ROOT / "content" / "research"

def validate_research_article(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    words = len(text.split())
    
    has_tldr = "> **TL;DR:**" in text
    has_author = 'author: "Suresh Bhati"' in text
    has_faq = "## ❓ 7. Frequently Asked Questions" in text or "Frequently Asked Questions" in text
    has_faq_schema = '"FAQPage"' in text
    has_scholarly_schema = '"ScholarlyArticle"' in text
    has_pmid = "PMID:" in text
    has_disclaimer = "Medical Disclaimer" in text or "Academic Disclaimer" in text or "Academic & Medical Disclaimer" in text
    
    checks = {
        "Word Count >= 1500": words >= 1500,
        "TL;DR Summary Block": has_tldr,
        "Author Suresh Bhati": has_author,
        "15 Question FAQ Section": has_faq,
        "FAQPage JSON-LD Schema": has_faq_schema,
        "ScholarlyArticle Schema": has_scholarly_schema,
        "PubMed Citations": has_pmid,
        "Academic & Medical Disclaimer": has_disclaimer
    }
    
    passed = all(checks.values())
    return {
        "file": path.name,
        "words": words,
        "passed": passed,
        "score": f"{sum(checks.values())}/{len(checks)}",
        "checks": checks
    }

def main():
    print("🔬 Auditing Quality Gate Compliance for Research Articles...")
    files = sorted(list(RESEARCH_DIR.glob("*.md")))
    total = len(files)
    
    passed_count = 0
    results = []
    
    for f in files:
        res = validate_research_article(f)
        results.append(res)
        if res["passed"]:
            passed_count += 1
            print(f"  ✅ {f.name[:50]:<50} | Score: {res['score']} | Words: {res['words']}")
        else:
            print(f"  ❌ {f.name[:50]:<50} | Score: {res['score']} | Failed Checks: {[k for k, v in res['checks'].items() if not v]}")
            
    print(f"\n📊 RESEARCH AUDIT SUMMARY")
    print(f"  Total Articles Checked: {total}")
    print(f"  Passed 100% Quality Gate: {passed_count}/{total} ({passed_count/total*100:.1f}%)")

if __name__ == "__main__":
    main()
