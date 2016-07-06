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
from correios.exceptions import InvalidAddressesException, InvalidTrackingCode
from correios.models.posting import ShippingLabel, TrackingCode
from correios.models.data import SERVICE_SEDEX

@pytest.mark.parametrize("tracking_code", [
    "DL74668653 BR",
    "DL746686536BR",
    "DL74668653BR",
    "dl74668653br",
])
def test_tracking_code_constructor(tracking_code):
    tracking = TrackingCode(tracking_code)
    assert str(tracking) == "DL746686536BR"
    assert tracking.code == "DL746686536BR"
    assert tracking.prefix == "DL"
    assert tracking.number == "74668653"
    assert tracking.digit == 6
    assert tracking.nodigit == "DL74668653 BR"
    assert tracking.short == "DL74668653BR"


@pytest.mark.parametrize("tracking_code", [
    "DL7466865BR",
    "DL746686530BR",  # invalid digit (0)
    "DL7466X653 BR",
    "DL74668653B",
    "D746686530 BR",
    "DL46686530 B1",
])
def test_fail_invalid_tracking_code(tracking_code):
    with pytest.raises(InvalidTrackingCode):
        TrackingCode(tracking_code)


@pytest.mark.parametrize("tracking_code,digit", [
    ("DL74668653 BR", 6),
    ("DL02000000 BR", 0),
    ("DL00000000 BR", 5),
])
def test_tracking_code_digit_calculator(tracking_code, digit):
    tracking = TrackingCode(tracking_code)
    assert tracking.digit == digit


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
