# Topic Research Rule — AyurShakti.shop

> **OpenCode Required Skills:**
> Before executing tasks in this document, load the following skills from the OpenCode library (Home Directory):
> - `seo-aeo-keyword-research`
> - `seo-content-planner`
> - `seo-keyword-strategist`
> - `seo-aeo-content-cluster`
> - `deep-research`
> - `competitive-landscape`

## Purpose
AI agent ke liye topic research ka master rule. Jab bhi naye article topics suggest karne honge, yeh file AI ko guide karegi ki KAISE research karna hai, KISKE liye karna hai, aur KYA rules follow karne hain. Baar-baar instructions repeat nahi karne padenge.

---

## 0. Multi-Platform Algorithm Pre-Flight Check (Auto-Adjust — Run Before Every Session)

Yeh step HAR session start pe run karo, Section 1 jane se pehle. Multiple platforms check karo — Google, Bing, AI Search (ChatGPT/Perplexity/Gemini), AI crawlers. Agar kisi platform ne policy/algorithm change kiya hai toh strategy auto-adjust ho jayegi.

### A. Check ALL Platform Updates (Automated)
```websearch queries — agent run karega:

# Google
1. "Google algorithm update 2026 [current month]"
2. "Google helpful content update 2026"
3. "Google AI content policy 2026"
4. "Google SEO ranking factors 2026"
5. "Google spam update 2026"
6. "Google core update 2026"

# Bing & ChatGPT Search
7. "Bing Webmaster update 2026"
8. "Bing indexation policy 2026"
9. "ChatGPT Search update 2026 publisher policy"

# AI Search (Perplexity / Gemini)
10. "Perplexity AI source freshness update 2026"
11. "Google AI Overviews citation update 2026"
12. "Gemini AI citation policy 2026"

# AI Crawlers & LLM Access
13. "AI crawler robots.txt policy 2026"
14. "ChatGPT crawler GPTBot update 2026"
15. "Google-Extended crawler update 2026"
```

### B. Auto-Adjust Strategy Per Platform

| Update Detected | Auto-Adjustment in Topic Research |
|----------------|-----------------------------------|
| **Google Helpful Content** | KD filter → < 20 only (was < 25). Min volume → 1000/mo (was 500). Avoid "thin" topics. Prefer pillar content only |
| **Google Spam Update** | Reduce daily cadence by 50% temporarily. Increase human touch pass. Manual review mandatory for each topic |
| **Google Core Update** | **PAUSE** topic research for 3-5 days. Run audit on existing content first. Resume only after volatility subsides |
| **Google AI Overviews** | Prioritize topics with question-based intent ("how", "what is", "why"). Add AEO-focused research. Boost FAQ schema topics |
| **Google E-E-A-T Update** | Only research topics where you can cite PubMed/NIH sources (min 2 citations per topic). Author bio verification needed |
| **Bing Index Update** | Bing Webmaster connected. API key in `secrets/bing-client-credentials.json`. Auto-submit via `scripts/bing-sitemap-submit.py`. Bing has lower KD tolerance — adjust KD filter to < 20 for Bing-targeted topics |
| **ChatGPT Search Policy** | Priority to listicle-format topics (43.8% of ChatGPT citations are listicles). Add question-based intent filter. Ensure clean HTML structure |
| **Perplexity Freshness Change** | Only research topics that can be updated monthly. Remove topics that can't be refreshed. Perplexity favors recent content |
| **AI Crawler Policy Change** | Verify robots.txt allows GPTBot + Claude-Web + Google-Extended. Add llms.txt requirement to topic briefs |
| **No update found** | Proceed with standard filters from Section 5 |

### C. Auto-Adjust Implementation

```
IF any platform update found:
  → agent applies modified thresholds immediately
  → Section 5 filters run with platform-adjusted values
  → Section 6 checklist runs with adjusted criteria
  → User notified: "⚠️ [Platform] update detected. Filters adjusted: [specific changes]"

IF no update across all platforms:
  → "✅ No platform updates detected. Proceeding with standard multi-platform filters."
```

### D. Platform Monitoring Log

Har session ke end mein platform status log karo:

```
Platform Status Log — [Date]
├─ Google: ✅ No updates | Updates: [list] | Adjustments: [list]
├─ Bing: ✅ No updates | Updates: [list] | Adjustments: [list]
├─ AI Search (ChatGPT/Perplexity): ✅ Stable | Changes: [list]
├─ AI Crawlers: ✅ All allowed | Blocked: [list]
└─ Action: [Proceed / Pause / Adjust filters]
```

---

| Priority | Country | AdSense RPM | Reason |
|----------|---------|-------------|--------|
| 1 | USA | $15-50 | Highest CPC, max revenue |
| 2 | UK | $10-35 | High CPC, English audience |
| 3 | Canada | $8-25 | Good CPC, English audience |
| 4 | Australia | $8-25 | Good CPC, English audience |
| 5 | New Zealand | $6-18 | Decent CPC |
| 6 | India | $0.5-2 | Volume play only (high search, low CPC) |

