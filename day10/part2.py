"""
Mark the inside squares next to the loop as we go. These will be the
seeds to fill the inside area from. Once we have the loop, make sure
none of the seeds are on the loop. Then, dilate the inside until we
can't dilate anymore. We  won't know which side is inside, so we'll have 
to check whether the final area goes all the way to the edge of the
grid. If it does, then we know that the inside is the opposite side of
the loop.
"""
from itertools import count
from pathlib import Path

import numpy as np
from scipy.ndimage import binary_dilation, binary_fill_holes


class InvalidCameFromError(Exception):
    def __init__(self, came_from):
        self.came_from = came_from
        super().__init__(f"Invalid came_from: {came_from}")


text = Path("input.txt").read_text()
grid = np.array([list(line) for line in text.splitlines()])
x, y = next((x, y) for y, row in enumerate(grid) for x, c in enumerate(row) if c == "S")
loop_mask = np.zeros(grid.shape, dtype=bool)
inside_mask = np.zeros(grid.shape, dtype=bool)
assert grid[y][x] == "S"
y -= 1
came_from = "S"
for steps in count(start=1):
    loop_mask[y, x] = True
    match grid[y][x]:
        case "F":
            if came_from == "S":
                inside_mask[y - 1, x] = True
                inside_mask[y - 1, x - 1] = True
                inside_mask[y, x - 1] = True
                x += 1
                came_from = "W"
            elif came_from == "E":
                inside_mask[y + 1, x + 1] = True
                y += 1
                came_from = "N"
            else:
                raise ValueError(f"Invalid came_from: {came_from}")
        case "L":
            if came_from == "N":
                inside_mask[y - 1, x + 1] = True
                x += 1
                came_from = "W"
            elif came_from == "E":
                inside_mask[y, x - 1] = True
                inside_mask[y + 1, x - 1] = True
                inside_mask[y + 1, x] = True
                y -= 1
                came_from = "S"
            else:
                raise ValueError(f"Invalid came_from: {came_from}")
        case "J":
            if came_from == "N":
                inside_mask[y, x + 1] = True
                inside_mask[y + 1, x] = True
                inside_mask[y + 1, x + 1] = True
                x -= 1
                came_from = "E"
            elif came_from == "W":
                inside_mask[y - 1, x - 1] = True
                y -= 1
                came_from = "S"
            else:
                raise ValueError(f"Invalid came_from: {came_from}")
        case "7":
            if came_from == "W":
                inside_mask[y - 1, x + 1] = True
                inside_mask[y - 1, x + 1] = True
                inside_mask[y, x + 1] = True
                y += 1
                came_from = "N"
            elif came_from == "S":
                inside_mask[y + 1, x - 1] = True
                x -= 1
                came_from = "E"
            else:
                raise ValueError(f"Invalid came_from: {came_from}")
        case "|":
            if came_from == "N":
                inside_mask[y, x + 1] = True
                y += 1
                came_from = "N"
            elif came_from == "S":
                inside_mask[y, x - 1] = True
                y -= 1
                came_from = "S"
            else:
                raise ValueError(f"Invalid came_from: {came_from}")
        case "-":
            if came_from == "W":
                inside_mask[y - 1, x] = True
                x += 1
                came_from = "W"
            elif came_from == "E":
                inside_mask[y + 1, x] = True
                x -= 1
                came_from = "E"
            else:
                raise ValueError(f"Invalid came_from: {came_from}")
        case "S":
            break
        case _:
            raise ValueError(f"Invalid pipe character: {grid[y][x]}")


def print_grid(grid):
    for row in grid:
        print("".join(["x" if b else " " for b in row]))


print_grid(loop_mask)
print()
print()


print_grid(binary_fill_holes(loop_mask) ^ loop_mask)

inside_mask = inside_mask & ~loop_mask
old_inside_count = 0
while True:
    inside_mask = binary_dilation(inside_mask) & ~loop_mask
    inside_count = np.count_nonzero(inside_mask)
    if old_inside_count == inside_count:
        break
    old_inside_count = inside_count

print_grid(inside_mask)
print(inside_count)
