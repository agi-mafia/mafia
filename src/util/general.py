from collections import Counter
import random
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
    if len(most_frequent_members) == 0:
        return -1
    else:
        return random.choice(most_frequent_members)
