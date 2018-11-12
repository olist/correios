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
from unittest import mock

import pytest
from requests.exceptions import ConnectTimeout
from zeep.exceptions import Fault

from correios.exceptions import (
    AuthenticationError,
    CanceledPostingCardError,
    ClosePostingListError,
    ConnectTimeoutError,
    NonexistentPostingCardError,
    PostingListSerializerError,
    TrackingCodesLimitExceededError,
)
from correios.models.address import ZipCode
from correios.models.builders import ModelBuilder
from correios.models.data import (
    EXTRA_SERVICE_AR,
    EXTRA_SERVICE_MP,
    EXTRA_SERVICE_VD_PAC,
    EXTRA_SERVICE_VD_SEDEX,
    FREIGHT_ERROR_FINAL_ZIPCODE_RESTRICTED,
    FREIGHT_ERROR_INITIAL_AND_FINAL_ZIPCODE_RESTRICTED,
    FREIGHT_ERROR_INITIAL_ZIPCODE_RESTRICTED,
    SERVICE_PAC,
    SERVICE_SEDEX,
    SERVICE_SEDEX10,
)
from correios.models.posting import (
    FreightResponse,
    NotFoundTrackingEvent,
    PostalUnit,
    PostInfo,
    PostingList,
    TrackingCode,
)
from correios.models.user import ExtraService, PostingCard, Service
from correios.serializers import PostingListSerializer
from correios.utils import get_resource_path, to_decimal
from correios.xml_utils import fromstring

from .vcr import vcr

try:
    from correios import client as correios
except ImportError:
    correios = None


@pytest.mark.skipif(not correios, reason="API Client support disabled")
@vcr.use_cassette
def test_basic_client():
    client = correios.Correios(username="sigep", password="XXXXXX", environment=correios.Correios.TEST)
    assert client.sigep_url == str(get_resource_path('wsdls/AtendeCliente-test.wsdl'))
    assert not client.sigep_verify
    assert client.username == "sigep"
    assert client.password == "XXXXXX"


@pytest.mark.skipif(not correios, reason="API Client support disabled")
@mock.patch('zeep.proxy.OperationProxy.__call__')
def test_client_timeout_error(mock_soap_client, client):
    mock_soap_client.side_effect = ConnectTimeout()
    with pytest.raises(ConnectTimeoutError):
        client.find_zipcode(ZipCode("70002-900"))


@pytest.mark.skipif(not correios, reason="API Client support disabled")
@vcr.use_cassette
def test_client_authentication_error(client):
    with pytest.raises(AuthenticationError):
        client.get_user(contract_number="9911222777", posting_card_number="0056789123")


@pytest.mark.skipif(not correios, reason="API Client support disabled")
@vcr.use_cassette
def test_client_canceled_posting_card_error(client):
    with pytest.raises(CanceledPostingCardError):
        client.get_user(contract_number="9911222777", posting_card_number="0057018901")


@pytest.mark.skipif(not correios, reason="API Client support disabled")
@vcr.use_cassette
def test_client_nonexistent_posting_card_error(client):
    with pytest.raises(NonexistentPostingCardError):
        client.get_user(contract_number="9911222777", posting_card_number="4444444444")


@pytest.mark.skipif(not correios, reason="API Client support disabled")
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


@pytest.mark.skipif(not correios, reason="API Client support disabled")
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


@pytest.mark.skipif(not correios, reason="API Client support disabled")
@vcr.use_cassette
def test_verify_service_availability(client, posting_card):
    status = client.verify_service_availability(posting_card, SERVICE_SEDEX10, "82940150", "01310000")
    assert status is True


@pytest.mark.skipif(not correios, reason="API Client support disabled")
@vcr.use_cassette
def test_get_posting_card_status(client, posting_card):
    status = client.get_posting_card_status(posting_card)
    assert status == PostingCard.ACTIVE


@pytest.mark.skipif(not correios, reason="API Client support disabled")
@vcr.use_cassette
def test_request_tracking_codes(client, user):
    result = client.request_tracking_codes(user, Service.get(SERVICE_SEDEX), quantity=10)
    assert len(result) == 10
    assert len(result[0].code) == 13


