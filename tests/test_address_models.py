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

from correios.exceptions import InvalidZipCodeException, InvalidStateException
from correios.models.address import ZipCode, State


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
