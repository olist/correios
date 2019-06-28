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


from datetime import datetime
from typing import Dict, Optional

from ..utils import to_decimal, to_integer
from .address import ReceiverAddress, SenderAddress, ZipAddress
from .posting import (
    EventStatus,
    FreightResponse,
    NotFoundTrackingEvent,
    Package,
    PostalUnit,
    PostInfo,
    PostingList,
    Receipt,
    ShippingLabel,
    TrackingCode,
    TrackingEvent,
)
from .user import Contract, ExtraService, FederalTaxNumber, PostingCard, Service, StateTaxNumber, User


class ModelBuilder:
    def build_service(self, service_data):
        service = Service(
            code=service_data.codigo,
            id=service_data.id,
            description=service_data.descricao,
            category=service_data.servicoSigep.categoriaServico,
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
            user=user, number=contract_data.contratoPK.numero, regional_direction=contract_data.codigoDiretoria
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
            complements=[zip_address_data.complemento, zip_address_data.complemento2],
        )
        return zip_address

    def build_post_info(self, data, user: User) -> PostInfo:
        post_info = PostInfo(
            postal_unit=self.build_postal_unit(data.plp),
            posting_list=self._load_posting_list(data=data, user=user),
            value=data.plp.valor_global,
        )
        return post_info

    def build_receipt(self, data) -> Optional[Receipt]:
        if (data.status_processamento == Receipt.STATUS_UNPROCESSED or data.status_processamento == ""):
            return None

        receipt = Receipt(
            number=data.numero_comprovante_postagem,
            post_date=data.data_postagem_sara.text,
            value=data.valor_cobrado.text,
        )
        return receipt

    def build_postal_unit(self, data) -> PostalUnit:
        postal_unit = PostalUnit(code=data.mcu_unidade_postagem, description=data.nome_unidade_postagem)
        return postal_unit

    def _load_posting_list(self, data, user: User) -> PostingList:
        contract_number = to_integer(data.remetente.numero_contrato)

        contract = next(c for c in user.contracts if c.number == contract_number)

        posting_card_number = str(data.plp.cartao_postagem.text)

        posting_card = next(p for p in contract.posting_cards if p.number == posting_card_number)

        posting_list = PostingList(custom_id=0)

        for postal_object in data.objeto_postal:

            posting_list.add_shipping_label(
                self._load_shipping_label(
                    data=postal_object,
                    posting_card=posting_card,
                    sender_address=self._load_sender_address(data.remetente),
                )
            )

        posting_list.close_with_id(data.plp.id_plp)

        return posting_list

    def _load_shipping_label(self, data, posting_card: PostingCard, sender_address: SenderAddress) -> ShippingLabel:

        declared_value = getattr(data.servico_adicional, "valor_declarado", None)
        extra_services_codes = list(data.servico_adicional.codigo_servico_adicional)
        extra_services = [ExtraService.get(code) for code in extra_services_codes if code]

        invoice_value = getattr(data.nacional, "valor_nota_fiscal", None)

        billing = getattr(data.nacional, "valor_a_cobrar", None) or "0.00"

        shipping_label = ShippingLabel(
            billing=to_decimal(billing),
            invoice_number=data.nacional.numero_nota_fiscal,
            invoice_series=data.nacional.serie_nota_fiscal,
            value=to_decimal(declared_value or invoice_value or "0.00"),
            text=data.nacional.descricao_objeto,
            posting_card=posting_card,
            sender=sender_address,
            receiver=self._load_receiver_address(data),
            package=self._load_package(data),
            service=Service.get(data.codigo_servico_postagem.text),
            tracking_code=data.numero_etiqueta.text,
            receipt=self.build_receipt(data),
        )

        shipping_label.add_extra_services(
            [extra_service for extra_service in extra_services if extra_service not in shipping_label.extra_services]
        )

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
            phone=data.telefone_remetente.text or "",
        )

        return sender_address

    def _load_receiver_address(self, data) -> ReceiverAddress:
        receiver_data = data.destinatario

        extra_data = data.nacional

        receiver_address = ReceiverAddress(
            email=getattr(receiver_data, "email_remetente", ""),
            name=receiver_data.nome_destinatario.text or "",
            street=receiver_data.logradouro_destinatario.text or "",
            number=receiver_data.numero_end_destinatario.text or "",
            complement=receiver_data.complemento_destinatario.text or "",
            neighborhood=extra_data.bairro_destinatario.text or "",
            zip_code=extra_data.cep_destinatario.text or "",
            city=extra_data.cidade_destinatario.text or "",
            state=extra_data.uf_destinatario.text or "",
            phone=receiver_data.celular_destinatario.text or "",
        )

        return receiver_address

    def _build_package_data(self, data):
        dimensions = data.dimensao_objeto

        if dimensions.tipo_objeto == Package.TYPE_BOX:
            package_data = {
                "height": dimensions.dimensao_altura.text,
                "length": dimensions.dimensao_comprimento.text,
                "weight": data.peso.text,
                "width": dimensions.dimensao_largura.text,
            }
        elif dimensions.tipo_objeto == Package.TYPE_CYLINDER:
            package_data = {
                "diameter": dimensions.dimensao_diametro.text,
                "length": dimensions.dimensao_comprimento.text,
                "weight": data.peso.text,
            }
        else:
            package_data = {"weight": data.peso.text}

        package_data = {k: float(v.replace(",", ".")) for (k, v) in package_data.items()}
        package_data["package_type"] = dimensions.tipo_objeto
        return package_data

    def _load_package(self, data) -> Package:
        package_data = self._build_package_data(data)
        package = Package(service=data.codigo_servico_postagem.text, **package_data)
        return package

    def build_posting_card_status(self, response):
        if response.lower() != "normal":
            return PostingCard.CANCELLED
        return PostingCard.ACTIVE

    def build_tracking_codes_list(self, response):
        codes = response.split(",")
        return TrackingCode.create_range(codes[0], codes[1])

    def _load_invalid_event(self, tracking_code: TrackingCode, tracked_object):
        event = NotFoundTrackingEvent(timestamp=datetime.utcnow(), comment=tracked_object.erro)
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

            if "erro" in tracked_object and tracked_object.erro:
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
        for service_data in response.cServico:
            freight = self.build_freight(service_data=service_data)
            result.append(freight)
        return result

    def build_freight(self, service_data) -> FreightResponse:
        return FreightResponse(
            service=Service.get(service_data.Codigo),
            delivery_time=int(service_data.PrazoEntrega),
            value=to_decimal(service_data.ValorSemAdicionais),
            declared_value=to_decimal(service_data.ValorValorDeclarado),
            mp_value=to_decimal(service_data.ValorMaoPropria),
            ar_value=to_decimal(service_data.ValorAvisoRecebimento),
            saturday=service_data.EntregaSabado and service_data.EntregaSabado.lower() == "s" or False,
            home=service_data.EntregaDomiciliar and service_data.EntregaDomiciliar.lower() == "s" or False,
            error_code=to_integer(service_data.Erro) or 0,
            error_message=service_data.MsgErro or "",
        )
