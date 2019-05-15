from unittest import mock

import pytest

from .vcr import replace_auth, vcr


@pytest.fixture
def username():
    return "cuca"


@pytest.fixture
def password():
    return "beludo"


@pytest.fixture
def request_body(username, password):
    body = (
        "<?xml version=''1.0'' encoding=''utf-8''?>"
        '<soap-env:Envelope xmlns:soap-env="http://schemas.xmlsoap.org/soap/envelope/">'
        '<soap-env:Body><ns0:buscaEventosLista xmlns:ns0="http://resource.webservice.correios.com.br/">'
        "<usuario>{}</usuario><senha>{}senha><tipo>L</tipo><resultado>T</resultado><lingua>101</lingua>"
        "<objetos>JB683971943BR</objetos><objetos>JT365572014BR</objetos>"
        "</ns0:buscaEventosLista></soap-env:Body></soap-env:Envelope>"
        ""
    )
    body = body.format(username, password)
    return body.encode()


def test_replace_auth(request_body, username, password):
    request = mock.Mock(body=request_body)
    body = str(replace_auth(request))

    assert username not in body
    assert password not in body


def test_vcr_uses_replace_auth():
    assert vcr.before_record_request == replace_auth
