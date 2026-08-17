#!/usr/bin/env python3
"""
Google Analytics + Search Console traffic reporter.

Fetches GA4 metrics (users, pageviews, sessions) and GSC performance
(clicks, impressions, queries) for ayurshakti.shop.

Usage:
    python3 scripts/analytics-report.py                  # Last 24h
    python3 scripts/analytics-report.py --days 7          # Last 7 days
    python3 scripts/analytics-report.py --days 30         # Last 30 days
    python3 scripts/analytics-report.py --save            # Also save to tracking history
    python3 scripts/analytics-report.py --json            # JSON output (for scripts)
"""
import argparse
import json
import os
import sys
from datetime import UTC, datetime, timedelta

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib.auth import get_google_api_token
from lib.tracking import TRACKING_DIR, load_json, save_json
from lib.utils import setup_logger

GA4_PROPERTY_ID = "533609055"
GSC_SITE_URL = "sc-domain%3Aayurshakti.shop"
HISTORY_PATH = os.path.join(TRACKING_DIR, "analytics-history.json")

logger = setup_logger("analytics", log_file=os.path.join(TRACKING_DIR, "analytics.log"))


def fetch_ga4(token: str, start_date: str, end_date: str) -> dict:
    import urllib.request
    payload = json.dumps({
        "dateRanges": [{"startDate": start_date, "endDate": end_date}],
        "metrics": [
            {"name": "activeUsers"},
            {"name": "screenPageViews"},
            {"name": "sessions"},
            {"name": "newUsers"},
            {"name": "totalUsers"},
            {"name": "averageSessionDuration"},
            {"name": "bounceRate"}
        ],
        "dimensions": [{"name": "date"}]
    }).encode()

    req = urllib.request.Request(
        f"https://analyticsdata.googleapis.com/v1beta/properties/{GA4_PROPERTY_ID}:runReport",
        data=payload,
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    )
    resp = json.loads(urllib.request.urlopen(req).read())
    return resp


def fetch_gsc(token: str, start_date: str, end_date: str, row_limit: int = 10) -> dict:
    import urllib.request
    payload = json.dumps({
        "startDate": start_date,
        "endDate": end_date,
        "dimensions": ["query"],
        "rowLimit": row_limit,
        "orderBy": [{"fieldName": "impressions", "sortOrder": "DESCENDING"}]
    }).encode()

    req = urllib.request.Request(
        f"https://www.googleapis.com/webmasters/v3/sites/{GSC_SITE_URL}/searchAnalytics/query",
        data=payload,
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    )
    resp = json.loads(urllib.request.urlopen(req).read())
    return resp


def parse_ga4_response(resp: dict) -> dict:
    rows = resp.get("rows", [])
    daily = []
    totals = {"users": 0, "new_users": 0, "sessions": 0, "pageviews": 0, "avg_duration": 0.0, "bounce": 0.0}

    for row in rows:
        dims = row.get("dimensionValues", [])
        vals = row.get("metricValues", [])
        if len(dims) < 1 or len(vals) < 7:
            continue
        d = {
            "date": dims[0]["value"],
            "users": int(vals[0].get("value", 0)),
            "pageviews": int(vals[1].get("value", 0)),
            "sessions": int(vals[2].get("value", 0)),
            "new_users": int(vals[3].get("value", 0)),
            "avg_session_duration": float(vals[5].get("value", 0)),
            "bounce_rate": float(vals[6].get("value", 0)),
        }
        daily.append(d)
        totals["users"] += d["users"]
        totals["new_users"] += d["new_users"]
        totals["sessions"] += d["sessions"]
        totals["pageviews"] += d["pageviews"]

    if daily:
        totals["avg_duration"] = sum(d["avg_session_duration"] for d in daily) / len(daily)
        totals["bounce"] = sum(d["bounce_rate"] for d in daily) / len(daily)

    return {"daily": daily, "totals": totals}


