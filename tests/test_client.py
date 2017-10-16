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

import pytest

from correios import client as correios
from correios.exceptions import PostingListSerializerError, TrackingCodesLimitExceededError
from correios.models.address import ZipCode
from correios.models.data import (
    EXTRA_SERVICE_AR,
    EXTRA_SERVICE_MP,
    EXTRA_SERVICE_VD,
    SERVICE_PAC,
    SERVICE_SEDEX,
    SERVICE_SEDEX10
)
from correios.models.posting import NotFoundTrackingEvent, Package, PostingList, ShippingLabel, TrackingCode
from correios.models.user import ExtraService, PostingCard, Service
from correios.utils import get_wsdl_path

from .vcr import vcr


@vcr.use_cassette
def test_basic_client():
    client = correios.Correios(username="sigep", password="XXXXXX", environment=correios.Correios.TEST)
    assert client.sigep_url == get_wsdl_path('AtendeCliente-test.wsdl')
    assert not client.sigep_verify
    assert client.username == "sigep"
    assert client.password == "XXXXXX"


@vcr.use_cassette
def test_get_user(client):
    user = client.get_user(contract_number="9911222777", posting_card_number="0056789123")

    assert user.name == "ECT"
    assert user.federal_tax_number == "34028316000103"
    assert user.state_tax_number == "0733382100116"
    assert user.status_number == 1
    assert len(user.contracts) == 1

    contract = user.contracts[0]
    assert len(contract.posting_cards) == 1


@vcr.use_cassette
def test_find_zip_code(client):
    zip_address = client.find_zipcode(ZipCode("70002-900"))

    assert zip_address.id == 0
    assert zip_address.zip_code == "70002900"
    assert zip_address.state == "DF"
    assert zip_address.city == "Brasília"
    assert zip_address.district == "Asa Norte"
    assert zip_address.address == "SBN Quadra 1 Bloco A"
    assert zip_address.complements == []


@vcr.use_cassette
def test_verify_service_availability(client, posting_card):
    status = client.verify_service_availability(posting_card, SERVICE_SEDEX10, "82940150", "01310000")
    assert status is True


@vcr.use_cassette
def test_get_posting_card_status(client, posting_card):
    status = client.get_posting_card_status(posting_card)
    assert status == PostingCard.ACTIVE


@vcr.use_cassette
def test_request_tracking_codes(client, user):
    result = client.request_tracking_codes(user, Service.get(SERVICE_SEDEX), quantity=10)
    assert len(result) == 10
    assert len(result[0].code) == 13


@vcr.use_cassette
def test_generate_verification_digit(client):
    result = client.generate_verification_digit(["DL74668653 BR"])
    assert result[0] == 6


@vcr.use_cassette
def test_close_posting_list(client, posting_card, posting_list: PostingList, shipping_label: ShippingLabel):
    shipping_label.posting_card = posting_card
    posting_list.add_shipping_label(shipping_label)
    posting_list = client.close_posting_list(posting_list, posting_card)
    assert posting_list.number is not None
    assert posting_list.closed


@vcr.use_cassette
def test_get_tracking_codes_events(client):
    result = client.get_tracking_code_events(["FJ064849483BR", "DU477828695BR"])

    assert len(result) == 2
    assert result[0] != result[1]

    assert isinstance(result[0], TrackingCode)
    assert result[0].code in ("FJ064849483BR", "DU477828695BR")

    assert isinstance(result[1], TrackingCode)
    assert result[1].code in ("FJ064849483BR", "DU477828695BR")


@vcr.use_cassette
def test_get_tracking_code_events(client):
    result = client.get_tracking_code_events("FJ064849483BR")

    assert isinstance(result[0], TrackingCode)
    assert result[0].code == "FJ064849483BR"


@vcr.use_cassette
def test_get_tracking_code_events_without_city_field(client):
    result = client.get_tracking_code_events("PJ651329640BR")

    assert isinstance(result[0], TrackingCode)
    assert result[0].code == "PJ651329640BR"
    assert result[0].events[0].city == ""


@vcr.use_cassette
def test_get_tracking_code_with_no_verification_digitevents(client):
    result = client.get_tracking_code_events("FJ06484948BR")

    assert isinstance(result[0], TrackingCode)
    assert result[0].code == "FJ064849483BR"


@vcr.use_cassette
def test_get_tracking_code_object_not_found_by_correios(client):
    tracking_code = client.get_tracking_code_events("DU05508759BR")[0]
    assert tracking_code.events

    event = tracking_code.events[0]
    assert isinstance(event, NotFoundTrackingEvent)
    assert event.timestamp
    assert event.status.type == "ERROR"
    assert event.status.status == 0


def test_get_tracking_codes_events_over_limit(client):
    codes = ["DU05508759BR"] * 51
    with pytest.raises(TrackingCodesLimitExceededError):
        client.get_tracking_code_events(codes)


def test_builder_posting_card_status():
    builder = correios.ModelBuilder()
    assert builder.build_posting_card_status("Normal") == PostingCard.ACTIVE
    assert builder.build_posting_card_status("Cancelado") == PostingCard.CANCELLED


