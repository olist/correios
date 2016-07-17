from datetime import datetime, timedelta

from reportlab.graphics.barcode import createBarcodeDrawing
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus.flowables import Flowable

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

        canvas.rect(self.x1, self.y1, self.width, self.height)

        # logo
        logo = ImageReader(self.shipping_label.logo)
        canvas.drawImage(logo, self.x1 + 8 * mm, self.y2 - (27 * mm), width=25 * mm,
                         preserveAspectRatio=True, anchor="sw", mask="auto")

        # datagrid
        datagrid = createBarcodeDrawing("ECC200DataMatrix",
                                        value=self.shipping_label.get_datamatrix_info(),
                                        width=25 * mm, height=25 * mm)
        datagrid.drawOn(canvas, self.x1 + 40 * mm, self.y2 - (27 * mm))

        # canvas.rect(self.x1 + 8*mm, self.y2 - (25*mm), 1*mm, 1*mm, fill=1)
        # codes = ['Codabar', 'Code11', 'Code128', 'Code128Auto', 'EAN13', 'EAN5', 'EAN8', 'ECC200DataMatrix',
        #          'Extended39', 'Extended93', 'FIM', 'I2of5', 'ISBN', 'MSI', 'POSTNET', 'QR', 'Standard39',
        #          'Standard93', 'UPCA', 'USPS_4State']
        # canvas.setStrokeColor(colors.red)
        # canvas.rect(50, 50, 80 * mm, 18 * mm)
        # code = Code128("DL746686536BR", barWidth=0.5 * mm, barHeight=18 * mm)
        # code.drawOn(canvas, 50, 50)

        canvas.drawString(self.hmargin, self.vmargin, str(self.shipping_label.tracking_code))


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
        self.labels[0].drawOn(self.canvas, *self._label_position[0])
        # self.labels[1].drawOn(self.canvas, *self._label_position[1])
        # self.labels[2].drawOn(self.canvas, *self._label_position[2])
        # self.labels[3].drawOn(self.canvas, *self._label_position[3])
        self.draw_grid()

        self.canvas.showPage()
        self.canvas.save()
        # pages = []
        # for group_start in range(0, len(self.labels), self.labels_per_page):
        #     group = self.labels[group_start:group_start + self.labels_per_page]
        #     group = (group + [None] * self.labels_per_page)[:self.labels_per_page]
        #     pages.append(group)
        #
        # tables = []
        # for page in pages:
        #     matrix = [(page[0], page[1]),
        #               (page[2], page[3])]
        #     table = Table(matrix, colWidths=self.label_width, rowHeights=self.label_height, style=[
        #         ('LINEBEFORE', (-1, 0), (-1, -1), 0.1, colors.gray),
        #         ('LINEABOVE', (0, -1), (-1, -1), 0.1, colors.gray),
        #         ('LEFTPADDING', (0, 0), (-1, -1), 0),
        #         ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        #         ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
        #         ('TOPPADDING', (0, 0), (-1, -1), 0),
        #     ])
        #     tables.append(table)
        # self.document.build(tables)
        return self.file


sender_address = AddressFactory()
receiver_address = AddressFactory()
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

shipping_label1 = ShippingLabel(
    posting_card=posting_card,
    sender=sender_address,
    receiver=receiver_address,
    service=40096,  # SERVICE_SEDEX_CODE
    tracking_code="PD12345678 BR",
)

ss = ShippingLabelPages()
ss.add_shipping_label(shipping_label1)
# ss.add_shipping_label("teste2")
# ss.add_shipping_label("teste3")
# ss.add_shipping_label("teste4")
# ss.add_shipping_label("teste5")
# ss.add_shipping_label("teste6")
# ss.add_shipping_label("teste7")
# ss.add_shipping_label("teste8")
# ss.add_shipping_label("teste9")
ss.render()
