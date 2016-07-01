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


from typing import Optional

from correios.exceptions import InvalidAddressesException
from .address import Address


class ShippingLabel(object):
    def __init__(self,
                 sender: Address,
                 receiver: Address,
                 order: Optional[str] = "",
                 invoice: Optional[str] = "",
                 ):
        if sender == receiver:
            raise InvalidAddressesException("Sender and receiver cannot be the same")
        self.sender = sender
        self.receiver = receiver
        self.order = order
        self.invoice = invoice

    def get_order(self, template="{!s}"):
        return template.format(self.order)

    def get_invoice(self, template="{!s}"):
        return template.format(self.invoice)
