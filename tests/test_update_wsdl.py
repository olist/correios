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


import tempfile
from unittest import mock
from unittest.mock import call

from requests import HTTPError

from correios.update_wsdl import WSDLUpdater

from .vcr import vcr


def get_wsdl_updater(path):
    response_mock = mock.MagicMock()
    response_mock.text = "response value"
    session = mock.MagicMock()
    session.get.return_value = response_mock

    return WSDLUpdater(wsdl_path=path, session=session)


@vcr.use_cassette
def test_basic_update():
    with tempfile.TemporaryDirectory() as wsdl_path:
        wsdl_updater = WSDLUpdater(wsdl_path=wsdl_path)
        wsdl_updater.update_all()


def test_wsdl_updater_download():
    with tempfile.TemporaryDirectory() as wsdl_path:
        wsdl_updater = get_wsdl_updater(wsdl_path)
        wsdl_updater.download_wsdl('https://example.com/service.wsdl', 'service-production.wsdl')

    wsdl_updater.session.get.assert_called_once_with('https://example.com/service.wsdl')

    printed = wsdl_updater.output.getvalue()
    assert 'Updating file: service-production.wsdl URL: https://example.com/service.wsdl' in printed
    assert 'Successfully create file:' in printed
    assert 'Updated with success' in printed


def test_wsdl_update_all():
    with tempfile.TemporaryDirectory() as wsdl_path:
        wsdl_updater = get_wsdl_updater(wsdl_path)
        wsdl_updater.update_all()
        wsdl_updater.session.get.assert_has_calls([
            call('https://apps.correios.com.br/SigepMasterJPA/AtendeClienteService/AtendeCliente?wsdl'),
            call('https://apphom.correios.com.br/SigepMasterJPA/AtendeClienteService/AtendeCliente?wsdl'),
            call('https://webservice.correios.com.br/service/rastro/Rastro.wsdl'),
            call('http://ws.correios.com.br/calculador/CalcPrecoPrazo.asmx?WSDL'),
        ], any_order=True)


def test_wsdl_download_error():
    response_mock = mock.MagicMock()
    response_mock.text = "response value"
    session = mock.MagicMock()
    session.get.side_effect = HTTPError("test error")

    wsdl_updater = WSDLUpdater(wsdl_path="", session=session)
    wsdl_updater.update_all()

    printed = wsdl_updater.output.getvalue()
    assert ('Updating file: AtendeCliente-production.wsdl '
            'URL: https://apps.correios.com.br/SigepMasterJPA/AtendeClienteService/AtendeCliente?wsdl') in printed
    assert ("Error downloading https://apps.correios.com.br/SigepMasterJPA/AtendeClienteService/AtendeCliente?wsdl: "
            "test error") in printed
