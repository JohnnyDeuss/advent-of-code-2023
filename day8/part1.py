from itertools import cycle
from pathlib import Path

text = Path("input.txt").read_text()
instructions, paths_str = text.split("\n\n")
paths = {line[:3]: (line[7:10], line[12:15]) for line in paths_str.splitlines()}

current = "AAA"
for step, direction in enumerate(cycle(list(instructions)), start=1):
    path_idx = 0 if direction == "L" else 1
    current = paths[current][path_idx]
    print(current, step, direction)
    if current == "ZZZ":
        break
print(step)
