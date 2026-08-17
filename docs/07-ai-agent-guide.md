# AI Agent Guide — ayurshakti.shop

## First File to Read

**START HERE:** `README.md` (project root) — has the document index.
Then read this file for agent-specific instructions.

---

## Doc Reading Sequence (Priority)

| Order | File | When to Read |
|-------|------|-------------|
| 1 | `README.md` | Always — entry point |
| 2 | `docs/07-ai-agent-guide.md` | Always — agent instructions |
| 3 | `docs/01-overview.md` | First time / new task |
| 4 | `docs/35-firebase-hosting.md` | Deployment / Firebase tasks |
| 5 | `docs/34-resource-hosting.md` | Image asset hosting tasks |
| 6 | `docs/02-cloudflare.md` | DNS / edge infra tasks |
| 7 | `docs/05-analytics-seo.md` | SEO / reporting tasks |
| 8 | `docs/06-credentials.md` | Reference — lookup only |
| 9 | `docs/03-gcp-apis.md` | GCP / API management tasks |

---

## Key Task Routing Guide

| User Request | Tool / Action | Reference Doc |
|--------------|---------------|---------------|
| "Build static site" | `npm run build` | `docs/35-firebase-hosting.md` |
| "Deploy to Firebase" | `firebase deploy --only hosting` | `docs/35-firebase-hosting.md` |
| "Upload image asset" | Store in `/public/images/` or push to GitHub media repo | `docs/34-resource-hosting.md` |
| "Check GA4 analytics" | Google Analytics Data API | `docs/05-analytics-seo.md` |
| "SEO keyword analysis" | Search Console API + `websearch` | `docs/05-analytics-seo.md` |
| "Manage DNS / Cloudflare" | Cloudflare API token | `docs/02-cloudflare.md` |
| "Submit to Bing" | `python3 scripts/bing-sitemap-submit.py` | `docs/09-article-writing-rule.md` |
| "Send email" | `email_send_email` | `docs/15-email-marketing-system.md` |

---

## Continuous Task Tracking & Clean Code Rules

1. **Always know the next step:** Evaluate logical follow-ups upon completing any task.
2. **Handle Manual Dependencies:** If manual user action is needed, record a Todo task in `data/tracking/project-tasks.json` assigned to "User".
3. **Keep Code Clean:** Use `scratch/` for temporary one-off scripts and delete them after execution.
4. **Security Rules:** NEVER print secrets/tokens in output; load all credentials dynamically from `secrets/`.
