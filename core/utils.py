# utils.py
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from django.conf import settings
import os

def generate_pdf_pass(student, month, year, town):
    pdf_filename = f"{student.user.username}_bus_pass_{month}_{year}.pdf"
    pdf_path = os.path.join(settings.MEDIA_ROOT, pdf_filename)

    c = canvas.Canvas(pdf_path, pagesize=A4)
    width, height = A4

    # Title
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(width/2, height - 50, "QuickPass - Student Bus Pass")

    # --- Info block (left side) ---
    c.setFont("Helvetica", 12)
    left_x = 80
    top_y = height - 120
    line_gap = 20

    c.drawString(left_x, top_y, f"Name: {student.full_name}")
    c.drawString(left_x, top_y - line_gap, f"Username: {student.user.username}")
    c.drawString(left_x, top_y - 2*line_gap, f"Course: {student.course}")
    c.drawString(left_x, top_y - 3*line_gap, f"Academic Year: {student.academic_year}")
    c.drawString(left_x, top_y - 4*line_gap, f"Town: {town.name}")
    c.drawString(left_x, top_y - 5*line_gap, f"Price: Rs.{town.price}")
    c.drawString(left_x, top_y - 6*line_gap, f"Month: {month} {year}")

    # --- Student Photo (right side, aligned with info) ---
    if student.photo:
        photo_path = os.path.join(settings.MEDIA_ROOT, str(student.photo))
        if os.path.exists(photo_path):
            photo_width = 180
            photo_height = 200
            photo_x = width - photo_width - 100
            photo_y = top_y - photo_height + 40  # align vertically with info block
            c.drawImage(photo_path, photo_x, photo_y,
                        width=photo_width, height=photo_height,
                        preserveAspectRatio=True, mask='auto')

    # --- Clerk signature (bottom left) ---
    c.setFont("Helvetica-Oblique", 12)
    c.drawString(left_x, 100, "Clerk Sign: __________________")

    c.showPage()
    c.save()
    return pdf_path
