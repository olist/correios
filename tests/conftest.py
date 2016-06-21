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


from datetime import datetime, timedelta

import pytest

from correios.client import Correios
from correios.models.user import FederalTaxNumber, StateTaxNumber, Contract, PostingCard, User


@pytest.fixture
def valid_federal_tax_number():
    return FederalTaxNumber("73.119.555/0001-20")


@pytest.fixture
def valid_state_tax_number():
    return StateTaxNumber("73.119.555/0001-20")


@pytest.fixture
def datetime_object():
    return datetime(1970, 4, 1)


@pytest.fixture
def default_user():
    return User(name="ECT", federal_tax_number="34028316000103", state_tax_number="0733382100116", status_number=1)


# noinspection PyShadowingNames
@pytest.fixture
def default_contract(datetime_object):
    contract = Contract(
        number=9912208555,
        customer_code=279311,
        direction_code=10,
        direction="DR - BRASÍLIA",
        status_code="A",
        start_date=datetime_object,
        end_date=datetime_object + timedelta(days=5),
        posting_cards=[]
    )
    return contract


# noinspection PyShadowingNames
@pytest.fixture
def default_posting_card(default_contract, datetime_object):
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

    return posting_card


@pytest.fixture
def default_test_client():
    return Correios(username="sigep", password="n5f9t8", environment=Correios.TEST)