**Rule:** Pehle USA/UK/CA/AU ke liye topics filter karo. India sirf tab jab volume bahut zyada ho (10K+/mo) aur content Hindi/regional na ho.

---

## 2. Website Coverage (Categories)

AyurShakti.shop covers **Humans + Pets** dono:

### Human Health (Ayurveda)
- Herbs & Supplements — Ashwagandha, Giloy, Amla, Shilajit, Tulsi, Triphala, Moringa, Bhringraj, Neem, Turmeric, Shatavari, Brahmi, Safed Musli, Gokshura, etc.
- Men's Health — Testosterone, libido, sperm count, ED, premature ejaculation, bodybuilding naturally
- Women's Health — PCOS, PCOD, menstrual health, fertility, pregnancy, menopause, hormonal balance, Shatavari
- Hair Care — Hair fall, hair growth, dandruff, premature gray hair, hair oil DIY, Ayurvedic hair treatment
- Skin Care — Glowing skin, acne, pigmentation, anti-aging, face packs, Ayurvedic skincare routine
- Weight Loss — Belly fat, metabolism boost, Ayurvedic diet, Triphala for weight loss, dosha-based diet
- Digestion & Gut Health — Constipation, gas, bloating, acidity, IBS, Agni (digestive fire), Triphala
- Immunity & Detox — Immunity boosters, Chyawanprash, detox at home, Panchakarma basics
- Sleep & Stress — Insomnia, anxiety, stress relief, Brahmi for brain, Ashwagandha for stress
- Diabetes & Blood Sugar — Natural blood sugar control, Ayurvedic diabetes management
- Joint Health — Arthritis pain, joint inflammation, natural remedies
- Thyroid — Hypothyroidism, hyperthyroidism, natural management
- Heart Health — BP, cholesterol, Ayurvedic heart care
- Respiratory — Asthma, cough, cold, lung health, Tulsi, Giloy

### Pet Health
- **Dogs:** Ayurvedic herbs for dogs, homemade dog food, turmeric for dogs, coconut oil for dogs, Triphala for dogs, anxiety in dogs, joint health, skin problems, digestion
- **Cats:** Ayurvedic remedies for cats, homemade cat food, flea treatment, hairballs, anxiety, kidney support, skin problems, digestion

---

## 3. Skills to Load (from skill-library/)

Jab bhi topic research ka task aaye, yeh skills load karo:

### Primary (Topic & Keyword Research)
| Skill | Purpose |
|-------|---------|
| `seo-aeo-keyword-research` | Keyword research with AEO question queries, difficulty tiers |
| `seo-keyword-strategist` | Keyword density, LSI keywords, semantic optimization |
| `seo-content-planner` | Content outlines, topic clusters, calendar planning |
| `seo-aeo-content-cluster` | Topical authority mapping, pillar + cluster structure |

### Secondary (Strategy & Analysis)
| Skill | Purpose |
|-------|---------|
| `content-strategy` | Full content strategy framework, buyer stage mapping |
| `competitive-landscape` | Competitor gap analysis, differentiation |
| `efficient-web-research` | Token-efficient web research protocol |
| `deep-research` | Autonomous deep research for trending topics |

### Tertiary (Writing & Optimization)
| Skill | Purpose |
|-------|---------|
| `ai-seo` | AI search (LLM/AEO) optimization |
| `programmatic-seo` | Scaled content generation patterns |
| `blog-writing-guide` | Blog writing structure & formatting |
| `copywriting` | Persuasive copy angles |
| `marketing-psychology` | Psychological triggers for topics (dual path: `.agents/skills/` + `skill-library/`) |

### Utilities
| Skill | Purpose |
|-------|---------|
| `seo-technical` | Technical SEO audit if needed |
| `seo-aeo-content-quality-auditor` | Content quality check |
| `seo-cannibalization-detector` | Keyword cannibalization check |
| `keyword-extractor` | Extract keywords from competitor content |
| `seo-content-refresher` | Refresh outdated content |

**Usage:** Agent apne aap in skills ko load karega jab topic research ka task detect hoga.

---

## 4. Tools to Use

### Web Research Tools
| Tool | When to Use |
|------|-------------|
| `websearch` | Primary tool for topic discovery, trend spotting, volume estimation |
| `webfetch` | Fetch competitor content, Google SERP analysis, source validation |
| `browser_puppeteer_navigate` | Browse competitor sites, Google Trends, Reddit/Quora threads |
| `browser_puppeteer_screenshot` | Capture competitor page structure, SERP screenshots |
| `browser_puppeteer_evaluate` | Extract page text content when webfetch fails |

### AI Agent Tools
| Tool | When to Use |
|------|-------------|
| `skill` | Load relevant skills from skill-library/ |
| `task` | Deploy subagents for parallel research (e.g., 5 topics at once) |
| `question` | Ask user for clarification if rules are ambiguous |

### Codebase Tools
| Tool | When to Use |
|------|-------------|
| `glob` | Find existing content files matching a topic |
| `grep` | Check if a topic already exists in content |
| `read` | Read existing articles to avoid duplication |
| `bash` | Run npm/node/Python scripts for automation |

---

## 5. Keyword Filters (Strict Rules)