def parse_gsc_response(resp: dict) -> dict:
    rows = resp.get("rows", [])
    queries = []
    totals = {"clicks": 0, "impressions": 0, "avg_position": 0.0}

    for r in rows:
        q = {
            "query": r.get("keys", ["?"])[0],
            "clicks": int(r.get("clicks", 0)),
            "impressions": int(r.get("impressions", 0)),
            "position": round(r.get("position", 0), 1),
        }
        queries.append(q)
        totals["clicks"] += q["clicks"]
        totals["impressions"] += q["impressions"]

    if rows:
        totals["avg_position"] = round(
            sum(q["position"] * q["impressions"] for q in queries) / totals["impressions"], 1
        ) if totals["impressions"] > 0 else 0

    return {"queries": queries, "totals": totals}


def build_recommendations(ga4: dict, gsc: dict) -> list:
    recs = []
    gt = ga4["totals"]
    gst = gsc["totals"]

    if gst["impressions"] == 0:
        recs.append(("P0", "GSC shows 0 impressions — site is not indexed/ranking. "
                           "Confirm GSC ownership, submit sitemap.xml, and wire the "
                           "Indexing API into publish flow (docs/05-analytics-seo.md)."))
    else:
        ctr = (gst["clicks"] / gst["impressions"]) * 100 if gst["impressions"] else 0
        if ctr < 2:
            recs.append(("P1", f"Search CTR is {ctr:.2f}% — low. Improve title/description "
                               "snippets and target higher-intent queries."))
        if gst["avg_position"] and gst["avg_position"] > 20:
            recs.append(("P1", f"Avg position {gst['avg_position']:.1f} — pages rank deep. "
                               "Build internal links and topical clusters to push up."))

    if gt["users"] > 0 and gt["new_users"] == gt["users"]:
        recs.append(("P1", "0% returning users — add email capture / remarketing so "
                           "traffic compounds instead of leaking."))

    if gt["pageviews"] > 0 and gt["bounce"] > 0.9:
        recs.append(("P1", f"Bounce {gt['bounce'] * 100:.1f}% is very high — visitors leave "
                           "without engaging. Improve intro/intent match and internal links."))

    if gt["pageviews"] >= gt["sessions"] * 5:
        recs.append(("P2", "High pages/session — good depth. Add internal links between "
                           "posts to spread authority across clusters."))

    if not recs:
        recs.append(("P3", "No critical issues detected. Keep the weekly --save cadence "
                           "and watch impressions/clicks climb."))
    return recs


def print_strategy(ga4: dict, gsc: dict):
    recs = build_recommendations(ga4, gsc)
    print()
    print("=" * 65)
    print("  GROWTH STRATEGY — DATA-DRIVEN RECOMMENDATIONS")
    print("=" * 65)
    for pri, text in recs:
        print(f"\n  [{pri}] {text}")
    print("\n  Full playbook: docs/17-traffic-growth-strategy.md")
    print()


def print_report(ga4: dict, gsc: dict, days: int):
    gt = ga4["totals"]
    gst = gsc["totals"]
    period_label = f"Last {days}d" if days > 1 else "Last 24h"

    print()
    print("=" * 65)
    print(f"  AYURSHAKTI.SHOP — TRAFFIC REPORT ({period_label})")
    print(f"  Generated: {datetime.now(UTC).strftime('%Y-%m-%d %H:%M UTC')}")
    print("=" * 65)

    print("\n  📈 GA4 — Summary")
    print(f"  {'─' * 55}")
    print(f"    Users:          {gt['users']:>8}")
    print(f"    New Users:      {gt['new_users']:>8}")
    print(f"    Sessions:       {gt['sessions']:>8}")
    print(f"    Pageviews:      {gt['pageviews']:>8}")
    print(f"    Avg Duration:   {gt['avg_duration']:>8.0f}s")
    print(f"    Bounce Rate:    {gt['bounce'] * 100:>7.1f}%")

    if ga4["daily"]:
        print(f"\n  {'Date':<12} {'Users':<7} {'New':<7} {'Sessions':<9} {'Pageviews':<11} {'Avg Dur':<9} {'Bounce':<7}")
        print(f"  {'─' * 60}")
        for d in ga4["daily"]:
            dur = f"{d['avg_session_duration']:.0f}s"
            print(f"  {d['date'][:10]:<12} {d['users']:<7} {d['new_users']:<7} {d['sessions']:<9} {d['pageviews']:<11} {dur:<9} {d['bounce_rate'] * 100:<7.1f}%")

    print("\n  🔍 GSC — Search Performance")
    print(f"  {'─' * 55}")
    print(f"    Clicks:         {gst['clicks']:>8}")
    print(f"    Impressions:    {gst['impressions']:>8}")
    if gst["impressions"] > 0:
        ctr = (gst["clicks"] / gst["impressions"]) * 100
        print(f"    CTR:            {ctr:>7.2f}%")
        print(f"    Avg Position:   {gst['avg_position']:>8.1f}")

    if gsc["queries"]:
        print(f"\n  {'Query':<40} {'Clicks':<8} {'Impressions':<12} {'Position':<8}")
        print(f"  {'─' * 68}")
        for q in gsc["queries"]:
            print(f"  {q['query'][:38]:<40} {q['clicks']:<8} {q['impressions']:<12} {q['position']:<8}")
    else:
        print("\n  ℹ️  No search data yet — Google still crawling new site.")

    print()


