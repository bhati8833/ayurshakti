# Article Writing Rule — AyurShakti.shop

> **OpenCode Required Skills:**
> Before executing tasks in this document, load the following skills from the OpenCode library (Home Directory):
> - `avoid-ai-writing`
> - `seo-aeo-blog-writer`
> - `marketing-psychology`
> - `professional-proofreader`

## Purpose
AI agent ke liye article writing ka master rule. Jab bhi koi article likhna ho (topic list se ya fresh order pe), yeh file AI ko guide karegi ki KAISE likhna hai, KONSE skills/tools use karne hain, aur article ko HUMAN kaise banaya jaye. Baar-baar instructions repeat nahi karne padenge.

---
## 0. Multi-Platform Pre-Write Check (Auto-Adjust — Run Before Every Article)

Section 0 of `08-topic-research-rule.md` pehle run hota hai (topic-level multi-platform check). Yeh section **article-writing level** ka auto-adjust hai — har platform ke update ke hisaab se writing style, human touch, aur SEO rules change ho jayenge.

### A. Check ALL Platform Updates (Shares Data from Topic Research Section 0)
Agar topic research section 0 ne updates detect kiye hain, toh wahi findings use karo. Agar direct article request hai (without topic research), tab yeh check karo:

```websearch queries:
# Google
1. "Google algorithm update 2026 [current month]"
2. "Google AI content detection update 2026"
3. "Google helpful content update 2026 writing guidelines"

# Bing & ChatGPT Search
4. "Bing Webmaster guidelines 2026"
5. "ChatGPT Search content formatting update 2026"

# AI Search & AI Overviews
6. "Perplexity AI content source update 2026"
7. "Google AI Overviews content formatting 2026"
8. "Gemini AI content citation update 2026"
```

### B. Auto-Adjust Writing Strategy Per Platform

| Update Detected | Auto-Adjustment in Article Writing |
|----------------|------------------------------------|
| **Google Helpful Content** | Word count min → 2000 (was 1500). Keyword density max → 1% (was 1.5%). Add personal anecdote requirement per section |
| **Google Spam Update** | `avoid-ai-writing` skill run **2 times** (before + after human touch pass). Add manual fact-check step. Reduce cadence by 50% |
| **Google Core Update** | **DELAY** publishing by 3-5 days. Write but don't schedule. Let ranking volatility settle first |
| **Google AI Content Policy** | Increase personal story ratio (min 1 story per H2). Reduce factual claims — more "traditionally used" phrasing |
| **Google AI Overviews / SGE** | First 100 words MUST be a direct answer. Definition sentence mandatory. TL;DR + FAQ + schema = required (not optional) |
| **Google E-E-A-T Update** | Author bio with credentials required. External citations min 3 per article. Medical disclaimer must be prominent |
| **Bing Index / SEO Update** | Submit article sitemap to Bing Webmaster after publish. Use clean HTML structure. Avoid complex JavaScript rendering |
| **ChatGPT Search Policy** | Use listicle format for key sections (43.8% ChatGPT citations are listicles). Ensure clean HTML — no hidden text, no broken tags |
| **Perplexity Freshness** | Include month/year in article date. Add "Last updated" tag. Perplexity prefers content updated within 60 days |
| **No update found** | Proceed with standard writing rules from Section 5-10 |

### C. Auto-Adjust Implementation

```
IF any platform update detected:
  → Modify writing template per affected platform (word count, structure, keyword density)
  → Increase/decrease human touch passes
  → Adjust SEO rules dynamically
  → Notify: "⚠️ Writing rules adjusted for [Platform: Update Name]"

IF no update across all platforms:
  → "✅ No writing-impacting updates on any platform. Standard rules apply."
```

---
## 1. Article Writing Workflow

```
User Request → Article to Write
    │
    ├─ Step 1: Load Skills (writing, human-touch, seo, publishing)
    │
    ├─ Step 2: Research & Prepare (topic study, competitor check)
    │
    ├─ Step 3: Write Draft (structure + body + human touch)
    │
    ├─ Step 4: AI Pattern Removal (avoid-ai-writing audit)
    │
    ├─ Step 5: SEO + AEO Optimization (keywords, schema, readability)
    │
    ├─ Step 6: Quality Check (8-point checklist)
    │
    ├─ Step 7: Proofread (professional-proofreader)
    │
    ├─ Step 8: Run Pre-Publish Checklist (10/10 gate)
    │   - Image, TL;DR, FAQ(5), Schema, Human touch
    │   - Internal links, H2/H3, Word count ≥1500, Keyword, No banned phrases
    │   - Fail → fix and retry. Pass → proceed to Step 9
    │
    └─ Step 9: Add to Approval Queue → Auto-Scheduler picks in 12h window
        - Push article to `scripts/approval-queue.json`
        - `schedule-posts.py` runs every 12h
        - Picks 2 random articles → schedules at EST 8-10am / 6-8pm
        - See `docs/11-article-approval-scheduler.md`
```

---
## 2. Skills to Load (from skill-library/)

Jab bhi article write karne ka task aaye, yeh skills load karo:

### Primary — Writing & Structure
| Skill | Purpose |
|-------|---------|
| `seo-aeo-blog-writer` | Long-form blog with TL;DR, definition sentence, FAQ (5 exact questions), comparison table |
| `seo-content-writer` | SEO content framework, keyword density, E-E-A-T signals |
| `blog-writing-guide` | Blog structure, voice, banned words, formatting |

### Primary — Human Touch
| Skill | Purpose |
|-------|---------|
| `avoid-ai-writing` | 21-pattern AI detection + 43-entry replacement table — MUST RUN 2 TIMES (before & after human touch pass) AND STRICT MANUAL REVIEW REQUIRED (Spam Update Rule) |
| `beautiful-prose` | Strong, concrete, verb-forward prose — no filler, no therapy voice |
| `marketing-psychology` | Behavioral science hooks — social proof, loss aversion, authority bias |
| `copywriting` | Persuasive angles, CTAs, benefit-driven headlines |

### Primary — SEO & AEO
| Skill | Purpose |
|-------|---------|
| `seo-aeo-content-quality-auditor` | Score article out of 100 (SEO + AEO + Readability) before publish |
| `ai-seo` | LLM/AEO optimization — make content extractable by ChatGPT/Perplexity |
| `seo-schema` | JSON-LD structured data (Article, FAQ, HowTo, Product schema) |
| `seo-aeo-internal-linking` | Internal link mapping after article is written |
| `seo-images` | Image alt text, filename, compression, lazy loading |

### Secondary — Editing & Polishing
| Skill | Purpose |
|-------|---------|
| `professional-proofreader` | Grammar, spelling, punctuation, clarity, voice preservation |
| `seo-content-refresher` | Refresh outdated articles with new data |
| `seo-cannibalization-detector` | Check existing content for keyword overlap |

