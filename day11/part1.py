"""
Convert the input into coordinates, apply expansion rules and calculate
the manhattan distance.
"""
from pathlib import Path

import numpy as np
from scipy.spatial.distance import cdist

text = Path("input.txt").read_text()
grid = np.array([list(line) for line in text.splitlines()])
galaxies = np.argwhere(grid == "#")
max_coords = galaxies.max(axis=0)
missing_y = sorted(set(range(max_coords[0] + 1)) - set(galaxies[:, 0]), reverse=True)
missing_x = sorted(set(range(max_coords[1] + 1)) - set(galaxies[:, 1]), reverse=True)
for y in missing_y:
    galaxies[galaxies[:, 0] > y, 0] += 1
for x in missing_x:
    galaxies[galaxies[:, 1] > x, 1] += 1
result = cdist(galaxies, galaxies, metric="cityblock").sum()
print(int(result // 2))
