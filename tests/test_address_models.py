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
import warnings

import pytest

from correios.exceptions import InvalidZipCodeError, InvalidStateError
from correios.models.address import (ZipCode, State, Address, Phone, ReceiverAddress,
                                     SenderAddress)


def test_basic_zip():
    zip_code = ZipCode("82940150")
    assert zip_code.code == "82940150"
    assert zip_code.prefix == 82940
    assert zip_code.sufix == 150


def test_sanitize_zip():
    zip_code = ZipCode("82940-150")
    assert zip_code.code == "82940150"
    assert zip_code.prefix == 82940
    assert zip_code.sufix == 150


@pytest.mark.parametrize('zipcode', ("12345", "123456789", "12.345-000", "12345.000"))
def test_fail_invalid_zipcode_format(zipcode):
    with pytest.raises(InvalidZipCodeError):
        ZipCode(zipcode)


@pytest.mark.parametrize('zipcode', ("00000-000", "728001-000"))
def test_fail_invalid_zipcode_range(zipcode):
    with pytest.raises(InvalidZipCodeError):
        ZipCode(zipcode)


@pytest.mark.parametrize('zip_code, state', [
                         ('13560060', 'SP'),
                         ('04547-003', 'SP'),
                         ('28921-100', 'RJ'),
                         ('22440-033', 'RJ'),
                         ('29213-360', 'ES'),
                         ('29048-495', 'ES'),
                         ('35900-457', 'MG'),
                         ('30190-060', 'MG'),
                         ('42800-040', 'BA'),
                         ('40015-170', 'BA'),
                         ('49500-000', 'SE'),
                         ('49037-580', 'SE'),
                         ('57820-000', 'AL'),
                         ('57032-901', 'AL'),
                         ('53370-255', 'PE'),
                         ('50030-150', 'PE'),
                         ('58400-355', 'PB'),
                         ('58051-900', 'PB'),
                         ('59580-000', 'RN'),
                         ('59015-900', 'RN'),
                         ('64260-000', 'PI'),
                         ('64046-902', 'PI'),
                         ('62598-973', 'CE'),
                         ('60060-440', 'CE'),
                         ('65268-000', 'MA'),
                         ('65056-480', 'MA'),
                         ('68040-090', 'PA'),
                         ('66115-970', 'PA'),
                         ('68925-000', 'AP'),
                         ('68908-119', 'AP'),
                         ('69340-000', 'RR'),
                         ('69310-000', 'RR'),
                         ('69400-000', 'AM'),
                         ('69041-000', 'AM'),
                         ('69928-000', 'AC'),
                         ('69918-093', 'AC'),
                         ('76907-438', 'RO'),
                         ('76803-970', 'RO'),
                         ('77600-000', 'TO'),
                         ('77061-900', 'TO'),
                         ('76400-000', 'GO'),
                         ('74810-907', 'GO'),
                         ('73010-521', 'DF'),
                         ('70150-000', 'DF'),
                         ('78200-000', 'MT'),
                         ('78030-210', 'MT'),
                         ('79730-000', 'MS'),
                         ('79101-901', 'MS'),
                         ('83203-100', 'PR'),
                         ('80730-000', 'PR'),
                         ('88330-000', 'SC'),
                         ('88058-512', 'SC'),
                         ('95670-000', 'RS'),
                         ('90560-003', 'RS')])
def test_zip_code_state(zip_code, state):
    zip_code = ZipCode(zip_code)
    assert zip_code.state == state


@pytest.mark.parametrize('zip_code, region', [
                         ('13560060', 'INTERIOR'),
                         ('04547-003', 'CAPITAL'),
                         ('28921-100', 'INTERIOR'),
                         ('22440-033', 'CAPITAL'),
                         ('29213-360', 'INTERIOR'),
                         ('29048-495', 'CAPITAL'),
                         ('35900-457', 'INTERIOR'),
                         ('30190-060', 'CAPITAL'),
                         ('42800-040', 'INTERIOR'),
                         ('40015-170', 'CAPITAL'),
                         ('49500-000', 'INTERIOR'),
                         ('49037-580', 'CAPITAL'),
                         ('57820-000', 'INTERIOR'),
                         ('57032-901', 'CAPITAL'),
                         ('53370-255', 'INTERIOR'),
                         ('50030-150', 'CAPITAL'),
                         ('58400-355', 'INTERIOR'),
                         ('58051-900', 'CAPITAL'),
                         ('59580-000', 'INTERIOR'),
                         ('59015-900', 'CAPITAL'),
                         ('64260-000', 'INTERIOR'),
                         ('64046-902', 'CAPITAL'),
                         ('62598-973', 'INTERIOR'),
                         ('60060-440', 'CAPITAL'),
                         ('65268-000', 'INTERIOR'),
                         ('65056-480', 'CAPITAL'),
                         ('68040-090', 'INTERIOR'),
                         ('66115-970', 'CAPITAL'),
                         ('68925-000', 'INTERIOR'),
                         ('68908-119', 'CAPITAL'),
                         ('69340-000', 'INTERIOR'),
                         ('69310-000', 'CAPITAL'),
                         ('69400-000', 'INTERIOR'),
                         ('69041-000', 'CAPITAL'),
                         ('69928-000', 'INTERIOR'),
                         ('69918-093', 'CAPITAL'),
                         ('76907-438', 'INTERIOR'),
                         ('76803-970', 'CAPITAL'),
                         ('77600-000', 'INTERIOR'),
                         ('77061-900', 'CAPITAL'),
                         ('76400-000', 'INTERIOR'),
                         ('74810-907', 'CAPITAL'),
                         ('73010-521', 'CAPITAL'),
                         ('70150-000', 'CAPITAL'),
                         ('78200-000', 'INTERIOR'),
                         ('78030-210', 'CAPITAL'),
                         ('79730-000', 'INTERIOR'),
                         ('79101-901', 'CAPITAL'),
                         ('83203-100', 'INTERIOR'),
                         ('80730-000', 'CAPITAL'),
                         ('88330-000', 'INTERIOR'),
                         ('88058-512', 'CAPITAL'),
                         ('95670-000', 'INTERIOR'),
                         ('90560-003', 'CAPITAL')])
