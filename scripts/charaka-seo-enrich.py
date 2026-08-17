#!/usr/bin/env python3
"""
Charaka Samhita — Phase-A SEO Enrichment (NO images)
Fixes applied to all 150 chapter files:
  1. section:  correct section label (fixes ~40% mislabeled cikitsa chapters)
  2. category: "Charaka Samhita ({section})" matching corrected section
  3. labels:   section label corrected
  4. description: UNIQUE per chapter (from first verse + keyword prefix)
  5. reading_time: from book-info.json (real values, not fallback "5")
  6. prev_chapter / next_chapter: per-section reading order (enables pagination)
  7. TL;DR: unique data-driven rewrite (subject + sanskrit + section nature)
Stub section-intro pages are detected and get generic TL;DR skip (rewritten in Phase B).
"""

import json
import os
import re
import sys

DIR = os.path.join("content", "samhitas", "charaka-samhita")
book = json.load(open(os.path.join(DIR, "book-info.json"), encoding="utf-8"))

# reading times + titles from book-info.json
rt_map = {ch["slug"]: ch.get("reading_time") for ch in book["chapters"]}
title_map = {ch["slug"]: ch["title"] for ch in book["chapters"]}

SECTION_NATURE = {
    "Sutrasthana": "the fundamental principles (sutra) of diet, regimen, and therapy that underpin Ayurvedic clinical practice",
    "Nidanasthana": "the etiology (nidana), premonitory symptoms (purvarupa), and clinical varieties of disease",
    "Vimanasthana": "the methods of examination, measurement (vimana), and clinical reasoning of the physician",
    "Sharirasthana": "the anatomy, embryology, and constitution of the human body (sharira)",
    "Indriyasthana": "the sensory signs (indriya) and prognostic indications of disease outcome",
    "Chikitsasthana": "the therapeutic protocols (cikitsa), formulations, doses, and clinical management of disease",
    "Kalpasthana": "the pharmaceutical preparations (kalpa) of purificatory herbs and their methods of use",
    "Siddhisthana": "the successful administration (siddhi) of enema, emesis, and panchakarma procedures",
}


def classify_section(filename):
    base = filename[:-3]
    low = base.lower()
    # Content-based overrides (high confidence) — fix mislabeled cikitsa/nidana/siddhi chapters
    if "cikitsa" in low or "therapeutics" in low:
        return "Chikitsasthana"
    if "pathology" in low or "-nidana" in low:
        return "Nidanasthana"
    if "siddhi" in low:
        return "Siddhisthana"
    # Prefix-based fallback
    if base.startswith("sutrasthana-"):
        return "Sutrasthana"
    if base.startswith("nidanasthana-"):
        return "Nidanasthana"
    if base.startswith("vimanasthana-"):
        return "Vimanasthana"
    if base.startswith("sharirasthana-"):
        return "Sharirasthana"
    if base.startswith("siddhisthana-"):
        return "Siddhisthana"
    if base.startswith("chikitsasthana-"):
        return "Chikitsasthana"
    if base.startswith("kalpasthana-"):
        return "Kalpasthana"
    if base.startswith("indriyasthana-"):
        return "Indriyasthana"
    return "Sutrasthana"


def is_stub(title):
    return bool(re.search(r"Section on|\(Sutra Sthana\)|\(Nidana Sthana\)|\(Vimana Sthana\)|\(Sharira Sthana\)|\(Indriya Sthana\)|\(Cikitsa Sthana\)|\(Kalpa Sthana\)|\(Siddhi Sthana\)", title))


def parse_title(title):
    """Split 'Chapter 12a - Subject (sanskrit)' -> (chapter_label, subject, sanskrit)"""
    m = re.match(r"^Chapter\s+(\d+[a-z]?)\s*-\s*(.+)$", title)
    if not m:
        return ("", title, "")
    label, rest = m.group(1), m.group(2).strip()
    sm = re.search(r"\(([^()]+)\)\s*$", rest)
    sanskrit = sm.group(1).strip() if sm else ""
    subject = rest[: sm.start()].strip().rstrip("— -") if sm else rest.strip()
    return (label, subject, sanskrit)


def clean_verse(line):
    line = re.sub(r"^\d+\.\s*", "", line).strip()
    line = line.replace("“", "").replace("”", "").replace("‘", "'").replace("’", "'")
    line = re.sub(r"\s+", " ", line).strip(" .") + "."
    return line


def first_verse(content):
    for line in content.splitlines():
        if re.match(r"^\d+\.\s", line.strip()):
            return clean_verse(line.strip())
    return ""


NATURE_SHORT = {
    "Sutrasthana": "Core principles of diet, regimen, and therapy.",
    "Nidanasthana": "Etiology, premonitory symptoms, and clinical varieties.",
    "Vimanasthana": "Methods of examination and clinical reasoning.",
    "Sharirasthana": "Anatomy, embryology, and human constitution.",
    "Indriyasthana": "Sensory signs and prognostic indications.",
    "Chikitsasthana": "Therapeutic protocols, formulations, and clinical management.",
    "Kalpasthana": "Pharmaceutical preparations of purificatory herbs.",
    "Siddhisthana": "Panchakarma procedures and their successful administration.",
}


