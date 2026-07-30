"""Cutlist → FFmpeg trim/concat/center-crop 9:16 → `renders/base.mp4`.

Silent, caption-less, unbranded — captions, watermark, end-card, and audio
mixing are Phase 2/3. This is the M1 rough cut only.
"""

from __future__ import annotations

import logging
import shutil
import tempfile
from pathlib import Path

from core.cutlist import Cutlist, Segment
from pipeline.ffmpeg_utils import ffprobe_json, run_ffmpeg

logger = logging.getLogger(__name__)

# Tolerance between the cutlist's intended duration and the actual render —
# covers concat/encode rounding, not a sign of a broken assembly.
DURATION_CHECK_TOLERANCE_S = 2.0


class AssembleError(RuntimeError):
    pass


def assemble(job_dir: Path, cutlist: Cutlist, video_path: Path) -> Path:
    renders_dir = job_dir / "renders"
    renders_dir.mkdir(parents=True, exist_ok=True)
    output_path = renders_dir / "base.mp4"

    width, height = cutlist.output.resolution
    # Center crop to 9:16 then scale to the target resolution — no manual
    # x_offset knob yet (US-D2 is Phase 2+); crop.mode is always "center".
    crop_filter = f"crop=ih*9/16:ih:(iw-ih*9/16)/2:0,scale={width}:{height},setsar=1"

    tmp_dir = Path(tempfile.mkdtemp(prefix="assemble_", dir=renders_dir))
    try:
        segment_paths = [
            _render_segment(job_dir, video_path, crop_filter, tmp_dir, index, segment)
            for index, segment in enumerate(cutlist.segments)
        ]
        _concat(job_dir, segment_paths, output_path)
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)

    _verify_output(output_path, cutlist)
    logger.info("job %s: assembled %s", job_dir.name, output_path)
    return output_path


def _render_segment(
    job_dir: Path, video_path: Path, crop_filter: str, tmp_dir: Path, index: int, segment: Segment
) -> Path:
    seg_path = tmp_dir / f"segment_{index:03d}.mp4"
    duration = segment.out_s - segment.in_s
    run_ffmpeg(
        [
            "-ss",
            f"{segment.in_s}",
            "-i",
            str(video_path),
            "-t",
            f"{duration}",
            "-vf",
            crop_filter,
            "-c:v",
            "libx264",
            "-preset",
            "medium",
            "-crf",
            "18",
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            "-avoid_negative_ts",
            "make_zero",
            str(seg_path),
        ],
        job_dir=job_dir,
    )
    return seg_path


def _concat(job_dir: Path, segment_paths: list[Path], output_path: Path) -> None:
    filelist_path = segment_paths[0].parent / "concat.txt"
    filelist_path.write_text("".join(f"file '{p.resolve()}'\n" for p in segment_paths))
    run_ffmpeg(
        [
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(filelist_path),
            "-c:v",
            "libx264",
            "-preset",
            "medium",
            "-crf",
            "18",
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            str(output_path),
        ],
        job_dir=job_dir,
    )


def _verify_output(output_path: Path, cutlist: Cutlist) -> None:
    probe = ffprobe_json(output_path)
    streams = probe.get("streams", [])
    if not any(s.get("codec_type") == "video" for s in streams):
        raise AssembleError(f"{output_path} has no video stream")
    if not any(s.get("codec_type") == "audio" for s in streams):
        raise AssembleError(f"{output_path} has no audio stream")

    duration = float(probe["format"]["duration"])
    expected = sum(s.out_s - s.in_s for s in cutlist.segments)
    if abs(duration - expected) > DURATION_CHECK_TOLERANCE_S:
        raise AssembleError(
            f"{output_path} duration {duration:.1f}s is far from the expected "
            f"{expected:.1f}s from the cutlist"
        )
