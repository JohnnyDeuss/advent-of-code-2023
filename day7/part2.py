"""
Encode each hands with characters that would sort correctly lexically.
Then transform them into a string that encodes the hierarchy
information. 
"""
from collections import Counter
from enum import IntEnum, auto
from pathlib import Path


class HandType(IntEnum):
    HIGH_CARD = auto()
    ONE_PAIR = auto()
    TWO_PAIR = auto()
    THREE_OF_A_KIND = auto()
    FULL_HOUSE = auto()
    FOUR_OF_A_KIND = auto()
    FIVE_OF_A_KIND = auto()


def lexical_encode(hand: str) -> str:
    table = str.maketrans("23456789TJQKA", "23456789B0DEF")
    return hand.translate(table)


def invert_dict(d: dict[str, int]) -> dict[int, list[str]]:
    inverted: dict[int, list[str]] = {}
    for key, value in d.items():
        inverted.setdefault(value, []).append(key)
    return inverted


def order_encode(hand: str) -> str:
    """
    Encode into a string with the following format: 1 character
    indicating the type of hand, followed by characters indicating the
    strength of the pairs, triples, etc.
    """
    encoded_hand = lexical_encode(hand)
    encoded_hand_without_jokers = encoded_hand.replace("0", "")
    joker_count = len(encoded_hand) - len(encoded_hand_without_jokers)
    counter = Counter(encoded_hand_without_jokers)
    counts = sorted(counter.values())
    if counts:
        counts[-1] += joker_count
    else:
        counts = [joker_count]

    if counts == [1, 1, 1, 1, 1]:
        hand_type = HandType.HIGH_CARD
    elif counts == [1, 1, 1, 2]:
        hand_type = HandType.ONE_PAIR
    elif counts == [1, 2, 2]:
        hand_type = HandType.TWO_PAIR
    elif counts == [1, 1, 3]:
        hand_type = HandType.THREE_OF_A_KIND
    elif counts == [2, 3]:
        hand_type = HandType.FULL_HOUSE
    elif counts == [1, 4]:
        hand_type = HandType.FOUR_OF_A_KIND
    elif counts == [5]:
        hand_type = HandType.FIVE_OF_A_KIND
    else:
        raise ValueError(f"Unexpected count: {counts}")
    print(
        hand,
        encoded_hand,
        encoded_hand_without_jokers,
        counts,
        f"{hand_type}{encoded_hand}",
    )
    return f"{hand_type}{encoded_hand}"


text = Path("input.txt").read_text()

hand_bid_strs = [line.split() for line in text.splitlines()]
hand_bids = [(order_encode(hand), int(bid_str)) for hand, bid_str in hand_bid_strs]
hand_bids = sorted(hand_bids, key=lambda hand_bid: hand_bid[0])
result = sum([hand_bid[1] * rank for rank, hand_bid in enumerate(hand_bids, start=1)])

print(result)
