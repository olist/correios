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

# noinspection PyPep8Naming
from PIL import Image as image

from correios import DATADIR
from correios.exceptions import (InvalidAddressesError, InvalidTrackingCodeError,
                                 InvalidVolumeInformationError, InvalidDimensionsError)
from correios.models.data import SERVICE_SEDEX, EXTRA_SERVICE_RN, EXTRA_SERVICE_AR
from correios.models.posting import ShippingLabel, TrackingCode, PostingList

FIXTURESDIR = os.path.join(os.path.dirname(__file__), "fixtures")


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
    assert tracking.splitted == "DL 746 686 536 BR"
    assert repr(tracking) == "<TrackingCode code='DL746686536BR'>"


@pytest.mark.parametrize("tracking_code", [
    "DL7466865BR",
    "DL746686530BR",  # invalid digit (0)
    "DL7466X653 BR",
    "DL74668653B",
    "D746686530 BR",
    "DL46686530 B1",
])
def test_fail_invalid_tracking_code(tracking_code):
    with pytest.raises(InvalidTrackingCodeError):
        TrackingCode(tracking_code)


@pytest.mark.parametrize("tracking_code,digit", [
    ("DL74668653 BR", 6),
    ("DL02000000 BR", 0),
    ("DL00000000 BR", 5),
])
def test_tracking_code_digit_calculator(tracking_code, digit):
    tracking = TrackingCode(tracking_code)
    assert tracking.digit == digit


def test_basic_shipping_label(posting_card, sender_address, receiver_address, tracking_code):
    shipping_label = ShippingLabel(
        posting_card=posting_card,
        sender=sender_address,
        receiver=receiver_address,
        service=SERVICE_SEDEX,
        extra_services=[EXTRA_SERVICE_AR],
        tracking_code=tracking_code,
        logo=os.path.join(FIXTURESDIR, "test_logo.jpg"),
        order="123",
        invoice_number="321",
        invoice_series="A1",
        invoice_type="",
        volume_sequence=(1, 2),
        width=11, height=2, length=16,
        weight=100,
        text="Hello World!",
        latitude=-25.4131980,
        longitude=-49.2584896,
    )

    assert shipping_label.posting_card == posting_card
    assert shipping_label.sender == sender_address
    assert shipping_label.receiver == receiver_address

    assert shipping_label.service == SERVICE_SEDEX
    assert shipping_label.get_service_name() == "SEDEX"

    assert shipping_label.extra_services == [EXTRA_SERVICE_RN, EXTRA_SERVICE_AR]

    assert shipping_label.tracking_code == tracking_code
    assert shipping_label.get_tracking_code().replace(" ", "") == str(shipping_label.tracking_code)

    assert isinstance(shipping_label.logo, image.Image)
    assert shipping_label.logo.filename == os.path.join(FIXTURESDIR, "test_logo.jpg")

    assert shipping_label.order == "123"
    assert shipping_label.get_order() == "123"

    assert shipping_label.invoice_number == "321"
    assert shipping_label.get_invoice() == "321"

    assert shipping_label.get_contract_number() == "9912208555"

    assert shipping_label.volume_sequence == (1, 2)
    assert shipping_label.get_volume_sequence() == "1/2"

    assert shipping_label.weight == 100
    assert shipping_label.get_weight() == "100"

    assert shipping_label.text == "Hello World!"

    assert shipping_label.latitude == -25.4131980
    assert shipping_label.longitude == -49.2584896

    assert shipping_label.posting_list_group == 0

    assert shipping_label.get_symbol_filename() == os.path.join(DATADIR, "express.gif")
    assert isinstance(shipping_label.symbol, image.Image)

    assert len(shipping_label.get_datamatrix_info()) == 164  # datamatrix info size accordingly with documentation
    assert shipping_label.get_sender_data().count("<br/>") == 3
    assert shipping_label.get_receiver_data().count("<br/>") == 3

    assert repr(shipping_label) == "<ShippingLabel tracking='{!s}'>".format(shipping_label.tracking_code)


