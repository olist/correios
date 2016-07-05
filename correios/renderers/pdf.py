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

from reportlab.pdfgen import canvas

from correios.models.posting import ShippingLabel


class ShippingLabelRenderer(object):
    def render(self, shipping_label: ShippingLabel):
        with BytesIO() as pdffile:
            label_canvas = canvas.Canvas(pdffile)
            label_canvas.drawString(100, 100, "teste")
            label_canvas.showPage()
            label_canvas.save()
            ret = pdffile.getvalue()

        with open("/Users/osantana/foo.pdf", "wb") as f:
            f.write(ret)

        return ret
