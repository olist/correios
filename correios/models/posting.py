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
from decimal import Decimal
from typing import Optional, Union, Sequence

# noinspection PyPep8Naming
from PIL import Image as image

from correios import DATADIR
from correios.exceptions import InvalidAddressesException, InvalidVolumeInformation, InvalidTrackingCode
from .address import Address
from .data import SERVICES
from .user import Service, ExtraService, PostingCard

TRACKING_CODE_SIZE = 13
TRACKING_CODE_NUMBER_SIZE = 8
TRACKING_CODE_PREFIX_SIZE = 2
TRACKING_CODE_SUFFIX_SIZE = 2


class TrackingCode(object):
    def __init__(self, code: str):
        self.prefix = code[:2].upper()
        self.number = "".join(d for d in code[2:10] if d.isdigit())
        self.suffix = code[-2:].upper()
        self._digit = None

        if len(code) == TRACKING_CODE_SIZE and code[10:11] != " ":
            self._digit = int(code[10:11])

        self._validate()

    def _validate(self):
        if len(self.prefix) != TRACKING_CODE_PREFIX_SIZE or not self.prefix.isalpha():
            raise InvalidTrackingCode("Invalid tracking code prefix {}".format(self.prefix))

        if len(self.suffix) != TRACKING_CODE_SUFFIX_SIZE or not self.suffix.isalpha():
            raise InvalidTrackingCode("Invalid tracking code suffix {}".format(self.suffix))

        if len(self.number) != TRACKING_CODE_NUMBER_SIZE or not self.number.isnumeric():
            raise InvalidTrackingCode("Invalid tracking code number {}".format(self.number))

        if self._digit is not None and self._digit != self.calculate_digit(self.number):
            raise InvalidTrackingCode("Invalid tracking code number {} or digit {} (must be {})".format(
                self.number,
                self._digit,
                self.calculate_digit(self.number))
            )

    def calculate_digit(self, number: str) -> int:
        numbers = [int(c) for c in number if c.isdigit()]

        multipliers = [8, 6, 4, 2, 3, 5, 9, 7]
        module = sum(multipliers[i] * digit for i, digit in enumerate(numbers)) % 11

        if not module:
            return 5

        if module == 1:
            return 0

        return 11 - module

    @property
    def digit(self):
        if self._digit is None:
            self._digit = self.calculate_digit(self.number)
        return self._digit

    @property
    def code(self):
        return self.prefix + self.number + str(self.digit) + self.suffix

    @property
    def nodigit(self):
        return "{}{} {}".format(self.prefix, self.number, self.suffix)

    @property
    def short(self):
        return "{}{}{}".format(self.prefix, self.number, self.suffix)

    @property
    def splitted(self):
        code = self.code
        return "{!s} {!s} {!s} {!s} {!s}".format(code[:2], code[2:5], code[5:8], code[8:11], code[11:])

    def __str__(self):
        return self.code


