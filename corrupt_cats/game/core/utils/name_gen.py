"""Randomly generates name of a country."""
import random

from .functions import rnd
from .lists import (
    s1, s2, s3, s4, s5, s6
)


class NameGen:
    def __init__(self):
        self.method = random.randint(1, 5)

    def generate_name(self, method: int = None) -> str:
        """Generates a random country name.
        'parts' should be integer in range(1, 6)
        """
        if method is None:
            method = self.method

        if method < 1 or method > 5 or not isinstance(method, int):
            raise TypeError(
                f"Expected arg 'parts' of type 'int' and in range(1, 6), got {method}."
            )

        return gen_name(method)


def connect(strings, split_index: int = None):
    i = split_index

    if i is None:
        res = "".join(strings)
    else:
        res = "".join(strings[:i]) + " " + "".join(strings[i:])

    return res.title()


def gen_name(method: int):
    """Actually generates name of a country, according to different name types."""
    cases = {
        1: (s1, s2, s3, s4, s5),
        2: (s1, s2, s3, s6),
        3: (s3, s4, s5),
        4: (s2, s3, s6),
        5: (s3, s4, s1, s3, s6)
    }
    seq_tuple = cases.get(method)  # getting sequences we are going to use
    rnd_gen = (rnd(seq) for seq in seq_tuple)  # get random indexes for each sequence
    parts = [seq[i] for seq, i in zip(seq_tuple, rnd_gen)]  # get one element from each sequence
    return connect(parts) if method != 5 else connect(parts, 3)  # return connecred parts
