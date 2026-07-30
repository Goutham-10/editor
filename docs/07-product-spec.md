# Product Spec & Technical Architecture (v0 MVP)

**Product:** Brand-Locked Short-Form Video Editor
**Date:** July 2026
**Status:** This doc supersedes `03-mvp-plan.md` wherever they disagree. See §11 for what changed and why.

---

## 1. What we are building

**One line:** Upload raw talking-head footage, pick a brand profile, get back a finished brand-locked 9:16 short.

This is a **product**, not an agency workflow. There is no client onboarding, no account management, no Drive folders, no email loop. There is a service that takes a video file plus a brand profile and returns an edited video file.

**v0 runs entirely on the operator's machine** — local filesystem, local Postgres, local FFmpeg/Whisper — but it is **shaped like a SaaS from day one**: an HTTP API over a layered FastAPI service, jobs persisted in a database, artifacts addressed by job id, and a thin web UI. Going hosted later means changing where files and the database live, not rewriting the product.

**Core loop:**

```
raw footage + brand.yaml  →  [ one synchronous job ]  →  edited 9:16 MP4 (+ hook variants)
```

**Who uses it:** one operator/creator running their own footage through it. Multi-tenant users, auth, and billing are explicitly not in v0.

## 2. Scope

### In scope (v0)

- Single-speaker talking-head source, 1–15 minutes, any aspect, uploaded as one file.
- Word-level transcription (faster-whisper, local, free).
- Silence / dead-air / filler removal.
- LLM edit planning via **OpenRouter**: transcript + scene log + silence map + sampled frames → `cutlist.json`.
- 9:16 output with center-weighted crop and a manual horizontal-offset knob.
- Brand config as a **YAML file** — colors, fonts, caption style, logo, end-card, music, output targets.
- Word-timed brand-styled burned-in captions.
- Logo watermark + branded end-card with CTA.
- Background music from a local pre-cleared library, ducked under the voice, loudness-normalized to −14 LUFS.
- Up to 3 hook variants (same body, different opening 3–5 s).
- Draft render → review → revise-by-plain-English-notes → final render.
- Automated QC pass (sampled frames + audio stats) before a job is marked complete.
- HTTP API + minimal web UI: upload, watch progress, preview, download, revise.
- One job at a time, run synchronously end to end.

### Out of scope (v0)

- Multi-tenancy, auth, accounts, billing.
- Parallel jobs, queues, workers, autoscaling. Second job while one is running gets `409 Busy`.
- Any paid API. No ElevenLabs, no fal/Seedance, no hosted transcription.
- Cloud storage, Drive integration, email/link delivery.
- Multi-speaker, multicam, long-form, AI avatars, motion graphics beyond captions/end-card.
- Subject-tracking auto-reframe (center crop + manual offset only).
- Per-brand learning memory (`corrections.md`) — deferred, see §10.
- Brand-kit onboarding flows, kit proposals, client sign-off. A brand profile is a YAML file the operator writes.

## 3. Product requirements

| Requirement | Target |
|---|---|
| Input | 1 video file, 1–15 min, ≤4 GB, single primary speaker |
| Output | 1080×1920 MP4, H.264 + AAC, −14 LUFS, platform-upload-clean |
| Output length | 15–90 s, within ±15% of requested target |
| Hook variants | 0–3, differing only in the opening 3–5 s |
| Job runtime | ≤ 1.5× source duration on the operator's machine (5-min source → ≤8 min job) |
| Concurrency | Exactly 1 job at a time |
| LLM cost per job | ≤ $0.05 on cheap paid models; $0 on free-tier models |
| Non-LLM cost per job | $0 |
| Human touchpoints | 1 (draft review) |
| Recoverability | Any stage re-runnable from on-disk artifacts without redoing earlier stages |

## 4. The free/cheap stack

