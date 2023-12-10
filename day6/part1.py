"""
The problem is an inequality:

]

x + d/x > t
x + d/x - t > 0
x^2 + d - tx > 0
x^2 - tx + d > 0

This is a quadratic inequality, so we can solve it by finding the roots
and checking the sign of the parabola in between.

x = (t±D)/2

where D is the discriminant, D = b²-4ac.
"""

import operator
from functools import reduce
from math import ceil, floor
from pathlib import Path

text = Path("input.txt").read_text()
times, distances = [
    [int(x) for x in line.split(":")[1].split()] for line in text.splitlines()
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


solutions_list = [
    solve_quadratic_equation(1, -time, distance)
    for time, distance in zip(times, distances)
]
solutions_list = [solutions for solutions in solutions_list if len(solutions) == 2]
num_solutions_each = [
    floor(solutions[1]) - ceil(solutions[0]) + 1 for solutions in solutions_list
]
result = reduce(operator.mul, num_solutions_each)
print(result)
