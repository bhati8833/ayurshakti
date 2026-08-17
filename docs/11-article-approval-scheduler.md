# Article Approval & Next.js Publishing Pipeline — AyurShakti.shop

## Workflow

```
Write Article (Markdown) ──► 10/10 Gate Verification ──► Commit & Push to GitHub ──► Firebase Deployment ──► Indexing API Notify
```

---

## Pre-Publish Checklist (10/10 Gate)

Every article must pass the **10/10 quality check** before being published to the static site:

| # | Check | How to Verify |
|---|-------|---------------|
| 1 | **Featured Image Present** | Article has hero image in `/public/images/` or GitHub resource CDN |
| 2 | **TL;DR Block Exists** | Executive summary callout block present |
| 3 | **FAQ Section (5 Q&A)** | Exactly 5 structured Q&A items |
| 4 | **FAQPage JSON-LD Schema** | `<script type="application/ld+json">` with FAQPage schema |
| 5 | **Human Touch Audit** | Passed anti-AI voice check (natural flow, no AI clichés) |
| 6 | **Internal Links (2-4)** | Interlinked to canonical texts or glossary terms (`/glossary`, `/canonical-texts`) |
| 7 | **H2/H3 Heading Hierarchy** | Clean semantic heading structure (1x H1, 5-8 H2s) |
| 8 | **Word Count ≥ 1500** | Deep, authoritative content |
| 9 | **Primary Keyword Placement** | Keyword in H1, URL slug, and first 100 words |
| 10 | **No Cliché Banned Phrases** | Avoid "In conclusion", "The bottom line", etc. |

---

## Build & Deployment Sequence

1. **Write & Save**: Save post as `.md` or `.tsx` inside `content/` / `src/app/articles/`.
2. **Registry Entry**: Add metadata to `data/tracking/article-registry.json`.
3. **Build & Verify**: Run static export check:
   ```bash
   npm run build
   ```
4. **Deploy to Firebase Hosting**:
   ```bash
   firebase deploy --only hosting
   ```
5. **Google Indexing Notification**: Call GCP Indexing API for instant crawling:
   ```python
   python3 scripts/bing-sitemap-submit.py --url https://www.ayurshakti.shop/articles/YOUR-SLUG
   ```
