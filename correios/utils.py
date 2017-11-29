# Copyright 2016 Osvaldo Santana Neto
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import re
from datetime import datetime
from decimal import Decimal
from itertools import chain
from pathlib import Path
from typing import Container, Iterable, Sized, Union

import pkg_resources


def capitalize_phrase(phrase: str) -> str:
    return ' '.join(word.capitalize() for word in phrase.split(' '))


def rreplace(string: str, old: str, new: str, count: int = 0) -> str:
    """
    Return a copy of string with all occurences of substring
    old replace by new starting from the right. If the optional
    argument count is given only the first count occurences are
    replaced.
    """

    reverse = string[::-1]
    if count:
        return reverse.replace(old[::-1], new[::-1], count)[::-1]

    return reverse.replace(old[::-1], new[::-1])[::-1]


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
            except Exception:
                msg = "RangeSet argument must be a range, RangeSet or an Iterable, not {}"
                raise ValueError(msg.format(type(r)))

            self.ranges.extend(element)

    def __iter__(self):
        return chain.from_iterable(r for r in self.ranges)

    def __contains__(self, elem):
        return any(elem in r for r in self.ranges)

    def __len__(self):
        return sum(len(r) for r in self.ranges)


def to_integer(number: Union[int, str]) -> int:
    return int(str(number).strip())


def to_datetime(date: Union[datetime, str], fmt="%Y-%m-%d %H:%M:%S%z") -> datetime:
    if isinstance(date, str):
        last_colon_pos = date.rindex(":")
        date = date[:last_colon_pos] + date[last_colon_pos + 1:]
        return datetime.strptime(date, fmt)
    return date


def to_decimal(value: Union[Decimal, str, float], precision=2) -> Decimal:
    if not isinstance(value, Decimal):
        value = rreplace(str(value), ",", ".", 1)
        if "." in value:
            real, imag = value.rsplit(".", 1)
        else:
            real, imag = value, "0"
        real = re.sub("[,._]", "", real)
        value = Decimal("{}.{}".format(real, imag))

    quantize = Decimal("0." + "0" * precision)
    return value.quantize(quantize)


def get_resource_path(path) -> Path:
    resource_package = 'correios'
    resource_path = os.path.join("data", path)
    return Path(pkg_resources.resource_filename(resource_package, resource_path))