class ShippingLabel(object):
    variable_data_identifier = 51  # Variable data identifier for package
    invoice_template = "{!s}"
    contract_number_template = "{!s}"
    order_template = "{!s}"
    service_name_template = "{!s}"
    volume_template = "{!s}/{!s}"
    weight_template = "{!s}"
    receipt_template = ("Recebedor: ___________________________________________<br/>"
                        "Assinatura: __________________ Documento: _______________")
    sender_header = "DESTINATÁRIO"
    carrier_logo = os.path.join(DATADIR, "carrier_logo.png")
    receiver_data_template = ("{receiver.name}<br/>"
                              "{receiver.street}, {receiver.number}<br/>"
                              "{receiver.complement} {receiver.neighborhood}<br/>"
                              "<b>{receiver.zip_code_display}</b> {receiver.city}/{receiver.state}")

    sender_data_template = ("<b>Remetente:</b> {sender.name}<br/>"
                            "{sender.street}, {sender.number}<br/>"
                            "{sender.complement} - {sender.neighborhood}<br/>"
                            "<b>{sender.zip_code_display}</b> {sender.city}-{sender.state}")

    def __init__(self,
                 posting_card: PostingCard,
                 sender: Address,
                 receiver: Address,
                 service: Union[Service, int],
                 tracking_code: Union[TrackingCode, str],
                 extra_services: Optional[Sequence[Union[ExtraService, str, int]]] = None,
                 logo: Optional[Union[str, image.Image]] = None,
                 order: Optional[str] = "",
                 invoice: Optional[str] = "",
                 value: Optional[Decimal] = None,
                 volume: tuple = (1, 1),
                 weight: int = 0,
                 text: Optional[str] = ""):

        self.posting_card = posting_card

        if sender == receiver:
            raise InvalidAddressesException("Sender and receiver cannot be the same")

        self.sender = sender
        self.receiver = receiver

        if isinstance(service, int):
            service = SERVICES[service]
        self.service = service

        self.extra_services = []
        self.extra_services += self.service.default_extra_services
        if extra_services:
            self.extra_services += [ExtraService.get(es) for es in extra_services]

        if isinstance(tracking_code, str):
            tracking_code = TrackingCode(tracking_code)
        self.tracking_code = tracking_code

        if logo is None:
            logo = os.path.join(DATADIR, "default_logo.png")

        if isinstance(logo, str):
            logo = image.open(logo)

        self.logo = logo

        self.order = order
        self.invoice = invoice

        if value is None:
            value = Decimal("0.00")
        self.value = value

        if len(volume) != 2:
            raise InvalidVolumeInformation("Volume must be a tuple with 2 elements: (number, total)")

        self.volume = volume
        self.weight = weight
        self.text = text
        self.carrier_logo = image.open(self.carrier_logo)

        self.posting_list = None  # TODO

    @property
    def symbol(self):
        return self.service.symbol_image

    def get_order(self):
        return self.order_template.format(self.order)

    def get_invoice(self):
        return self.invoice_template.format(self.invoice)

    def get_contract_number(self):
        return self.contract_number_template.format(self.posting_card.get_contract_number())

    def get_service_name(self):
        return self.service_name_template.format(self.service.display_name)

    def get_volume(self):
        return self.volume_template.format(*self.volume)

    def get_weight(self):
        return self.weight_template.format(self.weight)

    def get_symbol_filename(self, extension="gif"):
        return self.service.get_symbol_filename(extension)

    def get_tracking_code(self):
        return self.tracking_code.splitted

    def get_receiver_data(self):
        return self.receiver_data_template.format(receiver=self.receiver)

    def get_sender_data(self):
        return self.sender_data_template.format(sender=self.sender)

    def _get_extra_service_info(self) -> str:
        extra_services_numbers = ["00" for _ in range(6)]
        for i, extra_service in enumerate(self.extra_services[:6]):
            extra_services_numbers[i] = "{:02d}".format(extra_service.number)
        return "".join(extra_services_numbers)

    def get_datamatrix_info(self):
        parts = [
            "{!s:>08}".format(self.receiver.zip_code),
            "{!s:>05}".format(self.receiver.zip_code_complement),
            "{!s:>08}".format(self.receiver.zip_code),
            "{!s:>05}".format(self.receiver.zip_code_complement),
            "{!s:>01}".format(self.receiver.zip_code.digit),
            "{!s:>02}".format(self.variable_data_identifier),
            "{!s:>13}".format(self.tracking_code),
            "{!s:>12}".format(self._get_extra_service_info()),
            "{!s:>010}".format(self.posting_card.number),
            "{!s:>05}".format(self.service.code),
            "00",  # TODO: Posting listing group
            "{!s:>05}".format(self.receiver.number),
            "{!s:<20}".format(self.receiver.complement[:20]),
            "{!s:>05}".format(str(int(self.value * 100))),
            "{!s:>012}".format(str(self.receiver.phone)[:12] or "0" * 12),
            "-00.000000",  # TODO: latitude
            "-00.000000",  # TODO: longitude
            "|",
            "{!s:<30}".format(self.text[:30]),
        ]
        return "".join(parts)
