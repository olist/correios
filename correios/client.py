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


import logging
import re
from decimal import Decimal
from pathlib import Path
from typing import List, Optional, Sequence, Union

from requests.exceptions import Timeout
from zeep.exceptions import Fault

from .exceptions import (
    AuthenticationError,
    CanceledPostingCardError,
    ClientError,
    ClosePostingListError,
    ConnectTimeoutError,
    NonexistentPostingCardError,
    TrackingCodesLimitExceededError,
)
from .models.address import ZipAddress, ZipCode
from .models.builders import ModelBuilder
from .models.data import EXTRA_SERVICE_AR, EXTRA_SERVICE_MP
from .models.posting import FreightResponse, Package, PostInfo, PostingList, TrackingCode
from .models.user import ExtraService, PostingCard, Service, User
from .serializers import PostingListSerializer
from .soap import SoapClient
from .utils import get_resource_path
from .xml_utils import fromstring

logger = logging.getLogger(__name__)

KG = 1000  # g
# environ servico url filename
CORREIOS_WEBSERVICES = {
    "sigep-production": (
        "https://apps.correios.com.br/SigepMasterJPA/AtendeClienteService/AtendeCliente?wsdl",
        "AtendeCliente-production.wsdl",
    ),
    "sigep-test": (
        "https://apphom.correios.com.br/SigepMasterJPA/AtendeClienteService/AtendeCliente?wsdl",
        "AtendeCliente-test.wsdl",
    ),
    "websro": ("https://webservice.correios.com.br/service/rastro/Rastro.wsdl", "Rastro.wsdl"),
    "freight": ("http://ws.correios.com.br/calculador/CalcPrecoPrazo.asmx?WSDL", "CalcPrecoPrazo.asmx"),
}

ERRORS = {
    re.compile(r"autenticacao"): AuthenticationError,
    re.compile(r"^O Cartão de Postagem.*Cancelado.$"): CanceledPostingCardError,
    re.compile(r"^Cartao de Postagem inexistente"): NonexistentPostingCardError,
}


