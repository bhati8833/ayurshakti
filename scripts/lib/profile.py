#!/usr/bin/env python3
"""
Central profile loader for ayurshakti.shop scripts.
Usage:
  from lib.profile import PROFILE, SITE_URL, AUTHOR_NAME, CONTACT_EMAIL
"""
import json
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.normpath(os.path.join(SCRIPT_DIR, ".."))
CONFIG_PATH = os.path.join(PROJECT_DIR, "config", "profile.json")

def load():
    if not os.path.exists(CONFIG_PATH):
        raise FileNotFoundError(f"Profile not found: {CONFIG_PATH}")
    with open(CONFIG_PATH) as f:
        return json.load(f)

PROFILE = load()
SITE = PROFILE["site"]
AUTHOR = PROFILE["author"]
CONTACT = PROFILE["contact"]
BRAND = PROFILE["brand"]
SCRIPTS = PROFILE["scripts"]

SITE_URL = SITE["url"]
SITE_NAME = SITE["name"]
SITE_DOMAIN = SITE["domain"]
SITEMAP_URL = SITE["sitemap"]
AUTHOR_NAME = AUTHOR["name"]
CONTACT_EMAIL = CONTACT["email"]
