"""
Parse all the games and draws, and compare the counts with the limits
to tally up the IDs of the games that have no conflicts.
"""
from pathlib import Path

limits = {
    "red": 12,
    "green": 13,
    "blue": 14,
}
text = Path("input.txt").read_text()
tally = 0
for line in text.splitlines():
    game_str, line = line.split(": ")
    draws = line.split("; ")
    for draw in draws:
        draw_items = draw.split(", ")
        draw_str_dict = dict([reversed(draw_item.split()) for draw_item in draw_items])
        draw_dict = {k: int(v) for k, v in draw_str_dict.items()}
        conflict_found = any(draw_dict[k] > limits[k] for k in draw_dict)
        if conflict_found:
            break
    if not conflict_found:
        id = int(game_str.removeprefix("Game "))
        tally += id
print(tally)