Every topic candidate MUST pass these filters:

### A. Competition Filter
- **Keyword Difficulty (KD):** < 25 (MUST)
  - KD < 20 — Premium (direct target, high chance to rank)
  - KD 20-30 — Good (needs strong content, doable)
  - KD 30-40 — Borderline (only if angle is unique & existing content is weak)
  - KD > 40 — SKIP (waste of resources)
- **SERP Analysis:** Top 10 results mein koi high-DR site (80+) na ho
- **Backlink Gap:** Top ranking pages mein 50+ unique domains nahi hone chahiye
- **Content Gap:** Top 5 results thin/weak content ho toh best

### B. Volume Filter
- **Minimum Volume:** 500 searches/month
- **Target Volume:** 1,500 — 15,000 searches/month
- **Sweet Spot:** 2,000 — 8,000/month with KD < 20
- **Avoid:** Volume < 200 (waste of time) ya > 50,000 (too competitive)

### C. CPC Filter
- **Minimum CPC:** $2.00 (US market)
- **Target CPC:** $5.00 — $30.00
- **Low CPC tolerance:** Sirf tab allow karo jab volume > 10,000/month ho
- **Check:** Google Ads CPC data use karo, keyword planner ya Ahrefs/SEMrush alternatives

### D. Per-Platform KD / Volume Thresholds

2026 mein traffic sirf Google se nahi aata. Har platform ka apna difficulty metric hota hai:

| Platform | KD Threshold | Volume Min | Notes |
|----------|-------------|-----------|-------|
| **Google Organic** | < 25 | 500/mo | Standard. KD < 20 preferred |
| **Bing Organic** | < 20 | 200/mo | Bing ka KD metric alag hota hai — lower competition, lower volume |
| **Google AI Overviews** | < 30 organic KD | 200/mo question queries | Must rank in organic top 20 (97% AI Overviews citations from top 20). Question-based intent required |
| **ChatGPT Search** | N/A (citation-based) | Any | Needs listicle format + clean HTML + existing indexation. Citation rate: 43.8% listicles |
| **Perplexity** | N/A (freshness-based) | Any | Needs monthly refreshable content. Fact-dense paragraphs. Reddit cross-citations matter |
| **YouTube Search** | N/A | 500/mo | Video optimization separate. Topic should work as script |

**Rule:** Google KD < 25 is still primary filter. Other platform thresholds are ADDITIONAL — topic must be viable on at least 2 platforms.

### E. Search Intent
| Intent | Priority | Why |
|--------|----------|-----|
| Informational | High | Blog posts, guides, listicles — easiest to rank |
| Commercial Investigation | High | "best", "vs", "reviews", "benefits" — high CPC |
| Transactional | Medium | "buy", "price" — hard for blog to compete |
| Navigational | Low | Brand searches — irrelevant |

**Rule:** Topics ka intent informational ya commercial investigation hona chahiye.

### F. Cannibalization Prevention (CRITICAL for 3-5/Day)
- **No duplicate primary keywords** — har article ka unique target keyword hona chahiye
- **Check existing posts** before adding any topic (use `grep` ya `seo-cannibalization-detector`)
- **Weekly audit required:** Run cannibalization detector every Sunday
- **If cannibalization found:** Merge articles ya redirect — never keep 2 articles for same keyword

### G. Monetization Potential
- **AdSense Friendly:** Topic has high advertiser competition (proof: high CPC)
- **Affiliate Ready:** Products available to promote (Amazon, health stores)
- **Product Sales:** Site ke Ayurvedic products se connect ho sakta hai

---

## 6. Topic Validation Checklist (10-Point — Multi-Platform)

Har topic ko finalize karne se pehle yeh 10 points check karo:

```
[ ] 1. KD < 25 — keyword difficulty low hai?
[ ] 2. Volume > 500/mo — enough searches?
[ ] 3. CPC > $2 — AdSense ke liye profitable?
[ ] 4. USA/UK/CA/AU — target country hai?
[ ] 5. Site category mein fits? (human/pet health)
[ ] 6. Already covered nahi hai? (check existing posts)
[ ] 7. Search intent informational/commercial hai?
[ ] 8. Monetized ho sakta hai? (ads/affiliate/product)
[ ] 9. Seasonal relevance — abhi ya upcoming season mein relevant hai?
[ ] 10. Multi-platform viable — at least 2 platforms se traffic aa sakta hai?
```

Sirf wohi topics final karo jo **10/10 ya at least 9/10** pass karein.

---

## 7. Content Gap Analysis Rules

Topics research karte time yeh gaps dhoondo:

| Gap Type | How to Find | Example |
|----------|-------------|---------|
| **Keyword Gap** | Competitors rank for, site nahi | "ashwagandha for women" — competitor rank kar raha, tum nahi |
| **Content Depth Gap** | Existing articles thin hain | Top 10 results mein 500-word articles — tum 2000-word likh sakte ho |
| **Angle Gap** | Same topic, different POV | Sab "benefits of ashwagandha" likh rahe — tum "ashwagandha for bodybuilding" likho |
| **Format Gap** | No video/infographic/listicle | Topic par koi "ultimate guide" nahi hai |
| **Freshness Gap** | Old content, update needed | Last updated 2020 — tum 2026 version likho |
| **AEO Gap** | AI search questions unanswered | "How does ashwagandha reduce cortisol?" ka koi article nahi hai |

