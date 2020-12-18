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
from contextlib import suppress
from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Dict, List, Optional, Sequence, Union

from correios import DATADIR, xml_utils
from correios.exceptions import InvalidEventStatusError, PostingListSerializerError
from correios.models.data import EXTRA_SERVICE_AR, EXTRA_SERVICE_MP
from correios.utils import get_wsdl_path, to_decimal, to_integer

from .models.address import ReceiverAddress, SenderAddress, ZipAddress, ZipCode
from .models.posting import (
    Freight,
    FreightError,
    Package,
    PostalUnit,
    PostInfo,
    PostingList,
    Receipt,
    ShippingLabel,
    TrackingCode,
    TrackingEvent
)
from .models.user import Contract, ExtraService, FederalTaxNumber, PostingCard, Service, StateTaxNumber, User
from .soap import SoapClient

KG = 1000  # g


class ValidRestrictResponse(Enum):
    INITIAL_ZIPCODE_RESTRICTED = 9
    FINAL_ZIPCODE_RESTRICTED = 10
    INITIAL_AND_FINAL_ZIPCODE_RESTRICTED = 11

    @classmethod
    def restricted_codes(cls):
        return [
            cls.FINAL_ZIPCODE_RESTRICTED.value,
            cls.INITIAL_AND_FINAL_ZIPCODE_RESTRICTED.value,
            cls.FINAL_ZIPCODE_RESTRICTED.value
        ]


