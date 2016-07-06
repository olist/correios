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


from typing import Optional, Union

from correios.exceptions import InvalidAddressesException, InvalidVolumeInformation, InvalidTrackingCode
from .data import SERVICES
from .user import Service
from .address import Address

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

    def __str__(self):
        return self.code


class ShippingLabel(object):
    def __init__(self,
                 sender: Address,
                 receiver: Address,
                 service: Union[Service, int],
                 tracking_code: Union[TrackingCode, str],
                 order: Optional[str] = "",
                 invoice: Optional[str] = "",
                 volume: tuple = (0, 0),
                 weight: int = 0,
                 text: Optional[str] = ""):

        if sender == receiver:
            raise InvalidAddressesException("Sender and receiver cannot be the same")

        self.sender = sender
        self.receiver = receiver

        if isinstance(service, int):
            service = SERVICES[service]
        self.service = service

        if isinstance(tracking_code, str):
            tracking_code = TrackingCode(tracking_code)
        self.tracking_code = tracking_code

        self.order = order
        self.invoice = invoice

        if volume is None:
            volume = (1, 1)

        if len(volume) != 2:
            raise InvalidVolumeInformation("Volume must be a tuple with 2 elements: (number, total)")

        self.volume = volume
        self.weight = weight
        self.text = text

    def get_order(self, template="{!s}"):
        return template.format(self.order)

    def get_invoice(self, template="{!s}"):
        return template.format(self.invoice)

    def get_volume(self, template="{}/{}"):
        return template.format(*self.volume)

    def get_symbol_filename(self, extension="gif"):
        return self.service.get_symbol_filename(extension)
