"""
Just like before, parse the ranges as ranges and fill in the gaps. This
time, whenever the current range overlaps with multiple range maps, we
split our current range and recursively try each sub-range.
"""
import bisect
from itertools import batched, pairwise
from pathlib import Path

INFINITY = 2**62


def parse_map(map: str) -> list[tuple[range, range]]:
    map = map.split(":\n")[1]
    lines = [[int(x) for x in line.split()] for line in map.splitlines()]
    return [
        (range(src, src + width), range(dst, dst + width)) for dst, src, width in lines
    ]


def enrich_ranges(ranges: list[tuple[range, range]]) -> list[tuple[range, range]]:
    ranges = sorted(ranges, key=lambda x: x[0].start)
    new_ranges = [
        (range(ranges[-1][0].stop, INFINITY), range(ranges[-1][0].stop, INFINITY))
    ]
    if ranges[0][0].start > 0:
        new_ranges.append((range(0, ranges[0][0].start), range(0, ranges[0][0].start)))
    for range_a, range_b in pairwise([src_range for src_range, _ in ranges]):
        assert range_a.stop <= range_b.start
        if range_a.stop < range_b.start:
            new_ranges.append(
                (range(range_a.stop, range_b.start), range(range_a.stop, range_b.start))
            )

    return sorted(ranges + new_ranges, key=lambda x: x[0].start)


text = Path("input.txt").read_text()
seeds_str, *maps = text.split("\n\n")
seeds = [int(x) for x in seeds_str.split(": ")[1].split()]
seed_ranges = [range(start, start + width) for start, width in batched(seeds, 2)]
range_maps = [parse_map(map) for map in maps]
range_maps = [enrich_ranges(map) for map in range_maps]

lowest_location = INFINITY


def get_lowest_location(
    current_range: range, range_maps: list[list[tuple[range, range]]]
) -> range:
    map, *rest_range_maps = range_maps
    start_idx = (
        bisect.bisect_right(
            map, current_range.start, key=lambda ranges: ranges[0].start
        )
        - 1
    )
    stop_idx = (
        bisect.bisect_right(
            map,
            current_range.stop,
            key=lambda ranges: ranges[0].start,
            lo=start_idx + 1,
        )
        - 1
    )
    locations: list[range] = []
    for ranges in map[start_idx : stop_idx + 1]:
        current_sub_range = range(
            max(current_range.start, ranges[0].start),
            min(current_range.stop, ranges[0].stop),
        )
        mapped_range = range(
            current_sub_range.start - ranges[0].start + ranges[1].start,
            current_sub_range.stop - ranges[0].start + ranges[1].start,
        )
        if rest_range_maps:
            locations.append(get_lowest_location(mapped_range, rest_range_maps))
        else:
            locations.append(mapped_range)
    return min(locations, key=lambda x: x.start)


lowest_location = min(
    [get_lowest_location(seed_range, range_maps) for seed_range in seed_ranges],
    key=lambda x: x.start,
)
print(lowest_location.start)
