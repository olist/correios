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

from requests import Session
from zeep import Client, Transport

logger = logging.getLogger(__name__)


class SoapClient(Client):
    def __init__(self, wsdl, cert=None, verify=True, timeout=8, **kwargs):
        session = Session()
        session.cert = cert
        session.verify = verify
        session.timeout = timeout
        session.headers.update({'Content-Type': 'text/xml;charset=UTF-8'})

        transport = Transport(
            operation_timeout=timeout,
            session=session
        )

        super().__init__(wsdl=wsdl, transport=transport, **kwargs)
