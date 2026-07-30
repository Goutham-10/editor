"""Edit-planning stage: transcript + scenes + silence + sampled frames + a bare
brand context → one LLM call → `cutlist.v1.json`, validated as a hard gate.

Brand handling here is deliberately minimal — just a name and free-text notes.
The real brand YAML loader (`app/service/brand_service.py`) is Phase 2's job;
nothing downstream of Phase 1 consumes brand styling yet.
"""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from app.config import PROJECT_ROOT
from core.cutlist import Cutlist, validate_cutlist
from llm.openrouter import LLMUsage, OpenRouterClient, extract_json, image_content_block

logger = logging.getLogger(__name__)

_PROMPT_PATH = Path(__file__).resolve().parent.parent / "llm" / "prompts" / "edit_plan.md"

MAX_FRAMES_FOR_PLANNING = 12
REPAIR_ATTEMPTS = 2  # total LLM calls = 1 + REPAIR_ATTEMPTS, bounded on purpose
SNAP_TOLERANCE_S = 0.3  # nudge near-miss cut points onto the real word boundary


class PlanningError(RuntimeError):
    pass


@dataclass
class PlanResult:
    cutlist: Cutlist
    cutlist_path: Path
    usage: LLMUsage
    model: str
    hook_note: str | None


def _select_frames(frame_paths: list[Path], max_frames: int) -> list[Path]:
    if len(frame_paths) <= max_frames:
        return frame_paths
    step = len(frame_paths) / max_frames
    return [frame_paths[int(i * step)] for i in range(max_frames)]


def _word_boundaries(transcript: dict[str, Any]) -> list[float]:
    boundaries: list[float] = []
    for segment in transcript.get("segments", []):
        for word in segment.get("words", []):
            boundaries.append(word["start"])
            boundaries.append(word["end"])
    return boundaries


def _snap_to_word_boundaries(
    cutlist_data: dict[str, Any], boundaries: list[float]
) -> dict[str, Any]:
    """Nudge near-miss cut points onto the real word boundary they were meant
    to hit. This corrects small drift from the model, it doesn't invent data:
    a value outside the tolerance is left untouched and surfaces as a real
    validation failure."""
    if not boundaries:
        return cutlist_data
    for segment in cutlist_data.get("segments", []):
        for key in ("in_s", "out_s"):
            value = segment.get(key)
            if not isinstance(value, int | float):
                continue
            nearest = min(boundaries, key=lambda b: abs(b - value))
            if abs(nearest - value) <= SNAP_TOLERANCE_S:
                segment[key] = nearest
    return cutlist_data


def _build_prompt(context_block: str, transcript: dict, scenes: dict, silence: dict) -> str:
    template = _PROMPT_PATH.read_text()
    return (
        template.replace("{{CONTEXT_BLOCK}}", context_block)
        .replace("{{TRANSCRIPT_JSON}}", json.dumps(transcript))
        .replace("{{SCENES_JSON}}", json.dumps(scenes))
        .replace("{{SILENCE_JSON}}", json.dumps(silence))
    )


def _accumulate(total: LLMUsage, usage: LLMUsage) -> LLMUsage:
    return LLMUsage(
        prompt_tokens=total.prompt_tokens + usage.prompt_tokens,
        completion_tokens=total.completion_tokens + usage.completion_tokens,
        total_tokens=total.total_tokens + usage.total_tokens,
        cost_usd=total.cost_usd + usage.cost_usd,
    )


