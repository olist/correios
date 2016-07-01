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


import pytest

from correios.exceptions import InvalidAddressesException
from correios.models.posting import ShippingLabel


def test_basic_shipping_label(sender_address, receiver_address):
    shipping_label = ShippingLabel(
        sender=sender_address,
        receiver=receiver_address,
        order="123",
        invoice="321",
    )

    assert shipping_label.sender == sender_address
    assert shipping_label.receiver == receiver_address
    assert shipping_label.get_order() == "123"
    assert shipping_label.get_order("Order: {}") == "Order: 123"
    assert shipping_label.get_invoice() == "321"
    assert shipping_label.get_invoice("Invoice #{}") == "Invoice #321"


def test_fail_shipping_label_same_addresses(sender_address):
    with pytest.raises(InvalidAddressesException):
        ShippingLabel(sender_address, sender_address)
