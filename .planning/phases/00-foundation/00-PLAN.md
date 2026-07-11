---
phase: 00-foundation
plan: 00
type: execute
wave: 1
depends_on: []
files_modified:
  - theme-and-logo/ayurshakti-main.xml (pre-modified by researcher)
  - scripts/ads-worker.js (pre-created by researcher)
  - No local files created in remaining work — all changes via Blogger dashboard and Cloudflare dashboard
autonomous: false
requirements:
  - R-001
  - R-002
  - R-003
  - R-004
  - R-005
  - R-006
  - R-007
  - R-008
  - R-009
  - R-010
  - R-011
  - R-012
  - R-013
  - R-014
  - R-015
user_setup: []

must_haves:
  truths:
    - "Visitor can read full About Us page with named author (Suresh Bhati) and credentials"
    - "Visitor can see Medical Disclaimer, Terms of Service, Contact Us, and Privacy Policy linked in footer — all pointing to correct URLs"
    - "Every health article shows a standardized medical disclaimer auto-footer and author bio box"
    - "Every health article shows 'Updated: Month dd, yyyy' when last-updated differs from publish date"
    - "No article contains definitive medical claims (cures, treats, prevents) — all use 'may help'/'traditionally used' language"
    - "ads.txt returns valid content at ayurshakti.shop/ads.txt"
    - "PageSpeed scores >80 on mobile and desktop"
    - "HTTPS active, mobile-responsive confirmed, GA4 + GSC verified as working"
    - "Comments are moderated (not disabled) with moderation policy message"
  artifacts:
    - path: "theme-and-logo/ayurshakti-main.xml"
      provides: "Theme with medical disclaimer auto-footer, author bio box, last-updated date, fixed footer links"
      min_lines: 5000
      contains: "medical-disclaimer"
    - path: "scripts/ads-worker.js"
      provides: "Cloudflare Worker script for ads.txt serving"
      min_lines: 15
      contains: "adsTxtContent"
    - path: "https://www.ayurshakti.shop/p/about-us.html"
      provides: "About Us page with Suresh Bhati author credentials"
    - path: "https://www.ayurshakti.shop/p/privacy-policy.html"
      provides: "Privacy Policy with AI crawler section and correct contact email"
    - path: "https://www.ayurshakti.shop/ads.txt"
      provides: "ads.txt content served via Cloudflare Worker"
    - path: "Live articles (12)"
      provides: "All 12 articles rewritten with safe medical language"
  key_links:
    - from: "Theme XML footer"
      to: "Legal pages"
      via: "Footer Page List gadget links to About, Contact, Disclaimer, Terms, Privacy"
      pattern: "pages/p/"
    - from: "Theme XML postFooter"
      to: "/p/disclaimer.html"
      via: "Medical disclaimer auto-footer includes link to full disclaimer"
      pattern: "disclaimer\\.html"
    - from: "Cloudflare Worker ads-txt"
      to: "ayurshakti.shop/ads.txt"
      via: "Worker route serves ads.txt at root path"
      pattern: "ads\\.txt"

---

<objective>
Complete all remaining Phase 0 Foundation work: legal page content (About Us, Privacy Policy), author profile setup, technical verification (PageSpeed, GA4/GSC, ads.txt deploy, mobile responsiveness, HTTPS), and article medical claim audit.

The researcher already completed theme XML modifications (medical disclaimer auto-footer, last-updated date, author bio box, footer URL fix) and created the ads-worker.js script. This plan covers everything else.

Purpose: Ensure site meets AdSense YMYL prerequisites — legal compliance, medical disclaimers on all content, named author attribution, technical baseline verified.
Output: All 15 requirements verified as complete. Phase 0 passes to Phase 1.
</objective>

<execution_context>
@/home/shiva/.config/opencode/gsd-core/workflows/execute-plan.md
@/home/shiva/.config/opencode/gsd-core/templates/summary.md
</execution_context>

<context>
@.planning/PROJECT.md
@.planning/ROADMAP.md
@.planning/STATE.md
@.planning/phases/00-foundation/00-RESEARCH.md
@config/profile.json
</context>

<notes>
## Pre-Completed Items (Researcher already committed)

