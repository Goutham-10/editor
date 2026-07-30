# User Stories (v0 MVP)

**Product:** Brand-Locked Short-Form Video Editor
**Date:** July 2026
**Reads on:** `07-product-spec.md` (canonical)

One actor: **the user** — a creator/marketer/operator who has raw footage and a brand profile, running the tool on their own machine. No clients, no onboarding flows, no accounts in v0.

Stories are grouped by the loop they belong to: submit → get an edit back → adjust → finish. Everything below is about the core product: **raw footage in, edited footage out.**

---

## Epic A — Submit a job

### US-A1: Upload footage and get an edit
**As a** user, **I want** to upload one raw video, pick a brand, and say how long I want the output, **so that** I get a finished branded short back without touching an editor.

Acceptance criteria:
- I upload a single file (1–15 min, up to 4 GB) through the web UI or `POST /api/jobs`.
- I choose a brand profile from the list, a target duration, and optionally a variant count and free-text notes.
- The job starts immediately and I get a job id back.
- When it finishes I have a downloadable 9:16 MP4 that matches my brand profile.

### US-A2: Be told immediately when footage is unusable
**As a** user, **I don't want** to wait through a full job to learn the footage was never going to work.

Acceptance criteria:
- Corrupt files, inaudible audio, >15 min sources, multi-speaker footage, and sources too short for the target are rejected at ingest — before any transcription or render work.
- The job ends in `rejected` with a specific, plain-English reason and what to do about it (re-shoot, trim, lower the target).
- Rejection happens within the first minute of the job, not at the end.

### US-A3: Know the tool is busy
**As a** user, **I want** a clear answer when I submit while another job is running, **so that** I'm never confused about whether my upload was accepted.

Acceptance criteria:
- Submitting while a job is running returns `409 Busy` naming the running job.
- The UI shows the running job and its current stage instead of accepting a second upload.

---

## Epic B — Control the look (brand profile)

### US-B1: Define a brand in one YAML file
**As a** user, **I want** all brand rules in a single readable YAML file, **so that** I can change the look without touching code.

Acceptance criteria:
- One file per brand in `brands/<id>.yaml` covering colors, fonts, caption style, logo, end-card CTA, music track, output resolution/loudness, and word rules.
- Editing the YAML and re-running a job changes the output accordingly — no code change, no restart required.
- The profile is validated on load; a malformed or missing-asset profile produces a clear error naming the field, not a mid-render crash.

### US-B2: Reproducible output per job
**As a** user, **I want** a job to stay reproducible even after I edit the brand file, **so that** re-rendering an old job doesn't silently change it.

Acceptance criteria:
- The resolved brand profile is snapshotted into the job directory at job start.
- Re-running an old job's cutlist reproduces an equivalent video, using the snapshot, not the current YAML.

---

## Epic C — Get a usable edit back

### US-C1: See a draft before finals
**As a** user, **I want** a fast watermarked draft first, **so that** I can react before spending time on full-resolution renders.

Acceptance criteria:
- Draft is 720p with a "DRAFT" burn-in, correct 9:16 aspect, within ±15% of my target length.
- Draft is previewable inline in the UI and downloadable.
- The job moves to `needs_review` and waits for me.

### US-C2: Understand what the editor did
**As a** user, **I want** the job to tell me what it chose and why, **so that** I can judge the edit instead of guessing.

Acceptance criteria:
- The job detail shows the chosen hook line, the number of segments kept vs. cut, final duration, and any QC notes or flags.
- The full `cutlist.json` and `transcript.json` are downloadable.
- If the planner found no strong hook, it says so explicitly rather than shipping a weak one silently.

### US-C3: Word-accurate branded captions
**As a** user, **I want** captions that are on-brand, in sync, and readable, **so that** the output is postable as-is.

Acceptance criteria:
- Captions come only from the transcript — never invented words.
- Captions stay in sync throughout, verified at the start, middle, and end (±100 ms).
- Styling (font, colors, active-word highlight, casing, ≤4 words per line) comes from the brand profile; captions sit in the safe zone and never cover the speaker's mouth.

### US-C4: Clean audio
**As a** user, **I want** the audio to sound finished, **so that** I don't have to run it through anything else.

Acceptance criteria:
- Background music from the brand's chosen track, ducked under the voice.
- Output normalized to −14 LUFS with no clipping.
- No abrupt music cut at the end — it resolves under the end-card.

### US-C5: Hook variants
**As a** user, **I want** up to 3 versions that differ only in the opening, **so that** I can A/B them.

Acceptance criteria:
- I set a variant count at submission (0–3).
- Variants share the identical body and differ only in the opening 3–5 s.
- Each is a separate download with a clear name (`acme_hookA_60s.mp4`) and a one-line description of its hook.

---

## Epic D — Adjust and finish

### US-D1: Revise with plain English
**As a** user, **I want** to type notes in normal language, **so that** I don't have to learn timestamps or edit jargon.

Acceptance criteria:
- I post notes like "hook feels slow, captions cover her face around 0:22" to `/api/jobs/{id}/revise`.
- The system writes a new cutlist version and re-renders the draft.
- The response summarizes what changed in one line per note, and says so plainly if a note couldn't be applied.
- Every cutlist version is retained; I can see the diff between versions.

### US-D2: Fix a bad crop myself
**As a** user, **I want** a simple horizontal-offset knob when the center crop cuts off the speaker, **so that** an otherwise good edit isn't wasted.

Acceptance criteria:
- QC flags an off-center face in the draft.
- I set an `x_offset_pct` and re-render without redoing transcription, analysis, or planning.

### US-D3: Approve and get finals
**As a** user, **I want** approval to produce upload-ready files, **so that** nothing further is needed before posting.

Acceptance criteria:
- On approve, finals render at 1080×1920 (main cut + each variant), watermark-free.
- H.264 + AAC, −14 LUFS, sensible filenames, and they upload to TikTok/Meta without re-encoding complaints.
- The QC pass runs before the job is marked `completed`; a failed QC surfaces the specific problem instead of completing quietly.

---

## Epic E — Operability

### US-E1: Never lose work to a crash
**As a** user, **I want** a failed job to be resumable, **so that** a crash at the render stage doesn't cost me the transcription and planning.

Acceptance criteria:
- Every stage writes its artifact to the job directory before the next begins.
- A failure records which stage failed and why; re-running resumes from that stage.
- A job left running when the server restarts is marked failed with its stage preserved — never stuck in limbo.

### US-E2: See what a job cost and how long it took
**As a** user, **I want** cost and timing per job, **so that** I know if this is economical at volume.

Acceptance criteria:
- Each job records LLM tokens in/out, USD cost, total wall-clock, and per-stage timings.
- Job history lists these across jobs.
- LLM cost above $0.10 is visibly flagged.

### US-E3: Swap the LLM without a code change
**As a** user, **I want** to change models via config, **so that** I can trade quality against cost as the OpenRouter catalog changes.

Acceptance criteria:
- The planning/QC model is set by an env var, with a configured fallback model.
- Rate limits or an unavailable model produce a retry, then a fallback, then a clear error naming the model — never a silent low-quality result.
