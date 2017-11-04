import argparse
import logging
import sys

import os
import requests

logger = logging.getLogger(__name__)

WSDL_DIR = os.path.join(os.path.dirname(__file__), 'wsdls')


class WSDLDownloadError(Exception):
    pass


class WSDLUpdater:
    def __init__(self, wsdl_dir=WSDL_DIR):
        self.wsdl_dir = wsdl_dir


def create_file(path, filename, body):
    file_path = os.path.join(path, filename)
    logger.debug('Creating file: {} Path: {}'.format(filename, path))

    with open(file_path, 'w+') as file:
        file.truncate()
        file.write(body)

    logger.debug('Successfully create file: {}'.format(filename))


def update_wsdl(path=WSDL_DIR):
    for file_spec in SPECS:
        url = file_spec['url']
        filename = file_spec['filename']

        logger.debug('Updating File: {} URL: {}'.format(filename, url))

        response = requests.get(url)
        if response.status_code != 200:
            raise WSDLDownloadError('Fail to download Correios: {}'.format(url))

        create_file(path=path, filename=file_spec['filename'], body=response.text)


def cli():
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    update_wsdl()

    parser = argparse.ArgumentParser(description='Updates Correios WSDL files')
    parser.add_argument(
        '-p',
        '--path',
        dest='wsdl_path',
        default=WSDL_DIR,
        help='Custom path where wsdl files will be saved.'
    )
    args = parser.parse_args()

    print('Updating Correios WSDL')
    print('Files will be saved on: {path}'.format(path=args.wsdl_path))
    try:
        update_wsdl(path=args.wsdl_path)
        print('Updated with success')
    except Exception as error:
        print('Fail to update with error: {error}'.format(error=error))


if __name__ == '__main__':
    cli()
