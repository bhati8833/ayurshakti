# Content & API Tracking System

## Overview
This tracking system is the single source of truth for the AI Agent to prevent duplicate content creation and strictly monitor API rate limits to prevent account bans.

## Mandatory AI Workflow Rules

Whenever the AI Agent is tasked with content creation, publishing, or social syndication, it MUST follow these rules:

### 1. Pre-Flight Content Check
Before outlining or writing a new article, the AI MUST read `data/tracking/article-registry.json`.
- Check if the proposed `keyword` or `topic` already exists.
- If it exists, abort and pick a new topic.

### 2. Registration & Publishing
When a new article is drafted:
- Register the entry in `data/tracking/article-registry.json` with status `Draft`.
- Record the featured image status in the registry under an `image` object (e.g., `{"status": "Pending" | "Generated", "file_name": "...", "path": "..."}`).
- Once published to Blogger, update the status to `Published`, set the `published_at` timestamp, and save the live `url`.

### 3. API Limit Guard
Before executing any social syndication script or making API calls:
- Read `data/tracking/api-usage-log.json`.
- Check if the current date matches `last_reset_date`. If not, reset `used_today` counters to `0` and update the date.
- Verify that `used_today` + planned posts <= `daily_limit`.
- If the limit is reached, ABORT posting for that specific platform to prevent bans.
- After a successful post, increment the counters in `data/tracking/api-usage-log.json`.

### 4. Syndication Update
After posting to a social platform (via API or Browser Automation):
- Open `data/tracking/article-registry.json`.
- Locate the article by `id`.
- Update the `social_syndication` section for that platform (e.g., set `bluesky.status = "Done"`, set timestamp, and record the post URL).

### 5. Email Send Limits
Before sending any email blast (newsletter or broadcast):
- GmailApp free limit: **100 recipients/day**
- Apps Script ke `CONFIG.MAX_DAILY_EMAILS = 80` (buffer)
- Bounce tracking: auto-unsubscribe after 3 bounces per `docs/15-email-marketing-system.md`
- Newsletter weekly trigger: Tuesday 8am EST

## File Locations
- **Content Ledger:** `data/tracking/article-registry.json`
- **Rate Limit Log:** `data/tracking/api-usage-log.json`
- **Email Subscribers:** Google Sheet (`AyurShakti Email List`)