| Concern | Choice | License / cost | Notes |
|---|---|---|---|
| LLM (planning, revision, QC) | **OpenRouter**, model set by `OPENROUTER_MODEL` | free-tier models $0; cheap paid ≈$0.01–0.05/job | Free tier: 20 req/min, 50 req/day unfunded, 1000/day after a one-time $10 credit purchase. Vision-capable free models exist (Gemma-4 family, Nemotron Nano Omni) and are needed for the frame watch-pass + QC. Swap models by env var — the catalog churns. |
| Speech-to-text | **faster-whisper**, local | MIT, $0 | Word-level timestamps. Runs on CPU; GPU if available. |
| Text-to-speech *(optional)* | **Kokoro-82M**, local | Apache-2.0, $0 | 82M params, ~327 MB, CPU-capable, commercial use permitted. Only used if a job needs a spoken hook card or end-card VO. Off by default — v0 may never call it. |
| Music | **Local pre-cleared library** (`assets/music/`) | CC0 / Pixabay / Mixkit, $0 | No generation. Each track ships with its license file. Caution: verify tracks aren't Content-ID registered before commercial delivery. |
| Scene detection | PySceneDetect | MIT, $0 | |
| Silence map | auto-editor (analysis only) | Unlicense, $0 | |
| Cut / concat / crop / audio / composite | **FFmpeg** direct | LGPL, $0 | `sidechaincompress`, `loudnorm`, `afftdn`, `eq` |
| Captions & end-card | **libass/ASS subtitles** via FFmpeg | $0 | Word-timed karaoke styling with brand fonts/colors, no browser dependency. HTML/CSS overlay (HyperFrames) is a Phase-4 upgrade if ASS styling hits a ceiling. |
| API | FastAPI + uvicorn | $0 | |
| Database | Postgres, local | $0 | Job/artifact/revision records. Docker one-liner. |
| Storage | Local filesystem | $0 | `storage/jobs/<job_id>/` |
| Compute | Operator's machine | $0 | |

**Deliberately rejected:** ElevenLabs (paid), Stable Audio Open (non-commercial license), MusicGen (CC-BY-NC weights), Suno-style wrappers (legally gray), fal/Seedance (paid, off by default), Remotion (license cost).

## 5. Architecture

### 5.1 Shape

Three layers, inside-out:

1. **`core/`** — pure logic, zero I/O: cutlist schema, validation rules, source-time→output-time mapping, hook scoring helpers, caption chunking. Unit-testable in isolation.
2. **`pipeline/`** — the video stages. Each is a plain function `(job_dir, config) → artifact`, shells out to FFmpeg/Whisper, writes its artifact to disk, and is idempotent (skips if its output exists and is valid).
3. **`app/`** — the FastAPI service: `routes → service → store → DB`, per house conventions. `job_service.py` orchestrates the pipeline; routes stay thin; only `store/` touches a `Session`.

The pipeline is a **library, not a pile of CLI scripts**. The CLI runner and the HTTP API are both thin callers of the same functions — which is what makes "local v0 today, hosted service later" a config change instead of a rewrite.

### 5.2 Layout

```
editor/
├── migrations.py                # idempotent schema entrypoint — imports app.models (the sole source of truth) and create_all's
├── pyproject.toml               # uv-managed; mypy strict
├── core/                        # PURE — no I/O, no FastAPI, no SQLAlchemy
│   ├── cutlist.py               #   schema types + validation rules
│   ├── timemap.py               #   source-time → output-time mapping (unit-tested)
│   └── captions.py              #   word→line chunking, safe-zone math
├── pipeline/                    # stages: shell out, write artifacts, idempotent
│   ├── ingest.py  transcribe.py  analyze.py  plan.py
│   ├── assemble.py  overlay.py  audio.py  render.py  qc.py
├── llm/
│   ├── openrouter.py            # single OpenRouter client (chat + vision)
│   └── prompts/                 # edit_plan.md, revise.md, qc.md
├── app/
│   ├── main.py                  # FastAPI() + router mount loop only
│   ├── config.py                # pydantic-settings — the ONLY reader of .env
│   ├── deps.py  logging_config.py
│   ├── db/session.py
│   ├── models/job/              # ORM, one file per table
│   │   ├── job.py  artifact.py  revision.py
│   ├── schemas/                 # pydantic wire contracts
│   │   ├── job.py  brand.py
│   ├── routes/                  # thin; __init__ exposes ALL_ROUTERS
│   │   ├── job_routes.py  brand_routes.py  health_routes.py
│   ├── service/
│   │   ├── job_service.py       # orchestrates pipeline stages, owns the job lock
│   │   └── brand_service.py     # loads + validates brand YAML
│   └── store/
│       ├── job_store.py  artifact_store.py  revision_store.py
├── brands/                      # <brand_id>.yaml — the brand profiles
├── assets/
│   ├── brands/<brand_id>/       # logo.png, fonts/
│   ├── fonts/                   # bundled open-licensed fallbacks
│   └── music/                   # CC0 library + license files
├── storage/jobs/<job_id>/       # gitignored working dirs
│   ├── source.mp4  mezzanine.mp4
│   ├── analysis/{transcript,scenes,silence}.json  frames/
│   ├── cutlist.v1.json  cutlist.v2.json
│   └── renders/{draft.mp4,final.mp4,final_hookA.mp4,...}
└── web/                         # minimal static UI (upload / status / preview / download)
```

