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


from correios.models.data import SERVICE_SEDEX
from correios.models.posting import ShippingLabel
from correios.renderers.pdf import ShippingLabelRenderer


def test_render_basic_shipping_label(sender_address, receiver_address, tracking_code):
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

    renderer = ShippingLabelRenderer()

    pdf = renderer.render(shipping_label)
    assert pdf == "wat?"
