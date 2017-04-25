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
from datetime import datetime
from decimal import Decimal
from typing import Union, Sequence, List, Dict, Optional

from correios import xml_utils, DATADIR
from correios.exceptions import PostingListSerializerError, TrackingCodesLimitExceededError
from correios.models.data import EXTRA_SERVICE_MP, EXTRA_SERVICE_AR
from correios.utils import to_decimal, to_integer
from .models.address import ZipAddress, ZipCode
from .models.posting import (NotFoundTrackingEvent, TrackingCode, PostingList, ShippingLabel,
                             TrackingEvent, EventStatus, Package, Freight, FreightError)
from .models.user import User, FederalTaxNumber, StateTaxNumber, Contract, PostingCard, Service, ExtraService
from .soap import SoapClient

KG = 1000  # g


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
        posting_card.unit = posting_card_data.unidadeGenerica

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

    def build_posting_card_status(self, response):
        if response.lower() != "normal":
            return PostingCard.CANCELLED
        return PostingCard.ACTIVE

    def build_tracking_codes_list(self, response):
        codes = response.split(",")
        return TrackingCode.create_range(codes[0], codes[1])

    def _load_invalid_event(self, tracking_code: TrackingCode, tracked_object):
        event = NotFoundTrackingEvent(
            timestamp=datetime.now(),
            comment=tracked_object.erro,
        )
        tracking_code.add_event(event)

    def _load_events(self, tracking_code: TrackingCode, events):
        for event in events:
            timestamp = datetime.strptime("{} {}".format(event.data, event.hora), TrackingEvent.timestamp_format)
            event = TrackingEvent(
                timestamp=timestamp,
                status=EventStatus(event.tipo, event.status),
                location_zip_code=getattr(event, "codigo", ""),
                location=getattr(event, "local", ""),
                city=getattr(event, "cidade", ""),
                state=getattr(event, "uf", ""),
                receiver=getattr(event, "recebedor", ""),
                document=getattr(event, "documento", ""),
                comment=getattr(event, "comentario", ""),
                description=getattr(event, "descricao", ""),
                details=getattr(event, "detalhes", ""),
            )

            tracking_code.add_event(event)

    def load_tracking_events(self, tracking_codes: Dict[str, TrackingCode], response):
        result = []
        for tracked_object in response.objeto:
            tracking_code = tracking_codes[tracked_object.numero]

            if 'erro' in tracked_object:
                self._load_invalid_event(tracking_code, tracked_object)
            else:
                tracking_code.name = tracked_object.nome
                tracking_code.initials = tracked_object.sigla
                tracking_code.category = tracked_object.categoria
                self._load_events(tracking_code, tracked_object.evento)

            result.append(tracking_code)

        return result

    def build_freights_list(self, response):
        result = []
        for service_data in response.Servicos.cServico:
            service = Service.get(service_data.Codigo)
            error_code = to_integer(service_data.Erro)
            if error_code:
                freight = FreightError(
                    service=service,
                    error_code=error_code,
                    error_message=service_data.MsgErro,
                )
            else:
                delivery_time = int(service_data.PrazoEntrega)
                value = to_decimal(service_data.ValorSemAdicionais)
                declared_value = to_decimal(service_data.ValorValorDeclarado)
                ar_value = to_decimal(service_data.ValorAvisoRecebimento)
                mp_value = to_decimal(service_data.ValorMaoPropria)
                saturday = service_data.EntregaSabado or ""
                home = service_data.EntregaDomiciliar or ""
                freight = Freight(
                    service=service,
                    delivery_time=delivery_time,
                    value=value,
                    declared_value=declared_value,
                    ar_value=ar_value,
                    mp_value=mp_value,
                    saturday=saturday.upper() == "S",
                    home=home.upper() == "S",
                )
            result.append(freight)
        return result


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
        xml_utils.SubElement(sender_info, "nome_remetente", cdata=sender.name)
        xml_utils.SubElement(sender_info, "logradouro_remetente", cdata=sender.street)
        xml_utils.SubElement(sender_info, "numero_remetente", cdata=sender.number)
        xml_utils.SubElement(sender_info, "complemento_remetente", cdata=sender.complement)
        xml_utils.SubElement(sender_info, "bairro_remetente", cdata=sender.neighborhood)
        xml_utils.SubElement(sender_info, "cep_remetente", cdata=str(sender.zip_code))
        xml_utils.SubElement(sender_info, "cidade_remetente", cdata=str(sender.city)[:30])
        xml_utils.SubElement(sender_info, "uf_remetente", cdata=str(sender.state))
        xml_utils.SubElement(sender_info, "telefone_remetente", cdata=sender.phone.short)
        xml_utils.SubElement(sender_info, "fax_remetente", cdata="")
        xml_utils.SubElement(sender_info, "email_remetente", cdata=sender.email)
        return sender_info

    def _get_shipping_label_element(self, shipping_label: ShippingLabel):
        item = xml_utils.Element("objeto_postal")
        xml_utils.SubElement(item, "numero_etiqueta", text=str(shipping_label.tracking_code))
        xml_utils.SubElement(item, "codigo_objeto_cliente")
        xml_utils.SubElement(item, "codigo_servico_postagem", text=str(shipping_label.service))
        xml_utils.SubElement(item, "cubagem", text=str(shipping_label.posting_weight).replace(".", ","))
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
        xml_utils.SubElement(address, "numero_end_destinatario", text=str(receiver.number))

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
    MAX_TRACKING_CODES_PER_REQUEST = 50

    # 'environment': ('url', 'ssl_verification')
    sigep_urls = {
        'production': ("https://apps.correios.com.br/SigepMasterJPA/AtendeClienteService/AtendeCliente?wsdl", True),
        'test': ("https://apphom.correios.com.br/SigepMasterJPA/AtendeClienteService/AtendeCliente?wsdl", False),
    }
    websro_url = "https://webservice.correios.com.br/service/rastro/Rastro.wsdl"
    freight_url = "http://ws.correios.com.br/calculador/CalcPrecoPrazo.asmx?WSDL"

    def __init__(self, username, password, timeout=8, environment="production"):
        self.username = username
        self.password = password
        self.timeout = timeout

        url, verify = self.sigep_urls[environment]
        self.sigep_url = url
        self.sigep_verify = verify

        self.sigep_client = SoapClient(self.sigep_url, verify=self.sigep_verify, timeout=self.timeout)
        self.sigep = self.sigep_client.service

        self.websro_client = SoapClient(self.websro_url, timeout=self.timeout)
        self.websro = self.websro_client.service

        self.freight_client = SoapClient(self.freight_url, timeout=self.timeout)
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

    def verify_service_availability(self,
                                    posting_card: PostingCard,
                                    service: Service,
                                    from_zip_code: Union[ZipCode, str],
                                    to_zip_code: Union[ZipCode, str]) -> bool:
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

        if len(tracking_list) > Correios.MAX_TRACKING_CODES_PER_REQUEST:
            msg = '{} tracking codes requested exceeds the limit of {} stabilished by the Correios'
            msg = msg.format(len(tracking_list), Correios.MAX_TRACKING_CODES_PER_REQUEST)
            raise TrackingCodesLimitExceededError(msg)

        tracking_codes = {}
        for tracking_code in tracking_list:
            tracking_code = TrackingCode.create(tracking_code)
            tracking_codes[tracking_code.code] = tracking_code

        response = self.websro.buscaEventosLista(self.username, self.password, "L", "T", "101",
                                                 tuple(tracking_codes.keys()))
        return self.model_builder.load_tracking_events(tracking_codes, response)

    def calculate_freights(self,
                           posting_card: PostingCard,
                           services: List[Union[Service, int]],
                           from_zip: Union[ZipCode, int, str], to_zip: Union[ZipCode, int, str],
                           package: Package,
                           value: Union[Decimal, float] = 0.00,
                           extra_services: Optional[Sequence[Union[ExtraService, int]]] = None):

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
