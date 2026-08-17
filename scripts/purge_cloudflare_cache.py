#!/usr/bin/env python3
"""
Purge Cloudflare CDN Cache using stored zone ID and API token.
"""

import json
import urllib.request
from pathlib import Path

ROOT = Path("/home/shiva/ayurshakti.shop")
ZONE_ID_FILE = ROOT / "secrets" / "cloudflare-zone-id.txt"
TOKEN_FILE = ROOT / "secrets" / "cloudflare-api-token.txt"

def purge_cache():
    if not ZONE_ID_FILE.exists() or not TOKEN_FILE.exists():
        print("❌ Cloudflare secrets not found in secrets/ directory.")
        return False
        
    zone_id = ZONE_ID_FILE.read_text().strip()
    token = TOKEN_FILE.read_text().strip()
    
    url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/purge_cache"
    data = json.dumps({"purge_everything": True}).encode("utf-8")
    
    req = urllib.request.Request(
        url,
        data=data,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        },
        method="POST"
    )
    
    try:
        with urllib.request.urlopen(req) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            if result.get("success"):
                print("⚡ Cloudflare CDN Cache successfully purged (Purge Everything: True)!")
                return True
            else:
                print("❌ Cloudflare API Error:", result.get("errors"))
                return False
    except Exception as e:
        print(f"❌ Failed to purge Cloudflare cache: {e}")
        return False

if __name__ == "__main__":
    purge_cache()
