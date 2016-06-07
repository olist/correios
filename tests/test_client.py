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


from correios.client import Correios
from correios.models.address import ZipCode
from .vcr import vcr


@vcr.use_cassette
def test_basic_client():
    client = Correios(username="foo", password="bar", environment='test')
    assert client.url == "https://apphom.correios.com.br/SigepMasterJPA/AtendeClienteService/AtendeCliente?wsdl"
    assert not client.verify
    assert client.username == "foo"
    assert client.password == "bar"


# TODO
# def test_verify_service_availability():
#     client = Correios(username="sigep", password="n5f9t8", environment="test")
#     status = client.verify_service_availability(user)


@vcr.use_cassette
def test_get_info():
    client = Correios(username="foo", password="bar", environment="test")
    user = client.get_user(contract="9912208555", card="0057018901")

    assert user.name == "ECT"
    assert user.federal_tax_number == "34028316000103"
    assert user.state_tax_number == "0733382100116"
    assert user.status_number == 1
    assert len(user.contracts) == 1

    contract = user.contracts[0]
    assert len(contract.posting_cards) == 1


@vcr.use_cassette
def test_find_zip_code():
    client = Correios(username="sigep", password="n5f9t8", environment="test")
    zip_address = client.find_zipcode(ZipCode("70002-900"))

    assert zip_address.id == 0
    assert zip_address.zip_code == "70002900"
    assert zip_address.state == "DF"
    assert zip_address.city == "Brasília"
    assert zip_address.district == "Asa Norte"
    assert zip_address.address == "SBN Quadra 1 Bloco A"
    assert zip_address.complements == []
