"""
Search from both directions for digits and stitch them together to form
two-digit numbers and then sum them up. This time, we search with
regular expressions, to easily search for multiple variable length
patterns. We compile a separate regex for the reversed patterns, so that
we can search for them in the reversed string. We replace the match
with the digits they represent, and then stitch them together to form
two-digit numbers.
"""
import re
from pathlib import Path


def as_numerical_digit(digit: str) -> str:
    return (
        digit.replace("one", "1")
        .replace("two", "2")
        .replace("three", "3")
        .replace("four", "4")
        .replace("five", "5")
        .replace("six", "6")
        .replace("seven", "7")
        .replace("eight", "8")
        .replace("nine", "9")
    )


patterns = [
    "one",
    "two",
    "three",
    "four",
    "five",
    "six",
    "seven",
    "eight",
    "nine",
]
digit_re = re.compile("|".join(["\d", *patterns]))
reversed_digit_re = re.compile(
    "|".join(["\d", *[pattern[::-1] for pattern in patterns]])
)

text = Path("input.txt").read_text()
orig_text = text
lines = text.splitlines()
numbers = [
    int(
        as_numerical_digit(digit_re.search(line).group())
        + as_numerical_digit(reversed_digit_re.search(line[::-1]).group()[::-1])
    )
    for line in lines
]
solution = sum(numbers)
print(solution)