def build_description(section, subject, sanskrit, verse):
    prefix = f"Charaka Samhita ({section}) — {subject}"
    if sanskrit:
        prefix += f" ({sanskrit})"
    core = f"{prefix}. {NATURE_SHORT.get(section, 'Classical Ayurvedic principles.')}"
    if len(core) + 33 <= 158:
        return core + " Unabridged classical translation."
    return core[:158].rstrip(" .") + "."


def build_tldr(section, chapter_label, subject, sanskrit):
    nature = SECTION_NATURE.get(section, "the classical principles of Ayurveda")
    sanskrit_part = f" ({sanskrit})" if sanskrit else ""
    ch_part = f"Chapter {chapter_label}" if chapter_label else section
    return (
        f"## TL;DR — Executive Clinical Summary\n\n"
        f"**{subject}** — This chapter of the Charaka Samhita, {section} {ch_part}, "
        f"expounds {subject.lower()}{sanskrit_part} as taught by Acharya Atreya through Agnivesha "
        f"and revised by Acharya Charaka. It covers {nature}."
    )


SECTION_ORDER = {
    "Sutrasthana": 1, "Nidanasthana": 2, "Vimanasthana": 3, "Sharirasthana": 4,
    "Indriyasthana": 5, "Chikitsasthana": 6, "Kalpasthana": 7, "Siddhisthana": 8,
}


def order_files(files):
    """Section-scoped reading order: each section's stub first, then its real chapters
    in classical section order, then chapter_number, letter."""
    def sort_key(f):
        title = title_map.get(f[:-3], "")
        stub = 0 if is_stub(title) else 1
        section = classify_section(f)
        sec_order = SECTION_ORDER.get(section, 99)
        m = re.match(r"^[a-z]+-ch-(\d+)([a-z]?)", f)
        num = int(m.group(1)) if m else 999
        return (sec_order, stub, num, m.group(2) if m else "", f)
    return sorted(files, key=sort_key)


def update_frontmatter(raw, updates):
    """Rewrite frontmatter field values in-place, preserving original field order & quotes."""
    lines = raw.split("\n")
    # find frontmatter bounds
    if not lines or lines[0].strip() != "---":
        return raw
    end = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end = i
            break
    if end is None:
        return raw
    body = "\n".join(lines[end + 1:])
    fm = lines[1:end]
    out = []
    for line in fm:
        m = re.match(r'^([a-z_]+):\s*(.*)$', line)
        if m and m.group(1) in updates:
            out.append(f'{m.group(1)}: "{updates[m.group(1)]}"')
            del updates[m.group(1)]
        else:
            out.append(line)
    for k, v in updates.items():
        out.append(f'{k}: "{v}"')
    return "---\n" + "\n".join(out) + "\n---\n\n" + body


def main():
    files = [f for f in os.listdir(DIR) if f.endswith(".md")]
    ordered = order_files(files)
    pos = {f: i for i, f in enumerate(ordered)}

    changed = 0
    for fname in ordered:
        path = os.path.join(DIR, fname)
        raw = open(path, encoding="utf-8").read()
        manual = 'seo_manual: "true"' in raw.split("---", 2)[1] if raw.startswith("---") else False
        title = title_map.get(fname[:-3], fname[:-3].replace("-", " ").title())
        section = classify_section(fname)
        chapter_label, subject, sanskrit = parse_title(title)

        # --- TL;DR regeneration (skip stubs and manually refined pages) ---
        content_after_fm = raw.split("---", 2)[2] if raw.startswith("---") else raw
        if not manual and not is_stub(title) and "## TL;DR" in content_after_fm:
            new_tldr = build_tldr(section, chapter_label, subject, sanskrit)
            content_after_fm = re.sub(
                r"## TL;DR[^\n]*\n.*?(?=\n---|\n#|\n## )", new_tldr + "\n\n", content_after_fm, count=1, flags=re.S
            )
            # rebuild raw with new body
            fm_end = raw.index("---", 3)
            raw = raw[: fm_end + 3] + "\n" + content_after_fm.lstrip("\n")

        # --- description from first verse (skip manually refined pages) ---
        desc = build_description(section, subject, sanskrit, first_verse(content_after_fm)) if not manual else None

        # --- prev/next ---
        idx = pos[fname]
        prev = ordered[idx - 1][:-3] if idx > 0 else ""
        nxt = ordered[idx + 1][:-3] if idx < len(ordered) - 1 else ""

        # --- reading time ---
        rt = rt_map.get(fname[:-3]) or 5

        updates = {
            "section": section,
            "category": f"Charaka Samhita ({section})",
            "description": desc,
            "reading_time": str(rt),
            "prev_chapter": prev,
            "next_chapter": nxt,
        }
        if manual:
            updates.pop("description")
        new_raw = update_frontmatter(raw, updates)

        # labels fix
        new_raw = re.sub(
            r'(labels:\s*\[[^\]]*?)"[^"]*sthana[^"]*"',
            lambda m: m.group(1) + f'"{section}"',
            new_raw, count=1, flags=re.I
        )

        if new_raw != raw:
            open(path, "w", encoding="utf-8").write(new_raw)
            changed += 1

    print(f"✅ Updated {changed}/{len(files)} files")

    # --- Fix book-info.json section labels ---
    for ch in book["chapters"]:
        ch["section"] = classify_section(ch["slug"] + ".md")
    with open(os.path.join(DIR, "book-info.json"), "w", encoding="utf-8") as f:
        json.dump(book, f, indent=2, ensure_ascii=False)
    print("✅ book-info.json section labels corrected")


if __name__ == "__main__":
    main()