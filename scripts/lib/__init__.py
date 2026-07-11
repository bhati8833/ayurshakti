#!/usr/bin/env python3
"""
scripts.lib - Shared utilities for AyurShakti automation scripts.

Exports:
- auth: get_blogger_access_token()
- tracking: load_json, save_json, check_api_usage, increment_api_usage, update_article_registry, load_pipeline_status, save_pipeline_status, update_pipeline_status, get_pipeline_status
- utils: setup_logger, load_config, get_est_now, dry_run_check, DRY_RUN
- paths: SCRIPT_DIR, PROJECT_DIR, SECRETS_DIR, TRACKING_DIR, EST_TZ
"""
from .auth import get_blogger_access_token
from .tracking import (
    API_LOG_PATH,
    ARTICLE_REGISTRY_PATH,
    PIPELINE_STATUS_PATH,
    VALID_STAGES,
    VALID_STATUSES,
    check_api_usage,
    get_pipeline_status,
    increment_api_usage,
    load_json,
    load_pipeline_status,
    save_json,
    save_pipeline_status,
    update_article_registry,
    update_pipeline_status,
)
from .utils import (
    DRY_RUN,
    EST_TZ,
    PROJECT_DIR,
    SCRIPT_DIR,
    SECRETS_DIR,
    TRACKING_DIR,
    dry_run_check,
    get_est_now,
    load_config,
    setup_logger,
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
    "load_pipeline_status",
    "save_pipeline_status",
    "update_pipeline_status",
    "get_pipeline_status",
    "ARTICLE_REGISTRY_PATH",
    "API_LOG_PATH",
    "PIPELINE_STATUS_PATH",
    "VALID_STAGES",
    "VALID_STATUSES",
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