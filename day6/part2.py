"""
Exactly the same as part 1, we just parse the numbers differently.
"""

from math import ceil, floor
from pathlib import Path

text = Path("input.txt").read_text()
time, distance = [
    int(line.split(":")[1].replace(" ", "")) for line in text.splitlines()
]


def solve_quadratic_equation(a: int, b: int, c: int) -> list[float]:
    discriminant = b**2 - 4 * a * c
    if discriminant < 0:
        return []
    if discriminant == 0:
        return [-b / (2 * a)]
    return sorted(
        [
            (-b - discriminant**0.5) / (2 * a),
            (-b + discriminant**0.5) / (2 * a),
        ]
    )


solutions = solve_quadratic_equation(1, -time, distance)
assert len(solutions) == 2
result = floor(solutions[1]) - ceil(solutions[0]) + 1
print(result)
