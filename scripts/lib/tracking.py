#!/usr/bin/env python3
"""
Shared tracking utilities for JSON state files.
Centralized load/save, API usage tracking, and article registry operations.
"""
import json
import os
from datetime import datetime, timezone
from typing import Any

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TRACKING_DIR = os.path.normpath(os.path.join(SCRIPT_DIR, "..", "..", "data", "tracking"))

ARTICLE_REGISTRY_PATH = os.path.join(TRACKING_DIR, "article-registry.json")
API_LOG_PATH = os.path.join(TRACKING_DIR, "api-usage-log.json")


def load_json(path: str, default: Any = None) -> Any:
    """
    Load JSON file with graceful handling of missing/malformed files.

    Args:
        path: Path to JSON file
        default: Default value if file missing or invalid (default: empty dict for registry/log, empty list otherwise)

    Returns:
        Parsed JSON data or default
    """
    if default is None:
        # Heuristic: registry/log files are dicts, others may be lists
        default = {} if ("registry" in path or "log" in path) else []

    if os.path.exists(path):
        try:
            with open(path) as f:
                return json.load(f)
        except (json.JSONDecodeError, Exception):
            return default
    return default


def save_json(path: str, data: Any) -> None:
    """
    Save JSON data to file with pretty indentation.

    Args:
        path: Path to write JSON file
        data: Data to serialize
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


def check_api_usage(service_name: str, daily_limit: int = 0, monthly_limit: int = 0) -> bool:
    """
    Check if API usage is within limits before making calls.

    Args:
        service_name: Name of the service (e.g., "blogger_api", "indexnow", "bluesky")
        daily_limit: Max calls per day (0 = unlimited)
        monthly_limit: Max calls per month (0 = unlimited)

    Returns:
        bool: True if within limits, False if limit exceeded
    """
    log = load_json(API_LOG_PATH, {})
    limits = log.get("limits", {})
    svc = limits.get(service_name, {})
    used_today = svc.get("used_today", 0)
    used_month = svc.get("used_this_month", 0)

    if daily_limit > 0 and used_today >= daily_limit:
        return False
    if monthly_limit > 0 and used_month >= monthly_limit:
        return False
    return True


def increment_api_usage(service_name: str) -> None:
    """
    Increment API usage counter after successful call.

    Args:
        service_name: Name of the service that was called
    """
    log = load_json(API_LOG_PATH, {})
    limits = log.setdefault("limits", {})
    svc = limits.setdefault(service_name, {})
    svc["used_today"] = svc.get("used_today", 0) + 1
    svc["used_this_month"] = svc.get("used_this_month", 0) + 1
    log["last_reset_date"] = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    save_json(API_LOG_PATH, log)


def update_article_registry(post_data: dict, status: str, scheduled_est: str | None = None) -> None:
    """
    Update or create article registry entry.

    Args:
        post_data: Dict with at least 'id', 'title', optionally 'url', 'labels'
        status: Article status (e.g., "Scheduled", "Published", "Failed")
        scheduled_est: Optional scheduled time string in EST
    """
    registry = load_json(ARTICLE_REGISTRY_PATH, {"articles": []})
    if "articles" not in registry:
        registry["articles"] = []

    post_id = post_data.get("id")
    found = False

    for art in registry["articles"]:
        if art.get("id") == post_id:
            art.update({
                "title": post_data.get("title"),
                "url": post_data.get("url", ""),
                "status": status,
                "labels": post_data.get("labels", []),
                "scheduled_est": scheduled_est,
                "timestamp": datetime.now(timezone.utc).isoformat()
            })
            found = True
            break

    if not found:
        registry["articles"].append({
            "id": post_id,
            "title": post_data.get("title"),
            "url": post_data.get("url", ""),
            "status": status,
            "labels": post_data.get("labels", []),
            "scheduled_est": scheduled_est,
            "timestamp": datetime.now(timezone.utc).isoformat()
        })

    save_json(ARTICLE_REGISTRY_PATH, registry)


__all__ = [
    "load_json",
    "save_json",
    "check_api_usage",
    "increment_api_usage",
    "update_article_registry",
    "ARTICLE_REGISTRY_PATH",
    "API_LOG_PATH",
    "SCRIPT_DIR",
    "TRACKING_DIR"
]