# Go-To-Market Plan: Stealth Agency → Productized Service → Product

**Date:** July 2026
**Reads on:** `01-market-research.md` (wedge: raw talking-head footage → brand-locked short-form ads/shorts for DTC brands and performance agencies), `02-technical-feasibility.md` (COGS ≈ $2–4/video), `03-mvp-plan.md` (Claude-Code-as-editor internal tool, no web app, Drive intake, ≤10 min operator time per job).
**Operator:** Goutham, solo. No team, no budget to speak of, MVP finishing in 2–3 weeks.

---

## 1. Strategy Assessment: The Stealth-Agency-First Play

**The plan under review:** launch as a cheap, fast editing "agency." Never mention the automation. Run the agent internally, let real client feedback mature it, bank cash now, productize later.

### Verdict: correct strategy, with three modifications

This is the right play for a solo founder with this exact asset. Reasons it's right:

1. **It monetizes the MVP on day one.** The MVP plan explicitly frames v1 as "a scrappy internal tool that lets one person run a video editing agency where the editor is Claude Code." The agency wrapper *is* the MVP's natural commercial skin — no extra build needed.
2. **Clients pay for outcomes, not tools.** A DTC marketer paying $30/short does not care whether a human or an agent cut it; they care that it's on-brand, fast, and converts. Selling the outcome sidesteps the "is AI editing good enough?" objection entirely — they judge the video, not the pipeline.
3. **It buys the moat data.** The `corrections.md` learning loop (doc 03) only compounds with real revision notes from real brands. An agency funnel is the cheapest possible way to acquire that training data — clients literally pay you to generate it.
4. **Margin structure is absurd and forgiving.** At $2–4 COGS against $30–150 human-benchmark pricing, you can underprice every human competitor by 50–70% and still run 85–95% gross margins. You can afford to eat mistakes, redo jobs free, and over-deliver — luxuries a human-labor agency can't match.
5. **It defers the hardest competition.** As SaaS you'd fight OpusClip ($20M ARR, SoftBank), Mirage ($175M raised), Descript. As a cheap fast editing service you fight… freelancers on Upwork and $2,500/mo boutique shops. Much softer field.

### Honest stress-test: the risks

