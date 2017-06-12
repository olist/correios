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
import math
from datetime import datetime, timedelta
from decimal import Decimal
from typing import Optional, Tuple, Union, List, Dict  # noqa: F401

from PIL import Image

from correios import DATADIR
from correios import exceptions
from correios.utils import to_decimal
from .address import Address, ZipCode
from .data import (INSURANCE_VALUE_THRESHOLD_PAC, INSURANCE_VALUE_THRESHOLD_SEDEX, INSURANCE_PERCENTUAL_COST,
                   SERVICE_PAC, SERVICE_SEDEX, TRACKING_EVENT_TYPES, TRACKING_STATUS)
from .user import Contract  # noqa: F401
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

INSURANCE_VALUE_THRESHOLDS = {
    Service.get(SERVICE_PAC).code: INSURANCE_VALUE_THRESHOLD_PAC,
    Service.get(SERVICE_SEDEX).code: INSURANCE_VALUE_THRESHOLD_SEDEX
}


class EventStatus:
    def __init__(self,
                 event_type: str,
                 status_code: Union[str, int]) -> None:
        event_type = event_type.upper()
        status_code = int(status_code)
        event_status_data = self._get_event_status_data(event_type, status_code)

        self.type = event_type
        self.status = status_code
        self.category = event_status_data[0]
        self.description = event_status_data[1]
        self.detail = event_status_data[2]
        self.action = event_status_data[3]

    def _get_event_status_data(self, event_type, status_code):
        if event_type not in TRACKING_EVENT_TYPES:
            raise exceptions.InvalidEventStatusError("{} is not valid".format(event_type))

        try:
            return TRACKING_STATUS[event_type, status_code]
        except KeyError:
            raise exceptions.InvalidEventStatusError("{} is not valid".format(event_type))

    @property
    def display_event_type(self):
        return TRACKING_EVENT_TYPES[self.type]

    def __str__(self):
        return '({}, {})'.format(self.type, self.status)

    def __repr__(self):
        return '<EventStatus({!r}, {!r})>'.format(self.type, self.status)


class ErrorEventStatus(EventStatus):
    def __init__(self):
        super().__init__("ERROR", 0)


class TrackingEvent:
    timestamp_format = "%d/%m/%Y %H:%M"

    def __init__(self,
                 timestamp: datetime,
                 status: Union[Tuple[str, Union[str, int]], EventStatus],
                 location_zip_code: Union[str, ZipCode] = "",
                 location: str = "",
                 receiver: str = "",
                 city: str = "",
                 state: str = "",
                 document: str = "",
                 comment: str = "",
                 description: str = "",
                 details: str = "",
                 ) -> None:
        self.timestamp = timestamp
        self.location = location
        self.receiver = receiver
        self.city = city
        self.state = state
        self.document = document
        self.comment = comment
        self.description = description
        self.details = details

        if location_zip_code:
            location_zip_code = ZipCode.create(location_zip_code)
        self.location_zip_code = location_zip_code

        if isinstance(status, tuple):
            status = EventStatus(*status)
        self.status = status

    def __str__(self):
        return '{} - {} - {}/{}'.format(self.description, self.location, self.city, self.state)

    def __repr__(self):
        timestamp = self.timestamp.strftime(self.timestamp_format)
        return '<TrackingEvent({!s}, {!s})>'.format(self.status, timestamp)


class NotFoundTrackingEvent(TrackingEvent):
    def __init__(self, timestamp: datetime, comment) -> None:
        super().__init__(timestamp=timestamp, status=ErrorEventStatus(), comment=comment)