@pytest.mark.skipif(not correios, reason="API Client support disabled")
@vcr.use_cassette
def test_generate_verification_digit(client):
    result = client.generate_verification_digit(["DL74668653 BR"])
    assert result[0] == 6


@vcr.use_cassette
def test_get_post_info(client):
    result = client._auth_call('solicitaXmlPlp', 875057)

    data = fromstring(result.encode('iso-8859-1'))

    user = client.get_user(
        contract_number=data.remetente.numero_contrato.text,
        posting_card_number=data.plp.cartao_postagem.text
    )

    post_info = client.get_post_info(number=875057)
    assert isinstance(post_info, PostInfo)
    assert str(post_info.value) == data.plp.valor_global.text

    postal_unit = post_info.postal_unit
    assert isinstance(postal_unit, PostalUnit)
    assert postal_unit.code == data.plp.mcu_unidade_postagem
    assert postal_unit.description == data.plp.nome_unidade_postagem

    posting_list = post_info.posting_list
    assert isinstance(posting_list, PostingList)
    assert posting_list.number == data.plp.id_plp

    shipping_labels = posting_list.shipping_labels
    assert len(shipping_labels) == len(data.objeto_postal)

    for obj in data.objeto_postal:
        tracking_code = TrackingCode.create(obj.numero_etiqueta.text)
        assert tracking_code.short in shipping_labels
        label = shipping_labels[tracking_code.short]

        extra_info = obj.nacional
        billing = getattr(extra_info, 'valor_a_cobrar', None) or '0.00'
        assert label.billing == to_decimal(billing)
        assert label.invoice_number == extra_info.numero_nota_fiscal
        assert label.invoice_series == extra_info.serie_nota_fiscal

        extra_services = obj.servico_adicional

        declared_value = getattr(extra_services, 'valor_declarado', None)

        invoice_value = getattr(extra_info, 'valor_nota_fiscal', None)

        assert label.real_value == to_decimal(
            declared_value or invoice_value or '0.00'
        )

        assert label.text == extra_info.descricao_objeto
        posting_card_number = user.contracts[0].posting_cards[0].number
        assert label.posting_card.number == posting_card_number

        sender = data.remetente

        assert label.sender.email == sender.email_remetente.text
        assert label.sender.name == sender.nome_remetente.text
        assert label.sender.street == sender.logradouro_remetente.text
        assert label.sender.number == sender.numero_remetente.text
        assert label.sender.complement == sender.complemento_remetente.text
        assert label.sender.neighborhood == sender.bairro_remetente.text
        assert label.sender.zip_code == sender.cep_remetente.text
        assert label.sender.city == sender.cidade_remetente.text
        assert label.sender.state == sender.uf_remetente.text
        assert (
            label.sender.phone.number == (sender.telefone_remetente.text or '')
        )

        receiver = obj.destinatario

        assert label.receiver.email == (receiver.email_destinatario.text or '')

        assert label.receiver.name == receiver.nome_destinatario.text
        assert label.receiver.street == receiver.logradouro_destinatario.text
        assert label.receiver.number == receiver.numero_end_destinatario.text
        assert (
            label.receiver.complement ==
            (receiver.complemento_destinatario.text or '')
        )
        assert (
            label.receiver.neighborhood == extra_info.bairro_destinatario.text
        )
        assert label.receiver.zip_code == extra_info.cep_destinatario.text
        assert label.receiver.city == extra_info.cidade_destinatario.text
        assert label.receiver.state == extra_info.uf_destinatario.text
        assert (
            label.receiver.phone.number ==
            (receiver.celular_destinatario.text or '')
        )

        assert len(label.extra_services) == len(extra_services)

        for service in extra_services.codigo_servico_adicional:
            assert service in label.extra_services

        package = label.package

        assert package.service == obj.codigo_servico_postagem

        dimensions = obj.dimensao_objeto

        assert package.package_type == dimensions.tipo_objeto

        assert package.real_diameter == float(
            dimensions.dimensao_diametro.text.replace(',', '.')
        )

        assert package.real_height == float(
            dimensions.dimensao_altura.text.replace(',', '.')
        )

        assert package.real_length == float(
            dimensions.dimensao_comprimento.text.replace(',', '.')
        )

        assert package.real_weight == float(obj.peso.text.replace(',', '.'))
        assert package.real_width == float(
            dimensions.dimensao_largura.text.replace(',', '.')
        )

        receipt = label.receipt

        assert receipt.number == obj.numero_comprovante_postagem
        assert receipt.real_post_date == obj.data_postagem_sara.text
        assert receipt.real_value == obj.valor_cobrado.text


