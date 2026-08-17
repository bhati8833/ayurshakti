#!/usr/bin/env python3
"""
Seznam Webmaster API Client for ayurshakti.shop
API Docs: https://reporter.seznam.cz/wm/
"""
import json
import os
import sys
import urllib.request
import urllib.error

SECRETS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "secrets")
API_KEY_FILE = os.path.join(SECRETS_DIR, "seznam-api-key.txt")
BASE_URL = "https://reporter.seznam.cz/wm/api"

def get_api_key():
    with open(API_KEY_FILE) as f:
        return f.read().strip()

def make_request(endpoint, method="GET", data=None, params=None):
    api_key = get_api_key()
    url = f"{BASE_URL}{endpoint}"
    if params:
        from urllib.parse import urlencode
        url += "?" + urlencode(params)
    
    req = urllib.request.Request(url, method=method)
    req.add_header("Authorization", f"Bearer {api_key}")
    req.add_header("Content-Type", "application/json")
    req.add_header("Accept", "application/json")
    req.add_header("User-Agent", "ayurshakti-seznam-api/1.0")
    
    if data:
        req.data = json.dumps(data).encode("utf-8")
    
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.load(resp)
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        print(f"HTTP {e.code}: {error_body}")
        raise
    except Exception as e:
        print(f"Request failed: {e}")
        raise

def get_web_status(site_url="https://www.ayurshakti.shop"):
    """Get site overview"""
    return make_request("/web", params={"url": site_url})

def get_documents(site_url="https://www.ayurshakti.shop", limit=100):
    """Get page counts and sample URLs"""
    return make_request("/web/documents", params={"url": site_url, "limit": limit})

def get_documents_history(site_url="https://www.ayurshakti.shop", days=30):
    """Get historical page counts"""
    return make_request("/web/documents-history", params={"url": site_url, "days": days})

def get_document_info(site_url="https://www.ayurshakti.shop", url=None):
    """Get info about specific URL"""
    params = {"url": site_url}
    if url:
        params["document"] = url
    return make_request("/web/document", params=params)

def reindex_url(site_url="https://www.ayurshakti.shop", url=None):
    """Request reindex of specific URL (requires write key)"""
    data = {"url": site_url}
    if url:
        data["document"] = url
    return make_request("/web/document/reindex", method="POST", data=data)

def list_sites():
    """List configured domains"""
    return make_request("/sites")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Seznam Webmaster API Client")
    parser.add_argument("command", choices=["status", "documents", "history", "document", "reindex", "sites"])
    parser.add_argument("--url", help="Site URL (default: https://www.ayurshakti.shop)")
    parser.add_argument("--document", help="Specific document URL")
    parser.add_argument("--limit", type=int, default=100, help="Limit for documents")
    parser.add_argument("--days", type=int, default=30, help="Days for history")
    args = parser.parse_args()
    
    site_url = args.url or "https://www.ayurshakti.shop"
    
    result = None
    try:
        if args.command == "status":
            result = get_web_status(site_url)
        elif args.command == "documents":
            result = get_documents(site_url, args.limit)
        elif args.command == "history":
            result = get_documents_history(site_url, args.days)
        elif args.command == "document":
            result = get_document_info(site_url, args.document)
        elif args.command == "reindex":
            result = reindex_url(site_url, args.document)
        elif args.command == "sites":
            result = list_sites()
        
        if result:
            print(json.dumps(result, indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)