**Risk 1 — Delivery quality variance.** The pipeline will produce some bad edits, especially in month one (doc 03 targets <30% manual-rescue rate *by end of week 3*, meaning early on it's higher). As an "agency" your brand is only as good as the worst video you ship. **Mitigation:** the founder QC checkpoint is non-negotiable on every job for the first 90 days; never ship a draft you haven't watched; keep a "redo free, no questions" policy (it costs you $3, not $150). Price low enough that expectations start at "budget editor," then over-deliver on speed.

**Risk 2 — Agency work eating the product.** Classic trap: client work fills all available hours, the tool stagnates, and in 12 months you own a job, not a company. **Mitigation:** hard rule — *any manual rescue that happens twice becomes next weekend's pipeline fix*, per doc 03's weekly review question. Track operator-minutes per job religiously; if median hands-on time exceeds ~20 minutes for two consecutive weeks, stop selling and fix the pipeline. Cap at ~8 active clients until hands-on time is under 10 min/job. The agency is the test harness, not the business.

**Risk 3 — Mispriced expectations / scope creep.** Clients will ask for multicam, long-form, motion graphics — everything doc 03 scoped out. A human agency would say yes. **Mitigation:** publish a narrow menu (vertical shorts + hook variants, that's it) and decline everything else with "we specialize." Specialization reads as premium, not limitation.

**Risk 4 — Disclosure ethics.** See below.

**Risk 5 — Concentration/churn.** With 5–10 clients, losing two is a 20–40% revenue hit. Accept this; it's a feature of the phase. The point is learning velocity, not revenue durability.

### The disclosure question — recommended stance

Full stealth ("a human editor edits your videos") is a lie that can detonate later; full disclosure ("an AI edits everything") invites tire-kicking, price anchoring to $15/mo SaaS tools, and idea theft. **Recommended stance: truthful non-disclosure with an AI-forward framing available on demand.**

Concretely:
- Market yourself as **"an editing studio with a proprietary AI-assisted pipeline — that's how we're this fast and this cheap."** This is 100% true, explains your unbeatable turnaround/price (which will otherwise trigger suspicion), and pre-empts the "wait, is this AI?" gotcha.
- Never claim a human edited the video. Never invent a fake team ("our editors"). Use "we" for the studio, singular founder if asked.
- If a client directly asks "is this AI-edited?", answer honestly: "Yes — AI does the assembly, I direct and QC every frame. You're judging the output either way."
- Don't reveal the *architecture* (Claude Code, cutlists, skills). "Proprietary pipeline" is all anyone needs. The stealth applies to the how, not the what.
- Contractually: your terms should state work may be produced with AI-assisted tooling. This protects you with brands that have AI-content policies (some ad platforms and enterprises now require disclosure). Note the trust data from doc 01 cuts in your favor: the backlash is against *synthetic humans*, not AI-assisted editing of real footage. "Real footage, professionally finished" is the safe harbor — lean on it.

This stance costs you almost nothing commercially (2026 buyers expect good vendors to use AI) and removes the only existential PR risk of the stealth play.

### Recommended sequencing and transition triggers

**Phase 1 — Stealth agency (months 0–3).** Per-video and small-retainer deals, manual everything, founder QC on every job. *Goal: 8–12 paying clients, $3–6k MRR, <10 min operator time/job, revision median ≤1.*

**Phase 2 — Productized service (months 3–9).** Designjoy-style: public pricing page, fixed tiers, subscription billing (Stripe), async intake, 24–48h SLA. Still no product reveal beyond "AI-assisted pipeline." *Trigger to enter: pipeline handles ≥70% of jobs with zero manual rescue AND ≥5 clients on repeat monthly billing.* *Goal: $15–30k MRR, waitlist forming, operator time flat while volume 3–5x.*

**Phase 3 — Product / SaaS (months 9–18).** Reveal and productize: self-serve upload, brand-kit onboarding, the review UI (doc 03's v2), usage pricing. The agency becomes the "managed tier" at the top of the pricing page — keep it, it's high-margin and a sales channel. *Trigger to enter: (a) demand exceeding what one operator can QC (~30+ videos/day), (b) revisions-per-client trending toward zero (the brand model works without you), and (c) a clear self-serve segment appearing in the funnel (founder-shorts buyers who want $99/mo, not $500/mo).* Do **not** reveal earlier just because building in public is fun — the reveal resets your competitive position from "boutique studio" to "one of 30 AI editing startups," so do it when you have the case-study arsenal and revenue to be the credible one.

---

## 2. Positioning & Branding

### Positioning statement

**For** DTC brands and performance marketers who need a constant stream of on-brand short-form video, **who** are stuck choosing between slow expensive human editors ($50–150/asset, 48–72h turnaround) and generic clip tools that make everyone's content look the same, **[Studio]** is a productized video editing service **that** turns raw footage into finished, brand-locked ads and shorts in 24 hours at a fraction of freelancer cost. **Unlike** freelancers, agencies, and clip-SaaS, **we** maintain a living brand profile for every client — every correction you ever give us is remembered, so video #10 needs fewer notes than video #1, and nothing we ship ever looks like anyone else's content.

### Category framing

Frame as a **productized editing service** in public ("editing subscription," "your editing department, flat monthly rate"), and as a **creative-volume subscription** when selling to performance marketers ("ship 15–25 fresh ad variants a month without hiring"). Avoid "AI video tool" — that category anchors to $15–30/mo and invites comparison to OpusClip. You are competing with the $1,500–2,500/mo retainer line item, not the SaaS line item.

### Naming directions (quick checks: pronounceable, .com-or-.co plausibility, not colliding with doc-01 competitors)

| Name | Vibe | Quick check |
|---|---|---|
| **Cutlist** | Insider editing term, doubles as the product's core artifact | cutlist.co likely gettable; clean, technical, memorable — **top pick** |
| **Everyframe** | Quality promise ("we QC every frame") | Likely available; slightly long |
| **Hooksmith** | Performance-marketing native (hooks = the money object) | Strong for ICP-A; niche if you broaden |
| **Reelworks** | "Real/reel" pun, workshop feel | Check collisions with VFX houses named Realworks |
| **Brandcut** | Brand-locked + editing | Descriptive, a bit flat; likely available |
| **Offcut Studio** | Editing-room term, boutique feel | Distinctive; "offcut" = scraps, slight negative read |
| **Tempo Post** | Speed + post-production | "Post" signals industry credibility |
| **Shipshorts** | Verb-first, volume promise | Playful; may read low-end |

Recommendation: **Cutlist** (or Cutlist Studio). It's the rare name that works as agency now and product later, and you already own the concept internally.

### Taglines

- "Raw footage in. On-brand ads out. 24 hours."
- "Your brand's editing department — without the department."
- "Ship ads as fast as you shoot them."
- "Fresh creative, every week, never off-brand."

### Brand personality

Fast, precise, quietly confident, operator-to-operator. No AI hype language, no "revolutionary." Speak like a senior editor who answers email in minutes. Proof over adjectives: before/afters, turnaround screenshots, CPM numbers. Clean invoicing, no dark patterns — doc 01 showed the category's billing reputation is radioactive (OpusClip 22% one-star, Icon's cancel traps); being the trustworthy operator is free differentiation.

### Messaging pillars (mapped to doc-01 pains)

1. **Brand consistency** (the 94%/9% gap): "Every video looks like *you*. We keep a living profile of your brand — colors, fonts, caption style, and every note you've ever given us." Proof: side-by-side of client's video vs. generic OpusClip output.
2. **Turnaround** (48–72h industry standard): "Draft in 24 hours, finals same day you approve. React to trends while they're still trends." Proof: timestamped delivery logs.
3. **Cost** ($50–150/asset benchmark): "Agency-quality shorts from $35. Retainers from $495 — a third of a freelancer, a tenth of an agency." Proof: pricing table vs. named benchmarks.
4. **Variant volume** (15–25 variants, 22–31% CPM savings): "One shoot → a month of ad variants. Hit the creative-refresh cadence the winners run." Proof: 1 raw video → 3 hook variants deliverable, CPM-refresh stats.

### One-liner & elevator pitch

**One-liner:** "We turn your raw footage into finished, on-brand short-form ads in 24 hours, for about a third of what an editor costs."

**Elevator pitch:** "Performance marketing is a creative-volume game now — winning brands ship 15–25 ad variants a month, but human editing makes that cost $3–5k and weeks of back-and-forth. We're a productized editing studio with a proprietary AI-assisted pipeline: send us raw creator or founder footage, and we send back brand-locked vertical ads and shorts — hooks chosen, captions in your fonts and colors, end-card, mixed audio — in 24 hours. We keep a living profile of your brand, so every correction sticks and video ten needs fewer notes than video one. Plans start at $495/month, first video free."

---

## 3. ICPs, Ranked

### ICP-A: DTC brands, $1–10M revenue, active on Meta/TikTok — **hit first**

- **Firmographics:** 2–20 employees, Shopify stack, spending $10–100k/mo on paid social, in-house or fractional media buyer, already sourcing UGC (Billo/Insense/creators) or founder-shot footage. Decision-maker: founder or head of growth. Verticals with visual products: skincare, supplements, apparel, food/bev, home.
- **Watering holes:** Meta Ad Library itself (they're publicly visible!), Twitter/X DTC circles ("DTC Twitter"), r/DTC and r/PPC (Reddit), Chew On This / DTC newsletters' communities, Shopify app-adjacent Slack groups, ADworld/agency events.
- **Trigger events (use these to time outreach):** ≥10 active ads in Ad Library but same creatives running 30+ days (creative fatigue, visible via 2026's impression-range buckets); hiring posts for "video editor" or "creative strategist"; recently ran Billo/Insense creators (raw footage exists, needs cutting); Q4 prep starting September (creative volume panic); new product launch.
- **Objections:** "We have an editor" (→ "keep them for hero assets; we do variant volume they don't have time for"), "Is quality good enough for paid?" (→ free first video on their own footage — zero-risk proof), "Another vendor to manage" (→ async, no calls, no briefs beyond a form).
- **Why first:** proven willingness to pay ($100–150/asset benchmarks), *recurring quantifiable* need (15–25 variants/mo), publicly identifiable via Ad Library (list-building is trivially targeted), and hook-variant delivery is your most defensible demo — a clip tool literally cannot do it from raw footage.

### ICP-B: Small performance-marketing agencies (white-label) — second, fast-follow

- **Firmographics:** 2–15 person Meta/TikTok agencies and media-buying shops, 5–30 brand clients, currently juggling freelance editors at $30–75/hr. Decision-maker: founder/head of creative.
- **Watering holes:** r/PPC, r/agency, r/FacebookAds, Twitter media-buyer community, agency Slack/Discord groups (Exit Five, Demand Curve alumni, uGURUS-type communities), Upwork (they post editing jobs constantly — each post is a lead).
- **Trigger events:** posting freelance editing gigs; winning new retainer clients (they announce on LinkedIn); complaining publicly about editor flakiness/turnaround.
- **Objections:** "Our clients have strict brand guidelines" (→ that's the entire product), "White-label confidentiality" (→ contractual, unbranded delivery), "Volume pricing?" (→ yes, that's the point).
- **Why second not first:** one agency = 5–20 brands' volume through one relationship (amazing leverage, and *they* handle end-client management), but sales cycles are slower, they negotiate price hard, and their QC bar is highest — better to arrive with DTC case studies in hand around week 6–8.

### ICP-C: Founders/experts doing personal-brand shorts — third, opportunistic only

- **Firmographics:** B2B founders, coaches, consultants, newsletter writers posting to LinkedIn/Shorts/TikTok; either DIY-editing (pain: time) or paying $1.5–2.5k/mo retainers (pain: cost).
- **Watering holes:** LinkedIn itself, X build-in-public circles, ghostwriter/personal-brand-agency networks (partnership channel, §4), podcast communities.
- **Trigger events:** just launched a podcast/YouTube; posting raw unedited videos; announced a content "challenge."
- **Objections:** price sensitivity ("my nephew uses CapCut"), taste subjectivity (personal brand = personal opinions = revision loops), single-video-per-week volume.
- **Why third:** lowest willingness-to-pay, highest revision subjectivity, and lowest volume per client — but it's the future self-serve PLG funnel (doc 01's door #2) and individual founders make great *visible* portfolio pieces. Take them when they come inbound; don't spend outbound effort here yet.

**Recommendation: 80% of outbound effort on ICP-A for weeks 1–6, add ICP-B at week 6 with case studies, ICP-C inbound-only.**

---

## 4. Channel Plan

### 4.1 Cold email — primary channel

**List building.** The killer move: source from **Meta Ad Library**, not generic databases — every DTC brand running ads is publicly listed with their active creatives. Tools: Adyntel (Ad Library scraper, integrates with Clay), AdsLeadz, or manual Ad Library search by vertical keyword. Filter: 5–30 active ads, creatives unchanged 3+ weeks (fatigue signal), UGC-style creative (they buy footage). Enrich founder/growth-lead emails via Apollo.io (free tier: ~100+ credits/mo; $49/mo for real volume) or Clay ($149/mo — worth it by week 3 for the Ad Library → email waterfall). Target list: 300 accounts by end of week 2, growing ~150/week.

**Deliverability basics (non-negotiable):** buy 2 secondary domains (e.g. trycutlist.com, cutlisthq.com — never your main domain), 2–3 mailboxes each (Google Workspace), warm 2–3 weeks (Instantly/Smartlead include warming, ~$37–97/mo), SPF/DKIM/DMARC on all, max ~25–30 sends/mailbox/day, plain-text emails, no links in email #1, spintax variation. Total capacity: ~100–150 sends/day by week 4.

**Volume & conversion math (2026 benchmarks: platform-average reply ~3.4%, good campaigns 5–10%; positive-reply 1–2% typical, 4–6% for tight niche targeting — you have tight targeting plus a free-video offer):**
- 1,000 sends/mo (well within 2–3 mailbox capacity)
- Replies: 5–8% = 50–80 (personalized, trigger-based, free offer — above average is realistic)
- Positive: ~2–3% = 20–30
- Free-video acceptances: 12–20
- Paying conversions (free video → paid): 30–40% = **4–8 clients/month from email alone**

**Sequence: 3 emails, 3–4 days apart.**

*Email 1 — the fatigue observation (personalized from Ad Library):*
> Subject: your [Brand] hook ad
>
> Hi [Name] — I was in the Ad Library looking at [vertical] brands and noticed [Brand]'s been running the same 4 creatives since [month]. Fatigue's usually setting in by then (CPMs creep 20–30% vs. brands refreshing weekly).
>
> I run a small editing studio that turns raw footage — UGC, founder clips, whatever you've got — into finished on-brand ad variants in 24 hours. One raw video becomes 3 hook variants, captions in your fonts/colors, ready to upload.
>
> Want me to cut one free from footage you already have? If it's not better than what's running, you've lost nothing.
>
> — Goutham

*Email 2 — the math (day 3–4):*
> Subject: re: your [Brand] hook ad
>
> Quick follow-up with the actual math. Brands shipping 15–25 fresh variants/month see 22–31% lower CPMs than monthly refreshers. At editor rates ($100–150/asset) that's $3k+/mo, so almost nobody does it.
>
> We do it for a flat monthly rate that's about a third of that, 24-hour turnaround. The free test video offer stands — one raw file, you'll have variants back tomorrow.

*Email 3 — the breakup + proof (day 7–8):*
> Subject: last one — before/after
>
> Won't keep nudging. Here's a 30-second before/after from a [vertical] brand we work with: [link]. Raw phone footage in, three branded hook variants out, same day.
>
> If creative volume becomes a bottleneck before Q4, you know where I am. The first video's free whenever you want it.

**Effort:** ~1 hr/day once warmed (Clay/Instantly automate the mechanics; personalization line is the manual part).
**Week-1 actions:** buy domains, set up mailboxes + warming, start Ad Library list (100 accounts), draft sequences in Instantly. (Sends start week 3–4 when warm — start warming *now*.)

### 4.2 Cold DM (X + LinkedIn) — secondary, immediate (no warmup needed)

- **Volume:** 10–15/day X, 10/day LinkedIn (stay under spam thresholds; LinkedIn ~100 connection requests/week max).
- **X script (media buyers/DTC founders):** "Saw your thread on [creative testing/UGC costs]. I run an editing studio doing exactly the variant-volume thing — raw footage → 3 branded hooks in 24h. Happy to cut one free from any raw file you've got, zero strings. Worst case you get a free ad."
- **LinkedIn (agency owners, ICP-B):** connect with note: "Fellow [Meta ads] world — I run a white-label shorts editing studio (24h turnaround, flat rates). No pitch, just useful to know people solving the same creative-volume problem." Then value-first follow-up after accept.
- **Rule:** DM people who *just posted about the pain* (editor complaints, creative fatigue, hiring editors). Reply publicly first, DM second — warm beats cold.
- **Week-1:** follow 200 relevant accounts, reply to 5 posts/day, start DMs day 3.

### 4.3 Organic social — X primary, LinkedIn secondary

**Do NOT build-in-public about the AI pipeline** (it burns the stealth). Instead, build in public about **the agency**: client results, before/afters, turnaround receipts, "how we think about hooks" mini-lessons. Before/after edits are the perfect content unit — post the raw 10 seconds next to the finished 10 seconds. Cadence: 1 post/day X, 3/week LinkedIn; 1 before/after video/week minimum. Every free portfolio video (§6, week 1–2) is a content piece *and* the recipient often reshares — that's the real distribution. Expected: slow burn, 1–3 inbound leads/mo by month 2; its real job is making your DMs and emails credible (people check your profile).
**Week-1:** set up profiles, write 10 posts in a batch, publish the first before/after.

### 4.4 Communities — r/PPC, r/DTC, r/FacebookAds, agency Slacks/Discords

How not to get banned: **90/10 rule** — 90% genuinely useful answers (you now know a lot about creative volume, CPM refresh data, caption best practices), 10% soft mention only where directly relevant, never links in posts, offer to DM instead. Build 2–3 weeks of comment karma before any self-referential content. One "we analyzed 50 DTC brands' Ad Library creative-refresh rates" data post (you have the scraped data as a byproduct of list building!) is worth 100 promo posts and is fully within rules.
**Week-1:** join, lurk, comment helpfully 2×/day. Data post in week 4–5.

### 4.5 Paid boosts — later, small

Skip until you have a proven result-post (a before/after or case study that already performed organically). Then: $200–400 test boosting it on LinkedIn to media-buyer/founder titles, or $150–300 on Meta retargeting site visitors. CPMs on LinkedIn ($30–80) make this a month-3+ tool, only when a $500+/mo LTV is proven so payback math works. Not a week-1–8 activity.

### 4.6 Marketplaces — Upwork yes (targeted), Fiverr no

- **Upwork:** don't compete as a generic editor — **bid specifically on "short-form ads variant" and "UGC editing" jobs** (10–15 proposals/week, ~$50–100/mo in Connects). Your unfair advantage: 24h delivery and 3-variants-for-the-price-of-one offers that human editors can't match profitably. Also mine it for ICP-B leads (agencies posting editing jobs = qualified prospects for direct outreach off-platform *after* a completed contract, per ToS). Pros: immediate cash, reviews, real footage variety for pipeline hardening. Cons: 10% fee, race-to-bottom pricing, no brand equity. Treat as: cash + test-data channel for months 1–2, deliberately wound down by month 4.
- **Fiverr:** skip — pure price competition, wrong buyer.
- **Contra:** list a profile (free, commission-free, good link for DMs), low effort.
**Week-1:** Upwork profile live, 5 proposals sent.

### 4.7 Partnerships — the sleeper channel

- **UGC marketplaces/creators (Billo, Insense ecosystems, freelance UGC creators):** they deliver *raw* footage that brands still must edit — you are their natural last mile. DM 20 UGC creators: "offer your clients finished ads, not just footage — white-label editing, 24h, rev-share or wholesale rate." One productive creator = recurring deal flow.
- **Media buyers / fractional CMOs:** they recommend vendors constantly. Offer 10% recurring referral or wholesale pricing.
- **Ghostwriters & LinkedIn-brand agencies (for ICP-C):** they sell writing; video is their most-requested upsell they can't deliver. White-label shorts at wholesale = a whole ICP-C funnel with zero acquisition cost.
**Week-1:** list 30 potential partners; begin DMs in week 3 once you have 2–3 portfolio pieces.

---

## 5. Pricing Strategy

**Anchors:** human editors $50–150/short; Billo $99–150/video (that's *unedited* creator footage!); agency/freelancer retainers $1,000–5,000/mo; productized editing subscriptions $495–2,500/mo; OpusClip-type SaaS $15–30/mo (avoid this anchor entirely — never let a prospect frame you as software). **COGS: $2–4/video** plus operator minutes.

### Ladder

**Founding-client offer (first 5 clients only, weeks 3–6):**
- First video free. Then **$25/video or $295/mo for 12 videos**, locked for 6 months, in exchange for a testimonial + permission to use before/afters. Margin: 12 × $3.5 = $42 COGS → ~86% gross margin even at giveaway pricing. Purpose: testimonials, corrections-data, case studies — not profit.

**Per-video intro pricing (the door-opener, no commitment):**
- **$35/short** (one finished vertical short, 2 revision rounds)
- **$75/variant pack** (1 raw video → 3 hook variants — vs. ~$300+ at human per-asset rates). This is the hero SKU for ICP-A.
- Margin: $35 – ~$3 COGS = ~91%; variant pack $75 – ~$6 = ~92% (variants share one edit-planning pass; marginal renders are nearly free per doc 03 use-case 5).

**Subscription tiers (push everyone here by video #2):**

| Tier | Price | Includes | COGS | Gross margin |
|---|---|---|---|---|
| **Starter** | $495/mo | 15 shorts (or 5 variant packs), 48h turnaround | ~$50 | ~90% |
| **Growth** | $995/mo | 40 shorts / mixed variant packs, 24h, priority | ~$130 | ~87% |
| **Unlimited** (Designjoy-style) | $1,995/mo | Unlimited requests, **2 active jobs at a time** (the queue is the fair-use cap — throughput naturally limits to ~40–60/mo), same-day drafts | ~$150–200 | ~90% |
| **White-label agency** (ICP-B) | $1,495/mo base | 50 videos across up to 10 end-brands, unbranded delivery, volume top-ups at $20/video | ~$170 | ~89% |

Positioning check: Starter at $495 = one-third of a $1,500 freelancer retainer for ~2× the volume; Unlimited at $1,995 undercuts short-form agency floors ($2,500) while the queue cap protects you exactly the way Designjoy's one-active-request model protects Brett Williams at $4,995–5,995/mo. Raise prices ~20–30% for clients 10+ (announced at signup for founders: "founding pricing, locks for 6 months").

**Rules:** 2 revision rounds included (doc 03 edge case 12); rush same-day +50%; re-skins $10; annual = 2 months free. Clean billing: cancel anytime, self-serve, no credit expiry — the anti-OpusClip stance, stated on the pricing page.

### "Quick money in 30 days" — path to first $1–3k MRR

- Days 1–7: 5 free portfolio videos for visible people (§6). Upwork live → target 2 small jobs (~$100–200 total). Warmup + lists running.
- Days 8–14: convert 2 free-video recipients to founding offer (2 × $295 = $590 MRR). Upwork: 2–3 more jobs (~$300 cash). DMs producing 5–10 conversations.
- Days 15–21: cold email live. 3 more founding/per-video clients from DMs + email replies (~$900 additional MRR mix of $295 subs and variant packs).
- Days 22–30: first $495 Starter conversion from a happy per-video client; 1 more founding client.
- **Day-30 realistic outcome: $1,500–2,500 MRR + $500–800 one-off/Upwork cash, 5–8 clients.** Aggressive-but-possible: $3k if one white-label agency lands early. COGS across all of it: under $150. The gating factor is your outreach hours, not margin or capacity.

---

## 6. 90-Day Plan

### Weeks 1–2 (MVP finishing per doc 03 — GTM runs in parallel)

- **W1:** Buy name/domains; one-page landing site (positioning, 3 SKUs, before/after placeholder, intake form — Carrd/Framer, one evening). Email infra + warming ON (the 3-week clock starts now). Ad Library list: 100 accounts. Social profiles live; 10 posts batched; join communities and start commenting. Upwork profile + 5 proposals.
- **W2:** **Portfolio seeding: edit 5 videos free for visible people** — pick founders/creators with engaged audiences who post raw video (DM: "I cut this from your last video — yours, no strings; if you like it I'll do 2 more"). Their reposts are your launch. List to 300. First real before/after posted. Line up the doc-03 weekend-3 design partners as founding clients #1–2.

### Weeks 3–6 (outbound + first paid clients + testimonials)

- **W3:** Cold email live (start 50/day, scale as warm). DMs at full cadence (20–25/day). Founding offer to all free-video recipients and design partners. First paid jobs ship. Partner DMs to UGC creators begin.
- **W4:** 1,000 cumulative sends. Community data post ("we analyzed 50 DTC brands' creative refresh rates"). Target: 4 paying clients, ~$800–1,200 MRR. Collect testimonials with every delivery ("one sentence + your logo").
- **W5:** First case study written (client numbers if shareable: turnaround, cost vs. prior editor, any CPM/CTR movement). Begin ICP-B outreach with case study attached. Raise per-video to $45 for new clients.
- **W6:** Target: 6–8 clients, $2–3k MRR. Ops review per doc-03 metrics: if manual-rescue rate >30% or operator time >15 min/job, freeze new-client intake for one week and fix the pipeline. **Founding offer closes (5 clients or week 6, whichever first).**

### Weeks 7–12 (scale outbound, publish results, raise prices, productize)

- **W7–8:** Email volume to 150/day (add mailboxes). Publish case study #2–3 publicly; boost the best one ($200 test if organic traction). First white-label agency signed (goal). Subscription tiers formally on the site; migrate per-video clients to Starter.
- **W9–10:** **Productized-service launch:** public pricing page, Stripe subscriptions, async intake polished (the phase-2 transition — trigger check: ≥5 monthly-recurring clients, ≥70% zero-rescue jobs). Wind down Upwork bidding. Partnerships: 2 active referral deals.
- **W11:** Prices +25% for new clients (Starter → $595, Growth → $1,245). Test Unlimited tier with the best existing client. Hiring nothing; buying nothing; the pipeline absorbs volume or it gets fixed.
- **W12:** Quarter review: MRR (target **$5–8k**), churn, margin/video, revisions-per-client trend (the moat metric). **Product-reveal decision:** stay stealth through month 6 unless (a) revisions-per-client is clearly declining (brand model demonstrably works), (b) 3+ public case studies exist, and (c) inbound demand exceeds QC capacity. If all three: begin phase-3 planning (waitlist page teasing "the engine behind [Studio]"). Otherwise: keep compounding quietly — stealth is an asset, not a deadline.

---

## 7. Metrics

One dashboard (a spreadsheet, per doc 03), reviewed every Friday.

**Leading indicators — weekly targets (steady state, ~week 4+):**

| Metric | Weekly target | Alarm |
|---|---|---|
| Cold emails sent | 250 → 750 by W8 | Deliverability: bounce >3%, spam complaints >0.1% |
| Email reply rate | ≥5% | <2% two weeks running → rewrite sequence/list |
| DMs sent (X+LI) | 100–125 | Response <10% → improve targeting/warmth |
| Positive conversations opened | 10–15 | — |
| Free/first videos delivered | 3–5 | — |
| Free→paid conversion | ≥30% | <20% → quality or offer problem: watch the drafts |
| Content posts | 7 X + 3 LI + 1 before/after | — |
| Upwork proposals (W1–8 only) | 10 | — |

**Lagging indicators — monthly:**

| Metric | M1 | M2 | M3 |
|---|---|---|---|
| Paying clients | 5–8 | 10–14 | 14–20 |
| MRR | $1.5–2.5k | $3–5k | $5–8k |
| Logo churn | — | <10%/mo | <10%/mo |
| Gross margin/video | >85% | >85% | >87% |
| Revenue per operator-hour | >$50 | >$80 | >$120 |

**Bridge metrics (tie GTM to product, from doc 03):** operator minutes/job (≤10), manual-rescue % (<30% trending down), revisions per client over time (**the moat metric** — must decline for the phase-3 thesis to hold), turnaround SLA hit-rate (>90% of drafts in 24h).

**The one weekly question stays:** "What was the most expensive minute of my time this week?" — in GTM terms: if the answer is ever "editing," fix the pipeline; if it's "selling," that's fine — that's the job right now.

---

## Appendix: benchmark sources

- Cold email 2026 benchmarks: [Instantly benchmark report](https://instantly.ai/cold-email-benchmark-report-2026) (3.43% avg reply), [Belkins](https://belkins.io/blog/cold-email-response-rates), [Apollo](https://www.apollo.io/insights/whats-the-expected-reply-rate-for-a-well-run-outbound-cold-email-campaign) (good = >5%), [Puzzle Inbox segment benchmarks](https://puzzleinbox.com/blog/cold-email-reply-rate-benchmarks-2026-by-segment)
- Designjoy model: [designjoy.co](https://www.designjoy.co/) ($4,995–7,995/mo, queue-capped unlimited, ~$1–2M/yr solo)
- Editing subscription comps: [Feedbird roundup](https://feedbird.com/blog/best-video-editing-services/), [beCreatives](https://becreatives.co/video-editing-prices/), [Increditors](https://increditors.com/how-much-does-professional-video-editing-cost/) ($495–2,500/mo bands)
- Ad Library prospecting: [Adyntel](https://www.adyntel.com/facebook-ads-scraper/) (Clay integration), [AdsLeadz](https://adsleadz.com/), [Clay community workflow](https://community.clay.com/x/general/ecezychddt0a/using-the-meta-ad-library-api-to-check-brands-acti)
- All pricing anchors for editors/agencies/UGC/SaaS: doc 01 §2–3.
