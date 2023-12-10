"""
Mark all digits on the schematic with a component ID, building a map
of component IDs to their numbers. Every array element that has a digit
belonging to the same component is assigned the same ID. Then, we
convolve the array with a 3x3 mask of ones with the mask that marks all
symbols. This will create a mask that covers all symbols and their
direct neighbors. We also create a mask that marks all digits on the
schematic. Where this neighbor mask and the component mask overlap, we
have found a digit that is adjacent to a symbol. We then extract the
component ID using this overlap and look up the schematic number for it.
Finally, we sum up all the numbers we found.
"""

import string
from collections import defaultdict
from pathlib import Path

import numpy as np
from scipy.signal import convolve2d

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

symbol_grid = ~np.isin(grid, list(string.digits + "."))

mask = np.ones((3, 3))
overlap_mask = convolve2d(symbol_grid, mask, mode="same") >= 1
component_mask = component_grid > 0
matches = set([int(x) for x in component_grid[overlap_mask & component_mask]])
print(sum([int(component_strings[match]) for match in matches]))