---

## 8. Topic Output Format

Agent jab topics suggest karega, yeh format use karega:

```markdown
## Topic Suggestion

| Field | Value |
|-------|-------|
| **Title** | Ashwagandha for Women: Complete Hormonal Balance Guide |
| **Category** | Herbs & Supplements / Women's Health |
| **Target Keyword** | ashwagandha for women |
| **Search Volume** | 4,200/mo (US) |
| **KD Score** | 18 |
| **CPC** | $6.50 |
| **Intent** | Informational |
| **Target Countries** | US, UK, CA, AU |
| **Competition Level** | Low |
| **Monetization** | AdSense + Affiliate (Amazon) + Product Sales |
| **Why This Topic** | High volume, low KD, existing articles are thin (500 words), CPC high |
| **Related Keywords** | ashwagandha for women benefits, ashwagandha for PCOS, ashwagandha dosage for women |
```

---

## 9. Research Sources (Preferred Order)

Topics research karte time yeh sources use karo:

1. **Google Trends** (trends.google.com) — Trending topics, seasonality
2. **Google Keyword Planner** — Volume + CPC data
3. **Google Search (manual SERP)** — Competition analysis, featured snippets
4. **People Also Ask (Google SERP)** — AEO question opportunities
5. **Reddit** (site:reddit.com ayurveda) — Real user questions, pain points
6. **Quora** (site:quora.com ayurveda) — What people are asking
7. **Amazon Reviews** — Product pain points (health niche)
8. **AnswerThePublic** — Question-based keyword ideas
9. **Ahrefs / SEMrush / Ubersuggest** — If data available
10. **Competitor Blogs** — What's working for them
11. **YouTube Search** (youtube.com) — Video topics, high-intent queries, comment-based pain points
12. **Pinterest Trends** (trends.pinterest.com) — Visual search trends, seasonal spikes
13. **Google News** (news.google.com) — Trending health topics, newsjack opportunities
14. **Bing Webmaster Tools** (webmaster.microsoft.com) — Bing index status, sitemap submission, Bing search performance
15. **Perplexity** (perplexity.ai) — Check topic is cited by AI, see what sources Perplexity prioritizes
16. **ChatGPT Search** (chatgpt.com) — Manual check: does ChatGPT cite your domain for health queries?
17. **YouTube Search** (youtube.com) — Video topic viability, health content on YouTube trends
18. **Pinterest Trends** (trends.pinterest.com) — Visual search trends for Ayurveda/herbal topics
19. **Reddit** (reddit.com) — Cross-check: is topic being discussed in health/Ayurveda subreddits? Perplexity + ChatGPT both cite Reddit heavily
20. **PubMed E-utilities** (free, no key) — `python3 scripts/pubmed-cite.py '<topic> clinical trial' 3` — Auto-fetch PubMed citations for E-E-A-T. Unlimited, free, no API key

---

## 10. Prohibited Topics

Yeh topics kabhi suggest mat karo:

- **Disease Claims:** "Ayurveda cures cancer" — YMYL violation, legal risk
- **Prescription Drug Comparisons:** "Ayurveda vs Metformin" — medical advice
- **Miracle Cures:** "Lose 20kg in 7 days" — fake, damages credibility
- **Copyright Content:** Copy-paste from other sites
- **Politics / Religion:** Unrelated to health niche
- **Adult Content:** Not relevant
- **Gambling / Drugs:** Against AdSense policy

---

## 11. Workflow Summary

```
User Request → Topic Research Needed
    │
    ├─ STEP 0: Multi-Platform Pre-Flight Check (Section 0)
    │   ├─ websearch: Google updates [current month]
    │   ├─ websearch: Bing index changes
    │   ├─ websearch: ChatGPT/Perplexity/Gemini policy updates
    │   ├─ websearch: AI crawler policy updates
    │   ├─ IF any platform update → auto-adjust filters per platform + notify
    │   ├─ IF no updates → proceed with standard multi-platform filters
    │   └─ Log platform status
    │
    ├─ Step 1: Load Skills (seo-aeo-keyword-research, content-strategy, etc.)
    │
    ├─ Step 2: Web Research (Google Trends, Bing Webmaster, Perplexity, Keyword Planner, SERP check)
    │
    ├─ Step 3: Apply Filters
    │   ├─ Google: KD < 25, Vol > 500, CPC > $2, Intent match
    │   ├─ Bing: KD < 20, Vol > 200, indexation check
    │   ├─ AI Search: freshness, listicle format viability, question intent
    │   └─ Must be viable on at least 2 platforms
    │
    ├─ Step 4: Gap Analysis (competitors, content depth, angle, AEO, platform gaps)
    │
    ├─ Step 5: Validation (10-point multi-platform checklist)
    │
    └─ Output (table format with all fields + platform viability)
```

---

## 12. Version History

