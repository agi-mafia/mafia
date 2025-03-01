import random
from collections import Counter
from typing import Iterable


def most_frequent_random(l: Iterable):
    """Returns the most frequent member of a list.

    If there is a draw, chooses randomly between the most frequent members.
    """
    if not l:
        return None
    counts = Counter(l)
    max_freq = max(counts.values())
    most_frequent_members = [num for num, freq in counts.items() if freq == max_freq]
    return random.choice(most_frequent_members)