### Utilities
| Skill | Purpose |
|-------|---------|
| `deep-research` | Deep dive on complex topics before writing |
| `efficient-web-research` | Token-efficient competitor article analysis |
| `keyword-extractor` | Extract keywords from top-ranking competitors |
| `seo-aeo-meta-description-generator` | Generate 150-160 char meta descriptions |

**Usage:** Agent auto-load inhe karega jab article writing task detect hoga.

---
## 3. Tools to Use

### Web Research Tools
| Tool | When to Use |
|------|-------------|
| `websearch` | Research topic, find stats/data, study competitor articles |
| `webfetch` | Fetch top 3-5 competitor articles for content/style analysis |
| `browser_puppeteer_navigate` | Browse competitor pages, Google featured snippets |
| `browser_puppeteer_screenshot` | Capture reference layouts, tables, infographics |

### Writing & Publishing Tools
| Tool | When to Use |
|------|-------------|
| `skill` | Load relevant writing skills before drafting |
| `task` | Deploy subagents for parallel tasks (e.g., research + outline + fact-check) |
| `bash` | Run build & deploy scripts, format checks. **PubMed citations:** `python3 scripts/pubmed-cite.py 'keyword study trial' 3` |
| `read` | Read existing articles, topic list, reference docs |
| `grep` | Check if content already exists for a keyword |
| `glob` | Find related articles for internal linking |
| `question` | Ask user for clarification on ambiguous writing instructions |

---
## 4. Pre-Writing Phase

Har article likhne se pehle yeh karo:

### A. Read the Topic
- Read topic from user ke order ya research se
- Extract: target keyword, category, target countries, search intent

### B. RSS Feed Check (Competitor Monitoring)
- RSS feeds se check karo ki **competitors ne recent mein** kya publish kiya
- Use `search_blogs("topic keyword", "30d")` — rss-feeds-mcp se 25+ Ayurveda feeds
- Note karo: konsi angles already covered, kya missing hai
- Freshly published articles ko priority do (trending indicator)

### C. Competitor Article Study
- Websearch karo top 3-5 ranking articles for the target keyword
- Note karo: word count, structure, headings, what's missing
- Analysis store karo for reference while writing

### D. Keyword Research for Article
- Primary keyword already given (from topic research)
- Find 3-5 LSI/semantic keywords to sprinkle naturally
- Find 5 long-tail questions for FAQ section

### E. PubMed Citation Fetch (E-E-A-T Boost)
- Run `python3 scripts/pubmed-cite.py '<primary keyword> clinical trial' 3` to get 3 relevant PubMed studies
- Run `python3 scripts/pubmed-cite.py '<primary keyword> benefits' 2` for additional supporting research
- Paste PMID + DOI links directly into article as external citations
- PubMed API is **free, no API key, unlimited usage** — use for EVERY article

### F. Load Writing Template
- Article length based on competition:
  - If competitors have 500-800 words → write 2000-2500 words
  - If competitors have 1500-2000 words → write 3000-4000 words
  - Minimum: 1500 words. Maximum: 5000 words (unless guide)
- Structure: H1 title → TL;DR → H2 sections (5-8) → H3 subsections → FAQ → Conclusion

---
## 5. Article Structure (Mandatory)

Har article yeh structure FOLLOW karega:

### H1: Title
- Include primary keyword naturally
- Emotional trigger ya benefit-driven hook
- Max 60 characters (SEO best practice)
- Example: *Triphala for Weight Loss: How This Ayurvedic Formula Burns Belly Fat*

### TL;DR Block (Right After H1)
- 2-3 sentence direct answer to article's core question
- Must be extractable standalone — AI engines cite this first
- Format: blockquote in markdown

### H2: What Is [Topic]
- First line = clean definition sentence (extractable)
- Explain what it is in simple terms
- Brief history / origin if relevant (Ayurveda context)

### H2: Why [Topic] Matters
- Problem-agitate-solution structure
- Why reader should care
- Backed by stat/data where possible

### H2: How [Topic] Works (with H3 sub-sections)
- Break into 3-5 H3 sub-concepts
- Each H3 = one mechanism / one benefit / one use case
- Natural keyword placement in H3 headings

### H2: Practical Tips / How to Use
- Actionable advice reader can implement TODAY
- Dosage guidance, timing, combinations
- DIY recipes where applicable (Ayurveda articles)

### H2: Common Mistakes to Avoid (Optional)
- 3-5 mistakes people make
- What to do instead

### H2: Frequently Asked Questions (5 Questions)
- Exactly 5 FAQ entries
- Questions use long-tail + secondary keywords
- Each answer = max 50 words, standalone (no "as mentioned above")
- Format: Q / A pairs

### H2: Conclusion
- Summarize 2-3 key takeaways
- Clear CTA (try this herb, consult Ayurvedic doctor, share your experience)
- No "in conclusion" phrases — avoid AI tells

### Article Structure Variations (By Type)

Har article type ka optimal structure thoda different hota hai:

#### Type A: Herb / Supplement Guide (e.g., "Ashwagandha Benefits")
```
H1 → TL;DR → What Is It → Benefits (list with H3s) → How to Use → Dosage → Side Effects → FAQ → Conclusion
```
- Word count: 2500-4000
- Schema: Article + FAQPage + HowTo (if dosage guide)

#### Type B: Listicle (e.g., "Top 10 Ayurvedic Herbs for Immunity")
```
H1 → TL;DR → Intro → Item 1 (H3) → Item 2 (H3) → ... → Item 10 (H3) → Quick Comparison Table → FAQ → Conclusion
```
- Word count: 2000-3000
- Each item: H3 + 150-200 words
- Schema: Article + FAQPage + ListItem

#### Type C: How-To Guide (e.g., "How to Use Triphala for Weight Loss")
```
H1 → TL;DR → What You'll Need → Step 1 (H2) → Step 2 (H2) → ... → Step 5 (H2) → Tips for Best Results → Common Mistakes → FAQ → Conclusion
```
- Word count: 2000-3000
- Schema: Article + HowTo + FAQPage
- Each step: clear instruction + why it works

#### Type D: Comparison Article (e.g., "Ashwagandha vs Shilajit")
```
H1 → TL;DR → Quick Comparison Table → What Is Ashwagandha → What Is Shilajit → Head-to-Head (by factor) → Which One Should You Choose? → FAQ → Conclusion
```
- Word count: 2000-3000
- Schema: Article + FAQPage + Product (if comparing products)
- Head-to-Head factors: benefits, dosage, side effects, cost, taste

#### Type E: FAQ Article (e.g., "Ashwagandha: 15 Common Questions Answered")
```
H1 → TL;DR → Q1 (H3) → Q2 (H3) → ... → Q15 (H3) → Quick Reference Table → Conclusion
```
- Word count: 1500-2500
- Schema: FAQPage (primary) + Article
- Each answer: 50-80 words, standalone

---

## 5B. Supplementary Content Blocks

In blocks ko article mein include karo jahan relevant ho:

