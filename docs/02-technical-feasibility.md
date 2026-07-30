# Technical Feasibility: Agentic Video Editing Pipeline

**Date:** July 2026
**Verdict up front:** This is very buildable, and the timing is unusually good. The two hard problems of 2023–24 — (1) an edit representation an LLM can reliably write, and (2) affordable generated b-roll — are both solved as of mid-2026. The v1 you described ("connect every MCP/API to Claude Code and prompt it") is not a hack; it is roughly what HeyGen itself is now evangelizing with HyperFrames, and what the viral Remotion Claude Code skill (25k+ installs in week one, Jan 2026) demonstrated at scale. The moat will not be the plumbing — it will be taste encoded as prompts/skills, plus the brand-kit layer.

---

## 1. Generative video tools (b-roll, product shots, generated scenes)

The market has bifurcated: **premium cinematic models** (Veo 3.1, Sora 2 Pro, Runway Gen-4.5) at $0.15–0.70/sec, and **commodity workhorses** (Seedance, Hailuo, Kling) at $0.01–0.10/sec. For automated pipelines that need b-roll at volume, the commodity tier is the right default — a human reviewing a finished edit rarely notices the difference on a 3-second insert shot.

| Model | API? | Price (via API) | Best for | Notes |
|---|---|---|---|---|
| **Seedance 2.0** (ByteDance) | Yes (BytePlus official; fal, Replicate, OpenRouter, EvoLink) | ~$0.14/sec official; **$0.022–0.045/sec** via third-party tiers ([TechNode](https://technode.com/2026/03/05/bytedances-seedance-2-0-video-model-costs-about-0-14-per-second/), [EvoLink](https://evolink.ai/seedance-2-0), [Atlas Cloud](https://www.atlascloud.ai/blog/case-studies/seedance-2.0-pricing-full-cost-breakdown-2026)) | **B-roll king.** Product shots, lifestyle inserts, motion-heavy clips | Roughly 100x cheaper than Sora 2 at 720p via resellers. Multiple pricing tiers (Fast/Standard/Pro) |
| **Kling 3.0 / O1** (Kuaishou) | Yes (official dev API, prepaid packages) | **$0.07–0.14/sec**; 5s 1080p w/ sound ≈ $0.70 ([Kling dev pricing](https://kling.ai/dev/pricing), [eesel](https://www.eesel.ai/blog/kling-ai-pricing)) | Human motion, physics, product-in-hand shots | Failed API tasks don't consume credits — good for agent retry loops. API credits separate from consumer plans |
| **Runway Gen-4 / 4.5** | Yes (dev portal, $0.01/credit) | Gen-4 Turbo ~$0.05/sec, Gen-4 ~$0.12/sec, Gen-4.5 ~$0.25/sec ([Runway docs](https://docs.dev.runwayml.com/guides/pricing/), [FairStack](https://fairstack.ai/blog/runway-pricing)) | Stylized/cinematic b-roll, image-to-video with reference consistency | Most mature Western API; good docs. Mid-priced |
| **Veo 3.1** (Google, Gemini API) | Yes (Gemini API / Vertex) | $0.15/sec Fast, $0.40/sec Standard (both with native audio); Lite $0.03/sec no audio; 4K $0.30–0.60/sec ([Google pricing](https://ai.google.dev/gemini-api/docs/pricing), [aifreeapi](https://www.aifreeapi.com/en/posts/veo-3-1-pricing)) | Hero shots where native audio/dialogue matters | Veo 3.0 endpoints shut down June 30, 2026 — build on 3.1 only |
| **Sora 2 / 2 Pro** (OpenAI) | Yes, but **dying** | $0.10/sec 720p; Pro $0.30–0.70/sec ([costgoat](https://costgoat.com/pricing/sora), [eesel](https://www.eesel.ai/blog/sora-2-pricing)) | — | **Do not build on it.** Sora app ended April 26, 2026; API discontinues September 24, 2026 |
| **Hailuo 03** (MiniMax) | Yes (official platform API) | **$0.0104/sec 512p, $0.04/sec 768p, $0.08/sec 1080p** ([MiniMax docs](https://platform.minimax.io/docs/guides/pricing-video), [APIMart](https://apimart.ai/blog/hailuo-03-minimax-3-0-api-pricing-features-how-to-access)) | Cheapest usable b-roll; social-format clips | Great cost floor for draft passes: generate at 512p, re-render winners at 1080p |
| **Luma Dream Machine** | Yes (separate API billing) | ~$0.32/generation base ([Luma helpdesk](https://lumaai-help.freshdesk.com/support/solutions/articles/151000210176-what-are-your-prices-for-api-), [lumalabs pricing](https://lumalabs.ai/pricing)) | Quick image-to-video | Fine, but no strong reason to prefer over Seedance/Hailuo |
| **Pika** | API mostly via aggregators (fal) | comparable to Luma | Effects/meme-style transforms | Consumer-skewed; not a pipeline anchor |
| **Higgsfield** | Consumer subscription, credit packs; **not API-first** | $15–129/mo plans; ~$5/100 credits top-ups; Kling 3.0 ≈ 6 credits/video vs Veo 3.1 ≈ 40–70 ([higgsfield.ai/pricing](https://higgsfield.ai/pricing), [imagine.art breakdown](https://www.imagine.art/blogs/higgsfield-ai-pricing)) | Human UI aggregator, camera-control presets | It's a *competitor's UX layer*, not infrastructure. Skip for the pipeline; study it for product ideas |

**MCP availability:** fal.ai and Replicate both ship MCP servers exposing their whole model catalogs, which is the pragmatic way to give Claude Code access to Seedance/Kling/Hailuo/Veo through one interface rather than five SDKs.

**Opinion:** default to **Seedance 2.0 (fast tier) via fal or BytePlus** for b-roll at ~$0.10–0.25 per 5s clip, with **Hailuo 03 at 512p** for cheap draft iterations and **Veo 3.1 Fast** reserved for hero shots needing audio. Ignore Sora entirely.

---

## 2. AI avatars / UGC generation

| Tool | API? | Pricing | Notes |
|---|---|---|---|
| **HeyGen** | **Yes — best-in-class, plus an official MCP server** | Pay-as-you-go: ~$1/min (Avatar III 1080p) to $4/min (Avatar IV 1080p) and $5/min (Avatar IV Digital Twin 4K); range $0.0167–0.0667/sec ([HeyGen API pricing](https://developers.heygen.com/docs/pricing), [help center](https://help.heygen.com/en/articles/10060327-heygen-api-pricing-explained)) | Official MCP with `generate_avatar_video`, voice/avatar listing, OAuth connector for Claude ([HeyGen MCP](https://www.heygen.com/model-context-protocol), [Claude Code docs](https://developers.heygen.com/mcp/claude-code)). Credits expire after 12 months; no subscription required |
| **Captions / Mirage** | Yes (Mirage API) | Per-second-of-video credit billing; Captions API $0.15/min of input video for captioning ([Mirage API pricing](https://help.mirage.app/docs/api/pricing)) | Mirage is a genuine "UGC foundation model" — generates original actors with natural body language, not lip-synced photos. The most native-feeling UGC output |
| **Arcads** | Platform-first; pricing gated behind signup | ~$110/mo → ~50 videos; effectively **~$11/finished video** ([Wireflow](https://www.wireflow.ai/blog/arcads-pricing), [eesel](https://www.eesel.ai/blog/arcads-ai-pricing)) | Great output quality for ads, but opaque credits and weak developer story. Treat as a benchmark competitor, not a component |
| **Creatify** | Yes (API available) | Plans from $19/mo; free tier 10 credits ([Creatify](https://creatify.ai/review/arcads-ai), [ngram comparison](https://www.ngram.com/blog/arcads-vs-creatify)) | Cheaper Arcads alternative with a real API; worth testing for UGC ad SKU |

**Opinion:** **HeyGen for v1** — the official MCP server means the avatar leg of your pipeline is literally a config entry in Claude Code, and pay-as-you-go pricing ($1–4/min) maps cleanly to per-video COGS. Evaluate Mirage for the "authentic UGC" aesthetic once volume justifies a second integration.

---

## 3. Sound design, music, and transcription

### Voice, SFX, music generation

| Service | What | Price | Source |
|---|---|---|---|
| ElevenLabs TTS | VO / narration | $0.10/1k chars (Multilingual v2/v3), $0.05/1k (Flash) | [elevenlabs.io/pricing/api](https://elevenlabs.io/pricing/api) |
| ElevenLabs SFX | Whooshes, risers, ambience | **$0.12/min** (≈40 credits/sec self-set duration) | [ElevenLabs help](https://help.elevenlabs.io/hc/en-us/articles/25735337678481-How-much-does-it-cost-to-generate-sound-effects) |
| Eleven Music | Full backing tracks | **$0.15/min** | [Flexprice breakdown](https://flexprice.io/blog/elevenlabs-pricing-breakdown) |
| Suno | Songs | **No official API.** Third-party wrappers $0.014–0.111/song ([Sunor](https://sunor.cc/blog/suno-api-pricing-2026)) | Legally gray for a commercial product — avoid wrappers |
| Udio | Songs | Effectively dead for pipelines: downloads disabled since Oct 2025, walled-garden UMG platform ([Undetectr](https://undetectr.com/blog/epidemic-sound-vs-ai-music)) | Skip |
| Mubert | Generative bg loops via API | API-first, royalty-free, good for corporate/lo-fi beds ([Mubert](https://mubert.com/blog/mubert-vs-suno-which-ai-music-generator-is-better-in-2026)) | Solid fallback |
| Epidemic Sound Partner API | Licensed human-made catalog (55k tracks, 250k SFX) | Free prototyping tier (50 downloads, non-commercial); Startup/Enterprise = custom contract ([developers.epidemicsound.com](https://developers.epidemicsound.com/)) | Best *quality*, but requires a partnership agreement — defer to post-v1 |

### Mixing / ducking
No API needed. FFmpeg's `sidechaincompress` filter does auto-ducking (music dips under voice), `loudnorm` handles EBU R128 normalization for platform loudness targets. Both free, both trivially scriptable by an agent. This is a place where people reach for paid tools (Auphonic etc.) unnecessarily.

### Transcription (word-level timestamps → captions)
All four options below return word-level timestamps, which is what you need for animated captions and for giving the LLM a time-addressable transcript to cut against.

| Service | Price | Notes |
|---|---|---|
| **OpenAI Whisper / GPT-4o-transcribe** | $0.003–0.006/min ([diyai](https://diyai.io/ai-tools/speech-to-text/openai-whisper-api-pricing-2026/)) | The default; `whisper.cpp`/`faster-whisper` run **free locally** with word timestamps |
| **AssemblyAI Universal-2** | **$0.15/hour** (~$0.0025/min) ([futureagi](https://futureagi.com/blog/speech-to-text-apis-in-2026-benchmarks-pricing-developer-s-decision-guide/)) | Cheapest hosted; good LLM-ready extras (chapters, entities) |
| Deepgram Nova-3 | $0.46/hour ([futureagi](https://futureagi.com/blog/speech-to-text-apis-in-2026-benchmarks-pricing-developer-s-decision-guide/)) | Best for realtime — which you don't need |
| ElevenLabs Scribe | $0.22/hour ([Flexprice](https://flexprice.io/blog/elevenlabs-pricing-breakdown)) | Convenient if already on ElevenLabs |

**Opinion:** transcription is a rounding error (a 10-minute video costs 3–6 cents). Use **faster-whisper locally for $0** in v1, ElevenLabs for SFX/music ($0.12–0.15/min), FFmpeg for all mixing.

---

## 4. Motion graphics: Remotion, HyperFrames, and the template-API crowd

This is where the July-2026 landscape has genuinely changed.

### Remotion — mature, but mind the license
React → video. The official **Remotion skill for Claude Code went viral in January 2026** (6M+ views, 25k installs in week one) — Claude writes TypeScript compositions, Remotion renders them ([remotion.dev](https://www.remotion.dev/)).

**Licensing (important for you):** free only for individuals and companies of ≤3 people. Your product is explicitly an "automation," which triggers the **Automators license: $0.01 per render with a $100/month minimum spend** (Enterprise: same per-render, $500/mo minimum). The $25/seat "Creators" tier does *not* cover automated pipelines ([remotion.pro/license](https://www.remotion.pro/license), [docs](https://www.remotion.dev/docs/license)). Render compute via Remotion Lambda is genuinely cheap — pennies per video minute plus AWS S3/bandwidth ([cost example](https://www.remotion.dev/docs/lambda/cost-example)).

### HyperFrames — the agent-native disruptor (and it's free)
**HyperFrames** is HeyGen's open-source (Apache 2.0) HTML-to-video renderer, launched 2026 and explicitly "built for agents": the agent writes plain HTML/CSS/JS (GSAP, Lottie, CSS animations — anything seekable), a headless browser captures deterministic frames, FFmpeg stitches the MP4. No custom DSL, no React requirement, **no license fees** ([hyperframes.heygen.com](https://hyperframes.heygen.com/), [GitHub](https://github.com/heygen-com/hyperframes), [MindStudio guide](https://www.mindstudio.ai/blog/ai-video-editing-claude-code-hyperframes)). LLMs are better at writing vanilla HTML than at any proprietary format, which is the entire thesis.

**Opinion:** for a bootstrapped v1, **HyperFrames beats Remotion**: identical capability class for captions/lower-thirds/brand outros, zero licensing cost, zero minimum spend, agent-first design. Remotion is the upgrade path when you want its ecosystem (Player for a future web UI, Lambda for distributed rendering, battle-tested captions packages) and $100/mo is noise.

### Adjacent options
- **Lottie / Theatre.js:** free animation formats/libraries; both run *inside* HyperFrames or Remotion compositions — use them as ingredients, not as the renderer.
- **After Effects via Plainly:** renders data-driven AE templates through an API — Starter $69/mo for 50 render-minutes ([plainlyvideos.com/pricing](https://www.plainlyvideos.com/pricing)). Right choice only if a motion designer hands you .aep files. Skip.
- **Template render APIs:** Shotstack $49/mo for 200 min at 720p, sliding $0.25→$0.11/min ([shotstack.io/pricing](https://shotstack.io/pricing/)); Creatomate $54/mo for 2,000 credits (~14 credits/min at 720p) ([JSON2Video comparison](https://json2video.com/how-to/creatomate-alternative/)); JSON2Video $49.95/mo for 200 Full-HD minutes ([json2video.com](https://json2video.com/how-to/shotstack-alternative/)). These are JSON-template renderers — fine products, but they put a $50–100/mo tax and a third-party ceiling on exactly the layer you can own for free with FFmpeg + HyperFrames.
- **Editframe:** still alive ("Build Video With Code"), now shipping agent-oriented "skills" docs ([editframe.com](https://editframe.com/)) — watch it, don't depend on it.

---

## 5. Timeline management & the programmatic editing core

**The key architectural question: what data structure represents the edit, and what turns it into pixels?**

My answer: **a plain JSON cutlist (an "Edit Decision List") authored by the LLM, rendered by FFmpeg.** Everything else is optional elaboration.

### The render substrate
- **FFmpeg** — free, universal, handles 95% of an editor's actual job: trim, concat (demuxer or `filter_complex`), crossfades (`xfade`), speed ramps, overlays, audio mix/ducking, loudness, encoding. An LLM writes FFmpeg invocations extremely well because there's two decades of training data. This is your render engine for the *footage* track.
- **MoviePy v2 / Mosaico** — Pythonic wrappers over FFmpeg; MoviePy is in "maintainers wanted" mode ([GitHub](https://github.com/zulko/moviepy)) and slow for long renders. Unnecessary indirection when the agent can write FFmpeg directly.
- **Editly** — abandoned. Skip.
- **MLT / `melt` CLI** — a genuinely capable headless multitrack editor (the engine behind Kdenlive/Shotcut), scriptable via XML, designed for headless servers ([mltframework.org](https://www.mltframework.org/docs/melt/)); there's even a write-only OTIO→MLT adapter ([otio-mlt-adapter](https://github.com/apetrynet/otio-mlt-adapter)) and MLT agent skills on marketplaces ([LobeHub](https://lobehub.com/skills/agentskillexchange-skills-mlt-multimedia-framework-video-editing-processing)). It's the strongest "real NLE headlessly" option — but its XML is niche for LLMs and it buys you little over FFmpeg + HTML overlays. Keep as a v2 option if you need true multitrack compositing.
- **OpenTimelineIO** — the right *interchange* format (export a `.otio` so a human can open the edit in Resolve/Premiere later). Do **not** make it your internal representation for v1; a flat JSON schema you define is easier for the LLM and for debugging. Add an OTIO exporter when customers ask for "open in my editor."

### Cloud editing APIs (rendering-as-a-service)
Covered above (Shotstack/Creatomate/JSON2Video). Add: **Rendi**, a hosted FFmpeg API — free tier 50 GB processing, Pro $25/mo, ~$0.15/GB processed ([rendi.dev/pricing](https://www.rendi.dev/pricing)); and **Transloadit** (broader file pipeline, 5 GB free, assembly-based pricing) ([comparison](https://transloadit.com/compare/rendi/)). Rendi is the one to remember: when local rendering stops scaling, it's "your same FFmpeg commands, hosted" — no re-architecture.

### Open-source GUI editors — can an agent drive them?
- **OpenCut** (MIT, Next.js/React, browser-based CapCut alternative) ([opencut.dev](https://opencut.dev/)), **OpenReel**, **designcombo/react-video-editor** (Remotion-based CapCut/Canva clone) ([GitHub](https://github.com/designcombo/react-video-editor)) — these matter for a *future human review UI*, not for the agent. They are UIs; driving them headlessly is fighting the tool. The interesting pattern: designcombo's editor and Remotion Player share the composition model, so your v2 "human tweaks the agent's edit" story has a ready-made OSS foundation.
- **Kdenlive/Shotcut/OpenShot/Olive** — desktop apps; only their engines (MLT, libopenshot) are agent-relevant, and MLT is covered above.

### Auto-editing intelligence (the actual "editor brain" helpers)
- **auto-editor** — outstanding OSS CLI: analyzes loudness/motion, cuts silence/dead space automatically, can export cutlists to editor timelines ([PyPI](https://pypi.org/project/auto-editor/)). This alone does 60% of a talking-head edit. Free.
- **PySceneDetect** — shot-boundary detection CLI/library (`scenedetect -i video.mp4 detect-content split-video`) for logging multi-shot footage ([scenedetect.com](https://www.scenedetect.com/)). Free.
- **Auto-reframe (16:9 → 9:16):** Google **AutoFlip** (MediaPipe) ([Google Research](https://research.google/blog/autoflip-an-open-source-framework-for-intelligent-video-reframing/)); newer OSS CLIs like [auto-vertical-reframe](https://github.com/KazKozDev/auto-vertical-reframe) (YOLOv11 + ByteTrack, smoothed virtual-camera pans) and [Autocrop-vertical](https://github.com/kamilstanuch/Autocrop-vertical) (YOLOv8 + FFmpeg). All free; auto-vertical-reframe is the most modern.
- **Shot quality scoring / jump-cut smoothing:** no dominant OSS tool — this is where the *vision LLM* (Section 6) earns its keep, scoring frames and choosing takes.

---

## 6. The LLM orchestration layer

**Claude Code (or the Agent SDK headlessly) as the director, bash as the hands, MCPs as the phone lines.** The ecosystem has converged on exactly this pattern in the last six months:

- **Claude-Code-Video-Toolkit** — skills + MCP servers for Remotion, Manim, YouTube clipping, FFmpeg post ([GitHub](https://github.com/wilwaldon/Claude-Code-Video-Toolkit))
- **FFmpeg MCPs** — several: [Video Editor MCP](https://mcpservers.org/servers/Kush36Agrawal/Video_Editor_MCP), [beambuilder/ffmpeg-mcp-server](https://github.com/beambuilder/ffmpeg-mcp-server) (highlight extraction from Claude-chosen segments), [VFX MCP](https://mcpservers.org/servers/conneroisu/vfx-mcp). Honestly, for a CLI agent these are optional — Claude Code runs `ffmpeg` in bash natively; MCPs matter more for non-CLI surfaces.
- **Remotion** — official Claude Code skill; plus [remotion-mcp-app](https://github.com/mcp-use/remotion-mcp-app) with a live interactive player.
- **HeyGen official MCP** — avatar generation as a first-class agent tool ([HeyGen MCP](https://www.heygen.com/model-context-protocol)).
- **HyperFrames** — designed from scratch for this workflow ([MindStudio: Claude Code + Hyperframes workflow](https://www.mindstudio.ai/blog/ai-video-editing-claude-code-hyperframes)).

**"Watching" the footage:** Gemini's video input tokenizes at ~300 tokens/sec of video (258/frame at 1 fps + 32/sec audio) ([Google docs](https://ai.google.dev/gemini-api/docs/video-understanding)). On Gemini Flash-tier pricing that means a full "watch" of a 10-minute raw clip costs **cents** ($0.02–0.20 depending on model tier) ([pricing](https://ai.google.dev/gemini-api/docs/pricing)). The winning pattern: **transcript (Whisper) + scene log (PySceneDetect) + sampled keyframes or a Gemini watch-pass** feed a single edit-planning prompt; Claude writes the JSON cutlist; bash executes. Use Gemini as the cheap eyes, Claude as the editor brain.

---

## 7. Cost modeling (per finished video)

Assumes local compute for FFmpeg/Whisper/HyperFrames (a $50–100/mo VPS or the founder's machine amortizes to pennies per video).

### (a) Talking-head edit — 10 min raw → ~6 min finished
(transcribe → silence-cut → captions → 4 b-roll inserts → music → duck/normalize → render)

| Item | Cost |
|---|---|
| Transcription (faster-whisper local / Whisper API) | $0.00–0.06 |
| Scene detect + silence cut (PySceneDetect, auto-editor) | $0.00 |
| Gemini watch-pass + Claude edit-planning tokens | $0.30–1.50 |
| B-roll: 4 × 5s Seedance clips (+1 retry each) | $0.45–1.10 |
| Music 6 min (Eleven Music $0.15/min) + 5 SFX | $1.00–1.30 |
| Captions/branding render (HyperFrames) + FFmpeg assembly | $0.00 (compute) |
| **Total** | **≈ $1.75–4.00** |

### (b) UGC ad with AI avatar — 30–45s
| Item | Cost |
|---|---|
| Script (Claude) | $0.05–0.20 |
| HeyGen avatar, 0.75 min @ $1–4/min | $0.75–3.00 |
| 2 × Seedance product b-roll clips | $0.25–0.55 |
| Music + SFX + captions + assembly | $0.25–0.40 |
| **Total** | **≈ $1.30–4.15** — vs. Arcads' ~$11/video and $150+ human UGC creators |

### (c) Motion-graphics piece — 30–60s (HyperFrames/Remotion)
| Item | Cost |
|---|---|
| Claude tokens (writing + 2–3 iteration renders) | $1.00–3.00 |
| Music | $0.15 |
| Render compute (local or Lambda pennies) | $0.00–0.10 |
| Remotion license *if used* ($0.01/render, $100/mo min) | $0.01+ |
| **Total** | **≈ $1.15–3.30** |

**Headline: $2–4 COGS per finished video** across all three SKUs. At a $30–100/video or $99–499/mo price point, gross margins are software-grade. The dominant cost is *LLM orchestration tokens*, not media APIs — which means costs fall every time model prices drop.

---

## 8. Recommended v1 stack (opinionated)

**Director:** Claude Code / Claude Agent SDK, one repo, with a `CLAUDE.md` + skills encoding your editing taste (pacing rules, caption style, brand-kit usage). The brand kit is just files in the repo: `brand/logo.svg`, `fonts/`, `colors.json`, `voice.md`.

**Pipeline (all invoked via bash by the agent):**
1. **Ingest & understand:** `ffprobe` → **faster-whisper** (word timestamps, $0) → **PySceneDetect** → optional **Gemini Flash watch-pass** for content notes.
2. **Rough cut:** **auto-editor** for silence/dead-space removal → Claude writes a **JSON cutlist** (your own ~20-line schema: segments, in/out, overlays, audio events) — this file *is* the edit, versionable and human-inspectable.
3. **Assembly:** **FFmpeg** executes the cutlist (trims, concat, xfade, `sidechaincompress` ducking, `loudnorm`).
4. **Captions, lower-thirds, branded intro/outro:** **HyperFrames** (free, Apache 2.0, agent-native) rendering HTML overlays composited by FFmpeg. Swap to **Remotion Automators** ($0.01/render, $100/mo min) when you want its ecosystem and Player for a review UI.
5. **Media generation on demand:** **Seedance 2.0 via fal/BytePlus** for b-roll (~$0.02–0.05/sec), **HeyGen MCP** for avatars, **ElevenLabs** for VO/SFX/music.
6. **Delivery:** MP4 + the cutlist JSON + (later) an OTIO export.

**Defer to v2+:** web timeline UI for human tweaks (build on OpenCut/designcombo + Remotion Player), OTIO interchange, Epidemic Sound partnership, cloud rendering (Rendi/Lambda — only when local stops scaling), Mirage UGC model, auto-reframe SKU (auto-vertical-reframe), multitrack MLT rendering.

**Why this wins:** every deterministic step is free OSS; every paid API sits behind a clean per-unit price; the only novel artifact you own is the cutlist schema plus the prompts/skills that encode editorial judgment. Total fixed cost of the stack: **$0/month** until you adopt Remotion. That is about as lightweight as a video company can be.
