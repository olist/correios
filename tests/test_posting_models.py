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

import pytest
from PIL.Image import Image

from correios import DATADIR
from correios.exceptions import (InvalidAddressesError, InvalidEventStatusError,
                                 InvalidTrackingCodeError, InvalidPackageSequenceError,
                                 InvalidPackageDimensionsError, PostingListError,
                                 InvalidPackageWeightError)
from correios.models.data import (SERVICE_SEDEX, SERVICE_PAC, EXTRA_SERVICE_RR, EXTRA_SERVICE_AR,
                                  TRACKING_EVENT_TYPES)
from correios.models.posting import (EventStatus, NotFoundTrackingEvent,
                                     Package, PostingList, ShippingLabel, TrackingCode,
                                     TrackingEvent)
from correios.models.user import Service, ExtraService
from .conftest import ShippingLabelFactory

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


def test_tracking_code_creator():
    tracking_code1 = TrackingCode.create("DL746686536BR")
    assert tracking_code1.code == "DL746686536BR"

    tracking_code2 = TrackingCode.create(tracking_code1)
    assert tracking_code1 == tracking_code2


def test_tracking_code_range_generator():
    tracking_codes = TrackingCode.create_range("DL74668650 BR", "DL74668654 BR")
    assert len(tracking_codes) == 5
    assert all(isinstance(tc, TrackingCode) for tc in tracking_codes)


def test_fail_tracking_code_invalid_range_generator():
    with pytest.raises(InvalidTrackingCodeError):
        TrackingCode.create_range("DL74668650 BR", "SX74668654 BR")  # different prefix

    with pytest.raises(InvalidTrackingCodeError):
        TrackingCode.create_range("DL74668650 BR", "DL74668654 US")  # different suffix

    with pytest.raises(InvalidTrackingCodeError):
        TrackingCode.create_range("DL74668654 BR", "DL74668650 BR")  # end < start


def test_basic_shipping_label(posting_card, sender_address, receiver_address, tracking_code, package):
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
        package=package,
        text="Hello World!",
        latitude=-25.4131980,
        longitude=-49.2584896,
    )

    assert shipping_label.posting_card == posting_card
    assert shipping_label.sender == sender_address
    assert shipping_label.receiver == receiver_address

    assert shipping_label.service == Service.get(SERVICE_SEDEX)
    assert shipping_label.get_service_name() == "SEDEX"

    assert shipping_label.extra_services == [ExtraService.get(EXTRA_SERVICE_RR),
                                             ExtraService.get(EXTRA_SERVICE_AR)]

    assert shipping_label.tracking_code == tracking_code
    assert shipping_label.get_tracking_code().replace(" ", "") == str(shipping_label.tracking_code)

    assert isinstance(shipping_label.logo, Image)
    assert shipping_label.logo.filename == os.path.join(FIXTURESDIR, "test_logo.jpg")

    assert shipping_label.order == "123"
    assert shipping_label.get_order() == "123"

    assert shipping_label.invoice_number == "321"
    assert shipping_label.get_invoice() == "321"

    assert shipping_label.get_contract_number() == "9912208555"
    assert shipping_label.get_package_sequence() == "{}/{}".format(*shipping_label.package.sequence)
    assert shipping_label.get_weight() == "{}g".format(shipping_label.package.weight)

    assert shipping_label.text == "Hello World!"

    assert shipping_label.latitude == -25.4131980
    assert shipping_label.longitude == -49.2584896

    assert shipping_label.posting_list_group == 0

    assert shipping_label.get_symbol_filename() == os.path.join(DATADIR, "express.gif")
    assert isinstance(shipping_label.symbol, Image)

    assert len(shipping_label.get_datamatrix_info()) == 164  # datamatrix info size accordingly with documentation
    assert shipping_label.get_sender_data().count("<br/>") == 3
    assert shipping_label.get_receiver_data().count("<br/>") == 3

    assert repr(shipping_label) == "<ShippingLabel tracking='{!s}'>".format(shipping_label.tracking_code)


def test_basic_default_shipping_label(posting_card, sender_address, receiver_address, package):
    shipping_label = ShippingLabel(
        posting_card=posting_card,
        sender=sender_address,
        receiver=receiver_address,
        service=40096,  # SERVICE_SEDEX_CODE
        package=package,
        tracking_code="PD12345678 BR",
    )

    assert shipping_label.service == Service.get(SERVICE_SEDEX)
    assert shipping_label.tracking_code.code == "PD123456785BR"
    assert len(shipping_label.extra_services) == 1


