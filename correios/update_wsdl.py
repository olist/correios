import logging
import os

import requests

logger = logging.getLogger(__name__)


MODULE_PATH = os.path.join(os.path.dirname(__file__), 'wsdls')


SPECS = [
    {
        'url': (
            'https://apps.correios.com.br/'
            'SigepMasterJPA/AtendeClienteService/AtendeCliente?wsdl'
        ),
        'filename': 'AtendeCliente-production.wsdl'
    },
    {
        'url': (
            'https://apphom.correios.com.br/'
            'SigepMasterJPA/AtendeClienteService/AtendeCliente?wsdl'
        ),
        'filename': 'AtendeCliente-test.wsdl'
    },
    {
        'url': (
            'https://webservice.correios.com.br/'
            'service/rastro/Rastro.wsdl'
        ),
        'filename': 'Rastro.wsdl'
    },
    {
        'url': (
            'http://ws.correios.com.br/'
            'calculador/CalcPrecoPrazo.asmx?WSDL'
        ),
        'filename': 'CalcPrecoPrazo.asmx'
    },
    {
        'url': (
            'https://webservice.correios.com.br/'
            'service/rastro/Rastro_schema1.xsd'
        ),
        'filename': 'Rastro_schema1.xsd'
    },
]


def create_file(filename, body, path):
    file_path = os.path.join(path, filename)
    logger.debug(
        'Creating file: {filename}\n'
        'Path: {path}'.format(filename=filename, path=path)
    )

    with open(file_path, 'w+') as file:
        file.truncate()
        file.write(body)

    logger.debug(
        'Successfully create file: {filename}'.format(filename=filename)
    )


def update_wsdl(path=MODULE_PATH):
    for file_spec in SPECS:
        logger.debug(
            'Updating File: {filename}'.format(**file_spec)
        )

        response = requests.get(file_spec['url'])

        if response.status_code != 200:
            logger.warning(
                'Fail to access Correios: {url}'.format(**file_spec)
            )
            continue

        create_file(file_spec['filename'], response.text, path=path)


if __name__ == '__main__':
    import sys

    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    update_wsdl()