class TrackingCode:
    def __init__(self, code: str) -> None:
        self.prefix = code[:2].upper()
        self.number = "".join(d for d in code[2:10] if d.isdigit())
        self.suffix = code[-2:].upper()
        self._digit = None

        if len(code) == TRACKING_CODE_SIZE and code[10:11] != " ":
            self._digit = int(code[10:11])

        self._validate()

        # filled by tracking service
        self.category = None  # type: Optional[str]
        self.name = None  # type: Optional[str]
        self.initials = None  # type: Optional[str]
        self.events = []  # type: List[TrackingEvent]

    def _validate(self):
        if len(self.prefix) != TRACKING_CODE_PREFIX_SIZE or not self.prefix.isalpha():
            raise exceptions.InvalidTrackingCodeError("Invalid tracking code prefix {}".format(self.prefix))

        if len(self.suffix) != TRACKING_CODE_SUFFIX_SIZE or not self.suffix.isalpha():
            raise exceptions.InvalidTrackingCodeError("Invalid tracking code suffix {}".format(self.suffix))

        if len(self.number) != TRACKING_CODE_NUMBER_SIZE or not self.number.isnumeric():
            raise exceptions.InvalidTrackingCodeError("Invalid tracking code number {}".format(self.number))

        if self._digit is not None and self._digit != self.calculate_digit(self.number):
            raise exceptions.InvalidTrackingCodeError("Invalid tracking code number {} or digit {} (must be {})".format(
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
        mod = sum(multipliers[i] * digit for i, digit in enumerate(numbers)) % 11

        if not mod:
            return 5

        if mod == 1:
            return 0

        return 11 - mod

    @classmethod
    def create_range(cls, start: Union[str, 'TrackingCode'], end: Union[str, 'TrackingCode']):
        if not isinstance(start, TrackingCode):
            start = TrackingCode(start)

        if not isinstance(end, TrackingCode):
            end = TrackingCode(end)

        if start.prefix != end.prefix:
            raise exceptions.InvalidTrackingCodeError(
                "Different tracking code prefixes: {} != {}".format(start.prefix, end.prefix)
            )

        if start.suffix != end.suffix:
            raise exceptions.InvalidTrackingCodeError(
                "Different tracking code suffixes: {} != {}".format(start.suffix, end.suffix)
            )

        start_number = int(start.number)
        end_number = int(end.number)

        if start_number > end_number:
            raise exceptions.InvalidTrackingCodeError(
                "Invalid range numbers: {} > {}".format(start_number, end_number)
            )

        code_range = range(int(start.number), int(end.number) + 1)
        return [TrackingCode(start.prefix + "{:08}".format(n) + start.suffix) for n in code_range]

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


class Package:
    TYPE_ENVELOPE = 1  # type: int
    TYPE_BOX = 2  # type: int
    TYPE_CYLINDER = 3  # type: int

    freight_package_types = {
        TYPE_BOX: 1,
        TYPE_CYLINDER: 2,
        TYPE_ENVELOPE: 3,
    }  # type: Dict[int, int]

    def __init__(self,
                 package_type: int = TYPE_BOX,
                 width: Union[float, int] = 0,  # cm
                 height: Union[float, int] = 0,  # cm
                 length: Union[float, int] = 0,  # cm
                 diameter: Union[float, int] = 0,  # cm
                 weight: Union[float, int] = 0,  # g
                 sequence=(1, 1),
                 service: Optional[Union[Service, str, int]] = None) -> None:

        if service:
            service = Service.get(service)

        Package.validate(package_type, width, height, length, diameter, service, weight)

        if len(sequence) != 2 or sequence[0] > sequence[1]:
            raise exceptions.InvalidPackageSequenceError("Package must be a tuple with 2 elements: (number, total)")

        self.package_type = package_type

        self.real_width = width  # cm
        self.real_height = height  # cm
        self.real_length = length  # cm
        self.real_diameter = diameter  # cm
        self.real_weight = weight  # g
        self.sequence = sequence
        self.service = service

    @property
    def width(self) -> int:
        return max(MIN_WIDTH, int(math.ceil(self.real_width)))

    @width.setter
    def width(self, width):
        Package._validate_dimension("width", width, MAX_WIDTH)
        self.real_width = width

    @property
    def height(self) -> int:
        return max(MIN_HEIGHT, int(math.ceil(self.real_height)))

    @height.setter
    def height(self, height):
        Package._validate_dimension("height", height, MAX_HEIGHT)
        self.real_height = height

    @property
    def length(self) -> int:
        return max(MIN_LENGTH, int(math.ceil(self.real_length)))

    @length.setter
    def length(self, length):
        Package._validate_dimension("length", length, MAX_LENGTH)
        self.real_length = length

    @property
    def diameter(self) -> int:
        return max(MIN_DIAMETER, int(math.ceil(self.real_diameter)))

    @diameter.setter
    def diameter(self, diameter):
        Package._validate_dimension("diameter", diameter, MAX_DIAMETER)
        self.real_diameter = diameter

    @property
    def weight(self) -> int:
        return int(math.ceil(self.real_weight))

    @weight.setter
    def weight(self, weight):
        Package._validate_weight(weight, self.service)
        self.real_weight = weight

    @property
    def volumetric_weight(self) -> int:
        return Package.calculate_volumetric_weight(self.width, self.height, self.length)

    @property
    def posting_weight(self) -> int:
        return Package.calculate_posting_weight(self.weight, self.volumetric_weight)

    @property
    def freight_package_type(self) -> int:
        """
        SIGEP API and Freight API different codes to identify package types:

        SIGEP | Freight | Type
        ------+---------+----------
          1   |    3    | Envelope
          2   |    1    | Box
          3   |    2    | Cylinder
        """
        return self.freight_package_types[self.package_type]

    @classmethod
    def calculate_volumetric_weight(cls, width, height, length) -> int:
        return int(math.ceil((width * height * length) / IATA_COEFICIENT))

    @classmethod
    def calculate_posting_weight(cls, weight, volumetric_weight) -> int:
        if volumetric_weight <= VOLUMETRIC_WEIGHT_THRESHOLD:
            return weight
        return int(math.ceil(max(volumetric_weight, weight)))

    @classmethod
    def calculate_insurance(cls,
                            per_unit_value: Union[int, float, Decimal],
                            quantity: int = 1,
                            service: Union[Service, int] = None) -> Decimal:
        value = Decimal("0.00")
        per_unit_value = Decimal(per_unit_value)
        insurance_value_threshold = INSURANCE_VALUE_THRESHOLDS.get(Service.get(service).code, per_unit_value)

        if per_unit_value > insurance_value_threshold:
            value = (per_unit_value - insurance_value_threshold) * INSURANCE_PERCENTUAL_COST

        return to_decimal(value * quantity)

    @classmethod
    def validate(cls,
                 package_type: int,
                 width: Union[float, int] = 0,
                 height: Union[float, int] = 0,
                 length: Union[float, int] = 0,
                 diameter: Union[float, int] = 0,
                 service: Optional[Union[Service, str, int]] = None,
                 weight: Union[float, int] = 0) -> None:

        width = int(math.ceil(width))
        height = int(math.ceil(height))
        length = int(math.ceil(length))
        diameter = int(math.ceil(diameter))
        weight = int(math.ceil(weight))

        if service:
            service = Service.get(service)

        Package._validate_weight(weight, service)

        if package_type == Package.TYPE_ENVELOPE:
            if any([width, height, length, diameter]):
                raise exceptions.InvalidPackageDimensionsError(
                    "Invalid dimensions: {}x{}x{}".format(width, height, length)
                )
            return

        if package_type == Package.TYPE_BOX:
            if diameter:
                raise exceptions.InvalidPackageDimensionsError(
                    "Package does not use diameter: {}".format(diameter)
                )

            cls._validate_dimension("width", width, MAX_WIDTH)
            cls._validate_dimension("height", height, MAX_HEIGHT)
            cls._validate_dimension("length", length, MAX_LENGTH)
            cls._validate_dimension("sum of dimensions", width + height + length, MAX_SIZE)
            return

        # Volume.TYPE_CYLINDER
        if width or height:
            raise exceptions.InvalidPackageDimensionsError(
                "Cylinder does not use width/height: {}x{}".format(width, height)
            )

        cls._validate_dimension("length", length, MAX_CYLINDER_LENGTH)
        cls._validate_dimension("diameter", diameter, MAX_DIAMETER)
        cls._validate_dimension("cylinder size", length + 2 * diameter, MAX_CYLINDER_SIZE)

    @classmethod
    def _validate_dimension(cls, name, value, maximum):
        msg = "Invalid {} (range 0~{}): {}".format(name, maximum, value)
        if value <= 0:
            raise exceptions.InvalidMinPackageDimensionsError(msg)

        if value > maximum:
            raise exceptions.InvalidMaxPackageDimensionsError(msg)

    @classmethod
    def _validate_weight(cls, weight, service: Optional[Union[Service, str, int]]=None) -> None:
        if weight <= 0:
            raise exceptions.InvalidMinPackageWeightError("Invalid weight {!r}g".format(weight))

        if not service:
            return

        service = Service.get(service)

        if service.max_weight is None:
            return

        if weight > service.max_weight:
            message = "Max weight exceeded for service {!r}: {!r}g (max. {!r}g)".format(
                weight,
                str(service),
                service.max_weight,
            )
            raise exceptions.InvalidMaxPackageWeightError(message)


class ShippingLabel:
    variable_data_identifier = 51  # Variable data identifier for package
    invoice_template = "{!s}"
    contract_number_template = "{!s}"
    order_template = "{!s}"
    service_name_template = "{!s}"
    package_template = "{!s}/{!s}"
    weight_template = "{!s}g"
    receipt_template = ("Recebedor: ___________________________________________<br/>"
                        "Assinatura: __________________ Documento: _______________")
    sender_header = "DESTINATÁRIO"
    carrier_logo = os.path.join(DATADIR, "carrier_logo_bw.png")
    receiver_data_template = ("{receiver.label_name!s:>.50}<br/>"
                              "{receiver.label_address!s:>.95}<br/>"
                              "<b>{receiver.zip_code_display}</b> {receiver.city}/{receiver.state}")

    sender_data_template = ("<b>Remetente:</b> {sender.label_name!s:>.40}<br/>"
                            "{sender.label_address!s:>.95}<br/>"
                            "<b>{sender.zip_code_display}</b> {sender.city}-{sender.state}")

    def __init__(self,
                 posting_card: PostingCard,
                 sender: Address,
                 receiver: Address,
                 service: Union[Service, int],
                 tracking_code: Union[TrackingCode, str],
                 package: Package,
                 extra_services: Optional[List[Union[ExtraService, int]]] = None,
                 logo: Optional[Union[str, Image.Image]] = None,
                 order: Optional[str] = "",
                 invoice_number: Optional[str] = "",
                 invoice_series: Optional[str] = "",
                 invoice_type: Optional[str] = "",
                 value: Optional[Decimal] = Decimal("0.00"),
                 billing: Optional[Decimal] = Decimal("0.00"),
                 text: Optional[str] = "",
                 latitude: Optional[float] = 0.0,
                 longitude: Optional[float] = 0.0) -> None:

        if sender == receiver:
            raise exceptions.InvalidAddressesError("Sender and receiver cannot be the same")

        if logo is None:
            logo = os.path.join(DATADIR, "default_logo.png")

        if isinstance(logo, str):
            logo = Image.open(logo)

        self.posting_card = posting_card
        self.sender = sender
        self.receiver = receiver
        self.service = Service.get(service)
        self.tracking_code = TrackingCode.create(tracking_code)
        self.package = package
        self.logo = logo
        self.order = order
        self.invoice_number = invoice_number
        self.invoice_series = invoice_series
        self.invoice_type = invoice_type
        self.real_value = value
        self.billing = billing
        self.text = text
        self.latitude = latitude
        self.longitude = longitude
        self.carrier_logo = Image.open(self.carrier_logo)

        self.extra_services = self.service.default_extra_services[:]
        if extra_services:
            self.add_extra_services(extra_services)

        self.posting_list = None  # type: Optional[PostingList]
        self.posting_list_group = 0

    def __repr__(self):
        return "<ShippingLabel tracking={!r}>".format(str(self.tracking_code))

    def add_extra_services(self, extra_services: List[Union["ExtraService", int]]):
        for extra_service in extra_services:
            self.add_extra_service(extra_service)

    def add_extra_service(self, extra_service: Union["ExtraService", int]):
        extra_service = ExtraService.get(extra_service)
        if extra_service.is_declared_value():
            self.service.validate_declared_value(self.value)
        self.extra_services.append(extra_service)

    @property
    def value(self) -> Decimal:
        return max(self.service.min_declared_value, self.real_value)

    @property
    def symbol(self):
        return self.service.symbol_image

    @property
    def contract(self):
        return self.posting_card.contract

    @property
    def posting_weight(self):
        return self.package.posting_weight

    def get_order(self):
        return self.order_template.format(self.order)

    def get_invoice(self):
        return self.invoice_template.format(self.invoice_number)

    def get_contract_number(self):
        return self.contract_number_template.format(self.posting_card.get_contract_number())

    def get_service_name(self):
        return self.service_name_template.format(self.service.display_name)

    def get_package_sequence(self):
        return self.package_template.format(*self.package.sequence)

    def get_weight(self):
        return self.weight_template.format(self.package.weight)

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
            "{!s:>05}".format(self.receiver.zip_complement),
            "{!s:>08}".format(self.sender.zip_code),
            "{!s:>05}".format(self.sender.zip_complement),
            "{!s:>01}".format(self.receiver.zip_code.digit),
            "{!s:>02}".format(self.variable_data_identifier),
            "{!s:>13}".format(self.tracking_code),
            "{!s:>12}".format(self._get_extra_service_info()),
            "{!s:>010}".format(self.posting_card.number),
            "{!s:>05}".format(self.service.code),
            "{!s:>02}".format(self.posting_list_group),
            "{!s:>05}".format(self.receiver.number),
            "{!s:<20}".format(self.receiver.complement[:20]),
            "{!s:>05}".format(0 if self.value is None else int(self.value * 100)),
            "{!s:>012}".format(str(self.receiver.phone)[:12] or "0" * 12),
            "{:+010.6f}".format(self.latitude),
            "{:+010.6f}".format(self.longitude),
            "|",
            "{!s:<30}".format(self.text[:30]),
        ]
        return "".join(parts)

    def __contains__(self, extra_service: ExtraService):
        return extra_service in self.extra_services


class PostingList:
    def __init__(self, custom_id: int, logo: Optional[Union[str, Image.Image]] = None) -> None:
        # will be filled by close_posting_list
        self.number = None  # type: Optional[int]

        if logo is None:
            logo = os.path.join(DATADIR, "carrier_logo.png")

        if isinstance(logo, str):
            logo = Image.open(logo)

        self.logo = logo
        self.custom_id = custom_id
        self.shipping_labels = {}  # type: Dict[str, ShippingLabel]

        # filled by the first shipping label
        self.initial_shipping_label = None  # type: Optional[ShippingLabel]
        self.posting_card = None  # type: PostingCard
        self.contract = None  # type: Contract
        self.sender = None  # type: Address

    def add_shipping_label(self, shipping_label: ShippingLabel):
        if not self.initial_shipping_label:
            self.initial_shipping_label = shipping_label
            self.posting_card = shipping_label.posting_card
            self.contract = shipping_label.contract
            self.sender = shipping_label.sender

        if shipping_label.tracking_code.short in self.shipping_labels:
            raise exceptions.PostingListError("Shipping label {!r} already in posting list".format(shipping_label))

        if shipping_label.posting_card != self.posting_card:
            raise exceptions.PostingListError(
                "Invalid posting card: {} != {}".format(shipping_label.posting_card, self.posting_card)
            )
        self.shipping_labels[shipping_label.tracking_code.short] = shipping_label
        shipping_label.posting_list = self

    def get_tracking_codes(self):
        return list(self.shipping_labels.keys())

    def close_with_id(self, number: int):
        self.number = number

    @property
    def closed(self):
        return self.number is not None


class Freight:
    def __init__(self,
                 service: Union[Service, int],
                 delivery_time: Union[int, timedelta],
                 value: Union[Decimal, float, int, str],
                 declared_value: Union[Decimal, float, int, str] = 0.00,
                 mp_value: Union[Decimal, float, int, str] = 0.00,
                 ar_value: Union[Decimal, float, int, str] = 0.00,
                 saturday: bool = False,
                 home: bool = False) -> None:

        self.service = Service.get(service)

        if not isinstance(delivery_time, timedelta):
            delivery_time = timedelta(days=delivery_time)
        self.delivery_time = delivery_time

        if not isinstance(value, Decimal):
            value = to_decimal(value)
        self.value = value

        if not isinstance(declared_value, Decimal):
            declared_value = to_decimal(declared_value)
        self.declared_value = declared_value

        if not isinstance(mp_value, Decimal):
            mp_value = to_decimal(mp_value)
        self.mp_value = mp_value

        if not isinstance(ar_value, Decimal):
            ar_value = to_decimal(ar_value)
        self.ar_value = ar_value

        self.saturday = saturday
        self.home = home
        self.error_code = 0
        self.error_message = ""

    @property
    def total(self):
        return self.value + self.declared_value + self.ar_value + self.mp_value


class FreightError(Freight):
    def __init__(self,
                 service: Union[Service, int],
                 error_code: Union[str, int],
                 error_message: str) -> None:
        super().__init__(service=service, delivery_time=0, value=Decimal("0.00"))
        self.error_code = int(error_code)
        self.error_message = error_message
