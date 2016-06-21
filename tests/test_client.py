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


from correios.client import ModelBuilder, Correios
from correios.models.address import ZipCode
from correios.models.services import SERVICE_SEDEX10, SERVICE_SEDEX
from correios.models.user import PostingCard
from .vcr import vcr


@vcr.use_cassette
def test_basic_client():
    client = Correios(username="sigep", password="n5f9t8", environment=Correios.TEST)
    assert client.url == "https://apphom.correios.com.br/SigepMasterJPA/AtendeClienteService/AtendeCliente?wsdl"
    assert not client.verify
    assert client.username == "sigep"
    assert client.password == "n5f9t8"


@vcr.use_cassette
def test_get_user():
    client = Correios(username="sigep", password="n5f9t8", environment=Correios.TEST)
    user = client.get_user(contract="9912208555", posting_card="0057018901")

    assert user.name == "ECT"
    assert user.federal_tax_number == "34028316000103"
    assert user.state_tax_number == "0733382100116"
    assert user.status_number == 1
    assert len(user.contracts) == 1

    contract = user.contracts[0]
    assert len(contract.posting_cards) == 1


@vcr.use_cassette
def test_find_zip_code():
    client = Correios(username="sigep", password="n5f9t8", environment=Correios.TEST)
    zip_address = client.find_zipcode(ZipCode("70002-900"))

    assert zip_address.id == 0
    assert zip_address.zip_code == "70002900"
    assert zip_address.state == "DF"
    assert zip_address.city == "Brasília"
    assert zip_address.district == "Asa Norte"
    assert zip_address.address == "SBN Quadra 1 Bloco A"
    assert zip_address.complements == []


@vcr.use_cassette
def test_verify_service_availability(default_posting_card):
    client = Correios(username="sigep", password="n5f9t8", environment=Correios.TEST)
    status = client.verify_service_availability(default_posting_card, SERVICE_SEDEX10, "82940150", "01310000")
    assert status


@vcr.use_cassette
def test_get_posting_card_status(default_posting_card):
    client = Correios(username="sigep", password="n5f9t8", environment=Correios.TEST)
    status = client.get_posting_card_status(default_posting_card)
    assert status == PostingCard.ACTIVE


@vcr.use_cassette
def test_request_tracking_codes(default_user):
    client = Correios(username="sigep", password="n4f9t8", environment=Correios.TEST)
    result = client.request_tracking_codes(default_user, SERVICE_SEDEX)
    assert len(result) == 2
    assert len(result[0].code) == 13
    assert len(result[1].code) == 13


def test_builder_posting_card_status():
    builder = ModelBuilder()
    assert builder.build_posting_card_status("Normal") == PostingCard.ACTIVE
    assert builder.build_posting_card_status("Cancelado") == PostingCard.CANCELLED
