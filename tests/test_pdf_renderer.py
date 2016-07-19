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

from correios.models.data import SERVICE_SEDEX, SERVICE_SEDEX10
from correios.models.posting import ShippingLabel
from correios.renderers.pdf import ShippingLabelsPDFRenderer
from tests.conftest import AddressFactory

TESTDIR = os.path.dirname(__file__)


def test_render_basic_shipping_label(posting_card):
    shipping_label1 = ShippingLabel(
        posting_card=posting_card,
        sender=AddressFactory(),
        receiver=AddressFactory(),
        service=SERVICE_SEDEX,
        tracking_code="PD12345678BR",
        invoice="123",
        order="OLT123ABCDEF",
        weight=50,
        text="Obs: Este texto é opcional e pode ser usado como quiser."
    )

    shipping_label2 = ShippingLabel(
        posting_card=posting_card,
        sender=AddressFactory(),
        receiver=AddressFactory(),
        service=SERVICE_SEDEX10,
        tracking_code="PD12345555BR",
        invoice="654",
        order="OLT123XXXXX",
        weight=150,
    )

    shipping_labels = ShippingLabelsPDFRenderer()
    shipping_labels.add_shipping_label(shipping_label1)
    shipping_labels.add_shipping_label(shipping_label2)
    pdf = shipping_labels.render()
    assert pdf.getvalue().startswith(b"%PDF-1.4")