class ModelBuilder:
    def build_service(self, service_data):
        service = Service(
            code=service_data.codigo,
            id=service_data.id,
            description=service_data.descricao,
            category=service_data.servicoSigep.categoriaServico
        )
        return service

    def build_posting_card(self, contract: Contract, posting_card_data):
        posting_card = PostingCard(
            contract=contract,
            number=posting_card_data.numero,
            administrative_code=posting_card_data.codigoAdministrativo,
        )

        posting_card.start_date = posting_card_data.dataVigenciaInicio
        posting_card.end_date = posting_card_data.dataVigenciaFim
        posting_card.status = posting_card_data.statusCartaoPostagem
        posting_card.status_code = posting_card_data.statusCodigo
        posting_card.unit = posting_card_data.unidadeGenerica.strip() or 0

        for service_data in posting_card_data.servicos:
            service = self.build_service(service_data)
            posting_card.add_service(service)

        return posting_card

    def build_contract(self, user: User, contract_data):
        contract = Contract(
            user=user,
            number=contract_data.contratoPK.numero,
            regional_direction=contract_data.codigoDiretoria,
        )

        contract.customer_code = contract_data.codigoCliente
        contract.status_code = contract_data.statusCodigo
        contract.start_date = contract_data.dataVigenciaInicio
        contract.end_date = contract_data.dataVigenciaFim

        for posting_card_data in contract_data.cartoesPostagem:
            self.build_posting_card(contract, posting_card_data)

        return contract

    def build_user(self, user_data):
        user = User(
            name=user_data.nome,
            federal_tax_number=FederalTaxNumber(user_data.cnpj),
            state_tax_number=StateTaxNumber(user_data.inscricaoEstadual),
            status_number=user_data.statusCodigo,
        )

        for contract_data in user_data.contratos:
            self.build_contract(user, contract_data)

        return user

    def build_zip_address(self, zip_address_data):
        zip_address = ZipAddress(
            id=zip_address_data.id,
            zip_code=zip_address_data.cep,
            state=zip_address_data.uf,
            city=zip_address_data.cidade,
            district=zip_address_data.bairro,
            address=zip_address_data.end,
            complements=[zip_address_data.complemento, zip_address_data.complemento2]
        )
        return zip_address

    def build_post_info(self, data, user: User, validate_package: bool = True) -> PostInfo:
        post_info = PostInfo(
            postal_unit=self.build_postal_unit(data.plp),
            posting_list=self._load_posting_list(
                data=data,
                user=user,
                validate_package=validate_package
            ),
            value=data.plp.valor_global
        )
        return post_info

    def build_receipt(self,  data) -> Optional[Receipt]:
        if data.status_processamento != Receipt.STATUS_PROCESSED:
            return None

        receipt = Receipt(
            number=data.numero_comprovante_postagem,
            post_date=data.data_postagem_sara.text,
            value=data.valor_cobrado.text
        )
        return receipt

    def build_postal_unit(self, data) -> PostalUnit:
        postal_unit = PostalUnit(
            code=data.mcu_unidade_postagem,
            description=data.nome_unidade_postagem,
        )
        return postal_unit

    def _load_posting_list(self, data, user: User, validate_package: bool = True) -> PostingList:
        contract_number = to_integer(data.remetente.numero_contrato)

        contract = next(
            c for c in user.contracts if c.number == contract_number
        )

        posting_card_number = str(data.plp.cartao_postagem.text)

        posting_card = next(
            p for p in contract.posting_cards
            if p.number == posting_card_number
        )

        posting_list = PostingList(custom_id=0)

        for postal_object in data.objeto_postal:

            posting_list.add_shipping_label(self._load_shipping_label(
                data=postal_object,
                posting_card=posting_card,
                sender_address=self._load_sender_address(data.remetente),
                validate_package=validate_package
            ))

        posting_list.close_with_id(data.plp.id_plp)

        return posting_list

    def _load_shipping_label(
        self,
        data,
        posting_card: PostingCard,
        sender_address: SenderAddress,
        validate_package: bool = True
    ) -> ShippingLabel:

        declared_value = getattr(
            data.servico_adicional,
            'valor_declarado',
            None
        )
        extra_services_codes = list(
            data.servico_adicional.codigo_servico_adicional
        )
        extra_services = [
            ExtraService.get(code) for code in extra_services_codes if code
        ]

        invoice_value = getattr(data.nacional, 'valor_nota_fiscal', None)

        billing = getattr(data.nacional, 'valor_a_cobrar', None) or '0.00'

        shipping_label = ShippingLabel(
            billing=to_decimal(billing),
            invoice_number=data.nacional.numero_nota_fiscal,
            invoice_series=data.nacional.serie_nota_fiscal,
            value=to_decimal(declared_value or invoice_value or '0.00'),
            text=data.nacional.descricao_objeto,
            posting_card=posting_card,
            sender=sender_address,
            receiver=self._load_receiver_address(data),
            package=self._load_package(data, validate_package=validate_package),
            service=Service.get(data.codigo_servico_postagem.text),
            tracking_code=data.numero_etiqueta.text,
            receipt=self.build_receipt(data)
        )

        shipping_label.add_extra_services([
            extra_service for extra_service in extra_services
            if extra_service not in shipping_label.extra_services
        ])

        return shipping_label

    def _load_sender_address(self, data) -> SenderAddress:
        sender_address = SenderAddress(
            email=data.email_remetente.text,
            name=data.nome_remetente.text,
            street=data.logradouro_remetente.text,
            number=data.numero_remetente.text,
            complement=data.complemento_remetente.text,
            neighborhood=data.bairro_remetente.text,
            zip_code=data.cep_remetente.text,
            city=data.cidade_remetente.text,
            state=data.uf_remetente.text,
            phone=data.telefone_remetente.text or '',
        )

        return sender_address

    def _load_receiver_address(self, data) -> ReceiverAddress:
        receiver_data = data.destinatario

        extra_data = data.nacional

        receiver_address = ReceiverAddress(
            email=getattr(receiver_data, 'email_remetente', ''),
            name=receiver_data.nome_destinatario.text or '',
            street=receiver_data.logradouro_destinatario.text or '',
            number=receiver_data.numero_end_destinatario.text or '',
            complement=receiver_data.complemento_destinatario.text or '',
            neighborhood=extra_data.bairro_destinatario.text or '',
            zip_code=extra_data.cep_destinatario.text or '',
            city=extra_data.cidade_destinatario.text or '',
            state=extra_data.uf_destinatario.text or '',
            phone=receiver_data.celular_destinatario.text or '',
        )

        return receiver_address

    def _load_package(self, data, validate_package) -> Package:
        dimensions = data.dimensao_objeto

        type_ = dimensions.tipo_objeto.text.strip()
        type_ = int(type_) if type_.isdigit() else None

        diameter = float(
            dimensions.dimensao_diametro.text.replace(',', '.')
        )

        if type_ == Package.TYPE_BOX:
            diameter = 0

        package = Package(
            diameter=diameter,
            height=float(dimensions.dimensao_altura.text.replace(',', '.')),
            length=float(
                dimensions.dimensao_comprimento.text.replace(',', '.')
            ),
            weight=float(data.peso.text.replace(',', '.')),
            width=float(dimensions.dimensao_largura.text.replace(',', '.')),
            package_type=dimensions.tipo_objeto,
            service=data.codigo_servico_postagem.text,
            validate_package=validate_package
        )

        return package

    def build_posting_card_status(self, response):
        if response.lower() != "normal":
            return PostingCard.CANCELLED
        return PostingCard.ACTIVE

    def build_tracking_codes_list(self, response):
        codes = response.split(",")
        return TrackingCode.create_range(codes[0], codes[1])

    def _load_events(self, tracking_code: TrackingCode, events):
        for event in events:
            timestamp = datetime.strptime("{} {}".format(event.data, event.hora), TrackingEvent.timestamp_format)
            cidade_destino = ""
            uf_destino = ""
            local_destino = ""
            endereco_logradouro = ""
            endereco_numero = ""
            endereco_bairro = ""
            endereco_localidade = ""
            endereco_uf = ""
            if len(event['destino']) > 0:
                cidade_destino = getattr(event['destino'][0], "cidade", "") or ""
                uf_destino = getattr(event['destino'][0], "uf", "") or ""
                local_destino = getattr(event['destino'][0], "local", "") or ""
            if event['endereco'] is not None:
                endereco_logradouro = event['endereco']['logradouro']
                endereco_numero = event['endereco']['numero']
                endereco_bairro = event['endereco']['bairro']
                endereco_localidade = event['endereco']['localidade']
                endereco_uf = event['endereco']['uf']
            try:
                event = TrackingEvent(
                    timestamp=timestamp,
                    status=getattr(event, "status", "") or "",
                    event_type=getattr(event, "tipo", "") or "",
                    location_zip_code=getattr(event, "codigo", "") or "",
                    location=getattr(event, "local", "") or "",
                    city=getattr(event, "cidade", "") or "",
                    state=getattr(event, "uf", "") or "",
                    receiver=getattr(event, "recebedor", "") or "",
                    document=getattr(event, "documento", "") or "",
                    comment=getattr(event, "comentario", "") or "",
                    description=getattr(event, "descricao", "") or "",
                    detail=getattr(event, "detalhe", "") or "",
                    destination_location=local_destino,
                    destination_city=cidade_destino,
                    destination_uf=uf_destino,
                    address_street=endereco_logradouro,
                    address_number=endereco_numero,
                    address_district=endereco_bairro,
                    address_city=endereco_localidade,
                    address_state=endereco_uf
                )
            except InvalidEventStatusError:
                tracking_code.events = []
                return

            tracking_code.add_event(event)

    def load_tracking_events(self, tracking_codes: Dict[str, TrackingCode], response):
        result = []
        for tracked_object in response.objeto:

            with suppress(KeyError):
                tracking_code = tracking_codes[tracked_object.numero]

                tracking_code.name = tracked_object.nome
                tracking_code.initials = tracked_object.sigla
                tracking_code.category = tracked_object.categoria
                self._load_events(tracking_code, tracked_object.evento)

                result.append(tracking_code)

        return result

    def build_freights_list(self, response):
        result = []
        for service_data in response.cServico:
            freight = self.build_freight(service_data=service_data)
            result.append(freight)
        return result

    def build_freight(self, service_data):
        data = {
            'service': Service.get(service_data.Codigo),
            'error_code': to_integer(service_data.Erro),
            'delivery_time': int(service_data.PrazoEntrega),
            'value': to_decimal(service_data.ValorSemAdicionais),
            'declared_value': to_decimal(service_data.ValorValorDeclarado),
            'ar_value': to_decimal(service_data.ValorAvisoRecebimento),
            'mp_value': to_decimal(service_data.ValorMaoPropria),
            'saturday': service_data.EntregaSabado or "",
            'home': service_data.EntregaDomiciliar or "",
            'error_message': service_data.MsgErro or None
        }

        if (
            data['error_code'] and
            not data['error_code'] in ValidRestrictResponse.restricted_codes()
        ):
            return FreightError(**data)
        return Freight(**data)