| # | Requirement | Status | Evidence |
|---|-------------|--------|----------|
| R-006 | Link ALL legal pages in footer | ✅ DONE | Footer bug fixed — Disclaimer URL corrected to `/p/disclaimer.html`, duplicate removed. Committed in `ayurshakti-main.xml`. |
| R-007 | Medical disclaimer auto-footer in theme | ✅ DONE | `<div class='medical-disclaimer'>` added to `postFooter` includable with CSS variables. Committed in theme XML. |
| R-008 | "Consult healthcare provider" auto-footer | ✅ DONE | Combined with R-007 — disclaimer text includes "Always consult a qualified healthcare provider." |
| R-011 | Last-updated date visible on articles | ✅ DONE | `<span class='updated'>` added in `postHeader` showing "Updated: Month dd, yyyy" when `lastUpdated != date`. Committed in theme XML. |
| R-014 | ads.txt script created | ✅ SCRIPT EXISTS | `scripts/ads-worker.js` created with placeholder Pub-XXXX ID. DEPLOYMENT still needed (Task 2). |

## Implementation Notes

- **All work is dashboard-based** — Blogger Dashboard (pages, posts, settings, profile) and Cloudflare Dashboard (Workers & Pages). No local file modifications beyond what's already committed.
- **Authentication expected** — Agent uses browser (browser_puppeteer) to log into Blogger (google.com) and Cloudflare. Auth gates created dynamically if login fails.
- **Author info** — Suresh Bhati, contact@ayurshakti.shop. Full details in `config/profile.json`.
- **Blogger ID**: 5016036252143286656
- **Published articles**: 12 confirmed (per STATE.md, may be 11 per RESEARCH.md — verify count in Task 3)
</notes>

<tasks>

