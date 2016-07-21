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
from typing import Union, Sequence

from correios import xml_utils, DATADIR
from correios.exceptions import PostingListClosingError, PostingListSerializerError
from .models.address import ZipAddress, ZipCode
from .models.posting import TrackingCode, PostingList
from .models.user import User, FederalTaxNumber, StateTaxNumber, Contract, PostingCard, Service
from .soap import SoapClient

DEFAULT_TRACKING_CODE_QUANTITY = 2  # I tried 1, 2, N... and Correios always return 2 codes :/


class ModelBuilder:
    def build_service(self, service_data):
        service = Service(
            id=service_data.id,
            code=service_data.codigo,
            description=service_data.descricao,
            category=service_data.servicoSigep.categoriaServico,
            postal_code=service_data.servicoSigep.ssiCoCodigoPostal,
            start_date=service_data.vigencia.dataInicial,
            end_date=service_data.vigencia.dataFinal,
        )
        return service

    def build_posting_card(self, contract: Contract, posting_card_data):
        posting_card = PostingCard(
            contract=contract,
            number=posting_card_data.numero,
            administrative_code=posting_card_data.codigoAdministrativo,
            start_date=posting_card_data.dataVigenciaInicio,
            end_date=posting_card_data.dataVigenciaFim,
            status=posting_card_data.statusCartaoPostagem,
            status_code=posting_card_data.statusCodigo,
            unit=posting_card_data.unidadeGenerica,
        )

        for service_data in posting_card_data.servicos:
            service = self.build_service(service_data)
            posting_card.add_service(service)

        return posting_card

    def build_contract(self, contract_data):
        contract = Contract(
            number=contract_data.contratoPK.numero,
            customer_code=contract_data.codigoCliente,
            regional_direction=contract_data.codigoDiretoria,
            status_code=contract_data.statusCodigo,
            start_date=contract_data.dataVigenciaInicio,
            end_date=contract_data.dataVigenciaFim,
        )

        for posting_card_data in contract_data.cartoesPostagem:
            self.build_posting_card(contract, posting_card_data)

        return contract

    def build_user(self, user_data):
        contracts = []
        for contract_data in user_data.contratos:
            contract = self.build_contract(contract_data)
            contracts.append(contract)

        user = User(
            name=user_data.nome,
            federal_tax_number=FederalTaxNumber(user_data.cnpj),
            state_tax_number=StateTaxNumber(user_data.inscricaoEstadual),
            status_number=user_data.statusCodigo,
            contracts=contracts,
        )
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
        return [TrackingCode(c) for c in codes]


class PostingListSerializer:
    def __init__(self, posting_list: PostingList):
        self.posting_list = posting_list

    def _validate(self, xml):
        with open(os.path.join(DATADIR, "posting_list_schema.xsd")) as xsd:
            document = xml_utils.parse(xsd)
        schema = xml_utils.XMLSchema(document)
        return schema.validate(xml)

    def _get_posting_list_element(self):
        posting_list = xml_utils.Element("plp")
        xml_utils.SubElement(posting_list, "id_plp")
        xml_utils.SubElement(posting_list, "valor_global")
        xml_utils.SubElement(posting_list, "mcu_unidade_postagem")
        xml_utils.SubElement(posting_list, "nome_unidade_postagem")
        xml_utils.SubElement(posting_list, "cartao_postagem", text=str(self.posting_list.posting_card))
        return posting_list

    def _get_sender_info_element(self):
        sender = self.posting_list.sender
        posting_card = self.posting_list.posting_card
        contract = self.posting_list.contract

        sender_info = xml_utils.Element("remetente")
        xml_utils.SubElement(sender_info, "numero_contrato", text=str(contract.number))
        xml_utils.SubElement(sender_info, "diretoria", text=str(contract.regional_direction_number))
        xml_utils.SubElement(sender_info, "codigo_administrativo", text=str(posting_card.administrative_code))
        xml_utils.SubElement(sender_info, "nome_remetente", cdata=sender.name)
        xml_utils.SubElement(sender_info, "logradouro_remetente", cdata=sender.street)
        xml_utils.SubElement(sender_info, "numero_remetente", cdata=sender.number)
        xml_utils.SubElement(sender_info, "complemento_remetente", cdata=sender.complement)
        xml_utils.SubElement(sender_info, "bairro_remetente", cdata=sender.neighborhood)
        xml_utils.SubElement(sender_info, "cep_remetente", cdata=str(sender.zip_code))
        xml_utils.SubElement(sender_info, "cidade_remetente", cdata=str(sender.city))
        xml_utils.SubElement(sender_info, "uf_remetente", cdata=str(sender.state))
        xml_utils.SubElement(sender_info, "telefone_remetente", cdata=str(sender.phone))
        xml_utils.SubElement(sender_info, "fax_remetente", cdata="")
        xml_utils.SubElement(sender_info, "email_remetente", cdata=sender.email)
        return sender_info

    def _get_shipping_label_element(self, shipping_label):
        item = xml_utils.Element("objeto_postal")
        xml_utils.SubElement(item, "numero_etiqueta", text=str(shipping_label.tracking_code))
        xml_utils.SubElement(item, "codigo_objeto_cliente")
        return item

    def get_document(self, validate=True):
        if not self.posting_list.shipping_labels:
            raise PostingListSerializerError("Cannot serialize an empty posting list")

        if self.posting_list.closed:
            raise PostingListSerializerError("Cannot serialize a closed posting list")

        root = xml_utils.Element("correioslog")
        root.append(xml_utils.Element("tipo_arquivo", text="Postagem"))
        root.append(xml_utils.Element("versao_arquivo", text="2.3"))
        root.append(self._get_posting_list_element())
        root.append(self._get_sender_info_element())
        root.append(xml_utils.Element("forma_pagamento"))

        for shipping_label in self.posting_list.shipping_labels.values():
            root.append(self._get_shipping_label_element(shipping_label))

        if validate and not self._validate(root):
            raise PostingListSerializerError("Invalid posting list XML object")

        return root

    def get_xml(self, validate=True) -> bytes:
        return xml_utils.tostring(self.get_document(validate=validate))


