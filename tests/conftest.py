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


import random
from datetime import datetime, timedelta

import factory
import pytest
from pytest_factoryboy import register

from correios.models import data
from correios.models.address import Address
from correios.models.data import TRACKING_PREFIX
from correios.models.posting import TrackingCode, ShippingLabel, PostingList
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


class ContractFactory(factory.Factory):
    class Meta:
        model = Contract

    number = 9912208555
    customer_code = 279311
    regional_direction = 10
    status_code = "A"
    start_date = factory.LazyFunction(datetime.utcnow)
    end_date = factory.LazyAttribute(lambda o: o.start_date + timedelta(days=5))
    posting_cards = []


register(ContractFactory, "contract")


class PostingCardFactory(factory.Factory):
    class Meta:
        model = PostingCard

    contract = factory.SubFactory(ContractFactory)
    number = 57018901
    administrative_code = 8082650
    start_date = factory.LazyFunction(datetime.utcnow)
    end_date = factory.LazyAttribute(lambda o: o.start_date + timedelta(days=5))
    status = 1
    status_code = "I"
    unit = 8


register(PostingCardFactory, "posting_card")


def _random_tracking_code():
    prefix = random.choice(list(TRACKING_PREFIX.keys()))
    number = "".join(str(random.randrange(0, 10)) for _ in range(8))
    return "{}{} BR".format(prefix, number)


class TrackingCodeFactory(factory.Factory):
    class Meta:
        model = TrackingCode

    code = factory.LazyFunction(_random_tracking_code)


register(TrackingCodeFactory, "tracking_code")


class AddressFactory(factory.Factory):
    class Meta:
        model = Address

    name = factory.Faker("name", locale="pt_BR")
    street = factory.Faker("street_name", locale="pt_BR")
    number = factory.Faker("building_number", locale="pt_BR")
    city = factory.Faker("city", locale="pt_BR")
    state = factory.Faker("estado_sigla", locale="pt_BR")
    zip_code = factory.Faker("postcode", locale="pt_BR")
    complement = factory.Faker("secondary_address")
    neighborhood = factory.Sequence(lambda n: "Neighborhood #{}".format(n))
    phone = factory.Faker("phone_number", locale="pt_BR")
    cellphone = factory.Faker("phone_number", locale="pt_BR")
    email = factory.Faker("email")
    latitude = factory.Faker("latitude", locale="pt_BR")
    longitude = factory.Faker("longitude", locale="pt_BR")


register(AddressFactory, "address")
register(AddressFactory, "sender_address")
register(AddressFactory, "receiver_address")

_services = [
    data.SERVICE_PAC,
    data.SERVICE_SEDEX,
    data.SERVICE_SEDEX10,
    data.SERVICE_SEDEX12,
]


class ShippingLabelFactory(factory.Factory):
    class Meta:
        model = ShippingLabel

    posting_card = factory.SubFactory(PostingCardFactory)
    sender = factory.LazyFunction(AddressFactory.build)
    receiver = factory.LazyFunction(AddressFactory.build)
    service = factory.LazyFunction(lambda: random.choice(_services))
    tracking_code = factory.SubFactory(TrackingCodeFactory)
    volume_type = ShippingLabel.TYPE_PACKAGE
    width = factory.LazyFunction(lambda: random.randint(11, 30))
    height = factory.LazyFunction(lambda: random.randint(2, 30))
    length = factory.LazyFunction(lambda: random.randint(16, 30))
    weight = factory.LazyFunction(lambda: random.randint(1, 150) * 100)
    invoice_number = factory.LazyFunction(lambda: "{!s:>04}".format(random.randint(1234, 9999)))
    order = factory.LazyFunction(lambda: "OLT123ABC{!s:>03}".format(random.randint(1, 999)))
    text = factory.Faker("text", max_nb_chars=100)
    latitude = 0.0
    longitude = 0.0


register(ShippingLabelFactory, "shipping_label")


class PostingListFactory(factory.Factory):
    class Meta:
        model = PostingList

    id_ = factory.Sequence(lambda n: n)


register(PostingListFactory, "posting_list")
