"""Thin CLI runner for development: chains ingest -> transcribe -> analyze ->
plan -> assemble and prints a summary. All logic lives in the pipeline/core/
llm modules above — this file is just a caller.

Usage:
    python -m pipeline.run <source.mp4> --target 60 --brand-name "Test Brand"
"""

from __future__ import annotations

import argparse
import logging
import sys
import time
from collections.abc import Sequence
from pathlib import Path

from app.logging_config import configure_logging
from pipeline.analyze import analyze
from pipeline.assemble import assemble
from pipeline.ingest import ingest
from pipeline.plan import plan
from pipeline.transcribe import transcribe

logger = logging.getLogger(__name__)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Run the Phase 1 edit pipeline end to end on one source video."
    )
    parser.add_argument("source", type=Path, help="path to the raw source video")
    parser.add_argument(
        "--target", type=float, default=60.0, help="target output duration, seconds"
    )
    parser.add_argument("--brand-name", type=str, default="Untitled Brand")
    parser.add_argument("--brand-notes", type=str, default="")
    parser.add_argument(
        "--whisper-model", type=str, default=None, help="override WHISPER_MODEL_SIZE for this run"
    )
    args = parser.parse_args(argv)

    configure_logging()
    t_start = time.monotonic()

    logger.info("ingesting %s", args.source)
    ingest_result = ingest(args.source)
    job_dir = ingest_result.job_dir
    video_path = ingest_result.working_video_path

    logger.info("job %s: transcribing", ingest_result.job_id)
    transcribe(job_dir, video_path, model_size=args.whisper_model)

    logger.info("job %s: analyzing", ingest_result.job_id)
    analyze(job_dir, video_path)

    logger.info("job %s: planning", ingest_result.job_id)
    plan_result = plan(
        job_dir,
        target_duration_s=args.target,
        brand_name=args.brand_name,
        brand_notes=args.brand_notes,
        job_id=ingest_result.job_id,
        source_duration_s=ingest_result.duration_s,
    )

    logger.info("job %s: assembling", ingest_result.job_id)
    output_path = assemble(job_dir, plan_result.cutlist, video_path)

    elapsed_s = time.monotonic() - t_start
    output_duration_s = sum(s.out_s - s.in_s for s in plan_result.cutlist.segments)

    print()
    print("=== Job complete ===")
    print(f"job dir:         {job_dir}")
    print(f"source duration: {ingest_result.duration_s:.1f}s")
    print(f"output duration: {output_duration_s:.1f}s (target {args.target:.1f}s)")
    print(f"output file:     {output_path}")
    print(f"chosen hook:     {plan_result.hook_note or '(none flagged — see qc_notes)'}")
    if plan_result.cutlist.qc_notes:
        print(f"qc_notes:        {plan_result.cutlist.qc_notes}")
    print(f"llm model:       {plan_result.model}")
    print(
        f"llm cost:        ${plan_result.usage.cost_usd:.4f} "
        f"({plan_result.usage.total_tokens} tokens)"
    )
    print(f"wall clock:      {elapsed_s:.1f}s")
    return 0


if __name__ == "__main__":
    sys.exit(main())
