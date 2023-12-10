from pathlib import Path

import numpy as np

text = Path("input.txt").read_text()
lines = text.splitlines()
sequences = [np.array(line.split(" "), dtype=int) for line in lines]

total = 0
for seq in sequences:
    first_digits = [seq[0]]
    diff = np.diff(seq)
    while np.any(diff != 0):
        first_digits.append(diff[0])
        diff = np.diff(diff)
    new_digit = 0
    for first_digit in reversed(first_digits):
        new_digit = -new_digit + first_digit
    total += new_digit
print(total)