| Date | Changes |
|------|---------|
| 2026-07-07 | Initial creation — Shiva's master config for AI topic research |
| 2026-07-07 | Added KD tiers (5A), 9th checklist (6), YouTube/Pinterest/News (9). Added Sections 13-18: Seasonal Calendar, Topic Clusters, SERP Features, Competitor Radar, KPIs, Content Brief + Cadence |
| 2026-07-07 | Updated cadence to 3-5/day with phase-based scaling (Section 18). Added Cannibalization Prevention clause (Section 5E). Added RSS Research Section 19. |
| 2026-07-07 | Added Section 0: Algorithm Pre-Flight Check (Auto-Adjust) — Google update detection + auto-strategy adjustment. Updated Workflow Summary diagram. |
| 2026-07-07 | Section 0 expanded to Multi-Platform Pre-Flight Check — Google + Bing + ChatGPT/Perplexity + AI crawlers. Added Section 0D Platform Monitoring Log. Section 5D: Per-Platform KD/Volume Thresholds (Bing, AI Overviews, ChatGPT, Perplexity, YouTube). Section 6: Updated to 10-point checklist. Section 9: Added 6 multi-platform research sources. Workflow diagram updated with multi-platform branching. |
| 2026-07-07 | Bing credentials saved to `secrets/bing-client-credentials.json`. `scripts/bing-sitemap-submit.py` created for sitemap + IndexNow URL submission. `schedule-posts.py` auto-submits to Bing on publish. `llms.txt` deployed via Cloudflare Worker at `llms.ayurshakti.shop/llms.txt`. robots.txt updated with AI crawler rules + llms.txt reference. |
| 2026-07-07 | Full site audit. GSC + GA4 data verified. Theme JS redirect (`?m=0` → canonical) added to fix Google duplicate warning. Sitemap atom.xml submitted to GSC. Cron setup for scheduler. |
| 2026-07-07 | Added `docs/12-backlink-strategy.md` — Phase 1/2/3 architecture. Backlink opportunity analysis added to Gap Analysis section. |
| 2026-07-07 | `config/profile.json` created. All scripts refactored. Email: contact@ayurshakti.shop via Gmail. |

---

## 13. Seasonal Topic Calendar (Ayurvedic)

Ayurveda seasons ke saath closely linked hai. Topics ko **current + upcoming season** ke hisaab se prioritize karo:

### Spring (Feb-Apr) — Kapha Season
| Focus Area | Topic Ideas | Why |
|------------|-------------|-----|
| Detox | Triphala detox, spring cleanse, Panchakarma at home | Kapha accumulation, body needs cleaning |
| Allergies | Natural antihistamines, Tulsi for hay fever | Spring allergies peak |
| Weight Loss | Ayurvedic weight loss, Kapha-balancing diet | Kapha season = easiest time to lose weight |
| Immunity | Chyawanprash benefits, seasonal immunity | Transition season = sickness peak |

### Summer (May-Jul) — Pitta Season
| Focus Area | Topic Ideas | Why |
|------------|-------------|-----|
| Skin Care | Ayurvedic sunscreen, glowing skin diet, aloe vera | Sun damage, Pitta aggravation |
| Digestion | Light diet, buttermilk benefits, mint for cooling | Agni weakens in heat |
| Hydration | Ayurvedic summer drinks, coconut water benefits | Dehydration risk |
| Hair | Coconut oil benefits, cooling hair masks | Summer hair damage |

### Monsoon (Aug-Oct) — Vata Season (early) + Pitta (late)
| Focus Area | Topic Ideas | Why |
|------------|-------------|-----|
| Digestion | Gas/bloating remedies, ginger for digestion, Triphala | Weak agni, digestion issues peak |
| Immunity | Giloy benefits, Tulsi for monsoon, cold prevention | Infections, waterborne diseases |
| Joint Health | Ayurvedic joint pain remedies, Vata-balancing oils | Vata aggravation = joint pain |
| Skin | Fungal infections, Ayurvedic antifungal, Neem | Humidity = fungal growth |

### Autumn / Winter (Nov-Jan) — Vata Season
| Focus Area | Topic Ideas | Why |
|------------|-------------|-----|
| Immunity | Ashwagandha for immunity, Chyawanprash daily use | Cold & flu peak |
| Joint Health | Warm oils, joint pain relief, massage benefits | Vata = stiffness, pain |
| Sleep | Insomnia remedies, warm milk with turmeric, Brahmi | Vata causes anxiety/sleep issues |
| Respiratory | Tulsi for cough, steam inhalation, lung health | Respiratory infections peak |

**Implementation Rule:** Har quarter mein **current season (80%) + next season (20%)** topics research karo. Isse content ready rahega publish time par.

---

## 14. Topic Cluster Architecture (Pillar + Cluster)

Har major topic ke liye **pillar page + cluster articles** ka structure follow karo. Isse topical authority build hoti hai.

### Cluster Template

