# 00-Session-Startup — AyurShakti.shop

## Auto-Execute on Every New Session

### Step 0: Load Profile Identity
1. **CRITICAL:** Read `config/profile.json`. Use the `author.name` (Suresh Bhati) and `contact.email` (contact@ayurshakti.shop) from this file for all content, emails, or metadata attribution. Do NOT assume the author's name is "shiva" based on the system username.

---

### Step 1: Platform & Infrastructure Context (Next.js + Firebase + Cloudflare + GitHub)
- **Framework**: Next.js 14 SSG (`output: 'export'`) with React, TypeScript, Tailwind CSS, Motion.
- **Hosting**: Firebase Hosting (Static Edge CDN, site: `ayur-shakti`).
- **CDN & Security**: Cloudflare (DNS, DDoS Protection, Edge Caching, Brotli Compression).
- **Image Hosting**: GitHub repository & Cloudflare resource proxy (`resources.ayurshakti.shop`).

---

### Step 2: Verify Tracking, Content & Tasks
1. Read `data/tracking/article-registry.json`: Identify how many articles are "Draft" (pending write) and how many are "Ready to Publish" or "Published". **CRITICAL:** If an article status is `"Published"`, skip its body to save tokens.
2. Read `data/tracking/manual-image-requests.txt`: Identify pending image requests.
3. Read `data/tracking/project-tasks.json`: Identify "Todo" tasks assigned to "AI" or "User". **CRITICAL:** If a task is `"Completed"`, skip it to save tokens.
4. Read `data/tracking/api-usage-log.json`: Verify system rate limits and status.

---

### Step 3: Dynamic Action Menu
Present a streamlined **Dynamic Action Menu** based on the status gathered:

> **System Status:** 
> - 📝 Pending Drafts: [Count]
> - 🖼️ Pending Images: [Count]
> - ✅ Ready to Publish: [Count]
> - 📱 Pending Social Posts: [Count]
> - ⚙️ Pending AI Backlog Tasks: [Count]
> 
> **What should we execute today? (Choose a number)**
> 1. **New Topic Research** (Doc 08)
> 2. **Complete Pending Articles** (Write Next.js Markdown articles — Doc 09)
> 3. **Check Manual Image Requests** (GitHub image hosting workflow — Doc 34)
> 4. **Build & Deploy to Firebase Hosting** (`npm run build` && `firebase deploy --only hosting` — Doc 35)
> 5. **Generate / Publish Social Media Posts** (Bluesky, Pinterest, X)
> 6. **Email Marketing Tasks** (Doc 15)
> 7. **Execute Backlink Outreach Strategy** (Doc 12)
> 8. **Execute Pending Backlog Task** (Check `project-tasks.json`)
> 9. **Cloudflare Security & Traffic Report** (Check Cloudflare edge metrics & security logs)
> 10. **Full SEO & Analytics Audit** (Review GSC, Bing Webmaster, GA4)
> 11. **Custom Request**

---

**CRITICAL TOKEN SAVING INSTRUCTION:** 
Do NOT pre-fetch or read any referenced rule documents (Doc 08, Doc 09, Doc 34, Doc 35) during startup. ONLY read a specific document WHEN the user explicitly selects that action.
