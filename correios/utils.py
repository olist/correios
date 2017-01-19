from itertools import chain
from typing import Container, Iterable, Sized


def capitalize_phrase(phrase: str) -> str:
    return ' '.join(word.capitalize() for word in phrase.split(' '))


def rreplace(string: str, old: str, new: str, count: int = 0) -> str:
    """
    Return a copy of string with all occurences of substring
    old replace by new starting from the right. If the optional
    argument count is given only the first count occurences are
    replaced.
    """

    return string[::-1].replace(old[::-1], new[::-1], count)[::-1]


class RangeSet(Sized, Iterable, Container):
    def __init__(self, *ranges):
        self.ranges = []

        for r in ranges:
            if isinstance(r, range):
                self.ranges.append(r)
                continue

            try:
                element = list(r.ranges)
            except AttributeError:
                element = None

            try:
                element = element or [range(*r)]
            except:
                msg = "RangeSet argument must be a range, RangeSet or an Iterable, not {}"
                raise ValueError(msg.format(type(r)))

            self.ranges.extend(element)

    def __iter__(self):
        return chain.from_iterable(r for r in self.ranges)

    def __contains__(self, elem):
        return any(elem in r for r in self.ranges)

    def __len__(self):
        return sum(len(r) for r in self.ranges)