| Block | Format | Purpose |
|-------|--------|---------|
| **Key Takeaways Box** | `<div class="takeaways"><h3>Key Takeaways</h3><ul>3-5 bullets</ul></div>` | Skimmers ko quick summary. Right after TL;DR ya after intro |
| **Quick Reference Table** | Markdown table | Dosage comparison, nutrition facts, quick comparison |
| **Disclaimer Box** | `<blockquote class="disclaimer"><strong>Disclaimer:</strong> ...</blockquote>` | Legal protection. Right before Conclusion ya after TL;DR |
| **Related Posts** | "📖 Also Read: [Title 1] · [Title 2] · [Title 3]" | End of article, before disclaimer. Internal linking boost |
| **Product Recommendation Box** | "🛒 **Try It Yourself:** [Product name] — [affiliate link]" | Near dosage/how-to section. Affiliate monetization |
| **Reader Poll / Question** | "💬 **What's your experience?** Share in comments below..." | End of article. Engagement boost |

---
## 6. Human Writing Touch (CRITICAL)

Yeh section MOST IMPORTANT hai. AI-generated content detect hone se bachne ke liye in rules ko STRICTLY follow karo.

### A. Run avoid-ai-writing Skill on Every Draft
Har draft likhne ke baad, `avoid-ai-writing` skill run karo. Yeh detect karega:

| Pattern Category | What It Catches | Fix |
|-----------------|-----------------|-----|
| Em dashes | -- used as em dashes | Use periods or commas |
| Hedging | "may", "might", "could", "potentially" | Be direct or remove |
| Hollow intensifiers | "very", "extremely", "incredibly" | Use stronger verb |
| Rule of three | Forced 3-item lists | Break pattern |
| Filler transitions | "Moreover", "Furthermore", "In addition" | Remove or use natural flow |
| Significance inflation | "game-changer", "revolutionary", "unlock" | Say what it actually does |
| Template phrases | "In today's world", "It's important to note" | Delete completely |
| Generic conclusions | "In conclusion", "To summarize" | End naturally |
| Leverage/utilize/robust | Corporate buzzwords | use/use/reliable |

### B. Write Like a Human (Not an AI)

#### Use Personal Pronouns
- Write "I", "you", "we" throughout
- Example: "I have seen many patients benefit from Triphala..."
- Example: "You might be wondering how Ashwagandha actually works..."

#### Add Personal Stories / Anecdotes
- Start sections with mini-stories
- Example: "A patient came to me last month with chronic acidity. She had tried everything..."
- Example: "When I first started using Brahmi, I noticed the difference in 2 weeks..."

#### Conversational Tone (Hinglish Mix)
- Use natural Hindi-English mix where it feels authentic
- NOT formal textbook English
- NOT corporate blog speak
- Example: Ayurveda kyun kaam karta hai? Kyunki yeh root cause ko target karta hai.
- Example: TOH yeh raha asli sawaal — kaise kaam karta hai Ashwagandha?

#### Ask Rhetorical Questions
- "So what does this mean for you?"
- "But does it actually work?"
- "The real question is — how much should you take?"

#### Vary Sentence Length
- Mix short and long sentences
- One-sentence paragraphs for impact
- NOT every sentence same length (AI tells)

#### Use Specific Examples (Not Generic)
- BAD: "Many people find it helpful"
- GOOD: "A 2021 study on 50 adults showed 30% reduction in cortisol after 8 weeks"
- BAD: "It supports immune health"
- GOOD: "My aunt took Giloy throughout flu season last year — didn't catch a single cold"

### C. Avoid These AI Tells (Absolute Prohibitions)

Never use:
- "Nestled in the heart of..." (location descriptions)
- "Let's dive in" / "Let's explore"
- "In the realm of..."
- "From ancient times to modern day..."
- "Harness the power of..."
- "Embark on a journey..."
- "Unlock the secrets..."
- "In this article, we will..."
- "It's worth noting that..."
- "When it comes to..."
- "Picture this:" (as forced scene setup)
- "Consider this:" (as fake engagement)
- "The bottom line is..."
- "At the end of the day..."
- "In a nutshell..."

### D. Beautiful Prose Rules (Optional Enhancement)

When high-quality prose is needed, load `beautiful-prose` skill:
- Prefer concrete nouns over abstractions
- Prefer strong verbs over adverbs
- Short sentences for impact
- Declarative sentences preferred
- No therapy/validation language ("I hear you", "give yourself grace")
- Open with substance, not a hook
- Close cleanly without summary

---
## 7. SEO & Multi-Platform Optimization

Har article mein yeh SEO + multi-platform elements must hain.

### A. Keyword Usage
| Element | Rule |
|---------|------|
| Primary keyword in H1 | Yes — naturally, first 60 chars |
| Primary keyword in first 100 words | Yes — naturally |
| LSI/semantic keywords | 3-5 throughout article |
| Keyword density | 0.5-1.5% (not more, not less) |
| Keyword in at least 2 H2s | Yes |
| Keyword in meta description | Yes — 150-160 chars |

### B. Internal Linking (CRITICAL RULE FOR NEXT.JS)
- Link to 2-4 existing related articles on the site.
- **ALWAYS use clean relative URLs:** `/articles/slug-name` (e.g., `/articles/ashwagandha-benefits`).
- For glossary terms use `/glossary`, for canonical texts use `/canonical-texts`, and for dosha quiz use `/dosha-quiz`.
- Use descriptive anchor text (not "click here").
- Priority: link to pillar pages, then other cluster articles.

### C. Schema Markup (JSON-LD)
Add schema type based on article content:
| Article Type | Schema to Add |
|-------------|---------------|
| Standard blog post | Article |
| How-to guide | HowTo |
| Product review/herb guide | Product + Review |
| FAQ article | FAQPage |
| Recipe (Ayurvedic DIY) | Recipe |

### D. Image Optimization
- At least 1 featured image per article (Append a request to `data/tracking/manual-image-requests.txt`).
- See `docs/13-image-generation-guide.md` for manual image request rules.
- Alt text includes keyword naturally
- Filename: keyword-separated-by-hyphens.jpg
- Compress images (use TinyPNG or similar)

### E. URL Slug
- Derived automatically from title
- Keep short (3-5 words max)
- Include primary keyword
- No stop words (a, an, the, and, of, for)

### F. Open Graph & Twitter Cards
| Tag | Required? | Value |
|-----|-----------|-------|
| `og:title` | Yes | Same as meta title (60 chars) |
| `og:description` | Yes | Same as meta description (160 chars) |
| `og:image` | Yes | Featured image URL (1200x628) |
| `og:url` | Yes | Canonical article URL |
| `og:type` | Yes | `article` |
| `twitter:card` | Yes | `summary_large_image` |
| `twitter:title` | Recommended | Same as og:title |
| `twitter:description` | Recommended | Same as og:description |
| `twitter:image` | Recommended | Same as og:image |

