"""
Looking at the input, there are 6 disjoint components. Every node, apart
from the starting nodes, can get visited from at least one node. 
Checking each loop, we notice that they're perfectly periodic, i.e. the
number of steps between our starting A and each subsequent Z is
consistent. This means we just need to find the LCM of the periods of
each loop.
"""

from itertools import cycle
from math import lcm
from pathlib import Path

text = Path("input.txt").read_text()
instructions, paths_str = text.split("\n\n")
paths = {line[:3]: (line[7:10], line[12:15]) for line in paths_str.splitlines()}

currents = {node for node in paths.keys() if node.endswith("A")}

visited = set()
loops = []
for current in currents:
    if current in visited:
        continue
    queue = []
    queue.append(current)
    loop = set()
    while queue:
        current = queue.pop(0)
        if current in loop:
            continue
        loop.add(current)
        queue.extend(paths[current])
    loops.append(loop)
    visited.update(loop)

factors = []
for loop in loops:
    current = next(node for node in currents if node in loop)
    for step, direction in enumerate(cycle(list(instructions)), start=1):
        path_idx = 0 if direction == "L" else 1
        current = paths[current][path_idx]
        if current.endswith("Z"):
            factors.append(step)
            break

print(lcm(*factors))
