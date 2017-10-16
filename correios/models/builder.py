from datetime import datetime
from typing import Dict

from correios.utils import to_decimal, to_integer

from .address import ZipAddress
from .posting import EventStatus, Freight, FreightError, NotFoundTrackingEvent, TrackingCode, TrackingEvent
from .user import Contract, FederalTaxNumber, PostingCard, Service, StateTaxNumber, User


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
        if response.lower() != 'normal':
            return PostingCard.CANCELLED
        return PostingCard.ACTIVE

    def build_tracking_codes_list(self, response):
        codes = response.split(',')
        return TrackingCode.create_range(codes[0], codes[1])

    def _load_invalid_event(self, tracking_code: TrackingCode, tracked_object):
        event = NotFoundTrackingEvent(
            timestamp=datetime.now(),
            comment=tracked_object.erro,
        )
        tracking_code.add_event(event)

    def _load_events(self, tracking_code: TrackingCode, events):
        for event in events:
            timestamp = datetime.strptime('{} {}'.format(event.data, event.hora), TrackingEvent.timestamp_format)
            event = TrackingEvent(
                timestamp=timestamp,
                status=EventStatus(event.tipo, event.status),
                location_zip_code=getattr(event, 'codigo', ''),
                location=getattr(event, 'local', ''),
                city=getattr(event, 'cidade', ''),
                state=getattr(event, 'uf', ''),
                receiver=getattr(event, 'recebedor', ''),
                document=getattr(event, 'documento', ''),
                comment=getattr(event, 'comentario', ''),
                description=getattr(event, 'descricao', ''),
                details=getattr(event, 'detalhes', ''),
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
        for service_data in response.cServico:
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
                saturday = service_data.EntregaSabado or ''
                home = service_data.EntregaDomiciliar or ''
                freight = Freight(
                    service=service,
                    delivery_time=delivery_time,
                    value=value,
                    declared_value=declared_value,
                    ar_value=ar_value,
                    mp_value=mp_value,
                    saturday=saturday.upper() == 'S',
                    home=home.upper() == 'S',
                )
            result.append(freight)
        return result