### 5.3 Pipeline stages

```
ingest      ffprobe, validate, checksum, 1080p mezzanine if oversized
transcribe  faster-whisper → transcript.json (word timestamps)
analyze     PySceneDetect → scenes.json; auto-editor → silence.json; 1 fps frames/
plan        OpenRouter: transcript + scenes + silence + sampled frames + brand.yaml → cutlist.json
validate    core/cutlist.py rules — hard gate, no render without a valid cutlist
assemble    FFmpeg trim/concat/crop → base.mp4
overlay     ASS captions + logo watermark + end-card → composited.mp4
audio       music bed + sidechain duck + loudnorm −14 LUFS
render      draft (720p, "DRAFT" burn-in) or final (1080×1920, one per variant)
qc          OpenRouter vision on sampled frames + audio stats → pass/fail + notes
```

Every stage writes into the job dir; nothing lives only in memory. Stage failures record which stage failed, and a re-run resumes from that stage.

### 5.4 Cutlist — the one real artifact

Authored by the LLM, executed by FFmpeg, validated by `core/`, versioned per revision, diffable, replayable.

```json
{
  "version": 1,
  "job_id": "0f3c…",
  "brand": "acme",
  "output": { "aspect": "9:16", "resolution": [1080,1920], "target_duration_s": 60,
              "crop": { "mode": "center", "x_offset_pct": 0 } },
  "segments": [
    { "id": "hook",   "in_s": 143.20, "out_s": 147.85, "role": "hook",
      "note": "strongest line: 'we lost $40k learning this'" },
    { "id": "body-1", "in_s": 12.40,  "out_s": 31.10,  "role": "body" },
    { "id": "cta",    "in_s": 231.00, "out_s": 238.20, "role": "cta", "transition_out": "fade" }
  ],
  "overlays": [
    { "type": "captions", "source": "transcript.json", "burn": true },
    { "type": "watermark", "position": "top-right" },
    { "type": "endcard", "duration_s": 2.5 }
  ],
  "audio": [
    { "type": "music", "track": "assets/music/warm-acoustic-01.mp3", "gain_db": -18, "duck": true },
    { "type": "loudnorm", "target_lufs": -14 }
  ],
  "variants": [
    { "id": "hookA", "replace_segment": "hook", "in_s": 143.20, "out_s": 147.85 },
    { "id": "hookB", "replace_segment": "hook", "in_s": 8.10,   "out_s": 12.05 }
  ],
  "qc_notes": "speaker looks off-camera at 78.2s"
}
```

**Validator rules (hard gate):** segments non-overlapping; `in_s < out_s`; all timestamps within source bounds; total duration within ±15% of target; cut points land on word boundaries (±80 ms per the transcript); no two cuts closer than 0.7 s; every referenced asset exists on disk.

### 5.5 Brand profile YAML

One file per brand in `brands/`. The operator writes it by hand; the service validates it against a pydantic schema on load and returns a clear error if it's malformed.

```yaml
id: acme
name: Acme Skincare
colors:
  primary: "#1A6B54"
  accent: "#F4C95D"
  caption_text: "#FFFFFF"
  caption_highlight: "#F4C95D"     # active-word color
fonts:
  captions: assets/brands/acme/fonts/AcmeSans-Bold.ttf
  fallback: assets/fonts/Montserrat-Bold.ttf
captions:
  style: word-pop                  # word-pop | karaoke | blocks
  position: lower-third
  max_words_per_line: 4
  uppercase: true
logo:
  file: assets/brands/acme/logo.png
  position: top-right
  opacity: 0.85
endcard:
  enabled: true
  duration_s: 2.5
  cta_text: "Shop now → acme.com"
music:
  track: assets/music/warm-acoustic-01.mp3
  gain_db: -18
  duck: true
output:
  aspect: "9:16"
  resolution: [1080, 1920]
  loudness_lufs: -14
rules:
  banned_words: ["cheap"]
  profanity_policy: bleep          # bleep | cut | allow | flag
```

### 5.6 Data model

Three tables. Brand profiles are **not** in the database — they are YAML files, read at job start and snapshotted into the job dir so a job is reproducible even if the YAML later changes.

- **`jobs`** — `id` (uuid), `brand_id`, `status`, `stage`, `source_filename`, `source_duration_s`, `target_duration_s`, `variant_count`, `notes`, `error_stage`, `error_message`, `llm_tokens_in/out`, `llm_cost_usd`, `created_at`, `started_at`, `finished_at`.
- **`artifacts`** — `id`, `job_id`, `kind` (`transcript` | `cutlist` | `draft` | `final` | `variant` | `qc_report`), `path`, `variant_id`, `created_at`.
- **`revisions`** — `id`, `job_id`, `version`, `notes_text`, `cutlist_path`, `change_summary`, `created_at`.