class Correios:
    PRODUCTION = "production"
    TEST = "test"
    MAX_TRACKING_CODES_PER_REQUEST = 50

    def __init__(
        self,
        username: str,
        password: str,
        timeout: int = 8,
        environment: str = "production",
        local_wsdl_path: Optional[Path] = None,
    ) -> None:

        if local_wsdl_path is None:
            local_wsdl_path = get_resource_path("wsdls")
        self.local_wsdl_path = local_wsdl_path

        ssl_check = environment == "production"
        sigep_key = "sigep-{}".format(environment)
        if not self.local_wsdl_path:
            sigep_url = (CORREIOS_WEBSERVICES[sigep_key][0], ssl_check)
            websro_url = CORREIOS_WEBSERVICES["websro"][0]
            freight_url = CORREIOS_WEBSERVICES["freight"][0]
        else:
            sigep_url = (str(self.local_wsdl_path / CORREIOS_WEBSERVICES[sigep_key][1]), ssl_check)
            websro_url = str(self.local_wsdl_path / CORREIOS_WEBSERVICES["websro"][1])
            freight_url = str(self.local_wsdl_path / CORREIOS_WEBSERVICES["freight"][1])

        self.username = username
        self.password = password
        self.timeout = timeout

        self.sigep_url = sigep_url[0]
        self.sigep_verify = sigep_url[1]

        self.sigep_client = SoapClient(self.sigep_url, verify=self.sigep_verify, timeout=self.timeout)
        self.sigep = self.sigep_client.service

        self.websro_client = SoapClient(websro_url, timeout=self.timeout)
        self.websro = self.websro_client.service

        self.freight_client = SoapClient(freight_url, timeout=self.timeout)
        self.freight = self.freight_client.service

        self.model_builder = ModelBuilder()

    def _handle_exception(self, exception):
        message = str(exception)
        logger.debug("Caught error: {!r}".format(message))

        for regex, exception in ERRORS.items():
            if regex.search(message):
                raise exception(message)

        raise ClientError(message)

    def _auth_call(self, method_name, *args, **kwargs):
        kwargs.update({"usuario": self.username, "senha": self.password})
        return self._call(method_name, *args, **kwargs)

    def _call(self, method_name, *args, **kwargs):
        method = getattr(self.sigep, method_name)
        try:
            return method(*args, **kwargs)

        except Timeout:
            raise ConnectTimeoutError("Timeout connection error ({} seconds)".format(self.timeout))

        except Fault as exc:
            self._handle_exception(exc)

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
        to_zip_code: Union[ZipCode, str],
    ) -> bool:
        from_zip_code = ZipCode.create(from_zip_code)
        to_zip_code = ZipCode.create(to_zip_code)
        result = self._auth_call(
            "verificaDisponibilidadeServico",
            posting_card.administrative_code,
            str(service),
            str(from_zip_code),
            str(to_zip_code),
        )
        return result

    def get_posting_card_status(self, posting_card: PostingCard) -> bool:
        result = self._auth_call("getStatusCartaoPostagem", posting_card.number)
        return self.model_builder.build_posting_card_status(result)

    def request_tracking_codes(self, user: User, service: Service, quantity=1, receiver_type="C") -> list:
        result = self._auth_call("solicitaEtiquetas", receiver_type, str(user.federal_tax_number), service.id, quantity)
        return self.model_builder.build_tracking_codes_list(result)

    def generate_verification_digit(self, tracking_codes: Sequence[str]) -> List[int]:
        tracking_codes = [TrackingCode(tc).nodigit for tc in tracking_codes]
        result = self._auth_call("geraDigitoVerificadorEtiquetas", tracking_codes)

        return result

    def get_post_info(self, number: int) -> PostInfo:
        result = self._auth_call("solicitaXmlPlp", number)

        data = fromstring(result.encode("iso-8859-1"))
        contract_number = data.remetente.numero_contrato.text  # type: ignore
        posting_card_number = data.plp.cartao_postagem.text  # type: ignore

        user = self.get_user(contract_number=contract_number, posting_card_number=posting_card_number)

        return self.model_builder.build_post_info(data=data, user=user)

    def _generate_xml_string(self, posting_list: PostingList) -> str:
        posting_list_serializer = PostingListSerializer()
        xml = posting_list_serializer.serialize(posting_list)
        return xml.decode("ISO-8859-1")

    def close_posting_list(self, posting_list: PostingList, posting_card: PostingCard) -> PostingList:
        xml = self._generate_xml_string(posting_list)
        tracking_codes = posting_list.get_tracking_codes()

        try:
            id_ = self._auth_call(
                "fechaPlpVariosServicos", xml, posting_list.custom_id, posting_card.number, tracking_codes
            )
        except ClientError as exc:
            if str(exc).startswith("A PLP não será fechada"):
                message = "Unable to close PLP. Tracking codes {} are already assigned to another PLP"
                message = message.format(tracking_codes)
                raise ClosePostingListError(message)
            raise

        posting_list.close_with_id(id_)
        return posting_list

    def get_tracking_code_events(self, tracking_list):
        if isinstance(tracking_list, (str, TrackingCode)):
            tracking_list = [tracking_list]

        if len(tracking_list) > Correios.MAX_TRACKING_CODES_PER_REQUEST:
            msg = "{} tracking codes requested exceeds the limit of {} stabilished by the Correios"
            msg = msg.format(len(tracking_list), Correios.MAX_TRACKING_CODES_PER_REQUEST)
            raise TrackingCodesLimitExceededError(msg)

        tracking_codes = {}
        for tracking_code in tracking_list:
            tracking_code = TrackingCode.create(tracking_code)
            tracking_codes[tracking_code.code] = tracking_code

        response = self.websro.buscaEventosLista(
            self.username, self.password, "L", "T", "101", list(tracking_codes.keys())
        )
        return self.model_builder.load_tracking_events(tracking_codes, response)

    def calculate_freights(
        self,
        posting_card: PostingCard,
        services: List[Union[Service, int]],
        from_zip: Union[ZipCode, int, str],
        to_zip: Union[ZipCode, int, str],
        package: Package,
        value: Union[Decimal, float] = 0.00,
        extra_services: Optional[Sequence[Union[ExtraService, int]]] = None,
    ) -> List[FreightResponse]:

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
        self, service: Union[Service, int], from_zip: Union[ZipCode, int, str], to_zip: Union[ZipCode, int, str]
    ) -> int:
        service = Service.get(service)
        from_zip = ZipCode.create(from_zip)
        to_zip = ZipCode.create(to_zip)

        response = self.freight.CalcPrazo(str(service), str(from_zip), str(to_zip))
        return response.cServico[0].PrazoEntrega
