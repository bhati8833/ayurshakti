# Domain Pitfalls: Health Blog (Blogger) × AdSense Monetization

**Domain:** Ayurvedic health/wellness blog on Google Blogger, monetized via AdSense
**Researched:** 2026-07-11
**Overall confidence:** HIGH (synthesized from multiple 2026 AdSense and SEO sources)

---

## How to Read This Document

Pitfalls are ranked by severity. **Critical** = causes AdSense rejection or permanent account ban. **Moderate** = kills traffic growth or wastes effort. **Minor** = reduces efficiency but won't sink the project.

Each pitfall includes:
- **Warning signs** — detect early before it's too late
- **Prevention** — how to avoid (actionable)
- **Phase mapping** — which roadmap phase should address it
- **AdSense policy risk** — whether this violates AdSense ToS

---

## Critical Pitfalls

### Pitfall C1: YMYL Health Content Without E-E-A-T Signals (AdSense Rejection #1 for Health Blogs)

**What goes wrong:** Google treats health/wellness content as "Your Money or Your Life" (YMYL). For AdSense approval, health sites must demonstrate Experience, Expertise, Authoritativeness, and Trustworthiness (E-E-A-T). An Ayurveda blog with no author bylines, no credentials, no disclaimers, and anonymous AI-written content triggers the highest scrutiny level. Most health blogs get rejected on this alone.

**Why it happens:**
- Blogger does not natively support author bio pages with credentials
- AI-written articles lack personal experience signals
- No named author = "unaccountable publisher" in reviewer eyes
- The platform makes it hard to add structured author markup

**Consequences:**
- AdSense rejection with "Low Value Content" (catch-all for E-E-A-T failure)
- Even if approved, Google may limit ad serving or demonetize later
- Pages rank lower in search due to YMYL quality rater demotion

**AdSense policy violation:** YES — Policy 8 (Content Quality). Health content without expertise signals is treated as high-risk.

**Warning signs:**
- No author name appears on any blog post
- About page has no mention of who writes the health content
- Articles make specific health claims without citing sources
- No medical/health disclaimer visible on the site
- AI detection tools score articles >80% AI-written

