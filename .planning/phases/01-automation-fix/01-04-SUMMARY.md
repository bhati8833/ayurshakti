---
phase: 01-automation-fix
plan: 04
subsystem: automation
tags: [logging, subprocess, rotation, utils]
requires: [01-02]
provides: [run_subprocess_logged, rotating_logger]
affects: [schedule-posts.py, lib.utils]
decisions:
  - "Used stdlib logging.handlers.RotatingFileHandler (no external deps)"
  - "run_subprocess_logged returns (success, stdout, stderr) for flexible handling"
  - "Dry-run mode logs commands without executing"
  - "All three syndication scripts now have output captured and logged"
metrics:
  duration_minutes: 45
  completed: "2026-07-11"
  tasks_completed: 3
  files_modified: 2
  lines_added: 120
  lines_removed: 80
status: complete
---

# Phase 1 Plan 04: Automation Fix - Subprocess Logging & Log Rotation Summary

## One-Liner
Added `run_subprocess_logged()` to capture stdout/stderr from all subprocess calls in `schedule-posts.py` and implemented 5MB/5-file log rotation via `RotatingFileHandler` in shared `lib.utils`.

## Changes Made

### scripts/lib/utils.py (+70 lines)
- **Added `run_subprocess_logged(cmd_list, logger, timeout=30, dry_run_check=True)`**:
  - Uses `subprocess.run()` with `capture_output=True, text=True, timeout=timeout`
  - Returns `(success: bool, stdout: str, stderr: str)`
  - On success: logs stdout at INFO, stderr at WARNING if present
  - On failure: logs stderr at ERROR, stdout at DEBUG
  - On timeout/exception: logs error, returns `(False, "", error_msg)`
  - Respects `--dry-run` flag: logs "DRY-RUN: would execute ..." and returns `(True, "", "")`
- **Enhanced `setup_logger()`** with `RotatingFileHandler`:
  - `maxBytes=5*1024*1024` (5MB)
  - `backupCount=5` (keeps 5 rotated files)
  - Format: `"%(asctime)s | %(levelname)s | %(message)s"`
  - Console + rotating file handlers both at INFO level
- Exported new functions in `__all__`

### scripts/schedule-posts.py (refactored)
- **Imports**: Now uses shared `lib.utils` for `setup_logger`, `run_subprocess_logged`, `get_est_now`, `load_config`, `dry_run_check`, `EST_TZ`
- **Removed**: Local `log()` function, local `now_est()` function, local `load_json()` for config
- **Replaced 3 `subprocess.run()` calls** with `run_subprocess_logged()`:
  1. `bing-sitemap-submit.py` — captures IndexNow submission result
  2. `notify-ping.py` — captures ping service results
  3. `social-post.py` — captures social posting results
- **Removed bare `except Exception: pass`** blocks — all errors now logged with full output
- **Added syndication tracking** in `schedule-log.json`:
  - `indexnow_status`: "success" | "failed" | "error" | "pending"
  - `ping_status`: "success" | "failed" | "error" | "pending"
  - `social_status`: "success" | "failed" | "error" | "pending"
- **Logger used directly** (no wrapper `log()` function)

## Verification Results

### Automated Tests
```
✅ setup_logger creates rotating log with correct format
✅ run_subprocess_logged respects --dry-run
✅ run_subprocess_logged captures stdout/stderr
✅ Log rotation works: main + rotated backups, count limited (max 3 + main)
✅ schedule-posts.py imports and parses correctly
✅ Uses shared utils and run_subprocess_logged
✅ No bare except Exception: pass
✅ Tracks syndication results
```

### Human Verification (Dry-Run)
```
$ python3 scripts/schedule-posts.py --dry-run
  🔍 DRY-RUN: scheduler run
2026-07-11 13:25:27,315 | INFO | ============================================================
2026-07-11 13:25:27,316 | INFO | 🔍 DRY-RUN MODE: No API calls will be made
2026-07-11 13:25:27,316 | INFO | ============================================================
...
```

- Log file `scripts/scheduler-run.log` created with rotating handler format
- Shows "DRY-RUN: would execute ..." for each subprocess command
- No actual API calls made in dry-run mode
- Timestamps and log levels properly formatted

## Threat Model Compliance

| Threat ID | Category | Mitigation |
|-----------|----------|------------|
| T-04-01 | Info Disclosure | Logs contain no secrets; only titles, URLs, status |
| T-04-02 | DoS (Log Growth) | 5MB × 5 files = 25MB cap prevents disk exhaustion |
| T-04-03 | Injection | `run_subprocess_logged` uses list args (`shell=False`), no user input in commands |

## Success Criteria Met

- ✅ **R-018**: All subprocess calls in `schedule-posts.py` log stdout/stderr on success and failure
- ✅ **R-022**: `scheduler-run.log` rotates at 5MB, keeps 5 backups via `RotatingFileHandler`
- ✅ Shared utils provide reusable logging and subprocess utilities for other scripts

## Deviations from Plan
None — plan executed exactly as written.

## Known Stubs
None — all functionality implemented and verified.

## Threat Flags
None — no new attack surface introduced beyond what's in threat model.

## Self-Check
- [x] Created files exist: `scripts/lib/utils.py`, `scripts/schedule-posts.py`
- [x] Commits exist for all changes
- [x] Automated tests pass
- [x] Human verification (dry-run) passes