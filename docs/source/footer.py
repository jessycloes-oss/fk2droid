import sys
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import io
pdfmetrics.registerFont(TTFont('DV', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'))
src, label = sys.argv[1], sys.argv[2]
r = PdfReader(src); w = PdfWriter(); n = len(r.pages)
for i, p in enumerate(r.pages):
    W, H = float(p.mediabox.width), float(p.mediabox.height)
    b = io.BytesIO(); c = canvas.Canvas(b, pagesize=(W, H)); c.setFont('DV', 7.5); c.setFillGray(0.45)
    c.drawCentredString(W/2, 22, f"{label} — page {i+1}/{n} — non affilié à Google, Honda ni Carlinkit")
    c.save(); b.seek(0)
    p.merge_page(PdfReader(b).pages[0]); w.add_page(p)
w.write(src)