**Job status machine:** `pending → running → needs_review → (revising → needs_review)* → completed`, plus terminal `failed` (pipeline error) and `rejected` (footage unusable — flagged at ingest before any edit work).

### 5.7 Concurrency: exactly one job

A single in-process worker with a global job lock. `POST /jobs` accepts only when the lock is free; otherwise `409 Busy` with the running job's id.

The pipeline itself is **straight-line synchronous** — one stage after another, no fan-out, no task queue, no Celery/Redis. The API returns `202 Accepted` with a job id rather than blocking the HTTP connection for the several minutes a render takes, and the client polls `GET /jobs/{id}`. Same single-job semantics, without a 6-minute request that any proxy would time out.

Restart behavior: a job left `running` at startup is marked `failed` with `error_stage` preserved; its artifacts are still on disk, so a re-run resumes.

### 5.8 API surface

| Method | Path | Purpose |
|---|---|---|
| `GET` | `/health` | liveness + whether the worker is busy |
| `GET` | `/api/brands` | list valid brand profiles found in `brands/` |
| `GET` | `/api/brands/{id}` | one profile, parsed and validated |
| `POST` | `/api/jobs` | multipart: file + `brand_id` + `target_duration_s` + `variant_count` + `notes` → `202 {job_id}` or `409` |
| `GET` | `/api/jobs` | job history |
| `GET` | `/api/jobs/{id}` | status, stage, progress, chosen hook, qc notes, cost, artifact list |
| `GET` | `/api/jobs/{id}/artifacts/{kind}` | stream/download draft, final, variant, transcript, cutlist |
| `POST` | `/api/jobs/{id}/revise` | plain-English notes → new cutlist version → re-render draft |
| `POST` | `/api/jobs/{id}/approve` | render finals + variants, run QC, mark complete |

### 5.9 Web UI (minimal, one page)

Upload form (file, brand dropdown, target length, variant count, notes) → live status with current stage → inline `<video>` preview of the draft → notes box that posts to `/revise` → Approve button → download links for finals. Static HTML/JS served by FastAPI. No framework, no build step, no auth.

## 6. Edge cases (v0 posture)

Detect cheaply at ingest or QC → fix with one simple knob → otherwise fail the job with a specific human-readable reason. No clever subsystems.

| Case | Detection | v0 handling |
|---|---|---|
| Bad/quiet audio | ffprobe loudness + Whisper mean word confidence | one `afftdn` + gain attempt; still bad → `rejected` with reason |
| Multiple speakers | dialogue pattern in transcript | proceed only if one speaker >85% of words; else `rejected` |
| Horizontal source | ffprobe aspect | center crop; QC checks face position; operator sets `x_offset_pct` and re-renders |
| Too short (<90 s for a 60 s target) | duration at ingest | auto-lower target and say so; <20 s usable → `rejected` |
| Too long (>15 min) | duration at ingest | `rejected` with "trim to the relevant 15 minutes" |
| Huge file (>4 GB / 4K60) | ffprobe at ingest | transcode 1080p mezzanine, use it for everything; keep original untouched |
| Profanity / banned words | transcript scan | per-brand `profanity_policy` |
| Over-aggressive silence cuts | validator: no two cuts <0.7 s apart; keep ≥150 ms sentence-end gaps | conservative auto-editor margins; human catches the rest at draft |
| Caption drift after concat | QC checks 3 random captions ±100 ms | captions re-timed from `core/timemap.py`, never by re-transcribing the render |
| Whisper hallucination in silence | words landing inside detected silence | dropped before captioning |
| No usable hook | planner scores top-3 candidates and must report a weak best | fall back to a caption-card hook; still weak → flag in job, don't fake it |
| OpenRouter rate limit / model unavailable | HTTP 429 / 404 from OpenRouter | one retry with backoff, then fall back to `OPENROUTER_FALLBACK_MODEL`, then fail the stage with the model name in the error |
| Render failure mid-pipeline | non-zero exit; ffprobe verifies output duration/streams | one auto-retry, then `failed` with the stage recorded; every FFmpeg command line logged to the job dir |

## 7. Metrics

Recorded on the `jobs` row, no spreadsheet needed:

- **Cost per job** — LLM tokens in/out and USD (everything else is $0). Alarm above $0.10.
- **Wall-clock per job**, and per stage — tells you what to optimize.
- **Revision rounds** per job (target: median ≤1).
- **QC first-try pass rate**.
- **Failure rate by stage and reason category** (footage quality / pipeline bug / model judgment / rate limit).
- **Hook kept** — did the operator keep the model's chosen hook? The single best proxy for edit judgment.

