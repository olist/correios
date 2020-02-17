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


from datetime import datetime, timedelta, timezone
from decimal import Decimal

import pytest
from PIL.Image import Image

from correios.exceptions import (
    InvalidExtraServiceError,
    InvalidFederalTaxNumberError,
    InvalidRegionalDirectionError,
    InvalidServiceDeclaredValue,
    InvalidUserContractError,
    MaximumDeclaredValueError,
    MinimumDeclaredValueError,
)
from correios.models.data import (
    EXTRA_SERVICE_AR,
    EXTRA_SERVICE_MP,
    EXTRA_SERVICE_RR,
    EXTRA_SERVICE_VD_PAC,
    EXTRA_SERVICE_VD_PAC_MINI,
    EXTRA_SERVICE_VD_SEDEX,
    SERVICE_PAC,
    SERVICE_SEDEX,
)
from correios.models.user import (
    Contract,
    ExtraService,
    FederalTaxNumber,
    PostingCard,
    RegionalDirection,
    Service,
    StateTaxNumber,
    User,
)


def test_basic_federal_tax_number_tax_number():
    federal_tax_number = FederalTaxNumber("73119555000120")
    assert federal_tax_number.number == "73119555000120"


def test_sanitize_federal_tax_number_tax_number():
    federal_tax_number = FederalTaxNumber("73.119.555/0001-20")
    assert federal_tax_number.number == "73119555000120"


def test_compare_federal_tax_number_with_string():
    federal_tax_number = FederalTaxNumber("73.119.555/0001-20")
    assert federal_tax_number == "73.119.555/0001-20"
    assert federal_tax_number == "73119555000120"


def test_fail_invalid_federal_tax_number():
    with pytest.raises(InvalidFederalTaxNumberError):
        FederalTaxNumber("1234567890123")

    with pytest.raises(InvalidFederalTaxNumberError):
        FederalTaxNumber("123456789012345")

    with pytest.raises(InvalidFederalTaxNumberError):
        FederalTaxNumber("73119555000199")  # invalid verification digit


def test_convert_federal_tax_number_to_str():
    assert str(FederalTaxNumber("73.119.555/0001-20")) == "73119555000120"


def test_federal_tax_number_repr():
    assert repr(FederalTaxNumber("73.119.555/0001-20")) == "<FederalTaxNumber number: 73119555000120>"


def test_federal_tax_number_display():
    assert FederalTaxNumber("73119555000120").display() == "73.119.555/0001-20"


def test_basic_state_tax_number_tax_number():
    state_tax_number = StateTaxNumber("733382100116")
    assert state_tax_number.number == "733382100116"


def test_sanitize_state_tax_number_tax_number():
    state_tax_number = StateTaxNumber("733.382.100.116")
    assert state_tax_number.number == "733382100116"


def test_convert_state_tax_number_to_str():
    assert str(StateTaxNumber("733382100116")) == "733382100116"


def test_convert_state_tax_number_display():
    assert StateTaxNumber("733382100116").display() == "733382100116"


def test_state_tax_number_repr():
    assert repr(StateTaxNumber("733.382.100.116")) == "<StateTaxNumber number: 733382100116>"


def test_basic_user(valid_federal_tax_number, valid_state_tax_number):
    user = User(
        name="ECT",
        federal_tax_number=valid_federal_tax_number,
        state_tax_number=valid_state_tax_number,
        status_number=1,
    )

    assert user.name == "ECT"
    assert user.federal_tax_number == "73119555000120"
    assert user.status_number == 1
    assert user.contracts == []


def test_sanitize_user_data(valid_federal_tax_number, valid_state_tax_number):
    user = User(
        name="    NAME WITH TRAILLING WHITESPACES      ",
        federal_tax_number=valid_federal_tax_number,
        state_tax_number=valid_state_tax_number,
        status_number="1  ",
    )

    assert user.name == "NAME WITH TRAILLING WHITESPACES"
    assert user.status_number == 1


def test_fail_add_contract_twice(contract, valid_federal_tax_number, valid_state_tax_number):
    user = User(
        name="ECT",
        federal_tax_number=valid_federal_tax_number,
        state_tax_number=valid_state_tax_number,
        status_number=1,
    )
    user.add_contract(contract)

    with pytest.raises(InvalidUserContractError):
        user.add_contract(contract)


def test_basic_contract(user):
    contract = Contract(user=user, number=9911222777, regional_direction=10)

    assert contract.number == 9911222777
    assert contract.regional_direction.number == 10
    assert contract.posting_cards == []
    assert str(contract) == "9911222777"
    assert repr(contract) == "<Contract number=9911222777>"


