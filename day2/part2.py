"""
Very similar, but just keep updating the lower bound for each color on
every draw. Multiply the lower bounds together to get the power.
"""
import operator
from functools import reduce
from pathlib import Path

limits = {
    "red": 12,
    "green": 13,
    "blue": 14,
}
text = Path("input.txt").read_text()
total = 0
for line in text.splitlines():
    game_str, line = line.split(": ")
    draws = line.split("; ")
    lower_bound = {"red": 0, "green": 0, "blue": 0}
    for draw in draws:
        draw_items = draw.split(", ")
        draw_str_dict = dict([reversed(draw_item.split()) for draw_item in draw_items])
        draw_dict = {k: int(v) for k, v in draw_str_dict.items()}
        lower_bound = {k: max(lower_bound[k], draw_dict.get(k, 0)) for k in lower_bound}
    power = reduce(operator.mul, lower_bound.values())
    total += power
print(total)
