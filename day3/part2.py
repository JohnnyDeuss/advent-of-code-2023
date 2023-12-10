"""
Similarly, we create masks for all components and symbols. This time we
convolve the component masks and count the amount of time each square is
classed as a neighbor of a component. We then create a mask that marks
all squares that neighbor two components. Where this neighbor mask
overlaps with the gear mask, we have found a symbol that is adjacent
to two gears. We then extract the component IDs in the square around
this gear and look up the schematic numbers for them. Finally, we sum
up all the numbers we found.
"""
import string
from collections import defaultdict
from pathlib import Path

import numpy as np
from scipy.signal import convolve2d


def print_grid(grid):
    for line in grid.astype(int).astype(str):
        print("".join(line))


text = Path("input.txt").read_text()
lines = text.splitlines()
grid = np.array([list(line) for line in lines])
component_grid = np.zeros(grid.shape)
current_component = 0
component_strings = defaultdict(str)
for y, line in enumerate(grid):
    is_continuation = False
    for x, character in enumerate(line):
        if character in string.digits:
            if is_continuation:
                component_grid[y, x] = current_component
            else:
                current_component += 1
                component_grid[y, x] = current_component
                is_continuation = True
            component_strings[current_component] += character
        else:
            is_continuation = False

potential_gear_grid = grid == "*"
mask = np.ones((3, 3))
component_masks = [
    convolve2d(component_grid == component, mask, mode="same") >= 1
    for component in component_strings.keys()
]
summed_masks = sum(component_masks)
gear_grid = potential_gear_grid & (summed_masks == 2)
component_mask = component_grid > 0
total = 0
for y, x in zip(*np.nonzero(gear_grid)):
    component_a, component_b = set(
        component_grid[y - 1 : y + 2, x - 1 : x + 2].flatten()
    ) - {0}
    total += int(component_strings[component_a]) * int(component_strings[component_b])
print(total)
