---
phase: 01-automation-fix
plan: 05
subsystem: automation-pipeline-tracking
tags: [tracking, pipeline, dashboard, automation]
requires: [01-02]
provides: [pipeline-status-tracking]
affects: [data/tracking/pipeline-status.json, scripts/lib/tracking.py, scripts/schedule-posts.py, scripts/social-post.py, scripts/notify-ping.py, scripts/bing-sitemap-submit.py]
tech_stack:
  added: [fcntl (file locking), atomic write pattern]
  patterns: [shared library extension, pipeline stage tracking, CLI interface]
key_files:
  created: []
  modified:
    - scripts/lib/tracking.py
    - scripts/lib/__init__.py
    - scripts/schedule-posts.py
    - scripts/social-post.py
    - scripts/notify-ping.py
    - scripts/bing-sitemap-submit.py
    - data/tracking/pipeline-status.json
decisions:
  - "Used JSON file with atomic writes instead of database for simplicity (D-09)"
  - "File locking with fcntl for concurrent access safety"
  - "Each script updates only its own stage, preserving others"
  - "CLI added to lib.tracking module for querying dashboard"
  - "Status enum: pending, in_progress, completed, failed"
  - "Stage enum: scheduled, published, social-posted, pinged"
metrics:
  duration_seconds: 1200
  tasks_completed: 3
  files_modified: 6
  lines_added: 622
  lines_removed: 34
status: complete
---

# Phase 1 Plan 05: Automation Fix - Pipeline Status Dashboard Summary

## One-Liner
JSON-based pipeline status dashboard tracking each article through scheduled → published → social-posted → pinged stages with CLI query interface.

## Changes Made

### 1. Extended `scripts/lib/tracking.py` with Pipeline Status Functions
- **New constants**: `PIPELINE_STATUS_PATH`, `VALID_STAGES`, `VALID_STATUSES`
- **Core functions**:
  - `load_pipeline_status()` / `save_pipeline_status()` - atomic JSON I/O with file locking
  - `update_pipeline_status(url, stage, status, details)` - validates enums, preserves other stages
  - `get_pipeline_status(url=None)` - returns full dashboard or single article detail
- **Safety**: Atomic writes via temp file + `os.rename()`, `fcntl` locking for concurrency
- **Validation**: Raises `ValueError` for invalid stage/status values

### 2. Updated `scripts/lib/__init__.py`
- Exported new pipeline functions and constants

### 3. Integrated Pipeline Updates into All 4 Chain Scripts

| Script | Stage Updated | Details |
|--------|---------------|---------|
| `schedule-posts.py` | `scheduled` + `published` | On successful Blogger scheduling → `scheduled:completed` with post_id and scheduled time. On LIVE status → `published:completed` with published URL. |
| `bing-sitemap-submit.py` | `pinged` | After IndexNow submit → `pinged:completed` with status_code, or `failed` with error |
| `notify-ping.py` | `pinged` | After pinging 3 services → `pinged:completed` with success/failed counts, or `failed` |
| `social-post.py` | `social-posted` | After all platforms → `social-posted:completed` with per-platform details, or `failed` |

### 4. Added CLI Interface
```bash
# Summary dashboard
python3 -m lib.tracking --pipeline-status

# Single article detail
python3 -m lib.tracking --pipeline-status --url "https://www.ayurshakti.shop/article.html"
```

**Output Example (Summary):**
```
URL                                                          Title                                    Scheduled    Published    Social       Pinged      
--------------------------------------------------------------------------------------------------------------------------------------
https://www.ayurshakti.shop/test-article.html                Test Article                             completed    completed    completed    completed   
```

**Output Example (Detail):**
```
Article: Test Article
------------------------------------------------------------
  scheduled:
    Status: completed
    Timestamp: 2026-07-11T08:10:35.476653+00:00
    Details: {"post_id": "12345", "title": "Test Article", "scheduled_est": "2026-07-11T08:00:00-05:00"}
  published: ...
  social-posted: ...
  pinged: ...
```

## Data Structure (`data/tracking/pipeline-status.json`)
```json
{
  "articles": {
    "https://www.ayurshakti.shop/article.html": {
      "title": "Article Title",
      "stages": {
        "scheduled": {"status": "completed", "timestamp": "...", "details": {...}},
        "published": {"status": "completed", "timestamp": "...", "details": {...}},
        "social-posted": {"status": "completed", "timestamp": "...", "details": {...}},
        "pinged": {"status": "completed", "timestamp": "...", "details": {...}}
      }
    }
  }
}
```

## Verification
- ✅ Automated tests pass: pipeline updates, retrieval, partial update preservation, enum validation
- ✅ All 4 scripts import `update_pipeline_status` and call it for their stages
- ✅ CLI shows summary and detailed views correctly
- ✅ JSON file created atomically with valid structure

## Deviations from Plan
None - executed exactly as specified.

## Threat Flags
| Flag | File | Description |
|------|------|-------------|
| threat_flag: concurrent_write | data/tracking/pipeline-status.json | Multiple scripts may write concurrently; mitigated by fcntl locking and atomic rename |
| threat_flag: info_disclosure | data/tracking/pipeline-status.json | Contains public article URLs and operational status only; no secrets |

## Known Stubs
- None - all pipeline stages wired to actual script execution points