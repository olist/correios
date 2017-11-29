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


import argparse
import os
import sys
from io import StringIO

from requests import HTTPError, Session

from .client import CORREIOS_WEBSERVICES
from .utils import get_resource_path

WSDL_DIR = get_resource_path("wsdls")


class WSDLUpdater:
    webservices = CORREIOS_WEBSERVICES

    def __init__(self, wsdl_path: str, session=None, output=None) -> None:
        self.wsdl_path = wsdl_path

        if session is None:
            session = Session()
        self.session = session

        if output is None:
            output = StringIO()
        self.output = output

    def out(self, msg):
        print(msg, file=self.output)

    def save(self, path: str, content: str):
        with open(path, 'w') as file:
            file.write(content)
        self.out('Successfully create file: {}'.format(path))

    def download_wsdl(self, url: str, filename: str):
        path = os.path.join(self.wsdl_path, filename)

        self.out('Updating file: {} URL: {}'.format(filename, url))

        response = self.session.get(url)
        response.raise_for_status()

        self.save(path, response.text)
        self.out('Updated with success')

    def update_all(self):
        self.out('Updating Correios Webservice WSDLs')
        self.out('Files will be saved on: {}'.format(self.wsdl_path))

        for webservice, args in self.webservices.items():
            url, filename = args
            try:
                self.download_wsdl(url, filename)
            except HTTPError as ex:
                self.out("Error downloading {}: {}".format(url, ex))


def cli():
    parser = argparse.ArgumentParser(description='Updates Correios WSDL files')
    parser.add_argument(
        '-q',
        '--quiet',
        dest='output',
        action='store_const',
        const=None,
        default=sys.stdout,
    )
    parser.add_argument(
        '-p',
        '--path',
        dest='wsdl_path',
        default=str(WSDL_DIR),
        help='Custom path where wsdl files will be saved.'
    )
    args = parser.parse_args()

    updater = WSDLUpdater(wsdl_path=args.wsdl_path, output=args.output)
    return updater.update_all()


if __name__ == '__main__':
    sys.exit(cli() or 0)