def test_sanitize_contract_data(user):
    contract = Contract(user=user, number="9911222777  ", regional_direction="   10")
    contract.customer_code = "279311"
    contract.status_code = "A"
    contract.start_date = "2014-05-09 00:00:00-03:00"
    contract.end_date = "2018-05-16 00:00:00-03:00"

    assert contract.number == 9911222777
    assert contract.regional_direction.number == 10
    assert contract.customer_code == 279311
    assert contract.status_code == "A"
    assert contract.start_date == datetime(2014, 5, 9, 0, 0, tzinfo=timezone(timedelta(hours=-3)))
    assert contract.end_date == datetime(2018, 5, 16, 0, 0, tzinfo=timezone(timedelta(hours=-3)))


def test_basic_posting_card(contract):
    posting_card = PostingCard(contract=contract, number=56789123, administrative_code=8888888)

    assert posting_card.number == "0056789123"
    assert posting_card.administrative_code == "08888888"
    assert posting_card.get_contract_number() == 9911222777
    assert str(posting_card) == "0056789123"
    assert repr(posting_card) == "<PostingCard number='0056789123', contract=9911222777>"


def test_sanitize_posting_card_data(contract):
    posting_card = PostingCard(contract=contract, number="0056789123", administrative_code=8888888)
    posting_card.start_date = "2014-05-09 00:00:00-03:00"
    posting_card.end_date = "2018-05-16 00:00:00-03:00"
    posting_card.status = "01"
    posting_card.status_code = "I"
    posting_card.unit = "08        "

    assert posting_card.number == "0056789123"
    assert posting_card.administrative_code == "08888888"
    assert posting_card.start_date == datetime(2014, 5, 9, 0, 0, tzinfo=timezone(timedelta(hours=-3)))
    assert posting_card.end_date == datetime(2018, 5, 16, 0, 0, tzinfo=timezone(timedelta(hours=-3)))
    assert posting_card.status == 1
    assert posting_card.status_code == "I"
    assert posting_card.unit == 8


def test_basic_service():
    service = Service(
        code=40215,
        id=104707,
        description="SEDEX 10",
        category="SERVICO_COM_RESTRICAO",
        symbol="premium",
        max_weight=10000,
    )

    assert service.id == 104707
    assert service.code == "40215"
    assert service.display_name == "SEDEX 10"
    assert service.description == "SEDEX 10"
    assert service.category == "SERVICO_COM_RESTRICAO"
    assert service.get_symbol_filename().endswith("/premium.gif")
    assert service.get_symbol_filename("png").endswith("/premium.png")
    assert isinstance(service.symbol_image, Image)
    assert service.max_weight == 10000


def test_sanitize_service():
    service = Service(
        code="40215                    ",
        id=104707,
        description="SEDEX 10                      ",
        category="SERVICO_COM_RESTRICAO",
    )

    assert service.id == 104707
    assert service.code == "40215"
    assert service.description == "SEDEX 10"
    assert service.category == "SERVICO_COM_RESTRICAO"


def test_service_getter():
    service = Service.get(40215)
    assert service.id == 104707
    assert service.code == "40215"
    assert service.description == "SEDEX 10"
    assert service.category == "SERVICO_COM_RESTRICAO"
    assert Service.get(service) == service


def test_fail_invalid_declared_value_in_sedex():
    service = Service.get(SERVICE_SEDEX)
    with pytest.raises(MaximumDeclaredValueError):
        service.validate_declared_value(service.max_declared_value + 1)

    with pytest.raises(MinimumDeclaredValueError):
        service.validate_declared_value(service.min_declared_value - 1)


@pytest.mark.parametrize("insurance_code", [EXTRA_SERVICE_VD_SEDEX, EXTRA_SERVICE_VD_PAC, EXTRA_SERVICE_VD_PAC_MINI])
def test_fail_invalid_insurance_declared_value(insurance_code):
    service = Service.get(SERVICE_PAC)
    with pytest.raises(InvalidServiceDeclaredValue):
        service.validate_insurance_declared_value(Decimal("0.00"), insurance_code)


@pytest.mark.parametrize("insurance_code", [EXTRA_SERVICE_VD_SEDEX, EXTRA_SERVICE_VD_PAC, EXTRA_SERVICE_VD_PAC_MINI])
def test_valid_insurance_declared_value(insurance_code):
    service = Service.get(SERVICE_PAC)
    assert service.validate_insurance_declared_value(Decimal("10.00"), insurance_code) is True


