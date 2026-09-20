from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def generate_id_card_pdf(teacher):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="ID_Card_{teacher.teacher_id}.pdf"'
    
    p = canvas.Canvas(response, pagesize=letter)
    p.drawString(100, 750, f"ID Card - {teacher.name}")
    p.drawString(100, 730, f"Teacher ID: {teacher.teacher_id}")
    p.drawString(100, 710, f"Designation: {teacher.designation}")
    p.drawString(100, 690, f"Phone: {teacher.phone}")
    
    p.showPage()
    p.save()
    return response

def generate_salary_slip_pdf(teacher, month, year, payment):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Salary_Slip_{teacher.teacher_id}_{month}_{year}.pdf"'
    
    p = canvas.Canvas(response, pagesize=letter)
    p.drawString(100, 750, f"Salary Slip - {month}/{year}")
    p.drawString(100, 730, f"Name: {teacher.name}")
    p.drawString(100, 710, f"Teacher ID: {teacher.teacher_id}")
    p.drawString(100, 690, f"Amount: {payment.amount}")
    p.drawString(100, 670, f"Date: {payment.paid_date}")
    
    p.showPage()
    p.save()
    return response
