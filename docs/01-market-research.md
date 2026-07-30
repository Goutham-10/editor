# Market Research: Agentic Brand-Consistent Video Editing

**Date:** July 2026
**Purpose:** Deep market research to inform the MVP decision for an agentic video editing product — user uploads raw footage (or none), the system holds their brand kit (colors, fonts, logo, style), and it autonomously edits and delivers a finished video. Target formats: talking-head videos, UGC ads, product videos, motion graphics, shorts/reels.

---

## 1. Market Size & Tailwinds

### 1.1 The demand side is enormous and still compounding

- **Creator economy:** ~$254B in 2025, projected to reach **$310–323B in 2026** and ~$2.08T by 2035 (23.4% CAGR) ([Precedence Research](https://www.precedenceresearch.com/creator-economy-market), [Grand View Research](https://www.grandviewresearch.com/industry-analysis/creator-economy-market-report), [Research and Markets](https://www.researchandmarkets.com/reports/6226071/creator-economy-market-report)).
- **Short-form video ad spend:** ~**$111B globally in 2025**, heading to ~$145.8B by 2028. TikTok alone is projected at $35–44B in ad revenue in 2026; YouTube Shorts crossed 200B daily views (up ~186% YoY); Reels are 50% of all time spent on Instagram ([Marketing LTB](https://marketingltb.com/blog/statistics/short-form-video-statistics/), [ShortsIntel](https://www.shortsintel.com/statistics/short-form-video-marketing)). 71% of marketers say short-form video has the highest ROI of any social format; 33% plan to invest more in it than any other format in 2026.
- **UGC market:** US spend on UGC content passed **$10B in 2025** (+11% YoY); the UGC platform market was ~$7–9.6B in 2025 growing at ~28–34% CAGR toward $46–64B by 2034 ([Dimension Market Research](https://dimensionmarketresearch.com/report/user-generated-content-marketing-market/), [Fortune Business Insights](https://www.fortunebusinessinsights.com/user-generated-content-platform-114207), [Billo](https://billo.app/blog/ugc-statistics/)). Creator content now represents **>16% of total US digital ad spend**.
- **SMB/business adoption:** **91% of businesses use video as a marketing tool** (a three-year all-time high); 93% of marketers call it integral to strategy; 92% plan to spend the same or more on video in 2026; **63% of marketers now use AI to create video**, up from 51% a year earlier ([Wyzowl](https://wyzowl.com/video-marketing-statistics/)).
- **AI video generation market:** small but exploding — ~$0.7–1.2B in 2025 depending on definition, growing at **19–46% CAGR** ([Grand View Research](https://www.grandviewresearch.com/industry-analysis/ai-video-generator-market-report), [Fortune Business Insights](https://www.fortunebusinessinsights.com/ai-video-generator-market-110060)). Note: this measures *generation* tools; the money it substitutes (human editing + production services) is orders of magnitude larger.

### 1.2 The creative-volume arms race (the single most important tailwind)

Performance advertising has become a creative-volume game:

- Brands that refresh creative every 7–10 days see **CPMs 22–31% lower** than monthly refreshers; brands running **15–25 active ad variants per campaign** consistently outperform those with fewer than five ([Billo benchmarks](https://billo.app/blog/how-many-ad-creatives-do-you-need/), [Sepia Lab](https://sepia-lab.com/en/blog/ad-creative-volume-benchmarks)).
- Top large ad accounts ship **~31 new ads per week**; the fastest-growing TikTok brands produce **200+ new creatives per month**. Meanwhile the *average* DTC brand ships 2–4 new creatives a month and recycles 3–5 ads for weeks ([adgpt](https://adgpt.com/blog/ai-ad-creative-dtc-brands-beat-creative-fatigue), [Flighted](https://www.flighted.co/blog/meta-ads-strategy-for-dtc-brands)).

That gap — what brands *should* ship vs. what they *can afford to produce* — is the market. Human editing capacity is the binding constraint, not ideas and not footage.

### 1.3 Why now (technically)

a16z's January 2026 thesis ["It's time for agentic video editing"](https://a16z.com/its-time-for-agentic-video-editing/) (Justine Moore) lays out the unlock precisely:

1. **Vision models can now process long video** — Gemini 3-class models handle up to an hour of footage, generate timestamped labels, and find moments.
2. **Models can use tools** — agents can operate editing software/renderers, not just describe edits.
3. **Generation models are good enough for hybrid pipelines** — real A-roll + generated B-roll.

Her framing is the category thesis in one line: *"What Cursor did for coding, these agents will do for video production."* The 80/20 rule of video (80% of time on editing, 20% on filming) means the edit is where the value is. TikTok itself launched an "Agentic Hub" at Cannes Lions 2026 claiming automation of up to 85% of routine editing tasks and a 47% production cost reduction for brands ([digen resource](https://resource.digen.ai/ai-video-agent-for-content-creators-2026/)). Surveys claim ~62% of professional creators now use AI in at least one production stage vs 18% in 2025.

**Investor validation:** OpusClip raised $20M from SoftBank Vision Fund 2 at a **$215M valuation on ~$20M ARR** (March 2025) ([Forbes](https://www.forbes.com/sites/ianshepherd/2025/03/13/softbank-is-betting-on-the-future-of-ai-content-creation-with-opusclip/), [Sacra](https://sacra.com/c/opusclip/)); Captions rebranded to **Mirage**, raised $75M more (total $175M, ~$500M valuation) to train short-form-native video models ([TechCrunch](https://techcrunch.com/2026/03/24/mirage-raises-75m-to-continue-building-models-for-its-ai-video-editing-app-captions/)); YC-backed **Mosaic** raised a $3.8M seed for agentic editing with TubeScience and News Corp as customers ([Mosaic](https://mosaic.so/blog/mosaic-seed-round-announcement)).

---

## 2. Current Problems: What Video Costs Today

### 2.1 Human editors

- **Upwork:** median $35/hr; entry $15–40/hr, mid-tier $45–75/hr, experts with motion graphics $80–150/hr. Per-project: **$150–500 per YouTube video**, $500–2,000+ for corporate work ([Upwork](https://www.upwork.com/hire/video-editors/cost/), [Pixflow guide](https://pixflow.net/blog/freelance-video-editing-rates/)).
- **Fiverr:** $25–300 per gig typical; basic edits from $10, pro tiers $50–100+, high-end $500+ ([Fiverr](https://www.fiverr.com/resources/guides/video-animation/video-editor-cost)).
- **Short-form specifically:** ~$50+ per short at the low end; freelancer retainers around $1,500–2,500/mo for 4 long-form videos or $2,500–5,000/mo for 8 long-form + 16 shorts ([GigRadar](https://gigradar.io/blog/freelance-video-editing)).

### 2.2 Agencies and productized services

- Monthly retainers: **$750–5,000/mo standard**, $5,000–10,000+/mo premium; short-form-focused shops start ~$2,500/mo; a small-business social retainer (4–8 shorts/mo) runs **$1,000–3,000/mo** ([Vidico](https://vidico.com/news/video-retainer-packages/), [Increditors](https://increditors.com/how-much-does-professional-video-editing-cost/)).
- **Turnaround:** 48–72 hours standard, 24–48h for retainer clients, with 30–100% surcharges for 24h rush. Every revision round adds days.

### 2.3 UGC sourcing (the substitute for "just film it")

- **Billo:** from **$99/video** (realistically ~$150 with fast delivery/premium creators), no subscription ([Billo](https://billo.app/blog/billo-vs-insense/)).
- **Insense:** **$500+/mo subscription** (billed quarterly) *plus* creator payments *plus* 7–20% marketplace fees ([UGC Roster](https://www.ugcroster.com/blog/brands/billo-vs-insense-pricing-cheaper-ugc)).
- **Icon.com:** $999 for 6 human UGC ads (sourcing + scripting + editing bundled).

### 2.4 The pain, concretely

Do the math for a DTC brand trying to hit the 15–25 variant benchmark: at even $100–150 per finished short-form asset, shipping 30 creatives/month costs $3,000–4,500 plus 1–2 weeks of coordination latency, brief-writing, and revision ping-pong. For a founder posting daily shorts, a $2,000/mo editor retainer is often the single largest content line item. Emma Chamberlain famously spent 30–40 hours editing a 15-minute vlog (cited in the a16z piece). The universal complaints from founders/marketers producing at volume: cost per asset, multi-day turnaround that kills trend-reactivity, inconsistent quality across freelancers, and the coordination tax of briefing every edit.

---

## 3. Competitive Landscape

The market splits into six clusters. Almost nobody sits in the "upload raw footage → finished, on-brand, done-for-you edit" quadrant.

### 3.1 Text-based / assistant editors (human still drives)

| Product | Pricing | Positioning | Strengths |
|---|---|---|---|
| **Descript** | Free; Hobbyist $16/mo; Creator $24/mo; Business $50/mo ([pricing](https://www.descript.com/pricing)) | Edit video like a doc; "Underlord" AI co-editor removes filler words, fixes audio, suggests B-roll, generates clips | Best-in-class transcript editing; strongest brand in podcast/creator space; Underlord is the closest thing to a mainstream editing agent |
| **Captions / Mirage** | $9.99–$279.99/mo | Mobile-first AI video studio; now an AI research lab training short-form-native models (pacing, framing, attention) | 20M+ users, $175M raised; vertically integrated models |
| **Eddie AI** | Free tier; Plus $21/mo; Pro $83/mo; Pro+ $208/mo ([pricing](https://www.heyeddie.ai/pricing)) | "AI assistant editor for pros" — multicam, A-roll/B-roll organization, rough cuts, exports to Premiere/Resolve | Genuinely handles raw footage; respected by pro editors; positioned as assistant, not replacement |
| **AutoPod** | $29/mo, Premiere plugin ([review](https://vidpros.com/autopod-review-ai-editing-for-podcasts-worth-it/)) | Auto multicam switching, jump cuts, social clips for video podcasts | Beloved single-purpose tool; proof that narrow automated editing sells |

**Read:** Descript/Eddie automate *tasks*, not *outcomes*. The user is still the editor; there is no brand kit driving the final look, and output quality depends on the operator.

### 3.2 Clip repurposers (long-form in → clips out)

| Product | Pricing | Notes |
|---|---|---|
| **OpusClip** | Free; Starter $15/mo; Pro $29/mo (300 min). Credits charged on *source* length ([eesel breakdown](https://www.eesel.ai/blog/opusclip-pricing)) | Category leader: ~10M users, ~$20M ARR, $215M valuation. AI B-roll, virality scores, scheduling |
| **Submagic** | $19–69/mo ([site](https://www.submagic.co/)) | Viral caption templates + B-roll + zooms for shorts; strong with solo creators |
| **Pictory** | Starter ~$25/mo; Pro $39/mo; Teams $99/mo | Script/blog → video; long-to-short repurposing |

**Read:** This is the most commoditized cluster — dozens of near-identical tools. They *select and caption* moments; they don't really *edit*, and outputs are visually interchangeable across customers (same caption styles, same zooms). Nothing about the output says "this is *your* brand."

### 3.3 Template/browser editors (DIY, brand kits exist but human does the work)

| Product | Pricing |
|---|---|
| **Veed** | $12/mo Lite; Pro $24/mo ([comparison](https://www.ngram.com/blog/kapwing-vs-veed)) |
| **Kapwing** | Pro $16/mo/user; Business $50/mo/user |
| **InVideo** | Free; Plus $25/mo; Max $60/mo |
| **CapCut** | Free; Standard $10/mo; Pro $20/mo — free tier bars commercial use, and a June 2025 ToS update grants ByteDance perpetual, sublicensable rights over uploaded content, surviving account deletion ([async.com analysis](https://async.com/blog/capcut-terms-of-service/)) |

**Read:** These have brand-kit *features* (fonts/colors/logo storage) but the user still assembles every video. They compete on price and feature breadth, and their AI features are bolt-ons. CapCut's ToS is a live liability for agencies and brands — a real switching trigger.

### 3.4 AI avatar / synthetic UGC generation (no footage needed)

| Product | Pricing | Notes |
|---|---|---|
| **HeyGen** | Creator ~$24–29/mo + credits; real-world test: **$384 for 50 min** of Avatar IV output ([blogrecode test](https://blogrecode.com/synthesia-vs-heygen-comparison-creating-ai-videos/)) | Best avatar realism; marketing/translation focus; Trustpilot 2.3/5 and BBB "F" on billing/support ops |
| **Synthesia** | Starter $18–29/mo (10 min); Creator $64–89/mo (30 min) | Enterprise L&D winner, SOC 2, 240+ avatars; top G2 negatives are "Avatar Limitations" (443 mentions) ([G2 analysis](https://learn.g2.com/ai-video-generator-insights)) |
| **Arcads** | **$110/mo** entry, no free trial ([eesel](https://www.eesel.ai/blog/arcads-ai-pricing)) | Most believable AI UGC actors; loved by performance marketers for creative testing |
| **Creatify** | From $19–29/mo | URL → auto-generated product ad; cheap volume play |
| **MakeUGC** | ~$25–69/mo (~$10/video) | Budget Arcads alternative |
| **Icon.com** | $999 / 6 human UGC ads + custom software tiers ([pricing](https://icon.com/pricing)) | "AI Admaker" + human creators hybrid; well-funded but reviews cite billing traps, no self-serve cancel, buggy software, inconsistent quality ([review](https://easyai.indevs.in/icon-ai-admaker/)) |
| **Runway** | $12–95/mo, credit-based; a 10-sec 1080p clip burns 100–150 credits ([pricing](https://runwayml.com/pricing)) | Generation model leader; a tool for making footage, not finishing videos |

**Read:** This cluster solves "no footage" but is running into a trust ceiling: **~46% of consumers are uncomfortable with brands using AI creators, 48% say AI content feels less trustworthy, only 15% highly trust AI influencers, and 80% of Gen Z question digital visuals' authenticity** ([Superscale performance study](https://superscale.ai/learn/ai-vs-traditional-ugc-complete-comparison/), [Social Native](https://www.socialnative.com/articles/ai-generated-ugc-brand-trust/)). AI UGC wins on volume metrics (views/shares); real footage wins on trust and purchase intent. Platforms are also moving toward AI-content labeling. This is a structural tailwind for **real footage, AI-edited** over fully synthetic.

### 3.5 Agentic editors (the emerging direct competition)

- **Mosaic** ([mosaic.so](https://mosaic.so/)) — YC W25, $3.8M seed (Apr 2026). Node/canvas where users build reusable editing agents; runs edits "on autopilot," A/B tests variants from the same raw footage. Customers: TubeScience (Meta's largest creative partner), News Corp. Closest philosophical competitor, but it's a *workflow canvas for power users/agencies*, not a done-for-you brand-aware product.
- **Overlap** ([overlap.ai](http://overlap.ai/)) — node workflows for adaptation (clipping, reformatting, dubbing).
- **OneTake AI, AutoEdits.ai, Druid Cat, Mobbi** — early "upload footage, get an edit" plays; none has visible scale or a brand-kit-centric pitch.
- **Descript Underlord / TikTok Agentic Hub** — incumbents and platforms moving agentic; TikTok's version will be free but platform-locked and generic by design.

**Read:** The agentic wave is real and validated (a16z is actively soliciting deals), but every current entrant is either (a) a pro-sumer workflow builder (Mosaic), (b) a feature inside a human-driven editor (Underlord), or (c) a thin wrapper. **No one owns "we know your brand; send footage; receive finished on-brand video."**

### 3.6 Human UGC marketplaces & agencies (substitute competition)

Billo ($99–150/video), Insense ($500+/mo + creator fees), Trend, and thousands of freelancers/agencies. They deliver authenticity but not speed, volume economics, or consistency. Increasingly they are the *supply chain* for raw footage that still needs editing into ad variants — i.e., potential channel partners, not just competitors.

---

## 4. What Users Hate About Existing Tools

Recurring complaint themes across Trustpilot, G2, and Reddit:

1. **Generic, interchangeable output.** Clip tools apply the same caption styles and zooms to everyone. Typical creator advice on OpusClip: "learn to cut clips yourself — quality over quantity" ([Trustpilot](https://www.trustpilot.com/review/opus.pro)). Nothing in the output reflects the customer's identity.
2. **No real brand consistency.** **94% of marketers say brand consistency is their top concern as AI content scales — only 9% think current tools solve it**; AI tools lack persistent brand memory, and today's corrections don't carry into tomorrow's generations ([Venngage](https://venngage.com/blog/ai-brand-consistency-guide/), [ALStudio](https://alstudio.ai/Blog/blog-brand-consistency-at-scale)). This is the single clearest, quantified unmet need found in this research.
3. **Credit-system rage.** Veed users burned 470 of 500 credits on one AI video then needed 217 more just to export; credits vanish at renewal ([Trustpilot](https://www.trustpilot.com/review/veed.io)). OpusClip charges credits on source-video length regardless of clips used, and paid-for projects expire when the subscription lapses. HeyGen's 200-credit cap gets called "bait-and-switch."
4. **Billing/cancellation dark patterns.** OpusClip (22% one-star reviews; no renewal reminders), Icon (no self-serve cancel, charges after cancellation), Veed (per-workspace subscriptions that must each be cancelled), HeyGen (BBB "F"). The category has a trust deficit a clean operator can exploit.
5. **Reliability.** OpusClip's #1 recent Trustpilot complaint: videos hang for hours or never finish processing, with unhelpful support.
6. **Uncanny avatars.** Synthesia's top G2 negatives are avatar limitations; even HeyGen's best avatars get flagged for robotic movement and unnatural mouths/teeth. Consumers distrust synthetic spokespeople (Section 3.4 data).
7. **"Clipping isn't editing."** Repurposers require existing long-form content and only *select* moments. Users with raw footage — multiple takes, bad audio, no structure — have nowhere to go except Descript (DIY) or a human.
8. **Rights concerns.** CapCut's perpetual license over uploads makes it radioactive for agencies and brands with IP obligations.

---

## 5. Gap Analysis: Where's the Whitespace?

Map the landscape on two axes — **who does the work** (DIY tool → done-for-you) and **what drives the output** (generic templates → your brand):

- **DIY + generic:** CapCut, Veed, Kapwing, InVideo — saturated, price-competitive.
- **DIY + brand-aware:** Veed/Kapwing brand kits, Synthesia brand kit — brand kit as static asset storage, human still edits.
- **Done-for-you + generic:** OpusClip, Submagic, TikTok Agentic Hub — automated but interchangeable output; also human marketplaces (Billo) which are done-for-you but slow/expensive.
- **Done-for-you + brand-driven: effectively empty.** Mosaic is nearest but sells workflow-building to agencies/power users; Icon bundles humans and is executing poorly.

The defensible product insight: a **persistent brand model** (colors, fonts, logo, caption style, pacing preferences, banned words, past corrections) that *drives an autonomous edit* and **learns from every revision**. That directly answers the 94%/9% brand-consistency gap, and it compounds: every edit makes the next one better, which credit-metered clip tools structurally cannot match because they have no memory.

### Segment-by-segment scoring

| Video type | Tailwind | Incumbent coverage | Willingness to pay | Automation tractability |
|---|---|---|---|---|
| **UGC ads (real footage → ad variants)** | Extreme (15–25 variants, 7–10-day refresh, $111B short-form ad spend) | **Weak** — synthetic-gen tools (Arcads/Creatify) don't edit real footage; Icon is stumbling; agencies are the incumbent | High ($100–150/asset human benchmark; Arcads charges $110/mo for *synthetic*) | High — performance ads follow a known grammar (hook → problem → demo → social proof → CTA) |
| **Talking-head shorts (founders/experts/podcasts)** | Strong (LinkedIn/Shorts founder-led content boom) | Medium — OpusClip et al. cover *clipping from long-form*, badly on brand; raw-footage editing uncovered | Medium ($50/short, $1.5–2.5K/mo retainers) | High — single speaker, transcript-driven |
| **Product videos (DTC/ecom)** | Strong | Medium (Creatify auto-generates from URLs, but generic) | Medium | Medium |
| **Motion graphics** | Moderate | Weak (real gap, still human-dominated at $80–150/hr) | High | **Low — hardest to automate credibly; wrong MVP** |
| **Faceless/B-roll shorts** | Moderate | Heavy (dozens of cheap "faceless channel" tools) | Low | High but commoditized |

---

## 6. Conclusion: Ranked Opportunities & the First Use Case

### Ranked opportunities

**#1 — Brand-consistent ad-variant editing from real footage, for DTC brands and performance agencies.**
Raw creator/founder footage in (from Billo, Insense, in-house shoots, or the founder's phone) → finished, on-brand ad variants out: multiple hooks, caption styles locked to the brand kit, logo end-cards, platform-native aspect ratios, A/B sets. Why first: (a) the creative-volume math (15–25 variants, 31 ads/week at the top) creates *recurring, quantifiable* demand with a hard ROI story (22–31% CPM savings from fresh creative); (b) willingness to pay is proven at $99–150 per human-made asset and $110/mo for merely *synthetic* actors; (c) the authenticity backlash against AI avatars (~46–48% distrust) makes "real footage, AI-edited" the safe harbor — you sidestep the uncanny valley entirely because you never synthesize a human; (d) incumbent coverage is weakest here: Arcads/Creatify generate, they don't edit; OpusClip clips podcasts, not ad footage; Mosaic sells plumbing, not outcomes; Icon proves demand for done-for-you ads while fumbling execution; (e) performance-ad editing is formulaic enough for agents to hit professional quality *now*.

**#2 — Branded talking-head shorts for founders, experts, and B2B content teams.** Same technical core (transcript-driven editing of a single speaker), broader but cheaper market, natural PLG motion. Strong fast-follow or parallel self-serve tier — the OpusClip user who has outgrown generic clips and wants *their* look without a $2K/mo editor.

**#3 — Ecommerce product videos** from footage + product imagery (expansion of #1's customer base, partially covered by Creatify).

**#4 — Podcast/long-form post-production** (Eddie AI, AutoPod territory — real but pro-editor-owned and more crowded).

**#5 — Motion graphics** — highest per-hour rates ($80–150/hr) but lowest automation tractability; treat brand-kit-driven motion templates (intros, lower thirds, end-cards) as a *feature* of #1/#2, not a standalone wedge.

### The single use case to attack first

**Build the agent that turns raw talking-head footage into finished, brand-locked short-form video — and sell it first as "ad variants at volume" to DTC brands and the performance agencies that serve them.**

This is one technical product (speaker footage in → branded vertical video out) with two doors: the ad-variant door commands agency-level pricing (~$500–2,000/mo replacing a $2,500–5,000 retainer or $3,000+/mo in per-asset fees, at 100x the turnaround speed), while the founder-shorts door provides the self-serve volume funnel later. The brand kit is the moat: static brand kits are a commodity checkbox, but a **learning brand model that remembers every correction** is exactly what 94% of marketers say they need and 9% say they have. Avoid: motion graphics first (too hard), fully synthetic avatars (trust ceiling + brutal competition from $175M-funded Mirage and HeyGen), and generic clipping (commoditized, SoftBank-funded incumbent at $15/mo).

Positioning in one sentence: **"Your brand's editor, on autopilot — real footage in, on-brand ads and shorts out, in minutes not weeks."**

---

## Appendix: Key source URLs

- a16z, "It's time for agentic video editing" (Jan 2026): https://a16z.com/its-time-for-agentic-video-editing/
- Wyzowl Video Marketing Statistics 2026: https://wyzowl.com/video-marketing-statistics/
- Short-form ad spend: https://marketingltb.com/blog/statistics/short-form-video-statistics/
- Creator economy: https://www.precedenceresearch.com/creator-economy-market
- UGC market: https://dimensionmarketresearch.com/report/user-generated-content-marketing-market/ ; https://billo.app/blog/ugc-statistics/
- Creative volume benchmarks: https://billo.app/blog/how-many-ad-creatives-do-you-need/ ; https://sepia-lab.com/en/blog/ad-creative-volume-benchmarks
- Editor rates: https://www.upwork.com/hire/video-editors/cost/ ; https://pixflow.net/blog/freelance-video-editing-rates/ ; https://vidico.com/news/video-retainer-packages/
- OpusClip: https://www.eesel.ai/blog/opusclip-pricing ; https://www.trustpilot.com/review/opus.pro ; https://sacra.com/c/opusclip/
- Descript: https://www.descript.com/pricing ; Eddie AI: https://www.heyeddie.ai/pricing ; AutoPod: https://vidpros.com/autopod-review-ai-editing-for-podcasts-worth-it/
- HeyGen vs Synthesia: https://blogrecode.com/synthesia-vs-heygen-comparison-creating-ai-videos/ ; https://learn.g2.com/ai-video-generator-insights
- Arcads/Creatify/MakeUGC: https://www.eesel.ai/blog/arcads-ai-pricing ; https://www.ngram.com/blog/arcads-vs-creatify
- Icon: https://icon.com/pricing ; https://easyai.indevs.in/icon-ai-admaker/
- CapCut ToS: https://async.com/blog/capcut-terms-of-service/
- Veed complaints: https://www.trustpilot.com/review/veed.io
- AI vs human UGC trust: https://superscale.ai/learn/ai-vs-traditional-ugc-complete-comparison/ ; https://www.socialnative.com/articles/ai-generated-ugc-brand-trust/
- Brand consistency gap: https://venngage.com/blog/ai-brand-consistency-guide/
- Mosaic: https://mosaic.so/blog/mosaic-seed-round-announcement
- Mirage/Captions funding: https://techcrunch.com/2026/03/24/mirage-raises-75m-to-continue-building-models-for-its-ai-video-editing-app-captions/
- Billo/Insense: https://billo.app/blog/billo-vs-insense/ ; https://www.ugcroster.com/blog/brands/billo-vs-insense-pricing-cheaper-ugc
