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

from correios.models.posting import ShippingLabel, PostingList
from exceptions import RendererError

VERTICAL_SECURITY_MARGIN = 6  # pt


class PDF:
    def __init__(self, page_size):
        self._file = BytesIO()
        self.canvas = Canvas(self._file, pagesize=page_size)
        self._saved = False

    @property
    def file(self) -> BytesIO:
        if not self._saved:
            self.canvas.save()
            self._saved = True

        self._file.seek(0)
        return self._file

    def save(self, filename):
        with open(filename, "wb") as pdf_file:
            pdf_file.write(self.file.read())

    def __bytes__(self):
        return self.file.getvalue()


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
    def __init__(self, page_size=pagesizes.A4, shipping_labels_margin=(0, 0), posting_list_margin=(5 * mm, 5 * mm)):
        self.labels = []
        self._tracking_codes = set()

        self.page_size = page_size
        self.page_width = page_size[0]
        self.page_height = page_size[1]

        self.posting_list = None
        self.posting_list_margin = posting_list_margin

        self.shipping_labels_margin = shipping_labels_margin
        self.shipping_labels_width = self.page_width - (2 * shipping_labels_margin[0])
        self.shipping_labels_height = self.page_height - (2 * shipping_labels_margin[1])
        self.col_size = self.shipping_labels_width / 2
        self.row_size = self.shipping_labels_height / 2
        self._label_position = (
            (shipping_labels_margin[0], self.page_height / 2),
            (shipping_labels_margin[0] + self.col_size, self.page_height / 2),
            (shipping_labels_margin[0], shipping_labels_margin[1]),
            (shipping_labels_margin[0] + self.col_size, shipping_labels_margin[1]),
        )

    def set_posting_list(self, posting_list: PostingList):
        self.posting_list = posting_list
        for shipping_label in posting_list.shipping_labels.values():
            self.add_shipping_label(shipping_label)

    def add_shipping_label(self, shipping_label: ShippingLabel):
        if str(shipping_label.tracking_code) in self._tracking_codes:
            raise RendererError("Shipping Label {!s} already added".format(shipping_label.tracking_code))
        label = ShippingLabelFlowable(shipping_label, self.col_size, self.row_size)
        self.labels.append(label)
        self._tracking_codes.add(str(shipping_label.tracking_code))

    def draw_grid(self, canvas):
        canvas.setLineWidth(0.2)
        canvas.setStrokeColor(colors.gray)
        canvas.line(self.hmargin, self.page_height / 2, self.shipping_labels_width + self.hmargin,
                    self.page_height / 2)
        canvas.line(self.page_width / 2, self.vmargin, self.page_width / 2,
                    self.shipping_labels_height + self.vmargin, )

    def render_posting_list(self, pdf=None) -> PDF:
        if pdf is None:
            pdf = PDF(self.page_size)
        canvas = pdf.canvas

        hmargin, vmargin = 5 * mm, 5 * mm
        width, height = self.shipping_labels_width - 10 * mm, self.shipping_labels_height - 10 * mm
        x1, y1, x2, y2 = 5 * mm, 5 * mm, width + 5 * mm, height + 5 * mm

        canvas.rect(x1, y1, self.shipping_labels_width, self.shipping_labels_height)
        logo = ImageReader(self.posting_list.logo)
        canvas.drawImage(logo, x1 + 5 * mm, y2, width=25 * mm,
                         preserveAspectRatio=True, anchor="sw", mask="auto")

        # TODO
        canvas.showPage()
        return pdf

    def render_labels(self, pdf=None) -> PDF:
        if pdf is None:
            pdf = PDF(self.page_size)

        canvas = pdf.canvas

        pos = len(self._label_position) - 1
        for i, label in enumerate(self.labels):
            pos = i % len(self._label_position)
            self.labels[i].drawOn(canvas, *self._label_position[pos])
            if pos == len(self._label_position) - 1:
                self.draw_grid(canvas)
                canvas.showPage()

        if pos != len(self._label_position) - 1:
            self.draw_grid(canvas)
            canvas.showPage()

        return pdf

    def render_label(self, shipping_label: ShippingLabel) -> PDF:
        pdf = PDF(self.page_size)
        canvas = pdf.canvas

        label = ShippingLabelFlowable(shipping_label, self.col_size, self.row_size)
        label.drawOn(canvas, *self._label_position[0])

        self.draw_grid(canvas)

        canvas.showPage()

        return pdf

    def render(self) -> PDF:
        pdf = PDF(self.page_size)
        self.render_posting_list(pdf)
        self.render_labels(pdf)
        return pdf
