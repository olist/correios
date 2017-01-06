from itertools import chain
from typing import Sized, Iterable, Container, Set


class RangeSet(Sized, Iterable, Container):
    def __init__(self, *ranges):
        self.ranges = []

        for r in ranges:
            if isinstance(r, range):
                r = [r]
            elif isinstance(r, RangeSet):
                r = list(r.ranges)
            elif isinstance(r, Iterable) and not isinstance(r, Set):
                r = [range(*r)]
            else:
                msg = "RangeSet argument must be a range, RangeSet or an Iterable, not {}"
                raise ValueError(msg.format(type(r)))

            self.ranges.extend(r)

    def __iter__(self):
        return chain.from_iterable(r for r in self.ranges)

    def __contains__(self, elem):
        return any(elem in r for r in self.ranges)

    def __len__(self):
        return sum(len(r) for r in self.ranges)