```
Pillar: "Ashwagandha: Complete Guide to Benefits, Dosage & Side Effects" (3000+ words)
├─ Cluster 1: "Ashwagandha for Men: Testosterone & Muscle Growth" (1500 words)
├─ Cluster 2: "Ashwagandha for Women: Hormonal Balance & PCOS" (1500 words)
├─ Cluster 3: "Ashwagandha Dosage: How Much Should You Take?" (1200 words)
├─ Cluster 4: "Ashwagandha Side Effects: What to Watch Out For" (1200 words)
├─ Cluster 5: "Ashwagandha vs Shilajit: Which is Better?" (1500 words)
├─ Cluster 6: "Best Time to Take Ashwagandha: Morning or Night?" (1000 words)
└─ Cluster 7: "Ashwagandha for Sleep & Anxiety: Does It Work?" (1500 words)
```

### Cluster Rules

| Aspect | Rule |
|--------|------|
| **Pillar to Cluster Ratio** | 1 pillar : 5-10 cluster articles |
| **Interlinking** | Har cluster → pillar (contextual link). Pillar → all clusters (table of contents style) |
| **Pillar Word Count** | 3000-5000 words (comprehensive) |
| **Cluster Word Count** | 1000-2000 words (focused, single subtopic) |
| **Publish Order** | Pehle pillar, phir 2-3 clusters per week |
| **Topic Selection** | Cluster topics = related keywords from research phase |

### When to Use Clusters
- **Must-use:** Herbs (Ashwagandha, Giloy, Triphala, Shilajit, etc.)
- **Must-use:** Health conditions (PCOS, diabetes, thyroid, weight loss)
- **Nice-to-have:** General topics (Ayurvedic diet, skincare routine)

---

## 15. SERP Feature Targeting Strategy

Har topic ke intent ke hisaab se specific SERP feature target karo.

### Intent → Feature Mapping

| Search Intent | Target SERP Feature | Content Strategy |
|---------------|-------------------|-----------------|
| "how to" | Featured Snippet (Paragraph) | Step-by-step format, clear instructions, numbered list |
| "what is" | Featured Snippet (Paragraph) | Definition in first 50 words, bold key terms |
| "benefits" | Featured Snippet (List) | Bulleted list of benefits, short explanations |
| "vs" / comparison | Comparison Table | HTML table with differences, price, pros/cons |
| "best" + noun | Listicle Featured Snippet | Numbered list (Top 5/7/10), each with H3 + details |
| "dosage" | Featured Snippet (Table) | Table format: age, dosage, timing, precautions |
| "side effects" | Featured Snippet (List) | Numbered list with severity indicators |
| Questions (PAA) | People Also Ask | FAQ section with schema markup |
| "remedies" | Listicle + Image Pack | Numbered home remedies, step photos |
| "diet" / "food" | Featured Snippet + Image | Table format food lists, clear categorization |

### Optimization Template

```
For EVERY article targeting featured snippet:

1. Directly answer question in first 100 words
2. Use <h2> for the target question
3. Format answer as: paragraph (how/what), list (benefits/remedies), table (comparison/dosage)
4. Keep answer 40-60 words (snippet length sweet spot)
5. Use schema markup (FAQ, HowTo, Article)
```

### Image SERP Optimization
- Har article mein **at least 1 infographic** (canva ya custom)
- Alt text = target keyword naturally
- File name = keyword-based (e.g., `ashwagandha-benefits-infographic.jpg`)
- Dimensions: 1200x628px (social share optimized)

---

## 16. Competitor Radar

### Primary Competitors (High Priority — Monitor Weekly)

| Site | DR | Strength | Gap (Our Opportunity) |
|------|-----|----------|----------------------|
| healthline.com | 89 | High authority, medical review | Too generic, no Ayurveda depth |
| verywellhealth.com | 82 | Trusted, well-structured | Western-focused, minimal Ayurveda |
| organicfacts.net | 72 | Good herbal content | Thin content (300-500 words) |
| stylecraze.com | 68 | Beauty + wellness | Low authority, clickbait titles |
| ndtv.com/food (health) | 85 | India-specific content | Not purely Ayurveda |

### Secondary Competitors (Monitor Bi-Weekly)

| Site | DR | Strength | Our Edge |
|------|-----|----------|----------|
| ayurtimes.com | 45 | Ayurveda-specific | Low DR — overtake easily |
| easyayurveda.com | 42 | Classic Ayurveda | Poor UX, slow |
| planetayurveda.com | 50 | Product-focused | Thin blog content |
| netmeds.com (health blog) | 70 | Pharmacy brand | Generic content |
| 1mg.com (health blog) | 72 | Pharma brand | Not Ayurveda-specific |

### Backlink Opportunity Analysis (Weekly)
- See `docs/12-backlink-strategy.md` for Phase 1/2/3 plan
- **Topic Backlink Potential:** Har topic research ke time check karo — "is topic pe guest post mil sakta hai?"
- **Competitor Backlinks:** Analyze top 3 competitor backlinks per keyword using `websearch`
- **Broken Link Targets:** High-authority pages linking to dead Ayurveda content

### Gap Analysis Workflow (Monthly)

