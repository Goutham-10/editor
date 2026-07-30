"""Scene detection, silence/energy mapping, and frame sampling for the LLM watch-pass.

Writes `analysis/scenes.json`, `analysis/silence.json`, and
`analysis/frames/frame_%04d.jpg` into the job dir.
"""

from __future__ import annotations

import json
import logging
import subprocess
from dataclasses import dataclass
from pathlib import Path

from scenedetect import SceneManager, open_video
from scenedetect.detectors import ContentDetector

from pipeline.ffmpeg_utils import ffprobe_json, parse_fps, run_ffmpeg

logger = logging.getLogger(__name__)

# Silence classification over auto-editor's per-frame audio-energy levels.
SILENCE_THRESHOLD = 0.02
MERGE_GAP_S = 0.2  # matches auto-editor's own default --margin
MIN_SILENCE_S = 0.15  # drop sub-frame noise blips


class AnalyzeError(RuntimeError):
    pass


@dataclass
class AnalyzeResult:
    scenes_path: Path
    silence_path: Path
    frame_paths: list[Path]


def _detect_scenes(video_path: Path, duration_s: float) -> list[dict[str, float]]:
    # pyav backend avoids routing scene detection's frame decode through
    # opencv's video path (see CLAUDE task notes re: a benign objc dylib
    # warning between PyAV and opencv-python on macOS).
    video = open_video(str(video_path), backend="pyav")
    manager = SceneManager()
    manager.add_detector(ContentDetector())
    manager.detect_scenes(video)
    scene_list = manager.get_scene_list()
    if not scene_list:
        # No detected boundary just means one continuous shot end to end.
        return [{"start_s": 0.0, "end_s": round(duration_s, 3)}]
    return [
        {"start_s": round(start.get_seconds(), 3), "end_s": round(end.get_seconds(), 3)}
        for start, end in scene_list
    ]


def _run_auto_editor_levels(video_path: Path, fps: float) -> list[float]:
    cmd = ["auto-editor", "levels", "--edit", "audio", "-tb", str(fps), str(video_path)]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise AnalyzeError(f"auto-editor levels failed on {video_path}: {result.stderr.strip()}")
    levels: list[float] = []
    for line in result.stdout.splitlines():
        line = line.strip()
        if not line or line.startswith("@"):
            continue
        levels.append(float(line))
    return levels


def _levels_to_silences(levels: list[float], fps: float) -> list[dict[str, float]]:
    if not levels or fps <= 0:
        return []

    raw_intervals: list[tuple[int, int]] = []
    start_idx: int | None = None
    for i, level in enumerate(levels):
        silent = level < SILENCE_THRESHOLD
        if silent and start_idx is None:
            start_idx = i
        elif not silent and start_idx is not None:
            raw_intervals.append((start_idx, i))
            start_idx = None
    if start_idx is not None:
        raw_intervals.append((start_idx, len(levels)))

    seconds = [(s / fps, e / fps) for s, e in raw_intervals]

    merged: list[list[float]] = []
    for start_s, end_s in seconds:
        if merged and start_s - merged[-1][1] <= MERGE_GAP_S:
            merged[-1][1] = end_s
        else:
            merged.append([start_s, end_s])

    return [
        {"start_s": round(s, 3), "end_s": round(e, 3)}
        for s, e in merged
        if e - s >= MIN_SILENCE_S
    ]


def _sample_frames(video_path: Path, job_dir: Path) -> list[Path]:
    frames_dir = job_dir / "analysis" / "frames"
    frames_dir.mkdir(parents=True, exist_ok=True)
    for stale in frames_dir.glob("frame_*.jpg"):
        stale.unlink()
    pattern = frames_dir / "frame_%04d.jpg"
    run_ffmpeg(["-i", str(video_path), "-vf", "fps=1", "-q:v", "2", str(pattern)], job_dir=job_dir)
    return sorted(frames_dir.glob("frame_*.jpg"))


def analyze(job_dir: Path, video_path: Path) -> AnalyzeResult:
    probe = ffprobe_json(video_path)
    video_stream = next((s for s in probe["streams"] if s.get("codec_type") == "video"), None)
    if video_stream is None:
        raise AnalyzeError(f"no video stream found in {video_path}")

    fps = parse_fps(video_stream.get("r_frame_rate", "0/1")) or 30.0
    duration_s = float(probe["format"]["duration"])

    scenes = _detect_scenes(video_path, duration_s)
    scenes_path = job_dir / "analysis" / "scenes.json"
    scenes_path.write_text(json.dumps({"scenes": scenes}, indent=2))

    levels = _run_auto_editor_levels(video_path, fps)
    silences = _levels_to_silences(levels, fps)
    mean_energy = sum(levels) / len(levels) if levels else 0.0
    silence_path = job_dir / "analysis" / "silence.json"
    silence_path.write_text(
        json.dumps(
            {
                "fps": fps,
                "threshold": SILENCE_THRESHOLD,
                "margin_s": MERGE_GAP_S,
                "mean_energy": round(mean_energy, 4),
                "silences": silences,
            },
            indent=2,
        )
    )

    frame_paths = _sample_frames(video_path, job_dir)

    logger.info(
        "job %s: %d scene(s), %d silence region(s), %d sampled frame(s)",
        job_dir.name,
        len(scenes),
        len(silences),
        len(frame_paths),
    )

    return AnalyzeResult(
        scenes_path=scenes_path, silence_path=silence_path, frame_paths=frame_paths
    )
