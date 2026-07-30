# Product Backlog (v0 MVP)

**Product:** Brand-Locked Short-Form Video Editor
**Date:** July 2026
**Reads on:** `07-product-spec.md`, `05-user-stories.md`

Phase-ordered by dependency, no time estimates. Each phase ends at a milestone that is demonstrable on real footage. Story references are to `05-user-stories.md`.

Build order rationale: **the edit engine first, the service around it second.** The pipeline is written as a library from the start, so wrapping it in FastAPI is a thin layer rather than a rewrite.

---

## Phase 0 — Foundations

- [x] Project scaffold per house FastAPI conventions: `core/`, `pipeline/`, `llm/`, `app/{routes,service,store,models,schemas,db}`, `brands/`, `assets/`, `storage/`, `web/`.
- [x] `uv` project + `pyproject.toml`, Python 3.12. (mypy runs in default, non-strict mode by explicit choice — not worth the friction pre-Phase-1.)
- [x] `app/config.py` via pydantic-settings — the single reader of `.env` (OpenRouter key/model/fallback, DB URL, storage root, whisper model size).
- [x] `app/logging_config.py` — stdlib logging configured once; never `print()`, never log the API key.
- [x] Database: using **Supabase Postgres** instead of local Postgres/Docker. `migrations.py` is the single idempotent entrypoint (`uv run python migrations.py`) — it imports `app.models` (the ORM classes are the sole source of truth for the schema) and runs `Base.metadata.create_all(checkfirst=True)`. Run manually after adding/changing a model.
- [x] Local toolchain verified: FFmpeg + ffprobe, faster-whisper, auto-editor, PySceneDetect all import and run correctly (confirmed by decoding a real test clip through both PyAV and PySceneDetect in-process).
- [ ] `assets/fonts/` open-licensed fallback fonts + license files. *(still manual — needs actual font downloads)*
- [ ] `assets/music/` 3–5 CC0 tracks + license file per track. *(still manual — needs actual audio downloads)*
- [x] OpenRouter key working; smoke-tested a text call and a vision call. Default model `google/gemma-4-31b-it:free` was rate-limited upstream at test time; settled on `google/gemma-4-26b-a4b-it:free` (primary) + `nvidia/nemotron-nano-12b-v2-vl:free` (fallback) — different providers so one outage doesn't take out both.

### 🏁 M0 — "Environment proven"
Every tool in the stack runs by hand on this machine, and an OpenRouter vision call round-trips an image successfully.

---

## Phase 1 — The edit engine (footage → coherent rough cut)

> The load-bearing path. No API, no captions, no audio yet. (US-A1, US-C2, US-E1)

- [ ] `pipeline/ingest.py` — validate, ffprobe, checksum, 1080p mezzanine for oversized sources, job-dir scaffold.
- [ ] `pipeline/transcribe.py` — faster-whisper → `transcript.json` with word timestamps.
- [ ] `pipeline/analyze.py` — PySceneDetect → `scenes.json`; auto-editor → `silence.json`; 1 fps frame sampling.
- [ ] `core/cutlist.py` — cutlist schema types + validator: non-overlapping segments, `in_s < out_s`, in-bounds timestamps, duration ±15%, word-boundary cuts ±80 ms, no two cuts <0.7 s apart, referenced assets exist.
- [ ] `core/timemap.py` — source-time → output-time mapping **with unit tests**. Load-bearing for caption sync; write the tests first.
- [ ] `llm/openrouter.py` — one client: chat + vision, retry with backoff, fallback model, token/cost accounting returned per call.
- [ ] `llm/prompts/edit_plan.md` — transcript + scenes + silence + sampled frames + brand profile → cutlist. Includes hook doctrine, structure grammar (hook → problem → proof → CTA), pacing rules, and the honesty rule (score top-3 hooks; report a weak best rather than faking one).
- [ ] `pipeline/plan.py` — assembles the planning context, calls OpenRouter, writes `cutlist.v1.json`, runs the validator as a hard gate.
- [ ] `pipeline/assemble.py` — cutlist → FFmpeg trim/concat/center-crop 9:16 → `base.mp4`.
- [ ] Thin CLI runner (`python -m pipeline.run <file> --brand acme --target 60`) for development.

