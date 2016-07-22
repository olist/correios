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

from PIL import Image as image

from correios import DATADIR
from correios.exceptions import (InvalidAddressesError, InvalidVolumeInformationError,
                                 InvalidTrackingCodeError, PostingListError, InvalidShippingLabelError)
from .address import Address
from .data import SERVICES
from .user import Service, ExtraService, PostingCard

TRACKING_CODE_SIZE = 13
TRACKING_CODE_NUMBER_SIZE = 8
TRACKING_CODE_PREFIX_SIZE = 2
TRACKING_CODE_SUFFIX_SIZE = 2
IATA_COEFICIENT = 6.0
VOLUMETRIC_WEIGHT_THRESHOLD = 10000  # g


class TrackingCode:
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
            raise InvalidTrackingCodeError("Invalid tracking code prefix {}".format(self.prefix))

        if len(self.suffix) != TRACKING_CODE_SUFFIX_SIZE or not self.suffix.isalpha():
            raise InvalidTrackingCodeError("Invalid tracking code suffix {}".format(self.suffix))

        if len(self.number) != TRACKING_CODE_NUMBER_SIZE or not self.number.isnumeric():
            raise InvalidTrackingCodeError("Invalid tracking code number {}".format(self.number))

        if self._digit is not None and self._digit != self.calculate_digit(self.number):
            raise InvalidTrackingCodeError("Invalid tracking code number {} or digit {} (must be {})".format(
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

    def __repr__(self):
        return "<TrackingCode code={!r}>".format(self.code)


class ShippingLabel:
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

    TYPE_ENVELOPE = 1
    TYPE_PACKAGE = 2
    TYPE_CYLINDER = 3

    def __init__(self,
                 posting_card: PostingCard,
                 sender: Address,
                 receiver: Address,
                 service: Union[Service, int],
                 tracking_code: Union[TrackingCode, str],
                 volume_type: int = TYPE_PACKAGE,
                 width: int = 0, height: int = 0, length: int = 0, weight: int = 0, diameter: int = 0,
                 extra_services: Optional[Sequence[Union[ExtraService, str, int]]] = None,
                 logo: Optional[Union[str, image.Image]] = None,
                 order: Optional[str] = "",
                 invoice_number: Optional[str] = "",
                 invoice_series: Optional[str] = "",
                 invoice_type: Optional[str] = "",
                 value: Optional[Decimal] = Decimal("0.00"),
                 billing: Optional[Decimal] = Decimal("0.00"),
                 volume_sequence: tuple = (1, 1),
                 text: Optional[str] = ""):

        if sender == receiver:
            raise InvalidAddressesError("Sender and receiver cannot be the same")

        if len(volume_sequence) != 2:
            raise InvalidVolumeInformationError("Volume must be a tuple with 2 elements: (number, total)")

        if isinstance(service, int):
            service = SERVICES[service]

        if isinstance(tracking_code, str):
            tracking_code = TrackingCode(tracking_code)

        if logo is None:
            logo = os.path.join(DATADIR, "default_logo.png")

        if isinstance(logo, str):
            logo = image.open(logo)

        if volume_type == ShippingLabel.TYPE_ENVELOPE:
            width, height, length, diameter = (0, 0, 0, 0)
        elif volume_type == ShippingLabel.TYPE_PACKAGE:
            diameter = 0
            width = min(105, max(11, width))
            height = min(105, max(2, height))
            length = min(105, max(16, length))
            if not all([width, height, length]):
                raise InvalidShippingLabelError("Incorrect package dimensions {}x{}x{}".format(width, height, length))
            if 200 < (width + height + length) < 29:
                raise InvalidShippingLabelError("Incorrect package dimensions {}x{}x{}".format(width, height, length))

        else:  # ShippingLabel.TYPE_CYLINDER
            width, height = (0, 0)
            if not all([length, diameter]):
                raise InvalidShippingLabelError("Incorrect cylinder dimensions {}x{}".format(length, diameter))
            if (length + 2 * diameter) > 28:
                raise InvalidShippingLabelError("Incorrect cylinder dimensions {}x{}".format(length, diameter))

        self.posting_card = posting_card
        self.sender = sender
        self.receiver = receiver
        self.service = service
        self.tracking_code = tracking_code
        self.width = width  # cm
        self.height = height  # cm
        self.length = length  # cm
        self.weight = weight  # in grams
        self.diameter = diameter  # in cm
        self.volume_type = volume_type
        self.logo = logo
        self.order = order
        self.invoice_number = invoice_number
        self.invoice_series = invoice_series
        self.invoice_type = invoice_type
        self.value = value
        self.billing = billing
        self.volume_sequence = volume_sequence
        self.text = text
        self.carrier_logo = image.open(self.carrier_logo)

        self.extra_services = []
        self.extra_services += service.default_extra_services
        if extra_services:
            self.extra_services += [ExtraService.get(es) for es in extra_services]

        self.posting_list = None

    def __repr__(self):
        return "<ShippingLabel tracking={!r}>".format(str(self.tracking_code))

    @property
    def symbol(self):
        return self.service.symbol_image

    @property
    def contract(self):
        return self.posting_card.contract

    @property
    def volumetric_weight(self):
        volumetric_weight = (self.width * self.height * self.length) / IATA_COEFICIENT
        if volumetric_weight <= VOLUMETRIC_WEIGHT_THRESHOLD:
            return self.weight
        return max(volumetric_weight, self.weight)

    def get_order(self):
        return self.order_template.format(self.order)

    def get_invoice(self):
        return self.invoice_template.format(self.invoice_number)

    def get_contract_number(self):
        return self.contract_number_template.format(self.posting_card.get_contract_number())

    def get_service_name(self):
        return self.service_name_template.format(self.service.display_name)

    def get_volume_sequence(self):
        return self.volume_template.format(*self.volume_sequence)

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
            "{!s:>08}".format(self.sender.zip_code),
            "{!s:>05}".format(self.sender.zip_code_complement),
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


class PostingList:
    def __init__(self,
                 id_: int):
        self.id = id_
        self.initial_shipping_label = None
        self.shipping_labels = {}

        # filled by the first shipping label
        self.closed = False
        self.posting_card = None
        self.contract = None
        self.sender = None

    def add_shipping_label(self, shipping_label: ShippingLabel):
        if not self.initial_shipping_label:
            self.initial_shipping_label = shipping_label
            self.posting_card = shipping_label.posting_card
            self.contract = shipping_label.contract
            self.sender = shipping_label.sender

        if shipping_label.tracking_code in self.shipping_labels:
            raise PostingListError("Shipping label {!r} already in posting list".format(shipping_label))

        if shipping_label.posting_card != self.posting_card:
            raise PostingListError("Invalid posting card: {} != {}".format(shipping_label.posting_card,
                                                                           self.posting_card))

        self.shipping_labels[shipping_label.tracking_code] = shipping_label
        shipping_label.posting_list = self

    def get_tracking_codes(self):
        return list(self.shipping_labels.keys())

    def close(self):
        self.closed = True
