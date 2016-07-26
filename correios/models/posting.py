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
from datetime import datetime
from decimal import Decimal
from typing import Optional, Union, Sequence

from PIL import Image

from correios import DATADIR
from correios.exceptions import (InvalidAddressesError, InvalidVolumeInformationError,
                                 InvalidTrackingCodeError, PostingListError, InvalidDimensionsError)
from .address import Address, ZipCode
from .user import Service, ExtraService, PostingCard

TRACKING_CODE_SIZE = 13
TRACKING_CODE_NUMBER_SIZE = 8
TRACKING_CODE_PREFIX_SIZE = 2
TRACKING_CODE_SUFFIX_SIZE = 2
IATA_COEFICIENT = 6.0
VOLUMETRIC_WEIGHT_THRESHOLD = 10000  # g
MIN_WIDTH, MAX_WIDTH = 11, 105  # cm
MIN_HEIGHT, MAX_HEIGHT = 2, 105  # cm
MIN_LENGTH, MAX_LENGTH = 16, 105  # cm
MIN_DIAMETER, MAX_DIAMETER = 16, 91  # cm
MIN_CYLINDER_LENGTH, MAX_CYLINDER_LENGTH = 18, 105  # cm
MIN_SIZE, MAX_SIZE = 29, 200  # cm
MAX_CYLINDER_SIZE = 28


class EventStatus:
    def __init__(self, event_type: str, status: int):
        self.type = event_type
        self.status = status


class TrackingEvent:
    def __init__(self,
                 timestamp: datetime,
                 status: EventStatus,
                 location_zip_code: Union[str, ZipCode],
                 location: str = "",
                 receiver: str = "",
                 city: str = "",
                 state: str = "",
                 document: str = "",
                 comment: str = "",
                 ):
        self.timestamp = timestamp
        self.status = status
        self.location_zip_code = ZipCode.create(location_zip_code)
        self.location = location
        self.receiver = receiver
        self.city = city
        self.state = state
        self.document = document
        self.comment = comment


