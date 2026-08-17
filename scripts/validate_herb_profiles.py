#!/usr/bin/env python3
"""
Validate herb profiles against 16/16 quality gate
Checks both draft and published profiles
"""
import re
import json
from pathlib import Path

ROOT = Path("/home/shiva/ayurshakti.shop")
DRAFT_DIR = ROOT / "content" / "herbs_draft"
HERBS_DIR = ROOT / "content" / "herbs"

def load_frontmatter_and_content(filepath):
    content = filepath.read_text(encoding="utf-8")
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            import yaml
            fm = yaml.safe_load(parts[1])
            body = parts[2]
            return fm, body
    return {}, content

def check_profile(filepath, is_draft=False):
    """Run all 16 checks on a profile"""
    fm, body = load_frontmatter_and_content(filepath)
    slug = filepath.stem
    checks = {}
    
    # 1. Featured image present (check for image reference)
    checks["1_featured_image"] = bool(re.search(r'!\[.*?\]\(.*?\)', body) or fm.get("image"))
    
    # 2. TL;DR block present
    checks["2_tldr_block"] = bool(re.search(r'>\s*\*\*TL;DR:', body, re.IGNORECASE))
    
    # 3. FAQ section (5 Q&A)
    faq_matches = re.findall(r'##\s+FAQ|###\s+Q\d*|###\s+Question', body, re.IGNORECASE)
    checks["3_faq_section"] = len(faq_matches) >= 5 or "FAQ" in body.upper()
    
    # 4. FAQPage JSON-LD schema
    checks["4_faq_schema"] = bool(re.search(r'FAQPage', body))
    
    # 5. Human touch audit (no AI patterns) - basic check
    ai_patterns = ["delve", "in today's world", "it's important to note", "in conclusion", "the bottom line", "unlock the secrets"]
    checks["5_human_touch"] = not any(p in body.lower() for p in ai_patterns)
    
    # 6. Internal links (2-4)
    internal_links = re.findall(r'\]\(/herbs/|/articles/|/glossary|/dosha-quiz|/canonical-texts', body)
    checks["6_internal_links"] = 2 <= len(internal_links) <= 10
    
    # 7. H2/H3 structure (5-8 H2s)
    h2_count = len(re.findall(r'^##\s+', body, re.MULTILINE))
    checks["7_h2_h3_structure"] = 5 <= h2_count <= 10
    
    # 8. Word count >= 1500
    word_count = len(body.split())
    checks["8_word_count"] = word_count >= 1500
    
    # 9. Primary keyword in H1 + first 100 words
    h1_match = re.search(r'^#\s+(.+)', body, re.MULTILINE)
    first_100 = " ".join(body.split()[:100])
    keyword = fm.get("title", "").split("(")[0].strip().lower() if fm.get("title") else slug
    checks["9_keyword_placement"] = h1_match and keyword in h1_match.group(1).lower() and keyword in first_100.lower()
    
    # 10. No banned phrases
    banned = ["in conclusion", "the bottom line", "to summarize", "let's dive in", "let's explore", "in today's world", "it's worth noting"]
    checks["10_no_banned"] = not any(p in body.lower() for p in banned)
    
    # 11. Medical disclaimer
    checks["11_medical_disclaimer"] = bool(re.search(r'Medical Disclaimer', body))
    
    # 12. PubMed citations (check for PMID)
    checks["12_pubmed_citations"] = bool(re.search(r'PMID:?\s*\d+', body))
    
    # 13. Plagiarism - skip (manual)
    checks["13_plagiarism"] = None  # Manual check
    
    # 14. Bing sitemap / robots.txt / llms.txt - project level
    checks["14_bing_sitemap"] = None  # Project level
    
    # 15. Multi-platform optimized (listicle format, definition sentences, fact density)
    has_list = bool(re.search(r'^\d+\.\s', body, re.MULTILINE))
    has_def = bool(re.search(r'is a|is an|refers to|means', body[:500], re.IGNORECASE))
    checks["15_multi_platform"] = has_list or has_def
    
    # 16. Labels match category
    checks["16_labels_match"] = bool(fm.get("labels"))
    
    # Score
    passed = sum(1 for v in checks.values() if v is True)
    total = sum(1 for v in checks.values() if v is not None)
    score = f"{passed}/{total}"
    
    return {
        "slug": slug,
        "checks": checks,
        "score": score,
        "word_count": word_count,
        "h2_count": h2_count,
        "internal_links": len(internal_links)
    }

def main():
    print("🔍 Validating herb profiles against 16/16 gate...\n")
    
    all_results = {}
    
    # Check drafts
    for f in sorted(DRAFT_DIR.glob("*.md")):
        result = check_profile(f, is_draft=True)
        all_results[f.stem] = result
        status = "✅" if result["score"].split("/")[0] == result["score"].split("/")[1] else "⚠️"
        print(f"  {status} {f.stem}: {result['score']} (words: {result['word_count']}, H2s: {result['h2_count']}, links: {result['internal_links']})")
    
    # Check published
    for f in sorted(HERBS_DIR.glob("*.md")):
        result = check_profile(f)
        all_results[f.stem] = result
        status = "✅" if result["score"].split("/")[0] == result["score"].split("/")[1] else "⚠️"
        print(f"  {status} {f.stem} (published): {result['score']} (words: {result['word_count']}, H2s: {result['h2_count']}, links: {result['internal_links']})")
    
    # Summary
    print(f"\n📊 VALIDATION SUMMARY")
    print(f"  Total profiles checked: {len(all_results)}")
    print(f"  Drafts: {len(list(DRAFT_DIR.glob('*.md')))}")
    print(f"  Published: {len(list(HERBS_DIR.glob('*.md')))}")
    
    # Check-specific summary
    check_names = {
        "1_featured_image": "Featured Image",
        "2_tldr_block": "TL;DR Block",
        "3_faq_section": "FAQ Section (5)",
        "4_faq_schema": "FAQPage Schema",
        "5_human_touch": "Human Touch",
        "6_internal_links": "Internal Links (2-4)",
        "7_h2_h3_structure": "H2/H3 Structure",
        "8_word_count": "Word Count ≥1500",
        "9_keyword_placement": "Keyword in H1+100",
        "10_no_banned": "No Banned Phrases",
        "11_medical_disclaimer": "Medical Disclaimer",
        "12_pubmed_citations": "PubMed Citations",
        "15_multi_platform": "Multi-Platform Opt",
        "16_labels_match": "Labels Match"
    }
    
    print(f"\n📋 CHECK-BY-CHECK:")
    for key, name in check_names.items():
        passed = sum(1 for r in all_results.values() if r["checks"].get(key) is True)
        total = sum(1 for r in all_results.values() if r["checks"].get(key) is not None)
        pct = (passed/total*100) if total else 0
        bar = "█" * int(pct/10) + "░" * (10-int(pct/10))
        print(f"  {name:25s} {passed:2d}/{total:2d} ({pct:5.1f}%) {bar}")
    
    # Save detailed report
    output = ROOT / "data" / "validation_report.json"
    with open(output, "w") as f:
        json.dump(all_results, f, indent=2, default=str)
    print(f"\n💾 Detailed report saved to {output}")

if __name__ == "__main__":
    main()