def save_to_history(ga4: dict, gsc: dict, days: int):
    history = load_json(HISTORY_PATH, {"reports": []})
    history.setdefault("reports", [])

    entry = {
        "timestamp": datetime.now(UTC).isoformat(),
        "period_days": days,
        "ga4_totals": ga4["totals"],
        "ga4_daily": ga4["daily"],
        "gsc_totals": gsc["totals"],
        "gsc_queries": gsc["queries"][:10],
    }
    history["reports"].append(entry)

    # Keep last 90 reports
    if len(history["reports"]) > 90:
        history["reports"] = history["reports"][-90:]

    save_json(HISTORY_PATH, history)
    logger.info(f"Report saved to analytics-history.json (#{len(history['reports'])})")


def run_report(days: int = 1, save: bool = False, json_output: bool = False, strategy: bool = False) -> dict:
    token = get_google_api_token()
    today = datetime.now(UTC).strftime("%Y-%m-%d")
    start = (datetime.now(UTC) - timedelta(days=days - 1)).strftime("%Y-%m-%d")

    try:
        ga4_raw = fetch_ga4(token, start, today)
        ga4 = parse_ga4_response(ga4_raw)
    except Exception as e:
        logger.error(f"GA4 fetch failed: {e}")
        ga4 = {"daily": [], "totals": {"users": 0, "new_users": 0, "sessions": 0, "pageviews": 0, "avg_duration": 0, "bounce": 0}}

    try:
        gsc_raw = fetch_gsc(token, start, today)
        gsc = parse_gsc_response(gsc_raw)
    except Exception as e:
        logger.error(f"GSC fetch failed: {e}")
        gsc = {"queries": [], "totals": {"clicks": 0, "impressions": 0, "avg_position": 0}}

    if save:
        save_to_history(ga4, gsc, days)

    if json_output:
        result = {
            "ga4": ga4,
            "gsc": gsc,
            "period_days": days,
            "generated_at": datetime.now(UTC).isoformat()
        }
        print(json.dumps(result, indent=2))
    elif strategy:
        print_strategy(ga4, gsc)
    else:
        print_report(ga4, gsc, days)

    return {"ga4": ga4, "gsc": gsc}


def main():
    parser = argparse.ArgumentParser(description="Google Analytics + Search Console traffic report")
    parser.add_argument("--days", type=int, default=1, help="Number of days to report (default: 1)")
    parser.add_argument("--save", action="store_true", help="Save report to tracking history")
    parser.add_argument("--json", action="store_true", help="Output raw JSON instead of formatted table")
    parser.add_argument("--strategy", action="store_true", help="Print data-driven growth recommendations")
    args = parser.parse_args()

    run_report(days=args.days, save=args.save, json_output=args.json, strategy=args.strategy)


if __name__ == "__main__":
    main()