```
1. Pick top 3 competitors from list
2. Use `websearch` "site:competitor.com ayurveda [topic]"
3. Fetch top 5 ranking pages from each
4. Compare with our content:
   - Keyword coverage (what they rank for, we don't)
   - Content depth (their word count vs ours)
   - Angle uniqueness (what angle can we use that they don't)
   - SERP features (do they have featured snippets we can steal?)
5. Output: 3-5 topic opportunities per competitor
```

---

## 17. Performance KPIs (Post-Publish Tracking)

Har published topic ko track karo. Refresh decision KPIs based hota hai.

### Benchmarks

| Metric | 30 Days | 60 Days | 90 Days | Action if Below |
|--------|---------|---------|---------|-----------------|
| **Avg Position** | < 30 | < 20 | < 10 | Content refresh needed |
| **Clicks/Day** | > 5 | > 20 | > 50 | Optimize CTR (title/meta) |
| **CTR** | > 2% | > 3% | > 5% | Rewrite title + meta description |
| **Impressions/Day** | > 200 | > 500 | > 1000 | Internal linking boost |
| **AdSense RPM** | — | > $5 | > $10 | Add more commercial keywords |
| **Bounce Rate** | — | < 70% | < 60% | Improve content readability |

### Tracking Setup

```
Har article publish karte time:

1. Google Search Console mein note karo — target keyword, publish date
2. Google Analytics mein event set karo — "article_publish" with topic category
3. Spreadsheet mein log karo (see template below)

Post Performance Log:

| Article | Keyword | Publish Date | 30d Position | 30d Clicks | 60d Position | 60d Clicks | Action Needed |
|---------|---------|-------------|-------------|-----------|-------------|-----------|---------------|
| ...     | ...     | ...         | ...         | ...       | ...         | ...       | ...           |
```

### Refresh Rules
- **30-day check:** Agar position > 30 → internal linking from high-traffic pages, update title/meta
- **60-day check:** Agar position > 20 → rewrite intro, add more sections, improve readability
- **90-day check:** Agar position > 10 → major rewrite (2000+ words), add new sections, update stats
- **180-day check:** Agar position < 10 → leave it, move to next topic
- **Seasonal refresh:** Har season start pe relevant topics ko update karo (add current year, freshen stats)

---

## 18. Content Brief Template + Publishing Cadence

### Content Brief Format

Har finalized topic ke liye yeh brief generate karo:

```markdown
## Content Brief

| Field | Value |
|-------|-------|
| **Article Title** | [Title — include primary keyword in first 60 chars] |
| **Slug** | `/[keyword-slug]` (NEVER use `/blog/` prefix) |
| **Meta Title** | [60 chars max, primary keyword first] |
| **Meta Description** | [155-160 chars, include keyword + CTA] |
| **Target Keyword** | [Primary keyword] |
| **Secondary Keywords** | [3-5 LSI/semantic keywords] |
| **Word Count** | [1500-2500 words] |
| **Readability Target** | Grade 6-8 (Flesch) |
| **Category** | [From Section 2] |

### H2 Structure
1. Introduction (150-200 words — hook + keyword in first 100 words)
2. [H2 — directly answers search intent]
3. [H2 — deep dive subtopic]
4. [H2 — benefits / how-to / comparison]
5. [H2 — practical tips / dosage / precautions]
6. FAQ (3-5 questions with schema markup)
7. Conclusion (100 words — summary + CTA)

### Internal Links Required
- [ ] Link to pillar page (if cluster article)
- [ ] Link to 2-3 existing related articles
- [ ] Link to product page (if applicable)

### External Links
- [ ] Reference 1-2 high-DR sources (for E-E-A-T)
- [ ] Cite PubMed/NCBI study (if available)

### Image Requirements
- [ ] Featured image: 1200x628px (keyword filename, alt text)
- [ ] 1 infographic (Canva)
- [ ] 2-3 inline images (relevant, royalty-free)

### Affiliate Links
- [ ] Amazon affiliate links (where relevant)
- [ ] Product page links

### Schema
- [ ] Article schema
- [ ] FAQ schema (if FAQ section present)
- [ ] HowTo schema (if step-by-step guide)
```

### Publishing Cadence (PAUSED — May 2026 Core Update)

> **⚠️ CORE UPDATE ALERT:** Due to the May 2026 Google Core Update, aggressive topic research and scaling are currently PAUSED. Focus entirely on content pruning, updating existing articles, and maintaining current rankings.

| Phase | Articles/Day | Articles/Month | Focus | Risk Level |
|-------|-------------|---------------|-------|------------|
| **Current** (Core Update) | 0-1/day | 0-30 | Content pruning, updates, audits | HIGH |

**⚠️ Cannibalization Warning:** 3-5/day means **90-150 unique keywords per month**. Har article ka UNIQUE primary keyword hona chahiye. Use `seo-cannibalization-detector` weekly.

| Metric | Value | Notes |
|--------|-------|-------|
| **Topics Researched/Week** | 25-35 | Batched on Monday, covers full week |
| **Articles Written/Day** | 3-5 | AI-assisted + human touch pass |
| **Articles Published/Day** | 3-5 | Auto-schedule via approval queue |
| **Pillar Pages/Month** | 8-12 | Topical authority building |
| **Cluster Articles/Month** | 25-40 | Around pillar pages |
| **Best Time to Publish** | Tue-Thu, 8-10am EST | Highest engagement |
| **Cannibalization Check** | Weekly (Sundays) | `seo-cannibalization-detector` run |

