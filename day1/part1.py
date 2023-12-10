"""
Search for digits from both ends and stitch them together to form two
digit numbers and then sum them up.
"""
import string
from pathlib import Path

text = Path("input.txt").read_text()
lines = text.splitlines()
numbers = [
    int(
        next(c for c in line if c in string.digits)
        + next(c for c in reversed(line) if c in string.digits)
    )
    for line in lines
]
solution = sum(numbers)
print(solution)