@pytest.mark.skipif(not correios, reason="API Client support disabled")
@vcr.use_cassette
def test_close_posting_list(client, posting_card, posting_list, shipping_label):
    shipping_label.posting_card = posting_card
    posting_list.add_shipping_label(shipping_label)
    posting_list = client.close_posting_list(posting_list, posting_card)
    assert posting_list.number is not None
    assert posting_list.closed


@pytest.mark.skipif(not correios, reason="API Client support disabled")
@mock.patch('zeep.proxy.OperationProxy.__call__')
def test_client_close_posting_list_error(
    mock_soap_client,
    client,
    posting_card,
    posting_list,
    shipping_label,
):
    mock_soap_client.side_effect = Fault(
        'A PLP não será fechada , o(s) objeto(s) [PP40233163BR] já estão '
        'vinculados em outra PLP!'
    )
    shipping_label.posting_card = posting_card
    posting_list.add_shipping_label(shipping_label)
    with pytest.raises(ClosePostingListError):
        client.close_posting_list(posting_list, posting_card)


@pytest.mark.skipif(not correios, reason="API Client support disabled")
@vcr.use_cassette
def test_get_tracking_codes_events(client):
    codes = ["BE058714266BR", "JT365572014BR"]
    result = client.get_tracking_code_events(codes)

    assert len(result) == 2
    assert result[0] != result[1]

    assert isinstance(result[0], TrackingCode)
    assert result[0].code in codes

    assert isinstance(result[1], TrackingCode)
    assert result[1].code in codes


@pytest.mark.skipif(not correios, reason="API Client support disabled")
@vcr.use_cassette
def test_get_tracking_code_events(client):
    result = client.get_tracking_code_events("BE058714266BR")

    assert isinstance(result[0], TrackingCode)
    assert result[0].code == "BE058714266BR"


@pytest.mark.skipif(not correios, reason="API Client support disabled")
@vcr.use_cassette
def test_get_tracking_code_events_without_city_field(client):
    result = client.get_tracking_code_events("FJ064849483BR")

    assert isinstance(result[0], TrackingCode)
    assert result[0].code == "FJ064849483BR"
    assert result[0].events[0].city == ""


@pytest.mark.skipif(not correios, reason="API Client support disabled")
@vcr.use_cassette
def test_get_tracking_code_with_no_verification_digitevents(client):
    result = client.get_tracking_code_events("BE05871426BR")

    assert isinstance(result[0], TrackingCode)
    assert result[0].code == "BE058714266BR"


@pytest.mark.skipif(not correios, reason="API Client support disabled")
@vcr.use_cassette
def test_get_tracking_code_object_not_found_by_correios(client):
    tracking_code = client.get_tracking_code_events("DU05508759BR")[0]
    assert tracking_code.events

    event = tracking_code.events[0]
    assert isinstance(event, NotFoundTrackingEvent)
    assert event.timestamp
    assert event.status.type == "ERROR"
    assert event.status.status == 0


@pytest.mark.skipif(not correios, reason="API Client support disabled")
def test_get_tracking_codes_events_over_limit(client):
    codes = ["DU05508759BR"] * 51
    with pytest.raises(TrackingCodesLimitExceededError):
        client.get_tracking_code_events(codes)


@pytest.mark.skipif(not correios, reason="API Client support disabled")
def test_builder_posting_card_status():
    builder = ModelBuilder()
    assert builder.build_posting_card_status("Normal") == PostingCard.ACTIVE
    assert builder.build_posting_card_status("Cancelado") == PostingCard.CANCELLED


