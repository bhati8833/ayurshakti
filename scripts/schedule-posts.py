#!/usr/bin/env python3
"""
AyurShakti Auto-Scheduler v1.0
Picks approved articles from queue → schedules at best times (EST)
Morning: 8-10am | Evening: 6-8pm | ±15min jitter
"""

import json
import logging
import os
import random
import sys
import argparse
from datetime import UTC, datetime, timedelta, timezone
from urllib.request import HTTPError, Request, urlopen

import markdown

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from lib.profile import SITEMAP_URL

CONFIG_PATH = os.path.join(SCRIPT_DIR, "schedule-config.json")
QUEUE_PATH = os.path.join(SCRIPT_DIR, "approval-queue.json")
LOG_PATH = os.path.join(SCRIPT_DIR, "schedule-log.json")
LOG_FILE = os.path.join(SCRIPT_DIR, "scheduler-run.log")
TRACKING_DIR = os.path.normpath(os.path.join(SCRIPT_DIR, "..", "data", "tracking"))
os.makedirs(TRACKING_DIR, exist_ok=True)
API_LOG_PATH = os.path.join(TRACKING_DIR, "api-usage-log.json")
ARTICLE_REGISTRY_PATH = os.path.join(TRACKING_DIR, "article-registry.json")

# Use shared logger with rotation from lib.utils
from lib.utils import setup_logger, get_est_now, load_config, dry_run_check, run_subprocess_logged, EST_TZ
from lib.auth import get_blogger_access_token
from lib.tracking import check_api_usage, increment_api_usage, update_article_registry, load_json as load_tracking_json, save_json

logger = setup_logger("scheduler", LOG_FILE)


def get_next_window_times(config, now_est):
    """Calculate next 2 schedule windows (morning + evening) based on current time"""
    windows = sorted(config["schedule_windows"], key=lambda w: w["start_hour"])
    today = now_est.date()
    results = []

    for w in windows:
        start = datetime(today.year, today.month, today.day, w["start_hour"], 0, 0, tzinfo=now_est.tzinfo)
        end = datetime(today.year, today.month, today.day, w["end_hour"], 0, 0, tzinfo=now_est.tzinfo)
        if end <= now_est:
            start += timedelta(days=1)
            end += timedelta(days=1)
        jitter = random.randint(-config["jitter_minutes"], config["jitter_minutes"])
        sched_time = start + timedelta(minutes=random.randint(0, 120))
        sched_time += timedelta(minutes=jitter)
        if sched_time < start:
            sched_time = start
        if sched_time >= end:
            sched_time = end - timedelta(minutes=1)
        results.append({
            "slot": w["slot"],
            "label": w["label"],
            "datetime_est": sched_time,
            "datetime_utc": sched_time.astimezone(UTC)
        })

    return results[:config["posts_per_day"]]


def schedule_post(post_data, publish_at_utc, token, blog_id):
    """Schedule a single post on Blogger with future publish date"""
    api_url = f"https://www.googleapis.com/blogger/v3/blogs/{blog_id}/posts/"

    published_str = publish_at_utc.strftime("%Y-%m-%dT%H:%M:%S.000Z")

    # Convert Markdown to HTML before publishing
    html_content = markdown.markdown(post_data["content"], extensions=['extra', 'tables'])

    body = json.dumps({
        "title": post_data["title"],
        "content": html_content,
        "labels": post_data.get("labels", []),
        "published": published_str,
        "status": "LIVE"
    }).encode("utf-8")

    req = Request(
        api_url,  # POST to /posts/ (no ID in URL)
        data=body,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        },
        method="POST"
    )

    try:
        resp = urlopen(req)
        result = json.loads(resp.read())
        numeric_id = result.get("id")
        logger.info(f"  ✅ Scheduled → EST: {publish_at_utc.astimezone(EST).strftime('%b %d, %I:%M %p')} | UTC: {published_str} | Blogger ID: {numeric_id}")
        return result
    except HTTPError as e:
        err = e.read().decode()[:200]
        logger.error(f"  ❌ API Error {e.code}: {err}")
        return None