def plan(
    job_dir: Path,
    *,
    target_duration_s: float,
    brand_name: str,
    brand_notes: str = "",
    job_id: str | None = None,
    source_duration_s: float | None = None,
    max_frames: int = MAX_FRAMES_FOR_PLANNING,
) -> PlanResult:
    job_id = job_id or job_dir.name
    analysis_dir = job_dir / "analysis"

    transcript = json.loads((analysis_dir / "transcript.json").read_text())
    scenes = json.loads((analysis_dir / "scenes.json").read_text())
    silence = json.loads((analysis_dir / "silence.json").read_text())

    frame_paths = sorted((analysis_dir / "frames").glob("frame_*.jpg"))
    selected_frames = _select_frames(frame_paths, max_frames)

    source_duration = (
        source_duration_s if source_duration_s is not None else float(transcript["duration_s"])
    )

    context_block = (
        f"job_id: {job_id}\n"
        f"brand: {brand_name}\n"
        f"brand_notes: {brand_notes or '(none)'}\n"
        f"target_duration_s: {target_duration_s}\n"
        f"source_duration_s: {source_duration}\n"
    )

    prompt_text = _build_prompt(context_block, transcript, scenes, silence)

    content: list[dict[str, Any]] = [{"type": "text", "text": prompt_text}]
    content.extend(image_content_block(frame_path) for frame_path in selected_frames)

    messages: list[dict[str, Any]] = [{"role": "user", "content": content}]
    word_boundaries = _word_boundaries(transcript)
    asset_roots = [job_dir, analysis_dir, PROJECT_ROOT]

    client = OpenRouterClient()
    total_usage = LLMUsage(0, 0, 0, 0.0)
    last_errors: list[str] = ["no attempt completed"]
    model_used = ""

    for attempt in range(1, REPAIR_ATTEMPTS + 2):
        response = client.chat(messages, temperature=0.4, max_tokens=3000)
        model_used = response.model
        total_usage = _accumulate(total_usage, response.usage)

        raw_json = extract_json(response.content)
        try:
            cutlist_data = json.loads(raw_json)
        except json.JSONDecodeError as exc:
            last_errors = [f"model did not return valid JSON: {exc}"]
            messages.append({"role": "assistant", "content": response.content})
            messages.append(
                {
                    "role": "user",
                    "content": (
                        f"That was not valid JSON ({exc}). Return ONLY the corrected "
                        "JSON object, nothing else."
                    ),
                }
            )
            continue

        # These three are authoritative regardless of what the model echoed back.
        cutlist_data["job_id"] = job_id
        cutlist_data["brand"] = brand_name
        cutlist_data.setdefault("output", {})["target_duration_s"] = target_duration_s

        cutlist_data = _snap_to_word_boundaries(cutlist_data, word_boundaries)

        try:
            cutlist = Cutlist.model_validate(cutlist_data)
        except Exception as exc:
            last_errors = [f"cutlist did not match the expected schema: {exc}"]
            messages.append({"role": "assistant", "content": response.content})
            messages.append(
                {
                    "role": "user",
                    "content": (
                        f"That JSON didn't match the required schema: {exc}. "
                        "Return ONLY the corrected JSON object."
                    ),
                }
            )
            continue

        result = validate_cutlist(
            cutlist,
            source_duration_s=source_duration,
            word_boundaries=word_boundaries,
            asset_roots=asset_roots,
        )
        if result.ok:
            cutlist_path = job_dir / "cutlist.v1.json"
            cutlist_path.write_text(cutlist.model_dump_json(indent=2))
            hook_note = next(
                (s.note for s in cutlist.segments if s.role == "hook" and s.note), None
            )
            logger.info(
                "job %s: planning succeeded on attempt %d/%d (model %s, cost $%.4f)",
                job_id,
                attempt,
                REPAIR_ATTEMPTS + 1,
                model_used,
                total_usage.cost_usd,
            )
            return PlanResult(
                cutlist=cutlist,
                cutlist_path=cutlist_path,
                usage=total_usage,
                model=model_used,
                hook_note=hook_note,
            )

        last_errors = result.errors
        logger.warning(
            "job %s: cutlist failed validation on attempt %d/%d: %s",
            job_id,
            attempt,
            REPAIR_ATTEMPTS + 1,
            result.errors,
        )
        messages.append({"role": "assistant", "content": response.content})
        messages.append(
            {
                "role": "user",
                "content": (
                    "That cutlist failed validation with these errors:\n- "
                    + "\n- ".join(result.errors)
                    + "\nReturn ONLY the corrected JSON object, fixing every error above."
                ),
            }
        )

    raise PlanningError(
        f"cutlist failed validation after {REPAIR_ATTEMPTS + 1} attempt(s): {last_errors}"
    )
