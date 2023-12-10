"""
Looking at the input, the loop goes north and returns from the west, so
we just follow it and count how long it takes to get back to S.
"""
from itertools import count
from pathlib import Path


class InvalidCameFromError(Exception):
    def __init__(self, came_from):
        self.came_from = came_from
        super().__init__(f"Invalid came_from: {came_from}")


text = Path('input.txt').read_text()
grid = text.splitlines()
x, y = next((x, y) for y, row in enumerate(grid) for x, c in enumerate(row) if c == 'S')
assert grid[y][x] == 'S'
y -= 1
came_from = 'S'
for steps in count(start=1):
    match grid[y][x]:
        case 'F':
            if came_from == 'S':
                x += 1
                came_from = 'W'
            elif came_from == 'E':
                y += 1
                came_from = 'N'
            else:
                raise ValueError(f'Invalid came_from: {came_from}')
        case 'L':
            if came_from == 'N':
                x += 1
                came_from = 'W'
            elif came_from == 'E':
                y -= 1
                came_from = 'S'
            else:
                raise ValueError(f'Invalid came_from: {came_from}')
        case 'J':
            if came_from == 'N':
                x -= 1
                came_from = 'E'
            elif came_from == 'W':
                y -= 1
                came_from = 'S'
            else:
                raise ValueError(f'Invalid came_from: {came_from}')
        case '7':
            if came_from == 'W':
                y += 1
                came_from = 'N'
            elif came_from == 'S':
                x -= 1
                came_from = 'E'
            else:
                raise ValueError(f'Invalid came_from: {came_from}')
        case '|':
            if came_from == 'N':
                y += 1
                came_from = 'N'
            elif came_from == 'S':
                y -= 1
                came_from = 'S'
            else:
                raise ValueError(f'Invalid came_from: {came_from}')
        case '-':
            if came_from == 'W':
                x += 1
                came_from = 'W'
            elif came_from == 'E':
                x -= 1
                came_from = 'E'
            else:
                raise ValueError(f'Invalid came_from: {came_from}')
        case 'S':
            break
        case _:
            raise ValueError(f'Invalid pipe character: {grid[y][x]}')

print((steps + 1) // 2)
