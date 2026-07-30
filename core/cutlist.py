"""Cutlist schema (product spec §5.4) and the hard-gate validator.

Pure logic only: no filesystem writes, no network, no FastAPI/SQLAlchemy
imports. The one permitted bit of I/O is `Path.exists()` for the
asset-reference rule, per spec.
"""

from __future__ import annotations

import re
from collections.abc import Sequence
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

Role = Literal["hook", "body", "cta", "other"]

# Rule constants — see spec §5.4 "Validator rules (hard gate)".
MIN_SEGMENT_DURATION_S = 0.7  # "no two cuts closer than 0.7s apart"
WORD_BOUNDARY_TOLERANCE_S = 0.08
DURATION_TOLERANCE_PCT = 0.15

# Overlay/audio fields that may hold a filesystem path, checked for existence.
_ASSET_FIELDS = ("source", "asset", "track", "file")
_ASSET_LIKE = re.compile(r"\.(json|png|jpg|jpeg|ttf|otf|mp3|mp4|wav)$", re.IGNORECASE)


class Crop(BaseModel):
    mode: Literal["center"] = "center"
    x_offset_pct: float = 0.0


class Output(BaseModel):
    aspect: str = "9:16"
    resolution: tuple[int, int] = (1080, 1920)
    target_duration_s: float
    crop: Crop = Field(default_factory=Crop)


class Segment(BaseModel):
    id: str
    in_s: float
    out_s: float
    role: Role
    note: str | None = None
    speed: float = 1.0
    transition_out: Literal["cut", "fade"] | None = None


class Overlay(BaseModel):
    """Deliberately loose: Phase 1 only ever emits a `captions` overlay, but
    the schema (spec §5.4) allows `watermark`/`endcard` too, which belong to
    Phase 2/3. `extra="allow"` lets those pass through once other stages
    start emitting them, without this file needing to change."""

    model_config = ConfigDict(extra="allow")
    type: str


class AudioItem(BaseModel):
    model_config = ConfigDict(extra="allow")
    type: str


class Variant(BaseModel):
    id: str
    replace_segment: str
    in_s: float
    out_s: float


class Cutlist(BaseModel):
    version: int = 1
    job_id: str
    brand: str
    output: Output
    segments: list[Segment]
    overlays: list[Overlay] = Field(default_factory=list)
    audio: list[AudioItem] = Field(default_factory=list)
    variants: list[Variant] = Field(default_factory=list)
    qc_notes: str | None = None


class CutlistValidationError(Exception):
    """Raised by callers that treat validation as a hard gate."""

    def __init__(self, errors: list[str]) -> None:
        self.errors = errors
        super().__init__("; ".join(errors))


@dataclass
class ValidationResult:
    ok: bool
    errors: list[str] = field(default_factory=list)


def _looks_like_asset_path(value: str) -> bool:
    return bool(_ASSET_LIKE.search(value))


def _asset_exists(value: str, asset_roots: Sequence[Path]) -> bool:
    candidate = Path(value)
    if candidate.is_absolute():
        return candidate.exists()
    return any((root / candidate).exists() for root in asset_roots)


def validate_cutlist(
    cutlist: Cutlist,
    *,
    source_duration_s: float,
    word_boundaries: Sequence[float] = (),
    asset_roots: Sequence[Path] = (),
) -> ValidationResult:
    """Enforce every rule in spec §5.4. Pure aside from `Path.exists()`."""
    errors: list[str] = []

    if not cutlist.segments:
        errors.append("cutlist has no segments")
        return ValidationResult(ok=False, errors=errors)

    for seg in cutlist.segments:
        if not seg.in_s < seg.out_s:
            errors.append(f"segment {seg.id}: in_s ({seg.in_s}) must be < out_s ({seg.out_s})")
            continue
        if not (0.0 <= seg.in_s <= source_duration_s):
            errors.append(
                f"segment {seg.id}: in_s {seg.in_s} is outside source bounds "
                f"[0, {source_duration_s}]"
            )
        if not (0.0 <= seg.out_s <= source_duration_s):
            errors.append(
                f"segment {seg.id}: out_s {seg.out_s} is outside source bounds "
                f"[0, {source_duration_s}]"
            )
        duration = seg.out_s - seg.in_s
        if duration < MIN_SEGMENT_DURATION_S:
            errors.append(
                f"segment {seg.id}: duration {duration:.3f}s is under the "
                f"{MIN_SEGMENT_DURATION_S}s minimum — two cuts would land closer "
                "than 0.7s apart in the output"
            )

    # Non-overlapping in source time, regardless of assembly (list) order.
    by_start = sorted(cutlist.segments, key=lambda s: s.in_s)
    for a, b in zip(by_start, by_start[1:], strict=False):
        if b.in_s < a.out_s:
            errors.append(f"segments {a.id!r} and {b.id!r} overlap in source time")

    if word_boundaries:
        lo, hi = min(word_boundaries), max(word_boundaries)
        for seg in cutlist.segments:
            for label, t in (("in_s", seg.in_s), ("out_s", seg.out_s)):
                if t <= lo + WORD_BOUNDARY_TOLERANCE_S or t >= hi - WORD_BOUNDARY_TOLERANCE_S:
                    continue  # near the source's extremities, not a mid-speech cut
                nearest = min(word_boundaries, key=lambda b: abs(b - t))
                drift = abs(nearest - t)
                if drift > WORD_BOUNDARY_TOLERANCE_S:
                    errors.append(
                        f"segment {seg.id}.{label}={t:.3f}s is {drift * 1000:.0f}ms from "
                        f"the nearest word boundary (limit {WORD_BOUNDARY_TOLERANCE_S * 1000:.0f}ms)"
                    )

    total = sum(s.out_s - s.in_s for s in cutlist.segments)
    target = cutlist.output.target_duration_s
    if target > 0:
        low, high = target * (1 - DURATION_TOLERANCE_PCT), target * (1 + DURATION_TOLERANCE_PCT)
        if not (low <= total <= high):
            errors.append(
                f"total duration {total:.1f}s is outside ±{DURATION_TOLERANCE_PCT:.0%} of "
                f"target {target:.1f}s (allowed [{low:.1f}, {high:.1f}])"
            )

    if asset_roots:
        for kind, items in (("overlay", cutlist.overlays), ("audio", cutlist.audio)):
            for item in items:
                data: dict[str, Any] = item.model_dump()
                for asset_field in _ASSET_FIELDS:
                    value = data.get(asset_field)
                    if (
                        isinstance(value, str)
                        and _looks_like_asset_path(value)
                        and not _asset_exists(value, asset_roots)
                    ):
                        errors.append(
                            f"{kind} {data.get('type')!r} references a missing asset: {value}"
                        )

    return ValidationResult(ok=not errors, errors=errors)
