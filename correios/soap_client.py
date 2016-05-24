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


import os
from io import StringIO

import requests
from suds.client import Client
from suds.transport import Reply
from suds.transport.http import HttpAuthenticated

from . import DATADIR


class RequestsTransport(HttpAuthenticated):
    def __init__(self, **kwargs):
        self._requests_session = requests.Session()
        self.cert = kwargs.pop('cert', None)
        HttpAuthenticated.__init__(self, **kwargs)

    def open(self, request):
        self.addcredentials(request)
        resp = self._requests_session.get(
            request.url,
            data=request.message,
            headers=request.headers,
            cert=self.cert,
            verify=True)
        result = StringIO(resp.content.decode('utf-8'))
        return result

    def send(self, request):
        self.addcredentials(request)
        resp = self._requests_session.post(
            request.url,
            data=request.message,
            headers=request.headers,
            cert=self.cert,
            verify=True
        )
        result = Reply(resp.status_code, resp.headers, resp.content)
        return result


class SoapClient(Client):
    def __init__(self, url, *args, **kwargs):
        cert = os.path.join(DATADIR, "correios.cert.pem")
        key = os.path.join(DATADIR, "correios.pub.pem")
        transport = RequestsTransport(cert=(cert, key))
        headers = {"Content-Type": "text/xml;charset=UTF-8", "SOAPAction": ""}
        super().__init__(url, transport=transport, headers=headers, **kwargs)
