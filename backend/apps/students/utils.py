import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from django.conf import settings

def generate_id_card_pdf(student):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=(3.375*inch, 2.125*inch))
    
    p.setFont("Helvetica-Bold", 12)
    p.drawString(10, 2.125*inch - 20, "Al Modina Model Madrasah")
    p.setFont("Helvetica", 8)
    p.drawString(10, 2.125*inch - 35, "ID Card")
    
    p.setFont("Helvetica", 10)
    p.drawString(10, 1.5*inch, f"Name: {student.name}")
    p.drawString(10, 1.3*inch, f"ID: {student.student_id}")
    dept = student.general_department.name_en if student.general_department else (student.islamic_department.name_en if student.islamic_department else "N/A")
    p.drawString(10, 1.1*inch, f"Class: {dept}")
    p.drawString(10, 0.9*inch, f"Session: {student.academic_year}")
    p.drawString(10, 0.7*inch, f"Guardian: {student.guardian_name}")
    p.drawString(10, 0.5*inch, f"Phone: {student.guardian_phone}")
    
    p.showPage()
    p.save()
    
    buffer.seek(0)
    return buffer.getvalue()
