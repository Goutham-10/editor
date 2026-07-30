from core.cutlist import Cutlist, Output, Segment
from core.timemap import source_to_output


def _cutlist(segments: list[Segment]) -> Cutlist:
    return Cutlist(
        job_id="test-job",
        brand="test-brand",
        output=Output(target_duration_s=60.0),
        segments=segments,
    )


# Three segments, output order == list order, deliberately not contiguous or
# ordered in source time: a=[10,20) -> output [0,10), b=[25,30) -> output
# [10,15), c=[40,42) -> output [15,17). Gaps 20-25 and 30-40 are cuts.
SEGMENTS = [
    Segment(id="a", in_s=10.0, out_s=20.0, role="body"),
    Segment(id="b", in_s=25.0, out_s=30.0, role="body"),
    Segment(id="c", in_s=40.0, out_s=42.0, role="cta"),
]


def test_inside_first_segment() -> None:
    cutlist = _cutlist(SEGMENTS)
    assert source_to_output(cutlist, 15.0) == 5.0


def test_inside_middle_segment() -> None:
    cutlist = _cutlist(SEGMENTS)
    assert source_to_output(cutlist, 27.0) == 12.0


def test_inside_last_segment_across_gaps() -> None:
    cutlist = _cutlist(SEGMENTS)
    # a contributes 10s, b contributes 5s of output before c starts at 15s.
    assert source_to_output(cutlist, 41.0) == 16.0


def test_inside_a_cut_returns_none() -> None:
    cutlist = _cutlist(SEGMENTS)
    assert source_to_output(cutlist, 22.0) is None  # gap between a and b
    assert source_to_output(cutlist, 35.0) is None  # gap between b and c


def test_before_first_segment_returns_none() -> None:
    cutlist = _cutlist(SEGMENTS)
    assert source_to_output(cutlist, 5.0) is None


def test_after_last_segment_returns_none() -> None:
    cutlist = _cutlist(SEGMENTS)
    assert source_to_output(cutlist, 50.0) is None


def test_exact_segment_start_boundary() -> None:
    cutlist = _cutlist(SEGMENTS)
    assert source_to_output(cutlist, 10.0) == 0.0  # start of a
    assert source_to_output(cutlist, 40.0) == 15.0  # start of c


def test_exact_segment_end_boundary() -> None:
    cutlist = _cutlist(SEGMENTS)
    assert source_to_output(cutlist, 20.0) == 10.0  # end of a
    assert source_to_output(cutlist, 42.0) == 17.0  # end of c


def test_adjacent_boundary_resolves_to_earlier_segment_in_list_order() -> None:
    # a's out_s (20.0) and b's in_s (25.0) are different source timestamps
    # but map to the same output instant, since a and b are back-to-back
    # in the assembled output.
    cutlist = _cutlist(SEGMENTS)
    assert source_to_output(cutlist, 20.0) == source_to_output(cutlist, 25.0) == 10.0


def test_single_segment() -> None:
    cutlist = _cutlist([Segment(id="only", in_s=3.0, out_s=9.0, role="body")])
    assert source_to_output(cutlist, 3.0) == 0.0
    assert source_to_output(cutlist, 6.0) == 3.0
    assert source_to_output(cutlist, 9.0) == 6.0
    assert source_to_output(cutlist, 2.9) is None
    assert source_to_output(cutlist, 9.1) is None
