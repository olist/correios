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

from correios.exceptions import InvalidAddressesException, InvalidVolumeInformation
from .data import SERVICES
from .user import Service
from .address import Address, TrackingCode


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