def test_basic_default_shipping_label(posting_card, sender_address, receiver_address):
    shipping_label = ShippingLabel(
        posting_card=posting_card,
        sender=sender_address,
        receiver=receiver_address,
        service=40096,  # SERVICE_SEDEX_CODE
        width=11, height=2, length=16, weight=10000,
        tracking_code="PD12345678 BR",
    )

    assert shipping_label.service == SERVICE_SEDEX
    assert shipping_label.tracking_code.code == "PD123456785BR"
    assert len(shipping_label.extra_services) == 1


def test_fail_shipping_label_same_addresses(posting_card, sender_address, tracking_code):
    with pytest.raises(InvalidAddressesError):
        ShippingLabel(posting_card, sender_address, sender_address, SERVICE_SEDEX,
                      width=10, height=10, length=10, weight=10000,
                      tracking_code=tracking_code)


def test_basic_envelop_dimensions_validation():
    ShippingLabel.validate_dimensions(ShippingLabel.TYPE_ENVELOPE, 0, 0, 0, 0)


@pytest.mark.parametrize("weight,width,height,length,posting_weight", [
    (9000, 50, 60, 15, 9000),
    (15000, 43, 28, 52, 15000),
    (7000, 55, 31, 40, 11366),
])
def test_posting_weight_calculation(weight, width, height, length, posting_weight):
    assert round(ShippingLabel.calculate_posting_weight(weight, width, height, length)) == posting_weight


@pytest.mark.parametrize("volume_type,width,height,length,diameter", [
    (ShippingLabel.TYPE_ENVELOPE, 1, 0, 0, 0),
    (ShippingLabel.TYPE_ENVELOPE, 0, 1, 0, 0),
    (ShippingLabel.TYPE_ENVELOPE, 0, 0, 1, 0),
    (ShippingLabel.TYPE_ENVELOPE, 0, 0, 0, 1),
    (ShippingLabel.TYPE_ENVELOPE, 1, 1, 1, 1),
    (ShippingLabel.TYPE_PACKAGE, 11, 2, 16, 1),  # invalid diameter
    (ShippingLabel.TYPE_PACKAGE, 10, 2, 16, 0),  # min width=11
    (ShippingLabel.TYPE_PACKAGE, 110, 2, 16, 0),  # max width=105
    (ShippingLabel.TYPE_PACKAGE, 11, 1, 16, 0),  # min height=2
    (ShippingLabel.TYPE_PACKAGE, 11, 110, 16, 0),  # max height=110
    (ShippingLabel.TYPE_PACKAGE, 11, 2, 15, 0),  # min length=15
    (ShippingLabel.TYPE_PACKAGE, 11, 2, 110, 0),  # max length=110
    (ShippingLabel.TYPE_PACKAGE, 105, 105, 105, 0),  # sum > 200
    (ShippingLabel.TYPE_CYLINDER, 1, 0, 18, 16),  # invalid width
    (ShippingLabel.TYPE_CYLINDER, 0, 1, 18, 16),  # invalid height
    (ShippingLabel.TYPE_CYLINDER, 0, 0, 1, 16),  # min length=18
    (ShippingLabel.TYPE_CYLINDER, 0, 0, 110, 16),  # max length=105
    (ShippingLabel.TYPE_CYLINDER, 0, 0, 18, 15),  # min diameter=16
    (ShippingLabel.TYPE_CYLINDER, 0, 0, 18, 110),  # max diameter=91
    (ShippingLabel.TYPE_CYLINDER, 0, 0, 18, 16),  # max cylinder size=28
])
def test_fail_dimensions_validation(volume_type, width, height, length, diameter):
    with pytest.raises(InvalidDimensionsError):
        ShippingLabel.validate_dimensions(volume_type, width, height, length, diameter)


def test_fail_invalid_volumes_argument(posting_card, sender_address, receiver_address, tracking_code):
    with pytest.raises(InvalidVolumeInformationError):
        # noinspection PyTypeChecker
        ShippingLabel(posting_card, sender_address, receiver_address, SERVICE_SEDEX,
                      width=10, height=10, length=10, weight=10000,
                      tracking_code=tracking_code, volume_sequence=(1,))  # invalid tuple


def test_basic_posting_list(shipping_label):
    posting_list = PostingList(
        id_=12345,
    )
    posting_list.add_shipping_label(shipping_label)

    # TODO
    assert posting_list.id == 12345
    assert not posting_list.closed
    assert posting_list.get_tracking_codes()
