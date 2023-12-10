"""
Again, parse both sides as sets and find the overlap. This time, we're
keeping a ticket count for the 10 subsequent card numbers, aggregating
as we go along. We can sum the tickets as we go.
"""
from pathlib import Path

import numpy as np

text = Path("input.txt").read_text()
lines = text.splitlines()
lines = [line.split(": ")[1] for line in lines if line]
total = 0
mult_arr = np.ones((11,), dtype=int)
for line in lines:
    left, right = line.split(" | ")
    left_set = set([int(x) for x in left.split()])
    right_set = set([int(x) for x in right.split()])
    overlap = left_set & right_set
    mult = mult_arr[0]
    total += mult
    mult_arr = np.append(mult_arr[1:], 1)
    mult_arr[: len(overlap)] += mult

print(total)