### 🏁 M1 — "It can edit"
A 5-minute self-recorded talking-head becomes a coherent 60-second vertical cut, segments chosen by the LLM, run by one command. Silent, caption-less, unbranded — but the edit judgment is real and the cutlist is valid.

---

## Phase 2 — Brand lock (the cut becomes on-brand)

> (US-B1, US-B2, US-C3)

- [ ] Brand YAML schema as a pydantic model + `app/service/brand_service.py` loader: validate fields, resolve asset paths, fail loudly with the offending field name.
- [ ] One real brand profile in `brands/` with logo + font in `assets/brands/<id>/`.
- [ ] Brand snapshot written into the job dir at job start (reproducibility, US-B2).
- [ ] `core/captions.py` — word→line chunking (≤4 words), casing, safe-zone geometry.
- [ ] `pipeline/overlay.py` — ASS/libass caption generation from transcript + `timemap`, styled from the brand profile (font, colors, active-word highlight); logo watermark; end-card with CTA; composited by FFmpeg.
- [ ] Caption sync verification helper: compare 3 sampled caption timestamps against expected output times.

### 🏁 M2 — "It's on-brand"
The M1 cut now carries brand-styled word-timed captions, logo watermark, and end-card. Sync verified at start, middle, and end. Changing a hex value in the YAML visibly changes the next render.

---

## Phase 3 — Finish quality (sound, drafts, variants, QC)

> (US-C1, US-C4, US-C5, US-D3)

- [ ] `pipeline/audio.py` — music bed from the brand's track, `sidechaincompress` ducking, `loudnorm` −14 LUFS, music resolved under the end-card instead of hard-cut.
- [ ] `pipeline/render.py` — draft mode (720p + "DRAFT" burn-in) and final mode (1080×1920); ffprobe verification of duration/streams before declaring success; idempotent (skips valid existing outputs).
- [ ] Variants: `variants` block in the cutlist → N final renders differing only in the opening segment; named `<brand>_<slug>_hookA_<len>s.mp4`.
- [ ] `llm/prompts/qc.md` + `pipeline/qc.py` — sample 12 frames + first/last + audio stats; vision check for captions in safe zone, logo present and unclipped, face inside crop, no black/frozen frames, end-card rendered, duration in spec; returns pass/fail + specific notes.
- [ ] Per-stage timing + token/cost accumulation recorded through the run.

### 🏁 M3 — "Postable output"
One command takes fresh footage to a QC-passed 1080×1920 final plus two hook variants, with music and captions, that upload to TikTok and Meta without complaint.

---

## Phase 4 — The service (SaaS shape)

> Wrap the engine. Nothing about the pipeline changes here. (US-A1, US-A3, US-D1, US-E2)

- [ ] ORM models, one file per table: `jobs`, `artifacts`, `revisions`; registered via `app/models/__init__`; run `migrations.py` after adding them.
- [ ] Store layer: `job_store.py`, `artifact_store.py`, `revision_store.py` — plain functions, the only code touching a `Session`.
- [ ] `app/service/job_service.py` — orchestrates the pipeline stages, owns the **global single-job lock**, updates status/stage transitions, records cost and timings, raises typed exceptions.
- [ ] Pydantic wire schemas in `app/schemas/`, kept separate from the ORM models.
- [ ] Routes (thin, translating typed exceptions to HTTP): `POST /api/jobs` (multipart, `202` or `409 Busy`), `GET /api/jobs`, `GET /api/jobs/{id}`, `GET /api/jobs/{id}/artifacts/{kind}`, `GET /api/brands`, `GET /api/brands/{id}`, `GET /health`.
- [ ] Job status machine enforced in the service: `pending → running → needs_review → completed`, plus `failed` / `rejected`.
- [ ] Startup reconciliation: any job left `running` is marked `failed` with its stage preserved.
- [ ] `llm/prompts/revise.md` + `POST /api/jobs/{id}/revise` — plain-English notes → cutlist v(n+1) + one-line change summary per note → draft re-render; revision rows retained.
- [ ] `POST /api/jobs/{id}/approve` — finals + variants + QC → `completed`.
- [ ] Re-render knobs without full re-run: `x_offset_pct` crop fix, end-card CTA change (US-D2).
- [ ] Verify every endpoint against the live server, success and failure paths, via `/docs` + curl.

