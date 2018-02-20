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
from datetime import datetime, timedelta
from decimal import Decimal

import pytest
from PIL.Image import Image

from correios import exceptions
from correios.models import posting
from correios.models.data import (
    EXTRA_SERVICE_AR,
    EXTRA_SERVICE_RR,
    EXTRA_SERVICE_VD,
    SERVICE_PAC,
    SERVICE_SEDEX,
    TRACKING_EVENT_TYPES,
)
from correios.models.user import ExtraService, Service

from .conftest import ShippingLabelFactory

FIXTURESDIR = os.path.join(os.path.dirname(__file__), "fixtures")


@pytest.mark.parametrize("tracking_code", [
    "DL74668653 BR",
    "DL746686536BR",
    "DL74668653BR",
    "dl74668653br",
])
def test_tracking_code_constructor(tracking_code):
    tracking = posting.TrackingCode(tracking_code)
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
    with pytest.raises(exceptions.InvalidTrackingCodeError):
        posting.TrackingCode(tracking_code)


@pytest.mark.parametrize("tracking_code,digit", [
    ("DL74668653 BR", 6),
    ("DL02000000 BR", 0),
    ("DL00000000 BR", 5),
])
def test_tracking_code_digit_calculator(tracking_code, digit):
    tracking = posting.TrackingCode(tracking_code)
    assert tracking.digit == digit


def test_tracking_code_creator():
    tracking_code1 = posting.TrackingCode.create("DL746686536BR")
    assert tracking_code1.code == "DL746686536BR"

    tracking_code2 = posting.TrackingCode.create(tracking_code1)
    assert tracking_code1 == tracking_code2


def test_tracking_code_range_generator():
    tracking_codes = posting.TrackingCode.create_range("DL74668650 BR", "DL74668654 BR")
    assert len(tracking_codes) == 5
    assert all(isinstance(tc, posting.TrackingCode) for tc in tracking_codes)


def test_fail_tracking_code_invalid_range_generator():
    with pytest.raises(exceptions.InvalidTrackingCodeError):
        posting.TrackingCode.create_range("DL74668650 BR", "SX74668654 BR")  # different prefix

    with pytest.raises(exceptions.InvalidTrackingCodeError):
        posting.TrackingCode.create_range("DL74668650 BR", "DL74668654 US")  # different suffix

    with pytest.raises(exceptions.InvalidTrackingCodeError):
        posting.TrackingCode.create_range("DL74668654 BR", "DL74668650 BR")  # end < start


