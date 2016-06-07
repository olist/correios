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


from .models.user import User, FederalTaxNumber, StateTaxNumber, Contract, PostingCard, Service
from .soap import SoapClient


class ModelBuilder(object):
    def build_service(self, service_data):
        service = Service(
            id=service_data.id,
            code=service_data.codigo,
            description=service_data.descricao,
            category=service_data.servicoSigep.categoriaServico,
            requires_dimensions=service_data.servicoSigep.exigeDimensoes,
            requires_payment=service_data.servicoSigep.exigeValorCobrar,
            postal_code=service_data.servicoSigep.ssiCoCodigoPostal,
            code_type1=service_data.tipo1Codigo,
            code_type2=service_data.tipo2Codigo,
            start_date=service_data.vigencia.dataInicial,
            end_date=service_data.vigencia.dataFinal,
        )
        return service

    def build_posting_card(self, posting_card_data):
        services = []
        for service_data in posting_card_data.servicos:
            service = self.build_service(service_data)
            services.append(service)

        posting_card = PostingCard(
            number=posting_card_data.numero,
            administrative_code=posting_card_data.codigoAdministrativo,
            start_date=posting_card_data.dataVigenciaInicio,
            end_date=posting_card_data.dataVigenciaFim,
            status=posting_card_data.statusCartaoPostagem,
            status_code=posting_card_data.statusCodigo,
            unit=posting_card_data.unidadeGenerica,
            services=services
        )
        return posting_card

    def build_contract(self, contract_data):
        posting_cards = []
        for posting_card_data in contract_data.cartoesPostagem:
            posting_card = self.build_posting_card(posting_card_data)
            posting_cards.append(posting_card)

        contract = Contract(
            number=contract_data.contratoPK.numero,
            customer_code=contract_data.codigoCliente,
            management_code=contract_data.codigoDiretoria,
            management_name=contract_data.descricaoDiretoriaRegional,
            status_code=contract_data.statusCodigo,
            start_date=contract_data.dataVigenciaInicio,
            end_date=contract_data.dataVigenciaFim,
            posting_cards=posting_cards,
        )
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

    def _call(self, method_name, *args, **kwargs):
        method = getattr(self.service, method_name)

        kwargs.update({
            "usuario": self.username,
            "senha": self.password,
        })

        # TODO: handle errors
        return method(*args, **kwargs)

    # TODO
    # def verify_service_availability(self,
    #                                 administrative_code: str,
    #                                 service_number: str,
    #                                 from_zip: Zip,
    #                                 to_zip: Zip):
    #     response = self._call("verificaDisponibilidadeServico",
    #                           int(administrative_code),
    #                           service_number,
    #                           str(from_zip),
    #                           str(to_zip),
    #                           self.username,
    #                           self.password)
    #
    #     return response

    def get_user(self, contract_data: str, card: str):
        user_data = self._call("buscaCliente", contract_data, card)
        return self.model_builder.build_user(user_data)
