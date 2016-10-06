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

import pytest

from correios.exceptions import InvalidZipCodeError, InvalidStateError, InvalidAddressNumberError
from correios.models.address import ZipCode, State, Address, Phone


def test_basic_zip():
    zip_code = ZipCode("82940150")
    assert zip_code.code == "82940150"


def test_sanitize_zip():
    zip_code = ZipCode("82940-150")
    assert zip_code.code == "82940150"


def test_fail_invalid_zip():
    with pytest.raises(InvalidZipCodeError):
        ZipCode("12345")

    with pytest.raises(InvalidZipCodeError):
        ZipCode("123456789")


def test_convert_zip_to_str():
    assert str(ZipCode("82940-150")) == "82940150"


def test_zip_repr():
    assert repr(ZipCode("82940-150")) == "<ZipCode code: 82940150>"


def test_zip_display():
    assert ZipCode("82940150").display() == "82940-150"


@pytest.mark.parametrize("zip_code,digit", [
    ("71010050", 6),
    ("82940150", 1),
])
def test_zip_code_check_digit(zip_code, digit):
    zip_code = ZipCode(zip_code)
    assert zip_code.digit == digit


@pytest.mark.parametrize("zip_code", [
    71010050,
    "71010050",
    ZipCode("71010050"),
])
def test_zip_code_creation(zip_code):
    assert ZipCode.create(zip_code) == ZipCode("71010050")


def test_basic_phone():
    phone = Phone("+1 (212) 555-1234")
    assert phone == "+12125551234"
    assert phone == Phone("12125551234", "US")
    assert phone.display() == "212-555-1234"
    assert phone.short == "2125551234"
    assert str(phone) == "12125551234"
    assert repr(phone) == "<Phone 12125551234>"


def test_empty_phone():
    phone = Phone("")
    assert phone == ""
    assert phone == Phone("", "US")
    assert phone.display() == ""
    assert phone.short == ""
    assert str(phone) == ""
    assert repr(phone) == "<Phone >"


@pytest.mark.parametrize("code,name", (
        ('AC', 'Acre'),
        ('AL', 'Alagoas'),
        ('AP', 'Amapá'),
        ('AM', 'Amazonas'),
        ('BA', 'Bahia'),
        ('CE', 'Ceará'),
        ('DF', 'Distrito Federal'),
        ('ES', 'Espírito Santo'),
        ('GO', 'Goiás'),
        ('MA', 'Maranhão'),
        ('MT', 'Mato Grosso'),
        ('MS', 'Mato Grosso do Sul'),
        ('MG', 'Minas Gerais'),
        ('PA', 'Pará'),
        ('PB', 'Paraíba'),
        ('PR', 'Paraná'),
        ('PE', 'Pernambuco'),
        ('PI', 'Piauí'),
        ('RJ', 'Rio de Janeiro'),
        ('RN', 'Rio Grande do Norte'),
        ('RS', 'Rio Grande do Sul'),
        ('RO', 'Rondônia'),
        ('RR', 'Roraima'),
        ('SC', 'Santa Catarina'),
        ('SP', 'São Paulo'),
        ('SE', 'Sergipe'),
        ('TO', 'Tocantins'),
))
def test_states(code, name):
    state = State(code)
    assert state.code == code
    assert state.display() == name

    state = State(name)
    assert state.code == code
    assert state.display() == name


@pytest.mark.parametrize("state", ("df", "distrito federal"))
def test_lowercase_state_name(state):
    state = State(state)
    assert state.code == "DF"
    assert state.display() == "Distrito Federal"


def test_fail_invalid_state():
    with pytest.raises(InvalidStateError):
        State("XY")

    with pytest.raises(InvalidStateError):
        State("Unknown State")


def test_convert_state():
    assert str(State("Distrito Federal")) == "DF"


def test_state_repr():
    assert repr(State("DF")) == "<State code: DF name: Distrito Federal>"


def test_basic_address():
    address = Address(
        name="John Doe",
        phone="+111555-12345",
        cellphone="+11155-54321",
        email="john.doe@example.com",
        street="Rua dos Bobos",
        number="5",
        complement="apto. 3",
        neighborhood="Centro",
        city="Vinicius de Moraes",
        state="RJ",
        zip_code="12345-678",
        latitude="10.0",
        longitude="-10.0",
    )

    assert address.name == "John Doe"
    assert address.phone == "+111555-12345"
    assert address.cellphone == "+11155-54321"
    assert address.email == "john.doe@example.com"
    assert address.street == "Rua dos Bobos"
    assert address.number == "5"
    assert address.complement == "apto. 3"
    assert address.neighborhood == "Centro"
    assert address.city == "Vinicius de Moraes"
    assert address.state == "RJ"
    assert address.zip_code == "12345-678"
    assert address.zip_code_display == "12345-678"


def test_fail_invalid_address_number():
    with pytest.raises(InvalidAddressNumberError):
        Address(name="John Doe",
                street="Rua dos Bobos",
                number="asd",
                city="Vinicius de Moraes",
                state="RJ",
                zip_code="12345-678")


def test_basic_address_only_mandatory_args():
    address = Address(
        name="John Doe",
        street="Rua dos Bobos",
        number="0",
        city="Vinicius de Moraes",
        state="RJ",
        zip_code="12345-678",
    )

    assert address.name == "John Doe"
    assert address.street == "Rua dos Bobos"
    assert address.number == "0"
    assert address.city == "Vinicius de Moraes"
    assert address.state == "RJ"
    assert address.zip_code == "12345-678"
    assert address.email == ""
    assert address.complement == ""
    assert address.neighborhood == ""
    assert address.phone == ""
    assert address.cellphone == ""
    assert address.latitude == Decimal("0.0")
    assert address.longitude == Decimal("0.0")
