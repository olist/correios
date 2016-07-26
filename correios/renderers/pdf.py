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

from reportlab.graphics.barcode import createBarcodeDrawing
from reportlab.lib import colors, pagesizes
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Flowable, Paragraph

from correios.models.posting import ShippingLabel

VERTICAL_SECURITY_MARGIN = 6  # pt


class ShippingLabelFlowable(Flowable):
    def __init__(self, shipping_label: ShippingLabel, label_width, label_height, hmargin=5 * mm, vmargin=5 * mm):
        super().__init__()
        self.shipping_label = shipping_label

        self.label_width = label_width
        self.hmargin = hmargin
        self.width = self.label_width - (2 * hmargin)

        self.label_height = label_height
        self.vmargin = vmargin
        self.height = self.label_height - (2 * vmargin)

        self.x1 = self.hmargin
        self.y1 = self.vmargin
        self.x2 = self.hmargin + self.width
        self.y2 = self.vmargin + self.height

    def wrap(self, *args):
        return self.label_width, self.label_height

    def draw(self):
        canvas = self.canv
        canvas.setLineWidth(0.1)

        # logo
        logo = ImageReader(self.shipping_label.logo)
        canvas.drawImage(logo, self.x1 + 5 * mm, self.y2 - (27 * mm), width=25 * mm,
                         preserveAspectRatio=True, anchor="sw", mask="auto")

        # datagrid
        datagrid = createBarcodeDrawing("ECC200DataMatrix",
                                        value=self.shipping_label.get_datamatrix_info(),
                                        width=25 * mm, height=25 * mm)
        datagrid.drawOn(canvas, self.x1 + 40 * mm, self.y2 - (27 * mm))

        # symbol
        symbol = ImageReader(self.shipping_label.symbol)
        canvas.drawImage(symbol, self.x1 + 70 * mm, self.y2 - (27 * mm), width=25 * mm,
                         preserveAspectRatio=True, anchor="sw", mask="auto")

        # header labels
        label_style = ParagraphStyle(name="label", fontName="Helvetica", fontSize=7, leading=8)
        text = Paragraph("{}<br/>{}".format(self.shipping_label.get_invoice(),
                                            self.shipping_label.get_order()),
                         style=label_style)
        text.wrap(25 * mm, 14)
        text.drawOn(canvas, self.x1 + 5 * mm, self.y2 - (28 * mm) - 14)

        text = Paragraph("{}<br/>{}".format(self.shipping_label.get_contract_number(),
                                            self.shipping_label.get_service_name()),
                         style=label_style)
        text.wrap(25 * mm, 14)
        text.drawOn(canvas, self.x1 + 40 * mm, self.y2 - (28 * mm) - 14)

        text = Paragraph("{}<br/>{}".format(self.shipping_label.get_package_sequence(),
                                            self.shipping_label.get_weight()),
                         style=label_style)
        text.wrap(25 * mm, 14)
        text.drawOn(canvas, self.x1 + 70 * mm, self.y2 - (28 * mm) - 14)

        # tracking
        canvas.setFont("Helvetica-Bold", 10)
        canvas.drawCentredString(self.x1 + 42.5 * mm, self.y2 - 40 * mm,
                                 self.shipping_label.get_tracking_code())
        code = createBarcodeDrawing("Code128", value=str(self.shipping_label.tracking_code),
                                    width=75 * mm, height=18 * mm, quiet=0)
        code.drawOn(canvas, 10 * mm, self.y2 - (59 * mm))  # Code 128 already include horizontal margins

        # extra services (first three)
        first_row = self.y2 - (40 * mm) - 10  # font-size=10pt
        for extra_service in self.shipping_label.extra_services:
            canvas.drawString(self.x2 - (10 * mm), first_row, extra_service.code)
            first_row -= 14

        # receipt
        receipt_style = ParagraphStyle(name="label", fontName="Helvetica", fontSize=8, leading=14)
        text = Paragraph(self.shipping_label.receipt_template, style=receipt_style)
        text.wrap(self.width - (10 * mm), 28)
        text.drawOn(canvas, self.x1 + (5 * mm), self.y2 - (60 * mm) - 28)

        # sender header
        canvas.setFillColor(colors.black)
        canvas.line(self.x1, self.y2 - (70 * mm), self.x2, self.y2 - (70 * mm))
        width = stringWidth(self.shipping_label.sender_header, "Helvetica", 10) + 2
        canvas.rect(self.x1, self.y2 - (70 * mm) - 14, width, 14, fill=True)

        canvas.setFont("Helvetica", 9)
        canvas.setFillColor(colors.white)
        canvas.drawString(self.x1 + 4, self.y2 - (70 * mm) - 10, self.shipping_label.sender_header)

        carrier_logo = ImageReader(self.shipping_label.carrier_logo)
        canvas.drawImage(carrier_logo, self.x2 - 20 * mm, self.y2 - (70 * mm) - 12, height=10,
                         preserveAspectRatio=True, anchor="sw", mask="auto")

        # receiver
        receiver_style = ParagraphStyle("receiver", fontName="Helvetica", fontSize=10, leading=15)
        text = Paragraph(self.shipping_label.get_receiver_data(), style=receiver_style)
        text.wrap(self.width, 22 * mm)
        text.drawOn(canvas, self.x1 + 5 * mm, self.y2 - (98 * mm))

        # receiver zip barcode
        code = createBarcodeDrawing("Code128", value=str(self.shipping_label.receiver.zip_code),
                                    width=50 * mm, height=18 * mm)
        code.drawOn(canvas, 0, self.y2 - (117 * mm))

        # text
        text_style = ParagraphStyle("text", fontName="Helvetica", fontSize=10)
        text = Paragraph(self.shipping_label.text, style=text_style)
        width = self.x2 - (self.x1 + (45 * mm))
        text.wrap(width, 18 * mm)
        text.breakLines(width)
        text.drawOn(canvas, self.x1 + (45 * mm), self.y2 - (98 * mm))

        # sender
        canvas.line(self.x1, self.y2 - (118 * mm), self.x2, self.y2 - (118 * mm))
        sender_style = ParagraphStyle("sender", fontName="Helvetica", fontSize=9)
        text = Paragraph(self.shipping_label.get_sender_data(), style=sender_style)
        text.wrap(self.width, 22 * mm)
        text.drawOn(canvas, self.x1 + 5 * mm, self.y1 + 2 * mm)

        # border
        canvas.rect(self.x1, self.y1, self.width, self.height)


