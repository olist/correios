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
from datetime import timedelta

import pytest

from correios.exceptions import InvalidFederalTaxNumber
from correios.models.user import FederalTaxNumber, StateTaxNumber, User, Contract


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
    with pytest.raises(InvalidFederalTaxNumber):
        FederalTaxNumber("1234567890123")

    with pytest.raises(InvalidFederalTaxNumber):
        FederalTaxNumber("123456789012345")

    with pytest.raises(InvalidFederalTaxNumber):
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
        management_code=10,
        management_name="DR - BRASÍLIA",
        status_code="A",
        start_date=datetime_object,
        end_date=datetime_object + timedelta(days=5),
        posting_cards=[]
    )

    assert contract.number == 9912208555
    assert contract.customer_code == 279311
    assert contract.management_code == 10
    assert contract.management_name == "DR - BRASÍLIA"
    assert contract.status_code == "A"
    assert contract.start_date == datetime_object
    assert contract.end_date == datetime_object + timedelta(days=5)
    assert contract.posting_cards == []


def test_sanitize_contract_data(datetime_object):
    contract = Contract(
        number="9912208555  ",
        customer_code=279311,
        management_code="    10",
        management_name="DR - BRASÍLIA                 ",
        status_code="A",
        start_date=datetime_object,
        end_date=datetime_object + timedelta(days=5),
        posting_cards=[]
    )
    assert contract.number == 9912208555
    assert contract.management_code == 10
    assert contract.management_name == "DR - BRASÍLIA"