class Correios:
    PRODUCTION = "production"
    TEST = "test"

    # 'environment': ('url', 'ssl_verification')
    environments = {
        'production': ("https://apps.correios.com.br/SigepMasterJPA/AtendeClienteService/AtendeCliente?wsdl", True),
        'test': ("https://apphom.correios.com.br/SigepMasterJPA/AtendeClienteService/AtendeCliente?wsdl", False),
    }

    def __init__(self, username, password, environment="production"):
        url, verify = self.environments[environment]
        self.url = url
        self.verify = verify

        self.username = username
        self.password = password

        self._soap_client = SoapClient(self.url, verify=self.verify)
        self.service = self._soap_client.service
        self.model_builder = ModelBuilder()

    def _auth_call(self, method_name, *args, **kwargs):
        kwargs.update({
            "usuario": self.username,
            "senha": self.password,
        })
        return self._call(method_name, *args, **kwargs)

    def _call(self, method_name, *args, **kwargs):
        method = getattr(self.service, method_name)
        return method(*args, **kwargs)  # TODO: handle errors

    def get_user(self, contract: str, posting_card: str):
        user_data = self._auth_call("buscaCliente", contract, posting_card)
        return self.model_builder.build_user(user_data)

    def find_zipcode(self, zip_code: Union[ZipCode, str]) -> ZipAddress:
        zip_address_data = self._call("consultaCEP", str(zip_code))
        return self.model_builder.build_zip_address(zip_address_data)

    def verify_service_availability(self,
                                    posting_card: PostingCard,
                                    service: Service,
                                    from_zip_code: Union[ZipCode, str],
                                    to_zip_code: Union[ZipCode, str]):
        from_zip_code = ZipCode(from_zip_code)
        to_zip_code = ZipCode(to_zip_code)
        result = self._auth_call("verificaDisponibilidadeServico",
                                 posting_card.administrative_code, str(service),
                                 str(from_zip_code), str(to_zip_code))
        return result

    def get_posting_card_status(self, posting_card: PostingCard):
        result = self._auth_call("getStatusCartaoPostagem", posting_card.number)
        return self.model_builder.build_posting_card_status(result)

    def request_tracking_codes(self, user: User, service: Service, receiver_type="C"):
        result = self._auth_call("solicitaEtiquetas",
                                 receiver_type, str(user.federal_tax_number),
                                 service.id, DEFAULT_TRACKING_CODE_QUANTITY)
        return self.model_builder.build_tracking_codes_list(result)

    def generate_verification_digit(self, tracking_codes: Sequence[str]):
        tracking_codes = [TrackingCode(tc).nodigit for tc in tracking_codes]
        result = self._auth_call("geraDigitoVerificadorEtiquetas",
                                 tracking_codes)

        return result

    def close_posting_list(self, posting_list: PostingList, posting_card: PostingCard) -> PostingList:
        posting_list_serializer = PostingListSerializer(posting_list)
        label_list = posting_list.get_tracking_codes()
        customer_id = self._auth_call("fechaPlpVariosServicos",
                                      posting_list_serializer.get_xml(),
                                      posting_list.id, posting_card.number,
                                      label_list)
        if customer_id != posting_list.id:
            raise PostingListClosingError("Returned customer id ({!r}) does not match "
                                          "requested ({!r})".format(customer_id, posting_list.id))

        posting_list.close()
        return posting_list
