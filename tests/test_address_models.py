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


import pytest

from correios.exceptions import InvalidZipCodeException, InvalidStateException, InvalidTrackingCode
from correios.models.address import ZipCode, State, TrackingCode, Address, Phone


def test_basic_zip():
    zip_code = ZipCode("82940150")
    assert zip_code.code == "82940150"


def test_sanitize_zip():
    zip_code = ZipCode("82940-150")
    assert zip_code.code == "82940150"


def test_fail_invalid_zip():
    with pytest.raises(InvalidZipCodeException):
        ZipCode("12345")

    with pytest.raises(InvalidZipCodeException):
        ZipCode("123456789")


def test_convert_zip_to_str():
    assert str(ZipCode("82940-150")) == "82940150"


def test_zip_repr():
    assert repr(ZipCode("82940-150")) == "<ZipCode code: 82940150>"


def test_zip_display():
    assert ZipCode("82940150").display() == "82940-150"


def test_basic_phone():
    phone = Phone("+1 (212) 555-1234")
    assert phone == "+12125551234"
    assert phone == Phone("12125551234", "US")
    assert phone.display() == "+1 212-555-1234"
    assert str(phone) == "12125551234"
    assert repr(phone) == "<Phone 12125551234>"

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
    with pytest.raises(InvalidStateException):
        State("XY")

    with pytest.raises(InvalidStateException):
        State("Unknown State")


def test_convert_state():
    assert str(State("Distrito Federal")) == "DF"


def test_state_repr():
    assert repr(State("DF")) == "<State code: DF name: Distrito Federal>"


@pytest.mark.parametrize("tracking_code", [
    "DL74668653 BR",
    "DL746686536BR",
    "DL74668653BR",
    "dl74668653br",
])
def test_tracking_code_constructor(tracking_code):
    tracking = TrackingCode(tracking_code)
    assert str(tracking) == "DL746686536BR"
    assert tracking.code == "DL746686536BR"
    assert tracking.prefix == "DL"
    assert tracking.number == "74668653"
    assert tracking.digit == 6
    assert tracking.nodigit == "DL74668653 BR"
    assert tracking.short == "DL74668653BR"


@pytest.mark.parametrize("tracking_code", [
    "DL7466865BR",
    "DL746686530BR",  # invalid digit (0)
    "DL7466X653 BR",
    "DL74668653B",
    "D746686530 BR",
    "DL46686530 B1",
])
def test_fail_invalid_tracking_code(tracking_code):
    with pytest.raises(InvalidTrackingCode):
        TrackingCode(tracking_code)


@pytest.mark.parametrize("tracking_code,digit", [
    ("DL74668653 BR", 6),
    ("DL02000000 BR", 0),
    ("DL00000000 BR", 5),
])
def test_tracking_code_digit_calculator(tracking_code, digit):
    tracking = TrackingCode(tracking_code)
    assert tracking.digit == digit


def test_basic_address():
    address = Address(
        name="John Doe",
        phone="+111555-12345",
        cellphone="+11155-54321",
        email="john.doe@example.com",
        street="Rua dos Bobos",
        number="0",
        complement="apto. 3",
        neighborhood="Centro",
        city="Vinicius de Moraes",
        state="RJ",
        zip_code="12345-678",
    )

    assert address.name == "John Doe"
    assert address.phone == "+111555-12345"
    assert address.cellphone == "+11155-54321"
    assert address.email == "john.doe@example.com"
    assert address.street == "Rua dos Bobos"
    assert address.number == "0"
    assert address.complement == "apto. 3"
    assert address.neighborhood == "Centro"
    assert address.city == "Vinicius de Moraes"
    assert address.state == "RJ"
    assert address.zip_code == "12345-678"