def test_zip_code_region(zip_code, region):
    zip_code = ZipCode(zip_code)
    assert zip_code.region == region


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
    assert address.basic_address == "Rua Dos Bobos, 5 - Apto. 3, Centro"


def test_basic_address_only_mandatory_args():
    address = Address(
        name="JOHN DOE",
        street="Rua dos Bobos",
        number="0",
        city="Vinicius de Moraes",
        state="RJ",
        zip_code="12345-678",
    )

    assert address.name == "JOHN DOE"
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
    assert address.basic_address == "Rua Dos Bobos, 0"
    assert address.label_name == "John Doe"


def test_basic_address_with_neighborhood():
    address = Address(
        name="John Doe",
        street="Rua dos Bobos",
        number="5",
        city="Vinicius de Moraes",
        state="RJ",
        zip_code="12345-678",
        neighborhood="Vila Nau",
        complement="ap 5",
    )

    assert address.basic_address == "Rua Dos Bobos, 5 - Ap 5, Vila Nau"


def test_basic_address_with_neighborhood_without_complement():
    address = Address(
        name="John Doe",
        street="Rua dos Bobos",
        number="5",
        city="Vinicius de Moraes",
        state="RJ",
        zip_code="12345-678",
        neighborhood="Vila Nau",
    )

    assert address.basic_address == "Rua Dos Bobos, 5, Vila Nau"


@pytest.mark.parametrize("raw,filtered,number,zip_complement", (
    ('1234', '1234', '1234', '1234'),
    ('123B', '123', '123', '123'),
    ('km 5', '5', '5', '5'),
    ('s/n', '', 'S/N', '0'),
    ('S/N', '', 'S/N', '0'),
))
def test_address_number_handling(raw, filtered, number, zip_complement):
    address = Address(
        name="John Doe", street="Rua dos Bobos", city="Vinicius de Moraes", state="RJ", zip_code="12345-678",
        number=raw,
    )
    assert address.filtered_number == filtered
    assert address.number == number
    assert address.zip_complement == zip_complement


def test_address_label_address():
    address = Address(
        name="John Doe",
        street="RUA dos Bobos",
        number="1234",
        city="Vinicius de Moraes",
        state="RJ",
        zip_code="12345-678",
        neighborhood="VILA Vileza",
        complement="AP 01",
    )

    with warnings.catch_warnings(record=True) as captured_warnings:
        warnings.simplefilter("always")

        assert "Rua" in address.label_address
        assert "Vila" in address.label_address
        assert "1234" in address.label_address
        assert "Ap 01" in address.label_address

        assert len(captured_warnings) == 4
        assert all(w.category == DeprecationWarning for w in captured_warnings)
        assert all("deprecated" in str(w.message) for w in captured_warnings)


@pytest.mark.parametrize('address_class', (ReceiverAddress, SenderAddress))
def test_custom_address_label_address(address_class):
    address = address_class(
        name="John Doe",
        street="RUA dos Bobos",
        number="1234",
        city="Vinicius de Moraes",
        state="RJ",
        zip_code="12345-678",
        neighborhood="VILA Vileza",
        complement="AP 01",
    )

    assert '<br/>' in address.label_address
    assert 'Rua' in address.label_address
    assert 'Vila' in address.label_address
    assert '1234' in address.label_address
    assert 'Ap 01' in address.label_address


@pytest.mark.parametrize('address_class', (ReceiverAddress, SenderAddress))
def test_custom_address_label_address_long_street_name(address_class):
    address = address_class(
        name="John Doe",
        street="RUA Professor José Caetano dos Santos Mascarenhas",
        number="1234",
        city="Vinicius de Moraes",
        state="RJ",
        zip_code="12345-678",
        neighborhood="VILA Vileza",
        complement="AP 01",
    )

    assert '<br/>' not in address.label_address
    assert 'Rua' in address.label_address
    assert 'Vila' in address.label_address
    assert '1234' in address.label_address
    assert 'Ap 01' in address.label_address
