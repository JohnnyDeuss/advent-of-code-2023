"""
Parse the ranges as ranges. Fill in any gaps in the ranges with new
ranges. Then, repeatedly apply the maps to the current number, until we
reach the end. Keep track of the lowest number we encounter. Ranges are
sorted so we can use binary search to find the map that applies to the
current number.
"""
import bisect
from itertools import pairwise
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
range_maps = [parse_map(map) for map in maps]
range_maps = [enrich_ranges(map) for map in range_maps]

lowest_location = INFINITY

for seed in seeds:
    current = seed
    for map in range_maps:
        idx = bisect.bisect_right(map, current, key=lambda ranges: ranges[0].start) - 1
        range_pair = map[idx]
        assert current in range_pair[0], f"{current} not in {range_pair[0]}"
        current = current - map[idx][0].start + map[idx][1].start
    if current < lowest_location:
        lowest_location = current
print(lowest_location)
