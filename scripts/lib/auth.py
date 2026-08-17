#!/usr/bin/env python3
"""
Shared authentication utilities for Google APIs.
Centralized Blogger OAuth 2.0 token refresh flow.
"""
import base64
import json
import os
import time
from urllib.parse import urlencode
from urllib.request import Request, urlopen

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SECRETS_DIR = os.path.normpath(os.path.join(SCRIPT_DIR, "..", "..", "secrets"))


def get_google_api_token(scopes: str | None = None) -> str:
    """
    Generate JWT-based access token from GCP service account.

    Uses secrets/ayurshakti-501603-a1a6ff0396df.json to generate
    a signed JWT and exchange it for an OAuth 2.0 bearer token.

    Args:
        scopes: Space-separated OAuth scopes (default: analytics + webmasters)

    Returns:
        str: Valid bearer token for Google APIs

    Raises:
        FileNotFoundError: If service account JSON not found
        Exception: If token exchange fails
    """
    from cryptography.hazmat.primitives import serialization, hashes
    from cryptography.hazmat.primitives.asymmetric import padding

    if scopes is None:
        scopes = ("https://www.googleapis.com/auth/analytics.readonly "
                  "https://www.googleapis.com/auth/webmasters")

    sa_path = os.path.join(SECRETS_DIR, "ayurshakti-501603-a1a6ff0396df.json")
    if not os.path.exists(sa_path):
        raise FileNotFoundError(f"Service account JSON not found: {sa_path}")

    with open(sa_path) as f:
        data = json.load(f)

    key = serialization.load_pem_private_key(data["private_key"].encode(), password=None)

    now = int(time.time())
    claim = json.dumps({
        "iss": data["client_email"],
        "scope": scopes,
        "aud": "https://oauth2.googleapis.com/token",
        "exp": now + 3600,
        "iat": now
    })
    header_b64 = base64.urlsafe_b64encode(
        json.dumps({"alg": "RS256", "typ": "JWT"}).encode()
    ).rstrip(b"=").decode()
    payload_b64 = base64.urlsafe_b64encode(claim.encode()).rstrip(b"=").decode()
    unsigned = f"{header_b64}.{payload_b64}"
    sig = base64.urlsafe_b64encode(
        key.sign(unsigned.encode(), padding.PKCS1v15(), hashes.SHA256())
    ).rstrip(b"=").decode()
    jwt = f"{unsigned}.{sig}"

    req = Request(
        "https://oauth2.googleapis.com/token",
        data=urlencode({
            "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
            "assertion": jwt
        }).encode(),
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    resp = json.loads(urlopen(req).read())

    if "access_token" not in resp:
        raise Exception(f"Token exchange failed: {resp}")
    return resp["access_token"]


def get_blogger_access_token() -> str:
    """
    Refresh and return Blogger OAuth 2.0 access token.

    Reads client_id, client_secret, refresh_token, and token_uri from
    secrets/blogger-oauth-tokens.json and performs token refresh.

    Returns:
        str: Valid access token for Blogger API calls

    Raises:
        FileNotFoundError: If secrets file not found
        Exception: If token refresh fails
    """
    secrets_path = os.path.join(SECRETS_DIR, "blogger-oauth-tokens.json")
    if not os.path.exists(secrets_path):
        raise FileNotFoundError(f"Blogger OAuth tokens not found: {secrets_path}")

    with open(secrets_path) as f:
        s = json.load(f)

    data = {
        "client_id": s["client_id"],
        "client_secret": s["client_secret"],
        "refresh_token": s["refresh_token"],
        "grant_type": "refresh_token"
    }
    req = Request(s["token_uri"], data=urlencode(data).encode(), method="POST")
    resp = json.loads(urlopen(req).read().decode())

    if "access_token" not in resp:
        raise Exception(f"Token refresh failed: {resp}")
    return resp["access_token"]


__all__ = [
    "get_blogger_access_token",
    "get_google_api_token",
    "SCRIPT_DIR",
    "SECRETS_DIR"
]