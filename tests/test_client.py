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

from correios.client import ModelBuilder, Correios, PostingListSerializer
from correios.exceptions import PostingListSerializerError, TrackingCodesLimitExceededError
from correios.models.address import ZipCode
from correios.models.data import SERVICE_SEDEX10, SERVICE_SEDEX, EXTRA_SERVICE_VD
from correios.models.posting import (NotFoundTrackingEvent, PostingList, ShippingLabel,
                                     TrackingCode)
from correios.models.user import PostingCard, Service, ExtraService
from .vcr import vcr


@vcr.use_cassette
def test_basic_client():
    client = Correios(username="sigep", password="n5f9t8", environment=Correios.TEST)
    assert client.sigep_url == "https://apphom.correios.com.br/SigepMasterJPA/AtendeClienteService/AtendeCliente?wsdl"
    assert not client.sigep_verify
    assert client.username == "sigep"
    assert client.password == "n5f9t8"


@vcr.use_cassette
def test_get_user():
    client = Correios(username="sigep", password="n5f9t8", environment=Correios.TEST)
    user = client.get_user(contract_number="9912208555", posting_card_number="0057018901")

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
def test_verify_service_availability(posting_card):
    client = Correios(username="sigep", password="n5f9t8", environment=Correios.TEST)
    status = client.verify_service_availability(posting_card, SERVICE_SEDEX10, "82940150", "01310000")
    assert status


@vcr.use_cassette
def test_get_posting_card_status(posting_card):
    client = Correios(username="sigep", password="n5f9t8", environment=Correios.TEST)
    status = client.get_posting_card_status(posting_card)
    assert status == PostingCard.ACTIVE


@vcr.use_cassette
def test_request_tracking_codes(user):
    client = Correios(username="sigep", password="n5f9t8", environment=Correios.TEST)
    result = client.request_tracking_codes(user, Service.get(SERVICE_SEDEX), quantity=10)
    assert len(result) == 10
    assert len(result[0].code) == 13


@vcr.use_cassette
def test_generate_verification_digit():
    client = Correios(username="sigep", password="n5f9t8", environment=Correios.TEST)
    result = client.generate_verification_digit(["DL74668653 BR"])
    assert result[0] == 6


@vcr.use_cassette
def test_close_posting_list(posting_card, posting_list: PostingList, shipping_label: ShippingLabel):
    shipping_label.posting_card = posting_card
    posting_list.add_shipping_label(shipping_label)
    client = Correios(username="sigep", password="n5f9t8", environment=Correios.TEST)
    posting_list = client.close_posting_list(posting_list, posting_card)
    assert posting_list.number is not None
    assert posting_list.closed


@vcr.use_cassette
def test_get_tracking_codes_events():
    client = Correios(username="sigep", password="n5f9t8", environment=Correios.TEST)
    result = client.get_tracking_code_events(["FJ064849483BR", "DU477828695BR"])

    assert len(result) == 2
    assert result[0] != result[1]

    assert isinstance(result[0], TrackingCode)
    assert result[0].code in ("FJ064849483BR", "DU477828695BR")

    assert isinstance(result[1], TrackingCode)
    assert result[1].code in ("FJ064849483BR", "DU477828695BR")


@vcr.use_cassette
def test_get_tracking_code_events():
    client = Correios(username="sigep", password="n5f9t8", environment=Correios.TEST)
    result = client.get_tracking_code_events("FJ064849483BR")

    assert isinstance(result[0], TrackingCode)
    assert result[0].code == "FJ064849483BR"


@vcr.use_cassette
def test_get_tracking_code_events_withou_city_field():
    client = Correios(username="sigep", password="n5f9t8", environment=Correios.TEST)
    result = client.get_tracking_code_events("PJ651329640BR")

    assert isinstance(result[0], TrackingCode)
    assert result[0].code == "PJ651329640BR"
    assert result[0].events[0].city == ""


@vcr.use_cassette
def test_get_tracking_code_with_no_verification_digitevents():
    client = Correios(username="sigep", password="n5f9t8", environment=Correios.TEST)
    result = client.get_tracking_code_events("FJ06484948BR")

    assert isinstance(result[0], TrackingCode)
    assert result[0].code == "FJ064849483BR"


@vcr.use_cassette
def test_get_tracking_code_object_not_found_by_correios():
    client = Correios(username="sigep", password="n5f9t8", environment=Correios.TEST)
    tracking_code = client.get_tracking_code_events("DU05508759BR")[0]

    assert tracking_code.events

    event = tracking_code.events[0]
    assert isinstance(event, NotFoundTrackingEvent)
    assert event.timestamp
    assert event.status.type == "ERROR"
    assert event.status.status == 1


def test_get_tracking_codes_events_over_limit():
    client = Correios(username="sigep", password="n5f9t8", environment=Correios.TEST)
    codes = ["DU05508759BR"] * 51
    with pytest.raises(TrackingCodesLimitExceededError):
        client.get_tracking_code_events(codes)


def test_builder_posting_card_status():
    builder = ModelBuilder()
    assert builder.build_posting_card_status("Normal") == PostingCard.ACTIVE
    assert builder.build_posting_card_status("Cancelado") == PostingCard.CANCELLED


def test_posting_list_serialization(posting_list, shipping_label):
    posting_list.add_shipping_label(shipping_label)
    serializer = PostingListSerializer()
    document = serializer.get_document(posting_list)
    serializer.validate(document)
    xml = serializer.get_xml(document)
    assert xml.startswith(b'<?xml version="1.0" encoding="ISO-8859-1"?><correioslog>')
    assert b"<codigo_servico_adicional>019</codigo_servico_adicional>" not in xml
    assert b"<valor_declarado>10,29</valor_declarado>" not in xml


def test_declared_value(posting_list, shipping_label):
    shipping_label.extra_services.append(ExtraService.get(EXTRA_SERVICE_VD))
    shipping_label.value = 10.29
    posting_list.add_shipping_label(shipping_label)
    serializer = PostingListSerializer()
    document = serializer.get_document(posting_list)
    serializer.validate(document)
    xml = serializer.get_xml(document)
    assert b"<codigo_servico_adicional>019</codigo_servico_adicional>" in xml
    assert b"<valor_declarado>10,29</valor_declarado>" in xml


def test_fail_empty_posting_list_serialization(posting_list):
    serializer = PostingListSerializer()
    with pytest.raises(PostingListSerializerError):
        serializer.get_document(posting_list)


def test_fail_closed_posting_list_serialization(posting_list: PostingList, shipping_label):
    posting_list.add_shipping_label(shipping_label)
    posting_list.close_with_id(number=12345)

    serializer = PostingListSerializer()
    with pytest.raises(PostingListSerializerError):
        serializer.get_document(posting_list)
