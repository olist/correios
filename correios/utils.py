from collections.abc import Container, Iterable, Set, Sized
from itertools import chain
from typing import Any, Union


class RangeSet(Sized, Iterable, Container):
    def __init__(self, *ranges: Union[range, Any]):
        self.ranges = []

        for r in ranges:
            if isinstance(r, range):
                r = [r]
            elif isinstance(r, RangeSet):
                r = list(r.ranges)
            elif isinstance(r, Iterable) and not isinstance(r, Set):
                r = [range(*r)]
            else:
                raise Exception("Invalid argument type {} of argument {!r}".format(type(r), r))

            self.ranges.extend(r)

    def __iter__(self):
        return chain.from_iterable(r for r in self.ranges)

    def __contains__(self, elem):
        return any(elem in r for r in self.ranges)

    def __len__(self):
        return sum(len(r) for r in self.ranges)
