from io import BytesIO

from reportlab.graphics.barcode import createBarcodeDrawing
from reportlab.graphics.barcode.code128 import Code128
from reportlab.graphics.barcode.ecc200datamatrix import ECC200DataMatrix
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus import Table
from reportlab.platypus.flowables import Flowable

VERTICAL_SECURITY_MARGIN = 6  # pt


class ShippingLabelRenderer(Flowable):
    def __init__(self, shipping_label, width, height):
        super().__init__()
        self.shipping_label = shipping_label
        self.width = width
        self.height = height

    def wrap(self, *args):
        return self.width, self.height

    def draw(self):
        canvas = self.canv
        canvas.setLineWidth(0.1)

        codes = ['Codabar', 'Code11', 'Code128', 'Code128Auto', 'EAN13', 'EAN5', 'EAN8', 'ECC200DataMatrix',
                 'Extended39', 'Extended93', 'FIM', 'I2of5', 'ISBN', 'MSI', 'POSTNET', 'QR', 'Standard39',
                 'Standard93', 'UPCA', 'USPS_4State']

        datagrid = ECC200DataMatrix("asd")
        datagrid.drawOn(canvas, 200, 200)

        canvas.setStrokeColor(colors.red)
        canvas.rect(50, 50, 80 * mm, 18 * mm)

        code = Code128("DL746686536BR", barWidth=0.5 * mm, barHeight=18 * mm)
        code.drawOn(canvas, 50, 50)

        canvas.drawString(5 * mm, 5 * mm, self.shipping_label)


class ShippingLabelSheet:
    def __init__(self, page_size=A4, **kwargs):
        self.file = BytesIO()

        document_spec = {
            "pagesize": page_size,
            "leftMargin": 5 * mm,
            "rightMargin": 5 * mm,
            "topMargin": 5 * mm,
            "bottomMargin": 5 * mm,
        }
        document_spec.update(kwargs)
        self.document = SimpleDocTemplate("phello.pdf", **document_spec)
        self.labels_per_page = 4
        self.label_width = self.document.width / 2
        self.label_height = self.document.height / 2 - VERTICAL_SECURITY_MARGIN
        self.labels = []

    def add_shipping_label(self, shipping_label):
        label = ShippingLabelRenderer(shipping_label, self.label_width, self.label_height)
        self.labels.append(label)

    def render(self):
        pages = []
        for group_start in range(0, len(self.labels), self.labels_per_page):
            group = self.labels[group_start:group_start + self.labels_per_page]
            group = (group + [None] * self.labels_per_page)[:self.labels_per_page]
            pages.append(group)

        tables = []
        for page in pages:
            matrix = [(page[0], page[1]),
                      (page[2], page[3])]
            table = Table(matrix, colWidths=self.label_width, rowHeights=self.label_height, style=[
                ('LINEBEFORE', (-1, 0), (-1, -1), 0.1, colors.gray),
                ('LINEABOVE', (0, -1), (-1, -1), 0.1, colors.gray),
                ('LEFTPADDING', (0, 0), (-1, -1), 0),
                ('RIGHTPADDING', (0, 0), (-1, -1), 0),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
                ('TOPPADDING', (0, 0), (-1, -1), 0),
            ])
            tables.append(table)
        self.document.build(tables)
        return self.file


ss = ShippingLabelSheet()
ss.add_shipping_label("teste1")
# ss.add_shipping_label("teste2")
# ss.add_shipping_label("teste3")
# ss.add_shipping_label("teste4")
# ss.add_shipping_label("teste5")
# ss.add_shipping_label("teste6")
# ss.add_shipping_label("teste7")
# ss.add_shipping_label("teste8")
# ss.add_shipping_label("teste9")
ss.render()
