# Charaka Samhita — SEO Refinement Checkpoint

**Last updated:** 2026-08-18 (session end — pushed + deployed)

## Next Session: Resume at Chapter 18

1. Read `content/samhitas/charaka-samhita/sutrasthana-ch-18-the-three-kinds-of-edema-shotha.md` (already reviewed; NOT yet refined — raw OCR content still in place).
2. Write premium refinement (pattern below), then continue ch-19, ch-20...

## Source of Truth for All 150 URLs

- **`content/samhitas/charaka-samhita/book-info.json`** — canonical 150-chapter list with new SEO slugs (source of truth; updated by rename + enrichment).
- `data/tracking/charaka_audit_tracking.json` — OLD file_path values (pre-rename). Do NOT trust its paths; use book-info.json slugs. Regenerate later if needed.
- Old Blogger-style URLs (`/2026/07/slug.html` or `/search?q=`) were **never indexed** → no redirects needed (user decision).

## Completed This Cycle (refined → premium, seo_manual:true, 5 FAQ, OCR clean)

| # | File slug | Words ~ | Status |
|---|-----------|---------|--------|
| 1 | `sutrasthana-general-principles` (hub) | — | Premium hub (earlier) |
| 3 | `sutrasthana-ch-03-...-aragvadha` | — | Premium + PubMed (earlier) |
| 5 | `sutrasthana-ch-05-...-matrashita` | — | Premium (earlier) |
| 6 | `sutrasthana-ch-06-...-tasyashita` | — | Premium (earlier) |
| 7 | `sutrasthana-ch-07-...-vega...` | — | Premium (earlier) |
| 8 | `sutrasthana-ch-08-...-indriya-upakrama` | — | Premium (earlier) |
| 9 | `sutrasthana-ch-09-...-cikitsa-chatuspada` | — | Premium (earlier) |
| 10 | `sutrasthana-ch-10-...-in-therapeusis-cikitsa` | 2,900 | Premium |
| 11 | `sutrasthana-ch-11-...-eshana-of-man` | 5,384 | Premium |
| 12 | `sutrasthana-ch-12-...-influences-of-vata` | 2,833 | Premium |
| 13 | `sutrasthana-ch-13-...-oleation-therapy-sneha` | 3,981 | Premium |
| 14 | `sutrasthana-ch-14-...-sudation-therapy-sveda` | 3,798 | Premium |
| 15 | `sutrasthana-ch-15-...-armamentarium-upakalpa-of-the-physician` | 3,493 | Premium |
| 16 | `sutrasthana-ch-16-...-fully-equipped-physician-cikitsa-prabhrita` | ~2,600 | Premium |
| 17 | `sutrasthana-ch-17-...-diseases-of-the-head-shiroroga-and-of-the-heart-hridroga` | ~5,400 | Premium |

## Remaining Refinement Queue (Sutrasthana)

- ch-18 (shotha) → ch-19 (udara) → ch-20 (mahagadha) → ch-21 (ashta-unindita) → ch-22 (langhana-brmhana) → ch-23 (santarpana) → ch-24 (vidhishonita) → ch-25 (yajjah-purushiya) → ch-26 (atisaukshmya) → ch-27 (annapana-vidhi) → ch-28 (vividha-ashita) → ch-29 (dasha-pranayatana) → ch-30 (arthe-dasha-mahamula) → ch-30b (definition of Ayurveda) → Nidanasthana 1-10 → Vimanasthana 1-9 → Sharirasthana 1-9 → Indriyasthana 1-13 → Chikitsasthana 1a-30 → Kalpasthana 1-17 → Siddhisthana 1-13 (stubs).
- 7 section stubs (`{section}-general-principles`) renamed; only sutrasthana hub is premium so far — others need hub refinement later.

## Premium Refinement Pattern (all refined chapters)

- TL;DR — Executive Clinical Summary, Introduction, thematic H2s (ALL verses preserved, OCR fixed), 5 FAQ under `## Frequently Asked Questions`, `## About This Rendering` with 3 internal links (prev, next, section hub), `seo_manual: "true"`, unique keyword-rich description, author **Suresh Bhati**, no banned phrases ("In conclusion", "delve", "unlock", "className", "blockquote"), single H1, no images/PubMed for pure classical renderings (only ch-3 has PubMed PMID 42227486).

## Deployment (DONE this session)

- `npm run build` verified OK → `git push origin master` → GitHub Actions → Firebase Hosting → Cloudflare purge via API (zone id + token in `secrets/`).

## Commands

```bash
# Re-run enrichment after content changes
python3 -B scripts/charaka-seo-enrich.py
# Full herb pipeline (only when herb content changed)
python3 scripts/build_herb_synonyms.py && python3 scripts/extract_herbs_v2.py && python3 scripts/generate_herb_profile.py && python3 scripts/validate_herb_profiles.py
# QA check (word count / H2 / FAQ / links / banned)
# tsc typecheck
npx tsc --noEmit
# Build + deploy
npm run build && git add . && git commit -m "..." && git push origin master
```

## Notes / Gotchas

- Frontmatter chain keys: `prev_chapter` / `next_chapter` (not `prev`/`next`).
- `scripts/rename_charaka_slugs.py` LSP `ModuleSpec | None` warnings are harmless (importlib load of hyphenated filename).
- `src/app/samhitas/[bookSlug]/[chapterSlug]/page.tsx` LSP diagnostics (`cleanChapterTitle`, `date`) are stale — both exist in `src/lib/markdown.ts`; tsc passes.
- Section counts: Sutrasthana 42, Chikitsasthana 37, Kalpasthana 17, Indriyasthana 13, Siddhisthana 13, Nidanasthana 10, Vimanasthana 9, Sharirasthana 9 (total 150).
- Ch-2 (apamarga) absent from OCR set — chain skips it (ch-1 → ch-3).
- Phase C pending: approval-queue cleanup, Giloy article, scheduler.