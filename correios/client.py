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


from typing import Sequence

from .models.address import ZipCodeType, ZipAddress, TrackingCode
from .models.user import User, FederalTaxNumber, StateTaxNumber, Contract, PostingCard, Service
from .soap import SoapClient


class ModelBuilder(object):
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
            direction_code=contract_data.codigoDiretoria,
            direction=contract_data.descricaoDiretoriaRegional,
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


class Correios(object):
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

    def get_user(self, contract: str, card: str):
        user_data = self._auth_call("buscaCliente", contract, card)
        return self.model_builder.build_user(user_data)

    def find_zipcode(self, zip_code: ZipCodeType):
        zip_address_data = self._call("consultaCEP", str(zip_code))
        return self.model_builder.build_zip_address(zip_address_data)

    def verify_service_availability(self, posting_card: PostingCard, services: Sequence[Service], from_zip_code: ZipCodeType, to_zip_code: ZipCodeType):
        services = str(services[0].code)  # ",".join(str(s.code) for s in services)

        result = self._auth_call("verificaDisponibilidadeServico",
                                 posting_card.administrative_code, services,
                                 str(from_zip_code), str(to_zip_code))
        return result

    def get_posting_card_status(self, posting_card: PostingCard):
        result = self._auth_call("getStatusCartaoPostagem", posting_card.number)
        return self.model_builder.build_posting_card_status(result)

    def request_tracking_codes(self, user: User, service: Service, quantity: int=1, receiver_type="C"):
        result = self._auth_call("solicitaEtiquetas",
                                 receiver_type, str(user.federal_tax_number),
                                 service.id, quantity)
        return self.model_builder.build_tracking_codes_list(result)
