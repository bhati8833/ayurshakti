# Email Marketing System — ayurshakti.shop

> **SEO Component: Traffic Acquisition (Direct + Retention)**
> Part of the ayurshakti.shop traffic ecosystem. Complements SEO (docs/05), Backlinks (docs/12), and Content Syndication (docs/14).

## Architecture

```
Visitor ──► Signup Form (Next.js Newsletter Component)
                │
                ▼
      Google Sheet (subscribers)
                │
                ▼
      Google Apps Script
          ├─ onFormSubmit → Welcome Email + Lead Magnet
          ├─ sendWeeklyNewsletter → Latest 3 articles
          ├─ sendCustomEmail → Ad-hoc broadcast
          └─ checkBounces → Cleanup failed
                │
                ▼
          Gmail SMTP (contact@ayurshakti.shop)
                │
                ▼
          Subscriber Inbox ──► Click ──► ayurshakti.shop (with UTM)
                                              │
                                              ▼
                                          GA4 Tracking
```

### Email Flow

```
        SIGNUP                    WEEKLY                     AD-HOC
    ┌──────────┐            ┌──────────────┐            ┌──────────┐
    │ Form Fill │            │ Time Trigger │            │ Manual   │
    └────┬─────┘            └──────┬───────┘            └────┬─────┘
         │                         │                         │
         ▼                         ▼                         ▼
    Welcome Email            Newsletter Send            Custom Broadcast
    ├─ Lead Magnet PDF       ├─ Fetch 3 latest posts    ├─ Subject + Body
    ├─ "5 Ayurvedic          ├─ Build HTML template     ├─ Send to all active
    │  Home Remedies"        ├─ Loop non-unsubscribed   └─ UTM auto-tagged
    ├─ GA4 tracking          ├─ Batch 80/day (limit)
    ├─ UTM params            └─ GA4 + UTM
    └─ Mark lead_sent=TRUE
```

## Google Sheet Structure

**Sheet Name:** `AyurShakti Email List`
**Spreadsheet ID:** `1-8SFDK23ZXMGKmBfdXpY-wNkwTGWZfTUTy9JJPZAZas`

| Column | Type | Purpose |
|--------|------|---------|
| `A: timestamp` | Auto | Form submission time |
| `B: name` | String | Subscriber first name |
| `C: email` | String | Subscriber email (UNIQUE) |
| `D: source` | String | Signup location (sidebar, popup, post-footer, lead-magnet) |
| `E: lead_sent` | TRUE/FALSE | Welcome email delivered? |
| `F: unsubscribed` | TRUE/FALSE | Opt-out status |
| `G: unsubscribed_at` | Date | When they opted out |
| `H: last_newsletter_sent` | Date | Last newsletter date |
| `I: bounce_count` | Number | Failed delivery count (auto-bounce after 3) |

## Apps Script Code

Deploy this as a **Google Apps Script** project attached to the Sheet.

**File:** `scripts/email-apps-script-code.js` — full deployable code.

### Function Reference

| Function | Trigger | Description |
|----------|---------|-------------|
| `installTriggers()` | Manual (run once) | Sets up form submit + weekly triggers |
| `sendWelcomeEmail(e)` | On form submit | Sends lead magnet + welcome |
| `sendWeeklyNewsletter()` | Time (weekly) | Sends latest 3 articles to all active |
| `sendCustomEmail(subject, bodyHtml)` | Manual (from editor) | Ad-hoc broadcast |
| `addUnsubscribe(email)` | Manual | Marks subscriber as unsubscribed |
| `checkBounces()` | Time (daily) | Checks Gmail bounce reports |
| `sendTestWelcome()` | Manual | Debug: sends welcome to owner |

### Configuration (Edit These)

```javascript
var CONFIG = {
  SHEET_NAME: 'AyurShakti Email List',
  LEAD_MAGNET_URL: 'https://resources.ayurshakti.shop/pdfs/lead-magnet.pdf',
  BLOG_URL: 'https://www.ayurshakti.shop',
  BLOG_NAME: 'AyurShakti',
  OWNER_EMAIL: 'contact@ayurshakti.shop',
  MAX_DAILY_EMAILS: 80,     // GmailApp free limit is 100, keep buffer
  // WEEKLY_SEND_DAY default: 2 (Tue) — set via CONFIG.WEEKLY_SEND_DAY || 2 fallback
  // WEEKLY_SEND_HOUR default: 8 (8 AM EST) — set via CONFIG.WEEKLY_SEND_HOUR || 8 fallback
  UNSUBSCRIBE_BOUNCE_LIMIT: 3  // Auto-unsubscribe after N bounces
};
```

### UTMs (Auto-Tagged)

| Parameter | Welcome Email | Newsletter | Custom |
|-----------|---------------|------------|--------|
| `utm_source` | email | email | email |
| `utm_medium` | email | newsletter | broadcast |
| `utm_campaign` | welcome | weekly-{YYYY-MM-DD} | {custom} |
| `utm_content` | lead-magnet | article-{index} | {content-name} |

