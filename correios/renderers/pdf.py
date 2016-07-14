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


from io import BytesIO

from reportlab.lib.units import mm
from reportlab.pdfgen.canvas import Canvas

from correios.models.posting import ShippingLabel
from .base import AbstractDocument


class ShippingLabelRenderer(object):
    def __init__(self, shipping_label: ShippingLabel):
        self.shipping_label = shipping_label

    def render(self, canvas, x, y):
        canvas.rect(0, 0, 106 * mm, 138 * mm)
        # label = Drawing(106 * mm, 138 * mm)
        # label.add(Rect(0, 0, 106 * mm, 138 * mm))
        # canvas = Canvas("{}.pdf".format(shipping_label.tracking_code.code))
        # canvas.drawString(100, 100, "teste")
        # canvas.showPage()
        # return label


class Document(AbstractDocument):
    def render(self):
        pdf = BytesIO()
        canvas = Canvas(pdf)
        for shipping_label in self.shipping_labels:
            shipping_label_renderer = ShippingLabelRenderer(shipping_label)
            shipping_label_renderer.render(canvas, 0, 0)

        canvas.showPage()
        canvas.save()
        return pdf.getvalue()
