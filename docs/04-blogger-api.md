# Blogger API — ayurshakti.shop

## Blog Info

| Field | Value |
|-------|-------|
| Blog ID | `944859273218738540` |
| Blog Name | `ayurshakti` |
| URL | `https://www.ayurshakti.shop/` |
| Posts | 0 |

## Authentication Methods

### A) API Key — Read Only (Public Data)

> **⚠️ Actual key in `secrets/blogger-api-key.txt`**

```bash
curl "https://www.googleapis.com/blogger/v3/blogs/944859273218738540?key=YOUR_BLOGGER_API_KEY"
```

### B) OAuth Refresh Token — Read/Write (Recommended)

```
Refresh Token: (see secrets/blogger-oauth-tokens.json)
File:          secrets/blogger-oauth-tokens.json
```

**Get access token:**
```bash
curl -X POST "https://oauth2.googleapis.com/token" \
  -d "client_id=YOUR_CLIENT_ID&client_secret=YOUR_CLIENT_SECRET&refresh_token=YOUR_REFRESH_TOKEN&grant_type=refresh_token"
```

**Python:**
```python
import json, requests

def get_token(config_path="secrets/blogger-oauth-tokens.json"):
    with open(config_path) as f:
        creds = json.load(f)
    r = requests.post("https://oauth2.googleapis.com/token", data={
        "client_id": creds["client_id"],
        "client_secret": creds["client_secret"],
        "refresh_token": creds["refresh_token"],
        "grant_type": "refresh_token"
    })
    return r.json()["access_token"]
```

### C) Service Account — Read Only

```
Email:    blogger-service-account@ayurshakti-501603.iam.gserviceaccount.com
Key File: secrets/ayurshakti-501603-a1a6ff0396df.json
```
Can read blog data via JWT → OAuth token exchange. Cannot write (pending Author invite).

### Regenerating Refresh Token

If refresh token is lost/expired:
```bash
# 1. Generate auth URL (replace YOUR_CLIENT_ID):
# https://accounts.google.com/o/oauth2/auth?client_id=YOUR_CLIENT_ID&redirect_uri=http://localhost:8080&response_type=code&scope=https://www.googleapis.com/auth/blogger&access_type=offline&prompt=consent

# 2. Authorize -> copy code from redirect URL

# 3. Exchange (replace YOUR_CLIENT_ID, YOUR_CLIENT_SECRET, {CODE}):
curl -X POST "https://oauth2.googleapis.com/token" \
  -d "code={CODE}&client_id=YOUR_CLIENT_ID&client_secret=YOUR_CLIENT_SECRET&redirect_uri=http://localhost:8080&grant_type=authorization_code"
```

## API Resources (Blogger v3)

| # | Resource | Methods | Auth Required | Notes |
|---|----------|---------|--------------|-------|
| 1 | **blogs** | GET | API Key / OAuth | Get blog info, posts count, pages count |
| 2 | **blogs** by URL | GET `byurl?url=` | API Key | Lookup blog ID from URL |
| 3 | **posts** | GET, LIST | API Key | List/fetch posts |
| 4 | **posts** | POST, PUT, PATCH, DELETE | OAuth | CRUD operations on posts |
| 5 | **posts** search | GET `search?q=` | API Key | Search posts by keyword |
| 6 | **pages** | GET, LIST | API Key | List/fetch static pages |
| 7 | **pages** | POST, PUT, DELETE | OAuth | CRUD on static pages (`/p/`) |
| 8 | **comments** | GET, LIST | API Key | Read comments |
| 9 | **comments** | DELETE, APPROVE | OAuth | Moderate comments (remove/approve) |
| 10 | **pageViews** | GET | OAuth | Traffic stats (by date range) |
| 11 | **users** | GET | OAuth | User info |
| 12 | **blogUserInfos** | GET | OAuth | Blog + user combined info |
| 13 | **postUserInfos** | GET, LIST | OAuth | Posts with user info |

### ❌ NOT Available via API (Manual Only)

| Feature | How to Manage |
|---------|---------------|
| Theme/XML upload | Blogger Web UI → Theme → Customize → Edit HTML |
| Widget settings | Blogger Web UI → Layout |
| Blog settings (title, meta desc, SEO) | Blogger Web UI → Settings |
| Labels/Tags (standalone CRUD) | Only via posts API (labels embedded) |
| Comments moderation UI | Blogger Web UI → Comments |
| Email posting config | Blogger Web UI → Settings → Email |

> **CRITICAL INSTRUCTION FOR AI:**
> Whenever you modify the Blogger XML theme file (`theme-and-logo/ayurshakti-main.xml`), you MUST immediately create a new "Todo" task in `data/tracking/project-tasks.json` assigned to "User", telling them to manually copy the updated XML code and paste it into the Blogger HTML Editor. Never mark a theme update as completely resolved without assigning this manual step.

**Scope:** `https://www.googleapis.com/auth/blogger`
**Base URL:** `https://www.googleapis.com/blogger/v3/`

### REST Endpoint Cheatsheet

| Method | Endpoint | Auth | Use |
|--------|----------|------|-----|
| GET | `/v3/blogs/{blogId}` | Key | Blog info |
| GET | `/v3/blogs/byurl?url=` | Key | Blog by URL |
| GET | `/v3/blogs/{blogId}/posts` | Key | List posts |
| GET | `/v3/blogs/{blogId}/posts/{postId}` | Key | Single post |
| POST | `/v3/blogs/{blogId}/posts/` | OAuth | Create post |
| PUT | `/v3/blogs/{blogId}/posts/{postId}` | OAuth | Update post |
| PATCH | `/v3/blogs/{blogId}/posts/{postId}` | OAuth | Partial update |
| DELETE | `/v3/blogs/{blogId}/posts/{postId}` | OAuth | Delete post |
| GET | `/v3/blogs/{blogId}/posts/search?q=` | Key | Search posts |
| GET | `/v3/blogs/{blogId}/pages` | Key | List pages |
| GET | `/v3/blogs/{blogId}/pages/{pageId}` | Key | Single page |
| POST | `/v3/blogs/{blogId}/pages` | OAuth | Create page |
| PUT | `/v3/blogs/{blogId}/pages/{pageId}` | OAuth | Update page |
| DELETE | `/v3/blogs/{blogId}/pages/{pageId}` | OAuth | Delete page |
| GET | `/v3/blogs/{blogId}/comments` | Key | List comments |
| DELETE | `/v3/blogs/{blogId}/comments/{commentId}` | OAuth | Delete comment (spam) |
| GET | `/v3/blogs/{blogId}/pageviews` | OAuth | Traffic stats |
| GET | `/v3/users/{userId}` | OAuth | User info |

## Authentication Comparison

| Method | Read Posts/Pages | Write Posts | Theme Upload | Endpoint |
|--------|:-:|:-:|:-:|---------|
| API Key (restricted) | ✅ | ❌ | ❌ | `?key=` querystring |
| OAuth (refresh token) | ✅ | ✅ | ❌ | `Authorization: Bearer` |
| Service Account | ✅ | ❌* | ❌ | JWT exchange |
| Web UI (manual) | — | ✅ | ✅ | Browser |

*\*Service account needs author invite to write*

## Create Post Example

```python
import requests
token = get_token()  # from refresh token above
requests.post("https://www.googleapis.com/blogger/v3/blogs/944859273218738540/posts/",
  headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
  json={"title": "My Post", "content": "<p>HTML content</p>", "labels": ["ayurveda", "health"]})
```