class TrackingCode:
    def __init__(self, code: str):
        self.prefix = code[:2].upper()
        self.number = "".join(d for d in code[2:10] if d.isdigit())
        self.suffix = code[-2:].upper()
        self._digit = None

        if len(code) == TRACKING_CODE_SIZE and code[10:11] != " ":
            self._digit = int(code[10:11])

        self._validate()

        # filled by tracking service
        self.category = None
        self.name = None
        self.initials = None
        self.events = []

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

    @classmethod
    def create(cls, tracking_code: Union[str, 'TrackingCode']):
        if isinstance(tracking_code, cls):
            return tracking_code
        return cls(tracking_code)

    @classmethod
    def calculate_digit(cls, number: str) -> int:
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

    def add_event(self, event: TrackingEvent):
        self.events.append(event)

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
    carrier_logo = os.path.join(DATADIR, "carrier_logo_bw.png")
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
                 logo: Optional[Union[str, Image.Image]] = None,
                 order: Optional[str] = "",
                 invoice_number: Optional[str] = "",
                 invoice_series: Optional[str] = "",
                 invoice_type: Optional[str] = "",
                 value: Optional[Decimal] = Decimal("0.00"),
                 billing: Optional[Decimal] = Decimal("0.00"),
                 volume_sequence: tuple = (1, 1),
                 text: Optional[str] = "",
                 latitude: Optional[float] = 0.0,
                 longitude: Optional[float] = 0.0):

        if sender == receiver:
            raise InvalidAddressesError("Sender and receiver cannot be the same")

        if len(volume_sequence) != 2:
            raise InvalidVolumeInformationError("Volume must be a tuple with 2 elements: (number, total)")

        if logo is None:
            logo = os.path.join(DATADIR, "default_logo.png")

        if isinstance(logo, str):
            logo = Image.open(logo)

        self.validate_dimensions(volume_type, width, height, length, diameter)

        self.posting_card = posting_card
        self.sender = sender
        self.receiver = receiver
        self.service = Service.get(service)
        self.tracking_code = TrackingCode.create(tracking_code)
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
        self.latitude = latitude
        self.longitude = longitude
        self.carrier_logo = Image.open(self.carrier_logo)

        self.extra_services = []
        self.extra_services += self.service.default_extra_services
        if extra_services:
            self.extra_services += [ExtraService.get(es) for es in extra_services]

        self.posting_list = None
        self.posting_list_group = 0

    @classmethod
    def calculate_volumetric_weight(cls, width, height, length):
        return int((width * height * length) / IATA_COEFICIENT)

    @classmethod
    def calculate_posting_weight(cls, weight, width, height, length):
        volumetric_weight = cls.calculate_volumetric_weight(width, height, length)
        if volumetric_weight <= VOLUMETRIC_WEIGHT_THRESHOLD:
            return weight
        return max(volumetric_weight, weight)

    @classmethod
    def validate_dimensions(cls, volume_type, width, height, length, diameter):
        if volume_type == ShippingLabel.TYPE_ENVELOPE:
            if any([width, height, length, diameter]):
                raise InvalidDimensionsError("Invalid envelope dimensions: {}x{}x{}".format(width, height, length))
            return

        if volume_type == ShippingLabel.TYPE_PACKAGE:
            if diameter:
                raise InvalidDimensionsError("Package does not use diameter: {}".format(diameter))

            if not MIN_WIDTH <= width <= MAX_WIDTH:
                raise InvalidDimensionsError("Invalid package width (range 11~105): {}".format(width))

            if not MIN_HEIGHT <= height <= MAX_HEIGHT:
                raise InvalidDimensionsError("Invalid package height (range 2~105): {}".format(height))

            if not MIN_LENGTH <= length <= MAX_LENGTH:
                raise InvalidDimensionsError("Invalid package length (range 16~105): {}".format(length))

            if not MIN_SIZE <= (width + height + length) <= MAX_SIZE:
                raise InvalidDimensionsError("Invalid package dimensions: {}x{}x{}".format(width, height, length))

            return

        # ShippingLabel.TYPE_CYLINDER
        if width or height:
            raise InvalidDimensionsError("Cylinder does not use width/height: {}x{}".format(width, height))

        if not MIN_CYLINDER_LENGTH <= length <= MAX_CYLINDER_LENGTH:
            raise InvalidDimensionsError("Invalid cylinder length (range 18~105): {}".format(length))

        if not MIN_DIAMETER <= diameter <= MAX_DIAMETER:
            raise InvalidDimensionsError("Invalid cylinder diameter (range 5~91): {}".format(diameter))

        if (length + 2 * diameter) > MAX_CYLINDER_SIZE:
            raise InvalidDimensionsError("Invalid cylinder dimensions: {}x{}".format(length, diameter))

    def __repr__(self):
        return "<ShippingLabel tracking={!r}>".format(str(self.tracking_code))

    @property
    def symbol(self):
        return self.service.symbol_image

    @property
    def contract(self):
        return self.posting_card.contract

    @property
    def posting_weight(self):
        return self.calculate_posting_weight(self.weight, self.width, self.height, self.length)

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
            "{!s:>02}".format(self.posting_list_group),
            "{!s:>05}".format(self.receiver.number),
            "{!s:<20}".format(self.receiver.complement[:20]),
            "{!s:>05}".format(str(int(self.value * 100))),
            "{!s:>012}".format(str(self.receiver.phone)[:12] or "0" * 12),
            "{:+010.6f}".format(self.latitude),
            "{:+010.6f}".format(self.longitude),
            "|",
            "{!s:<30}".format(self.text[:30]),
        ]
        return "".join(parts)


class PostingList:
    def __init__(self, custom_id: int):
        self.id = None  # will be filled by close_posting_list
        self.custom_id = custom_id
        self.shipping_labels = {}

        # filled by the first shipping label
        self.initial_shipping_label = None
        self.posting_card = None
        self.contract = None
        self.sender = None

    def add_shipping_label(self, shipping_label: ShippingLabel):
        if not self.initial_shipping_label:
            self.initial_shipping_label = shipping_label
            self.posting_card = shipping_label.posting_card
            self.contract = shipping_label.contract
            self.sender = shipping_label.sender

        if shipping_label.tracking_code.short in self.shipping_labels:
            raise PostingListError("Shipping label {!r} already in posting list".format(shipping_label))

        if shipping_label.posting_card != self.posting_card:
            raise PostingListError("Invalid posting card: {} != {}".format(shipping_label.posting_card,
                                                                           self.posting_card))
        self.shipping_labels[shipping_label.tracking_code.short] = shipping_label
        shipping_label.posting_list = self

    def get_tracking_codes(self):
        return list(self.shipping_labels.keys())

    def close_with_id(self, id_: int):
        self.id = id_

    @property
    def closed(self):
        return self.id is not None
