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

from .exceptions import InvalidZipCode, InvalidFederalTaxNumber


class Zip(object):
    def __init__(self, code):
        self._code = None
        self.code = code

    @property
    def code(self):
        return self._code

    @code.setter
    def code(self, code):
        code = "".join(d for d in code if d.isdigit())
        if len(code) != 8:
            raise InvalidZipCode("Zip code must have 8 digits")
        self._code = code

    def display(self):
        return "{}-{}".format(self.code[:5], self.code[-3:])

    def __str__(self):
        return self.code

    def __repr__(self):
        return "<Zip code: {}>".format(self.code)


class AbstractTaxNumber(object):
    def __init__(self, number: str):
        self._number = None
        self.number = number

    @property
    def number(self):
        return self._number

    @number.setter
    def number(self, number):
        self._number = self._validate(number)

    def _validate(self, raw_number):
        raise NotImplementedError()

    def display(self):
        raise NotImplementedError()

    def __str__(self):
        return self.number

    def __repr__(self):
        return "<{} number: {}>".format(self.__class__.__name__, self.number)


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

    def _validate(self, raw_number):
        raw_number = "".join(d for d in raw_number if d.isdigit())

        if len(raw_number) != FederalTaxNumber.FEDERAL_TAX_NUMBER_SIZE:
            raise InvalidFederalTaxNumber("Tax Number must have {} digits".format(self.FEDERAL_TAX_NUMBER_SIZE))

        if not self._check_verification_digits(raw_number):
            raise InvalidFederalTaxNumber("Invalid Federal Tax Number verification digits")

        return raw_number

    def display(self):
        return "{}.{}.{}/{}-{}".format(self.number[:2],
                                       self.number[2:5],
                                       self.number[5:8],
                                       self.number[8:12],
                                       self.number[12:])


class StateTaxNumber(AbstractTaxNumber):
    def _validate(self, raw_number):
        return "".join(d for d in raw_number if d.isdigit())

    def display(self):
        return self.number


class User(object):
    def __init__(self, name: str, federal_tax_number: FederalTaxNumber, status: int, updated_at: datetime,
                 contracts=None):
        self.name = name
        self.federal_tax_number = federal_tax_number
        self.status = status
        self.updated_at = updated_at
        self.contracts = []

        if contracts is not None:
            self.contracts = contracts

    @classmethod
    def from_response(cls, response):
        user = cls(name=response.nome,
                   federal_tax_number=FederalTaxNumber(response.cnpj),
                   status=response.statusCodigo,
                   updated_at=response.dataAtualizacao)
        # for x in contracts...
        return user
