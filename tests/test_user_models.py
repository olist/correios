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


import os
from datetime import timedelta, datetime, timezone

import pytest

from correios import DATADIR
from correios.exceptions import InvalidFederalTaxNumberException, InvalidExtraServiceException
from correios.models.data import EXTRA_SERVICE_AR, EXTRA_SERVICE_MP, EXTRA_SERVICE_VD, EXTRA_SERVICE_RN
from correios.models.user import FederalTaxNumber, StateTaxNumber, User, Contract, PostingCard, Service, ExtraService


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
    with pytest.raises(InvalidFederalTaxNumberException):
        FederalTaxNumber("1234567890123")

    with pytest.raises(InvalidFederalTaxNumberException):
        FederalTaxNumber("123456789012345")

    with pytest.raises(InvalidFederalTaxNumberException):
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
    user = User(name="ECT",
                federal_tax_number=valid_federal_tax_number,
                state_tax_number=valid_state_tax_number,
                status_number=1,
                contracts=[])

    assert user.name == "ECT"
    assert user.federal_tax_number == "73119555000120"
    assert user.status_number == 1
    assert user.contracts == []


def test_sanitize_user_data(valid_federal_tax_number, valid_state_tax_number):
    user = User(name="    NAME WITH TRAILLING WHITESPACES      ",
                federal_tax_number=valid_federal_tax_number,
                state_tax_number=valid_state_tax_number,
                status_number="1  ",
                contracts=[])

    assert user.name == "NAME WITH TRAILLING WHITESPACES"
    assert user.status_number == 1


def test_basic_contract(datetime_object):
    contract = Contract(
        number=9912208555,
        customer_code=279311,
        direction_code=10,
        direction="DR - BRASÍLIA",
        status_code="A",
        start_date=datetime_object,
        end_date=datetime_object + timedelta(days=5),
    )

    assert contract.number == 9912208555
    assert contract.customer_code == 279311
    assert contract.direction_code == 10
    assert contract.direction == "DR - BRASÍLIA"
    assert contract.status_code == "A"
    assert contract.start_date == datetime_object
    assert contract.end_date == datetime_object + timedelta(days=5)
    assert contract.posting_cards == []


def test_sanitize_contract_data():
    contract = Contract(
        number="9912208555  ",
        customer_code=279311,
        direction_code="   10",
        direction="DR - BRASÍLIA                 ",
        status_code="A",
        start_date="2014-05-09 00:00:00-03:00",
        end_date="2018-05-16 00:00:00-03:00",
    )
    assert contract.number == 9912208555
    assert contract.direction_code == 10
    assert contract.direction == "DR - BRASÍLIA"
    assert contract.start_date == datetime(year=2014, month=5, day=9, tzinfo=timezone(timedelta(hours=-3)))
    assert contract.end_date == datetime(year=2018, month=5, day=16, tzinfo=timezone(timedelta(hours=-3)))


def test_basic_posting_card(default_contract, datetime_object):
    posting_card = PostingCard(
        contract=default_contract,
        number=57018901,
        administrative_code=8082650,
        start_date=datetime_object,
        end_date=datetime_object + timedelta(days=5),
        status=1,
        status_code="I",
        unit=8,
    )

    assert posting_card.number == "0057018901"
    assert posting_card.administrative_code == "08082650"
    assert posting_card.start_date == datetime_object
    assert posting_card.end_date == datetime_object + timedelta(days=5)
    assert posting_card.status == 1
    assert posting_card.status_code == "I"
    assert posting_card.unit == 8


def test_sanitize_posting_card_data(default_contract):
    posting_card = PostingCard(
        contract=default_contract,
        number="0057018901",
        administrative_code=8082650,
        start_date="2014-05-09 00:00:00-03:00",
        end_date="2018-05-16 00:00:00-03:00",
        status="01",
        status_code="I",
        unit="08        ",
    )

    assert posting_card.number == "0057018901"
    assert posting_card.administrative_code == "08082650"
    assert posting_card.start_date == datetime(year=2014, month=5, day=9, tzinfo=timezone(timedelta(hours=-3)))
    assert posting_card.end_date == datetime(year=2018, month=5, day=16, tzinfo=timezone(timedelta(hours=-3)))
    assert posting_card.status == 1
    assert posting_card.status_code == "I"
    assert posting_card.unit == 8


def test_basic_service(datetime_object):
    service = Service(
        id=104707,
        code=40215,
        display_name="SEDEX 10",
        description="SEDEX 10",
        category="SERVICO_COM_RESTRICAO",
        postal_code=244,
        start_date=datetime_object,
        end_date=datetime_object + timedelta(days=5),
        symbol="premium",
    )

    assert service.id == 104707
    assert service.code == 40215
    assert service.display_name == "SEDEX 10"
    assert service.description == "SEDEX 10"
    assert service.category == "SERVICO_COM_RESTRICAO"
    assert service.postal_code == 244
    assert service.start_date == datetime_object
    assert service.end_date == datetime_object + timedelta(days=5)
    assert service.get_symbol_filename() == os.path.join(DATADIR, "premium.gif")
    assert service.get_symbol_filename("png") == os.path.join(DATADIR, "premium.png")


def test_sanitize_service():
    service = Service(
        id=104707,
        code="40215                    ",
        description="SEDEX 10                      ",
        category="SERVICO_COM_RESTRICAO",
        postal_code="244",
        start_date="2014-05-09 00:00:00-03:00",
        end_date="2018-05-16 00:00:00-03:00",
    )

    assert service.id == 104707
    assert service.code == 40215
    assert service.description == "SEDEX 10"
    assert service.category == "SERVICO_COM_RESTRICAO"
    assert service.postal_code == 244
    assert service.start_date == datetime(year=2014, month=5, day=9, tzinfo=timezone(timedelta(hours=-3)))
    assert service.end_date == datetime(year=2018, month=5, day=16, tzinfo=timezone(timedelta(hours=-3)))


def test_basic_extra_service():
    extra_service = ExtraService(1, "AR", "Aviso de Recebimento")
    assert extra_service.number == 1
    assert extra_service.code == "AR"
    assert extra_service.name == "Aviso de Recebimento"
    assert repr(extra_service) == "<ExtraService number=1, code='AR'>"


def test_extra_service_sanitize_code():
    extra_service = ExtraService(1, "ar", "Aviso de Recebimento")
    assert extra_service.code == "AR"


@pytest.mark.parametrize("number,code,name", (
        (0, "XY", "Invalid Number"),
        (1, "XYZ", "Invalid Code"),
        (1, "XY", ""),  # Invalid Name
))
def test_fail_extra_service_invalid_data(number, code, name):
    with pytest.raises(InvalidExtraServiceException):
        ExtraService(number, code, name)


def test_fail_get_unknown_service():
    with pytest.raises(InvalidExtraServiceException):
        ExtraService.get("00")


@pytest.mark.parametrize("number_or_code,extra_service", (
        (1, EXTRA_SERVICE_AR),
        (2, EXTRA_SERVICE_MP),
        (19, EXTRA_SERVICE_VD),
        (25, EXTRA_SERVICE_RN),
        ("AR", EXTRA_SERVICE_AR),
        ("MP", EXTRA_SERVICE_MP),
        ("VD", EXTRA_SERVICE_VD),
        ("RN", EXTRA_SERVICE_RN),
        (EXTRA_SERVICE_AR, EXTRA_SERVICE_AR),
))
def test_extra_service_getter(number_or_code, extra_service):
    assert ExtraService.get(number_or_code) == extra_service