class PostingListSerializer:
    def _get_posting_list_element(self, posting_list):
        element = xml_utils.Element("plp")
        xml_utils.SubElement(element, "id_plp")
        xml_utils.SubElement(element, "valor_global")
        xml_utils.SubElement(element, "mcu_unidade_postagem")
        xml_utils.SubElement(element, "nome_unidade_postagem")
        xml_utils.SubElement(element, "cartao_postagem", text=str(posting_list.posting_card))
        return element

    def _get_sender_info_element(self, posting_list):
        sender = posting_list.sender
        posting_card = posting_list.posting_card
        contract = posting_list.contract

        sender_info = xml_utils.Element("remetente")
        xml_utils.SubElement(sender_info, "numero_contrato", text=str(contract.number))
        xml_utils.SubElement(sender_info, "numero_diretoria", text=str(contract.regional_direction_number))
        xml_utils.SubElement(sender_info, "codigo_administrativo", text=str(posting_card.administrative_code))
        xml_utils.SubElement(sender_info, "nome_remetente", cdata=str(sender.name))
        xml_utils.SubElement(sender_info, "logradouro_remetente", cdata=str(sender.street))
        xml_utils.SubElement(sender_info, "numero_remetente", cdata=str(sender.number) or 'S/n')
        xml_utils.SubElement(sender_info, "complemento_remetente", cdata=str(sender.complement))
        xml_utils.SubElement(sender_info, "bairro_remetente", cdata=str(sender.neighborhood))
        xml_utils.SubElement(sender_info, "cep_remetente", cdata=str(sender.zip_code))
        xml_utils.SubElement(sender_info, "cidade_remetente", cdata=str(sender.city)[:30])
        xml_utils.SubElement(sender_info, "uf_remetente", cdata=str(sender.state))
        xml_utils.SubElement(sender_info, "telefone_remetente", cdata=sender.phone.short)
        xml_utils.SubElement(sender_info, "fax_remetente", cdata="")
        xml_utils.SubElement(sender_info, "email_remetente", cdata=str(sender.email))
        return sender_info

    def _get_shipping_label_element(self, shipping_label: ShippingLabel):
        item = xml_utils.Element("objeto_postal")
        xml_utils.SubElement(item, "numero_etiqueta", text=str(shipping_label.tracking_code))
        xml_utils.SubElement(item, "codigo_objeto_cliente")
        xml_utils.SubElement(item, "codigo_servico_postagem", text=str(shipping_label.service))
        xml_utils.SubElement(item, "cubagem", text=str(Decimal('0.00')).replace(".", ","))
        xml_utils.SubElement(item, "peso", text=str(shipping_label.package.weight))
        xml_utils.SubElement(item, "rt1")
        xml_utils.SubElement(item, "rt2")

        receiver = shipping_label.receiver
        address = xml_utils.SubElement(item, "destinatario")
        xml_utils.SubElement(address, "nome_destinatario", cdata=str(receiver.name))
        xml_utils.SubElement(address, "telefone_destinatario", cdata=receiver.phone.short)
        xml_utils.SubElement(address, "celular_destinatario", cdata=receiver.cellphone.short)
        xml_utils.SubElement(address, "email_destinatario", cdata=str(receiver.email))
        xml_utils.SubElement(address, "logradouro_destinatario", cdata=str(receiver.street))
        xml_utils.SubElement(address, "complemento_destinatario", cdata=str(receiver.complement))
        xml_utils.SubElement(address, "numero_end_destinatario", text=str(receiver.number) or 'S/n')

        national = xml_utils.SubElement(item, "nacional")
        xml_utils.SubElement(national, "bairro_destinatario", cdata=str(receiver.neighborhood))
        xml_utils.SubElement(national, "cidade_destinatario", cdata=str(receiver.city)[:30])
        xml_utils.SubElement(national, "uf_destinatario", text=str(receiver.state))
        xml_utils.SubElement(national, "cep_destinatario", cdata=str(receiver.zip_code))
        xml_utils.SubElement(national, "codigo_usuario_postal")
        xml_utils.SubElement(national, "centro_custo_cliente")
        xml_utils.SubElement(national, "numero_nota_fiscal", text=str(shipping_label.invoice_number))
        xml_utils.SubElement(national, "serie_nota_fiscal", text=str(shipping_label.invoice_series))
        xml_utils.SubElement(national, "valor_nota_fiscal", text=str(shipping_label.value).replace(".", ","))
        xml_utils.SubElement(national, "natureza_nota_fiscal", text=str(shipping_label.invoice_type))
        xml_utils.SubElement(national, "descricao_objeto", cdata=str(shipping_label.text)[:20])
        xml_utils.SubElement(national, "valor_a_cobrar", text=str(shipping_label.billing).replace(".", ","))

        extra_services = xml_utils.SubElement(item, "servico_adicional")
        for extra_service in shipping_label.extra_services:
            xml_utils.SubElement(extra_services, "codigo_servico_adicional",
                                 text="{!s:>03}".format(extra_service.number))
        xml_utils.SubElement(extra_services, "valor_declarado", text=str(shipping_label.value).replace(".", ","))

        dimensions = xml_utils.SubElement(item, "dimensao_objeto")
        xml_utils.SubElement(dimensions, "tipo_objeto", text="{!s:>03}".format(shipping_label.package.package_type))
        xml_utils.SubElement(dimensions, "dimensao_altura", text=str(shipping_label.package.height))
        xml_utils.SubElement(dimensions, "dimensao_largura", text=str(shipping_label.package.width))
        xml_utils.SubElement(dimensions, "dimensao_comprimento", text=str(shipping_label.package.length))
        xml_utils.SubElement(dimensions, "dimensao_diametro", text=str(shipping_label.package.diameter))

        xml_utils.SubElement(item, "data_postagem_sara")
        xml_utils.SubElement(item, "status_processamento", text="0")
        xml_utils.SubElement(item, "numero_comprovante_postagem")
        xml_utils.SubElement(item, "valor_cobrado")

        return item

    def get_document(self, posting_list: PostingList):
        if not posting_list.shipping_labels:
            raise PostingListSerializerError("Cannot serialize an empty posting list")

        if posting_list.closed:
            raise PostingListSerializerError("Cannot serialize a closed posting list")

        root = xml_utils.Element("correioslog")
        root.append(xml_utils.Element("tipo_arquivo", text="Postagem"))
        root.append(xml_utils.Element("versao_arquivo", text="2.3"))
        root.append(self._get_posting_list_element(posting_list))
        root.append(self._get_sender_info_element(posting_list))
        root.append(xml_utils.Element("forma_pagamento"))

        for shipping_label in posting_list.shipping_labels.values():
            root.append(self._get_shipping_label_element(shipping_label))

        return root

    def validate(self, document):
        with open(os.path.join(DATADIR, "posting_list_schema.xsd")) as xsd:
            xsd_document = xml_utils.parse(xsd)
        schema = xml_utils.XMLSchema(xsd_document)
        return schema.assert_(document)

    def get_xml(self, document) -> bytes:
        xmlstring = str(xml_utils.tostring(document, encoding="unicode"))
        encoded_xmlstring = xmlstring.encode("iso-8859-1", errors='ignore')
        return b'<?xml version="1.0" encoding="ISO-8859-1"?>' + encoded_xmlstring