### Weekly Workflow

```
Monday:    Topic research (25-35 topics) → Batch to approval queue
Tuesday:   Content briefs (5-7) → Start writing (3-4 articles)
Wednesday: Writing day (4-5 articles) + editing
Thursday:  Writing day (4-5 articles) + editing + publish scheduled
Friday:    Writing day (3-4 articles) + editing + publish scheduled + performance review
Saturday:  Catch-up + pending article completion + queue refill
Sunday:    Cannibalization audit + gap analysis + next week prep
```

---

## 19. RSS Feed Research (Advanced Competitor Monitoring)

RSS feeds ka use karo **competitor monitoring, trending topic detection, aur content gap analysis** ke liye — yeh 3-layer research process ka part hai.

### Setup
- **MCP Server:** `rss-feeds-mcp` installed in opencode.jsonc — auto-available
- **Feeds Config:** `~/.rss-mcp/feeds.json` — 30+ feeds pre-seeded (25 Ayurveda + 5 health/SEO)
- **No API key required** — completely free, runs locally

### Available Tools

| Tool | Function | Use Case |
|------|----------|----------|
| `fetch_blogs` | Fetch latest posts from ALL feeds | Daily trending topic scan |
| `fetch_by_category` | Fetch posts filtered by category | Ayurveda-only vs SEO-only scan |
| `fetch_from_source` | Fetch posts from one specific feed | Deep dive into one competitor |
| `search_blogs` | Search across all feeds by keyword | Topic gap analysis |
| `add_feed` | Add a new RSS feed | Expand monitoring |
| `list_categories` | List all feed categories | See available groups |
| `list_feeds` | List all configured feeds | Check what's being monitored |

### Research Workflow (3-Layer)

RSS akela kaafi nahi — yeh **Layer 1** hai. Pura workflow:

```
User: "Research topic — ashwagandha for women"
         │
         ├── LAYER 1: RSS (rss-feeds-mcp)
         │   ├─ search_blogs("ashwagandha women", "30d") → 25+ Ayurveda feeds
         │   ├─ Result: "PlanetAyurveda ne likha, EasyAyurveda ne likha"
         │   └─ Gap detect: "Kisi ne 'ashwagandha for PCOS women' deeply cover nahi kiya"
         │
         ├── LAYER 2: websearch (Google SERP)
         │   ├─ search("ashwagandha for women kd cpc volume")
         │   ├─ search("site:healthline.com ashwagandha women")
         │   └─ Result: KD score, CPC, featured snippets, DR analysis
         │
         ├── LAYER 3: webfetch (Deep Content Analysis)
         │   ├─ Fetch → top 3 competitor articles full content
         │   ├─ Compare: word count, headings, missing sections
         │   └─ Result: "Top article sirf 800 words — tum 2500 likh sakte ho"
         │
         ├── APPLY FILTERS (Section 5+6)
         │   ├─ KD < 25? ✅ | Volume > 500? ✅ | CPC > $2? ✅
         │   └─ 9/9 checklist pass ✅
         │
         └── OUTPUT: Topic suggestion with competitive analysis
```

### Example Queries

```
Agent commands — baar baar use honge:

# Daily trending scan
"Fetch latest Ayurveda blog posts from last 48 hours"

# Topic validation with RSS
"Search all Ayurveda feeds for 'triphala weight loss' — kya competitors ne likha hai?"

# Competitor deep dive
"Fetch latest 5 posts from PlanetAyurveda feed — what topics are they covering?"

# Gap analysis
"Search all Ayurveda feeds for keywords: PCOS, hormonal balance, fertility
 — konsi topics kisi ne cover nahi ki?"

# Full advanced research
"Research 'ashwagandha for women' — use RSS to check competitor coverage,
 websearch for KD/volume/CPC, then webfetch top article for content gap analysis"
```

### Pre-Seeded Feeds (30+)

| Category | Feeds | Count |
|----------|-------|-------|
| **Ayurveda Competitors** | EasyAyurveda, PlanetAyurveda, DeepAyurveda, Nimba, Upakarma, TravancoreAyurveda, BirlaAyurveda | 7 |
| **Ayurveda References** | MotherOfHealth, AyurvedaExperience, AyurvedicVillage, SimpleAyurveda, AyurMedia, AyurvedicClinic, MNAyurveda, SaumyaAyurveda, AyurvedaMagazine, LiveRight, AyurvedicIndia, Ashpveda, PaavaniAyurveda, Vaidyagrama, KamaAyurveda | 15 |
| **Health Research** | MedlinePlus, NIH News, Patient.info | 3 |
| **SEO Reference** | HubSpot, SearchEngineLand, Moz | 3 |
| **General News** | TechCrunch, Google News Health | 2 |

### Notes
- Feeds can be added anytime via `add_feed(name, url, category)` tool
- If a feed fails, the server handles it gracefully — no crash
- All fetching happens locally — no data sent to third parties
