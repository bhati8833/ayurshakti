#!/usr/bin/env python3
"""
Shared tracking utilities for JSON state files.
Centralized load/save, API usage tracking, article registry, and pipeline status operations.
"""
import fcntl
import json
import os
import tempfile
from datetime import UTC, datetime
from typing import Any

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TRACKING_DIR = os.path.normpath(os.path.join(SCRIPT_DIR, "..", "..", "data", "tracking"))

ARTICLE_REGISTRY_PATH = os.path.join(TRACKING_DIR, "article-registry.json")
API_LOG_PATH = os.path.join(TRACKING_DIR, "api-usage-log.json")
PIPELINE_STATUS_PATH = os.path.join(TRACKING_DIR, "pipeline-status.json")

VALID_STAGES = ("scheduled", "published", "social-posted", "pinged", "indexing")
VALID_STATUSES = ("pending", "in_progress", "completed", "failed")


def _normalize_url(url: str) -> str:
    """Normalize URL: strip trailing slash, ensure https."""
    url = url.rstrip("/")
    if url.startswith("http://"):
        url = "https://" + url[7:]
    return url


def _load_with_lock(path: str, default: Any = None) -> Any:
    """Load JSON file with file locking for thread safety."""
    if default is None:
        default = {} if ("registry" in path or "log" in path or "pipeline" in path) else []

    if not os.path.exists(path):
        return default

    try:
        with open(path) as f:
            fcntl.flock(f.fileno(), fcntl.LOCK_SH)
            try:
                return json.load(f)
            except (json.JSONDecodeError, Exception):
                return default
            finally:
                fcntl.flock(f.fileno(), fcntl.LOCK_UN)
    except (OSError, IOError):
        # Fallback if locking fails (e.g., on some filesystems)
        try:
            with open(path) as f:
                return json.load(f)
        except (json.JSONDecodeError, Exception):
            return default


