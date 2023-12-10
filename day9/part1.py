from pathlib import Path

import numpy as np

text = Path("input.txt").read_text()
lines = text.splitlines()
sequences = [np.array(line.split(" "), dtype=int) for line in lines]

total = 0
for seq in sequences:
    final_digits = [seq[-1]]
    diff = np.diff(seq)
    while np.any(diff != 0):
        final_digits.append(diff[-1])
        diff = np.diff(diff)
    new_digit = np.sum(final_digits)
    total += new_digit
print(total)