**Prevention:**
1. Add a named "Editor" or "Reviewed by" line to every health article (Blogger supports post author in settings)
2. Create an author bio page showing relevant experience (even if it's "Ayurveda enthusiast with 5 years of research")
3. Add PubMed / government health site citations to every health claim
4. Include a prominent **Medical Disclaimer** on ALL health posts: "This content is for informational purposes only and is not medical advice. Consult a qualified health practitioner."
5. Add reviewer attribution — even an AI-assisted disclosure adds transparency

**Phase:**
- Phase 1 (Content Infrastructure): Add medical disclaimer template, author attribution system, citation format
- Phase 3 (AdSense Application): Audit every published article for E-E-A-T signals before applying

---

### Pitfall C2: Unedited AI Content That Reads Like Generic Output

**What goes wrong:** Google's 2026 AdSense policy does not ban AI content — but it aggressively rejects spammy, templated, unedited AI output. Generic AI articles that "could have been written by anyone" are flagged as "Low Value Content." The March 2026 Core Update specifically targeted sites publishing 50+ AI articles/day without human oversight.

**Why it happens:**
- AI agent generates articles at high volume with similar structure
- No human editing pass to add unique examples, personal stories, or specific insights
- Every article follows the same H2 structure pattern → detected as templated
- All articles have the same "voice" — no author differentiation

**Consequences:**
- "Low Value Content" rejection from AdSense
- Google Search may de-index entire sections (site-wide penalty)
- The March 2026 update showed that sites with >40% unedited AI content lost 55%+ traffic

**AdSense policy violation:** YES — falls under "Spammy Automatically Generated Content" and "Low-value content."

**Warning signs:**
- Article Word document comparisons show identical structure across posts
- No first-person anecdotes or unique examples in any article
- AI detection tools flag most content
- Articles lack specific local knowledge (Ayurveda needs regional context)

**Prevention:**
1. Implement a mandatory human editing step before approval queue
2. AI generates draft → human/editor adds: unique insight, local example, personal story
3. Vary article structure: some listicles, some how-to guides, some Q&A, some personal-experience
4. Add original images (AI-generated images count as original — better than stock photos)
5. Keep AI-to-publish ratio at max 5-7 articles/week (not 50/day)
6. Add transparency footer: "This article was researched and written with AI assistance and reviewed by [Editor Name]"

**Phase:**
- Phase 1 (Content Pipeline): Add editorial review gate before approval queue
- Phase 2 (Quality Systems): Build automated 10/10 checklist validator
- Phase 3 (Pre-AdSense): Audit all 30+ articles for generic AI patterns

---

### Pitfall C3: Missing Mandatory Pages (About, Contact, Privacy, Disclaimer, Terms)

**What goes wrong:** Google AdSense requires a Privacy Policy, About Us, Contact, and Terms & Conditions. For health blogs, a Medical Disclaimer is also mandatory. Missing any of these is an immediate rejection trigger. The Privacy Policy must specifically mention Google AdSense use of cookies and third-party ad networks.

**Why it happens:**
- Blogger new blogs often skip these pages (they're not auto-created)
- Bloggers assume content alone is enough
- Health-specific disclaimers are overlooked

**Consequences:**
- Instant AdSense rejection with "Missing Policy Pages" or "Site Not Ready"
- GDPR/CCPA compliance failure (legal risk for EU/CA visitors)

**AdSense policy violation:** YES — Policy 1 (Privacy Policy) and Policy 9 (Transparency).

**Warning signs:**
- Check footer of site — no Privacy Policy link
- Searching "site:ayurshakti.shop privacy policy" returns nothing
- No Contact page with email/phone
- Health articles have no disclaimer at top or bottom

**Prevention:**
1. Create ALL five pages before the first AdSense application:
   - **Privacy Policy** (must mention AdSense, cookies, third-party ads, GDPR/CCPA)
   - **About Us** (include author/editor background, site purpose)
   - **Contact Us** (functional contact form or email)
   - **Terms & Conditions** (user agreement, copyright notice)
   - **Medical Disclaimer** (prominently linked on all health posts)
2. Link ALL pages in the footer navigation
3. Update Privacy Policy to 2026 standards (must mention AI crawlers like GPTBot, ClaudeBot — relevant because site has llms.txt)

**Phase:**
- Phase 0 (Foundation): Create all 5 pages before anything else
- Phase 3 (Pre-AdSense): Audit pages for completeness against 2026 standards
- Ongoing: Update Privacy Policy annually

---

### Pitfall C4: Applying for AdSense Too Early (With Too Few Posts)

**What goes wrong:** Multiple sources across 2026 confirm that 15-25 high-quality articles is the practical threshold for AdSense approval. Applying with 5-8 thin articles is the #1 reason for rejection. Each rejection adds a cooldown (2-4 weeks before reapply is safe), delaying monetization by months.

**Why it happens:**
- "Get approved fast" culture pushes premature applications
- The project has 11 published articles — below the 15-25 threshold
- Articles may be high-quality individually but the site lacks volume

**Consequences:**
- Rejection with "Insufficient Content" — vague, demoralizing
- Must wait 2-4 weeks before reapplying
- Each rejection also hurts because Google re-reviews the entire site

**AdSense policy violation:** Not directly, but triggers the "Low Value Content" rejection umbrella.

**Warning signs:**
- Article count < 15 published
- Total word count across all articles < 15,000 words
- No content in some categories or labels
- Site age < 60 days

**Prevention:**
1. Do NOT apply until at least **20 high-quality articles** are published
2. Each article should be 1000-2000 words minimum
3. Ensure articles cover multiple sub-topics within Ayurveda (topical depth)
4. Apply only when the site has been actively publishing for 2+ months
5. Apply when you see consistent organic traffic (even 500 visits/month helps)

**Phase:**
- Phase 3 (AdSense Application): Must be scheduled — don't apply in Phase 1 or 2

---

### Pitfall C5: No Medical Disclaimer on Health Content

**What goes wrong:** This is specific to health/wellness blogs. Google AdSense reviewers are trained to check for health disclaimers. Articles that give health advice (Ayurvedic remedies for PCOS, Giloy benefits, etc.) without disclaimers are treated as "potentially harmful content." This is a hard rejection signal.

**Why it happens:**
- Bloggers assume herbal/natural remedies are "safe" and don't need disclaimers
- No template in Blogger theme for health disclaimers
- AI-generated articles don't auto-include disclaimers

**Consequences:**
- AdSense rejection (Policy 8 — harmful health content)
- Legal liability if a reader follows advice and suffers harm
- Google can ban the entire Adsense account permanently if health misinformation is flagged

**AdSense policy violation:** YES — Critical. Health misinformation/prohibited content.

**Warning signs:**
- Searching article content for "consult your doctor" — not found
- No disclaimer box at the top or bottom of health articles
- Articles use definitive language ("this cures X") instead of suggestive ("may help with X")

**Prevention:**
1. Add a standardized medical disclaimer template to the Blogger theme
2. Every health article MUST include: "This information is for educational purposes only. Consult a healthcare provider before starting any treatment."
3. Avoid definitive medical claims: Use "may help," "traditionally used for," "some studies suggest" — NEVER "cures," "treats," "prevents" (this is also FDA/regulatory risk)
4. Include the disclaimer in the article body (not just sidebar/footer)

**Phase:**
- Phase 0 (Foundation): Add disclaimer template to theme
- Phase 1 (Content Pipeline): Auto-append disclaimer to every AI-generated health article
- Phase 3 (Pre-AdSense): Audit all articles for disclaimer compliance

---

## Moderate Pitfalls

### Pitfall M1: Broken Automation Scheduler Preventing Consistent Publishing

**What goes wrong:** The auto-scheduler (`schedule-posts.py`) has NEVER successfully published a single article — every run fails with "Invalid post id" 400 error. This means the 5-7 articles/week pipeline cannot function. Google favors sites with consistent, predictable publishing schedules. Months of silence followed by 20 articles dumped at once looks like a content farm.

**Why it happens:**
- Queue entries use placeholder string IDs instead of actual Blogger numeric post IDs
- Code was never tested end-to-end before being put into production
- No error output checking in subprocess calls

**Consequences:**
- Content production stalls — 22 drafts never get published
- No consistent publishing cadence → Google sees an inactive site
- Social posting, ping notifications, IndexNow all depend on the scheduler → entire pipeline dead
- 10 published articles have zero social distribution (no social proof for AdSense review)

**AdSense policy violation:** Indirect — an inactive site with irregular publishing looks like a low-effort site to reviewers.

**Warning signs:**
- Scheduler logs show 400 errors on every run
- Article registry has "scheduled" entries that never move to "published"
- Social post stats show all articles have empty social_posts: {}

**Prevention:**
1. Fix the post ID bug: replace string IDs with actual numeric Blogger post IDs
2. Implement a `--dry-run` mode for safe testing
3. Run scheduler manually for 1 week to verify it works before enabling cron
4. Add logging that surfaces failures (currently silently swallowed)
5. Build a status dashboard showing: scheduled → published → social-posted → pinged

**Phase:**
- Phase 1 (Fix Automation): This is the highest-priority technical fix

---

### Pitfall M2: Targeting Competition-Heavy Keywords Without Long-Tail Strategy

**What goes wrong:** New health blogs target broad keywords like "ayurvedic medicine" or "PCOS treatment" that have SEO difficulty scores of 70+. These keywords are dominated by established health portals (Healthline, WebMD, NDTV Health). A 3-month-old Blogger blog has zero chance of ranking for these. Result: no organic traffic, no AdSense revenue.

**Why it happens:**
- AI keyword research defaults to high-volume, high-competition terms
- No understanding of domain authority disadvantage (new domain, Blogger subdomain history)
- "Publish and pray" approach instead of strategic keyword targeting

**Consequences:**
- Zero organic traffic for 6+ months
- AdSense rejection because site has no visitors (not mandatory but helps approval)
- At ~$1-3 RPM, even 1000 visits/month = $1-3/month — not worth the effort

**Warning signs:**
- Search Console shows impressions but zero clicks for target keywords
- Target keywords have >50 SEO difficulty scores
- Articles rank on page 5+ for all targets
- Competitor analysis shows Healthline/WebMD dominating every target

**Prevention:**
1. Target ONLY long-tail keywords: "giloy benefits for thyroid patients in Hindi" not "giloy benefits"
2. Use "question-based" keywords: "can I take ashwagandha with thyroid medication" not "ashwagandha benefits"
3. Focus on ["informational intent" keywords] — people searching for answers, not product comparisons
4. Build topical clusters: 15-20 articles on "Ayurveda for digestive health" rather than one article each on 20 unrelated topics
5. Use Google Search Console data to find keywords where the site already ranks (even position 50+) and optimize those articles

**Phase:**
- Phase 1 (Content Pipeline): Keyword research methodology built into article topic selection
- Phase 2 (SEO Systems): Add keyword difficulty checker to the topic validation step

---

### Pitfall M3: Blogger Platform Limitations That Kill E-E-A-T Signals

**What goes wrong:** Blogger is severely limited compared to WordPress for demonstrating E-E-A-T. No author box plugins, no schema markup plugins, no way to add verified credentials, no custom post types for author pages. Reviewers comparing a Blogger health site to a WordPress health site see the Blogger site as less professional.

**Why it happens:**
- Team chose Blogger for zero-cost, but the E-E-A-T tradeoff is significant
- Blogger's native author system is weak (one Google account = one author)
- Adding JSON-LD author markup requires manual theme editing
- No way to add "Reviewed by Dr. X" badges or medical review timestamps

**Consequences:**
- AdSense reviewers may subconsciously downgrade Blogger health sites
- Harder to prove "accountable publisher" status (anonymous Google account as author)
- Schema markup must be maintained manually in theme XML (fragile approach)

**Warning signs:**
- All articles show "Posted by Unknown" or the same Google account name
- No author photo, credentials, or links to professional profiles (LinkedIn, etc.)
- JSON-LD author field is missing or points to a generic Google profile
- No way to have multiple expert authors

**Prevention:**
1. Create a dedicated "Author" page in Blogger as a static page with full credentials
2. In each post, manually add an author bio box at the bottom (HTML widget in theme)
3. Add SameAs links in JSON-LD pointing to LinkedIn, Twitter, any professional profiles
4. If possible, get a real Ayurveda practitioner to review content and list them as "Reviewed by Dr. [Name]"
5. Consider adding a "Content reviewed on [date]" badge to articles
6. Use the llms.txt Worker to expose author credentials to AI crawlers as a trust signal

**Phase:**
- Phase 1 (Content Infrastructure): Add author box template, update JSON-LD
- Phase 3 (Pre-AdSense): Audit all articles for author attribution completeness

---

### Pitfall M4: Pinterest Strategy Done Wrong (Spamming Without SEO)

**What goes wrong:** Pinterest is the #1 recommended traffic source for new health/wellness blogs. But common mistakes kill results: pinning the same image repeatedly, no keyword-optimized pin descriptions, no Rich Pins, pinning only own content, ignoring mobile optimization. Result: zero traffic from Pinterest after months of effort.

**Why it happens:**
- Social auto-poster sends identical pin designs for every article
- No Pinterest-specific keyword research
- Pin descriptions are auto-generated and generic
- Pinterest Rich Pins are not set up (Blogger supports them but requires configuration)
- Pinterest account is treated like Twitter (post frequency ≠ pin frequency)

**Consequences:**
- Zero referral traffic from Pinterest (a $0 traffic source wasted)
- Missed AdSense approval signal (consistent traffic from ANY source helps)

**Warning signs:**
- Pinterest analytics show < 100 monthly outbound clicks after 3 months of pinning
- Pins have no descriptions or generic descriptions
- All pins for different articles look visually identical
- Rich Pins validation fails
- Pinterest account is personal, not business (no analytics available)

**Prevention:**
1. Convert Pinterest account to Business (free, enables analytics)
2. Set up Rich Pins for Blogger (adds article title, description, author automatically to pins)
3. Create 3-5 different pin designs per article (different images, text overlays)
4. Write keyword-rich pin descriptions (200-300 chars, front-load keywords)
5. Follow 80/20 rule: 20% own content, 80% other relevant pins
6. Pin consistently: 5-15 pins/day, spaced out (use Tailwind free or manual scheduling)
7. Target seasonal content 45-60 days ahead (e.g., "winter ayurvedic tips" in October)

**Phase:**
- Phase 1 (Content Pipeline): Add Pinterest-specific pin creation to publishing workflow
- Phase 4 (Traffic Growth): Dedicated Pinterest SEO optimization sprint

---

### Pitfall M5: Ignoring Google Search Console & Indexing Issues

**What goes wrong:** The project has Google Search Console connected but the Indexing API integration is NOT implemented. Google is not being notified of new content. Additionally, the indexing log is empty (`[]`), meaning no one is monitoring which pages are indexed. If pages aren't indexed, they don't appear in search — zero organic traffic.

**Why it happens:**
- Indexing API code was documented (in docs) but never implemented in scheduler
- No automated check for "is this URL indexed in Google?"
- Empty tracking logs mask the problem

**Consequences:**
- New articles may take weeks or months to appear in search
- Orphan pages with no internal links may never get indexed
- AdSense reviewer may find fewer indexed pages than expected

**Warning signs:**
- Search Console shows steep drop in indexed pages vs. published pages
- "site:ayurshakti.shop" returns fewer results than articles published
- Indexing log is still empty after months of running
- Sitemap errors in Search Console

**Prevention:**
1. Implement Google Indexing API notification in the scheduler (use the existing service account that already has Search Console permissions)
2. Add a weekly "index check" script that verifies all published URLs are indexed
3. Fix the empty indexing-log.json to actually record operations
4. Ensure Blogger auto-generated sitemap is submitted to Search Console (it should be, but verify)
5. Add IndexNow integration (Bing's protocol) — it's free and notifies multiple search engines

**Phase:**
- Phase 1 (Fix Automation): Indexing API and sitemap submission
- Phase 2 (SEO Systems): Monitoring and alerting for indexation drops

---

### Pitfall M6: Single Traffic Source Dependency (Putting All Eggs in Google)

**What goes wrong:** The business plan lists multiple sources (Google, Bing, social, AI crawlers), but the reality is the project has:
- Broken social posting (10 articles, zero social distribution)
- No Pinterest traffic (Rich Pins not set up)
- Broken Bing integration (API returning 400/404/405)
- Empty Medium/LinkedIn queue (never processed)

If Google algorithm update hits, there's zero backup traffic.

**Why it happens:**
- Every distribution channel has a technical blocker
- Social posting depends on the scheduler (which is broken)
- Multi-source strategy is planned but not operational

**Consequences:**
- If Google core update de-ranks Ayurveda content, traffic goes to zero
- AdSense review: a site with traffic only from one source looks suspicious
- Bing traffic opportunity is completely missed (significant for Indian health queries)

**Warning signs:**
- GA4 shows 100% traffic from Google, 0% from all other sources
- Bing Webmaster Tools shows zero queries
- Social media accounts have zero outbound clicks to the blog

**Prevention:**
1. Fix social poster for Bluesky and X/Twitter first (lowest effort, already have working API tokens)
2. Fix Pinterest Rich Pins and start pinning (highest ROI traffic source for health/wellness)
3. Fix Bing API integration or use web-based URL submission as fallback
4. Process the pending LinkedIn/Medium queue (browser automation needed)
5. Diversify BEFORE applying for AdSense — a site with traffic from multiple sources is more credible

**Phase:**
- Phase 1 (Fix Automation): Fix social poster, scheduler, Bing
- Phase 4 (Traffic Growth): Monitor and optimize multi-source traffic

---

### Pitfall M7: Using Cookie-Based Auth for Social Media (Security + Reliability Risk)

**What goes wrong:** The project stores browser session cookies for Reddit, Quora, Medium, Pinterest, and X in `secrets/cookies-*.txt` files. Cookie-based authentication breaks every time:
1. The session expires (usually 1-30 days)
2. The user logs out on another device
3. The platform changes its cookie format
4. 2FA is required on next login

**Why it happens:**
- API tokens were not available or required complex OAuth setup
- Quick solution at the time was "export cookies and use them"

**Consequences:**
- Social auto-posting fails silently for weeks before anyone notices
- If cookies leak, attacker gains full account access (no 2FA bypass needed)
- Each cookie refresh requires manual browser work (defeats automation)

**AdSense policy violation:** Not directly, but social accounts compromised could post spam linking to the blog → AdSense account risk.

**Warning signs:**
- Social posting logs show cookie expiry errors
- Scripts fail with "401 Unauthorized" for platforms using cookies
- Cookie files in secrets have dates older than 30 days

**Prevention:**
1. Replace cookie auth with API tokens wherever possible (X/Twitter and Pinterest already migrated — good)
2. For platforms without APIs (Reddit, Quora, Medium), build a browser automation fallback using Puppeteer that re-logs in programmatically or at least detects cookie expiry
3. Add a cookie expiry date tracker in the article registry
4. Document the refresh process so it's not tribal knowledge

**Phase:**
- Phase 1 (Fix Automation): Cookie audit and migration plan
- Phase 5 (Infrastructure): Build cookie health monitoring

---

### Pitfall M8: No ads.txt File

**What goes wrong:** Google AdSense requires an `ads.txt` file in the site root to declare authorized ad sellers. Without it, AdSense may serve limited ads or none at all. Many new Blogger blogs miss this.

**Why it happens:**
- Blogger does not auto-generate ads.txt
- No clear documentation on how to add it to Blogger (it's not straightforward)
- Not required for approval but required for earning

**Consequences:**
- AdSense approved but paying $0 because no ad serving
- Advertisers cannot verify the site is authorized to sell their inventory
- Revenue loss of 100% until fixed

**AdSense policy violation:** YES — mandatory for ad serving (not for approval, but for revenue).

**Warning signs:**
- Visit `ayurshakti.shop/ads.txt` → returns 404 or empty
- AdSense dashboard shows "Ads.txt not found" warning

**Prevention:**
1. Create ads.txt file with content: `google.com, pub-XXXXXXXXXXXXXXXX, DIRECT, f08c47fec0942fa0`
2. In Blogger, go to Settings → Search Preferences → Custom robots.txt and add ads.txt there, OR
3. Use Cloudflare Workers to serve ads.txt at the root URL (since Blogger doesn't support custom files in root)
4. Alternatively, use a Cloudflare Page Rule to rewrite a Blogger page to serve as ads.txt

**Phase:**
- Phase 3 (Pre-AdSense): Set up ads.txt before or immediately after AdSense approval

---

## Minor Pitfalls

### Pitfall m1: No Internal Linking Strategy

**What goes wrong:** Articles are published as standalone pages with no links between related content. This kills topical authority signals and user engagement (readers don't stay on the site).

**Prevention:** Every new article should link to at least 2-3 existing related articles. Add "Related Posts" section at the bottom of each article (Blogger theme may support this via labels).

**Phase:** Phase 1 (Content Pipeline)

---

### Pitfall m2: Image Optimization Ignored (File Size, Alt Text, CDN)

**What goes wrong:** Large, unoptimized images slow page load time. Missing alt text = missed SEO opportunity. Images stored on Blogger's CDN (not Cloudflare) bypass compression.

**Prevention:** Add automated image optimization step: compress to <100KB, add keyword-rich alt text, verify images are served via `resources.ayurshakti.shop` CDN.

**Phase:** Phase 1 (Content Infrastructure)

---

### Pitfall m3: No Content Refresh Strategy

**What goes wrong:** Health information changes. An article about "best ayurvedic remedies for COVID" published in 2026 may contain outdated recommendations. Google favors fresh, updated content.

**Prevention:** After 6 months, articles with declining traffic should be reviewed and updated. Add a "Last updated" date to articles.

**Phase:** Phase 2 (Quality Systems)

---

### Pitfall m4: Overusing Exact-Match Anchor Text in Internal Links

**What goes wrong:** Every internal link uses exact-match keywords ("giloy benefits for immunity"). This looks manipulative to Google's link analysis algorithms.

**Prevention:** Vary anchor text: use partial matches, "click here for more," "this article explains," and natural phrases.

**Phase:** Phase 1 (Content Pipeline)

---

### Pitfall m5: Relying Solely on Blogger's Built-In SEO

**What goes wrong:** Blogger's built-in SEO features are basic — no meta description control on homepage, limited Open Graph control, no canonical URL management, no breadcrumb schema without custom theme editing.

**Prevention:** Verify the custom theme already handles: custom meta descriptions, OG tags (confirmed in PROJECT.md ✓), JSON-LD schema (confirmed ✓), breadcrumb markup.

**Phase:** Phase 1 (Content Infrastructure)

---

### Pitfall m6: Publishing Without Running the 10/10 Checklist

**What goes wrong:** The 10/10 pre-publish checklist exists in docs but is enforced only by manual inspection. An AI agent can incorrectly set `checklist_10_10: true` without actually verifying. Articles slip through without images, FAQ, schema, or proper word count.

**Prevention:** Build a `verify_checklist.py` script that programmatically checks each of the 10 conditions against the article HTML before adding to the approval queue.

**Phase:** Phase 2 (Quality Systems)

---

### Pitfall m7: Logging Without Rotation (Disk Space Death)

**What goes wrong:** `scheduler-run.log` and `scheduler-cron.log` grow indefinitely. On a cloud VM or server, this fills disk and kills the automation entirely.

**Prevention:** Implement `logrotate` or `RotatingFileHandler` with 5MB max per file, keep last 5 rotations.

**Phase:** Phase 5 (Infrastructure)

---

### Pitfall m8: Applying for AdSense Too Many Times in Rapid Succession

**What goes wrong:** Each rejection resets the review timer. Reapplying within 2 weeks guarantees another rejection. Multiple rapid applications can get the domain flagged as "problematic."

**Prevention:** After rejection, wait minimum 15-30 days. Fix ALL issues from the rejection email. Do NOT reapply more than 3 times in 6 months.

**Phase:** Phase 3 (AdSense Application Strategy)

---

## Phase-Specific Warnings

| Phase | Topic | Likely Pitfall | Severity | Mitigation |
|-------|-------|---------------|----------|------------|
| Phase 0: Foundation | Theme setup, legal pages | Missing medical disclaimer, no Privacy Policy | Critical | Create all 5 legal pages before any content goes live |
| Phase 1: Fix Automation | Scheduler, social poster, image paths | Broken pipeline publishes 0 articles; social backlog persists | Critical | Fix post ID bug first; add dry-run mode; test manually for 1 week |
| Phase 1: Content Pipeline | AI article generation | Generic AI patterns that E-E-A-T reviewers flag | Critical | Mandate human editing gate; add unique examples to every article |
| Phase 2: Quality Systems | 10/10 checklist, content audit | Checklist bypassed, thin articles slip through | Moderate | Build programmatic validator; reject articles that fail automated checks |
| Phase 3: AdSense Application | Applying for approval | Applying with <20 articles, no disclaimers, no author attribution | Critical | Enforce hard min-20-article gate; run full E-E-A-T audit first |
| Phase 3: AdSense Application | Ad placement | Ads near navigation buttons = accidental clicks | Critical | Follow AdSense ad placement policies: not above fold too aggressively |
| Phase 4: Traffic Growth | Pinterest, social distribution | Pinterest spamming without SEO, cookie expiry kills auto-posting | Moderate | Set up Rich Pins, keyword-optimize pin descriptions, monitor cookie health |
| Phase 5: Infrastructure | Logging, monitoring, secrets | Logs fill disk; credential drift; no audit trail | Minor | Log rotation, credential expiry alerts, status dashboard |
| Ongoing | Content freshness | 6-month-old health articles with no updates | Moderate | Scheduled quarterly content audit and refresh |

---

## AdSense Policy Violation Risk Matrix

| Issue | Policy Violated | Risk Level | Likelihood |
|-------|----------------|------------|------------|
| No medical disclaimer | Harmful health content (Policy 8) | **Critical** | HIGH — almost certain rejection |
| Unedited AI content | Low-value content / Spammy auto-generated | **Critical** | HIGH — detectable pattern in 2026 |
| No Privacy Policy | Missing required policy pages (Policy 1) | **Critical** | HIGH — instant rejection |
| No author attribution | Insufficient E-E-A-T signals (Policy 8) | **Critical** | HIGH — especially for YMYL health |
| Article <800 words | Thin content (Policy 8) | **High** | MEDIUM — if multiple thin posts exist |
| No Contact/About | Site transparency (Policy 9) | **High** | MEDIUM-HIGH — missing trust signals |
| Broken navigation/404s | Site architecture (Policy 6) | **Medium** | LOW — minor, but adds up |
| No ads.txt | Missing ads.txt | **Medium** | LOW — blocks revenue, not approval |
| Clicking own ads | Invalid traffic (Policy 3) | **Critical** | LOW — team knows not to do this |

---

## Key Numbers Summary

| Metric | Minimum for AdSense | Target for Revenue |
|--------|-------------------|-------------------|
| Published articles | 15-20 | 50+ |
| Words per article | 800-1000 | 1500-2500 |
| Monthly pageviews | None required | 10,000+ |
| RPM (health niche US traffic) | — | $5-15 |
| RPM (health niche India traffic) | — | $0.50-2 |
| Site age before applying | 1-2 months | 3-6 months |
| Author credentials | Named author with bio | Reviewed by qualified practitioner |
| Legal pages | 4 (Privacy, About, Contact, Terms) | 5 (add Medical Disclaimer) |
| Article images | 1 per article minimum | 3-5 optimized images per article |
| Internal links per article | 0 (no requirement) | 2-3 minimum |
| Pinterest pins per week | 0 | 15-30 |

---

## Sources

- Google AdSense Program Policies (2026) — support.google.com/adsense
- Multiple 2026 AdSense approval/rejection guides across blogs and platforms (Medium, BlogerHub, SahilDubey, Webtimize, HikeWeb, GuideX, Bloggerscope)
- YMYL & E-E-A-T guidance from Search Engine Land, AdSense Audit, Koantic, TheStacc
- AI content policy clarifications from ProAICraft, AdSense Audit, TheHumanizeAI
- Pinterest SEO 2026 guides from BloggersPassion, TheSocialSkinny, Pingroupie, BloggingExplorer
- Project-specific findings from CONCERNS.md and PROJECT.md audits

**Confidence notes:** Stack-level pitfalls (E-E-A-T, Privacy Policy, AI detection) are HIGH confidence — consistently reported across all 2026 sources. Traffic growth pitfalls (Pinterest specifics, platform limitations) are MEDIUM confidence — platform-specific, but the general principles are well-established. Blogger-specific quirks (ads.txt workaround, author attribution limits) are MEDIUM confidence — platform-specific knowledge from Blogger blogs.
