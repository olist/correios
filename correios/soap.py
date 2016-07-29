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
from io import BytesIO

import requests
from suds.client import Client
from suds.transport import Reply
from suds.transport.http import HttpAuthenticated


logger = logging.getLogger(__name__)


class RequestsTransport(HttpAuthenticated):
    def __init__(self, **kwargs):
        self._requests_session = requests.Session()
        self.cert = kwargs.pop('cert', None)
        self.verify = kwargs.pop('verify', True)
        self.timeout = kwargs.pop('timeout', 8)
        HttpAuthenticated.__init__(self, **kwargs)

    def open(self, request):
        self.addcredentials(request)
        logger.debug("request.open: %s", request)
        resp = self._requests_session.get(
            request.url,
            data=request.message,
            headers=request.headers,
            cert=self.cert,
            verify=self.verify,
            timeout=self.timeout,
        )
        result = BytesIO(resp.content)
        return result

    def send(self, request):
        self.addcredentials(request)
        logger.debug("request.send: %s", request)
        resp = self._requests_session.post(
            request.url,
            data=request.message,
            headers=request.headers,
            cert=self.cert,
            verify=self.verify,
            timeout=self.timeout,
        )
        result = Reply(resp.status_code, resp.headers, resp.content)
        return result


class SoapClient(Client):
    def __init__(self, url, cert=None, verify=True, timeout=8, *args, **kwargs):
        transport = RequestsTransport(cert=cert, verify=verify, timeout=timeout)
        headers = {"Content-Type": "text/xml;charset=UTF-8", "SOAPAction": ""}
        super().__init__(url, transport=transport, headers=headers, **kwargs)
