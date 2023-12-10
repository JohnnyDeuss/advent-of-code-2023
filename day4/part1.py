"""
Parse both sides into sets and find the overlap. Sum up the number of
overlapping elements minus one, and raise two to that power to get the
score.
"""
from pathlib import Path

text = Path("input.txt").read_text()
lines = text.splitlines()
lines = [line.split(": ")[1] for line in lines if line]
total = 0
for line in lines:
    left, right = line.split(" | ")
    left_set = set([int(x) for x in left.split()])
    right_set = set([int(x) for x in right.split()])
    overlap = left_set & right_set
    if overlap:
        exp = len(overlap) - 1
        total += 2**exp
print(total)
