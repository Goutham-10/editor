"""Source-time → output-time mapping.

Load-bearing: this is what keeps captions in sync once Phase 2 builds them
from `transcript.json` word timestamps. A caption's word lives at a source
timestamp; this function is the only correct way to find where that word
lands in the assembled output, because segments in a cutlist can reorder
and drop material from the source.
"""

from __future__ import annotations

from core.cutlist import Cutlist


def source_to_output(cutlist: Cutlist, source_time_s: float) -> float | None:
    """Map a source-time timestamp to its position in the assembled output.

    Segments are walked in `cutlist.segments` order (i.e. assembly/output
    order, not source order — a cutlist may reorder or reuse only part of
    the source). Returns `None` if `source_time_s` falls inside a cut: a
    stretch of source time no segment kept.

    Boundaries are inclusive on both ends of a segment. If a source
    timestamp sits exactly on the shared edge of two different segments
    (segment A's `out_s` equal to segment B's `in_s`), it resolves to
    whichever segment comes first in `cutlist.segments` order.
    """
    output_offset = 0.0
    for segment in cutlist.segments:
        duration = segment.out_s - segment.in_s
        if segment.in_s <= source_time_s <= segment.out_s:
            return output_offset + (source_time_s - segment.in_s)
        output_offset += duration
    return None