def _save_with_lock(path: str, data: Any) -> None:
    """Save JSON file atomically with file locking."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    temp_path = path + ".tmp"
    try:
        with open(temp_path, "w") as f:
            fcntl.flock(f.fileno(), fcntl.LOCK_EX)
            try:
                json.dump(data, f, indent=2)
                f.flush()
                os.fsync(f.fileno())
            finally:
                fcntl.flock(f.fileno(), fcntl.LOCK_UN)
        os.rename(temp_path, path)
    except (OSError, IOError):
        # Fallback without locking
        try:
            with open(temp_path, "w") as f:
                json.dump(data, f, indent=2)
            os.rename(temp_path, path)
        except Exception:
            if os.path.exists(temp_path):
                os.remove(temp_path)
            raise


def load_json(path: str, default: Any = None) -> Any:
    """
    Load JSON file with graceful handling of missing/malformed files.

    Args:
        path: Path to JSON file
        default: Default value if file missing or invalid (default: empty dict for registry/log, empty list otherwise)

    Returns:
        Parsed JSON data or default
    """
    return _load_with_lock(path, default)


def save_json(path: str, data: Any) -> None:
    """
    Save JSON data to file with pretty indentation.

    Args:
        path: Path to write JSON file
        data: Data to serialize
    """
    _save_with_lock(path, data)


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
    log["last_reset_date"] = datetime.now(UTC).strftime("%Y-%m-%d")
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
                "timestamp": datetime.now(UTC).isoformat()
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
            "timestamp": datetime.now(UTC).isoformat()
        })

    save_json(ARTICLE_REGISTRY_PATH, registry)


# --- Pipeline Status Functions ---

def load_pipeline_status() -> dict:
    """Load pipeline status from JSON file."""
    return load_json(PIPELINE_STATUS_PATH, {"articles": {}})


def save_pipeline_status(data: dict) -> None:
    """Save pipeline status to JSON file atomically."""
    save_json(PIPELINE_STATUS_PATH, data)


def update_pipeline_status(url: str, stage: str, status: str, details: dict | None = None) -> bool:
    """
    Update pipeline status for an article at a specific stage.

    Args:
        url: Article URL (will be normalized)
        stage: Pipeline stage - one of "scheduled", "published", "social-posted", "pinged"
        status: Stage status - one of "pending", "in_progress", "completed", "failed"
        details: Optional dict with platform-specific info (e.g., {"platform": "bluesky", "post_id": "..."})

    Returns:
        bool: True on success, False on validation error
    """
    if stage not in VALID_STAGES:
        raise ValueError(f"Invalid stage: {stage}. Must be one of {VALID_STAGES}")
    if status not in VALID_STATUSES:
        raise ValueError(f"Invalid status: {status}. Must be one of {VALID_STATUSES}")

    url = _normalize_url(url)
    data = load_pipeline_status()
    articles = data.setdefault("articles", {})

    if url not in articles:
        articles[url] = {
            "title": "",
            "stages": {s: {"status": "pending", "timestamp": None, "details": None} for s in VALID_STAGES}
        }

    article = articles[url]
    timestamp = datetime.now(UTC).isoformat() if status != "pending" else None

    article["stages"][stage] = {
        "status": status,
        "timestamp": timestamp,
        "details": details or None
    }

    # Update title if provided in details
    if details and "title" in details and not article["title"]:
        article["title"] = details["title"]

    save_pipeline_status(data)
    return True


def get_pipeline_status(url: str | None = None) -> dict:
    """
    Get pipeline status for all articles or a specific URL.

    Args:
        url: Optional article URL to filter. If None, returns all articles.

    Returns:
        dict: Pipeline status data
    """
    data = load_pipeline_status()
    if url:
        url = _normalize_url(url)
        articles = data.get("articles", {})
        if url in articles:
            return {"articles": {url: articles[url]}}
        return {"articles": {}}
    return data


__all__ = [
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
    "SCRIPT_DIR",
    "TRACKING_DIR",
    "VALID_STAGES",
    "VALID_STATUSES",
]


def _print_pipeline_summary(data: dict) -> None:
    """Print a summary of all articles in the pipeline."""
    articles = data.get("articles", {})
    if not articles:
        print("No articles in pipeline.")
        return

    print(f"\n{'URL':<60} {'Title':<40} {'Scheduled':<12} {'Published':<12} {'Social':<12} {'Pinged':<12}")
    print("-" * 150)
    for url, article in articles.items():
        title = article.get("title", "")[:38]
        stages = article.get("stages", {})
        sched = stages.get("scheduled", {}).get("status", "pending")[:10]
        publ = stages.get("published", {}).get("status", "pending")[:10]
        social = stages.get("social-posted", {}).get("status", "pending")[:10]
        pinged = stages.get("pinged", {}).get("status", "pending")[:10]
        print(f"{url[:58]:<60} {title:<40} {sched:<12} {publ:<12} {social:<12} {pinged:<12}")


def _print_article_detail(article: dict) -> None:
    """Print detailed status for a single article."""
    title = article.get("title", "Unknown")
    stages = article.get("stages", {})
    print(f"\nArticle: {title}")
    print("-" * 60)
    for stage in VALID_STAGES:
        info = stages.get(stage, {"status": "pending", "timestamp": None, "details": None})
        status = info.get("status", "pending")
        timestamp = info.get("timestamp", "N/A")
        details = info.get("details", {})
        print(f"  {stage}:")
        print(f"    Status: {status}")
        print(f"    Timestamp: {timestamp}")
        if details:
            print(f"    Details: {json.dumps(details, indent=6)}")


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Pipeline status tracking")
    parser.add_argument("--pipeline-status", action="store_true", help="Show pipeline status summary")
    parser.add_argument("--url", help="Filter by article URL")
    args = parser.parse_args()

    if args.pipeline_status:
        data = get_pipeline_status(args.url)
        if args.url:
            articles = data.get("articles", {})
            if args.url in articles:
                _print_article_detail(articles[args.url])
            else:
                print(f"Article not found: {args.url}")
        else:
            _print_pipeline_summary(data)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()