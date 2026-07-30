# editor

A local tool that takes raw talking-head video footage and a brand profile (a YAML file) and produces a finished, brand-locked 9:16 short-form video. Word-level transcription, silence removal, and edit planning are done with an LLM (via OpenRouter); cutting, cropping, captions, and audio are done with FFmpeg.

It's built as a FastAPI service with jobs persisted in Postgres (via Supabase) — shaped like a SaaS — but right now it runs entirely on one person's machine, for one operator, with no auth, multi-tenancy, or billing. See `docs/07-product-spec.md` (sections 1 and 11) for why.

## Current status

Early. Phase 0 (project scaffold, config, logging, DB migrations, local toolchain) is done.

Phase 1 (the actual edit engine) is in progress: ingest, transcription, scene/silence analysis, the cutlist schema and validator, source-to-output time mapping (with unit tests), the OpenRouter client, and the edit-planning prompt are all implemented and have been exercised end to end on real footage — there's a real job directory under `storage/jobs/` with a transcript, scene/silence analysis, and a generated `cutlist.v1.json` to show for it.

Not yet built: the assemble stage that turns a cutlist into an actual rendered clip (`pipeline/assemble.py`), and a CLI runner to drive the pipeline from the command line. The FastAPI app currently only exposes `/health` — no job routes, no brand loading, no web UI yet. See `docs/06-product-backlog.md` for the full phase-by-phase plan.

## Requirements

- Python 3.12+
- [uv](https://docs.astral.sh/uv/)
- FFmpeg (with ffprobe) on your PATH
- A Postgres database — this repo uses Supabase Postgres, not a local instance
- An [OpenRouter](https://openrouter.ai/keys) API key (a vision-capable model is needed for edit planning and QC)

## Setup

```bash
uv sync
cp .env.example .env
# fill in .env: OPENROUTER_API_KEY, OPENROUTER_MODEL, OPENROUTER_FALLBACK_MODEL,
# DATABASE_URL (your Supabase Postgres connection string), WHISPER_MODEL_SIZE
uv run python migrations.py
```

`migrations.py` is idempotent — it imports `app.models` and creates any missing tables. Re-run it after adding or changing a model.

To run the API:

```bash
uv run uvicorn app.main:app --reload
```

There is no CLI pipeline runner yet (`pipeline/assemble.py` and a `python -m pipeline.run ...` entrypoint are still on the backlog for Phase 1).

## Development

```bash
uv run mypy .
uv run ruff check .
uv run pytest
```

## Project layout

- `app/` — the FastAPI service: routes, service layer, store layer, ORM models, pydantic schemas, DB session, config.
- `core/` — pure logic, no I/O: cutlist schema/validation, source-to-output time mapping.
- `pipeline/` — the video processing stages (ingest, transcribe, analyze, plan, ...), each a plain function that shells out and writes an artifact to disk.
- `llm/` — the OpenRouter client and the prompt templates used for edit planning, revision, and QC.
- `brands/` — brand profile YAML files, one per brand.
- `assets/` — brand assets (logos, fonts) and a local music library.
- `storage/` — per-job working directories (gitignored; disposable, reconstructible from source + cutlist).
- `web/` — the (not yet built) minimal static web UI.

## Docs

The full product spec, architecture, user stories, and phase-by-phase backlog live in `docs/`. Start with `docs/07-product-spec.md`.
