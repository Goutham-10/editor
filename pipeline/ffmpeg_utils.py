"""Shared ffprobe/ffmpeg helpers used by every pipeline stage that shells out.

Every FFmpeg invocation is appended to `<job_dir>/ffmpeg.log` (full command
line + exit code) so any render is reproducible from the job dir alone.
"""

from __future__ import annotations

import json
import logging
import subprocess
from datetime import UTC, datetime
from fractions import Fraction
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


class FFmpegError(RuntimeError):
    pass


def parse_fps(rate: str) -> float:
    """Parse an ffprobe `r_frame_rate` string like "30000/1001" into a float."""
    try:
        return float(Fraction(rate))
    except (ZeroDivisionError, ValueError):
        return 0.0


def ffprobe_json(path: Path) -> dict[str, Any]:
    cmd = [
        "ffprobe",
        "-v",
        "error",
        "-print_format",
        "json",
        "-show_format",
        "-show_streams",
        str(path),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise FFmpegError(f"ffprobe failed on {path}: {result.stderr.strip()}")
    data: dict[str, Any] = json.loads(result.stdout)
    return data


def run_ffmpeg(args: list[str], *, job_dir: Path) -> None:
    """Run an `ffmpeg ...` command, logging the full command line to the job dir."""
    cmd = ["ffmpeg", "-y", *args]
    log_path = job_dir / "ffmpeg.log"
    timestamp = datetime.now(UTC).isoformat()
    with log_path.open("a") as log_file:
        log_file.write(f"\n# {timestamp}\n{' '.join(cmd)}\n")

    result = subprocess.run(cmd, capture_output=True, text=True)

    with log_path.open("a") as log_file:
        log_file.write(f"exit code: {result.returncode}\n")
        if result.returncode != 0:
            log_file.write(f"stderr:\n{result.stderr}\n")

    if result.returncode != 0:
        raise FFmpegError(
            f"ffmpeg command failed (exit {result.returncode}): {' '.join(cmd)}\n{result.stderr}"
        )

    logger.info("ffmpeg ok: %s", " ".join(cmd))