def test_fail_shipping_label_same_addresses(posting_card, sender_address, tracking_code, package):
    with pytest.raises(InvalidAddressesError):
        ShippingLabel(posting_card, sender_address, sender_address, SERVICE_SEDEX,
                      package=package,
                      tracking_code=tracking_code)


def test_package_basic_envelop_dimensions_validation():
    Package.validate(Package.TYPE_ENVELOPE, 0, 0, 0, 0)


@pytest.mark.parametrize("weight,width,height,length,posting_weight", [
    (9000, 50, 60, 15, 9000),
    (15000, 43, 28, 52, 15000),
    (7000, 55, 31, 40, 11367),
    (15000, 73, 73, 73, 64837)  # math.ceil(64836.1)
])
def test_package_posting_weight_calculation(weight, width, height, length, posting_weight):
    volumetric_weight = Package.calculate_volumetric_weight(width, height, length)
    assert Package.calculate_posting_weight(weight, volumetric_weight) == posting_weight


@pytest.mark.parametrize("package_type,width,height,length,diameter", [
    (Package.TYPE_ENVELOPE, 1, 0, 0, 0),
    (Package.TYPE_ENVELOPE, 0, 1, 0, 0),
    (Package.TYPE_ENVELOPE, 0, 0, 1, 0),
    (Package.TYPE_ENVELOPE, 0, 0, 0, 1),
    (Package.TYPE_ENVELOPE, 1, 1, 1, 1),
    (Package.TYPE_BOX, 11, 2, 16, 1),  # invalid diameter
    (Package.TYPE_BOX, 10, 2, 16, 0),  # min width=11
    (Package.TYPE_BOX, 110, 2, 16, 0),  # max width=105
    (Package.TYPE_BOX, 11, 1, 16, 0),  # min height=2
    (Package.TYPE_BOX, 11, 110, 16, 0),  # max height=110
    (Package.TYPE_BOX, 11, 2, 15, 0),  # min length=15
    (Package.TYPE_BOX, 11, 2, 110, 0),  # max length=110
    (Package.TYPE_BOX, 105, 105, 105, 0),  # sum > 200
    (Package.TYPE_CYLINDER, 1, 0, 18, 16),  # invalid width
    (Package.TYPE_CYLINDER, 0, 1, 18, 16),  # invalid height
    (Package.TYPE_CYLINDER, 0, 0, 1, 16),  # min length=18
    (Package.TYPE_CYLINDER, 0, 0, 110, 16),  # max length=105
    (Package.TYPE_CYLINDER, 0, 0, 18, 15),  # min diameter=16
    (Package.TYPE_CYLINDER, 0, 0, 18, 110),  # max diameter=91
    (Package.TYPE_CYLINDER, 0, 0, 18, 16),  # max cylinder size=28
])
def test_fail_package_dimensions_validation(package_type, width, height, length, diameter):
    with pytest.raises(InvalidPackageDimensionsError):
        Package.validate(package_type, width, height, length, diameter)


def test_package_weight_validation():
    Package.validate(Package.TYPE_BOX, 12, 10, 20, service=Service.get(SERVICE_SEDEX), weight=10000)
    # 10065 - service with no max weight
    Package.validate(Package.TYPE_BOX, 12, 10, 20, service=Service.get(10065), weight=50000)


def test_fail_package_weight_validation():
    with pytest.raises(InvalidPackageWeightError):
        Package.validate(Package.TYPE_BOX, 12, 10, 20, service=Service.get(SERVICE_SEDEX), weight=50000)


@pytest.mark.parametrize("sequence", [
    (1,),
    (3, 2),
])
def test_fail_package_invalid_sequence(sequence):
    with pytest.raises(InvalidPackageSequenceError):
        Package(package_type=Package.TYPE_BOX, width=11, height=10, length=16, weight=10000,
                sequence=sequence)  # invalid tuple


def test_basic_posting_list(shipping_label):
    posting_list = PostingList(custom_id=12345)
    posting_list.add_shipping_label(shipping_label)

    assert posting_list.custom_id == 12345
    assert not posting_list.closed
    tracking_codes = posting_list.get_tracking_codes()
    assert tracking_codes and shipping_label.tracking_code.short in tracking_codes


