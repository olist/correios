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
from requests.adapters import HTTPAdapter
from zeep import Client, Transport

logger = logging.getLogger(__name__)


class SoapClient(Client):

    def __init__(self, wsdl, cert=None, verify=True, timeout=8, **kwargs):
        session = Session()
        session.cert = cert
        session.verify = verify
        session.timeout = timeout

        session.mount('http', HTTPAdapter(max_retries=3))
        session.mount('https', HTTPAdapter(max_retries=3))

        session.headers['Content-Type'] = 'text/xml;charset=UTF-8'
        session.headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'  # noqa

        transport = Transport(
            operation_timeout=timeout,
            session=session
        )

        super().__init__(wsdl=wsdl, transport=transport, **kwargs)
