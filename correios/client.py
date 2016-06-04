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


from .models.user import User, FederalTaxNumber, StateTaxNumber, Contract, PostingCard
from .soap import SoapClient


class ModelBuilder(object):
    def build_posting_card(self, posting_card_data):
        posting_card = PostingCard(
            number=posting_card_data.numero,
            administrative_code=posting_card_data.codigoAdministrativo,
            start_date=posting_card_data.dataVigenciaInicio,
            end_date=posting_card_data.dataVigenciaFim,
            status=posting_card_data.statusCartaoPostagem,
            status_code=posting_card_data.statusCodigo,
            unit=posting_card_data.unidadeGenerica,
            services=[]  # TODO: implement this (last one?)
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


"""
   contratos[] =
         cartoesPostagem[] =
               codigoAdministrativo = "08082650  "
               dataAtualizacao = 2015-10-07 09:34:49-03:00
               dataVigenciaFim = 2018-05-16 00:00:00-03:00
               dataVigenciaInicio = 2014-05-09 00:00:00-03:00
               datajAtualizacao = 115280
               datajVigenciaFim = 118136
               datajVigenciaInicio = 114129
               horajAtualizacao = 93449
               numero = "0057018901"
               servicos[] =
                  (servicoERP){
                     codigo = "40215                    "
                     dataAtualizacao = 2014-05-05 13:47:35-03:00
                     datajAtualizacao = 114125
                     descricao = "SEDEX 10                      "
                     horajAtualizacao = 134735
                     id = 104707
                     servicoSigep =
                        (servicoSigep){
                           categoriaServico = "SERVICO_COM_RESTRICAO"
                           chancela =
                                 dataAtualizacao = 2013-05-03 00:00:00-03:00
                                 descricao = "(104707) SEDEX 10-D"
                                 id = 20
                              }
                           exigeDimensoes = False
                           exigeValorCobrar = False
                           imitm = 104707
                           servico = 104707
                           ssiCoCodigoPostal = "244"
                        }
                     servicosAdicionais[] = <empty>
                     tipo1Codigo = "CNV"
                     tipo2Codigo = "A"
                     vigencia =
                        (vigenciaERP){
                           dataFinal = 2040-12-31 00:00:00-02:00
                           dataInicial = 2001-06-10 00:00:00-03:00
                           datajFim = 140366
                           datajIni = 101161
                           id = 104707
                        }
                  },
                  (servicoERP){
                     codigo = "81019                    "
                     dataAtualizacao = 2014-05-14 11:13:24-03:00
                     datajAtualizacao = 114134
                     descricao = "E-SEDEX STANDARD              "
                     horajAtualizacao = 111324
                     id = 104672
                     servicoSigep =
                        (servicoSigep){
                           categoriaServico = "SERVICO_COM_RESTRICAO"
                           chancela =
                              (chancelaMaster){
                                 chancela = ""
                                 dataAtualizacao = 2012-08-16 00:00:00-03:00
                                 descricao = "(104672) E-SEDEX ST"
                                 id = 9
                              }
                           exigeDimensoes = False
                           exigeValorCobrar = False
                           imitm = 104672
                           servico = 104672
                           ssiCoCodigoPostal = "275"
                        }
                     servicosAdicionais[] = <empty>
                     tipo1Codigo = "CNV"
                     tipo2Codigo = "A"
                     vigencia =
                        (vigenciaERP){
                           dataFinal = 2040-12-31 00:00:00-02:00
                           dataInicial = 2000-08-22 00:00:00-03:00
                           datajFim = 140366
                           datajIni = 100235
                           id = 104672
                        }
                  },
                  (servicoERP){
                     codigo = "41068                    "
                     dataAtualizacao = 2014-05-08 08:38:13-03:00
                     datajAtualizacao = 114128
                     descricao = "PAC                           "
                     horajAtualizacao = 83813
                     id = 109819
                     servicoSigep =
                        (servicoSigep){
                           categoriaServico = "PAC"
                           chancela =
                              (chancelaMaster){
                                 chancela = ""
                                 dataAtualizacao = 2015-02-03 00:00:00-02:00
                                 descricao = "(113546) PAC - CONT"
                                 id = 38
                              }
                           exigeDimensoes = False
                           exigeValorCobrar = False
                           imitm = 109819
                           servico = 109819
                           ssiCoCodigoPostal = "201"
                        }
                     servicosAdicionais[] = <empty>
                     tipo1Codigo = "CNV"
                     tipo2Codigo = "A"
                     vigencia =
                        (vigenciaERP){
                           dataFinal = 2040-12-31 00:00:00-02:00
                           dataInicial = 2005-12-27 00:00:00-02:00
                           datajFim = 140366
                           datajIni = 105361
                           id = 109819
                        }
                  },
                  (servicoERP){
                     codigo = "40444                    "
                     dataAtualizacao = 2015-02-06 15:30:54-02:00
                     datajAtualizacao = 115037
                     descricao = "SEDEX - CONTRATO              "
                     horajAtualizacao = 153054
                     id = 109811
                     servicoSigep =
                        (servicoSigep){
                           categoriaServico = "SEDEX"
                           chancela =
                              (chancelaMaster){
                                 chancela = ""
                                 dataAtualizacao = 2013-04-19 00:00:00-03:00
                                 descricao = "(109811) SEDEX - CO"
                                 id = 17
                              }
                           exigeDimensoes = False
                           exigeValorCobrar = False
                           imitm = 109811
                           servico = 109811
                           ssiCoCodigoPostal = "263"
                        }
                     servicosAdicionais[] = <empty>
                     tipo1Codigo = "CNV"
                     tipo2Codigo = "A"
                     vigencia =
                        (vigenciaERP){
                           dataFinal = 2040-12-31 00:00:00-02:00
                           dataInicial = 2005-11-03 00:00:00-02:00
                           datajFim = 140366
                           datajIni = 105307
                           id = 109811
                        }
                  },
                  (servicoERP){
                     codigo = "40436                    "
                     dataAtualizacao = 2014-05-05 13:59:15-03:00
                     datajAtualizacao = 114125
                     descricao = "SEDEX - CONTRATO              "
                     horajAtualizacao = 135915
                     id = 109810
                     servicoSigep =
                        (servicoSigep){
                           categoriaServico = "SEDEX"
                           chancela =
                              (chancelaMaster){
                                 chancela = ""
                                 dataAtualizacao = 2013-04-19 00:00:00-03:00
                                 descricao = "(109810) SEDEX - CO"
                                 id = 18
                              }
                           exigeDimensoes = False
                           exigeValorCobrar = False
                           imitm = 109810
                           servico = 109810
                           ssiCoCodigoPostal = "263"
                        }
                     servicosAdicionais[] = <empty>
                     tipo1Codigo = "CNV"
                     tipo2Codigo = "A"
                     vigencia =
                        (vigenciaERP){
                           dataFinal = 2040-12-31 00:00:00-02:00
                           dataInicial = 2007-01-01 00:00:00-02:00
                           datajFim = 140366
                           datajIni = 107001
                           id = 109810
                        }
                  },
                  (servicoERP){
                     codigo = "40096                    "
                     dataAtualizacao = 2014-05-15 17:13:18-03:00
                     datajAtualizacao = 114135
                     descricao = "SEDEX (CONTRATO)              "
                     horajAtualizacao = 171318
                     id = 104625
                     servicoSigep =
                        (servicoSigep){
                           categoriaServico = "SEDEX"
                           chancela =
                              (chancelaMaster){
                                 chancela = ""
                                 dataAtualizacao = 2013-04-17 00:00:00-03:00
                                 descricao = "(104625) SEDEX - CO"
                                 id = 16
                              }
                           exigeDimensoes = False
                           exigeValorCobrar = False
                           imitm = 104625
                           servico = 104625
                           ssiCoCodigoPostal = "263"
                        }
                     servicosAdicionais[] = <empty>
                     tipo1Codigo = "CNV"
                     tipo2Codigo = "A"
                     vigencia =
                        (vigenciaERP){
                           dataFinal = 2040-12-31 00:00:00-02:00
                           dataInicial = 1997-01-02 00:00:00-02:00
                           datajFim = 140366
                           datajIni = 97002
                           id = 104625
                        }
                  },
                  (servicoERP){
                     codigo = "40380                    "
                     dataAtualizacao = 2014-05-05 13:53:57-03:00
                     datajAtualizacao = 114125
                     descricao = "SEDEX REVERSO 40096           "
                     horajAtualizacao = 135357
                     id = 109806
                     servicoSigep =
                        (servicoSigep){
                           categoriaServico = "REVERSO"
                           chancela =
                              (chancelaMaster){
                                 chancela = ""
                                 dataAtualizacao = 2013-03-25 00:00:00-03:00
                                 descricao = "(109806) SEDEX REVE"
                                 id = 6
                              }
                           exigeDimensoes = False
                           exigeValorCobrar = False
                           imitm = 109806
                           servico = 109806
                           ssiCoCodigoPostal = "740"
                        }
                     servicosAdicionais[] = <empty>
                     tipo1Codigo = "CNV"
                     tipo2Codigo = "A"
                     vigencia =
                        (vigenciaERP){
                           dataFinal = 2040-12-31 00:00:00-02:00
                           dataInicial = 2005-09-01 00:00:00-03:00
                           datajFim = 140366
                           datajIni = 105244
                           id = 109806
                        }
                  },
                  (servicoERP){
                     codigo = "40010                    "
                     dataAtualizacao = 2015-08-17 08:32:37-03:00
                     datajAtualizacao = 115229
                     descricao = "SEDEX A VISTA                 "
                     horajAtualizacao = 83237
                     id = 104295
                     servicoSigep =
                        (servicoSigep){
                           categoriaServico = "SEDEX"
                           chancela =
                              (chancelaMaster){
                                 chancela = ""
                                 dataAtualizacao = 2013-06-11 00:00:00-03:00
                                 descricao = "(104295) SEDEX A VI"
                                 id = 22
                              }
                           exigeDimensoes = False
                           exigeValorCobrar = False
                           imitm = 104295
                           servico = 104295
                           ssiCoCodigoPostal = "275"
                        }
                     servicosAdicionais[] = <empty>
                     tipo1Codigo = "CNV"
                     tipo2Codigo = "A"
                     vigencia =
                        (vigenciaERP){
                           dataFinal = 2020-12-01 00:00:00-02:00
                           dataInicial = 2001-03-18 00:00:00-03:00
                           datajFim = 120336
                           datajIni = 101077
                           id = 104295
                        }
                  },
                  (servicoERP){
                     codigo = "41211                    "
                     dataAtualizacao = 2014-09-16 10:26:34-03:00
                     datajAtualizacao = 114259
                     descricao = "PAC - CONTRATO                "
                     horajAtualizacao = 102634
                     id = 113546
                     servicoSigep =
                        (servicoSigep){
                           categoriaServico = "PAC"
                           chancela =
                              (chancelaMaster){
                                 chancela = ""
                                 dataAtualizacao = 2015-02-03 00:00:00-02:00
                                 descricao = "(113546) PAC - CONT"
                                 id = 38
                              }
                           exigeDimensoes = False
                           exigeValorCobrar = False
                           imitm = 113546
                           servico = 113546
                           ssiCoCodigoPostal = "201"
                        }
                     servicosAdicionais[] = <empty>
                     tipo1Codigo = "CNV"
                     tipo2Codigo = "A"
                     vigencia =
                        (vigenciaERP){
                           dataFinal = 2040-12-31 00:00:00-02:00
                           dataInicial = 2008-08-31 00:00:00-03:00
                           datajFim = 140366
                           datajIni = 108244
                           id = 113546
                        }
                  },
                  (servicoERP){
                     codigo = "40630                    "
                     dataAtualizacao = 2014-02-25 16:08:21-03:00
                     datajAtualizacao = 114056
                     descricao = "SEDEX PAGAMENTO NA ENTREGA -  "
                     horajAtualizacao = 160821
                     id = 114976
                     servicoSigep =
                        (servicoSigep){
                           categoriaServico = "SEDEX"
                           chancela =
                              (chancelaMaster){
                                 chancela = ""
                                 dataAtualizacao = 2014-01-27 00:00:00-02:00
                                 descricao = "(114976) SEDEX PAGA"
                                 id = 27
                              }
                           exigeDimensoes = False
                           exigeValorCobrar = False
                           imitm = 114976
                           servico = 114976
                           ssiCoCodigoPostal = "641"
                        }
                     servicosAdicionais[] = <empty>
                     tipo1Codigo = "CNV"
                     tipo2Codigo = "A"
                     vigencia =
                        (vigenciaERP){
                           dataFinal = 2040-12-31 00:00:00-02:00
                           dataInicial = 2009-09-11 00:00:00-03:00
                           datajFim = 140366
                           datajIni = 109254
                           id = 114976
                        }
                  },
                  (servicoERP){
                     codigo = "40916                    "
                     dataAtualizacao = 2012-07-23 09:57:56-03:00
                     datajAtualizacao = 112205
                     descricao = "SEDEX AGRUPADO II             "
                     horajAtualizacao = 95756
                     id = 118568
                     servicoSigep =
                        (servicoSigep){
                           categoriaServico = "SEDEX"
                           chancela =
                              (chancelaMaster){
                                 chancela = ""
                                 dataAtualizacao = 2014-04-14 00:00:00-03:00
                                 descricao = "(118568) SEDEX AGRU"
                                 id = 30
                              }
                           exigeDimensoes = False
                           exigeValorCobrar = False
                           imitm = 118568
                           servico = 118568
                           ssiCoCodigoPostal = "275"
                        }
                     servicosAdicionais[] = <empty>
                     tipo1Codigo = "CNV"
                     tipo2Codigo = "A"
                     vigencia =
                        (vigenciaERP){
                           dataFinal = 2040-12-31 00:00:00-02:00
                           dataInicial = 2012-01-04 00:00:00-02:00
                           datajFim = 140366
                           datajIni = 112004
                           id = 118568
                        }
                  },
                  (servicoERP){
                     codigo = "40908                    "
                     dataAtualizacao = 2014-02-25 16:15:44-03:00
                     datajAtualizacao = 114056
                     descricao = "SEDEX AGRUPADO I              "
                     horajAtualizacao = 161544
                     id = 118567
                     servicoSigep =
                        (servicoSigep){
                           categoriaServico = "SEDEX"
                           chancela =
                              (chancelaMaster){
                                 chancela = ""
                                 dataAtualizacao = 2014-04-14 00:00:00-03:00
                                 descricao = "(118567) SEDEX AGRU"
                                 id = 31
                              }
                           exigeDimensoes = False
                           exigeValorCobrar = False
                           imitm = 118567
                           servico = 118567
                           ssiCoCodigoPostal = "275"
                        }
                     servicosAdicionais[] = <empty>
                     tipo1Codigo = "CNV"
                     tipo2Codigo = "A"
                     vigencia =
                        (vigenciaERP){
                           dataFinal = 2040-12-31 00:00:00-02:00
                           dataInicial = 2012-01-04 00:00:00-02:00
                           datajFim = 140366
                           datajIni = 112004
                           id = 118567
                        }
                  },
                  (servicoERP){
                     codigo = "41300                    "
                     dataAtualizacao = 2014-02-25 16:37:12-03:00
                     datajAtualizacao = 114056
                     descricao = "PAC GRANDES FORMATOS          "
                     horajAtualizacao = 163712
                     id = 120366
                     servicoSigep =
                        (servicoSigep){
                           categoriaServico = "SERVICO_COM_RESTRICAO"
                           chancela =
                              (chancelaMaster){
                                 chancela = ""
                                 dataAtualizacao = 2014-05-26 00:00:00-03:00
                                 descricao = "(120366) PAC GRANDE"
                                 id = 33
                              }
                           exigeDimensoes = False
                           exigeValorCobrar = False
                           imitm = 120366
                           servico = 120366
                           ssiCoCodigoPostal = "275"
                        }
                     servicosAdicionais[] = <empty>
                     tipo1Codigo = "CNV"
                     tipo2Codigo = "A"
                     vigencia =
                        (vigenciaERP){
                           dataFinal = 2040-12-31 00:00:00-02:00
                           dataInicial = 2013-02-01 00:00:00-02:00
                           datajFim = 140366
                           datajIni = 113032
                           id = 120366
                        }
                  },
                  (servicoERP){
                     codigo = "40169                    "
                     dataAtualizacao = 2014-04-16 08:18:30-03:00
                     datajAtualizacao = 114106
                     descricao = "SEDEX 12                      "
                     horajAtualizacao = 81830
                     id = 115218
                     servicoSigep =
                        (servicoSigep){
                           categoriaServico = "SERVICO_COM_RESTRICAO"
                           chancela =
                              (chancelaMaster){
                                 chancela = ""
                                 dataAtualizacao = 2014-05-28 00:00:00-03:00
                                 descricao = "(115218) SEDEX 12"
                                 id = 34
                              }
                           exigeDimensoes = False
                           exigeValorCobrar = False
                           imitm = 115218
                           servico = 115218
                           ssiCoCodigoPostal = "263"
                        }
                     servicosAdicionais[] = <empty>
                     tipo1Codigo = "CNV"
                     tipo2Codigo = "A"
                     vigencia =
                        (vigenciaERP){
                           dataFinal = 2040-12-31 00:00:00-02:00
                           dataInicial = 2012-01-01 00:00:00-02:00
                           datajFim = 140366
                           datajIni = 112001
                           id = 115218
                        }
                  },
                  (servicoERP){
                     codigo = "40290                    "
                     dataAtualizacao = 2014-02-25 16:00:29-03:00
                     datajAtualizacao = 114056
                     descricao = "SEDEX HOJE                    "
                     horajAtualizacao = 160029
                     id = 108934
                     servicoSigep =
                        (servicoSigep){
                           categoriaServico = "SERVICO_COM_RESTRICAO"
                           chancela =
                              (chancelaMaster){
                                 chancela = ""
                                 dataAtualizacao = 2014-05-28 00:00:00-03:00
                                 descricao = "(108934) SEDEX HOJE"
                                 id = 35
                              }
                           exigeDimensoes = False
                           exigeValorCobrar = False
                           imitm = 108934
                           servico = 108934
                           ssiCoCodigoPostal = "263"
                        }
                     servicosAdicionais[] = <empty>
                     tipo1Codigo = "CNV"
                     tipo2Codigo = "A"
                     vigencia =
                        (vigenciaERP){
                           dataFinal = 2040-12-31 00:00:00-02:00
                           dataInicial = 2004-11-04 00:00:00-02:00
                           datajFim = 140366
                           datajIni = 104309
                           id = 108934
                        }
                  },
                  (servicoERP){
                     codigo = "10154                    "
                     dataAtualizacao = 2011-12-14 09:28:06-02:00
                     datajAtualizacao = 111348
                     descricao = "CARTA COMERCIAL  REGISTRADA   "
                     horajAtualizacao = 92806
                     id = 118424
                     servicoSigep =
                        (servicoSigep){
                           categoriaServico = "CARTA_REGISTRADA"
                           chancela =
                              (chancelaMaster){
                                 chancela = ""
                                 dataAtualizacao = 2014-06-20 00:00:00-03:00
                                 descricao = "(118424) CARTA COME"
                                 id = 36
                              }
                           exigeDimensoes = False
                           exigeValorCobrar = False
                           imitm = 118424
                           servico = 118424
                           ssiCoCodigoPostal = "275"
                        }
                     servicosAdicionais[] = <empty>
                     tipo1Codigo = "CNV"
                     tipo2Codigo = "A"
                     vigencia =
                        (vigenciaERP){
                           dataFinal = 2040-12-31 00:00:00-02:00
                           dataInicial = 2011-12-01 00:00:00-02:00
                           datajFim = 140366
                           datajIni = 111335
                           id = 118424
                        }
                  },
                  (servicoERP){
                     codigo = "41246                    "
                     dataAtualizacao = 2014-02-25 16:36:19-03:00
                     datajAtualizacao = 114056
                     descricao = "REM. CAMPANHA PAPAI NOEL DOS  "
                     horajAtualizacao = 163619
                     id = 115487
                     servicoSigep =
                        (servicoSigep){
                           categoriaServico = "SEM_CATEGORIA"
                           chancela =
                              (chancelaMaster){
                                 chancela = ""
                                 dataAtualizacao = 2014-07-10 00:00:00-03:00
                                 descricao = "(115487) REM. CAMPA"
                                 id = 37
                              }
                           exigeDimensoes = False
                           exigeValorCobrar = False
                           imitm = 115487
                           servico = 115487
                           ssiCoCodigoPostal = "276"
                        }
                     servicosAdicionais[] = <empty>
                     tipo1Codigo = "CNV"
                     tipo2Codigo = "A"
                     vigencia =
                        (vigenciaERP){
                           dataFinal = 2040-12-31 00:00:00-02:00
                           dataInicial = 2008-01-01 00:00:00-02:00
                           datajFim = 140366
                           datajIni = 108001
                           id = 115487
                        }
                  },
                  (servicoERP){
                     codigo = "40150                    "
                     dataAtualizacao = 2014-02-25 15:47:33-03:00
                     datajAtualizacao = 114056
                     descricao = "SERVICO DE PROTOCOLO POSTAL - "
                     horajAtualizacao = 154733
                     id = 115136
                     servicoSigep =
                        (servicoSigep){
                           categoriaServico = "SEDEX"
                           chancela =
                              (chancelaMaster){
                                 chancela = ""
                                 dataAtualizacao = 2015-03-16 00:00:00-03:00
                                 descricao = "(115136) SERVICO DE"
                                 id = 39
                              }
                           exigeDimensoes = False
                           exigeValorCobrar = False
                           imitm = 115136
                           servico = 115136
                           ssiCoCodigoPostal = "263"
                        }
                     servicosAdicionais[] = <empty>
                     tipo1Codigo = "CNV"
                     tipo2Codigo = "A"
                     vigencia =
                        (vigenciaERP){
                           dataFinal = 2040-12-31 00:00:00-02:00
                           dataInicial = 2007-01-01 00:00:00-02:00
                           datajFim = 140366
                           datajIni = 107001
                           id = 115136
                        }
                  },
                  (servicoERP){
                     codigo = "10065                    "
                     dataAtualizacao = 2012-10-05 00:08:53-03:00
                     datajAtualizacao = 112279
                     descricao = "CARTA COMERCIAL A FATURAR     "
                     horajAtualizacao = 120853
                     id = 109480
                     servicoSigep =
                        (servicoSigep){
                           categoriaServico = "CARTA_REGISTRADA"
                           chancela =
                              (chancelaMaster){
                                 chancela = ""
                                 dataAtualizacao = 2015-11-20 00:00:00-02:00
                                 descricao = "(109480) CARTA COME"
                                 id = 42
                              }
                           exigeDimensoes = False
                           exigeValorCobrar = False
                           imitm = 109480
                           servico = 109480
                           ssiCoCodigoPostal = "275"
                        }
                     servicosAdicionais[] = <empty>
                     tipo1Codigo = "CNV"
                     tipo2Codigo = "A"
                     vigencia =
                        (vigenciaERP){
                           dataFinal = 2040-05-01 00:00:00-03:00
                           dataInicial = 2005-10-18 00:00:00-02:00
                           datajFim = 140122
                           datajIni = 105291
                           id = 109480
                        }
                  },
               statusCartaoPostagem = "01"
               statusCodigo = "I"
               unidadeGenerica = "08        "
            },
         codigoCliente = 279311
         codigoDiretoria = "          10"
         contratoPK =
            (contratoERPPK){
               diretoria = 10
               numero = "9912208555  "
            }
         dataAtualizacao = 2014-11-19 09:50:29-02:00
         dataAtualizacaoDDMMYYYY = None
         dataVigenciaFim = 2018-05-16 00:00:00-03:00
         dataVigenciaFimDDMMYYYY = None
         dataVigenciaInicio = 2008-05-16 00:00:00-03:00
         dataVigenciaInicioDDMMYYYY = None
         datajAtualizacao = 114323
         datajVigenciaFim = 118136
         datajVigenciaInicio = 108137
         descricaoDiretoriaRegional = "DR - BRASÍLIA                 "
         horajAtualizacao = 95029
         statusCodigo = "A"
      },
 """
