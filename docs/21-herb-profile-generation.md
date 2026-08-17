# Herb Profile Generation System — AyurShakti.shop

## Overview
Automated pipeline to generate structured herb profiles from existing classical texts, research papers, and glossary content. Implements Triphala/Dashmool exclusion rule (formula components not listed as ingredients).

## Architecture

### Data Flow
```
Source Content (458 MD files)
    ↓
build_herb_synonyms.py → data/herb_synonyms.json (42 herbs, 137 Sanskrit names, 2 formulas)
    ↓
extract_herbs_v2.py → data/herb_index.json (42 profiles with classical refs, formula flags)
    ↓
generate_herb_profile.py → content/herbs_draft/ (32 drafts, 10 skipped Published)
    ↓
validate_herb_profiles.py → data/validation_report.json (16/16 gate)
```

### Key Files
| File | Purpose |
|------|---------|
| `scripts/build_herb_synonyms.py` | Ground truth mapping from 10 existing + 32 additional herbs |
| `scripts/extract_herbs_v2.py` | Scans 458 files, builds index with formula detection |
| `scripts/generate_herb_profile.py` | Template engine with conditional sections, idempotency |
| `scripts/validate_herb_profiles.py` | 16/16 quality gate checker |

## Combination Formula Handling

### Exclusion Rule (Implemented)
- **Triphala**: amalaki, haritaki, bibhitaki → NOT listed as ingredients in other profiles
- **Dashmool**: bilva, agnimantha, shyonaka, patala, gambhari, brihati, kantakari, gokshura, shalaparni, prishniparni → NOT listed as ingredients
- Formula pages list components; component pages show "Part of [Formula]" badge

### Formula Pages Generated
- `triphala.md` — Classical Formulations category, lists 3 components
- `dashmool.md` — Classical Formulations category, lists 10 components

## Template Structure (9 Sections + Frontmatter)

### Frontmatter
```yaml
title: "Herb Name (Botanical Name)"
category: "Herb Profiles" | "Classical Formulations"
date: "YYYY-MM-DD"
status: "Draft" | "Published"
description: "SEO description with botanical name, category, key features"
labels: ["Herb Profiles", "Sanskrit Name", "Category Tag"]
```

### Sections (Conditional - Only Render If Data Exists)
1. **🌿 Botanical & Multilingual Nomenclature** — Table with botanical, family, Sanskrit, Hindi, English, regional names
2. **🔥 Ayurvedic Energy Profile (Taseer & Dravyaguna)** — Rasa, Guna, Virya, Vipaka, Dosha Karma
3. **🧪 Phytochemical & Nutritional Composition** — Key compounds, alkaloids, minerals
4. **💡 Primary Clinical Use Cases** — Numbered list with mechanisms
5. **💊 Classical Formulations & Dosage** — Filtered (excludes formula components)
6. **📜 Classical References** — Samhita chapters, Nighantu verses
7. **🔬 Modern Research Summary** — Research paper references
8. **🔗 Related Botanical Profiles & Formulations** — Cross-links + formula relationships

### Mandatory Elements (16/16 Gate)
- Medical disclaimer (always rendered)
- No featured images required (user preference)
- TL;DR, FAQ, FAQPage schema — **to be added in next phase**

## Idempotency
- Skips generation if `status: "Published"` in existing frontmatter
- 10 existing profiles preserved (ashwagandha, shatavari, giloy, brahmi, tulsi, turmeric, amalaki, haritaki, bibhitaki, triphala)

## Validation (16/16 Quality Gate)

| Check | Current Pass Rate |
|-------|-------------------|
| Human Touch / No Banned / Labels / Keyword | 100% |
| Medical Disclaimer | 76% |
| Internal Links | 33% |
| H2/H3 Structure | 24% |
| TL;DR / FAQ / FAQPage / Image / PubMed / Word Count | 0% |

**Next Phase**: Add TL;DR, FAQ×5, FAQPage JSON-LD, PubMed citations, internal linking engine

## Scripts Reference

### build_herb_synonyms.py
Creates `data/herb_synonyms.json` with:
- 42 herbs × botanical, family, Sanskrit/Hindi/English/Tamil/Telugu/Arabic/Chinese names
- 2 combination formulas (Triphala, Dashmool) with components
- Reverse lookup: component → formula

### extract_herbs_v2.py
Scans 458 content files across 8 directories:
- samhitas/, canonical_texts/, research/, essays_and_studies/, other_works/, herbs/, herb_profiles/, pet-health/
- Matches 137 Sanskrit names from glossary (21,499 terms)
- Outputs `data/herb_index.json` with classical refs, formula flags, existing profile data

### generate_herb_profile.py
- Reads `herb_index.json`, applies template with conditional sections
- Idempotency: skips `status: "Published"` files
- Formula filtering: removes Triphala/Dashmool components from ingredient lists
- Outputs to `content/herbs_draft/`

### validate_herb_profiles.py
16/16 quality gate checker, outputs `data/validation_report.json`

## Current Status (as of 2026-08-17)

| Metric | Value |
|--------|-------|
| Herbs in synonyms | 42 |
| Profiles in index | 42 |
| Published profiles | 42 |
| Formula components flagged | 6 |
| Classical refs coverage | 40/42 |

## Next Phase Tasks

1. **Template Overhaul**: Add TL;DR, FAQ×5, FAQPage JSON-LD, PubMed citations, medical disclaimer (always), 5+ H2s
2. **Data Enrichment**: rasa/guna/virya/vipaka/dosha_karma, clinical uses, phytochemicals, PubMed PMIDs
3. **Re-generation**: All drafts pass 14/16 (plagiarism + Bing sitemap project-level)
4. **Internal Linking Engine**: Min 3 links/profile (same dosha, condition, family)
5. **Dynamic Navbar**: Replace hardcoded herbLinks with `getHerbDocs()`
6. **Sitemap Generation**: Add herb URLs to sitemap

## Commands

```bash
# Full pipeline
python3 scripts/build_herb_synonyms.py
python3 scripts/extract_herbs_v2.py
python3 scripts/generate_herb_profile.py
python3 scripts/validate_herb_profiles.py

# Single herb regeneration
python3 -c "
from scripts.generate_herb_profile import generate_herb_profile
import json
with open('data/herb_index.json') as f: idx = json.load(f)
generate_herb_profile('arjuna', {**idx['arjuna'], 'slug': 'arjuna'})
"
```
