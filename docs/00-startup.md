# 00-Session-Startup — AyurShakti.shop

## Auto-Execute on Every New Session

### Step 0: Load Profile Identity
1. **CRITICAL:** Read `config/profile.json`. Use the `author.name` (Suresh Bhati) and `contact.email` (contact@ayurshakti.shop) from this file for any content creation, email sending, or identity-related tasks. Do NOT assume the author's name is "shiva" based on the system username, and do NOT use `vle.bhati@gmail.com` for sending/reading emails unless specifically instructed.

### Moltbook Agent Context
- **Agent:** `suresh_bhati` (https://www.moltbook.com/u/suresh_bhati)
- **API Key:** stored in `~/.config/moltbook/credentials.json` (NEVER commit the key to docs — rotate it if it was ever exposed)
- **Owner Email:** contact@ayurshakti.shop
- **Status:** Claimed & Active (account created 2026-07-11)
- **Community:** m/ayurshakti (https://www.moltbook.com/m/ayurshakti) — Owner/Moderator (near-empty; do NOT post here exclusively)
- **Rules:** ENGLISH ONLY for all posts/comments. No Hindi/Devanagari.

#### CRITICAL — Anti-Spam Rules (learned 2026-07-11)
The first post (PCOS Ayurveda backlink) was AUTO-FLAGGED `is_spam: true` with 0 reach, because a brand-new account (karma 7, 3 followers, age < 1 day) posted a self-promotional external backlink. Moltbook's filter penalizes exactly this pattern. Follow these rules on EVERY future post:
1. **No external/self-promotional backlinks from a new or low-karma account.** Do NOT include `ayurshakti.shop` links until the account has built karma (target ≥ ~100) and a real follower base through genuine engagement.
2. **Value-first, never link-first.** The post body must deliver standalone insight, a story, or a genuine question. A blog link is at most a "read more" after value is established — and only once karma allows.
3. **Build karma BEFORE promoting.** Spend sessions commenting thoughtfully on `m/general` AI/agent posts, upvoting, and replying. Karma comes from engagement, not self-promotion.
4. **Post where the audience is.** `m/general` is the active front page. Do not post only to the empty `m/ayurshakti` community.
5. **No repetitive/identical cross-posting or duplicate promotional posts.**
6. **Clean up the flagged post:** the existing spam-flagged PCOS post should be deleted/removed to clear the negative signal before posting compliant content.

#### Reach & Topic Strategy (data-driven, 2026-07-11)
- Moltbook's audience is **AI/agent engineers** ("front page of the agent internet"). The entire high-reach feed is AI/LLM/agent/security/tooling content (top posts: 300+ upvotes, 1000+ comments). Pure Ayurveda/wellness gets ~0 reach AND triggers spam filters (audience + promo mismatch).
- **To get reach with Ayurveda content, frame it for the AI/agent audience**, e.g.:
  - "I built an Ayurvedic knowledge agent / RAG over classical Sanskrit texts"
  - "Ancient diagnostic frameworks (doshas) as a classification model for agent health"
  - "Ayurveda's Agni (digestive fire) as a metaphor for agent context pruning"
  - Biohacking / health-optimization angles the tech audience already engages with
- **Comments drive reach** — end posts with a genuine question to maximize `comment_count`.
- **ROI reality:** Moltbook is low-ROI for pure Ayurveda. Prioritize Ayurveda reach on Reddit (r/ayurveda, r/PCOS), Quora, Pinterest. Use Moltbook only for AI/agent-angled content that builds the brand as a credible "Ayurveda + AI" voice.
- See `docs/16-moltbook-playbook.md` for the full analysis and posting checklist.

### Step 1: Verify Tracking, Tasks & Limits
1. Read `data/tracking/article-registry.json`: Identify how many articles are "Draft" (pending write) and how many are "Ready to Publish" or "Approved". **CRITICAL:** If an article's status is `"Published"`, DO NOT read its body/details. Skip it to save tokens.
2. Read `data/tracking/manual-image-requests.txt`: Identify how many image requests have `Status: Pending`.
3. Read `data/tracking/social-media-log.json` (if exists): Identify any pending social media posts. **CRITICAL:** If a post is `"Published"`, ignore its details.
3. Read `data/tracking/project-tasks.json`: Identify any "Todo" tasks assigned to "AI" or "User". **CRITICAL:** If a task has `"status": "Completed"` or contains the tag `"completed"`, DO NOT read its description or details to save tokens. Skip it.
4. Read `data/tracking/api-usage-log.json` and check credentials: Check current API rate limit status. **CRITICAL:** Only read the `used_today` or main limits, skip deep nested checks unless a limit is nearing 100%.

### Step 2: Dynamic Report & Ask User
Instead of a static list, generate a **Dynamic Action Menu** based on the data gathered in Step 1. Present it to the user like this:

> **System Status:** 
> - 📝 Pending Drafts: [Count]
> - 🖼️ Pending Images: [Count]
> - ✅ Ready to Publish: [Count]
> - 📱 Pending Social Posts: [Count]
> - ⚙️ Pending AI Backlog Tasks: [Count]
> 
> **What should we execute today? (Choose a number)**
> 1. **New Topic Research** (Doc 8)
> 2. **Complete Pending Articles** (Write articles for pending Drafts - Doc 9)
> 3. **Check Manual Image Requests** (User generates images manually - Doc 13)
> 4. **Publish / Schedule Approved Articles** (Doc 11 & Doc 4)
> 5. **Generate / Publish Social Media Posts**
> 6. **Email Marketing Tasks** (Doc 15 — Send newsletter, check subscribers, create lead magnet)
> 7. **Execute Backlink Outreach Strategy** (Doc 12)
> 8. **Execute Pending Backlog Task** (e.g. TASK-002: Update Python scripts)
> 9. **Cloudflare Security & Traffic Report** (Check Cloudflare traffic, bandwidth, bugs, and security/WAF events)
> 10. **Full SEO & Analytics Audit** (Review GSC, Bing Webmaster, and GA4 to analyze page growth and identify drops/weaknesses. Automatically add actionable improvements as new "Todo" tasks in `project-tasks.json`)
> 11. **Custom Request**

---
**CRITICAL INSTRUCTION FOR AI (TOKEN SAVING):** 
Do NOT read or pre-fetch any of the referenced rule documents (e.g., Doc 8, Doc 9, Doc 11, Doc 12, Doc 13) during this startup phase. ONLY load and read a specific document WHEN the user explicitly selects an option from the menu above.
