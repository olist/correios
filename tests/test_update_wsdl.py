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


from unittest import mock

import requests

from correios.update_wsdl import WSDL_DIR, update_wsdl

FILE_BODY = 'Whatever'


@mock.patch('correios.update_wsdl.open', new_callable=mock.mock_open)
@mock.patch('requests.Response')
@mock.patch.object(requests, 'get')
def test_update_wsdl_success(
    mock_requests_get,
    mock_requests_response,
    mock_open
):
    mock_requests_response.text = FILE_BODY
    mock_requests_response.status_code = 200
    mock_requests_get.return_value = mock_requests_response

    update_wsdl()

    open_calls = [
        mock.call(
            '/'.join((WSDL_DIR, 'AtendeCliente-production.wsdl')), 'w+'
        ),
        mock.call('/'.join((WSDL_DIR, 'AtendeCliente-test.wsdl')), 'w+'),
        mock.call('/'.join((WSDL_DIR, 'Rastro.wsdl')), 'w+'),
        mock.call('/'.join((WSDL_DIR, 'CalcPrecoPrazo.asmx')), 'w+'),
        mock.call('/'.join((WSDL_DIR, 'Rastro_schema1.xsd')), 'w+'),
    ]

    mock_open.assert_has_calls(open_calls, any_order=True)

    mock_file = mock_open()

    mock_file.write.assert_called_with(FILE_BODY)
    assert mock_file.write.call_count == 5


@mock.patch('correios.update_wsdl.open', new_callable=mock.mock_open)
@mock.patch('requests.Response')
@mock.patch.object(requests, 'get')
def test_update_wsdl_fail(
    mock_requests_get,
    mock_requests_response,
    mock_open
):
    mock_requests_response.status_code = 500
    mock_requests_get.return_value = mock_requests_response

    update_wsdl()

    mock_open().assert_not_called()
