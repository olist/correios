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

from correios.models.posting import PostingList
from correios.models.user import PostingCard
from .conftest import ShippingLabelFactory

try:
    from correios.renderers.pdf import PostingReportPDFRenderer
except ImportError:
    PostingReportPDFRenderer = None

TESTDIR = os.path.dirname(__file__)


@pytest.mark.skipif(not PostingReportPDFRenderer, reason="PDF generation support disabled")
def test_render_basic_shipping_label():
    shipping_labels_renderer = PostingReportPDFRenderer()
    shipping_labels = [ShippingLabelFactory.build() for _ in range(5)]

    for sl in shipping_labels:
        sl.weight_template = "Peso (g): <b>{!s}</b>"
        sl.invoice_template = "NF: {!s}"
        sl.order_template = "Ped.: <font size=6>{!s}</font>"
        sl.contract_number_template = "Contrato: <b>{!s}</b>"
        sl.service_name_template = "<b>{!s}</b>"
        sl.volume_template = "Volume: {!s}/{!s}"
        shipping_labels_renderer.add_shipping_label(sl)

    pdf = shipping_labels_renderer.render_labels()
    assert bytes(pdf).startswith(b"%PDF-1.4")


@pytest.mark.skipif(not PostingReportPDFRenderer, reason="PDF generation support disabled")
def test_render_basic_posting_list(posting_list: PostingList, posting_card: PostingCard):
    posting_list.close_with_id(number=12345)
    shipping_labels_renderer = PostingReportPDFRenderer()
    shipping_labels = [ShippingLabelFactory.build(posting_card=posting_card) for _ in range(5)]
    for shipping_label in shipping_labels:
        posting_list.add_shipping_label(shipping_label)
    shipping_labels_renderer.set_posting_list(posting_list)
    pdf = shipping_labels_renderer.render_posting_list()
    assert bytes(pdf).startswith(b"%PDF-1.4")


@pytest.mark.skipif(not PostingReportPDFRenderer, reason="PDF generation support disabled")
def test_render_all_posting_docs(posting_list: PostingList, posting_card: PostingCard):
    posting_list.close_with_id(number=12345)
    shipping_labels_renderer = PostingReportPDFRenderer()
    shipping_labels = [ShippingLabelFactory.build(posting_card=posting_card) for _ in range(35)]
    for shipping_label in shipping_labels:
        posting_list.add_shipping_label(shipping_label)
    shipping_labels_renderer.set_posting_list(posting_list)
    pdf = shipping_labels_renderer.render()
    assert bytes(pdf).startswith(b"%PDF-1.4")