def test_basic_shipping_label(posting_card, sender_address, receiver_address, tracking_code, package):
    shipping_label = posting.ShippingLabel(
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

    # noinspection PyUnresolvedReferences
    assert shipping_label.logo.filename == os.path.join(FIXTURESDIR, "test_logo.jpg")

    assert shipping_label.order == "123"
    assert shipping_label.get_order() == "123"

    assert shipping_label.invoice_number == "321"
    assert shipping_label.get_invoice() == "321"

    assert shipping_label.get_contract_number() == "9911222777"
    assert shipping_label.get_package_sequence() == "{}/{}".format(*shipping_label.package.sequence)
    assert shipping_label.get_weight() == "{}g".format(shipping_label.package.weight)

    assert shipping_label.text == "Hello World!"

    assert shipping_label.latitude == -25.4131980
    assert shipping_label.longitude == -49.2584896

    assert shipping_label.posting_list_group == 0

    assert shipping_label.get_symbol_filename().endswith("/express.gif")
    assert isinstance(shipping_label.symbol, Image)

    assert len(shipping_label.get_datamatrix_info()) == 164  # datamatrix info size accordingly with documentation
    assert shipping_label.get_sender_data().count("<br/>") >= 2
    assert shipping_label.get_receiver_data().count("<br/>") >= 2

    assert repr(shipping_label) == "<ShippingLabel tracking='{!s}'>".format(shipping_label.tracking_code)


def test_basic_default_shipping_label(posting_card, sender_address, receiver_address, package):
    shipping_label = posting.ShippingLabel(
        posting_card=posting_card,
        sender=sender_address,
        receiver=receiver_address,
        service=4162,  # SERVICE_SEDEX_CODE
        package=package,
        tracking_code="PD12345678 BR",
    )

    assert shipping_label.service == Service.get(SERVICE_SEDEX)
    assert shipping_label.tracking_code.code == "PD123456785BR"
    assert len(shipping_label.extra_services) == 1


def test_shipping_label_with_declared_value(posting_card, sender_address, receiver_address, package):
    service = Service.get(SERVICE_SEDEX)
    shipping_label = posting.ShippingLabel(
        posting_card=posting_card,
        sender=sender_address,
        receiver=receiver_address,
        service=service,
        package=package,
        tracking_code="PD12345678 BR",
        value=service.max_declared_value - Decimal("1.00"),
        extra_services=[EXTRA_SERVICE_VD],
    )
    assert ExtraService.get(EXTRA_SERVICE_VD) in shipping_label.extra_services


def test_shipping_label_with_min_declared_value_pac(posting_card, sender_address, receiver_address, package):
    service = Service.get(SERVICE_PAC)
    shipping_label = posting.ShippingLabel(
        posting_card=posting_card,
        sender=sender_address,
        receiver=receiver_address,
        service=service,
        package=package,
        tracking_code="PD12345678 BR",
        value=Decimal("0"),
        extra_services=[EXTRA_SERVICE_VD],
    )
    assert shipping_label.value == Decimal("18.50")


def test_shipping_label_with_min_declared_value_sedex(posting_card, sender_address, receiver_address, package):
    service = Service.get(SERVICE_SEDEX)
    shipping_label = posting.ShippingLabel(
        posting_card=posting_card,
        sender=sender_address,
        receiver=receiver_address,
        service=service,
        package=package,
        tracking_code="PD12345678 BR",
        value=Decimal("0"),
        extra_services=[EXTRA_SERVICE_VD],
    )
    assert shipping_label.value == Decimal("18.50")


def test_fail_shipping_label_with_invalid_declared_value(posting_card, sender_address, receiver_address, package):
    service = Service.get(SERVICE_SEDEX)
    shipping_label = posting.ShippingLabel(
        posting_card=posting_card,
        sender=sender_address,
        receiver=receiver_address,
        service=service,
        package=package,
        tracking_code="PD12345678 BR",
        value=service.max_declared_value + Decimal("1.00"),
    )

    with pytest.raises(exceptions.MaximumDeclaredValueError):
        shipping_label.add_extra_service(ExtraService.get(EXTRA_SERVICE_VD))


def test_fail_shipping_label_same_addresses(posting_card, sender_address, tracking_code, package):
    with pytest.raises(exceptions.InvalidAddressesError):
        posting.ShippingLabel(
            posting_card,
            sender_address,
            sender_address,
            SERVICE_SEDEX,
            package=package,
            tracking_code=tracking_code,
        )


def test_package_basic():
    package = posting.Package(
        package_type=posting.Package.TYPE_BOX,
        width=11,
        height=10,
        length=16,
        weight=10000,
        service=SERVICE_PAC,
    )
    assert isinstance(package.service, Service)
    assert package.package_type == posting.Package.TYPE_BOX


@pytest.mark.parametrize("package,freight_package_type", [
    (posting.Package(posting.Package.TYPE_ENVELOPE, 0, 0, 0, weight=1), 3),
    (posting.Package(posting.Package.TYPE_BOX, 11, 10, 16, weight=1), 1),
    (posting.Package(posting.Package.TYPE_CYLINDER, 0, 0, 14, 2, weight=1), 2),
])
def test_freight_package_type(package, freight_package_type):
    assert package.freight_package_type == freight_package_type


def test_package_basic_envelop_dimensions_validation():
    posting.Package.validate(
        posting.Package.TYPE_ENVELOPE,
        0, 0, 0, 0,
        weight=1,
    )


@pytest.mark.parametrize("weight,width,height,length,posting_weight", [
    (9000, 50, 60, 15, 9000),
    (15000, 43, 28, 52, 15000),
    (7000, 55, 31, 40, 11367),
    (15000, 73, 73, 73, 64837)  # math.ceil(64836.1)
])
def test_package_posting_weight_calculation(weight, width, height, length, posting_weight):
    volumetric_weight = posting.Package.calculate_volumetric_weight(width, height, length)
    assert posting.Package.calculate_posting_weight(weight, volumetric_weight) == posting_weight


@pytest.mark.parametrize("package_type,width,height,length,diameter,exc", [
    (posting.Package.TYPE_ENVELOPE, 1, 0, 0, 0, exceptions.InvalidPackageDimensionsError),
    (posting.Package.TYPE_ENVELOPE, 0, 1, 0, 0, exceptions.InvalidPackageDimensionsError),
    (posting.Package.TYPE_ENVELOPE, 0, 0, 1, 0, exceptions.InvalidPackageDimensionsError),
    (posting.Package.TYPE_ENVELOPE, 0, 0, 0, 1, exceptions.InvalidPackageDimensionsError),
    (posting.Package.TYPE_ENVELOPE, 1, 1, 1, 1, exceptions.InvalidPackageDimensionsError),
    (posting.Package.TYPE_BOX, 11, 2, 16, 1, exceptions.InvalidPackageDimensionsError),  # invalid diameter
    (posting.Package.TYPE_BOX, 110, 2, 16, 0, exceptions.InvalidMaxPackageDimensionsError),  # max width=105
    (posting.Package.TYPE_BOX, 11, 110, 16, 0, exceptions.InvalidMaxPackageDimensionsError),  # max height=110
    (posting.Package.TYPE_BOX, 11, 2, 110, 0, exceptions.InvalidMaxPackageDimensionsError),  # max length=110
    (posting.Package.TYPE_BOX, 105, 105, 105, 0, exceptions.InvalidMaxPackageDimensionsError),  # sum > 200
    (posting.Package.TYPE_CYLINDER, 1, 0, 18, 16, exceptions.InvalidPackageDimensionsError),  # invalid width
    (posting.Package.TYPE_CYLINDER, 0, 1, 18, 16, exceptions.InvalidPackageDimensionsError),  # invalid height
    (posting.Package.TYPE_CYLINDER, 0, 0, 110, 16, exceptions.InvalidMaxPackageDimensionsError),  # max length=105
    (posting.Package.TYPE_CYLINDER, 0, 0, 18, 110, exceptions.InvalidMaxPackageDimensionsError),  # max diameter=91
    (posting.Package.TYPE_CYLINDER, 0, 0, 18, 16, exceptions.InvalidMaxPackageDimensionsError),  # max cylinder size=28
])
def test_fail_package_dimensions_validation(package_type, width, height, length, diameter, exc):
    with pytest.raises(exc):
        posting.Package.validate(package_type, width, height, length, diameter, weight=1)


def test_package_weight_validation():
    posting.Package.validate(
        posting.Package.TYPE_BOX,
        12, 10, 20,
        service=Service.get(SERVICE_SEDEX),
        weight=10000,
    )

    posting.Package.validate(
        posting.Package.TYPE_BOX,
        12, 10, 20,
        service=Service.get(10065),  # 10065 - service with no max weight
        weight=50000,
    )


def test_fail_package_weight_validation():
    with pytest.raises(exceptions.InvalidMaxPackageWeightError):
        posting.Package.validate(
            posting.Package.TYPE_BOX,
            12, 10, 20,
            service=Service.get(SERVICE_SEDEX),
            weight=50000,
        )


def test_fix_bug_of_weight_using_diameter_information():
    package = posting.Package(
        package_type=posting.Package.TYPE_CYLINDER,
        diameter=2,
        length=20,
        weight=10000,
        service=SERVICE_PAC,
    )
    assert package.real_weight == 10000
    assert package.real_diameter == 2


@pytest.mark.parametrize("sequence", [
    (1,),
    (3, 2),
])
def test_fail_package_invalid_sequence(sequence):
    with pytest.raises(exceptions.InvalidPackageSequenceError):
        posting.Package(
            package_type=posting.Package.TYPE_BOX,
            width=11,
            height=10,
            length=16,
            weight=10000,
            sequence=sequence,  # invalid tuple
        )


@pytest.mark.parametrize("dimension,value,minimum", [
    ("width", 1, posting.MIN_WIDTH),
    ("height", 1, posting.MIN_HEIGHT),
    ("length", 1, posting.MIN_LENGTH),
    ("weight", 1, 1),
])
def test_box_package_change_dimensions_below_minimum(package, dimension, value, minimum):
    setattr(package, dimension, value)
    assert getattr(package, dimension) == minimum


@pytest.mark.parametrize("dimension,value,minimum", [
    ("diameter", 1, posting.MIN_DIAMETER),
    ("length", 1, posting.MIN_LENGTH),
    ("weight", 1, 1),
])
def test_cylinder_package_change_dimensions_below_minimum(package, dimension, value, minimum):
    package.package_type = package.TYPE_CYLINDER
    setattr(package, dimension, value)
    assert getattr(package, dimension) == minimum


@pytest.mark.parametrize("dimension,value,exc", [
    ("width", 0, exceptions.InvalidMinPackageDimensionsError),
    ("width", posting.MAX_WIDTH + 1, exceptions.InvalidMaxPackageDimensionsError),
    ("height", 0, exceptions.InvalidMinPackageDimensionsError),
    ("height", posting.MAX_HEIGHT + 1, exceptions.InvalidMaxPackageDimensionsError),
    ("length", 0, exceptions.InvalidMinPackageDimensionsError),
    ("length", posting.MAX_LENGTH + 1, exceptions.InvalidMaxPackageDimensionsError),
    ("weight", 0, exceptions.InvalidMinPackageWeightError),
    ("weight", 100000, exceptions.InvalidMaxPackageWeightError),
])
def test_fail_box_package_change_invalid_dimensions(package, dimension, value, exc):
    with pytest.raises(exc):
        setattr(package, dimension, value)


@pytest.mark.parametrize("dimension,value,exc", [
    ("diameter", 0, exceptions.InvalidMinPackageDimensionsError),
    ("diameter", posting.MAX_DIAMETER + 1, exceptions.InvalidMaxPackageDimensionsError),
    ("length", 0, exceptions.InvalidMinPackageDimensionsError),
    ("length", posting.MAX_LENGTH + 1, exceptions.InvalidMaxPackageDimensionsError),
])
def test_fail_cylinder_package_change_invalid_dimensions(package, dimension, value, exc):
    package.package_type = package.TYPE_CYLINDER
    with pytest.raises(exc):
        setattr(package, dimension, value)


def test_basic_posting_list(shipping_label):
    posting_list = posting.PostingList(custom_id=12345)
    posting_list.add_shipping_label(shipping_label)

    assert posting_list.custom_id == 12345
    assert not posting_list.closed
    tracking_codes = posting_list.get_tracking_codes()
    assert tracking_codes and shipping_label.tracking_code.short in tracking_codes


def test_fail_add_different_sender_in_posting_list():
    posting_list = posting.PostingList(custom_id=12345)
    posting_list.add_shipping_label(ShippingLabelFactory.build())

    with pytest.raises(exceptions.PostingListError):
        posting_list.add_shipping_label(ShippingLabelFactory.build())


def test_fail_add_same_shipping_label_twice_in_posting_list(shipping_label):
    posting_list = posting.PostingList(custom_id=12345)
    posting_list.add_shipping_label(shipping_label)

    with pytest.raises(exceptions.PostingListError):
        posting_list.add_shipping_label(shipping_label)


def test_calculate_insurance_when_not_applicable():
    value = posting.Package.calculate_insurance(per_unit_value=50, quantity=2, service=SERVICE_SEDEX)
    assert value == Decimal(0)

    value = posting.Package.calculate_insurance(per_unit_value=Decimal(10), service=SERVICE_PAC)
    assert value == Decimal(0)


def test_calculate_insurance_pac():
    value = posting.Package.calculate_insurance(per_unit_value=193, service=SERVICE_PAC)
    assert value == Decimal(1)

    value = posting.Package.calculate_insurance(per_unit_value=Decimal(193), quantity=2, service=SERVICE_PAC)
    assert value == Decimal(2)

    value = posting.Package.calculate_insurance(per_unit_value=Decimal(500), quantity=2, service=SERVICE_PAC)
    assert value == Decimal('6.30')


def test_calculate_insurance_sedex():
    value = posting.Package.calculate_insurance(per_unit_value=Decimal(500), service=SERVICE_SEDEX)
    assert value == Decimal('2.98')

    value = posting.Package.calculate_insurance(per_unit_value=Decimal(500), quantity=2, service=SERVICE_SEDEX)
    assert value == Decimal('5.95')


def test_event_status():
    event_status = posting.EventStatus('BDE', 1)
    assert repr(event_status) == "<EventStatus('BDE', 1)>"


@pytest.mark.parametrize("status", (posting.EventStatus("BDE", "01"), ("BDE", "01")))
def test_basic_tracking_event(status):
    tracking_event = posting.TrackingEvent(
        timestamp=datetime(2010, 1, 2, 1, 2),
        status=status,
        location_zip_code="82940150",
        location="Correios",
        receiver="José",
        city="Curitiba",
        state="PR",
        document="XYZ",
        comment="The comment",
        description="The description",
        details="The details",
    )

    assert tracking_event.timestamp == datetime(2010, 1, 2, 1, 2)
    assert tracking_event.status.type == "BDE"
    assert tracking_event.status.status == 1
    assert tracking_event.location_zip_code == "82940150"
    assert tracking_event.location == "Correios"
    assert tracking_event.receiver == "José"
    assert tracking_event.city == "Curitiba"
    assert tracking_event.state == "PR"
    assert tracking_event.document == "XYZ"
    assert tracking_event.comment == "The comment"
    assert tracking_event.description == "The description"
    assert tracking_event.details == "The details"

    assert repr(tracking_event) == "<TrackingEvent((BDE, 1), 02/01/2010 01:02)>"
    assert str(tracking_event) == "The description - Correios - Curitiba/PR"


def test_tracking_event_timestamp_format(tracking_event):
    expected_date = "01/01/2016 12:00"
    assert tracking_event.timestamp.strftime(posting.TrackingEvent.timestamp_format) == expected_date


def test_basic_not_found_tracking_event():
    tracking_event = posting.NotFoundTrackingEvent(
        timestamp=datetime(2010, 1, 2, 1, 2),
        comment="Not found",
    )
    assert tracking_event.timestamp == datetime(2010, 1, 2, 1, 2)
    assert tracking_event.status.type == "ERROR"
    assert tracking_event.status.status == 0
    assert tracking_event.comment == "Not found"


@pytest.mark.parametrize("status_type,status_number", [
    ("BDE", 0),
    ("BDI", 0),
    ("BDR", 0),
    ("BLQ", 1),
    # ("CAR", 0),
    ("CD", 0),
    ("CMT", 0),
    ("CO", 1),
    ("CUN", 0),
    ("DO", 0),
    ("EST", 1),
    ("FC", 1),
    ("IDC", 1),
    ("LDI", 0),
    ("LDE", 0),
    ("OEC", 0),
    ("PAR", 15),
    ("PMT", 1),
    ("PO", 0),
    ("RO", 0),
    ("TRI", 0),
    # ("CMR", 0),
])
def test_basic_event_status(status_type, status_number):
    event_status = posting.EventStatus(status_type, status_number)

    assert event_status.type == status_type
    assert event_status.status == status_number
    assert event_status.display_event_type == TRACKING_EVENT_TYPES[status_type]

    assert str(event_status) == "({}, {})".format(status_type, status_number)
    assert repr(event_status) == "<EventStatus({!r}, {!r})>".format(status_type, status_number)


@pytest.mark.parametrize("event_type", ("XYZ", "ABC", "XXX", "WTF", "BD", "ERROR"))
def test_invalid_event_status(event_type):
    with pytest.raises(exceptions.InvalidEventStatusError):
        posting.EventStatus(event_type, 1)


def test_basic_freight():
    freight = posting.FreightResponse(SERVICE_SEDEX, timedelta(days=5), Decimal("10.00"))
    assert freight.total == Decimal("10.00")
    assert freight.delivery_time == timedelta(days=5)
    assert freight.declared_value == Decimal("0.00")
    assert freight.saturday is False
    assert freight.home is False


def test_basic_freight_conversion():
    freight = posting.FreightResponse(SERVICE_SEDEX, 5, 10.00)
    assert freight.delivery_time == timedelta(days=5)
    assert freight.total == Decimal("10.00")
