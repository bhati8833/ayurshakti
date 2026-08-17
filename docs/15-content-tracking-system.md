# Content & API Tracking System

## Overview
This tracking system is the single source of truth for the AI Agent to prevent duplicate content creation and strictly monitor API rate limits.

---

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
- Once built and deployed to Firebase Hosting, update status to `Published`, set the `published_at` timestamp, and save the live URL (`/articles/slug-name`).

### 3. API Limit Guard
Before executing any social syndication script or making API calls:
- Read `data/tracking/api-usage-log.json`.
- Check if the current date matches `last_reset_date`. If not, reset `used_today` counters to `0` and update the date.
- Verify that `used_today` + planned posts <= `daily_limit`.
- If the limit is reached, ABORT posting for that specific platform.
- After a successful post, increment the counters in `data/tracking/api-usage-log.json`.

---

## File Locations
- **Content Ledger:** `data/tracking/article-registry.json`
- **Rate Limit Log:** `data/tracking/api-usage-log.json`
- **Email Subscribers:** Google Sheet (`AyurShakti Email List`)
