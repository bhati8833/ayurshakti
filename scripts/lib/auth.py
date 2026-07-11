#!/usr/bin/env python3
"""
Shared authentication utilities for Google APIs.
Centralized Blogger OAuth 2.0 token refresh flow.
"""
import json
import os
from urllib.request import Request, urlopen
from urllib.parse import urlencode

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SECRETS_DIR = os.path.normpath(os.path.join(SCRIPT_DIR, "..", "..", "secrets"))


def get_blogger_access_token():
    """
    Refresh and return Blogger OAuth 2.0 access token.

    Reads secrets/blogger-oauth-tokens.json, POSTs to token_uri with refresh_token,
    returns access_token.

    Returns:
        str: Valid access token for Blogger API calls

    Raises:
        FileNotFoundError: If secrets file doesn't exist
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
    resp = json.loads(urlopen(req).read())

    if "access_token" not in resp:
        raise Exception(f"Token refresh failed: {resp}")
    return resp["access_token"]


__all__ = ["get_blogger_access_token", "SCRIPT_DIR", "SECRETS_DIR"]