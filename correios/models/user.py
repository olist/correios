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


from datetime import datetime
from typing import List, TypeVar

from correios.exceptions import InvalidFederalTaxNumberException


N = TypeVar("N", int, str)
D = TypeVar("D", datetime, str)


def _to_integer(number: N) -> int:
    try:
        return int(number.strip())
    except AttributeError:
        return int(number)


def _to_datetime(date: D, fmt="%Y-%m-%d %H:%M:%S%z"):
    if date is None:
        return date

    if isinstance(date, str):
        last_colon_pos = date.rindex(":")
        date = date[:last_colon_pos] + date[last_colon_pos + 1:]
        return datetime.strptime(date, fmt)
    return date


class AbstractTaxNumber(object):
    def __init__(self, number: str):
        self._number = self._validate(number)

    @property
    def number(self) -> str:
        return self._number

    def _sanitize(self, raw_number: str) -> str:
        return "".join(d for d in raw_number if d.isdigit())

    def _validate(self, raw_number: str):
        raise NotImplementedError()  # pragma: no cover

    def display(self) -> str:
        raise NotImplementedError()  # pragma: no cover

    def __str__(self):
        return self.number

    def __repr__(self):
        return "<{} number: {}>".format(self.__class__.__name__, self.number)

    def __eq__(self, other):
        return self.number == self._sanitize(other)


class FederalTaxNumber(AbstractTaxNumber):
    FEDERAL_TAX_NUMBER_SIZE = 14

    def _check_verification_digits(self, raw_number):
        number = [int(d) for d in raw_number[:12]]
        prod = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        assert len(number) == len(prod)

        while len(number) < 14:
            r = sum(x * y for (x, y) in zip(number, prod)) % 11
            f = (11 - r) if r > 1 else 0
            number.append(f)
            prod.insert(0, prod[0] + 1)

        number = "".join(str(d) for d in number)
        return raw_number == number

    def _validate(self, raw_number: str):
        raw_number = self._sanitize(raw_number)

        if len(raw_number) != FederalTaxNumber.FEDERAL_TAX_NUMBER_SIZE:
            raise InvalidFederalTaxNumberException(
                "Tax Number must have {} digits".format(self.FEDERAL_TAX_NUMBER_SIZE))

        if not self._check_verification_digits(raw_number):
            raise InvalidFederalTaxNumberException("Invalid Federal Tax Number verification digits")

        return raw_number

    def display(self) -> str:
        return "{}.{}.{}/{}-{}".format(self.number[:2],
                                       self.number[2:5],
                                       self.number[5:8],
                                       self.number[8:12],
                                       self.number[12:])


class StateTaxNumber(AbstractTaxNumber):
    def _validate(self, raw_number: str):
        return self._sanitize(raw_number)

    def display(self) -> str:
        return self.number


class Service(object):
    # noinspection PyShadowingBuiltins
    def __init__(self,
                 id: int,
                 code: N,
                 description: str,
                 category: str,
                 postal_code: N,
                 start_date: D=None,
                 end_date: D=None):
        self.id = id
        self.code = _to_integer(code)
        self.description = description.strip()
        self.category = category.strip()
        self.postal_code = _to_integer(postal_code)
        self.start_date = _to_datetime(start_date)
        self.end_date = _to_datetime(end_date)

    def __repr__(self):
        return "Service(id={0.id!r}, code={0.code!r}, description={0.description!r}, category={0.category!r}, " \
               "postal_code={0.postal_code!r}, start_date={0.start_date!r}, end_date={0.end_date!r})".format(self)


class PostingCard(object):
    def __init__(self,
                 number: N,  # 10 digits
                 administrative_code: N,  # 8 digits
                 start_date: D,
                 end_date: D,
                 status: N,  # 2 digits
                 status_code: str,
                 unit: N,  # 2 digits
                 services: List[Service]):
        self.number = _to_integer(number)
        self.administrative_code = _to_integer(administrative_code)
        self.start_date = _to_datetime(start_date)
        self.end_date = _to_datetime(end_date)
        self.status = _to_integer(status)
        self.status_code = status_code
        self.unit = _to_integer(unit)
        self.services = services


class Contract(object):
    def __init__(self,
                 number: N,
                 customer_code: int,
                 administrative_code: N,
                 management_name: str,
                 status_code: str,
                 start_date: D,
                 end_date: D,
                 posting_cards: List[PostingCard]):

        self.number = _to_integer(number)
        self.customer_code = customer_code
        self.administrative_code = _to_integer(administrative_code)
        self.management_name = management_name.strip()
        self.status_code = status_code
        self.start_date = _to_datetime(start_date)
        self.end_date = _to_datetime(end_date)
        self.posting_cards = posting_cards


class User(object):
    def __init__(self,
                 name: str,
                 federal_tax_number: FederalTaxNumber,
                 state_tax_number: StateTaxNumber,
                 status_number: N,
                 contracts: List[Contract]):
        self.name = name.strip()
        self.federal_tax_number = federal_tax_number
        self.state_tax_number = state_tax_number
        self.status_number = _to_integer(status_number)

        self.contracts = contracts
