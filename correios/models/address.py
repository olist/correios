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


from decimal import Decimal
from typing import List, Union

from phonenumbers import NumberParseException
from phonenumbers import PhoneNumberFormat, parse, format_number

from correios.exceptions import InvalidZipCodeError, InvalidStateError, InvalidAddressNumberError

ZIP_CODE_LENGTH = 8
STATE_LENGTH = 2


class ZipCode:
    def __init__(self, code: str):
        self._code = self._validate(code)

    @property
    def code(self) -> str:
        return self._code

    def _validate(self, code) -> str:
        code = "".join(d for d in code if d.isdigit())

        if len(code) != ZIP_CODE_LENGTH:
            raise InvalidZipCodeError("ZipCode code must have 8 digits")

        return code

    def display(self) -> str:
        return "{}-{}".format(self.code[:5], self.code[-3:])

    def __eq__(self, other):
        if isinstance(other, ZipCode):
            return self.code == other.code

        return self._code == self._validate(other)

    def __str__(self):
        return self.code

    def __repr__(self):
        return "<ZipCode code: {}>".format(self.code)

    def _next_multiple(self, n: int) -> int:
        return n + (n % 10 and (10 - (n % 10)))

    @property
    def digit(self):
        validator = sum(int(d) for d in self.code)
        return self._next_multiple(validator) - validator

    @classmethod
    def create(cls, code: Union['ZipCode', int, str]) -> 'ZipCode':
        if isinstance(code, ZipCode):
            return code

        if isinstance(code, int):
            code = str(code)

        return ZipCode(code)


class State:
    STATES = {
        'AC': 'Acre',
        'AL': 'Alagoas',
        'AP': 'Amapá',
        'AM': 'Amazonas',
        'BA': 'Bahia',
        'CE': 'Ceará',
        'DF': 'Distrito Federal',
        'ES': 'Espírito Santo',
        'GO': 'Goiás',
        'MA': 'Maranhão',
        'MT': 'Mato Grosso',
        'MS': 'Mato Grosso do Sul',
        'MG': 'Minas Gerais',
        'PA': 'Pará',
        'PB': 'Paraíba',
        'PR': 'Paraná',
        'PE': 'Pernambuco',
        'PI': 'Piauí',
        'RJ': 'Rio de Janeiro',
        'RN': 'Rio Grande do Norte',
        'RS': 'Rio Grande do Sul',
        'RO': 'Rondônia',
        'RR': 'Roraima',
        'SC': 'Santa Catarina',
        'SP': 'São Paulo',
        'SE': 'Sergipe',
        'TO': 'Tocantins',
    }
    _name_map = {v.lower(): k for k, v in STATES.items()}

    def __init__(self, code: str):
        self._code = self._validate(code)

    @property
    def code(self) -> str:
        return self._code

    def _validate(self, raw_state) -> str:
        state = self._name_map.get(raw_state.lower(), raw_state)
        state = state.upper()

        if len(state) != STATE_LENGTH or state not in self.STATES:
            raise InvalidStateError("State code {} is invalid".format(state))

        return state

    def display(self):
        return self.STATES[self.code]

    def __eq__(self, other):
        return self.code == self._validate(other)

    def __str__(self):
        return self.code

    def __repr__(self):
        return "<State code: {} name: {}>".format(self.code, self.display())


class ZipAddress:
    # noinspection PyShadowingBuiltins
    def __init__(self,
                 id: int,
                 zip_code: Union[ZipCode, str],
                 state: Union[State, str],
                 city: str,
                 district: str,
                 address: str,
                 complements: List[str]):
        self.id = id
        self.zip_code = ZipCode(str(zip_code))
        self.state = State(str(state))
        self.city = city
        self.district = district
        self.address = address
        self.complements = [c for c in complements if c]


class Phone:
    def __init__(self, number: str, country="BR"):
        try:
            self.parsed = self._parse(number, country)
        except NumberParseException:
            self.parsed = None
        self.country = country
        self.number = "".join(d for d in number if d.isdigit())

    def _parse(self, number: str, country: str):
        if number.startswith("+"):
            return parse(number)
        return parse(number, country)

    def display(self) -> str:
        if not self.parsed:
            return ""
        country_code = "+{!s}".format(self.parsed.country_code)
        return format_number(self.parsed, PhoneNumberFormat.INTERNATIONAL).replace(country_code, "").strip()

    @property
    def short(self) -> str:
        if not self.parsed:
            return ""
        return str(self.parsed.national_number)

    def __eq__(self, other: Union["Phone", str]):
        if not isinstance(other, Phone):
            other = Phone(other, self.country)
        return self.parsed == other.parsed

    def __str__(self):
        if not self.parsed:
            return ""
        return "{}{}".format(self.parsed.country_code, self.parsed.national_number)

    def __repr__(self):
        return "<Phone {!s}>".format(self)


class Address:
    def __init__(self,
                 name: str,
                 street: str,
                 number: Union[int, str],
                 city: str,
                 state: Union[State, str],
                 zip_code: Union[ZipCode, str],
                 complement: str = "",
                 neighborhood: str = "",
                 phone: Union[Phone, str] = "",
                 cellphone: Union[Phone, str] = "",
                 email: str = "",
                 latitude: Union[Decimal, str] = "0.0",
                 longitude: Union[Decimal, str] = "0.0",
                 ):
        self.name = name
        self.street = street
        self.city = city
        self.complement = complement
        self.neighborhood = neighborhood
        self.email = email

        self.number = str(number)
        if not self.number.isdigit():
            raise InvalidAddressNumberError("Address number can only have digits")

        if not isinstance(state, State):
            state = State(state)
        self.state = state

        if not isinstance(zip_code, ZipCode):
            zip_code = ZipCode(zip_code)
        self.zip_code = zip_code

        if not isinstance(phone, Phone):
            phone = Phone(phone)
        self.phone = phone

        if not isinstance(cellphone, Phone):
            cellphone = Phone(cellphone)
        self.cellphone = cellphone

        if not isinstance(latitude, Decimal):
            latitude = Decimal(latitude)
        self.latitude = latitude

        if not isinstance(longitude, Decimal):
            longitude = Decimal(longitude)
        self.longitude = longitude

    @property
    def zip_code_display(self):
        return self.zip_code.display()

    @property
    def display_address(self):
        address = "{}, {} {}".format(self.street, self.number, self.complement)
        city = "{} / {} - {}".format(self.city, self.state, self.zip_code.display())
        return address.strip(), city.strip()