@pytest.mark.parametrize("insurance_code", [EXTRA_SERVICE_RR, EXTRA_SERVICE_AR, EXTRA_SERVICE_MP])
def test_fail_invalid_insurance_code(insurance_code):
    service = Service.get(SERVICE_PAC)
    with pytest.raises(InvalidServiceDeclaredValue):
        service.validate_insurance_declared_value(Decimal("10.00"), insurance_code)


@pytest.mark.parametrize("insurance_code", [EXTRA_SERVICE_RR, EXTRA_SERVICE_AR, EXTRA_SERVICE_MP])
def test_valid_insurance_code(insurance_code):
    service = Service.get(SERVICE_PAC)
    assert service.validate_insurance_declared_value(Decimal("0.00"), insurance_code) is True


def test_fail_invalid_declared_value_in_pac():
    service = Service.get(SERVICE_PAC)
    with pytest.raises(MaximumDeclaredValueError):
        service.validate_declared_value(service.max_declared_value + 1)

    with pytest.raises(MinimumDeclaredValueError):
        service.validate_declared_value(service.min_declared_value - 1)


def test_basic_extra_service():
    extra_service = ExtraService(1, "AR", "Aviso de Recebimento")
    assert extra_service.number == 1
    assert extra_service.code == "AR"
    assert extra_service.name == "Aviso de Recebimento"
    assert extra_service.display_on_label is True
    assert repr(extra_service) == "<ExtraService number=1, code='AR'>"
    assert extra_service == 1


def test_extra_service_sanitize_code():
    extra_service = ExtraService(1, "ar", "Aviso de Recebimento")
    assert extra_service.code == "AR"


@pytest.mark.parametrize(
    "number,code,name",
    ((0, "XY", "Invalid Number"), (1, "XYZ", "Invalid Code"), (1, "", "Invalid Code"), (1, "XY", "")),  # Invalid Name
)
def test_fail_extra_service_invalid_data(number, code, name):
    with pytest.raises(InvalidExtraServiceError):
        ExtraService(number, code, name)


def test_fail_get_unknown_service():
    with pytest.raises(KeyError):
        ExtraService.get(0)


@pytest.mark.parametrize(
    "number,extra_service_code",
    ((1, "AR"), (2, "MP"), (25, "RR"), (19, "VD"), (64, "VD"), (65, "VD"), (ExtraService.get(EXTRA_SERVICE_AR), "AR")),
)
def test_extra_service_getter(number, extra_service_code):
    assert ExtraService.get(number).code == extra_service_code


@pytest.mark.parametrize(
    "number,code,description,is_declared_value",
    (
        (19, "VD", "Valor Declarado (Encomendas)", True),
        (64, "VD", "Valor Declarado (Encomendas)", True),
        (65, "VD", "Valor Declarado (Encomendas)", True),
        (1, "AR", "Aviso de Recebimento", False),
        (25, "RR", "Registro Nacional", False),
    ),
)
def test_extra_service_is_declared_value(number, code, description, is_declared_value):
    extra_service = ExtraService(number, code, description)
    assert extra_service.is_declared_value() == is_declared_value


def test_basic_regional_direction():
    regional_direction = RegionalDirection(1, "AC", "AC - ADMINISTRAÇAO CENTRAL")
    assert regional_direction.number == 1
    assert regional_direction.code == "AC"
    assert regional_direction.name == "AC - ADMINISTRAÇAO CENTRAL"
    assert repr(regional_direction) == "<RegionalDirection number=1, code='AC'>"


def test_regional_direction_sanitize_code():
    regional_direction = RegionalDirection(1, "ac", "AC - ADMINISTRAÇAO CENTRAL")
    assert regional_direction.code == "AC"


@pytest.mark.parametrize(
    "number,code,name", ((0, "XY", "Invalid Number"), (1, "", "Invalid Code"), (1, "XY", ""))  # Invalid Name
)
def test_fail_regional_direction_invalid_data(number, code, name):
    with pytest.raises(InvalidRegionalDirectionError):
        RegionalDirection(number, code, name)


def test_fail_get_unknown_regional_direction():
    with pytest.raises(KeyError):
        RegionalDirection.get(0)


def test_regional_direction_getter():
    regional_direction = RegionalDirection.get(1)
    assert regional_direction.number == 1
    assert regional_direction.code == "AC"
    assert regional_direction.name == "AC - ADMINISTRAÇAO CENTRAL"
    assert RegionalDirection.get(regional_direction) == regional_direction
