#!/usr/bin/env python3
"""
Charaka Samhita — Clean SEO slug renaming (150 files).
Converts Blogger-derived junk slugs (truncations, duplicated 'chapter-N-', wrong section prefixes)
into clean section-scoped slugs derived from each file's frontmatter title.

Rules:
  - Section stubs (title matches is_stub) -> '{section_kebab}-general-principles'
  - Regular chapters -> '{section_kebab}-ch-{num}{letter}-{slugified-title-tail}'
  - Section from classify_section() (with known mislabel exceptions + rasayana/vajikarana rules)

Usage:
  python3 scripts/rename_charaka_slugs.py            # dry-run: prints plan, writes nothing
  python3 scripts/rename_charaka_slugs.py --apply    # git mv files + update book-info.json + refs
"""

import json
import os
import re
import subprocess
import sys

import importlib.util

SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location("ces", os.path.join(SCRIPTS_DIR, "charaka-seo-enrich.py"))
_ces = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_ces)
classify_section = _ces.classify_section
is_stub = _ces.is_stub

DIR = os.path.join("content", "samhitas", "charaka-samhita")
BOOK = os.path.join(DIR, "book-info.json")
TRACKING = os.path.join("data", "tracking", "charaka_audit_tracking.json")

SEC_KEBAB = {
    "Sutrasthana": "sutrasthana",
    "Nidanasthana": "nidanasthana",
    "Vimanasthana": "vimanasthana",
    "Sharirasthana": "sharirasthana",
    "Indriyasthana": "indriyasthana",
    "Chikitsasthana": "chikitsasthana",
    "Kalpasthana": "kalpasthana",
    "Siddhisthana": "siddhisthana",
}


def parse_frontmatter(raw):
    if not raw.startswith("---"):
        return {}
    end = raw.find("\n---", 3)
    if end < 0:
        return {}
    fm = {}
    for line in raw[3:end].split("\n"):
        m = re.match(r'^([a-z_]+):\s*"?([^"]*)"?\s*$', line)
        if m:
            fm[m.group(1)] = m.group(2)
    return fm


def slugify(text, maxlen=100):
    s = text.lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    s = s.strip("-").strip(".")
    return s[:maxlen].rstrip("-")


def clean_title_tail(title):
    """'Chapter 12a - Subject (sanskrit)' -> 'subject-sanskrit' (no 'Chapter N -' prefix)."""
    m = re.match(r"^Chapter\s+\d+[a-z]?\s*-\s*(.+)$", title)
    rest = m.group(1) if m else title
    rest = rest.strip()
    # convert parentheses to dashes for keyword tail: "Therapeutics (Cikitsa)" -> "therapeutics-cikitsa"
    rest = re.sub(r"\((.*?)\)", r"-\1", rest)
    return slugify(rest)


def new_slug_for(fname, title, content):
    base = fname[:-3]
    low_content = content.lower()
    # Content-based override: rasayana/vajikarana quarter-chapters (first verse names
    # the parent chapter "on Vitalization" / "on Virilification") = Chikitsasthana ch 1-2
    section = classify_section(fname)
    if "chapter on vitalization" in low_content or "chapter on virilification" in low_content:
        section = "Chikitsasthana"
    kebab = SEC_KEBAB[section]
    # num from the section prefix (ch-01), letter from the title segment (chapter-1a)
    m1 = re.search(r"-ch-(\d+)([a-z]?)", base)
    m2 = re.search(r"-chapter-(\d+)([a-z]?)", base)
    num = m1.group(1) if m1 else (m2.group(1) if m2 else "")
    letter = (m2.group(2) if m2 and m2.group(2) else (m1.group(2) if m1 else ""))
    if is_stub(title):
        return f"{kebab}-general-principles"
    tail = clean_title_tail(title)
    if not tail:
        tail = slugify(base)  # fallback: cleaned old slug
    return f"{kebab}-ch-{num}{letter}-{tail}"


def main():
    apply_mode = "--apply" in sys.argv
    files = sorted(f for f in os.listdir(DIR) if f.endswith(".md"))
    plan = []
    used = {}
    for fname in files:
        raw = open(os.path.join(DIR, fname), encoding="utf-8").read()
        fm = parse_frontmatter(raw)
        title = fm.get("title", "")
        new = new_slug_for(fname, title, raw) + ".md"
        if new == fname:
            continue
        if new in used:
            used[new].append(fname)
        else:
            used[new] = [fname]
        plan.append((fname, new, title[:70]))

    collisions = {k: v for k, v in used.items() if len(v) > 1}
    print(f"Planned renames: {len(plan)} | collisions: {len(collisions)}")
    for new, olds in collisions.items():
        print(f"  COLLISION -> {new}: {olds}")
    for old, new, title in plan:
        print(f"  {old[:70]}\n    -> {new}")

    if not apply_mode:
        print("\nDRY-RUN (no changes). Re-run with --apply to execute.")
        sys.exit(0 if not collisions else 2)

    # 1) git mv each file
    for old, new, _ in plan:
        subprocess.run(["git", "mv", os.path.join(DIR, old), os.path.join(DIR, new)], check=True)

    # 2) update book-info.json slugs (match by old slug)
    book = json.load(open(BOOK, encoding="utf-8"))
    old_slug_map = {o[:-3]: n[:-3] for o, n, _ in plan}
    changed = 0
    for ch in book["chapters"]:
        if ch.get("slug") in old_slug_map:
            ch["slug"] = old_slug_map[ch["slug"]]
            changed += 1
    json.dump(book, open(BOOK, "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    print(f"✅ book-info.json slugs updated: {changed}")

    # 3) update tracking file slug references
    if os.path.exists(TRACKING):
        raw = open(TRACKING, encoding="utf-8").read()
        for o, n, _ in plan:
            raw = raw.replace(o[:-3], n[:-3])
        open(TRACKING, "w", encoding="utf-8").write(raw)
        print("✅ tracking file slug references updated")

    # 4) global old->new slug replace in all .md files (internal links)
    linked = 0
    for fname in os.listdir(DIR):
        if not fname.endswith(".md"):
            continue
        p = os.path.join(DIR, fname)
        raw = open(p, encoding="utf-8").read()
        new_raw = raw
        for o, n, _ in plan:
            new_raw = new_raw.replace(o[:-3], n[:-3])
        if new_raw != raw:
            open(p, "w", encoding="utf-8").write(new_raw)
            linked += 1
    print(f"✅ internal link replacements across {linked} files")

    print("\n✅ APPLY complete. Re-run charaka-seo-enrich.py to regenerate chains/sections.")


if __name__ == "__main__":
    main()