# Article Approval & Auto-Scheduler — AyurShakti.shop

## Workflow

```
Write Article → 10/10 Checklist → Approval Queue → Auto-Schedule → Publish
                                           ↓
                              schedule-posts.py runs:
                              1. Pick 2 random from queue (10/10 filter + category dedup)
                              2. Calc best time (EST 8-10am / 6-8pm)
                              3. ±15min jitter (bounded to window)
                              4. Blogger API: create/set future published date
                              5. Remove from queue → log
                              6. Indexing API: notify Google about new URL
                              7. Log indexing result (success/retry/fail)
```

## Schedule Config

| Field | Value | Why |
|-------|-------|-----|
| Timezone | `America/New_York` | Target US/CA high CPC |
| Morning window | 8-10am EST | Peak health search |
| Evening window | 6-8pm EST | Post-work wellness reading |
| Posts/day | 2 | Fast growth for new blog |
| Jitter | ±15min | Natural feel, avoid batch flags |
| Weekend | Yes | 7 days/week |

## Pre-Publish Checklist (10/10 Gate)

Har article queue mein tabhi jayega jab **10/10 pass** kare:

| # | Check | How to Verify |
|---|-------|---------------|
| 1 | Featured image present | Post content has `<img>` tag |
| 2 | TL;DR block exists | `<blockquote><strong>TL;DR:</strong>` present |
| 3 | FAQ section (5 Q&A) | Exactly 5 `<h3>` in FAQ section |
| 4 | FAQPage JSON-LD schema | `<script type="application/ld+json">` with FAQPage |
| 5 | Human touch audit | 0 AI tells detected (avoid-ai-writing audit) |
| 6 | Internal links (2-4) | Links to other ayurshakti.shop posts |
| 7 | H2/H3 structure | 5-8 H2 sections with H3 subsections |
| 8 | Word count ≥ 1500 | Count body text only (exclude HTML) |
| 9 | Keyword in H1 + first 100 words | Primary keyword appears naturally |
| 10 | No banned phrases | "The Bottom Line", "In conclusion", etc. |

## Queue System

### Adding to Queue

```python
# approve-article.py usage (or manual JSON edit):
{
  "id": "4511289799426205145",
  "title": "Brahmi Benefits for Brain Health...",
  "content": "<p>HTML content...</p>",
  "labels": ["Ayurvedic Herbs", "Brain Health"],
  "approved_at": "2026-07-07T12:00:00Z"
}
```

Push to `scripts/approval-queue.json`:
```bash
python3 -c "
import json
q = json.load(open('scripts/approval-queue.json'))
q.append({'id': 'POST_ID', 'title': 'TITLE', 'content': 'CONTENT', 'labels': [], 'approved_at': '2026-07-07T12:00:00Z'})
json.dump(q, open('scripts/approval-queue.json','w'), indent=2)
echo 'Added to queue'
"
```

### Running Scheduler

Manual run:
```bash
cd /home/shiva/ayurshakti.shop && python3 scripts/schedule-posts.py
```

Auto via cron (every 12h at midnight + noon EST):
```
0 0,12 * * * cd /home/shiva/ayurshakti.shop && python3 scripts/schedule-posts.py >> scripts/schedule-log.json 2>&1
```

## Scheduler Logic

### Time Calculation

1. Read config (`scripts/schedule-config.json`)
2. Get current time in EST
3. Calculate next 2 schedule windows:
   - **Morning:** If before 8am EST → today 8am + jitter; else → tomorrow 8am + jitter
   - **Evening:** If before 6pm EST → today 6pm + jitter; else → tomorrow 6pm + jitter
4. Pick 2 random articles from queue
5. Assign article to window
6. Send `PUT` to Blogger API with `published: FUTURE_ISO_DATE`
7. Blogger auto-mark as "Scheduled"

### Blogger API Scheduling

Blogger accepts future `published` dates. Post appears in "Scheduled" section:
```python
{
  "title": "...",
  "content": "...",
  "labels": ["..."],
  "published": "2026-07-08T12:15:00.000Z",  # Future date
  "status": "LIVE"
}
```

### Indexing API Integration

Post schedule hone ke baad turant Google ko notify karo:

```python
def notify_google(post_url):
    token = get_service_account_token(indexing_scope=True)
    r = requests.post("https://indexing.googleapis.com/v3/urlNotifications:publish",
        headers={"Authorization": f"Bearer {token}"},
        json={"url": post_url, "type": "URL_UPDATED"})
    return r.ok
```

Post URL format: `https://www.ayurshakti.shop/2026/07/article-name.html`

### Rate Limits & Backoff

| API | Limit | Backoff Strategy |
|-----|:-----:|------------------|
| Blogger API | 100 req/100s | Wait 1s, retry max 3x |
| Indexing API | 1 req/sec (200/day) | Exponential backoff: 1s, 2s, 4s |
| Combined | N/A | 500ms delay between Blogger + Indexing calls |

## Files

| File | Purpose |
|------|---------|
| `scripts/schedule-config.json` | Timezone, windows, posts/day config |
| `scripts/schedule-posts.py` | Main scheduler — pick + calc + API |
| `scripts/approval-queue.json` | Queue of approved articles |
| `scripts/schedule-log.json` | Audit log of all scheduled posts |
| `scripts/scheduler-run.log` | Last run log output |
| `data/tracking/indexing-log.json` | Indexing API call history + status |
| `docs/11-article-approval-scheduler.md` | This rule doc |

## What Else Is Possible

| Feature | Description | Complexity |
|---------|-------------|:----------:|
| Best time auto-learn | GA4 data se peak hours detect kare | ⭐⭐⭐ |
| Batch mode | 7 posts ek saath schedule (1/day for week) | ⭐⭐ |
| Content calendar HTML | `/p/calendar.html` — visual upcoming schedule | ⭐⭐ |
| Auto internal linking | Schedule time pe purane posts mein links daale | ⭐⭐ |
| Telegram/WhatsApp alert | "Post X scheduled for 8am tomorrow" | ⭐⭐ |
| Weekend toggle | Sat-Sun skip kare to avoid low-traffic days | ⭐ |
| Priority queue | "High priority" articles schedule first | ⭐ |
