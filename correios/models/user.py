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

from correios.exceptions import InvalidFederalTaxNumber


N = TypeVar("N", int, str)
D = TypeVar("D", datetime, str)


class AbstractTaxNumber(object):
    def __init__(self, number: str):
        self._number = None
        self.set_number(number)

    def get_number(self) -> str:
        return self._number

    def set_number(self, number: str):
        self._number = self._validate(number)

    number = property(get_number, set_number)

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
            raise InvalidFederalTaxNumber("Tax Number must have {} digits".format(self.FEDERAL_TAX_NUMBER_SIZE))

        if not self._check_verification_digits(raw_number):
            raise InvalidFederalTaxNumber("Invalid Federal Tax Number verification digits")

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


class PostingCard(object):
    pass


class Contract(object):
    def __init__(self,
                 number: N,
                 customer_code: int,
                 management_code: N,
                 management_name: str,
                 status_code: str,
                 start_date: datetime,
                 end_date: datetime,
                 posting_cards: List[PostingCard]):
        try:
            self.number = int(number.strip())
        except AttributeError:
            self.number = number

        self.customer_code = customer_code

        try:
            self.management_code = int(management_code.strip())
        except AttributeError:
            self.management_code = management_code

        self.management_name = management_name.strip()
        self.status_code = status_code
        self.start_date = start_date
        self.end_date = end_date
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

        try:
            self.status_number = int(status_number.strip())
        except AttributeError:
            self.status_number = status_number

        self.contracts = contracts