def test_posting_list_serialization(posting_list, shipping_label):
    posting_list.add_shipping_label(shipping_label)
    serializer = correios.PostingListSerializer()
    document = serializer.get_document(posting_list)
    serializer.validate(document)
    xml = serializer.get_xml(document)
    assert xml.startswith(b'<?xml version="1.0" encoding="ISO-8859-1"?><correioslog>')
    assert b"<codigo_servico_adicional>019</codigo_servico_adicional>" not in xml
    assert b"<valor_declarado>10,29</valor_declarado>" not in xml


def test_posting_list_serialization_with_crazy_utf8_character(posting_list, shipping_label):
    shipping_label.receiver.neighborhood = 'Olho D’Água'
    posting_list.add_shipping_label(shipping_label)
    serializer = correios.PostingListSerializer()
    document = serializer.get_document(posting_list)
    serializer.validate(document)
    xml = serializer.get_xml(document)
    assert xml.startswith(b'<?xml version="1.0" encoding="ISO-8859-1"?><correioslog>')


def test_declared_value(posting_list, shipping_label):
    shipping_label.extra_services.append(ExtraService.get(EXTRA_SERVICE_VD))
    shipping_label.real_value = 10.29
    posting_list.add_shipping_label(shipping_label)
    serializer = correios.PostingListSerializer()
    document = serializer.get_document(posting_list)
    serializer.validate(document)
    xml = serializer.get_xml(document)
    assert shipping_label.service == Service.get(SERVICE_PAC)
    assert b"<codigo_servico_adicional>019</codigo_servico_adicional>" in xml
    assert b"<valor_declarado>18,00</valor_declarado>" in xml


def test_fail_empty_posting_list_serialization(posting_list):
    serializer = correios.PostingListSerializer()
    with pytest.raises(PostingListSerializerError):
        serializer.get_document(posting_list)


def test_fail_closed_posting_list_serialization(posting_list: PostingList, shipping_label):
    posting_list.add_shipping_label(shipping_label)
    posting_list.close_with_id(number=12345)

    serializer = correios.PostingListSerializer()
    with pytest.raises(PostingListSerializerError):
        serializer.get_document(posting_list)


def test_limit_size_city_name(posting_list, shipping_label):
    shipping_label.receiver.city = 'Porto Alegre (Rio Grande do Sul)'
    shipping_label.sender.city = 'Santa Maria (Rio Grande do Sul)'
    posting_list.add_shipping_label(shipping_label)
    serializer = correios.PostingListSerializer()
    document = serializer.get_document(posting_list)
    serializer.validate(document)
    xml = serializer.get_xml(document)

    assert b"<cidade_destinatario><![CDATA[Porto Alegre (Rio Grande do Su]]></cidade_destinatario>" in xml
    assert b"<cidade_remetente><![CDATA[Santa Maria (Rio Grande do Sul]]></cidade_remetente>" in xml


@vcr.use_cassette
def test_calculate_freights(client, posting_card, package):
    freights = client.calculate_freights(posting_card, [SERVICE_SEDEX, SERVICE_PAC], "07192100", "80030001", package)
    assert len(freights) == 2

    freight = freights[0]
    assert freight.error_code == 0
    assert freight.error_message == ""
    assert freight.service == SERVICE_SEDEX
    assert freight.delivery_time.days == 1
    assert freight.total == Decimal("23.75")
    assert freight.saturday is True
    assert freight.home is True

    freight = freights[1]
    assert freight.error_code == 0
    assert freight.error_message == ""
    assert freight.service == SERVICE_PAC
    assert freight.delivery_time.days == 6
    assert freight.total == Decimal("14.10")
    assert freight.saturday is False
    assert freight.home is True


@vcr.use_cassette
def test_calculate_freights_with_extra_services(client, posting_card, package):
    freights = client.calculate_freights(
        posting_card=posting_card,
        services=[SERVICE_SEDEX],
        from_zip="07192100",
        to_zip="80030001",
        package=package,
        value="9000.00",
        extra_services=[EXTRA_SERVICE_AR, EXTRA_SERVICE_MP]
    )
    assert len(freights) == 1

    freight = freights[0]
    assert freight.service == SERVICE_SEDEX
    assert freight.total == Decimal("96.03")
    assert freight.value == Decimal("23.75")
    assert freight.declared_value == Decimal("62.48")
    assert freight.mp_value == Decimal("5.50")
    assert freight.ar_value == Decimal("4.30")


@vcr.use_cassette
def test_calculate_freight_with_error(client, posting_card, package: Package):
    package.real_weight = 80000  # invalid weight (80kg)
    freights = client.calculate_freights(posting_card, [SERVICE_SEDEX], "99999000", "99999999", package)
    assert len(freights) == 1
    assert freights[0].error_code == -4
    assert freights[0].error_message == "Peso excedido."


@vcr.use_cassette
def test_calculate_delivery_time(client):
    expected_delivery_time = 1
    delivery_time = client.calculate_delivery_time(Service.get(SERVICE_SEDEX), '07192100', '80030001')
    assert expected_delivery_time == int(delivery_time)


@vcr.use_cassette
def test_calculate_delivery_time_service_not_allowed_for_path(client):
    expected_delivery_time = 0
    delivery_time = client.calculate_delivery_time(Service.get(SERVICE_PAC), '01311300', '01311300')
    assert expected_delivery_time == int(delivery_time)
