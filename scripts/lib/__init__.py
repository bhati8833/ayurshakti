#!/usr/bin/env python3
"""
scripts.lib - Shared utilities for AyurShakti automation scripts.

Exports:
- auth: get_blogger_access_token()
- tracking: load_json, save_json, check_api_usage, increment_api_usage, update_article_registry
- utils: setup_logger, load_config, get_est_now, dry_run_check, DRY_RUN
- paths: SCRIPT_DIR, PROJECT_DIR, SECRETS_DIR, TRACKING_DIR, EST_TZ
"""
from .auth import get_blogger_access_token
from .tracking import (
    load_json,
    save_json,
    check_api_usage,
    increment_api_usage,
    update_article_registry,
    ARTICLE_REGISTRY_PATH,
    API_LOG_PATH,
)
from .utils import (
    setup_logger,
    load_config,
    get_est_now,
    dry_run_check,
    DRY_RUN,
    SCRIPT_DIR,
    PROJECT_DIR,
    SECRETS_DIR,
    TRACKING_DIR,
    EST_TZ,
)

__all__ = [
    # auth
    "get_blogger_access_token",
    # tracking
    "load_json",
    "save_json",
    "check_api_usage",
    "increment_api_usage",
    "update_article_registry",
    "ARTICLE_REGISTRY_PATH",
    "API_LOG_PATH",
    # utils
    "setup_logger",
    "load_config",
    "get_est_now",
    "dry_run_check",
    "DRY_RUN",
    # paths
    "SCRIPT_DIR",
    "PROJECT_DIR",
    "SECRETS_DIR",
    "TRACKING_DIR",
    "EST_TZ",
]

__version__ = "1.0.0"