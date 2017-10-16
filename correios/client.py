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
from typing import List, Optional, Sequence, Union

from correios.exceptions import TrackingCodesLimitExceededError
from correios.models.data import EXTRA_SERVICE_AR, EXTRA_SERVICE_MP
from correios.utils import get_wsdl_path

from .models.address import ZipAddress, ZipCode
from .models.builder import ModelBuilder
from .models.posting import Package, PostingList, TrackingCode
from .models.user import ExtraService, PostingCard, Service, User
from .serializers import PostingListSerializer
from .soap import SoapClient

KG = 1000  # g


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