@pytest.mark.skipif(not correios, reason="API Client support disabled")
def test_posting_list_serialization(posting_list, shipping_label):
    posting_list.add_shipping_label(shipping_label)
    serializer = PostingListSerializer()
    document = serializer.get_document(posting_list)
    serializer.validate(document)
    xml = serializer.get_xml(document)
    assert xml.startswith(b'<?xml version="1.0" encoding="ISO-8859-1"?><correioslog>')
    assert b"<codigo_servico_adicional>064</codigo_servico_adicional>" not in xml
    assert b"<valor_declarado>10,29</valor_declarado>" not in xml


@pytest.mark.skipif(not correios, reason="API Client support disabled")
def test_posting_list_serialization_with_crazy_utf8_character(posting_list, shipping_label):
    shipping_label.receiver.neighborhood = 'Olho D’Água'
    posting_list.add_shipping_label(shipping_label)
    serializer = PostingListSerializer()
    document = serializer.get_document(posting_list)
    serializer.validate(document)
    xml = serializer.get_xml(document)
    assert xml.startswith(b'<?xml version="1.0" encoding="ISO-8859-1"?><correioslog>')


@pytest.mark.skipif(not correios, reason="API Client support disabled")
@pytest.mark.parametrize('extra_service_vd,code', [
    (EXTRA_SERVICE_VD_PAC, b'064'),
    (EXTRA_SERVICE_VD_SEDEX, b'019'),
])
def test_declared_value(extra_service_vd, code, posting_list, shipping_label):
    shipping_label.extra_services.append(ExtraService.get(extra_service_vd))
    shipping_label.real_value = 10.29
    posting_list.add_shipping_label(shipping_label)
    serializer = PostingListSerializer()
    document = serializer.get_document(posting_list)
    serializer.validate(document)
    xml = serializer.get_xml(document)
    assert shipping_label.service == Service.get(SERVICE_PAC)
    assert b'<codigo_servico_adicional>%b</codigo_servico_adicional>' % code in xml
    assert b'<valor_declarado>19,50</valor_declarado>' in xml


@pytest.mark.skipif(not correios, reason="API Client support disabled")
def test_fail_empty_posting_list_serialization(posting_list):
    serializer = PostingListSerializer()
    with pytest.raises(PostingListSerializerError):
        serializer.get_document(posting_list)


@pytest.mark.skipif(not correios, reason="API Client support disabled")
def test_fail_closed_posting_list_serialization(posting_list, shipping_label):
    posting_list.add_shipping_label(shipping_label)
    posting_list.close_with_id(number=12345)

    serializer = PostingListSerializer()
    with pytest.raises(PostingListSerializerError):
        serializer.get_document(posting_list)


@pytest.mark.skipif(not correios, reason="API Client support disabled")
def test_limit_size_city_name(posting_list, shipping_label):
    shipping_label.receiver.city = 'Porto Alegre (Rio Grande do Sul)'
    shipping_label.sender.city = 'Santa Maria (Rio Grande do Sul)'
    posting_list.add_shipping_label(shipping_label)
    serializer = PostingListSerializer()
    document = serializer.get_document(posting_list)
    serializer.validate(document)
    xml = serializer.get_xml(document)

    assert b"<cidade_destinatario><![CDATA[Porto Alegre (Rio Grande do Su]]></cidade_destinatario>" in xml
    assert b"<cidade_remetente><![CDATA[Santa Maria (Rio Grande do Sul]]></cidade_remetente>" in xml


@pytest.mark.skipif(not correios, reason="API Client support disabled")
@vcr.use_cassette
def test_calculate_freights(client, posting_card, package):
    freights = client.calculate_freights(posting_card, [SERVICE_SEDEX, SERVICE_PAC], "07192100", "80030001", package)
    assert len(freights) == 2

    freight = freights[0]
    assert freight.error_code == 0
    assert not freight.error_message
    assert freight.service == SERVICE_SEDEX
    assert freight.delivery_time.days == 1
    assert freight.total == Decimal("23.75")
    assert freight.saturday is True
    assert freight.home is True

    freight = freights[1]
    assert freight.error_code == 0
    assert not freight.error_message
    assert freight.service == SERVICE_PAC
    assert freight.delivery_time.days == 6
    assert freight.total == Decimal("14.10")
    assert freight.saturday is False
    assert freight.home is True