# Use zoneinfo-based EST from lib.utils
EST = EST_TZ


def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="AyurShakti Auto-Scheduler")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be scheduled without making API calls")
    args = parser.parse_args()

    # Check dry-run mode
    if dry_run_check("scheduler run"):
        logger.info("=" * 60)
        logger.info("🔍 DRY-RUN MODE: No API calls will be made")
        logger.info("=" * 60)

    logger.info("=" * 60)
    logger.info("🔄 SCHEDULER STARTED")
    logger.info("=" * 60)

    config = load_config("schedule-config.json")
    if not config:
        logger.error("❌ Config not found. Aborting.")
        return

    queue = load_tracking_json(QUEUE_PATH)
    if not queue or len(queue) == 0:
        logger.info("ℹ️  Queue empty. Nothing to schedule.")
        return

    # Filter: only 10/10 checklist passed
    approved = [p for p in queue if p.get("checklist_10_10") is True]
    if not approved:
        logger.info("ℹ️  No articles have passed 10/10 checklist. Nothing to schedule.")
        return

    # Strip 'id' field from approval queue items (Blogger assigns numeric ID on creation)
    for item in approved:
        if "id" in item:
            logger.warning(f"  ⚠️  Stripping 'id' field from queue item: {item['title'][:40]}...")
            del item["id"]

    logger.info(f"📋 Queue has {len(queue)} articles ({len(approved)} approved 10/10)")

    n = min(config["posts_per_day"], len(approved))
    # Category dedup: pick n articles with different top labels
    to_schedule = []
    used_categories = set()
    candidates = sorted(approved, key=lambda p: random.random())
    for p in candidates:
        cats = set(p.get("labels", []))
        if not cats & used_categories or len(to_schedule) == 0:
            to_schedule.append(p)
            used_categories.update(cats)
        if len(to_schedule) >= n:
            break
    # Fallback: if not enough unique-category posts, just pick random
    if len(to_schedule) < n:
        remaining = [p for p in approved if p not in to_schedule]
        extra = random.sample(remaining, min(n - len(to_schedule), len(remaining)))
        to_schedule.extend(extra)

    logger.info(f"🎯 Picked {len(to_schedule)} articles for today:")

    now = get_est_now()
    windows = get_next_window_times(config, now)
    logger.info(f"🕐 Current EST: {now.strftime('%b %d, %I:%M %p')}")
    logger.info(f"📅 Schedule windows: {[w['label'] for w in windows]}")

    try:
        token = get_blogger_access_token()
        logger.info("🔑 OAuth token refreshed")
    except Exception as e:
        logger.error(f"❌ Auth failed: {e}")
        return

    blog_id = config["blog_id"]

    if not check_api_usage("blogger_api"):
        logger.error("❌ Blogger API daily/monthly limit reached. Aborting.")
        return

    log_records = load_tracking_json(LOG_PATH)
    scheduled_ids = []
    failed_ids = []

    for i, post in enumerate(to_schedule):
        if i >= len(windows):
            logger.warning(f"⚠️  No more windows for post: {post['title'][:40]}...")
            break

        win = windows[i]
        logger.info(f"\n📝 Scheduling: {post['title'][:50]}")
        logger.info(f"   Window: {win['label']} → EST: {win['datetime_est'].strftime('%b %d, %I:%M %p')}")

        # Dry-run check for each post
        if dry_run_check(f"schedule '{post['title'][:40]}...'"):
            continue

        result = schedule_post(post, win["datetime_utc"], token, blog_id)

        if result and result.get("status") in ("LIVE", "SCHEDULED"):
            numeric_id = result.get("id")
            scheduled_ids.append(numeric_id)
            increment_api_usage("blogger_api")
            # Update article registry with numeric Blogger ID from API response
            post_with_id = dict(post)
            post_with_id["id"] = numeric_id
            update_article_registry(post_with_id, "Scheduled", win["datetime_est"].strftime("%Y-%m-%d %I:%M %p"))

            # Track syndication results
            syndication_results = {
                "indexnow_status": "pending",
                "ping_status": "pending",
                "social_status": "pending",
            }

            # Notify Bing IndexNow
            try:
                post_url = result.get("url", "")
                if post_url:
                    logger.info(f"  📡 Submitting to IndexNow: {post_url}")
                    success, stdout, stderr = run_subprocess_logged(
                        ["python3", os.path.join(SCRIPT_DIR, "bing-sitemap-submit.py"),
                         "--url", f"https://www.ayurshakti.shop/{post_url}"],
                        logger, timeout=15
                    )
                    syndication_results["indexnow_status"] = "success" if success else "failed"
                    if not success:
                        logger.warning(f"  ⚠️  IndexNow submission failed: {stderr}")
            except Exception as e:
                logger.error(f"  ❌ IndexNow error: {e}")
                syndication_results["indexnow_status"] = "error"

            # Notify ping services
            try:
                ping_url = f"https://www.ayurshakti.shop/{result.get('url', '')}" if result.get('url') else SITEMAP_URL
                logger.info(f"  📡 Pinging services: {ping_url}")
                success, stdout, stderr = run_subprocess_logged(
                    ["python3", os.path.join(SCRIPT_DIR, "notify-ping.py"),
                     "--url", ping_url],
                    logger, timeout=30
                )
                syndication_results["ping_status"] = "success" if success else "failed"
                if not success:
                    logger.warning(f"  ⚠️  Ping services failed: {stderr}")
            except Exception as e:
                logger.error(f"  ❌ Ping services error: {e}")
                syndication_results["ping_status"] = "error"

            # Social auto-post (Bluesky + queue X/LinkedIn)
            try:
                post_url = result.get("url", "")
                post_title = result.get("title", post.get("title", ""))
                if post_url:
                    logger.info(f"  📱 Posting to social: {post_title[:40]}...")
                    success, stdout, stderr = run_subprocess_logged(
                        ["python3", os.path.join(SCRIPT_DIR, "social-post.py"),
                         "--url", f"https://www.ayurshakti.shop/{post_url}",
                         "--title", post_title],
                        logger, timeout=30
                    )
                    syndication_results["social_status"] = "success" if success else "failed"
                    if not success:
                        logger.warning(f"  ⚠️  Social posting failed: {stderr}")
            except Exception as e:
                logger.error(f"  ❌ Social posting error: {e}")
                syndication_results["social_status"] = "error"

            log_records.append({
                "id": numeric_id,
                "title": post["title"],
                "scheduled_est": win["datetime_est"].strftime("%Y-%m-%d %I:%M %p"),
                "scheduled_utc": win["datetime_utc"].strftime("%Y-%m-%dT%H:%M:%SZ"),
                "window": win["slot"],
                "timestamp": datetime.now(UTC).isoformat(),
                "syndication": syndication_results,
            })
        else:
            failed_ids.append(post.get("id", "unknown"))

    # Remove scheduled items from queue
    updated_queue = [p for p in queue if p.get("id") not in scheduled_ids]
    save_json(QUEUE_PATH, updated_queue)
    save_json(LOG_PATH, log_records)

    logger.info("\n📊 RESULTS")
    logger.info(f"   ✅ Scheduled: {len(scheduled_ids)}")
    logger.info(f"   ❌ Failed: {len(failed_ids)}")
    logger.info(f"   📋 Remaining in queue: {len(updated_queue)}")
    logger.info("=" * 60)
    logger.info("✅ SCHEDULER COMPLETE")
    logger.info("=" * 60)


if __name__ == "__main__":
    from urllib.parse import urlencode
    main()
