#!/usr/bin/env python3
import json
import urllib.request
import urllib.parse
from pathlib import Path

ZONE_ID = "f63c29bc9532dc008cd45e2db084ee4e"
TOKEN_FILE = Path("secrets/cloudflare-api-token.txt")

if not TOKEN_FILE.exists():
    print(f"Error: {TOKEN_FILE} not found")
    exit(1)

token = TOKEN_FILE.read_text().strip()
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

# 1. Fetch current DNS records
req = urllib.request.Request(
    f"https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/dns_records?per_page=100",
    headers=headers,
    method="GET"
)

try:
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode())
        records = data.get("result", [])
except Exception as e:
    print("Failed to fetch DNS records:", e)
    exit(1)

print(f"Found {len(records)} existing DNS records.")

blogger_ips = {"216.239.32.21", "216.239.34.21", "216.239.36.21", "216.239.38.21"}

# 2. Delete old Blogger A records
for rec in records:
    r_id = rec["id"]
    r_type = rec["type"]
    r_name = rec["name"]
    r_content = rec["content"]
    
    if r_type == "A" and r_content in blogger_ips:
        print(f"Deleting old Blogger A record: {r_name} -> {r_content} (ID: {r_id})")
        del_req = urllib.request.Request(
            f"https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/dns_records/{r_id}",
            headers=headers,
            method="DELETE"
        )
        try:
            with urllib.request.urlopen(del_req) as del_resp:
                print(f"  Result: {del_resp.status}")
        except Exception as e:
            print(f"  Error deleting {r_id}:", e)

# 3. Add new Firebase A record (199.36.158.100)
new_a_payload = json.dumps({
    "type": "A",
    "name": "ayurshakti.shop",
    "content": "199.36.158.100",
    "ttl": 1,
    "proxied": False
}).encode()

add_a_req = urllib.request.Request(
    f"https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/dns_records",
    data=new_a_payload,
    headers=headers,
    method="POST"
)

print("Adding new A record: ayurshakti.shop -> 199.36.158.100")
try:
    with urllib.request.urlopen(add_a_req) as a_resp:
        res = json.loads(a_resp.read().decode())
        if res.get("success"):
            print("  Successfully added A record!")
        else:
            print("  Failed:", res.get("errors"))
except Exception as e:
    print("  Error adding A record:", e)

# 4. Add new Firebase TXT record (hosting-site=ayur-shakti)
new_txt_payload = json.dumps({
    "type": "TXT",
    "name": "ayurshakti.shop",
    "content": "hosting-site=ayur-shakti",
    "ttl": 1
}).encode()

add_txt_req = urllib.request.Request(
    f"https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/dns_records",
    data=new_txt_payload,
    headers=headers,
    method="POST"
)

print("Adding new TXT record: ayurshakti.shop -> hosting-site=ayur-shakti")
try:
    with urllib.request.urlopen(add_txt_req) as txt_resp:
        res = json.loads(txt_resp.read().decode())
        if res.get("success"):
            print("  Successfully added TXT record!")
        else:
            print("  Failed:", res.get("errors"))
except Exception as e:
    print("  Error adding TXT record:", e)

print("\nDNS update script finished!")