class Correios:
    PRODUCTION = "production"
    TEST = "test"

    def __init__(
        self,
        username,
        password,
        timeout=8,
        environment="production",
        wsdl_path=None
    ):

        # 'environment': ('url', 'ssl_verification')
        sigep_urls = {
            'production': (
                get_wsdl_path('AtendeCliente-production.wsdl', path=wsdl_path),
                True
            ),
            'test': (
                get_wsdl_path('AtendeCliente-test.wsdl', path=wsdl_path),
                False
            ),
        }
        websro_url = get_wsdl_path('Rastro.wsdl', path=wsdl_path)
        freight_url = get_wsdl_path('CalcPrecoPrazo.asmx', path=wsdl_path)

        self.username = username
        self.password = password
        self.timeout = timeout
        self.wsdl_path = wsdl_path

        url, verify = sigep_urls[environment]
        self.sigep_url = url
        self.sigep_verify = verify

        self.sigep_client = SoapClient(self.sigep_url, verify=self.sigep_verify, timeout=self.timeout)
        self.sigep = self.sigep_client.service

        self.websro_client = SoapClient(websro_url, timeout=self.timeout)
        self.websro = self.websro_client.service

        self.freight_client = SoapClient(freight_url, timeout=self.timeout)
        self.freight = self.freight_client.service

        self.model_builder = ModelBuilder()

    def _auth_call(self, method_name, *args, **kwargs):
        kwargs.update({
            "usuario": self.username,
            "senha": self.password,
        })
        return self._call(method_name, *args, **kwargs)

    def _call(self, method_name, *args, **kwargs):
        method = getattr(self.sigep, method_name)
        return method(*args, **kwargs)  # TODO: handle errors

    def get_user(self, contract_number: Union[int, str], posting_card_number: Union[int, str]) -> User:
        contract_number = str(contract_number)
        posting_card_number = str(posting_card_number)
        user_data = self._auth_call("buscaCliente", contract_number, posting_card_number)
        return self.model_builder.build_user(user_data)

    def find_zipcode(self, zip_code: Union[ZipCode, str]) -> ZipAddress:
        zip_address_data = self._call("consultaCEP", str(zip_code))
        return self.model_builder.build_zip_address(zip_address_data)

    def verify_service_availability(
        self,
        posting_card: PostingCard,
        service: Service,
        from_zip_code: Union[ZipCode, str],
        to_zip_code: Union[ZipCode, str]
    ) -> bool:
        from_zip_code = ZipCode.create(from_zip_code)
        to_zip_code = ZipCode.create(to_zip_code)
        result = self._auth_call("verificaDisponibilidadeServico",
                                 posting_card.administrative_code, str(service),
                                 str(from_zip_code), str(to_zip_code))
        return result

    def get_posting_card_status(self, posting_card: PostingCard) -> bool:
        result = self._auth_call("getStatusCartaoPostagem", posting_card.number)
        return self.model_builder.build_posting_card_status(result)

    def request_tracking_codes(self, user: User, service: Service, quantity=1, receiver_type="C") -> list:
        result = self._auth_call("solicitaEtiquetas",
                                 receiver_type, str(user.federal_tax_number),
                                 service.id, quantity)
        return self.model_builder.build_tracking_codes_list(result)

    def generate_verification_digit(self, tracking_codes: Sequence[str]) -> List[int]:
        tracking_codes = [TrackingCode(tc).nodigit for tc in tracking_codes]
        result = self._auth_call("geraDigitoVerificadorEtiquetas",
                                 tracking_codes)

        return result

    def get_post_info(self, number: int) -> PostInfo:
        result = self._auth_call('solicitaXmlPlp', number)

        data = xml_utils.fromstring(result.encode('iso-8859-1'))
        contract_number = data.remetente.numero_contrato.text  # type: ignore
        posting_card_number = data.plp.cartao_postagem.text  # type: ignore

        user = self.get_user(
            contract_number=contract_number,
            posting_card_number=posting_card_number
        )

        return self.model_builder.build_post_info(data=data, user=user, validate_package=False)

    def _generate_xml_string(self, posting_list: PostingList) -> str:
        posting_list_serializer = PostingListSerializer()
        document = posting_list_serializer.get_document(posting_list)
        posting_list_serializer.validate(document)
        xml = posting_list_serializer.get_xml(document)
        return xml.decode("ISO-8859-1")

    def close_posting_list(self, posting_list: PostingList, posting_card: PostingCard) -> PostingList:
        xml = self._generate_xml_string(posting_list)
        tracking_codes = posting_list.get_tracking_codes()

        id_ = self._auth_call("fechaPlpVariosServicos", xml,
                              posting_list.custom_id, posting_card.number, tracking_codes)
        posting_list.close_with_id(id_)

        return posting_list

    def get_tracking_code_events(self, tracking_list):
        if isinstance(tracking_list, (str, TrackingCode)):
            tracking_list = [tracking_list]

        tracking_codes = {}
        for tracking_code in tracking_list:
            tracking_code = TrackingCode.create(tracking_code)
            tracking_codes[tracking_code.code] = tracking_code

        response = self.websro.buscaEventosLista(
            self.username,
            self.password,
            "L",
            "T",
            "101",
            list(tracking_codes.keys())
        )

        return self.model_builder.load_tracking_events(tracking_codes, response)

    def calculate_freights(
        self,
        posting_card: PostingCard,
        services: List[Union[Service, int]],
        from_zip: Union[ZipCode, int, str], to_zip: Union[ZipCode, int, str],
        package: Package,
        value: Union[Decimal, float] = 0.00,
        extra_services: Optional[Sequence[Union[ExtraService, int]]] = None
    ):

        administrative_code = posting_card.administrative_code
        services = [Service.get(s) for s in services]
        from_zip = ZipCode.create(from_zip)
        to_zip = ZipCode.create(to_zip)

        if extra_services is None:
            extra_services = []
        else:
            extra_services = [ExtraService.get(es) for es in extra_services]

        response = self.freight.CalcPrecoPrazo(
            administrative_code,
            self.password,
            ",".join(str(s) for s in services),
            str(from_zip),
            str(to_zip),
            package.weight / KG,
            package.package_type,
            package.length,
            package.height,
            package.width,
            package.diameter,
            "S" if EXTRA_SERVICE_MP in extra_services else "N",
            value,
            "S" if EXTRA_SERVICE_AR in extra_services else "N",
        )
        return self.model_builder.build_freights_list(response)

    def calculate_delivery_time(
        self,
        service: Union[Service, int],
        from_zip: Union[ZipCode, int, str],
        to_zip: Union[ZipCode, int, str]
    ):
        service = Service.get(service)
        from_zip = ZipCode.create(from_zip)
        to_zip = ZipCode.create(to_zip)

        response = self.freight.CalcPrazo(str(service), str(from_zip), str(to_zip))
        return response.cServico[0].PrazoEntrega
