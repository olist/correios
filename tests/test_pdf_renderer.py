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

from correios.models.data import SERVICE_SEDEX
from correios.models.posting import ShippingLabel
from correios.renderers.pdf import Document


TESTDIR = os.path.dirname(__file__)


def test_render_basic_shipping_label(default_posting_card, sender_address, receiver_address, tracking_code):
    shipping_label = ShippingLabel(
        posting_card=default_posting_card,
        sender=sender_address,
        receiver=receiver_address,
        service=SERVICE_SEDEX,
        tracking_code=tracking_code,
        order="123",
        invoice="321",
        volume=(1, 1),
        weight=100,
    )

    document = Document()
    # document.add_posting_list(plp)
    document.add_shipping_label(shipping_label)

    pdf = document.render()
    filename = os.path.join(TESTDIR, "test.pdf")
    with open(filename, "wb") as fp:
        fp.write(pdf)

    # from subprocess import run
    # run("open -a Preview {}".format(filename), shell=True)
