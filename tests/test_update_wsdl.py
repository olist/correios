from unittest import mock

import requests

from correios.update_wsdl import MODULE_PATH, update_wsdl

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
            '/'.join((MODULE_PATH, 'AtendeCliente-production.wsdl')), 'w+'
        ),
        mock.call('/'.join((MODULE_PATH, 'AtendeCliente-test.wsdl')), 'w+'),
        mock.call('/'.join((MODULE_PATH, 'Rastro.wsdl')), 'w+'),
        mock.call('/'.join((MODULE_PATH, 'CalcPrecoPrazo.asmx')), 'w+'),
        mock.call('/'.join((MODULE_PATH, 'Rastro_schema1.xsd')), 'w+'),
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
