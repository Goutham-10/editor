"""faster-whisper transcription → analysis/transcript.json with word timestamps."""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

from faster_whisper import WhisperModel

from app.config import get_settings

logger = logging.getLogger(__name__)


def transcribe(job_dir: Path, video_path: Path, *, model_size: str | None = None) -> Path:
    """Transcribe `video_path` and write `<job_dir>/analysis/transcript.json`.

    Schema:
        {
          "language": "en",
          "duration_s": 68.8,
          "segments": [
            {
              "id": 0, "start": 0.0, "end": 4.52, "text": "...",
              "words": [{"word": "This", "start": 0.0, "end": 0.18, "confidence": 0.67}, ...]
            }
          ]
        }
    """
    settings = get_settings()
    size = model_size or settings.whisper_model_size
    model = WhisperModel(size, device="cpu", compute_type="int8")

    raw_segments, info = model.transcribe(str(video_path), word_timestamps=True)

    segments: list[dict[str, Any]] = []
    for idx, seg in enumerate(raw_segments):
        words = [
            {
                "word": w.word.strip(),
                "start": round(w.start, 3),
                "end": round(w.end, 3),
                "confidence": round(w.probability, 4),
            }
            for w in (seg.words or [])
        ]
        segments.append(
            {
                "id": idx,
                "start": round(seg.start, 3),
                "end": round(seg.end, 3),
                "text": seg.text.strip(),
                "words": words,
            }
        )

    transcript = {
        "language": info.language,
        "duration_s": round(info.duration, 3),
        "segments": segments,
    }

    out_path = job_dir / "analysis" / "transcript.json"
    out_path.write_text(json.dumps(transcript, indent=2))
    word_count = sum(len(s["words"]) for s in segments)
    logger.info(
        "job %s: transcribed %d segments / %d words (%s)",
        job_dir.name,
        len(segments),
        word_count,
        info.language,
    )
    return out_path
