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

import pytest

from correios import DATADIR
from correios.exceptions import InvalidAddressesException
from correios.models.posting import ShippingLabel
from correios.models.data import SERVICE_SEDEX


def test_basic_shipping_label(sender_address, receiver_address, tracking_code):
    shipping_label = ShippingLabel(
        sender=sender_address,
        receiver=receiver_address,
        service=SERVICE_SEDEX,
        tracking_code=tracking_code,
        order="123",
        invoice="321",
        volume=(1, 1),
        weight=100,
    )

    assert shipping_label.sender == sender_address
    assert shipping_label.receiver == receiver_address
    assert shipping_label.get_order() == "123"
    assert shipping_label.get_order("Order: {}") == "Order: 123"
    assert shipping_label.get_invoice() == "321"
    assert shipping_label.get_invoice("Invoice #{}") == "Invoice #321"
    assert shipping_label.get_volume() == "1/1"
    assert shipping_label.get_volume("Volume: {}/{}") == "Volume: 1/1"
    assert shipping_label.service == SERVICE_SEDEX
    assert shipping_label.get_symbol_filename() == os.path.join(DATADIR, "express.gif")
    assert shipping_label.tracking_code == tracking_code


def test_fail_shipping_label_same_addresses(sender_address, tracking_code):
    with pytest.raises(InvalidAddressesException):
        ShippingLabel(sender_address, sender_address, SERVICE_SEDEX, tracking_code=tracking_code)