## 8. Risks

| Risk | Mitigation |
|---|---|
| Free OpenRouter models too weak for edit judgment | model is one env var; benchmark free vs. cheap paid on the same 3 sources and pick on quality, not price |
| Free-tier rate limits (50/day unfunded) block a work session | one-time $10 credit lifts it to 1000/day; fallback model configured |
| Caption desync after concat | pure `timemap` function with unit tests; QC spot-check |
| ASS caption styling can't hit the brand look | HyperFrames HTML overlay is the named Phase-4 upgrade |
| Music Content-ID claims despite "free" license | verify each library track before use; keep the license file next to the track |
| Job runtime too slow on CPU | mezzanine transcode; whisper model size configurable; GPU if present |
| Local-only design leaks into hosted later | storage and DB access behind config; no absolute paths outside `config.py` |

## 9. Manual setup (accounts, keys, assets)

Short list — that's the point of this stack.

1. **OpenRouter account** → create API key → `OPENROUTER_API_KEY`. Optional but recommended: buy $10 of credit once, which raises free-model limits from 50 to 1000 requests/day and unlocks cheap paid models as a fallback.
2. **Local tooling:** Python 3.12+, `uv`, FFmpeg (with ffprobe), Docker (for Postgres) or a native Postgres.
3. **Python deps** via `uv add`: fastapi, uvicorn, sqlalchemy, psycopg, pydantic-settings, faster-whisper, auto-editor, scenedetect, pyyaml, httpx. First faster-whisper run downloads model weights (~1–3 GB).
4. **Fonts:** download open-licensed fallbacks (e.g., Montserrat, OFL) into `assets/fonts/` with the license file.
5. **Music:** download 3–5 CC0 tracks (Pixabay / Mixkit / FMA CC0) into `assets/music/`, license file next to each.
6. **Brand assets:** for each brand, a transparent-PNG logo and its font file into `assets/brands/<id>/`, then write `brands/<id>.yaml`.
7. **Disk:** ≥100 GB free, or point `storage/` at an external drive.

Not needed: ElevenLabs, fal, Google Drive, cloud storage, domain, hosting, Stripe.

## 10. Deferred (each with a trigger)

| Deferred | Trigger to build |
|---|---|
| Per-brand correction memory (revision notes fed back into planning) | the same note gets given twice for one brand |
| HTML/CSS caption & end-card renderer (HyperFrames) | ASS styling can't match a brand's look |
| Parallel jobs / real queue | one operator is waiting on the lock regularly |
| Multi-tenancy, auth, billing | someone other than the operator needs access |
| Cloud storage + hosted deploy | jobs need to run away from the operator's machine |
| Subject-tracking auto-reframe | second job where the speaker moves out of a center crop |
| AI music/b-roll generation | a licensed, commercially-safe, free-or-cheap option exists |
| TTS hook cards (Kokoro) | a real job needs a spoken line the speaker never said |

## 11. What changed from `03-mvp-plan.md`

1. **Product, not agency.** Client onboarding, brand-kit sign-off, intake forms, delivery links, invoicing, and design-partner management are all cut. The deliverable is a working editor, not a service business.
2. **Brand config is a YAML file**, hand-written by the operator, validated on load, snapshotted per job. No onboarding flow.
3. **Local-only v0.** No Google Drive, no shared folders, no cloud storage. Uploads hit an HTTP endpoint; artifacts live in `storage/jobs/<job_id>/`.
4. **Free/cheap stack only.** OpenRouter replaces direct paid LLM calls; a local CC0 music library replaces ElevenLabs; Kokoro (Apache-2.0) covers TTS if ever needed; Seedance/fal stays out. FFmpeg + libass replaces the browser-based overlay renderer for v0.
5. **One synchronous job at a time.** No queue, no workers, no parallelism; a second submission gets `409 Busy`.
6. **SaaS-shaped from day one.** FastAPI service with `routes → service → store → DB` layering, job records in Postgres, an HTTP API, and a minimal web UI — so "hosted" later is a deployment change, not a rewrite.

---

**Sources for stack choices:** [OpenRouter free models](https://openrouter.ai/collections/free-models) · [OpenRouter vision models](https://openrouter.ai/collections/vision-models) · [Kokoro-82M (Apache-2.0)](https://kokorottsai.com/) · [Pixabay music licensing](https://pixabay.com/music/) · [Stable Audio Open license terms](https://huggingface.co/stabilityai/stable-audio-open-1.0)