<task type="auto" tdd="false">
  <name>Task 1: Legal Pages Content Update & Author Profile Setup</name>
  <files>No local files — all changes via Blogger Dashboard (Pages, Settings → User Profile)</files>
  <action>
    Perform the following in order using the Blogger Dashboard via browser:

    1. **Update About Us page** (R-001):
       - Navigate to Blogger Dashboard → Pages → Edit "About Us" page
       - Replace content with the full revision draft from RESEARCH.md section 1.1
       - Key changes: Replace "The AyurShakti Team" with named author **Suresh Bhati**
       - Include author bio, credentials, professional background, mission statement
       - Add author photo if available (use the existing About Us page layout)
       - Use exact bio text from `config/profile.json` author.bio field as base

    2. **Update Privacy Policy** (R-005):
       - Navigate to Blogger Dashboard → Pages → Edit "Privacy Policy" page
       - Add Section 8: AI Crawlers and Data Processing (use template from RESEARCH.md Code Example 6)
       - Change contact email from `admin@ayurshakti.shop` to `contact@ayurshakti.shop`
       - Remove or clarify Amazon Associates reference (per D-05 recommendation: remove until affiliate program is active)
       - Add GDPR cookie consent placeholder note
       - Re-number sections if necessary after additions
       - Preserve all existing content about AdSense cookies, data collection, GA4

    3. **Set author bio in Blogger profile** (R-010):
       - Navigate to Blogger Dashboard → Settings → User Profile
       - Set "Display name" to **Suresh Bhati**
       - Paste the "Introduction" (About Me) bio from RESEARCH.md section 2.2:
         > Suresh Bhati is the founder of AyurShakti, an Ayurveda and pet wellness resource. With years of personal research into Ayurvedic remedies and a passion for holistic health for both humans and animals, Suresh shares evidence-informed guides on herbs, natural remedies, and traditional wellness practices. Every article is researched using peer-reviewed studies and Ayurvedic classical texts.
       - Save profile
       - IMPORTANT: The theme's `aboutPostAuthor` includable (already in theme) renders the author box only when `data:post.author.aboutMe` is non-empty — this step activates it

    4. **Verify existing legal pages** (R-002, R-003, R-004):
       - Navigate to Blogger Dashboard → Pages and confirm these exist:
         - Contact Us at `/p/contact-us.html` — verify uses `contact@ayurshakti.shop`
         - Medical Disclaimer at `/p/disclaimer.html` — verify content is adequate per RESEARCH.md 1.3
         - Terms of Service at `/p/terms-conditions.html` — verify content is adequate per RESEARCH.md 1.4
       - If any page is missing or deficient, create/update it
       - Confirm Cloudflare Email Routing for contact@ is active per PROJECT.md
  </action>
  <acceptance_criteria>
    - About Us page displays Suresh Bhati as named author with credentials
    - Privacy Policy has Section 8 on AI crawlers, correct contact email, Amazon reference removed
    - Blogger profile has "Introduction" bio text filled — author bio box renders on article pages
    - Contact Us, Medical Disclaimer, Terms of Service pages exist and are adequate
    - Cloudflare Email Routing functional for contact@
  </acceptance_criteria>
  <verify>
    <automated>MISSING — dashboard work; manual verification required. Open each live page and verify content.</automated>
    <human-check>
      1. Visit https://www.ayurshakti.shop/p/about-us.html — confirm author name "Suresh Bhati" visible
      2. Visit https://www.ayurshakti.shop/p/privacy-policy.html — confirm Section 8 (AI Crawlers) exists
      3. Visit any article (e.g., https://www.ayurshakti.shop/) — scroll to bottom, confirm author bio box appears
      4. Visit https://www.ayurshakti.shop/p/disclaimer.html — confirm loads correctly
      5. Visit https://www.ayurshakti.shop/p/terms-conditions.html — confirm loads correctly
      6. Visit https://www.ayurshakti.shop/p/contact-us.html — confirm contact@ email shown
    </human-check>
  </verify>
  <done>
    All 5 legal pages verified live with correct content. Author bio box renders on article pages. Privacy Policy includes AI crawler section. Contact email consistent across pages.
  </done>
</task>

<task type="auto" tdd="false">
  <name>Task 2: Technical Verification & Infrastructure</name>
  <files>No local files — changes via Cloudflare Dashboard, PageSpeed Insights, and Blogger Settings</files>
  <action>
    Perform the following using the Cloudflare Dashboard, browser, and Blogger Settings:

    1. **Deploy ads.txt Cloudflare Worker** (R-014):
       - Navigate to Cloudflare Dashboard → Workers & Pages → Create Application → Create Worker
       - Name: `ayurshakti-ads-txt`
       - Use existing code from `scripts/ads-worker.js` — paste the full content
       - Save and Deploy
       - Verify Worker deployed successfully (copy the workers.dev URL and test it)
       - Go to your domain → Workers → Add Route:
         - Route: `ayurshakti.shop/ads.txt`
         - Worker: `ayurshakti-ads-txt`
       - Verify: visit `https://ayurshakti.shop/ads.txt` — should return `google.com, pub-XXXXXXXXXXXXXXXX, DIRECT, f08c47fec0942fa0`
       - Note: The pub-XXXX ID is a placeholder. This is acceptable per RESEARCH.md — AdSense does not require ads.txt for approval, only for earning. Replace after Phase 6.

    2. **Verify HTTPS** (R-012):
       - Visit `https://www.ayurshakti.shop` — confirm padlock icon, valid certificate
       - Check Cloudflare SSL/TLS → Edge Certificates → Always Use HTTPS: should be ON
       - Verify `http://` redirects to `https://`

    3. **Run PageSpeed Insights** (R-012):
       - Visit `https://pagespeed.web.dev/` and run tests on 3-5 article URLs
       - Test both mobile and desktop for each URL
       - Document scores. Target: >80 on both mobile and desktop
       - If any score is <80, apply fixes in order:
         a. Compress hero images to <100KB, use WebP
         b. Ensure image dimensions set in HTML (width/height)
         c. Check Cloudflare caching settings (TTFB should be <200ms via CDN)
       - Re-test after fixes

    4. **Mobile responsiveness check** (R-012):
       - Use Google Mobile-Friendly Test: `https://search.google.com/test/mobile-friendly`
       - Or use browser dev tools: resize to 375px width and check navigation, images, text reflow
       - Document any issues found

    5. **Verify GA4 + Google Search Console** (R-013):
       - Open GA4 dashboard → Realtime report → visit site → confirm 1 active user appears
       - Open Google Search Console → confirm property verified for ayurshakti.shop
       - Check for crawl errors
       - Verify sitemap is submitted (atom.xml is the Blogger sitemap)
       - Document findings

    6. **Configure comment moderation** (R-015):
       - Navigate to Blogger Dashboard → Settings → Posts, comments and sharing
       - Set Comment Moderation: **Always**
       - Set Who can comment: **Registered users only**
       - Comment location: Embedded (keep current)
       - Paste moderation policy message:
         > Comments are moderated. No medical advice will be provided in comments. Please consult a qualified healthcare provider for personal health concerns.
       - Enable backlinks moderation
       - Do NOT disable comments entirely — moderation preserves reader engagement while preventing spam/liability
  </action>
  <acceptance_criteria>
    - ads.txt returns content at ayurshakti.shop/ads.txt
    - HTTPS confirmed active with valid certificate
    - PageSpeed scores >80 on mobile and desktop (or fixes attempted)
    - Mobile-friendly confirmed
    - GA4 realtime shows active visit when testing
    - Search Console property verified
    - Comments set to "Always" moderation with policy message
  </acceptance_criteria>
  <verify>
    <automated>MISSING — dashboard/site verification; browser checks required.</automated>
    <human-check>
      1. Visit https://ayurshakti.shop/ads.txt — confirm text/plain response with "google.com" content
      2. Visit https://www.ayurshakti.shop — confirm padlock icon (HTTPS)
      3. Check PageSpeed results documented (scores and any fixes applied)
      4. Resize browser to 375px — confirm site is mobile-friendly
      5. Open GA4 Realtime report — confirm activity shows when visiting site
      6. Open Blogger Settings → Posts, comments — confirm moderation is "Always"
    </human-check>
  </verify>
  <done>
    ads.txt deployed and verified. HTTPS confirmed. PageSpeed >80 on mobile + desktop. Mobile-responsive confirmed. GA4 and GSC verified as working. Comment moderation configured.
  </done>
</task>

<task type="auto" tdd="false" effort="high">
  <name>Task 3: Article Medical Claim Audit & Rewrite</name>
  <files>No local files — all article edits in Blogger Dashboard → Posts</files>
  <action>
    Audit ALL 12 published articles for definitive medical claims. This is the most critical YMYL compliance task. Follow this protocol:

    **Step 1: Inventory articles**
    - Navigate to Blogger Dashboard → Posts
    - Count published articles (verify the exact number — RESEARCH.md says 11, STATE.md says 12)
    - List all published article titles and URLs

    **Step 2: For each article, scan for forbidden patterns**

    Use the regex patterns from RESEARCH.md Code Example 5 as search terms. For each match, evaluate context:

    | Search Pattern | Context is OK (keep) | Context is NOT OK (rewrite) |
    |---|---|---|
    | `\bcures?\b` | "Studies suggest curcumin may help..." | "Giloy cures fever" |
    | `\btreats?\b` | "Traditionally used to treat..." | "This herb treats arthritis" |
    | `\bprevents?\b` | "May support immune function" | "Prevents recurring fevers" |
    | `\beliminates?\b` | — | "Eliminates toxins from body" |
    | `\breverses?\b` | — | "Reverses liver damage" |
    | `\bguarantees?\b` | — | "Guaranteed results" |
    | `\bmiracles?\b` | — | "Miracle cure for..." |
    | `\bclinically\s*proven\b` | — | "Clinically proven to work" |
    | `\binstant\b` (relief) | — | "Instant relief from..." |
    | `\bdestroys?\b` (cancer/bacteria) | "lab study showed..." | "Destroys cancer cells" |
    | `\bheals?\b` (definitive) | "May help heal..." | "Heals wounds completely" |

    **Step 3: Rewrite protocol**
    - For each definitive claim found, rewrite using safe language:
      - "cures" → "may help manage"
      - "treats" (definitive) → "traditionally used for"
      - "prevents" (definitive) → "may support"
      - "eliminates" → "may help reduce"
      - "reverses" → "may support"
      - "clinically proven" → "studies suggest"
      - "instant" → "gradual" or remove
    - Keep factual statements about study results ("A 2023 study found that...")
    - Keep traditional use descriptions ("In Ayurveda, this herb is traditionally used for...")
    - Add qualifying phrases: "may help", "traditionally used", "studies suggest", "some research indicates"

    **Step 4: Key article to prioritize**
    - **Giloy Benefits for Immunity** — RESEARCH.md specifically flags this article for definitive language like "prevents recurring fevers" and "Giloy activates macrophages"

    **Step 5: Apply changes**
    - For each article with issues: edit in Blogger editor → make changes → Update (do NOT change publish date unless needed)
    - The "Updated" date will auto-show on the article now that the theme has last-updated date support

    **Step 6: Final check**
    - After all rewrites: spot-check 3-5 articles by re-reading to ensure no remaining definitive claims
    - Verify the medical disclaimer auto-footer and author bio box render correctly on each checked article
  </action>
  <acceptance_criteria>
    - All 12 articles audited for definitive medical claims
    - Every instance of "cures"/"treats"/"prevents" (used definitively) rewritten to "may help"/"traditionally used"/"studies suggest"
    - Giloy article specifically fixed (known to have definitive language per research)
    - No article contains a claim that could trigger an AdSense policy violation
    - Articles retain their factual content, study citations, and traditional use descriptions — only definitive efficacy language is softened
  </acceptance_criteria>
  <verify>
    <automated>MISSING — manual content audit; no automated test available for language compliance.</automated>
    <human-check>
      1. Spot-check 3-5 articles on the live site — confirm no "cures", "treats (definitively)", "prevents" language remains
      2. Confirm medical disclaimer auto-footer appears at bottom of each checked article
      3. Confirm author bio box (Suresh Bhati) appears at bottom of each checked article
      4. Confirm "Updated:" date appears on any recently-modified articles
    </human-check>
  </verify>
  <done>
    All 12 articles rewritten to use safe medical language (may help / traditionally used / studies suggest). No definitive medical claims remain. Medical disclaimer and author bio appear on every article.
  </done>
</task>

</tasks>

<threat_model>
## Trust Boundaries

No code is written in this phase. All work is content editing (Blogger pages/articles) and configuration (Cloudflare Worker, Blogger settings). Security enforcement is `false` per RESEARCH.md. No STRIDE analysis applicable.

The only security-sensitive action is the ads.txt Worker — it must only serve `/ads.txt` and not expose internal paths. The worker code (already created by researcher) restricts to exact `/ads.txt` path and returns 404 for everything else.
</threat_model>

<verification>
## Phase 0 Verification Checklist

After all 3 tasks complete, verify end-to-end:

### Legal Pages
- [ ] About Us: named author (Suresh Bhati) with credentials visible
- [ ] Contact Us: uses contact@ayurshakti.shop, Cloudflare Email Routing functional
- [ ] Medical Disclaimer: adequate content, linked from footer
- [ ] Terms of Service: adequate content, linked from footer
- [ ] Privacy Policy: includes AI crawlers Section 8, contact@ email, Amazon reference removed

### Footer
- [ ] All 5 pages linked in footer with correct URLs (privacy-policy.html, disclaimer.html, terms-conditions.html, about-us.html, contact-us.html)
- [ ] No duplicate entries
- [ ] No broken links

### Theme Modifications (pre-committed by researcher — verify live)
- [ ] Medical disclaimer auto-footer renders on every single-post article
- [ ] Author bio box (Suresh Bhati) renders on every article
- [ ] "Updated: Month dd, yyyy" shows when lastUpdated differs from publish date

### Technical
- [ ] ads.txt returns content at ayurshakti.shop/ads.txt
- [ ] HTTPS active (padlock icon)
- [ ] PageSpeed >80 on mobile AND desktop
- [ ] Mobile-friendly (375px test passes)
- [ ] GA4 Realtime shows activity
- [ ] Google Search Console property verified, no crawl errors

### Content
- [ ] All 12 articles audited and rewritten — no "cures", "treats", "prevents" claims
- [ ] Giloy article specifically fixed
- [ ] Comments set to "Always" moderation with policy message

### Blogging
- [ ] Comment moderation: Always
- [ ] Who can comment: Registered users only
- [ ] Moderator policy message: live
</verification>

<success_criteria>
1. All 15 requirements (R-001 through R-015) verified as complete
2. Site meets AdSense YMYL prerequisites — legal pages, medical disclaimers, author attribution, no definitive claims
3. Phase 0 ready to pass to Phase 1 (Automation Fix)
</success_criteria>

<output>
Create `.planning/phases/00-foundation/00-SUMMARY.md` when done
</output>
