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
from datetime import datetime

import pytest
from factory import Factory, Faker, LazyFunction, Sequence, SubFactory, faker
from pytest_factoryboy import register

from correios.models import data
from correios.models.address import Address, ReceiverAddress, SenderAddress
from correios.models.data import TRACKING_PREFIX
from correios.models.posting import Package, PostingList, ShippingLabel, TrackingCode, TrackingEvent
from correios.models.user import Contract, FederalTaxNumber, PostingCard, StateTaxNumber, User

try:
    from correios import client as correios
except ImportError:
    correios = None


@pytest.fixture
def valid_federal_tax_number():
    return FederalTaxNumber("73.119.555/0001-20")


@pytest.fixture
def valid_state_tax_number():
    return StateTaxNumber("73.119.555/0001-20")


class UserFactory(Factory):
    class Meta:
        model = User

    name = "ECT"
    federal_tax_number = "34028316000103"
    state_tax_number = "0733382100116"
    status_number = 1


register(UserFactory, "user")


class ContractFactory(Factory):
    class Meta:
        model = Contract

    user = SubFactory(UserFactory)
    number = 9911222777
    regional_direction = 10


register(ContractFactory, "contract")


class PostingCardFactory(Factory):
    class Meta:
        model = PostingCard

    contract = SubFactory(ContractFactory)
    number = 56789123
    administrative_code = 8888888


register(PostingCardFactory, "posting_card")


class TrackingEventFactory(Factory):
    class Meta:
        model = TrackingEvent

    timestamp = datetime(2016, 1, 1, 12)
    status = ('PO', '1')
    location_zip_code = "07192-100"
    location = "CEE"
    city = faker.Faker("city", locale="pt_BR")
    state = faker.Faker("estado_sigla", locale="pt_BR")
    description = "Objeto postado"


register(TrackingEventFactory, "tracking_event")


def _random_tracking_code():
    prefix = random.choice(list(TRACKING_PREFIX.keys()))
    number = "".join(str(random.randrange(0, 10)) for _ in range(8))
    return "{}{} BR".format(prefix, number)


class TrackingCodeFactory(Factory):
    class Meta:
        model = TrackingCode

    code = LazyFunction(_random_tracking_code)


register(TrackingCodeFactory, "tracking_code")


class AddressFactory(Factory):
    class Meta:
        model = Address

    name = Faker("name", locale="pt_BR")
    street = Faker("street_name", locale="pt_BR")
    number = Faker("building_number", locale="pt_BR")
    city = Faker("city", locale="pt_BR")
    state = Faker("estado_sigla", locale="pt_BR")
    zip_code = "07192-100"
    complement = Faker("secondary_address")
    neighborhood = Sequence(lambda n: "Neighborhood #{}".format(n))
    phone = Faker("phone_number", locale="pt_BR")
    cellphone = Faker("phone_number", locale="pt_BR")
    email = Faker("email")
    latitude = Faker("latitude", locale="pt_BR")
    longitude = Faker("longitude", locale="pt_BR")


class ReceiverAddressFactory(AddressFactory):
    class Meta:
        model = ReceiverAddress


class SenderAddressFactory(AddressFactory):
    class Meta:
        model = SenderAddress


register(AddressFactory, "address")
register(ReceiverAddressFactory, "receiver_address")
register(SenderAddressFactory, "sender_address")

_services = [
    data.SERVICE_PAC,
    data.SERVICE_SEDEX,
    data.SERVICE_SEDEX10,
    data.SERVICE_SEDEX12,
]


class PackageFactory(Factory):
    class Meta:
        model = Package

    package_type = Package.TYPE_BOX
    width = LazyFunction(lambda: random.randint(11, 30))
    height = LazyFunction(lambda: random.randint(2, 30))
    length = LazyFunction(lambda: random.randint(18, 30))
    weight = LazyFunction(lambda: random.randint(1, 100) * 100)
    service = LazyFunction(lambda: random.choice(_services))
    sequence = Sequence(lambda n: (n, n + 1))


register(PackageFactory, "package")


class ShippingLabelFactory(Factory):
    class Meta:
        model = ShippingLabel

    posting_card = SubFactory(PostingCardFactory)
    sender = LazyFunction(SenderAddressFactory.build)
    receiver = LazyFunction(ReceiverAddressFactory.build)
    service = data.SERVICE_PAC
    tracking_code = SubFactory(TrackingCodeFactory)
    package = SubFactory(PackageFactory)
    invoice_number = LazyFunction(lambda: "{!s:>04}".format(random.randint(1234, 9999)))
    order = LazyFunction(lambda: "OLT123ABC{!s:>03}".format(random.randint(1, 999)))
    text = Faker("text", max_nb_chars=100)
    latitude = 0.0
    longitude = 0.0


register(ShippingLabelFactory, "shipping_label")


class PostingListFactory(Factory):
    class Meta:
        model = PostingList

    custom_id = Sequence(lambda n: n)


register(PostingListFactory, "posting_list")


@pytest.fixture
def client():
    return correios.Correios(username="sigep", password="XXXXXX", environment=correios.Correios.TEST)
