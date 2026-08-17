# AGENTS.md — ayurshakti.shop

## Session Startup (MANDATORY)

Read and execute `docs/00-startup.md` on every new session. It loads `config/profile.json` for identity, checks tracking files, and presents an action menu. Do NOT read any other docs until the user selects an action.

## Identity

Author is **Suresh Bhati** (from `config/profile.json`). Do NOT assume "shiva" from the system username. Use `contact@ayurshakti.shop` for email operations.

## Environment & Platform

- **Framework**: Next.js 14 (React, TypeScript, Tailwind CSS, Motion) — `output: 'export'`
- **Hosting**: Firebase Hosting (Static Site Generation / Edge CDN — project `ayur-shakti`)
- **DNS & CDN**: Cloudflare (DDoS Protection, Edge Caching, Brotli, SSL)
- **Image Hosting**: GitHub repository & Cloudflare resource proxy (`resources.ayurshakti.shop`)
- **Python**: ≥ 3.12 (required for automation scripts)
- **Node.js**: ≥ 18 (required for Next.js build & Firebase tools)
- **Secrets**: All credentials in `secrets/` (gitignored). See `docs/04-credentials.md`.

## Key Commands

```bash
# Build Next.js static output locally
npm run build

# Push changes to GitHub to trigger automated CI/CD deployment
git add .
git commit -m "Deployment update"
git push origin master

# Submit sitemap/URL to Bing IndexNow
python3 scripts/bing-sitemap-submit.py
python3 scripts/bing-sitemap-submit.py --url ARTICLE_URL

# Ping search engines after publish
python3 scripts/notify-ping.py

# Social syndication (Bluesky/X/Pinterest)
python3 scripts/social-post.py --url URL --title "Title"
```

## Linting / Formatting

Ruff is configured in `pyproject.toml`:
```bash
ruff check .        # lint
ruff format .       # format
```

Next.js linting:
```bash
npm run lint
```

## Internal Linking Rule (Next.js / Firebase)

- Use clean relative URLs: `/articles/slug-name`
- For glossary terms: `/glossary`
- For canonical texts: `/canonical-texts`
- For dosha quiz: `/dosha-quiz`
- Do NOT use legacy Blogger URLs (`/2026/07/slug.html` or `/search?q=`).

## Critical Gotchas

- **Firebase Hosting**: Ensure `npm run build` generates the `out/` folder cleanly before deploying.
- **Image Hosting**: Use GitHub repository (`/public/images` or `blog_images/`) and `resources.ayurshakti.shop`.
- **Published articles**: When reading `article-registry.json`, skip items with status "Published" to save tokens.
- **Author name**: Always use "Suresh Bhati" for bylines, never "shiva".

## Herb Profile Generation Pipeline

```bash
# Full pipeline (run after content updates)
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

## Key Directories

| Path | Purpose |
|------|---------|
| `content/herbs/` | Published herb profiles (10 existing) |
| `content/herbs_draft/` | Generated drafts awaiting validation |
| `content/samhitas/` | Classical text chapters (366 chapters) |
| `content/canonical_texts/` | Classical manuscripts & research |
| `content/glossary/` | 21,499 Sanskrit terms (A-Z JSON) |
| `data/herb_synonyms.json` | 42 herbs × multilingual names + 2 formulas |
| `data/herb_index.json` | Extracted data for all 42 profiles |

## Combination Formula Exclusion Rule

- **Triphala**: amalaki, haritaki, bibhitaki → NOT listed as ingredients elsewhere
- **Dashmool**: 10 roots → NOT listed as ingredients elsewhere
- Formula pages list components; components link to formula

## Quality Gates

| Content Type | Gate | Status |
|--------------|------|--------|
| Articles | 16/16 (docs/13-article-writing-rule.md) | Active |
| Herb Profiles | 16/16 (docs/21-herb-profile-generation.md) | TL;DR/FAQ/Schema pending |

