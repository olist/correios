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
from typing import List, Union, Optional

from correios.exceptions import InvalidFederalTaxNumberException


def _to_integer(number: Union[int, str]) -> int:
    try:
        return int(number.strip())
    except AttributeError:
        return int(number)


def _to_datetime(date: Union[datetime, str], fmt="%Y-%m-%d %H:%M:%S%z") -> datetime:
    if isinstance(date, str):
        last_colon_pos = date.rindex(":")
        date = date[:last_colon_pos] + date[last_colon_pos + 1:]
        return datetime.strptime(date, fmt)
    return date


def _to_federal_tax_number(federal_tax_number) -> "FederalTaxNumber":
    if isinstance(federal_tax_number, FederalTaxNumber):
        return federal_tax_number

    return FederalTaxNumber(federal_tax_number)


def _to_state_tax_number(state_tax_number) -> "StateTaxNumber":
    if isinstance(state_tax_number, StateTaxNumber):
        return state_tax_number

    return StateTaxNumber(state_tax_number)


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
                 code: Union[int, str],
                 description: str,
                 category: str,
                 postal_code: Union[int, str],
                 start_date: Union[datetime, str, type(None)]=None,
                 end_date: Union[datetime, str, type(None)]=None):
        self.id = id
        self.code = _to_integer(code)
        self.description = description.strip()
        self.category = category.strip()
        self.postal_code = _to_integer(postal_code)
        self.start_date = _to_datetime(start_date)
        self.end_date = _to_datetime(end_date)

    def __str__(self):
        return str(self.code)


class Contract(object):
    def __init__(self,
                 number: Union[int, str],
                 customer_code: int,
                 direction_code: Union[int, str],
                 direction: str,
                 status_code: str,
                 start_date: Union[datetime, str],
                 end_date: Union[datetime, str],
                 posting_cards: Optional[List['PostingCard']]=None):

        self.number = _to_integer(number)
        self.customer_code = customer_code
        self.direction = direction.strip()
        self.status_code = status_code
        self.direction_code = _to_integer(direction_code)

        if start_date is not None:
            start_date = _to_datetime(start_date)
        self.start_date = start_date

        if end_date is not None:
            end_date = _to_datetime(end_date)
        self.end_date = end_date

        if posting_cards is None:
            posting_cards = []
        self.posting_cards = posting_cards

    def add_posting_card(self, posting_card: 'PostingCard'):
        self.posting_cards.append(posting_card)


class PostingCard(object):
    ACTIVE = True
    CANCELLED = False

    def __init__(self,
                 contract: Contract,
                 number: Union[int, str],  # 10 digits
                 administrative_code: Union[int, str],  # 8 digits
                 start_date: Union[datetime, str],
                 end_date: Union[datetime, str],
                 status: Union[int, str],  # 2 digits
                 status_code: str,
                 unit: Union[int, str],  # 2 digits
                 services: Optional[List[Service]]=None):
        self.contract = contract
        self._number = _to_integer(number)
        self._administrative_code = _to_integer(administrative_code)
        self.start_date = _to_datetime(start_date)
        self.end_date = _to_datetime(end_date)
        self.status = _to_integer(status)
        self.status_code = status_code
        self.unit = _to_integer(unit)

        if services is None:
            services = []
        self.services = services

        if self not in self.contract.posting_cards:
            self.contract.add_posting_card(self)

    @property
    def number(self):
        return "{:010}".format(self._number)

    @property
    def administrative_code(self):
        return "{:08}".format(self._administrative_code)

    def add_service(self, service: Service):
        self.services.append(service)


class User(object):
    def __init__(self,
                 name: str,
                 federal_tax_number: Union[str, FederalTaxNumber],
                 state_tax_number: Optional[Union[str, StateTaxNumber]]=None,
                 status_number: Optional[Union[int, str]]=None,
                 contracts: Optional[List[Contract]]=None):
        self.name = name.strip()
        self.federal_tax_number = _to_federal_tax_number(federal_tax_number)

        if status_number is not None:
            status_number = _to_integer(status_number)
        self.status_number = status_number

        if state_tax_number is not None:
            state_tax_number = _to_state_tax_number(state_tax_number)
        self.state_tax_number = state_tax_number

        if contracts is None:
            contracts = []
        self.contracts = contracts