### Example Email Templates

**Welcome Email:**
```
Subject: Welcome to AyurShakti — Your Free Guide Inside!

Hi {name},

Welcome to the AyurShakti community! I'm Suresh Bhati, and I'm thrilled
to have you here.

As promised, here's your free guide:
👉 {LEAD_MAGNET_URL}

This guide covers 5 Ayurvedic home remedies for common pet ailments that
you can start using today.

What to expect next:
- Weekly Ayurveda tips and articles in your inbox
- Evidence-based natural remedies for humans and pets
- Early access to new research and guides

Stay healthy,
Suresh Bhati
AyurShakti

---
To unsubscribe: {UNSUBSCRIBE_LINK}
```

**Newsletter:**
```
Subject: This Week in Ayurveda — {DATE}

Hi {name},

Here are this week's top articles from AyurShakti:

1. {Article 1 Title}
   {Article 1 Snippet}
   Read more: {Article 1 Link}

2. {Article 2 Title}
   {Article 2 Snippet}
   Read more: {Article 2 Link}

3. {Article 3 Title}
   {Article 3 Snippet}
   Read more: {Article 3 Link}

Wishing you wellness,
Suresh Bhati

---
To unsubscribe: {UNSUBSCRIBE_LINK}
```

## Lead Magnet

| Item | Details |
|------|---------|
| Title | "5 Ayurvedic Home Remedies for Common Pet Ailments" |
| Format | Google Doc → Export as PDF |
| Storage | GitHub Repo → Cloudflare Pages (`resources.ayurshakti.shop/pdfs/`) |
| Delivery | Welcome email mein PDF link |
| Content | 5 simple home remedies with ingredients, method, dosage |
| Length | 3-5 pages |

**Creation Steps:**
1. Google Docs mein document banao
2. Content fill karo (simple English, actionable)
3. File → Download → PDF → Name: `lead-magnet.pdf`
4. Copy to `blog_images/pdfs/lead-magnet.pdf` (manual step — file lives on Cloudflare R2 at `resources.ayurshakti.shop/pdfs/`, not in git)
5. Git add + commit + push to GitHub
6. Cloudflare Pages auto-deploy karega
7. URL: `https://resources.ayurshakti.shop/pdfs/lead-magnet.pdf`
8. Verify in browser

## Signup Form (Next.js Newsletter Component)

### Custom React Component (Next.js)
```tsx
<form id="ayur-subscribe" action="YOUR_APPS_SCRIPT_WEB_APP_URL" method="POST">
  <h3>Get Weekly Ayurveda Tips</h3>
  <input type="text" name="name" placeholder="Your Name" required />
  <input type="email" name="email" placeholder="Your Email" required />
  <button type="submit">Subscribe</button>
</form>
```

### Component Placement
1. Embedded in Next.js footer and sidebar components.
2. Form submits data directly to Google Apps Script Endpoint.

## Limits & Constraints

| Limit | Value | Mitigation |
|-------|-------|------------|
| GmailApp daily send | 100 recipients/day | Batch 80/day, stagger over week |
| GmailApp recipients/msg | 50 (via CC/BCC) | Send in batches of 50 |
| Apps Script execution | 6 min/execution | Keep list < 500 for weekly send |
| Apps Script triggers | 20 total | Only use 2 triggers |
| Gmail storage | 15 GB free | Unsubscribe bounces regularly |

## Setup Instructions (Step-by-Step)

### 1. Apps Script Setup
1. Open Sheet → Extensions → Apps Script
2. Delete default code → Paste `scripts/email-apps-script-code.js`
3. Save project → Name it "AyurShakti Email"
4. Run `installTriggers()` once → Authorize
5. Run `sendTestWelcome()` → Check email

### 2. Form Setup
1. Google Forms → Create with Name + Email
2. Link response destination to Sheet
3. Add component to Next.js page or layout
4. Test: Submit form → Check sheet → Check email

### 3. Lead Magnet
1. Create PDF guide
2. Upload to Google Drive
3. Update `CONFIG.LEAD_MAGNET_URL`

### 4. Weekly Newsletter
1. Verify `sendWeeklyNewsletter()` ran correctly
2. Check GA4 for email UTM traffic

## Security

| Item | Practice |
|------|----------|
| Script access | Only editor access to Sheet |
| Unsubscribe | Mandatory link in every email |
| Data | Email list never shared |
| Rate limits | Max 80/day, never abuse Gmail |
| Bounce handling | Auto-remove after 3 bounces |

## Integration With Other Docs

| Doc | Connection |
|-----|------------|
| `docs/05-analytics-seo.md` | Email UTM tracking via GA4 Measurement Protocol |
| `docs/12-backlink-strategy.md` | Email outreach for guest posts, niche edits (Phase 3) |
| `docs/14-content-tracking-system.md` | Email send count tracked in api-usage-log.json |

## Version History

| Date | Changes |
|------|---------|
| 2026-07-08 | Initial creation — Sheet + Apps Script + Form + Lead Magnet |