- Rendered via Next.js metadata API in static exports
- Manually verify using [metatags.io](https://metatags.io) or Facebook Sharing Debugger

### G. External Linking / Citation Rules
- **Minimum:** 2-3 external links per article from high-DR sources (DR 70+)
- **Preferred Sources:** PubMed, NCBI, NIH, Harvard Health, Mayo Clinic, WebMD, Cleveland Clinic
- **PubMed Auto-Fetch:** Use `python3 scripts/pubmed-cite.py '<keyword study trial>' 3` to auto-fetch PubMed citations with PMID + DOI links — free, no API key needed
- **Link Behavior:** Open in new tab (`target="_blank"`), `rel="noopener noreferrer nofollow"`
- **Citation Placement:** Link specific claims directly — not just a "References" section dump
- **E-E-A-T Strategy:**
  - Health claims → Cite PubMed/NCBI study
  - Statistics → Cite original source (not third-party repost)
  - Ayurvedic concepts → Cite classical text (Charaka Samhita, Sushruta Samhita) or modern commentary

### H. Bing SEO Optimization
- **Bing Webmaster:** Site registered. API key in `secrets/bing-client-credentials.json`
- **Sitemap Submit:** `python3 scripts/bing-sitemap-submit.py` — submits sitemap to Bing ping
- **URL Submit:** `python3 scripts/bing-sitemap-submit.py --url ARTICLE_URL` — submits single URL via IndexNow
- **Auto-Submit:** `scripts/schedule-posts.py` calls Bing IndexNow automatically after each scheduled post
- **Clean HTML:** Avoid JavaScript-rendered content — Bing's crawler is less JS-capable than Google
- **Explicit meta description:** Bing uses meta description heavily for snippets — make it compelling
- **Bing favicon:** Ensure site favicon is set (Bing shows it in search results)
- **Backlinks matter more on Bing** than Google — prioritize getting 2-3 niche-relevant backlinks per pillar article

### I. Perplexity AEO Optimization
Perplexity extracts and cites content differently than Google. Optimize specifically for Perplexity:

| Rule | Why | Implementation |
|------|-----|---------------|
| **Fact-dense paragraphs (5-7 tokens)** | Perplexity answers are short (5-7 token snippets) | Make first sentence of each H2 section a standalone fact — max 10 words |
| **Freshness matters more** | Perplexity heavily weights recent content | Include "Updated [Month Year]" tag. Refresh articles every 60 days |
| **Reddit cross-presence** | 46.7% of Perplexity sources are Reddit | Link to relevant Reddit discussions. Participate in Ayurveda subreddits |
| **Direct answers to questions** | Perplexity answers user queries directly | Every H2 should answer one specific question. Avoid tangential content |
| **No paywalls / login gates** | Perplexity cannot access gated content | Ensure entire article is readable without authentication |
| **Structured data matters** | Perplexity uses schema for rich answers | FAQPage, HowTo, Article schema always present |

### J. ChatGPT Search Optimization
ChatGPT Search cites web content when it needs real-time info. Optimize for retrieval:

| Rule | Why | Implementation |
|------|-----|---------------|
| **Listicle format preferred** | 43.8% of ChatGPT citations are listicles | Include at least one numbered list or bullet list per article |
| **Clean HTML** | ChatGPT parses HTML structure for citations | No hidden divs, no broken tags, clean heading hierarchy (H1→H2→H3) |
| **First 100 words = extract** | ChatGPT often cites opening paragraph | First 100 words must contain the answer + keyword naturally |
| **Existing indexation required** | ChatGPT only cites already-indexed pages | Article must be indexed by Google/Bing first (wait 48h before expecting citations) |
| **No UGC as primary source** | ChatGPT rarely cites user-generated content | Avoid forum-style content. Must be authoritative guide format |
| **Authoritative tone** | ChatGPT prefers .org/.edu but cites high-quality blogs | Use "Studies show" rather than "I think". Cite PubMed/NIH |

### K. Google AI Overviews Optimization
Google AI Overviews pull from organic top 20. Optimize for extraction:

| Rule | Why | Implementation |
|------|-----|---------------|
| **Rank in organic top 20** | 97% of AI Overviews citations come from top 20 | Must achieve top 20 ranking for target keyword |
| **Featured snippet = 2x citation** | Pages with featured snippets cited twice as often | Target "what is", "how to", "benefits" queries for snippet format |
| **Clear definition sentences** | AI Overviews extract definitions for intro | First H2 sentence MUST be a definition: "[Topic] is [category] that [function]" |
| **Question-answer format** | AI Overviews answer user questions directly | Structure H2s as questions. FAQ section is critical |
| **High-authority backlinks** | AI Overviews prefer E-E-A-T signals | Minimum 3 external citations to PubMed/NIH per article |

### L. AI Crawler & llms.txt Configuration
Ensure AI crawlers can access your content:

```
# robots.txt — ALLOW AI crawlers (don't block)
User-agent: GPTBot
Allow: /

User-agent: Google-Extended
Allow: /

User-agent: Claude-Web
Allow: /

User-agent: CCBot
Allow: /

User-agent: PerplexityBot
Allow: /
```

- **llms.txt file:** Create `llms.txt` at site root (for Claude, ChatGPT knowledge retrieval)
- **Structure:** Simple markdown file listing site name, description, and key article links
- **Verify:** Run article URL through each platform's testing tool

---
## 8. AEO (AI Engine Optimization) Rules

AI engines (ChatGPT, Perplexity, Gemini) yahi content extract karte hain:

### A. TL;DR Block (Critical for AEO)
- First extractable block AI picks up
- Must be a direct answer to the searcher's question
- 2-3 sentences, self-contained

### B. Definition Sentence
- Right after each H2, first line must be a clean definition
- Example: *Triphala is a traditional Ayurvedic herbal formulation made from three fruits: Amla, Haritaki, and Bibhitaki.*
- AI engines extract definition sentences for feature snippets

### C. FAQ Section
- 5 questions maximum
- Each answer under 50 words
- Each answer standalone (AI extracts individual Q/A pairs)
- Questions = long-tail keywords people voice-search

### D. Comparison Table
- When comparing products/methods, use a markdown table
- AI engines extract tables into rich results
- Example: Ashwagandha vs Brahmi — benefits, dosage, side effects

### E. Bullet Lists
- Use `-` bullets for scannable lists
- AI extracts lists for "list of" queries

---
## 9. Readability Rules

| Metric | Target |
|--------|--------|
| Reading grade level | 8-10 (Flesch-Kincaid) |
| Average sentence length | 15-20 words |
| Paragraph max | 3-4 sentences |
| Active voice ratio | > 90% |
| Transition words | Natural use, not forced |
| Subheading frequency | Every 200-300 words |

### Formatting Rules
- Short paragraphs (2-3 sentences max)
- White space between sections
- Bold only for key terms (1-2 per section max)
- No ALL CAPS
- Quotes: Use `>` for emphasis sparingly
- Code blocks: Only for actual code or command scripts

---
## 9B. Platform-Specific Writing Rules

Har platform ka apna content preference hota hai. Article likhte time in rules ko apply karo:

### A. Google Organic Writing Rules
| Rule | Detail |
|------|--------|
| **E-E-A-T Signals** | Author byline + bio. External citations (3+). Medical disclaimer. Last-updated date |
| **Snippet Optimization** | First 100 words = direct answer. Use H2 for question. Bullet/list format for "benefits" queries |
| **Content Depth** | Minimum 1500 words. Cover topic comprehensively. No thin content |
| **Internal Linking** | 2-4 links to existing articles. Link to pillar pages for topical authority |

### B. Bing Organic Writing Rules
| Rule | Detail |
|------|--------|
| **Meta Description** | Bing uses meta desc heavily for snippets — write compelling 150-160 char description |
| **Explicit Headings** | Bing prefers descriptive H2s. Use question-based H2s (e.g., "What Are the Benefits of Ashwagandha?") |
| **Clean HTML** | Avoid JavaScript-heavy rendering. Bing's crawler is less JS-capable |
| **Backlink Signal** | Backlinks matter more on Bing than Google. Prioritize 2-3 niche backlinks per article |

### C. Google AI Overviews Writing Rules
| Rule | Detail |
|------|--------|
| **Top 20 Ranking** | AI Overviews only cite pages in organic top 20 — must rank first |
| **Definition Sentence** | Every H2's first sentence must be a clean, extractable definition |
| **Question-Answer Format** | Structure content to answer specific user questions directly |
| **Featured Snippet** | Pages with featured snippets are cited 2x more. Target snippet-optimized queries |

### D. ChatGPT Search Writing Rules
| Rule | Detail |
|------|--------|
| **Listicle Sections** | Include at least one numbered list (e.g., "Top 5 Benefits"). 43.8% of ChatGPT citations are listicles |
| **Clean HTML Structure** | H1 → H2 → H3 hierarchy. No broken tags. No hidden content |
| **Authoritative Tone** | Use "Studies show" / "Research indicates" — not "I think" |
| **Existing Indexation** | Article must be indexed by Google/Bing before ChatGPT will cite it |
| **Fact-Dense Intro** | First 100 words must contain the core answer + supporting fact |

### E. Perplexity Writing Rules
| Rule | Detail |
|------|--------|
| **Short Fact Snippets** | Perplexity extracts 5-7 token snippets. First sentence of each section = standalone fact |
| **Freshness Signal** | Include "Updated [Month Year]" in article. Refresh content every 60 days |
| **Reddit Cross-Reference** | Link to relevant Reddit discussions. 46.7% of Perplexity sources are Reddit |
| **No Fluff** | Perplexity penalizes irrelevant content. Every paragraph must add value |
| **Direct Answers** | Each H2 should directly answer one specific question. No tangents |

### F. AI Crawler Compatibility
| Rule | Detail |
|------|--------|
| **robots.txt** | Allow GPTBot, Google-Extended, Claude-Web, CCBot, PerplexityBot |
| **llms.txt** | Create `llms.txt` at site root listing key articles for AI knowledge retrieval |
| **Server-Side Rendering** | Ensure content is visible without JavaScript |
| **No Login Walls** | Full article must be readable without authentication |

---
## 10. Pre-Publish Quality Checklist (16/16 Gate)

Article tabhi **queue mein jayega** jab yeh 16/16 pass kare:

```
[ ] 0. Labels match article category — `labels` array has correct menu category label(s):
    - Ayurvedic Herbs (if herb-specific: brahmi, ashwagandha, triphala, turmeric, giloy, shatavari, etc.)
    - Individual herb name as sub-label (e.g., "Ashwagandha", "Brahmi", "Giloy") — for All Herbs sub-menu links
    - Brain Health (if brain/memory/cognition)
    - Men's Health (if men/male/testosterone)
    - Women's Health (if women/pcos/female/hormonal)
    - Dog Health (if dog/canine/pet)
    - Natural Remedies (if general health: gut, digestion, allergy, joint, anxiety, etc.)
    CRITICAL: Without this, the category page stays EMPTY and no one finds the article.
[ ] 1. Featured image present — post content me <img> tag hai? (Ya manual-image-requests.txt me entry hai?)
[ ] 2. TL;DR block present — <blockquote><strong>TL;DR:</strong> ke baad 2-3 sentence?
[ ] 3. FAQ section — exactly 5 Q&A pairs with <h3> headings?
[ ] 4. FAQPage JSON-LD schema — <script type="application/ld+json"> with FAQPage present?
[ ] 5. Human touch audit — avoid-ai-writing se 0 AI patterns detected?
[ ] 6. Internal links — 2-4 links to other ayurshakti.shop articles?
[ ] 7. H2/H3 structure — 5-8 H2 sections with H3 subsections?
[ ] 8. Word count ≥ 1500 — body text minimum?
[ ] 9. Primary keyword in H1 + first 100 words?
[ ] 10. No banned phrases — "The Bottom Line", "In conclusion", etc removed?
[ ] 11. Medical disclaimer present — <blockquote class="disclaimer"> with consult-doctor warning?
[ ] 12. PubMed citations fetched via `scripts/pubmed-cite.py` — 2-3 PMID links in article?
[ ] 13. Plagiarism check — Copyscape ya Quetext se unique verified?
[ ] 14. Bing sitemap submitted (`python3 scripts/bing-sitemap-submit.py`)? / robots.txt allows AI crawlers? llms.txt present?
[ ] 15. Multi-platform optimized — listicle format (ChatGPT), definition sentences (AI Overviews), fact-density (Perplexity)?
```

**16/16 pass → Push to approval-queue.json → Auto-scheduler picks up**
**< 16/16 → Fix issues and re-run checklist**

See `docs/11-article-approval-scheduler.md` for full scheduler rules.

---
## 11. Post-Schedule Steps

Article schedule hone ke baad:

### A. Internal Linking Update
- Go back to 2-3 older related articles
- Add a link FROM them TO this new article
- Use `seo-aeo-internal-linking` skill for optimized anchors

### B. Bing Sitemap Submit
- Run: `python3 scripts/bing-sitemap-submit.py` to submit `atom.xml` to Bing
- Or use `--url ARTICLE_URL` for IndexNow single-URL submission
- Auto-submit already happens in `schedule-posts.py` — this is for manual runs

### C. Schema Validation
- Run article URL through Google Rich Results Test
- Fix any schema errors

### D. Backlink Building (After Publish)
- See `docs/12-backlink-strategy.md` for full Phase 1/2/3 plan
- **Phase 1 (AI Agent):** Quora answer, Reddit post, Medium republish, Pinterest pin within 48h of publish
- **Phase 2 (API):** `notify-ping.py` fires automatically, IndexNow already running
- **Phase 3 (Manual):** HARO pitch if topic is newsworthy, guest post pitch if pillar page

### E. Performance Check (After 7 Days)
- Check GA4 for traffic to new article
- Check Search Console for impressions/clicks
- If no impressions after 14 days → revisit title and meta description

### E. Content Refresh Schedule
| Timeframe | Action |
|-----------|--------|
| 1 month | Check ranking, update if needed |
| 3 months | Add new data/stats if available |
| 6 months | Full content refresh with latest info |
| 12 months | Major update or consolidate with related article |

---
## 12. Article Output Format

Agent jab article complete karega, yeh format use karega:

```markdown
## Article Complete

| Field | Value |
|-------|-------|
| **Title** | Triphala for Weight Loss: How This Ayurvedic Formula Burns Belly Fat |
| **Word Count** | 2,450 |
| **Target Keyword** | triphala for weight loss |
| **Category** | Weight Loss / Herbs & Supplements |
| **Primary Skill Used** | seo-aeo-blog-writer |
| **Human Touch Audit** | avoid-ai-writing — 0 patterns detected |
| **SEO Score** | 92/100 |
| **AEO Score** | 88/100 |
| **Readability Score** | Grade 9 |
| **Internal Links** | 3 (link1, link2, link3) |
| **Schema Added** | Article + FAQPage |
| **Ready to Publish** | Yes |
```

---
## 13. Workflow Summary (Quick Reference)

```
                       ┌──────────────────────────┐
                       │ USER: Write              │
                       │ Article on Topic         │
                       └──────────┬───────────────┘
                                  │
                       ┌──────────▼───────────────┐
                       │ STEP 0: Multi-Platform   │
                       │ Pre-Write Check          │
                       │ - Check Google updates   │
                       │ - Check Bing indexation  │
                       │ - Check ChatGPT/Perplex  │
                       │   ity/Gemini policy      │
                       │ - Check AI crawler rules │
                       │ - Auto-adjust per platfrm│
                       └──────────┬───────────────┘
                                  │
                       ┌──────────▼───────────────┐
                       │ Load Skills              │
                       │ - seo-aeo-blog-writer    │
                       │ - avoid-ai-writing       │
                       │ - etc.                   │
                       └──────────┬───────────────┘
                                  │
                       ┌──────────▼───────────────┐
                       │ Research Phase           │
                       │ - Competitor articles    │
                       │ - LSI keywords           │
                       │ - Long-tail Qs           │
                       │ - Platform viability     │
                       └──────────┬───────────────┘
                                  │
                      ┌───────────▼───────────────┐
                      │ Write Draft               │
                      │ - H1 + TL;DR              │
                      │ - 5-8 H2 sections         │
                      │ - 5 FAQ entries           │
                      │ - Conclusion              │
                      └───────────┬───────────────┘
                                  │
                      ┌───────────▼───────────────┐
                      │ Human Touch Pass          │
                      │ - avoid-ai-writing audit  │
                      │ - Add stories             │
                      │ - Conversational tone     │
                      └───────────┬───────────────┘
                                  │
                      ┌───────────▼───────────────┐
                      │ Multi-Platform Opt Pass   │
                      │ - Google SEO (keywords,   │
                      │   schema, meta, links)    │
                      │ - Bing SEO (clean HTML,   │
                      │   meta desc, sitemap)     │
                      │ - ChatGPT (listicle fmt,  │
                      │   clean hierarchy)        │
                      │ - AI Overviews (def sent, │
                      │   top 20 ranking strat)   │
                      │ - Perplexity (fact snip,  │
                      │   freshness, direct ans)  │
                      └───────────┬───────────────┘
                                  │
                       ┌──────────▼───────────────┐
                       │ Quality Check            │
                       │ - 15/15 checklist        │
                       │ - Disclaimer check       │
                       │ - Citations check        │
                       │ - Platform gate check    │
                       └──────────┬───────────────┘
                                  │
                       ┌──────────▼───────────────┐
                       │ Gate: Pass 15/15?        │
                       │ No → Fix & retry         │
                       │ Yes → Queue              │
                       └──────────┬───────────────┘
                                  │
                       ┌──────────▼───────────────┐
                       │ Approval Queue           │
                       │ scripts/approval-queue   │
                       │ .json                    │
                       └──────────┬───────────────┘
                                  │
                       ┌──────────▼───────────────┐
                       │ Auto-Scheduler           │
                       │ schedule-posts.py        │
                       │ (every 12h)              │
                       │ - Pick 2 random          │
                       │ - Best time EST          │
                       │   8-10am / 6-8pm         │
                       │ - Static site build      │
                       │   future publish         │
                       └──────────┬───────────────┘
                                  │
                       ┌──────────▼───────────────┐
                       │ Post-Schedule            │
                       │ - Schema validate        │
                       │ - Update old int links   │
                       │ - Submit sitemap Bing    │
                       │ - Track after 7 days     │
                       │   (per platform)         │
                       └──────────────────────────┘
```

---
## 14. Version History

| Date | Changes |
|------|---------|
| 2026-07-07 | Initial creation — Shiva's master config for AI article writing with human touch |
| 2026-07-07 | Added article type templates (5), OG tags + citation rules (7), 13/13 checklist (10). New sections 15-18: Disclaimer, Brand Voice, Media/TOC/Author, Content Mix |
| 2026-07-07 | Updated publishing strategy to 3-5/day with phase-based scaling (Section 18). Added RSS Feed Check step in Pre-Writing (Section 4B). Added Cannibalization Audit (Section 18E) + Quality Gate Volume Strategy (Section 18F). |
| 2026-07-07 | Added Section 0: Pre-Write Algorithm Check (Auto-Adjust) — Google update detection + auto-writing strategy adjustment. Updated Workflow diagram. |
| 2026-07-07 | Section 0 expanded to Multi-Platform Pre-Write Check (Google + Bing + ChatGPT/Perplexity + AI crawlers). Section 7 renamed to SEO & Multi-Platform Optimization — added 5 new subsections (Bing SEO, Perplexity AEO, ChatGPT Search, Google AI Overviews, AI Crawler/llms.txt). New Section 9B: Platform-Specific Writing Rules (6 platforms). Section 10: 13/13 → 15/15 Gate. Workflow diagram updated with Multi-Platform Optimization Pass. |
| 2026-07-07 | Bing credentials saved to `secrets/bing-client-credentials.json`. `scripts/bing-sitemap-submit.py` created. Section 7H updated with script commands + creds reference. Section 10 checklist item 14 updated with explicit script call. Section 11B added (Bing Sitemap Submit step). `llms.txt` deployed via Cloudflare Worker at `llms.ayurshakti.shop/llms.txt`. robots.txt updated with AI crawler rules + llms.txt. |
| 2026-07-07 | Site audit completed. Fixed Google "Duplicate without user-selected canonical" — JS redirect injected in theme `ayurshakti.xml` (`?m=0/?m=1` → canonical). Sitemap `atom.xml` submitted to GSC (0 errors). Cron setup: `0 0,12 * * *` for auto-scheduler. |
| 2026-07-07 | Added `docs/12-backlink-strategy.md` — Phase 1/2/3 backlink architecture. Created `notify-ping.py`, `social-post.py`, `monitor-mentions.py`. Integrated into auto-pipeline. |
| 2026-07-07 | Created `config/profile.json` — centralized site/author/contact config. Refactored all 5 scripts. Replaced email from cPanel to Gmail (contact@ → App Password). Rewrote MCP email server for Gmail IMAP/SMTP. |

---

## 15. Medical Disclaimer & Affiliate Disclosure (YMYL Compliance)

Health niche (YMYL) hone ki wajah se legal compliance CRITICAL hai. Har article mein yeh sections must hain.

### A. Medical Disclaimer Template

```html
<blockquote class="disclaimer">
<strong>⚠️ Medical Disclaimer:</strong> The information on this website is for informational and educational purposes only. 
It is not a substitute for professional medical advice, diagnosis, or treatment. Always consult a qualified 
healthcare provider before starting any supplement, herb, or Ayurvedic treatment, especially if you are pregnant, 
nursing, have a medical condition, or are taking prescription medications.
</blockquote>
```

**Placement Rules:**
- **Must appear:** Right before Conclusion section
- **Optional:** Also after TL;DR for high-stakes topics (dosage, disease management)
- **Format:** Blockquote with `class="disclaimer"` for consistent styling

### B. Affiliate Disclosure Template

```html
<p class="affiliate-disclosure">
<em>Disclosure:</em> Some links on this page are affiliate links. We may earn a small commission at no extra cost 
to you if you make a purchase through these links. We only recommend products we have researched and believe add 
value to our readers.
</p>
```

**Placement Rules:**
- **Must appear:** If article contains ANY affiliate links
- **FTC requires:** "clear and conspicuous" disclosure — place near top of article (after TL;DR or after first affiliate link)
- **Format:** Italic, smaller text, `class="affiliate-disclosure"`

### C. Prohibited Medical Claims (Legally Binding)
- ❌ "Cures [disease]" — illegal without FDA approval
- ❌ "Treats [condition]" — claim requires clinical evidence
- ❌ "Replace your medication" — dangerous
- ❌ "Guaranteed results" — can't guarantee
- ✅ Instead say: "May support", "Traditionally used for", "Some studies suggest"

### D. E-E-A-T Author Attribution
- Har article mein byline hona chahiye: "By [Name]" ya "Reviewed by [Name]" at top
- Author bio should show credentials (if medical professional)
- No author = low E-E-A-T signal to Google

---

## 16. Brand Voice & Tone Guide

AyurShakti.shop ka ek **distinct brand voice** hona chahiye — consistent across all articles.

### Voice Pillars

| Pillar | What It Means | Example |
|--------|--------------|---------|
| **Warmly Authoritative** | Expert-like but not cold. Knows Ayurveda deeply but explains in simple terms | "Ayurveda 5000 saal se yeh kehta aa raha hai — aur main personally isko patients mein effective dekha hai." |
| **Conversational Hinglish** | Natural Hindi-English mix. NOT formal, NOT slangy | "TOH yeh raha asli sawaal — kaise kaam karta hai Ashwagandha? Chaliye samajhte hain." |
| **Honest & Balanced** | Don't overhype. Mention both benefits AND side effects. Builds trust. | "Ashwagandha generally safe hai, but kuch logon ko mild side effects ho sakte hain." |
| **Action-Oriented** | Every article should give the reader something to DO | "Kal subah uthke 1 tsp Triphala powder gungune paani ke saath le kar dekhiye." |

### Tone Levels by Context

| Context | Tone | Example |
|---------|------|---------|
| Herb benefits | Enthusiastic but factual | "Ashwagandha ka ek unique benefit — yeh cortisol ko naturally reduce karta hai." |
| Side effects / warnings | Cautious, direct | "Important: pregnancy mein Ashwagandha avoid karein. Yeh uterine contractions trigger kar sakta hai." |
| How-to / Dosage | Instructional, clear | "Step 1: 1/2 tsp Triphala powder lein. Step 2: Garam paani mein mix karein. Step 3: Sone se 1 ghanta pehle piyen." |
| Personal story | Warm, relatable | "Mere ek client ko 3 saal se acidity thi. Triphala ne 2 hafte mein farak dikha diya." |
| FAQ | Direct, concise | "Q: Kya Triphala khali pet lena chahiye? A: Haan — subah khali pet ya raat ko sone se pehle." |

### Brand Personality (If AyurShakti was a person)
- **Age:** 35-45 (experienced, not old)
- **Vibe:** Knowledgeable elder brother / didi who's lived abroad but knows desi nuskhe
- **Education:** Studied Ayurveda (not just Google-certified)
- **Communication:** "Main personally yeh recommend karta hoon" — takes ownership
- **NOT:** Corporate blog, textbook, Wikipedia, chatbot

### Banned Brand Voice Patterns
- ❌ Corporate speak ("Our solution", "leverage", "synergy")
- ❌ Clickbait tone ("You won't believe what happens next!")
- ❌ Desperate tone ("Buy now!", "Limited offer!")
- ❌ Overly academic ("Furthermore, it is posited that...")
- ✅ Authentic tone you'd use with a friend asking for health advice

---

## 17. Media Guidelines, TOC & Author Bio

### A. Image Sourcing & Attribution

| Source | License Type | Attribution Required? | Best For |
|--------|-------------|---------------------|----------|
| Canva (Pro) | Royalty-free | No (with Pro license) | Featured images, infographics, social graphics |
| Unsplash | Free (Unsplash license) | No, but appreciated | Blog inline images, backgrounds |
| Pexels | Free (Pexels license) | No | Blog inline images |
| Custom (Canva Design) | Owned | N/A | Infographics, comparison charts, dosage tables |
| AI-generated (DALL-E/Midjourney) | Varies | Check platform TOS | Unique herb illustrations |

**Image Rules:**
- No copyright images (Google Images directly downloaded = lawsuit risk)
- No watermarked images
- All images must be compressed (TinyPNG or Canva export → compressed)
- Supported formats: JPEG (photos), PNG (graphics), WebP (preferred for speed)

### B. Article Image Requirements

| Image Type | Min Size | Placement | Notes |
|-----------|---------|-----------|-------|
| **Featured Image** | 1200x628px | Top of article (og:image) | Keyword in filename, keyword in alt text |
| **Infographic** | 800x2000px | After TL;DR or after intro | Canva template, branded with AyurShakti logo |
| **Inline Image 1** | 800x600px | Near first H3 | Relevant to first sub-topic |
| **Inline Image 2** | 800x600px | Mid-article | Break up text, relevant to content |
| **Comparison/Schema Image** | 600x800px | In comparison table section | Optional, if applicable |

### C. Table of Contents (TOC) for Long Articles

Articles > 2500 words mein TOC add karo:

```html
<details class="toc">
<summary><strong>📖 Table of Contents</strong></summary>
<ul>
  <li><a href="#what-is">What Is Ashwagandha?</a></li>
  <li><a href="#benefits">Benefits of Ashwagandha</a></li>
  <li><a href="#dosage">How to Take Ashwagandha</a></li>
  <li><a href="#side-effects">Side Effects</a></li>
  <li><a href="#faq">FAQ</a></li>
</ul>
</details>
```

- Use HTML anchor IDs in H2s: `<h2 id="what-is">What Is Ashwagandha?</h2>`
- Keep TOC collapsible (`<details>` tag)
- Place TOC right after TL;DR block

### D. Author Bio Template

```html
<div class="author-bio">
<strong>About the Author:</strong> [Name] is an Ayurvedic wellness researcher and content creator at 
AyurShakti.shop. With [X years] of experience in natural health, [he/she/they] writes evidence-based 
articles to help people achieve better health through Ayurveda.
</div>
```

- Place after Conclusion, before Disclaimer
- Add Google E-E-A-T signal: link to author's Google Scholar / LinkedIn if available
- If guest author: mention "Reviewed by [Medical Professional]" with credentials

### E. Related Posts Block

End of article mein 3-5 related articles link karo:
- Internal linking boost
- User engagement (lower bounce rate)
- Format: bullet list with mini-descriptions

```markdown
**📚 Also Read:**
- [Triphala for Weight Loss: Complete Guide](/blog/triphala-for-weight-loss)
- [Ashwagandha Benefits for Men](/blog/ashwagandha-for-men)
- [Best Time to Take Ashwagandha](/blog/best-time-to-take-ashwagandha)
```

---

## 18. Content Mix Strategy

### A. Evergreen vs Trending Ratio

| Article Type | % of Total | Examples | Refresh Frequency |
|-------------|-----------|---------|------------------|
| **Evergreen (Herb Guides)** | 50% | Ashwagandha guide, Triphala benefits | 12 months |
| **Evergreen (Condition Guides)** | 20% | PCOS diet, diabetes management | 6-12 months |
| **Seasonal** | 15% | Winter immunity, summer skin care | Per season |
| **Trending / Newsjack** | 10% | New study on Ashwagandha, celebrity using Ayurveda | Once (news value) |
| **Comparison / "vs" Articles** | 5% | Ashwagandha vs Shilajit | 12 months |

**Rule:** Pehle 3 months sirf **Evergreen (Herb + Condition)** articles likho — inki shelf life sabse lambi hoti hai. 3 months ke baad seasonal + trending start karo.

### B. Content Recycling Rules

Purane articles ko zinda rakhne ke liye:

| Strategy | When | How |
|----------|------|-----|
| **Content Refresh** | Every 6-12 months | Update stats, add new studies, freshen examples, update year |
| **Content Merge** | When multiple thin articles exist on same keyword | Merge into 1 comprehensive pillar, 301 redirect rest |
| **Content Repurpose** | After article is 3+ months old | Convert → YouTube script, infographic, Twitter thread, newsletter |
| **Internal Link Update** | Every 3 months | Add links FROM old articles TO new articles (and vice versa) |
| **Schema Update** | When Google adds new schema types | Add new structured data for better SERP features |

### C. Article Silos / Topical Authority

Articles ko topical silos mein organize karo. Google ko dikhe ki tum specific topics mein expert ho:

```
Silo: Ashwagandha
├─ Pillar: Ashwagandha Complete Guide
├─ Cluster: Ashwagandha for Men
├─ Cluster: Ashwagandha for Women  
├─ Cluster: Ashwagandha Dosage
├─ Cluster: Ashwagandha vs Shilajit
└─ Cluster: Ashwagandha Side Effects

Silo: Triphala
├─ Pillar: Triphala Complete Guide
├─ Cluster: Triphala for Weight Loss
├─ Cluster: Triphala for Digestion
└─ Cluster: Best Time to Take Triphala
```

### D. Publishing Strategy (3-5/Day)

| Phase | Focus | Articles/Day | Articles/Month | Goal |
|-------|-------|-------------|---------------|------|
| **Month 1** (Warmup) | Herb pillars + clusters (Ashwagandha, Triphala, Giloy, Shilajit) | 2-3 | 60-90 | Establish topical authority |
| **Month 2-3** (Scale) | Health condition pillars (PCOS, weight loss, digestion, immunity) + filler | 3-4 | 90-120 | Capture high-volume health queries |
| **Month 4+** (Sustain) | Seasonal + trending + consolidated + refresh old | 4-5 | 120-150 | Maintain authority + scale revenue |

### E. Cannibalization Audit (Weekly — Sundays)

Because 3-5/day = 90-150 articles/month:

1. Run `seo-cannibalization-detector` skill (from skill-library)
2. Check: koi 2 articles same primary keyword target toh nahi kar rahe?
3. If found: merge into one comprehensive article, 301 redirect the other
4. Log audit results in performance tracker

### F. Quality Gate Volume Strategy

| Check | Frequency | Tool/Skill |
|-------|-----------|------------|
| Cannibalization | Weekly (Sun) | `seo-cannibalization-detector` |
| 15/15 Checklist | Per article | Manual gate |
| SEO Score | Per article | `seo-aeo-content-quality-auditor` (min 85/100) |
| 7-day Performance | Per article | GA4 + Search Console |
| Monthly Refresh Check | Monthly | Identify articles below 30d benchmarks |

### G. Multi-Platform Content Strategy

Har article ko ek baar publish karke chhodna kaafi nahi — usse **multi-platform assets** mein repurpose karo:

| Platform | Asset Type | Conversion Method | Schedule |
|----------|-----------|-------------------|----------|
| **YouTube (Shorts)** | 60-sec explainer video | Extract top 3 benefits → shoot/script as short | 1 per week (pick best-performing article) |
| **Pinterest** | Infographic + Rich Pin | Convert key data points → Canva infographic (800x2000px) | 2 per week |
| **Reddit** | Discussion thread | Post question in r/Ayurveda → link to article as reference | 1 per week |
| **ChatGPT / AI Knowledge** | llms.txt entry | Add article to site's `llms.txt` for AI knowledge retrieval | Per publish |
| **Email Newsletter** | Teaser + link | Extract TL;DR + top benefit → send to list | 1 per week |
| **Twitter/X** | Quote card + link | Pull one surprising stat → image card | 2 per week |

**Content Repurpose Workflow:**
```
Article Published → Wait 48h for indexation
    │
    ├─ Create Pinterest infographic (Canva) → Pin to relevant board
    ├─ Write Reddit post (r/Ayurveda, r/herbalism) → Link to article
    ├─ Add to llms.txt on site root
    ├─ Schedule YouTube Short if article is top-10 traffic
    └─ Log repurposing in performance tracker
```

---
## 19. Markdown to HTML Auto-Conversion Rule

**CRITICAL RULE FOR ALL AI AGENTS:**
- AI agents MUST ALWAYS write articles in **Markdown format** (e.g., `**bold**`, `[link](url)`, `## Heading`, `* list`).
- DO NOT attempt to write raw HTML in the article draft.
- The system's content pipeline renders Markdown articles directly into clean React HTML components during `npm run build` static export.
- Do NOT use complex Markdown that cannot be translated to standard HTML (keep tables simple, use standard bullet lists).