@pytest.mark.skipif(not correios, reason="API Client support disabled")
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


@pytest.mark.skipif(not correios, reason="API Client support disabled")
@vcr.use_cassette
def test_calculate_freight_with_error(client, posting_card, package):
    package.real_weight = 80000  # invalid weight (80kg)
    freights = client.calculate_freights(posting_card, [SERVICE_SEDEX], "99999000", "99999999", package)
    assert len(freights) == 1
    assert freights[0].error_code == -4
    assert freights[0].error_message == "Peso excedido."


@pytest.mark.skipif(not correios, reason="API Client support disabled")
@vcr.use_cassette
def test_calculate_delivery_time(client):
    expected_delivery_time = 1
    delivery_time = client.calculate_delivery_time(Service.get(SERVICE_SEDEX), '07192100', '80030001')
    assert expected_delivery_time == int(delivery_time)


@pytest.mark.skipif(not correios, reason="API Client support disabled")
@vcr.use_cassette
def test_calculate_delivery_time_service_not_allowed_for_path(client):
    expected_delivery_time = 0
    delivery_time = client.calculate_delivery_time(Service.get(SERVICE_PAC), '01311300', '01311300')
    assert expected_delivery_time == int(delivery_time)


@pytest.mark.skipif(not correios, reason="API Client support disabled")
@vcr.use_cassette
def test_calculate_freight_with_error_code_10_restricted(client, posting_card, package):
    freights = client.calculate_freights(
        posting_card=posting_card,
        services=[SERVICE_SEDEX],
        from_zip='07192100',
        to_zip='09960610',
        package=package,
        value="9000.00",
        extra_services=[EXTRA_SERVICE_AR, EXTRA_SERVICE_MP]
    )

    assert len(freights) == 1
    freight = freights[0]  # FreightResponse

    assert isinstance(freight, FreightResponse)
    assert freight.is_restricted_address()
    assert freight.error_code == FREIGHT_ERROR_FINAL_ZIPCODE_RESTRICTED
    assert freight.value != 0
    assert freight.delivery_time.days == 2
    assert freight.saturday


@pytest.mark.skipif(not correios, reason="API Client support disabled")
@vcr.use_cassette
def test_calculate_freight_with_error_code_11_restricted(
    client,
    posting_card,
    package
):
    freights = client.calculate_freights(
        posting_card=posting_card,
        services=[SERVICE_SEDEX],
        from_zip='09960610',
        to_zip='04475490',
        package=package,
        value="9000.00",
        extra_services=[EXTRA_SERVICE_AR, EXTRA_SERVICE_MP]
    )

    assert len(freights) == 1

    freight = freights[0]
    assert isinstance(freight, FreightResponse)
    assert len(freights) == 1
    assert freight.is_restricted_address()
    assert freight.error_code == FREIGHT_ERROR_INITIAL_AND_FINAL_ZIPCODE_RESTRICTED
    assert freight.value != 0
    assert freight.delivery_time.days == 8
    assert freight.saturday


@pytest.mark.skipif(not correios, reason="API Client support disabled")
@vcr.use_cassette
def test_calculate_freight_with_error_code_9_restricted(
    client,
    posting_card,
    package
):
    freights = client.calculate_freights(
        posting_card=posting_card,
        services=[SERVICE_SEDEX],
        from_zip='09960610',
        to_zip='04475490',
        package=package,
        value="9000.00",
        extra_services=[EXTRA_SERVICE_AR, EXTRA_SERVICE_MP]
    )

    assert len(freights) == 1

    freight = freights[0]
    assert isinstance(freight, FreightResponse)
    assert freight.is_restricted_address()
    assert freight.error_code == FREIGHT_ERROR_INITIAL_ZIPCODE_RESTRICTED
    assert freight.value != 0
    assert freight.delivery_time.days == 8
    assert freight.saturday
