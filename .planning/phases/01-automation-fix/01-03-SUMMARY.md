---
phase: 01-automation-fix
plan: 03
subsystem: automation-infrastructure
tags: [dependencies, pyproject, ping-services, refactor]
dependency_graph:
  requires: []
  provides: ["requirements.txt", "pyproject.toml", "scripts/notify-ping.py"]
  affects: ["scripts/schedule-posts.py", "scripts/social-post.py", "scripts/bing-sitemap-submit.py"]
tech_stack:
  added:
    - "requirements.txt with pinned deps (requests==2.32.3, markdown==3.6, cryptography==42.0.8, python-dotenv==1.0.1)"
    - "pyproject.toml with ruff, pytest, coverage config"
  patterns:
    - "Modern Python project structure"
    - "Shared lib imports (lib.utils)"
key_files:
  created:
    - requirements.txt
    - pyproject.toml
  modified:
    - scripts/notify-ping.py
decisions:
  - "Pinned exact versions for reproducible installs per RESEARCH.md Standard Stack"
  - "Dev dependencies (pytest, ruff) in pyproject.toml optional-dependencies.dev"
  - "notify-ping.py reduced from 15 to 3 active ping services (IndexNow, Ping-O-Matic, Weblogs.com)"
  - "5-second timeout for all ping requests to prevent hanging"
  - "Added --dry-run support using lib.utils.dry_run_check"
  - "Uses lib.utils.setup_logger for structured logging"
metrics:
  duration_seconds: 180
  completed_date: "2026-07-11"
status: complete
---

# Phase 1 Plan 03: Automation Fix - Dependencies & Ping Cleanup Summary

**One-liner:** Created requirements.txt + pyproject.toml with pinned deps, cleaned notify-ping.py to 3 active services with 5s timeouts and --dry-run support.

## Changes Made

### 1. requirements.txt (NEW)
Created at repo root with pinned runtime dependencies per RESEARCH.md Standard Stack:
- `requests==2.32.3` - HTTP client for API calls
- `markdown==3.6` - Markdown to HTML conversion
- `cryptography==42.0.8` - JWT/service account auth
- `python-dotenv==1.0.1` - Environment variable loading

### 2. pyproject.toml (NEW)
Modern Python project configuration with:
- `[build-system]` - setuptools + wheel
- `[project]` - metadata, Python >=3.12, pinned dependencies
- `[project.optional-dependencies.dev]` - pytest, pytest-cov, ruff
- `[tool.ruff]` - linting config (target py312, line-length 100)
- `[tool.pytest]` - test discovery config
- `[tool.coverage]` - coverage reporting config

### 3. scripts/notify-ping.py (REFACTORED)
**Before:** 15 ping services (many defunct: Google Blog Search, FeedBurner, Technorati, etc.)
**After:** 3 active services with 5s timeout each:
| Service | Type | Endpoint |
|---------|------|----------|
| IndexNow (Bing/Yandex/Seznam) | POST JSON | `https://api.indexnow.org/indexnow` |
| Ping-O-Matic | XML-RPC | `http://rpc.pingomatic.com/` |
| Weblogs.com | XML-RPC | `http://rpc.weblogs.com/ping` |

Added:
- `TIMEOUT = 5` constant applied to all `urlopen()` and `ServerProxy` calls
- `argparse` for `--url` and `--dry-run` flags
- Import `dry_run_check`, `setup_logger` from `lib.utils`
- Structured logging via `setup_logger("notify-ping")`

## Verification Results

```
✅ requirements.txt has all 4 pinned deps
✅ pip install -r requirements.txt succeeds
✅ pyproject.toml validates (tomllib load + structure checks)
✅ notify-ping.py has exactly 3 services
✅ notify-ping.py has 5s timeout
✅ notify-ping.py uses lib.utils imports
✅ python3 scripts/notify-ping.py --dry-run works
```

## Deviations from Plan

None - plan executed exactly as written.

## Auth Gates

None encountered.

## Next Steps

Plan 04 will refactor `schedule-posts.py` to fix the Blogger API 400 error (PUT → POST), add `--dry-run`, and use the new shared lib modules.