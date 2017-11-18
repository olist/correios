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


from typing import Optional

from . import xml_utils
from .exceptions import PostingListSerializerError
from .models.posting import PostingList, ShippingLabel
from .utils import get_resource_path


class PostingListSerializer:
    def __init__(self, xsd_path: Optional[str] = None) -> None:
        if xsd_path is None:
            xsd_path = str(get_resource_path("posting_list_schema.xsd"))
        self.xsd_path = xsd_path

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

    def get_document(self, posting_list: PostingList) -> xml_utils.Element:
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

    def validate(self, document) -> None:
        with open(self.xsd_path) as xsd:
            xsd_document = xml_utils.parse(xsd)
        schema = xml_utils.XMLSchema(xsd_document)
        return schema.assertValid(document)

    def get_xml(self, document) -> bytes:
        xmlstring = str(xml_utils.tostring(document, encoding="unicode"))
        encoded_xmlstring = xmlstring.encode("iso-8859-1", errors='ignore')
        return b'<?xml version="1.0" encoding="ISO-8859-1"?>' + encoded_xmlstring

    def serialize(self, posting_list: PostingList) -> bytes:
        document = self.get_document(posting_list)
        self.validate(document)
        return self.get_xml(document)
