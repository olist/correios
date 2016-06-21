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


from .user import Service

SERVICE_LIST = [
    Service(id=104707, code=40215, description='SEDEX 10', category='SERVICO_COM_RESTRICAO', postal_code=244),
    Service(id=104672, code=81019, description='E-SEDEX STANDARD', category='SERVICO_COM_RESTRICAO', postal_code=275),
    Service(id=109819, code=41068, description='PAC', category='PAC', postal_code=201),
    Service(id=109811, code=40444, description='SEDEX - CONTRATO', category='SEDEX', postal_code=263),
    Service(id=109810, code=40436, description='SEDEX - CONTRATO', category='SEDEX', postal_code=263),
    Service(id=104625, code=40096, description='SEDEX (CONTRATO)', category='SEDEX', postal_code=263),
    Service(id=109806, code=40380, description='SEDEX REVERSO 40096', category='REVERSO', postal_code=740),
    Service(id=104295, code=40010, description='SEDEX A VISTA', category='SEDEX', postal_code=275),
    Service(id=113546, code=41211, description='PAC - CONTRATO', category='PAC', postal_code=201),
    Service(id=114976, code=40630, description='SEDEX PAGAMENTO NA ENTREGA -', category='SEDEX', postal_code=641),
    Service(id=118568, code=40916, description='SEDEX AGRUPADO II', category='SEDEX', postal_code=275),
    Service(id=118567, code=40908, description='SEDEX AGRUPADO I', category='SEDEX', postal_code=275),
    Service(id=120366, code=41300, description='PAC GRANDES FORMATOS', category='SERVICO_COM_RESTRICAO', postal_code=275),
    Service(id=115218, code=40169, description='SEDEX 12', category='SERVICO_COM_RESTRICAO', postal_code=263),
    Service(id=108934, code=40290, description='SEDEX HOJE', category='SERVICO_COM_RESTRICAO', postal_code=263),
    Service(id=118424, code=10154, description='CARTA COMERCIAL  REGISTRADA', category='CARTA_REGISTRADA', postal_code=275),
    Service(id=115487, code=41246, description='REM. CAMPANHA PAPAI NOEL DOS', category='SEM_CATEGORIA', postal_code=276),
    Service(id=115136, code=40150, description='SERVICO DE PROTOCOLO POSTAL -', category='SEDEX', postal_code=263),
    Service(id=109480, code=10065, description='CARTA COMERCIAL A FATURAR', category='CARTA_REGISTRADA', postal_code=275)
]

SERVICES = {s.code: s for s in SERVICE_LIST}
SERVICE_PAC = SERVICES[41068]
SERVICE_SEDEX = SERVICES[40096]
SERVICE_SEDEX10 = SERVICES[40215]
SERVICE_SEDEX12 = SERVICES[40169]
SERVICE_E_SEDEX = SERVICES[81019]