class ShippingLabelsPDFRenderer:
    def __init__(self, page_size=pagesizes.A4, hmargin=0, vmargin=0):
        self.file = BytesIO()
        self.canvas = Canvas(self.file, pagesize=page_size)
        self.labels = []

        self.page_width = page_size[0]
        self.hmargin = hmargin
        self.width = self.page_width - (2 * hmargin)

        self.page_height = page_size[1]
        self.vmargin = vmargin
        self.height = self.page_height - (2 * vmargin)

        self.col_size = self.width / 2
        self.row_size = self.height / 2

        self._label_position = (
            (self.hmargin, self.page_height / 2),
            (self.hmargin + self.col_size, self.page_height / 2),
            (self.hmargin, self.vmargin),
            (self.hmargin + self.col_size, self.vmargin),
        )

    def add_shipping_label(self, shipping_label: ShippingLabel):
        label = ShippingLabelFlowable(shipping_label, self.col_size, self.row_size)
        self.labels.append(label)

    def draw_grid(self):
        self.canvas.setLineWidth(0.2)
        self.canvas.setStrokeColor(colors.gray)
        self.canvas.line(self.hmargin, self.page_height / 2, self.width + self.hmargin,
                         self.page_height / 2)
        self.canvas.line(self.page_width / 2, self.vmargin, self.page_width / 2,
                         self.height + self.vmargin, )

    def render(self) -> BytesIO:
        pos = len(self._label_position) - 1
        for i, label in enumerate(self.labels):
            pos = i % len(self._label_position)
            self.labels[i].drawOn(self.canvas, *self._label_position[pos])
            if pos == len(self._label_position) - 1:
                self.draw_grid()
                self.canvas.showPage()

        if pos != len(self._label_position) - 1:
            self.draw_grid()
            self.canvas.showPage()

        self.canvas.save()
        self.file.seek(0)
        return self.file
