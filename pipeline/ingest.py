"""Ingest stage: validate the source file, checksum it, scaffold the job dir,
and — for oversized sources — produce a 1080p mezzanine used for everything
downstream while the original stays untouched (spec §6 "Huge file" row).
"""

from __future__ import annotations

import hashlib
import logging
import shutil
import uuid
from dataclasses import dataclass
from pathlib import Path

from app.config import get_settings
from pipeline.ffmpeg_utils import ffprobe_json, parse_fps, run_ffmpeg

logger = logging.getLogger(__name__)

# spec §6 "Huge file" row: >4GB or 4K/60 triggers a 1080p mezzanine transcode.
OVERSIZED_BYTES = 4 * 1024**3
OVERSIZED_MIN_HEIGHT = 2160
OVERSIZED_MIN_FPS = 60.0

_CHECKSUM_CHUNK = 1024 * 1024


class IngestError(RuntimeError):
    pass


@dataclass
class IngestResult:
    job_id: str
    job_dir: Path
    source_path: Path
    working_video_path: Path
    duration_s: float
    width: int
    height: int
    fps: float
    checksum_sha256: str
    transcoded: bool


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(_CHECKSUM_CHUNK), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _job_subdirs(job_dir: Path) -> None:
    for sub in ("raw", "analysis", "analysis/frames", "renders"):
        (job_dir / sub).mkdir(parents=True, exist_ok=True)


def ingest(source_path: Path, *, storage_root: Path | None = None) -> IngestResult:
    source_path = Path(source_path).resolve()
    if not source_path.is_file():
        raise IngestError(f"source file does not exist: {source_path}")

    probe = ffprobe_json(source_path)
    streams = probe.get("streams", [])
    video_stream = next((s for s in streams if s.get("codec_type") == "video"), None)
    if video_stream is None:
        raise IngestError(f"no video stream found in {source_path}")

    duration_raw = probe.get("format", {}).get("duration") or video_stream.get("duration")
    if duration_raw is None:
        raise IngestError(f"could not determine duration of {source_path}")
    duration_s = float(duration_raw)
    if duration_s <= 0:
        raise IngestError(f"source {source_path} has zero or negative duration")

    width = int(video_stream.get("width", 0))
    height = int(video_stream.get("height", 0))
    fps = parse_fps(video_stream.get("r_frame_rate", "0/1"))

    settings = get_settings()
    root = storage_root or settings.storage_root
    job_id = uuid.uuid4().hex
    job_dir = root / "jobs" / job_id
    _job_subdirs(job_dir)

    checksum = _sha256(source_path)

    raw_source_path = job_dir / "raw" / f"source{source_path.suffix or '.mp4'}"
    shutil.copyfile(source_path, raw_source_path)

    file_size = source_path.stat().st_size
    oversized = file_size > OVERSIZED_BYTES or (
        height >= OVERSIZED_MIN_HEIGHT and fps >= OVERSIZED_MIN_FPS
    )

    if oversized:
        mezzanine_path = job_dir / "raw" / "mezzanine.mp4"
        run_ffmpeg(
            [
                "-i",
                str(raw_source_path),
                "-vf",
                "scale=-2:1080",
                "-c:v",
                "libx264",
                "-preset",
                "medium",
                "-crf",
                "20",
                "-c:a",
                "aac",
                "-b:a",
                "192k",
                str(mezzanine_path),
            ],
            job_dir=job_dir,
        )
        working_video_path = mezzanine_path
        logger.info(
            "job %s: source is oversized, transcoded mezzanine at %s", job_id, mezzanine_path
        )
    else:
        working_video_path = raw_source_path

    logger.info(
        "job %s ingested: %s (%dx%d @ %.2ffps, %.1fs, %d bytes)",
        job_id,
        source_path.name,
        width,
        height,
        fps,
        duration_s,
        file_size,
    )

    return IngestResult(
        job_id=job_id,
        job_dir=job_dir,
        source_path=raw_source_path,
        working_video_path=working_video_path,
        duration_s=duration_s,
        width=width,
        height=height,
        fps=fps,
        checksum_sha256=checksum,
        transcoded=oversized,
    )
