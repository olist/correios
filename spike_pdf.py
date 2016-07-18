from datetime import datetime, timedelta

from reportlab.graphics.barcode import createBarcodeDrawing
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Paragraph
from reportlab.platypus.flowables import Flowable

from correios.models.data import SERVICE_SEDEX, SERVICE_SEDEX10
from correios.models.posting import ShippingLabel
from correios.models.user import PostingCard, Contract
from tests.conftest import AddressFactory

VERTICAL_SECURITY_MARGIN = 6  # pt


class ShippingLabelRenderer(Flowable):
    def __init__(self, shipping_label: ShippingLabel, total_width, label_height, hmargin=5 * mm, vmargin=5 * mm):
        super().__init__()
        self.shipping_label = shipping_label

        self.label_width = total_width
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

        text = Paragraph("{}<br/>{}".format(self.shipping_label.get_volume(),
                                            self.shipping_label.get_weight()),
                         style=label_style)
        text.wrap(25 * mm, 14)
        text.drawOn(canvas, self.x1 + 70 * mm, self.y2 - (28 * mm) - 14)

        # tracking
        canvas.setFont("Helvetica-Bold", 10)
        canvas.drawCentredString(self.x1 + 42.5 * mm, self.y2 - 40 * mm,
                                 self.shipping_label.get_tracking_code())
        code = createBarcodeDrawing("Code128", value=self.shipping_label.get_tracking_code(),
                                    width=95 * mm, height=18 * mm)
        code.drawOn(canvas, 0, self.y2 - (59 * mm))  # Code 128 already include horizontal margins

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


class ShippingLabelPages:
    def __init__(self, page_size=A4, hmargin=0, vmargin=0):
        # self.file = BytesIO()
        self.file = open("phello.pdf", "wb")
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

    def add_shipping_label(self, shipping_label):
        label = ShippingLabelRenderer(shipping_label, self.col_size, self.row_size)
        self.labels.append(label)

    def draw_grid(self):
        self.canvas.setLineWidth(0.1)
        self.canvas.setStrokeColor(colors.gray)
        self.canvas.line(self.hmargin, self.page_height / 2, self.width + self.hmargin,
                         self.page_height / 2)
        self.canvas.line(self.page_width / 2, self.vmargin, self.page_width / 2,
                         self.height + self.vmargin, )

    def render(self):
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
        return self.file


contract = Contract(
    number=9912208555,
    customer_code=279311,
    direction_code=10,
    direction="DR - BRASÍLIA",
    status_code="A",
    start_date=datetime.now(),
    end_date=datetime.now() + timedelta(days=5),
    posting_cards=[]
)

posting_card = PostingCard(
    contract=contract,
    number=57018901,
    administrative_code=8082650,
    start_date=datetime.now(),
    end_date=datetime.now() + timedelta(days=5),
    status=1,
    status_code="I",
    unit=8,
)

ShippingLabel.weight_template = "Peso (g): <b>{!s}</b>"
ShippingLabel.invoice_template = "NF: {!s}"
ShippingLabel.order_template = "Ped.: <font size=6>{!s}</font>"
ShippingLabel.contract_number_template = "Contrato: <b>{!s}</b>"
ShippingLabel.service_name_template = "<b>{!s}</b>"
ShippingLabel.volume_template = "Volume: {!s}/{!s}"

shipping_label1 = ShippingLabel(
    posting_card=posting_card,
    sender=AddressFactory(),
    receiver=AddressFactory(),
    service=SERVICE_SEDEX,
    tracking_code="PD12345678 BR",
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
    tracking_code="PD12345555 BR",
    invoice="654",
    order="OLT123XXXXX",
    weight=150,
)

ss = ShippingLabelPages()
ss.add_shipping_label(shipping_label1)
ss.add_shipping_label(shipping_label2)
ss.add_shipping_label(shipping_label2)
ss.add_shipping_label(shipping_label1)
ss.add_shipping_label(shipping_label1)
ss.render()