### 🏁 M4 — "It's a service"
A job runs end to end over HTTP: upload → poll status → download draft → post revision notes → approve → download finals. Job history, cost, and timings queryable from the database. Second concurrent upload correctly refused.

---

## Phase 5 — Web UI

> (US-A1, US-A3, US-C1, US-C2, US-D1, US-D3)

- [ ] Single static page served by FastAPI: upload form (file, brand dropdown, target length, variant count, notes).
- [ ] Live status view: current stage, elapsed time, busy indicator when the lock is held.
- [ ] Draft preview inline (`<video>`), plus chosen hook, kept/cut segment counts, QC notes.
- [ ] Notes box → `/revise`; version list with the change summary per version.
- [ ] Approve button → finals with download links per variant.
- [ ] Job history list with status, duration, and cost.

### 🏁 M5 — "Usable without the terminal"
The full loop — upload, watch, review, revise, approve, download — is doable in a browser with no CLI and no curl.

---

## Phase 6 — Hardening

> Make it survive real footage. (US-A2, US-C3, US-E1, US-E3)

- [ ] Ingest guards with plain-English rejection reasons: corrupt file, inaudible/quiet audio (one `afftdn` + gain attempt first), multi-speaker (>15% second speaker), too short (auto-lower target, or reject under 20 s usable), too long (>15 min), oversized (mezzanine path).
- [ ] Whisper hallucination guard: drop transcript words landing inside detected silence before captioning.
- [ ] Profanity / banned-word pass honoring `profanity_policy` (bleep / cut / allow / flag).
- [ ] OpenRouter resilience: 429/404 handling, backoff, fallback model, error naming the model; free-tier daily-limit detection surfaced clearly.
- [ ] Render resilience: one auto-retry, full FFmpeg command line logged per call to the job dir, ffprobe output verification.
- [ ] Stage-level resume verified by killing the process mid-render and re-running.
- [ ] QC tuned against deliberately broken renders: black frames, off-screen captions, clipped logo, cropped face, silent audio.
- [ ] Model bake-off: same 3 sources through 2 free and 1 cheap paid OpenRouter model; pick the default on edit quality, record the comparison.

### 🏁 M6 — "Hardened"
Every deliberately broken input (silent audio, 4 GB 4K60 file, 20-minute ramble, two speakers, profanity, killed mid-render) produces either a correct output or a specific, actionable failure — never a silent one, never a hang.

---

## Phase 7 — Real use

- [ ] Run 10 real jobs on genuinely different footage (different lighting, accents, lengths, aspect ratios).
- [ ] Log every manual intervention; classify as bug / missing guard / model judgment; fix the bugs.
- [ ] Confirm the economics: median LLM cost per job, median wall-clock, QC first-try pass rate, hook-kept rate.
- [ ] Tune `edit_plan.md` against the collected failures — this prompt is the product.

### 🏁 M7 — "It actually works"
10 consecutive real jobs, median ≤1 revision round, median LLM cost under $0.05, and the operator would post the output without touching another editor.

---

## Deferred (each with a trigger)

| Item | Trigger |
|---|---|
| Per-brand correction memory feeding the planner | the same revision note is given twice for one brand |
| HTML/CSS caption + end-card renderer (HyperFrames) | ASS styling can't match a brand's look |
| Parallel jobs / real queue | waiting on the single-job lock becomes routine |
| Multi-tenancy, auth, billing | someone other than the operator needs access |
| Cloud storage + hosted deployment | jobs need to run off this machine |
| Subject-tracking auto-reframe | second job where the speaker leaves a center crop |
| TTS hook cards (Kokoro-82M, Apache-2.0) | a job needs a spoken line the speaker never said |
| AI music / b-roll generation | a commercially-safe free-or-cheap option exists |