def test_fail_add_different_sender_in_posting_list():
    posting_list = PostingList(custom_id=12345)
    posting_list.add_shipping_label(ShippingLabelFactory.build())

    with pytest.raises(PostingListError):
        posting_list.add_shipping_label(ShippingLabelFactory.build())


def test_fail_add_same_shipping_label_twice_in_posting_list(shipping_label):
    posting_list = PostingList(custom_id=12345)
    posting_list.add_shipping_label(shipping_label)

    with pytest.raises(PostingListError):
        posting_list.add_shipping_label(shipping_label)


def test_calculate_insurance_when_not_applicable():
    value = Package.calculate_insurance(per_unit_value=50, quantity=2, service=SERVICE_SEDEX)
    assert value == Decimal(0)

    value = Package.calculate_insurance(per_unit_value=Decimal(10), service=SERVICE_PAC)
    assert value == Decimal(0)


def test_calculate_insurance_pac():
    value = Package.calculate_insurance(per_unit_value=193, service=SERVICE_PAC)
    assert value == Decimal(1)

    value = Package.calculate_insurance(per_unit_value=Decimal(193), quantity=2, service=SERVICE_PAC)
    assert value == Decimal(2)

    value = Package.calculate_insurance(per_unit_value=Decimal(500), quantity=2, service=SERVICE_PAC)
    assert value == Decimal('6.30')


def test_calculate_insurance_sedex():
    # not implemented, defaults to zero
    value = Package.calculate_insurance(per_unit_value=Decimal(500), quantity=2, service=SERVICE_SEDEX)
    assert value == Decimal('0')


def test_event_status():
    event_status = EventStatus('BDE', 1)
    assert repr(event_status) == "<EventStatus('BDE', 1)>"


@pytest.mark.parametrize("status", (EventStatus("BDE", "01"), ("BDE", "01")))
def test_basic_tracking_event(status):
    tracking_event = TrackingEvent(timestamp=datetime(2010, 1, 2, 1, 2),
                                   status=status,
                                   location_zip_code="82940150",
                                   location="Correios",
                                   receiver="José",
                                   city="Curitiba",
                                   state="PR",
                                   document="XYZ",
                                   comment="The comment",
                                   description="The description",
                                   details="The details")

    assert tracking_event.timestamp == datetime(2010, 1, 2, 1, 2)
    assert tracking_event.status.type == "BDE"
    assert tracking_event.status.status == "01"
    assert tracking_event.location_zip_code == "82940150"
    assert tracking_event.location == "Correios"
    assert tracking_event.receiver == "José"
    assert tracking_event.city == "Curitiba"
    assert tracking_event.state == "PR"
    assert tracking_event.document == "XYZ"
    assert tracking_event.comment == "The comment"
    assert tracking_event.description == "The description"
    assert tracking_event.details == "The details"

    assert repr(tracking_event) == "<TrackingEvent((BDE, 01), 02/01/2010 01:02)>"
    assert str(tracking_event) == "The description - Correios - Curitiba/PR"


def test_tracking_event_timestamp_format(tracking_event):
    expected_date = "01/01/2016 12:00"
    assert tracking_event.timestamp.strftime(TrackingEvent.timestamp_format) == expected_date


def test_basic_not_found_tracking_event():
    tracking_event = NotFoundTrackingEvent(timestamp=datetime(2010, 1, 2, 1, 2),
                                           status=("ERROR", 1),
                                           comment="Not found")
    assert tracking_event.timestamp == datetime(2010, 1, 2, 1, 2)
    assert tracking_event.status.type == "ERROR"
    assert tracking_event.status.status == 1
    assert tracking_event.comment == "Not found"


@pytest.mark.parametrize("event_type", list(TRACKING_EVENT_TYPES.keys()))
def test_basic_event_status(event_type):
    event_status = EventStatus(event_type, 1)

    assert event_status.type == event_type
    assert event_status.status == 1
    assert event_status.display_event_type == TRACKING_EVENT_TYPES[event_type]

    assert str(event_status) == "({}, 1)".format(event_type)
    assert repr(event_status) == "<EventStatus({!r}, 1)>".format(event_type)


@pytest.mark.parametrize("event_type", ("XYZ", "ABC", "XXX", "WTF", "BD", ""))
def test_invalid_event_status(event_type):
    with pytest.raises(InvalidEventStatusError):
        EventStatus(event_type, 1)
