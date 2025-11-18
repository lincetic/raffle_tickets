import io
import random
from pathlib import Path
from datetime import date

import qrcode
from PIL import Image
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader


# =====================================================
#   CORE PUBLIC FUNCTION
# =====================================================

def render_tickets_pdf(
    tickets,
    output_path: str,
    logo_path: str = None,
    basket_path: str = None,
    orientation="A4",
):
    """
    Render all tickets into a PDF file.
    """
    page_size = landscape(A4) if orientation == "landscape" else A4
    c = canvas.Canvas(output_path, pagesize=page_size)
    page_w, page_h = page_size

    # Ticket geometry
    ticket_w = 14 * cm
    ticket_h = 7 * cm

    margin_x = 0.5 * cm
    margin_y = 0.5 * cm
    spacing_x = 0.5 * cm
    spacing_y = 0.2 * cm

    # Grid (how many tickets fit)
    cols = int((page_w - 2 * margin_x + spacing_x) // (ticket_w + spacing_x))
    rows = int((page_h - 2 * margin_y + spacing_y) // (ticket_h + spacing_y))
    per_page = cols * rows

    # Preload images (scaled)
    logo_data = load_and_scale_image(logo_path, target_height_cm=1.5) if logo_path else None
    basket_data = load_and_scale_image(basket_path, target_height_cm=3.0) if basket_path else None

    total = len(tickets)

    for i, (ticket_id, participant) in enumerate(tickets):
        index_on_page = i % per_page

        col = index_on_page % cols
        row = index_on_page // cols

        x = margin_x + col * (ticket_w + spacing_x)
        y = page_h - margin_y - (row + 1) * ticket_h - row * spacing_y

        draw_ticket(c, x, y, ticket_w, ticket_h, ticket_id, participant, logo_data, basket_data)

        if (i + 1) % per_page == 0 and i + 1 < total:
            c.showPage()

    c.save()


# =====================================================
#   DRAWING HELPERS
# =====================================================

def draw_ticket(c, x, y, w, h, ticket_id, participant, logo_data=None, basket_data=None):
    """Draws a single ticket."""
    draw_ticket_outline(c, x, y, w, h)
    draw_cut_line(c, x, y, h)

    if logo_data:
        draw_logo_pair(c, x, y, w, h, logo_data)

    if basket_data:
        draw_basket(c, x, y, basket_data)

    draw_text_blocks(c, x, y, w, h, ticket_id)
    draw_participant_vertical(c, x, y, participant)
    draw_qr_codes(c, x, y, w, h, ticket_id)


# -----------------------------------------------------
#   Small Sublayers
# -----------------------------------------------------

def draw_ticket_outline(c, x, y, w, h):
    c.roundRect(x, y, w, h, radius=0, stroke=1, fill=0)


def draw_cut_line(c, x, y, h):
    cut_x = x + 60
    c.setDash(2, 4)
    c.line(cut_x, y, cut_x, y + h)
    c.setDash()


def draw_logo_pair(c, x, y, w, h, logo_data):
    img, iw_pt, ih_pt = logo_data

    # Left bottom
    c.drawImage(img, x + 10, y + 10, width=iw_pt, height=ih_pt, mask='auto')

    # Right top
    c.drawImage(img, x + w - iw_pt - 10, y + h - ih_pt - 10,
                width=iw_pt, height=ih_pt, mask='auto')


def draw_basket(c, x, y, basket_data):
    img, iw_pt, ih_pt = basket_data
    c.drawImage(img, x + 70, y + 50,
                width=iw_pt, height=ih_pt,
                mask='auto')


def draw_text_blocks(c, x, y, w, h, ticket_id):
    title = "SORTEO DE NAVIDAD"
    current_year = date.today().year
    description = (
        f"Para resultar premiado, su número deberá coincidir con las {len(ticket_id)} últimas\n"
        f"cifras del sorteo de la Lotería de Navidad del 22 de diciembre de {current_year}"
    )

    c.setFont("Helvetica-Bold", 18)
    c.drawString(x + 70, y + h - 30, title)

    c.setFont("Helvetica-Bold", 16)
    ticket_str = f"#{ticket_id}"
    c.drawString(x + 10, y + h - 20, ticket_str)
    c.drawString(x + 70, y + 10, ticket_str)

    text_obj = c.beginText(x + 70, y + 40)
    text_obj.setFont("Helvetica-Bold", 8)
    text_obj.setLeading(10)
    text_obj.textLines(description)
    c.drawText(text_obj)


def draw_participant_vertical(c, x, y, participant):
    """Writes participant vertically at the left side."""
    if not participant:
        return

    c.saveState()
    c.translate(x + 15, y + 60)
    c.rotate(90)
    c.setFont("Helvetica", 10)
    c.drawString(0, 0, participant)
    c.restoreState()


def draw_qr_codes(c, x, y, w, h, ticket_id):
    """Generates and draws two QR codes."""
    key_secret = random.randint(1000, 9999)
    payload = f"?{ticket_id} - {key_secret}"

    qr_img, qr_w, qr_h = make_qr_image(payload)

    # Bottom-right
    c.drawImage(qr_img, x + w - qr_w - 5, y + 5, width=qr_w, height=qr_h)

    # Top-left
    c.drawImage(qr_img, x + 5, y + h - qr_h - 30, width=qr_w, height=qr_h)


# =====================================================
#   IMAGE HELPERS
# =====================================================

def load_and_scale_image(path: str, target_height_cm: float | None = None):
    """Load image and return (ImageReader, width_pt, height_pt) scaled."""
    img = Image.open(Path(path)).convert("RGBA")
    iw, ih = img.size

    dpi = img.info.get("dpi", (72, 72))[0] or 72
    iw_pt = iw * 72 / dpi
    ih_pt = ih * 72 / dpi

    if target_height_cm:
        target_h = target_height_cm * cm
        scale = target_h / ih_pt
        iw_pt *= scale
        ih_pt *= scale

    return ImageReader(img), iw_pt, ih_pt


# =====================================================
#   QR GENERATOR
# =====================================================

def make_qr_image(payload, size_cm=1.5):
    qr = qrcode.make(payload)
    img = qr.convert("RGB")
    size_pt = size_cm * cm
    return ImageReader(img), size_pt, size_pt
