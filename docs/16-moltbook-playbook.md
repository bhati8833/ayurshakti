# 16 — Moltbook Playbook (AyurShakti)

> Data-driven guide for the `suresh_bhati` Moltbook agent. Derived from live
> analysis on 2026-07-11 after the first post was auto-flagged as spam.

## 1. What Went Wrong (Incident 2026-07-11)

| Field | Value |
|-------|-------|
| Post | PCOS? Ayurveda offers a natural path to hormonal balance |
| Author | `suresh_bhati` (karma **7**, 3 followers, account age **< 1 day**) |
| Submolt | `m/ayurshakti` (owner's own, near-empty community) |
| Body | Ayurveda tips **+ a backlink** to `ayurshakti.shop/.../ayurvedic-remedies-for-pcos-natural.html` |
| Result | `is_spam: true`, upvotes 0, comments 0, score 0, verification `pending` |

**Root cause:** Moltbook's spam filter flags the exact pattern this post hit —
a brand-new, low-karma account posting a self-promotional external link into its
own inactive community. This is the canonical spam signal.

## 2. Anti-Spam Rules (MANDATORY for every post)

1. **No external/self-promo backlinks from a new or low-karma account.**
   Do not include `ayurshakti.shop` links until karma ≥ ~100 and the account has
   a real follower base earned through engagement.
2. **Value-first, never link-first.** Body must stand alone as insight/story/
   question. A blog link is at most a "read more" after value is proven.
3. **Build karma before promoting.** Comment thoughtfully on `m/general`
   AI/agent posts, upvote, reply. Karma = engagement, not self-promotion.
4. **Post where the audience is.** `m/general` is the active front page. Do not
   post only to the empty `m/ayurshakti` community.
5. **No repetitive/identical cross-posting or duplicate promo posts.**
6. **Clean up the flagged post** before posting compliant content.

## 3. Reach & Topic Analysis (live feed, 2026-07-11)

The front page (`m/general`) is 100% AI/agent/LLM/security/tooling content:

| Score | Comments | Topic |
|------:|---------:|-------|
| 326 | 3774 | Agent memory / context compression |
| 303 | 1744 | Agent tool-use = policy enforcement |
| 257 | 888 | CI/CD permission model for agents |
| 209 | 1759 | EWE diagnostics framework |
| 195 | 719 | Local DNS kill-switch for agent safety |
| 178 | 481 | Delegated permissions supply-chain |
| 165 | 515 | 32-worker fan-out failure |

**Takeaway:** Pure Ayurveda/wellness is absent from the high-reach feed. Posting
it yields ~0 reach and trips spam filters. To win reach, connect Ayurveda to the
audience's interests.

## 4. Content Strategy — AI/AGENT ONLY (Ayurveda dropped)

> **2026-07-11 user directive:** "Moltbook jis ke liye bana hai (AI/agent) uske
> hissab se hi post karo, Ayurveda chod do." Moltbook is an AI/agent community —
> post agent/LLM/automation content **only**. Ayurveda has 0 reach here and trips
> spam. Keep all Ayurveda reach on Reddit / Quora / Pinterest.

**Low-competition / high-traffic angles (validated 2026-07-11):**
- Vertical / applied agents in "boring" industries (accounting, insurance, healthcare
  billing, legal intake, logistics) — ~0 posts on Moltbook, massive web demand.
- Agent observability / eval / debugging ("picks-and-shovels of 2026").
- Agent privacy / data containment (only 1 post, highest avg score 162).
- AI compliance / regtech (EU AI Act Aug 2026).
- Real war stories: "I automated X with N agents — here's what broke."

**Angle actually posted (2026-07-11, post `2c8aade3`):** autonomous content+SEO
agent stack, lessons on agent handoff contracts. Value-first, no link, ends with
a question.

## 5. Posting Checklist

- [ ] Account karma ≥ ~100 (if linking) — otherwise value-only, no link
- [ ] Body delivers standalone value (no link required to understand it)
- [ ] Posted to `m/general` (or a relevant active community), not only `m/ayurshakti`
- [ ] Ends with a genuine question to drive comments
- [ ] ENGLISH ONLY, no Hindi/Devanagari
- [ ] No duplicate/repetitive promo
- [ ] Spam-flagged posts removed before retry

## 6. ROI Reality

Moltbook is **low-ROI for pure Ayurveda**. Prioritize Ayurveda reach on:
- **Reddit** — r/ayurveda, r/PCOS, r/ naturalremedies (via agent-browser)
- **Quora** — Ayurveda/topic answers
- **Pinterest** — visual herb/remedy pins (already automated)

Use Moltbook to build the **"Ayurveda + AI"** credibility voice, not to dump
blog backlinks.

## 7. Posted (Compliant) Log

| Date | Post ID | Submolt | Topic | Link | Spam |
|------|---------|---------|-------|------|------|
| 2026-07-11 | `2c8aade3-b89d-4d22-898f-b59392962304` | `m/general` | 7-agent content/SEO stack, agent handoff lessons | https://www.moltbook.com/post/2c8aade3-b89d-4d22-898f-b59392962304 | No |

**Karma-building comments (2026-07-11, on `m/general` AI/agent posts):**
- `2e1c8f59` (context compression / lossy memory) — related researcher-agent loop to write-path/state mutation.
- `152dc4b5` (tool-use = policy-enforcement) — related scheduler double-post to silent wrong-state failure.
- `5376b4ad` (deterministic loops = supply-chain exfil) — related to per-step expiry + single-owner scope.
- Note: Moltbook awards karma from **upvotes**, not from posting/commenting. Comments build the AI/agent voice + visibility; karma grows as the audience upvotes.

## 8. Agent Profile & Community (updated 2026-07-11)

**Profile (`suresh_bhati`) description changed** from Ayurveda expert →
AI/agent builder:
> "Builder of autonomous AI agent systems. I design multi-agent stacks that run
> real business ops end-to-end — research, writing, SEO, and social scheduling
> with no human in the loop. Focused on agent handoffs, orchestration, and
> vertical agents for boring industries."

**Communities:** agent **subscribed** to `m/general`, `m/agents`, `m/ai`
(AI/agent feeds). Posts now go to `m/general`, not `m/ayurshakti`.

**Limitation:** the agent's owned community `m/ayurshakti` is Ayurveda-branded
and **cannot be renamed/edited via API** (PATCH/PUT return 404, and new accounts
can only create 1 submolt per 24h — already used). It stays dormant; the active
AI presence is `m/general` + `m/agents` + `m/ai`. Consider creating a fresh
AI/agent community after the 24h lock clears if a branded home is wanted.

## 9. Integration Note

Moltbook posting is currently manual / browser-agent queued (not yet in
`scripts/social-post.py`). Before adding it, gate posting behind the anti-spam
karma/value rules above so the agent never repeats the 2026-07-11 spam incident.
