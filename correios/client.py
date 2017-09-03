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
from decimal import Decimal
from typing import Dict, List, Optional, Sequence, Union

from correios.exceptions import TrackingCodesLimitExceededError
from correios.models.data import EXTRA_SERVICE_AR, EXTRA_SERVICE_MP
from correios.utils import get_wsdl_path, to_decimal, to_integer

from .models.address import ZipAddress, ZipCode
from .models.posting import (
    EventStatus,
    Freight,
    FreightError,
    NotFoundTrackingEvent,
    Package,
    PostingList,
    TrackingCode,
    TrackingEvent
)
from .models.user import Contract, ExtraService, FederalTaxNumber, PostingCard, Service, StateTaxNumber, User
from .serializers import PostingListSerializer
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


class Correios:
    PRODUCTION = "production"
    TEST = "test"
    MAX_TRACKING_CODES_PER_REQUEST = 50

    # 'environment': ('url', 'ssl_verification')
    sigep_urls = {
        'production': (get_wsdl_path('AtendeCliente-production.wsdl'), True),
        'test': (get_wsdl_path('AtendeCliente-test.wsdl'), False),
    }
    websro_url = get_wsdl_path('Rastro.wsdl')
    freight_url = get_wsdl_path('CalcPrecoPrazo.asmx')

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

    def calculate_delivery_time(self,
                                service: Union[Service, int],
                                from_zip: Union[ZipCode, int, str],
                                to_zip: Union[ZipCode, int, str]):
        service = Service.get(service)
        from_zip = ZipCode.create(from_zip)
        to_zip = ZipCode.create(to_zip)

        response = self.freight.CalcPrazo(str(service), str(from_zip), str(to_zip))
        return response.cServico[0].PrazoEntrega
